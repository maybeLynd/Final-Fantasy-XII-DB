"""check_s35.py - FABLE, 2026-10-03, on SWE2-AUDIT-SPEC's L2 expansion (item 1, S-35 notation).

Claim checked: CONTRACT-binding-profiles.md section 5 writes `01F7FFE0+0x38` (written) and `01F7FFE0+8/+9`
(read). 01F7FFE0 is an 8-byte POINTER cell (InputManagerPointer), so the bytes touched are in the
POINTEE: [01F7FFE0]+0x38, [01F7FFE0]+0x08, [01F7FFE0]+0x09. The literal reading - static cells 01F80018,
01F7FFE8, 01F7FFE9 - has no reference anywhere in .text.

Prints PASS/FAIL lines and FAILS N last. Controls:
  C1 (sensitivity, image): a patched copy of the image whose store at 0019744B is rewritten to hit the
     LITERAL cell 01F80018 rip-relatively must be FOUND by the same raw index. So the zero on the real
     image is not instrument blindness.
  C2 (sensitivity, reading): the old literal reading, asserted as a claim ("some .text instruction
     writes 01F80018"), must FAIL on the real image.
  C3 (positive): the raw index must find the pointer cell 01F7FFE0 itself at >= the 8 poll sites read here.
"""
import os
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_REG_RIP  # noqa: E402

DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CELL = 0x01F7FFE0
LITERALS = (0x01F7FFE8, 0x01F7FFE9, 0x01F80018)
fails = 0


def report(ok, label, detail):
    global fails
    print("%s %s: %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        fails += 1


def text_sec(img):
    for name, sva, vs, ra, rs in img.secs:
        if name == ".text":
            return sva, ra, min(vs, rs)
    raise SystemExit("no .text")


def raw_index(img, target):
    """Every .text instruction whose memory operand resolves to `target`, by a raw disp32 scan
    (rip-relative with 0/1/2/4 trailing immediate bytes, and image-base-relative [reg+RVA]),
    each candidate confirmed by decoding the instruction that contains it."""
    sva, ra, n = text_sec(img)
    buf = np.frombuffer(img.d, dtype=np.uint8, count=n, offset=ra)
    d32 = buf[:-3].astype(np.int64) | (buf[1:-2].astype(np.int64) << 8) | (buf[2:-1].astype(np.int64) << 16) | (buf[3:].astype(np.int64) << 24)
    d32 = np.where(d32 >= 2 ** 31, d32 - 2 ** 32, d32)
    pos_va = img.base + sva + np.arange(len(d32), dtype=np.int64)
    cand = set()
    for k in (0, 1, 2, 4):
        cand.update(np.nonzero(pos_va + 4 + k + d32 == target)[0].tolist())
    cand.update(np.nonzero(d32 == target - img.base)[0].tolist())
    hits = []
    for p in sorted(cand):
        va = img.base + sva + p
        for back in range(1, 12):
            st = va - back
            ins = list(img.cs.disasm(img.read(st, 16), st, 1))
            if not ins:
                continue
            i = ins[0]
            if not (i.address < va and i.address + i.size >= va + 4):
                continue
            got = False
            for op in i.operands:
                if op.type != X86_OP_MEM:
                    continue
                if op.mem.base == X86_REG_RIP and i.address + i.size + op.mem.disp == target:
                    got = True
                elif op.mem.base != X86_REG_RIP and op.mem.disp == target - img.base:
                    got = True
            if got:
                hits.append((i.address, i.mnemonic + " " + i.op_str))
                break
    return sorted(set(hits))


def main():
    img = Img.load()
    head = os.popen('git -C "%s" rev-parse --short HEAD' % DB).read().strip()
    print("check_s35.py  HEAD %s  image sha256 73461d08... (asserted by rvlib)" % head)

    # 1. the type store says 01F7FFE0 is an 8-byte pointer cell, and the pointee rows exist
    types = open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8").read().splitlines()
    fields = open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8").read().splitlines()
    ptr = [r for r in types if r.startswith("InputManagerPointer\t")]
    report(len(ptr) == 1 and ptr[0].split("\t")[1] == "0x8" and "0x01F7FFE0" in ptr[0],
           "T1 store: InputManagerPointer is 0x8 at 01F7FFE0", ptr[0][:90] if ptr else "missing")
    rows = {}
    for r in fields:
        c = r.split("\t")
        if c[0] == "InputManager" and c[1] in ("0x08", "0x09", "0x38"):
            rows[c[1]] = c[3]
    report(set(rows) == {"0x08", "0x09", "0x38"}, "T2 store: pointee rows InputManager +0x08/+0x09/+0x38 declared",
           ", ".join("%s %s" % kv for kv in sorted(rows.items())))

    # 2. the bytes: each touch is a qword load of the cell followed by an access through the loaded register
    sites = [  # (load, use, disp, kind)
        (0x00197444, 0x0019744B, 0x38, "write"),
        (0x001973FF, 0x0019740F, 0x08, "read"),
        (0x00197513, 0x0019751A, 0x08, "read"),
        (0x00197527, 0x0019752E, 0x09, "read"),
        (0x001975C4, 0x001975CB, 0x08, "read"),
        (0x001975D8, 0x001975DF, 0x09, "read"),
    ]
    for load, use, disp, kind in sites:
        li = next(img.cs.disasm(img.read(load, 15), load, 1))
        ui = next(img.cs.disasm(img.read(use, 15), use, 1))
        lop = li.operands[1] if len(li.operands) == 2 else None
        ok_load = (li.mnemonic == "mov" and lop is not None and lop.type == X86_OP_MEM and lop.mem.base == X86_REG_RIP
                   and li.address + li.size + lop.mem.disp == CELL and lop.size == 8)
        dreg = li.reg_name(li.operands[0].reg) if ok_load else None
        mem = [op for op in ui.operands if op.type == X86_OP_MEM]
        ok_use = bool(mem) and ui.reg_name(mem[0].mem.base) == dreg and mem[0].mem.disp == disp
        if kind == "write":
            ok_use = ok_use and ui.operands[0].type == X86_OP_MEM and ui.mnemonic == "mov"
        report(ok_load and ok_use, "B %s %08X" % (kind, use),
               "%08X %s %s ; %08X %s %s  -> [%08X]+0x%02X (pointee)" % (li.address, li.mnemonic, li.op_str,
                                                                       ui.address, ui.mnemonic, ui.op_str, CELL, disp))

    # 3. raw index: the literal cells have no reference anywhere in .text
    for lit in LITERALS:
        h = raw_index(img, lit)
        report(len(h) == 0, "R literal %08X (= 01F7FFE0+0x%X) has no .text reference" % (lit, lit - CELL),
               "%d hits %s" % (len(h), ["%08X %s" % x for x in h[:4]]))

    # C3 positive control: the same index finds the pointer cell itself
    hc = raw_index(img, CELL)
    poll = [a for a, t in hc if 0x00197293 <= a < 0x001976DE]
    report(len(poll) >= 8, "C3 positive: raw index finds 01F7FFE0 itself",
           "%d .text references, %d in the poll body 00197293..001976DE" % (len(hc), len(poll)))

    # C1 sensitivity: plant a literal-cell store into a patched copy; the index must find it
    st = 0x00197444
    # mov byte ptr [rip+disp32], 1  = C6 05 disp32 01 (7 bytes), then pad the rest of the 2 insns (7+4=11) with nops
    disp = 0x01F80018 - (st + 7)
    patch = b"\xC6\x05" + struct.pack("<i", disp) + b"\x01" + b"\x90" * 4
    pimg = img.patched(st, patch)
    hp = raw_index(pimg, 0x01F80018)
    report(any(a == st for a, _ in hp), "C1 sensitivity: a planted literal store at 00197444 is found",
           "%d hits %s" % (len(hp), ["%08X %s" % x for x in hp[:2]]))

    # C2 sensitivity: the OLD literal reading as a claim must FAIL on the real image
    old_reading_holds = any(True for _ in raw_index(img, 0x01F80018))
    report(not old_reading_holds, "C2 old reading 'static cell 01F80018 is written' is FALSE on the real image",
           "old reading %s" % ("HOLDS (unexpected)" if old_reading_holds else "fails, as it must"))

    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
