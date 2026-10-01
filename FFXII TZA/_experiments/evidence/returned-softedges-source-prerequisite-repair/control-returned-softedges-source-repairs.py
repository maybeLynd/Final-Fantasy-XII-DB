"""Final caller-path controls for returned field/member/pointer defects.

Use a complete pointer-pin copy and a positive twin before missing/mutated cases.
No independent audit census or legacy bug rerun. Published inputs stay immutable.
"""
import hashlib, importlib.util, json, pathlib, shutil, sys
W=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('delivery',W/'prepare-residue-packet-publication.py')
M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
out=W/'returned-softedges-source-repair-controls-01';out.mkdir()
checks=[]
pointer_original=M.ROOT/'Database/FFXII TZA/_experiments/evidence/phyretext-pointer-key-binding'
v=json.loads((W/'softedges-pointer-key-binding-result-04.json').read_text())
baseline=out/'pointer-complete-baseline';baseline.mkdir()
for pin in v['source_pins']:
    dest=baseline/pin['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(pointer_original/pin['path'],dest)
target=out/'pointer-baseline-result.json'
M.checked_run([sys.executable,str(W/'reduce-softedges-pointer-key-binding.py'),str(target),str(baseline)],timeout=45,receipt_prefix=out/'pointer-baseline-cli')
pv=json.loads(target.read_text())
if pv.get('producer_complete') is not True or len(pv['routes'])!=2 or not any(p['path']=='softedges-resource-source-01/phyretext.fx.phyre' for p in pv['source_pins']):raise ValueError('positive twin incomplete')
checks.append(dict(case='pointer-complete-baseline',status='PASS_POSITIVE_TWIN'))

def refuse(name,argv,target):
    error=None
    try:M.checked_run(argv,timeout=45,receipt_prefix=out/(name+'-cli'))
    except RuntimeError as e:error=str(e)
    if error is None or target.exists():raise ValueError('required defect accepted '+name)
    checks.append(dict(case=name,status='PASS_REFUSED_NO_FINAL_RESULT',labelled_synthetic=True,error=error))

for name,pc,key,value in [('pointer-setne',0x59ece1,'mnemonic','setne'),('pointer-compare-zero',0x59ecde,'args','eax, 0'),('pointer-bit5',0x59ecb5,'args','r15d, 5'),('pointer-missing-guard',None,None,None),('pointer-missing-asset',None,None,None)]:
    case=out/name;shutil.copytree(baseline,case)
    if pc is None:
        p=case/('softedges-array-terminal-guard-source-01/original-code.json' if name.endswith('guard') else 'softedges-resource-source-01/phyretext.fx.phyre');p.unlink()
    else:
        p=case/'softedges-member-resolution-continuation-code-01.json';raw=json.loads(p.read_text());hits=0
        for q in raw['ranges']:
            for i in q['instructions']:
                if int(i['pc'],16)==pc:i[key]=value;hits+=1
        if hits!=1:raise ValueError('missing exact polarity target')
        p.write_text(json.dumps(raw,indent=2),encoding='utf8')
    target=out/(name+'-must-not-exist.json')
    refuse(name,[sys.executable,str(W/'reduce-softedges-pointer-key-binding.py'),str(target),str(case)],target)

case=out/'field-displacement-bytes-only';case.mkdir()
original=M.ROOT/'Database/FFXII TZA/_experiments/evidence/phyretext-softedges-field-extent/softedges-resource-source-01'
for n in ['original-code-raw-01.json','array-binding-code-01.json','member-bridge-code-01.json','constructor-source-retained-01.json']:
    shutil.copyfile(original/n,case/n)
hits=0
for p in case.glob('*.json'):
    raw=json.loads(p.read_text())
    for q in raw['ranges']:
        for i in q['instructions']:
            if i['pc']=='0x1ea5c1':
                b=bytes.fromhex(i['bytes']);i['bytes']=(b[:-4]+(0x9c8).to_bytes(4,'little')).hex();hits+=1
        q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
    p.write_text(json.dumps(raw,indent=2),encoding='utf8')
if hits!=1:raise ValueError('field original target missing')
target=out/'field-must-not-exist.json'
refuse('field-displacement-bytes-only',[sys.executable,str(W/'reduce-softedges-field-extent.py'),str(case),str(target)],target)
if 'annotation disagrees' not in checks[-1]['error']:raise ValueError('field refusal did not reach intended byte/annotation gate')

old=W/'softedges-member-source-qualification-controls-01'
for name in ['width-bytes-only','negative-status-bytes-only','negative-status-consistent','upstream-facts-missing']:
    target=out/(name+'-must-not-exist.json')
    refuse(name,[sys.executable,str(W/'check-softedges-member-boundaries.py'),str(old/name/'source'),str(target)],target)
    if name=='upstream-facts-missing' and json.loads(pathlib.Path(str(target)+'.upstream-status.json').read_text())['exit']==0:raise ValueError('upstream failure swallowed')
with (out/'result.json').open('x') as f:json.dump(dict(status='PASS_FINAL_RETURNED_REPAIR_CONTROLS_INDEPENDENT_PENDING',checks=checks,
    driver_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    final_driver_sha256={n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in ['reduce-softedges-field-extent.py','reduce-softedges-pointer-key-binding.py','check-softedges-member-boundaries.py','check-softedges-member-boundaries-03.py','validate-title-source-annotations.py']},
    limits='Current three actual caller paths. Existing semantic acceptances remain scoped; new repairs independent pending. Baseline twin plus ten refusal controls, not native/live experiments or reviewer census credit.'),f,indent=2)
print('Complete pointer positive twin and ten returned/required-prerequisite controls verified on final actual callers')
