"""Local prepare/submit routing; no native effects or natural-state claim."""
import importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
 s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('proof','prove-title-queue-consumption.py');S=module('annotations','validate-title-source-annotations.py')

def closed_tail(ix,a,z,tail,args):
 todo=[a];seen=set();calls=[]
 while todo:
  pc=todo.pop()
  if pc in seen:continue
  if pc not in ix or not a<=pc<z:raise ValueError('unclosed known-tail CFG')
  seen.add(pc);i=ix[pc];m=i['mnemonic'];n=pc+len(bytes.fromhex(i['bytes']))
  if pc==tail:
   if m!='jmp' or i['args']!=args:raise ValueError('known external tail changed')
   continue
  if m=='ret':continue
  if m=='jmp':todo.append(int(i['args'],16));continue
  if m.startswith('j'):todo.append(int(i['args'],16))
  if m=='call':calls.append(dict(pc=hex(pc),target=i['args']))
  todo.append(n)
 if seen!={pc for pc in ix if a<=pc<z}:raise ValueError('unchecked normal source')
 return dict(entry=hex(a),end_exclusive=hex(z),instructions=len(seen),calls=calls,tail=dict(pc=hex(tail),target=args))

def main():
 if len(sys.argv)!=4:raise ValueError('source_directory capture_status fresh_result')
 src,st,out=map(pathlib.Path,sys.argv[1:])
 if out.exists():raise ValueError('immutable result exists')
 status=json.loads(st.read_text());name='renderer-init-command-routing-source-02.json'
 if status.get('exit')!=0:raise ValueError('upstream capture failed or missing exit')
 if status.get('source_name')!=name or status.get('source_sha256')!=P.sha(src/name) or status.get('driver_sha256')!=P.sha(src/'capture-renderer-init-command-routing.py'):
  raise ValueError('capture source/driver receipt prerequisite')
 pins=[];raw,ix=P.load(src,name,pins);ann=S.validate(raw)
 if raw.get('invocation_driver_sha256')!=status['driver_sha256']:raise ValueError('source invocation moved')
 expected={'0x1f16c0':('0x1f1733','23ed9dbe9ddfef706b965b95ef6bed847451af4235ee6ff3b2c1cf505be27610'),
  '0x1fb840':('0x1fb86b','b17914307d1e9114e81532083a3e6d654ec47aedbc0985beb0964a234363131b'),
  '0x1a1850':('0x1a1920','d56dcbcdfa225d3d2a3b080bb9906afadc3f1c6eec9312a685af554fb2a218ae'),
  '0x1fb830':('0x1fb83f','0d27a6d9e1d379dc423bd7be9aa2c7b4a4f779052ad58383a08611c1245d07b1'),
  '0x16d6a0':('0x16d6a3','b6cbececf1b07e74f37d57710c68c31f0b92cb08d51093252b321b07542e177b')}
 for pc,m,a in [(0x1f16ca,'mov','rdi, rcx'),(0x1f16cd,'mov','rbx, rdx'),
  (0x1f16d0,'mov','ecx, 1'),(0x1f16d5,'call','0x16d6a0'),(0x1f16e1,'mov','edx, 0x18'),
  (0x1f16e6,'call','0x1a1470'),(0x1f16eb,'test','rax, rax'),(0x1f16ee,'je','0x1f16ff'),
  (0x1f16f0,'lea','rcx, [rip + 0x711831]'),(0x1f16f7,'mov','r8, rax'),
  (0x1f16fa,'mov','qword ptr [rax], rcx'),(0x1f16ff,'xor','r8d, r8d'),
  (0x1f1702,'mov','qword ptr [rip + 0x1d917af], rax'),
  (0x1f1710,'mov','qword ptr [r8 + 8], rdi'),(0x1f1714,'mov','qword ptr [r8 + 0x10], rbx'),
  (0x1f1709,'lea','rcx, [rip + 0x1d917a0]'),(0x1f1718,'call','0x1fb840'),
  (0x1f171d,'lea','rcx, [rip + 0x1d9178c]'),
  (0x1fb846,'mov','rdx, qword ptr [rcx + 8]'),(0x1fb84a,'mov','rbx, rcx'),
  (0x1fb854,'call','0x16d6a0'),(0x1fb859,'mov','rcx, qword ptr [rbx + 8]'),
  (0x1fb85d,'mov','qword ptr [rbx], rcx'),(0x1fb860,'mov','rax, qword ptr [rcx]'),
  (0x16d6a0,'ret','0'),(0x1fb830,'mov','rdx, qword ptr [rcx]'),
  (0x1fb833,'mov','rcx, qword ptr [rip + 0x1d83c96]'),
  (0x1a1869,'mov','rsi, rdx'),(0x1a186c,'mov','rbx, rcx'),(0x1a186f,'call','0x189120'),
  (0x1a1874,'test','rax, rax'),(0x1a1877,'je','0x1a18e0'),(0x1a1879,'mov','edx, 0x28'),
  (0x1a1885,'call','0x1a1470'),(0x1a188a,'mov','rbx, rax'),
  (0x1a18ae,'mov','rdx, rsi'),(0x1a18b1,'mov','rcx, rbx'),(0x1a18b4,'call','0x1f4950'),
  (0x1a18b9,'mov','rdi, rax'),(0x1a18cb,'call','0x189120'),
  (0x1a18d0,'mov','r8, qword ptr [rdi]'),(0x1a18d3,'mov','rdx, qword ptr [rax + 8]'),
  (0x1a18d7,'mov','rcx, rdi'),(0x1a18da,'call','qword ptr [r8 + 8]'),
  (0x1a18fe,'mov','rcx, qword ptr [rbx + 8]'),(0x1a1902,'mov','rax, qword ptr [rcx]'),
  (0x1a1905,'mov','r8d, 0x40'),(0x1a190b,'mov','rdx, rsi'),(0x1a190e,'call','qword ptr [rax]')]:P.need(ix,pc,m,a)
 if len(raw['ranges'])!=5 or any((q['end_exclusive'],q['sha256'])!=expected.get(q['start']) for q in raw['ranges']):raise ValueError('original full-body prerequisite changed')
 if raw.get('pdata_entries')!=[[0x1f16c0,0x1f1733,0x1d6b7c8],[0x1fb840,0x1fb86b,0x1d529d0],[0x1a1850,0x1a1920,0x1d57588]]:raise ValueError('normal root extent changed')
 table=raw.get('physical_table',{})
 # Explicit byte/table checks; no inferred slots beyond the two bound entries.
 import hashlib
 if table!=dict(address='0x902f28',bytes='a0d6160000000000a0161f0000000000',sha256=hashlib.sha256(bytes.fromhex('a0d6160000000000a0161f0000000000')).hexdigest(),slots=['0x16d6a0','0x1f16a0']):raise ValueError('physical prepare-slot identity changed')
 for pc,a in [(0x1f16f0,0x902f28),(0x1f1702,0x1f82eb8),(0x1f1709,0x1f82eb0),(0x1f171d,0x1f82eb0),(0x1fb833,0x1f7f4d0)]:
  if ix[pc]['memory'][0]['rip_target']!=hex(a):raise ValueError('bound node/table/target changed')
 cfg=[closed_tail(ix,0x1f16c0,0x1f1733,0x1f172e,'0x1fb830'),
      closed_tail(ix,0x1fb840,0x1fb86b,0x1fb868,'qword ptr [rax]'),
      closed_tail(ix,0x1fb830,0x1fb83f,0x1fb83a,'0x1a1850'),P.closed(ix,0x1a1850,0x1a1920),P.closed(ix,0x16d6a0,0x16d6a3)]
 prior,pi=P.load(src,'renderer-queue-initialization-source-02.json',pins);priorann=S.validate(prior)
 init_hashes={'0x189000':'59e677af8cc3bfd61ce22db0c0ddf022dd8cde0003c182a5a498cd8cf407818e','0x184f20':'951ae5de70606c756ae21acb1d07fac4e0257a1af3940d20deb858b96afda816','0x186cd0':'5d6e8834d9060c51779ef3246fa76dd0b632e60ec977ee829a941b313cd88b17'}
 if any(not any(q['start']==a and q['sha256']==h for q in prior['ranges']) for a,h in init_hashes.items()):raise ValueError('retained initializer identity changed')
 getter,gi=P.load(src,'title-cleanup-callback-queue-source-01.json',pins);getterann=S.validate(getter)
 q=next((q for q in getter['ranges'] if q['start']=='0x189120'),None)
 if q is None or q['end_exclusive']!='0x189128' or q['sha256']!='b02fbb2973e16dbb84c98a083df86088e8bf9ed44f9acb18380d73344cdd193e':raise ValueError('retained getter prerequisite incomplete')
 P.need(gi,0x189120,'mov','rax, qword ptr [rip + 0x1df6471]');P.need(gi,0x189127,'ret','')
 if gi[0x189120]['memory'][0]['rip_target']!='0x1f7f598':raise ValueError('wrong renderer getter')
 for pc,m,a in [(0x187153,'mov','rdx, qword ptr [rsi + 0xb58]'),(0x18715a,'mov','dword ptr [rsi + 0xcb8], r12d'),
  (0x187161,'mov','rcx, qword ptr [rsi + 0xb10]'),(0x187168,'call','0x1f16c0'),
  (0x189061,'call','0x184f20'),(0x189067,'mov','qword ptr [rip + 0x1df652a], rax')]:P.need(pi,pc,m,a)
 result=dict(status='PRODUCER_PROVED_CONDITIONAL_RENDERER_INIT_COMMAND_ROUTING_INDEPENDENT_PENDING',producer_complete=True,
  method='A original normal CFG/dataflow with retained sources; no execution',exe_sha256=P.SHA,source_pins=pins,
  annotation_prerequisites=[ann,priorann,getterann],normal_cfgs=cfg,checker_sha256=P.sha(pathlib.Path(__file__)),
  capture_receipt=dict(path=st.name,sha256=P.sha(st),exit=0),
  question='Which target/arguments does the post-index initializer command use on current-renderer null versus nonnull submission?',
  established=[
   '186CD0 writes CB8zero then calls1F16C0 with RCX=[renderer+B10],RDX=[renderer+B58]. These are loaded values, not the renderer receiver itself.',
   'Under valid normal arena allocation,1F16C0 builds a24B command902F28 with its original args at8/10, stages it atnode01F82EB0+8, calls1FB840, then tails1FB830.1FB840 promotesnode8->0 and tails command slot0. Physical slot0=16D6A0 is original3B RET0, not a synthetic stub; under unmodified identity it imposes no conditional gate or command-body effect.',
   '1FB830 passes live node0 asRDX and currentglobal01F7F4D0 asRCX to1A1850. That local submission first reads current renderer01F7F598 through189120. It does not inherit a renderer object argument from the initializer.',
   'If the first getter returnsnull, the local null branch retains original submission targetRBX, loads target+8 asRCX, commandRSI asRDX andR8D40, then calls target-receiver slot0 at1A190E. Immediate indirect dispatch is established; that opaque method need not execute the command or prove a GPU/native effect.',
   'If the first getter is nonnull, the other arm allocates28h, calls1F4950 with the command andR8D0, then calls returned wrapper slot8 usingRDX=[second getter result+8]. Valid normal construction/nonnull second getter are premises. Two getter reads are separate; no atomicity or stable equality is proved. Wrapper and downstream BG11 execution remain separately established evidence.',
   '189000 publishes the renderer only after184F20 normally returns. Thus IF no intervening opaque/interfering publication supplies the global before this post-index submission, the construction path selects the null-renderer branch. Publication order alone is not a universal natural null-state or final no-overwrite proof.'],
  normalized=dict(null_renderer_dispatch=dict(receiver='qword [incoming target+8]',command='incoming RDX retained inRSI',third_argument=64,slot_byte_offset=0),
   nonnull_renderer_dispatch=dict(receiver='1F4950 returned wrapper',second_argument='second189120 result+8 contents',slot_byte_offset=8),
   prepare=dict(vtable='0x902f28',slot0='0x16d6a0',original_bytes='c20000',effect='RET0 only')),
  refuted=['Unconditional same submission arm across renderer publication state','Original16D6A0 imposes an assertion/nonnull guard','First and second getter values are automatically one atomic snapshot'],
  assumptions=['Normal ABI/return and backed valid arena/command/node/target/wrapper/global objects','Unmodified command vtable and no intervening alias/mutation for composed node identity','No interfering global publication for conditional prepublication null-route statement'],
  unresolved=['Natural initialized state/caller scheduling and actual target/wrapper method effects','All global writers, alias/overwrite, allocator placement/failure, exception cleanup, lifetime and GPU consequences'],
  limitations=['Do not equate prepare, dispatch, accepted record, executed command and native consequence','Known prepare leaf is3B RET0; rejected01 one-byte RET guess produced no source. Raw failure and preimage preserved.','No new BG9/BG11/frame census; existing accepted/under-review evidence remains separate'],
  affected_claims=['FABLE renderer initialization/command lifecycle call boundaries','OPUS selected caller arguments, prepare and renderer-global-sensitive submission contracts'],
  native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
  cleanup='Reference reads and bounded synchronous scripts only; no PC/game/instrument/save/config/reference/peer mutation')
 out.write_text(json.dumps(result,indent=2)+'\n');print('PROVED conditional init-command preparation/dispatch ABI; natural execution/effects OPEN')
if __name__=='__main__':main()
