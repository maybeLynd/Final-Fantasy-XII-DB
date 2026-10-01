"""retool.py - OPUS's reusable static-RE lookups over the certified image (2026-09-30). Replaces one-off inline snippets.

  python retool.py dis ADDR [--to ADDR2] [--n 60] [--grep PAT]   disassemble a function (or a range), rip targets and strings annotated
  python retool.py refs LO [HI] [--stores]                       every rip-relative reference into [LO, HI] (default HI = LO)
  python retool.py callers ADDR [ADDR ...]                       direct callers (call/jmp) and rip references of each address
  python retool.py qwords LO [HI]                                aligned qwords in any section whose value lies in [LO, HI]
  python retool.py site ADDR [--before 20] [--after 5]           the instructions around one address inside its function
  python retool.py str ADDR                                      the C string at ADDR

The function list is the v4 extents (uc1_band.apply_extents) plus the UC-1 frontier bodies. The reference/caller scan is
cached in Tools/work/OPUS/_re_cache.pkl, keyed by the image hash and the extents, so it runs once (about 60-120 s).
"""
import argparse, hashlib, os, pickle, re as _re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
WORK = os.path.join(DB, "Tools", "work", "OPUS")
sys.path.insert(0, os.path.join(DB, "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import rc9_channels as R  # noqa: E402
import uc1_band  # noqa: E402

CACHE = os.path.join(WORK, "_re_cache.pkl")   # a derived cache in the ignored work tree, keyed by image + extents
RIP = 41


def h(x):
    return int(x, 16)


def sizes():
    s, _ = uc1_band.apply_extents(dict(R.ext))
    for st_, sz in uc1_band.load()["frontier"].items():
        s.setdefault(st_, sz)
    return s


def cstr(a, n=96):
    d = R.at(a, n) or b""
    t = d.split(b"\0")[0]
    return t.decode("latin1", errors="replace") if len(t) >= 3 and all(32 <= c < 127 or c in (9, 10, 13) for c in t) else None


def ann(i):
    for op in i.operands:
        if op.type == 3 and op.mem.base == RIP:
            g = i.address + i.size + op.mem.disp
            s = cstr(g) if 0x01C00000 <= g < 0x02000000 else None
            return "  ; -> %08X%s" % (g, " %r" % s if s else "")
    if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x"):
        return ""
    for op in i.operands:
        if op.type == 2 and 0x01C00000 <= op.imm < 0x02000000:
            s = cstr(op.imm)
            if s:
                return "  ; %r" % s
    return ""


def fmt(i):
    return "%08X  %-8s %s%s" % (i.address, i.mnemonic, i.op_str, ann(i))


def func_of(a, sz=None):
    sz = sz or sizes()
    best = None
    for f, n in sz.items():
        if f <= a < f + n and (best is None or f > best):
            best = f
    return best


def scan():
    sz = sizes()
    key = hashlib.sha1((open(R.b.EXE, "rb").read(1 << 20).hex() + repr(sorted(sz.items()))).encode()).hexdigest()
    if os.path.isfile(CACHE):
        c = pickle.load(open(CACHE, "rb"))
        if c.get("key") == key:
            return c
    refs, calls = {}, {}
    for f, n in sz.items():
        d = R.at(f, n)
        if not d:
            continue
        for i in R.md.disasm(d, f):
            if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == 2:
                calls.setdefault(i.operands[0].imm, set()).add((f, i.address))
            for k, op in enumerate(i.operands):
                if op.type == 3 and op.mem.base == RIP:
                    g = i.address + i.size + op.mem.disp
                    kind = "lea" if i.mnemonic == "lea" else ("W" if k == 0 and i.mnemonic not in ("cmp", "test", "push") else "R")
                    refs.setdefault(g, set()).add((f, i.address, kind))
    c = {"key": key, "refs": refs, "calls": calls}
    pickle.dump(c, open(CACHE, "wb"))
    return c


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("dis"); p.add_argument("addr"); p.add_argument("--to"); p.add_argument("--n", type=int, default=0); p.add_argument("--grep")
    p = sub.add_parser("refs"); p.add_argument("lo"); p.add_argument("hi", nargs="?"); p.add_argument("--stores", action="store_true")
    p = sub.add_parser("callers"); p.add_argument("addrs", nargs="+")
    p = sub.add_parser("qwords"); p.add_argument("lo"); p.add_argument("hi", nargs="?")
    p = sub.add_parser("site"); p.add_argument("addr"); p.add_argument("--before", type=int, default=20); p.add_argument("--after", type=int, default=5)
    p = sub.add_parser("str"); p.add_argument("addr")
    p = sub.add_parser("vt"); p.add_argument("addrs", nargs="+")   # function -> vtables naming it + RTTI class + slot
    p = sub.add_parser("grep"); p.add_argument("pattern"); p.add_argument("--lo"); p.add_argument("--hi")  # regex over every instruction
    a = ap.parse_args()
    if a.cmd == "dis":
        start = h(a.addr)
        n = R.ext.get(start) or sizes().get(start) or 0x400
        end = h(a.to) + 1 if a.to else start + n
        cnt = 0
        for i in R.md.disasm(R.at(start, end - start), start):
            line = fmt(i)
            if a.grep and not _re.search(a.grep, line):
                continue
            print(line)
            cnt += 1
            if a.n and cnt >= a.n:
                break
    elif a.cmd == "refs":
        lo = h(a.lo); hi = h(a.hi) if a.hi else lo
        c = scan()
        for g in sorted(x for x in c["refs"] if lo <= x <= hi):
            for f, ad, kind in sorted(c["refs"][g]):
                if a.stores and kind == "R":
                    continue
                i = next(R.md.disasm(R.at(ad, 16), ad, 1))
                print("%08X %s  in %08X: %s" % (g, kind, f, fmt(i)))
    elif a.cmd == "callers":
        c = scan()
        for x in a.addrs:
            t = h(x)
            cs = sorted(c["calls"].get(t, ()))
            rs = sorted(c["refs"].get(t, ()))
            print("%08X  direct: %s" % (t, " ".join("%08X@%08X" % y for y in cs) or "-"))
            print("          rip refs: %s" % (" ".join("%08X@%08X(%s)" % y for y in rs) or "-"))
    elif a.cmd == "qwords":
        import pefile
        lo = h(a.lo); hi = h(a.hi) if a.hi else lo
        pe = pefile.PE(R.b.EXE, fast_load=True)
        base = pe.OPTIONAL_HEADER.ImageBase
        for s in pe.sections:
            data = s.get_data(); va = base + s.VirtualAddress
            for off in range(0, len(data) - 7, 8):
                q = struct.unpack_from("<Q", data, off)[0]
                if lo <= q <= hi:
                    print("%08X in %s holds %08X" % (va + off, s.Name.rstrip(b"\0").decode(), q))
    elif a.cmd == "site":
        t = h(a.addr)
        sz = sizes()
        f = func_of(t, sz)
        ins = list(R.md.disasm(R.at(f, sz[f]), f))
        k = next(j for j, i in enumerate(ins) if i.address >= t)
        print("in %08X:" % f)
        for i in ins[max(0, k - a.before):k + a.after + 1]:
            print(("> " if i.address == t else "  ") + fmt(i))
    elif a.cmd == "str":
        print(repr(cstr(h(a.addr), 256)))
    elif a.cmd == "grep":
        rx = _re.compile(a.pattern)
        lo = h(a.lo) if a.lo else 0
        hi = h(a.hi) if a.hi else 1 << 40
        for f, n in sorted(sizes().items()):
            if not lo <= f < hi:
                continue
            d = R.at(f, n)
            if not d:
                continue
            for i in R.md.disasm(d, f):
                t = "%s %s" % (i.mnemonic, i.op_str)
                if rx.search(t):
                    print("%08X %s" % (f, fmt(i)))
    elif a.cmd == "vt":
        for x in a.addrs:
            t = h(x)
            hits = qword_sites(t)
            if not hits:
                print("%08X  named by no qword (not a vtable slot)" % t)
            for site in hits:
                vt, cls = vtable_start(site)
                print("%08X  at %08X = vtable %s slot %s  class %s" % (
                    t, site, "%08X" % vt if vt else "?", (site - vt) // 8 if vt else "?", cls or "?"))


def qword_sites(value):
    import pefile
    pe = pefile.PE(R.b.EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    out = []
    for s in pe.sections:
        data = s.get_data()
        for off in range(0, len(data) - 7, 8):
            if struct.unpack_from("<Q", data, off)[0] == value:
                out.append(base + s.VirtualAddress + off)
    return out


def rtti_class(vt):
    """MSVC x64: [vt - 8] -> complete object locator (signature 1); COL + 0x0C = RVA of the type descriptor, whose
    name (".?AV...@@") is at + 0x10. Returns the demangled-ish class name, or None when vt - 8 is not a locator."""
    col = struct.unpack("<Q", R.at(vt - 8, 8))[0]
    d = R.at(col, 0x18) if col else None
    if not d or struct.unpack_from("<I", d, 0)[0] != 1:
        return None
    base = col - struct.unpack_from("<I", d, 0x14)[0]           # COL + 0x14 = RVA of the COL itself
    td = base + struct.unpack_from("<I", d, 0x0C)[0]
    raw = R.at(td + 0x10, 200) or b""
    name = raw.split(b"\0")[0].decode("latin1", errors="replace")
    if not name.startswith(".?A"):
        return None
    if "?$" in name:
        return name          # a template instance: the simple split below would garble it, so give the raw mangled name
    parts = name[4:].rstrip("@").split("@")
    return "::".join(reversed([p for p in parts if p]))


def vtable_start(site, back=64):
    """Walk back from a slot to the first slot whose preceding qword is a complete object locator."""
    for k in range(back):
        vt = site - 8 * k
        cls = rtti_class(vt)
        if cls:
            return vt, cls
    return None, None


if __name__ == "__main__":
    main()
