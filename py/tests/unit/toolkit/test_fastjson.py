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
import threading

# Third-party imports
import pytest
from teatype.toolkit import dump_json, fastclone, load_json

def test_dump_creates_parents_and_prettifies(tmp_path):
    target = tmp_path / 'a' / 'b' / 'data.json'
    dump_json({'k': [1, None]}, str(target), prettify=True)
    assert target.read_text(encoding='utf-8').startswith('{\n  "k"')
    assert load_json(str(target)) == {'k': [1, None]}
    with pytest.raises(FileNotFoundError):
        dump_json({}, str(tmp_path / 'missing' / 'data.json'), create_parents=False)

def test_dump_is_atomic_and_keeps_permissions(tmp_path):
    target = tmp_path / 'data.json'
    dump_json({'v': 1}, str(target))
    os.chmod(target, 0o640)
    with pytest.raises(TypeError):
        dump_json({'v': object()}, str(target))
    assert load_json(str(target)) == {'v': 1}
    dump_json({'v': 2}, str(target), fsync=True)
    assert load_json(str(target)) == {'v': 2}
    assert os.stat(target).st_mode & 0o777 == 0o640
    assert os.listdir(tmp_path) == ['data.json']

def test_load_accepts_non_finite_tokens_written_by_the_stdlib(tmp_path):
    target = tmp_path / 'data.json'
    target.write_text(json.dumps({'a': float('nan'), 'b': [float('-inf'), 2.5]}), encoding='utf-8')
    assert load_json(str(target)) == {'a': None, 'b': [None, 2.5]}

def test_load_rejects_corrupt_and_scalar_documents(tmp_path):
    target = tmp_path / 'data.json'
    target.write_text('{broken', encoding='utf-8')
    with pytest.raises(ValueError):
        load_json(str(target))
    target.write_text('3', encoding='utf-8')
    with pytest.raises(TypeError):
        load_json(str(target))

def test_load_is_thread_safe(tmp_path):
    target = tmp_path / 'data.json'
    dump_json({'values': list(range(3000))}, str(target))
    failures = []

    def work():
        for _ in range(200):
            try:
                assert load_json(str(target))['values'][-1] == 2999
            except Exception as exc:
                failures.append(exc)

    threads = [threading.Thread(target=work) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert failures == []

def test_fastclone_is_independent_of_the_original():
    original = {'a': [1, {'b': 2}], 'c': {'d': [3]}}
    clone = fastclone(original)
    clone['a'][1]['b'] = 99
    clone['c']['d'].append(4)
    assert original == {'a': [1, {'b': 2}], 'c': {'d': [3]}}
