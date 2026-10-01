"""waits.py - OV-11, "remaining native wait services": the complete set of services the wait-slot dispatcher calls
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  J  THE SWITCH in 0025DF00 is on the wait slot's kind byte +0x14: `cmp eax, 7; ja 0025E127` (the blocked exit) and an
     8-entry RVA table at image base + 0x13E3CC. Its targets: 0 -> 0025E127 (blocked), 1 and 2 -> 0025E0BE (the
     interpreter arm), 3 -> 0025E027, 4 -> 0025E091, 5 -> 0025E00A, 6 -> 0025E058, 7 -> 0025E083
  A  EACH SERVICE ARM calls exactly one predicate and, on success, writes kind 1:
     3 -> 003DBF60 (the target's matching entry; resumes when it returns 0xFF = absent), sets +0x27
     4 -> 003DC050 (the caller's detached notification), then 003DB2A0 removes it
     5 -> 002674B0 (the actor/resource-entry list)
     6 -> 003DB640 (the target's channel bit; resumes when clear), sets +0x27
     7 -> 00267420 (the actor/channel list), sharing arm 6's tail
  K  sensitivity: the table read is bounded by the `cmp 7` and entry 8 is not a code address
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
TX = [s for s in SECS if s[0] == b".text"][0]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
def callers(t):
    return [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == t]
def jcc(t):
    return [tb + j for j in range(len(text) - 6) if text[j] == 0x0F and 0x80 <= text[j + 1] <= 0x8F
            and tb + j + 6 + struct.unpack_from("<i", text, j + 2)[0] == t]
def ptrs(t):
    pat = struct.pack("<Q", t); out = []
    for nm, vs, va, rs, ro in SECS:
        blob = d[ro:ro + rs]; k = blob.find(pat)
        while k >= 0: out.append(B + va + k); k = blob.find(pat, k + 1)
    return out
def riprefs(t):
    # any disp32 in .text that resolves rip-relative to t: the displacement is followed by 0, 1, 2 or 4 immediate bytes;
    # the instruction starts 2..9 bytes before it, and must decode as ONE instruction ending exactly there with a rip operand
    # (decoding from a fixed offset lands mid-instruction - the first draft found not even the known lea at 003DDA83)
    out = []
    for j in range(len(text) - 4):
        disp = struct.unpack_from("<i", text, j)[0]
        for tail in (0, 1, 2, 4):
            end = j + 4 + tail
            if tb + end + disp != t: continue
            for back in range(2, 10):
                x = next(cs.disasm(text[j - back:end], tb + j - back, 1), None)
                if x and x.size == back + 4 + tail and "rip" in x.op_str: out.append(x.address)
    return sorted(set(out))

tb0 = 0x120000 + 0x13E3CC
tab = [B + struct.unpack_from("<I", d, off(tb0 + 4 * k))[0] for k in range(9)]
sw = dis(0x25DFF0, 0x25E00A)
check("J", at(sw, {0x25DFF0: "movzx eax, byte ptr [rsi + 0x14]", 0x25DFF4: "cmp eax, 7", 0x25DFF7: "ja 0x25e127",
                   0x25DFFD: "mov ecx, dword ptr [r14 + rax*4 + 0x13e3cc]", 0x25E008: "jmp rcx"})
      and tab[:8] == [0x25E127, 0x25E0BE, 0x25E0BE, 0x25E027, 0x25E091, 0x25E00A, 0x25E058, 0x25E083],
      "kind 0..7 -> %s" % " ".join("%08X" % a for a in tab[:8]))
arms = dis(0x25E00A, 0x25E0BE)
check("A", at(arms, {0x25E011: "call 0x2674b0", 0x25E01E: "mov byte ptr [rsi + 0x14], 1",
                     0x25E03B: "call 0x3dbf60", 0x25E040: "cmp eax, 0xff", 0x25E045: "jne 0x25e127", 0x25E04F: "mov byte ptr [rsi + 0x27], 1",
                     0x25E069: "call 0x3db640", 0x25E070: "jne 0x25e127", 0x25E07A: "mov byte ptr [rsi + 0x27], 1",
                     0x25E08A: "call 0x267420", 0x25E08F: "jmp 0x25e06e",
                     0x25E09F: "call 0x3dc050", 0x25E0A9: "je 0x25e127", 0x25E0B0: "call 0x3db2a0", 0x25E0B5: "mov byte ptr [rsi + 0x14], 1"})
      and sorted(int(s.split()[1], 16) for s in arms.values() if s.startswith("call 0x") and "0x20e600" not in s)
          == [0x267420, 0x2674B0, 0x3DB2A0, 0x3DB640, 0x3DBF60, 0x3DC050],
      "the service arms call exactly 002674B0, 003DBF60, 003DB640, 00267420, 003DC050 + 003DB2A0 (besides the pointer resolver)")
check("K", not (0x121000 <= tab[8] < 0x8C2000), "entry 8 (%08X) is not a code address: the table has eight entries" % tab[8])
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
