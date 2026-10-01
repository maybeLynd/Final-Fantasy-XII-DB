"""Read-only metadata reducer with labelled private byte interventions."""
import hashlib,json,re,struct,sys
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();u=lambda b,o:struct.unpack_from('<I',b,o)[0]
raw=json.loads((W/'raw.json').read_text())
for f in raw['reference']['files']:
 b=(R/(f['module']+'.'+f['extension'])).read_bytes();assert sha(b)==f['sha256'] and len(b)==f['bytes']
code=(R/'resolver591.bin').read_bytes();assert len(code)==591 and sha(code)==raw['reference']['resolver_sha256']
# Exact native reader identity; meaning of bank bases is a retained canonical premise.
at={int(i['pc'],16):i for i in raw['resolver']};load=at[0x26247c]
assert bytes.fromhex(load['hex'])==code[0x3c:0x3c+len(bytes.fromhex(load['hex']))]
assert load['mnemonic']=='mov' and load['memory'][0]['scale']==8 and load['memory'][0]['disp']==4 and load['memory'][0]['kind']=='r','Original native descriptor load +4/stride8'
def meta(b,e):
 pool=u(b,8);t0=u(b,4);n=u(b,t0);t2=u(b,0x14);end=t0+4+4*n;assert t2==(end+15)//16*16 and not any(b[end:t2]);names=[]
 for i in range(n):
  p=pool+u(b,t0+4+4*i);assert pool<=p<len(b) and (p==pool or b[p-1]==0) and b[p]!=0;z=b.index(b'\0',p);names.append(dict(index=i,field_offset=t0+4+4*i,offset=p,hex=b[p:z].hex(),name=b[p:z].decode('cp932')))
 assert e[:4]==b'EBP2' and u(e,4)==20;sect=u(e,0x10);assert sect==0x80 and u(e,sect)==0x8000000b;stop=sect+u(e,sect+4);vt=sect+u(e,sect+0x28);nv=u(e,vt);assert sect<=vt and vt+4+8*nv<=stop<=len(e)
 assert n==nv,'T0/native descriptor count disagreement'
 globals=[]
 for i in range(u(b,t2)):
  d,p=struct.unpack_from('<II',b,t2+4+8*i);a=pool+p;assert b[a-1]==0;z=b.index(b'\0',a);globals.append(dict(descriptor=d,name=b[a:z].decode('cp932'),record_offset=t2+4+8*i))
 return dict(t0=t0,t0_count=n,native_table=vt,native_count=nv,names=names,globals=globals)
metadata={m:meta((R/(m+'.dbg')).read_bytes(),(R/(m+'.ebp')).read_bytes()) for m in ['ctrl','btlctrl','evctrl','mapctrl']}
assert [(metadata[m]['t0_count'],metadata[m]['native_count']) for m in metadata]==[(56,56),(92,92),(115,115),(127,127)]
def observe(c,b,e):
 mt=meta(b,e);co=c['code_offset'];op=e[co+3];idx=struct.unpack_from('<H',e,co+4)[0];assert op==(0x49 if c['kind']=='assignment' else 0x4a);assert 0<=idx<mt['native_count'];off=mt['native_table']+4+8*idx;d,second=struct.unpack_from('<II',e,off)
 return dict(index=idx,name=mt['names'][idx]['name'],name_field_offset=mt['names'][idx]['field_offset'],name_byte_offset=mt['names'][idx]['offset'],descriptor_field_offset=off,descriptor_record_hex=e[off:off+8].hex(),descriptor=f'{d:08x}',width=d>>28,is_float=(d>>27)&1,storage_class=(d>>24)&7,offset=d&0xffffff,second_dword=second,global_name_matches=[x for x in mt['globals'] if x['descriptor']==d])
observations=[];controls=[]
for c in raw['cases']:
 m=c['module'];b=(R/(m+'.dbg')).read_bytes();e=(R/(m+'.ebp')).read_bytes();assert e[c['code_offset']:c['code_offset']+len(bytes.fromhex(c['code_hex']))].hex()==c['code_hex']
 text=bytes.fromhex(c['source']['hex']).decode('cp932');assert text==c['source']['text'];match=re.fullmatch(r'\s*(\w+)\s*=\s*(\d+)\s*;?\s*',text) if c['kind']=='assignment' else re.fullmatch(r'\s*dvar\s*\(\s*\d+\s*,\s*(\w+)\s*\)\s*;\s*',text);assert match and match[1]==c['expected_source_name']
 original=observe(c,b,e);assert original['index']==c['index'] and original['name']==c['expected_source_name'],'Original operand/name sample binding'
 ee=bytearray(e);struct.pack_into('<H',ee,c['code_offset']+4,c['index']+1);mutant=observe(c,b,bytes(ee));assert mutant['name']!=c['expected_source_name'],'Changed original encoded operand control'
 bb=bytearray(b);n=metadata[m]['names'];a=n[c['index']]['field_offset'];z=n[c['index']+1]['field_offset'];bb[a:a+4],bb[z:z+4]=bb[z:z+4],bb[a:a+4];name_mutant=observe(c,bytes(bb),e);assert name_mutant['name']!=c['expected_source_name'],'Changed original encoded name directory control'
 if '--fault-accept-shifted-operand' in sys.argv:assert mutant['name']==c['expected_source_name'],'Shifted operand falsely accepted as original name'
 if '--fault-ignore-name-directory' in sys.argv:assert name_mutant['name']==c['expected_source_name'],'Changed name directory falsely accepted'
 observations.append(dict(case=c,observation=original));controls.append(dict(module=m,pc=c['pc'],original_positive=True,private_encoded_operand=mutant,private_encoded_name_directory=name_mutant))
# Independent descriptor->global-name positive at selected original map operand32.
glob=observations[-1]['observation'];assert glob['storage_class']==0 and any(x['name']==glob['name'] for x in glob['global_name_matches'])
ev=observations[0]['observation'];assert (ev['descriptor'],ev['width'],ev['is_float'],ev['storage_class'],ev['offset'])==('01000905',0,0,1,0x905) and not ev['global_name_matches']
# Actual encoded count mismatch challenges equal-directory-count prerequisite.
e=(R/'evctrl.ebp').read_bytes();ee=bytearray(e);struct.pack_into('<I',ee,metadata['evctrl']['native_table'],114);rejected=False
try:meta((R/'evctrl.dbg').read_bytes(),bytes(ee))
except AssertionError as err:assert str(err)=='T0/native descriptor count disagreement';rejected=True
assert rejected,'Encoded count mismatch control did not reach detector'
if '--fault-ignore-count-domain' in sys.argv:assert not rejected,'Count-domain defect accepted'
result=dict(status='SAMPLED_ORIGINAL_VARIABLE_NAME_BINDING_SUPPORTED',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),counts=[dict(module=m,t0=v['t0_count'],native=v['native_count']) for m,v in metadata.items()],native_reader=load,observations=observations,controls=controls,count_control=dict(original=115,encoded_private=114,rejected=rejected),interpretation='All four original T0/native counts agree. Five exact bytecode operands select the same T0 names as retained source candidates, with changed-operand/name/count controls. ev operand0x61 identifies descriptor01000905: file-class, width0 u8, floatbit0, byteoffset905 under the existing native bank-base model. map operand0x20 has independent same descriptor/name in original T2 global directory. Supports sampled T0-index/name binding and ev destination storage identity, not only literal similarity.',limits='No original debugger/compiler reader or writer establishing universal T0 ordering/all entries/scopes; metadata sample and canonical storage model remain distinct. No actual slot/file-bank pointer, load flag values, initializer/lifetime/gameplay set/clear/read path, store/notification effects or normal reachability. ev source grouping attribution ambiguity remains; no SN1X closure. Private data bytes not executed. PC OFF/S19 unchanged/fullL1+L2 NOT_MET')
p=W/'result.json';encoded=(json.dumps(result,indent=2)+'\n').encode()
if p.exists():assert p.read_bytes()==encoded,'Frozen result differs'
else:p.write_bytes(encoded)
print('PASS65 five original name/descriptor samples; ev0x61 file-u8+905; no runtime effects or universal index proof',flush=True)
