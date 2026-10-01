"""Read original named entry bindings; no game or bytecode execution."""
import ast,datetime,hashlib,json,re,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
if (W/'raw.json').exists():
 import subprocess
 subprocess.run([sys.executable,str(W/'check.py')],check=True);sys.exit(0)
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d
t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-NAMED-ENTRY-LINE-CONVENTION');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
if R.exists():
 assert (W/'diagnostic.json').exists() and not (W/'raw.json').exists()
else:R.mkdir(exist_ok=False)
def preserve(name,data):
 p=R/name
 if p.exists():assert p.read_bytes()==data,name
 else:p.write_bytes(data)
parent=Path('Database/FFXII TZA/_experiments/evidence/sn1-q0-source-coordinate-domain');pr=json.loads((parent/'raw.json').read_text())
parser=parent/'retained/selected-sbn-functions.py';pb=parser.read_bytes();assert sha(pb)==pr['reference']['selected_parser_sha256']
g={'struct':struct};exec(compile(pb,'retained unchanged OPUS SBN parser','exec'),g)
preserve('selected-sbn-functions.py',pb)
consumer=Path('Database/FFXII TZA/01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md');cb=(R/'consumer-before.md').read_bytes() if (R/'consumer-before.md').exists() else consumer.read_bytes();preserve('consumer-before.md',cb)
layout=Path('Database/FFXII TZA/25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md');lb=(R/'ebp-layout-before.md').read_bytes() if (R/'ebp-layout-before.md').exists() else layout.read_bytes();preserve('ebp-layout-before.md',lb)
if not (R/'driver-before-run.py').exists():preserve('driver-before-run.py',Path(__file__).read_bytes())
preserve('driver-after-shared-tail-fix.py',Path(__file__).read_bytes())
root=Path('D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin');identities=[];rows=[];bindings=[]
def cstr(b,o,end=None):
 assert o==0 or b[o-1]==0
 z=b.index(b'\0',o,end or len(b));return b[o:z].decode('cp932',errors='strict')
for m in ['ctrl','btlctrl','evctrl','mapctrl']:
 files={}
 for ext in ['dbg','sbn','ebp']:
  p=root/(m+'.'+ext);data=p.read_bytes()
  if ext!='ebp':
   pi=next(i for i in pr['reference']['files'] if i['module']==m and i['extension']==ext)
   assert sha(data)==pi['sha256'] and data==(parent/'retained'/p.name).read_bytes()
  files[ext]=data;preserve(p.name,data)
  identities.append(dict(module=m,extension=ext,path=str(p),bytes=len(data),sha256=sha(data),provenance='Admitted extraction used by peers; DBG/SBN bytes also equal immutable60 input; no fresh whole-VBF provenance audit'))
 b,s,e=files['dbg'],files['sbn'],files['ebp'];blocks=[]
 for bo,be in g['sbn_blocks'](s):
  L,bases,starts,te=g['sbn_group_read'](s,bo);assert L==len(starts)>0
  blocks.append([dict(offset=a,hex=s[a:s.index(b'\0',a,be)].hex(),text=s[a:s.index(b'\0',a,be)].decode('cp932',errors='strict')) for a in starts])
 assert e[:4]==b'EBP2' and u32(e,4)==20
 base=u32(e,0x10);assert base==0x80 and u32(e,base)==0x8000000B
 end=base+u32(e,base+4);assert base<end<=len(e)
 D=base+u32(e,base+0x18);ns=u32(e,D);assert 0<ns<100 and D+4+48*ns<=end
 namebase=base+u32(e,base+0x4C);assert base<namebase<end
 o=u32(b,0);assert u32(b,o)==ns
 offs=struct.unpack_from('<%dI'%(4*ns+1),b,o+4);heap=u32(b,8);assert o<heap<len(b)
 for sc in range(ns):
  entoff=D+4+48*sc;ent=struct.unpack_from('<IHHIIIIIIHH',e,entoff)
  q0,q1,q2,q3=offs[4*sc:4*sc+4];assert q0<q1<=q2<q3<o
  n=(q1-q0)//4;assert n*4==q1-q0
  nname=u32(b,q1);assert q1+4+4*nname<=q2 and not any(b[q1+4+4*nname:q2])
  jt=base+ent[6];nj=u32(e,jt);assert jt+4+4*nj<=end
  expected_shared=(m=='evctrl' and sc==1)
  assert nname==nj or (expected_shared and (nname,nj)==(160,158))
  pcs=[u32(e,jt+4+4*k) for k in range(nj)]
  start=base+ent[3];assert base<=start<end
  # Validate the already established byte-to-instruction binding as a prerequisite,
  # without claiming another independent acceptance of its population law.
  nonzero=[j for j in range(n) if b[q0+4*j:q0+4*j+4]!=b'\0'*4];length=max(nonzero)+1
  code=e[start:start+length];assert len(code)==length
  flags=[];pc=0
  while pc<length and (not expected_shared or sum(flags)<ent[4]):
   op=code[pc];assert 3<=op<=0x63
   size=1 if op<0x48 else 3;assert pc+size<=length
   flags.extend([1]+[0]*(size-1));pc+=size
  validated_length=pc
  assert flags==[b[q0+4*j+3] for j in range(validated_length)] and sum(flags)==ent[4]
  if expected_shared:assert length-validated_length==144 and sum(b[q0+4*j+3] for j in range(length))-ent[4]==48
  else:assert validated_length==length
  names=[cstr(b,heap+u32(b,q1+4+4*k)) for k in range(nname)]
  bindings.append(dict(module=m,scope=sc,entry_file_offset=entoff,entry_hex=e[entoff:entoff+48].hex(),base=base,section_end=end,directory=D,name_pool=namebase,jump_table=jt,q0=q0,q1=q1,q2=q2,q3=q3,q1_count=nname,jt_count=nj,code_start=start,code_bytes=length,validated_code_bytes=validated_length,shared_tail_exception=expected_shared))
  for k,name in enumerate(names):
   if name.startswith('@'):continue
   assert k<nj;pc=pcs[k];assert pc<validated_length and flags[pc]==1
   off=q0+4*pc;line,block,flag=struct.unpack_from('<HBB',b,off);assert block<len(blocks)
   candidates=[]
   for convention,index in [('one-based',line-1),('zero-based',line)]:
    candidates.append(dict(convention=convention,index=index,source=blocks[block][index] if 0<=index<len(blocks[block]) else None))
   occurrences=[dict(block=bi,index=j,source=x) for bi,bl in enumerate(blocks) for j,x in enumerate(bl) if re.search(r'\b'+re.escape(name)+r'\b',x['text'])]
   row=dict(module=m,scope=sc,name=name,jump_index=k,jump_pc=pc,jump_field_offset=jt+4+4*k,dbg_name_offset=heap+u32(b,q1+4+4*k),q0_offset=off,record_hex=b[off:off+4].hex(),line=line,block=block,flag=flag,candidates=candidates,occurrences=occurrences)
   rows.append(row)
   print(m,sc,name,'pc',pc,'line',line,'block',block,[(c['convention'],c['source']['text'] if c['source'] else None) for c in candidates],flush=True)
raw=dict(method='A actual admitted original files and retained OPUS source parser; no compiled script/native/guest/live execution',question='Do named original entry bindings distinguish source[lineNo-1] versus source[lineNo]?',reference=dict(parent=parent.as_posix(),parent_manifest_sha256=sha((parent/'manifest.json').read_bytes()),parser_sha256=sha(pb),consumer_path=consumer.as_posix(),consumer_sha256=sha(cb),layout_path=layout.as_posix(),layout_sha256=sha(lb),files=identities),tools=dict(python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes()),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),driver_sha256=sha(Path(__file__).read_bytes()),bindings=bindings,rows=rows,cleanup=dict(inputs_unchanged=all(sha(Path(x['path']).read_bytes())==x['sha256'] for x in identities),peer_consumer_unchanged=consumer.read_bytes()==cb,peer_layout_unchanged=layout.read_bytes()==lb,pc_off=True),limits='Named entries only. Lexical occurrence is not automatically declaration/attribution; preserve ambiguities. No universal coordinate safety, compiler writer identity/cause, normal game/source loading or SN1 X closure; evctrl shared tail is an explicit prerequisite exception.')
assert all(raw['cleanup'].values())
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('CAPTURE61',len(rows),'named bindings',flush=True)
