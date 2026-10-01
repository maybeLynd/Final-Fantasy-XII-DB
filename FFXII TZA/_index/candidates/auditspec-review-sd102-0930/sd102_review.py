"""SWE2-AUDIT-SPEC independent check for SD-102 (2026-09-30).
R1  every 32/64-bit immediate stored or loaded in 002DAF30 / 002DAC70 / 002DD350, decoded as VIF codes and GIF tags by
    the PS2 field layout (not by pinned instruction text):
      VIF code: CMD bits 24-30, NUM 16-23, IMMEDIATE 0-15 (UNPACK: ADDR 0-9, USN 14, FLG 15; vn = CMD>>2&3, vl = CMD&3)
      GIF tag lo: NLOOP 0-14, EOP 15, PRE 46, PRIM 47-57, FLG 58-59, NREG 60-63; hi = REGS nibbles
R2  PRIM bit decode of 0x15C / 0x154.
R3  the "kick" callees: body length and first instructions of 0016D6A0, 003A1DB0 (is the kick a real call or a folded stub).
R4  the direct callees of each emitter, in order.
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_IMM
VIFCMD = {0x00: "NOP", 0x10: "FLUSHE", 0x11: "FLUSH", 0x13: "FLUSHA", 0x14: "MSCAL", 0x15: "MSCALF", 0x17: "MSCNT",
          0x01: "STCYCL", 0x50: "DIRECT", 0x51: "DIRECTHL"}
GIFREG = {0: "PRIM", 1: "RGBAQ", 2: "ST", 3: "UV", 4: "XYZF2", 5: "XYZ2", 6: "TEX0_1", 7: "TEX0_2", 8: "CLAMP_1",
          0xA: "FOG", 0xC: "XYZF3", 0xD: "XYZ3", 0xE: "A+D", 0xF: "NOP"}
def vif(v):
    cmd = (v >> 24) & 0x7F
    if cmd & 0x60 == 0x60:
        vn, vl = (cmd >> 2) & 3, cmd & 3
        fmt = "V%d-%d" % (vn + 1, [32, 16, 8, 5][vl])
        return "UNPACK %s NUM %d ADDR 0x%X USN %d FLG %d" % (fmt, (v >> 16) & 0xFF, v & 0x3FF, (v >> 14) & 1, (v >> 15) & 1)
    return "%s num %d imm 0x%X" % (VIFCMD.get(cmd, "cmd 0x%02X" % cmd), (v >> 16) & 0xFF, v & 0xFFFF)
def giftag(lo):
    return "NLOOP %d EOP %d PRE %d PRIM 0x%X FLG %d NREG %d" % (lo & 0x7FFF, (lo >> 15) & 1, (lo >> 46) & 1,
                                                               (lo >> 47) & 0x7FF, (lo >> 58) & 3, lo >> 60)
def regs(hi, n):
    return ",".join(GIFREG.get((hi >> (4 * i)) & 0xF, "?%X" % ((hi >> (4 * i)) & 0xF)) for i in range(n))
def prim(p):
    t = ["POINT", "LINE", "LINESTRIP", "TRIANGLE", "TRISTRIP", "TRIFAN", "SPRITE", "?"][p & 7]
    return "%s IIP %d TME %d FGE %d ABE %d AA1 %d FST %d CTXT %d" % (t, (p >> 3) & 1, (p >> 4) & 1, (p >> 5) & 1,
                                                                  (p >> 6) & 1, (p >> 7) & 1, (p >> 8) & 1, (p >> 9) & 1)
for f in (0x002DAF30, 0x002DAC70, 0x002DD350):
    print("R1 %s size %s" % (tk.fname(f), tk.fsize(f)))
    for x in tk.fdis(f):
        for op in x.operands:
            if op.type != X86_OP_IMM: continue
            v = op.imm & 0xFFFFFFFFFFFFFFFF
            if v >= 1 << 32:
                print("   %08X %-34s GIFtag? %s | as REGS(13): %s" % (x.address, x.mnemonic + " " + x.op_str, giftag(v), regs(v, 13)))
            elif v >= 0x01000000 and (v >> 24) & 0x7F in VIFCMD or (v >> 24) & 0x60 == 0x60 and v >= 0x60000000:
                print("   %08X %-34s VIF %s" % (x.address, x.mnemonic + " " + x.op_str, vif(v)))
            elif v in (0x15C, 0x154):
                print("   %08X %-34s PRIM %s" % (x.address, x.mnemonic + " " + x.op_str, prim(v)))
    calls = [x.op_str for x in tk.fdis(f) if x.mnemonic == "call"]
    print("R4 %08X calls: %s" % (f, " ".join(calls)))
for s in (0x0016D6A0, 0x003A1DB0):
    body = tk.fdis(s) if tk.fsize(s) else tk.dis(s, s + 24)
    print("R3 %s size %s: %s" % (tk.fname(s), tk.fsize(s), " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in body[:6])))
