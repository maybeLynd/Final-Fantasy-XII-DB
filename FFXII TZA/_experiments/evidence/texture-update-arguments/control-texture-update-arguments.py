"""Actual producer/freezer CLI refusal paths, successful positive reused."""
import hashlib, importlib.util, json, pathlib, shutil, subprocess, sys

W = pathlib.Path(__file__).resolve().parent
out = W/'texture-update-arguments-controls-01'
if out.exists():
    raise ValueError('immutable controls exist')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
spec = importlib.util.spec_from_file_location('update_freeze_control', W/'freeze-texture-update-arguments.py')
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
r = F.prerequisites(W)
checker = W/'prove-texture-update-arguments.py'
Sspec = importlib.util.spec_from_file_location('update_mutation_roles', W/'validate-title-source-annotations.py')
S = importlib.util.module_from_spec(Sspec)
Sspec.loader.exec_module(S)


def consistent(source, pc, suffix, replacement, args, disp=None):
    p = source/'texture-async-count-path-source-01.json'
    raw = json.loads(p.read_text())
    q = next(q for q in raw['ranges'] if q['start']=='0x622010')
    i = next(i for i in q['instructions'] if i['pc']==pc)
    if not i['bytes'].endswith(suffix):
        raise ValueError('mutation byte preimage changed')
    i['bytes'] = i['bytes'][:-len(suffix)] + replacement
    i['args'] = args
    if disp is not None:
        i['memory'][0]['displacement'] = disp
    q['sha256'] = hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
    S.validate(raw)  # A valid instruction mutation; not a malformed fixture.
    p.write_text(json.dumps(raw, indent=2)+'\n')


out.mkdir()
records=[]
for label in ('consistent-payload-offset', 'consistent-advance-shift', 'missing-source', 'false-argument-store-role', 'failed-positive-exit'):
    case=out/label
    source=case/'source'
    source.mkdir(parents=True)
    if label=='failed-positive-exit':
        names=['texture-update-arguments-result-01.json', 'texture-update-arguments-positive-02.status.json', 'prove-texture-update-arguments.py']
    else:
        names=[q['path'] for q in r['source_pins']]
    for name in names:
        shutil.copyfile(W/name, source/name)
    target=case/('packet' if label=='failed-positive-exit' else 'result.json')
    program=checker
    expected='required shipping updater/leaf identity changed'
    if label=='consistent-payload-offset':
        consistent(source, '0x62205e', '28', '30', 'r15, qword ptr [r14 + rcx + 0x30]', 0x30)
    elif label=='consistent-advance-shift':
        consistent(source, '0x622135', '03', '04', 'rax, 4')
    elif label=='missing-source':
        # Disposable control copy only; preserve every original input.
        (source/'texture-async-count-path-source-01.json').unlink()
        expected='FileNotFoundError'
    elif label=='false-argument-store-role':
        p=source/'texture-async-count-path-source-01.json';raw=json.loads(p.read_text())
        i=next(i for q in raw['ranges'] for i in q['instructions'] if i['pc']=='0x6220f8')
        if i['memory'][0]['role']!='w':raise ValueError('store-role preimage changed')
        i['memory'][0]['role']='r';p.write_text(json.dumps(raw,indent=2)+'\n')
        expected='memory/address/access annotation disagrees'
    else:
        p=source/'texture-update-arguments-positive-02.status.json';v=json.loads(p.read_text());v['exit']=79
        p.write_text(json.dumps(v,indent=2)+'\n')
        program=W/'freeze-texture-update-arguments.py'
        expected='required positive invocation failed or incomplete'
    args=[sys.executable, '-B', str(program), str(target), str(source)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (case/'stdout').write_bytes(run.stdout);(case/'stderr').write_bytes(run.stderr)
    record=dict(case=label,argv=args,exit=run.returncode,result_absent=not target.exists(),
                expected_error_seen=expected in run.stderr.decode(errors='replace'))
    (case/'status.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
    if run.returncode==0 or not record['result_absent'] or not record['expected_error_seen']:
        raise ValueError('invalid concrete refusal '+label)
(out/'result.json').write_text(json.dumps(dict(status='PASS_ACTUAL_TEXTURE_UPDATE_REFUSALS_INDEPENDENT_PENDING',
    checker_sha256=sha(checker),freezer_sha256=sha(W/'freeze-texture-update-arguments.py'),
    positive_reused=dict(path='texture-update-arguments-result-01.json',sha256=sha(W/'texture-update-arguments-result-01.json')),
    refusals=records,limits='Five actual producer/freezer controls; no original-code/game execution or independent acceptance'),indent=2)+'\n')
print('Five actual updater/freezer refusal controls; successful positive reused')
