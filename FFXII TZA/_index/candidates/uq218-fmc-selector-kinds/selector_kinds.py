"""selector_kinds.py - UQ-218: the selectors behind @FMC command 0x0B (FABLE, Claude Opus 5.5, 2026-09-28). Static from the
certified image plus one census of the .ca/.cm @FMC blocks. Follows ../uq218-fmc-opcode-crosswalk/.

  S1 CharacterRenderSystem_Initialize (004269A0) passes 01F000A0 to 0041D6E0, which stores it at 02CA4668 - the pointer 0x0B
     reads. 01F000A0 is a .data table of 0x30 16-byte entries {1, cell}; kind k's selector is the function in cell [+8].
     Kinds 0, 1, 2, 4, 0xA, 0xB, 0x10, 0x20-0x25 and 0x2F have their own selector; every other kind uses 005C5230 (returns 0)
  S2 kind 0x10 (004225A0) is a random countdown: when record +0x412 is 0xFF it draws n = (lo - 1 + rand() % (hi - lo + 1)) *
     frameLimit, with lo, hi = entry bytes +0x2DD, +0x2DE (0x0A's operand bytes +3, +4) and frameLimit the byte at 01DFE0B4
     (1 at 30 fps, 2 at 60 fps - the boot-fixups contract); each call then returns 0 and decrements, and the call that finds 0
     returns 1 and re-arms 0xFF
  S3 the kinds 0x0A authors are exactly 0, 1, 2, 0xA, 0xB, 0x10, 0x20, 0x21, 0x24, 0x25 - all with their own selector. Kinds 0,
     0xA, 0xB share 004256E0 (argument 0 / 1 / 2); kind 1 is 00422420 (a draw from 003A6E60(5), cached at +0x411); kind 2 is
     00422500; kinds 0x20, 0x21, 0x24, 0x25 (00422630, 004226C0, 00422870, 00422940) each call the yaw-to-point 00424370
  S4 prediction from S2's divisor: every authored kind-0x10 0x0A has lo <= hi (so hi - lo + 1 > 0)
  C  controls: kinds 5-9 bind to 005C5230, and none is authored; a lo > hi command would fail S4 (none found)
  Not claimed: what kinds other than 0x10 decide by - 004256E0 and 003A6E60 are read only in part, and kinds 2 and 0x20 answer
  through the battle unit's view request (002ED500 -> 0031B4B0 -> 0031ADB0) with queries 0x30 and 4, whose results were not read
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
I = dis(0x4269D8, 0x40); R = dis(0x41D6E0, 8)
rel = lambda at, n=3: at + 7 + struct.unpack_from("<i", d, off(at) + n)[0]
TAB = 0x1F000A0
sel = {}
for k in range(0x30):
    one, cell = struct.unpack_from("<QQ", d, off(TAB + 16 * k)); sel[k] = struct.unpack_from("<Q", d, off(cell))[0]
own = sorted(k for k, f in sel.items() if f != 0x5C5230)
ok("S1", rel(0x4269D8) == TAB and I[0x426A0D] == "call 0x41d6e0" and R[0x41D6E0].startswith("mov qword ptr [rip")
   and rel(0x41D6E0) == 0x2CA4668 and own == [0, 1, 2, 4, 0xA, 0xB, 0x10, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x2F]
   and sel[3] == 0x5C5230,
   "004269D8 lea -> %08X, 0041D6E0 stores it at %08X; kinds with their own selector %s" % (rel(0x4269D8), rel(0x41D6E0), [hex(k) for k in own]))
K = dis(0x4225A0, 0x90)
iat = 0x4225D0 + struct.unpack_from("<i", d, off(0x4225CA) + 2)[0]
ok("S2", K[0x4225B5] == "cmp byte ptr [rdi + 0x412], 0xff" and K[0x4225C3] == "movsx ebx, byte ptr [rcx + 0x2dd]"
   and K[0x4225D0] == "movsx r8d, byte ptr [rsi + 0x2de]" and K[0x4225D9] == "sub r8d, ebx" and K[0x4225DC] == "dec bl"
   and K[0x4225DE] == "inc r8d" and K[0x4225E1] == "idiv r8d" and K[0x4225EB] == "add dl, bl" and K[0x4225F5] == "imul ecx, eax"
   and 0x4225EB + struct.unpack_from("<i", d, off(0x4225E4) + 3)[0] == 0x1DFE0B4 and iat == 0x8C3098
   and K[0x42260E] == "mov byte ptr [rdi + 0x412], 0xff" and K[0x422615] == "mov eax, 1" and K[0x422620] == "dec al",
   "rand via IAT %08X; n = (lo - 1 + rand %% (hi - lo + 1)) * byte[01DFE0B4]; countdown returns 0, then 1 and re-arms" % iat)
sys.path.insert(0, r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
from census_format_magics import load_index
f = io.open(VBF, "rb"); names, blocks = load_index(f); BLOCK = 0x10000
def read_all(p):
    sb, size, o = names[p]; n = (size + BLOCK - 1) // BLOCK; out = b""; f.seek(o)
    for i in range(n):
        cs = blocks[sb + i] or BLOCK; exp = BLOCK if i < n - 1 else size - BLOCK * (n - 1); c = f.read(cs)
        out += zlib.decompress(c) if cs != exp else c
    return out
kinds = collections.Counter(); lohi_bad = 0; lohi = collections.Counter()
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
        elen = struct.unpack_from("<I", dd, o + 8)[0]; rend = o + elen
        ro, ri, rcount = o + 0x30, 0, struct.unpack_from("<I", dd, o + 0x0C)[0]
        while ro + 6 <= rend and ri < rcount:
            subc = dd[ro + 3]; rlen = struct.unpack_from("<H", dd, ro + 4)[0]
            if rlen < 6 or ro + rlen > rend: break
            so = ro + 6
            for _ in range(subc):
                w2 = struct.unpack_from("<H", dd, so + 2)[0]; ccnt, slen = w2 & 0x3F, w2 >> 6; co = so + 4
                for _ in range(ccnt):
                    cw = struct.unpack_from("<H", dd, co)[0]; op, cl = cw & 0x7F, cw >> 7
                    if cl == 0: break
                    if op == 0x0A:
                        k, lo, hi = dd[co + 2], struct.unpack_from("b", dd, co + 3)[0], struct.unpack_from("b", dd, co + 4)[0]
                        kinds[k] += 1
                        if k == 0x10: lohi[(lo, hi)] += 1; lohi_bad += (lo > hi)
                    co += cl
                so += slen
            ro += rlen; ri += 1
def calls(a, tgt, n=0xC0): return any(i.mnemonic == "call" and i.op_str == hex(tgt) for i in MD.disasm(d[off(a):off(a) + n], a))
ang = [sel[k] for k in (0x20, 0x21, 0x24, 0x25)]
ok("S3", sorted(kinds) == [0, 1, 2, 0xA, 0xB, 0x10, 0x20, 0x21, 0x24, 0x25] and all(sel[k] != 0x5C5230 for k in kinds)
   and (sel[0], sel[0xA], sel[0xB], sel[1], sel[2]) == (0x4223F0, 0x422400, 0x422410, 0x422420, 0x422500)
   and ang == [0x422630, 0x4226C0, 0x422870, 0x422940] and all(calls(a, 0x424370) for a in ang),
   "authored kinds %s" % {hex(k): v for k, v in sorted(kinds.items())})
ok("S4", lohi_bad == 0 and sum(lohi.values()) == kinds[0x10], "kind 0x10 (lo, hi): %s" % dict(lohi.most_common(8)))
ok("C", all(sel[k] == 0x5C5230 for k in range(5, 10)) and not any(k in kinds for k in range(5, 10)),
   "kinds 5-9 bind to 005C5230 and none is authored")
print("FAILS", fails); sys.exit(1 if fails else 0)
