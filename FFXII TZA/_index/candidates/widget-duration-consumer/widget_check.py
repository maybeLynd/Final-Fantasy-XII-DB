"""widget_check.py - 00244DD0's deferred dispatch and delay, and 002468A0's transition duration, bound from the listing
(FABLE, Claude Opus 5.5, 2026-09-28). Static binding plus exact integer models.
  D1  mode 2 zeroes +0x70 only when +0x40 bit 16 is SET: bt edx,0x10 / jae 00244E6D skips the store (00244E62-00244E6A)
  D2  +0x40 bit 0 gates the nibble dispatch: clear -> nibble 1 (and F1 / or 1) and jump to the tail's or 0x30 (00244EDF);
      set -> nibble 0 schedules, 2 rebases, 3 schedules, anything else returns at 00244EF7
  D3  delay order: word[record+2], then cmove to 0 when 00181C90 returns 1 (00244EAD), then the bit-11 override
      (bt / btr / shr 0x16) after it; conversion imul 60, mul 0x10624DD3, shr 6 (unsigned)
  D4  the unsigned conversion equals floor(x*60/1000) for every x in 0..65535 (covers the u16 and the 10-bit sources)
  D5  +0x90: imul ecx,[rsp+0x70],60 (32-bit product), imul 0x10624DD3, sar 6, sign correction (shr 31 / add): signed
      truncation toward zero - 1000 -> 60, -17 -> -1, 35791395 -> -2147483
  C   controls: the opposite polarity (jb) would zero when the bit is clear; an unsigned model of D5 gives a different
      value for -17
"""
import os, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
F = {}
for l in open(CACHE, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split(None, 2)
    if len(p) == 3 and p[1] in ("00244DD0", "002468A0"): F[int(p[0], 16)] = p[2].split(" ;")[0]
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def has(want): return all(F.get(a) == s for a, s in want.items())
ok("D1", has({0x00244E62: "bt edx, 0x10", 0x00244E66: "jae 0x244e6d", 0x00244E68: "xor ecx, ecx", 0x00244E6A: "mov dword ptr [rbx + 0x70], ecx"}),
   "mode 2: jae (bit 16 clear) skips the zeroing store, so +0x70 is zeroed when the bit is set")
ok("D2", has({0x00244E1A: "test dl, 1", 0x00244E1D: "jne 0x244e2c", 0x00244E1F: "and dword ptr [rbx + 0x7c], 0xfffffff1",
              0x00244E23: "or dword ptr [rbx + 0x7c], 1", 0x00244E27: "jmp 0x244edf", 0x00244E37: "je 0x244e47", 0x00244E39: "sub ecx, 2",
              0x00244E3C: "je 0x244e62", 0x00244E3E: "cmp ecx, 1", 0x00244E41: "jne 0x244ef7", 0x00244EDF: "or dword ptr [rbx + 0x7c], 0x30"}),
   "bit 0 clear -> nibble 1 -> tail or 0x30; bit 0 set: 0 schedule, 2 rebase, 3 schedule, else return at 00244EF7")
ok("D3", has({0x00244E9C: "movzx edi, word ptr [rcx + 2]", 0x00244EA0: "call 0x181c90", 0x00244EA7: "cmp eax, 1", 0x00244EAD: "cmove edi, ecx",
              0x00244EB0: "bt eax, 0xb", 0x00244EB4: "jae 0x244ec2", 0x00244EB8: "btr edi, 0xb", 0x00244EBF: "shr edi, 0x16",
              0x00244EC2: "imul ecx, edi, 0x3c", 0x00244ECF: "mul ecx", 0x00244ED1: "shr edx, 6", 0x00244ED4: "mov dword ptr [rbx + 0x70], edx"}),
   "record u16 -> zero gate (cmove) -> bit-11 override after it -> unsigned x60 / 1000")
conv = lambda x: (((x * 60) & 0xFFFFFFFF) * 0x10624DD3 >> 32) >> 6
bad = [x for x in range(65536) if conv(x) != (x * 60) // 1000]
ok("D4", not bad, "floor(x*60/1000) for all x in 0..65535 (first mismatch %s)" % (bad[:1] or "none"))
ok("D5", has({0x00246971: "imul ecx, dword ptr [rsp + 0x70], 0x3c", 0x00246995: "mov eax, 0x10624dd3", 0x0024699A: "imul ecx",
              0x002469A6: "sar edx, 6", 0x002469A9: "mov eax, edx", 0x002469AB: "shr eax, 0x1f", 0x002469AE: "add edx, eax",
              0x002469B0: "mov dword ptr [rbx + 0x90], edx"}), "+0x90: 32-bit product, signed reciprocal, sar 6 and sign correction")
s32 = lambda v: v - (1 << 32) if v & 0x80000000 else v
def signed_conv(a):
    p = s32((a * 60) & 0xFFFFFFFF)
    hi = (p * 0x10624DD3) >> 32                                       # imul: signed 64-bit product, high half
    q = hi >> 6                                                       # sar
    return q + (1 if q < 0 else 0)                                    # shr 31 / add: round toward zero
vals = {a: signed_conv(a) for a in (1000, -17, 35791394, 35791395)}
ok("D5m", vals == {1000: 60, -17: -1, 35791394: 2147483, 35791395: -2147483}, "signed model: %s" % vals)
unsigned_m17 = conv((-17) & 0xFFFFFFFF)
mut = dict(F); mut[0x00244E66] = "jb 0x244e6d"
ok("C", not all(mut.get(a) == s for a, s in {0x00244E66: "jae 0x244e6d"}.items()) and s32(unsigned_m17) != -1, "controls: D1 binding refuses a jb mutant; unsigned model of -17 gives %d, not -1" % unsigned_m17)
print("FAILS", fails); sys.exit(1 if fails else 0)
