"""Bounded interprocedural read-before-kill proof for two callback inputs.

Only the original pre-overwrite call graph is modeled. No synthetic execution,
sample counts, hidden side-channel guarantee, or inferred natural error trigger.
"""
import hashlib, importlib.util, json, pathlib, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
W=pathlib.Path(__file__).resolve().parent
def module(n,f):
    s=importlib.util.spec_from_file_location(n,W/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
P=module('callback_input_proof','prove-title-queue-consumption.py')
S=module('callback_input_roles','validate-title-source-annotations.py')
FAMILIES={0:{'rdx','edx','dx','dh','dl'},1:{'r8','r8d','r8w','r8b'}}
FULL_WRITES={0:{'rdx','edx'},1:{'r8','r8d'}}
EXTENTS={0x32f3d0:0x32f427,0x408b30:0x408b38,0x408b10:0x408b18,
         0x36b130:0x36b159,0x409090:0x4090c5,0x5c5230:0x5c5233}

def main():
    out=pathlib.Path(sys.argv[1]);src=pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else W
    if out.exists():raise ValueError('immutable result exists')
    d=src/'capture-namebinding-callback-inputs.py'
    st=json.loads((src/'namebinding-callback-inputs-capture-01.status.json').read_text())
    if st.get('exit')!=0 or st.get('driver_sha256')!=P.sha(d):raise ValueError('capture failed/stale')
    if not(src/'namebinding-callback-inputs-capture-01.stdout').read_bytes().strip() or(src/'namebinding-callback-inputs-capture-01.stderr').read_bytes().strip():raise ValueError('capture incomplete')
    pins=[];v,ix=P.load(src,'namebinding-callback-inputs-source-01.json',pins);S.validate(v)
    if v.get('invocation_driver_sha256')!=P.sha(d):raise ValueError('actual capture invocation changed')
    if [(int(q['start'],16),int(q['end_exclusive'],16)) for q in v['ranges']]!=list(EXTENTS.items()):raise ValueError('early graph boundaries changed')
    prov=json.loads((src/'namebinding-callback-inputs-retained-provenance-01.json').read_text())
    if prov['sha256']!=P.sha(src/prov['local_path']):raise ValueError('retained callback preimage changed')
    retained,ri=P.load(src,prov['local_path'],pins);S.validate(retained);ix.update(ri)
    b=(S.ROOT/'Database/Tools/work/exe/FFXII_TZA.exe').read_bytes()
    if hashlib.sha256(b).hexdigest()!=P.SHA:raise ValueError('reference image changed')
    e=struct.unpack_from('<I',b,60)[0];o=struct.unpack_from('<H',b,e+20)[0]
    sec=[struct.unpack_from('<IIII',b,e+24+o+k*40+8) for k in range(struct.unpack_from('<H',b,e+6)[0])]
    for bundle in [v,retained]:
        for q in bundle['ranges']:
            a,z=int(q['start'],16),int(q['end_exclusive'],16)
            raw=next(b[ro+a-0x120000-va:ro+z-0x120000-va] for _,va,rs,ro in sec if 0x120000+va<=a and z<=0x120000+va+rs)
            if raw!=bytes.fromhex(''.join(i['bytes'] for i in q['instructions'])):raise ValueError('reference byte identity changed')
    cfgs=[P.closed(ix,a,z) for a,z in EXTENTS.items()]
    P.need(ix,0x2e4d3e,'movsxd','rdi, ecx');P.need(ix,0x2e4d46,'call','0x32f3d0')
    P.need(ix,0x2e4d68,'call','0x36b130');P.need(ix,0x2e4d73,'call','0x409090')
    P.need(ix,0x2e4d78,'mov','r8d, dword ptr [rdi + 0x14]');P.need(ix,0x2e4d7c,'mov','rdx, rax')
    P.need(ix,0x2e4d82,'call','0x36c660');P.need(ix,0x409097,'lea','rdx, [rip + 0x1af68a2]')
    P.need(ix,0x4090a3,'mov','r8d, dword ptr [rcx]');P.need(ix,0x5c5230,'xor','eax, eax');P.need(ix,0x5c5232,'ret','')
    # Calls are expanded into their original graph, not assumed volatile-clobber
    # stubs. Branches include all successors; loops close over (pc, live-inputs).
    md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True;memo={};active=set();kills=set();calls=set();states=set()
    def solve(entry,mask):
        key=(entry,mask)
        if key in memo:return memo[key]
        if key in active:raise ValueError('unmodeled recursive early graph')
        active.add(key);end=0x2e4d82 if entry==0x2e4d20 else EXTENTS[entry]
        todo=[(entry,mask)];seen=set();returns=set()
        while todo:
            pc,live=todo.pop()
            if (pc,live) in seen:continue
            seen.add((pc,live));states.add((entry,pc,live))
            if pc==end and entry==0x2e4d20:
                if live:raise ValueError('callback inputs still live at opaque boundary')
                returns.add(live);continue
            if pc not in ix or not entry<=pc<end:raise ValueError('unclosed early graph')
            i=ix[pc];raw=bytes.fromhex(i['bytes']);dec=list(md.disasm(raw,pc))
            if len(dec)!=1 or dec[0].size!=len(raw):raise ValueError('invalid input-dependency instruction')
            reads,writes=dec[0].regs_access();rr={dec[0].reg_name(q) for q in reads};ww={dec[0].reg_name(q) for q in writes}
            for bit,names in FAMILIES.items():
                if live&(1<<bit) and rr&names:raise ValueError('incoming argument read before kill at '+hex(pc))
                if live&(1<<bit) and ww&FULL_WRITES[bit]:live&=~(1<<bit);kills.add((pc,bit))
            n=pc+len(raw);m=i['mnemonic']
            if m=='ret':returns.add(live);continue
            if m=='call':
                target=int(i['args'],16)
                if target not in EXTENTS:raise ValueError('opaque pre-overwrite call '+hex(target))
                calls.add((pc,target))
                for state in solve(target,live):todo.append((n,state))
            elif m=='jmp':todo.append((int(i['args'],16),live))
            elif m.startswith('j'):todo.extend([(int(i['args'],16),live),(n,live)])
            else:todo.append((n,live))
        active.remove(key)
        if not returns:raise ValueError('no checked exit from early graph')
        memo[key]=returns;return returns
    exits=solve(0x2e4d20,3)
    if exits!={0}:raise ValueError('incoming argument proof incomplete')
    # The rest of the full retained callback has no stored original copies:
    # neither input was read at all before its kill. Subsequent opaque callees
    # therefore receive replacement values. Conditional followup still matters.
    P.need(ix,0x2e4dc6,'call','0x2ea6e0');P.need(ix,0x2e4dcb,'test','eax, eax')
    P.need(ix,0x2e4dcd,'jne','0x2e4de1');P.need(ix,0x2e4dcf,'or','byte ptr [rdi + 0x18], 2')
    report=dict(status='PRODUCER_VALID_CALLBACK_INPUT_INDEPENDENCE_INDEPENDENT_PENDING',producer_complete=True,
        method='A ORIGINAL_CODE_INPUT_INVARIANT',exe_sha256=P.SHA,source_pins=pins,checker_sha256=P.sha(pathlib.Path(__file__)),
        normal_helper_cfgs=cfgs,root_prefix=dict(entry='0x2e4d20',stop_before_opaque_call='0x2e4d82',incoming=['RDX destination','R8D success'],exit_live_masks=sorted(exits)),
        original_expanded_calls=[dict(pc=hex(pc),target=hex(t)) for pc,t in sorted(calls)],
        argument_kills=[dict(pc=hex(pc),input='RDX' if bit==0 else 'R8D',operation=ix[pc]['mnemonic']+' '+ix[pc]['args']) for pc,bit in sorted(kills)],
        established=['With fixed valid ECX record/current memory and normal original execution, incoming R8D success and RDX destination are never read before full overwrite across the complete early original call graph. Both are dead before36C660; no stored copy survives. The callback does not gate local behavior on either argument.',
          '32F3D0 expands only original408B30/408B10 getters and shipping5C5230 zero stub;36B130 is a leaf.409090 unconditionally replacesRDX and conditionally replacesR8D; callback then overwritesR8D from record+14. No assumed volatile-register clobber or fabricated native effects establishes this invariant.',
          'Ready18mask02 still follows original2EA6E0 return0, with removal/registration rules and callee effects separate. Incoming success0 versus1 cannot itself distinguish successful content here; a ready record is not proof of valid delivered bytes.'],
        limitations=['No proof the failed-read path naturally invokes this callback; error-helper count==-1 condition and actual IO/count writers are separate.',
          'Valid pointer/resource mappings, normal ABI returns, fixed relevant memory/execution environment and no interference are premises; exceptions, timing/side channels and arbitrary invalid inputs are not certified.',
          'No full followup/registration/tagging/storage semantics or complete lifetime/recovery proof. Shipping zero stub cannot establish omitted native effects.',
          'Static proof/control receipts are producer evidence, not native executions, independent acceptance or whole runtime-row closure.'],
        affected_claims=['Namebinding callback/readiness distinction in existing FABLE/OPUS deletion consumers','SPEC deletion/pin review; failure notification is not successful-content certification','Future OV19/21 error-recovery/lifetime preparations must keep natural failed delivery separate'],
        required_invocation_receipts=[dict(path=n,sha256=P.sha(src/n)) for n in ['capture-namebinding-callback-inputs.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','namebinding-callback-inputs-retained-provenance-01.json','namebinding-callback-inputs-capture-01.status.json','namebinding-callback-inputs-capture-01.stdout','namebinding-callback-inputs-capture-01.stderr']],
        native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0,next_discriminator='Natural failed callback delivery/count writer and valid-content recovery remain separate; do not sample input-status independence in live game again.',cleanup='Finite original reads and static invariant; no game/PC/native/emulated/instrument/save/config/reference/peer mutation')
    with out.open('x',encoding='utf8')as f:json.dump(report,f,indent=2);f.write('\n')
    print('Original incoming success/destination never read before kills; conditional readiness not successful-content proof')
if __name__=='__main__':main()
