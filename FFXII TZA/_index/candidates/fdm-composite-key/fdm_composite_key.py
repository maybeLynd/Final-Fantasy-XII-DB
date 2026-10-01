"""fdm_composite_key.py - the @FDM composite key built by 00521050, and what the shipped data can reach
(FABLE, Claude Opus 5.5, 2026-09-26).

SCOPE. C2 executes one DELIMITED ORIGINAL-CODE WINDOW - the image bytes 005210A6..005210BB, the key arithmetic of
the per-node body 00521050 - under Unicorn with a synthetic command record. It proves what number that arithmetic
produces for given words; it does NOT exercise rendering, the 005048A0 lookup, 00373060, or which records the game
actually reaches. C3 is a static archive census; the authored-command census (word+4 is 2 or 3 in all 7,193 0x14
commands) is on the-authored-presentation-command-handlers.md and is cited, not re-run.

  C1 static: the window decodes to  movzx edx,ax / mov rcx,rdi / movzx eax,word [rbx+2] / and edx,0xfffc /
     shl edx,0xe / or edx,eax / call 005048A0.
  C2 executed window: key = ((w4 & 0xFFFC) << 14) | w2 == ((w4 >> 2) << 16) | w2 for every w4 in 0..0xFFFF
     (w2 = 0x3CD3), so the group contribution starts at bit 16.
       w4 = 0x000A (group 2, lookup bit set), w2 = 0x3CD3 -> 0x23CD3   (the construction the page meant)
       w4 = 0x0002 / 0x0003, w2 = 0xBCD3           -> 0xBCD3    (group 0: the key IS word+2)
       no w4 with w2 = 0x3CD3 yields 0xBCD3         (so 0xBCD3 is not group 2 / item 0x3CD3)
  C3 archive census (needs FF12_VBF, default = the Steam install path): every key in every .cm's @FDM key table
     is below 0x10000, i.e. carries a zero group contribution.
Prints PASS/FAIL per check; exit 1 on any FAIL. A missing archive is a FAIL, not a skip.
"""
import io, os, struct, sys, zlib
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RDX, UC_X86_REG_RDI, UC_X86_REG_RSP

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro

fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", nm, detail))
    if not ok: fails += 1

W0, W1 = 0x005210A6, 0x005210BB
code = d[off(W0):off(W1) + 5]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
got = ["%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(code, W0)]
want = ["movzx edx, ax", "mov rcx, rdi", "movzx eax, word ptr [rbx + 2]", "and edx, 0xfffc", "shl edx, 0xe",
        "or edx, eax", "call 0x5048a0"]
check("C1 window decodes to the key arithmetic", got == want, "| ".join(got))

REC, STK = 0x10000000, 0x20000000
mu = Uc(UC_ARCH_X86, UC_MODE_64)
page = W0 & ~0xFFF
mu.mem_map(page, 0x2000); mu.mem_write(W0, code[:W1 - W0])
mu.mem_map(REC, 0x1000); mu.mem_map(STK, 0x1000)
def run(w2, w4):
    mu.mem_write(REC, struct.pack("<HHHH", 0, w2, w4, 0))
    mu.reg_write(UC_X86_REG_RBX, REC); mu.reg_write(UC_X86_REG_RAX, w4)   # 00521090 movzx eax, word [rbx+4]
    mu.reg_write(UC_X86_REG_RDI, 0); mu.reg_write(UC_X86_REG_RSP, STK + 0x800)
    mu.reg_write(UC_X86_REG_RDX, 0xDEADBEEF)
    mu.emu_start(W0, W1)
    return mu.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF

bad = [w4 for w4 in range(0x10000) if run(0x3CD3, w4) != (((w4 >> 2) << 16) | 0x3CD3)]
check("C2a executed key == ((w4>>2)<<16)|w2 for all 65,536 w4", not bad, "mismatches=%d" % len(bad))
k = run(0x3CD3, 0x000A)
check("C2b group 2 / item 0x3CD3 -> 0x23CD3", k == 0x23CD3, "got 0x%X" % k)
k2, k3 = run(0xBCD3, 2), run(0xBCD3, 3)
check("C2c w4 2 and 3 (the only authored values) leave key = word+2", k2 == k3 == 0xBCD3, "got 0x%X 0x%X" % (k2, k3))
hits = [w4 for w4 in range(0x10000) if run(0x3CD3, w4) == 0xBCD3]
check("C2d no w4 turns item 0x3CD3 into 0xBCD3", not hits, "w4 hits=%d" % len(hits))
# sensitivity: the (group << 14) reading the page used corresponds to a shift of 0xC on (w4 & 0xFFFC); patch the
# shl immediate (005210B8) to 0x0C and the same executed checks must fail - else C2 could not see that defect
mu.mem_write(0x005210B8, b"\x0c")
k = run(0x3CD3, 0x000A); badm = [w4 for w4 in range(0, 0x10000, 4) if run(0x3CD3, w4) != (((w4 >> 2) << 16) | 0x3CD3)]
check("C2e mutant (shl 0x0C) is caught", k != 0x23CD3 and len(badm) > 0, "mutant key 0x%X, mismatches=%d" % (k, len(badm)))
mu.mem_write(0x005210B8, b"\x0e")

VBF = os.environ.get("FF12_VBF", r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FFXII_TZA.vbf")
if not os.path.exists(VBF):
    check("C3 archive census", False, "archive not found: %s (set FF12_VBF)" % VBF)
else:
    sys.path.insert(0, str(ROOT / "Database/Tools/analysis-kit/gfz-scripts"))
    from census_format_magics import load_index
    BLOCK = 0x10000
    f = io.open(VBF, "rb"); names, blocks = load_index(f)
    def read_all(p):
        sb, size, o = names[p]; nb = (size + BLOCK - 1) // BLOCK; out = b""; f.seek(o)
        for i in range(nb):
            c = blocks[sb + i] or BLOCK; exp = BLOCK if i < nb - 1 else size - BLOCK * (nb - 1)
            b = f.read(c); out += zlib.decompress(b) if c != exp else b
        return out
    files = keys = high = 0; m1283 = None
    for p in [q for q in names if q.lower().endswith(".cm")]:
        b = read_all(p); var, _, cnt = struct.unpack_from("<III", b, 4); base = 0x40 if var == 1 else 0x30
        for i in range(cnt):
            o = base + struct.unpack_from("<I", b, base + i * 4)[0]
            if b[o:o + 4] != b"@FDM": continue
            kt = o + struct.unpack_from("<H", b, o + 0x32)[0]; kn = struct.unpack_from("<I", b, kt)[0]
            ks = struct.unpack_from("<%dI" % kn, b, kt + 4)
            files += 1; keys += kn; high += sum(1 for x in ks if x >> 16)
            if p.lower().endswith("/m1283.cm"): m1283 = (ks[0], ks[-1], kn)
    check("C3a @FDM tables and keys counted", files == 1045 and keys > 0, "files=%d keys=%d" % (files, keys))
    check("C3b no authored key is >= 0x10000", high == 0, "keys>=0x10000: %d" % high)
    check("C3c m1283 keys are 0xBCD3..0xBCE9 (23)", m1283 == (0xBCD3, 0xBCE9, 23), repr(m1283))

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
