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
from abc import ABC, abstractmethod
from typing import Iterable, Iterator

# Third-party imports
from teatype.logging import log
from teatype.toolkit import dt, generate_id, kebabify

def _name(model:str|type) -> str:
    return model if isinstance(model, str) else model.__name__

class _HSDBTable:
    """
    One collection (the entries of one model) of the raw data a migration works on. Rows are the plain dicts
    of the json files, incl. id, created_at, updated_at and relation ids. Obtained via `HSDBMigration.table()`.
    """
    def __init__(self, migration:'HSDBMigration', folder:str) -> None:
        self._migration = migration
        self.folder = folder

    @property
    def _rows(self) -> dict:
        return self._migration._data.setdefault(self.folder, {})

    def __contains__(self, id:str) -> bool:
        return id in self._rows

    def __getitem__(self, id:str) -> dict:
        return self._rows[id]

    def __iter__(self) -> Iterator[dict]:
        return iter(list(self._rows.values())) # A copy, so rows can be deleted while looping

    def __len__(self) -> int:
        return len(self._rows)

    def get(self, id:str, default:dict=None) -> dict|None:
        return self._rows.get(id, default)

    def add_field(self, name:str, default:object=None) -> None:
        """
        Add `name` to every row that does not have it yet. `default` may be a callable(row).
        """
        for row in self:
            if name not in row:
                row[name] = default(row) if callable(default) else default

    def rename_field(self, old:str, new:str) -> None:
        for row in self:
            if old in row:
                if new in row:
                    raise ValueError(f'Row "{row["id"]}" of "{self.folder}" already has a field "{new}"')
                row[new] = row.pop(old)

    def remove_field(self, name:str) -> None:
        for row in self:
            row.pop(name, None)

    def transform(self, function) -> None:
        """
        Call function(row) for every row; it edits the row in place or returns a new dict that replaces it.
        """
        for row in self:
            result = function(row)
            if result is not None and result is not row:
                result.setdefault('id', row['id'])
                self._rows[row['id']] = result

    def create(self, data:dict, id:str=None) -> dict:
        """
        Add a row with a generated id (or `id`) and the current time as created_at/updated_at, unless given.
        """
        id = id or data.get('id') or generate_id()
        if any(id in rows for rows in self._migration._data.values()):
            raise ValueError(f'An entry with id "{id}" already exists')
        row = dict(data)
        row['id'] = id
        row.setdefault('created_at', dt.now())
        row.setdefault('updated_at', row['created_at'])
        self._rows[id] = row
        return row

    def delete(self, id:str) -> None:
        del self._rows[id]

    def reject(self, id:str, reason:str) -> None:
        """
        Take the row out of the database into rejectpile/indexdb/<folder>/<id>.json, together with the reason.
        """
        row = self._rows.pop(id)
        self._migration._rejected.setdefault(self.folder, {})[id] = {'reason': reason,
                                                                     'migration': self._migration.name,
                                                                     'rejected_at': dt.now(),
                                                                     'data': row}

    def rename(self, model:str) -> None:
        """
        Move the whole collection to another model name.
        """
        target = self._migration._kebab(_name(model))
        rows = self._migration._data.pop(self.folder, {})
        clash = rows.keys() & self._migration._data.get(target, {}).keys()
        if clash:
            raise ValueError(f'"{target}" already contains the ids {sorted(clash)}')
        self._migration._data.setdefault(target, {}).update(rows)
        self.folder = target

    def drop(self) -> None:
        self._migration._data.pop(self.folder, None)

class HSDBMigration(ABC):
    """
    Base class of a migration file (`<number>_<name>.py`, one subclass per file). Implement `migrate()` and edit the
    raw data through `table()`. All edits happen on an in-memory copy; the database is only touched after
    `migrate()` (and `validate()`) returned without exception, see HSDBMigrator.

    Set the class attribute `cold_mode = True` for a dry run: the result is only reported and logged, nothing is applied.
    """
    cold_mode:bool = False

    def _attach(self, data:dict, models:Iterable[str], name:str) -> None:
        self._data = data # {folder: {id: row}}
        self._models = set(models) # Names of the models the application passes to hsdb.init
        self._rejected = {} # {folder: {id: {reason, migration, rejected_at, data}}}
        self.name = name

    def _kebab(self, name:str) -> str:
        return kebabify(name, remove='-model', plural=True)

    def table(self, name:str|type) -> _HSDBTable:
        """
        Collection of a model by class name (or class). Also takes the raw folder name of a model that no longer exists.
        """
        name = _name(name)
        folder = self._kebab(name)
        if folder in self._data or name in self._models:
            return _HSDBTable(self, folder)
        if name in self._data:
            return _HSDBTable(self, name)
        raise KeyError(f'Unknown table "{name}", present: {self.tables()}')

    def tables(self) -> list:
        """
        Folder names of all collections that contain entries.
        """
        return sorted(folder for folder, rows in self._data.items() if rows)

    def log(self, message:str) -> None:
        log(f'[{self.name}] {message}')

    #########
    # Hooks #
    #########

    @abstractmethod
    def migrate(self) -> None:
        """
        Called once with the raw data loaded. Edit it via `self.table(...)`.
        """

    def validate(self) -> None:
        """
        Optional, called after `migrate()`. Raise to abort the migration.
        """
