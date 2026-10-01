import ast,hashlib,json,re,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u=lambda b,o:struct.unpack_from('<I',b,o)[0];raw=json.loads((W/'raw.json').read_text())
for f in raw['reference']['files']:
 b=(W/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
b=(R/'evctrl.dbg').read_bytes();e=(R/'evctrl.ebp').read_bytes();s=(R/'evctrl.sbn').read_bytes();pool=u(b,8);T0=u(b,4);T2=u(b,20);N=u(b,T0);sect=u(e,16);vt=sect+u(e,sect+40);assert N==u(e,vt)==115 and u(b,T2)==943 and T0==0x78 and T2==((T0+4+4*N+15)//16)*16 and (T2+4+8*943+15)//16*16==u(b,0x2c)
def name_at(bb,pos):
 a=pool+pos;assert pool<=a<len(bb) and (a==pool or bb[a-1]==0) and bb[a]!=0;z=bb.index(b'\0',a);return bb[a:z]
names=[name_at(b,u(b,T0+4+4*i)) for i in range(N)];pairs=[(u(b,T2+4+8*j),name_at(b,u(b,T2+8+8*j))) for j in range(943)]
observed=[];controls=[]
for r in raw['rows']:
 i=r['index'];a=vt+4+8*i;d=u(e,a);matches=[n for dd,n in pairs if dd==d];assert e[a:a+8].hex()==r['native_record_hex'] and a==r['native_record_offset'] and b[T0+4+4*i:T0+8+4*i].hex()==r['t0_field_hex'];assert d==int(r['descriptor'],16)==0xa02+i and d>>24==0
 assert len(matches)==1 and matches[0]==names[i] and matches[0]!=names[i+1] and matches[0].hex()==r['t0_name']['hex'],'Exact independent global name identity'
 for t in r['t2_matches']:
  z=t['record_offset'];assert b[z:z+8].hex()==t['record_hex'] and u(b,z)==d and name_at(b,u(b,z+4)).hex()==t['name']['hex']
 assert len(r['t2_matches'])==1
 ee=bytearray(e);struct.pack_into('<I',ee,a,d+1);mut=[n for dd,n in pairs if dd==u(ee,a)];assert len(mut)==1 and mut[0]!=names[i],'Encoded native descriptor shift changes selected global name'
 bb=bytearray(b);struct.pack_into('<I',bb,T0+4+4*i,u(b,T0+4+4*(i+1)));nm=name_at(bb,u(bb,T0+4+4*i));assert nm!=matches[0],'Encoded name-offset shift changes selected native/global identity'
 if '--fault-attribution-implies-name-shift' in sys.argv:assert matches[0]==names[i+1],'Source alignment does not prove shifted variable directory'
 observed.append(dict(index=i,descriptor=f'{d:08x}',name=names[i].decode('cp932'),global_t2_record=r['t2_matches'][0],matches_unshifted=True,matches_next=False));controls.append(dict(index=i,encoded_descriptor_shift_name=mut[0].decode('cp932'),encoded_t0_shift_name=nm.decode('cp932'),original_name_match=True))
assert len(observed)==62 and len({x['descriptor'] for x in observed})==62
parent=json.loads((R/'parent61-raw.json').read_text());pb=(R/'selected-sbn-functions.py').read_bytes();assert sha(pb)==parent['reference']['parser_sha256'];ns={'struct':struct};exec(compile(pb,'retained original source parser','exec'),ns);bo,be=ns['sbn_blocks'](s)[0];L,bases,starts,te=ns['sbn_group_read'](s,bo);texts=[s[a:s.index(b'\0',a,be)] for a in starts];groups=[];continuing=False
for i,t in enumerate(texts):
 if not continuing:groups.append([])
 groups[-1].append(i);continuing=t.decode('cp932').rstrip('\r\n \t').endswith(chr(92))
assert len(groups)==1912 and not continuing
c=raw['first_store'];bind=next(x for x in parent['bindings'] if x['module']=='evctrl' and x['scope']==1);a=bind['code_start']+c['pc'];qo=bind['q0']+4*c['pc'];assert a==c['code_offset'] and qo==c['q0_offset'] and e[a:a+3].hex()==c['code_hex']=='490100' and b[qo:qo+4].hex()==c['q0_hex'];ln,bk,fl=struct.unpack_from('<HBB',b,qo);assert bk==0 and fl==1
current=b' '.join(texts[j] for j in groups[ln-1]).split(b'//')[0];preceding=b' '.join(texts[j] for j in groups[ln-2]).split(b'//')[0]
src=(R/'opus-variable-binding-primary.py').read_bytes();assert sha(src)==raw['reference']['primary_sha256'];fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='on');assert sha(ast.dump(fn,include_attributes=True).encode())==raw['reference']['predicate_ast_sha256'];pred={'NAMES':{'evctrl':names},'re':re};exec(compile(ast.Module(body=[fn],type_ignores=[]),'unchanged published OPUS on() predicate','exec'),pred)
cur1=pred['on']('evctrl',1,current);cur2=pred['on']('evctrl',2,current);before=pred['on']('evctrl',1,preceding);assert cur1 is False and cur2 is True and before is True,'Actual original source/predicate discriminator'
if '--fault-current-group-is-variable-binding' in sys.argv:assert cur1,'Actual current marker predicate cannot override independent metadata binding'
control=dict(original_first_store=c,logical_marker=ln,current_physical=[j+1 for j in groups[ln-1]],preceding_physical=[j+1 for j in groups[ln-2]],tagged_group=current.decode('cp932'),preceding_group=preceding.decode('cp932'),actual_opus_predicate_unshifted_on_current=cur1,actual_opus_predicate_shifted_on_current=cur2,actual_opus_predicate_unshifted_on_preceding=before,independent_t2_name_for_operand1=observed[0]['name'])
result=dict(status='GLOBAL_NAME_BINDING_DISTINCT_FROM_SOURCE_MARKER_ALIGNMENT',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),identities=observed,controls=controls,source_predicate_control=control,interpretation='All62 selected original ev global descriptors/T2 names agree with T0[n], none with T0[n+1]. Exact first POPV1 marker mentions next T0[2] name and preceding group mentions original T0[1]; unchanged published on() predicate reproduces that discrepancy. Source-marker alignment and native/global name identity are distinct. These metadata bindings refute using the observed source offset as proof of a shifted directory in this domain; retain OPUS59/0 observations and count-insufficiency warning, qualify interpretation/consumer mapping.',limits='62-domain metadata identity under admitted original T2 descriptor/name format, not universal T0 ordering115entries/allmodules/scopes/compilerwriter or semantic meaning ofmonster flags. No original debugger/native/VM/game execution, values/lifetime/normalreachability or source-span/global-minus1 rule. OPUS59/0 counts are existing owner corroboration, not new tests. Preserve65 publication addendum/old invalidmanifest; scientific inputs verified atoriginalcommit. Independent acceptance and consumer incorporation pending. PC OFF/S19/fullL1+L2 NOT_MET')
p=W/'result.json';enc=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==enc,'Frozen result differs'
else:p.write_bytes(enc)
print('PASS68 independent descriptor/name pairing resolves62-domain identity; first actual predicate shows source-marker offset, not name shift proof',flush=True)
