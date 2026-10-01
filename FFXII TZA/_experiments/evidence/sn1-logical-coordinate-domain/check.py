"""Conditional source-domain reduction; no compiler/VM/native/game execution."""
import collections,hashlib,json,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;prep=json.loads((W/'preparation.json').read_text());P=Path(prep['parent']);sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((P/'manifest.json').read_bytes())==prep['parent_manifest_sha256'] and sha((P/'raw.json').read_bytes())==prep['parent_raw_sha256']
raw=json.loads((P/'raw.json').read_text());g={'struct':struct};pb=(P/'retained/selected-sbn-functions.py').read_bytes();assert sha(pb)==raw['reference']['selected_parser_sha256'];exec(compile(pb,'unchanged retained OPUS parser','exec'),g)
def domain(record,blocks,physical=False):
 line,block,flag=struct.unpack('<HBB',record);assert flag in [0,1]
 if record==b'\0'*4:return 'OBSERVED_PAD_NOT_SOURCE'
 if block>=len(blocks):return 'UNRESOLVED_BLOCK'
 L=blocks[block]['physical' if physical else 'logical']
 return 'CONDITIONAL_LOGICAL_IN_RANGE' if 1<=line<=L else 'UNRESOLVED_LOGICAL_COORDINATE'
source_blocks=[];totals=collections.Counter();missing=[];controls=[];in_group=[];encoding_controls=[]
for m in raw['modules']:
 b=(P/'retained'/(m['name']+'.dbg')).read_bytes();s=(P/'retained'/(m['name']+'.sbn')).read_bytes()
 for ext,data in [('dbg',b),('sbn',s)]:assert sha(data)==next(i['sha256'] for i in raw['reference']['files'] if (i['module'],i['extension'])==(m['name'],ext))
 blocks=[]
 for bi,(o,end) in enumerate(g['sbn_blocks'](s)):
  L,bases,starts,p=g['sbn_group_read'](s,o);groups=[];current=[];continuations=0
  for j,a in enumerate(starts):
   data=s[a:s.index(b'\0',a,end)];decoded=data.decode('cp932');raw_end=data.endswith(b'\\');cont=raw_end if '--fault-raw-byte-fold' in sys.argv else decoded.endswith('\\')
   assert not (raw_end and not decoded.endswith('\\')) or not cont, 'CP932 trailing5C character must not be classified as ASCII continuation'
   if raw_end and not decoded.endswith('\\'):
    assert data[-2:]==bytes.fromhex('945c') and decoded[-1]=='能'
    encoding_controls.append(dict(module=m['name'],block=bi,physical_line=j+1,offset=a,bytes=data.hex(),decoded=decoded,terminal_character=decoded[-1],terminal_character_bytes=data[-2:].hex(),raw_byte_predicate=True,decoded_ascii_predicate=cont,role='Actual original negative control for byte5C versus ASCII continuation; both map source lines'))
   current.append(dict(physical_index=j,offset=a,bytes=data.hex()));continuations+=int(cont)
   if not cont:groups.append(current);current=[]
  assert not current,'Terminal continuation outside this observed closed-group domain'
  block=dict(module=m['name'],block=bi,physical=L,logical=len(groups),continuations=continuations,groups=groups)
  assert len(groups)==L-continuations;blocks.append(block);source_blocks.append({k:v for k,v in block.items() if k!='groups'})
  if any(len(group)>1 for group in groups):
   group_index=next(j for j,group in enumerate(groups) if len(group)>1);encoded=struct.pack('<HBB',group_index+1,bi,1)
   assert domain(encoded,blocks)=='CONDITIONAL_LOGICAL_IN_RANGE'
   detected=False if '--fault-ignore-multiphysical-group' in sys.argv else len(blocks[bi]['groups'][group_index])>1
   assert detected,'Actual source multi-physical group must be detected by private valid coordinate control'
   controls.append(dict(module=m['name'],block=bi,kind='private-original-source-multiphysical-group',bytes=encoded.hex(),line=group_index+1,physical_span=groups[group_index],detected=True,limits='Private record addresses an actual multi-line source group; not an emitted original compiler coordinate'))
 actual_positive=None
 for sc in m['scopes']:
  for x in sc['records']:
   data=b[x['file_offset']:x['file_offset']+4];assert data.hex()==x['record_hex'];d=domain(data,blocks);totals[d]+=1
   if d=='CONDITIONAL_LOGICAL_IN_RANGE':
    if actual_positive is None and x['flag']==1:actual_positive=dict(scope=sc['index'],record=x,data=data.hex())
    if len(blocks[x['block']]['groups'][x['line']-1])>1:in_group.append(dict(module=m['name'],scope=sc['index'],index=x['index'],record_hex=data.hex(),line=x['line'],block=x['block'],flag=x['flag'],physical_span=blocks[x['block']]['groups'][x['line']-1]))
   elif d!='OBSERVED_PAD_NOT_SOURCE':missing.append(dict(module=m['name'],scope=sc['index'],index=x['index'],offset=x['file_offset'],record_hex=data.hex(),line=x['line'],block=x['block'],flag=x['flag'],logical_count=blocks[x['block']]['logical'] if x['block']<len(blocks) else None,old_physical_category=x['category']))
 assert actual_positive is not None and domain(bytes.fromhex(actual_positive['data']),blocks)=='CONDITIONAL_LOGICAL_IN_RANGE'
 controls.append(dict(module=m['name'],kind='positive-original-start-record',**actual_positive))
 for bi,block in enumerate(blocks):
  if block['continuations']==0:continue
  good=struct.pack('<HBB',block['logical'],bi,1);bad=struct.pack('<HBB',block['logical']+1,bi,1)
  assert domain(good,blocks)=='CONDITIONAL_LOGICAL_IN_RANGE'
  assert domain(bad,blocks,physical='--fault-physical-guard' in sys.argv)=='UNRESOLVED_LOGICAL_COORDINATE','LogicalL+1 within physicalL must be rejected by actual conditional domain guard'
  assert domain(bad,blocks,physical=True)=='CONDITIONAL_LOGICAL_IN_RANGE'
  controls.append(dict(module=m['name'],block=bi,kind='private-encoded-logical-boundary',positive_bytes=good.hex(),negative_bytes=bad.hex(),positive_line=block['logical'],negative_line=block['logical']+1,physicalL=block['physical'],logicalL=block['logical'],legacy_physical_false_accept=True,limits='Actual4B interpreted private records, not emitted original compiler values or malformed native execution proof'))
new=[x for x in missing if x['old_physical_category']!='outside-both-index-conventions']
assert not new and missing==prep['known_physical_missing'] and totals['OBSERVED_PAD_NOT_SOURCE']==59
counter_mode=prep.get('counter_mode','RAW_TERMINAL5C_CANDIDATE')
if '--fault-old-preparation-mode' in sys.argv:counter_mode='DECODED_ASCII_CONTINUATION'
assert counter_mode in ['RAW_TERMINAL5C_CANDIDATE','DECODED_ASCII_CONTINUATION']
assert [(x['module'],x['block'],x['physical'],x['logical']) for x in source_blocks]==[(x['module'],x['block'],x['physical'],x['logical']+(len(x['non_ascii_terminal5c']) if counter_mode=='RAW_TERMINAL5C_CANDIDATE' else 0)) for x in prep['source_blocks']], 'Decoded logical domain corrects raw terminal-byte candidate'
assert len([c for c in controls if c['kind']=='private-encoded-logical-boundary'])==2 and len([c for c in controls if c['kind']=='positive-original-start-record'])==4
assert [(x['module'],x['block'],x['physical_line']) for x in encoding_controls]==[('mapctrl',0,977),('mapctrl',0,1187)]
assert b'\\'.decode('cp932').endswith('\\') and not bytes.fromhex('945c').decode('cp932').endswith('\\')
result=dict(status='CONDITIONAL_LOGICAL_DOMAIN_NO_ADDITIONAL_MISSING_ORIGINAL_RECORDS',method='A original60 physical bytes and conditional63 terminal ASCII-backslash folding, no compiler/VM/native/game',parent_manifest_sha256=prep['parent_manifest_sha256'],parent_raw_sha256=prep['parent_raw_sha256'],preparation_sha256=sha((W/'preparation.json').read_bytes()),source_blocks=source_blocks,counts=dict(totals),missing=missing,new_logical_missing=new,controls=controls,source_encoding_controls=encoding_controls,stored_coordinates_in_multiphysical_groups=in_group,interpretation='Decoded CP932 ASCII-backslash folding, not raw terminal5C folding: mapctrl block0 has two terminal能 characters encoded945C and zero actual terminal ASCII backslashes. All actual non-pad original records remain within the conditional one-based logical domain except the six known block2 EOF+1 records, whose blocks have no continuation. Two encoded logicalL+1 controls prove physicalL guard would falsely accept in continued blocks. Negative original absence accepted only within this conditional carrier after positive/detection controls, not universal compiler/malformed safety. Logical groups may span several physical source records by construction; no original non-pad coordinate names a multi-physical group in these inputs. This is not a proof that native compiler never emits such a coordinate.',limits='No universal original compiler/writer rule, single-statement attribution, native callback/live loading or SN1 X/cause closure. Raw terminal5C is not sufficient: two mapctrl source lines end in CP932 multibyte characters; corrected decoded-ASCII candidate used. evctrl544 and ctrl19 terminal ASCII backslashes remain; general lexical/compiler/comments/quotes behavior not proved. No terminal-open group in actual inputs. Counts are range observations, not experiments/semantic acceptance. Peer consumer implementation not edited; independent review/propagation pending. PC OFF/S19 unchanged/fullL1+L2 NOT_MET.')
p=W/'result.json';encoded=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==encoded
else:p.write_bytes(encoded)
print('PASS64 conditional logical domain: no additional missing original records; six retained; four original positive and two encoded boundary controls; native/compiler rule not proved',flush=True)
