"""select_teardown_form_clusters_4.py - EC-7 family C member selectors, fourth
pass (SWE2-EC7-FRONTIER-FORM-CLUSTERS-4), declared on
object-construction-destruction-and-static-lifetime.md.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_teardown_form_clusters_4.py [--write]
"""
import io, os, struct, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
BASE = 0x120000

def norm(s):
    return "; ".join(t.strip() for t in s.split(";"))

def leaf(m, c, j, x):
    return not c and not j and not x
def one_call(m, c, j, x):
    return len(c) == 1 and not j and not x
def call_tail(m, c, j, x):
    return len(c) == 1 and len(j) == 1 and not x
def jcc_tail(m, c, j, x):
    return not c and not j and len(x) == 1
def shared_only(*ts):
    want = set(ts)
    return lambda m, c, j, x: c == want and not j and not x
def shared_calls(*ts):
    want = set(ts)
    return lambda m, c, j, x: want <= set(c) and not j and not x
def shared_any(*ts):
    want = set(ts)
    return lambda m, c, j, x: want <= (set(c) | set(j) | set(x))
def targets_exact(nc, nj, nx):
    return lambda m, c, j, x: len(c) == nc and len(j) == nj and len(x) == nx
def form_only(m, c, j, x):
    return True

FAMILIES = [
    ("nativeadapter-countedalignedfreeloopself.tsv", 104,
     "test rcx,rcx; je T; push rdi; sub rsp,I; mov M[rsp],I; "
     "mov M[rsp],rbx; mov M[rsp],rsi; mov rsi,rcx; test edx,edx; je T; "
     "lea rbx,M[rcx]; mov edi,edx; nop M[rax+rax]; mov rcx,M[rbx]; "
     "test rcx,rcx; je T; mov eax,ecx; not al; test al,I; je T; call T; "
     "nop; add rbx,I; sub rdi,I; jne T; mov rcx,rsi; call T; "
     "mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x00584730),
     "NativeAdapter.CountedAlignedFreeLoopSelf - EC-7 family C\n"
     "if this null return; counted loop over edx elements at [this+8] stride\n"
     "# 0x10: free each ref-flagged pointer via shared aligned-free 00584730;\n"
     "# then free this itself via 00584730."
),
    ("nativeadapter-refflagalignedfreeclear.tsv", 58,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; mov eax,M[rcx]; "
     "shr eax,I; not al; test al,I; je T; mov rcx,M[rcx]; test rcx,rcx; "
     "je T; call T; nop; xor eax,eax; mov M[rbx],rax; mov M[rbx],eax; "
     "add rsp,I; pop rbx; ret",
     shared_any(0x00584730),
     "NativeAdapter.RefFlagAlignedFreeClear - EC-7 family C\n"
     "if [this] bit31 is clear, free [this+X] via shared 00584730; zero the\n"
     "# pointer/size fields."
),
    ("nativeadapter-refflagsiblingboundedlookup.tsv", 164,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; sub rsp,I; "
     "mov rbx,rcx; mov ebp,edx; mov ecx,M[rcx]; btr ecx,I; cmp edx,M[rbx]; "
     "je T; cmp ecx,I; jbe T; mov rdi,M[rbx]; jmp T; test ecx,ecx; je T; "
     "lea rdi,M[rbx]; jmp T; xor edi,edi; mov rcx,rbx; call T; mov rsi,rax; "
     "test rax,rax; jne T; test ebp,ebp; je T; lea eax,M[rsi]; jmp T; "
     "mov M[rsp],r14; lea r14,M[rbx]; cmp rdi,rsi; je T; cmp rdi,r14; je T; "
     "mov eax,M[rbx]; shr eax,I; not al; test al,I; je T; test rdi,rdi; "
     "je T; mov rcx,rdi; call T; cmp rsi,r14; je T; mov M[r14],rsi; "
     "mov r14,M[rsp]; mov M[rbx],ebp; xor eax,eax; mov rbx,M[rsp]; "
     "mov rbp,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x00584730),
     "NativeAdapter.RefFlagSiblingBoundedLookup - EC-7 family C\n"
     "ref-flag counted element op: bound arg2 against [this]&~bit31, pick the\n"
     "# inline-vs-heap element pointer, call a member lookup; on failure either\n"
     "# return 0xD or free the range via shared 00584730 + member fixup."
),
    ("nativeadapter-refflagsiblingboundedlookup2.tsv", 135,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov r8d,M[rcx]; "
     "mov edi,edx; btr r8d,I; mov rbx,rcx; cmp edx,M[rcx]; je T; "
     "cmp edx,r8d; cmovb r8d,edx; mov rdx,M[rcx]; mov ecx,edi; call T; "
     "mov rsi,rax; test rax,rax; jne T; test edi,edi; je T; lea eax,M[rsi]; "
     "mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret; "
     "mov rcx,M[rbx]; mov eax,M[rbx]; cmp rcx,rsi; je T; shr eax,I; not al; "
     "test al,I; je T; test rcx,rcx; je T; call T; mov M[rbx],rsi; "
     "mov M[rbx],edi; mov rbx,M[rsp]; xor eax,eax; mov rsi,M[rsp]; "
     "add rsp,I; pop rdi; ret",
     shared_any(0x00584730),
     "NativeAdapter.RefFlagSiblingBoundedLookup2 - EC-7 family C\n"
     "ref-flag counted element op, second spelling: min(arg2,[this]&~bit31);\n"
     "# call a member lookup on [this+8]; on failure return 0xD else shrink the\n"
     "# range and free the tail via shared 00584730."
),
    ("nativeadapter-dynamicoffsetrefflagbounded.tsv", 114,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rax,M[rcx]; mov ebx,r8d; "
     "mov ecx,M[rcx]; sub ecx,M[rax]; movsxd rdi,ecx; add rdi,rdx; "
     "mov r8d,M[rdi]; btr r8d,I; cmp ebx,M[rdi]; je T; mov rdx,M[rdi]; "
     "cmp ebx,r8d; mov ecx,ebx; cmovb r8d,ebx; call T; test rax,rax; jne T; "
     "test ebx,ebx; je T; mov eax,I; mov rbx,M[rsp]; add rsp,I; pop rdi; "
     "ret; mov r8d,ebx; mov rdx,rax; mov rcx,rdi; call T; xor eax,eax; "
     "mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     targets_exact(2, 0, 0),
     "NativeAdapter.DynamicOffsetRefFlagBounded - EC-7 family C\n"
     "compute an element pointer at arg1+([this+0x18]+([this+0x48]-[[rax]+0xF4])\n"
     "# scaled); bound arg3 against its ref-flag count; call a member lookup; on\n"
     "# failure return 0xD else call a member op with (elem,result,arg3)."
),
    ("nativeleaf-refflag72strideaccessor.tsv", 58,
     "mov eax,M[rcx]; btr eax,I; cmp eax,I; jbe T; mov r8,M[rcx]; "
     "mov eax,edx; lea rax,M[rax+rax]; lea rax,M[rax]; lea rax,M[r8+rax]; "
     "ret; lea r8,M[rcx]; xor ecx,ecx; test eax,eax; mov eax,edx; "
     "cmove r8,rcx; lea rax,M[rax+rax]; lea rax,M[rax]; lea rax,M[r8+rax]; "
     "ret",
     leaf,
     "NativeLeaf.RefFlag72StrideAccessor - EC-7 family C\n"
     "if [this+0x20]&~bit31 > 1 index the heap array at [this+0x28] else the\n"
     "# inline buffer this+0x28; return &elem[arg2] at 72-byte stride +4."
),
    ("nativeleaf-refflag40strideaccessor.tsv", 67,
     "mov eax,M[rcx]; btr eax,I; mov r8d,edx; cmp edx,eax; jae T; "
     "mov eax,M[rcx]; btr eax,I; cmp eax,I; jbe T; mov rdx,M[rcx]; "
     "lea rcx,M[r8+r8]; mov rax,M[rdx+rcx]; ret; lea rdx,M[rcx]; "
     "xor ecx,ecx; test eax,eax; cmove rdx,rcx; lea rcx,M[r8+r8]; "
     "mov rax,M[rdx+rcx]; ret; xor ecx,ecx; mov eax,ecx; ret",
     leaf,
     "NativeLeaf.RefFlag40StrideAccessor - EC-7 family C\n"
     "if arg2 >= [this+0x18]&~bit31 return 0; index heap [this+0x20] or inline\n"
     "# this+0x20 at 40-byte stride; return [elem+8]."
),
    ("nativeleaf-listwalkvcallslot3.tsv", 115,
     "push r14; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov M[rsp],rsi; "
     "mov M[rsp],rdi; mov rsi,rcx; mov rbx,M[rcx]; test rbx,rbx; je T; "
     "nop M[rax+rax]; mov rdx,M[rbx]; mov rcx,rsi; call T; nop; "
     "mov rdi,M[rbx]; mov rax,M[rsi]; mov r8d,I; mov rdx,rbx; "
     "lea rcx,M[rsi]; call M[rax]; nop; mov rbx,rdi; test rdi,rdi; jne T; "
     "mov rbx,M[rsp]; mov rsi,M[rsp]; mov rdi,M[rsp]; add rsp,I; pop r14; "
     "ret",
     targets_exact(1, 0, 0),
     "NativeLeaf.ListWalkVcallSlot3 - EC-7 family C\n"
     "walk the intrusive list at [this+0x18]; per node call a member op with\n"
     "# (this,[node]) then vcall [this+0x30] slot 3 with r8=0x58."
),
    ("nativeadapter-flaggedteardownchain.tsv", 73,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; cmp M[rcx],I; je T; "
     "add rcx,I; call T; nop; lea rcx,M[rbx]; call T; nop; lea rcx,M[rbx]; "
     "call T; nop; mov rcx,rbx; add rsp,I; pop rbx; jmp T",
     shared_any(0x005CD6D0),
     "NativeAdapter.FlaggedTeardownChain - EC-7 family C\n"
     "if [this+0xB8]!=0 call shared 005CD6D0 on this+0x90; then call a member\n"
     "# teardown on +0x58 and +0x20; tail-dispatch to a member finisher."
),
    ("nativeadapter-containerpopfront.tsv", 161,
     "push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov M[rsp],rsi; "
     "mov rdi,rcx; cmp M[rcx],I; jbe T; mov rbx,M[rcx]; mov rsi,M[rbx]; "
     "mov M[rsp],rsi; dec M[rcx]; mov rcx,rbx; call T; lea rdx,M[rdi]; "
     "mov rcx,rbx; call T; lea rcx,M[rdi]; mov rax,M[rcx]; mov r8d,I; "
     "mov rdx,rbx; call M[rax]; lea rcx,M[rdi]; movzx r9d,M[rsp]; "
     "lea r8,M[rsp]; lea rdx,M[rsp]; call T; mov M[rsp],rsi; test rsi,rsi; "
     "je T; mov rcx,rsi; call T; jmp T; xor eax,eax; mov M[rsp],rax; jmp T; "
     "xor eax,eax; mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x0016D6D0, 0x0016DA60, 0x00199DB0),
     "NativeAdapter.ContainerPopFront - EC-7 family C\n"
     "if [this+0x48] nonzero: take head [this+0x30]->+0x20, dec the count, call\n"
     "# shared 0016D6D0 + 0016DA60 on the node, vcall [this+0x50] slot 3 with\n"
     "# r8=0x28, then shared 00199DB0 on this+0x58; optionally call a member op."
),
    ("nativeadapter-countedemberloop.tsv", 146,
     "push rbx; push rdi; sub rsp,I; cmp M[rcx],I; mov rdi,rcx; "
     "mov ebx,edx; jne T; test edx,edx; je T; mov edx,ebx; call T; "
     "test ebx,ebx; je T; mov M[rsp],rbp; mov ebp,ebx; movzx ebx,M[rsp]; "
     "mov M[rsp],rsi; xor esi,esi; mov M[rsp],r14; nop M[rax]; "
     "mov rcx,M[rdi]; lea r8,M[rsp]; add rcx,rsi; lea rdx,M[rsp]; "
     "mov M[rsp],rcx; movzx r9d,bl; lea rcx,M[rdi]; call T; add rsi,I; "
     "sub rbp,I; jne T; mov r14,M[rsp]; mov rsi,M[rsp]; mov rbp,M[rsp]; "
     "cmp M[rdi],I; sete al; mov M[rdi],al; add rsp,I; pop rdi; pop rbx; ret",
     shared_any(0x00199DB0),
     "NativeAdapter.CountedEmberLoop - EC-7 family C\n"
     "if [this+0x90]==0 and arg1 nonzero: call a member op then loop arg1 times\n"
     "# calling shared 00199DB0 on this+0x20 with a stack record, stepping the\n"
     "# record source by 0xA."
),
    ("nativeleaf-bumpallocpop.tsv", 17,
     "mov rax,M[rcx]; mov M[rcx],rax; add rax,I; mov M[rcx],rax; ret",
     leaf,
     "NativeLeaf.BumpAllocPop - EC-7 family C\n"
     "rax=[this+0x10]; store to [this+0x30]; advance [this+0x10] by 0x10;\n"
     "# return."
),
    ("nativeadapter-multirecordvtableinit.tsv", 387,
     "mov M[rsp],rcx; push rbp; push rsi; push rdi; push r12; push r13; "
     "push r14; push r15; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; "
     "movzx ebp,r8b; mov r12d,edx; mov r14,rcx; xor edi,edi; "
     "mov M[rcx],rdi; mov M[rcx],rdi; mov M[rcx],rdi; add rcx,I; "
     "lea rdx,M[rip]; call T; nop; lea rdx,M[rip]; lea rcx,M[rsp]; call T; "
     "lea r15,M[r14]; mov M[rsp],r15; lea rbx,M[r15]; xor ecx,ecx; "
     "mov M[rbx],rcx; mov M[rbx],rcx; mov M[rbx],rcx; mov M[rbx],rcx; "
     "mov M[r15],edi; lea rcx,M[r15]; mov rdx,rax; call T; mov M[rbx],rbx; "
     "mov M[r15],rbx; mov M[r15],rdi; mov M[r15],dil; mov M[r15],edi; "
     "lea rdx,M[rip]; lea rcx,M[rsp]; call T; lea rsi,M[r14]; "
     "mov M[rsp],rsi; lea rbx,M[rsi]; xor ecx,ecx; mov M[rbx],rcx; "
     "mov M[rbx],rcx; mov M[rbx],rcx; mov M[rbx],rcx; mov M[rsi],edi; "
     "lea rcx,M[rsi]; mov rdx,rax; call T; mov M[rbx],rbx; mov M[rsi],rbx; "
     "mov M[rsi],rdi; mov M[rsi],dil; mov M[rsi],edi; lea rcx,M[r14]; "
     "call T; mov M[r14],bpl; mov edx,r12d; mov rcx,r14; call T; "
     "test r12d,r12d; je T; mov esi,r12d; movzx ebx,M[rsp]; mov rcx,M[r14]; "
     "add rcx,rdi; mov M[rsp],rcx; movzx r9d,bl; lea r8,M[rsp]; "
     "lea rdx,M[rsp]; mov rcx,r15; call T; add rdi,I; sub rsi,I; jne T; "
     "cmp M[r14],I; je T; lea rcx,M[r14]; call T; nop; mov rax,r14; "
     "mov rbx,M[rsp]; add rsp,I; pop r15; pop r14; pop r13; pop r12; "
     "pop rdi; pop rsi; pop rbp; ret",
     shared_any(0x00199DB0, 0x001EDF00, 0x005CC8A0, 0x005CD0A0),
     "NativeAdapter.MultiRecordVtableInit - EC-7 family C\n"
     "zero three qwords of the out record; install member vtables via shared\n"
     "# ctor stub 001EDF00 on this+0x18 and a stack record; zero-init the\n"
     "# this+0x20 sub-record; then run the longer init pipeline via shared\n"
     "# 00199DB0/005CC8A0/005CD0A0."
),
    ("nativeadapter-lazysingletonallocinit.tsv", 66,
     "sub rsp,I; mov M[rsp],I; mov rax,M[rip]; test rax,rax; jne T; "
     "mov ecx,I; call T; mov M[rsp],rax; test rax,rax; je T; mov rcx,rax; "
     "call T; nop; mov M[rip],rax; add rsp,I; ret",
     shared_any(0x00210EC0),
     "NativeAdapter.LazySingletonAllocInit - EC-7 family C\n"
     "if the member rip global is null: allocate a member-sized record via\n"
     "# shared 00210EC0, init it via a member op, store it to the global."
),
    ("nativeadapter-boundedrangecopycompare.tsv", 404,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; push r12; "
     "push r13; push r14; push r15; sub rsp,I; mov rbx,M[rcx]; "
     "lea rsi,M[rcx]; xor ebp,ebp; mov r12,r8; mov r15,rdx; mov r14,rcx; "
     "mov rdi,rsi; mov al,I; test rbx,rbx; je T; mov r13,M[r8]; "
     "mov rsi,M[r8]; sub rsi,r13; nop M[rax]; nop M[rax+rax]; "
     "mov rdx,M[rbx]; mov r8,rsi; mov rdi,M[rbx]; mov rcx,r13; sub rdi,rdx; "
     "cmp rdi,rsi; cmovl r8,rdi; call T; test eax,eax; jne T; cmp rsi,rdi; "
     "jge T; or eax,I; jmp T; cmp rsi,rdi; mov eax,ebp; setg al; shr eax,I; "
     "mov rdi,rbx; test al,al; je T; mov rbx,M[rbx]; jmp T; mov rbx,M[rbx]; "
     "test rbx,rbx; jne T; lea rsi,M[r14]; mov r13,rdi; test al,al; je T; "
     "cmp rdi,M[r14]; je T; mov rcx,rdi; call T; mov rdi,rax; "
     "mov rdx,M[r12]; mov rcx,M[rdi]; mov rbx,M[rdi]; mov rsi,M[r12]; "
     "sub rbx,rcx; sub rsi,rdx; mov r8,rbx; cmp rsi,rbx; cmovl r8,rsi; "
     "call T; test eax,eax; jne T; cmp rbx,rsi; jl T; mov eax,ebp; setg al; "
     "test eax,eax; js T; mov M[r15],rdi; mov M[r15],bpl; jmp T; "
     "cmp rdi,rsi; je T; lea r8,M[rdi]; mov rdx,r12; mov rcx,r14; call T; "
     "test al,al; jne T; mov ebp,I; mov rdx,r12; mov rcx,r14; call T; "
     "mov r8,rsi; mov rdx,rdi; jmp T; lea rdi,M[r14]; cmp r13,rdi; je T; "
     "lea r8,M[r13]; mov rdx,r12; mov rcx,r14; call T; test al,al; jne T; "
     "mov ebp,I; mov rdx,r12; mov rcx,r14; call T; mov r8,rdi; mov rdx,r13; "
     "mov r9d,ebp; mov rcx,rax; mov rbx,rax; call T; inc M[r14]; "
     "mov M[r15],rbx; mov M[r15],I; mov rbx,M[rsp]; mov rax,r15; "
     "mov rbp,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop r15; pop r14; pop r13; "
     "pop r12; pop rdi; ret",
     shared_any(0x0016D720, 0x0016D840, 0x001A3100, 0x00861ED2),
     "NativeAdapter.BoundedRangeCopyCompare - EC-7 family C\n"
     "bounded copy/compare over the [r8] range into [rcx+8]-anchored storage:# per window call member ops and shared 0016D720/0016D840/001A3100 with# shared 00861ED2 (memcmp) verification; 404B five-call pipeline."
),
]

def load_sections(d):
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    n = struct.unpack_from("<H", d, pe + 6)[0]
    o = pe + 24 + struct.unpack_from("<H", d, pe + 20)[0]
    secs = []
    for _ in range(n):
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((va, max(vsz, rsz), rptr)); o += 40
    return secs

def form_and_targets(md, d, secs, a, size):
    r = a - BASE
    off = next((rp + (r - sva) for sva, sl, rp in secs if sva <= r < sva + sl), None)
    toks, calls, jmps, jccs, imms, memw = [], set(), set(), set(), [], []
    for ins in md.disasm(d[off:off + size], a):
        ops = []
        for op in ins.operands:
            if op.type == X86_OP_REG:
                ops.append(md.reg_name(op.reg))
            elif op.type == X86_OP_IMM:
                if ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j"):
                    ops.append("T")
                    if not (a <= op.imm < a + size):
                        if ins.mnemonic == "call": calls.add(op.imm)
                        elif ins.mnemonic == "jmp": jmps.add(op.imm)
                        else: jccs.add(op.imm)
                else:
                    ops.append("I")
                    imms.append(op.imm)
            elif op.type == X86_OP_MEM:
                memw.append(op.size)
                ops.append("M[rip]" if op.mem.base == X86_REG_RIP else
                           "M[%s%s]" % (md.reg_name(op.mem.base) if op.mem.base else "",
                                        "+" + md.reg_name(op.mem.index) if op.mem.index else ""))
        toks.append((ins.mnemonic + " " + ",".join(ops)).strip())
    return "; ".join(toks), calls, jmps, jccs, {"imms": imms, "memw": memw, "size": size}

def prior_members(tsv):
    p = os.path.join(ROOT, tsv)
    out = set()
    if os.path.exists(p):
        for l in io.open(p, encoding="utf-8", errors="replace"):
            t = l.split("#")[0].split("\t")[0].strip()
            try: out.add(int(t.split()[0], 16))
            except (ValueError, IndexError): pass
    return out

def main():
    write = "--write" in sys.argv
    sizes = CD.load_functions(None)
    res = CD.evaluate(CD.DEFAULT_DB, sizes)
    frontier = res["frontier_set"]
    a_set = res["explained_set"] - res["claimed_set"]
    d = open(EXE, "rb").read()
    secs = load_sections(d)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    priors = {tsv: prior_members(tsv) for tsv, _, _, _, _ in FAMILIES}
    pool = set(frontier)
    for tsv in priors:
        pool |= (priors[tsv] - a_set)
    cache = {a: form_and_targets(md, d, secs, a, sizes[a]) for a in pool if a in sizes}
    ok = True
    results = {}
    for tsv, sz, skel, tcheck, header in FAMILIES:
        members = sorted(a for a, (f, c, j, x, m) in cache.items()
                         if (sz is None or sizes[a] == sz) and f == norm(skel)
                         and tcheck(m, c, j, x))
        if not members:
            print("REFUSE %s: skeleton matched nobody" % tsv); ok = False; continue
        bad = [a for a in members if a in a_set]
        if bad:
            print("REFUSE %s: %d member(s) measure A" % (tsv, len(bad))); ok = False; continue
        results[tsv] = (members, header)
        tg = collections.Counter(t for a in members for t in cache[a][1] | cache[a][2] | cache[a][3])
        print("%-46s %3d members | targets %s" %
              (tsv, len(members), ", ".join("%08X x%d" % kv for kv in tg.most_common(6))))
    if not ok or not write:
        print("dry run" if ok else "refused"); return
    for tsv, (members, header) in results.items():
        with io.open(os.path.join(ROOT, tsv), "w", encoding="utf-8", newline="\n") as f:
            f.write("# " + header.replace("\n", "\n# ") + "\n")
            f.write("address\ttargets\n")
            for a in members:
                tg = sorted(cache[a][1] | cache[a][2] | cache[a][3])
                f.write("%08X\t%s\n" % (a, ",".join("%08X" % t for t in tg)))
        print("wrote", tsv, len(members))

if __name__ == "__main__":
    main()
