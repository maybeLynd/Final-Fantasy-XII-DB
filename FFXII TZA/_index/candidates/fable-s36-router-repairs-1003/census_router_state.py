"""census_router_state.py - FABLE, 2026-10-03, for SWE2-AUDIT-SEM's S-36 D2.

Writers and readers of the UI request router's state cells, from the certified image:

  0215F1A0 u8       mailbox pending byte
  0215F1A1 u8       mailbox blocked byte
  0215F1A2, 0215F1A3  the two bytes between the blocked byte and the id (measured, so the record's extent is honest)
  0215F1A4 u32      mailbox request id
  0215F1A8 u32      mailbox parameter
  020927D8 u32      request-id copy written by 00252B40
  01E0C2C0 u32[22]  the inhibit table (aggregate bit -> request-id mask)

Bodies decoded: every .pdata RUNTIME_FUNCTION (chained entries attributed to their root), PLUS every function in the
catalogue (Tools/work/graph/functions.tsv) whose entry no .pdata entry covers - leaf functions have no unwind data,
and four of the mailbox's own accessors are such leaves. A catalogue body is decoded to its body_bytes.

  P1  every RIP-relative memory operand or LEA whose [target, target+width) overlaps a cell, with its access kind from
      capstone's operand access flags (W, R, RW) or A (address formed by LEA).
  P2  image-base-relative forms: a non-RIP memory operand whose disp, as an RVA, overlaps a cell's RVA range (the
      [reg+RVA] form with reg = 00120000), and any disp equal to a cell VA.
  P3  raw rel32 sweep of the whole of .text: every 4-byte window whose disp32, as RIP-relative for an instruction ending
      0/1/2/4 bytes after it, lands in a cell. Each window is re-decoded from 1..15 bytes back; a decode whose start is a
      known instruction boundary is preferred, else the longest; the hit is CONFIRMED when that instruction's rip target
      is the cell. Confirmed hits at no decoded instruction boundary are UNLISTED code.
  P4  raw constants: every dword equal to a cell RVA or VA and every qword equal to a cell VA, in .text/.rdata/.data.
  P5  displaced anchors: every RIP-relative LEA that forms an address within 0x100 bytes of a cell (overlapping it or
      not) is followed forward through its body (to an overwrite of the register, a ret or an unconditional jmp; add/sub
      of an immediate move the anchor). A [reg+disp] that lands on a cell is a DISPLACED access; a [reg+index*s+disp]
      is listed as INDEXED and must carry a disposition below (read from the bytes by FABLE, 2026-10-03), or C5 fails.

Controls (each must hold or the census measured nothing):
  C1  the leaf writer 00252B4C (020927D8, no .pdata) is found by P1 through the catalogue;
  C2  the drain reader 002E0D05 (0215F1A4) is found by P1;
  C3  P3 re-finds every P1 RIP-relative site (the raw sweep is not blind);
  C4  P5 finds the router's table walk: its anchor 00254B88 reaches the table at [rcx-4] (00254BA5) as DISPLACED.

Prints FAILS N last.
"""
import bisect
import collections
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
from capstone import CS_AC_READ, CS_AC_WRITE  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP, X86_REG_INVALID  # noqa: E402
import numpy as np  # noqa: E402

img = Img.load()
img.cs.detail = True
BASE = img.base
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")

CELLS = [  # (va, width, name)
    (0x0215F1A0, 1, "mailbox.pending"),
    (0x0215F1A1, 1, "mailbox.blocked"),
    (0x0215F1A2, 1, "byte 0215F1A2"),
    (0x0215F1A3, 1, "byte 0215F1A3"),
    (0x0215F1A4, 4, "mailbox.id"),
    (0x0215F1A8, 4, "mailbox.parameter"),
    (0x020927D8, 4, "requestIdCopy"),
    (0x01E0C2C0, 88, "inhibitTable[22]"),
]
NAMES = {va: nm for va, cw, nm in CELLS}
# Dispositions of the INDEXED anchors, each read at the bytes (FABLE, 2026-10-03).
DISPOSITION = {
    0x00250270: "02092764 + r10*8 dword: lands on 020927D4 or 020927DC, never on 020927D8 (8-byte stride, +4 phase)",
    0x00252FF0: "02092764 + rax*8 dword: same phase argument as 00250270; never overlaps 020927D8",
    0x00252E60: "02092760 + rax*8: index forced to 0 unless ecx <= 0xB unsigned (00252E7C jbe); last element 020927B8",
    0x00252F40: "02092760 + rax*8: 00252F44 cmp ecx, 0xB; jbe, else 0; last element 020927B8",
    0x002530E0: "02092760 + rax*8: 0025310C cmp ecx, 0xB; jbe, else esi, which is 0 (002530FE xor esi, esi)",
    0x002534C0: "02092760 + rax*8: 002534D9 cmp ecx, 0xB; jbe, else 0",
    0x002535D0: "02092760 + rax*8: 002535F2 cmp ecx, 0xB; jbe, else 0",
    0x00286D60: "anchor 01E0C3F0 is above the table; the tracked use is a loop-alignment nop, not an access",
    0x002E0FA0: "0215F1D0 anchor: the aggregate's 16-byte reads span 0215F1C0..0215F20F, above the mailbox (0215F1AC end)",
    0x002E1020: "0215F1C0 + rax*4 with NO bound; callers 002283E2 (ebx = 1 at 00228396), 00228972 (ebx 0..15, "
                "00228982), 00229B12 (ecx = 1): no negative row reaches the mailbox",
    0x002E1C20: "0215F1C0 + rax*4, upper bound only (cmp ecx, 0x10; jge). A row must be <= -6 to reach the mailbox "
                "(0215F1C0 - 6*4 = 0215F1A8). The 38 raw call sites set ecx by a constant, xor, 00229510's loop counter "
                "esi 0..15 (00229576), or lea ecx, [reg +- k]; the lea bases were not all traced to constants "
                "(0022974E rsi, 0035D6B0 rax/rdi): bounded by reading for the constant forms only",
    0x002E1CA0: "same shape and same caveat as 002E1C20 over its 39 raw call sites",
    0x002E1CD0: "0215F1C0 + rax*4 indexed by edx, upper bound only. The 19 raw call sites pass edx = 0, 3, 6 or 0xD; the "
                "three 'or edx, -1' hits of a linear trace are the other arm of a je whose target re-enters with edx = 6 "
                "(002636A7, 0026C552, 0026C7FD), and 0025D41A passes r15d = sbb/and 3, so 0 or 3 (0025D271, 0025D274)",
}
fails = 0


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))


def cells_hit(t, w):
    return [(va, cw, nm) for va, cw, nm in CELLS if t < va + cw and t + max(w, 1) > va]


def sec(name):
    return next(s for s in img.secs if s[0] == name)


text_s = sec(".text")
TLO, THI = BASE + text_s[1], BASE + text_s[1] + text_s[4]

# ---- .pdata entries, root-attributed ----
po = img.off(BASE + img.exc_rva)
raw = []
for i in range(img.exc_size // 12):
    b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
    if not b:
        continue
    ui = img.off(BASE + u)
    fl = img.d[ui] >> 3
    n = img.d[ui + 2]
    root = BASE + b
    if fl & 4:
        co = ui + 4 + ((n + 1) & ~1) * 2
        root = struct.unpack_from("<I", img.d, co)[0] + BASE
    raw.append((BASE + b, BASE + e, root))
link = {b: r for b, e, r in raw}


def final_root(r):
    k = 0
    while r in link and link[r] != r and k < 16:
        r = link[r]
        k += 1
    return r


ranges = sorted((b, e, final_root(r), "pdata") for b, e, r in raw)
starts = [r[0] for r in ranges]


def pdata_cover(va):
    i = bisect.bisect_right(starts, va) - 1
    return i >= 0 and ranges[i][0] <= va < ranges[i][1]


# ---- catalogue leaves with no .pdata entry ----
ncat = 0
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if not i or len(p) < 3:
        continue
    try:
        fa, sz = int(p[0], 16), int(p[2])
    except ValueError:
        continue
    if TLO <= fa < THI and sz > 0 and not pdata_cover(fa):
        ranges.append((fa, fa + sz, fa, "catalogue"))
        ncat += 1
ranges.sort()

FAM = {}
for r64, subs in {
        "rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch", "rdx": "edx dx dl dh",
        "rsi": "esi si sil", "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    FAM[r64] = r64
    for s in subs.split():
        FAM[s] = r64
for k in range(8, 16):
    for s in ("r%d" % k, "r%dd" % k, "r%dw" % k, "r%db" % k):
        FAM[s] = "r%d" % k


def fam(x, reg):
    return FAM.get(x.reg_name(reg), x.reg_name(reg))


def kind(x, o):
    if x.mnemonic == "lea":
        return "A"
    k = ("R" if o.access & CS_AC_READ else "") + ("W" if o.access & CS_AC_WRITE else "")
    return k or "?"


P1, P2, P5 = [], [], []
bounds = set()
srcof = {}
lo_all = min(va for va, cw, nm in CELLS)
hi_all = max(va + cw for va, cw, nm in CELLS)
for b, e, root, src in ranges:
    if not (TLO <= b < THI):
        continue
    ins = list(img.cs.disasm(img.read(b, e - b), b))
    for j, x in enumerate(ins):
        bounds.add(x.address)
        for o in x.operands:
            if o.type != X86_OP_MEM:
                continue
            m = o.mem
            if m.base == X86_REG_RIP:
                t = x.address + x.size + m.disp
                hit = cells_hit(t, 1 if x.mnemonic == "lea" else o.size)
                for va, cw, nm in hit:
                    P1.append((va, root, x.address, kind(x, o), o.size, "%s %s" % (x.mnemonic, x.op_str), t, src))
                if (x.mnemonic == "lea" and x.operands[0].type == X86_OP_REG
                        and any(va - 0x100 <= t < va + cw + 0x100 for va, cw, nm in CELLS)):
                    reg = fam(x, x.operands[0].reg)
                    anchor = t
                    for y in ins[j + 1:j + 49]:
                        stop = False
                        for oo in y.operands:
                            if oo.type == X86_OP_MEM and oo.mem.base != X86_REG_INVALID and oo.mem.base != X86_REG_RIP \
                                    and fam(y, oo.mem.base) == reg:
                                tt = anchor + oo.mem.disp
                                if oo.mem.index != X86_REG_INVALID:
                                    P5.append(("INDEXED", root, x.address, y.address, anchor, tt,
                                               "%s %s" % (y.mnemonic, y.op_str), None, kind(y, oo)))
                                else:
                                    for va, cw, nm in cells_hit(tt, 1 if y.mnemonic == "lea" else oo.size):
                                        P5.append(("DISPLACED", root, x.address, y.address, anchor, tt,
                                                   "%s %s" % (y.mnemonic, y.op_str), va, kind(y, oo)))
                        try:
                            _r, w = y.regs_access()
                        except Exception:
                            w = []
                        if any(fam(y, r) == reg for r in w):
                            if y.mnemonic in ("add", "sub") and len(y.operands) == 2 and y.operands[1].type == X86_OP_IMM \
                                    and y.operands[0].type == X86_OP_REG and fam(y, y.operands[0].reg) == reg:
                                anchor += y.operands[1].imm if y.mnemonic == "add" else -y.operands[1].imm
                            else:
                                stop = True
                        if stop or y.mnemonic in ("ret", "jmp"):
                            break
            else:
                d = m.disp & 0xFFFFFFFF
                w = max(o.size, 1)
                for va, cw, nm in CELLS:
                    rva = va - BASE
                    if (m.base != X86_REG_INVALID or m.index != X86_REG_INVALID) and d < rva + cw and d + w > rva:
                        P2.append((va, root, x.address, "base+RVA", "%s %s" % (x.mnemonic, x.op_str)))
                    if d < va + cw and d + w > va:
                        P2.append((va, root, x.address, "VA disp", "%s %s" % (x.mnemonic, x.op_str)))

# ---- P3 raw rel32 sweep over .text ----
tb = img.d[text_s[3]:text_s[3] + text_s[4]]
arr = np.frombuffer(tb, dtype=np.uint8).astype(np.int64)
n4 = len(tb) - 3
dw = arr[0:n4] | (arr[1:n4 + 1] << 8) | (arr[2:n4 + 2] << 16) | (arr[3:n4 + 3] << 24)
dw = np.where(dw >= 2 ** 31, dw - 2 ** 32, dw)
pos = np.arange(n4, dtype=np.int64) + TLO
P3 = []
for k in (0, 1, 2, 4):
    t = pos + 4 + k + dw
    for p in np.nonzero((t >= lo_all) & (t < hi_all))[0]:
        tt = int(t[p])
        if cells_hit(tt, 1):
            P3.append((int(pos[p]), tt))
P3c = {}
for pva, t in P3:
    cands = []
    for back in range(1, 16):
        s = pva - back
        x = next(img.cs.disasm(img.read(s, 16), s), None)
        if x is None or not (x.address < pva and pva + 4 <= x.address + x.size):
            continue
        if any(o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP and x.address + x.size + o.mem.disp == t
               for o in x.operands):
            cands.append(x)
    if not cands:
        continue
    known = [x for x in cands if x.address in bounds]
    x = known[0] if known else max(cands, key=lambda c: c.size)
    P3c[x.address] = (t, "%s %s" % (x.mnemonic, x.op_str), bool(known))

# ---- P4 raw constants ----
P4 = []
for sname in (".text", ".rdata", ".data"):
    s = sec(sname)
    blob = img.d[s[3]:s[3] + s[4]]
    for va, cw, nm in CELLS:
        for val, size in ((va - BASE, 4), (va, 4), (va, 8)):
            pat = struct.pack("<I" if size == 4 else "<Q", val)
            i = blob.find(pat)
            while i >= 0:
                P4.append((va, sname, BASE + s[1] + i, size, "RVA" if val == va - BASE else "VA"))
                i = blob.find(pat, i + 1)

# ---- report ----
print("image 73461d08 (sha256 checked by rvlib); bodies: %d .pdata entries + %d catalogue leaves without .pdata"
      % (len(raw), ncat))
print()
print("P1  RIP-relative operands overlapping a cell")
per = collections.defaultdict(lambda: {"W": set(), "R": set(), "A": set()})
for va, root, site, k, w, txt, t, src in sorted(P1):
    print("  %08X %-18s fn %08X (%s)  site %08X  %-2s w%d  %s  -> %08X" % (va, NAMES[va], root, src, site, k, w, txt, t))
    for c in k:
        if c in "WRA":
            per[va][c].add(root)
print()
print("P2  image-base-relative / VA-displacement forms: %d" % len(P2))
for row in P2:
    print("  %08X fn %08X site %08X %s  %s" % row)
print()
print("P5  displaced anchors (LEA within 0x100 of a cell, followed to the register's next write)")
disp_hits = [r for r in P5 if r[0] == "DISPLACED"]
idx_rows = [r for r in P5 if r[0] == "INDEXED"]
for r in disp_hits:
    print("  DISPLACED fn %08X  anchor %08X -> %08X  use %08X -> %08X  %-2s %s  (cell %08X %s)" % (
        r[1], r[2], r[4], r[3], r[5], r[8], r[6], r[7], NAMES[r[7]]))
    for c in r[8]:
        if c in "WR":
            per[r[7]][c].add(r[1])
for r in idx_rows:
    print("  INDEXED   fn %08X  anchor %08X -> %08X  use %08X  base %08X  %s" % (r[1], r[2], r[4], r[3], r[5], r[6]))
    print("            disposition: %s" % DISPOSITION.get(r[1], "NONE"))
print()
unl = sorted(a for a, v in P3c.items() if not v[2])
print("P3  raw rel32 windows %d; confirmed instructions %d; at no decoded boundary (UNLISTED) %d" % (
    len(P3), len(P3c), len(unl)))
for a in unl:
    print("  UNLISTED %08X -> %08X  %s" % (a, P3c[a][0], P3c[a][1]))
p1sites = {r[2] for r in P1}
missed = sorted(p1sites - set(P3c))
print("  P1 sites the raw sweep did not re-find: %d %s" % (len(missed), ["%08X" % m for m in missed]))
print()
print("P4  raw RVA/VA constants equal to a cell: %d" % len(P4))
for row in P4:
    print("  %08X in %s at %08X (%d-byte %s)" % row)
print()
print("SUMMARY (functions per cell; R includes reads through a displaced anchor)")
for va, cw, nm in CELLS:
    d = per[va]
    print("  %08X w%-2d %-18s writers %d %s | readers %d %s | address-formed %d %s" % (
        va, cw, nm, len(d["W"]), sorted("%08X" % f for f in d["W"]), len(d["R"]), sorted("%08X" % f for f in d["R"]),
        len(d["A"]), sorted("%08X" % f for f in d["A"])))
print()
sites = {(r[0], r[2]) for r in P1}
check("C1", (0x020927D8, 0x00252B4C) in sites, "the leaf writer 00252B4C of 020927D8 is found through the catalogue")
check("C2", (0x0215F1A4, 0x002E0D05) in sites, "the drain reader 002E0D05 of 0215F1A4 is found")
check("C3", not missed and not unl, "the raw sweep re-finds every P1 site and finds no unlisted code")
check("C4", any(r[2] == 0x00254B88 and r[3] == 0x00254BA5 for r in disp_hits),
      "the router's anchor 00254B88 reaches the table at 00254BA5 ([rcx-4]) as DISPLACED")
check("C5", all(r[1] in DISPOSITION for r in idx_rows), "every INDEXED anchor has a disposition read at the bytes")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
