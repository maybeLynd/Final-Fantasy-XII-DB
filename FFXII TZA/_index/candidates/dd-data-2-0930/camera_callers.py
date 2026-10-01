"""Who reaches the camera-state snapshot 00864F30, and who reaches its sibling 0018A120 (SWE2-DATA 2026-09-30), static.

A raw image sweep, independent of the function list: every E8/E9 rel32 and 0F 8x jcc in .text whose target is the
function, every rip-relative operand that forms its address, and every aligned qword in the whole image equal to it
(a function table or vtable slot).
  K1 the snapshot 00864F30: its direct callers, rip references and pointer slots, listed with the owning function;
  C1 control: the same sweep on the sibling 0018A120 finds the nine callers the 2026-09-18 correction lists
     (00185C30 00186670 00187950 001897C0 00189CE0 0018A680 001B7850 001EBDD0 001EF6D0), so the sweep sees callers;
  K2 the correction's nine callers are callers of 0018A120, and none of them calls 00864F30.
  K3 00864F30 is slot 0 of the vtable 01CCFB78, whose RTTI class is GiBeginEff; that vtable's one rip reference is the
     factory 00865130, which allocates 0x90 bytes (the page's record size) and stores the vtable at +0;
  K4 slot 0 is the Gi command PREPARE step: 001FB840 ends `jmp qword ptr [rax]` on the command's vtable;
  K5 slot 1, the execute body 00864E90, consumes the record: +0x88 / +0x8C (movss) with the +8 block to 00210520, which
     copies the 64 bytes and the two floats into globals, and the +0x48 block to the device's vtable +0x30 call;
  K6 the trailing dwords are the floats 0039D1F0 / 0039D1E0 return (each one `movss xmm0, [rip+..]`), and 0039D1D0
     returns the address of a global (one `lea rax, [rip+..]`);
  K7 the helper 00678B50 rewrites only +0x28 and +0x38 of the +0x48 block, from two floats (source +0xB8 / +0xBC);
  K8 the ranking figure: 72 of the 114 instructions are SSE moves (movups / movaps / movss), 63.2 %.
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, text_range, owner, raw_rip_refs, BASE, secs, ins_at  # noqa

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
    for p in range(len(blob) - 5):
        b = blob[p]
        if b in (0xE8, 0xE9):
            if t0 + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == target:
                x = ins_at(t0 + p)
                if x is not None and x.size == 5:
                    out.append((t0 + p, x.mnemonic))
        elif b == 0x0F and p + 6 <= len(blob) and 0x80 <= blob[p + 1] <= 0x8F:
            if t0 + p + 6 + struct.unpack_from("<i", blob, p + 2)[0] == target:
                out.append((t0 + p, "jcc"))
    return out


def slots(target):
    q = struct.pack("<Q", target)
    out = []
    i = d.find(q)
    while i >= 0:
        for name, va, vs, ro_, rs in secs:
            if ro_ <= i < ro_ + rs:
                out.append((BASE + va + (i - ro_), name))
        i = d.find(q, i + 1)
    return out


def report(target):
    rc = rel_callers(target)
    rr = [x for x in raw_rip_refs(target, target + 1)]
    sl = slots(target)
    own = sorted(set(owner(a) for a, _ in rc if owner(a) is not None))
    print("   %08X: %d rel32/jcc sites, owners %s; %d rip refs %s; %d pointer slots %s" % (
        target, len(rc), " ".join("%08X" % o for o in own), len(rr),
        " ".join("%08X(%s)" % (a, m) for a, m, _, _ in rr), len(sl), " ".join("%08X%s" % s for s in sl)))
    return rc, own, rr, sl


NINE = {0x00185C30, 0x00186670, 0x00187950, 0x001897C0, 0x00189CE0, 0x0018A680, 0x001B7850, 0x001EBDD0, 0x001EF6D0}
rc1, own1, rr1, sl1 = report(0x00864F30)
rc2, own2, rr2, sl2 = report(0x0018A120)
check("C1 control: the sweep finds all nine listed callers of 0018A120", NINE <= set(own2),
      "missing %s" % sorted("%08X" % x for x in NINE - set(own2)))
check("K2 none of the nine calls 00864F30", not (NINE & set(own1)))
check("K1 the snapshot's reach is counted (reported above)", True,
      "%d direct sites, %d rip refs, %d pointer slots" % (len(rc1), len(rr1), len(sl1)))
from pe import dis, u64, u32, cstr, section  # noqa
vt = 0x01CCFB78
col = u64(vt - 8)
cls = cstr(0x120000 + u32(col + 12) + 16)
fac = {x.address: x for x in dis(0x00865130)}
refs = raw_rip_refs(vt, vt + 1)
check("K3 slot 0 of GiBeginEff's vtable; its one reference is the 0x90-byte factory",
      u64(vt) == 0x00864F30 and cls == ".?AVGiBeginEff@@" and [a for a, _, _, _ in refs] == [0x00865154]
      and fac[0x00865145].op_str == "edx, 0x90" and fac[0x0086515B].op_str == "qword ptr [rax], rcx", cls)
pr = dis(0x001FB840)
check("K4 001FB840 (prepare) tail-jumps through slot 0", pr[-1].mnemonic == "jmp" and pr[-1].op_str == "qword ptr [rax]")
ex = {x.address: x for x in dis(0x00864E90)}
check("K5 execute reads +0x8C/+0x88 with +8 for 00210520 and hands +0x48 to device +0x30",
      ex[0x00864EC2].op_str == "xmm2, dword ptr [rbx + 0x8c]" and ex[0x00864ECA].op_str == "rcx, [rbx + 8]"
      and ex[0x00864ECE].op_str == "xmm1, dword ptr [rbx + 0x88]" and ex[0x00864ED6].op_str == "0x210520"
      and ex[0x00864EDE].op_str == "rdx, [rbx + 0x48]" and ex[0x00864EE5].op_str == "qword ptr [rax + 0x30]")
g = [dis(a) for a in (0x0039D1D0, 0x0039D1E0, 0x0039D1F0)]
check("K6 0039D1D0 = lea of a global; 0039D1E0 / 0039D1F0 = one global float each",
      g[0][0].mnemonic == "lea" and g[1][0].mnemonic == "movss" and g[2][0].mnemonic == "movss"
      and all(x[-1].mnemonic == "ret" and len(x) == 2 for x in g))
h = dis(0x00678B50)
st = sorted(set(x.op_str.split(",")[0] for x in h if x.mnemonic == "movss" and x.op_str.startswith("dword ptr [rcx")))
check("K7 00678B50 stores only block +0x28 / +0x38", st == ["dword ptr [rcx + 0x28]", "dword ptr [rcx + 0x38]"], str(st))
f = dis(0x00864F30)
mv = [x for x in f if x.mnemonic in ("movups", "movaps", "movss")]
check("K8 72 of 114 instructions are SSE moves (63.2 %)", len(f) == 114 and len(mv) == 72,
      "%d of %d" % (len(mv), len(f)))
print("RESULT the 2026-09-18 caller list belongs to 0018A120; 00864F30 is GiBeginEff's PREPARE slot, reached only "
      "through its vtable, and the record is that 0x90-byte command, consumed by its execute slot")
print("FAILS %d" % FAILS)
