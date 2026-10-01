"""Read-only metadata/history integrity check. Does not execute an experiment."""
from pathlib import Path
from collections import Counter
import hashlib
import importlib.util
import json
import re

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parents[1]
ROOT = EXPERIMENTS.parent
SCRIPTS = ROOT.parent / 'Tools/analysis-kit/gfz-scripts'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_parser(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.frontmatter


def verified_body(raw, row, git_body):
    prefix = re.match(rb'^---\r?\n.*?\r?\n---\r?\n\r?\n', raw, re.S)
    assert prefix, row['record']
    body = raw[prefix.end():]
    original_raw_match = (len(body) == row['original_body_bytes'] and
                          digest(body) == row['original_body_sha256'])
    normalized = body.replace(b'\r\n', b'\n')
    assert len(normalized) == git_body['original_git_body_bytes']
    assert digest(normalized) == git_body['original_git_body_sha256'], row['record']
    return body, original_raw_match


def main():
    recovery = json.loads((HERE / 'recovery.json').read_text(encoding='utf-8'))
    records = recovery['records']
    publication = json.loads((HERE / 'publication-normalization.json').read_text(encoding='utf-8'))
    git_bodies = {r['record']: r for r in publication['records']}
    assert len(records) == 38
    assert {r['metadata']['experiment'] for r in records} == {f'EXP-{n:03}' for n in range(37, 75)}
    parsers = [load_parser(n) for n in ('check_experiments', 'check_contract_runtime')]
    result = []
    for row in records:
        raw = (EXPERIMENTS / row['record']).read_bytes()
        body, original_raw_match = verified_body(raw, row, git_bodies[row['record']])
        expected = row['metadata']
        for parse in parsers:
            # Both readers use text-mode universal newlines when reading files.
            assert parse(raw.decode('utf-8').replace('\r\n', '\n')) == expected, row['record']
        assert expected['live_game'] == 'false'
        owner = expected['contract']
        if owner.startswith('none - '):
            assert len(owner) > len('none - ')
        else:
            assert (EXPERIMENTS / owner).is_file(), owner
        assert (EXPERIMENTS / expected['tool']).is_file()
        mp = EXPERIMENTS / row['historical_manifest']
        assert digest(mp.read_bytes()) == row['historical_manifest_sha256']
        manifest = json.loads(mp.read_text(encoding='utf-8'))
        assert len(manifest['files']) == row['historical_files'] > 0
        for name, entry in manifest['files'].items():
            data = (mp.parent / name).read_bytes()
            assert len(data) == entry['bytes'] and digest(data) == entry['sha256'], (row['record'], name)
        result.append(dict(record=row['record'], original_body_sha256=digest(body),
                           original_raw_body_matches=original_raw_match,
                           original_git_text_body_matches=True,
                           historical_files_checked=len(manifest['files']),
                           parsed_evidence_class=expected['evidence_class'],
                           contract=owner))
    return dict(scope='Metadata parsing and retained-byte integrity only; no original-code rerun, live validation or semantic closure.',
                records=result, evidence_classes=dict(Counter(r['parsed_evidence_class'] for r in result)))


if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
