"""guard_adapter_registrars.py - what the 145 'CFG static-guard adapters' tear down (S-3, 2026-09-14, FABLE).

For each member of ../../Static-Initialization-And-Teardown/members/empty-dtor-teardown-wrappers.tsv (12 bytes:
lea rcx,[static] ; jmp 0016D6A0) this finds every REX.W lea/mov rip-relative reference to the member's address in .text,
the registering call that follows (atexit 00808B90 or other), and the registrar. For the 383-byte thread-safe local-static
registrars it reads the two lazy-static descriptor accessors called after _Init_thread_header (008092FC) and the code
pointer stored into the static, and names each accessor's descriptor record by the name string its initialiser stores at
record +0x30. Output: guard-adapter-registrars.tsv next to this script.

Usage (from Database/Tools/work/FABLE/pub140-scratch, which provides disw.py):  python <this> <members tsv>"""
import sys, struct, bisect, collections, os
exec(open('disw.py').read().split("fn = int")[0])

members = [int(l.strip(), 16) for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
mset = set(members)
TEXT_LO, TEXT_HI = 0x121000, 0x8C2000
t = bytes(d)
lo, hi = off(TEXT_LO), off(TEXT_HI)


def riptarget(x):
    return x.address + x.size + int(x.op_str.split("rip + ")[1].rstrip("]"), 16)


refs = collections.defaultdict(list)
for o in range(lo, hi - 7):
    if t[o] in (0x48, 0x4C) and t[o + 1] in (0x8D, 0x8B) and (t[o + 2] & 0xC7) == 0x05:
        va = TEXT_LO + (o - lo)
        tgt = va + 7 + struct.unpack_from("<i", t, o + 3)[0]
        if tgt in mset:
            refs[tgt].append(va)


def cstr(va):
    o = off(va)
    return bytes(d[o:o + 40]).split(b"\0")[0].decode("latin1")


def descriptor_name(acc):
    """accessor -> the record it returns (lea into 01F2Exxx) -> the string stored at record+0x30 anywhere in .text."""
    rec = None
    for x in md.disasm(d[off(acc):off(acc) + funcs[acc]], acc):
        if x.mnemonic == "lea" and "rip +" in x.op_str and 0x1F2E000 <= riptarget(x) < 0x1F2F000:
            rec = riptarget(x)
    if rec is None:
        return "?"
    want = rec + 0x30
    for o in range(lo, hi - 7):
        if t[o] == 0x48 and t[o + 1] == 0x89 and (t[o + 2] & 0xC7) == 0x05:
            va = TEXT_LO + (o - lo)
            if va + 7 + struct.unpack_from("<i", t, o + 3)[0] == want:
                for x in md.disasm(d[off(va - 7):off(va)], va - 7):
                    if x.mnemonic == "lea" and "rip +" in x.op_str:
                        return cstr(riptarget(x))
    return "?"


names_cache = {}
out = ["adapter\tstatic\tregistrar\tregistrar_bytes\tregistration\tfirst_descriptor\tsecond_descriptor\tstored_code_pointer"]
for m in members:
    body = list(md.disasm(t[off(m):off(m) + 12], m))
    static = "%08X" % riptarget(body[0])
    for r in refs[m] or [None]:
        if r is None:
            out.append("%08X\t%s\t-\t-\tnone\t-\t-\t-" % (m, static))
            continue
        nxt = next((x.op_str for x in md.disasm(t[off(r):off(r) + 40], r) if x.mnemonic in ("call", "jmp")), "?")
        starts = sorted(funcs)
        k = bisect.bisect_right(starts, r) - 1
        reg = starts[k]
        a = b = cp = "-"
        if funcs[reg] == 383:
            ins = list(md.disasm(d[off(reg):off(reg) + funcs[reg]], reg))
            cs = [x.op_str for x in ins if x.mnemonic == "call"]
            i = cs.index("0x8092fc")
            for acc in (cs[i + 1], cs[i + 2]):
                if acc not in names_cache:
                    names_cache[acc] = descriptor_name(int(acc, 16))
            a, b = names_cache[cs[i + 1]], names_cache[cs[i + 2]]
            for x in ins:
                if x.mnemonic == "lea" and x.op_str.startswith("rax, [rip + ") and riptarget(x) < TEXT_HI:
                    cp = "%08X" % riptarget(x)
        out.append("%08X\t%s\t%08X\t%d\t%s\t%s\t%s\t%s" % (m, static, reg, funcs[reg],
                                                         "atexit" if nxt == "0x808b90" else nxt, a, b, cp))
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard-adapter-registrars.tsv")
open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print(len(out) - 1, "rows ->", dst)
