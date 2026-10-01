"""select_frontier_form_clusters.py - EC-7 family C member selectors for the
generated-form clusters measured off the live frontier
(SWE2-EC7-FRONTIER-FORM-CLUSTERS), declared on generated-function-families.md.

Each group is ONE operand-aware instruction-form skeleton over its byte images;
operand widths and immediate values refine the semantic split where a census
cluster mixed operations:

  frame-advance-continuation-adapters (56B) - call the shared
      Presentation.EffectInstance frame-advance update 002F2530; if it returns
      nonzero, call a member-specific continuation; return the shared result.
  deletingdestructor-sharedteardown (92B) - install a member-specific vtable,
      call shared teardown 00633390, then dispatch on the deleting flags:
      bit0 gates deletion, bit2 selects sized-delete stub 0016D6A0 over the
      _aligned_free wrapper 00584730. Sibling spelling of
      DeletingDestructor.VtableAlignedOrGuardedFree on this page.
  fieldclear (mov [rcx+off],0; any width) / fieldconststore (nonzero imm) -
      the census cluster mixed clears and constant initialisers; split on the
      stored immediate.
  field*store/getter leaf accessors - no external targets.
  memberoffsettailcall - add rcx,imm; jmp member (imm8 and imm32 spellings).
      The indexed RelativeMemberAddressTailCall32/64 rows are a different form.
  fieldresetoffsettailcall (24B) - zero a member field, edx=4, this+=off,
      tail-call one of the four Presentation clone helpers.
  firstmemberpointertailcall (8B) - mov rcx,[rcx]; jmp member - the offset-zero
      spelling. The disp8 members of the same census cluster extend
      memberpointertailcall instead.
  globalhandlerslottailcall (26B) - load a member-specific global handler
      slot, guard it, then jmp rax with rcx=[r8+0x2E0], rdx=r8.
  callresulttailcall / callresultwithsavedinttailcall / memberpointertailcall /
      vtableinstallstub - EXTENSIONS of declared rows: same instruction form,
      more frontier members.
  outrecorddescriptorinit (58B) - if rdx non-null, write three member-specific
      rip pointers + zero fields + 1.0f into the out-record; return 1.
  singleton-staticobjectfixup (103B) - install a member vtable into a global
      slot, vcall [rax+0x48] if the slot's object changed, register the member
      fn via 006B6700, conditional _aligned_free of a second member global.
  callresultwithsavedthistailcall (30B) - saved-this spelling of the
      CallResultWithSaved* idiom: forward (result, this) to a member op.
  guardedpairinvokefieldstore (54B) - call shared guard 002F2D60; if zero,
      call a member fn + shared 0044B960 and store the result into a member
      field; return 1.
  pairedstaticconststore - write member constants to two member statics.
  nullableglobaltaildispatch (17B) - load a member global; if non-null,
      jne-tail-dispatch to a member-specific function.

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_frontier_form_clusters.py [--write]
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
SIZED_STUB = 0x0016D6A0
SHARED_TEARDOWN = 0x00633390
FRAME_ADVANCE = 0x002F2530
REGISTER = 0x006B6700
GUARD_PAIR = {0x002F2D60, 0x0044B960}
RESET_DELEGATES = {0x00470050, 0x0046FFA0, 0x0051DDC0, 0x0051DBF0}

def leaf(m, c, j, x):
    return not c and not j and not x
def one_tail(m, c, j, x):
    return not c and len(j) == 1 and not x
def call_tail(m, c, j, x):
    return len(c) == 1 and len(j) == 1 and not x

FAMILIES = [
    ("frame-advance-continuation-adapters.tsv", 56,
     "mov M[rsp],rbx; push rdi; sub rsp,I; mov rbx,rcx; call T; mov edi,eax; "
     "test eax,eax; jne T; mov rbx,M[rsp]; add rsp,I; pop rdi; ret; mov rcx,rbx; "
     "call T; mov rbx,M[rsp]; mov eax,edi; add rsp,I; pop rdi; ret",
     lambda m, c, j, x: FRAME_ADVANCE in c and len(c) == 2 and not j and not x,
     "Presentation.EffectInstance frame-advance continuation adapters - EC-7 family C\n"
     "# call shared update 002F2530; if nonzero call the member-specific continuation;\n"
     "# return the shared result."),
    ("deletingdestructor-sharedteardown.tsv", 92,
     "push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov edi,edx; mov rbx,rcx; "
     "lea rax,M[rip]; mov M[rcx],rax; call T; nop; test dil,I; je T; test dil,I; "
     "jne T; mov rcx,rbx; call T; nop; jmp T; mov edx,I; mov rcx,rbx; call T; nop; "
     "mov rax,rbx; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda m, c, j, x: c == {SHARED_TEARDOWN, ALIGNED_FREE, SIZED_STUB} and not j and not x,
     "deleting destructors, shared-teardown two-deallocator spelling - EC-7 family C\n"
     "# install member vtable; call shared teardown 00633390; bit0 gates delete;\n"
     "# bit2 selects sized-delete stub 0016D6A0 over _aligned_free 00584730."),
    ("nativeleaf-fieldclear.tsv", None,
     "mov M[rcx],I; ret",
     lambda m, c, j, x: leaf(m, c, j, x) and m["imms"] == [0],
     "NativeLeaf.FieldClear - EC-7 family C\n"
     "# mov [rcx+off], 0; ret - field clear, widths 1/2/4/8."),
    ("nativeleaf-fieldconststore.tsv", None,
     "mov M[rcx],I; ret",
     lambda m, c, j, x: leaf(m, c, j, x) and len(m["imms"]) == 1 and m["imms"][0] != 0,
     "NativeLeaf.FieldConstStore - EC-7 family C\n"
     "# mov [rcx+off], member const (nonzero); ret - constant field initialiser."),
    ("nativeadapter-memberoffsettailcall.tsv", None,
     "add rcx,I; jmp T", one_tail,
     "NativeAdapter.MemberOffsetTailCall - EC-7 family C\n"
     "# add rcx, imm8/imm32; jmp member. The indexed\n"
     "# RelativeMemberAddressTailCall32/64 rows on this page are a different form."),
    ("nativeleaf-constantdwordreturn.tsv", 6,
     "mov eax,I; ret", leaf,
     "NativeLeaf.ConstantDwordReturn - EC-7 family C\n# mov eax, member const; ret"),
    ("nativeadapter-fieldresetoffsettailcall.tsv", 24,
     "mov M[rcx],I; mov edx,I; add rcx,I; jmp T",
     lambda m, c, j, x: not c and len(j) == 1 and j <= RESET_DELEGATES and not x,
     "NativeAdapter.FieldResetOffsetTailCall - EC-7 family C\n"
     "# zero a member field; edx=4; this+=off; tail-call one of four Presentation\n"
     "# clone helpers {00470050, 0046FFA0, 0051DDC0, 0051DBF0}."),
    ("nativeadapter-firstmemberpointertailcall.tsv", 8,
     "mov rcx,M[rcx]; jmp T", one_tail,
     "NativeAdapter.FirstMemberPointerTailCall - EC-7 family C\n"
     "# mov rcx, [rcx]; jmp member - the offset-zero spelling. Disp8/disp32\n"
     "# members of the same census cluster extend memberpointertailcall."),
    ("nativeadapter-memberpointertailcall.tsv", None,
     "mov rcx,M[rcx]; jmp T",
     lambda m, c, j, x: one_tail(m, c, j, x) and m["size"] in (9, 12),
     "NativeAdapter.MemberPointerTailCall - EC-7 family C\n"
     "# mov rcx, [rcx+off]; jmp member."),
    ("nativedispatch-globalhandlerslottailcall.tsv", 26,
     "mov rax,M[rip]; test rax,rax; je T; mov rdx,rcx; mov rcx,M[r8]; jmp rax; ret",
     leaf,
     "NativeDispatch.GlobalHandlerSlotTailCall - EC-7 family C\n"
     "# dispatch through a member-specific global handler slot: if set, jmp rax\n"
     "# with rcx=[r8+0x2E0], rdx=r8. No direct external targets."),
    ("nativeadapter-callresulttailcall.tsv", 21,
     "sub rsp,I; call T; mov rcx,rax; add rsp,I; jmp T", call_tail,
     "NativeAdapter.CallResultTailCall - EC-7 family C\n"
     "# call a fetch; forward the result to a member-specific op."),
    ("nativeleaf-fieldbytestore.tsv", None,
     "mov M[rcx],dl; ret", leaf,
     "NativeLeaf.FieldByteStore - EC-7 family C\n# mov byte [rcx+off], dl; ret"),
    ("nativeleaf-fieldbytegetter.tsv", None,
     "movzx eax,M[rcx]; ret",
     lambda m, c, j, x: leaf(m, c, j, x) and m["memw"] == [1],
     "NativeLeaf.FieldByteGetter - EC-7 family C\n# movzx eax, byte [rcx+off]; ret"),
    ("nativeleaf-fielddwordgetter.tsv", None,
     "mov eax,M[rcx]; ret", leaf,
     "NativeLeaf.FieldDwordGetter - EC-7 family C\n# mov eax, dword [rcx+off]; ret"),
    ("nativeleaf-fielddwordstore.tsv", None,
     "mov M[rcx],edx; ret", leaf,
     "NativeLeaf.FieldDwordStore - EC-7 family C\n# mov dword [rcx+off], edx; ret"),
    ("nativeadapter-outrecorddescriptorinit.tsv", 58,
     "test rdx,rdx; je T; lea rax,M[rip]; mov M[rdx],I; mov M[rdx],rax; "
     "lea rax,M[rip]; mov M[rdx],rax; lea rax,M[rip]; mov M[rdx],rax; "
     "mov M[rdx],I; mov M[rdx],I; mov al,I; ret",
     leaf,
     "NativeAdapter.OutRecordDescriptorInitReturnTrue - EC-7 family C\n"
     "# if rdx non-null, write three member-specific rip pointers plus zeroed\n"
     "# fields and 1.0f into the out-record; always return 1."),
    ("nativeadapter-callresultwithsavedinttailcall.tsv", 28,
     "push rbx; sub rsp,I; mov ebx,ecx; call T; mov rcx,rax; mov edx,ebx; "
     "add rsp,I; pop rbx; jmp T", call_tail,
     "NativeAdapter.CallResultWithSavedIntTailCall - EC-7 family C\n"
     "# save ecx across the call; forward (result, saved-int) to a member op."),
    ("nativeleaf-fieldqwordgetter.tsv", None,
     "mov rax,M[rcx]; ret", leaf,
     "NativeLeaf.FieldQwordGetter - EC-7 family C\n# mov rax, qword [rcx+off]; ret"),
    ("nativeleaf-fieldqwordstore.tsv", None,
     "mov M[rcx],rdx; ret", leaf,
     "NativeLeaf.FieldQwordStore - EC-7 family C\n# mov qword [rcx+off], rdx; ret"),
    ("nativeleaf-fieldfloatstore.tsv", None,
     "movss M[rcx],xmm1; ret", leaf,
     "NativeLeaf.FieldFloatStore - EC-7 family C\n# movss [rcx+off], xmm1; ret"),
    ("runtime-singleton-staticobjectfixup.tsv", 103,
     "sub rsp,I; mov M[rsp],I; lea rax,M[rip]; mov M[rip],rax; lea rax,M[rip]; "
     "cmp M[rip],rax; je T; mov rcx,M[rip]; mov rax,M[rcx]; lea rdx,M[rip]; "
     "call M[rax]; lea rcx,M[rip]; call T; nop; test M[rip],I; je T; "
     "mov rcx,M[rip]; call T; nop; add rsp,I; ret",
     lambda m, c, j, x: c == {REGISTER, ALIGNED_FREE} and not j and not x,
     "Runtime.Singleton.StaticObjectFixupRegisterRelease - EC-7 family C\n"
     "# install a member vtable into a global slot; if the slot's object changed,\n"
     "# vcall [rax+0x48](obj, member fn); register the member fn via 006B6700;\n"
     "# conditional _aligned_free of a second member global via 00584730."),
    ("nativeadapter-callresultwithsavedthistailcall.tsv", 30,
     "push rbx; sub rsp,I; mov rbx,rcx; call T; mov rcx,rax; mov rdx,rbx; "
     "add rsp,I; pop rbx; jmp T", call_tail,
     "NativeAdapter.CallResultWithSavedThisTailCall - EC-7 family C\n"
     "# saved-this spelling: forward (result, this) to a member op."),
    ("cxxobjectlifecycle-vtableinstallstub.tsv", 11,
     "lea rax,M[rip]; mov M[rcx],rax; ret", leaf,
     "CxxObjectLifecycle.VtableInstallStub - EC-7 family C\n"
     "# lea rax, [rip+vtable]; mov [rcx], rax; ret"),
    ("nativeadapter-guardedpairinvokefieldstore.tsv", 54,
     "push rbx; sub rsp,I; mov rbx,rcx; call T; test eax,eax; jne T; add rsp,I; "
     "pop rbx; ret; mov rcx,rbx; call T; call T; mov M[rbx],eax; mov eax,I; "
     "add rsp,I; pop rbx; ret",
     lambda m, c, j, x: GUARD_PAIR <= c and len(c) == 3 and not j and not x,
     "NativeAdapter.GuardedPairInvokeFieldStore - EC-7 family C\n"
     "# call shared guard 002F2D60; if zero, call a member fn + shared 0044B960\n"
     "# and store the result into a member field; return 1."),
    ("nativeleaf-pairedstaticconststore.tsv", None,
     "mov M[rip],I; mov M[rip],I; ret", leaf,
     "NativeLeaf.PairedStaticConstStore - EC-7 family C\n"
     "# write member constants to two member statics; ret"),
    ("nativeadapter-nullableglobaltaildispatch.tsv", 17,
     "mov rcx,M[rip]; test rcx,rcx; jne T; ret",
     lambda m, c, j, x: not c and not j and len(x) == 1,
     "NativeAdapter.NullableGlobalTailDispatch - EC-7 family C\n"
     "# load a member-specific global; if non-null, jne-tail-dispatch to a\n"
     "# member-specific function."),
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
