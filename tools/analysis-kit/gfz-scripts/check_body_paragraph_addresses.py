#!/usr/bin/env python3
"""check_body_paragraph_addresses.py - does a body-description paragraph cite addresses its body touches?

OPUS, 2026-09-25. Found while working the UC-1 citation list: the vtable-method-index paragraph for
`005FD050` (a hub entry appended 2026-09-17) is right about the function's SHAPE and wrong about four
of its addresses - the object it constructs (02CC0410, published 032703C8), the guard epoch
(02CE2610 / 032F2610), the TLS index (02EAED3C / 02E3DD2C) and the atexit target (008ADDD0 /
00602DA0, which is a 0x01-filled data table nothing references). The interior anchor it cites
(005FD065) is correct, so an anchor check passes it.

This reads every paragraph that opens with a body header - a backticked listed entry followed by
'—' and a byte count, the hub-entry form `ADDR` — N B - and asks, for each other backticked
8-hex address in that paragraph, whether the named body supports it:

  SELF        the entry itself
  INTERIOR    an instruction address inside the body
  TRANSFER    a call/jmp/jcc target from the body
  RIP         a rip-relative operand target in the body (data or code)
  VIA-CALLEE  touched by a direct callee / tail-jump target of the body (one level)
  UNSUPPORTED none of the above - the paragraph names an address this body never touches

UNSUPPORTED is a QUESTION, not a verdict: a paragraph may legitimately name a caller, a sibling or
a global reached through a register. It is ranked by how many a paragraph has. Read-only.

    check_body_paragraph_addresses.py FILE.md [FILE.md ...] [--out rows.tsv]
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_default_instance_writers as W  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP  # noqa: E402

HEAD = re.compile(r"^`(00[0-9A-F]{6})`\s+—\s+\d[\d,]*\s*B\b")
TOK = re.compile(r"`(0[0-9A-F]{7})`")


def body_facts(img, e):
    """Instruction addresses, and every absolute address the body names: call/jump targets,
    rip-relative operands, and the image-base idiom `lea rX,[rip->imagebase]` then `[rX + rva]`
    (this image reaches many globals that way, and a rip-only view calls them unsupported)."""
    import reg_tracking as RT
    inner, targets, based = set(), set(), set()
    for i in img.body(e):
        inner.add(i.address)
        for op in i.operands:
            if op.type == X86_OP_IMM and (i.mnemonic == "call" or i.mnemonic.startswith("j")):
                targets.add(op.imm)
            if op.type == X86_OP_MEM:
                if op.mem.base == X86_REG_RIP:
                    targets.add(i.address + i.size + op.mem.disp)
                elif op.mem.base and RT.canon(i.reg_name(op.mem.base)) in based:
                    targets.add(img.base + op.mem.disp)
        if (i.mnemonic == "lea" and len(i.operands) == 2 and i.operands[1].type == X86_OP_MEM
                and i.operands[1].mem.base == X86_REG_RIP
                and i.address + i.size + i.operands[1].mem.disp == img.base):
            based.add(RT.canon(i.reg_name(i.operands[0].reg)))
            continue
        for r in RT.written(i):
            based.discard(r)
    return inner, targets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    img = W.Image()
    rows = []
    for path in a.files:
        lines = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
        n = 0
        while n < len(lines):
            m = HEAD.match(lines[n])
            if not m or int(m.group(1), 16) not in img.sizes:
                n += 1
                continue
            e = int(m.group(1), 16)
            para, start = [], n + 1
            while n < len(lines) and lines[n].strip():
                para.append(lines[n])
                n += 1
            text = " ".join(para)
            inner, targets = body_facts(img, e)
            # ONE LEVEL DOWN: a paragraph may credit a global to a direct callee or tail-jump target
            # ("calls 002E15D0 (clears the 0215F1A0 latch)"), which the body itself never touches.
            via = set()
            for c in targets:
                if c in img.sizes and c != e:
                    _ci, ct = body_facts(img, c)
                    via |= ct
            for t in sorted(set(TOK.findall(text))):
                v = int(t, 16)
                cls = ("SELF" if v == e else "INTERIOR" if v in inner else
                       "TRANSFER" if v in targets and v in img.sizes else "RIP" if v in targets else
                       "VIA-CALLEE" if v in via else "UNSUPPORTED")
                rows.append((os.path.basename(path), start, "%08X" % e, t, cls))
    per = collections.Counter((r[0], r[1], r[2]) for r in rows if r[4] == "UNSUPPORTED")
    tot = collections.Counter(r[4] for r in rows)
    print("addresses checked: %d  %s" % (len(rows), dict(tot)))
    print("paragraphs with UNSUPPORTED addresses: %d" % len(per))
    for (f, ln, e), k in per.most_common(15):
        print("  %-40s L%-5d %s  %d unsupported" % (f[:40], ln, e, k))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("file\tline\tentry\taddress\tclass\n")
            for r in rows:
                fh.write("%s\t%d\t%s\t%s\t%s\n" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
