"""ms_states.py - MS-1 and MS-2 (the map-screens page's registered residue) (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

MS-1: what container +0x179D2 bits 9, 10 and 11 mean as states.
  C  CENSUS: every write to the word (disp 0x179D2, found from the raw disp32 bytes, kept only where most linear decodes
     16..48 bytes earlier converge on the instruction), with each register source traced back to its immediate. Per bit
     (0x200, 0x400, 0x800) the setters and clearers are listed; whole-word stores are shown to carry no new bit 9-11
  9  BIT 9 = the reopen request after a link: set only by the location page's link path (002BB8BD, after 003BF8E0);
     cleared only in the two per-frame steps (002B784E track, 002BABE7 location), right after they find both page slots
     empty and call 003C21B0
  10 BIT 10 = "opened in mode 5" (the fullscreen opener): set only by 002B6220 (track, 0x500 with bit 8, when it creates
     the container) and the leaf 002BA000 (location), whose only caller is the mode-5 opener 0028E660; never cleared
  11 BIT 11 = the confirm latch: set only at 002BAA79 (r14d = 0x800 at 002BA927) at the end of the location map's confirm;
     never cleared, so after one confirm every later close and confirm is refused. The track map tests it but never sets it
MS-2: what the two floats +0x10 / +0x14 of the block 02B457F0 mean.
  O  their only writer is the setter 003C6360, called only by 00379870 (the NPS2 consumer: sub-location id -> world-to-image
     transform) with the record's originX / originZ (+0x10 / +0x14), or 0 for a null record; 003C6380 stores the extent
     at +0x18 / +0x1C. So the floats are the current sub-location picture's world origin, and the track arm negates them to
     translate world positions into picture space
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
S = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
     for i in range(n)]
TX = [s for s in S if s[0] == b".text"][0]
def off(v): return v - B - TX[2] + TX[4]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
def aligned(s0):
    hit = 0
    for st in range(s0 - 48, s0 - 16):
        for x in cs.disasm(text[st - tb:s0 - tb + 16], st):
            if x.address >= s0:
                hit += x.address == s0; break
    return hit * 2 > 32
writes = {}
pat = struct.pack("<I", 0x179D2); i = text.find(pat)
while i != -1:
    for back in range(8, 0, -1):
        s0 = i - back
        ins = list(cs.disasm(text[s0:s0 + 15], tb + s0, 1))
        if ins and ins[0].address + ins[0].size >= tb + i + 4 and "+ 0x179d2]" in ins[0].op_str and aligned(tb + s0):
            m = re.match(r"(or|and|xor|mov) word ptr \[\w+ \+ 0x179d2\], (\S+)$", "%s %s" % (ins[0].mnemonic, ins[0].op_str))
            if m: writes[ins[0].address] = m.groups()
            break
    i = text.find(pat, i + 1)
R32 = {"ax": "eax", "cx": "ecx", "dx": "edx", "bx": "ebx", "si": "esi", "di": "edi", "r14w": "r14d", "r15w": "r15d"}
def trace(a, reg, window=0x100):
    """the last `mov reg32, imm` before a on a converged linear decode (None if the source is not an immediate)"""
    for st in range(a - window, a - 8):
        ins = [x for x in cs.disasm(d[off(st):off(a)], st)]
        if not ins or ins[-1].address + ins[-1].size != a: continue
        for x in reversed(ins):
            ops = x.op_str.split(", ")
            if x.mnemonic in ("test", "cmp", "bt", "push"): continue       # reads, not writes
            if ops[0] in (reg, R32.get(reg)):
                return int(ops[1], 16) if x.mnemonic == "mov" and len(ops) == 2 and ops[1].startswith("0x") else None
        return None
    return None
sets = {9: [], 10: [], 11: []}; clears = {9: [], 10: [], 11: []}; whole = []
for a, (op, src) in sorted(writes.items()):
    v = int(src, 16) if src.startswith("0x") else (int(src) if src.isdigit() else trace(a, src))
    if a == 0x2BAA79: v = 0x800 if dis(0x2BA927, 0x2BA92D).get(0x2BA927) == "mov r14d, 0x800" else None   # r14 set in the parent fragment
    if op == "mov" or op == "xor": whole.append(a); continue
    for b in (9, 10, 11):
        if v is None: continue
        if op == "or" and v & (1 << b): sets[b].append(a)
        if op == "and" and not (v & (1 << b)) and v <= 0xFFFF: clears[b].append(a)
unres = [a for a, (op, src) in writes.items() if op in ("or", "and") and not src.startswith("0x") and not src.isdigit()
         and a != 0x2BAA79 and trace(a, src) is None]
check("C", len(writes) > 40 and not unres, "%d writes; unresolved register sources: %s; whole-word/xor merges: %s"
      % (len(writes), ["%08X" % a for a in unres], ["%08X" % a for a in whole]))
wm = {**dis(0x2B642E, 0x2B6454), **dis(0x2B9E13, 0x2B9E39)}
xm = {a: dis(a - 4, a).get(a - 4) for a in (0x2B7ABB, 0x2B7AE9, 0x2BAEC5, 0x2BAEF3, 0x3CB996, 0x3CB9C4)}
check("C2", all(wm.get(a) == "and cx, 4" for a in (0x2B6446, 0x2B9E2B)) and dis(0x2BA0F1, 0x2BA112).get(0x2BA102) == "or ax, 3"
      and all(v in ("and ax, 0x40", "and ax, 0x30") for v in xm.values()),
      "the whole-word stores toggle bit 2 or add bits 0-1; the xor merges are masked to 0x40 / 0x30: no bit 9-11")
check("9", sets[9] == [0x2BB8BD] and clears[9] == [0x2B784E, 0x2BABE7]
      and dis(0x2B7844, 0x2B7849).get(0x2B7844) == "call 0x3c21b0" and dis(0x2BABDD, 0x2BABE2).get(0x2BABDD) == "call 0x3c21b0",
      "bit 9 set %s, cleared %s (each after the both-slots-empty test and 003C21B0)" % (["%08X" % a for a in sets[9]], ["%08X" % a for a in clears[9]]))
text_calls = lambda t: [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == t]
op10 = dis(0x28E660, 0x28E678)
check("10", sets[10] == [0x2B6249, 0x2BA011] and clears[10] == [] and text_calls(0x2BA000) == [0x28E673]
      and op10.get(0x28E664) == "mov edx, 5" and dis(0x2B6220, 0x2B6250).get(0x2B622E) == "mov edx, 5",
      "bit 10 set %s by the two mode-5 openers, never cleared" % ["%08X" % a for a in sets[10]])
check("11", sets[11] == [0x2BAA79] and clears[11] == [], "bit 11 set only %s, never cleared" % ["%08X" % a for a in sets[11]])
# MS-2
refs = []
for j in range(len(text) - 4):
    r = struct.unpack_from("<i", text, j)[0]
    for extra in (0, 1, 4):
        t = tb + j + 4 + extra + r
        if t in (0x2B45800, 0x2B45804):
            for back in range(7, 0, -1):
                ins = list(cs.disasm(text[j - back:j + 15], tb + j - back, 1))
                if ins and "rip" in ins[0].op_str and ins[0].address + ins[0].size == tb + j + 4 + extra:
                    refs.append((ins[0].address, ins[0].mnemonic, ins[0].op_str)); break
stores = [a for a, m, o in refs if o.startswith("dword ptr [rip")]
src = dis(0x3798AE, 0x3798DA)
check("O", stores == [0x3C6360, 0x3C6368] and text_calls(0x3C6360) == [0x3798D5]
      and src.get(0x3798B8) == "movss xmm0, dword ptr [rcx + 0x10]" and src.get(0x3798BD) == "movss xmm1, dword ptr [rcx + 0x14]",
      "02B45800/04 written only by 003C6360, called only from the NPS2 consumer with the record's origin +0x10/+0x14")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
