import csv,hashlib,io,json,re,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';raw=json.loads((W/'raw.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
files={}
for x in raw['reference_files']:
 data=(R/('evctrl.'+x['extension'])).read_bytes();assert sha(data)==x['sha256'] and len(data)==x['bytes'];files[x['extension']]=data
pb=(R/'selected-sbn-functions.py').read_bytes();assert sha(pb)==raw['parser_sha256'];g={'struct':struct};exec(compile(pb,'unchanged retained OPUS SBN parser','exec'),g)
cat=(R/'verb-table.tsv').read_bytes();assert sha(cat)==raw['catalog_sha256'];rows=list(csv.DictReader(io.StringIO(cat.decode()),delimiter='\t'));assert [x for x in rows if x['call_id'] in ['0013','001A']]==raw['admitted_catalog_rows']
b,s,e=files['dbg'],files['sbn'],files['ebp'];bind=raw['bind'];assert bind['validated_code_bytes']==6130 and bind['q1_count']==160 and bind['jt_count']==158
def source(data):
 o,end=g['sbn_blocks'](data)[0];L,bases,starts,t=g['sbn_group_read'](data,o);out=[];logical=1;maps={}
 for j,a in enumerate(starts):
  z=data.index(b'\0',a,end);text=data[a:z];row=dict(physical_index=j,physical_line=j+1,offset=a,bytes=text.hex(),text=text.decode('cp932'),logical_line=logical,continues=text.endswith(b'\\'));out.append(row);maps.setdefault(logical,[]).append(row)
  if not row['continues']:logical+=1
 assert len(out)==L;return out,maps
lines,maps=source(s);continues=[x for x in lines if x['continues']];assert len([x for x in continues if x['physical_line']<961])==544
mut=bytearray(s);first=continues[0];last=first['offset']+len(bytes.fromhex(first['bytes']))-1;assert mut[last]==92;mut[last]=32;mlines,mmaps=source(bytes(mut))
def observe(case,code,source_lines,logical_map,physical=False):
 pc=case['pc'];line,block,flag=struct.unpack_from('<HBB',b,bind['q0']+4*pc);assert (line,block,flag)==(case['logical_line'],0,1)
 n=12 if case['verb']=='askpos' else 9;chunk=code[bind['code_start']+pc:bind['code_start']+pc+n];ops=[]
 for k in range(0,n,3):
  op=chunk[k];v=struct.unpack_from('<H',chunk,k+1)[0];ops.append((op,v));assert b[bind['q0']+4*(pc+k)+3]==1
 assert ops[0]==(0x4F,6) and ops[-2]==(0x4F,0) and ops[-1][0]==0x5D, 'Original source-call entry/variant precondition'
 if n==12:assert ops[1][0]==0x48
 src=[source_lines[line-1]] if physical else logical_map.get(line,[])
 assert len(src)==1
 text=src[0]['text'];pattern=r'\s*askpos\s*\(\s*6\s*,\s*[A-Za-z_][A-Za-z0-9_]*\s*,\s*0\s*\)\s*;\s*' if n==12 else r'\s*mesopenspeed\s*\(\s*6\s*,\s*0\s*\)\s*;\s*'
 return dict(pc=pc,record_hex=b[bind['q0']+4*pc:bind['q0']+4*pc+4].hex(),coordinate_line=line,physical_lookup=physical,source=src[0],bytecode_hex=chunk.hex(),ops=ops,match=bool(re.fullmatch(pattern,text)) and ops[-1][1]==case['call_id'],limits='Admitted call ID/name premise; literal order matched, physical PUSHV operand not newly equated to variable spelling. No opcode/native execution.')
observations=[];controls=[]
spec=json.loads((W/'corrected-spec.json').read_text());assert spec['original_raw_sha256']==sha((W/'raw.json').read_bytes())
for case in (raw['cases'] if '--fault-old-call-start' in sys.argv else spec['cases']):
 positive=observe(case,e,lines,maps,physical='--fault-physical-map' in sys.argv)
 assert positive['match'] and positive['source']['physical_line']==case['physical_one_based_line'],'Original call must match continued logical source, not direct physical index'
 negative=observe(case,e,lines,maps,physical=True);assert not negative['match']
 mutant=observe(case,e,lines,maps) if '--fault-ignore-splice-control' in sys.argv else observe(case,e,mlines,mmaps)
 assert not mutant['match'],'Removing one actual continuation must reject the source mapping'
 ee=bytearray(e);end=bind['code_start']+case['pc']+(12 if case['verb']=='askpos' else 9);struct.pack_into('<H',ee,end-2,0x1A if case['call_id']==0x13 else 0x13)
 call_mut=observe(case,bytes(ee),lines,maps);assert not call_mut['match']
 observations.append(positive);controls.append(dict(pc=case['pc'],original_positive=True,physical_negative=negative,source_private_one_backslash_removed=mutant,code_private_call_id_swapped=call_mut,source_mutation_offset=last,source_mutation_before=92,source_mutation_after=32,intervention='Private static data interpretations only, no original VM/code/game execution'))
for row in raw['named_candidates']:
 assert struct.unpack_from('<I',e,row['jump_field_offset'])[0]==row['jump_pc']
 assert row['jump_pc'] in [16,3230] and b[row['q0_offset']:row['q0_offset']+4].hex()==row['record_hex']
assignment_pc=16;assignment=e[bind['code_start']+16:bind['code_start']+22];assert assignment.hex()=='4f0000496100'
assignment_coord=struct.unpack_from('<HBB',b,bind['q0']+4*16);assert assignment_coord==(417,0,1)
assignment_source=maps[416];assert len(assignment_source)==1 and re.fullmatch(r'\s*test_load_flg\s*=\s*0\s*',assignment_source[0]['text'])
result=dict(status='BOUNDED_LOGICAL_SOURCE_SPLICE_CANDIDATE_SUPPORTED',call_variant='Original0x5D CALLPOPA, admitted interpreter same-current-actor dispatcher premise; no native effects execution',raw_sha256=sha((W/'raw.json').read_bytes()),method=raw['method'],observations=observations,controls=controls,continuations_before_targets=544,assignment_before_call=dict(pc=16,bytecode_hex=assignment.hex(),tagged_coordinate_line=417,source_literal_assignment=assignment_source[0],source_logical_line=416,physical_target_operand=0x61,limit='Literal0/operation compatible, descriptor name identity not newly proved; assignment and subsequent call share coordinate417, not a singular statement-line proof'),interpretation='Direct physical line lookup fails four actual original call statements. Backslash-folded one-based logical source coordinates match CALLPOPA IDs0013 askpos(6,var,0) and001A mesopenspeed(6,0) twice. Same-index MENU_TOP q1[0]/jt[0]=16 starts assignment0 followed by call22, and summon q1[76]/jt[76]=3230 starts call; source statements are coherent under that carrier despite table count mismatch. Initial negative proximity result cannot justify mismatched artifacts or a reordered table. MENU_TOP initial assignment and call share coordinate417, while compatible source assignment is logical416: attribution granularity is not automatically one statement/physical line. Count mismatch, general binding and original compiler rule remain unresolved.',limits=raw['limits'],cleanup='Retained inputs unchanged/hash checked. Private copies only; original source/code/parent evidence/peer catalog not modified. PC OFF.')
encoded=(json.dumps(result,indent=2)+'\n').encode();p=W/'result.json'
if p.exists():assert p.read_bytes()==encoded
else:p.write_bytes(encoded)
print('PASS63 four original calls match logical continuation carrier; direct physical lookup/source-splice/call-ID controls reject; table mismatch/cause/global rule unresolved',flush=True)
