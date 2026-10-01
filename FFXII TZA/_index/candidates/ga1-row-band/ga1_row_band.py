"""GA-1 follow-up: the status_data.bin row's +0x0A word, its +0x24 flags, and the +0x11..+0x1D band (OPUS, 2026-09-27).
Static reads of the shipping image plus the status table ASTRA retained (status-row-key-qualification/status-table.bin).

  B1 the query filler's status arm (0031C5D0) resolves the row's +0x0A word through 002F9860 into record +0x10
     (0031E288-0031E291); 002F9860 is a text resolver: bank = id / 1000 (0x10624DD3 multiply, sar 6), fewer than 28
     banks, entry = id - 1000*bank, the empty string 01CEB638 otherwise
  B2 the same arm packs the row's +0x06 bit 13 into record +0x25 bit 0 and the row's +0x24 bits 0..3 into record +0x25
     bits 1..4 (0031E295-0031E2E2)
  B3 DATA: +0x11, +0x12 and +0x14..+0x1D are twelve sparse columns - each byte is 0xFF in most rows and otherwise one
     of 25..31, the present values in a column distinct and counting down from 31 (a ranking), none equal to the row's
     +0x10 key (so NOT the listing-key family of +0x02 / +0x10 / +0x13 / +0x26 / +0x27); +0x1E / +0x1F are 0xFF in all
  B4 NO READER on the routes this probe has: none of the 18 functions that reference the class-26 slot 02EBF118 reads
     a row byte in +0x11..+0x1D other than +0x13, by displacement or by index, and the query arm copies only the five
     keys into its record, so no consumer reaches the band through the record
Not claimed: what the rankings rank; a reader that resolves class 26 through the generic encoded-id registry without
naming the slot.
"""
import re, struct, sys, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

Q = ins(0x31C5D0, sizes[0x31C5D0])
T = ins(0x2F9860, sizes[0x2F9860])
check("B1 +0x0A word -> 002F9860 (a text resolver: id / 1000 bank, < 28 banks) -> record +0x10",
      Q.get(0x31E288) == "movzx ecx, word ptr [rsi + 0xa]" and Q.get(0x31E28C) == "call 0x2f9860"
      and Q.get(0x31E291) == "mov qword ptr [rbx + 0x10], rax"
      and T.get(0x2F9866) == "mov eax, 0x10624dd3" and T.get(0x2F986F) == "sar edx, 6" and T.get(0x2F9879) == "cmp edx, 0x1c"
      and T.get(0x2F98A8) == "imul eax, edx, 0xfffffc18")
check("B2 +0x06 bit 13 -> record +0x25 bit 0; +0x24 bits 0..3 -> record +0x25 bits 1..4",
      Q.get(0x31E295) == "movzx eax, word ptr [rbp + 6]" and Q.get(0x31E299) == "shr ax, 0xd"
      and all(Q.get(a) == "movzx ecx, byte ptr [rbp + 0x24]" or Q.get(a) == "movzx eax, byte ptr [rbp + 0x24]"
              for a in (0x31E2A5, 0x31E2B7, 0x31E2C6, 0x31E2D6))
      and [Q.get(a) for a in (0x31E2AE, 0x31E2BF, 0x31E2CE, 0x31E2DE)] == ["and cl, 2", "and al, 4", "and cl, 8", "and al, 0x10"])

t = (DB / "_experiments/evidence/status-row-key-qualification/status-table.bin").read_bytes()
rows = [t[0x20 + i * 40:0x20 + (i + 1) * 40] for i in range(32)]
band = [0x11, 0x12] + list(range(0x14, 0x1E))
ok = True
for o in band:
    pres = [r[o] for r in rows if r[o] != 0xFF]
    ok &= 0 < len(pres) < 16 and all(25 <= v <= 31 for v in pres) and len(set(pres)) == len(pres) and max(pres) == 31
    ok &= all(r[o] != r[0x10] for r in rows if r[o] != 0xFF)
ok &= all(r[0x1E] == 0xFF and r[0x1F] == 0xFF for r in rows)
check("B3 DATA: twelve sparse ranking columns (distinct values from 31 down, else 0xFF), not the +0x10 key family", ok)

SLOT = 0x2EBF118
ref = set()
for ch, vs, va, rs, ro in SECS:
    if ch & 0x20000000:
        for p in range(ro, ro + rs - 4):
            v = BASE + va + p - ro
            if v + 4 + struct.unpack_from("<i", d, p)[0] == SLOT:
                k = bisect.bisect_right(keys, v) - 1
                if k >= 0 and v < keys[k] + sizes[keys[k]]: ref.add(keys[k])
# Receiver-typed: a status row is formed as base(0020E600 of the slot's +0xC) + word[slot +8] * id - the idiom every
# slot user shares (e.g. 0031E1C3-0031E1D2: mov rcx,[slot] / movzx edx, word [rcx+8] / imul edx, .. / add eax, edx).
# The register the closing `add` writes is the row; it is followed with its copies, and every row byte it reads is
# collected. POSITIVE CONTROL: the query arm's +0x13 / +0x26 / +0x27 reads must be among them.
M = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
def fam(r):
    mm = re.match(r"(r\d+)[dwb]?$", r); return M.get(r, mm.group(1) if mm else r)
seen_disp = {}; rows_formed = 0
for f in ref:
    body = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    for i, x in enumerate(body):
        m = re.match(r"mov (\w+), qword ptr \[rip \+ 0x([0-9a-f]+)\]", "%s %s" % (x.mnemonic, x.op_str))
        if not (m and x.address + x.size + int(m.group(2), 16) == SLOT): continue
        slotreg = fam(m.group(1)); k = None
        for j in range(i + 1, min(i + 8, len(body))):
            if re.match(r"movzx \w+, word ptr \[%s \+ 8\]" % slotreg, "%s %s" % (body[j].mnemonic, body[j].op_str)): k = j; break
        if k is None: continue
        row = None
        for j in range(k + 1, min(k + 6, len(body))):
            if body[j].mnemonic == "add":
                row = fam(body[j].op_str.split(",")[0]); start = j + 1; break
        if row is None: continue
        rows_formed += 1; regs = {row}
        at = {z.address: q for q, z in enumerate(body)}
        path = []; q = start
        while q < len(body) and len(path) < 50:          # one path: fall through conditionals, follow unconditional jmps
            z = body[q]; path.append(z)
            if z.mnemonic == "jmp" and re.fullmatch(r"0x[0-9a-f]+", z.op_str) and int(z.op_str, 16) in at:
                q = at[int(z.op_str, 16)]
            else:
                q += 1
        for y in path:
            s = "%s %s" % (y.mnemonic, y.op_str)
            for r in list(regs):
                for mm in re.finditer(r"(byte|word|dword|qword) ptr \[%s \+ 0x([0-9a-f]+)\]" % r, y.op_str):
                    seen_disp.setdefault(int(mm.group(2), 16), set()).add("%08X %s" % (y.address, s))
            mm = re.match(r"mov (\w+), (\w+)$", s)
            if mm and fam(mm.group(2)) in regs: regs.add(fam(mm.group(1)))
            elif y.mnemonic in ("mov", "movzx", "lea", "add", "sub", "imul", "xor", "pop") and y.op_str and fam(y.op_str.split(",")[0]) in regs \
                    and not y.op_str.split(",")[0].startswith(("byte", "word", "dword", "qword")):
                regs.discard(fam(y.op_str.split(",")[0]))
            if y.mnemonic in ("call", "ret") and not regs & {"rbx", "rbp", "rsi", "rdi", "r12", "r13", "r14", "r15"}: break
            if y.mnemonic == "call": regs -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
band_hits = {o: sorted(seen_disp[o])[:2] for o in band if o in seen_disp}
check("B4 receiver-typed: %d status rows formed across the %d slot users; the arm's key reads are found, and no row"
      " byte in +0x11..+0x1D other than +0x13 is read" % (rows_formed, len(ref)),
      len(ref) >= 15 and rows_formed >= 10 and all(o in seen_disp for o in (0x13, 0x26, 0x27)) and not band_hits,
      "control %s; band %s" % (sorted(hex(o) for o in (0x13, 0x26, 0x27) if o in seen_disp), band_hits))
print("FAILS", fails)
sys.exit(1 if fails else 0)
