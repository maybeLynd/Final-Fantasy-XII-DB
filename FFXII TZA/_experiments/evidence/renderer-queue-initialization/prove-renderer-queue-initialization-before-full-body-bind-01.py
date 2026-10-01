"""Bound exact original renderer bank construction/reserve/publication protocol.
Normal ABI and no interference are premises, not live initialized-state proof.
"""
import hashlib, importlib.util, json, pathlib, sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('proof','prove-title-queue-consumption.py')
S=module('source','validate-title-source-annotations.py')
source,out=map(pathlib.Path,sys.argv[1:])
if out.exists():raise ValueError('immutable result exists')
pins=[];raw,ix=P.load(source.parent,source.name,pins)
annotation=S.validate(raw)
if len(raw.get('normal_chains',[]))!=5 or len(raw.get('ranges',[]))!=7:raise ValueError('normal extent/chain prerequisite incomplete')
cfgs=[P.closed(ix,int(q['start'],16),int(q['end_exclusive'],16)) for q in raw['ranges']]
def need(pc,m,a):P.need(ix,pc,m,a)
ops=[(0x18902a,'cmp','qword ptr [rip + 0x1df6566], 0'),(0x189032,'jne','0x18906e'),
 (0x189034,'mov','ecx, 0xdd8'),(0x189039,'call','0x210ec0'),(0x189046,'je','0x189067'),
 (0x18905e,'mov','rcx, rax'),(0x189061,'call','0x184f20'),
 (0x189067,'mov','qword ptr [rip + 0x1df652a], rax'),
 (0x184f40,'mov','rdi, rcx'),(0x184f54,'xor','esi, esi'),
 (0x184fc0,'lea','rcx, [rdi + 0xc38]'),(0x184fd3,'lea','r9, [rip - 0x32a]'),
 (0x184fda,'lea','edx, [rsi + 0x20]'),(0x184fdd,'lea','r8d, [rsi + 4]'),
 (0x184fe1,'call','0x808fe4'),(0x185053,'mov','rcx, rdi'),(0x185056,'call','0x186cd0'),
 (0x18505c,'mov','rax, rdi'),(0x184cb6,'xor','eax, eax'),
 (0x184cbf,'mov','qword ptr [rcx], rax'),(0x184cc5,'mov','qword ptr [rcx + 8], rax'),
 (0x184cc9,'mov','qword ptr [rcx + 0x10], rax'),(0x184ccd,'add','rcx, 0x18'),
 (0x184cd1,'call','0x1edf00'),(0x1edf00,'lea','rax, [rip + 0x714819]'),
 (0x1edf07,'mov','qword ptr [rcx], rax'),(0x809000,'mov','rsi, r9'),
 (0x809003,'mov','r15, r8'),(0x809006,'mov','r14, rdx'),(0x809009,'mov','rdi, rcx'),
 (0x80900c,'xor','ebx, ebx'),(0x809015,'cmp','rbx, r15'),(0x809018,'je','0x809039'),
 (0x809022,'mov','rcx, rdi'),(0x809025,'call','rsi'),(0x809027,'add','rdi, r14'),
 (0x80902f,'inc','rbx'),(0x809037,'jmp','0x809015'),
 (0x186cee,'xor','r12d, r12d'),(0x186cf1,'mov','rsi, rcx'),
 (0x18712e,'mov','ebx, r12d'),(0x187131,'movsxd','rax, ebx'),
 (0x187134,'lea','rcx, [rsi + 0xc38]'),(0x18713b,'shl','rax, 5'),
 (0x18713f,'mov','edx, 0x1388'),(0x187144,'add','rcx, rax'),(0x187147,'call','0x188640'),
 (0x18714c,'inc','ebx'),(0x18714e,'cmp','ebx, 4'),(0x187151,'jb','0x187131'),
 (0x18715a,'mov','dword ptr [rsi + 0xcb8], r12d'),
 (0x18865d,'mov','r14d, edx'),(0x188660,'sar','rax, 4'),(0x188664,'cmp','edx, eax'),
 (0x188666,'jbe','0x188710'),(0x188682,'add','rcx, 0x18'),(0x188686,'mov','edx, r14d'),
 (0x188689,'xor','r8d, r8d'),(0x18868c,'shl','rdx, 4'),
 (0x188690,'call','qword ptr [rax + 0x10]'),(0x1886e4,'call','qword ptr [r9 + 0x18]'),
 (0x1886f3,'mov','qword ptr [rdi], rbp'),(0x1886f9,'mov','qword ptr [rdi + 8], rax'),
 (0x188700,'shl','rax, 4'),(0x18870c,'mov','qword ptr [rdi + 0x10], rax')]
for pc,m,a in ops:need(pc,m,a)
for pc,target in [(0x184fd3,'0x184cb0'),(0x1edf00,'0x902720'),(0x189067,'0x1f7f598')]:
    if ix[pc]['memory'][0]['rip_target']!=target:raise ValueError('constructor/global binding changed')
# All explicit replacements in these complete local bodies, not a prefix scan.
def replacements(a,b,names):
    return [(pc,i['mnemonic'],i['args']) for pc,i in ix.items() if a<=pc<b and
        (i['args'].split(',')[0] in names and i['mnemonic'] not in {'cmp','test','push'} )]
if replacements(0x186cd0,0x187198,{'r12','r12d','r12w','r12b'})!=[(0x186cee,'xor','r12d, r12d')]:raise ValueError('index-zero source changed')
if replacements(0x184f20,0x185064,{'rsi','esi','si','sil'})!=[(0x184f54,'xor','esi, esi')]:raise ValueError('bank count/stride source changed')
if replacements(0x186cd0,0x187198,{'rsi','esi','si','sil'})!=[(0x186cf1,'mov','rsi, rcx')]:raise ValueError('same renderer receiver changed')
result=dict(status='PRODUCER_PROVED_LOCAL_RENDERER_QUEUE_INITIALIZATION_INDEPENDENT_PENDING',producer_complete=True,
 method='A original instruction/dataflow/normal CFG proof; no native or game execution',exe_sha256=raw['exe_sha256'],source_pins=pins,
 annotation_prerequisite=annotation,normal_cfgs=cfgs,checker_sha256=P.sha(pathlib.Path(__file__)),
 question='What protocol constructs/reserves the same four callback banks and writes their rotation index before the renderer singleton is published?',
 established=[
 '184F20 passes same receiver+C38, stride32/count4/callback184CB0 to808FE4. Under normal ABI/return, the actual iterator calls that constructor at offsetsC38,C58,C78,C98; these are four algebraic iterations, not four native tests.',
 'Each184CB0 zeroes bank begin/current/end at0/8/10 and invokes1EDF00 at bank+18; shipping1EDF00 writes vtable902720. These are immediate original stores, not a live pointer/default sample.',
 '186CD0 preserves receiver inRSI and zero inR12. Its normal loop supplies each same bank to188640 withEDX5000, then writesDWORDreceiver+CB8=0 at18715A. No other explicit R12/RSI replacement precedes that store; normal ABI/non-interference and returning calls are premises.',
 '188640 capacity gate compares desired count with low32((end-begin)>>4). On the allocation arm it passes desiredCount*16 bytes andR8D0 to allocator-record+18 slot10. For5000 that is80000B per reached allocation request, not5000bytes. Slots/callback allocation/free effects remain opaque.',
 '188640 publishes begin/new-current/end after copy and optional old-block slot18 call. With unchanged initially empty bank and successful backed allocation, current remainsbegin and end=begin+80000. No allocation-success test certifies valid memory or actual allocation placement.',
 '189000 skips construction when global01F7F598 is nonnull. When null, it allocatesDD8; if allocation isnull it storesnull without the constructor. Otherwise184F20 normally returns its receiver and the caller stores returnedRAX to the global after construction. This is conditional order, not live initialization success/stability.'],
 assumptions=['Normal Win64 ABI preserves nonvolatile receiver/index registers; normal return from guard/constructors/allocator/helpers',
 'Correct backed receiver/storage and no interfering or aliased writes for composed initial-empty/successful-capacity statement',
 'The post-index1F16C0 call and earlier opaque helpers may have effects; no transitive no-overwrite guarantee is inferred'],
 limitations=['Not actual initialized process state, allocator placement, successful reserve, exception cleanup, all global writers or lifetime proof',
 'No frame/thread/delivery schedule or natural pending-title teardown proof; four banks/iterations are not four frames',
 'Written index0/zero cursors are point effects, not universal portable defaults or a final-state guarantee across opaque calls',
 'No arbitrary malformed pointer/index/capacity safety and no native intervention'],
 affected_claims=['FABLE queued title/native resource cleanup initialization preconditions','OPUS renderer+C38/CB8 layout, reserve16-byte element units and constructor/publication contract'],
 next_discriminator='Read allocator902720 slots and any actual caller/alias/interference obligation before asserting successful native initialization; reuse this protocol rather than live-sampling instruction constants.',
 native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
 cleanup='Offline original reads/synchronous helpers only; no game/PC/instrument/save/config/reference/peer mutation')
out.write_text(json.dumps(result,indent=2)+'\n')
print('PROVED bounded bank construction/reserve/index/publication protocol; initialized-process and opaque effects OPEN')
