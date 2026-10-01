"""store_saturation.py - the script VM's variable store 0026D530 saturates by width, and its s16 range is off by one at both ends
(FABLE, Claude Opus 5.5, 2026-09-28, on ASTRA-REQ-FABLE-SCRIPT-STORE-SATURATION). Decoded from the certified image; nothing executed.

  S1 the store takes the width from descriptor bits 28..31 (shr 0x1C / cmp 5 / ja -> ret, so widths 6 and 7 store nothing) and
     dispatches through the six-entry table at image base + 0x14D5F4: 0 u8 -> [0, 255], 1 s8 -> [-128, 127], 2 u16 -> [0, 0xFFFF],
     3 s16 -> floor 0xFFFF8001 (-32767) and ceiling 0x8000 (+32768) then a word store, 4 and 5 -> the same raw dword copy
  S2 the read side: PUSHV 00267FC0 takes the width the same way through its table at image base + 0x1480E8, and width 3 reaches
     0026802F 'movsx ecx, word ptr' - a sign-extending read
  S3 consequence, modelled from S1 and S2: a script store of +32768 into an s16 variable writes 0x8000, which the next read returns
     as -32768 - the one value whose sign flips; a store of -32768 writes 0x8001 and reads back -32767; +32767 and -32767 round-trip
  C  control: a model with the conventional [-32768, 32767] clamp disagrees with S1's constants at both edges, and the u16 arm
     (zero-extending read at 0026801E) returns 0xFFFF for a store of 65536 - so S3's flip is the s16 arm's own range
  Evidence classes: ASTRA executed the store leaf in isolation (their record); S1-S3 here are static. Whether any shipped script
  stores +32768 into an s16 variable is not claimed.
"""
import hashlib, os, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
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
def body(a, n): return {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(a):off(a) + n], a)}
table = lambda base_rva, n: [0x120000 + struct.unpack_from("<I", d, off(0x120000 + base_rva) + 4 * k)[0] for k in range(n)]
W = body(0x26D530, 0xC2)
ST = table(0x14D5F4, 6)
ok("S1", W[0x26D53F] == "shr eax, 0x1c" and W[0x26D542] == "cmp eax, 5" and W[0x26D545] == "ja 0x26d5f1" and W[0x26D5F1] == "ret"
   and ST == [0x26D55F, 0x26D57E, 0x26D5A1, 0x26D5C4, 0x26D5E9, 0x26D5E9]
   and W[0x26D570] == "mov ecx, 0xff" and W[0x26D58A] == "mov eax, 0xffffff80" and W[0x26D593] == "mov ecx, 0x7f" and W[0x26D5B4] == "mov ecx, 0xffff"
   and W[0x26D5C7] == "mov eax, 0xffff8001" and W[0x26D5D4] == "mov r9d, 0x8000" and W[0x26D5E3] == "mov word ptr [r8 + rdx*2], ax"
   and W[0x26D5ED] == "mov dword ptr [r8 + rcx*4], eax",
   "store table %s; s16 floor 0xFFFF8001, ceiling 0x8000, word store; widths 4 and 5 share the dword copy" % ["%08X" % t for t in ST])
R = body(0x267FC0, 0xA8); RT = table(0x1480E8, 6)
ok("S2", R[0x267FE1] == "shr eax, 0x1c" and RT == [0x267FFC, 0x26800D, 0x26801E, 0x26802F, 0x268040, 0x268050]
   and R[0x268037] == "movsx ecx, word ptr [rax + rcx*2]" and R[0x268026] == "movzx ecx, word ptr [rax + rcx*2]",
   "PUSHV table %s; width 3 -> 0026802F movsx word" % ["%08X" % t for t in RT])
def store_s16(v, lo=-32767, hi=32768):
    if v < lo: return lo & 0xFFFF
    return min(v, hi) & 0xFFFF
read_s16 = lambda w: w - 0x10000 if w & 0x8000 else w
cases = {v: read_s16(store_s16(v)) for v in (32768, 32769, -32768, 32767, -32767, 0)}
ok("S3", cases == {32768: -32768, 32769: -32768, -32768: -32767, 32767: 32767, -32767: -32767, 0: 0},
   "store then read, s16: %s" % cases)
conv = lambda v: max(-32768, min(v, 32767)) & 0xFFFF
u16 = lambda v: 0 if v < 0 else min(v, 0xFFFF)
ok("C", conv(32768) != store_s16(32768) and conv(-32768) != store_s16(-32768) and u16(65536) == 0xFFFF and read_s16(conv(32768)) == 32767,
   "the conventional clamp stores %#06x / %#06x at the edges where the image stores %#06x / %#06x; u16 of 65536 saturates to 0xFFFF"
   % (conv(32768), conv(-32768), store_s16(32768), store_s16(-32768)))
print("FAILS", fails); sys.exit(1 if fails else 0)
