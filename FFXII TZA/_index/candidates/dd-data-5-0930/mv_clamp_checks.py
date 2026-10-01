"""Clamping a point into a volume: callers, the closest-approach body and its second result (SWE2-DATA 2026-09-30), static.

A raw image sweep (E8/E9 rel32 and 0F 8x jcc in .text, independent of the function list) finds every caller of the
three entries. Then:
  A1 00363FD0's arguments: rcx -> 022D92B0 (point A), rdx -> 022D92C0 (point B), r8 -> 022D92A0 (direction);
  A2 its parameter is t = C0 - dot(B - A, dir) * (C1 / |dir|^2), clamped to [C0, C1] with C0 = [01EF93F0], C1 =
     [01EF93FC]; when |dir|^2 <= 0 it returns C0 (0036410D); the constants' values are printed;
  A3 the second result: |(B - A) + t * dir|^2 is stored to 022D92D4 (003641DC) and 022D92E4 (003641D4); t returns in xmm0;
  A4 for every caller, the instructions after the call up to the function end that load 022D92D4 or 022D92E4 are listed
     (a consumer of the second result); every caller is also listed with its owner and owner size, so the Audio-filed
     callers the pass-22 block describes by size are anchored here;
  A5 image-wide, every rip-relative load of 022D92D4 / 022D92E4, with its owner (who else reads the scratch cell);
  A6 the outcode history 022D9130: its rip readers and writers, with owners (the 0025C830 reader of 2026-09-18);
Controls: C1 the sweep finds 00363FD0's own stores to 022D92D4 (so a missing reader is not a blind sweep); C2 the
caller sweep finds 0025C830 calling 0025A8E0 (the published history reader's two calls).
"""
import os, struct, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, dis, text_range, owner, raw_rip_refs, ins_at, funcs, off  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]


def rel_callers(target):
    out = []
    for p in range(len(blob) - 6):
        b = blob[p]
        if b in (0xE8, 0xE9) and t0 + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == target:
            x = ins_at(t0 + p)
            if x is not None and x.size == 5:
                out.append(t0 + p)
        elif b == 0x0F and 0x80 <= blob[p + 1] <= 0x8F and t0 + p + 6 + struct.unpack_from("<i", blob, p + 2)[0] == target:
            out.append(t0 + p)
    return out


def rt(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


body = {x.address: x for x in dis(0x00363FD0)}
check("A1 arguments copied to the workbench: rcx -> 022D92B0, rdx -> 022D92C0, r8 -> 022D92A0",
      rt(body[0x00363FE7]) == 0x022D92B0 and body[0x00363FE4].op_str == "xmm3, xmmword ptr [rcx]"
      and rt(body[0x00363FF4]) == 0x022D92C0 and body[0x00363FEE].op_str == "xmm0, xmmword ptr [rdx]"
      and rt(body[0x00363FDD]) == 0x022D92A0 and body[0x00363FD4].op_str == "xmm0, xmmword ptr [r8]")
c0 = struct.unpack_from("<f", d, off(0x01EF93F0))[0]
c1 = struct.unpack_from("<f", d, off(0x01EF93FC))[0]
print("   constants: C0 [01EF93F0] = %r, C1 [01EF93FC] = %r" % (c0, c1))
check("A2 t = C0 - dot * (C1 / |dir|^2), clamped by maxss C0 / minss C1; degenerate |dir|^2 <= 0 returns C0",
      rt(body[0x003640BA]) == 0x01EF93FC and body[0x003640C6].op_str == "xmm0, xmm4"
      and rt(body[0x003640DA]) == 0x01EF93F0 and rt(body[0x003640FB]) == 0x01EF93F0 and body[0x003640FB].mnemonic == "maxss"
      and rt(body[0x00364103]) == 0x01EF93FC and body[0x00364103].mnemonic == "minss"
      and body[0x003640B8].mnemonic == "jbe" and rt(body[0x0036410D]) == 0x01EF93F0,
      "C0=%g C1=%g" % (c0, c1))
check("A3 the squared distance |(B-A) + t*dir|^2 goes to 022D92D4 and 022D92E4; t returns in xmm0",
      rt(body[0x003641DC]) == 0x022D92D4 and rt(body[0x003641D4]) == 0x022D92E4
      and body[0x00364172].op_str == "xmm0, xmm6")

cells = (0x022D92D4, 0x022D92E4)
print("   callers of the three entries (call site, owner, owner size):")
callers = {}
for tgt in (0x00361DE0, 0x003623C0, 0x00363FD0):
    cs = rel_callers(tgt)
    callers[tgt] = cs
    for c in cs:
        o = owner(c)
        print("     %08X -> %08X  in %s (%s B)" % (c, tgt, "%08X" % o if o else "unlisted", funcs.get(o, "?")))
readers_after = []
for c in callers[0x00363FD0]:
    o = owner(c)
    if o is None:
        continue
    for x in dis(o):
        if x.address > c and rt(x) in cells and not x.op_str.startswith("dword ptr [rip"):
            readers_after.append((c, x.address, x.mnemonic, x.op_str))
print("   A4 loads of 022D92D4 / 022D92E4 after a call to 00363FD0 in the calling function: %d" % len(readers_after))
for r in readers_after:
    print("     call %08X -> %08X %s %s" % r)
check("A4 every caller of 00363FD0 is listed (the census is non-empty)", len(callers[0x00363FD0]) > 0)

refs = raw_rip_refs(0x022D92D4, 0x022D92D8) + raw_rip_refs(0x022D92E4, 0x022D92E8)
loads = [r for r in refs if not r[2].startswith("dword ptr [rip")]
stores = [r for r in refs if r[2].startswith("dword ptr [rip")]
lo = {}
for a, mn, ops, tg in loads:
    lo.setdefault(owner(a), []).append("%08X %s" % (a, mn))
print("   A5 image-wide: %d stores, %d loads of the two cells; loading functions:" % (len(stores), len(loads)))
for o, l in sorted(lo.items(), key=lambda k: k[0] or 0):
    print("     %s (%s B): %s" % ("%08X" % o if o else "unlisted", funcs.get(o, "?"), ", ".join(l[:4])))
check("C1 control: the sweep sees 00363FD0's own store to 022D92D4 (003641DC)",
      any(a == 0x003641DC for a, *_ in stores))

h = raw_rip_refs(0x022D9130, 0x022D9134)
ho = {}
for a, mn, ops, tg in h:
    ho.setdefault(owner(a), []).append("%08X %s" % (a, "store" if ops.startswith("dword ptr [rip") else "load"))
print("   A6 the outcode history 022D9130:")
for o, l in sorted(ho.items(), key=lambda k: k[0] or 0):
    print("     %s (%s B): %s" % ("%08X" % o if o else "unlisted", funcs.get(o, "?"), ", ".join(l[:6])))
check("A6 0025C830 reads the history (0025CEFA)", any(a == 0x0025CEFA for a, *_ in h))
c2 = [c for c in rel_callers(0x0025A8E0) if owner(c) == 0x0025C830]
check("C2 control: the caller sweep finds 0025C830's calls to 0025A8E0, the last two (0025CEE2, 0025CEF5) just "
      "before the history read", {0x0025CEE2, 0x0025CEF5} <= set(c2), str(["%08X" % c for c in c2]))

p = {x.address: x for x in dis(0x00362230)}
check("A7 00362230 walks [r8+0x14] segments of 0x20 bytes from r8+0x40 (start +0, direction +0x10), calls 00363FD0 "
      "for each, and keeps the segment whose squared distance 022D92D4 is smallest; it writes start + t*dir (w = 1.0) "
      "to rdx and returns the record's float +0x30",
      p[0x0036223D].op_str == "eax, dword ptr [r8 + 0x14]" and p[0x00362241].op_str == "rbx, [r8 + 0x40]"
      and p[0x00362280].op_str == "r8, [rbx + 0x10]" and p[0x0036228A].op_str == "0x363fd0"
      and rt(p[0x00362292]) == 0x022D92D4 and p[0x0036229F].op_str == "xmm6, xmm0"
      and p[0x003622AA].op_str == "xmm6, xmm0" and p[0x003622B0].op_str == "rbx, 0x20"
      and p[0x0036238A].op_str == "xmmword ptr [r14], xmm2" and p[0x00362254].op_str == "xmm7, dword ptr [r8 + 0x30]"
      and p[0x0036239E].op_str == "xmm0, xmm7")
q = {x.address: x for x in dis(0x003631B0)}
check("A8 003631B0 selects the shape from the record's byte +9 (& 0x7F): 0 ellipse 00361DE0, 1 box 003623C0, "
      "2 segment chain 00362230, other: the point unchanged",
      q[0x0036326A].op_str == "ecx, byte ptr [rbx + 9]" and q[0x0036326E].op_str == "ecx, 0x7f"
      and q[0x003632CC].op_str == "0x361de0" and q[0x003632BA].op_str == "0x3623c0" and q[0x0036329E].op_str == "0x362230"
      and q[0x0036327D].op_str == "xmm0, xmmword ptr [rsi]")
print("   the records are offsets added to the base at %08X (00363263)" % rt(q[0x00363263]))
print("   callers of 003631B0: %s" % ", ".join("%08X in %08X" % (c, owner(c)) for c in rel_callers(0x003631B0)))
print("FAILS %d" % FAILS)
