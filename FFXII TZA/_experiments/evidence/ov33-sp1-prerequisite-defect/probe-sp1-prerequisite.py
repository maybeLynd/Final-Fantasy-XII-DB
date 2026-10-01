"""Concrete OV33 returned-producer control: zero corpus must not succeed.
Usage: python probe-sp1-prerequisite.py PINNED_SOURCE FIXTURE_DIR FRESH_OUTPUT_DIR
Explicit immutable inputs and fresh output; no peer source/archive writes.
"""
import hashlib,json,pathlib,re,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
source,fixture_dir,OUT=map(pathlib.Path,sys.argv[1:])
if OUT.exists():raise ValueError('immutable run exists')
extractor=ROOT/'agent_flow/tools/vbfextract.py'
fixture=fixture_dir/'positive.vbf'
bad=fixture.with_name('corrupt.vbf')
original=source.read_bytes();text=original.decode()
if hashlib.sha256(original).hexdigest()!='6cd80a4d37f0a0870106c11253c91bd01541d3065c4a2654f6a324bc5abd1701':
    raise ValueError('different original producer; re-evaluate, do not silently substitute')
if hashlib.sha256(extractor.read_bytes()).hexdigest()!='1841f666b28fb737bf02ab3bb0ea90a7515273f74533a772e7f7131c0e0de611':
    raise ValueError('extractor prerequisite changed')
if hashlib.sha256(fixture.read_bytes()).hexdigest()!='fe50bd5aed88d761a094e911f596ec3006728abbdddb8eacb855a0bc698cd94f':
    raise ValueError('positive fixture prerequisite changed')
if hashlib.sha256(bad.read_bytes()).hexdigest()!='0054cc9fa2a031e8e89d9a47447940b0acf970f4421ddd1e8d3c296c277ddb80':
    raise ValueError('negative fixture prerequisite changed')
if text.count('VBF = r"')!=1:raise ValueError('source adaptation premise changed')
OUT.mkdir();(OUT/'original.py').write_bytes(original)
def sha(b):return hashlib.sha256(b).hexdigest()
records=[]
for case,input_path in [('no_mpk_corpus',fixture),('bad_archive_control',bad)]:
    copy=OUT/(case+'.py')
    adapted,n=re.subn(r'^VBF = r"[^"]*"$', lambda _: 'VBF = '+repr(str(input_path)), text, flags=re.M)
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
control=(invalid['exit_code']!=0 and 'AssertionError' in invalid['stderr']
         and 'magic == b"SRYK"' in invalid['stderr'])
(OUT/'result.json').write_text(json.dumps(dict(
    question='Does required SP1 corpus-control mismatch produce terminal failure?',
    method='offline actual returned producer subprocess, declared input-path substitution',
    original_source=str(source.resolve()),original_source_sha256=sha(original),
    extractor_sha256=sha(extractor.read_bytes()),driver_sha256=sha(pathlib.Path(__file__).read_bytes()),
    records=records,defect_reproduced=defect,archive_parser_negative_control=control,
    verdict=('REJECT upstream prerequisite gate; retained actual 550-pack data findings not disproved'
             if defect and control else 'INVALID_CONTROL; no dependent semantic verdict'),
    prior_run='sp1-prerequisite-01 INVALID: regex replacement re-interpreted Windows path escapes; both child scripts failed before the producer ran. Do not use its REJECT wording/control boolean as a verdict. Use literal callback replacement and require actual archive-magic failure.',
    limits='Synthetic index has two non-mpk entries; no scientific corpus rerun or new game observation. Actual original-corpus count matched; this exposes a missing gate, not a counterexample count>=128.',
    needed_repair='Mandatory expected-corpus mismatch and omitted/malformed referenced SP1 records must fail or produce explicit incomplete status, which downstream acceptance checks. Add this actual invocation regression.',
    provided_source_unchanged=True,
    input_binding='explicit hash-checked source/fixture arguments, fresh output; no mutable default inputs'),indent=2)+'\n')
if not defect or not control:raise ValueError('reproducer/control did not discriminate; do not route as confirmed')
print('REPRODUCED: corpus MISMATCH and zero observations exit0/FAILS0; bad archive refuses; peer source unchanged')
