"""A coordinate-domain analysis, not compiler reconstruction or game execution."""
import ast,collections,datetime,hashlib,json,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
if (W/'raw.json').exists():
 import subprocess
 subprocess.run([sys.executable,str(W/'check.py')],check=True)
 sys.exit(0) # Immutable retained capture: default consumes corrected reducer, no recapture.
sys.path.insert(0,'Database/Tools/analysis-kit/gfz-scripts');import team
ok,d=team.board_status(team.BOARD);assert ok,d;t=next(t for t in json.loads(team.BOARD.read_text())['tasks'] if t['id']=='ASTRA-SN1-Q0-SOURCE-COORDINATE-DOMAIN');assert t['status']=='ACTIVE' and t['agent']=='ASTRA'
assert not (W/'raw.json').exists();R.mkdir(exist_ok=False)
producer=Path('Database/FFXII TZA/_index/candidates/sn1-layouts/sn1_layouts.py');pb=producer.read_bytes();tree=ast.parse(pb.decode());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['sbn_blocks','sbn_group_read']];assert len(nodes)==2
module=ast.Module(body=nodes,type_ignores=[]);selected=ast.unparse(module)+'\n';g={'struct':struct};exec(compile(module,'unchanged OPUS SBN functions','exec'),g)
(R/'original-sbn-producer.py').write_bytes(pb);(R/'selected-sbn-functions.py').write_bytes(selected.encode());(R/'driver-before-run.py').write_bytes(Path(__file__).read_bytes())
consumer=Path('Database/FFXII TZA/01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md');cb=consumer.read_bytes();(R/'consumer-before.md').write_bytes(cb)
root=Path('D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin');identities=[];modules=[]
def category(line,block,blocks):
 if block>=len(blocks):return 'block-outside-domain'
 L=blocks[block]['line_count']
 if line==0:return 'zero-line-convention-unresolved'
 if line>L:return 'outside-both-index-conventions'
 if line==L:return 'one-based-only-boundary'
 return 'inside-both-index-ranges'

for name in ['ctrl','btlctrl','evctrl','mapctrl']:
 files={}
 for ext in ['dbg','sbn']:
  p=root/(name+'.'+ext);data=p.read_bytes();files[ext]=data;(R/p.name).write_bytes(data);identities.append(dict(module=name,extension=ext,path=str(p),bytes=len(data),sha256=sha(data),provenance='Existing admitted extraction path used by FABLE/OPUS; exact local bytes pinned, no fresh whole-VBF provenance audit'))
 b=files['dbg'];s=files['sbn'];blocks=[]
 for block,(o,e) in enumerate(g['sbn_blocks'](s)):
  L,bases,lines,p=g['sbn_group_read'](s,o);assert L==len(lines)>0 and len(lines)==len(set(lines)) and lines==sorted(lines) and p<=bases[0]<=e
  text=[]
  for a in lines:
   assert bases[0]<=a<e and (a==bases[0] or s[a-1]==0);end=s.index(b'\0',a,e);text.append(dict(offset=a,bytes=s[a:end].hex()))
  blocks.append(dict(index=block,entry=o,end=e,line_count=L,group_bases=bases,line_offsets=lines,text=text))
 o=struct.unpack_from('<I',b)[0];ns=struct.unpack_from('<I',b,o)[0];offs=struct.unpack_from('<%dI'%(4*ns+1),b,o+4);assert ns>0 and ns<100 and o+4+4*(4*ns+1)<=len(b)
 scope=[];totals=collections.Counter();examples={}
 for k in range(ns):
  q0,q1,q2,q3=offs[k*4:k*4+4];assert 0<=q0<q1<=q2<q3<o and (q1-q0)%4==0
  records=[];counts=collections.Counter()
  for j in range((q1-q0)//4):
   line,block,flag=struct.unpack_from('<HBB',b,q0+4*j);assert flag in [0,1]
   cat=category(line,block,blocks);item=dict(index=j,file_offset=q0+4*j,record_hex=b[q0+4*j:q0+4*j+4].hex(),line=line,block=block,flag=flag,category=cat);records.append(item);counts[cat]+=1;totals[cat]+=1
   key=(cat,flag)
   if key not in examples:examples[key]=dict(scope=k,**item)
  scope.append(dict(index=k,q0=q0,q1=q1,q2=q2,q3=q3,record_count=len(records),counts=dict(counts),records=records))
 modules.append(dict(name=name,blocks=blocks,scope_count=ns,scopes=scope,coordinate_counts=dict(totals),examples=[dict(example_kind=f'{cat}/flag{flag}',**x) for (cat,flag),x in sorted(examples.items())]))
 (W/'in-progress-modules.json').write_text(json.dumps(modules,indent=2)+'\n')
positive=next((m,x) for m in modules for sc in m['scopes'] for x in sc['records'] if x['flag']==1 and x['category']=='inside-both-index-ranges');m,x=positive;blocks=m['blocks'];L=blocks[x['block']]['line_count']
controls=[]
for label,record in [('positive-original',x),('private-blockCount',dict(x,block=len(blocks))),('private-lineCount-plus1',dict(x,line=L+1)),('private-zero-line',dict(x,line=0)),('private-lineCount',dict(x,line=L))]:
 encoded=struct.pack('<HBB',record['line'],record['block'],record['flag']);line,block,flag=struct.unpack('<HBB',encoded);record=dict(record,line=line,block=block,flag=flag,record_hex=encoded.hex());c=category(line,block,blocks);controls.append(dict(name=label,module=m['name'],original_record=x,controlled_record=record,category=c,intervention=label!='positive-original'))
 if label=='positive-original':controls[-1]['resolved_candidates']=dict(one_based=blocks[x['block']]['text'][x['line']-1],zero_based=blocks[x['block']]['text'][x['line']])
raw=dict(method='A actual admitted DBG/SBN bytes and unchanged published OPUS SBN parser definitions; no original/native/emulator/live/compiled script execution',question='Can q0 coordinates be safely dereferenced as physical paired SBN block/line positions?',reference=dict(producer_path=producer.as_posix(),producer_sha256=sha(pb),selected_parser_sha256=sha(selected.encode()),consumer_path=consumer.as_posix(),consumer_sha256=sha(cb),files=identities),driver_sha256=sha(Path(__file__).read_bytes()),tools=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,interpreter=sys.executable,interpreter_sha256=sha(Path(sys.executable).read_bytes())),modules=modules,controls=controls,cleanup=dict(inputs_unchanged=all(sha(Path(i['path']).read_bytes())==i['sha256'] for i in identities),peer_producer_unchanged=producer.read_bytes()==pb,pc_off=True),limits='Coordinate range/actual bytes only; index convention, compiler source relation and causes of any inconsistent or zero-line record cannot be inferred from bounds alone. No X formula/disposition, q2/q3/bytecode law recapture, normal runtime reader/game claim or fresh full VBF audit. Private controls mutate data records only; parents immutable/full L1+L2 NOT_MET/S19 parked')
(W/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
assert raw['cleanup']['inputs_unchanged'] and raw['cleanup']['peer_producer_unchanged']
assert [c['category'] for c in controls]==['inside-both-index-ranges','block-outside-domain','outside-both-index-conventions','zero-line-convention-unresolved','one-based-only-boundary']
print('CAPTURE60',[(m['name'],m['coordinate_counts']) for m in modules],flush=True)
