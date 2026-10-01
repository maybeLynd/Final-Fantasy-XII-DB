"""chse_slot3.py - what reads a CHSE record's slot 3 (row +6), and what it becomes. SWE2-CONTRACT, 2026-09-30.
Static, from the shipping EXE, plus the shipped in/common/charseinfo_*.bin tables. Reads only.

Usage: python chse_slot3.py

Checks (each prints PASS/FAIL; exit 0 only if all pass):
  T1  the only code that reads the eight table pointers 021641A8..021641E0 is 002ED950 (rip census; the loader 002EA530
      takes the base with one lea) - control: the census re-finds the loader's lea at 002EA54E.
  T2  002ED950 returns row = table + 16*(idx+1) (a 0-based row after the 16-byte header), bounded by the table's +8 count.
  T3  every direct call or jump to 002ED950 in every listed body: exactly 002E60F0, 002EA6E0, 002ED910 - control: the
      scan re-finds 002E60F0's call at 002E6152.
  T4  what each caller reads from the row: 002E60F0 a u16 at +2*pass (slots 0-2, the SE ids); 002EA6E0 nothing (only
      the null test); 002ED910 a signed word at +6 - slot 3.
  T5  002ED910 order: 003212E0(actor) first; the slot-3 word only when there is no actor or 003212E0 returns negative.
  T6  003212E0: -1 unless the actor's record at +0x698 has byte +5 == 1, then the signed word +0x26 of [actor+0xE60].
  T7  the party read-in state machine 0037B4D0 calls 002ED910 at 0037B85B; a negative result goes to state 7
      (0037B864 -> 0037B86A); otherwise the result is the key (edx) of 0036F0F0 at 0037B896, the voice-pack
      find-or-evict (the-party-read-in-state-machine.md, row 4).
  T8  the id the step passes is 002EB7A0(0031C250(actor)) - the actor's definition key (0037B824 -> 0037B82B).
      002EB7A0 remaps the special ids 0-1 -> 0x630000 ('c' row 0), 8-9 -> 0x6E0001 ('n' row 1), 12-13 -> 0x770002
      ('w' row 2) - the empty-slot resources (the-party-read-in-state-machine.md) - and passes every other id through
      unchanged (ids above 13 by the ja, so a model id keeps its letter and names its own row). Any row is therefore
      reachable by an actor whose definition key names it; this check does not bound which keys ship.
      (Corrected before publication: a first draft of this check read the pass-through as "no letter".)
  T9  every direct call or jump to 002ED910 in every listed body: only 0037B4D0 (the same raw scan as T3).
  T10 whole-image negative for T3/T9, outside functions.tsv: every E8/E9 rel32 in every executable section whose
      target is 002ED950 or 002ED910, and every aligned qword (VA) or dword (RVA) in any section equal to either.
      Control: the raw scan re-finds 002E6152 (call 002ED950) and 0037B85B (call 002ED910). Hits must all lie inside
      the T3/T9 callers; no data reference (no function-pointer use) may exist outside .pdata, whose RUNTIME_FUNCTION
      begin-RVA for 002ED910 is exception metadata, not a pointer (it is counted and printed, not treated as a use).
  T11 the header: the loader 002EA530 makes no memory access through the buffer register (rdi) - it passes the
      buffer to the file read 0032E620 and the allocator tagger 0036C660 - and 002ED950's only access through the
      table pointer (rcx) is [rcx + 8], the count. With T1 (no other code takes the table pointers), header +0x04
      (version), +0x06 (letter) and +0x0C are read by no code that reaches the tables. Control: the same operand
      filter finds 002ED950's [rcx + 8].
  D1  the shipped slot-3 values of the three empty-slot rows (in/common; ch copies are byte-identical per
      chse_se_index_check.py).
  D2  the authored (non-0xFFFF) slot-3 values per table, read as 002ED910 reads them (signed word).
"""
import os
import struct
import sys

import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import block_writer_disjoint as b  # noqa: E402
import rip_refs  # noqa: E402

CHSE = r"D:\FFXII_TZA_extract\ps2data\image\ff12\in\common"
RES = []


def check(tag, ok, text):
    RES.append(ok)
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def dis(md, at, ext, f):
    return list(md.disasm(at(f, ext[f]), f))


def main():
    at, ext = b.load(), b.extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True

    hits = rip_refs.scan(0x021641A0, 0x021641E8)
    readers = sorted({fn for fn, a, k, m, o, t in hits})
    ctl = any(a == 0x002EA54E and k == "lea" for fn, a, k, m, o, t in hits)
    check("T1", ctl and readers == [0x002EA530, 0x002ED950] and
          sum(1 for h in hits if h[0] == 0x002ED950) == 8,
          "table readers %s; loader lea control %s" % ([("%08X" % r) for r in readers], ctl))

    t = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x002ED950)}
    check("T2", t.get(0x002ED9C2) == ("cmp", "edx, dword ptr [rcx + 8]") and
          t.get(0x002ED9C7) == ("lea", "rax, [rdx + 1]") and t.get(0x002ED9CB) == ("shl", "rax, 4"),
          "bound +8, row = (idx+1)<<4")

    callers, seen_ctl = set(), False
    for entry, size in sorted(ext.items()):
        code = at(entry, size)
        if not code:
            continue
        for i in md.disasm(code, entry):
            if i.mnemonic in ("call", "jmp") and i.op_str == "0x2ed950":
                callers.add(entry)
                seen_ctl |= i.address == 0x002E6152
    check("T3", seen_ctl and callers == {0x002E60F0, 0x002EA6E0, 0x002ED910},
          "callers %s; control 002E6152 %s" % (sorted("%08X" % c for c in callers), seen_ctl))

    e = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x002E60F0)}
    a = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x002EA6E0)}
    n = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x002ED910)}
    rax_reads_6a = [v for k, v in a.items() if "[rax +" in v[1] and k > 0x002EA701 and k < 0x002EA70B]
    check("T4", e.get(0x002E6131) == ("lea", "r13, [rax + rax]") and
          e.get(0x002E6157) == ("movzx", "ecx, word ptr [rax + r13]") and
          a.get(0x002EA706) == ("test", "rax, rax") and a.get(0x002EA70B, ("", ""))[0] == "call" and
          not rax_reads_6a and
          n.get(0x002ED939) == ("movsx", "eax, word ptr [rax + 6]"),
          "002E60F0 word [row + 2*pass]; 002EA6E0 null test only; 002ED910 movsx word [row + 6]")

    check("T5", n.get(0x002ED921) == ("call", "0x3212e0") and n.get(0x002ED92B) == ("jns", "0x2ed946") and
          n.get(0x002ED91F) == ("je", "0x2ed92d") and n.get(0x002ED92F) == ("call", "0x2ed950"),
          "003212E0 first; the row only on null actor or a negative result")

    u = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x003212E0)}
    check("T6", u.get(0x003212FF) == ("cmp", "byte ptr [rcx + 5], 1") and
          u.get(0x00321305) == ("mov", "rax, qword ptr [rax + 0xe60]") and
          u.get(0x0032130C) == ("movsx", "eax, word ptr [rax + 0x26]") and
          u.get(0x00321315) == ("or", "eax, 0xffffffff"),
          "[+0x698]+5 == 1 -> word [[+0xE60]+0x26], else -1")

    s = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x0037B4D0)}
    check("T7", s.get(0x0037B82B) == ("call", "0x2eb7a0") and s.get(0x0037B85B) == ("call", "0x2ed910") and
          s.get(0x0037B860) == ("mov", "edi, eax") and s.get(0x0037B864) == ("jns", "0x37b873") and
          s.get(0x0037B86A) == ("or", "byte ptr [rsi + 8], 7") and s.get(0x0037B891) == ("mov", "edx, edi") and
          s.get(0x0037B896) == ("call", "0x36f0f0"),
          "0037B85B -> edi -> edx of 0036F0F0 at 0037B896; negative -> state 7")

    base = 0x120000
    tbl = at(base + 0x1CB7D4, 14 * 4)
    arms = [base + struct.unpack_from("<i", tbl, 4 * k)[0] for k in range(14)]
    r = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x002EB7A0)}
    ids = {0x002EB7BC: 0x630000, 0x002EB7C4: 0x6E0001, 0x002EB7CC: 0x770002}
    arm_ok = all(r.get(k) == ("mov", "ecx, 0x%x" % v) for k, v in ids.items()) and r.get(0x002EB7D1) == ("mov", "eax, ecx")
    want = {0: 0x002EB7BC, 1: 0x002EB7BC, 8: 0x002EB7C4, 9: 0x002EB7C4, 12: 0x002EB7CC, 13: 0x002EB7CC}
    map_ok = all(arms[k] == want.get(k, 0x002EB7D1) for k in range(14))
    s4 = {i.address: (i.mnemonic, i.op_str) for i in dis(md, at, ext, 0x0037B4D0)}
    key_ok = s4.get(0x0037B824) == ("call", "0x31c250") and s4.get(0x0037B829) == ("mov", "ecx, eax")
    pass_ok = r.get(0x002EB7A0) == ("cmp", "ecx, 0xd") and r.get(0x002EB7A3) == ("ja", "0x2eb7d1")
    check("T8", arm_ok and map_ok and key_ok and pass_ok,
          "input 0031C250(actor) %s; ids above 13 pass through %s; special ids %s" % (
              key_ok, pass_ok, ["%d->%X" % (k, arms[k]) for k in range(14)]))

    def mem_via(f, reg):
        out = []
        for i in dis(md, at, ext, f):
            for op in i.operands:
                if op.type == capstone.x86.X86_OP_MEM and op.mem.base == reg:
                    out.append((i.address, i.mnemonic, i.op_str))
        return out
    ld = mem_via(0x002EA530, capstone.x86.X86_REG_RDI)
    rd = mem_via(0x002ED950, capstone.x86.X86_REG_RCX)
    check("T11", not ld and [x[2] for x in rd] == ["edx, dword ptr [rcx + 8]"],
          "loader accesses via rdi %s; 002ED950 accesses via rcx %s" % (ld, rd))

    c9 = set()
    for entry, size in sorted(ext.items()):
        code = at(entry, size)
        if not code:
            continue
        for i in md.disasm(code, entry):
            if i.mnemonic in ("call", "jmp") and i.op_str == "0x2ed910":
                c9.add(entry)
    check("T9", c9 == {0x0037B4D0}, "callers of 002ED910 %s" % sorted("%08X" % c for c in c9))

    exe = open(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
    pe = struct.unpack_from("<I", exe, 0x3C)[0]
    nsec = struct.unpack_from("<H", exe, pe + 6)[0]
    opt = struct.unpack_from("<H", exe, pe + 20)[0]
    tgt = {0x002ED950, 0x002ED910}
    raw_calls, data_refs, pdata = [], [], []
    for k in range(nsec):
        o = pe + 24 + opt + 40 * k
        vs, va, rs, ro = struct.unpack_from("<IIII", exe, o + 8)
        ch = struct.unpack_from("<I", exe, o + 36)[0]
        sec = exe[ro:ro + rs]
        name = exe[o:o + 8].rstrip(bytes(1))
        if ch & 0x20000000:
            for j in range(len(sec) - 5):
                if sec[j] in (0xE8, 0xE9):
                    t = base + va + j + 5 + struct.unpack_from("<i", sec, j + 1)[0]
                    if t in tgt:
                        raw_calls.append((base + va + j, t))
        for j in range(0, len(sec) - 8, 4):
            dq = struct.unpack_from("<Q", sec, j)[0]
            dd = struct.unpack_from("<I", sec, j)[0]
            if dq in tgt or (dd + base) in tgt:
                (pdata if name == b".pdata" else data_refs).append((base + va + j, dq, dd))
    inside = lambda a: any(f <= a < f + ext[f] for f in (0x002E60F0, 0x002EA6E0, 0x002ED910, 0x0037B4D0))
    ctl10 = (0x002E6152, 0x002ED950) in raw_calls and (0x0037B85B, 0x002ED910) in raw_calls
    check("T10", ctl10 and all(inside(a) for a, t in raw_calls) and not data_refs,
          "raw E8/E9 hits %d, all inside the known callers %s; data references %d (.pdata entries %d); controls %s" % (
              len(raw_calls), all(inside(a) for a, t in raw_calls), len(data_refs), len(pdata), ctl10))

    rows = {"c": 0, "n": 1, "w": 2}
    vals = {}
    for letter, row in rows.items():
        d = open(os.path.join(CHSE, "charseinfo_%s.bin" % letter), "rb").read()
        assert d[:4] == b"CHSE" and struct.unpack_from("<I", d, 8)[0] > row
        vals[letter] = struct.unpack_from("<4H", d, 16 + 16 * row)
    for letter, v in vals.items():
        print("D1  charseinfo_%s row %d slots %s -> slot 3 as read (movsx) = %d" % (
            letter, rows[letter], ["0x%04X" % x for x in v], struct.unpack("<h", struct.pack("<H", v[3]))[0]))
    import glob
    per = {}
    for fn in sorted(glob.glob(os.path.join(CHSE, "charseinfo_*.bin"))):
        d = open(fn, "rb").read()
        letter = os.path.basename(fn)[11]
        for k in range(struct.unpack_from("<I", d, 8)[0]):
            v = struct.unpack_from("<h", d, 16 + 16 * k + 6)[0]
            if v != -1:
                per.setdefault(letter, []).append(v)
    print("D2  authored slot-3 values (signed, as read): %d in total" % sum(len(v) for v in per.values()))
    for letter, v in sorted(per.items()):
        print("D2  charseinfo_%s: %d values, range %d..%d, distinct %d" % (letter, len(v), min(v), max(v), len(set(v))))
    return 0 if all(RES) else 1


if __name__ == "__main__":
    sys.exit(main())
