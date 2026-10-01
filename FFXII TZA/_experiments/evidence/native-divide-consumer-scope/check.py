import sys
sys.dont_write_bytecode=True
import hashlib,json,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text())
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256'] and capstone.__version__==raw['tools']['capstone']
for p in raw['tools']['provider_files']:assert sha(Path(p['path']).read_bytes())==p['sha256']
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
s=(R/'divide.py').read_text();fragment=s[s.index('# Z\n'):s.index('# M\n')];assert (R/'exact-Z-fragment.py').read_text()==fragment and sha((R/'exact-Z-fragment.py').read_bytes())==raw['reference']['fragment_sha256']
assert 'except Exception: continue' in fragment and 'regs_access()' in fragment
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'actual reviewed register policy','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;actual=[]
for v in raw['reference']['ranges']:
 b=(R/v['copy']).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256'];lo=int(v['lo'],16);ii=list(cs.disasm(b,lo));assert sum(i.size for i in ii)==len(b)
 for i in ii:actual.append(dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,args=i.op_str,written=sorted(roles.written(i))))
assert actual==raw['independent_shared_adapter']
for b,index,want in [('8900',0,'w'),('8d00',1,'addr'),('830001',0,'rw')]:
 i=next(cs.disasm(bytes.fromhex(b),0));assert roles.op_kind(i,i.operands[index],index)==want
arms=raw['arms'];assert [a['mode'] for a in arms]==['baseline','analysis-error','decode-short'] and all(a['source_check']['tag']=='Z' and a['source_check']['ok'] for a in arms)
baseline,error,short=arms;assert not baseline['required_analysis_errors'] and all(x['supplied_bytes']==x['decoded_bytes'] for x in baseline['scan_calls'])
assert len(error['required_analysis_errors'])==1 and error['required_analysis_errors'][0]['pc']==raw['reference']['private_error_pc'] and error['wx']==baseline['wx']
assert short['scan_calls'][1]['supplied_bytes']>short['scan_calls'][1]['decoded_bytes'] and short['wx']==baseline['wx']
assert baseline['wx']==['0x25e55f','0x261dbc']
assert raw['preflight']['full_peer_default_run'] is False
if '--fault-rejects-analysis' in sys.argv:assert not error['source_check']['ok'],'Exact source Z suppresses required register-analysis failure and still passes'
if '--fault-rejects-short-decode' in sys.argv:assert not short['source_check']['ok'],'Exact source Z accepts incomplete declared-range decoding'
if '--fault-retract-baseline' in sys.argv:assert baseline['required_analysis_errors'],'Current independent declared-range baseline is complete and error-free; preserve its valid scoped facts'
result=dict(status='EXACT_Z_FRAGMENT_ACCEPTS_FAILED_PREREQUISITES',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=[dict(mode=a['mode'],source_Z_pass=a['source_check']['ok'],required_analysis_errors=a['required_analysis_errors'],scan_calls=a['scan_calls'],wx=a['wx']) for a in arms],interpretation='Exact immutable Z fragment keeps PASS after an injected required register-analysis exception and a private truncated decode after its known restore. It checks the positive writer list but does not make analysis/decode completeness a prerequisite. Independent current baseline fully decodes literal claimed ranges with reviewed adapter; valid arithmetic/guard and these bounded writer observations are not retracted. Full producer default/metadata U/native state not executed or certified here.',consumer_change='OPUS owns smallest Z producer prerequisite/coverage repair and affected negative-claim limits. Qualify U as metadata handler catalogue unless allowed primary dispatch/code proof supports semantic routing; preserve structural parse exception in governing standard. Correct81/82 static-vs-executed labels, default-empty-registry vs actual onlymodule, generic guesterror vs observednative vector. Route consumer/reviewer once, no peer edits.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS84 exact producer-fragment failed-prerequisite controls; full default/native claims unproved',flush=True)
