"""Retain the invalid first reducer and correct its actual default procedure."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained/invalid-zero-suffix-assumption';R.mkdir(exist_ok=False);old=(W/'check.py').read_bytes();(R/'check-before.py').write_bytes(old)
s=old.decode();needle='and len(zeros)<=2';assert s.count(needle)==1
replacement="and len(zeros)<=(2 if '--fault-two-padding' in sys.argv else 3), 'Two-record suffix assumption excludes actual three-record suffix'"
s=s.replace(needle,replacement).replace("Observed all-zero suffix with no instruction-start flag, compatible with published 0..2 end marks; no real instruction-start at line0 in this corpus","Observed all-zero suffix with no instruction-start flag; actual range0..3, not canonical0..2; no real instruction-start at line0 in this corpus")
s=s.replace("All61 line0 records are observed all-zero suffixes of0..2 records and no start flags in this corpus.","All61 line0 records are observed all-zero suffixes of0..3 records and no start flags in this corpus; ctrl1, btl22, map1/map3 each have3. This refutes the canonical0..2 bound, not a q2/q3 formula.")
(W/'check.py').write_text(s)
raw=json.loads((W/'raw.json').read_text());exception=[]
for m in raw['modules']:
 for scope in m['scopes']:
  z=[x for x in scope['records'] if x['line']==0]
  if len(z)>2:exception.append(dict(module=m['name'],scope=scope['index'],count=len(z),indices=[x['index'] for x in z],q0=scope['q0'],q1=scope['q1'],record_count=scope['record_count']))
assert [(x['module'],x['scope'],x['count']) for x in exception]==[('ctrl',1,3),('btlctrl',22,3),('mapctrl',1,3),('mapctrl',3,3)]
(R/'failure.json').write_text(json.dumps(dict(status='INVALID_ZERO_SUFFIX_ASSUMPTION',phase='First reducer before result creation; primary raw capture complete',old_checker_sha256=hashlib.sha256(old).hexdigest(),assertion='Every zero-line suffix has at most2 records',cause='Copied canonical0..2 end-mark bound without testing the actual source domain. Four actual q0 scopes have3 all-zero suffix records, no start flags.',exceptions=exception,correction='Actual default reducer now preserves and reports0..3 and fault-two-padding must fail. Raw/inputs/driver not recaptured; canonical producer/domain/prose correction routed to owners.',limits='No original compiler padding cause or code byte length proven merely by zero source records.'),indent=2)+'\n')
original=(W/'capture.py').read_bytes();assert original==(W/'retained/driver-before-run.py').read_bytes()
c=original.decode();needle="W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()";assert c.count(needle)==1
c=c.replace(needle,needle+"\nif (W/'raw.json').exists():\n import subprocess\n subprocess.run([sys.executable,str(W/'check.py')],check=True)\n sys.exit(0) # Immutable retained capture: default consumes corrected reducer, no recapture.")
needle="c=category(record['line'],record['block'],blocks);controls.append"
assert c.count(needle)==1
c=c.replace(needle,"encoded=struct.pack('<HBB',record['line'],record['block'],record['flag']);line,block,flag=struct.unpack('<HBB',encoded);record=dict(record,line=line,block=block,flag=flag,record_hex=encoded.hex());c=category(line,block,blocks);controls.append")
(W/'capture.py').write_text(c)
(R/'producer-correction.json').write_text(json.dumps(dict(original_driver_sha256=hashlib.sha256(original).hexdigest(),current_driver_sha256=hashlib.sha256((W/'capture.py').read_bytes()).hexdigest(),raw_control_cause='Initial coordinate-only control dictionaries kept original record_hex. Their scalar category control remains valid, but not raw-byte parser proof.',actual_default_fix='Existing raw uses corrected checker with actual4B encode/decode controls. Future fresh capture controls encode/decode the mutated record and update its hex consistently. Initial raw/driver preserved; no recapture.'),indent=2)+'\n')
print('Preserved invalid zero-suffix reduction and original capture; corrected default reducer/producer path without recapture',flush=True)
