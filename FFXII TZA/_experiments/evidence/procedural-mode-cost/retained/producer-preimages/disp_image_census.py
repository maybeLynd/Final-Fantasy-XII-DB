#!/usr/bin/env python3
"""disp_image_census.py - every memory operand in .text at given displacements, across the image.

WHY THIS EXISTS. A field census built from a function list answers "which of THESE functions touch
this offset". It cannot answer "does anything read this field", because the honest reply to a
function list is always "nothing in the list". On 2026-09-15 `CharacterRenderSystemTail +0x28` was
documented as a per-frame fade step stamped into `CharacterRenderRecord +0x414`; the record census
showed two writes and no read, which by itself proves only that the census's seeds do not read it.
This instrument decodes .text end to end instead, and found 22 operands at displacement `0x414` of
which exactly the two known writes belong to that record - so the field has NO READER, the step
reading was withdrawn, and the field stayed UNRESOLVED.

WHAT IT IS. An UPPER BOUND on the accesses to a field at an offset. It cannot tell one type from
another: every site is printed with its base register and full instruction, and the caller decides
which sites are the type in question. That is the point - the twenty sites it cannot attribute are
what stop it being read as a type-aware census.

ITS LIMITS, which belong in any evidence line that cites it:

  * the sweep is LINEAR from the start of .text and resynchronises one byte past whatever capstone
    refuses, so data embedded in .text can decode as instructions; sites adjacent to a resync are
    the suspect ones, and the resync count is printed for that reason.
  * a displacement formed at run time (the offset in a register) is invisible.
  * so is a reader that folds an array element's offset into the displacement (`[base + 0x740*n +
    0x414]` with n constant), or that works from a pointer biased off the object base.
  * AND SO IS A FIELD OFFSET FOLDED INTO A LINK-TIME BASE ADDRESS, which is the worst of them because
    it leaves NO DISPLACEMENT AT ALL to key on (FABLE, 2026-09-16, on ActorManagerSlot +0x201):

        00267310  lea   rax, [rip + 0x1E31CF0]    ; = 02099011 = 02098E10 + 0x201
                  imul  rcx, rax, 0x288           ; slot * stride
                  movzx eax, byte ptr [rcx + rax] ; disp == 0

    Nothing about that site is unusual - it is what a compiler emits for `array[i].field` when the
    array base is a link-time constant - and a sweep keyed on `disp == 0x201` cannot match it. **A
    field reached ONLY through a folded base looks exactly like a field with no accesses**, and the
    under-count is invisible from inside the census. This instrument does not detect that shape; a
    sweep for `lea` targets near a known array base, differenced against the base, would.

ALWAYS PAIR IT WITH A POSITIVE CONTROL: run it on a displacement whose sites are already known and
check it returns them. A zero result from an instrument nobody proved can return non-zero is not a
negative. The self-test does exactly this against a known displacement.

ONE SWEEP, MANY DISPLACEMENTS. Decoding .text costs ~13 s, so asking it about nine offsets one at
a time costs nine sweeps for no reason. Give it several and it answers them all in one pass; the
per-displacement results are identical either way, which the self-test checks.

usage: disp_image_census.py <disp_hex> [<disp_hex> ...] [--kind r|w] [--exe PATH]
       disp_image_census.py --self-test
"""
import os
import struct
import sys

import capstone
from capstone import x86

HERE = os.path.dirname(os.path.abspath(__file__))
EXE_DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", "work", "exe", "FFXII_TZA.exe"))
BASE = 0x120000


def text_section(data):
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    optsz = struct.unpack_from("<H", data, pe + 20)[0]
    off = pe + 24 + optsz
    for _ in range(nsec):
        name = data[off:off + 8].rstrip(b"\0").decode()
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", data, off + 8)
        if name == ".text":
            return va, vsz, rptr, rsz
        off += 40
    raise SystemExit("no .text section")


def census(exe, disps, kind=None):
    """Return ({disp: rows}, decoded, resyncs); a row is (va, access, mnemonic, op_str, base_reg)."""
    data = open(exe, "rb").read()
    va, _vsz, rptr, rsz = text_section(data)
    body = data[rptr:rptr + rsz]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    want_disp = set(disps)
    rows = dict((d, []) for d in want_disp)
    decoded, resyncs, pos = 0, 0, 0
    while pos < len(body):
        last = pos
        for ins in md.disasm(body[pos:], va + BASE + pos):
            decoded += 1
            last = ins.address - (va + BASE) + ins.size
            for op in ins.operands:
                if op.type != x86.X86_OP_MEM or op.mem.disp not in want_disp or op.mem.base == 0:
                    continue
                acc = ("w" if op.access & capstone.CS_AC_WRITE else "") + \
                      ("r" if op.access & capstone.CS_AC_READ else "")
                if kind and kind not in acc:
                    continue
                rows[op.mem.disp].append(
                    (ins.address, acc, ins.mnemonic, ins.op_str, ins.reg_name(op.mem.base)))
        pos = last + 1 if last > pos else pos + 1
        resyncs += 1
    return rows, decoded, resyncs


def self_test(exe):
    """The control this instrument's own evidence line is required to quote."""
    # asked alongside another displacement, so the control also proves the multi-displacement
    # path does not leak sites between the offsets it is tracking
    rows, decoded, resyncs = census(exe, [0x48824, 0x4881C])
    got = sorted("%08X%s" % (a, k) for a, k, _m, _o, _b in rows[0x48824])
    want = sorted(["002E83A7w", "00426C6Bw", "0042EA94r", "0042EB2Br", "0042ED49w"])
    ok = got == want
    start = sorted("%08X%s" % (a, k) for a, k, _m, _o, _b in rows[0x4881C])
    want_start = sorted(["002EBC37w", "00426C60w", "0042EA9Cr", "0042EB36r", "0042ED3Ew"])
    if start != want_start:
        ok = False
        print("  FAIL: the 0x4881C half of the paired control returned %s" % start)
    print("control disp=0x48824 (+0x4881C): %s" % ("PASS" if ok else "FAIL"))
    if not ok:
        print("  expected %s" % want)
        print("  got      %s" % got)
    print("  %d instruction(s) decoded, %d resync(s)" % (decoded, resyncs))
    if decoded < 1000000:
        ok = False
        print("  FAIL: fewer than a million instructions decoded - the sweep stopped early")
    return 0 if ok else 1


def main(argv):
    exe = EXE_DEFAULT
    if "--exe" in argv:
        exe = argv[argv.index("--exe") + 1]
    if not os.path.exists(exe):
        raise SystemExit("image not found: %s" % exe)
    if "--self-test" in argv:
        return self_test(exe)
    if len(argv) < 2:
        raise SystemExit(__doc__)
    kind = argv[argv.index("--kind") + 1] if "--kind" in argv else None
    skip = set()
    for flag in ("--kind", "--exe"):
        if flag in argv:
            skip |= {argv.index(flag), argv.index(flag) + 1}
    disps = [int(a, 16) for i, a in enumerate(argv[1:], 1)
             if i not in skip and not a.startswith("--")]
    if not disps:
        raise SystemExit(__doc__)
    rows, decoded, resyncs = census(exe, disps, kind)
    for d in disps:
        if len(disps) > 1:
            print("displacement 0x%x" % d)
        for a, acc, m, o, b in rows[d]:
            print("%08X  %-2s %-8s %-44s base=%s" % (a, acc, m, o, b))
        print("--- %d operand(s) at displacement 0x%x%s"
              % (len(rows[d]), d, "; kind=%s" % kind if kind else ""))
    print("--- one sweep over .text: %d instruction(s) decoded, %d resync(s)" % (decoded, resyncs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
