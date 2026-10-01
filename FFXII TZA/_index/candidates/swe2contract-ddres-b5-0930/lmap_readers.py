"""lmap_readers.py - which lmap (menumap_location.bin) fields the location-map code reads, at the native offsets of the
lmap page's section 10. SWE2-CONTRACT, 2026-09-30. Static, instruction pins in the shipping EXE. Reads only.

Usage: python lmap_readers.py

Checks (PASS/FAIL; exit 0 only if all pass):
  C1  003C0740 walks array C: start = record + 4 + 24*(countA + countB) (003C07F9-003C0808), count = byte +2 (003C080B),
      stride 0x14 (003C084A), handing each entry to 003BCDE0 as r8 (003C0836, 003C083F).
  C2  003BCDE0 on one C entry (rdi = r8):
        +0x10 is a gate: 0xFFFF passes, anything else must pass PersistentFlag 0032A8A0 (003BCDEB-003BCE09);
        +0x00 / +0x02 are the two endpoints: the point's field id (+0xC) must equal one (003BCE94-003BCEA3), the other
        is the destination (003BCEB5), then found among the record's points by +0xC (003BCF45);
        +0x04/+0x06 and +0x0C/+0x0E are two word pairs 003C1180 tests (003BCEC9-003BCF06), unless mode +0xCA == 6;
        +0x04 .. +0x0F are copied into the 16-byte link descriptor (003BCFE6-003BD018).
  C3  no read of C +0x12 in 003BCDE0 or 003C0740 (control: the same filter finds +0x10 at 003BCDEB).
  P1  003C2320 (one draw row per point): point +0/+2 -> row +4/+6 (003C232E-003C2342); bytes +4..+7 -> row +8..+B,
      0xFF kept (003C2346-003C23A3); +8/+0xA -> row +0x18/+0x1A (003C23A6-003C23B2).
  P2  kind-0 arm (field points): +0xC field id -> row +0x1C, +0x10 & 3 -> row +0x1E (003C23CB-003C23DB).
  P3  kind-1 arm (markers, 003C248F): +0x11 marker kind (0xD remapped to 0x2F through 003BE700), +0x15 link selector,
      +0x10 -> row +0x20, +0x12 gate (0xFFFF or PersistentFlag) -> row +0x1C bit 0, then 003BDDE0 resolves the link.
  P5  003C1680 reads a point's +0x0C for the progress test 003C17E0 only when the point is kind 0 (array A): kind is
      r8d = 0 below countA (003C1765) and 1 above (003C178A), and 003C179D skips the read for kind 1. So the +0x0C that
      003C17E0 receives is a zone's field id, never a marker's destination-label id.
  P4  the kind-1 arm reads no +0x0C (the destination-label id of section 10.7) between 003C248F and its 003BDDE0 call
      at 003C253F. NARROWED 2026-09-30 on FABLE's rc36-lmap-label-fable-0930 (9a4cd5784): the marker arm CONTINUES past
      the call and reads +0x0C at 003C25BD (the drawn destination label) - this check's range ends at 003C253F and
      says nothing about the continuation.
"""
import os
import sys

import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import block_writer_disjoint as b  # noqa: E402

RES = []


def check(tag, ok, text):
    RES.append(ok)
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def main():
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True

    def body(f):
        return {i.address: (i.mnemonic, i.op_str) for i in md.disasm(at(f, ext[f]), f)}

    w = body(0x003C0740)
    check("C1", w.get(0x003C07F9) == ("movzx", "ecx, byte ptr [rcx + 1]") and
          w.get(0x003C07FD) == ("movzx", "eax, byte ptr [rdx]") and
          w.get(0x003C0805) == ("lea", "ecx, [rdx + 4]") and w.get(0x003C0808) == ("lea", "ecx, [rcx + rax*8]") and
          w.get(0x003C080B) == ("movzx", "eax, byte ptr [rdx + 2]") and w.get(0x003C084A) == ("add", "rdi, 0x14") and
          w.get(0x003C0836) == ("mov", "r8, rdi") and w.get(0x003C083F) == ("call", "0x3bcde0"),
          "C walk: rec+4+24*(A+B), count +2, stride 0x14, entry -> 003BCDE0 r8")

    c = body(0x003BCDE0)
    check("C2", c.get(0x003BCDEB) == ("movzx", "eax, word ptr [r8 + 0x10]") and
          c.get(0x003BCE01) == ("cmp", "ax, cx") and c.get(0x003BCE09) == ("call", "0x32a8a0") and
          c.get(0x003BCE94) == ("movzx", "eax, word ptr [rbx + 0xc]") and
          c.get(0x003BCE98) == ("cmp", "word ptr [rdi], ax") and c.get(0x003BCEA3) == ("cmp", "word ptr [rdi + 2], ax") and
          c.get(0x003BCEB5) == ("movzx", "r12d, word ptr [rax]") and
          c.get(0x003BCEC9) == ("movzx", "eax, word ptr [rdi + 4]") and
          c.get(0x003BCEDA) == ("movzx", "eax, word ptr [rdi + 6]") and c.get(0x003BCEE3) == ("call", "0x3c1180") and
          c.get(0x003BCEEC) == ("movzx", "eax, word ptr [rdi + 0xc]") and
          c.get(0x003BCEFD) == ("movzx", "eax, word ptr [rdi + 0xe]") and c.get(0x003BCF06) == ("call", "0x3c1180") and
          c.get(0x003BCEC0) == ("cmp", "byte ptr [rax + 0xca], 6") and
          c.get(0x003BCF45) == ("cmp", "word ptr [rax + 0xc], r12w") and
          c.get(0x003BCFE6) == ("lea", "rcx, [r14 + 4]") and c.get(0x003BCFED) == ("mov", "edx, 3") and
          c.get(0x003BD000) == ("movzx", "eax, word ptr [rdi + rcx]"),
          "C +0x10 gate, +0/+2 endpoints, +4/+6 and +0xC/+0xE to 003C1180, +4..+0xF copied")

    def mem_offsets(f, regs):
        out = []
        for i in md.disasm(at(f, ext[f]), f):
            for op in i.operands:
                if op.type == capstone.x86.X86_OP_MEM and op.mem.base in regs and op.mem.index == 0:
                    out.append((i.address, op.mem.base, op.mem.disp))
        return out
    R = capstone.x86
    offs = mem_offsets(0x003BCDE0, {R.X86_REG_RDI, R.X86_REG_R8})
    check("C3", (0x003BCDEB, R.X86_REG_R8, 0x10) in offs and not any(d == 0x12 for a, r, d in offs),
          "direct C-entry offsets read by 003BCDE0: %s" % sorted({d for a, r, d in offs}))

    p = body(0x003C2320)
    check("P1", p.get(0x003C232E) == ("movzx", "eax, word ptr [rdx]") and p.get(0x003C2334) == ("mov", "word ptr [rcx + 4], ax") and
          p.get(0x003C233B) == ("movzx", "eax, word ptr [rdx + 2]") and p.get(0x003C2342) == ("mov", "word ptr [rcx + 6], ax") and
          p.get(0x003C2346) == ("movzx", "eax, byte ptr [rdx + 4]") and p.get(0x003C2393) == ("movzx", "eax, byte ptr [rdx + 7]") and
          p.get(0x003C23A3) == ("mov", "byte ptr [rbp + 0xb], cl") and
          p.get(0x003C23A6) == ("movzx", "eax, word ptr [rdx + 8]") and p.get(0x003C23B2) == ("mov", "word ptr [rbp + 0x1a], ax"),
          "x/y -> row +4/+6; selector bytes +4..+7 -> row +8..+B; +8/+0xA -> row +0x18/+0x1A")
    check("P2", p.get(0x003C23CB) == ("movzx", "ecx, word ptr [rdx + 0xc]") and p.get(0x003C23CF) == ("mov", "word ptr [rbp + 0x1c], cx") and
          p.get(0x003C23D3) == ("movzx", "eax, word ptr [rdx + 0x10]") and p.get(0x003C23D7) == ("and", "ax, 3"),
          "kind 0: field id -> row +0x1C, +0x10 & 3 -> row +0x1E")
    check("P3", p.get(0x003C248F) == ("movzx", "edi, byte ptr [rdx + 0x11]") and
          p.get(0x003C2493) == ("movzx", "ebx, byte ptr [rdx + 0x15]") and p.get(0x003C2497) == ("cmp", "dil, 0xd") and
          p.get(0x003C24CE) == ("call", "0x3be700") and p.get(0x003C24E6) == ("movzx", "eax, byte ptr [r15 + 0x10]") and
          p.get(0x003C24F7) == ("movzx", "ecx, word ptr [r15 + 0x12]") and p.get(0x003C250D) == ("or", "dword ptr [rbp + 0x1c], 1") and
          p.get(0x003C253F) == ("call", "0x3bdde0"),
          "kind 1: +0x11 kind (0xD -> 0x2F), +0x15 selector, +0x12 gate, link via 003BDDE0")
    arm = [i for i in md.disasm(at(0x003C2320, ext[0x003C2320]), 0x003C2320) if 0x003C248F <= i.address <= 0x003C253F]
    reads_c = [i.address for i in arm for op in i.operands
               if op.type == R.X86_OP_MEM and op.mem.base in (R.X86_REG_RDX, R.X86_REG_R15) and op.mem.disp == 0xC]
    reads_ctl = [i.address for i in arm for op in i.operands
                 if op.type == R.X86_OP_MEM and op.mem.base in (R.X86_REG_RDX, R.X86_REG_R15) and op.mem.disp == 0x12]
    check("P4", not reads_c and reads_ctl == [0x003C24F7],
          "kind-1 arm reads of +0x0C: %s (control: +0x12 found at %s)" % (reads_c, ["%08X" % a for a in reads_ctl]))
    q = body(0x003C1680)
    check("P5", q.get(0x003C1765) == ("xor", "r8d, r8d") and q.get(0x003C178A) == ("mov", "r8d, 1") and
          q.get(0x003C179D) == ("test", "r8d, r8d") and q.get(0x003C17A0) == ("jne", "0x3c17b6") and
          q.get(0x003C17A2) == ("movzx", "ecx, word ptr [rcx + 0xc]") and q.get(0x003C17A6) == ("call", "0x3c17e0"),
          "003C1680: +0x0C -> 003C17E0 for kind 0 only")
    return 0 if all(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
