"""Concrete OV33 returned-producer control: zero corpus must not succeed.
Disclosed private input-path adaptation only; no peer source/archive writes.
"""
import hashlib,json,pathlib,re,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
OUT=W/'sp1-prerequisite-01'
if OUT.exists():raise ValueError('immutable run exists')
source=ROOT/'Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/t1b_sp1_counts.py'
extractor=ROOT/'agent_flow/tools/vbfextract.py'
fixture=ROOT/'Database/Tools/work/ASTRA/dashboard-views-eae0ed3c7-review/vbf-chain/positive.vbf'
bad=fixture.with_name('corrupt.vbf')
original=source.read_bytes();text=original.decode()
if text.count('VBF = r"')!=1:raise ValueError('source adaptation premise changed')
OUT.mkdir();(OUT/'original.py').write_bytes(original)
def sha(b):return hashlib.sha256(b).hexdigest()
records=[]
for case,input_path in [('no_mpk_corpus',fixture),('bad_archive_control',bad)]:
    copy=OUT/(case+'.py')
    adapted,n=re.subn(r'^VBF = r"[^"]*"$', 'VBF = '+repr(str(input_path)), text, flags=re.M)
    if n!=1:raise ValueError('more than declared input substitution')
    copy.write_text(adapted,encoding='utf8')
    argv=[sys.executable,'-B',str(copy)]
    q=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30)
    (OUT/(case+'.stdout.txt')).write_text(q.stdout)
    (OUT/(case+'.stderr.txt')).write_text(q.stderr)
    records.append(dict(case=case,argv=argv,exit_code=q.returncode,terminal=True,
                        stdout=q.stdout,stderr=q.stderr,input_sha256=sha(input_path.read_bytes()),
                        adapted_driver_sha256=sha(copy.read_bytes())))
if source.read_bytes()!=original:raise ValueError('peer source changed during test')
missing,invalid=records
defect=(missing['exit_code']==0 and not missing['stderr'] and 'packs 0  records 0' in missing['stdout']
        and 'MISMATCH (0, 0, 0)' in missing['stdout'] and 'FAILS 0' in missing['stdout'])
control=(invalid['exit_code']!=0 and bool(invalid['stderr']))
(OUT/'result.json').write_text(json.dumps(dict(
    question='Does required SP1 corpus-control mismatch produce terminal failure?',
    method='offline actual returned producer subprocess, declared input-path substitution',
    original_source=str(source.relative_to(ROOT)),original_source_sha256=sha(original),
    extractor_sha256=sha(extractor.read_bytes()),driver_sha256=sha(pathlib.Path(__file__).read_bytes()),
    records=records,defect_reproduced=defect,archive_parser_negative_control=control,
    verdict='REJECT upstream prerequisite gate; retained valid nine/550-pack findings not disproved',
    limits='Synthetic index has two non-mpk entries; no scientific corpus rerun or new game observation. Actual original-corpus count matched; this exposes a missing gate, not a counterexample count>=128.',
    needed_repair='Mandatory expected-corpus mismatch and omitted/malformed referenced SP1 records must fail or produce explicit incomplete status, which downstream acceptance checks. Add this actual invocation regression.',
    peer_source_unchanged=True),indent=2)+'\n')
if not defect or not control:raise ValueError('reproducer/control did not discriminate; do not route as confirmed')
print('REPRODUCED: corpus MISMATCH and zero observations exit0/FAILS0; bad archive refuses; peer source unchanged')
