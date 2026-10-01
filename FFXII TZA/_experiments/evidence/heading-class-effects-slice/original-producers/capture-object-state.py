"""Read-only primary-byte feasibility capture; no class preservation verdict."""
import ast,hashlib,json,struct,subprocess,sys,types
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained/object-state';assert not R.exists();R.mkdir()
prior=Path('Database/FFXII TZA/_experiments/evidence/heading-extent-repair-review')
sys.path.insert(0,str((prior/'python-deps').resolve()))
import capstone,pefile
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;b=json.loads(team.BOARD.read_bytes());t=next(t for t in b['tasks'] if t['id']=='ASTRA-HEADING-CLASS-EFFECTS-SLICE');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest={x['path']:x for x in json.loads((prior/'manifest.json').read_bytes())['members']}
needed=['retained/producer-source.py','retained/functions.tsv','retained/intervening-body963.bin','retained/reg_tracking.py','python-deps/pefile.py']
for n in needed:assert sha(prior/n)==manifest[n]['sha256'] and (prior/n).stat().st_size==manifest[n]['bytes']
identity={'method':'A justified native nested source capture; no machine-code/game execution','prior_commit':'feb631dd4755e77a1edfed3c9b20f7d629d30d70','driver_sha256':sha(Path(__file__)),'inputs':[{'path':str(prior/n),'sha256':sha(prior/n),'published_member':n} for n in needed],'providers':[]}
for p in [Path(sys.executable),Path(capstone.__file__),Path(capstone.__file__).parent/'lib/capstone.dll',Path(pefile.__file__)]:identity['providers'].append({'path':str(p),'sha256':sha(p)})
identity['python']=sys.version;identity['capstone']=capstone.__version__;identity['loaded_pefile']=pefile.__file__
exe=Path('Database/Tools/work/exe/FFXII_TZA.exe');assert sha(exe)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8';identity['exe']={'path':str(exe),'sha256':sha(exe),'external':True}
blob=exe.read_bytes();pe=pefile.PE(str(exe),fast_load=True);BASE=pe.OPTIONAL_HEADER.ImageBase
SECS=[(s.Name.rstrip(b'\0').decode(),BASE+s.VirtualAddress,max(s.Misc_VirtualSize,s.SizeOfRawData),s.PointerToRawData,s.SizeOfRawData) for s in pe.sections]
# Reuse unchanged reviewed producer parser functions, not a new extent framework.
source=(prior/'retained/producer-source.py').read_bytes();(R/'extent-parser-source.py').write_bytes(source)
nodes=[x for x in ast.parse(source).body if isinstance(x,ast.FunctionDef) and x.name in ['OFF','chain_root']];assert len(nodes)==2
ns={'blob':blob,'BASE':BASE,'SECS':SECS,'struct':struct};exec(compile(ast.Module(body=nodes,type_ignores=[]),'original879652c93 extent parser functions','exec'),ns)
OFF=ns['OFF'];pd=next(x for x in SECS if x[0]=='.pdata');praw=blob[pd[3]:pd[3]+pd[4]];pent={};records={}
for j in range(0,len(praw)-11,12):
 bb,ee,uu=struct.unpack('<III',praw[j:j+12])
 if bb:pent[BASE+bb]=(BASE+ee,BASE+uu);records[BASE+bb]={'table_pc':BASE+(pd[1]-BASE)+j,'raw_runtime_function':praw[j:j+12].hex()}
ns['pent']=pent;roots={a:ns['chain_root'](a) for a in pent}
roles=types.ModuleType('roles');policy=(prior/'retained/reg_tracking.py').read_bytes();(R/'reg_tracking.py').write_bytes(policy);exec(compile(policy,'shared reviewed access-role adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
steer=(prior/'retained/intervening-body963.bin').read_bytes();assert blob[OFF(0x2e45e0):OFF(0x2e45e0)+963]==steer
parent=json.loads((W/'raw.json').read_bytes());initial=json.loads((W/'capture-terminal.json').read_bytes());controls=json.loads((W/'source-checks-terminal.json').read_bytes())
assert initial['terminal'] and initial['returncode']==0 and not initial['stderr'] and initial['driver_sha256']==sha(W/'original-producers/capture.py')
assert controls[0]['returncode']==0 and controls[0]['terminal'] and not controls[0]['stderr'] and controls[0]['checker_sha256']==sha(W/'check-source.py')
identity['previous_raw_sha256']=sha(W/'raw.json');identity['previous_driver_sha256']=sha(W/'original-producers/capture.py')
# Three mode0 calls plus class3 zero-arg position writer and conditional clear.
targets=[0x2e6300,0x3e33e0,0x3e3440]
closure=json.loads((W/'raw-closure-r3.json').read_bytes());ct=json.loads((W/'capture-closure-r3-terminal.json').read_bytes());assert ct['terminal'] and ct['returncode']==0 and not ct['stderr'] and ct['driver_sha256']==sha(W/'original-producers/capture-closure-r3.py')
identity['closure_source_sha256']=sha(W/'raw-closure-r3.json');identity['edge_policy']='Corrected default producer uses CS_GRP_JUMP including conditional branches; 2E6300 is a deliberate smallest regression control, not a new native semantic experiment.'
wrappers=[f for f in closure['callees'] if f['entry'] in ['0x3e6bc0','0x3e6bd0']];calls=[]
assert len(wrappers)==2
for f in wrappers:
 assert any(x['mnemonic']=='add' and x['args']=='rcx, 0x580' for x in f['instructions'])
 jump=next(x for x in f['instructions'] if x['mnemonic']=='jmp');calls.append((int(jump['pc'],16),int(jump['args'],16)))
assert {a for _,a in calls}=={0x3e33e0,0x3e3440}
cat={}
for line in (prior/'retained/functions.tsv').read_text('utf-8').splitlines()[1:]:
 p=line.split('\t')
 try:a=int(p[0],16)
 except ValueError:continue
 if a in targets:cat[a]=(p[1],int(p[2]),line)
assert set(cat)==set(targets)
raw=[]
for a in targets:
 name,size,line=cat[a];frags=sorted((f,pent[f][0],pent[f][1]) for f in pent if roots[f]==a)
 contiguous=bool(frags) and all(frags[k][1]==frags[k+1][0] for k in range(len(frags)-1))
 union=frags[-1][1]-frags[0][0] if frags else None
 validated=contiguous and frags[0][0]==a and union==size
 code=blob[OFF(a):OFF(a)+size];file=f'{a:08X}.bin';(R/file).write_bytes(code)
 ins=list(cs.disasm(code,a));rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'written':sorted(roles.written(i)),'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
 uw=[]
 for f,e,u in frags:
  h=blob[OFF(u):OFF(u)+4];n=4+2*((h[2]+1)&~1);flags=h[0]>>3;tail=12 if flags&4 else 4 if flags&3 else 0
  uw.append(dict(begin=hex(f),end=hex(e),unwind=hex(u),flags=flags,raw_unwind=blob[OFF(u):OFF(u)+n+tail].hex(),**records[f]))
 raw.append({'entry':hex(a),'name':name,'catalogue_line':line,'bytes':size,'code_file':'retained/object-state/'+file,'code_sha256':hashlib.sha256(code).hexdigest(),'extent_status':'UNWIND_UNION_MATCH' if validated else 'UNPROVED_CATALOGUE_ONLY','unwind_union':union,'unwind_contiguous':contiguous,'fragments':uw,'decoded_bytes':sum(i.size for i in ins),'instructions':rows,'call_sites':[{'pc':hex(i.address),'target':i.op_str} for i in ins if i.mnemonic=='call'],'external_jumps':[{'pc':hex(i.address),'target':i.op_str,'mnemonic':i.mnemonic,'conditional':i.mnemonic!='jmp','resolved_immediate':i.operands[0].type==capstone.CS_OP_IMM} for i in ins if i.group(capstone.CS_GRP_JUMP) and (i.operands[0].type!=capstone.CS_OP_IMM or not a<=i.operands[0].imm<a+size)],'limits':'SOURCE_ONLY; operand role is not actor alias proof. Nested native/import/callback/normal return effects not summarized yet.'})
assert sha(exe)==identity['exe']['sha256']
for x in identity['inputs']:assert sha(Path(x['path']))==x['sha256']
(W/'identity-object-state.json').write_text(json.dumps(identity,indent=2)+'\n');(W/'raw-object-state.json').write_text(json.dumps({'direct_call_sites':[{'pc':hex(p),'target':hex(a)} for p,a in calls],'unique_targets':targets,'callees':raw,'status':'SOURCE_ONLY_NOT_CLASS_PRESERVATION','selection':'Two object-state tail targets and deliberate one-source edge regression control, not three new semantic cases. Prior raw/driver archives preserved.','cleanup':'Original references unchanged, no game/native/browser/input/instrument/process control.'},indent=2)+'\n')
print(json.dumps({'status':'SOURCE_ONLY_NOT_CLASS_PRESERVATION','unique_targets':len(targets),'extent_status':[(r['entry'],r['extent_status'],r['bytes'],r['unwind_union']) for r in raw]},indent=2))
