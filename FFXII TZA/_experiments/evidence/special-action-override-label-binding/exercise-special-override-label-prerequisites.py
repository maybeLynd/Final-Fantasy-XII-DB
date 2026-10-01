"""Run the actual label reducer with positive and incomplete/corrupt inputs.

Only private input-root binding is adapted; proof predicates are unchanged.
Children are bounded, synchronously waited and never left running.
"""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]
out=pathlib.Path(sys.argv[1])
if out.exists():raise ValueError('immutable control directory exists')
out.mkdir()
inputs=['capture-index-path.py','capture-special-override-constructor-dependencies.py',
        'capture-special-override-formatting-effects.py','capture-special-override-control.py',
        'special-override-constructor-dependencies-raw-01.json',
        'special-override-formatting-effects-raw-01.json','special-override-control-raw-01.json']
code=(W/'prove-special-override-label-binding.py').read_text()
old='W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]'
if code.count(old)!=1:raise ValueError('exact private-root adapter prerequisite')
adapted=code.replace(old,'W=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('+repr(str(ROOT))+')')
receipts=[]
for name in ['positive','missing_raw','incomplete_wrapper','changed_instruction','wrong_table_extent']:
    d=out/name;d.mkdir()
    for x in inputs:shutil.copyfile(W/x,d/x)
    (d/'prove-special-override-label-binding.py').write_text(adapted)
    p=d/'special-override-formatting-effects-raw-01.json'
    if name=='missing_raw':p.unlink()
    elif name!='positive':
        r=json.loads(p.read_text())
        if name=='incomplete_wrapper':r['wrapper_complete']=False
        elif name=='wrong_table_extent':r['switch_table']['entries']=293
        else:
            i=next(i for s in r['ranges'] for i in s['instructions'] if i['pc']=='0x1ce9b1');i['bytes']='48c1e004'
        p.write_text(json.dumps(r,indent=2)+'\n')
    result=d/'result.json'
    child=subprocess.run([sys.executable,str(d/'prove-special-override-label-binding.py'),str(result)],
                         capture_output=True,text=True,timeout=30)
    (d/'stdout.txt').write_text(child.stdout);(d/'stderr.txt').write_text(child.stderr)
    passed=(child.returncode==0 and result.exists()) if name=='positive' else (child.returncode!=0 and not result.exists())
    if name=='positive' and passed:
        r=json.loads(result.read_text())
        passed=[(x['state'],x['display_label'],x['native_action_word']) for x in r['labels']]==[
            (0,'OFF',None),(1,'Black Hole',241),(2,'Luminescence',231),(3,'Ark Blast',234),
            (4,'Whiteout',237),(5,'Windburst',229),(6,'Torrent',228),(7,'Cataclysm',227),(8,'Inferno',226)]
    receipt=dict(case=name,exit_code=child.returncode,result_created=result.exists(),passed=passed,
                 process='terminal; synchronous bounded subprocess',
                 adapted_driver_sha256=hashlib.sha256((d/'prove-special-override-label-binding.py').read_bytes()).hexdigest())
    (d/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');receipts.append(receipt)
    if not passed:raise ValueError('actual invocation control failed: '+name)
r=dict(status='VALIDATED_PRODUCER_CONTROLS',method='Private input integrity/prerequisite controls, not FF12/native execution or independent acceptance',
       original_driver_sha256=hashlib.sha256(code.encode()).hexdigest(),root_adapter='one exact filesystem-root replacement only',cases=receipts)
(out/'result.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS: actual positive and four refusing prerequisite paths; all children terminal')
