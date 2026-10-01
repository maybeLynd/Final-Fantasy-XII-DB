"""select_frontier_form_clusters_3.py - EC-7 family C member selectors, third
pass over the live frontier form census (SWE2-EC7-FRONTIER-FORM-CLUSTERS-3),
declared on generated-function-families.md.

Every group is ONE operand-aware instruction-form skeleton at a fixed body
size; literal byte-image counts differ because member constants, rip bases
and member-specific targets are encoded in the payload:

  slidetablerecordcopyinvoke (219B) - read two word indices from member rip
      tables, scale by 0x10 into a member rip record array, SIMD-copy a 16B
      record + 8B tail between the slots, advance a member counter, then
      invoke the caller-supplied callback r11 (=rcx) with rdx=arg1.
  bitfieldornodewalk (138B) - zero-init a 0x38B node record, attach the
      arg1 intrusive list head, seed a member rip table pointer, then walk
      nodes calling shared bitfield-or predicate 001B7CE0 until it clears;
      on success call shared 001AA0A0. Returns this.
  tableindexdispatchtailcall (65B) - resolve a record index word through a
      member global table at stride 0x740, require +0x284 clear, tail-dispatch
      to a member op. jcc carries the member target.
  nullguardtailcall (10B) - if rcx non-null, tail-dispatch to a member op.
      jcc carries the member target.
  recursivelistvcallwalk (96B) - self-recursive intrusive-list walk; per
      node vcall [rbp+0x30] slot 3 with r8=0x28, then recurse on [rbx].
      Internal self-call; no external targets.
  callboolnormalizereturnsete (23B) - call a member op; return sete(eax).
      Sibling of CallBoolNormalizeReturn (which is setne on al).
  doublecallresulttailcallsavedthis (46B) - save this->rbx; call member op;
      if non-null call the member op again; forward (result2, this) to a
      member tail target. Sibling of ConditionalDoubleCallResultTailCall
      (which saves ecx).
  bytesavesecondargresulttailcall2 (30B) - save arg2 byte->ebx; call member
      op; forward (result, saved byte) to a member tail target. Sibling of
      ByteSaveSecondArgResultTailCall (no result->rcx move).
  fixedpipelinecallresult (45B) - ecx=3 via lea; call shared 0036C1D0; call
      shared 0036A100 on ecx=arg1; call shared 0036C140; return its result.
  savedfourargcallresultcall (76B) - save all four args; call a member op;
      forward (result, arg1..arg4) to a second member op.
  stackconstonecall (22B) - push a dword 1 on the stack frame; call a member
      op; return void.
  nullableglobalclearcall (37B) - if a member global is non-null call shared
      00244F00 on it, then zero the global.
  refflagsetcallzero (26B) - if r8d bit31 is clear, set it (bts) and call a
      member op; return 0.
  dynamicoffsetrefflagcall (64B) - if r9d bit31 is already set return 5;
      else set it, compute rcx=[this+0x18]+((this+0x48)-[[rax]+0xF4])+arg1,
      call a member op; return 0.
  countedloopmemberinvoke (112B) - iterate ebx over a member count field
      (mask 0x7fffffff, min 1); per index call a member lookup twice reading
      [rax] and call shared 005CCB80 when positive.
  taggedoutrecordfloatvcall (142B) - pop a double arg off the arg vector,
      convert to float, vcall [this+8] slot 1; if the out-record tag matches
      shared singleton 006B0B20|1, store the result handle and return 1.
      Sibling of the tagged out-record vcall leaf family.
  sharedgetterthreeargtailcall (58B) - save arg1..arg3; call shared getter
      00210B30; forward (result, arg1..arg3) to a member tail target.
  recordfieldcopy (189B) - call a member getter; copy ~0x88 bytes of fields
      from the result record into out arg2.
  tableindexdispatchsetflag (97B) - same table-index resolve as the 65B
      spelling; when +0x284 is set call a member op on the record and set
      bit 0x800 at +0x290.
  chainpredicatereleasetail (50B) - call a member predicate on this; if true
      call a second member op on this, then tail-call a member release op.
  outrecordmembercalltailcall (41B) - rdx=[arg1+8]; call a member predicate
      on it; if zero tail-call a member op on this.
  globaloffsettailcall (19B) - rcx = member global + member offset;
      tail-call a member op.
  boundedtablewordlookup (36B) - if ecx <= member bound, index a member rip
      table of row pointers; if the row's first byte is non-null return the
      word/dword at [row + edx*stride + 8], else return -1.
  nullableoutrecordvptrcall (58B) - if the out-record pointer is non-null,
      call a member op on it and install a member rip vtable pointer;
      return 1.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_frontier_form_clusters_3.py [--write]
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

FAMILIES = [
    ("nativeleaf-slidetablerecordcopyinvoke.tsv", 219,
     "push rbx; sub rsp,I; movsx eax,M[rip]; lea rbx,M[rip]; shl eax,I; "
     "mov r9d,I; movsxd r8,eax; mov r10,rdx; mov r11,rcx; movups xmm1,M[r8+rbx]; "
     "movsx r8d,M[rip]; mov eax,r8d; shl eax,I; movsxd rdx,eax; movzx eax,M[rip]; "
     "lea rcx,M[rdx+rbx]; add ax,r9w; movzx r9d,M[rip]; movzx eax,ax; "
     "mov M[rcx],eax; mov eax,I; add eax,r9d; mov M[rip],r9w; movups M[rip],xmm1; "
     "mov M[rip],ax; mov eax,I; movsd xmm0,M[rip]; sub r8w,ax; psrldq xmm1,I; "
     "movsd M[rdx+rbx],xmm0; movd M[rdx+rbx],xmm1; cmp r9w,r8w; je T; "
     "add r9w,ax; mov M[rip],r9w; xor r8d,r8d; mov rdx,r10; call r11; "
     "movsx eax,M[rip]; movzx ecx,M[rip]; add cx,ax; mov M[rip],cx; inc cx; "
     "mov M[rip],cx; add rsp,I; pop rbx; ret",
     leaf,
     "NativeLeaf.SlideTableRecordCopyInvoke - EC-7 family C\n"
     "# two member index words (movsx word [rip], shl 4) select slots in a member\n"
     "# rip record array; SIMD-copies a 16B record + 8B tail between slots,\n"
     "# advances member counters, then calls the supplied callback r11=rcx.\n"
     "# 10 byte images collapse to ONE instruction form; no direct externals."),
    ("nativeadapter-bitfieldornodewalk.tsv", 138,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,rcx; xor edi,edi; "
     "mov M[rcx],rdi; mov M[rcx],rdi; mov M[rcx],rdi; mov M[rcx],edi; "
     "lea rcx,M[rdx]; mov M[rbx],rcx; mov rax,M[rcx]; cmp rax,rcx; mov rcx,rbx; "
     "cmove rax,rdi; mov M[rbx],rax; lea rax,M[rip]; mov M[rbx],rax; call T; "
     "test al,al; jne T; nop M[rax+rax]; mov rax,M[rbx]; test rax,rax; je T; "
     "mov rax,M[rax]; cmp rax,M[rbx]; cmove rax,rdi; mov M[rbx],rax; mov rcx,rbx; "
     "call T; test al,al; je T; mov rcx,rbx; call T; mov rax,rbx; mov rbx,M[rsp]; "
     "add rsp,I; pop rdi; ret",
     shared_only(0x001AA0A0, 0x001B7CE0),
     "NativeAdapter.BitfieldOrNodeWalk - EC-7 family C\n"
     "# zero-init a 0x38B node record, attach the arg1 list head, seed a member\n"
     "# rip table pointer; walk nodes calling shared bitfield-or 001B7CE0 until\n"
     "# it clears; on success call shared 001AA0A0. Returns this. 9 images,\n"
     "# ONE form. Distinct from the 132B StringKeyedChainAttach idiom."),
    ("nativeadapter-tableindexdispatchtailcall.tsv", 65,
     "test rcx,rcx; je T; mov rax,M[rcx]; test rax,rax; je T; cmp M[rax],I; "
     "je T; movzx ecx,M[rax]; cmp cx,I; je T; movsx rax,cx; imul rcx,rax,I; "
     "add rcx,M[rip]; je T; cmp M[rcx],I; jne T; ret",
     jcc_tail,
     "NativeAdapter.TableIndexDispatchTailCall - EC-7 family C\n"
     "# resolve index word [this+0xC0]->[rax] through a member global table\n"
     "# (stride 0x740); require +0x284 clear; jne-tail to a member op."),
    ("nativeadapter-nullguardtailcall.tsv", 10,
     "test rcx,rcx; jne T; ret",
     jcc_tail,
     "NativeAdapter.NullGuardTailCall - EC-7 family C\n"
     "# if rcx non-null, jne-tail to a member op; else return."),
    ("nativeleaf-recursivelistvcallwalk.tsv", 96,
     "test rdx,rdx; je T; mov M[rsp],rbx; push rbp; sub rsp,I; mov M[rsp],rsi; "
     "mov rbx,rdx; mov M[rsp],rdi; mov rbp,rcx; nop; mov rdx,M[rbx]; mov rcx,rbp; "
     "call T; mov rax,M[rbp]; lea rcx,M[rbp]; mov rdi,M[rbx]; mov r8d,I; "
     "mov rdx,rbx; call M[rax]; mov rbx,rdi; test rdi,rdi; jne T; mov rdi,M[rsp]; "
     "mov rsi,M[rsp]; mov rbx,M[rsp]; add rsp,I; pop rbp; ret",
     leaf,
     "NativeLeaf.RecursiveListVcallWalk - EC-7 family C\n"
     "# self-recursive intrusive-list walk; per node vcall [rbp+0x30] slot 3\n"
     "# with r8=0x28, then recurse on [rbx]. The self-call is internal;\n"
     "# no external targets."),
    ("nativeadapter-callboolnormalizereturnsete.tsv", 23,
     "sub rsp,I; call T; xor ecx,ecx; test eax,eax; sete cl; mov eax,ecx; "
     "add rsp,I; ret",
     one_call,
     "NativeAdapter.CallBoolNormalizeReturnSete - EC-7 family C\n"
     "# call a member op; return sete(eax). Sibling of CallBoolNormalizeReturn\n"
     "# (setne on al)."),
    ("nativeadapter-doublecallresulttailcallsavedthis.tsv", 46,
     "push rbx; sub rsp,I; mov rbx,rcx; call T; test rax,rax; je T; call T; "
     "mov rcx,rax; mov rdx,rbx; add rsp,I; pop rbx; jmp T; add rsp,I; pop rbx; ret",
     call_tail,
     "NativeAdapter.DoubleCallResultTailCallSavedThis - EC-7 family C\n"
     "# save this->rbx; call member op; if non-null call it again; forward\n"
     "# (result2, this) to a member tail target. Sibling of\n"
     "# ConditionalDoubleCallResultTailCall (saves ecx, 44B)."),
    ("nativeadapter-bytesavesecondargresulttailcall2.tsv", 30,
     "push rbx; sub rsp,I; movzx ebx,cl; call T; mov rcx,rax; movzx edx,bl; "
     "add rsp,I; pop rbx; jmp T",
     call_tail,
     "NativeAdapter.ByteSaveSecondArgResultTailCall2 - EC-7 family C\n"
     "# save arg2 byte->ebx; call member op; forward (result, saved byte) to a\n"
     "# member tail target. Sibling of ByteSaveSecondArgResultTailCall."),
    ("nativeadapter-fixedpipelinecallresult.tsv", 45,
     "push rbx; sub rsp,I; mov edx,I; mov ebx,ecx; lea ecx,M[rdx]; call T; "
     "mov ecx,ebx; call T; mov rbx,rax; call T; mov rax,rbx; add rsp,I; pop rbx; ret",
     shared_only(0x0036A100, 0x0036C140, 0x0036C1D0),
     "NativeAdapter.FixedPipelineCallResult - EC-7 family C\n"
     "# ecx=3 via lea; call shared 0036C1D0; call shared 0036A100 on ecx=arg1;\n"
     "# call shared 0036C140; return its result."),
    ("nativeadapter-savedfourargcallresultcall.tsv", 76,
     "mov M[rsp],rbx; mov M[rsp],rbp; mov M[rsp],rsi; push rdi; sub rsp,I; "
     "mov ebx,r9d; mov edi,r8d; mov esi,edx; mov ebp,ecx; call T; mov rcx,rax; "
     "mov M[rsp],ebx; mov r9d,edi; mov r8d,esi; mov edx,ebp; call T; "
     "mov rbx,M[rsp]; mov rbp,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     lambda m, c, j, x: len(c) == 2 and not j and not x,
     "NativeAdapter.SavedFourArgCallResultCall - EC-7 family C\n"
     "# save all four args; call a member op; forward (result, arg1..arg4)\n"
     "# to a second member op."),
    ("nativeadapter-stackconstonecall.tsv", 22,
     "sub rsp,I; mov M[rsp],I; call T; add rsp,I; ret",
     one_call,
     "NativeAdapter.StackConstOneCall - EC-7 family C\n"
     "# store dword 1 into the stack frame; call a member op; return void."),
    ("nativeleaf-nullableglobalclearcall.tsv", 37,
     "sub rsp,I; mov rcx,M[rip]; test rcx,rcx; je T; call T; mov M[rip],I; "
     "add rsp,I; ret",
     one_call,
     "NativeLeaf.NullableGlobalClearCall - EC-7 family C\n"
     "# if a member global is non-null call a member op on it, then zero\n"
     "# the global."),
    ("nativeadapter-refflagsetcallzero.tsv", 26,
     "sub rsp,I; test r8d,r8d; js T; bts r8d,I; call T; xor eax,eax; "
     "add rsp,I; ret",
     one_call,
     "NativeAdapter.RefFlagSetCallZero - EC-7 family C\n"
     "# if r8d bit31 is clear, set it (bts) and call a member op; return 0."),
    ("nativeadapter-dynamicoffsetrefflagcall.tsv", 64,
     "sub rsp,I; mov r10,r8; test r9d,r9d; jns T; mov eax,I; add rsp,I; ret; "
     "mov rax,M[rcx]; bts r9d,I; mov ecx,M[rcx]; mov r8d,r9d; sub ecx,M[rax]; "
     "movsxd rcx,ecx; add rcx,rdx; mov rdx,r10; call T; xor eax,eax; "
     "add rsp,I; ret",
     one_call,
     "NativeAdapter.DynamicOffsetRefFlagCall - EC-7 family C\n"
     "# if r9d bit31 set return 5; else set it, compute rcx = [this+0x18] +\n"
     "# ([this+0x48] - [[this]+0xF4]) + arg1, call a member op; return 0."),
    ("nativeadapter-countedloopmemberinvoke.tsv", 112,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov edx,M[rcx]; xor ebx,ebx; "
     "and edx,I; mov eax,I; mov rdi,rcx; cmovne eax,edx; test eax,eax; je T; "
     "mov edx,ebx; mov rcx,rdi; call T; mov ecx,M[rax]; test ecx,ecx; jle T; "
     "mov ecx,I; call T; mov edx,ebx; mov rcx,rdi; call T; mov ecx,M[rax]; "
     "test ecx,ecx; jg T; mov ecx,M[rdi]; inc ebx; and ecx,I; mov eax,I; "
     "cmovne eax,ecx; cmp ebx,eax; jb T; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     shared_calls(0x005CCB80),
     "NativeAdapter.CountedLoopMemberInvoke - EC-7 family C\n"
     "# iterate ebx over a member count field (mask 0x7fffffff, min 1); per\n"
     "# index call a member lookup twice reading [rax] and call shared\n"
     "# 005CCB80 when positive."),
    ("nativeleaf-taggedoutrecordfloatvcall.tsv", 142,
     "mov M[rsp],rbx; push rsi; sub rsp,I; mov rsi,r8; mov r8,rcx; mov rbx,r9; "
     "test rdx,rdx; je T; mov rax,M[rsp]; mov rcx,rdx; mov M[rsp],rdi; "
     "add M[rax],I; mov rax,M[rax]; movsd xmm1,M[rax]; cvtpd2ps xmm1,xmm1; "
     "call M[r8]; mov rdi,rax; test rbx,rbx; je T; call T; or rax,I; "
     "cmp rsi,rax; jne T; mov M[rbx],rdi; mov eax,I; mov rdi,M[rsp]; "
     "mov M[rbx],I; mov rbx,M[rsp]; add rsp,I; pop rsi; ret; xor eax,eax; "
     "mov rdi,M[rsp]; mov rbx,M[rsp]; add rsp,I; pop rsi; ret; xor eax,eax; "
     "mov rbx,M[rsp]; add rsp,I; pop rsi; ret",
     one_call,
     "NativeLeaf.TaggedOutRecordFloatVcall - EC-7 family C\n"
     "# pop a double arg off the arg vector, convert to float, vcall [this+8]\n"
     "# slot 1; if out-record tag matches member getter|1 store the result\n"
     "# handle and return 1. Sibling of the tagged out-record vcall leaves."),
    ("nativeadapter-sharedgetterthreeargtailcall.tsv", 58,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov ebx,r8d; "
     "mov edi,edx; mov esi,ecx; call T; mov rcx,rax; mov r9d,ebx; mov r8d,edi; "
     "mov edx,esi; mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; jmp T",
     call_tail,
     "NativeAdapter.SharedGetterThreeArgTailCall - EC-7 family C\n"
     "# save arg1..arg3; call shared getter 00210B30; forward (result,\n"
     "# arg1..arg3) to a member tail target."),
    ("nativeadapter-recordfieldcopy.tsv", 189,
     "push rbx; sub rsp,I; mov rcx,rdx; mov rbx,r8; call T; mov rdx,rax; "
     "movzx ecx,M[rax]; mov M[rbx],cl; mov ecx,M[rax]; mov M[rbx],ecx; "
     "mov ecx,M[rax]; mov M[rbx],ecx; mov rcx,M[rax]; mov M[rbx],rcx; "
     "mov ecx,M[rax]; mov M[rbx],ecx; mov ecx,M[rax]; mov M[rbx],ecx; "
     "mov eax,M[rax]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov rax,M[rdx]; mov M[rbx],rax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov eax,M[rdx]; mov M[rbx],eax; mov eax,M[rdx]; mov M[rbx],eax; "
     "mov rax,M[rdx]; mov M[rbx],rax; add rsp,I; pop rbx; ret",
     one_call,
     "NativeAdapter.RecordFieldCopy - EC-7 family C\n"
     "# call a member getter on arg1; copy ~0x88 bytes of fields from the\n"
     "# result record into out arg2."),
    ("nativeadapter-tableindexdispatchsetflag.tsv", 97,
     "sub rsp,I; test rcx,rcx; je T; mov rax,M[rcx]; test rax,rax; je T; "
     "cmp M[rax],I; je T; movzx ecx,M[rax]; cmp cx,I; je T; mov M[rsp],rbx; "
     "movsx rax,cx; imul rbx,rax,I; add rbx,M[rip]; je T; cmp M[rbx],I; "
     "je T; mov rcx,rbx; call T; or M[rbx],I; mov rbx,M[rsp]; add rsp,I; ret",
     one_call,
     "NativeAdapter.TableIndexDispatchSetFlag - EC-7 family C\n"
     "# table-index resolve as in the 65B spelling; when +0x284 is set call a\n"
     "# member op on the record and set bit 0x800 at +0x290."),
    ("nativeadapter-chainpredicatereleasetail.tsv", 50,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; call T; nop; test al,al; "
     "je T; mov rcx,rbx; call T; nop; mov rcx,rbx; add rsp,I; pop rbx; jmp T",
     lambda m, c, j, x: len(c) == 2 and len(j) == 1 and not x,
     "NativeAdapter.ChainPredicateReleaseTail - EC-7 family C\n"
     "# call a member predicate on this; if true call a second member op on\n"
     "# this, then tail-call a member release op."),
    ("nativeadapter-outrecordmembercalltailcall.tsv", 41,
     "push rbx; sub rsp,I; mov rdx,M[rdx]; mov rbx,rcx; call T; test eax,eax; "
     "jne T; mov rcx,rbx; add rsp,I; pop rbx; jmp T; add rsp,I; pop rbx; ret",
     call_tail,
     "NativeAdapter.OutRecordMemberCallTailCall - EC-7 family C\n"
     "# rdx=[arg1+8]; call a member predicate on it; if zero tail-call a\n"
     "# member op on this."),
    ("nativeadapter-globaloffsettailcall.tsv", 19,
     "mov rcx,M[rip]; add rcx,I; jmp T",
     lambda m, c, j, x: not c and len(j) == 1 and not x,
     "NativeAdapter.GlobalOffsetTailCall - EC-7 family C\n"
     "# rcx = member global + member offset; tail-call a member op."),
    ("nativeleaf-boundedtablewordlookup.tsv", 36,
     "cmp ecx,I; jg T; movsxd rax,ecx; lea rcx,M[rip]; mov rcx,M[rcx+rax]; "
     "cmp M[rcx],I; je T; movsxd rax,edx; mov eax,M[rcx+rax]; ret; or eax,I; ret",
     leaf,
     "NativeLeaf.BoundedTableWordLookup - EC-7 family C\n"
     "# if ecx <= member bound, index a member rip table of row pointers;\n"
     "# if the row's first byte is non-null return [row + edx*stride + 8],\n"
     "# else return -1. Member-specific bound and table base."),
    ("nativeadapter-nullableoutrecordvptrcall.tsv", 58,
     "mov M[rsp],rdx; push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; "
     "mov M[rsp],rdx; test rdx,rdx; je T; mov rcx,rdx; call T; lea rax,M[rip]; "
     "mov M[rbx],rax; mov al,I; add rsp,I; pop rbx; ret",
     one_call,
     "NativeAdapter.NullableOutRecordVptrCall - EC-7 family C\n"
     "# if the out-record pointer is non-null, call a member op on it and\n"
     "# install a member rip vtable pointer; return 1. Sibling of\n"
     "# OutRecordDescriptorInitReturnTrue (different call/store shape)."),
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
