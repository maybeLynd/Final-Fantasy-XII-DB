"""Two concrete normalizer prerequisite/identity refusals; reuse positive."""
import hashlib, json, pathlib, shutil, subprocess, sys
W = pathlib.Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
out = W / 'descriptor-offset-qualification-controls-01'
if out.exists(): raise ValueError('immutable controls exist')
d = W / 'normalize-namebinding-descriptor.py'
p = json.loads((W / 'descriptor-offset-qualification-result-01.json').read_text())
s = json.loads((W / 'descriptor-offset-qualification-positive-01.status.json').read_text())
if s['exit'] != 0 or s['checker_sha256'] != sha(d) or p['checker_sha256'] != sha(d) or p['producer_complete'] is not True:
    raise ValueError('positive missing/stale')
if any(sha(W/x['path']) != x['sha256'] for x in p['source_pins'] + p['required_invocation_receipts']):
    raise ValueError('positive prerequisite changed')
if sha(W / p['normalized_result']['path']) != p['normalized_result']['sha256']:
    raise ValueError('normalized result changed')
names = ['descriptor-offset-affected-preimages-01.json', 'descriptor-offset-retained-pin-result-01.json',
         'descriptor-offset-retained-pin-source-01.json', 'descriptor-offset-retained-adopter-source-01.json',
         'namebinding-error-policy-existing-resolution-01.json']
out.mkdir(); receipts = []
for label, error in [('missing-semantic-preimage', 'FileNotFoundError'), ('changed-offset-store', 'reference byte identity changed')]:
    c = out / label; c.mkdir()
    for name in names:
        if label == 'missing-semantic-preimage' and name == 'descriptor-offset-retained-pin-result-01.json': continue
        shutil.copyfile(W / name, c / name)
    if label == 'changed-offset-store':
        f = c / 'descriptor-offset-retained-adopter-source-01.json'; v = json.loads(f.read_text())
        q = next(x for x in v['ranges'] if x['start'] == '0x32e870')
        i = next(x for x in q['instructions'] if x['pc'] == '0x32e918')
        if i['bytes'] != '4189422c': raise ValueError('mutation preimage changed')
        i.update(bytes='41894228', args='dword ptr [r10 + 0x28], eax'); i['memory'][0]['displacement'] = 0x28
        q['sha256'] = hashlib.sha256(bytes.fromhex(''.join(x['bytes'] for x in q['instructions']))).hexdigest()
        f.write_text(json.dumps(v, indent=2) + '\n')
        a = c / 'descriptor-offset-affected-preimages-01.json'; av = json.loads(a.read_text())
        next(x for x in av['inputs'] if x['path'] == f.name)['sha256'] = sha(f)
        a.write_text(json.dumps(av, indent=2) + '\n')
    target = c / 'unexpected-result.json'; argv = [sys.executable, str(d), str(target), str(c)]
    r = subprocess.run(argv, capture_output=True)
    (c / 'stdout').write_bytes(r.stdout); (c / 'stderr').write_bytes(r.stderr)
    rec = dict(case=label, argv=argv, exit=r.returncode, expected_error=error,
               expected_error_seen=error in r.stderr.decode(errors='replace'), result_absent=not target.exists(),
               normalized_absent=not (c / 'namebinding-pin-exception-qualified-02.json').exists())
    (c / 'status.json').write_text(json.dumps(rec, indent=2) + '\n')
    if not (r.returncode and rec['expected_error_seen'] and rec['result_absent'] and rec['normalized_absent']):
        raise ValueError('actual normalizer refusal failed ' + label)
    receipts.append(rec)
(out / 'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_DESCRIPTOR_REFUSALS_INDEPENDENT_PENDING',
    checker_sha256=sha(d), driver_sha256=sha(pathlib.Path(__file__)),
    positive_reused=dict(path='descriptor-offset-qualification-result-01.json', sha256=sha(W/'descriptor-offset-qualification-result-01.json')),
    refusals=receipts, limits='Two actual CLI refusal controls, no repeated scientific positive or original-code execution. Sparse missing-input case is not a valid empty capture.'), indent=2) + '\n')
print('Two actual normalizer refusals; semantic preimage and original offset-store identity enforced')
