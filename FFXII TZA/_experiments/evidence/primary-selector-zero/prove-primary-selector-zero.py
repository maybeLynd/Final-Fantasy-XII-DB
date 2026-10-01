"""Reference caller selects indexed primary: constant propagation with ABI limits."""
import hashlib,importlib.util,json,pathlib,struct,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('selector_proof','prove-title-queue-consumption.py');S=module('selector_roles','validate-title-source-annotations.py')
def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 driver=src/'capture-primary-selector-zero.py';st=json.loads((src/'primary-selector-zero-capture-01.status.json').read_text())
 if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(driver):raise ValueError('selector capture failed/stale')
 if not(src/'primary-selector-zero-capture-01.stdout').read_bytes().strip() or (src/'primary-selector-zero-capture-01.stderr').read_bytes().strip():raise ValueError('selector capture incomplete')
 pins=[];raw,leaf=P.load(src,'primary-selector-zero-source-01.json',pins);S.validate(raw)
 if raw.get('invocation_driver_sha256')!=P.sha(driver):raise ValueError('selector driver changed')
 retained=src/'index-path-raw-02.json';v=json.loads(retained.read_text());S.validate(v);q=next(q for q in v['ranges'] if q['start']=='0x32fca0');pins.append(dict(path=retained.name,sha256=P.sha(retained)))
 if (q['end_exclusive'],q['sha256'])!=('0x330048','1d796bf176912574660eedaa1919235222d3a34b66f6492014cae31b3884f9f7'):raise ValueError('retained caller identity changed')
 b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
 e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0];secs=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
 def read(a,n):
  for vs,va,rs,ro in secs:
   if 0x120000+va<=a and a+n<=0x120000+va+rs:return b[ro+a-0x120000-va:ro+a-0x120000-va+n]
  raise ValueError('original bytes unbacked')
 for z in raw['ranges']+[q]:
  if bytes.fromhex(''.join(i['bytes'] for i in z['instructions']))!=read(int(z['start'],16),int(z['end_exclusive'],16)-int(z['start'],16)):raise ValueError('reference byte identity changed')
 P.need(leaf,0x5c5230,'xor','eax, eax');P.need(leaf,0x5c5232,'ret','');leafcfg=P.closed(leaf,0x5c5230,0x5c5233)
 ix={int(i['pc'],16):i for i in q['instructions']}
 ops=[(0x32fcca,'je','0x32fcee'),(0x32fcd4,'je','0x32fcee'),(0x32fcdb,'call','0x5c5230'),(0x32fce0,'xor','r14d, r14d'),(0x32fce3,'test','eax, eax'),(0x32fce5,'mov','r13d, r14d'),(0x32fce8,'setne','r13b'),(0x32fcec,'jmp','0x32fcf4'),(0x32fcee,'xor','r14d, r14d'),(0x32fcf1,'mov','r13d, r14d'),(0x33000c,'test','r13d, r13d'),(0x33000f,'mov','r13, qword ptr [rsp + 0x68]'),(0x330014,'mov','r9d, ebp'),(0x330017,'mov','rbx, qword ptr [rsp + 0xb8]'),(0x33001f,'mov','r8d, esi'),(0x330022,'mov','edx, r15d'),(0x330025,'mov','ecx, edi'),(0x330027,'je','0x330030'),(0x330029,'call','0x3306e0'),(0x330030,'call','0x330310')]
 for pc,m,a in ops:P.need(ix,pc,m,a)
 # Complete original local destination enumeration, not a global writer census.
 writes=[i['pc'] for i in q['instructions'] if i['args'].split(',')[0] in ['r13','r13d','r13w','r13b'] and i['mnemonic'] not in ['test','cmp','push']]
 if writes!=['0x32fce5','0x32fce8','0x32fcf1','0x33000f']:raise ValueError('another local selector assignment exists')
 r14=[i['pc'] for i in q['instructions'] if i['args'].split(',')[0] in ['r14','r14d','r14w','r14b'] and i['mnemonic'] not in ['test','cmp','push']]
 if r14!=['0x32fce0','0x32fcee','0x330007']:raise ValueError('zero source assignment changed')
 # The selector TEST executes before restoration; only MOVs intervene before JE.
 middle=[i for i in q['instructions'] if 0x33000f<=int(i['pc'],16)<0x330027]
 if not middle or any(i['mnemonic']!='mov' for i in middle):raise ValueError('selector branch flags are not preserved')
 rows=[dict(prefix='first-mode-getter ==1',entry='0x32fcee',r14d=0,r13d=0),dict(prefix='first!=1 and second==3',entry='0x32fcee',r14d=0,r13d=0),dict(prefix='otherwise',entry='0x32fcdb',leaf_eax=0,test_zero_flag=1,setne=0,r13d=0)]
 result=dict(status='PRODUCER_VALID_REFERENCE_PRIMARY_SELECTOR_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,leaf_cfg=leafcfg,local_r13_assignments=writes,local_r14_assignments=r14,exhaustive_prefix_partition=rows,
  established=['Original5C5230 is XOR EAX,EAX;RET, independent of argument/state. It is a shipping constant-zero leaf, not a fixture stub modelling a native effect.',
  'All three reference32FCA0 prefix classes set localR13D to0: either direct mode-gate arm clears it, or the actual5C5230 return TEST givesZF1 and SETNE writes0 into an already zero register. Only these two arms assign before the later selector TEST.',
  'Normal ABI-preserving intermediate callees cannot mutate nonvolatileR13/R14. The later TEST R13D executes BEFORE savedcallerR13 is restored. Only MOVs intervene; they preserve flags. JE330030 therefore selects330310, not3306E0, on every normal unmodified execution of this caller.',
  'This eliminates a live option/state observation prerequisite for this specific caller edge. Other3306E0 callers, code interventions, exception/unwind/nonreturning paths, ABI violations, payload success and owner lifetime are not certified.'],
  limitations=['No game/live/native/emulated execution or proof of natural entry into32FCA0','Normal original instructions/nonvolatile ABI and valid context/memory/no intervention premises','Not an allcaller proof that3306E0 is unreachable; do not infer script/resource/payload effects from this selector','Producer proof/controls are distinct from independent acceptance/canonical consumption'],
  affected_claims=['FABLE/OPUS GR18 primary branch: ordinary32FCA0 reference edge uses330310; alternate selection here is not an initialized-state unknown','Historical method wording referring to option5 initialization at this call must be narrowed:5C5230 is constant zero'],
  next_discriminator='Consume existing DG6 override-initialization/writer proof without repeating its census, then inspect remaining independent alternate callers only if they can bind these authored scripts. No new gameplay merely for this selector.',
  required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-primary-selector-zero.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','primary-selector-zero-capture-01.status.json','primary-selector-zero-capture-01.stdout','primary-selector-zero-capture-01.stderr']],
  checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Finite source reads/disposable checks only; no PC/game/save/config/reference/peer mutation')
 out.open('x').write(json.dumps(result,indent=2)+'\n');print('Original caller selector is always zero under normal ABI; alternate edge excluded here without live observation')
if __name__=='__main__':main()
