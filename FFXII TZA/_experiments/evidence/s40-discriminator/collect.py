import csv,hashlib,json,struct,sys
from pathlib import Path
import capstone
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
sys.path.insert(0,str(ROOT/'agent_flow/tools'));import vbfextract
archive=Path('D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf')
record={'method':'A bounded original/static/data preparation; no native/live execution',
 'python_version':sys.version,'python_binary_sha256':sha(Path(sys.executable).read_bytes()),
 'extractor_sha256':sha((ROOT/'agent_flow/tools/vbfextract.py').read_bytes()),'resources':[]}
with archive.open('rb') as f:
 names,blocks=vbfextract.load_index(f)
 cut=sorted(p for p in names if '/jsondata/cutscenes/' in '/'+p.lower() and p.endswith('.json') and 'evt_t0005' not in p)
 assert cut
 # Index listing first, not a bulk read. Only first two bounded candidates are eligible.
 record['candidate_paths']=cut[:2]
 for path in cut[:2]:
  assert names[path][1]<128*1024
  raw=vbfextract.read_entry(f,names,blocks,path)
  obj=json.loads(raw.decode('utf-8-sig'))
  common=obj.get('Common',{}) if isinstance(obj,dict) else {}
  if 'mGlareLuminance' not in common or 'mGlareThreshold' not in common:continue
  (HERE/'scene.json').write_bytes(raw)
  sb,size,off=names[path];selected=[];cursor=off
  for i in range((size+65535)//65536):
   stored=blocks[sb+i] or 65536;f.seek(cursor);b=f.read(stored);assert len(b)==stored
   selected.append({'index':sb+i,'offset':cursor,'bytes':stored,'sha256':sha(b)});cursor+=stored
  record['resources'].append({'path':path,'entry_tuple':names[path],'bytes':len(raw),'sha256':sha(raw),
   'stored_blocks':selected,'selected_common':{k:common[k] for k in ('mGlareLuminance','mGlareThreshold','EnableDof','mDofFocusDistance','mDofApertureFnumber') if k in common}})
  break
 assert len(record['resources'])==1,'no prepared strict scene within two-entry budget'
 f.seek(0);index_size=struct.unpack('<4sI',f.read(8))[1];assert 0<index_size<64*1024*1024
 f.seek(0);record['archive_index_sha256']=sha(f.read(index_size));record['archive_index_bytes']=index_size
record['archive_entire_content_hashed']=False
exe=(ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes();assert sha(exe)=='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
pe=struct.unpack_from('<I',exe,60)[0];opt=struct.unpack_from('<H',exe,pe+20)[0];base=struct.unpack_from('<Q',exe,pe+48)[0];assert base==0x120000
sections=[]
for i in range(struct.unpack_from('<H',exe,pe+6)[0]):
 o=pe+24+opt+i*40;vs,va,rs,ro=struct.unpack_from('<IIII',exe,o+8);sections.append((base+va,min(vs,rs),ro))
def read(a,n):
 for va,size,off in sections:
  if va<=a and a+n<=va+size:return exe[off+a-va:off+a-va+n]
 raise AssertionError('unbacked image range')
rva,n=struct.unpack_from('<II',exe,pe+24+112+24);runtime_functions=list(struct.iter_unpack('<III',read(base+rva,n)))
graph=ROOT/'Database/Tools/work/graph/functions.tsv';extents={int(r['entry'],16):int(r['body_bytes']) for r in csv.DictReader(graph.open(),delimiter='\t')}
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);record['code']=[]
for a in (0x18CD90,0x194310):
 size=extents[a];assert 0<size<=1024
 containing=[r for r in runtime_functions if r[0]+base<=a<r[1]+base]
 assert not containing or containing[0][0]+base==a
 code=read(a,size);ins=list(md.disasm(code,a));assert sum(i.size for i in ins)==size
 record['code'].append({'entry':hex(a),'bytes':size,'hex':code.hex(),'sha256':sha(code),
 'runtime_function':containing[0] if containing else None,
 'instructions':[{'address':hex(i.address),'bytes':i.bytes.hex(),'op':i.mnemonic,'args':i.op_str} for i in ins]})
 print('ORIGINAL',hex(a),size)
 for i in ins:
  if a==0x194310 or any(x in i.op_str for x in ('0xf4','0xf8','0x110')):print(hex(i.address),i.mnemonic,i.op_str)
record['exe_sha256']=sha(exe);record['capstone_version']=capstone.__version__
record['extent_graph_sha256']=sha(graph.read_bytes());record['extent_graph_role']='Historical bound hint, directly qualified against exact image/boundaries; not current semantic mirror/count authority.'
paths=['Database/FFXII TZA/_index/L2-VERDICTS.md','Database/FFXII TZA/17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md']
fixture=ROOT/'Database/FFXII TZA/_index/candidates/s40-opus-replay-post-process-init'
record['retained_fixture']={p.name:{'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in [fixture/'README.md',fixture/'result.json',fixture/'check.py',fixture/'crt_bridge.py']}
for source_name,target_name in [('README.md','retained-init-README.md'),('result.json','retained-init-result.json')]:
 (HERE/target_name).write_bytes((fixture/source_name).read_bytes())
(HERE/'retained-init-driver.txt').write_bytes((fixture/'check.py').read_bytes())
record['canonical_preimages']={p:{'bytes':len((ROOT/p).read_bytes()),'sha256':sha((ROOT/p).read_bytes())} for p in paths}
verdict=(ROOT/paths[0]).read_text();row=next(line for line in verdict.splitlines() if line.startswith('| **S-40**'))
assert 'AUDITSEM-REQ-OPUS-426' in row and 'device/live boundary preserved' in row
(HERE/'retained-current-verdict-row.txt').write_text(row+'\n')
result=json.loads((fixture/'result.json').read_text());assert result['ok'] and result['live_game'] is False and len(result['cases'])==8 and all(result['cases'].values())
record['retained_scope']={'accepted_result':'8 case outcomes; no rerun','live_game':False,'device':'one-method deferred-context model',
 'P2_20C_flags':result['results']['P2']['flags_20C'],'P2_runtime_result_ok':result['results']['P2']['ok'],
 'P2_halt':result['results']['P2']['halt'],
 'P2_handle':result['results']['P2']['handle'],'P2_lib':result['results']['P2']['lib'],
 'P2_init_result':result['results']['P2']['rets']['ctx_init'],
 'P2_plus108':result['results']['P2']['plus_108'],
 'limits':'Declared expected refusal/fault branch, not successful real immediate-context initialization.'}
(HERE/'source.json').write_text(json.dumps(record,indent=2)+'\n')
print('SCENE',record['resources'][0]['path'],record['resources'][0]['selected_common'])
