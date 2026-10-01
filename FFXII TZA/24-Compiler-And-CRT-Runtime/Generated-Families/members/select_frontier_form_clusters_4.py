"""select_frontier_form_clusters_4.py - EC-7 family C member selectors, fourth
pass over the live frontier form census (SWE2-EC7-FRONTIER-FORM-CLUSTERS-4),
declared on generated-function-families.md. Sub-threshold tail: every group
is ONE operand-aware instruction-form skeleton at a fixed body size with
exactly 4 members.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_frontier_form_clusters_4.py [--write]
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
    ("nativeadapter-floatfetchpushforward.tsv", 88,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; sub rsp,I; "
     "mov rbp,rcx; mov rbx,r9; mov rcx,rdx; mov rdi,r8; mov rsi,rdx; "
     "call T; movaps xmm1,xmm0; mov rcx,rbx; call T; mov r9,rbx; "
     "mov r8,rdi; mov rdx,rsi; mov rcx,rbp; mov rbx,M[rsp]; mov rbp,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; jmp T",
     shared_any(0x00267F60),
     "NativeAdapter.FloatFetchPushForward - EC-7 family C\n"
     "call a member float-fetch producing xmm0; push the float via shared\n"
     "# VMValueStack_PushFloat32Bits 00267F60; tail-dispatch to a member op\n"
     "# forwarding this + arg3 + arg4."
),
    ("nativeadapter-globalslotflagclearops.tsv", 94,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; movsxd rdi,ecx; "
     "lea rcx,M[rip]; mov rsi,M[rcx+rdi]; mov rbx,rsi; btr rbx,I; "
     "mov M[rcx+rdi],rbx; test rbx,I; jne T; mov ecx,edi; call T; "
     "and M[rax],I; test rsi,rsi; je T; test rbx,rbx; jne T; mov ecx,edi; "
     "call T; mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     shared_any(0x00263FF0, 0x0032F1B0),
     "NativeAdapter.GlobalSlotFlagClearOps - EC-7 family C\n"
     "clear bit 13 of a member global slot-table entry indexed by arg1; if the\n"
     "# entry empties call shared 00263FF0 and clear bit 3 of [rax+0x11]; if the\n"
     "# entry was already empty call shared 0032F1B0."
),
    ("nativeadapter-fanoutfieldupdate5.tsv", 94,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov ebx,edx; mov rdi,rcx; "
     "call T; lea rcx,M[rdi]; mov edx,ebx; call T; lea rcx,M[rdi]; "
     "mov edx,ebx; call T; lea rcx,M[rdi]; mov edx,ebx; call T; "
     "lea rcx,M[rdi]; mov edx,ebx; call T; mov rbx,M[rsp]; lea rax,M[rdi]; "
     "add rsp,I; pop rdi; ret",
     form_only,
     "NativeAdapter.FanoutFieldUpdate5 - EC-7 family C\n"
     "call a member op on this, then invoke member field-subobject ops at five\n"
     "# fixed member offsets (e.g. +0xD0/+0x160/+0x1F0/+0x270) forwarding arg2;\n"
     "# return &this[+0x280]-style tail field. External call count varies because\n"
     "# some member callees fall inside a sibling member's body range."
),
    ("nativeadapter-fanoutfieldupdate4.tsv", 80,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov ebx,edx; mov rdi,rcx; "
     "call T; lea rcx,M[rdi]; mov edx,ebx; call T; lea rcx,M[rdi]; "
     "mov edx,ebx; call T; lea rcx,M[rdi]; mov edx,ebx; call T; "
     "mov rbx,M[rsp]; lea rax,M[rdi]; add rsp,I; pop rdi; ret",
     form_only,
     "NativeAdapter.FanoutFieldUpdate4 - EC-7 family C\n"
     "same fan-out idiom as FanoutFieldUpdate5 with four fixed-offset field ops\n"
     "# and a +0x39C-style tail field return."
),
    ("nativeleaf-vectcountfloatorconst.tsv", 69,
     "mov rdx,M[rcx]; movabs rax,I; sub rdx,M[rcx]; imul rdx; sar rdx,I; "
     "mov rax,rdx; shr rax,I; add rdx,rax; test edx,edx; jne T; "
     "movss xmm0,M[rip]; ret; cmp M[rcx],I; jne T; xorps xmm0,xmm0; ret; "
     "mov rax,M[rcx]; movss xmm0,M[rax]; ret",
     leaf,
     "NativeLeaf.VectCountFloatOrConst - EC-7 family C\n"
     "vector element count via /20 magic multiply on ([+0x60]-[+0x58]); if\n"
     "# nonzero return the member rip float constant, else if [+0x10]==0 return\n"
     "# 0.0f else return [[+0x18]+0x24]."
),
    ("nativeleaf-floatbankglobalpublish.tsv", 644,
     "push rbx; sub rsp,I; mov rax,M[rcx]; mov rbx,rcx; movaps xmm1,M[rip]; "
     "mov rdx,rcx; movups M[rip],xmm1; mov M[rip],rcx; movups xmm2,M[rcx]; "
     "mov M[rip],rax; movss xmm0,M[rip]; addss xmm1,xmm2; "
     "movups M[rip],xmm2; movss M[rip],xmm1; movaps xmm1,xmm2; "
     "shufps xmm1,xmm2,I; addss xmm0,xmm1; movaps xmm1,xmm2; "
     "shufps xmm1,xmm2,I; shufps xmm2,xmm2,I; movss M[rip],xmm0; "
     "movss xmm0,M[rip]; addss xmm0,xmm1; movss M[rip],xmm0; "
     "movss xmm0,M[rip]; addss xmm0,xmm2; movss M[rip],xmm0; "
     "movups xmm1,M[rip]; movaps M[rip],xmm1; mov rcx,M[rcx]; test rcx,rcx; "
     "je T; call T; lea rdx,M[rip]; lea rcx,M[rip]; call T; mov rdx,M[rip]; "
     "mov rax,M[rip]; movaps xmm1,M[rip]; movdqa M[rdx],xmm1; cmp M[rax],I; "
     "je T; movss xmm0,M[rax]; movaps xmm3,M[rip]; movss xmm2,M[rip]; "
     "movss M[rip],xmm0; movss xmm1,M[rax]; movss M[rip],xmm1; "
     "movaps xmm0,M[rip]; movss xmm1,M[rip]; movups M[rip],xmm0; "
     "subss xmm1,xmm3; movaps M[rsp],xmm6; movaps xmm0,xmm3; "
     "shufps xmm0,xmm3,I; subss xmm2,xmm0; movaps xmm0,xmm3; "
     "shufps xmm0,xmm3,I; movss M[rip],xmm1; movss xmm1,M[rip]; "
     "movups M[rip],xmm3; movss M[rip],xmm2; subss xmm1,xmm0; "
     "movss xmm2,M[rip]; shufps xmm3,xmm3,I; subss xmm2,xmm3; "
     "movss M[rip],xmm1; movss M[rip],xmm2; call T; movss xmm1,M[rip]; "
     "movss xmm6,M[rip]; movss xmm3,M[rip]; movaps xmm2,xmm6; "
     "movss xmm0,M[rip]; mulss xmm0,xmm0; mulss xmm1,xmm1; mulss xmm2,xmm0; "
     "movaps xmm0,xmm6; mulss xmm0,xmm1; movss M[rip],xmm1; "
     "movaps xmm1,xmm6; mulss xmm3,xmm3; addss xmm2,xmm0; mulss xmm1,xmm3; "
     "movss M[rip],xmm3; movss M[rip],xmm2; addss xmm1,xmm2; "
     "cvtps2pd xmm0,xmm1; movss M[rip],xmm1; andps xmm0,M[rip]; "
     "cvtpd2ps xmm0,xmm0; call T; movss xmm1,M[rip]; movss xmm2,M[rip]; "
     "addss xmm6,xmm1; addss xmm1,xmm0; movss M[rip],xmm0; "
     "movss M[rip],xmm6; comiss xmm2,xmm1; ja T; movaps xmm1,xmm2; "
     "movss xmm0,M[rip]; mulss xmm0,xmm1; subss xmm6,xmm0; "
     "movss M[rip],xmm6; movups xmm1,M[rip]; movaps xmm6,M[rsp]; "
     "movaps M[rip],xmm1; movss M[rbx],xmm1; add rsp,I; pop rbx; ret; "
     "mov M[rbx],I; add rsp,I; pop rbx; ret",
     shared_any(0x0036DD80, 0x00398F90, 0x0039AF70, 0x00861F14),
     "NativeLeaf.FloatBankGlobalPublish - EC-7 family C\n"
     "publish a this+0x60 xmm vector into member rip float slots with shufps\n"
     "# lane extraction and adds; store this into a member rip pointer; then run\n"
     "# a longer pipeline using shared 0039AF70/00398F90/0036DD80/00861F14."
),
    ("nativeleaf-twofloatstore.tsv", 17,
     "movss M[rcx],xmm1; movss M[rcx],xmm2; ret",
     leaf,
     "NativeLeaf.TwoFloatStore - EC-7 family C\n"
     "store xmm1->[+0x1E8] and xmm2->[+0x1EC]; return."
),
    ("nativeadapter-nullablerecordwordtail.tsv", 31,
     "test rcx,rcx; je T; mov rax,M[rcx]; test rax,rax; je T; cmp M[rax],I; "
     "je T; movzx ecx,M[rax]; jmp T; ret",
     targets_exact(0, 1, 0),
     "NativeAdapter.NullableRecordWordTail - EC-7 family C\n"
     "if this and this[+0xC0] non-null and [rec]!=-1, movzx the record word and\n"
     "# tail-dispatch to a member op."
),
    ("nativeleaf-globalqwordstore.tsv", 10,
     "mov eax,ecx; mov M[rip],rax; ret",
     leaf,
     "NativeLeaf.GlobalQwordStore - EC-7 family C\n"
     "mov eax,ecx; store rax to a member rip qword; return."
),
    ("nativeadapter-popthreeintforwardtail.tsv", 89,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rcx,r9; "
     "mov rbx,r9; call T; mov rcx,rbx; mov esi,eax; call T; mov rcx,rbx; "
     "mov edi,eax; call T; mov ecx,eax; call T; mov rcx,rax; call T; "
     "mov r8d,esi; mov edx,edi; mov rcx,rax; mov rbx,M[rsp]; "
     "mov rsi,M[rsp]; add rsp,I; pop rdi; jmp T",
     shared_any(0x00263F10, 0x00264010, 0x00267E10),
     "NativeAdapter.PopThreeIntForwardTail - EC-7 family C\n"
     "pop three ints from the arg record via shared VMValueStack_\n"
     "# PopInt32CoerceFloat32 00267E10; compose via shared 00264010 + 00263F10;\n"
     "# tail-dispatch to a member op with (result,arg2,arg3)."
),
    ("nativeadapter-flagbyteconditionalop.tsv", 64,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; cmp M[rdx],I; je T; "
     "lea rdx,M[rip]; mov ecx,I; call T; mov rcx,M[rbx]; test rcx,rcx; "
     "je T; call T; nop; mov al,I; add rsp,I; pop rbx; ret",
     shared_any(0x005CDAA0, 0x006108C0),
     "NativeAdapter.FlagByteConditionalOp - EC-7 family C\n"
     "if [arg1+8]!=0, call shared 005CDAA0 with ecx=3 + member rip arg; if\n"
     "# [arg1+0x20] non-null call shared 006108C0 on it; return 1."
),
    ("nativeleaf-largefloatglobalpublish.tsv", 1118,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; push r14; "
     "push r15; sub rsp,I; mov rax,M[rip]; xor rax,rsp; mov M[rsp],rax; "
     "mov rdi,M[rcx]; mov rbx,rcx; mov r8d,M[rcx]; lea rcx,M[rsp]; "
     "lea rdx,M[rdi]; call T; movaps xmm0,M[rax]; movdqa M[rbx],xmm0; "
     "test M[rdi],I; je T; movups M[rip],xmm0; movups xmm2,M[rbx]; "
     "movups xmm1,xmm0; movss xmm0,M[rip]; addss xmm1,xmm2; "
     "movups M[rip],xmm2; movss M[rip],xmm1; movaps xmm1,xmm2; "
     "shufps xmm1,xmm2,I; addss xmm0,xmm1; movaps xmm1,xmm2; "
     "shufps xmm1,xmm2,I; shufps xmm2,xmm2,I; movss M[rip],xmm0; "
     "movss xmm0,M[rip]; addss xmm0,xmm1; movss M[rip],xmm0; "
     "movss xmm0,M[rip]; addss xmm0,xmm2; movss M[rip],xmm0; "
     "movups xmm0,M[rip]; movups M[rbx],xmm0; mov r8d,M[rbx]; "
     "lea rdx,M[rdi]; lea rcx,M[rsp]; call T; movaps xmm0,M[rax]; "
     "mov rax,M[rbx]; movdqa M[rbx],xmm0; test M[rax],I; je T; "
     "movups M[rip],xmm0; movups xmm2,M[rbx]; movups xmm1,xmm0; "
     "movss xmm0,M[rip]; mulss xmm1,xmm2; movups M[rip],xmm2; "
     "movss M[rip],xmm1; movaps xmm1,xmm2; shufps xmm1,xmm2,I; "
     "mulss xmm0,xmm1; movaps xmm1,xmm2; shufps xmm1,xmm2,I; "
     "shufps xmm2,xmm2,I; movss M[rip],xmm0; movss xmm0,M[rip]; "
     "mulss xmm0,xmm1; movss M[rip],xmm0; movss xmm0,M[rip]; "
     "mulss xmm0,xmm2; movss M[rip],xmm0; movups xmm0,M[rip]; "
     "movups M[rbx],xmm0; mov r8d,M[rbx]; lea rdx,M[rdi]; lea rcx,M[rsp]; "
     "call T; lea rsi,M[rbx]; lea rbp,M[rbx]; mov rdx,rbp; lea rcx,M[rbx]; "
     "movaps xmm0,M[rax]; movdqa M[rsi],xmm0; movzx r8d,M[rdi]; call T; "
     "movups xmm1,M[rsi]; movups M[rip],xmm1; movups xmm2,M[rbx]; "
     "movss xmm0,M[rip]; addss xmm1,xmm2; movups M[rip],xmm2; "
     "movss M[rip],xmm1; movaps xmm1,xmm2; shufps xmm1,xmm2,I; "
     "addss xmm0,xmm1; movaps xmm1,xmm2; shufps xmm1,xmm2,I; "
     "shufps xmm2,xmm2,I; movss M[rip],xmm0; movss xmm0,M[rip]; "
     "addss xmm0,xmm1; movss M[rip],xmm0; movss xmm0,M[rip]; "
     "addss xmm0,xmm2; movss M[rip],xmm0; movups xmm0,M[rip]; "
     "movups M[rsi],xmm0; mov rcx,M[rbx]; test rcx,rcx; je T; call T; "
     "mov rdx,rsi; mov rcx,rsi; call T; test M[rdi],I; jne T; "
     "mov rcx,M[rbx]; mov rdx,rbp; add rcx,I; call T; movaps xmm0,M[rbx]; "
     "movdqa M[rbx],xmm0; movaps xmm1,M[rsi]; movdqa M[rbx],xmm1; "
     "movzx eax,M[rdi]; and al,I; cmp al,I; jne T; mov rdx,rbx; "
     "lea rcx,M[rsp]; call T; mov r8,rbp; lea rcx,M[rsp]; mov rdx,rbp; "
     "movaps xmm0,M[rax]; movaps M[rsp],xmm0; movaps xmm1,M[rax]; "
     "movaps M[rsp],xmm1; movaps xmm0,M[rax]; movaps M[rsp],xmm0; "
     "movaps xmm1,M[rax]; movaps M[rsp],xmm1; mov M[rsp],I; mov M[rsp],I; "
     "mov M[rsp],I; call T; test M[rdi],I; lea rdx,M[rbx]; mov rcx,rbp; "
     "je T; call T; jmp T; call T; movaps xmm0,M[rsi]; lea rcx,M[rdi]; "
     "movups M[rbx],xmm0; mov M[rbx],I; mov edx,M[rbx]; call T; "
     "mov M[rbx],eax; cmp M[rbx],I; je T; lea r8,M[rbx]; lea rdx,M[rbx]; "
     "lea rcx,M[rbx]; call T; mov edx,M[rbx]; lea rcx,M[rdi]; call T; "
     "mov M[rbx],eax; cmp M[rbx],I; je T; lea r8,M[rbx]; lea rdx,M[rbx]; "
     "lea rcx,M[rbx]; call T; cmp M[rdi],I; jb T; mov edx,M[rbx]; "
     "lea rcx,M[rdi]; call T; mov r8d,eax; cmp eax,I; je T; "
     "movzx ecx,M[rbx]; mov eax,I; imul ecx,r8d; imul ecx; mov eax,I; "
     "sar edx,I; mov ecx,edx; shr ecx,I; add edx,ecx; movzx ecx,M[rbx]; "
     "mov M[rbx],dl; imul ecx,r8d; imul ecx; sar edx,I; mov eax,edx; "
     "shr eax,I; add edx,eax; mov M[rbx],dl; mov eax,M[rbx]; mov rdx,rsi; "
     "mov rcx,rdi; mov M[rbx],eax; call T; test eax,eax; jne T; "
     "mov rdx,M[rbx]; mov rcx,rbx; call T; jmp T; mov rdx,rbx; mov ecx,I; "
     "call T; mov rcx,M[rsp]; xor rcx,rsp; call T; lea r11,M[rsp]; "
     "mov rbx,M[r11]; mov rbp,M[r11]; mov rsi,M[r11]; mov rsp,r11; pop r15; "
     "pop r14; pop rdi; ret",
     shared_any(0x0026EE00, 0x002F31C0, 0x002F3570, 0x003970F0, 0x00397910, 0x00397ED0, 0x00398480, 0x00398F90, 0x0039ADE0, 0x0039AF70, 0x003A8950, 0x0042FDB0, 0x00430B90, 0x004314E0, 0x005002E0, 0x00808C40),
     "NativeLeaf.LargeFloatGlobalPublish - EC-7 family C\n"
     "stack-cookie frame; copy a member record via 00430B90 into this+0x110;\n"
     "# publish a long xmm/float bank into member rip slots; then run a 16-shared-\n"
     "# callee pipeline (0026EE00/002F31C0/00397xxx/004314E0/00808C40 family)."
),
    ("nativeadapter-popthreefloatguardtail.tsv", 122,
     "push rbx; sub rsp,I; movaps M[rsp],xmm6; mov rcx,r9; "
     "movaps M[rsp],xmm7; mov rbx,r9; movaps M[rsp],xmm8; call T; "
     "mov rcx,rbx; movaps xmm8,xmm0; call T; mov rcx,rbx; movaps xmm7,xmm0; "
     "call T; mov rcx,rbx; movaps xmm6,xmm0; call T; mov ecx,eax; "
     "mov ebx,eax; call T; mov ecx,ebx; call T; movsxd rcx,eax; "
     "movaps xmm3,xmm8; movaps xmm2,xmm7; movaps xmm1,xmm6; "
     "movaps xmm6,M[rsp]; movaps xmm7,M[rsp]; movaps xmm8,M[rsp]; "
     "add rsp,I; pop rbx; jmp T",
     shared_any(0x0016D6A0, 0x00267DB0, 0x00267E10, 0x003EB700),
     "NativeAdapter.PopThreeFloatGuardTail - EC-7 family C\n"
     "pop three floats via shared VMValueStack_PopNumericDiscard 00267DB0 into\n"
     "# xmm6..xmm8; pop an int via 00267E10; call 0016D6A0 (ICF-folded stub) and\n"
     "# shared 003EB700; tail-dispatch to a member op with xmm1..xmm3."
),
    ("nativeleaf-doublecallbool.tsv", 25,
     "sub rsp,I; call T; mov rcx,rax; call T; movzx eax,al; add rsp,I; ret",
     targets_exact(2, 0, 0),
     "NativeLeaf.DoubleCallBool - EC-7 family C\n"
     "call a member op; call a second member op on the result; return\n"
     "# movzx(eax,al)."
),
    ("nativeadapter-zerosecondargtailcall.tsv", 10,
     "mov r8d,edx; xor edx,edx; jmp T",
     targets_exact(0, 1, 0),
     "NativeAdapter.ZeroSecondArgTailCall - EC-7 family C\n"
     "r8d=arg2; edx=0; tail-dispatch to a member op. Sibling of\n"
     "# ConstantFirstArgumentTailCall (which sets ecx)."
),
    ("nativeadapter-nullablefetchbytetail.tsv", 46,
     "push rbx; sub rsp,I; movzx ebx,cl; call T; test rax,rax; je T; "
     "call T; mov rcx,rax; movzx edx,bl; add rsp,I; pop rbx; jmp T; "
     "add rsp,I; pop rbx; ret",
     targets_exact(1, 1, 0),
     "NativeAdapter.NullableFetchByteTail - EC-7 family C\n"
     "save arg1 byte; call a member fetch; if non-null fetch again and\n"
     "# tail-dispatch to a member op with (result,saved byte)."
),
    ("nativeleaf-liststringcompare.tsv", 87,
     "mov r10,rdx; test rdx,rdx; jne T; xor eax,eax; ret; mov r8,M[rip]; "
     "test r8,r8; je T; nop M[rax+rax]; mov rax,M[r8]; mov r9,r10; "
     "sub r9,rax; nop M[rax]; movzx edx,M[rax]; movzx ecx,M[rax+r9]; "
     "sub edx,ecx; jne T; inc rax; test ecx,ecx; jne T; test edx,edx; je T; "
     "mov r8,M[r8]; test r8,r8; jne T; xor r8d,r8d; mov rax,r8; ret",
     leaf,
     "NativeLeaf.ListStringCompare - EC-7 family C\n"
     "if arg1 null return 0; else walk a member rip linked list comparing each\n"
     "# node's string against arg1 byte-wise; return the matching node or 0."
),
    ("nativeadapter-setnefirstargtailcall.tsv", 14,
     "xor eax,eax; test ecx,ecx; setne al; mov ecx,eax; jmp T",
     targets_exact(0, 1, 0),
     "NativeAdapter.SetneFirstArgTailCall - EC-7 family C\n"
     "ecx = setne(arg1); tail-dispatch to a member op."
),
    ("nativeadapter-recordchaindoubleresolve.tsv", 231,
     "sub rsp,I; mov rax,M[rip]; xor rax,rsp; mov M[rsp],rax; "
     "movzx eax,M[rcx]; mov M[rsp],rcx; cmp ax,I; je T; movsx rax,ax; "
     "mov rdx,rcx; mov M[rsp],rbx; imul rbx,rax,I; add rbx,M[rip]; "
     "mov rcx,rbx; call T; test eax,eax; jne T; mov rcx,rbx; call T; "
     "movzx eax,M[rbx]; cmp ax,I; je T; mov rdx,M[rsp]; movsx rax,ax; "
     "imul rbx,rax,I; add rbx,M[rip]; mov rcx,rbx; call T; test eax,eax; "
     "jne T; mov rcx,rbx; call T; movzx ecx,M[rbx]; cmp cx,I; je T; "
     "lea r8,M[rsp]; lea rdx,M[rip]; call T; movzx ecx,M[rbx]; cmp cx,I; "
     "je T; lea r8,M[rsp]; lea rdx,M[rip]; call T; mov rbx,M[rsp]; "
     "mov rcx,M[rsp]; xor rcx,rsp; call T; add rsp,I; ret",
     shared_any(0x00426220, 0x0042EF90, 0x00808C40),
     "NativeAdapter.RecordChainDoubleResolve - EC-7 family C\n"
     "stack-cookie frame; resolve a word id through the 0x740-stride record\n"
     "# table via shared 00426220; on the resolved record resolve its +8 word the\n"
     "# same way; member ops verify each hop; shared 0042EF90 + cookie 00808C40."
),
    ("nativeadapter-handlerecordoutfloatinit.tsv", 116,
     "push rbx; sub rsp,I; mov rbx,rdx; call T; test rax,rax; je T; "
     "mov rax,M[rax]; test rax,rax; je T; cmp M[rax],I; je T; "
     "movzx ecx,M[rax]; cmp cx,I; je T; movsx rax,cx; imul rcx,rax,I; "
     "add rcx,M[rip]; je T; cmp M[rcx],I; je T; mov rdx,rbx; call T; "
     "mov M[rbx],I; add rsp,I; pop rbx; ret; xor eax,eax; mov M[rbx],rax; "
     "mov M[rbx],eax; mov M[rbx],I; add rsp,I; pop rbx; ret",
     shared_any(0x003588B0),
     "NativeAdapter.HandleRecordOutFloatInit - EC-7 family C\n"
     "resolve arg1 via shared ActorHandle_ResolveRegistryEntryByPackedId\n"
     "# 003588B0; chase [rax+0xC0]->word through the 0x740-stride table requiring\n"
     "# +0x284 set; call a member op on arg2 then store 1.0f at [arg2+0xC]; on\n"
     "# failure zero the out record and still store 1.0f."
),
    ("nativeleaf-clampedindextablestore.tsv", 57,
     "cmp ecx,I; jge T; test ecx,ecx; jns T; xor ecx,ecx; movsxd rax,ecx; "
     "imul rcx,rax,I; lea rax,M[rip]; mov M[rcx+rax],edx; ret; mov eax,I; "
     "cmp ecx,eax; cmovg ecx,eax; movsxd rax,ecx; imul rcx,rax,I; "
     "lea rax,M[rip]; mov M[rcx+rax],edx; ret",
     leaf,
     "NativeLeaf.ClampedIndexTableStore - EC-7 family C\n"
     "clamp arg1 into [0,member bound]; store arg2 into a member rip table at\n"
     "# member stride."
),
    ("nativeadapter-predicateguardsharedcall.tsv", 43,
     "push rbx; sub rsp,I; mov rbx,rcx; call T; test eax,eax; jne T; "
     "add rsp,I; pop rbx; ret; mov rcx,rbx; call T; mov eax,I; add rsp,I; "
     "pop rbx; ret",
     shared_any(0x002F2D60),
     "NativeAdapter.PredicateGuardSharedCall - EC-7 family C\n"
     "call a member predicate on this; if zero return 0; else call shared\n"
     "# 002F2D60 on this and return a member constant."
),
    ("nativeadapter-predicateguardconstcall.tsv", 40,
     "sub rsp,I; call T; test eax,eax; je T; mov ecx,I; call T; mov eax,I; "
     "add rsp,I; ret; xor eax,eax; add rsp,I; ret",
     shared_any(0x00314D40),
     "NativeAdapter.PredicateGuardConstCall - EC-7 family C\n"
     "call a member op; if zero return 0; else call shared 00314D40 with a\n"
     "# member ecx constant and return a member constant."
),
    ("nativeleaf-flagbit2setclear.tsv", 16,
     "and M[rcx],I; test edx,edx; setne al; shl al,I; or M[rcx],al; ret",
     leaf,
     "NativeLeaf.FlagBit2SetClear - EC-7 family C\n"
     "clear a member flag bit at [rcx+X]; if arg2 nonzero set bit (1<<1);\n"
     "# return."
),
    ("nativeadapter-popintforwardtail.tsv", 30,
     "sub rsp,I; mov rcx,r9; call T; mov ecx,eax; call T; mov ecx,eax; "
     "add rsp,I; jmp T",
     shared_any(0x00267E10),
     "NativeAdapter.PopIntForwardTail - EC-7 family C\n"
     "pop an int from arg2 via shared 00267E10; call a member op on it;\n"
     "# tail-dispatch to a member op."
),
    ("nativeadapter-nullablefirstmembertail.tsv", 17,
     "mov rcx,M[rcx]; test rcx,rcx; jne T; ret",
     targets_exact(0, 0, 1),
     "NativeAdapter.NullableFirstMemberTail - EC-7 family C\n"
     "rcx=[this+X]; if non-null tail-dispatch via jcc to a member op. jcc\n"
     "# carries the member target."
),
    ("nativeadapter-boolargfetchresulttail.tsv", 32,
     "push rbx; sub rsp,I; test ecx,ecx; setne bl; call T; mov rcx,rax; "
     "movzx edx,bl; add rsp,I; pop rbx; jmp T",
     targets_exact(1, 1, 0),
     "NativeAdapter.BoolArgFetchResultTail - EC-7 family C\n"
     "bl=setne(arg1); call a member fetch; tail-dispatch to a member op with\n"
     "# (result,saved bool)."
),
    ("nativeleaf-globalarrayflagscan.tsv", 89,
     "lea rcx,M[rip]; lea rdx,M[rip]; nop; mov rax,M[rcx]; test rax,rax; "
     "je T; test M[rax],I; je T; test M[rax],I; jne T; cmp M[rax],I; jl T; "
     "add rcx,I; cmp rcx,rdx; jl T; jmp T; xor eax,eax; ret; cmp M[rip],I; "
     "mov eax,I; mov ecx,I; cmove eax,ecx; ret",
     targets_exact(0, 1, 0),
     "NativeLeaf.GlobalArrayFlagScan - EC-7 family C\n"
     "scan a member rip pointer-array range for an entry whose [+0x40] bit4 is\n"
     "# set, [+0x3E8] &0x700 clear and [+0x3C5]>=0; tail-dispatch to a member op\n"
     "# or return 0 / a member-const-selected flag word."
),
    ("nativeadapter-zerofirstargtailcall.tsv", 7,
     "xor ecx,ecx; jmp T",
     targets_exact(0, 1, 0),
     "NativeAdapter.ZeroFirstArgTailCall - EC-7 family C\n"
     "ecx=0; tail-dispatch to a member op. Sibling of\n"
     "# ConstantFirstArgumentTailCall (imm is always 0 here)."
),
    ("nativeadapter-vtableinstalltail.tsv", 15,
     "lea rax,M[rip]; mov M[rcx],rax; jmp T",
     targets_exact(0, 1, 0),
     "NativeAdapter.VtableInstallTail - EC-7 family C\n"
     "install a member rip vtable at [this]; tail-dispatch to a member op."
),
    ("nativeleaf-flagbit1setclear.tsv", 14,
     "test dl,dl; je T; or M[rcx],I; ret; and M[rcx],I; ret",
     leaf,
     "NativeLeaf.FlagBit1SetClear - EC-7 family C\n"
     "if arg2 nonzero or [this+0x20] with 2 else and it with ~2; return."
),
    ("nativeleaf-nullablederefwordadd.tsv", 32,
     "mov rdx,M[rcx]; test rdx,rdx; je T; movzx eax,M[rdx]; test ax,ax; "
     "je T; movzx eax,ax; add eax,edx; cdqe; ret; xor eax,eax; ret",
     leaf,
     "NativeLeaf.NullableDerefWordAdd - EC-7 family C\n"
     "rdx=[this+X]; if non-null and [rdx] nonzero, return (u16)[rdx]+arg2\n"
     "# sign-extended; else 0."
),
    ("nativeadapter-indexedrecordstorecookie.tsv", 78,
     "sub rsp,I; mov rax,M[rip]; xor rax,rsp; mov M[rsp],rax; xor edx,edx; "
     "movsxd rax,ecx; mov M[rsp],edx; lea r8,M[rsp]; mov M[rsp],rdx; "
     "mov ecx,I; lea rdx,M[rip]; mov M[rsp],rax; call T; mov rcx,M[rsp]; "
     "xor rcx,rsp; call T; add rsp,I; ret",
     shared_any(0x00244F50, 0x00808C40),
     "NativeAdapter.IndexedRecordStoreCookie - EC-7 family C\n"
     "stack-cookie frame; build a stack record holding arg1 (index), a member\n"
     "# rip descriptor and scratch; call shared 00244F50; cookie-check via\n"
     "# 00808C40."
),
    ("nativeadapter-guardedrecordbuildcookie.tsv", 132,
     "mov r11,rsp; push rbx; sub rsp,I; mov rax,M[rip]; xor rax,rsp; "
     "mov M[rsp],rax; cmp M[rcx],I; mov rbx,rcx; jne T; mov M[r11],rcx; "
     "lea rax,M[r11]; xor ecx,ecx; mov M[rsp],edx; mov M[rsp],ecx; "
     "lea rdx,M[rip]; mov M[r11],rcx; mov M[r11],rcx; mov ecx,I; "
     "mov M[r11],r8d; lea r8,M[r11]; mov M[r11],rax; call T; "
     "mov M[rbx],rax; mov rdx,rax; mov rcx,M[rip]; call T; mov rcx,M[rsp]; "
     "xor rcx,rsp; call T; add rsp,I; pop rbx; ret",
     shared_any(0x00244F50, 0x00246AD0, 0x00808C40),
     "NativeAdapter.GuardedRecordBuildCookie - EC-7 family C\n"
     "stack-cookie frame; if [this+X] matches a member tag, build a stack\n"
     "# record via shared 00244F50 + 00246AD0, store the result at [this+Y];\n"
     "# cookie-check via 00808C40."
),
    ("nativeadapter-globalguardindexedcall.tsv", 41,
     "sub rsp,I; test M[rip],I; je T; or edx,I; lea ecx,M[rdx]; call T; "
     "add rsp,I; jmp T; add rsp,I; ret",
     shared_any(0x00225CD0, 0x00226280),
     "NativeAdapter.GlobalGuardIndexedCall - EC-7 family C\n"
     "if a member rip dword is nonzero, call shared 00225CD0 with (or-ed arg2\n"
     "# index); tail-dispatch to shared 00226280."
),
    ("nativeleaf-payloadbasebitextract.tsv", 27,
     "sub rsp,I; call T; movzx eax,M[rax]; shr eax,I; and eax,I; add rsp,I; "
     "ret",
     shared_any(0x002EF2B0),
     "NativeLeaf.PayloadBaseBitExtract - EC-7 family C\n"
     "call shared SaveImage_GetPersistentPayloadBase 002EF2B0; return\n"
     "# ([rax+X]>>n)&m bitfield."
),
    ("nativeleaf-payloadbaseflagset.tsv", 40,
     "push rbx; sub rsp,I; mov ebx,ecx; call T; and M[rax],I; test ebx,ebx; "
     "setne cl; shl cl,I; or M[rax],cl; add rsp,I; pop rbx; ret",
     shared_any(0x002EF2B0),
     "NativeLeaf.PayloadBaseFlagSet - EC-7 family C\n"
     "call shared 002EF2B0; clear a member mask bit in [rax+X]; if arg1 nonzero\n"
     "# set a member bit position."
),
    ("nativeleaf-threefloatstore.tsv", 25,
     "movss M[rcx],xmm1; movss M[rcx],xmm2; movss M[rcx],xmm3; ret",
     leaf,
     "NativeLeaf.ThreeFloatStore - EC-7 family C\n"
     "store xmm1->[+0x1C4], xmm2->[+0x1C8], xmm3->[+0x1CC] (member offsets);# return. Sibling of TwoFloatStore."
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
    # Pool per family (SWE2-EC7 2026-09-30, FABLE ruling point 3 on SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the
    # frontier less the UC-1 bodies (frontier by ruling) plus this family's OWN prior members; a body another
    # family owns, or that only another form file lists, is never taken. Selections outside it are reported.
    UC1F = set(CD.uc1_band.frontier_starts())
    others = res["claimed_set"] - set().union(*priors.values())
    pool_for = {tsv: (set(frontier) - UC1F) | (priors[tsv] - a_set - others) for tsv in priors}
    ok = True
    results = {}
    for tsv, sz, skel, tcheck, header in FAMILIES:
        members = sorted(a for a, (f, c, j, x, m) in cache.items()
                         if (sz is None or sizes[a] == sz) and f == norm(skel)
                         and tcheck(m, c, j, x))
        outside = [a for a in members if a not in pool_for[tsv]]
        if outside:
            print("  %s: %d form match(es) outside this family's pool (owned elsewhere / UC-1 / another file's prior), not taken: %s"
                  % (tsv, len(outside), " ".join("%08X" % a for a in outside[:12])))
        members = [a for a in members if a in pool_for[tsv]]
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
