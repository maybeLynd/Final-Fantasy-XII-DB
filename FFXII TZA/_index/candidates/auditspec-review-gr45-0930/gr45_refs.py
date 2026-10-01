"""gr45_refs.py - SWE2-AUDIT-SPEC independent reference census for the GR-4/GR-5 review (2026-09-30).

R1  every instruction in executable sections that references the table registry 02EBF038..02EBF13F (the 33 table slots
    pack.py names; action_data is 02EBF138) in the rip-relative form AND the image-base-relative form (disp32 =
    VA - 0x120000 on a non-rip base), found by raw disp32 arithmetic and confirmed by decoding at every candidate start.
    Reported per slot; the action slot's references are listed by kind (load / lea / store / indexed).
R2  every stored 64-bit value in any section equal to an address in the registry (a slot pointer table would let code
    reach the action header without naming 02EBF138).
R3  raw callers (E8/E9 and 0F 8x rel32) and stored pointers (abs64 values, any section) of the resolver 0020E600, the
    four "row-returning" functions the package names, and 0030A190.
"""
import struct, sys, collections
import img45 as I
from capstone.x86 import X86_REG_RIP

LO, HI = 0x02EBF038, 0x02EBF140
IBR = 0x120000


def decode_refs(lo, hi):
    hits = []
    for n, v, vs, p, rs in I.text_secs()[:1]:
        blob = I.raw[p:p + min(vs, rs)]
        cands = set(I.disp_candidates(lo, hi).items())
        seen = set()
        for k, kind in sorted(cands):
            for back in range(11, 0, -1):     # earliest start whose displacement field is exactly at k
                s = k - back
                if s < 0:
                    continue
                va = v + s
                try:
                    ins = next(I.md.disasm(blob[s:s + 16], va, 1))
                except StopIteration:
                    continue
                if ins.disp_size != 4 or ins.disp_offset != back:
                    continue
                for op in ins.operands:
                    if op.type != 3:
                        continue
                    if op.mem.base == X86_REG_RIP:
                        tgt = ins.address + ins.size + op.mem.disp
                        form = "rip"
                    elif op.mem.base != 0 or op.mem.index != 0:
                        tgt = op.mem.disp + IBR
                        form = "ib:" + (ins.reg_name(op.mem.base) if op.mem.base else "-") + \
                               ("+" + ins.reg_name(op.mem.index) + "*%d" % op.mem.scale if op.mem.index else "")
                    else:
                        tgt = op.mem.disp
                        form = "abs32"
                    if lo <= tgt < hi and (ins.address, tgt) not in seen:
                        seen.add((ins.address, tgt))
                        hits.append((ins.address, tgt, form, op.size, "%s %s" % (ins.mnemonic, ins.op_str)))
                break
    return hits


def stored_values(lo, hi):
    out = []
    for n, v, vs, p, rs, x in I.SECS:
        blob = I.raw[p:p + min(vs, rs)]
        for val in range(lo, hi):
            pat = struct.pack("<Q", val)
            k = blob.find(pat)
            while k >= 0:
                out.append((n, v + k, val))
                k = blob.find(pat, k + 1)
    return out


def main():
    hits = decode_refs(LO, HI)
    # genuine-instruction filter: the instruction must lie on a decode path; print all, the rip ones are exact
    per = collections.Counter()
    act = []
    for a, t, form, w, txt in hits:
        slot = t & ~7
        per[(slot, form.split(":")[0])] += 1
        if LO <= t < HI and slot == 0x02EBF138:
            act.append((a, t, form, w, txt))
    print("R1 registry references by slot and form (rip / ib = image-base-relative):")
    for (slot, form), c in sorted(per.items()):
        print("   %08X %-3s %d" % (slot, form, c))
    kinds = collections.Counter()
    nonload = []
    for a, t, form, w, txt in act:
        m = txt.split()[0]
        k = "load8" if (m == "mov" and txt.split(",")[0].split()[1].startswith("r") and w == 8 and "ptr [" in txt.split(",", 1)[1] and t == 0x02EBF138) else m
        kinds[(k, form)] += 1
        if k != "load8":
            nonload.append((a, t, form, w, txt))
    print("R1 action slot 02EBF138..3F: %d references; kinds %s" % (len(act), dict(kinds)))
    for x in nonload:
        print("   non-load %08X -> %08X %s w%d %s" % x)
    ib = [x for x in hits if x[2].startswith("ib")]
    print("R1 image-base-relative references into the registry: %d" % len(ib))
    for x in ib[:40]:
        print("   %08X -> %08X %s w%d %s" % x)
    idx = [x for x in hits if "*" in x[2] or ("rip" == x[2] and "*" in x[4])]
    print("R1 indexed forms into the registry: %d" % len(idx))
    for x in idx[:40]:
        print("   %08X -> %08X %s w%d %s" % x)
    lea = [x for x in hits if x[4].startswith("lea")]
    print("R1 lea (address-taken) of any registry slot: %d" % len(lea))
    for x in lea:
        print("   %08X -> %08X %s %s" % (x[0], x[1], x[2], x[4]))
    sv = stored_values(LO, HI)
    print("R2 stored 64-bit values equal to a registry address: %d %s" % (len(sv), ["%s %08X=%08X" % s for s in sv[:20]]))
    rel = I.relocs()
    for name, t in (("resolver", 0x0020E600), ("rowret", 0x00388FE0), ("rowret", 0x0038A9D0), ("rowret", 0x0038AA90),
                    ("rowret", 0x0038F970), ("GetPresentationParameter", 0x0030A190)):
        rs = I.raw_rel32_sites(t)
        cnt = collections.Counter(k for _, k in rs)
        st = stored_values(t, t + 1)
        print("R3 %-24s %08X raw rel32 sites %d %s; stored pointers %s" % (
            name, t, len(rs), dict(cnt) if len(rs) > 12 else ["%08X %s" % s for s in rs],
            ["%s %08X reloc=%s" % (s[0], s[1], s[1] in rel) for s in st]))


if __name__ == "__main__":
    main()
