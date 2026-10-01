"""gen_gif_tags.py - the GIF tag of every VIF1 packet template, decoded from authored bytes.

A microprogram's register list is authored data in its template, not code: the program stamps
NLOOP and copies PRIM / FLG / NREG / REGS from a VU cell the template's UNPACK uploaded
(the-bone-trails.md 5d, 5e). So the tags are readable statically, for the whole population.

Method: replay each template builder's immediate stores into a byte image, find its UNPACK
command words, and decode every 16-byte payload quadword as a candidate PS2 GIF tag, keeping
only quadwords whose every field is sane AND whose register list names real registers.

CONTROLS, both asserted before anything is written:
  POSITIVE  005409C0 (the bone trail) must yield cell 0 as PRIM TRIANGLE_STRIP, NREG 6,
            REGS ST/RGBAQ/XYZF2/ST/RGBAQ/XYZF2 - the decode published by hand at b81b07163.
  NEGATIVE  the same predicate over 150 ordinary functions, printed as a base rate. The
            predicate is NOT perfectly specific; the population rate has to beat that rate,
            and both numbers are reported rather than one tuned until the other passes.

Writes vif1-gif-tags.tsv beside itself. FABLE, 2026-09-20.
"""
import sys, os, io, collections, random

SCRATCH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch"
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRATCH)
sys.argv = ["gen_gif_tags", "301AD0"]
exec(open("disw.py").read().split("fn = int")[0])
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG

md.detail = True

REGNAME = {0: "PRIM", 1: "RGBAQ", 2: "ST", 3: "UV", 4: "XYZF2", 5: "XYZ2", 6: "TEX0_1", 7: "TEX0_2",
           8: "CLAMP_1", 9: "CLAMP_2", 10: "FOG", 12: "XYZF3", 13: "XYZ3", 14: "A+D", 15: "NOP"}
PRIMTYPE = {0: "POINT", 1: "LINE", 2: "LINE_STRIP", 3: "TRIANGLE", 4: "TRIANGLE_STRIP",
            5: "TRIANGLE_FAN", 6: "SPRITE"}


def build_image(fn):
    o = off(fn)
    if o is None or fn not in funcs:
        return {}
    img, base = {}, None
    for i in md.disasm(d[o:o + funcs[fn]], fn):
        ops = i.operands
        if i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_REG and md.reg_name(ops[1].reg) == "rcx" and base is None:
            base = md.reg_name(ops[0].reg)
        if i.mnemonic != "mov" or len(ops) != 2:
            continue
        if ops[0].type != X86_OP_MEM or ops[1].type != X86_OP_IMM or ops[0].mem.index != 0:
            continue
        if ops[0].mem.base == 0:
            continue
        if md.reg_name(ops[0].mem.base) not in (base, "rcx"):
            continue
        w = 8 if i.op_str.startswith("qword") else 4 if i.op_str.startswith("dword") \
            else 2 if i.op_str.startswith("word") else 1
        img[ops[0].mem.disp] = (ops[1].imm, w)
    return img


def flatten(img, size):
    buf = bytearray(size)
    for o_, (v, w) in img.items():
        if o_ < 0 or o_ + w > size:
            continue
        buf[o_:o_ + w] = int(v & ((1 << (8 * w)) - 1)).to_bytes(w, "little")
    return bytes(buf)


def decode_tag(lo, hi):
    nloop = lo & 0x7FFF
    eop = (lo >> 15) & 1
    if (lo >> 16) & 0x3FFFFFFF:
        return None
    pre = (lo >> 46) & 1
    prim = (lo >> 47) & 0x7FF
    flg = (lo >> 58) & 3
    nreg = (lo >> 60) & 0xF
    n = 16 if nreg == 0 else nreg
    if flg != 0 or (prim & 7) > 6:
        return None
    regs = [(hi >> (4 * k)) & 0xF for k in range(n)]
    if any(r == 11 for r in regs):
        return None
    # Zero-filled float payload decodes as a long run of descriptor 0; that was every one of the
    # twelve false positives the first run produced, so a tag must name real registers.
    if n > 8 or any(r == 0 for r in regs):
        return None
    if not pre and nloop == 0:
        return None
    return dict(nloop=nloop, eop=eop, pre=pre, prim=prim, nreg=n, regs=regs)


def tags_of(builder, size=None):
    img = build_image(builder)
    if not img:
        return []
    # The image is the builder's own store extent, not a fixed window. A fixed 0x600 window was the
    # first version of this and it silently truncated the largest templates - one register-write tag
    # was lost to it. Nothing here should depend on a magic size.
    if size is None:
        size = max(o_ + w for o_, (v, w) in img.items()) + 16
    buf = flatten(img, size)
    out = []
    for o_, (v, w) in sorted(img.items()):
        if w != 4 or not (0x60 <= ((v >> 24) & 0xFF) <= 0x7F):
            continue
        num = (v >> 16) & 0xFF
        for k in range(max(1, num)):
            q = o_ + 4 + 16 * k
            if q + 16 > size:
                break
            t = decode_tag(int.from_bytes(buf[q:q + 8], "little"),
                           int.from_bytes(buf[q + 8:q + 16], "little"))
            if t:
                t["cell"], t["unpack"] = k, o_
                if t["regs"] == [14]:
                    t["ad"] = ad_payload(buf, q, t["nloop"])
                out.append(t)
    return out


GSREG = {0x00: "PRIM", 0x01: "RGBAQ", 0x02: "ST", 0x03: "UV", 0x04: "XYZF2", 0x05: "XYZ2",
         0x06: "TEX0_1", 0x07: "TEX0_2", 0x08: "CLAMP_1", 0x09: "CLAMP_2", 0x0A: "FOG",
         0x0C: "XYZF3", 0x0D: "XYZ3", 0x14: "TEX1_1", 0x15: "TEX1_2", 0x16: "TEX2_1",
         0x17: "TEX2_2", 0x18: "XYOFFSET_1", 0x19: "XYOFFSET_2", 0x1A: "PRMODECONT",
         0x1B: "PRMODE", 0x1C: "TEXCLUT", 0x22: "SCANMSK", 0x34: "MIPTBP1_1", 0x35: "MIPTBP1_2",
         0x36: "MIPTBP2_1", 0x37: "MIPTBP2_2", 0x3B: "TEXA", 0x3D: "FOGCOL", 0x3F: "TEXFLUSH",
         0x40: "SCISSOR_1", 0x41: "SCISSOR_2", 0x42: "ALPHA_1", 0x43: "ALPHA_2", 0x44: "DIMX",
         0x45: "DTHE", 0x46: "COLCLAMP", 0x47: "TEST_1", 0x48: "TEST_2", 0x49: "PABE",
         0x4A: "FBA_1", 0x4B: "FBA_2", 0x4C: "FRAME_1", 0x4D: "FRAME_2", 0x4E: "ZBUF_1",
         0x4F: "ZBUF_2", 0x50: "BITBLTBUF", 0x51: "TRXPOS", 0x52: "TRXREG", 0x53: "TRXDIR",
         0x54: "HWREG", 0x60: "SIGNAL", 0x61: "FINISH", 0x62: "LABEL"}


def ad_payload(buf, q, nloop):
    """An A+D tag's NLOOP data quadwords: value in the low 64 bits, GS register id in bits 64..71."""
    out = []
    for k in range(nloop):
        p = q + 16 + 16 * k
        if p + 16 > len(buf):
            break
        val = int.from_bytes(buf[p:p + 8], "little")
        rid = buf[p + 8]
        out.append((rid, val))
    return out


def fmt(t):
    return "cell %2d  PRIM %-14s IIP%d TME%d ABE%d  NREG %d  [%s]" % (
        t["cell"], PRIMTYPE.get(t["prim"] & 7, "?"), (t["prim"] >> 3) & 1, (t["prim"] >> 4) & 1,
        (t["prim"] >> 6) & 1, t["nreg"], ", ".join(REGNAME.get(r, str(r)) for r in t["regs"]))


ctl = tags_of(0x5409C0)
ok = [t for t in ctl if t["cell"] == 0 and (t["prim"] & 7) == 4 and t["nreg"] == 6
      and t["regs"] == [2, 1, 4, 2, 1, 4]]
print("POSITIVE CONTROL 005409C0: %d tag(s); the published decode present: %s"
      % (len(ctl), "YES" if ok else "NO"))
for t in ctl:
    print("   " + fmt(t))
if not ok:
    raise SystemExit("positive control failed - nothing written")

random.seed(7)
others = [f for f in funcs if 0x300000 <= f <= 0x500000 and funcs[f] > 400]
sample = random.sample(others, min(150, len(others)))
fp = sum(1 for f in sample if tags_of(f))
BASE_RATE = fp / len(sample)
print("NEGATIVE CONTROL: %d of %d ordinary functions yield a tag - base rate %.1f%%"
      % (fp, len(sample), 100 * BASE_RATE))


def hub_pairs(hub):
    o = off(hub)
    # This script execs disw.py's head into its own globals, so a module-level name here can
    # silently overwrite one of the disassembler's. It happened: a local BASE shadowed the image
    # base and off() started returning floats. Assert rather than trust.
    assert isinstance(o, int), "disw globals clobbered: off() returned %r" % (o,)
    pairs, cur = [], None
    for i in md.disasm(d[o:o + funcs[hub]], hub):
        ops = i.operands
        if i.mnemonic == "lea" and ops and ops[0].type == X86_OP_REG \
                and md.reg_name(ops[0].reg) == "rcx" and ops[1].type == X86_OP_MEM \
                and md.reg_name(ops[1].mem.base) == "rip":
            cur = i.address + i.size + ops[1].mem.disp
        elif i.mnemonic == "call" and ops and ops[0].type == X86_OP_IMM and cur is not None:
            pairs.append((cur, ops[0].imm))
            cur = None
    return pairs


seen = {}
for obj, b in hub_pairs(0x37E0F0) + hub_pairs(0x37DF90):
    if b in funcs and b not in seen:
        seen[b] = obj
hit = {}
for b, obj in sorted(seen.items()):
    t = tags_of(b)
    if t:
        hit[b] = (obj, t)
print("\nPOPULATION: %d builders, %d with a tag (%.0f%%) against the %.1f%% base rate"
      % (len(seen), len(hit), 100 * len(hit) / max(1, len(seen)), 100 * BASE_RATE))

shapes = collections.Counter()
nad = ndraw = 0
for b, (obj, ts) in hit.items():
    for t in ts:
        # A tag with PRE=0 does not write PRIM; reporting its PRIM field as a primitive would be
        # reading a field the GS ignores. Say so instead.
        p = PRIMTYPE.get(t["prim"] & 7, "?") if t["pre"] else "(PRE=0)"
        shapes[(p, t["nreg"], tuple(REGNAME.get(r, str(r)) for r in t["regs"]))] += 1
        if t["regs"] == [14]:
            nad += 1
        else:
            ndraw += 1
print("\n%d tags: %d register-write (NREG 1, A+D) and %d vertex-list" % (nad + ndraw, nad, ndraw))
print("\nSHAPES:")
for (p, n, regs), c in shapes.most_common():
    print("   x%-3d %-22s NREG %-2d [%s]" % (c, p, n, ", ".join(regs)))

ALPHA_OP = {0: "Cs", 1: "Cd", 2: "0", 3: "?"}
ALPHA_C = {0: "As", 1: "Ad", 2: "FIX", 3: "?"}
ATST = {0: "NEVER", 1: "ALWAYS", 2: "LESS", 3: "LEQUAL", 4: "EQUAL", 5: "GEQUAL", 6: "GREATER",
        7: "NOTEQUAL"}
AFAIL = {0: "KEEP", 1: "FB_ONLY", 2: "ZB_ONLY", 3: "RGB_ONLY"}
ZTST = {0: "NEVER", 1: "ALWAYS", 2: "GEQUAL", 3: "GREATER"}


def dec_alpha(v):
    return "(%s-%s)*%s+%s  FIX=%d" % (ALPHA_OP[v & 3], ALPHA_OP[(v >> 2) & 3],
                                      ALPHA_C[(v >> 4) & 3], ALPHA_OP[(v >> 6) & 3],
                                      (v >> 32) & 0xFF)


def dec_test(v):
    return "ATE=%d ATST=%s AREF=%d AFAIL=%s DATE=%d ZTE=%d ZTST=%s" % (
        v & 1, ATST[(v >> 1) & 7], (v >> 4) & 0xFF, AFAIL[(v >> 12) & 3], (v >> 14) & 1,
        (v >> 16) & 1, ZTST[(v >> 17) & 3])


# Why the builders with no tag have none. "Unmeasured false-negative rate" is a weaker statement
# than the data supports: a template that authors no UNPACK payload cannot hold a tag at all.
noun = nopay = unexplained = 0
for b in sorted(set(seen) - set(hit)):
    img = build_image(b)
    ups = [(o_, v) for o_, (v, w) in img.items() if w == 4 and 0x60 <= ((v >> 24) & 0xFF) <= 0x7F]
    if not ups:
        noun += 1
    elif not any(o_ > u for u, _ in ups for o_ in img):
        nopay += 1
    else:
        unexplained += 1
print("\nTHE %d BUILDERS WITH NO TAG: %d author no UNPACK at all, %d an UNPACK with no payload "
      "stores after it, %d carry a payload and still yield nothing"
      % (len(seen) - len(hit), noun, nopay, unexplained))

adreg = collections.Counter()
blank = set_ = 0
unknown = []
for b, (obj, ts) in sorted(hit.items()):
    for t in ts:
        for rid, val in t.get("ad", []):
            adreg[rid] += 1
            # A slot with a real register id but a zero value is a named placeholder the program
            # fills at emit time; only a non-zero value is authored state. Counting a zero value
            # as authored is what the first version of this block did, and it was wrong.
            if val:
                set_ += 1
            else:
                blank += 1
            if rid not in GSREG:
                unknown.append((b, t["cell"], rid))
print("\nA+D PAYLOADS: %d register-write slots - %d carry a value, %d name a register but are zero"
      % (blank + set_, set_, blank))
print("   " + ", ".join("%s x%d" % (GSREG.get(r, "0x%02X" % r), c) for r, c in adreg.most_common()))
if unknown:
    print("   NOT A GS REGISTER (so these tags are likely false positives): "
          + ", ".join("%08X cell %d id 0x%02X" % u for u in unknown))
print("\nAUTHORED VALUES:")
for b, (obj, ts) in sorted(hit.items()):
    for t in ts:
        for rid, val in t.get("ad", []):
            if not val:
                continue
            extra = dec_alpha(val) if rid == 0x42 else dec_test(val) if rid == 0x47 else ""
            print("   %08X cell %-3d %-10s 0x%012X  %s"
                  % (b, t["cell"], GSREG.get(rid, "0x%02X" % rid), val, extra))

OUT = os.path.join(HERE, "vif1-gif-tags.tsv")
with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("builder\tobject\tcell\tunpack_at\tnloop\teop\tpre\tprim_raw\tprim\tiip\ttme\tfge\tabe"
             "\tnreg\tregs\tad_payload\n")
    for b, (obj, ts) in sorted(hit.items()):
        for t in ts:
            # PRE=0 means the tag does not write PRIM, so the field is not a primitive there.
            prim = PRIMTYPE.get(t["prim"] & 7, "?") if t["pre"] else "(PRE=0, PRIM unwritten)"
            ad = ";".join("%s=0x%X" % (GSREG.get(r, "0x%02X" % r), v) for r, v in t.get("ad", []))
            fh.write("%08X\t%08X\t%d\t+0x%X\t%d\t%d\t%d\t0x%03X\t%s\t%d\t%d\t%d\t%d\t%d\t%s\t%s\n" % (
                b, obj, t["cell"], t["unpack"], t["nloop"], t["eop"], t["pre"], t["prim"],
                prim, (t["prim"] >> 3) & 1, (t["prim"] >> 4) & 1,
                (t["prim"] >> 5) & 1, (t["prim"] >> 6) & 1, t["nreg"],
                ",".join(REGNAME.get(r, str(r)) for r in t["regs"]), ad))
print("\nwrote", OUT)
