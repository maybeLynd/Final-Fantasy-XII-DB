"""Compose retained original opcode2F frame construction with bank callback reads.

This local branch proof does not establish the live interpreter's initialized
range/scheduling or an opaque helper's effects. Reuse BG11; do not recapture it.
"""
import importlib.util,json,pathlib,struct,sys

W=pathlib.Path(__file__).resolve().parent
def module(name,file):
 s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('callback_frame_proof','prove-title-queue-consumption.py')
S=module('callback_frame_roles','validate-title-source-annotations.py')
BANK=[('0x185a50','0x185a7d','dfa1a293fdfc1e98492916b79b3479fdfc32928bb8d51fabcba3b02e3c6d4a88'),('0x5fea50','0x5feb21','d875fe2cc599597c3134165d5680324040fd39faa5cfb7b1728dc3cff05d5172'),('0x62ebc0','0x62ec07','f98fcc9cc174a3f7a6952fabe21ca3ac893475ad19bcecf9e6d360702acc530a'),('0x62ec07','0x62ec40','ff7f3241ac30a1d9fac75d1480cc2aefe8eb990fe7a5810ec9f82bd9eec4292a'),('0x62ec40','0x62ec67','376703e051b0e37e389aecb5653bb9d88f0ff51bab6f8da94dbb740bc98316a2'),('0x186610','0x18661f','89f1ea014898ea25e5107d42e83937bdfd92281abc6718fa6de4315ee306aaf0')]
RENDER=[('0x6106a0','0x6107e2','833a234a8071ab6ab2983614122410c5193d12b2157af738fdbd11f561de84a2'),('0x60a410','0x60aab7','4b654c1834ad69bd715c81399afe557f8cdb46db0ebf4eab65580ca1c8b20ab3'),('0x5fd050','0x5fd0d1','22d2a3c8af03c99c56c4b51e16ffc75762d7635fff57fcb865e1b5acb6f8a9b8'),('0x624670','0x624675','a1edf4c4981163b563a1199e40c223e9b0cb8feb2a7a99dd69f9d29d4aead762'),('0x624660','0x624668','ee25c9e3af9d40a73ad0aa13398cee73cedb9b998388406e9c31be8b84048d73'),('0x1f4a10','0x1f4a3f','cf996977382477519d2f26de693032fd7e3abb85c96bbe630c2dc696d3b69dff')]

def main():
 if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source]')
 out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
 if out.exists():raise ValueError('immutable result exists')
 status=src/'texture-async-bank-dispatch-positive-01.status.json';r=json.loads(status.read_text())
 producer=src/'prove-texture-async-bank-dispatch.py';bank_result=src/'texture-async-bank-dispatch-result-01.json';b=json.loads(bank_result.read_text())
 if r.get('exit')!=0 or r.get('checker_sha256')!=P.sha(producer) or b.get('producer_complete') is not True or b.get('checker_sha256')!=P.sha(producer):raise ValueError('required bank producer invocation/result failed or stale')
 stdout=src/'texture-async-bank-dispatch-positive-01.stdout';stderr=src/'texture-async-bank-dispatch-positive-01.stderr'
 if not stdout.read_bytes().strip() or stderr.read_bytes().strip():raise ValueError('required bank producer output missing/failed')
 for pin in b['source_pins']+b['required_invocation_receipts']:
  if P.sha(src/pin['path'])!=pin['sha256']:raise ValueError('required bank prerequisite preimage changed')
 # BG11's retained capture is a focused source record, not the later full-wrapper
 # schema. Do not alter it or invent wrapper completeness. Qualify its actual
 # bytes/roles/identity and limit this proof to the selected dispatch branch.
 pins=[];rp=src/'render-executor-consumption-raw-01.json';render=json.loads(rp.read_text())
 if render.get('exe_sha256')!=P.SHA or render.get('adapter_sha256')!=P.ADAPTER or render.get('driver_sha256')!=P.sha(src/'capture-index-path.py'):raise ValueError('required retained original capture prerequisite changed')
 if [(q['bytes'],q['observed']) for q in render['controls']]!=[('0f1101','w'),('488d4104','addr'),('f00fb101','rw')]:raise ValueError('required retained observer controls missing')
 pins.append(dict(path=rp.name,sha256=P.sha(rp)));x={int(i['pc'],16):i for q in render['ranges'] for i in q['instructions']}
 bank,y=P.load(src,'texture-async-bank-dispatch-source-01.json',pins)
 annotations=[S.validate(q) for q in (render,bank)]
 if [(q['start'],q['end_exclusive'],q['sha256']) for q in render['ranges']]!=RENDER:raise ValueError('required retained executor identity changed')
 if [(q['start'],q['end_exclusive'],q['sha256']) for q in bank['ranges']]!=BANK:raise ValueError('required retained bank identity changed')
 old=src/'render-executor-consumption-result-01.json';o=json.loads(old.read_text())
 if o.get('capture_sha256')!=P.sha(src/'render-executor-consumption-raw-01.json') or o.get('driver_sha256')!=P.sha(src/'check-render-executor-consumption.py') or o.get('exe_sha256')!=P.SHA:raise ValueError('required retained executor provenance changed')
 if render.get('invocation_driver_sha256')!=P.sha(src/'capture-render-executor-consumption.py'):raise ValueError('required retained capture driver changed')
 # Read only the already-retained dispatch table bytes from their shipping source.
 root=S.ROOT;d=(root/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
 if P.sha(root/'Database/Tools/work/exe/FFXII_TZA.exe')!=P.SHA:raise ValueError('original image identity changed')
 pe=struct.unpack_from('<I',d,60)[0];opt=struct.unpack_from('<H',d,pe+20)[0]
 secs=[struct.unpack_from('<IIII',d,pe+24+opt+40*k+8) for k in range(struct.unpack_from('<H',d,pe+6)[0])]
 def read(a,n):
  for vs,va,rs,ro in secs:
   if 0x120000+va<=a and a+n<=0x120000+va+rs:return d[ro+a-0x120000-va:ro+a-0x120000-va+n]
  raise ValueError('original table not fully backed')
 labels=read(0x60aad8,47);targets=read(0x60aab8,32)
 if labels.hex()!=o['dispatch']['labels_hex'] or targets.hex()!=o['dispatch']['targets_hex']:raise ValueError('required retained original dispatch table differs')
 arm=labels[46];target=0x120000+struct.unpack_from('<I',targets,4*arm)[0]
 if arm!=6 or target!=0x60a899:raise ValueError('original opcode2F dispatch changed')
 ops=[(0x60a5b3,'lea','rbx, [rsi + 0x70]'),(0x60a5c0,'mov','ecx, dword ptr [rsi]'),(0x60a5c2,'dec','ecx'),(0x60a5c4,'cmp','ecx, 0x2e'),(0x60a5c7,'ja','0x60a9c6'),(0x60a5cd,'movsxd','rax, ecx'),(0x60a5d0,'movzx','eax, byte ptr [r12 + rax + 0x4eaad8]'),(0x60a5d9,'mov','ecx, dword ptr [r12 + rax*4 + 0x4eaab8]'),(0x60a5e1,'add','rcx, r12'),(0x60a5e4,'jmp','rcx'),
      (0x60a899,'mov','rcx, qword ptr [rsp + 0x50]'),(0x60a89e,'test','rcx, rcx'),(0x60a8a1,'je','0x60a8b4'),(0x60a8a3,'mov','r8, rcx'),(0x60a8a6,'lea','rdx, [rsp + 0x58]'),(0x60a8ab,'mov','rcx, qword ptr [rcx + 0x28]'),(0x60a8af,'call','0x60b750'),(0x60a8b4,'mov','qword ptr [rsp + 0x50], 0'),
      (0x60a8bd,'mov','qword ptr [rbp - 0x50], r14'),(0x60a8c1,'lea','rax, [rsp + 0x50]'),(0x60a8c6,'mov','qword ptr [rbp - 0x48], rax'),(0x60a8ca,'mov','rax, qword ptr [rbx - 0x60]'),(0x60a8ce,'mov','qword ptr [rbp - 0x40], rax'),(0x60a8d2,'lea','rcx, [rbp - 0x50]'),(0x60a8d6,'call','qword ptr [rbx - 0x68]'),(0x60a8d9,'jmp','0x60a9d9'),(0x60a9d9,'sub','rsi, -0x80'),(0x60a9dd,'sub','rbx, -0x80'),(0x60a9e1,'cmp','rsi, r15'),(0x60a9e4,'jne','0x60a5c0')]
 for pc,m,a in ops:P.need(x,pc,m,a)
 bank_ops=[(0x185a54,'mov','r8d, dword ptr [rip + 0x1df9b35]'),(0x185a5b,'lea','rdx, [rip + 0xbae]'),(0x185a62,'call','0x5fea50'),(0x5fea5f,'mov','rsi, r8'),(0x5fea62,'mov','rdi, rdx'),(0x5feaf4,'mov','qword ptr [rcx + 8], rdi'),(0x5feaf8,'mov','qword ptr [rcx + 0x10], rsi'),(0x186610,'mov','edx, dword ptr [rcx + 0x10]'),(0x186613,'mov','rcx, qword ptr [rip + 0x1df8f9e]'),(0x18661a,'jmp','0x62ebc0')]
 for pc,m,a in bank_ops:P.need(y,pc,m,a)
 if y[0x186613]['memory'][0]['rip_target']!='0x1f7f5b8' or x[0x60a8ce]['memory'][0]['role']!='w':raise ValueError('actual current-context or frame-store role changed')
 # Local symbolic offsets: no numerical runtime stack address is needed.
 block_bias=0x70;frame_base=-0x50;data_store=-0x40
 if block_bias-0x60!=0x10 or block_bias-0x68!=8 or data_store-frame_base!=0x10:raise ValueError('callback frame offset derivation failed')
 receipts=list(dict.fromkeys([status.name,stdout.name,stderr.name,producer.name,bank_result.name,old.name,'check-render-executor-consumption.py','capture-render-executor-consumption.py']+[p['path'] for p in b['required_invocation_receipts']]))
 result=dict(status='PRODUCER_CHECKED_ORIGINAL_BANK_CALLBACK_FRAME_INDEPENDENT_PENDING',producer_complete=True,method='A RETAINED STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=annotations,required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in receipts],
  original_dispatch=dict(opcode=47,arm=arm,target=hex(target),labels_hex=labels.hex(),targets_hex=targets.hex()),instruction_pins=[dict(pc=hex(pc),mnemonic=m,args=a) for pc,m,a in ops+bank_ops],
  composition=dict(command_bytes=128,command_callback_offset=8,command_data_offset=16,frame_bytes=24,frame_field0='executor R14',frame_field8='pointer to executor stack slot rsp+50',frame_field16='QWORD from command+10',callback_input='temporary stack frame at rbp-50, not raw command',bank_read='lowDWORD frame+10, zero-extendedEDX',context_read='CURRENT global1F7F5B8 at callback execution',next_bank_read=False,normal_callback_return='60A8D9 then jump to128B cursor advance'),
  established=['If the verified interpreter reaches opcode2F on a valid original command record and optional60B750 returns normally, it reads callback from raw command+8 but passes a synthesized24B stack frame. Raw command+10 is copied into frame+10. It does not pass the raw opcode record.',
   'Composed with original185A50/5FEA50/186610, the callback selects the bank captured before submission, not the then-current global1F7F590 bank. The DWORD read discards any high bits; submission R8D zero-extends the bank. Context1F7F5B8 is instead freshly loaded by186610. Bank and context therefore have different read times.',
   'After186610/keyed consumer returns normally, the interpreter continues at60A8D9 and advances source and biased record cursors by128B before the next equality test. This local source order is not actual process timing, synchronous completion with the submitting caller or frame frequency.',
   'Earlier raw-command-address hypothesis is refuted for this shipped opcode2F branch. New bank-dispatch packet correctly left ABI unproved; this additive retained-data composition supplies that missing local connection without recapture, native calls or gameplay. The old BG11 request remains already retired, not counted again.'],
  assumptions=['Execution reaches the verified opcode2F branch with a valid stable unmodified record and normally returning optional helper/callback; native Windows x64 ABI preserves nonvolatileRBX/RBP/R14 and stack storage',
   'Original context/key/bank storage valid for the selected operation; natural initialization and complete queue publication/protocol remain independent'],
  limitations=['No fresh native/emulated/live execution or observed thread/event hit; no claim all interpreter paths/exception paths or normal game caller reachability proved',
   'Optional60B750 effects, record mutation/reentry/concurrency and runtime stack-frame lifetime beyond normal callback remain unproved; frame is transient and not a portable persistent object',
   'The context pointer may differ from submission-time state because the callback rereads it; no equality/lifetime/stability guarantee. Unconditional all-bank cancellation, counter38 meaning/writers/drain and native graphics effects remain OPEN',
   'No new wholeOV or historicalRT request closure, native experiment or external review run count; canonical BG11 is reused and scoped independent consumption remains pending'],
  affected_claims=['Existing OPUS bank-dispatch consumer: distinguish128B command from24B transient callback frame; queued bank versus current context ABI',
   'Existing FABLE bank-dispatch consumer: submission/global bank advance does not choose later callback bank; initialized scheduling/lifetime still open'],
  next_discriminator='Selected original submitting caller/flush/drain ordering and element38 writer closure if still unowned/required, before real-process scheduling. Existing BG11 consumer source is sufficient for this local callback ABI.',
  checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
  cleanup='Read-only shipping/retained inputs and finite reducer, no game/PC/input/instrument/native/save/config/reference/peer-process mutation')
 out.open('x').write(json.dumps(result,indent=2)+'\n')
 print('Original temporary-frame composition proved: captured bank, current context; raw-record argument hypothesis refuted')

if __name__=='__main__':main()
