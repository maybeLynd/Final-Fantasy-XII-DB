"""Two prepared callers through the reviewed original-byte access adapter."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;W=P.parent
ROOT=next(p for p in P.parents if(p/'Database/Tools/work/exe/FFXII_TZA.exe').is_file())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
status=json.loads((P/'extents-01.status.json').read_text())
if status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status.get('driver_sha256')!=sha(P/'prepare.py') or not(P/'extents-01.stdout').read_bytes() or(P/'extents-01.stderr').read_bytes():
    raise ValueError('current successful extent invocation required')
extents=json.loads((P/'extents-01.json').read_text())
if extents.get('complete') is not True or extents.get('driver_sha256')!=sha(P/'prepare.py') or extents.get('reused_preparation_sha256')!=sha(W/'ov42-gauge-callback-binding/prepare-handler-extents.py') or [b['entry'] for b in extents['bodies']]!=['0x331990','0x378a60']:
    raise ValueError('missing/current complete metadata required')
backend=W/'capture-index-path.py'
if sha(backend)!='cbfb9b4386d2e6db7618c36238362c3e0d9fce3d312c65c6f45b4957728ca497':
    raise ValueError('reviewed capture changed')
spec=importlib.util.spec_from_file_location('reviewed_capture',backend)
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
C.ROOT=ROOT;C.EXE=ROOT/'Database/Tools/work/exe/FFXII_TZA.exe'
C.ADAPTER=ROOT/'Database/Tools/analysis-kit/gfz-scripts/reg_tracking.py'
C.RANGES=[(int(b['entry'],16),int(b['end_exclusive'],16)) for b in extents['bodies']]
output=P/sys.argv[1]
if output.exists():raise ValueError('fresh output required')
sys.argv=[sys.argv[0],str(output)];C.main()
record=json.loads(output.read_text())
for body,mapped in zip(extents['bodies'],record['ranges']):
    actual=bytes.fromhex(''.join(i['bytes'] for i in mapped['instructions']))
    if actual.hex()!=body['physical_bytes'] or hashlib.sha256(actual).hexdigest()!=body['sha256']:
        raise ValueError('prepared original bytes disagree')
record.update(wrapper_complete=True,invocation_driver_sha256=sha(Path(__file__)),limits='STATIC_ONLY complete named callers, normal private-frame ABI. No inherited contents, natural field entry or transitive effects.')
output.write_text(json.dumps(record,indent=2)+'\n')
