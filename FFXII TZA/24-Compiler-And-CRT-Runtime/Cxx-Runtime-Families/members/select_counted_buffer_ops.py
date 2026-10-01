"""select_counted_buffer_ops.py - EC-7 family C member selectors for the counted-buffer
record idioms declared on object-construction-destruction-and-static-lifetime.md
(FABLE-REQ-SWE2-EC7-LIFECYCLE-FORM-BATCH).

The record is {dword size|own-flag, qword buf}: bit 31 of the first field is the
"this record owns the buffer" flag, and 00584730 is the null-guarded
_aligned_free wrapper. Four generated spellings around it:

  counted-buffer-field-replace-98b.tsv  (98B x21) - query a member-specific getter for
      {size|flags, buf}, allocate a replacement via a member-specific allocator,
      conditional-free the record's old buffer, commit {size, ptr}.
  counted-buffer-field-replace-99b.tsv  (99B x20) - the same idiom, second spelling
      (edx-side flag test, cmp rcx,rax).
  counted-buffer-list-materialisation.tsv (222B x17) - count the elements of the
      intrusive list rooted at a member-specific global, allocate count*8 via
      0017D260, zero-fill, conditional-free the record's old buffer, commit
      {count, ptr}, then copy the list into the array. Returns 0 or 0xD.
  counted-buffer-release-and-clear.tsv (68B x12) - if the own-flag is clear, free the
      buffer; either way zero the record's {size, ptr} fields.

Each group is ONE instruction-form skeleton (forms_of.py normalisation) and collapses
to ONE operand-aware byte image. Members whose skeleton matches but whose external
direct targets fall outside the family's controlled set refuse the write.

Pool = frontier | (prior members - A-measured).
Reads: Database/Tools/work/exe/FFXII_TZA.exe, Database/Tools/work/graph/functions.tsv.
Usage: python select_counted_buffer_ops.py [--write]
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
LIST_ALLOC = 0x0017D260

FAMILIES = [
    ("counted-buffer-field-replace-98b.tsv", 98,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rcx,rdx; mov rbx,r8; "
     "call T; mov edi,M[rax]; mov rdx,M[rax]; btr edi,I; mov ecx,edi; call T; "
     "mov rcx,M[rbx]; mov rsi,rax; mov eax,M[rbx]; cmp rcx,rsi; je T; shr eax,I; "
     "not al; test al,I; je T; test rcx,rcx; je T; call T; mov M[rbx],rsi; "
     "mov rsi,M[rsp]; mov M[rbx],edi; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda ts: ts - {ALIGNED_FREE} and len(ts - {ALIGNED_FREE}) == 2 and ALIGNED_FREE in ts,
     "counted-buffer field replace, 98-byte spelling - EC-7 family C\n"
     "# getter(key) -> {size|flags, buf}; alloc(size); conditional-free the record's\n"
     "# old buffer via 00584730 when the own-flag permits; commit {size, ptr}."),
    ("counted-buffer-field-replace-99b.tsv", 99,
     "mov M[rsp],rbx; mov M[rsp],rsi; push rdi; sub rsp,I; mov rcx,rdx; mov rbx,r8; "
     "call T; mov edi,M[rax]; mov rdx,M[rax]; btr edi,I; mov ecx,edi; call T; "
     "mov rcx,M[rbx]; mov rsi,rax; cmp rcx,rax; je T; mov edx,M[rbx]; shr edx,I; "
     "not dl; test dl,I; je T; test rcx,rcx; je T; call T; mov M[rbx],rsi; "
     "mov rsi,M[rsp]; mov M[rbx],edi; mov rbx,M[rsp]; add rsp,I; pop rdi; ret",
     lambda ts: ALIGNED_FREE in ts and len(ts - {ALIGNED_FREE}) == 2,
     "counted-buffer field replace, 99-byte spelling - EC-7 family C\n"
     "# Same idiom as the 98-byte spelling with edx-side flag test."),
    ("counted-buffer-list-materialisation.tsv", 222,
     "mov M[rsp],rbx; mov M[rsp],rbp; push rsi; sub rsp,I; mov rax,M[rip]; xor ebp,ebp; "
     "mov rsi,rdx; mov ebx,ebp; mov rcx,rax; test rax,rax; je T; mov rcx,M[rcx]; inc ebx; "
     "test rcx,rcx; jne T; mov M[rsp],r14; cmp ebx,M[rdx]; je T; test ebx,ebx; je T; "
     "mov r14d,ebx; mov edx,I; shl r14,I; mov rcx,r14; call T; mov rbp,rax; "
     "test rax,rax; je T; test ebx,ebx; je T; mov M[rsp],rdi; mov rdi,rax; shr r14,I; "
     "xor eax,eax; mov rcx,r14; rep stosq M[rdi],rax; mov rdi,M[rsp]; jmp T; "
     "test ebx,ebx; jne T; mov rcx,M[rsi]; cmp rcx,rbp; je T; mov eax,M[rsi]; "
     "shr eax,I; not al; test al,I; je T; test rcx,rcx; je T; call T; mov M[rsi],rbp; "
     "mov M[rsi],ebx; mov rax,M[rip]; mov rcx,M[rsi]; test rax,rax; je T; "
     "mov M[rcx],rax; lea rcx,M[rcx]; mov rax,M[rax]; test rax,rax; jne T; "
     "xor eax,eax; mov r14,M[rsp]; mov rbx,M[rsp]; mov rbp,M[rsp]; add rsp,I; "
     "pop rsi; ret ; mov eax,I; jmp T",
     lambda ts: ts == {LIST_ALLOC, ALIGNED_FREE},
     "counted-buffer list materialisation, 222-byte form - EC-7 family C\n"
     "# Count the intrusive list at a member-specific global; if the record's count\n"
     "# differs, allocate count*8 via 0017D260, zero-fill, conditional-free the old\n"
     "# buffer via 00584730, commit {count, ptr}; copy the list into the array."),
    ("counted-buffer-release-and-clear.tsv", 68,
     "push rbx; sub rsp,I; mov M[rsp],I; mov rbx,rcx; mov eax,M[rcx]; shr eax,I; "
     "not al; test al,I; je T; mov rcx,M[rcx]; test rcx,rcx; je T; call T; nop ; "
     "xor eax,eax; mov M[rbx],rax; mov M[rbx],eax; jmp T; xor eax,eax; mov M[rcx],rax; "
     "mov M[rcx],eax; add rsp,I; pop rbx; ret",
     lambda ts: ts == {ALIGNED_FREE},
     "counted-buffer release-and-clear, 68-byte form - EC-7 family C\n"
     "# If the record's own-flag is clear, free the buffer via 00584730; either way\n"
     "# zero the {size, ptr} fields."),
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
    toks, targets = [], set()
    for ins in md.disasm(d[off:off + size], a):
        ops = []
        for op in ins.operands:
            if op.type == X86_OP_REG:
                ops.append(md.reg_name(op.reg))
            elif op.type == X86_OP_IMM:
                if ins.mnemonic in ("call", "jmp") or ins.mnemonic.startswith("j"):
                    ops.append("T")
                    if ins.mnemonic in ("call", "jmp") and not (a <= op.imm < a + size):
                        targets.add(op.imm)
                else:
                    ops.append("I")
            elif op.type == X86_OP_MEM:
                ops.append("M[rip]" if op.mem.base == X86_REG_RIP else
                           "M[%s%s]" % (md.reg_name(op.mem.base) if op.mem.base else "",
                                        "+" + md.reg_name(op.mem.index) if op.mem.index else ""))
        toks.append((ins.mnemonic + " " + ",".join(ops)).strip())
    return "; ".join(toks), targets

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
    cache = {a: form_and_targets(md, d, secs, a, sizes[a]) for a in pool}
    ok = True
    results = {}
    for tsv, sz, skel, tcheck, header in FAMILIES:
        members = sorted(a for a, (f, ts) in cache.items()
                         if sizes[a] == sz and f == norm(skel) and tcheck(ts))
        if not members:
            print("REFUSE %s: skeleton matched nobody" % tsv); ok = False; continue
        bad = [a for a in members if a in a_set]
        if bad:
            print("REFUSE %s: %d member(s) measure A" % (tsv, len(bad))); ok = False; continue
        results[tsv] = (members, header)
        tg = collections.Counter(t for a in members for t in cache[a][1])
        print("%-42s %3d members | targets %s" %
              (tsv, len(members), ", ".join("%08X x%d" % kv for kv in tg.most_common(6))))
    if not ok or not write:
        print("dry run" if ok else "refused"); return
    for tsv, (members, header) in results.items():
        with io.open(os.path.join(ROOT, tsv), "w", encoding="utf-8", newline="\n") as f:
            f.write("# " + header.replace("\n", "\n# ") + "\n")
            f.write("address\ttargets\n")
            for a in members:
                f.write("%08X\t%s\n" % (a, ",".join("%08X" % t for t in sorted(cache[a][1]))))
        print("wrote", tsv, len(members))

if __name__ == "__main__":
    main()
