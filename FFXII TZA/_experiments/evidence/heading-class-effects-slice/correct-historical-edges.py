"""Additive re-reduction using the exact corrected default producer expression."""
import ast,hashlib,json,sys
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
source=(W/'capture.py').read_bytes();tree=ast.parse(source)
expressions=[v for d in ast.walk(tree) if isinstance(d,ast.Dict) for k,v in zip(d.keys,d.values) if isinstance(k,ast.Constant) and k.value=='external_jumps'];assert len(expressions)==1
expr=expressions[0];compiled=compile(ast.Expression(body=expr),'actual corrected default producer edge expression','eval')
# All current downstream actual capture files must share the same expression.
for file in ['capture-nested.py','capture-closure-r3.py','capture-object-state.py']:
 tt=ast.parse((W/file).read_bytes());ee=[v for d in ast.walk(tt) if isinstance(d,ast.Dict) for k,v in zip(d.keys,d.values) if isinstance(k,ast.Constant) and k.value=='external_jumps'];assert len(ee)==1 and ast.dump(ee[0])==ast.dump(expr)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
files=['raw.json','raw-nested.json','raw-closure-r3.json','raw-object-state.json'];changed=[];all_edges=[];inputs=[]
for name in files:
 raw=json.loads((W/name).read_bytes());inputs.append({'path':name,'sha256':sha(W/name)})
 for f in raw['callees']:
  data=(W/f['code_file']).read_bytes();assert len(data)==f['bytes']==f['decoded_bytes'] and hashlib.sha256(data).hexdigest()==f['code_sha256']
  ins=list(cs.disasm(data,int(f['entry'],16)));assert sum(i.size for i in ins)==len(data)
  ns={'ins':ins,'a':int(f['entry'],16),'size':f['bytes'],'capstone':capstone};edges=eval(compiled,ns)
  if '--fault-drop-conditional' in sys.argv:edges=[e for e in edges if not e['conditional']]
  before=[(e['pc'],e['target']) for e in f['external_jumps']];after=[(e['pc'],e['target']) for e in edges]
  if before!=after:changed.append({'capture':name,'entry':f['entry'],'old_jmp_only':f['external_jumps'],'corrected_all_external_jumps':edges})
  all_edges.append({'capture':name,'entry':f['entry'],'external_jumps':edges})
# Positive control was a real corrected downstream capture invocation, not helper existence.
actual=json.loads((W/'raw-object-state.json').read_bytes());ct=json.loads((W/'capture-object-state-terminal.json').read_bytes());assert ct['terminal'] and ct['returncode']==0 and not ct['stderr'] and ct['driver_sha256']==sha(W/'original-producers/capture-object-state.py')
f=next(f for f in actual['callees'] if f['entry']=='0x2e6300');want=[{'pc':'0x2e6303','target':'0x265510','mnemonic':'js','conditional':True,'resolved_immediate':True}];assert f['external_jumps']==want
for name in ['raw-nested.json','raw-object-state.json']:
 assert next(e for e in all_edges if e['capture']==name and e['entry']=='0x2e6300')['external_jumps']==want,'Conditional JS must survive the actual expression/re-reduction'
# Object capture selected two tail edges; historical raw field name was incorrect.
closure=json.loads((W/'raw-closure-r3.json').read_bytes());rowmap={x['pc']:x for f in closure['callees'] for x in f['instructions']};selected=[]
for e in actual['direct_call_sites']:
 x=rowmap[e['pc']];assert x['args']==e['target'];selected.append(dict(e,mnemonic=x['mnemonic'],kind='unconditional_tail' if x['mnemonic']=='jmp' else 'call'))
assert selected==[{'pc':'0x3e6bc7','target':'0x3e33e0','mnemonic':'jmp','kind':'unconditional_tail'},{'pc':'0x3e6bd7','target':'0x3e3440','mnemonic':'jmp','kind':'unconditional_tail'}]
if '--fault-tail-as-call' in sys.argv:assert all(x['kind']=='call' for x in selected),'Two selected source edges are JMP tails, not CALL sites'
result={'status':'ADDITIVE_EDGE_CORRECTION_VALID_SOURCE_ONLY','producer_sha256':hashlib.sha256(source).hexdigest(),'input_raw':inputs,'affected_edge_lists':changed,'corrected_edge_lists':all_edges,'object_capture_schema_correction':{'original_field':'direct_call_sites','correct_field':'selected_source_edges','values':selected},'limits':'Raw bytes/old drivers/receipts retained. Fix conditional-edge omission and one raw metadata label only; no class preservation/callback/native effects conclusion. Actual corrected capture JS positive control retained.'}
if '--fault-drop-conditional' not in sys.argv and '--fault-tail-as-call' not in sys.argv:(W/'edge-correction.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'affected':[(x['capture'],x['entry']) for x in changed],'selected_source_edges':selected},indent=2))
