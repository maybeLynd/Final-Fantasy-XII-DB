"""Validate the retained getter scope before its semantic reducer; no execution."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if(P/'inspect.py').exists():raise ValueError('local inspect.py would shadow stdlib dependency')
def load(name,file):
 s=importlib.util.spec_from_file_location(name,P/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
x=json.loads((P/'source-01.json').read_text());s=json.loads((P/'capture-01.status.json').read_text())
if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None or s['driver_sha256']!=sha(P/'capture.py') or not(P/'capture-01.stdout').read_bytes() or(P/'capture-01.stderr').read_bytes():raise ValueError('required capture failed')
if x.get('wrapper_complete') is not True or x['invocation_driver_sha256']!=sha(P/'capture.py'):raise ValueError('actual capture identity differs')
V=load('roles','validate-title-source-annotations.py');G=load('cfg','prove_owner_reload_order.py');a=V.validate(x)
if len(x['ranges'])!=1 or(x['ranges'][0]['start'],x['ranges'][0]['end_exclusive'],x['ranges'][0]['sha256'])!=('0x387090','0x387125','7fe996559221d1aae0ad0dfd1991bef228e8cbcc598eaa86eca585c65287fa87'):raise ValueError('wrong bounded getter input')
ix={int(i['pc'],16):i for r in x['ranges'] for i in r['instructions']};g=G.graph(ix,0x387090,0x387125)
if g['calls']!=[(0x3870bf,'0x31b860'),(0x3870ec,'0x31b860')] or g['returns']!=[0x387117,0x387124]:raise ValueError('getter effect/exit boundaries differ')
for pc,m,args in [(0x3870f6,'test','rax, rax'),(0x3870f9,'je','0x387118'),(0x3870fb,'test','rbx, rbx'),(0x3870fe,'je','0x387118'),(0x387100,'mov','ecx, 0x9f'),(0x387105,'cmp','word ptr [rax + 0x714], cx'),(0x38710c,'jne','0x387118'),(0x38710e,'movzx','eax, word ptr [rbx + 0x10]'),(0x387118,'movzx','eax, word ptr [rax + 0x714]')]:
 if(ix[pc]['mnemonic'],ix[pc]['args'])!=(m,args):raise ValueError('getter discriminator changed '+hex(pc))
out=dict(complete=True,method='A STATIC_ONLY feasibility, not semantic closure',driver_sha256=sha(Path(__file__)),source_sha256=sha(P/'source-01.json'),annotation=a,calls=[dict(pc=hex(pc),target=t) for pc,t in g['calls']],returns=[hex(pc) for pc in g['returns']],next_discriminator='Prove non9F supplied owner WORD714 reaches EAX/callerAX->R8W with no local range exclusion; keep two resolver returns distinct. Prove special9F substitution separately and determine field writer/admission prerequisites. Null second return branches to the raw WORD714 read; source-only low-address prediction, no live fault claim.',limits='This validates exact source/CFG and the intended discriminator, not natural callback returns, table initialization/identity, caller reachability, output-domain closure or independent acceptance.')
p=P/'feasibility-01.json'
if p.exists():raise ValueError('immutable feasibility result exists')
p.write_bytes((json.dumps(out,indent=2)+'\n').encode());print('VERIFIED149B complete getter/actual observer prerequisites; semantic reducer/field-writer proof next')
