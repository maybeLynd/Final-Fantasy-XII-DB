"""Retained source-coordinate reduction and actual raw-record detector controls."""
import ast,collections,hashlib,json,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest()
raw=json.loads((W/'raw.json').read_text());ref=raw['reference'];producer=(R/'original-sbn-producer.py').read_bytes();assert sha(producer)==ref['producer_sha256']
tree=ast.parse(producer.decode());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['sbn_blocks','sbn_group_read']];selected=ast.unparse(ast.Module(body=nodes,type_ignores=[]))+'\n';assert len(nodes)==2 and selected.encode()==(R/'selected-sbn-functions.py').read_bytes() and sha(selected.encode())==ref['selected_parser_sha256']
g={'struct':struct};exec(compile(ast.Module(body=nodes,type_ignores=[]),'unchanged retained SBN functions','exec'),g)
assert sha((R/'driver-before-run.py').read_bytes())==raw['driver_sha256'] and sha((R/'consumer-before.md').read_bytes())==ref['consumer_sha256']
assert len(raw['reference']['files'])==8 and {i['module'] for i in ref['files']}=={'ctrl','btlctrl','evctrl','mapctrl'}
for i in ref['files']:
 data=(R/(i['module']+'.'+i['extension'])).read_bytes();assert sha(data)==i['sha256'] and len(data)==i['bytes']

def category(line,block,blocks):
 if block>=len(blocks):return 'block-outside-domain'
 L=blocks[block]['line_count']
 if line==0:return 'zero-line-convention-unresolved'
 if line>L:return 'outside-both-index-conventions'
 if line==L:return 'one-based-only-boundary'
 return 'inside-both-index-ranges'

def record_domain(data,blocks):
 assert len(data)==4
 line,block,flag=struct.unpack('<HBB',data);assert flag in [0,1]
 return dict(line=line,block=block,flag=flag,category=category(line,block,blocks))

observations=[];all_counts=collections.Counter();zero_details=[];unresolved=[]
assert len(raw['modules'])==4 and raw['modules']==json.loads((W/'in-progress-modules.json').read_text())
for m in raw['modules']:
 b=(R/(m['name']+'.dbg')).read_bytes();s=(R/(m['name']+'.sbn')).read_bytes();blocks=m['blocks'];assert len(blocks)==len(g['sbn_blocks'](s))
 for block,(o,e) in zip(blocks,g['sbn_blocks'](s)):
  L,bases,lines,p=g['sbn_group_read'](s,o);assert (o,e,L,bases,lines)==(block['entry'],block['end'],block['line_count'],block['group_bases'],block['line_offsets']) and p<=bases[0]
  texts=[]
  for a in lines:
   assert bases[0]<=a<e and (a==bases[0] or s[a-1]==0);texts.append(dict(offset=a,bytes=s[a:s.index(b'\0',a,e)].hex()))
  assert texts==block['text']
 o=struct.unpack_from('<I',b)[0];ns=struct.unpack_from('<I',b,o)[0];offs=struct.unpack_from('<%dI'%(4*ns+1),b,o+4);assert ns==m['scope_count']==len(m['scopes'])
 counts=collections.Counter()
 for scope in m['scopes']:
  k=scope['index'];q0,q1,q2,q3=offs[4*k:4*k+4];assert [scope[x] for x in ['q0','q1','q2','q3']]==[q0,q1,q2,q3] and len(scope['records'])==scope['record_count']==(q1-q0)//4>0
  sc=collections.Counter();zeros=[]
  for x in scope['records']:
   a=q0+4*x['index'];data=b[a:a+4];d=record_domain(data,blocks);assert d=={key:x[key] for key in ['line','block','flag','category']} and x['record_hex']==data.hex() and x['file_offset']==a
   sc[d['category']]+=1;counts[d['category']]+=1
   if d['line']==0:zeros.append(x)
   if d['category']=='outside-both-index-conventions':
    bl=blocks[d['block']];unresolved.append(dict(module=m['name'],scope=k,index=x['index'],flag=d['flag'],coordinate_line=d['line'],physical_line_count=bl['line_count'],block=d['block'],record_hex=data.hex(),file_offset=a,scope_records=len(scope['records']),last_indexed_source=bl['text'][-1],source_tail_hex=s[bl['line_offsets'][-1]:bl['end']].hex(),reason='One past physical source block under both candidate index conventions; internal to q0 scope, not trailing table padding'))
  assert dict(sc)==scope['counts']
  if zeros:
   assert all(x['record_hex']=='00000000' and x['flag']==0 for x in zeros)
   assert [x['index'] for x in zeros]==list(range(scope['record_count']-len(zeros),scope['record_count'])) and len(zeros)<=2
   zero_details.append(dict(module=m['name'],scope=k,count=len(zeros),role='Observed all-zero suffix with no instruction-start flag, compatible with published 0..2 end marks; no real instruction-start at line0 in this corpus'))
 assert dict(counts)==m['coordinate_counts'];all_counts.update(counts);observations.append(dict(module=m['name'],scope_count=ns,source_line_counts=[bl['line_count'] for bl in blocks],coordinate_counts=dict(counts)))
assert sum(m['scope_count'] for m in raw['modules'])==50 and len(unresolved)==6 and all(x['coordinate_line']==x['physical_line_count']+1 for x in unresolved)
assert [(x['module'],x['scope'],x['index'],x['flag']) for x in unresolved]==[('btlctrl',1,3978,1),('btlctrl',1,3979,0),('btlctrl',1,3980,0),('mapctrl',1,5201,1),('mapctrl',1,5202,0),('mapctrl',1,5203,0)]
assert all(x['index']+3<x['scope_records'] for x in unresolved)
controls=raw['controls'];assert len(controls)==5 and controls[0]['name']=='positive-original'
m=next(m for m in raw['modules'] if m['name']==controls[0]['module']);x=controls[0]['original_record'];blocks=m['blocks'];original=bytes.fromhex(x['record_hex']);assert record_domain(original,blocks)['category']=='inside-both-index-ranges'
L=blocks[x['block']]['line_count'];raw_controls=[]
for name,data,expected in [('positive-original',original,'inside-both-index-ranges'),('private-blockCount',struct.pack('<HBB',x['line'],len(blocks),x['flag']),'block-outside-domain'),('private-lineCount-plus1',struct.pack('<HBB',L+1,x['block'],x['flag']),'outside-both-index-conventions'),('private-zero-line',struct.pack('<HBB',0,x['block'],x['flag']),'zero-line-convention-unresolved'),('private-lineCount',struct.pack('<HBB',L,x['block'],x['flag']),'one-based-only-boundary')]:
 d=record_domain(data,blocks)
 if '--fault-clamp-missing-line' in sys.argv and d['category']=='outside-both-index-conventions':d['category']='inside-both-index-ranges'
 assert d['category']==expected, 'Missing-coordinate control must not clamp to a valid source line'
 raw_controls.append(dict(name=name,bytes=data.hex(),decoded=d,expected=expected,method='Actual struct.unpack raw4B record path, private changed record only, no compiler/game execution'))
result=dict(method=raw['method'],reference=ref,raw_sha256=sha((W/'raw.json').read_bytes()),modules=observations,coordinate_counts=dict(all_counts),unresolved_physical_coordinates=unresolved,zero_suffixes=zero_details,raw_record_controls=raw_controls,
 interpretation='Two source block2 EOF+1 coordinate groups are inside q0 scope1 and include a start flag1, followed by two flag0 records. Btl source558 lines is addressed as559; map source557 lines as558. These six records cannot be blindly dereferenced into indexed physical SBN text under either 0/1-based convention. Nine lineCount coordinates are valid only in 1-based candidate; bounds do not independently certify compiler convention. All61 line0 records are observed all-zero suffixes of0..2 records and no start flags in this corpus.',
 required_change='Qualified source mapper returns unresolved/missing physical line for EOF+1 rather than clamp/index-past-end; canonical q0 prose records these internal instruction-start exceptions. Preserve physical layouts/source relation/q2-q3 evidence; unknown generated/virtual/stale/source-omission cause and source convention remain explicit. Owners add raw record domain controls to actual consumer/helper, not just a footnote.',
 control_limit='Initial capture controls perturb parsed coordinate fields; their record_hex is original context, not encoded mutant bytes. No raw-byte mutation proof attributed to those dictionaries. Default retained checker adds actual4B encode/decode controls through record_domain and keeps original raw/driver intact; these raw controls supersede any stronger interpretation of the coordinate-only receipt.',
 limits=raw['limits'],cleanup=raw['cleanup'])
out=W/'result.json'
if out.exists():assert json.loads(out.read_text())==result
else:out.write_text(json.dumps(result,indent=2)+'\n')
if (W/'manifest.json').exists():
 for m in json.loads((W/'manifest.json').read_text())['members']:
  data=(W/m['path']).read_bytes();assert len(data)==m['bytes'] and sha(data)==m['sha256']
print('PASS60 retained8 inputs/source parser/50 coordinate maps;6 internal EOF+1 records,61 all-zero suffixes; actual raw4B positive/block/line controls, no compiler/native/game execution',flush=True)
