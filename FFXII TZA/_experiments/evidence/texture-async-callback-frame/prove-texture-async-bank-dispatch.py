"""Submission is a record write; local bank consumer is a later boundary.

Method A only. Opaque capacity/flush/allocator calls and the opcode2F interpreter
remain explicit dependencies; no reconstructed fixture proves their effects.
"""
import importlib.util, json, pathlib, sys

W=pathlib.Path(__file__).resolve().parent


def module(name,file):
    spec=importlib.util.spec_from_file_location(name,W/file)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


P=module('bank_dispatch_cfg','prove-title-queue-consumption.py')
S=module('bank_dispatch_roles','validate-title-source-annotations.py')
BODY=[('0x185a50','0x185a7d','dfa1a293fdfc1e98492916b79b3479fdfc32928bb8d51fabcba3b02e3c6d4a88'),
      ('0x5fea50','0x5feb21','d875fe2cc599597c3134165d5680324040fd39faa5cfb7b1728dc3cff05d5172'),
      ('0x62ebc0','0x62ec07','f98fcc9cc174a3f7a6952fabe21ca3ac893475ad19bcecf9e6d360702acc530a'),
      ('0x62ec07','0x62ec40','ff7f3241ac30a1d9fac75d1480cc2aefe8eb990fe7a5810ec9f82bd9eec4292a'),
      ('0x62ec40','0x62ec67','376703e051b0e37e389aecb5653bb9d88f0ff51bab6f8da94dbb740bc98316a2'),
      ('0x186610','0x18661f','89f1ea014898ea25e5107d42e83937bdfd92281abc6718fa6de4315ee306aaf0')]


def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [disposable source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    status=src/'texture-async-bank-dispatch-capture-01.status.json';v=json.loads(status.read_text())
    if v.get('exit')!=0 or v.get('driver_sha256')!=P.sha(src/'capture-texture-async-bank-dispatch.py'):raise ValueError('required bank dispatch capture invocation failed or incomplete')
    stdout=src/'texture-async-bank-dispatch-capture-01.stdout';stderr=src/'texture-async-bank-dispatch-capture-01.stderr'
    if not stdout.read_bytes().strip() or stderr.read_bytes().strip():raise ValueError('required bank dispatch capture output missing/failed')
    pins=[];raw,x=P.load(src,'texture-async-bank-dispatch-source-01.json',pins);annotations=S.validate(raw)
    if [(q['start'],q['end_exclusive'],q['sha256']) for q in raw['ranges']]!=BODY:raise ValueError('required bank dispatch shipping identity changed')
    expected_pd=[[0x185a50,0x185a7d,0x1d52bc8],[0x5fea50,0x5feb21,0x1d52a90],[0x62ebc0,0x62ec07,0x1d8e1e4],[0x62ec07,0x62ec40,0x1daa2d0],[0x62ec40,0x62ec67,0x1daa2e4]]
    if raw.get('pdata_entries')!=expected_pd or len(raw.get('chains',[]))!=2:raise ValueError('required full bank consumer normal extents missing')
    if any(q.get('parent')!=expected_pd[2] or q.get('parent_raw')!='c0eb500007ec5000e4e1c601' for q in raw['chains']):raise ValueError('required bank consumer parent triple changed')
    if raw.get('leaf')!={'start':'0x186610','end_exclusive':'0x18661f','padding':'cc'}:raise ValueError('required callback leaf boundary changed')
    cfgs=[P.closed(x,a,z) for a,z in [(0x185a50,0x185a7d),(0x5fea50,0x5feb21),(0x62ebc0,0x62ec67)]]
    calls=[[dict(pc='0x185a62',target='0x5fea50')],
           [dict(pc='0x5fea86',target='0x600b30'),dict(pc='0x5fea95',target='qword ptr [rax + 0x10]')],
           [dict(pc='0x62ebec',target='qword ptr [rax]'),dict(pc='0x62ebf1',target='0x16d6d0'),dict(pc='0x62ec16',target='0x220390'),dict(pc='0x62ec30',target='qword ptr [rax + 0x18]')]]
    if [q['calls'] for q in cfgs]!=calls:raise ValueError('original bank dispatch call boundaries changed')
    operations=[
        (0x185a54,'mov','r8d, dword ptr [rip + 0x1df9b35]'),(0x185a5b,'lea','rdx, [rip + 0xbae]'),
        (0x185a67,'mov','eax, dword ptr [rip + 0x1df9b23]'),(0x185a6d,'inc','eax'),
        (0x185a6f,'and','eax, 3'),(0x185a72,'mov','dword ptr [rip + 0x1df9b18], eax'),
        (0x5fea5f,'mov','rsi, r8'),(0x5fea62,'mov','rdi, rdx'),(0x5fea65,'mov','rbx, rcx'),
        (0x5fea68,'test','rdx, rdx'),(0x5fea6b,'jne','0x5fea80'),(0x5fea6d,'lea','eax, [rdx + 1]'),
        (0x5fea80,'xor','edx, edx'),(0x5fea82,'lea','r8d, [rdx + 1]'),
        (0x5fea8b,'test','al, al'),(0x5fea8d,'jne','0x5fea98'),
        (0x5fea98,'mov','rax, qword ptr [rbx + 0x60]'),(0x5fea9c,'mov','r8, qword ptr [rbx + 0x58]'),
        (0x5feaa0,'lea','rdx, [rax + 0x80]'),(0x5feaaa,'jbe','0x5feab7'),
        (0x5feaac,'mov','rax, qword ptr [rbx + 0x50]'),(0x5feab0,'lea','rdx, [rax + 0x80]'),
        (0x5feab7,'xor','ecx, ecx'),(0x5feab9,'cmp','rdx, r8'),(0x5feabc,'ja','0x5feac4'),
        (0x5feabe,'mov','rcx, rax'),(0x5feac1,'mov','rax, rdx'),
        (0x5feac4,'mov','qword ptr [rbx + 0x60], rax'),(0x5feac8,'test','rcx, rcx'),(0x5feacb,'je','0x5feb0c'),
        (0x5feacd,'cmp','qword ptr [rbx + 0x88], 0'),(0x5fead5,'jne','0x5feade'),
        (0x5fead7,'mov','qword ptr [rbx + 0x88], rcx'),(0x5feade,'lea','rax, [rcx + 0x80]'),
        (0x5feae5,'mov','qword ptr [rbx + 0x90], rax'),(0x5feaec,'xor','eax, eax'),
        (0x5feaee,'mov','dword ptr [rcx], 0x2f'),(0x5feaf4,'mov','qword ptr [rcx + 8], rdi'),
        (0x5feaf8,'mov','qword ptr [rcx + 0x10], rsi'),(0x5feb11,'mov','eax, 0xd'),
        (0x186610,'mov','edx, dword ptr [rcx + 0x10]'),(0x186613,'mov','rcx, qword ptr [rip + 0x1df8f9e]'),
        (0x18661a,'jmp','0x62ebc0'),(0x62ebcf,'mov','eax, edx'),(0x62ebd1,'imul','rsi, rax, 0x38'),
        (0x62ebd5,'add','rsi, rcx'),(0x62ebd8,'mov','rbx, qword ptr [rsi + 0x10]'),
        (0x62ebdc,'lea','rdi, [rsi + 8]'),(0x62ebe0,'cmp','rbx, rdi'),(0x62ebe3,'je','0x62ebfe'),
        (0x62ebe5,'mov','rcx, qword ptr [rbx + 0x20]'),(0x62ebe9,'mov','rax, qword ptr [rcx]'),
        (0x62ebee,'mov','rcx, rbx'),(0x62ebf6,'mov','rbx, rax'),(0x62ebf9,'cmp','rax, rdi'),
        (0x62ebfc,'jne','0x62ebe5'),(0x62ebfe,'mov','rdi, qword ptr [rsi + 0x18]'),
        (0x62ec10,'mov','rdx, qword ptr [rdi]'),(0x62ec13,'mov','rcx, rsi'),
        (0x62ec1b,'mov','rax, qword ptr [rsi + 0x30]'),(0x62ec1f,'lea','rcx, [rsi + 0x30]'),
        (0x62ec23,'mov','rbx, qword ptr [rdi + 8]'),(0x62ec27,'mov','r8d, 0x28'),
        (0x62ec2d,'mov','rdx, rdi'),(0x62ec33,'mov','rdi, rbx'),(0x62ec39,'jne','0x62ec10'),
        (0x62ec45,'lea','rax, [rsi + 8]'),(0x62ec49,'mov','qword ptr [rsi + 0x10], rax'),
        (0x62ec4d,'mov','qword ptr [rax], rax'),(0x62ec52,'mov','qword ptr [rsi + 0x18], rax'),
        (0x62ec56,'mov','byte ptr [rsi + 0x20], al'),(0x62ec59,'mov','dword ptr [rsi + 0x28], eax')]
    for pc,m,a in operations:P.need(x,pc,m,a)
    if [x[p]['memory'][0]['rip_target'] for p in (0x185a54,0x185a67,0x185a72)]!=['0x1f7f590']*3 or x[0x185a5b]['memory'][0]['rip_target']!='0x186610' or x[0x186613]['memory'][0]['rip_target']!='0x1f7f5b8':raise ValueError('original bank/callback globals changed')
    if x[0x5feaee]['memory'][0]['role']!='w' or x[0x185a72]['memory'][0]['role']!='w':raise ValueError('actual command/global store role changed')
    cycles=[dict(initial=i,normal_unchanged_call_banks=[(i+n)&3 for n in range(4)],next_after4=i) for i in range(4)]
    if any(len(set(q['normal_unchanged_call_banks']))!=4 for q in cycles):raise ValueError('bank low-bit invariant derivation failed')
    result=dict(status='PRODUCER_CHECKED_BANK_SUBMISSION_AND_CONSUMER_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,
                source_pins=pins,annotation_prerequisite=annotations,normal_cfgs=cfgs,
                required_invocation_receipts=[dict(path=q.name,sha256=P.sha(q)) for q in (status,stdout,stderr,src/'capture-texture-async-bank-dispatch.py')],
                instruction_pins=[dict(pc=hex(pc),mnemonic=m,args=a) for pc,m,a in operations],low_bit_invariant=cycles,
                record=dict(bytes=128,opcode_dword='0x2f',callback_qword_offset=8,userdata_qword_offset=16),
                established=[
                    '185A50 passes the pre-call DWORD bank in zero-extendedR8D and callback186610 to5FEA50. After normal return it rereads global bank, overwrites the callee result, INC32/AND3/stores and returns that new low-two-bit value inEAX. It never tests submission success. Four unchanged/no-interference invocations rotate all4 residues; invocations are not frames.',
                    'NonNULL callback submission saves incoming callback/data, calls600B30(EDX0,R8D1) and conditionally context vslot10 if AL0. After those opaque boundaries it attempts one128B reservation, optionally wraps from cursor to begin under unsigned bounds, then updates cursor. Valid nonNULL reservation publishes first-batch begin if unset/end and writes opcode2F, callback+8 and userdata+10 before returning0. No direct call of the submitted pointer appears in this body.',
                    'NULL callback returns1 before those calls/record writes. Failed/nonNULL reservation returns0D without writing the command payload. A bank advance after normal submission return therefore does not establish a successful command record, much less callback execution. Post-opaque empty-buffer error case is conditional, not natural allocation-failure evidence.',
                    '186610 parses DWORD[its input+10], loads the CURRENT global1F7F5B8 context and tails62EBC0. If an opcode2F interpreter invokes it with the recorded command address, it receives the stored bank value; the interpreter ABI/reachability is not established here. The context pointer is not saved by185A50 in that command.',
                    '62EBC0 selects context+56*zeroextend32(EDX), begins at bank+10 and compares to sentinel bank+8. Each key at node+20 is called through its virtual slot0 before16D6D0 computes the next node. Unlike the distinct186230 pair queue, this uses a post-callback live tree successor, not a captured write-cursor snapshot.',
                    'After the key loop returns normally, it rereads root bank+18. Nonempty cleanup calls220390 for one subtree and allocator slot18 on the current28B node while following its+8 link. At normal exit it resets begin/sentinel links/root/color/count28. Opaque subtree/allocator effects and callback mutation remain limits. Resetting container count is not proof of GPU completion or element38 counter/drain state.',
                ],
                conditional_failure=dict(boundary='post600B30/optional vslot10 returns',begin=0,cursor=0,capacity_end=0,
                                         source_result=13,command_payload_written=False,wrapper_bank_advance=True,
                                         limits='Conditional post-boundary state, no stub/native failure or natural reachability assertion'),
                assumptions=['Valid nonwrapping128B command-buffer bounds/storage and ABI-preserving normally returning opaque calls',
                             'Stable finite ordered tree/iterator/sentinel/node/key storage and normally returning callbacks for ordinary traversal; no callback mutation/reentry safety implied',
                             'Bank/context stability through relevant reads for the ordinary4-cycle formula; other statements distinguish pre/post reads explicitly'],
                limitations=['Actual opcode2F interpreter target and record-address ABI/normal reachability remain unproved; compatible stored shape is not an executed dispatch',
                             '600B30/context vslot10/220390/allocator/native callback effects and scheduling are not executed or certified; no absolute transitive callback absence',
                             'No actual initialized context/tree/bank or buffer success, thread/order/timing, natural wrong-bank pending update, writer closure, counter38 meaning or lifetime/race/presentation guarantee',
                             'No all global/caller census from the candidate retool view; distinct1F7F598/186230 title queue is not substituted for keyed1F7F5B8'],
                affected_claims=['OPUS exact128B opcode2F record and callback/bank return ABI, container versus element counters',
                                 'FABLE bank rotation submission versus execution and live-tree traversal/lifetime preconditions'],
                next_discriminator='Primary opcode2F interpreter branch/actual callback argument, then capacity/native state and bank/element-counter writers if still required/unowned. No interactive setup justified by the local source.',
                checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
                cleanup='Read-only retained shipping source plus finite reducer; no PC/game/input/native/instrument/save/config/reference or peer-process mutation')
    out.open('x').write(json.dumps(result,indent=2)+'\n')
    print('Original command record, status-independent bank advance and local keyed consumer proved; opcode interpreter/native timing OPEN')


if __name__=='__main__':main()
