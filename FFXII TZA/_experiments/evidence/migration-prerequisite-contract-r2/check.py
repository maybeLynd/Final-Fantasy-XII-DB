import argparse, hashlib, json, re
from pathlib import Path
W = Path(__file__).resolve().parent
R = W / 'run-01'
ap = argparse.ArgumentParser()
ap.add_argument('--raw', type=Path, default=R / 'raw.json')
ap.add_argument('--out', type=Path, default=W / 'result.json')
a = ap.parse_args()
r = json.loads(a.raw.read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert r['finished'] is True and r['source_unchanged'] is True
assert r['source_commit'] == '1f11830e92aa71d7aea000fcd8b68cdfa9c46d6a'
assert r['original_commit'] == 'c5c0111ebf885668e06804da3642fc0117c644eb'
assert r['original_members_verified'] == 64
assert r['driver_sha256'] == sha(W / 'capture.py')
assert r['composer_sha256'] == sha(R / 'composer.py')
assert r['original_manifest_sha256'] == sha(R / 'original-manifest.json')
manifest = json.loads((R / 'original-manifest.json').read_text())
pins = {m['path']: m['sha256'] for m in manifest['members']}
assert pins['run-01/composer.py'] == r['composer_sha256']
expected = {'valid-tagged': True, 'fail-with-zero-exit': False, 'nonzero-exit': False,
            'missing-file': False, 'upstream-exception': False, 'malformed-output': False,
            'same-count-changed-tags': False, 'missing-object': False, 'missing-footer': False,
            'data-declared-findings': True, 'data-exit-two': False, 'data-half-built': False,
            'default-tab-fail': False, 'custom-tab-pass': True, 'custom-tab-fail': False,
            'bounded-timeout': False}
ids = {'generic--' + n for n in expected} | {'legacy--custom-tab-pass', 'legacy--custom-tab-fail'}
cases = {c['name']: c for c in r['cases']}
assert set(cases) == ids and len(r['cases']) == len(ids) == 18
assert set(r['sources']) == {'generic', 'legacy'}
for name, s in r['sources'].items():
    content = (R / s['retained']).read_bytes()
    assert sha(R / s['retained']) == s['sha256']
    assert hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest() == s['git_blob']
assert re.fullmatch(r'[0-9a-f]{40}', r['source_commit'])
for name, c in cases.items():
    source, case = name.split('--', 1)
    assert c['source'] == source and c['original_case'] == case
    assert c['expected_accepted'] is expected[case]
    assert c['child_reaped'] is True
    assert c['original_fixture_commit'] == r['original_commit']
    d = R / name
    assert sha(d / 'declaration.json') == c['declaration_sha256'] == pins['run-01/' + case + '/declaration.json']
    if case == 'missing-file': assert not (d / 'upstream.py').exists() and c['upstream_sha256'] is None
    else: assert sha(d / 'upstream.py') == c['upstream_sha256'] == pins['run-01/' + case + '/upstream.py']
    recorded = Path(r['run_directory'])
    assert c['invocation'][2] == str(recorded / 'composer.py')
    assert c['invocation'][3] == str(recorded / r['sources'][source]['retained'])
    assert c['invocation'][4] == str(recorded / name / 'upstream.py')
    assert c['invocation'][5] == str(recorded / name / 'declaration.json')
    if source == 'legacy':
        assert c['timed_out'] is False and c['returncode'] == 1 and not c['stdout']
        assert "TypeError: run() got an unexpected keyword argument 'exits'" in c['stderr']
    elif case == 'bounded-timeout':
        assert c['timed_out'] is True and c['returncode'] is None and c['deadline_seconds'] == 1
        assert 'COMPOSER_PASS' not in c['stdout']
    elif expected[case]:
        assert c['timed_out'] is False and c['returncode'] == 0
        assert c['stdout'].startswith('COMPOSER_PASS ') and not c['stderr']
        assert json.loads(c['stdout'].split(' ', 1)[1]) == {'complete': True, 'rows': [7, 9]}
    else:
        assert c['timed_out'] is False and c['returncode'] == 1
        assert c['stdout'].startswith('COMPOSER_FAIL ') and 'COMPOSER_PASS' not in c['stdout']
        assert not c['stderr']
        if case == 'custom-tab-fail': assert 'printed FAIL lines' in c['stdout'] and 'FAIL\tA\trequired failure' in c['stdout']
legacy = json.loads((W / 'legacy-corrected/raw.json').read_text())
assert legacy['finished'] is True and legacy['source_commit'] == r['source_commit']
assert legacy['original_failed_raw_sha256'] == sha(R / 'raw.json')
assert legacy['source_sha256'] == r['sources']['legacy']['sha256']
assert legacy['driver_sha256'] == sha(W / 'legacy-control.py')
assert legacy['composer_sha256'] == sha(W / 'legacy-corrected/composer.py')
assert len(legacy['cases']) == 2 and {c['name'] for c in legacy['cases']} == {'custom-tab-fail', 'custom-tab-pass'}
for c in legacy['cases']:
    assert c['timed_out'] is False and c['child_reaped'] is True and not c['stderr']
    original = cases['legacy--' + c['name']]
    assert c['upstream_sha256'] == original['upstream_sha256']
    assert c['declaration_sha256'] == original['declaration_sha256']
    assert c['invocation'][2] == legacy['composer_path']
    assert c['invocation'][3] == original['invocation'][3]
    assert c['invocation'][4:] == original['invocation'][4:]
    if c['name'] == 'custom-tab-pass':
        assert c['returncode'] == 0 and c['stdout'].startswith('COMPOSER_PASS ')
    else:
        assert c['returncode'] == 1 and c['stdout'].startswith('COMPOSER_FAIL ')
        assert 'COMPOSER_PASS' not in c['stdout'] and 'printed FAIL lines' in c['stdout']
        assert 'FAIL\tA\trequired failure' in c['stdout']
result = {'verdict': 'ACCEPT', 'scope': 'A03 recognized configured FAIL repair at exact final source and two legacy tab controls',
          'source_commit': r['source_commit'], 'raw_sha256': sha(a.raw),
          'legacy_corrected_raw_sha256': sha(W / 'legacy-corrected/raw.json'),
          'original_commit': r['original_commit'], 'original_manifest_sha256': r['original_manifest_sha256'],
          'result': 'Both configured FAIL composers exit1/refuse/no PASS; configured PASS controls succeed. All16 generic retained cases meet required exit/output/timeout expectations. Two legacy custom controls establish its repaired boundary directly.',
          'controls': 'Unchanged retained upstream/declarations; original64 byte members verified; fixed generic+legacy sources match cited commit. Generic composer unchanged. First two legacy attempts INVALID_API_CALL, retained; corrected composer checks exact signature and reaches supported API. Only legacy pair re-executed; generic sixteen not repeated.',
          'limits': 'Method A synthetic software verification. No FF12 shipping-code/live behavior, no new SN1 semantics or full M0-M5/L1+L2 completion. Timeout external to composer, not helper in-process enforcement. Legacy coverage only tab pair; names-only presence requires explicit caller completeness validator. Old rejection remains historical evidence.',
          'consumer': 'OPUS via structured OPUS-REQ-ASTRA-REVERIFY-A03-PREREQ-R2; existing incorporation transition must be verified separately.'}
if a.out.exists(): assert json.loads(a.out.read_text()) == result, 'Do not overwrite differing retained result'
else: a.out.write_text(json.dumps(result, indent=2) + '\n')
print('ACCEPT_REPAIRED_CONFIGURED_BOUNDARY', flush=True)
