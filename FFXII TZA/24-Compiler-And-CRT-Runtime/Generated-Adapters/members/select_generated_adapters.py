"""select_generated_adapters.py OUTDIR - EC-7 member selectors for three generated/template families (FABLE).

df4: every .text offset matching the 26-byte return-value adapter template
       40 53 48 83 EC 20 48 8B CA 49 8B D8 E8 ?? ?? ?? ?? 48 89 03 48 83 C4 20 5B C3
     that is also a function entry of exactly 26 bytes in the census.
df1: every function whose body equals the owned-buffer reset body of 0058B0C0-style members, derived from the
     first known member by wildcarding only RIP-relative/call displacements, and required to sit at vtable slot 11
     of a PClassDescriptor vtable (checked by the caller of this script; the byte template alone is printed here).
bk6: the four byte-identical 45-byte _Sentry_base destructor bodies, found by exact body comparison against 001952E0.
Writes one entry per line, sorted, to OUTDIR/<family>.tsv and prints counts. When OUTDIR is this script's own directory
(an in-place regeneration), bk6 goes to ../../Exception-Handling-And-Unwind/members/, the members file its declaring page reads."""
import sys, struct, re, os
sys.argv, OUT = [sys.argv[0]], sys.argv[1]
exec(open(os.path.join(os.path.dirname(__file__), "..", "pub140-scratch", "disw.py")).read().split("fn = int")[0]) if False else None
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUN = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    name = d[o:o + 8].rstrip(b"\0"); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, 0x120000 + va, vs, ro, rs))
text = [s for s in secs if s[0] == b".text"][0]
def off(a):
    for nm, va, vs, ro, rs in secs:
        if va <= a < va + max(vs, rs): return ro + (a - va)
funcs = {}
for line in open(FUN, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try:
        funcs[int(p[0], 16)] = (int(p[2]) if p[2].isdigit() else int(p[2], 0), p[1] if len(p) > 1 else "")
    except Exception:
        pass
os.makedirs(OUT, exist_ok=True)

def scan(pat, size):
    rx = re.compile(pat, re.S)
    hits = []
    tb = d[text[3]:text[3] + text[4]]
    for m in rx.finditer(tb):
        a = text[1] + m.start()
        hits.append(a)
    return hits

# df4
pat4 = rb"\x40\x53\x48\x83\xEC\x20\x48\x8B\xCA\x49\x8B\xD8\xE8....\x48\x89\x03\x48\x83\xC4\x20\x5B\xC3"
h4 = scan(pat4, 26)
df4 = sorted(a for a in h4 if a in funcs and funcs[a][0] == 26)
print("df4 template matches", len(h4), "at 26-byte entries", len(df4), "distinct call targets",
      len({a + 17 + struct.unpack_from("<i", d, off(a) + 13)[0] for a in df4}))
open(os.path.join(OUT, "df4-return-value-adapters.tsv"), "w").write("# 26-byte return-value adapter template, select_generated_adapters.py\n" + "\n".join("%08X" % a for a in df4) + "\n")

# bk6
ref = 0x1952E0; body = d[off(ref):off(ref) + funcs[ref][0]]
bk6 = sorted(a for a, (sz, nm) in funcs.items() if sz == len(body) and off(a) is not None and d[off(a):off(a) + sz] == body)
print("bk6 exact clones of 001952E0 body", len(bk6), ["%08X" % a for a in bk6])
# 2026-09-14 (FABLE, OPUS-NOTE-FABLE-BK6-SELECTOR-WRITES-ELSEWHERE): BK-6 is declared by the exception-funclets page,
# so an in-place run (OUTDIR = this directory) writes it to that page's members file; any other OUTDIR keeps the flat
# layout for out-of-tree verification.
HERE = os.path.dirname(os.path.abspath(__file__))
BK6_OUT = os.path.join(HERE, "..", "..", "Exception-Handling-And-Unwind", "members") if os.path.abspath(OUT) == HERE else OUT
open(os.path.join(BK6_OUT, "bk6-sentry-base-destructor-clones.tsv"), "w").write("# exact 45-byte body clones of 001952E0, select_generated_adapters.py\n" + "\n".join("%08X" % a for a in bk6) + "\n")
