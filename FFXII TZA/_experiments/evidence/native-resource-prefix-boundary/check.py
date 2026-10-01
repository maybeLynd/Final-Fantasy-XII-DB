import sys
sys.dont_write_bytecode=True
import hashlib,json,struct,types
from pathlib import Path
import capstone
W=Path(__file__).resolve().parent;R=W/'retained';sha=lambda b:hashlib.sha256(b).hexdigest();raw=json.loads((W/'raw.json').read_text())
assert sha(Path(sys.executable).read_bytes())==raw['tools']['python_sha256'] and capstone.__version__==raw['tools']['capstone']
for p in raw['tools']['provider_files']:assert sha(Path(p['path']).read_bytes())==p['sha256']
for f in raw['reference']['files']:assert sha((R/f['copy']).read_bytes())==f['sha256']
parent=json.loads((R/'parent82-raw.json').read_text());manifest=json.loads((R/'parent82-manifest.json').read_text());members={x['path']:x for x in manifest['members']}
for f in raw['reference']['files']:
 if f['path']!='manifest.json':assert members[f['path']]['sha256']==f['sha256']
assert parent['reference']['exe_sha256']==raw['reference']['exe_sha256']
code=(R/'parent82-selector.bin').read_bytes();source=next(f for f in parent['functions'] if f['name']=='selector');assert len(code)==159 and sha(code)==source['sha256']
roles=types.ModuleType('roles');exec(compile((R/'parent82-reg_tracking.py').read_bytes(),'actual reviewed access policy','exec'),roles.__dict__);cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;ii=list(cs.disasm(code,0x19a5b0));by={i.address:i for i in ii}
for i,row in zip(ii,source['instructions']):
 assert (hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)==(row['pc'],row['hex'],row['mnemonic'],row['args'])
 assert sorted(roles.written(i))==row['written'] and [roles.op_kind(i,o,j) for j,o in enumerate(i.operands) if o.type==capstone.CS_OP_MEM]==row['memory']
assert len(ii)==len(source['instructions'])
for pc,want in [(0x19a605,'8bc8'),(0x19a607,'4803cb'),(0x19a60a,'83e70f'),(0x19a610,'483bd9'),(0x19a613,'7315'),(0x19a615,'0fb703'),(0x19a618,'488d1c43'),(0x19a61c,'4883c302'),(0x19a625,'483bd9'),(0x19a628,'7204'),(0x19a62a,'33c0'),(0x19a630,'663903'),(0x19a633,'480f44d8'),(0x19a637,'488bc3')]:assert by[pc].bytes.hex()==want
assert by[0x19a630].operands[0].type==capstone.CS_OP_MEM and by[0x19a630].operands[0].size==2 and roles.op_kind(by[0x19a630],by[0x19a630].operands[0],0)=='r'
for b,index,want in [('8900',0,'w'),('8d00',1,'addr'),('830001',0,'rw')]:
 i=next(cs.disasm(bytes.fromhex(b),0));assert roles.op_kind(i,i.operands[index],index)==want
assert int(raw['id'],16)&15==7 and len(raw['cases'])==4
observations=[]
for c in raw['cases']:
 b=bytes.fromhex(c['resource_hex']);end=c['declared_size'];assert len(b)==end;p=0;steps=[]
 for j in range(7):
  assert p<end and p+2<=end;n=struct.unpack_from('<H',b,p)[0];assert n==0;steps.append(dict(index=j,prefix_offset=p,length=n));p+=2+2*n
 assert p==14 and p<end
 wordfits=p+2<=end
 if wordfits:
  n=struct.unpack_from('<H',b,p)[0];result='NULL' if n==0 else 'PREFIX+14';textend=p+2+2*n;full=textend<=end
 else:n=None;result='UNESTABLISHED_WORD_READ_OUTCOME';textend=None;full=None
 observations.append(dict(name=c['name'],declared_size=end,previous_prefix_steps=steps,current_prefix=p,pointer_lt_end=p<end,source_word_access=[p,p+2],word_fits_logical_span=wordfits,count=n,full_counted_end=textend,full_counted_span_fits=full,conditional_source_result=result,provenance='Source calculation with supplied successful API state, not interpreter/guest/native/live execution'))
assert [(x['conditional_source_result'],x['full_counted_span_fits']) for x in observations]==[('PREFIX+14',True),('PREFIX+14',False),('UNESTABLISHED_WORD_READ_OUTCOME',None),('NULL',True)]
if '--fault-fullspan-guard' in sys.argv:assert observations[1]['conditional_source_result']=='NULL','Original source returns a nonempty prefix without a full counted-text-span test'
if '--fault-text-pointer' in sys.argv:assert observations[0]['conditional_source_result']=='TEXT+16','Original selector returns length-prefix RBX, not text+2'
if '--fault-short-prefix-null' in sys.argv:assert observations[2]['conditional_source_result']=='NULL','Incomplete prefix still reaches a word-read attempt; outcome is not established'
result=dict(status='STATIC_PREFIX_CHECK_NOT_FULL_COUNTED_TEXT_VALIDATION',method=raw['method'],raw_sha256=sha((W/'raw.json').read_bytes()),observations=observations,interpretation='Exact source checks currentpointer<resourceend then reads u16 length and returns nonempty prefix. Supplied id7837/priorsevenempty records put prefix14; size16/count1 conditionally returns that prefix while fulltext ends18. Size15 still passes current-pointer check but two-byte prefix read exceeds logicalend, physical outcome unestablished. Zero complete prefix returnsnull. This falsifies a selector-alone fullspan postcondition, not actual native API acceptance or game safety.',consumer_change='Use conditional nonempty borrowed length-prefix result, not validated complete UTF16 span; callers/reconstruction need explicit resource-validation preconditions. Preserve native API validity/reach/lifetime uncertainty, no actual crash inference.',limits=raw['limits'])
if not any(a.startswith('--fault-') for a in sys.argv):
 p=W/'result.json'
 if p.exists():assert json.loads(p.read_text())==result
 else:p.write_text(json.dumps(result,indent=2)+'\n')
print('PASS83 original source/count-prefix boundary counterexamples only, no execution',flush=True)
