"""Method A: exact original typed-pop/reporting leaf and current consumers."""
import ast,hashlib,json,struct,subprocess,sys,types
from pathlib import Path
import capstone
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=W/'retained'
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):
 q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0 and not q.stderr
 return q.stdout
def run():
 assert (W/'check.py').is_file();compile((W/'check.py').read_bytes(),str(W/'check.py'),'exec')
 assert not R.exists(), 'Write-once static source capture'
 sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
 ok,d=team.board_status(team.BOARD);assert ok,d
 t=next(t for t in json.loads(team.BOARD.read_bytes())['tasks'] if t['id']=='ASTRA-SCRIPTVM-RETAIL-REPORT-CONSUMER-BOUNDARY')
 assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
 R.mkdir();ident={'method':'A static original source/current canonical consumers; no guest/native/live execution', 'driver_sha256':sha(Path(__file__)), 'python':sys.executable,'python_version':sys.version,'capstone':capstone.__version__,'head':git('rev-parse','HEAD').decode().strip(),'sources':[]}
 prior=Path('Database/FFXII TZA/_experiments/evidence/script-store-saturation/retained')
 for name in ['shipping-reader.py','reg_tracking.py']:
  p=prior/name;b=p.read_bytes();assert b==git('show','8db582868ae4a72bae3f9e76c1d709844e9d9d93:'+p.as_posix())
  (R/name).write_bytes(b);ident['sources'].append({'path':p.as_posix(),'copy':name,'sha256':sha(p),'verified_at':'8db582868ae4a72bae3f9e76c1d709844e9d9d93'})
 pages=['Database/FFXII TZA/01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md','Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md','Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md']
 for name in pages:
  p=Path(name);b=p.read_bytes();copy='pages/'+p.name;(R/'pages').mkdir(exist_ok=True);(R/copy).write_bytes(b)
  ident['sources'].append({'path':name,'copy':copy,'sha256':sha(p),'commit':git('log','-1','--format=%H','--',name).decode().strip(),'blob':git('hash-object','--no-filters',name).decode().strip()})
 ident['provider_files']=[]
 for p in [Path(sys.executable),Path(capstone.__file__),Path(capstone.__file__).parent/'lib/capstone.dll']:
  ident['provider_files'].append({'path':str(p),'sha256':sha(p)})
 (W/'pre-capture-identity.json').write_bytes((json.dumps(ident,indent=2)+'\n').encode())
 # Extract the unchanged certified reader functions only. Supply the same
 # certified image at the repo reference pathname; do not import its harness.
 rt=ast.parse((R/'shipping-reader.py').read_text('utf-8'))
 nodes=[n for n in rt.body if isinstance(n,ast.FunctionDef) and n.name in ['load_image','img_rd']]
 assert len(nodes)==2
 ns={'EXE':'Database/Tools/work/exe/FFXII_TZA.exe','SHA':SHA,'IMG_LO':0x120000,'hashlib':hashlib,'struct':struct}
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'original extracted certified reader','exec'),ns)
 raw,sections=ns['load_image']();assert hashlib.sha256(raw).hexdigest()==SHA
 roles=types.ModuleType('shared_roles');exec(compile((R/'reg_tracking.py').read_bytes(),'shared reviewed access-role adapter','exec'),roles.__dict__)
 cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True
 bodies=[]
 for label,pc,size in [('typed-pop',0x267e60,256),('report-wrapper',0x8620c0,14),('folded-return',0x16d6a0,3)]:
  b=ns['img_rd'](raw,sections,pc,size);(R/(label+'.bin')).write_bytes(b)
  rows=[{'pc':hex(i.address),'bytes':i.bytes.hex(),'mnemonic':i.mnemonic,'args':i.op_str,'memory':[{'kind':roles.op_kind(i,o,j),'bytes':o.size} for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]} for i in cs.disasm(b,pc)]
  assert sum(len(bytes.fromhex(i['bytes'])) for i in rows)==size
  bodies.append({'name':label,'pc':hex(pc),'bytes':size,'sha256':hashlib.sha256(b).hexdigest(),'instructions':rows})
 ident['exe']={'path':ns['EXE'],'sha256':SHA,'external':True,'limits':'Read-only certified image. Not copied/exported; no process/module observation.'}
 for s in ident['sources']:assert sha(Path(s['path']))==s['sha256'],'Source changed during capture'
 assert sha(Path(ns['EXE']))==SHA
 output={'identity':ident,'bodies':bodies,'limits':'Physical access/control flow and original code identity only. No callback stub, interpreter execution, native exceptions, actual authored reachability, resource lifetime or live observation.'}
 (W/'raw.json').write_bytes((json.dumps(output,indent=2)+'\n').encode())
 print('RETAINED_ORIGINAL_TYPED_POP_AND_RETURN_CHAIN')
if __name__=='__main__':run()
