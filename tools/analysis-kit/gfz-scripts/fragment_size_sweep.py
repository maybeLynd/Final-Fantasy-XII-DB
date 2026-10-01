"""One-off integrity sweep (OPUS, 2026-09-29): find page citations that size a function by its FIRST chained .pdata fragment.

Two corrections today (CON-170: 003266DB; CON-172: 002E45E0 '40-byte leaf') came from reading a shrink-wrapped function's
first unwind fragment as the whole function. This looks for the same shape across the corpus: a cited address that begins a
.pdata fragment whose UNWIND_INFO is NOT chained (a function root) but which has chained fragments after it, cited next to
a byte size equal to that first fragment's length (not the catalogue size). Also reports sizes cited for an address that is
itself a chained fragment (not a function start at all).

Output: one TSV row per hit - page, line, address, cited size, first-fragment size, catalogue size, kind.
"""
import io, os, re, struct, sys
import pefile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB = os.path.join(ROOT, "FFXII TZA")
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(BASE + s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData, s.Name.rstrip(b"\0").decode()) for s in pe.sections]


def OFF(va):
    for st, raw, rs, _n in SECS:
        if st <= va < st + rs:
            return raw + va - st
    raise ValueError


pd = next(s for s in SECS if s[3] == ".pdata"); praw = blob[pd[1]:pd[1] + pd[2]]
pent = {}
for j in range(0, len(praw) - 11, 12):
    b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
    if b_:
        pent[BASE + b_] = (BASE + e_, BASE + u_)


def chained_to(begin):
    u = pent[begin][1]; h = blob[OFF(u):OFF(u) + 4]
    if not (h[0] >> 3) & 4:
        return None
    c = OFF(u) + 4 + 2 * ((h[2] + 1) & ~1)
    return BASE + struct.unpack("<I", blob[c:c + 4])[0]


root_of = {}
for b in pent:
    r, seen = b, set()
    while r in pent and r not in seen:
        seen.add(r); n = chained_to(r)
        if n is None:
            break
        r = n
    root_of[b] = r
has_chain = {r for b, r in root_of.items() if b != r}
sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass

ADDR = re.compile(r"`?\b(00[0-9A-Fa-f]{6})\b`?")
SIZE = re.compile(r"\b(\d{1,5})(?:[- ]byte|\s?B\b)")
out = []
for dp, dn, fn in os.walk(DB):
    if any(x in dp for x in ("_experiments" + os.sep + "evidence", "candidates")):
        continue
    for f in fn:
        if not f.endswith(".md") or f in ("AUDIT-LOG.md", "PROGRAM-STATE.md"):
            continue
        path = os.path.join(dp, f); rel = os.path.relpath(path, DB)
        for ln, line in enumerate(io.open(path, encoding="utf-8", errors="replace"), 1):
            addrs = [(m.start(), int(m.group(1), 16)) for m in ADDR.finditer(line)]
            if not addrs:
                continue
            for sm in SIZE.finditer(line):
                n = int(sm.group(1))
                # the address nearest before the size on the same line
                prior = [a for pos, a in addrs if pos < sm.start()]
                if not prior:
                    continue
                a = prior[-1]
                if a in has_chain and a in pent:
                    first = pent[a][0] - a
                    if n == first and sizes.get(a) not in (None, n):
                        out.append((rel, ln, "%08X" % a, n, first, sizes.get(a), "first-fragment size cited for a chained function"))
                elif a in pent and root_of.get(a, a) != a:
                    frag = pent[a][0] - a
                    if n == frag:
                        out.append((rel, ln, "%08X" % a, n, frag, sizes.get(root_of[a]), "size of a chained fragment of %08X" % root_of[a]))
for r in sorted(set(out)):
    print("\t".join(str(x) for x in r))
print("HITS %d" % len(set(out)), file=sys.stderr)
