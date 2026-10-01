"""RC-29 side result: who requests title_menu.mrp (kind 7 0x3B) and E3_Logo.mrp (0x89)? (SWE2-DATA 2026-09-30), static.

Every raw call/jmp/jcc site of the eight request entry points (pool: 00249180, 00249210, 002493D0, 00249350,
00249320; path: 0032E400, 0032E620, 0032E3F0) is read with its 14 preceding instructions in the owning listed
function. A site is a candidate when an id-carrying register (r8d for the pool family, edx for the path family) is
formed there from a constant equal to the id, or from 'lea reg, [rdx + k]' / 'lea reg, [r9 + k]' with the kind
register holding 7 so that 7 + k = id (the compiler's idiom, e.g. 00394025 lea r8d, [rdx + 0x36] = 0x3D).
The .rdata id lists handed to the list helpers 003933F0 / 00393460 / 003934F0 are in request_lists.py
(../rc22-34-resource-readers-0930/), and the byte table at 01E09F68 is the kind-2 text-group map, so neither is
repeated here. nowload.mrp and title_fore3.mrp ship but have no entry in the kind-7 array at all.
Controls: C1 the same scan finds title.mrp (0x3A) at 00394044 (lea r8d, [rdx + 0x33]) and Loca.mrp (0xBF) at
004040FE; C2 it finds the lea-idiom request of title_logo.tm2 (0x3D) at 00394025.
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, owner, dis, secs, BASE  # noqa
from kind7 import paths  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


POOL = [0x00249180, 0x00249210, 0x002493D0, 0x00249350, 0x00249320]
PATH = [0x0032E400, 0x0032E620, 0x0032E3F0]
t = [s for s in secs if s[0] == ".text"][0]
name, va, vs, ro, rs = t
blob = d[ro:ro + rs]
sites = {}
for p in range(len(blob) - 6):
    b0 = blob[p]
    if b0 in (0xE8, 0xE9):
        tg = BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0]
        if tg in POOL or tg in PATH:
            sites[BASE + va + p] = tg
    elif b0 == 0x0F and 0x80 <= blob[p + 1] <= 0x8F:
        tg = BASE + va + p + 6 + struct.unpack_from("<i", blob, p + 2)[0]
        if tg in POOL or tg in PATH:
            sites[BASE + va + p] = tg
print("request-entry call sites (raw E8/E9/0F8x): %d" % len(sites))
cache = {}


def window(site):
    f = owner(site)
    if f is None:
        return None
    if f not in cache:
        cache[f] = dis(f)
    body = cache[f]
    idx = [i for i, x in enumerate(body) if x.address == site]
    return body[max(0, idx[0] - 14):idx[0]] if idx else None


def formed(win, reg, kind_regs):
    """values an id register can receive in the window: constants and 7-relative leas"""
    vals = []
    kind7 = False
    for x in win:
        op = x.op_str
        if re.fullmatch(r"(edx|ecx), 7", op) and x.mnemonic == "mov":
            kind7 = True
        m = re.fullmatch(r"%s, (0x[0-9a-f]+|\d+)" % reg, op)
        if m and x.mnemonic == "mov":
            vals.append((x.address, int(m.group(1), 0)))
        m = re.fullmatch(r"%s, \[(rdx|rcx|r9) \+ (0x[0-9a-f]+|\d+)\]" % reg, op)
        if m and x.mnemonic == "lea" and kind7:
            vals.append((x.address, 7 + int(m.group(2), 0)))
    return vals


found = {}
for s, tg in sorted(sites.items()):
    w = window(s)
    if not w:
        continue
    reg = "r8d" if tg in POOL else "edx"
    for a, v in formed(w, reg, None):
        found.setdefault(v, []).append((a, s, owner(s)))
arr, P = paths(7, 0x4D2, stop_on_miss=False)
for v, nm in ((0x3A, "title.mrp"), (0x3B, "title_menu.mrp"), (0x89, "E3_Logo.mrp"), (0xBF, "Loca.mrp"), (0x3D, "title_logo.tm2")):
    hits = found.get(v, [])
    print("   0x%03X %-15s (%s): %s" % (v, nm, P.get(v, "?").split(chr(92))[-1],
          " ".join("%08X->%08X in %08X" % h for h in hits) or "none"))
check("C1 title.mrp found at 00394044 and Loca.mrp at 004040FE",
      any(h[0] == 0x00394044 for h in found.get(0x3A, [])) and any(h[0] == 0x004040FE for h in found.get(0xBF, [])))
check("C2 title_logo.tm2 (0x3D) found through the lea idiom at 00394025", any(h[0] == 0x00394025 for h in found.get(0x3D, [])))
check("R1 no request site forms 0x3B (title_menu.mrp) or 0x89 (E3_Logo.mrp)", not found.get(0x3B) and not found.get(0x89))
names = [P.get(i, "") for i in range(0x4D2)]
check("R2 nowload.mrp and title_fore3.mrp have no kind-7 path (first arm)",
      not any(n.lower().endswith(("nowload.mrp", "title_fore3.mrp")) for n in names))
print("FAILS %d" % FAILS)
