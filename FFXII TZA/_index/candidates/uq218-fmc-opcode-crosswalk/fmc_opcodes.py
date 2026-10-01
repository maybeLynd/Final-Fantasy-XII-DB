"""fmc_opcodes.py - UQ-218: the @FMC command ids the archive uses, where each one's meaning is read, and the four that were
unread - 0x01, 0x0A, 0x0B, 0x28 (FABLE, Claude Opus 5.5, 2026-09-28). Static from the certified image plus one archive census.

  T  the invoker table 01EFFAF0: 76 slots x 0x10, slots 0x49-0x4B null, 33 slots the shared ret-0 stub 0016D6A0
  A  the archive: 32,151 @FMC blocks, 0 grammar violations, exactly 33 command ids used, none of them on a stub or null slot
  P1 0x01 (00417920) 'play track n': word +2 = {mode:4, n:12}; nothing happens when the current state already plays n
     (+0x80 == n); mode 0 starts n in a parallel state slot found by 0041C9A0 (the slot already playing n, else the first free
     one, +0x95 == 0); mode 1 does so only when the current state's +4 is 2; mode 2 replaces the current state when entry flag
     0x40 is up and otherwise raises entry flag 0x80 (a pending request); other modes do nothing. Authored modes: 0, 1, 2 only
  P2 0x0A (00418600) stores its four operand bytes at entry +0x2DC..+0x2DF and marks the current state (+4 = 1, +8 |= 2,
     +0x20 = entry +0x340); 0x0B (00417110) reads +0x2DC as a selector kind (0xFF = none), calls the selector reached
     through the context pointer at 02CA4668 ([ctx + kind*16 + 8]), and uses the returned index i (< byte +4) to play track
     word[+6 + 2i] + (the result's high half) through 0x01's own handler (00417390), after resetting the other idle state
     slots. Archive: every 0x0B is the command right after a 0x0A in the same group, and every 0x0B's length is
     6 + 2 * byte +4 (the track list)
  P3 0x28 (00520720 -> 003E6AA0) writes its dword +4 into bits 27..31 of render-record +0x304 and raises dirty bit 27 of
     +0x294; authored values are 1 and 10 only
  C  controls: a 4 + 2*count length law matches no 0x0B; 0x0B after a non-0x0A would fail P2's adjacency (none found, and
     the test sees a planted swap); a mode nibble of 3 in P1's decode reaches the do-nothing exit
  Not claimed: what the selector kinds choose, what +0x304's bits 27..31 select in 003B3C00, or any live behaviour
"""
import hashlib, io, os, struct, sys, zlib, collections
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
VBF = os.environ.get("FF12_VBF", r"D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
off = lambda v: next(ra + v - 0x120000 - va for vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def dis(a, n): return {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(a):off(a) + n], a)}
T = 0x1EFFAF0
slots = [struct.unpack_from("<Q", d, off(T + 0x10 * k))[0] for k in range(76)]
stub = [k for k, f in enumerate(slots) if f == 0x16D6A0]; null = [k for k, f in enumerate(slots) if f == 0]
ok("T", null == [0x49, 0x4A, 0x4B] and len(stub) == 33, "76 slots; null %s; %d on the ret-0 stub" % ([hex(k) for k in null], len(stub)))
# ---- archive
sys.path.insert(0, r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
from census_format_magics import load_index
f = io.open(VBF, "rb"); names, blocks = load_index(f); BLOCK = 0x10000
def read_all(p):
    sb, size, o = names[p]; n = (size + BLOCK - 1) // BLOCK; out = b""; f.seek(o)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK; exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1); c = f.read(cs)
        out += zlib.decompress(c) if cs != exp else c
    return out
ops = collections.Counter(); bad = 0; blocks_n = 0
b_after = collections.Counter(); b_len_ok = b_len_alt = b_total = 0; modes01 = collections.Counter(); v28 = collections.Counter()
for p in names:
    pl = p.lower()
    if not (pl.endswith(".ca") or pl.endswith(".cm")): continue
    dd = read_all(p)
    if len(dd) < 0x40: continue
    var, clen, cnt = struct.unpack_from("<III", dd, 4); base = 0x40 if var == 1 else 0x30
    for i in range(cnt):
        v = struct.unpack_from("<I", dd, base + i * 4)[0]
        if var == 1 and v == 0: continue
        o = base + v
        if dd[o:o + 4] != b"@FMC": continue
        blocks_n += 1; elen = struct.unpack_from("<I", dd, o + 8)[0]; rend = o + elen
        ro, ri, rcount = o + 0x30, 0, struct.unpack_from("<I", dd, o + 0x0C)[0]
        while ro + 6 <= rend and ri < rcount:
            subc = dd[ro + 3]; rlen = struct.unpack_from("<H", dd, ro + 4)[0]
            if rlen < 6 or ro + rlen > rend: bad += 1; break
            so = ro + 6
            for _ in range(subc):
                w2 = struct.unpack_from("<H", dd, so + 2)[0]; ccnt, slen = w2 & 0x3F, w2 >> 6; co = so + 4; prev = None
                for _ in range(ccnt):
                    cw = struct.unpack_from("<H", dd, co)[0]; op, cl = cw & 0x7F, cw >> 7
                    if cl == 0: bad += 1; break
                    ops[op] += 1
                    if op == 0x0B:
                        b_total += 1; b_after[prev] += 1; c = dd[co + 4]
                        b_len_ok += (cl == 6 + 2 * c); b_len_alt += (cl == 4 + 2 * c)
                    if op == 0x01: modes01[struct.unpack_from("<H", dd, co + 2)[0] & 0xF] += 1
                    if op == 0x28: v28[struct.unpack_from("<I", dd, co + 4)[0]] += 1
                    prev = op; co += cl
                so += slen
            ro += rlen; ri += 1
used = sorted(ops)
ok("A", blocks_n == 32151 and bad == 0 and len(used) == 33 and not (set(used) & (set(stub) | set(null))),
   "%d blocks, %d violations, %d ids used, none on a stub or null slot" % (blocks_n, bad, len(used)))
B = dis(0x417920, 0x160)
ok("P1", B[0x41792F] == "movzx r9d, word ptr [rcx + 2]" and B[0x41793D] == "shr edx, 4" and B[0x417943] == "cmp dword ptr [rbx + 0x80], edx"
   and B[0x41794F] == "and r9d, 0xf" and B[0x417963] == "cmp r9d, 1" and B[0x417967] == "jne 0x417a6d"
   and B[0x41796D] == "mov eax, dword ptr [r8 + 0xc]" and B[0x417971] == "test al, 0x40" and B[0x4179EB] == "bts eax, 7"
   and B[0x417A03] == "cmp word ptr [rbx + 4], 2" and B[0x417A0D] == "call 0x41c9a0" and set(modes01) <= {0, 1, 2},
   "word +2 = {mode:4, n:12}; modes 0/1/2 decoded, others exit; authored modes %s" % dict(modes01))
A = dis(0x418600, 0x45); Bb = dis(0x417110, 0x2C0)
ok("P2", [A[a] for a in (0x418600, 0x418604, 0x41862C, 0x418631, 0x41863C)] ==
   ["movzx eax, byte ptr [rcx + 2]", "mov byte ptr [r8 + 0x2dc], al", "mov eax, 1", "mov word ptr [rdx + 4], ax", "or word ptr [rdx + 8], 2"]
   and Bb[0x417138] == "movzx r8d, byte ptr [r8 + 0x2dc]" and Bb[0x417140] == "cmp r8b, 0xff" and Bb[0x4171FA] == "call qword ptr [rdx]"
   and Bb[0x41726B] == "movzx eax, word ptr [r13 + 4]" and Bb[0x41735C] == "movzx ecx, word ptr [r13 + r14*2 + 6]"
   and Bb[0x417390] == "call 0x417920" and 0x4171EE + struct.unpack_from("<i", d, off(0x4171E7) + 3)[0] == 0x2CA4668
   and b_after == {0x0A: b_total} and b_len_ok == b_total,
   "0x0A stores +0x2DC..; 0x0B selects through 02CA4668 and plays word[+6 + 2i] via 00417920; %d 0x0B, all after a 0x0A, all 6 + 2*count long" % b_total)
Z = dis(0x520720, 0x16); Y = dis(0x3E6AA0, 0x1E)
ok("P3", Z[0x520724] == "mov edx, dword ptr [rdx + 4]" and Z[0x520727] == "call 0x3e6aa0"
   and [Y[a] for a in (0x3E6AA0, 0x3E6AAA, 0x3E6AB4, 0x3E6AB7)] == ["or dword ptr [rcx + 0x294], 0x8000000", "and dword ptr [rcx + 0x304], 0x7ffffff",
   "shl edx, 0x1b", "or dword ptr [rcx + 0x304], edx"] and set(v28) == {1, 10},
   "dword +4 -> +0x304 bits 27..31, dirty bit 27 of +0x294; authored values %s" % dict(v28))
planted = collections.Counter({0x0A: b_total - 1, 0x09: 1})
ok("C", b_len_alt == 0 and planted != {0x0A: b_total} and B[0x417963] == "cmp r9d, 1",
   "4 + 2*count matches %d of %d 0x0B; the adjacency test rejects one planted non-0x0A predecessor" % (b_len_alt, b_total))
print("used ids:", " ".join("%02X" % k for k in used)); print("FAILS", fails); sys.exit(1 if fails else 0)
