"""NavGridParams consumers follow the builder 003924B0 (OPUS, 2026-09-27), consuming ASTRA's
_experiments/evidence/nav-grid-quantization (d0faaa923; its check.py PASS), re-read here by a non-author from the bytes.
  B1 003924CB stores 0x24 to 02AEE0B8 (cellBitsetBytes) BEFORE the call to the rectangle getter 00383740 (003924E4), and
     a zero return skips the rest (003924EB je): "no-op if the getter returns zero" holds after that store, not for it
  B2 the stores name the fields: 02AEE070 / 02AEE078 origins (from the getter's minima), 02AEE080 / 02AEE088 maxima,
     02AEE090 the cell size = floorf(refined) + 1.0 (call 00861F86, then addss [01CEBBA8] = 1.0)
  B3 budget = (0x2800 - [02AEE0B8]) / ([02AEE0B8] + 1) (003924F9-00392546), sqrtf at 00392587
  S  REGRESSION: the corridor contract's nav-grid row no longer calls 070 the cell size or 078 / 080 eps cells, and the
     NavGridParams ctor cell carries the qualification (FAILS before)
Not claimed: loaded map values, the imported math implementation, allocator lifetime; ASTRA's 100x100 / 336x320 rows are
conditional arithmetic, not execution.
"""
import os, re, struct, sys, math
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
d = open(os.path.join(os.path.dirname(DB), "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
X = {x.address: x for x in cs.disasm(d[off(0x3924B0):off(0x3924B0) + 607], 0x3924B0)}
def rip(a):
    x = X[a]; m = re.search(r"rip \+ (0x[0-9a-f]+)\]", x.op_str); return x.address + x.size + int(m.group(1), 16)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
check("B1 the 0x24 store precedes the getter; a zero return skips the rest",
      X[0x3924CB].op_str.endswith(", 0x24") and rip(0x3924CB) == 0x2AEE0B8 and X[0x3924E4].op_str == "0x383740"
      and X[0x3924EB].mnemonic == "je")
roles = {rip(0x392590): X[0x392590].op_str.split(", ")[1], rip(0x3925A0): X[0x3925A0].op_str.split(", ")[1],
         rip(0x3925B1): X[0x3925B1].op_str.split(", ")[1], rip(0x3925C1): X[0x3925C1].op_str.split(", ")[1],
         rip(0x392627): X[0x392627].op_str.split(", ")[1]}
check("B2 070 / 078 origins, 080 / 088 maxima, 090 cell size = floorf + 1.0",
      roles == {0x2AEE070: "xmm6", 0x2AEE078: "xmm8", 0x2AEE080: "xmm7", 0x2AEE088: "xmm9", 0x2AEE090: "xmm0"}
      and X[0x39251F].op_str == "xmm6, dword ptr [rsp + 0x20]" and X[0x392530].op_str == "xmm7, dword ptr [rsp + 0x30]"
      and X[0x392607].op_str == "0x861f86" and rip(0x39260C) == 0x1CEBBA8
      and struct.unpack_from("<f", d, off(0x1CEBBA8))[0] == 1.0, str({hex(k): v for k, v in roles.items()}))
check("B3 budget from 0x2800 and the stored 0x24; sqrtf", X[0x3924F9].op_str == "eax, 0x2800" and X[0x392546].op_str == "edi"
      and X[0x392587].op_str == "0x861f14")
page = open(os.path.join(DB, "06-Movement-And-Navigation", "CONTRACT-corridor-query-family.md"), encoding="utf-8").read()
row = next((l for l in page.splitlines() if l.startswith("| the nav-grid BSS block |")), "")
live = re.sub(r"~~.*?~~", "", row)
tt = [l for l in open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8") if l.startswith("NavGridParams\t")]
check("S the contract row and the types ctor cell follow the builder",
      "`0x2AEE070` cell size" not in live and "eps cells" not in live and "`0x2AEE090` cell size" in live
      and len(tt) == 1 and "QUALIFIED 2026-09-27 (OPUS)" in tt[0] and "floorf" in tt[0])

# ---- part 2 (OPUS, 2026-09-27): ASTRA authored-grid-shape (09e941af2) and nav-upper-bound-admission (bff8d55d0)
def f32(x): return struct.unpack("<f", struct.pack("<f", x))[0]
G = {x.address: x for x in cs.disasm(d[off(0x383740):off(0x383740) + 252], 0x383740)}
check("G the getter 00383740 reads the header as u8 sizes/counts and s16 origins; maxima = origin + count * size",
      G[0x38377E].op_str == "ecx, word ptr [rax + 4]" and G[0x38379C].op_str == "ecx, word ptr [rax + 6]"
      and G[0x3837BA].op_str == "ebx, byte ptr [rax + 2]" and G[0x3837CD].op_str == "ecx, byte ptr [rax]"
      and G[0x3837F2].op_str == "ebx, byte ptr [rax + 3]" and G[0x383805].op_str == "ecx, byte ptr [rax + 1]"
      and G[0x383771].op_str == "ecx, dword ptr [rax + 0x20]")
slot = open(os.path.join(DB, "_experiments", "evidence", "authored-grid-shape", "slot4.bin"), "rb").read()
h = slot[struct.unpack_from("<I", slot, 0x20)[0]:][:8]
cw, ch, nc, nr = h[0], h[1], h[2], h[3]; ox, oz = struct.unpack_from("<hh", h, 4)
w = f32(f32(f32(nc * cw) + ox) - ox); hh = f32(f32(f32(nr * ch) + oz) - oz)
budget = (0x2800 - 0x24) // 0x25; c0 = f32(math.sqrt(f32(f32(w * hh) / budget)))
nx, nz = int(f32(w / c0)), int(f32(hh / c0)); ref = max(f32(w / nx), f32(hh / nz))
def shape(cell): return int(f32(f32(f32(w + cell) - 1.0) / cell)), int(f32(f32(f32(hh + cell) - 1.0) / cell))
good = shape(f32(math.floor(ref) + 1.0)); bad = shape(f32(ref + 1.0))
check("A the authored alc0102 slot-4 header gives 13 x 13 / 6289 under floor-plus-one; the no-floor reading disagrees",
      bytes(h) == bytes.fromhex("05050a0a3f000d00") and budget == 275 and good == (13, 13) and good[0] * good[1] * 0x25 + 0x24 == 6289
      and bad == (12, 12), "c0 %.7f refined %s floor %s no-floor %s" % (c0, ref, good, bad))
Q = {x.address: x for x in cs.disasm(d[off(0x383F10):off(0x383F10) + 542], 0x383F10)}
unguarded = [a for a in Q if 0x383FD3 <= a < 0x38402C and Q[a].mnemonic in ("cmp", "test") ]
check("U 00383F10 admits both upper edges (ja) and loads the cell word unguarded",
      all(Q[a].mnemonic == "ja" for a in (0x383F77, 0x383F93, 0x383FAF, 0x383FCD)) and Q[0x383FAC].op_str == "xmm1, xmm0"
      and Q[0x383FCA].op_str == "xmm2, xmm0" and Q[0x38402C].op_str == "ecx, word ptr [r9 + rax*2]" and not unguarded)
x1 = f32(32256.998046875); dist = f32(x1 - f32(-32768.0))
check("R a strict world bound is not enough: one f32 ULP below 32257 rounds to the whole span (col 255 of 255)",
      x1 < -32768 + 255 * 255 and dist == 65025.0 and int(dist) // 255 == 255 and int(f32(f32(32256.99609375) + 32768.0)) // 255 == 254)
# T (added 2026-09-28, OPUS): what the unguarded index reads just past the table, on the ONE retained authored grid.
# 00383F10: table = decode(grid+8) as u16 (0038402C), list pool rdi = decode(grid+0xC) (00383F2E / 00383F3B); 0xFFFF
# is an empty cell (00384031); otherwise pool+word is a 0xFF-terminated region list (0038404F). Decoded data, bound to
# the retained slot's SHA-256; no load, allocation or live scene.
import hashlib
T_OK = hashlib.sha256(slot).hexdigest() == "b5d6da52eb8a402c9528898fd000bb928c26fc269866d2804544b58b155f9626"
g = struct.unpack_from("<I", slot, 0x20)[0]
tab, pool = struct.unpack_from("<II", slot, g + 8)
nc_, nr_ = slot[g + 2], slot[g + 3]
words = struct.unpack_from("<%dH" % (nc_ * nr_ + nc_ + 1), slot, tab)
past = words[nc_ * nr_:]
pool_len = len(slot) - pool
def verdict(wd): return "empty-cell" if wd == 0xFFFF else ("empty-list" if slot[pool + wd] == 0xFF else "list") if wd < pool_len else "OUTSIDE-POOL"
kinds = [verdict(wd) for wd in past]
T_OK = (T_OK and (tab, pool, nc_, nr_) == (0xAF0, 0xBC0, 10, 10) and tab + 2 * nc_ * nr_ == 0xBB8 and pool_len == 192
        and Q[0x383F2E].op_str == "ecx, dword ptr [rax + 0xc]" and Q[0x383F3B].op_str == "rdi, rax"
        and Q[0x384031].op_str == "ecx, 0xffff"
        and kinds == ["empty-list"] * 4 + ["empty-cell"] + ["OUTSIDE-POOL"] * 3 + ["empty-cell"] * 3)
check("T past the 100-entry table (row == rows): 100-103 pad -> empty list, 104 and 108-110 -> empty cell, 105-107 -> "
      "offsets outside the 192-byte pool", T_OK, "words %s" % [hex(x) for x in past])

live2 = re.sub(r"~~.*?~~", "", page, flags=re.S)
check("S2 contract section 10 carries the upper-edge item and the ctor cell the authored case",
      "The grid region query `00383F10` admits the exact upper edge" in live2 and "AUTHORED CASE 2026-09-27 (OPUS)" in tt[0])

print("FAILS", fails)
sys.exit(1 if fails else 0)
