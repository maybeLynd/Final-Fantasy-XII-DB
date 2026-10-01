"""Concrete actual-producer refusals, using fresh bounded synthetic fixtures."""
import copy, hashlib, json, pathlib, subprocess, sys
W=pathlib.Path(__file__).resolve().parent
out=pathlib.Path(sys.argv[1]);out.mkdir()
base=json.loads((W/'renderer-queue-initialization-source-02.json').read_text())
def missing(r):r['ranges']=[q for q in r['ranges'] if q['start']!='0x186cd0']
def incomplete(r):r['wrapper_complete']=False
def wrong_count(r):
    q=next(q for q in r['ranges'] if q['start']=='0x184f20')
    i=next(i for i in q['instructions'] if i['pc']=='0x184fdd')
    if i['bytes']!='448d4604':raise ValueError('mutation preimage moved')
    i.update(bytes='448d4605',args='r8d, [rsi + 5]')
    i['memory'][0]['displacement']=5
    q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
rows=[]
for tag,edit,error in [('missing-initializer',missing,'normal extent/chain prerequisite incomplete'),
                       ('failed-capture',incomplete,'missing original/adapter prerequisite'),
                       ('coherent-five-banks',wrong_count,'source operation mismatch 0x184fdd')]:
    c=out/tag;c.mkdir();raw=copy.deepcopy(base);edit(raw)
    raw['synthetic_fixture']='Intentionally invalid controlled producer input, not original/live evidence'
    src=c/'source.json';src.write_text(json.dumps(raw,indent=2)+'\n');result=c/'result.json'
    argv=[sys.executable,str(W/'prove-renderer-queue-initialization.py'),str(src),str(result)]
    z=subprocess.run(argv,capture_output=True,timeout=45)
    (c/'stdout').write_bytes(z.stdout);(c/'stderr').write_bytes(z.stderr)
    row=dict(case=tag,argv=argv,exit=z.returncode,expected_error=error,
             expected_error_seen=error.encode() in z.stderr,result_absent=not result.exists(),
             checker_sha256=hashlib.sha256((W/'prove-renderer-queue-initialization.py').read_bytes()).hexdigest())
    (c/'status.json').write_text(json.dumps(row,indent=2)+'\n')
    if not z.returncode or not row['expected_error_seen'] or not row['result_absent']:raise ValueError('invalid/nondiscriminating refusal '+tag)
    rows.append(row)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_REFUSALS_INDEPENDENT_PENDING',refusals=rows,
   limits='Synthetic producer inputs/actual CLI exits; not original-code execution, allocator failure or live FF12 observations'),indent=2)+'\n')
print('Three actual prerequisite/count refusals; no invalid result emitted')
