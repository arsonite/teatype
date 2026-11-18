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
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

# Third-party imports
import pytest
from teatype.db.hsdb import HSDBMigrator as migrator_module
from teatype.db.hsdb.HSDBMigrator import HSDBMigrationError, HSDBMigrator
from teatype.db.hsdb.core import HSDBAttribute, HSDBModel
from teatype.io.tempdir import tempdir

# All data lives in a gitignored folder next to this file, never in /var/lib or /tmp
_SCRATCH = os.path.join(os.path.dirname(__file__), 'dist')

@pytest.fixture
def workspace():
    with tempdir(_SCRATCH) as folder:
        yield Path(folder)

class Note(HSDBModel):
    body = HSDBAttribute(str, required=True)
    pinned = HSDBAttribute(bool, required=True)

def _row(id:str, **fields) -> dict:
    return {**fields, 'id': id, 'created_at': '2026-01-01T00:00:00.000000+0000Z', 'updated_at': '2026-01-01T00:00:00.000000+0000Z'}

class Env:
    """
    A database folder plus a migrations folder in a temporary workspace.
    """
    def __init__(self, root:Path) -> None:
        self.db = root / 'db'
        self.migrations = root / 'migrations'
        self.migrations.mkdir()

    def write_rows(self, folder:str, *rows:dict) -> None:
        for row in rows:
            file_path = self.db / 'indexdb' / folder / f'{row["id"]}.json'
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(json.dumps(row, indent=4))

    def read(self, folder:str, id:str) -> dict:
        return json.loads((self.db / 'indexdb' / folder / f'{id}.json').read_text())

    def snapshot(self) -> dict:
        return {str(file.relative_to(self.db)): file.read_bytes() for file in (self.db / 'indexdb').rglob('*.json')}

    def migration(self, file_name:str, body:str='', *, cold:bool=False) -> None:
        source = ('from teatype.db.hsdb.core import HSDBMigration\n\n'
                  'class Migration(HSDBMigration):\n'
                  f'    cold_mode = {cold}\n'
                  '    def migrate(self):\n' + textwrap.indent(textwrap.dedent(body).strip() or 'pass', '        ') + '\n')
        (self.migrations / file_name).write_text(source)

    def state(self) -> list:
        state_path = self.db / 'migrations.json'
        return json.loads(state_path.read_text()) if state_path.exists() else []

    def run(self, models:list=None, cold_mode:bool=False) -> None:
        HSDBMigrator(str(self.db), str(self.migrations), models or [], cold_mode=cold_mode).run()

@pytest.fixture
def env(workspace):
    return Env(workspace)

#######################
# Discovery and state #
#######################

def test_pending_migrations_run_in_number_order_and_are_recorded_once(env):
    env.write_rows('notes', _row('a', order=[]))
    for number in (10, 2, 1):
        env.migration(f'{number:04d}_step_{number}.py', f"self.table('Note').transform(lambda row: row['order'].append({number}))")
    (env.migrations / '__init__.py').write_text('raise RuntimeError("must be ignored")')
    (env.migrations / 'helper.py').write_text('raise RuntimeError("must be ignored")')
    (env.migrations / 'notes.txt').write_text('ignored')

    env.run()
    assert env.read('notes', 'a')['order'] == [1, 2, 10]
    assert [(entry['id'], entry['name']) for entry in env.state()] == [(1, 'step_1'), (2, 'step_2'), (10, 'step_10')]
    assert all(entry['applied_at'] for entry in env.state())

    env.run() # Nothing pending anymore
    assert env.read('notes', 'a')['order'] == [1, 2, 10]
    assert len(env.state()) == 3

def test_missing_migrations_folder_is_silent(env):
    env.write_rows('notes', _row('a'))
    HSDBMigrator(str(env.db), str(env.migrations / 'nope'), []).run()
    assert env.state() == []

def test_duplicate_numbers_are_an_error(env):
    env.migration('0001_first.py')
    env.migration('1_other.py')
    with pytest.raises(HSDBMigrationError, match='Duplicate migration number 1'):
        env.run()

def test_pending_below_applied_refuses_and_missing_file_only_warns(env, monkeypatch):
    env.write_rows('notes', _row('a'))
    env.migration('0002_second.py')
    env.run()
    env.migration('0001_late.py')
    with pytest.raises(HSDBMigrationError, match='0001_late is pending'):
        env.run()

    (env.migrations / '0001_late.py').unlink()
    (env.migrations / '0002_second.py').unlink()
    warnings = []
    monkeypatch.setattr(migrator_module, 'warn', warnings.append)
    env.run()
    assert len(warnings) == 1 and '2_second' in warnings[0]

def test_exactly_one_subclass_per_file(env):
    env.write_rows('notes', _row('a'))
    (env.migrations / '0001_none.py').write_text('x = 1\n')
    with pytest.raises(HSDBMigrationError, match='exactly one'):
        env.run()

def test_empty_database_records_migrations_without_running_them(env):
    env.migration('0001_unknown_table.py', "self.table('OldThing').drop()") # Would raise on data that never existed
    env.run()
    assert [entry['id'] for entry in env.state()] == [1]

##############
# Operations #
##############

def test_all_table_operations(env):
    env.write_rows('notes', _row('a', text='one', legacy=1, tags='x'), _row('b', text='two', legacy=2, tags='y'), _row('c', text='bad'), _row('d', text='gone'))
    env.write_rows('old-things', _row('o1', size=1), _row('o2', size=2))
    env.write_rows('exercises', _row('e1', name='run'))
    env.write_rows('drops', _row('x1'))
    env.migration('0001_everything.py', """
        notes = self.table('Note')
        assert self.tables() == ['drops', 'exercises', 'notes', 'old-things']
        notes.rename_field('text', 'body')
        notes.remove_field('legacy')
        notes.add_field('pinned', False)
        notes.add_field('slug', lambda row: row['body'].upper())
        notes.add_field('tags', 'untouched')               # exists already, kept
        notes.transform(lambda row: row.update(size=len(row['body'])))
        notes.transform(lambda row: {**row, 'copy': True} if row['id'] == 'a' else None)  # returned dict replaces the row
        notes.delete('d')
        notes.reject('c', 'no good')
        created = notes.create({'body': 'fresh'})
        assert created['id'] and created['created_at'] == created['updated_at']
        notes.create({'body': 'chosen'}, id='mine')
        assert len(notes) == 4 and notes['a']['body'] == 'one' and notes.get('zzz') is None
        assert sorted(row['body'] for row in notes) == ['chosen', 'fresh', 'one', 'two']
        self.table('old-things').rename('Exercise')        # raw folder name of a model that no longer exists
        self.table('Exercise')
        self.table('Drop').drop()
    """)
    env.run()

    a = env.read('notes', 'a')
    assert a == {'body': 'one', 'tags': 'x', 'id': 'a', 'created_at': '2026-01-01T00:00:00.000000+0000Z',
                 'updated_at': '2026-01-01T00:00:00.000000+0000Z', 'pinned': False, 'slug': 'ONE', 'size': 3, 'copy': True}
    assert env.read('notes', 'b')['body'] == 'two' and 'legacy' not in env.read('notes', 'b')
    assert env.read('notes', 'mine')['body'] == 'chosen'
    assert not (env.db / 'indexdb' / 'notes' / 'd.json').exists() and not (env.db / 'indexdb' / 'notes' / 'c.json').exists()
    rejected = json.loads((env.db / 'rejectpile' / 'indexdb' / 'notes' / 'c.json').read_text())
    assert rejected['reason'] == 'no good' and rejected['data']['id'] == 'c' and rejected['migration'] == '0001_everything'
    assert env.read('exercises', 'o2')['size'] == 2 and env.read('exercises', 'e1')['name'] == 'run'
    assert not (env.db / 'indexdb' / 'old-things').exists() and not (env.db / 'indexdb' / 'drops').exists() # Emptied folders vanish
    backup, = (env.db / 'backups' / 'migration').iterdir()
    assert backup.name.startswith('0001_everything_') and json.loads((backup / 'notes' / 'a.json').read_text())['text'] == 'one'

def test_unknown_table_lists_the_present_ones(env):
    env.write_rows('notes', _row('a'))
    env.migration('0001_typo.py', "self.table('Nots')")
    with pytest.raises(HSDBMigrationError, match="Unknown table .Nots.*notes"):
        env.run()

###########
# Failure #
###########

@pytest.mark.parametrize('body', ["self.table('Note').remove_field('x'); raise RuntimeError('boom')",
                                  "self.table('Note').transform(lambda row: {'id': 'other'})",
                                  "self.table('Note').transform(lambda row: row.update(bad=object()))"])
def test_failing_hook_leaves_data_untouched(env, body):
    env.write_rows('notes', _row('a', x=1), _row('b', x=2))
    env.migration('0001_fails.py', body)
    before = env.snapshot()
    with pytest.raises(HSDBMigrationError, match='nothing was written, the data is untouched'):
        env.run()
    assert env.snapshot() == before
    assert env.state() == [] and not (env.db / 'backups').exists()

def test_commit_failure_restores_the_backup(env, monkeypatch):
    env.write_rows('notes', _row('a', x=1), _row('b', x=2), _row('c', x=3))
    env.migration('0001_commit_fails.py', "t = self.table('Note'); t.remove_field('x'); t.reject('c', 'r')")
    before = env.snapshot()
    real_write, calls = migrator_module.file.write, []
    def flaky_write(file_path, *args, **kwargs):
        calls.append(file_path)
        if len(calls) == 3: # Two entries and the rejection were written by then
            raise OSError('disk full')
        return real_write(file_path, *args, **kwargs)
    monkeypatch.setattr(migrator_module.file, 'write', flaky_write)
    with pytest.raises(HSDBMigrationError, match='indexdb was restored from'):
        env.run()
    monkeypatch.undo()
    assert len(calls) == 3
    assert env.snapshot() == before
    assert env.state() == [] and not list((env.db / 'rejectpile').rglob('*.json'))
    assert len(list((env.db / 'backups' / 'migration').iterdir())) == 1 # Kept for inspection

############
# Cold mode #
############

def test_cold_migration_applies_earlier_ones_simulates_the_rest_and_stops(env):
    env.write_rows('notes', _row('a', text='one'))
    env.migration('0001_real.py', "self.table('Note').rename_field('text', 'body')")
    env.migration('0002_cold.py', "self.table('Note').add_field('pinned', False); self.table('Note').create({'body': 'x'}, id='n')", cold=True)
    env.migration('0003_chained.py', "t = self.table('Note'); assert 'pinned' in t['a']; t.reject('n', 'why')") # Sees 0002 in memory

    with pytest.raises(SystemExit, match='nothing was applied'):
        env.run()
    assert [entry['id'] for entry in env.state()] == [1]
    assert 'pinned' not in env.read('notes', 'a') and env.read('notes', 'a')['body'] == 'one' # 0001 applied
    assert not (env.db / 'indexdb' / 'notes' / 'n.json').exists()
    assert len(list((env.db / 'backups' / 'migration').iterdir())) == 1 # Only the real migration backed up

    dumps = {file.name.split('_', 2)[1]: json.loads(file.read_text()) for file in (env.db / 'dumps' / 'migrations').iterdir()}
    assert set(dumps) == {'cold', 'chained'}
    changed = dumps['cold']['collections']['notes']['changed']['a']
    assert changed['after']['pinned'] is False and 'pinned' not in changed['before']
    assert dumps['cold']['collections']['notes']['created']['n']['body'] == 'x'
    assert dumps['chained']['collections']['notes']['rejected']['n']['reason'] == 'why'

def test_global_cold_mode_changes_nothing(env):
    env.write_rows('notes', _row('a', text='one'))
    env.migration('0001_real.py', "self.table('Note').rename_field('text', 'body')")
    before = env.snapshot()
    with pytest.raises(SystemExit):
        env.run(cold_mode=True)
    assert env.snapshot() == before and env.state() == [] and not (env.db / 'backups').exists()
    assert len(list((env.db / 'dumps' / 'migrations').iterdir())) == 1

###############
# Schema drift #
###############

def test_schema_drift_is_reported(env, monkeypatch):
    stored = Note.schema()
    del stored['attributes']['pinned']
    stored['attributes']['legacy'] = {'type': 'str'}
    (env.db / 'models').mkdir(parents=True)
    (env.db / 'models' / 'Note.json').write_text(json.dumps(stored))
    messages = []
    monkeypatch.setattr(migrator_module, 'warn', lambda message: messages.append(('warn', message)))
    monkeypatch.setattr(migrator_module, 'hint', lambda message: messages.append(('hint', message)))

    env.run(models=[Note])
    assert len(messages) == 1 and messages[0][0] == 'warn'
    assert '+pinned, -legacy' in messages[0][1] and 'no pending migration' in messages[0][1] and str(env.migrations) in messages[0][1]

    messages.clear()
    env.migration('0001_pinned.py')
    env.write_rows('notes', _row('a'))
    env.run(models=[Note])
    assert messages[0][0] == 'hint' and '1 pending migration' in messages[0][1]

###################################
# End to end through hsdb.init    #
###################################

_HOST = """
import json, os, sys
from teatype.db.hsdb.core import HSDBAttribute, HSDBModel
from teatype.modulo.hsdb import hsdb

class Note(HSDBModel):
    body = HSDBAttribute(str, required=True)
    pinned = HSDBAttribute(bool, required=True)

db = hsdb.init('app', models=[Note])
print('RESULT ' + json.dumps(sorted(db.all('Note'), key=lambda row: row['id'])))
"""

_MIGRATION = """
from teatype.db.hsdb.core import HSDBMigration

class AddPinned(HSDBMigration):
    cold_mode = os.environ.get('COLD') == '1'
    def migrate(self):
        notes = self.table('Note')
        notes.rename_field('text', 'body')
        notes.add_field('pinned', False)
"""

def _host(workspace:Path, **extra_env) -> subprocess.CompletedProcess:
    (workspace / 'host.py').write_text(textwrap.dedent(_HOST))
    environment = {**os.environ, 'HSDB_ROOT_PATH': str(workspace / 'root'), **extra_env}
    return subprocess.run([sys.executable, str(workspace / 'host.py')], capture_output=True, text=True, env=environment, timeout=120)

def _result(process:subprocess.CompletedProcess) -> list:
    line, = [line for line in process.stdout.splitlines() if line.startswith('RESULT ')]
    return json.loads(line[len('RESULT '):])

def test_end_to_end_restore_after_migration_and_not_rerun(workspace):
    db = workspace / 'root' / 'hsdb' / 'app'
    old = {'id': 'n1', 'text': 'hello', 'created_at': '2026-01-01T00:00:00.000000+0000Z', 'updated_at': '2026-01-01T00:00:00.000000+0000Z'}
    (db / 'indexdb' / 'notes').mkdir(parents=True)
    (db / 'indexdb' / 'notes' / 'n1.json').write_text(json.dumps(old))
    (workspace / 'migrations').mkdir()
    (workspace / 'migrations' / '0001_add_pinned.py').write_text('import os\n' + _MIGRATION)

    process = _host(workspace, COLD='1', HSDB_MIGRATIONS_COLD_MODE='0') # Class attribute cold_mode: simulated only, the server does not start
    assert process.returncode != 0 and 'nothing was applied' in process.stderr
    assert json.loads((db / 'indexdb' / 'notes' / 'n1.json').read_text()) == old
    assert not (db / 'migrations.json').exists() and len(list((db / 'dumps' / 'migrations').iterdir())) == 1
    assert not (db / 'server.json').exists()

    process = _host(workspace, COLD='0', HSDB_MIGRATIONS_COLD_MODE='1') # The env var makes every migration cold
    assert process.returncode != 0 and not (db / 'migrations.json').exists()

    process = _host(workspace, COLD='0')
    assert process.returncode == 0, process.stderr
    assert _result(process) == [{'body': 'hello', 'pinned': False, 'id': 'n1', 'created_at': old['created_at'], 'updated_at': old['updated_at']}]
    assert 'could not be restored' not in process.stdout + process.stderr
    state = json.loads((db / 'migrations.json').read_text())
    assert [(entry['id'], entry['name']) for entry in state] == [(1, 'add_pinned')]
    assert len(list((db / 'backups' / 'migration').iterdir())) == 1

    process = _host(workspace, COLD='0') # Second start: not run again
    assert process.returncode == 0 and _result(process)[0]['body'] == 'hello'
    assert json.loads((db / 'migrations.json').read_text()) == state
    assert len(list((db / 'backups' / 'migration').iterdir())) == 1

def test_end_to_end_without_migrations_reports_skipped_entries(workspace):
    db = workspace / 'root' / 'hsdb' / 'app'
    (db / 'indexdb' / 'notes').mkdir(parents=True)
    (db / 'indexdb' / 'notes' / 'n1.json').write_text(json.dumps({'id': 'n1', 'text': 'hello', 'created_at': 'x', 'updated_at': 'x'}))
    process = _host(workspace)
    assert process.returncode == 0 and _result(process) == []
    assert '1 entries could not be restored, a migration is probably missing' in process.stdout + process.stderr
