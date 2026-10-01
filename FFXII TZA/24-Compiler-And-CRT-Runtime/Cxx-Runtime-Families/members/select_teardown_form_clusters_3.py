"""select_teardown_form_clusters_3.py - EC-7 family C member selectors, third
frontier form-cluster batch (SWE2-EC7-FRONTIER-FORM-CLUSTERS-3), declared on
object-construction-destruction-and-static-lifetime.md.

Ref-flag container release siblings of the declared aligned-free rows, plus
two std::vector teardown spellings. Every group is ONE operand-aware
instruction-form skeleton at a fixed body size:

  refflagsiblingalignedfreeinit (98B) - call two member ops on arg1
      (this-out + init); if ref flag bit31 set and count > 1, aligned-free
      [rbx+0x40] via 00584730 and clear the fields; call a member op on
      this; return 1.
  refflagsiblingalignedfreereleasethis (60B) - if this->+8 ref flag bit31
      is set and [this+0x10] non-null, aligned-free it via 00584730 and
      clear both fields.
  refflagsiblingalignedfreetail (93B) - call a member teardown on this;
      call a second member op; if the ref flag releases, aligned-free
      [rbx+0x20] via 00584730, clear fields, tail-call a member finisher.
  vectordestroydeallocloop (149B) - iterate the [begin,end) element range
      calling vcall slot 0 (dtor) per 0x18B element, then release the
      buffer through allocator vcall [r9+0x18] with computed byte size.
  vectorbufferrelease (86B) - compute element count via the /24 magic
      multiply and release the buffer through allocator vcall [r9+0x18].

Pool = frontier | (prior members - A-measured); A beats a declaration.
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_teardown_form_clusters_3.py [--write]
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
ALIGNED_FREE = 0x00584730

def norm(s):
    return "; ".join(t.strip() for t in s.split(";"))

def leaf(m, c, j, x):
    return not c and not j and not x

FAMILIES = [
    ("nativeadapter-refflagsiblingalignedfreeinit.tsv", 98,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rdx; mov rcx,rdx; call T; "
     "mov rcx,rbx; call T; nop; mov ecx,M[rbx]; mov eax,ecx; shr eax,I; "
     "not al; test al,I; je T; btr ecx,I; cmp ecx,I; jbe T; mov rcx,M[rbx]; "
     "test rcx,rcx; je T; call T; xor eax,eax; mov M[rbx],rax; mov M[rbx],eax; "
     "mov rcx,rbx; call T; nop; mov al,I; add rsp,I; pop rbx; ret",
     lambda m, c, j, x: ALIGNED_FREE in c and len(c) == 4 and not j and not x,
     "NativeAdapter.RefFlagSiblingAlignedFreeInit - EC-7 family C\n"
     "# call two member ops on arg1; if ref flag bit31 set and count > 1,\n"
     "# aligned-free [rbx+0x40] via 00584730 and clear the fields; call a\n"
     "# member op on this; return 1."),
    ("nativeadapter-refflagsiblingalignedfreereleasethis.tsv", 60,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; mov eax,M[rcx]; "
     "shr eax,I; not al; test al,I; je T; mov rcx,M[rcx]; test rcx,rcx; "
     "je T; call T; nop; xor eax,eax; mov M[rbx],rax; mov M[rbx],eax; "
     "add rsp,I; pop rbx; ret",
     lambda m, c, j, x: c == {ALIGNED_FREE} and not j and not x,
     "NativeAdapter.RefFlagSiblingAlignedFreeReleaseThis - EC-7 family C\n"
     "# if this->+8 ref flag bit31 is set and [this+0x10] non-null,\n"
     "# aligned-free it via 00584730 and clear both fields."),
    ("nativeadapter-refflagsiblingalignedfreetail.tsv", 93,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; call T; nop; "
     "mov rcx,rbx; call T; nop; mov ecx,M[rbx]; mov eax,ecx; shr eax,I; "
     "not al; test al,I; je T; btr ecx,I; cmp ecx,I; jbe T; mov rcx,M[rbx]; "
     "test rcx,rcx; je T; call T; nop; xor eax,eax; mov M[rbx],rax; "
     "mov M[rbx],eax; mov rcx,rbx; add rsp,I; pop rbx; jmp T",
     lambda m, c, j, x: ALIGNED_FREE in c and len(c) == 3 and len(j) == 1 and not x,
     "NativeAdapter.RefFlagSiblingAlignedFreeTail - EC-7 family C\n"
     "# call a member teardown on this; call a second member op; if the ref\n"
     "# flag releases, aligned-free [rbx+0x20] via 00584730, clear fields,\n"
     "# tail-call a member finisher."),
    ("nativeleaf-vectordestroydeallocloop.tsv", 149,
     "push rdi; sub rsp,I; mov M[rsp],I; mov M[rsp],rbx; mov M[rsp],rsi; "
     "mov rsi,rcx; mov rdi,M[rcx]; mov rbx,M[rcx]; cmp rbx,rdi; jae T; "
     "nop M[rax+rax]; mov rax,M[rbx]; xor edx,edx; mov rcx,rbx; call M[rax]; "
     "nop; add rbx,I; cmp rbx,rdi; jb T; mov r10,M[rsi]; test r10,r10; "
     "je T; lea rcx,M[rsi]; mov r9,M[rcx]; mov r8,M[rsi]; sub r8,r10; "
     "movabs rax,I; imul r8; sar rdx,I; mov rax,rdx; shr rax,I; add rdx,rax; "
     "lea r8,M[rdx+rdx]; shl r8,I; mov rdx,r10; call M[r9]; nop; "
     "mov rbx,M[rsp]; mov rsi,M[rsp]; add rsp,I; pop rdi; ret",
     leaf,
     "NativeLeaf.VectorDestroyDeallocLoop - EC-7 family C\n"
     "# iterate the [begin,end) element range calling vcall slot 0 (dtor)\n"
     "# per 0x18B element, then release the buffer through allocator vcall\n"
     "# [r9+0x18] with the computed byte size. 3 byte images, ONE form."),
    ("nativeleaf-vectorbufferrelease.tsv", 86,
     "sub rsp,I; mov M[rsp],I; mov r8,rcx; mov r10,M[rcx]; test r10,r10; "
     "je T; add rcx,I; mov r9,M[rcx]; mov r8,M[r8]; sub r8,r10; movabs rax,I; "
     "imul r8; sar rdx,I; mov rax,rdx; shr rax,I; add rdx,rax; "
     "lea r8,M[rdx+rdx]; shl r8,I; mov rdx,r10; call M[r9]; nop; add rsp,I; ret",
     leaf,
     "NativeLeaf.VectorBufferRelease - EC-7 family C\n"
     "# compute element count via the /24 magic multiply and release the\n"
     "# buffer through allocator vcall [r9+0x18]. 3 byte images, ONE form."),
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
