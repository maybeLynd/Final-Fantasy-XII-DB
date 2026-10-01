"""Bounded candidate-writer ordering, ABI and local writes; Method A only."""
import importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('normal_source','prove-title-queue-consumption.py')
S=module('actual_annotations','validate-title-source-annotations.py')
def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [source directory]')
    out=pathlib.Path(sys.argv[1]);source=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    pins=[];raw,x=P.load(source,'title-reset-order-source-01.json',pins);agreement=S.validate(raw)
    expected={
        '0x611f80':('0x611fe2','a809343e44cdce79c5da7b79dc989fcd1e5dc35f325af82a658a63e996f724f6'),
        '0x5de290':('0x5de2cf','bd2cc11a35e690587644cee488b29ce118adedc5f90a8bf36ba7a3cdd46b3314')}
    if len(raw['ranges'])!=2 or any(q['start'] not in expected or (q['end_exclusive'],q['sha256'])!=expected[q['start']] for q in raw['ranges']):raise ValueError('wrong/incomplete original body')
    if raw.get('pdata_entries')!=[[0x611F80,0x611FE2,0x1DA8660],[0x5DE290,0x5DE2CF,0x1D9FE28]]:raise ValueError('wrong named root metadata')
    g=P.closed(x,0x611F80,0x611FE2);tail=P.closed(x,0x5DE290,0x5DE2CF)
    if g['calls']!=[dict(pc=hex(p),target=hex(t)) for p,t in [(0x611F95,0x62B100),(0x611F9D,0x62BCB0),(0x611FC3,0x584730),(0x611FD4,0x5DE290)]] or g['returns']!=['0x611fe1']:raise ValueError('reset call/return closure changed')
    if tail['calls']!=[dict(pc=hex(p),target=hex(t)) for p,t in [(0x5DE2B4,0x5CDAA0),(0x5DE2C3,0x6108C0)]] or tail['returns']!=['0x5de2ce']:raise ValueError('tail call/return closure changed')
    for p,m,a in [
        (0x611F8F,'mov','rbx, rdx'),(0x611F92,'mov','rcx, rdx'),(0x611F95,'call','0x62b100'),
        (0x611F9A,'mov','rcx, rbx'),(0x611F9D,'call','0x62bcb0'),
        (0x611FA3,'mov','ecx, dword ptr [rbx + 0x30]'),(0x611FA6,'mov','eax, ecx'),
        (0x611FA8,'shr','eax, 0x1f'),(0x611FAB,'not','al'),(0x611FAD,'test','al, 1'),(0x611FAF,'je','0x611fc8'),
        (0x611FB1,'btr','ecx, 0x1f'),(0x611FB5,'cmp','ecx, 1'),(0x611FB8,'jbe','0x611fc8'),
        (0x611FBA,'mov','rcx, qword ptr [rbx + 0x38]'),(0x611FBE,'test','rcx, rcx'),(0x611FC1,'je','0x611fc8'),
        (0x611FC8,'xor','eax, eax'),(0x611FCA,'mov','qword ptr [rbx + 0x38], rax'),
        (0x611FCE,'mov','dword ptr [rbx + 0x30], eax'),(0x611FD1,'mov','rcx, rbx'),
        (0x611FDA,'mov','al, 1'),
        (0x5DE29F,'mov','rbx, rcx'),(0x5DE2A2,'cmp','byte ptr [rcx + 8], 0'),(0x5DE2A6,'je','0x5de2ba'),
        (0x5DE2AF,'mov','ecx, 3'),(0x5DE2BA,'mov','rcx, qword ptr [rbx + 0x20]'),
        (0x5DE2BE,'test','rcx, rcx'),(0x5DE2C1,'je','0x5de2c9')]:P.need(x,p,m,a)
    writes=[hex(p) for p,i in sorted(x.items()) if any(m['role'] in ('w','rw') and m['base'] not in ('rsp','rbp') for m in i['memory'])]
    if writes!=['0x611fca','0x611fce']:raise ValueError('unchecked local nonstack write')
    if any(i['mnemonic'].startswith('j') for p,i in x.items() if 0x611F80<=p<0x611F95):raise ValueError('first cleanup no longer unconditional')
    result=dict(status='PRODUCER_CHECKED_RESET_ORDER_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=agreement,normal_cfgs=[g,tail],
        checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),
        question='Does611F80 establish valid count/storage before62B100, and does5DE290 locally repair the cleared count?',
        competing_hypotheses=['Candidate establishes count>=1 before cleanup','Candidate cleans incoming object first and clears state afterward'],
        established=[
            '611F80 takes its object from RDX, copies it to RBX and RCX, and unconditionally calls62B100 before62BCB0, release testing or any local object write. Incoming RCX is not the object source in this entry. It provides no local count>=1 normalization or zero-count skip before the established first-access precondition.',
            'After both cleanup calls return normally, it reads current count+30; direct584730 is selected only when bit31clear, masked n>1, and pointer+38nonNULL. Thus the predicate uses state after cleanup, not necessarily the entry count. Opaque cleanup/free side effects remain unproved.',
            'All local normal paths converge at XOR EAX,EAX, QWORD[RBX+38]=0 then DWORD[RBX+30]=0, immediately passing the original object in RCX to5DE290. There is no local count-one initializer. This clears state before that call, not necessarily after its transitive effects.',
            '611F80 writes AL=1 after5DE290 returns and returns normally. Only the low byte is established; upper return bits and native error/exception propagation are not a Boolean32 result guarantee.',
            '5DE290 has no local nonstack writes: it conditionally calls5CDAA0 with ECX3 when byte[object+8] is nonzero, then conditionally calls6108C0 with pointer[object+20]. It does not locally establish count>=1 or change count+30. Callee effects/aliasing could change state and are outside this local result.',
            'The candidate-writer hypothesis therefore does not discharge the valid incoming count/storage obligation. Actual constructors, count writers and callers of cleanup remain the next static discriminator; neither natural empty-state reachability nor a game crash is proved.'
        ],
        assumptions=['ABI-correct backed object and normally returning calls preserving nonvolatile RBX','Local operations only; no implicit stack/object alias or concurrent writes'],
        limitations=['No initialized game state, actual constructor/caller census or lifetime/reuse proof','No5CCB80/62B870/584730/5CDAA0/6108C0 native effects or allocator/ownership meaning','No forced native call, emulator or live observation; zero-count natural reachability remains OPEN','No safe repeated-cleanup/idempotence guarantee'],
        affected_claims=['FABLE title cleanup valid count/storage and reset ordering','OPUS callback RDX object argument/AL return and count field contracts'],
        next_discriminator='Find actual constructors/count writers and normal callers that provide n>=1, rather than naming this cleanup entry an initializer.',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
        cleanup='Bounded original file reads and synchronous helpers only; no process/game/input/instrument/save/config/reference writes')
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print('Candidate cleanup precedes state clear; RDX/AL ABI and local tail writes qualified. Initialization OPEN')
if __name__=='__main__':main()
