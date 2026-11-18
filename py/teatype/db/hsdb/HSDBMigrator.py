# Copyright (C) 2024-2026 Burak Günaydin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# Standard-library imports
import copy
import glob
import importlib.util
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, NamedTuple

# Third-party imports
from teatype.db.hsdb.RawFileStructure import _FS, _FSProxy
from teatype.db.hsdb.core.HSDBMigration import HSDBMigration
from teatype.io import file
from teatype.logging import hint, log, success, warn
from teatype.toolkit import dt

_FILE_NAME = re.compile(r'^(\d+)_(.+)\.py$')
_KINDS = ('changed', 'created', 'deleted', 'rejected')
_SAMPLES = 3 # Changed entries shown per collection in the report
_VALUE_WIDTH = 40

class HSDBMigrationError(RuntimeError):
    """
    A migration could not be loaded or applied. The database is either untouched or restored from its backup.
    """

class _MigrationFile(NamedTuple):
    id:int
    name:str
    stem:str
    path:str

def _stamp() -> str:
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def _short(value:object) -> str:
    text = json.dumps(value)
    return text if len(text) <= _VALUE_WIDTH else text[:_VALUE_WIDTH - 1] + '…'

def _describe(before:dict, after:dict) -> str:
    parts = []
    for key in sorted(before.keys() | after.keys()):
        if key not in before:
            parts.append(f'+{key}={_short(after[key])}')
        elif key not in after:
            parts.append(f'-{key}')
        elif before[key] != after[key]:
            parts.append(f'{key}: {_short(before[key])} -> {_short(after[key])}')
    return ', '.join(parts)

def _diff(before:dict, after:dict, rejected:dict) -> dict:
    """
    Per collection the entries that changed, were created, deleted or rejected between two {folder: {id: row}} states.
    """
    diff = {}
    for folder in sorted(before.keys() | after.keys() | rejected.keys()):
        old, new, gone = before.get(folder, {}), after.get(folder, {}), rejected.get(folder, {})
        entry = {'changed': {id: {'before': old[id], 'after': new[id]} for id in sorted(old.keys() & new.keys()) if old[id] != new[id]},
                 'created': {id: new[id] for id in sorted(new.keys() - old.keys())},
                 'deleted': {id: old[id] for id in sorted(old.keys() - new.keys() - gone.keys())},
                 'rejected': gone}
        if any(entry.values()):
            diff[folder] = entry
    return diff

def _read_json(file_path:str) -> object:
    try:
        with open(file_path) as stored_file:
            return json.load(stored_file)
    except (OSError, ValueError) as exc:
        raise HSDBMigrationError(f'Could not read {file_path}: {exc}') from exc

class HSDBMigrator:
    """
    Applies the pending migrations of a database to its raw files, before HybridStorage.restore() reads them.
    See README.md, section "Migrations".
    """
    def __init__(self, db_path:str, migrations_path:str, models:List[type], cold_mode:bool=False) -> None:
        self.cold_mode = cold_mode
        self.fs = _FSProxy(_FS, db_path)
        self.migrations_path = migrations_path
        self.models = models
        self.state_path = os.path.join(db_path, 'migrations.json')

    #############
    # Internals #
    #############

    def _discover(self) -> List[_MigrationFile]:
        found = {}
        for file_path in glob.glob(os.path.join(self.migrations_path, '*.py')):
            match = _FILE_NAME.match(os.path.basename(file_path))
            if not match:
                continue
            number = int(match[1])
            if number in found:
                raise HSDBMigrationError(f'Duplicate migration number {number}: {os.path.basename(found[number].path)} and {os.path.basename(file_path)}')
            found[number] = _MigrationFile(number, match[2], match[1] + '_' + match[2], file_path)
        return [found[number] for number in sorted(found)]

    def _state(self) -> list:
        return _read_json(self.state_path) if os.path.exists(self.state_path) else []

    def _pending(self) -> List[_MigrationFile]:
        migrations = self._discover()
        state = self._state()
        applied = {entry['id'] for entry in state}
        for entry in state:
            if entry['id'] not in {migration.id for migration in migrations}:
                warn(f'Applied migration {entry["id"]}_{entry["name"]} has no file in {self.migrations_path}')
        pending = [migration for migration in migrations if migration.id not in applied]
        if pending and applied and pending[0].id < max(applied):
            raise HSDBMigrationError(f'Migration {pending[0].stem} is pending but a later migration ({max(applied)}) was already applied, '
                                     'renumber it or rename it to a number above the applied ones')
        return pending

    def _report_drift(self, pending:int) -> None:
        """
        Compare the models/*.json of the last start with the current models (HSDB overwrites them afterwards).
        """
        flat = lambda schema: {**schema.get('attributes', {}), **schema.get('relations', {})}
        for model in self.models:
            stored_path = os.path.join(self.fs.models.path, f'{model.__name__}.json')
            if not os.path.exists(stored_path):
                continue
            old, new = flat(_read_json(stored_path)), flat(json.loads(json.dumps(model.schema())))
            changes = [*(f'+{key}' for key in sorted(new.keys() - old.keys())),
                       *(f'-{key}' for key in sorted(old.keys() - new.keys())),
                       *(f'~{key}' for key in sorted(key for key in old.keys() & new.keys() if old[key] != new[key]))]
            if not changes:
                continue
            summary = f'Model "{model.__name__}" changed ({", ".join(changes)})'
            if pending:
                hint(f'{summary}, {pending} pending migration(s) will run')
            else:
                warn(f'{summary} but there is no pending migration, entries that no longer fit are skipped at restore. '
                     f'Create a migration in {self.migrations_path}')

    def _load_data(self) -> dict:
        data = {}
        indexdb = self.fs.indexdb.path
        for folder in sorted(os.listdir(indexdb)) if os.path.isdir(indexdb) else []:
            file_paths = glob.glob(os.path.join(indexdb, folder, '*.json'))
            data[folder] = {Path(file_path).stem: _read_json(file_path) for file_path in file_paths}
        return data

    def _load_class(self, migration:_MigrationFile) -> type:
        module_name = f'hsdb_migration_{migration.stem}'
        try:
            spec = importlib.util.spec_from_file_location(module_name, migration.path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module # Some decorators (dataclasses) look the module up by name
            spec.loader.exec_module(module)
        except Exception as exc:
            raise HSDBMigrationError(f'Could not load migration {migration.path}: {exc!r}') from exc
        classes = [value for value in vars(module).values()
                   if isinstance(value, type) and issubclass(value, HSDBMigration) and value is not HSDBMigration and value.__module__ == module_name]
        if len(classes) != 1:
            raise HSDBMigrationError(f'{migration.path} must contain exactly one HSDBMigration subclass, found {len(classes)}')
        return classes[0]

    def _execute(self, migration:_MigrationFile, migration_class:type, data:dict) -> tuple:
        """
        Run the hook on a copy of `data`, returns (data after, diff). Nothing is written.
        """
        after = copy.deepcopy(data)
        instance = migration_class()
        instance._attach(after, [model.__name__ for model in self.models], migration.stem)
        try:
            instance.migrate()
            instance.validate()
            diff = _diff(data, after, instance._rejected)
            for folder, entry in diff.items():
                for id, row in [*((id, change['after']) for id, change in entry['changed'].items()), *entry['created'].items()]:
                    if not isinstance(row, dict) or row.get('id') != id:
                        raise ValueError(f'Entry "{id}" of "{folder}" is not a dict with its own id')
                    json.dumps(row)
        except Exception as exc:
            raise HSDBMigrationError(f'Migration {migration.stem} failed ({exc!r}), nothing was written, the data is untouched') from exc
        return after, diff

    def _report(self, migration:_MigrationFile, diff:dict, dry_run:bool) -> None:
        hint(f'Migration {migration.stem} {"would change" if dry_run else "changed"}:' if diff else f'Migration {migration.stem} changes nothing')
        for folder, entry in diff.items():
            log(f'  {folder}: ' + ', '.join(f'{len(entry[kind])} {kind}' for kind in _KINDS))
            for id, change in list(entry['changed'].items())[:_SAMPLES]:
                log(f'    {id[:12]}: {_describe(change["before"], change["after"])}')

    def _log(self, migration:_MigrationFile, status:str, diff:dict=None, error:str=None) -> None:
        """
        One json per migration run in logs/migrations. status: applied, dry_run, recorded_empty or failed.
        """
        log_path = os.path.join(self.fs.logs.migrations.path, f'{migration.stem}_{_stamp()}.json')
        entry = {'migration': migration.stem, 'status': status, 'timestamp': dt.now(), 'collections': diff or {}}
        if error:
            entry['error'] = error
        file.write(log_path, entry, force_format='json', prettify=True, create_parents=True)
        log(f'  Migration log written to {log_path}')

    def _record(self, migration:_MigrationFile) -> None:
        file.write(self.state_path,
                   [*self._state(), {'id': migration.id, 'name': migration.name, 'applied_at': dt.now()}],
                   force_format='json',
                   prettify=True)

    def _commit(self, migration:_MigrationFile, diff:dict) -> None:
        """
        Backup indexdb, write the changes and record the migration; any failure restores the backup.
        """
        indexdb = self.fs.indexdb.path
        os.makedirs(indexdb, exist_ok=True)
        backup = os.path.join(self.fs.backups.migration.path, f'{migration.stem}_{_stamp()}')
        shutil.copytree(indexdb, backup)
        rejectpile = []
        try:
            for folder, entry in diff.items():
                rows = {**{id: change['after'] for id, change in entry['changed'].items()}, **entry['created']}
                for id, row in rows.items():
                    file.write(os.path.join(indexdb, folder, f'{id}.json'), row, force_format='json', prettify=True)
                for id, rejection in entry['rejected'].items():
                    rejectpile.append(os.path.join(self.fs.rejectpile.indexdb.path, folder, f'{id}.json'))
                    file.write(rejectpile[-1], rejection, force_format='json', prettify=True)
                for id in [*entry['deleted'], *entry['rejected']]:
                    Path(indexdb, folder, f'{id}.json').unlink(missing_ok=True)
                if os.path.isdir(os.path.join(indexdb, folder)) and not os.listdir(os.path.join(indexdb, folder)):
                    os.rmdir(os.path.join(indexdb, folder))
            self._record(migration)
        except Exception as exc:
            shutil.rmtree(indexdb)
            shutil.copytree(backup, indexdb)
            for file_path in rejectpile:
                Path(file_path).unlink(missing_ok=True)
            raise HSDBMigrationError(f'Applying migration {migration.stem} failed ({exc!r}), indexdb was restored from {backup}') from exc

    ##############
    # Public API #
    ##############

    def run(self) -> None:
        """
        Run all pending migrations in number order. Raises HSDBMigrationError if one fails, SystemExit after a cold run.
        """
        pending = self._pending()
        self._report_drift(len(pending))
        if not pending:
            return
        data = self._load_data()
        dry_run = False # The first cold migration and everything after it is only simulated
        for migration in pending:
            try:
                migration_class = self._load_class(migration)
            except HSDBMigrationError as exc:
                self._log(migration, 'failed', error=str(exc))
                raise
            dry_run = dry_run or self.cold_mode or migration_class.cold_mode
            if not any(data.values()):
                hint(f'Migration {migration.stem}: no entries to migrate' + ('' if dry_run else ', recorded without running it'))
                if not dry_run:
                    self._record(migration)
                self._log(migration, 'dry_run' if dry_run else 'recorded_empty')
                continue
            try:
                data, diff = self._execute(migration, migration_class, data)
                self._report(migration, diff, dry_run)
                if not dry_run:
                    self._commit(migration, diff)
            except HSDBMigrationError as exc:
                self._log(migration, 'failed', error=str(exc))
                raise
            self._log(migration, 'dry_run' if dry_run else 'applied', diff)
            if not dry_run:
                success(f'Applied migration {migration.stem}')
        if dry_run:
            raise SystemExit('HSDB migrations: cold migration run finished, nothing was applied from the first cold migration on, remove cold_mode to apply')
