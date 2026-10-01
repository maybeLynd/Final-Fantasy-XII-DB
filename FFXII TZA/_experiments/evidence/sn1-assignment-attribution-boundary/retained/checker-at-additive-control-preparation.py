import hashlib,json,re,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u=lambda b,o:struct.unpack_from('<I',b,o)[0]
raw=json.loads((W/'raw.json').read_text());parent=json.loads((R/'parent61-raw.json').read_text());p65=json.loads((R/'parent65-result.json').read_text());assert p65['observations'][0]['observation']['name']=='test_load_flg' and p65['observations'][0]['observation']['descriptor']=='01000905'
for f in raw['reference']['files']:
 b=(W/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
b=(R/'evctrl.dbg').read_bytes();e=(R/'evctrl.ebp').read_bytes();s=(R/'evctrl.sbn').read_bytes();pb=(R/'selected-sbn-functions.py').read_bytes();assert sha(pb)==parent['reference']['parser_sha256'];g={'struct':struct};exec(compile(pb,'retained original SBN parser','exec'),g)
bo,be=g['sbn_blocks'](s)[0];L,bases,starts,te=g['sbn_group_read'](s,bo);lines=[dict(physical=i+1,offset=a,hex=s[a:s.index(b'\0',a,be)].hex(),text=s[a:s.index(b'\0',a,be)].decode('cp932')) for i,a in enumerate(starts)];groups=[];continuing=False
for line in lines:
 if not continuing:groups.append([])
 groups[-1].append(line);continuing=line['text'].rstrip('\r\n \t').endswith(chr(92))
assert len(lines)==2456 and len(groups)==1912 and not continuing
pool=u(b,8);T0=u(b,4);N=u(b,T0);sect=u(e,0x10);vt=sect+u(e,sect+0x28);assert N==u(e,vt)==115
def varname(index):
 assert 0<=index<N;a=pool+u(b,T0+4+4*index);assert b[a-1]==0;return b[a:b.index(b'\0',a)].decode('cp932')
assert varname(0x61)=='test_load_flg' and u(e,vt+4+8*0x61)==0x01000905
def assignment(group):
 text=' '.join(x['text'] for x in group);m=re.fullmatch(r'\s*(\w+)\s*=\s*(\d+)\s*;?\s*(?://.*)?',text);return dict(name=m[1],value=int(m[2])) if m else None
def inspect(c,ee,bb):
 a=c['code_offset'];code=ee[a:a+6];assert code[0]==0x4f and code[3]==0x49;value=struct.unpack_from('<H',code,1)[0];idx=struct.unpack_from('<H',code,4)[0];line,block,flag=struct.unpack_from('<HBB',bb,c['q0_offset']);assert block==0 and flag==1 and 2<=line<=len(groups)
 name=varname(idx);prev=groups[line-2];curr=groups[line-1];pa=assignment(prev);ca=assignment(curr)
 return dict(value=value,index=idx,name=name,line=line,preceding_group=prev,tagged_group=curr,preceding_assignment=pa,tagged_assignment=ca,preceding_matches=pa==dict(name=name,value=value),tagged_matches=ca==dict(name=name,value=value))
rows=[];controls=[]
for c in raw['cases']:
 a=c['code_offset'];qo=c['q0_offset'];assert e[a:a+6].hex()==c['code_hex'] and b[qo:qo+24].hex()==c['q0_hex']
 bind=next(x for x in parent['bindings'] if x['module']=='evctrl' and x['scope']==c['scope']);ent=struct.unpack_from('<IHHIIIIIIHH',e,bind['entry_file_offset']);assert bind['base']+ent[3]+c['push_pc']==a and c['pop_pc']+3<=bind['validated_code_bytes'];tags=[struct.unpack_from('<HBB',b,qo+4*i) for i in range(6)];assert [x[2] for x in tags]==[1,0,0,1,0,0] and all(x[:2]==(c['tagged_line'],0) for x in tags)
 o=inspect(c,e,b);assert (o['value'],o['index'],o['name'])==(c['value'],0x61,'test_load_flg');assert o['preceding_matches'] and not o['tagged_matches'],'Original full assignment identity versus tagged group'
 if '--fault-tagged-group-as-statement' in sys.argv:assert o['tagged_matches'],'Tagged group incorrectly required as statement attribution'
 # Exact literal equality does not identify a different destination variable.
 if c['value']==0 and c['scope']==1:
  assert o['tagged_assignment']==dict(name='test_event_count',value=0)
  if '--fault-literal-only-attribution' in sys.argv:assert o['tagged_matches']==(o['tagged_assignment']['value']==o['value']),'Literal-only matcher falsely identifies different destination'
 ee=bytearray(e);struct.pack_into('<H',ee,a+4,0x60);operand=inspect(c,bytes(ee),b);assert not operand['preceding_matches'],'Encoded variable operand control'
 ee=bytearray(e);struct.pack_into('<H',ee,a+1,c['value']+1);literal=inspect(c,bytes(ee),b);assert not literal['preceding_matches'],'Encoded literal control'
 bb=bytearray(b)
 for i in range(6):struct.pack_into('<H',bb,qo+4*i,c['tagged_line']-1)
 shifted=inspect(c,e,bytes(bb));assert shifted['tagged_matches'] and not shifted['preceding_matches'],'Encoded coordinate shift changes attribution discriminator'
 rows.append(dict(case=c,observation=o));controls.append(dict(scope=c['scope'],pc=c['pop_pc'],original_positive=True,private_operand=operand,private_literal=literal,private_coordinate=shifted,limits='Private copied data interpreted only; no original VM/compiler/live execution'))
assert len(rows)==4 and sum(x['observation']['tagged_group'][0]['text'].strip()=='}' for x in rows)==2
# Reuse a retained original positive rather than rerunning settled call tests.
mb=json.loads((R/'parent63-manifest.json').read_text());r63=(R/'parent63-result.json').read_bytes();assert sha(r63)==next(x['sha256'] for x in mb['members'] if x['path']=='result.json');old=json.loads(r63)['observations'][0];assert old['pc']==22 and old['coordinate_line']==417 and old['match']
bind=next(x for x in parent['bindings'] if x['module']=='evctrl' and x['scope']==1);a=bind['code_start']+22;assert e[a:a+12].hex()==old['bytecode_hex'];assert groups[416][0]['hex']==old['source']['bytes'] and groups[416][0]['text'].strip().startswith('askpos(') and not groups[415][0]['text'].strip().startswith('askpos(')
if '--fault-universal-minus-one' in sys.argv:assert groups[415][0]['text'].strip().startswith('askpos('),'Universal minus-one misattributes retained original positive call'
call_control=dict(source='Unchanged retained63 result/manifest/original bytes inspected; no new call/native/VM/live execution',pc=22,coordinate=417,current_group_matches=True,universal_minus_one_matches=False,parent63_result_sha256=sha(r63))
result=dict(status='TAGGED_GROUP_NOT_EXACT_ASSIGNMENT_SPAN',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=rows,controls=controls,retained_call_control=call_control,interpretation='Four original immediate/store pairs to variable61 agree with the immediately preceding logical assignment, while their uniform q0 tags select another variable assignment or closing brace. Combined with65 destination identity this refutes representing the tagged group as necessarily containing the emitting statement. Correct logical-coordinate addressability and sampled preceding-statement compatibility are different facts. Do not globally subtract one: unchanged retained63 original call tag still selects its expected group.',limits='No universal preceding-line rule, compiler parse/emission cause, complete source span or reconstruction of original debug UI. Possible lookahead/post-emission/grouping alternatives remain unresolved. No native stores/file-bank values, branch outcomes, normal gameplay reachability, synchronization, lifetime, ev shared tail or SN1X closure. Four new sampled cases, prior63pc16/call22 not new call tests. Original input bytes unchanged; private data controls not execution. PC OFF/S19 parked/fullL1+L2 NOT_MET')
p=W/'result.json';encoded=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==encoded,'Frozen result differs'
else:p.write_bytes(encoded)
print('PASS66 four original assignment/tag mismatches; exact destination and literal controls; no universal shift rule',flush=True)
