"""select_frontier_form_clusters_2.py - EC-7 family C member selectors, second
pass over the live frontier form census (SWE2-EC7-FRONTIER-FORM-CLUSTERS-2),
declared on generated-function-families.md.

Every group is ONE operand-aware instruction-form skeleton over its byte
images; operand payloads and external-target structure refine the split where
a census cluster mixed operations or call arity:

  nullableoutrecordheaderinit (25B) - if the out-record pointer is non-null,
      write a member constant + two zero qwords into it; always return 1.
  stringkeyedchainattach (132B) - byte-compare walk over a global bucket chain
      keyed on a member rip table; attach the node at [this+0x10] at the head;
      return 0 on attach, member code 0x11/0x12 otherwise. No external calls.
  guardedsharedpairtailcall (44B) - call shared predicate 00280120; if zero,
      call shared bridge 00267E10 on r9, then tail-call a member-specific op
      with ecx=result.
  callresultdualtaildispatch (34B) - call shared bridge 00267E10 on r9;
      tail-call one of two member-specific ops selected on the result.
  memberfieldspantailcall (35B) - shuffle this->rdx, arg1->r9, load
      [this+0xE0]+0xD0 into rcx, r8=this+0x110; tail-call a member op.
  firstmemberinvokefieldstore (43B) - call a member op on [this]; on non-null
      store a member constant into a member field.
  conditionaldoublecallresulttailcall (44B) - save ecx; call member op; if
      the result is non-null call the member op again; forward
      (result2, saved-ecx) to a member tail target.
  callresultargshifttailcall (42B) - save edx->ebx, ecx->edi; call member op;
      forward (result, ecx, edx) to a member tail target.
  secondargumentzerotailcall (7B) / secondargumentconsttailcall (10B) /
      thirdargumentzerotailcall (8B) / fourthargumentzerotailcall (8B) - the
      argument-injecting tail-call spellings; ConstantFirstArgumentTailCall on
      this page is the ecx spelling and is a different form.
  constfirstargumentcalltailcall (23B) - ecx=member const; call a member op;
      tail-call a member op.
  serialrangeinvokeloop (85B) - iterate bx over a global serial range
      [rip]-relative base 0x1000..; invoke shared Items_License sink 003008A0
      with edx=0x63 per index.
  chainedmemberresulttailcall (40B) - call shared 00263F10 on rdx; call a
      member op on the result; forward (this, result2) to shared tail 0026B4E0.
  clampedtablelookup (83B) - bounds-checked read of a member rip table
      (stride 0x294), signed clamp arithmetic, word field fetch; no calls.
  callboolnormalizereturn (23B) - call a member op; return setne(al).
  globalhandlestateread (33B) - setne cl on a member global pointer; call the
      ICF-folded ret-0 stub 0016D6A0; return a second member global.
  doublederefflagextract (17B) - rax=[rcx+X]; eax=[[rax]+Y]>>k&1; ret.
  smallrecordvtablector (47B) - call shared init 00212CC0 on this; store arg1
      at +0x18; install a member vtable; return this.
  doubleselfinvoke (39B) - call the same member op on this twice.
  twosubobjectinvoketailcall (40B) - call a member op on this+0x58 then
      this+0x20; tail-call a member op on this.
  memberpredicatetreesearch (111B) - walk the intrusive tree at this+8,
      calling a member predicate per node; return the found flag.
  flaggatedinittailcall (62B) - if a member global flag is clear, zero two
      stack slots and call shared init 00226BE0; tail-call shared 00226280.
  twosharedcomposetailcall (49B) - call shared getter 002640C0; call shared
      bridge 00267E10 on the result arg; tail-call a member op.
  sharednormalizetailcallzero (79B) / sharednormalizetailcallone (82B) -
      call shared Movement normaliser 0026A1A0 with edx=0/edx=1; restore the
      caller's four args; tail-call a member op.
  guardedcallresultboolinvert (39B) - call shared predicate 00280120; if zero
      return 0; else call a member op and return sete(eax).
  outrecordzeroinitmemberinit (65B) - if the out pointer is non-null, memset
      it via shared import 00861EC0 (size 0x90) then call a member init.
  outrecordvtablepairstore (69B) - if the out pointer is non-null, call a
      member op on it and store two member rip pointers at +0/+8.
  twomanifoldcallindexedvcall (76B) - call member op on rdx; call member op
      on rdx again saving the result; if non-null vcall [this+8] with
      rax+[this+0x10].
  triplememberchainreturntrue (55B) - member predicate; if true call two
      more member ops on rdx; return 1.
  namedrecordregisterpair (39B) - call shared registrar 001FB840 with a
      member string; tail-call shared 0020E630 with a second member string.
  mallcorecordemplacetailcall (148B) - malloc(0x20) via shared 0085E730;
      member-construct the record; push-back into [this] end-pointer vector
      (fallback shared grow 001AB570); read global state via shared 0018B4E0;
      tail-call shared 0018AFF0.
  spancheckmembervcall (57B) - if the embedded sequence [this+X..this+Y] has
      more than one element and a non-null begin, vcall slot 3 on member +0x60.
  recursivespannodewalk (152B) - self-recursive tree walk; per node the same
      span-check + member vcall, then vcall [this+0x30] slot 3.
  fieldflagmaskclear - and [rcx+off], member mask; ret - flag-bit clear, byte
      and dword widths.
  fieldfloatgetter - movss xmm0, [rcx+off]; ret - displaced float getter.
  memberaddressaccessor / callthentailcall - EXTENSIONS of declared rows:
      same instruction form, more frontier members.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_frontier_form_clusters_2.py [--write]
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

ALIGNED_FREE = 0x00584730
RET0_STUB = 0x0016D6A0
BRIDGE = 0x00267E10
PREDICATE = 0x00280120
GETTER = 0x002640C0
MOVEMENT_NORM = 0x0026A1A0
SERIAL_SINK = 0x003008A0
INIT_16 = 0x00226BE0
AUDIO_TAIL = 0x00226280
CHAIN_FIRST = 0x00263F10
CHAIN_TAIL = 0x0026B4E0
MEMSET_IMPORT = 0x00861EC0
MALLOC = 0x0085E730
VEC_GROW = 0x001AB570
GLOBAL_READ = 0x0018B4E0
EMPLACE_TAIL = 0x0018AFF0
SMALL_INIT = 0x00212CC0
REGISTRAR = 0x001FB840
REG_TAIL = 0x0020E630

def leaf(m, c, j, x):
    return not c and not j and not x
def one_tail(m, c, j, x):
    return not c and len(j) == 1 and not x
def call_tail(m, c, j, x):
    return len(c) == 1 and len(j) == 1 and not x
def calls_only(m, c, j, x, n):
    return len(c) == n and not j and not x

FAMILIES = [
    ("nativeadapter-nullableoutrecordheaderinit.tsv", 25,
     "test rdx,rdx; je T; xor eax,eax; mov M[rdx],I; mov M[rdx],rax; "
     "mov M[rdx],rax; mov al,I; ret",
     leaf,
     "NativeAdapter.NullableOutRecordHeaderInitReturnTrue - EC-7 family C\n"
     "# if rdx non-null write a member constant + two zero qwords into the\n"
     "# out-record; always return 1."),
    ("runtime-container-stringkeyedchainattach.tsv", 132,
     "sub rsp,I; mov r10,M[rcx]; mov r11,rcx; test r10,r10; jne T; lea eax,M[r10]; "
     "add rsp,I; ret; mov M[rsp],rbx; mov rbx,M[rip]; mov r9,rbx; test rbx,rbx; "
     "je T; nop M[rax]; mov rax,M[r9]; mov r8,r10; sub r8,rax; nop M[rax+rax]; "
     "movzx edx,M[rax]; movzx ecx,M[rax+r8]; sub edx,ecx; jne T; inc rax; "
     "test ecx,ecx; jne T; test edx,edx; je T; mov r9,M[r9]; test r9,r9; jne T; "
     "mov M[r11],rbx; xor eax,eax; mov rbx,M[rsp]; mov M[rip],r11; add rsp,I; "
     "ret; mov eax,I; mov rbx,M[rsp]; add rsp,I; ret",
     leaf,
     "Runtime.Container.StringKeyedChainAttach - EC-7 family C\n"
     "# byte-compare walk over a global bucket chain keyed on a member rip\n"
     "# table; attach the node at [this+0x10] at the chain head; return 0 on\n"
     "# attach, a member code otherwise. No external calls."),
    ("nativeadapter-guardedsharedpairtailcall.tsv", 44,
     "push rbx; sub rsp,I; mov rbx,r9; call T; test eax,eax; jne T; mov rcx,rbx; "
     "call T; mov ecx,eax; add rsp,I; pop rbx; jmp T; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: c == {PREDICATE, BRIDGE} and len(j) == 1 and not x,
     "NativeAdapter.GuardedSharedPairTailCall - EC-7 family C\n"
     "# call shared predicate 00280120; if zero call shared bridge 00267E10 on\n"
     "# r9, then tail-call a member-specific op with ecx=result."),
    ("nativeadapter-callresultdualtaildispatch.tsv", 34,
     "sub rsp,I; mov rcx,r9; call T; test eax,eax; je T; add rsp,I; jmp T; "
     "add rsp,I; jmp T",
     lambda m, c, j, x: c == {BRIDGE} and len(j) == 2 and not x,
     "NativeAdapter.CallResultDualTailDispatch - EC-7 family C\n"
     "# call shared bridge 00267E10 on r9; tail-call one of two member-specific\n"
     "# ops selected on the result."),
    ("nativeadapter-memberfieldspantailcall.tsv", 35,
     "mov rax,rcx; lea r8,M[rcx]; mov rcx,M[rcx]; mov r9,rdx; add rcx,I; "
     "mov rdx,rax; jmp T",
     one_tail,
     "NativeAdapter.MemberFieldSpanTailCall - EC-7 family C\n"
     "# r8=this+off, rcx=[this+off2]+disp, r9=arg1, rdx=this; tail-call a\n"
     "# member-specific op (two observed)."),
    ("nativeadapter-firstmemberinvokefieldstore.tsv", 43,
     "push rbx; sub rsp,I; mov rbx,rcx; mov rcx,M[rcx]; test rcx,rcx; je T; "
     "call T; mov M[rbx],I; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: calls_only(m, c, j, x, 1),
     "NativeAdapter.FirstMemberInvokeFieldStore - EC-7 family C\n"
     "# call a member op on [this]; on non-null store a member constant into a\n"
     "# member field."),
    ("nativeadapter-conditionaldoublecallresulttailcall.tsv", 44,
     "push rbx; sub rsp,I; mov ebx,ecx; call T; test rax,rax; je T; call T; "
     "mov rcx,rax; mov edx,ebx; add rsp,I; pop rbx; jmp T; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: len(c) == 1 and len(j) == 1 and not x,
     "NativeAdapter.ConditionalDoubleCallResultTailCall - EC-7 family C\n"
     "# save ecx; call a member op; if non-null call it again; forward\n"
     "# (result, saved-ecx) to a member tail target."),
    ("nativeadapter-callresultargshifttailcall.tsv", 42,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov ebx,edx; mov edi,ecx; call T; "
     "mov rcx,rax; mov r8d,ebx; mov edx,edi; mov rbx,M[rsp]; add rsp,I; "
     "pop rdi; jmp T",
     call_tail,
     "NativeAdapter.CallResultArgShiftTailCall - EC-7 family C\n"
     "# call a member op; forward (result, old ecx, old edx) to a member tail\n"
     "# target."),
    ("nativeadapter-secondargumentzerotailcall.tsv", 7,
     "xor edx,edx; jmp T", one_tail,
     "NativeAdapter.SecondArgumentZeroTailCall - EC-7 family C\n"
     "# xor edx,edx; jmp member op."),
    ("nativeadapter-secondargumentconsttailcall.tsv", 10,
     "mov edx,I; jmp T", one_tail,
     "NativeAdapter.SecondArgumentConstTailCall - EC-7 family C\n"
     "# mov edx, member const; jmp member op."),
    ("nativeadapter-thirdargumentzerotailcall.tsv", 8,
     "xor r8d,r8d; jmp T", one_tail,
     "NativeAdapter.ThirdArgumentZeroTailCall - EC-7 family C\n"
     "# xor r8d,r8d; jmp member op."),
    ("nativeadapter-fourthargumentzerotailcall.tsv", 8,
     "xor r9d,r9d; jmp T", one_tail,
     "NativeAdapter.FourthArgumentZeroTailCall - EC-7 family C\n"
     "# xor r9d,r9d; jmp member op."),
    ("nativeadapter-constfirstargumentcalltailcall.tsv", 23,
     "sub rsp,I; mov ecx,I; call T; add rsp,I; jmp T", call_tail,
     "NativeAdapter.ConstFirstArgumentCallTailCall - EC-7 family C\n"
     "# ecx=member const; call a member op; tail-call a member op."),
    ("runtime-serialrangeinvokeloop.tsv", 85,
     "push rbx; sub rsp,I; mov eax,M[rip]; mov ebx,I; add eax,ebx; cmp eax,ebx; "
     "jle T; mov M[rsp],rdi; xor edi,edi; nop; mov r9d,I; mov M[rsp],edi; "
     "xor r8d,r8d; movzx ecx,bx; lea edx,M[r9]; call T; mov eax,M[rip]; "
     "inc ebx; add eax,I; cmp ebx,eax; jl T; mov rdi,M[rsp]; add rsp,I; "
     "pop rbx; ret",
     lambda m, c, j, x: c == {SERIAL_SINK} and not j and not x,
     "Runtime.SerialRangeInvokeLoop - EC-7 family C\n"
     "# iterate bx over a member global serial range (base +0x1000); invoke\n"
     "# shared Items_License sink 003008A0 with edx=0x63 per index."),
    ("nativeadapter-chainedmemberresulttailcall.tsv", 40,
     "push rbx; sub rsp,I; mov rbx,rcx; mov rcx,rdx; call T; mov rcx,rax; "
     "call T; mov edx,eax; mov rcx,rbx; add rsp,I; pop rbx; jmp T",
     lambda m, c, j, x: CHAIN_FIRST in c and len(c) == 2 and j == {CHAIN_TAIL}
     and not x,
     "NativeAdapter.ChainedMemberResultTailCall - EC-7 family C\n"
     "# call shared 00263F10 on rdx; call a member op on the result; forward\n"
     "# (this, result2) to shared tail 0026B4E0."),
    ("nativeleaf-clampedtablelookup.tsv", 83,
     "mov r8d,edx; cmp ecx,I; jl T; xor eax,eax; ret; movsxd rax,ecx; "
     "imul rdx,rax,I; lea rax,M[rip]; add rdx,rax; movzx ecx,M[rdx]; "
     "add ecx,r8d; jns T; or eax,I; sub eax,ecx; add ecx,I; and eax,I; "
     "add ecx,eax; cmp ecx,I; jl T; mov eax,ecx; shr eax,I; neg eax; "
     "shl eax,I; add ecx,eax; movsxd rax,ecx; lea rcx,M[rax+rax]; "
     "movzx eax,M[rdx+rcx]; ret",
     leaf,
     "NativeLeaf.ClampedTableLookup - EC-7 family C\n"
     "# bounds-checked read of a member rip table (stride 0x294); signed\n"
     "# clamp arithmetic; word field fetch; no external calls."),
    ("nativeadapter-callboolnormalizereturn.tsv", 23,
     "sub rsp,I; call T; xor ecx,ecx; test al,al; setne cl; mov eax,ecx; "
     "add rsp,I; ret",
     lambda m, c, j, x: calls_only(m, c, j, x, 1),
     "NativeAdapter.CallBoolNormalizeReturn - EC-7 family C\n"
     "# call a member op; return setne(al)."),
    ("nativeleaf-globalhandlestateread.tsv", 33,
     "sub rsp,I; xor ecx,ecx; cmp M[rip],rcx; setne cl; call T; mov rax,M[rip]; "
     "add rsp,I; ret",
     lambda m, c, j, x: c == {RET0_STUB} and not j and not x,
     "NativeLeaf.GlobalHandleStateRead - EC-7 family C\n"
     "# setne cl on a member global pointer; call the ICF-folded ret-0 stub\n"
     "# 0016D6A0; return a second member global."),
    ("nativeleaf-doublederefflagextract.tsv", 17,
     "mov rax,M[rcx]; mov rcx,M[rax]; mov eax,M[rcx]; shr eax,I; and eax,I; ret",
     leaf,
     "NativeLeaf.DoubleDerefFlagExtract - EC-7 family C\n"
     "# rax=[rcx+X]; eax=[[rax]+Y]>>k&1; ret."),
    ("nativeadapter-smallrecordvtablector.tsv", 47,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov ebx,edx; mov rdi,rcx; call T; "
     "lea rax,M[rip]; mov M[rdi],ebx; mov rbx,M[rsp]; mov M[rdi],rax; "
     "mov rax,rdi; add rsp,I; pop rdi; ret",
     lambda m, c, j, x: c == {SMALL_INIT} and not j and not x,
     "NativeAdapter.SmallRecordVtableCtor - EC-7 family C\n"
     "# call shared init 00212CC0 on this; store arg1 at +0x18; install a\n"
     "# member vtable; return this."),
    ("nativeadapter-doubleselfinvoke.tsv", 39,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; call T; nop; mov rcx,rbx; "
     "call T; nop; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: calls_only(m, c, j, x, 1),
     "NativeAdapter.DoubleSelfInvoke - EC-7 family C\n"
     "# call the same member op on this twice."),
    ("nativeadapter-twosubobjectinvoketailcall.tsv", 40,
     "push rbx; sub rsp,I; mov rbx,rcx; add rcx,I; call T; lea rcx,M[rbx]; "
     "call T; mov rcx,rbx; add rsp,I; pop rbx; jmp T",
     lambda m, c, j, x: len(c) == 1 and len(j) == 1 and not x,
     "NativeAdapter.TwoSubobjectInvokeTailCall - EC-7 family C\n"
     "# call a member op on this+off then this+off2; tail-call a member op on\n"
     "# this."),
    ("nativeadapter-memberpredicatetreesearch.tsv", 111,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; mov M[rsp],rdi; push r14; "
     "sub rsp,I; mov rbx,M[rcx]; lea rdi,M[rcx]; mov esi,r9d; mov ebp,r8d; "
     "mov r14d,edx; cmp rbx,rdi; je T; mov rcx,M[rbx]; mov r9d,esi; "
     "mov r8d,ebp; mov edx,r14d; call T; test al,al; jne T; mov rbx,M[rbx]; "
     "cmp rbx,rdi; jne T; xor al,al; mov rbx,M[rsp]; mov rbp,M[rsp]; "
     "mov rsi,M[rsp]; mov rdi,M[rsp]; add rsp,I; pop r14; ret; mov al,I; jmp T",
     lambda m, c, j, x: calls_only(m, c, j, x, 1),
     "NativeAdapter.MemberPredicateTreeSearch - EC-7 family C\n"
     "# walk the intrusive tree at this+8 calling a member predicate per node;\n"
     "# return the found flag."),
    ("nativeadapter-flaggatedinittailcall.tsv", 62,
     "sub rsp,I; test M[rip],I; jne T; xor edx,edx; mov M[rsp],I; xor r9d,r9d; "
     "mov M[rsp],I; xor r8d,r8d; lea ecx,M[rdx]; call T; add rsp,I; jmp T; "
     "add rsp,I; ret",
     lambda m, c, j, x: c == {INIT_16} and j == {AUDIO_TAIL} and not x,
     "NativeAdapter.FlagGatedInitTailCall - EC-7 family C\n"
     "# if a member global flag is clear, zero two stack slots and call shared\n"
     "# init 00226BE0 (ecx=0x16); tail-call shared 00226280."),
    ("nativeadapter-twosharedcomposetailcall.tsv", 49,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rdi,r9; call T; mov rcx,rdi; "
     "mov rbx,rax; call T; mov edx,eax; mov rcx,rbx; mov rbx,M[rsp]; "
     "add rsp,I; pop rdi; jmp T",
     lambda m, c, j, x: c == {GETTER, BRIDGE} and len(j) == 1 and not x,
     "NativeAdapter.TwoSharedComposeTailCall - EC-7 family C\n"
     "# call shared getter 002640C0; call shared bridge 00267E10 on r9; forward\n"
     "# (result, bridge-result) to a member tail target."),
    ("nativeadapter-sharednormalizetailcallzero.tsv", 79,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; sub rsp,I; "
     "mov rsi,rdx; mov rbp,rcx; mov rcx,rsi; xor edx,edx; mov rbx,r9; "
     "mov rdi,r8; call T; mov r9,rbx; mov r8,rdi; mov rdx,rsi; mov rcx,rbp; "
     "mov rbx,M[rsp]; mov rbp,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; jmp T",
     lambda m, c, j, x: c == {MOVEMENT_NORM} and len(j) == 1 and not x,
     "NativeAdapter.SharedNormalizeTailCallZero - EC-7 family C\n"
     "# call shared Movement normaliser 0026A1A0 (rcx=rdx, edx=0); restore the\n"
     "# caller's four args; tail-call a member op."),
    ("nativeadapter-sharednormalizetailcallone.tsv", 82,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; sub rsp,I; "
     "mov rsi,rdx; mov rbp,rcx; mov rcx,rsi; mov edx,I; mov rbx,r9; "
     "mov rdi,r8; call T; mov r9,rbx; mov r8,rdi; mov rdx,rsi; mov rcx,rbp; "
     "mov rbx,M[rsp]; mov rbp,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; jmp T",
     lambda m, c, j, x: c == {MOVEMENT_NORM} and len(j) == 1 and not x,
     "NativeAdapter.SharedNormalizeTailCallOne - EC-7 family C\n"
     "# call shared Movement normaliser 0026A1A0 (rcx=rdx, edx=1); restore the\n"
     "# caller's four args; tail-call a member op."),
    ("nativeadapter-guardedcallresultboolinvert.tsv", 39,
     "sub rsp,I; call T; test eax,eax; je T; xor eax,eax; add rsp,I; ret; "
     "call T; xor ecx,ecx; test eax,eax; sete cl; mov eax,ecx; add rsp,I; ret",
     lambda m, c, j, x: PREDICATE in c and len(c) == 2 and not j and not x,
     "NativeAdapter.GuardedCallResultBoolInvert - EC-7 family C\n"
     "# call shared predicate 00280120; if zero return 0; else call a member op\n"
     "# and return sete(eax)."),
    ("nativeadapter-outrecordzeroinitmemberinit.tsv", 65,
     "mov M[rsp],rdx; push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; "
     "mov M[rsp],rdx; test rdx,rdx; je T; xor edx,edx; mov r8d,I; mov rcx,rbx; "
     "call T; mov rcx,rbx; call T; nop; mov al,I; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: MEMSET_IMPORT in c and len(c) == 2 and not j and not x,
     "NativeAdapter.OutRecordZeroInitMemberInit - EC-7 family C\n"
     "# if the out pointer is non-null, memset it via shared import 00861EC0\n"
     "# (size 0x90) then call a member init; return 1."),
    ("nativeadapter-outrecordvtablepairstore.tsv", 69,
     "mov M[rsp],rdx; push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; "
     "mov M[rsp],rdx; test rdx,rdx; je T; mov rcx,rdx; call T; lea rax,M[rip]; "
     "mov M[rbx],rax; lea rax,M[rip]; mov M[rbx],rax; mov al,I; add rsp,I; "
     "pop rbx; ret",
     lambda m, c, j, x: calls_only(m, c, j, x, 1),
     "NativeAdapter.OutRecordVtablePairStore - EC-7 family C\n"
     "# if the out pointer is non-null, call a member op on it and store two\n"
     "# member rip pointers at +0/+8; return 1."),
    ("nativeadapter-twomanifoldcallindexedvcall.tsv", 76,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rdi,rcx; "
     "mov rbx,rdx; mov rcx,rdx; call T; mov rcx,rbx; mov rsi,rax; call T; "
     "test rax,rax; je T; movsxd rcx,M[rdi]; mov rdx,rsi; add rcx,rax; "
     "call M[rdi]; mov rbx,M[rsp]; xor eax,eax; mov rsi,M[rsp]; add rsp,I; "
     "pop rdi; ret",
     lambda m, c, j, x: len(c) == 2 and not j and not x,
     "NativeAdapter.TwoMemberCallIndexedVcall - EC-7 family C\n"
     "# call member op on rdx; call member op on rdx again saving the result;\n"
     "# if non-null vcall [this+8] with rcx=rax+[this+0x10]."),
    ("nativeadapter-triplememberchainreturntrue.tsv", 55,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; mov rcx,rdx; call T; "
     "test al,al; je T; mov rcx,rbx; call T; mov rcx,rbx; call T; nop; "
     "mov al,I; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: len(c) == 3 and not j and not x,
     "NativeAdapter.TripleMemberChainReturnTrue - EC-7 family C\n"
     "# member predicate on rdx; if true call two more member ops on rdx;\n"
     "# return 1."),
    ("nativeadapter-namedrecordregisterpair.tsv", 39,
     "push rbx; sub rsp,I; mov ebx,ecx; lea rcx,M[rip]; call T; mov edx,ebx; "
     "lea rcx,M[rip]; add rsp,I; pop rbx; jmp T",
     lambda m, c, j, x: c == {REGISTRAR} and j == {REG_TAIL} and not x,
     "NativeAdapter.NamedRecordRegisterPair - EC-7 family C\n"
     "# call shared registrar 001FB840 with a member string; tail-call shared\n"
     "# 0020E630 with a second member string and the saved arg."),
    ("nativeadapter-mallcorecordemplacetailcall.tsv", 148,
     "push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov ebx,edx; "
     "mov rdi,rcx; or r8d,I; xor edx,edx; lea ecx,M[rdx]; call T; "
     "mov M[rsp],rax; mov M[rsp],rax; test rax,rax; je T; mov edx,ebx; "
     "mov rcx,rax; call T; mov rbx,rax; jmp T; xor ebx,ebx; mov M[rsp],rbx; "
     "mov rdx,M[rdi]; cmp rdx,M[rdi]; jae T; lea rax,M[rdx]; mov M[rdi],rax; "
     "test rdx,rdx; je T; mov M[rdx],rbx; jmp T; lea r8,M[rsp]; mov rcx,rdi; "
     "call T; mov rbx,M[rsp]; call T; mov rcx,rax; mov rdx,rbx; mov rbx,M[rsp]; "
     "add rsp,I; pop rdi; jmp T",
     lambda m, c, j, x: {MALLOC, VEC_GROW, GLOBAL_READ} <= c and len(c) == 4
     and j == {EMPLACE_TAIL} and not x,
     "NativeAdapter.MallocRecordEmplaceTailCall - EC-7 family C\n"
     "# malloc(0x20) via shared 0085E730; member-construct the record; push-back\n"
     "# into [this]'s end-pointer vector (fallback shared grow 001AB570); read\n"
     "# global state via shared 0018B4E0; tail-call shared 0018AFF0."),
    ("runtime-container-spancheckmembervcall.tsv", 57,
     "sub rsp,I; mov M[rsp],I; mov rdx,M[rcx]; mov rax,M[rcx]; sub rax,rdx; "
     "cmp rax,I; jle T; mov r8d,M[rcx]; sub r8d,edx; test rdx,rdx; je T; "
     "add rcx,I; mov rax,M[rcx]; call M[rax]; nop; add rsp,I; ret",
     leaf,
     "Runtime.Container.SpanCheckMemberVcall - EC-7 family C\n"
     "# if the embedded sequence [this+X..this+Y] has more than one element and\n"
     "# a non-null begin, vcall slot 3 on the member object; no direct calls."),
    ("runtime-container-recursivespannodewalk.tsv", 152,
     "test rdx,rdx; je T; push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; "
     "mov M[rsp],rbp; mov M[rsp],rsi; mov rbx,rdx; mov rbp,rcx; nop M[rax]; "
     "mov rdx,M[rbx]; mov rcx,rbp; call T; mov rdi,M[rbx]; mov rdx,M[rbx]; "
     "mov rax,M[rbx]; sub rax,rdx; cmp rax,I; jle T; mov r8d,M[rbx]; "
     "sub r8d,edx; test rdx,rdx; je T; lea rcx,M[rbx]; mov rax,M[rcx]; "
     "call M[rax]; nop; mov rax,M[rbp]; mov r8d,I; mov rdx,rbx; lea rcx,M[rbp]; "
     "call M[rax]; mov rbx,rdi; test rdi,rdi; jne T; mov rbx,M[rsp]; "
     "mov rbp,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     leaf,
     "Runtime.Container.RecursiveSpanNodeWalk - EC-7 family C\n"
     "# self-recursive tree walk; per node a span-check + member vcall slot 3,\n"
     "# then vcall [this+0x30] slot 3; no direct external calls."),
    ("nativeleaf-fieldflagmaskclear.tsv", None,
     "and M[rcx],I; ret", leaf,
     "NativeLeaf.FieldFlagMaskClear - EC-7 family C\n"
     "# and [rcx+off], member mask; ret - flag-bit clear, byte and dword widths."),
    ("nativeleaf-fieldfloatgetter.tsv", None,
     "movss xmm0,M[rcx]; ret", leaf,
     "NativeLeaf.FieldFloatGetter - EC-7 family C\n"
     "# movss xmm0, [rcx+off]; ret - displaced float getter."),
    ("nativeleaf-memberaddressaccessor.tsv", None,
     "lea rax,M[rcx]; ret", leaf,
     "NativeLeaf.MemberAddressAccessor - EC-7 family C\n"
     "# lea rax, [rcx+off]; ret. EXTENSION of the declared row: same form,\n"
     "# more frontier members."),
    ("nativeadapter-callthentailcall.tsv", 18,
     "sub rsp,I; call T; add rsp,I; jmp T", call_tail,
     "NativeAdapter.CallThenTailCall - EC-7 family C\n"
     "# call a member op; tail-call a member op. EXTENSION of the declared row."),
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
