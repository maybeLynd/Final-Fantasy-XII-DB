"""d0_selector_census.py (_index/candidates/gi-0929-effects/) - authored values of element type 0xD0's blend-block
fields, over every EFX stream in the full extract (GI-9, FABLE 2026-09-29). Runs from any cwd; exit status 1 if any
check fails.

Definition = 0xA00 chunk + 0x10: 003A9A70 receives chunk + 0xC and stores the type at +4+0x44, so the definition is
chunk + 0x10. The birth 00464F20 copies definition +0x140 -> element +0x230 (target mode, bounded 0..9 at 00465867)
and definition +0x142 bit 4 -> element +0x232 bit 4 (the blend block); 00465CD0 reads the blend selector from
definition +0x143 & 7 (00465E41).
Inputs: D:/FFXII_TZA_extract; the embedded-stream list efx-embedded-stream-files.txt in Effect-File-Formats/members
(override the folder with GI_EFFECTS_MEMBERS).
Checks:
  P1 positive control: every 0xD0 target mode (definition +0x140) lies in 0..9
  P2 positive control: every type-0x40 light kind (definition +0x120, 004640C3 switch) lies in {0, 1, 2}
  R1 regression: 1,437 0xD0 definitions; the blend block is on in 45, and every one of those carries selector 0 (37)
     or 1 (8) - selectors 2-7 never reach the consumers
"""
import os, struct, collections, sys
ROOT = "D:/FFXII_TZA_extract"
MEMBERS = os.environ.get("GI_EFFECTS_MEMBERS",
                         r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\17-Presentation-Rendering\Effect-File-Formats\members")
EMB = os.path.join(MEMBERS, "efx-embedded-stream-files.txt")


def streams(b):
    for m in (b"EFX0010", b"EFX0009", b"EFX0008"):
        i = b.find(m)
        while i >= 0:
            sz = struct.unpack_from("<I", b, i + 0xC)[0]
            end = i + sz if 0x10 <= sz and i + sz <= len(b) else len(b)
            cur = i + 0x10
            while cur + 8 <= end:
                ln, fl, ty = struct.unpack_from("<IHH", b, cur)
                if ln < 8 or cur + ln > end or fl != 0x100:
                    break
                yield ty, cur, ln
                cur += ln
            i = b.find(m, max(cur, i + 1))


paths = []
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
    paths += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
paths += [os.path.join(ROOT, l.strip()) for l in open(EMB) if l.strip()]
mode = collections.Counter(); flags4 = collections.Counter(); sel_all = collections.Counter(); sel_on = collections.Counter()
lightkind = collections.Counter(); short = 0; files_on = collections.defaultdict(set)
for p in paths:
    b = open(p, "rb").read()
    for ty, o, ln in streams(b):
        if ty != 0xA00:
            continue
        t = b[o + 0xE]
        if t == 0x40 and ln > 0x131:
            lightkind[b[o + 0x130]] += 1
        if t != 0xD0:
            continue
        if ln <= 0x153:
            short += 1; continue
        m, f, s = b[o + 0x150], b[o + 0x152], b[o + 0x153]
        mode[m] += 1; sel_all[s & 7] += 1
        if f & 0x10:
            flags4["on"] += 1; sel_on[s & 7] += 1; files_on[s & 7].add(os.path.relpath(p, ROOT).replace("\\", "/"))
        else:
            flags4["off"] += 1
fails = []
p1 = bool(mode) and max(mode) <= 9
print("P1 0xD0 target mode values:", sorted(mode.items()), "PASS" if p1 else "FAIL")
p2 = bool(lightkind) and set(lightkind) <= {0, 1, 2}
print("P2 0x40 light kind values:", sorted(lightkind.items()), "PASS" if p2 else "FAIL")
print("0xD0 definitions:", sum(mode.values()), "too short:", short)
print("blend block (def +0x142 bit 4):", dict(flags4))
print("selector (def +0x143 & 7), all 0xD0:", sorted(sel_all.items()))
print("selector where the blend block is on:", sorted(sel_on.items()))
for s, fs in sorted(files_on.items()):
    print("  sel %d: %d files, e.g. %s" % (s, len(fs), sorted(fs)[:6]))
r1 = sum(mode.values()) == 1437 and flags4["on"] == 45 and dict(sel_on) == {0: 37, 1: 8}
print("R1 blend block on in 45 of 1,437, selectors only 0 (37) and 1 (8):", "PASS" if r1 else "FAIL")
for name, ok in (("P1", p1), ("P2", p2), ("R1", r1)):
    if not ok:
        fails.append(name)
print("FAILS %d" % len(fails))
sys.exit(1 if fails else 0)
