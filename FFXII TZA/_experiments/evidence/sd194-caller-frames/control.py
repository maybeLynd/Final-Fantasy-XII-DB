"""Three actual CLI controls for upstream, completeness and same-size stack edits."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
state=json.loads((P/'proof-02.status.json').read_text())
if state.get('terminal') is not True or state.get('exit')!=0 or state.get('exception') is not None or state.get('driver_sha256')!=sha(P/'prove.py') or json.loads((P/'result-02.json').read_text()).get('producer_complete') is not True:
    raise ValueError('positive current producer failed')
destination=P/sys.argv[1];destination.mkdir()
rows=[]
for name,expected in [('upstream-failed','required upstream failed: extents-01'),
                      ('metadata-incomplete','incomplete metadata/wrapper'),
                      ('same-size-stack-change','shipping original body identity mismatch')]:
    folder=destination/name;folder.mkdir();source=folder/'source';source.mkdir()
    for filename in ['prepare.py','capture.py','extents-01.status.json','extents-01.stdout','extents-01.stderr',
                     'capture-01.status.json','capture-01.stdout','capture-01.stderr','extents-01.json','source-01.json','retained-loader-source-01.json']:
        shutil.copyfile(P/filename,source/filename)
    if name=='upstream-failed':
        target=source/'extents-01.status.json';data=json.loads(target.read_text());data['exit']=1
    elif name=='metadata-incomplete':
        target=source/'extents-01.json';data=json.loads(target.read_text());data['complete']=False
    else:
        target=source/'source-01.json';data=json.loads(target.read_text());body=data['ranges'][0]
        instruction=next(i for i in body['instructions'] if i['pc']=='0x331992')
        instruction.update(bytes='4883ec18',args='rsp, 0x18')
        blob=bytes.fromhex(''.join(i['bytes'] for i in body['instructions']));digest=hashlib.sha256(blob).hexdigest();body['sha256']=digest
        metadata=json.loads((source/'extents-01.json').read_text());metadata['bodies'][0].update(physical_bytes=blob.hex(),sha256=digest)
        (source/'extents-01.json').write_text(json.dumps(metadata,indent=2))
    target.write_text(json.dumps(data,indent=2))
    output=folder/'result.json';command=[sys.executable,'-B',str(P/'prove.py'),str(output),'--source',str(source)]
    child=subprocess.run(command,capture_output=True,text=True,timeout=60)
    (folder/'stdout').write_text(child.stdout);(folder/'stderr').write_text(child.stderr)
    ok=child.returncode!=0 and expected in child.stderr and not output.exists()
    receipt=dict(argv=command,driver_sha256=sha(P/'prove.py'),exit=child.returncode,terminal=True,expected_diagnostic=expected,
                 expected_refusal=ok,result_exists=output.exists())
    (folder/'receipt.json').write_text(json.dumps(receipt,indent=2));rows.append(receipt)
    if not ok:raise ValueError('concrete prerequisite control failed: '+name)
(destination/'result.json').write_text(json.dumps(dict(producer_complete=True,status='THREE_ACTUAL_PREREQUISITE_REFUSALS',
    driver_sha256=sha(Path(__file__)),positive_result_sha256=sha(P/'result-02.json'),cases=rows),indent=2))
print(json.dumps(dict(status='THREE_ACTUAL_PREREQUISITE_REFUSALS',native_or_live_runs=0)))
