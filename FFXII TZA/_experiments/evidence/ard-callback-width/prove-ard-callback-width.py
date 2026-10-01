"""Original ARD destination/context widths and published-root invariant, Method A."""
import importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('ard_proof_dependencies','prove-title-queue-consumption.py');S=module('ard_proof_annotations','validate-title-source-annotations.py')
EXPECTED=[('0x3ea820','0x3ea87e','308425102be4b3d4ee2ba161ac0a85614f860eaa1658a2b4565016b20ff10034'),('0x3ea710','0x3ea81b','58cf78e87cc8413fb8225e96c234657389a116fd46a5d82b4ce65a0fde46ec81'),('0x36c660','0x36c6b2','d713286ef629452bdaee63fa100457488b5bdf22dbc2e647839c5ecb90dc6323'),('0x3ea87e','0x3ea947','9aa7279e0f3759df799f666e2485528f994238bd41880f82d028376e420363f7'),('0x3ea947','0x3ea9fc','dae400b2efd3a9f99a7464f943907e375c1244db0b7cdda49cc00db61ce58109')]
def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 driver=src/'capture-ard-callback-width.py';st=json.loads((src/'ard-callback-width-capture-01.status.json').read_text())
 if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(driver):raise ValueError('required ARD capture invocation failed or stale')
 if not (src/'ard-callback-width-capture-01.stdout').read_bytes().strip() or (src/'ard-callback-width-capture-01.stderr').read_bytes().strip():raise ValueError('required ARD capture output missing or failed')
 pins=[];raw,ix=P.load(src,'ard-callback-width-source-01.json',pins)
 if raw.get('invocation_driver_sha256')!=P.sha(driver):raise ValueError('required capture wrapper changed')
 if [(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']]!=EXPECTED:raise ValueError('required original ARD identity changed')
 annotations=S.validate(raw)
 # Actual validator checks annotations; pin every byte span to the full image too.
 import hashlib,struct
 data=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if hashlib.sha256(data).hexdigest()!=P.SHA:raise ValueError('original image changed')
 pe=struct.unpack_from('<I',data,60)[0];opt=struct.unpack_from('<H',data,pe+20)[0];secs=[struct.unpack_from('<IIII',data,pe+24+opt+k*40+8) for k in range(struct.unpack_from('<H',data,pe+6)[0])]
 def read(a,n):
  for vs,va,rs,ro in secs:
   if 0x120000+va<=a and a+n<=0x120000+va+rs:return data[ro+a-0x120000-va:ro+a-0x120000-va+n]
  raise ValueError('required original span unbacked')
 for a,z,h in EXPECTED:
  if hashlib.sha256(read(int(a,16),int(z,16)-int(a,16))).hexdigest()!=h:raise ValueError('source differs from original shipping image')
 binder=P.closed(ix,0x3ea710,0x3ea81b);tag=P.closed(ix,0x36c660,0x36c6b2)
 ops=[(0x3ea923,'call','0x36a100'),(0x3ea928,'mov','rcx, rax'),(0x3ea934,'call','0x36c660'),(0x36c66d,'mov','rbx, rcx'),(0x36c6a4,'mov','rax, rbx'),(0x3ea93e,'test','rax, rax'),(0x3ea941,'je','0x3ea9e4'),
 (0x3ea947,'lea','rdx, [rip - 0x23e]'),(0x3ea956,'mov','qword ptr [rsp + 0x40], rdx'),(0x3ea95e,'lea','rdx, [rsp + 0x30]'),(0x3ea96c,'mov','qword ptr [rsp + 0x20], rdx'),(0x3ea971,'mov','r8, rax'),(0x3ea976,'mov','dword ptr [rsp + 0x38], eax'),(0x3ea97f,'call','0x32e620'),
 (0x3ea732,'mov','ebp, ecx'),(0x3ea734,'mov','ecx, ecx'),(0x3ea736,'call','0x36c660'),(0x3ea73b,'mov','ecx, dword ptr [rbp + 0x10]'),(0x3ea746,'movsxd','rsi, eax'),(0x3ea749,'add','rsi, rbp'),(0x3ea754,'movsxd','rdi, eax'),(0x3ea757,'add','rdi, rbp'),(0x3ea75f,'movsxd','rbx, eax'),(0x3ea767,'add','rbx, rbp'),(0x3ea76a,'call','0x23a160'),(0x3ea777,'call','0x23a160'),(0x3ea784,'call','0x23a160'),(0x3ea809,'mov','qword ptr [rip + 0x27738b0], rbp'),(0x3ea810,'mov','rbp, qword ptr [rsp + 0x38]')]
 for pc,m,a in ops:P.need(ix,pc,m,a)
 if ix[0x3ea947]['memory'][0]['rip_target']!='0x3ea710' or ix[0x3ea809]['memory'][0]['rip_target']!='0x2b5e0c0':raise ValueError('callback/publication identity changed')
 bp_dest=[i['pc'] for pc,i in sorted(ix.items()) if 0x3ea710<=pc<0x3ea81b and i['args'].split(',')[0] in ['rbp','ebp','bp','bpl']]
 if bp_dest!=['0x3ea732','0x3ea810']:raise ValueError('binder saved-root has another local assignment')
 # Normalize algebraic widths; these are not native executions or live addresses.
 examples=[]
 for full in [0x7fffffff,0x80000000,0xffffffff,0x100010000,0xffffffff00000000]:
  context=full&0xffffffff;root=context;examples.append(dict(full_destination=hex(full),descriptor_context=hex(context),binder_saved_root=hex(root),full_pointer_preserved=context==full))
 if any(int(e['binder_saved_root'],16)>0xffffffff for e in examples):raise ValueError('width algebra control failed')
 cross=dict(root='0xffffff00',resolved_low32_offset='0x1000',signed_offset=0x1000,section_pointer=hex(0xffffff00+0x1000),natural_reachability=False)
 receipts=['ard-callback-width-capture-01'+s for s in ['.status.json','.stdout','.stderr']]+['capture-ard-callback-width.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py']
 result=dict(status='PRODUCER_VALID_ARD_CALLBACK_WIDTH_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=annotations,required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],normal_cfg=[binder,tag],instruction_pins=[dict(pc=hex(pc),mnemonic=m,args=a) for pc,m,a in ops],binder_root_assignments=bp_dest,bounded_algebra=examples,conditional_section_crossing=cross,
 established=['After normally returning36A100 and pointer-tagging36C660, loader3EA820 tests fullRAX, sends it as fullR8 read destination, but stores onlyEAX into DWORD descriptor+8. Descriptor+10 points to original3EA710. That destination/context distinction is before queue acceptance; it is not a performed read or callback.',
 'Pointer tag36C660 returns its incomingRCX through savedRBX without narrowing on every normal return. Its header accesses/import effects require valid backing/normalABI and are not native effects proved by this source. It cannot repair the later descriptor DWORD narrowing.',
 'At binder entry3EA732, MOV EBP,ECX makes saved root zeroextended32 regardless of incoming highRCX.3EA734 alsozeroextends RCX before tag call. No later local assignment toRBP precedes3EA809 publication; its normalABI callees must preserveRBP. Thus this writer alwayspublishes a root in0..FFFFFFFF at qword02B5E0C0. EBP does not signextend bit31.',
 'Sampling that published qword cannot recover or disprove a high original allocator result: it is alreadynarrowed, and unload zero is not evidence of a successful allocation. This writer invariant is not an allwriter/global-lifetime census.',
 'Section binding instead adds saved root in64bits to a SIGNED extension of the resolver lowDWORD. A root below4GiB does not alone prove every section/row pointer below4GiB: conditional rootFFFFFF00+offset1000=100000F00. This algebraic counterexample is not a shipped ARD/state or native execution.',
 'A high original destination and a low callback root are different storage identities unless additional alias/mapping facts establishotherwise. The original functions do not reconstruct highbits from read destination. Normal queued reachability, valid lowheader, allocator placement and actual consequences remainopen. Do not force a high call and present it as natural reachability.'],
 assumptions=['Execution reaches the named original normal loader/tag/binder branches with valid requested memory/descriptors/header and ABI-correct normally returning callees', 'No unexpected concurrent/instrumented code modification or nonvolatileRBP/RBX violation', 'Only this callback entry and publication writer are certified; otherwriters/queuecallback dispatch and real initialization not newly censused'],
 limitations=['No native/emulated/live/CRT module execution or new placement sample; retained EXP077/078/079 are prior bounded evidence, not additional runs', 'No alltime lowheap, initialized arena/topology, healthy highallocation, queued acceptance, callback lifetime, natural highroot or rewardedge occurrence', 'Signedsection arithmetic and cached rewardrow truncation are different widths/locations; full allocatedrange and actualbound section identity need their own evidence', 'No full GR18/OV5/OV8/AQ-ARENA closure or new whole runtime-row count; independent review and canonical incorporation pending'],
 affected_claims=['OPUS GR18 allocation placement question: full destination and low callback/published root must be distinguished before reward truncation inference','FABLE ARD binder: callback root parameter and signed offset/64bitsection addition contract','Future ASTRA observer: fullRAX at3EA93E orR8 at3EA97F, not publishedroot alone'],
 next_discriminator='Reuse retained arena placement and original allocator evidence; if actual placement stillrequired, observe the full allocator/tag-return destination at3EA93E or read-submit3EA97F with identity/state/queueacceptance controls. Publishedroot sample alone is insufficient. No menu setup authorized or automatic freshgame experiment here.',checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Only shipping source reads/finite reduction/disposable controls; no game/PC/input/native/instrument/save/config/reference/peer process change')
 out.open('x',encoding='utf-8').write(json.dumps(result,indent=2)+'\n');print('Original full read destination/low callback root invariant proved; real placement and section bounds remainOPEN')
if __name__=='__main__':main()
