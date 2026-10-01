"""Original2D admission/callback boundary and exact200B copy, Method A.

Existing accepted constructor/destructor interpretation is reused, not recounted
as our tests. This reducer derives the previously unassigned copy extent and
narrows the pending-counter search. Opaque callees are explicitly not executed.
"""
import importlib.util,json,pathlib,sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('retained_normal','prove-title-queue-consumption.py')
S=module('actual_annotations','validate-title-source-annotations.py')
def main():
    if len(sys.argv) not in (2,3):raise ValueError('fresh result [source directory]')
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    pins=[];raw,x=P.load(src,'texture-async-count-path-source-01.json',pins);agreement=S.validate(raw)
    spans={
        '0x6160b0':('0x61613b','f0d2a7fb3844a74434beebc10525b71c0d5248377daed3d60efa92571f9cda6e'),
        '0x62c360':('0x62c563','4a45482e8cabfec95d928ed6a5e70dd559a2a751b2216b312ae734f79828ec86'),
        '0x62eb90':('0x62ebbd','f26fd6450b096fe3493400b4301669aac1347e6093a0764daa403e7080455bf9'),
        '0x622010':('0x6221dc','c6c880f7e3a465dd2cc553bfc5dbf60240fe56e52261212eebf17b5ecacf9b95'),
        '0x621ff0':('0x621ffc','810781c10549c601701c17816fe2e4596ff61249f027f6586cf70c879b8b2145')}
    if len(raw['ranges'])!=5 or any(q['start'] not in spans or (q['end_exclusive'],q['sha256'])!=spans[q['start']] for q in raw['ranges']):raise ValueError('wrong/incomplete original body')
    entries=[[0x6160B0,0x61613B,0x1DA855C],[0x62C360,0x62C563,0x1DA84D0],[0x62EB90,0x62EBBD,0x1DDF508],[0x622010,0x6221DC,0x1D8F424]]
    if raw.get('pdata_entries')!=entries or raw.get('leaf',{}).get('padding')!='cc'*4:raise ValueError('root/leaf prerequisite changed')
    name='.?AV?$TAsyncUpdate@VPTexture2DD3D11@PRendering@Phyre@@@@';table=raw.get('table',{})
    if table.get('address')!='0xd54348' or table.get('COL')!='0x1d12448' or table.get('type_descriptor')!='0x1f5c5a0' or table.get('name')!=name or table.get('type_name_bytes')!=name.encode().hex() or table.get('slot0')!='0x621ff0' or table.get('raw_from_minus8')!='4824d10100000000f01f620000000000c824d10100000000':raise ValueError('physical RTTI/slot0 prerequisite changed')
    cfgs=[P.closed(x,a,b) for a,b,u in entries]
    for p,m,a in [
        (0x6160C8,'xor','edx, edx'),(0x6160CA,'mov','dword ptr [rbx + 0x30], edx'),
        (0x6160CD,'lea','rax, [rbx + 0x38]'),(0x6160D1,'test','rax, rax'),(0x6160D4,'je','0x616106'),
        (0x6160D6,'mov','qword ptr [rax], rdx'),(0x6160F1,'mov','dword ptr [rax + 0x38], edx'),
        (0x6160FB,'mov','qword ptr [rax + 0x40], rcx'),(0x6160FF,'mov','dword ptr [rbx + 0x30], 1'),
        (0x62C382,'mov','r9d, edx'),(0x62C385,'mov','rbx, rcx'),(0x62C388,'mov','ecx, dword ptr [rcx + 0x30]'),
        (0x62C38B,'and','ecx, 0x7fffffff'),(0x62C391,'mov','eax, 1'),(0x62C396,'cmovne','eax, ecx'),
        (0x62C399,'cmp','edx, eax'),(0x62C39B,'jb','0x62c3a7'),(0x62C39D,'mov','eax, 3'),
        (0x62C3CA,'cmp','qword ptr [r15 + rcx], rsi'),(0x62C3CE,'jne','0x62c3da'),(0x62C3D0,'mov','eax, 0x15'),
        (0x62C3F2,'test','dword ptr [rbx + 0xb4], 0x10000'),(0x62C3FC,'jne','0x62c4ce'),
        (0x62C4AA,'lea','rdx, [r15 + 0x40]'),(0x62C4AE,'add','rdx, rsi'),
        (0x62C4B1,'mov','qword ptr [rdx + 8], rbx'),(0x62C4B5,'mov','dword ptr [rdx + 0x10], r9d'),
        (0x62C4C7,'call','0x62eb90'),(0x62C548,'xor','eax, eax'),
        (0x62EB90,'mov','qword ptr [rsp + 0x10], rdx'),(0x62EB95,'sub','rsp, 0x38'),
        (0x62EB99,'movzx','r9d, byte ptr [rsp + 0x50]'),(0x62EBA7,'lea','r8, [rsp + 0x48]'),
        (0x62EBAC,'imul','r10, rax, 0x38'),(0x62EBB0,'add','rcx, r10'),(0x62EBB3,'call','0x199db0'),
        (0x621FF0,'mov','edx, dword ptr [rcx + 0x10]'),(0x621FF3,'mov','rcx, qword ptr [rcx + 8]'),(0x621FF7,'jmp','0x622010'),
        (0x622053,'mov','eax, edx'),(0x622055,'imul','r14, rax, 0x58'),
        (0x62206E,'mov','r13d, 0xb'),(0x622077,'cmovb','r13d, eax'),(0x622080,'xor','ebp, ebp'),
        (0x6220FD,'call','qword ptr [rax + 0x180]'),(0x622156,'inc','ebp'),(0x622158,'cmp','ebp, r13d'),(0x62215B,'jbe','0x622090')]:P.need(x,p,m,a)
    if x[0x6160F4]['memory'][0]['rip_target']!='0xd54348':raise ValueError('constructor table binding changed')
    # A source-linked symbolic load/store trace for this one straight-line block.
    # RCX is an object-relative address; staged register values name input bytes.
    rcx=None;values={};copy=[];pc=0x62C402
    while pc<0x62C490:
        i=x[pc];m=i['mnemonic'];mem=i['memory'];n=len(bytes.fromhex(i['bytes']))
        if m=='lea':
            assert len(mem)==1 and mem[0]['role']=='addr' and not mem[0]['index']
            b=mem[0]['base'];disp=mem[0]['displacement']
            if i['args'].startswith('rcx, ') and b=='rbx':rcx=disp
            elif i['args'].startswith('rcx, ') and b=='rcx' and rcx is not None:rcx+=disp
            else:raise ValueError('unmodelled copy address')
        elif m in ('movups','mov') and len(mem)==1:
            q=mem[0];assert not q['index']
            if q['role']=='r' and q['base']=='r8':values[i['args'].split(',')[0]]=(q['displacement'],q['size'])
            elif q['role']=='w' and q['base']=='rcx' and rcx is not None:
                reg=i['args'].rsplit(', ',1)[1]
                if reg not in values or values[reg][1]!=q['size']:raise ValueError('copy staging/width changed')
                offset,width=values[reg];copy.append(dict(pc=hex(pc),source_offset=offset,object_offset=rcx+q['displacement'],bytes=width))
            else:raise ValueError('unmodelled copy memory operation')
        else:raise ValueError('unmodelled copy instruction')
        pc+=n
    expected_copy=[(k,0xC0+k,16) for k in range(0,0xC0,16)]+[(0xC0,0x180,8)]
    if [(i['source_offset'],i['object_offset'],i['bytes']) for i in copy]!=expected_copy:raise ValueError('copy extent/order changed')
    if pc!=0x62C490 or sum(q['bytes'] for q in copy)!=200:raise ValueError('incomplete copy')
    result=dict(status='PRODUCER_CHECKED_ASYNC_ADMISSION_BOUNDARY_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,source_pins=pins,annotation_prerequisite=agreement,normal_cfgs=cfgs,
        checker_sha256=P.sha(pathlib.Path(__file__)),helper_sha256=P.sha(W/'prove-title-queue-consumption.py'),copy_trace=copy,
        question='What does the2D asynchronous admission path write/pass, and does the bound update entry settle the pending-counter writer?',
        established=[
            '626C-style naming is not used: exact62C360 checks unsigned input index<max(1,masked count), returns3 otherwise, and returns0x15 when selected element+0 isNULL. Maskedcount0 permits index0 before that resource read; actual zero-count validity remains a caller obligation.',
            'When DWORD[object+B4]&10000 isclear,62C360 copies exactly200B in input order from R8+0..C7 into object+C0..187, before writing the embedded async object data and calling62EB90. This is12 sequential16B load/store pairs and one8B pair, not a full staged snapshot or general overlap-safe copy.',
            'The queued-path data object is selected element+40; its+8 receives the original object pointer and its+10 receives the unsigned input index. The same RTTI-bound virtual0 atD54348→621FF0 loads those two fields and tail-calls622010. No actual queue callback execution or natural title-object binding is observed.',
            '62EB90 passes that saved pointer through a local record and calls199DB0 on context+38*zeroextend32(inputR8D). Its R9D is loaded from byte[entryRSP+18] after subtracting38, rather than taken from incomingR9D. Initialized value/meaning and199DB0 behavior remain open; no uninitialized-state or deferred-execution claim follows.',
            '622010 directly reads the element+28 block and calls context vslot180 for mip indices0 through its limit, at most12 calls under normal ABI-preserving returns. On its later maskedcount1 arm it calls584730 for the selected+28 block and nulls that field. Native graphics/free effects, dynamic count/storage and actual scheduling remain unproved.',
            'Reused accepted constructor premise: for a valid nonwrapping object,6160B0 sets count1 and the inline element+0/resource and+38/observed wait counter to0, then binds the embedded table at element+40. Hence an immediately unchanged fresh object is rejected by admission with0x15 and has a nonpositive drain field. This is source-state initialization, not observed loaded gameplay.',
        ],
        unresolved=['Who raises/lowers the element wait counter and its relationship to queued/inflight work: these sources do not establish the complete write closure','199DB0 entry/queue/flag behavior and whether callback execution is deferred or synchronous','Actual constructed/loaded object identity, resource binding, scheduler thread, lifetime/reuse/cancellation and natural title reachability','Meaning/readers of the200B tail remain unknown; physical copy extent does not identify a portable native structure'],
        assumptions=['ABI-correct normally returning original functions and valid object/element/input storage','Stable count/storage and nonwrapping correctly sized0x188 object for constructor/admission composition','Opaque native calls and nonvolatile registers obey the stated normal-return premises; source/target overlap safety is not assumed'],
        affected_claims=['OPUS PTexture2DD3D11+C0..187 physical write extent and callback/userdata ABI','FABLE Phyre async scheduling versus wait-counter and separate renderer/title queues'],
        native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,cleanup='Only original file reads and synchronous analysis; no game/process/input/instrument/save/config/reference/peer writes')
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print('Original200B copy and bound callback/admission ABI reduced; counter writer/scheduling OPEN')
if __name__=='__main__':main()
