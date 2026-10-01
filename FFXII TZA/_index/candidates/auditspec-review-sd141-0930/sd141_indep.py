"""sd141_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-141 (the flying-fade pair 02CB8410 / 02CB8414).
Uses sdx.py only (pefile + capstone + numpy over the certified image; not retool.py / the `pe` module).

  A  every .text operand starting in [02CB8410 - 0x40, 02CB8418) in rip / image-base-relative (any base, index-only,
     base+index) / absolute-disp32 form, with width and coverage of the pair.
  B  every rip lea whose target lies in [02CB8410 - 0x800, 02CB8418) (a base that could be handed on), with the
     .pdata root of the site.
  C  stored pointers: DIR64/HIGHLOW relocations and raw abs64/abs32/rva32 values into [02CB8410 - 0x800, 02CB8418).
  D  raw E8/E9/jcc callers of 001C7940 (the writer) - who stores the pair.
  Controls (each sensitive to a named defect of the instrument):
   K1 exact rip: the writer's two stores and 02CB8404's reader in 001FA820 must appear in A.
   K2 wide coverage: a real xmmword rip access is re-found by a window that starts 8 bytes INSIDE it, flagged COVERS.
   K3 image-base-relative: SD-121's `[r9 + rcx*4 + 0x21b97b0]` in 0036E3B0 must be found.
   K4 index-only / scale-1 base+index image-base-relative forms exist in the image (so the scan must decode them):
      the first such hits in 01E0C000..01E10000 are printed and must be non-empty.
   K5 relocation: the self pointers of 01F2E330 (SD-62 review) must be listed as DIR64 sites.
"""
import sdx

P = (0x02CB8410, 0x02CB8418)
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


print("== A. operands starting in [%08X, %08X)" % (P[0] - 0x40, P[1]))
A = sdx.window(P[0], P[1], 0x40)
for h in A:
    print("  " + sdx.fmt(h), " root", "%08X" % (sdx.root(h["addr"]) or 0))
cov = [h for h in A if h["covers"]]
print("  covering the pair: %d -> %s" % (len(cov), ["%08X %s" % (h["addr"], h["mn"]) for h in cov]))
print("  widest operand in the window: %d bytes; indexed hits: %d; image-base-relative hits: %d; abs32 hits: %d" % (
    max(h["width"] for h in A), sum(h["indexed"] for h in A), sum(h["form"] == "ibrel" for h in A),
    sum(h["form"] == "abs32" for h in A)))

print("== B. rip leas with target in [%08X, %08X)" % (P[0] - 0x800, P[1]))
B = sdx.rip_leas(P[0] - 0x800, P[1])
for s, r, t in sorted(B):
    print("  %08X lea %s -> %08X (pair - 0x%X)  root %08X" % (s, r, t, P[0] - t, sdx.root(s) or 0))
print("  %d leas" % len(B))

print("== C. stored pointers into [%08X, %08X)" % (P[0] - 0x800, P[1]))
C1 = sdx.relocs_into(P[0] - 0x800, P[1])
print("  relocations: %d %s" % (len(C1), ["%08X->%08X" % x for x in C1]))
C2 = sdx.data_refs(P[0] - 0x800, P[1])
C2d = [r for r in C2 if r[3] != ".text"]
print("  raw values outside .text (abs64/abs32/rva32): %d" % len(C2d))
for r in C2d[:40]:
    print("    %s at %08X = %08X (%s)" % r)

print("== D. callers of the writer 001C7940")
D = sdx.rel32(0x001C7940) + sdx.jcc(0x001C7940)
print("  %s" % ["%08X %s" % x for x in D])
print("  relocated slots holding 001C7940: %s" % ["%08X" % s for s, t in sdx.relocs_into(0x001C7940, 0x001C7941)])

print("== controls")
k1 = {h["addr"] for h in A}
check("K1", {0x001C9040, 0x001C8FFF, 0x001FA8D8} <= k1 and sdx.root(0x001FA8D8) == 0x001FA820,
      "exact rip: writer stores 001C9040 / 001C8FFF and 02CB8404's reader 001FA8D8 (root 001FA820) found")
# K2: first xmmword rip operand in .data, window starting 8 bytes inside it
x = None
for h in sdx.window(0x02CB0000, 0x02CB4000, 0):
    if h["width"] == 16 and h["form"] == "rip" and not h["lea"]:
        x = h
        break
k2 = sdx.window(x["start"] + 8, x["start"] + 12, 0x40) if x else []
check("K2", x is not None and any(h["addr"] == x["addr"] and h["covers"] for h in k2),
      "wide coverage: %s re-found from start+8 and flagged COVERS" % (sdx.fmt(x) if x else None))
k3 = sdx.window(0x022D97B0, 0x022D97B4, 0)
check("K3", any(h["addr"] == 0x0036E414 and h["form"] == "ibrel" for h in k3),
      "image-base-relative: 0036E414 `%s`" % sdx.txt(0x0036E414))
k4 = [h for h in sdx.window(0x01E0C000, 0x01E10000, 0) if h["form"] == "ibrel" and (
    h["base"] is None or (h["index"] and ("*" not in h["op"])))]
for h in k4[:6]:
    print("   K4 sample: " + sdx.fmt(h))
check("K4", len(k4) > 0, "index-only / scale-1 base+index image-base-relative forms occur (%d in 01E0C000..01E10000) "
      "and are decoded" % len(k4))
k5 = sdx.relocs_into(0x01F2E330, 0x01F2E370)
check("K5", len(k5) >= 6, "relocation control: %d DIR64 sites point into 01F2E330..01F2E36F" % len(k5))

print("== verdict inputs")
check("V1", [h["addr"] for h in cov] == [0x001C8FFF, 0x001C9040] and all(h["mn"] == "movss" and "], xmm0" in h["op"] for h in cov),
      "the only operands covering 02CB8410..02CB8417 in any form are the writer's two movss stores")
check("V2", not C1, "no relocated pointer targets 02CB7C10..02CB8417")
print("FAILS %d" % fails)
