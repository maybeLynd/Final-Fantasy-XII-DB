"""Bounded original selector -> actor record -> interpreter identity proof.

Fresh result [disposable source directory]. No scheduling samples/native runs.
Returned RC16 counts remain external corroboration, not executions of this tool.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
W=pathlib.Path(__file__).resolve().parent
def module(name,file):
    s=importlib.util.spec_from_file_location(name,W/file)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('regfile_proof','prove-title-queue-consumption.py')
S=module('regfile_roles','validate-title-source-annotations.py')
INPUT_PIN='2534bc9eea8804fb2335c742cfa85f5db27a99d868d7f945a013099c1836a334'
RAW_PIN='c2617234e510735e6a1a794de000feac0a8fd956af9f2fd1afbb4e4bac6c8993'

def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    driver=src/'capture-regfile-spawn-record.py';receipt=src/'regfile-spawn-record-capture-01.status.json'
    st=json.loads(receipt.read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(driver):raise ValueError('capture failed/stale')
    if not (src/'regfile-spawn-record-capture-01.stdout').read_bytes().strip() or (src/'regfile-spawn-record-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'regfile-spawn-record-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(driver) or v.get('retained_input_manifest_sha256')!=INPUT_PIN:
        raise ValueError('capture provenance changed')
    ip=src/'regfile-spawn-record-inputs-01';mp=ip/'manifest.json'
    if P.sha(mp)!=INPUT_PIN:raise ValueError('retained manifest changed')
    pins.append(dict(path=mp.relative_to(src).as_posix(),sha256=P.sha(mp)))
    for x in json.loads(mp.read_text())['members']:
        p=ip/x['path']
        if p.stat().st_size!=x['bytes'] or P.sha(p)!=x['sha256']:raise ValueError('retained input changed')
        pins.append(dict(path=p.relative_to(src).as_posix(),sha256=P.sha(p)))
    raw=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    pe=struct.unpack_from('<I',raw,60)[0];opt=struct.unpack_from('<H',raw,pe+20)[0]
    sections=[struct.unpack_from('<IIII',raw,pe+24+opt+k*40+8) for k in range(struct.unpack_from('<H',raw,pe+6)[0])]
    def read(a,n):
        for _,va,rs,ro in sections:
            if 0x120000+va<=a and a+n<=0x120000+va+rs:return raw[ro+a-0x120000-va:ro+a-0x120000-va+n]
        raise ValueError('unbacked original span')
    spans=[]
    for q in v['ranges']:
        a,z=int(q['start'],16),int(q['end_exclusive'],16)
        if bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))!=read(a,z-a):raise ValueError('reference byte identity changed')
        spans.append(dict(start=q['start'],end_exclusive=q['end_exclusive'],sha256=q['sha256'],origin=q.get('origin','new missing span')))
    # These complete leaves/callers have all normal successors in their ranges.
    closed=[P.closed(ix,a,z) for a,z in [(0x25ad10,0x25adf5),(0x25af60,0x25afb4),(0x263d40,0x263dc7),
        (0x269860,0x2699cc),(0x2640c0,0x2640c8),(0x3dbb60,0x3dbbd8),(0x3587c0,0x3587f2),
        (0x263ff0,0x264005),(0x358940,0x35895e),(0x358a00,0x358a15),
        (0x3dbcf0,0x3dbdb2),(0x3db6e0,0x3db788),(0x3dbdc0,0x3dbe92)]]
    ops=[
      # One popped group selector; the SAME supplied record reaches all lists.
      (0x34fa82,'mov','rsi, rdx'),(0x34fa85,'call','0x2640c0'),(0x34fa8d,'mov','rdi, rax'),
      (0x34fa90,'call','0x267e10'),(0x34fa95,'mov','r9d, eax'),(0x34fa98,'xor','r8d, r8d'),
      (0x34fa9b,'mov','rdx, rsi'),(0x34faa3,'call','0x25ad10'),(0x34faa8,'mov','r9d, ebx'),
      (0x34faab,'mov','r8d, 1'),(0x34fab1,'mov','rdx, rsi'),(0x34fab7,'call','0x25ad10'),
      (0x34fabc,'mov','r9d, ebx'),(0x34fabf,'mov','r8d, 4'),(0x34fac5,'mov','rdx, rsi'),
      (0x34facb,'call','0x25ad10'),(0x34fad0,'mov','r9d, ebx'),(0x34fad3,'mov','r8d, 2'),
      (0x34fad9,'mov','rdx, rsi'),(0x34fadf,'call','0x25ad10'),(0x34fae4,'mov','r9d, ebx'),
      (0x34fae7,'mov','r8d, 3'),(0x34faed,'mov','rdx, rsi'),(0x34fb02,'jmp','0x25ad10'),
      # list -> function ID -> the record's own ordinal, through the manager pool.
      (0x25ad29,'mov','ebx, r8d'),(0x25ad31,'mov','rdi, rdx'),(0x25ad34,'mov','word ptr [rdx + 0xf6], r9w'),
      (0x25ad3c,'mov','rsi, rcx'),(0x25ad3f,'call','0x263d40'),(0x25ad44,'mov','ebp, 0xa'),
      (0x25ad62,'lea','edx, [rbp + 4]'),(0x25ad6b,'mov','edx, 7'),(0x25ad74,'movzx','r8d, word ptr [rdi]'),
      (0x25ad78,'mov','r9d, eax'),(0x25ad7b,'mov','rcx, rsi'),(0x25ad7e,'call','0x25af60'),
      (0x25af71,'movsxd','rbx, edx'),(0x25af74,'mov','edi, r9d'),(0x25af96,'mov','ecx, dword ptr [rcx + 0x28]'),
      (0x25af99,'mov','edx, r8d'),(0x25af9c,'call','0x3587c0'),(0x25afa1,'mov','word ptr [rax + rbx*2 + 0xc8], di'),
      (0x3587c6,'movsxd','rbx, edx'),(0x3587c9,'call','0x263ff0'),(0x3587ce,'mov','rcx, qword ptr [rax + 8]'),
      (0x3587df,'mov','rax, qword ptr [rcx + rbx*8 + 8]'),(0x263ffa,'imul','rax, rax, 0x288'),
      # Read function metadata from this record, never a per-unit spawn record.
      (0x263d54,'mov','rbx, qword ptr [rcx]'),(0x263d5a,'movsxd','rdi, r9d'),(0x263d5d,'mov','esi, r8d'),
      (0x263d6b,'mov','rax, qword ptr [rdx + 0x40]'),(0x263d6f,'mov','ecx, dword ptr [rax + 0x18]'),
      (0x263d80,'lea','edx, [rsi + 1]'),(0x263d90,'movsx','eax, word ptr [rcx]'),
      (0x263d97,'lea','rcx, [rcx + rax*2]'),(0x263d9f,'jne','0x263d90'),
      (0x263da8,'movsx','eax, word ptr [rcx + rdi*2 + 2]'),
      # Both initial-spawn and respawn arms keep the original actor in RDI.
      (0x26986c,'mov','rdi, rcx'),(0x2698c4,'movzx','eax, word ptr [rdi + 0xd6]'),
      (0x269932,'mov','ebx, 0xe'),(0x26993f,'mov','r8d, 7'),(0x26994d,'cmovb','ebx, r8d'),
      (0x269951,'movzx','eax, word ptr [rdi + rbx*2 + 0xc8]'),
      (0x2699a4,'mov','rcx, rdi'),(0x2699a7,'lea','edx, [r9 + 2]'),(0x2699ab,'call','0x3dbb60'),
      (0x3dbba9,'mov','word ptr [rsp + 0x24], r8w'),(0x3dbbaf,'lea','rdx, [rsp + 0x20]'),
      (0x3dbbce,'call','0x3dbcf0'),(0x3dbd09,'mov','rbx, rcx'),(0x3dbd5c,'mov','rcx, rbx'),
      (0x3dbd5f,'call','0x3db7a0'),(0x3db7ab,'mov','r10, rcx'),
      # Selection -> start keeps A, PC and wait slot inside A.
      (0x3db6ea,'mov','rdi, rcx'),(0x3db710,'movzx','ebx, byte ptr [rdi + r8 + 0x94]'),
      (0x3db728,'mov','rax, qword ptr [rdi + 0xa0]'),(0x3db75c,'mov','rcx, rdi'),(0x3db75f,'call','0x3dbdc0'),
      (0x3dbde0,'mov','rbp, rcx'),(0x3dbde7,'mov','rax, qword ptr [rcx + 0xa8]'),
      (0x3dbdf2,'call','0x358a00'),(0x3dbe05,'add','rax, qword ptr [rbp + 0x58]'),(0x3dbe09,'mov','qword ptr [rdi], rax'),
      (0x358a00,'mov','r8, qword ptr [rcx + 0x48]'),(0x358a0f,'mov','eax, dword ptr [r8 + rax*8 + 8]'),
      # Already retained interpreter call and register-base provenance.
      (0x25df25,'mov','rdi, rdx'),(0x25e0ca,'mov','r8, rsi'),(0x25e0cd,'mov','rdx, rdi'),
      (0x25e0d3,'call','0x25e4c0'),(0x25e4d5,'mov','r15, rdx')]
    for pc,m,a in ops:P.need(ix,pc,m,a)
    # Check every local reassignment of the actor carrier before its use.
    def assignments(start,end,register):
        return [i['pc'] for i in ix.values() if start<=int(i['pc'],16)<end and
            i['args'].split(',')[0]==register and i['mnemonic'] not in ['test','cmp','push']]
    if assignments(0x34fa70,0x34fb02,'rsi')!=['0x34fa82','0x34faf8']:raise ValueError('wrapper actor carrier changed')
    # An earlier failure return restores caller RDI. It cannot reach submission;
    # a flat address filter incorrectly counts that epilogue as a reassignment.
    edges={};todo=[0x269860];seen=set()
    while todo:
        pc=todo.pop()
        if pc in seen:continue
        seen.add(pc);i=ix[pc];nxt=pc+len(bytes.fromhex(i['bytes']));m=i['mnemonic']
        if pc==0x2699ab or m.startswith('ret'):targets=[]
        elif m=='jmp':targets=[int(i['args'],16)]
        elif m.startswith('j'):targets=[nxt,int(i['args'],16)]
        else:targets=[nxt]
        if any(p not in ix or not 0x269860<=p<0x2699cc for p in targets):raise ValueError('submit path unclosed')
        edges[pc]=targets;todo.extend(targets)
    reaching={0x2699ab}
    while True:
        expanded=reaching|{pc for pc,ts in edges.items() if any(p in reaching for p in ts)}
        if expanded==reaching:break
        reaching=expanded
    actor_writes=[i['pc'] for pc,i in ix.items() if pc in reaching and i['args'].split(',')[0] in ['rdi','edi','di','dil'] and i['mnemonic'] not in ['test','cmp','push']]
    if actor_writes!=['0x26986c']:raise ValueError('submit actor carrier changed')
    if 0x269883 in reaching or edges[0x269884]:raise ValueError('failure epilogue reaches submission')
    if assignments(0x25df00,0x25e0d3,'rdi')!=['0x25df25']:raise ValueError('interpreter caller actor changed')
    if ix[0x25afa1]['memory'][0]['role']!='w' or ix[0x263d97]['memory'][0]['role']!='addr':raise ValueError('store/address roles changed')
    # One original authored actor, multiple selections; this is not a new census.
    ap=src/'regfile-spawn-record-authored-01/gol_b01.s000';b=ap.read_bytes()
    if hashlib.sha256(b).hexdigest()!=RAW_PIN:raise ValueError('authored source changed')
    pins.append(dict(path=ap.relative_to(src).as_posix(),sha256=P.sha(ap)))
    def u32(o):return struct.unpack_from('<I',b,o)[0]
    def u16(o):return struct.unpack_from('<H',b,o)[0]
    def name(o):return b[o:b.index(b'\0',o)].decode('cp932')
    if u32(0)!=0x8000000b:raise ValueError('authored layout changed')
    tab,pool=u32(0x18),u32(0x4c);actors=u32(tab)
    matches=[k for k in range(actors) if name(pool+u32(tab+4+k*0x30))=='monster_00']
    if matches!=[26]:raise ValueError('authored actor identity changed')
    e=tab+4+26*0x30;ft=u32(e+0x10);footer=u32(e+0x18);q=footer+2+u16(footer)*2;lists=[]
    for lid in range(5):
        count=u16(q);ids=[struct.unpack_from('<h',b,q+2+j*2)[0] for j in range(count)]
        if any(i<0 or i>=u32(ft) for i in ids):raise ValueError('authored function outside table')
        lists.append(dict(list=lid,offset=hex(q),function_ids=ids,names=[name(pool+u32(ft+4+8*i)) for i in ids]));q+=2+count*2
    if lists[1]['names']!=['spawn%02d'%i for i in range(6)] or lists[4]['names']!=['respawn%02d'%i for i in range(6)]:raise ValueError('authored selection control changed')
    if lists[0]['names']!=['entry%02d'%i for i in range(6)] or lists[2]['names'] or lists[3]['names']:raise ValueError('authored companion control changed')
    result=dict(status='PRODUCER_VALID_CONDITIONAL_SPAWN_RECORD_BINDING_INDEPENDENT_PENDING',producer_complete=True,method='A STATIC_ONLY',exe_sha256=P.SHA,
        source_pins=pins,original_spans=spans,normal_cfgs=closed,submit_carrier_control=dict(actor_writes=actor_writes,excluded_failure_pop='0x269883',excluded_return='0x269884',reaching_nodes=len(reaching)),authored_control=dict(image=ap.name,actor='monster_00',ordinal=26,entry=hex(e),function_table=hex(ft),footer=hex(footer),lists=lists),
        established=[
        'setentrygroup wrapper34FA70 pops one group selector and calls25AD10 with the SAME actor argument for entry,spawn,respawn,talk,touch (lists0,1,4,2,3). Restoring savedRSI at its tail does not alter the already-copied RDX.',
        '25AD10 reads the function from the supplied actor entry+40/18 and stores selection at that record+F6. Successful list1/4 selection sets override slots7/14 through its self ordinal and the current manager pool. With a coherent current manager, valid low self ordinal, stable pool/table and no interference, lookup returns the SAME record. This is function selection, not record allocation.',
        'Retained gol_b01 monster_00 ordinal26 has six spawn and six respawn functions in ONE authored actor entry/function table. Different selection indices change function IDs in that record; they do not supply another authored actor ordinal. Empty talk/touch lists remain absent, not substituted successful functions.',
        '269860 selects the spawn7 or conditional respawn14 override from its supplied actor and submits through3DBB60/3DBCF0 to that same actor. The record carrier is not reassigned before the call. Selection3DB6E0 and start3DBDC0 use that actor active-entry/wait-slot/function table/bytecode base.',
        'Retained25DF00 passes its actor unchanged inRDX into25E4C0; its prefix storesRDX inR15, the already established interpreter register-bank base. Thus selected spawn/respawn function execution on this coherent path uses the authored actor record bank, not a new bank per selection or its SpawnKeep BattleStats block.',
        'Previously accepted RC16 different-authored-actor in-pool reuse premise is superseded; no live reuse sample is needed to distinguish the two record-binding hypotheses on this bounded path. Actual multiple executions/order/cause/I1 values and full natural reachability are separate questions.'],
        limitations=['Coherent current manager and self-ordinal identity, valid metadata/indices, normal ABI-preserving returns and no interfering writes are explicit premises; corrupt/cross-manager/encoded-ID states are not certified',
        'No new game/native/emulated execution; retained SECTION12 raw instructions are source, and its external assertions are not tests run here',
        'No full interpreter/corpus recensus; accepted RC16 read-before-write/native-access bounds and unreachable takeover-reader limits remain',
        'Selecting/submitting/starting a request is not proof of natural executed bytecode, timing, callback lifetime or visible gameplay consequences',
        'Producer checks are not independent acceptance or canonical incorporation; owning FABLE/OPUS/CONTRACT pages remain peer-owned'],
        affected_claims=['RC16 exact spawn-group record-binding residue: conditional same authored-record function execution','FABLE-REQ-ASTRA-REGFILE-REUSE and FRONTIER AQ11 obsolete different-actor in-pool setup','OPUS/SWE2-CONTRACT register lifetime and spawn-selector contract'],
        next_discriminator='Independent review of coherent current-manager/self-index chain and scope; canonical owners incorporate only after acceptance. Any claim of actual repeated execution or current-manager interference must name a separate unresolved proposition.',
        checker_sha256=P.sha(pathlib.Path(__file__)),native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,
        required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-regfile-spawn-record.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','regfile-spawn-record-capture-01.status.json','regfile-spawn-record-capture-01.stdout','regfile-spawn-record-capture-01.stderr']],
        cleanup='Finite retained/reference reads and disposable controls; no PC/game/input/instrument/save/config/reference or peer mutation')
    with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Conditional same authored-record spawn/respawn binding; original source and raw script control, independent acceptance pending')

if __name__=='__main__':main()
