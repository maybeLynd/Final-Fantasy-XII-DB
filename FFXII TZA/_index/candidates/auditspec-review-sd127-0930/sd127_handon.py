"""sd127_handon.py - SWE2-AUDIT-SPEC (SD-127 review, 2026-09-30). One level into every callee a near-key base is handed
to (from sd127_leas.out), with sdx.track_entry(): the accesses the callee makes through the handed register (resolved
address, width, indexed), whether any lands on a HUD key, and the callee's own hand-ons (printed, not followed).
Indirect calls ([r15 + 0x88], `rax`) are listed as not followed.
"""
import bisect, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd141-0930"))
import sdx  # noqa: E402

DB = os.path.join(HERE, "..", "..", "..")
page = open(os.path.join(DB, "16-UI", "Battle-Hud", "the-battle-hud-layout-readers.md"), encoding="utf-8").read()
cited = set(int(x, 16) for x in re.findall(r"`(00[0-9A-F]{6})`", page))
rows = list(csv.DictReader(open(os.path.join(DB, "16-UI", "Layout-Parameter-System", "members", "layout-key-readers.tsv"),
                                encoding="utf-8"), delimiter="\t"))
hud = {int(r["global"], 16): r["key"] for r in rows if int(r["reader"], 16) in cited}
HK = sorted(hud)

# (site of the call, callee, register, base) from sd127_leas.out's hand-on lines
H = [(0x0023DAA3, 0x002F9860, "r9", 0x01E0BF60), (0x0023DF23, 0x002F9860, "r9", 0x01E0BF60),
     (0x00254030, 0x0017E7D0, "rdx", 0x01E0C2CC), (0x00254BC7, 0x0017E7D0, "rcx", 0x01E0C2CC),
     (0x00274F39, 0x00202B70, "rdx", 0x0209AB90), (0x00274F93, 0x00202B70, "rdx", 0x0209AB90),
     (0x002764A5, 0x00203170, "rcx", 0x0209AB90),
     (0x00296302, 0x002732E0, "r8", 0x0209C2BE), (0x00296387, 0x003F8A30, "rdx", 0x0209C240),
     (0x0029639B, 0x003F8A30, "rdx", 0x0209C298), (0x002963E2, 0x003F89C0, "rcx", 0x0209C240),
     (0x00296402, 0x003F89C0, "rcx", 0x0209C298), (0x00296416, 0x003F8A50, "rdx", 0x0209C240),
     (0x0029642A, 0x003F8A50, "rdx", 0x0209C298), (0x0029CAFE, 0x0039BEC0, "r8", 0x0209C330),
     (0x0029CB3C, 0x0039BB60, "r8", 0x0209C330), (0x002A1C86, 0x002B3C30, "rdx", 0x0209CB90),
     (0x002A1CDF, 0x002D89E0, "r9", 0x0209CB90), (0x002A5440, 0x002B4090, "rdx", 0x0209C990),
     (0x002ADBC9, 0x002AE610, "rdx", 0x01E0CE08), (0x002B19A2, 0x002AE610, "rdx", 0x01E0CE04),
     (0x002B756A, 0x00285F00, "rcx", 0x0209E5D0), (0x002BA21A, 0x00285F00, "rcx", 0x0209E608),
     (0x00400389, 0x004006A0, "rcx", 0x01E0C590)]
NOT_FOLLOWED = [(0x00244EF5, "call rax", "rdx", 0x01E0C0F8), (0x00246C09, "call rax", "rdx", 0x01E0C0E0),
                (0x00267A79, "call [r15+0x88]", "rdx", 0x01E0C32E), (0x0029626F, "jmp 00861EC0 (thunk)", "rcx", 0x0209C240),
                (0x002A1C0E, "call 00861EBA (thunk)", "rcx", 0x0209CB90)]


def keys_in(a, w):
    return [k for k in HK if a <= k < a + max(w, 1)]


hits = 0
for site, f, reg, base in H:
    k = HK[bisect.bisect_left(HK, base)]
    t, acc, calls, st = sdx.track_entry(f, reg, base)
    kh = [(a, txt, ad, w) for a, txt, ad, w, ix, lea in acc if not lea and keys_in(ad, w)]
    ix = [(a, txt, ad, w) for a, txt, ad, w, x, lea in acc if x]
    mx = max([ad + max(w, 1) - base for a, txt, ad, w, x, lea in acc if not lea] or [0])
    print("%08X -> %08X %s=%08X (next HUD key %08X at +0x%X): accesses %d, max extent +0x%X, indexed %d, hand-ons %d, "
          "stores %d%s" % (site, f, reg, base, k, k - base, len(acc), mx, len(ix), len(calls), len(st), "  KEY-HIT" if kh else ""))
    for a, txt, ad, w in ix:
        print("     indexed %08X %s (base %08X w%d)" % (a, txt, ad, w))
    for c in calls:
        print("     hand-on %08X %s %s" % c)
    for a, txt, ad, w in kh:
        print("     KEY %08X %s -> %08X %s" % (a, txt, ad, [hud[x] for x in keys_in(ad, w)]))
    hits += len(kh)
for x in NOT_FOLLOWED:
    k = HK[bisect.bisect_left(HK, x[3])]
    print("not followed: %08X %s %s=%08X (next HUD key +0x%X)" % (x[0], x[1], x[2], x[3], k - x[3]))
# second level: the callees' own hand-ons printed above
H2 = [(0x00217060, "rdx", 0x0209AB90), (0x00364980, "rcx", 0x0209CB90), (0x00364980, "r9", 0x0209CB90),
      (0x003659F0, "r8", 0x0209CB90), (0x002B3400, "rdx", 0x0209CB90), (0x002B49F0, "rdx", 0x0209C990),
      (0x003FFC60, "rcx", 0x01E0CE08), (0x003FFC60, "rcx", 0x01E0CE04), (0x0035BB20, "r8", 0x0209C2BE),
      (0x0020E600, "r9", 0x01E0BF60), (0x002B24B0, "r8", 0x0209CB90), (0x002B2150, "rdx", 0x0209CB90),
      (0x00377780, "rcx", 0x01E0C590), (0x002AC1E0, "rdx", 0x0209CB90), (0x002B1FB0, "rdx", 0x0209C990)]
for f, reg, base in H2:
    k = HK[bisect.bisect_left(HK, base)]
    t, acc, calls, st = sdx.track_entry(f, reg, base)
    kh = [(a, txt, ad, w) for a, txt, ad, w, ix, lea in acc if not lea and keys_in(ad, w)]
    ix = [(a, txt, ad, w) for a, txt, ad, w, x, lea in acc if x]
    mx = max([ad + max(w, 1) - base for a, txt, ad, w, x, lea in acc if not lea] or [0])
    print("level 2: %08X %s=%08X (next HUD key +0x%X): accesses %d, max extent +0x%X, indexed %d, hand-ons %s%s" % (
        f, reg, base, k - base, len(acc), mx, len(ix), ["%08X %s" % (c[0], c[1]) for c in calls], "  KEY-HIT" if kh else ""))
    for a, txt, ad, w in ix:
        print("     indexed %08X %s (base %08X w%d)" % (a, txt, ad, w))
    hits += len(kh)
print("key hits in followed callees (levels 1-2): %d" % hits)
