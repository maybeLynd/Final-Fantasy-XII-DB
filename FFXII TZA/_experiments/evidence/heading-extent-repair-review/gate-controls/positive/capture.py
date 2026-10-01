"""Original producer invocation and one labelled catalogue input intervention."""
import ast,hashlib,json,os,struct,subprocess,sys,types
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained'
sys.path.insert(0,str(W/'python-deps'))
import capstone,pefile
assert Path(pefile.__file__).resolve()==W/'python-deps/pefile.py'
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*a):
 q=subprocess.run(['git',*a],capture_output=True);assert q.returncode==0 and not q.stderr;return q.stdout
assert not R.exists();R.mkdir()
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d
b=json.loads(team.BOARD.read_bytes());t=next(t for t in b['tasks'] if t['id']=='OPUS-REQ-ASTRA-VERIFY-HEADING-EXTENT-REPAIR');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
source=Path('Database/Tools/analysis-kit/gfz-scripts/falsify_heading_delta.py')
page=Path('Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md')
record=Path('Database/FFXII TZA/_index/candidates/heading-full-extent-repair-0929/README.md')
catalog=Path('Database/Tools/work/graph/functions.tsv');exe=Path('Database/Tools/work/exe/FFXII_TZA.exe')
prior=Path('Database/FFXII TZA/_experiments/evidence/heading-passthrough-alias-boundary')
inputs=[(source,'producer-source.py'),(page,'contract.md'),(record,'repair-readme.md'),(catalog,'functions.tsv'),(prior/'intervening-body.json','prior-intervening-body.json'),(prior/'retained/intervening-body963.bin','intervening-body963.bin'),(prior/'retained/caller.bin','caller330.bin'),(prior/'retained/reg_tracking.py','reg_tracking.py')]
identity={'method':'A original static bytes/retained review and producer Python; not shipping-code execution/live game','driver_sha256':sha(Path(__file__)),'wrapper_sha256':sha(W/'h8-input-intervention.py'),'head':git('rev-parse','HEAD').decode().strip(),'sources':[],'providers':[]}
for p,n in inputs:
 data=p.read_bytes();(R/n).write_bytes(data);identity['sources'].append({'path':p.as_posix(),'copy':n,'sha256':hashlib.sha256(data).hexdigest()})
committed=git('show','879652c93:'+source.as_posix());(R/'producer-879652c93.py').write_bytes(committed)
assert source.read_bytes().replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n'),'Current producer differs from requested repair'
identity['producer_commit']={'commit':'879652c93','sha256':hashlib.sha256(committed).hexdigest(),'raw_equality':source.read_bytes()==committed,'text_comparison':'Only CRLF->LF comparison; both original raw byteversions retained'}
for p in [Path(sys.executable),Path(capstone.__file__),Path(capstone.__file__).parent/'lib/capstone.dll',Path(pefile.__file__)]:identity['providers'].append({'path':str(p),'sha256':sha(p)})
identity['dependency_provenance']='Reused exact published1548d3896 python-deps; initial import failure retained under run-01-import-failure. No install/download.'
identity['dependency_files']=[{'path':str(p),'sha256':sha(p)} for p in sorted((W/'python-deps').rglob('*')) if p.is_file()]
identity['python_version']=sys.version;identity['capstone_version']=capstone.__version__;identity['pefile_version']=pefile.__version__
identity['exe']={'path':exe.as_posix(),'sha256':sha(exe),'external':True};assert identity['exe']['sha256']==SHA
(W/'identity-before.json').write_text(json.dumps(identity,indent=2)+'\n')
# Retained bytes bind back to exact certified shipping image, without changing it.
pe=pefile.PE(str(exe),fast_load=True);base=pe.OPTIONAL_HEADER.ImageBase;assert base==0x120000
blob=exe.read_bytes();off=lambda va:pe.get_offset_from_rva(va-base)
for a,n,size in [(0x2e45e0,'intervening-body963.bin',963),(0x2e5030,'caller330.bin',330)]:assert blob[off(a):off(a)+size]==(R/n).read_bytes()
# Reviewed central access-role adapter is used for the actual normalized decode.
roles=types.ModuleType('roles');exec(compile((R/'reg_tracking.py').read_bytes(),'shared reviewed access-role adapter','exec'),roles.__dict__)
cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
ins=list(cs.disasm((R/'intervening-body963.bin').read_bytes(),0x2e45e0));assert sum(i.size for i in ins)==963
rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'written':sorted(roles.written(i)),'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in ins]
priorbody=json.loads((R/'prior-intervening-body.json').read_bytes());assert rows==priorbody['instructions']
entries=priorbody['exception_directory']['selected_entries'];assert len(entries)==8
runtime={e['raw_runtime_function']:e for e in entries};roots=[]
for e in entries:
 # Verify both records and unwind payloads against the image, not just summary.
 assert blob[off(int(e['table_pc'],16)):off(int(e['table_pc'],16))+12].hex()==e['raw_runtime_function']
 u=bytes.fromhex(e['raw_unwind_info']);assert blob[off(base+int(e['unwind_rva'],16)):off(base+int(e['unwind_rva'],16))+len(u)]==u
 cur=e;seen=set()
 while cur['flags']&4:
  assert cur['begin'] not in seen;seen.add(cur['begin']);u=bytes.fromhex(cur['raw_unwind_info']);trailer=4+2*((u[2]+1)&~1);cur=runtime[u[trailer:trailer+12].hex()]
 roots.append(cur['begin'])
assert roots==['0x2e45e0']*8
sizes=[e['bytes'] for e in entries];assert sizes==[40,27,397,45,93,144,47,170]
assert all(entries[k]['end']==entries[k+1]['begin'] for k in range(7)) and sum(sizes)==963
# Full inherited script invokes all its old checks; this review awards only H8/status.
receipts=[]
for label,a in [('original',[sys.executable,'-B',str(source)]),('first-fragment-catalogue',[sys.executable,'-B',str(W/'h8-input-intervention.py'),'--source',str(source),'--catalog',str(R/'functions.tsv')])]:
 env=os.environ.copy();env['PYTHONPATH']=str(W/'python-deps')
 q=subprocess.run(a,capture_output=True,text=True,env=env)
 receipts.append({'case':label,'argv':a,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'terminal':True,'producer_sha256':sha(source),'wrapper_sha256':identity['wrapper_sha256'] if label!='original' else None})
 (W/'producer-terminal.json').write_text(json.dumps(receipts,indent=2)+'\n')
 assert q.returncode==0 and not q.stderr,'Unexpected setup/process failure; retained status, no blind retry'
for x in identity['sources']:assert sha(Path(x['path']))==x['sha256'],'Source changed during test'
assert sha(exe)==SHA
(W/'identity.json').write_text(json.dumps(identity,indent=2)+'\n')
text=(R/'functions.tsv').read_text('utf-8');line=next(x for x in text.splitlines() if x.startswith('002E45E0\t'));p=line.split('\t');assert p[:3]==['002E45E0','Movement_UpdateSteeringTowardTarget','963']
new=p.copy();new[2]='40';changed='\t'.join(new)
mutant=text.replace(line,changed);assert mutant!=text and text.count(line)==1
mutation={'method':'io.open substitution on exact producer catalogue pathname, io.StringIO input; producer source unchanged','original_line':line,'replacement_line':changed,'changed_field':'size963->40 only','full_decoded_original_sha256':hashlib.sha256(text.encode()).hexdigest(),'full_decoded_mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest(),'limits':'Catalogue-reader intervention, not original FF12 behavior, reference EXE bytes unchanged'}
(W/'catalogue-intervention.json').write_text(json.dumps(mutation,indent=2)+'\n')
raw={'sizes':sizes,'roots':roots,'instructions':rows,'return_pcs':[hex(i.address) for i in ins if i.mnemonic=='ret'],'call_pcs':[hex(i.address) for i in ins if i.mnemonic=='call'],'first_fragment_return_pcs':[hex(i.address) for i in ins if i.address<0x2e4608 and i.mnemonic=='ret'],'original_sources_unchanged':True,'exe_unchanged':True,'control':'Two producer Python processes terminal; no persistent instrument/native game/browser control'}
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('ORIGINAL_H8_AND_FIRST_FRAGMENT_INPUT_STATUS_CAPTURED')
