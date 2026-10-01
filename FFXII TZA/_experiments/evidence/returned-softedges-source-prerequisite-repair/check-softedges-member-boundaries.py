"""Check only retained original member-recursion/array-callback boundaries.
Usage: python check-softedges-member-boundaries.py SOURCE_DIRECTORY FRESH_RESULT
No native execution, class census, installed-array proof or acceptance award.
Published source and results are immutable; missing/incomplete source is failure.
"""
import hashlib,json,pathlib,struct,sys
# Current actual CLI path requires the shipping-byte/annotation prerequisite.
# The identical legacy body is retained separately and in the published packet.
if __name__ == '__main__':
 import runpy
 runpy.run_path(str(pathlib.Path(__file__).with_name('check-softedges-member-boundaries-03.py')),run_name='__main__')
 raise SystemExit(0)
SHA='73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
source=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2])
if out.exists():raise ValueError('immutable result exists')
pins=[]
def load(name):
 p=source/name;z=p.read_bytes();r=json.loads(z)
 pins.append(dict(path=name,sha256=hashlib.sha256(z).hexdigest(),bytes=len(z)))
 if r.get('exe_sha256')!=SHA or r.get('wrapper_complete') is not True:raise ValueError('unchecked original capture prerequisite: '+name)
 if [(x['bytes'],x['observed']) for x in r.get('controls',[])]!=[('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:raise ValueError('actual adapter controls incomplete: '+name)
 for q in r['ranges']:
  a=int(q['start'],16);b=int(q['end_exclusive'],16);pc=a;raw=b''
  for x in q['instructions']:
   z=bytes.fromhex(x['bytes'])
   if int(x['pc'],16)!=pc or not z:raise ValueError('missing/overlapping instruction')
   pc+=len(z);raw+=z
  if pc!=b or hashlib.sha256(raw).hexdigest()!=q['sha256']:raise ValueError('incomplete/corrupt source span')
 return r
callback=load('softedges-elements-callback-source-01/original-code.json')
setter=load('softedges-member-assignment-code-01.json')
head=load('softedges-member-resolution-code-01.json')
tail=load('softedges-member-resolution-continuation-code-01.json')
fp=source/'softedges-elements-callback-source-01/facts.json';fz=fp.read_bytes();facts=json.loads(fz)
pins.append(dict(path=fp.relative_to(source).as_posix(),sha256=hashlib.sha256(fz).hexdigest(),bytes=len(fz)))
if facts.get('exe_sha256')!=SHA or facts.get('status')!='PRODUCER_SOURCE_COMPLETE_REVIEW_PENDING':raise ValueError('unchecked named assignment facts')
if facts.get('member_name')!='6d5f656c7300' or facts.get('slot_bytes')!='d0f3600000000000' or facts.get('callback')!='0x60f280':raise ValueError('wrong named slot/callback')
if facts.get('registration_source_sha256')!=next(p['sha256'] for p in pins if p['path']=='softedges-member-resolution-code-01.json'):raise ValueError('registration generation mismatch')
reg={int(i['pc'],16):i for q in head['ranges'] for i in q['instructions']}
for pc,target in [(0x5eedaf,0xd32dc0),(0x5eedcc,0xd4bd30),(0x5eedef,0x60f280)]:
 x=reg[pc];z=bytes.fromhex(x['bytes'])
 if len(z)!=7 or x['mnemonic']!='lea' or pc+7+struct.unpack('<i',z[-4:])[0]!=target:raise ValueError('original registration dependency changed')
if facts.get('file_classes',[{}])[-1].get('name')!='PArray<PShaderParameterDefinition>':raise ValueError('file/native named type mismatch')
def select(r,a,b):
 q=[q for q in r['ranges'] if int(q['start'],16)==a and int(q['end_exclusive'],16)==b]
 if len(q)!=1:raise ValueError('required exact range missing')
 return q[0]['instructions']
leaf=select(callback,0x60f3d0,0x60f3f1);cb=select(callback,0x60f280,0x60f290)
if ''.join(x['bytes'] for x in leaf)!='488b41704d8bd04c8bda4885c0740c458bc1498bd2498bcb48ffe0b815000000c3':raise ValueError('dispatcher boundary changed')
if ''.join(x['bytes'] for x in cb)!='4883ec28e857fdffff33c04883c428c3':raise ValueError('status propagation changed')
si=select(setter,0x60efe0,0x60f04d)
def instruction(ix,pc,mnemonic,args):
 x=next(x for x in ix if x['pc']==hex(pc))
 if (x['mnemonic'],x['args'])!=(mnemonic,args):raise ValueError('required original operation changed: '+hex(pc))
instruction(si,0x60eff8,'test','r8d, r8d');instruction(si,0x60effb,'jns','0x60f012')
instruction(si,0x60effd,'mov','eax, 5');instruction(si,0x60f011,'ret','')
instruction(si,0x60f02c,'call','0x5f03a0');instruction(si,0x60f031,'bts','ebx, 0x1f')
instruction(si,0x60f035,'mov','qword ptr [rdi + 8], rsi');instruction(si,0x60f040,'mov','dword ptr [rdi], ebx')
ri=select(head,0x59ec40,0x59ec53);pc=0x59ec53
for q in tail['ranges']:
 if int(q['start'],16)!=pc:raise ValueError('resolver continuation gap')
 ri+=q['instructions'];pc=int(q['end_exclusive'],16)
if pc!=0x59ed61 or len(tail.get('verified_unwind_chains',[]))!=7:raise ValueError('normal resolver continuation unverified/incomplete')
instruction(ri,0x59ed3b,'add','dword ptr [r12], r14d')
instruction(ri,0x59ed3f,'lea','eax, [rdx + rbx]');instruction(ri,0x59ed42,'add','rax, r13')
instruction(ri,0x59ed52,'xor','eax, eax')
result=dict(status='PRODUCER_CHECKED_INDEPENDENT_PENDING',method='A STATIC_ONLY',exe_sha256=SHA,
 producer_complete=True,checker_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),inputs=pins,
 established=[
  dict(claim='named-m_els-dispatch-ABI',result='60F3D0 uses metadata+70; supplies object/source/count directly to the callback, without a second member-offset or class-F4 address adjustment. Null callback returns21.'),
  dict(claim='callback-zero-not-count-acceptance',result='Registered60F280 executes60EFE0 then overwrites EAX with0. Negative signed count gives inner5/no array write but normal outer return0. Nonnegative normal continuation associates source/count|80000000. Opaque5F03A0 effects excluded.'),
  dict(claim='packed-member-return-width',result='59EC40 through-path address is (object + zext32(memberNativeOffset + childF4 - parentF4)) mod2^64. Residual offset update is mod2^32. It is not unrestricted signed pointer arithmetic; the original writes EAX before adding the64-bit object.')
 ],
 arithmetic_discriminator=dict(member_offset=0,child_f4=0,parent_f4=8,original_delta=4294967288,unrestricted_signed_delta=-8,
   label='ISA-width counterexample calculation only; supplied values are not claimed naturally reachable and this is not a native execution'),
 unresolved=['Actual file-member mapped-child construction and key22/27 terminal member','Successful loaded-resource binding and descriptor adjustments in that load','Pointer lifetime, cleanup effects, destination aliases and natural reachability'],
 limits='Conditional original source behavior, no forced call or game observations. The retained mapping records are not supplied here as runtime state. Registered native m_els name must be checked against separate source facts; this checker does not prove the loader installs that member.',
 live_runs=0,isolated_native_runs=0)
out.write_text(json.dumps(result,indent=2)+'\n')
print('CHECKED three bounded original-source claims; installed-array binding remains OPEN')
