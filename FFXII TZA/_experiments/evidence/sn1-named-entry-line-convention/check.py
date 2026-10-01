"""Read-only reducer; controls interpret private bytes, execute no FF12 code."""
import hashlib,json,re,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
raw=json.loads((W/'raw.json').read_text());g={'struct':struct};pb=(R/'selected-sbn-functions.py').read_bytes();assert sha(pb)==raw['reference']['parser_sha256'];exec(compile(pb,'retained OPUS source parser','exec'),g)
for f in raw['reference']['files']:
 data=(R/(f['module']+'.'+f['extension'])).read_bytes();assert len(data)==f['bytes'] and sha(data)==f['sha256']
def blocks(s):
 out=[]
 for o,end in g['sbn_blocks'](s):
  L,bases,starts,t=g['sbn_group_read'](s,o);assert len(starts)==L
  out.append([dict(offset=a,hex=s[a:s.index(b'\0',a,end)].hex(),text=s[a:s.index(b'\0',a,end)].decode('cp932')) for a in starts])
 return out
for bind in raw['bindings']:
 m=bind['module'];e=(R/(m+'.ebp')).read_bytes();b=(R/(m+'.dbg')).read_bytes()
 assert e[:4]==b'EBP2' and u32(e,0x10)==bind['base'] and u32(e,bind['base'])==0x8000000B
 assert e[bind['entry_file_offset']:bind['entry_file_offset']+48].hex()==bind['entry_hex']
 ent=struct.unpack_from('<IHHIIIIIIHH',bytes.fromhex(bind['entry_hex']));assert not any(bytes.fromhex(bind['entry_hex'])[36:])
 assert bind['base']+ent[3]==bind['code_start'] and bind['base']+ent[6]==bind['jump_table']
 limit=bind['code_bytes'] if '--fault-ignore-shared-tail' in sys.argv else bind['validated_code_bytes']
 pc=0;flags=[]
 while pc<limit:
  op=e[bind['code_start']+pc];assert 3<=op<=0x63;size=1 if op<0x48 else 3;flags.extend([1]+[0]*(size-1));pc+=size
 assert pc==limit and flags==[b[bind['q0']+4*j+3] for j in range(limit)],'Directory-bound bytecode binding; shared tail cannot be decoded as contiguous original body'
 assert sum(flags)==ent[4]
 if bind['shared_tail_exception']:
  assert (m,bind['scope'],bind['q1_count'],bind['jt_count'])==('evctrl',1,160,158)
  assert bind['code_bytes']-limit==144 and sum(b[bind['q0']+4*j+3] for j in range(bind['code_bytes']))-ent[4]==48
 else:assert limit==bind['code_bytes'] and bind['q1_count']==bind['jt_count']
observed=[]
for row in raw['rows']:
 m=row['module'];b=(R/(m+'.dbg')).read_bytes();e=(R/(m+'.ebp')).read_bytes();s=(R/(m+'.sbn')).read_bytes();bl=blocks(s)
 assert b[row['q0_offset']:row['q0_offset']+4].hex()==row['record_hex']
 assert u32(e,row['jump_field_offset'])==row['jump_pc']
 o=row['dbg_name_offset'];assert b[o-1]==0 and b[o:b.index(b'\0',o)].decode('cp932')==row['name']
 assert struct.unpack('<HBB',bytes.fromhex(row['record_hex']))==(row['line'],row['block'],1)
 for c in row['candidates']:
  index=row['line']-1 if c['convention']=='one-based' else row['line'];assert index==c['index'] and c['source']==(bl[row['block']][index] if 0<=index<len(bl[row['block']]) else None)
 occurrences=[dict(block=bi,index=j,source=x) for bi,bl0 in enumerate(bl) for j,x in enumerate(bl0) if re.search(r'\b'+re.escape(row['name'])+r'\b',x['text'])]
 assert occurrences==row['occurrences']
 labels=[x for x in occurrences if re.fullmatch(r'\s*'+re.escape(row['name'])+r'\s*:\s*',x['source']['text'])]
 assert len(labels)==1
 exceptional=(m,row['scope'])==('evctrl',1)
 observed.append(dict(module=m,name=row['name'],scope=row['scope'],pc=row['jump_pc'],label=labels[0],coordinate_line=row['line'],coordinate_block=row['block'],coordinate_selects_label_under_either_scheme=any(c['source'] and c['source']==labels[0]['source'] for c in row['candidates']),binding_status='UNACCEPTED_SHARED_TAIL_Q1_COUNT_MISMATCH' if exceptional else 'DIRECTORY_AND_Q1_BOUND',attribution='Entry does not itself locate the label declaration; source statement/bytecode discriminator required'))
assert len(observed)==16 and sum(x['binding_status'].startswith('UNACCEPTED') for x in observed)==2
assert not any(x['coordinate_selects_label_under_either_scheme'] for x in observed)
specs=[('btlctrl',531,2,4,0,0x0D,'assignment'),('btlctrl',537,2,5,1,0x0E,'assignment'),('mapctrl',729,0,388,2,0x52,'dvar'),('mapctrl',736,0,389,3,0x20,'dvar')]
def anchor(b,e,s,bind,pc,kind,zero=False):
 off=bind['q0']+4*pc;line,block,flag=struct.unpack_from('<HBB',b,off);assert flag==1
 n=6 if kind=='assignment' else 7;code=e[bind['code_start']+pc:bind['code_start']+pc+n]
 assert code[0]==0x4F and code[3]==(0x49 if kind=='assignment' else 0x4A)
 if kind=='dvar':assert code[6]==0x46
 value=struct.unpack_from('<H',code,1)[0];target=struct.unpack_from('<H',code,4)[0]
 bl=blocks(s);index=line if zero else line-1;src=bl[block][index] if 0<=index<len(bl[block]) else None
 match=None if src is None else re.fullmatch(r'\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\d+)\s*;\s*(?://.*)?',src['text']) if kind=='assignment' else re.fullmatch(r'\s*dvar\s*\(\s*(\d+)\s*,\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*;\s*(?://.*)?',src['text'])
 source_value=int(match.group(2 if kind=='assignment' else 1)) if match else None
 return dict(line=line,block=block,index=index,record_hex=b[off:off+4].hex(),bytecode_hex=code.hex(),value=value,target_operand=target,source=src,source_literal=source_value,literal_and_operation_match=source_value==value,variable_identity='Source spelling retained; descriptor operand is physical only, name equivalence not newly proved')
anchors=[];controls=[]
for m,pc,block,line,value,target,kind in specs:
 b=(R/(m+'.dbg')).read_bytes();e=(R/(m+'.ebp')).read_bytes();s=(R/(m+'.sbn')).read_bytes();bind=next(x for x in raw['bindings'] if x['module']==m and x['scope']==1)
 a=anchor(b,e,s,bind,pc,kind,zero='--fault-zero-based-mapping' in sys.argv);z=anchor(b,e,s,bind,pc,kind,zero=True)
 assert (a['block'],a['line'],a['value'],a['target_operand'])==(block,line,value,target)
 assert a['literal_and_operation_match'] and not z['literal_and_operation_match'],('Source literal/operation mapping discriminator',m,pc,a,z)
 # Original matching bytes positive; actual encoded line shift and immediate mutation
 # separately challenge the mapping. Neither is executed or admitted as original data.
 bb=bytearray(b);struct.pack_into('<H',bb,bind['q0']+4*pc,line+1)
 shifted=anchor(bytes(bb),e,s,bind,pc,kind)
 ee=bytearray(e);struct.pack_into('<H',ee,bind['code_start']+pc+1,value+1)
 altered=anchor(b,bytes(ee),s,bind,pc,kind)
 assert not shifted['literal_and_operation_match'] and not altered['literal_and_operation_match']
 anchors.append(dict(module=m,scope=1,pc=pc,kind=kind,one_based=a,zero_based=z))
 controls.append(dict(module=m,pc=pc,positive=a['literal_and_operation_match'],private_line_shift=shifted,private_immediate_change=altered,observation='Static interpretation of private data bytes only; no VM/original-code/live execution'))
result=dict(status='BOUNDED_ONE_BASED_SOURCE_STATEMENTS_SUPPORTED',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),named_entries=observed,anchors=anchors,controls=controls,invalid_first_attempt=dict(stage='BYTECODE_BINDING_PRECONDITION',cause='Known evctrl scope1 shared/dedup tail was incorrectly required to decode contiguously past directory instruction bound; first mismatch6130. No raw/result completed by that attempt.',corrected_default='Directory-bounded2084 instructions/6130 bytes checked, debug144-byte/48-mark tail recorded but not decoded as this body. Both named entries in exceptional q1=160/jt=158 scope left UNACCEPTED. Old driver and diagnostic retained.'),interpretation='Four exact original assignment/debug-call statements match source[lineNo-1]; source[lineNo] mismatches operation/literal or blank. Refutes unqualified historical zero-based mapping for these original statements and supports one-based lookup for them. Named label declaration heuristic alone failed; fourteen otherwise bound named entries do not select declaration under either convention. Source coordinate attribution need not equal label declaration. Two evctrl named bindings not accepted by this package.',limits='No universal writer/reader convention proof, malformed safety, opcode execution/native effects, source variable-to-descriptor identity, compiler cause for60 EOF+1, original shared-tail reconstruction or SN1 X closure. Read-only extracted files, no new whole-VBF provenance audit. Independent acceptance and canonical propagation pending; PC OFF/S19 parked/full L1+L2 NOT_MET.')
p=W/'result.json';encoded=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==encoded,'published result differs'
else:p.write_bytes(encoded)
print('PASS61 named-entry shortcut insufficient; four discriminating original literal/operation anchors support one-based mapping; shared-tail bindings unaccepted',flush=True)
