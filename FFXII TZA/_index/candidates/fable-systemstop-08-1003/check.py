"""check.py - executed regression for FABLE's amendment of CONTRACT-system-stop-registry.md section 14 (SystemStopRecord
+0x08), answering OPUS-REQ-FABLE-SYSTEMSTOP-14-1003 (FABLE, 2026-10-03). Static; reads the certified image only.

Claims checked:
  C1  the builder 00227680 stores the qword +0x08 of both records of one id: 0 on entry (2 stores) and all-ones in
      five arms (10 stores);
  C2  its record pointer is the per-id table: the start wrapper forms 01FD4160 + idx*8 (idx = id*3) and passes it;
  C3  every rip-relative reference into the table and the combined records (01FD4160..01FD46D0), found by a raw rel32
      sweep of every .text offset, lies in one of seven known functions (so the reader set below is complete for
      rip-formed bases);
  C4  in those functions, every operand through a table/record pointer maps to record offset 0x00, 0x10 or 0x14; the
      only +0x08 operands are the builder's stores (no reader of +0x08);
  C5  the combined records' +0x08 (01FD46A8 / 01FD46C0) and +0x10 (01FD46B0 / 01FD46C8) have no reader: their only
      rip references are the apply's copies (writes), the initialiser's +0x10 store and the loop bound (lea);
  C6  the apply's stack slots that those copies take +0x08 and +0x10 from ([rsp+0x40]/[rsp+0x48] and
      [rsp+0x28]/[rsp+0x30]) are written by no instruction in the apply (00226280..00226638, .pdata-covered, no jump
      leaves it).
Control (sensitivity): the same offset classifier must find the apply's known readers of +0x00 (002262E0, 002262E4)
and +0x10 (002262EE); a classifier that reached nothing would also print "no +0x08 reader".
Prints FAILS N last."""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone import x86_const as X  # noqa: E402
img = Img.load(); img.cs.detail = True
TABLE, COMB, END = 0x01FD4160, 0x01FD46A0, 0x01FD46D0
fails = 0


def check(name, ok, detail=""):
    global fails
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  | " + detail) if detail else "")); fails += not ok


def dis(s, e):
    return list(img.cs.disasm(img.read(s, e - s), s))


def rip_target(i, op):
    return i.address + i.size + op.mem.disp


# function extents (.pdata chains; three leaves have no .pdata and are bounded by their ret)
FUN = {0x00225CD0: 0x00225EA4, 0x00225EB0: 0x00226096, 0x00226280: 0x00226638, 0x00226B10: 0x00226B23,
       0x00226B30: 0x00226B9F, 0x00226BA0: 0x00226BB8, 0x00226BE0: 0x00227370}
BUILDER = (0x00227680, 0x00227D24)

# C1
st = [(i.address, i.op_str) for i in dis(*BUILDER) if i.mnemonic == "mov" and re.match(r"qword ptr \[r(dx|8|bx) \+ 8\], ", i.op_str)]
zero = [a for a, o in st if o.endswith(", rax")]
ones = [a for a, o in st if o.endswith("0xffffffffffffffff")]
check("C1 builder stores +0x08: 2 zero stores on entry, 10 all-ones stores in five arms", len(zero) == 2 and len(ones) == 10,
      "zero %s; ones %s" % (" ".join("%08X" % a for a in zero), " ".join("%08X" % a for a in ones)))
pre = {i.address: i for i in dis(0x00227680, 0x002276A6)}
check("C1 the zero is xor eax,eax at 00227686", pre.get(0x00227686) is not None and pre[0x00227686].mnemonic == "xor"
      and pre[0x00227686].op_str == "eax, eax")

# C2
w = {i.address: i for i in dis(0x00226BE0, 0x00226C80)}
lea = w.get(0x00226C20)
ok2 = (lea is not None and lea.mnemonic == "lea" and lea.op_str.startswith("rax,") and rip_target(lea, lea.operands[1]) == TABLE
       and w.get(0x00226C37) is not None and w[0x00226C37].op_str == "r15, [rax + r10*8]"
       and w.get(0x00226C5A) is not None and w[0x00226C5A].op_str == "rdx, r15"
       and w.get(0x00226C72) is not None and w[0x00226C72].mnemonic == "call" and w[0x00226C72].op_str == "0x227680")
check("C2 the start wrapper passes table 01FD4160 + idx*8 as rdx to 00227680", ok2)

# C3 raw rel32 sweep
_, va, vs, ra, rs = [s for s in img.secs if s[0] == ".text"][0]
raw = img.d[ra:ra + rs]
hits = {}
for p in range(len(raw) - 4):
    d = struct.unpack_from("<i", raw, p)[0]
    for imm in (0, 1, 2, 4):
        a = img.base + va + p
        t = a + 4 + imm + d
        if not (TABLE <= t < END):
            continue
        for back in range(2, 10):
            s = a - back
            ins = next(img.cs.disasm(img.read(s, 16), s), None)
            if ins is None or ins.address + ins.size != a + 4 + imm:
                continue
            if any(o.type == X.X86_OP_MEM and o.mem.base == X.X86_REG_RIP for o in ins.operands):
                hits[s] = t
                break
inside = lambda a: any(f <= a < e for f, e in FUN.items()) or BUILDER[0] <= a < BUILDER[1]
outside = sorted(a for a in hits if not inside(a))
check("C3 every rip reference into 01FD4160..01FD46D0 lies in the seven known functions", not outside and len(hits) > 0,
      "%d references; outside: %s" % (len(hits), " ".join("%08X" % a for a in outside) or "none"))

dref = 0
for name, sva, svs, sra, srs in img.secs:
    if name == ".text":
        continue
    blob = img.d[sra:sra + srs]
    for p in range(0, len(blob) - 8, 4):
        q = struct.unpack_from("<Q", blob, p)[0]; v = struct.unpack_from("<I", blob, p)[0]
        dref += (TABLE <= q < END) or (TABLE <= img.base + v < END)
check("C3 no absolute qword or 32-bit image-relative value in any other section points into the range", dref == 0,
      "%d" % dref)

# C4 per-function pointer-register operands -> record offset (base offset of the register mod 0x18)
BASES = {0x00225CD0: {"rcx + rdx": 0}, 0x00225EB0: {"r13": 0x14}, 0x00226280: {"rax": 0x10},
         0x00226B30: {"rax": 0, "rdx": 0x14}, 0x00227680: {"rdx": 0, "r8": 0, "rbx": 0}}
RANGES = {0x00225CD0: (0x00225E00, 0x00225EA4), 0x00225EB0: (0x00225FE0, 0x00226096), 0x00226280: (0x002262E0, 0x00226317),
          0x00226B30: (0x00226B60, 0x00226B9F), 0x00227680: BUILDER}
offs = {}
for f, regs in BASES.items():
    for i in dis(*RANGES[f]):
        m = re.search(r"\[(r[a-z0-9]+(?: \+ r[a-z0-9]+)?)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]", i.op_str)
        if not m or m.group(1) not in regs:
            continue
        disp = int(m.group(3), 0) * (-1 if m.group(2) == "-" else 1) if m.group(3) else 0
        o = (regs[m.group(1)] + disp) % 0x18
        rd = "W" if i.op_str.startswith(m.group(0)) or i.op_str.split(",")[0].endswith(m.group(0)) else "R"
        if i.mnemonic in ("test", "cmp"): rd = "R"
        if i.mnemonic in ("and", "or") and rd == "W": rd = "RW"
        offs.setdefault(o, []).append((i.address, rd, f))
eight = offs.get(8, [])
check("C4 operands at +0x08 are only the builder's 12 stores", len(eight) == 12 and all(f == 0x00227680 and "W" in rd for a, rd, f in eight),
      "offsets seen: %s" % ", ".join("+0x%02X x%d" % (k, len(v)) for k, v in sorted(offs.items())))
readers8 = [a for a, rd, f in eight if "R" in rd]
check("C4 no reader of +0x08 in any table function", not readers8)
# control
r0 = {a for a, rd, f in offs.get(0, []) if "R" in rd}
r10 = {a for a, rd, f in offs.get(0x10, []) if "R" in rd}
check("CONTROL the classifier finds the apply's +0x00 readers 002262E0/002262E4 and +0x10 reader 002262EE",
      {0x002262E0, 0x002262E4} <= r0 and 0x002262EE in r10,
      "+0x00 readers %d, +0x10 readers %d" % (len(r0), len(r10)))

# C5 combined records
comb = sorted((a, t) for a, t in hits.items() if COMB <= t < END)
desc = []
bad = []
for a, t in comb:
    ins = next(img.cs.disasm(img.read(a, 16), a))
    rec = "A" if t < 0x01FD46B8 else "B"
    o = t - (COMB if rec == "A" else 0x01FD46B8)
    kind = "lea" if ins.mnemonic == "lea" else ("W" if ins.op_str.startswith(("xmmword ptr [rip", "qword ptr [rip", "dword ptr [rip", "byte ptr [rip")) else "R")
    width = 16 if "xmmword" in ins.op_str else 8 if "qword" in ins.op_str else 4 if "dword" in ins.op_str else 1 if "byte" in ins.op_str else 0
    desc.append("%08X %s %s+0x%02X w%d" % (a, kind, rec, o, width))
    if kind == "R" and (o <= 8 < o + width or o <= 0x10 < o + width):
        bad.append(a)
check("C5 no reader of the combined records' +0x08 or +0x10 (01FD46A8/B0, 01FD46C0/C8)", not bad, "; ".join(desc))
acc = [(0x0022AB2D, "ecx, dword ptr [rax]"), (0x0025D95F, "qword ptr [rax], rcx")]
ok5 = True
for a, frag in acc:
    nx = list(img.cs.disasm(img.read(a, 0x30), a))
    ok5 &= nx[0].op_str == "0x226b10" and any(frag in i.op_str for i in nx[1:5])
check("C5 the record accessor 00226B10's two callers read +0x00 only (0022AB2D, 0025D95F)", ok5)

# C6 apply stack slots
ap = dis(0x00226280, 0x00226638)
wr = [i for i in ap if re.search(r"\[rsp \+ 0x(28|2c|30|34|40|44|48|4c)\]", i.op_str) and not i.mnemonic.startswith(("movups", "movsd")) or
      (re.search(r"\[rsp \+ 0x(28|2c|30|34|40|44|48|4c)\]", i.op_str) and i.op_str.startswith(("qword ptr [rsp", "dword ptr [rsp", "xmmword ptr [rsp")))]
lea_rsp = [i for i in ap if i.mnemonic == "lea" and "rsp" in i.op_str]
out_j = [i for i in ap if i.group(X.X86_GRP_JUMP) and i.operands[0].type == X.X86_OP_IMM and not (0x00226280 <= i.operands[0].imm < 0x00226638)]
check("C6 the apply never writes [rsp+0x28/0x30/0x40/0x48], takes no stack address, and no jump leaves it",
      not wr and not lea_rsp and not out_j, "writes %d, lea rsp %d, jumps out %d" % (len(wr), len(lea_rsp), len(out_j)))
print("FAILS %d" % fails)
