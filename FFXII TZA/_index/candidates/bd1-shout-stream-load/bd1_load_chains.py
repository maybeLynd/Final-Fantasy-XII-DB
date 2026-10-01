"""bd1_load_chains.py - control for BD-1 (FABLE, Claude Opus 5.5, 2026-09-26): what the Shout and Stream controllers load.

Checks:
  D1 the loader directory 0215F000: 002DF9A0 stores the table 01E127D0 in slot 33 (0215F108) and 01ECB7E0 in slot 39
     (0215F138). Their 64 entries are PS2Data\\sound\\shout\\us|jp\\shoutNN\\shoutNN.win.sab, NN = 00..63 in order.
  D2 no instruction reads either slot cell directly: every rip-relative access to 0215F108 / 0215F138 is 002DF9A0's store.
  D3 neither file-id decoder reaches those slots: 002ED6F0's type-letter arms give 12 other slots (planted negative:
     the arm table must decode, and slot 33 must not appear); 0032F170 gives 1, 5 or 8.
  D4 0036ED50 (the voice-pack load step of UQ-50) sizes and requests slot 0x21 and then slot 0x27 through
     0032E400 / 0032E620 for the entry's key word +0x14, keeping the two handles at +0xC / +0x10, with completion
     callbacks 0036EAB0 / 0036E9F0.
  D5 both callbacks call 002DF450 -> 001DC130 -> 00210B30 (the audio registry) -> 002111F0, which is
     `mov rcx, [rcx+0x20]; jmp 0021C680`: the controller at registry +0x20.
  D6 registry +0x20 is ShoutAudioController and +0x18 StreamAudioController: their constructors 0021BDB0 / 0021CC10
     install the vtables 00907FF0 / 00908200, which RTTI names.
  D7 the stream intake 001DC2E0 -> 00211270 is `mov rcx, [rcx+0x18]; jmp 0021D770`, and 002DF660's callers are the
     voice start 003E9C10, the BGM stream machine 003EADE0 and the bootstrap coordinator 003B8670.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, bisect
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, o + 8)[1:])
def off(v):
    for _, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
STARTS = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
                errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
def whole(a):
    i = bisect.bisect_right(STARTS, a)
    return list(cs.disasm(d[off(a):off(STARTS[i])], a))
def T(a): return ["%s %s" % (x.mnemonic, x.op_str) for x in whole(a)]
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
def q(v): return struct.unpack_from("<Q", d, off(v))[0]
def cstr(v): return d[off(v):off(v) + 200].split(b"\0")[0].decode("latin1")
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

# D1
REG = whole(0x2DF9A0)
def stored(cell):
    for a, b in zip(REG, REG[1:]):
        if a.mnemonic == "lea" and b.mnemonic == "mov" and rip(b) == cell and b.op_str.endswith("rax"): return rip(a)
tab = {33: stored(0x215F108), 39: stored(0x215F138)}
BS = "\\"
for slot, lang in ((33, "us"), (39, "jp")):
    names = [cstr(q(tab[slot] + 8 * k)) if tab[slot] else "" for k in range(64)]
    want = ["PS2Data%ssound%sshout%s%s%sshout%02d%sshout%02d.win.sab" % (BS, BS, BS, lang, BS, k, BS, k) for k in range(64)]
    check("D1 slot %d -> table %s, 64 entries shout\\%s\\shout00..63" % (slot, hex(tab[slot] or 0), lang), names == want,
          names[0] if names else "")
# D2
tva, trs, tro = [(va, rs, ro) for _, va, rs, ro in secs if va <= 0x1000 < va + rs][0]
from array import array
def rip_sites(cell):
    want = {cell - 4 - k - (BASE + tva) + tro: k for k in (0, 1, 2, 4)}
    cand = set()
    for s in range(4):
        a = array("i"); a.frombytes(d[tro + s: tro + s + ((trs - s) // 4) * 4])
        for i, v in enumerate(a):
            if v + tro + s + 4 * i in want: cand.add(BASE + tva + s + 4 * i)
    hits = {}
    for c in cand:
        f = STARTS[bisect.bisect_right(STARTS, c) - 1]
        for x in cs.disasm(d[off(f):off(c) + 16], f):
            if x.address <= c < x.address + x.size and rip(x) == cell: hits[x.address] = x
    return sorted(hits)
for cell in (0x215F108, 0x215F138):
    s = rip_sites(cell)
    check("D2 %08X: the only rip-relative access is 002DF9A0's store" % cell,
          len(s) == 1 and STARTS[bisect.bisect_right(STARTS, s[0]) - 1] == 0x2DF9A0, str([hex(v) for v in s]))
# D3
slots = set()
for code in range(0x43, 0x43 + 0x35):
    k = d[off(BASE + 0x1CD888 + code - 0x43)]
    tgt = BASE + struct.unpack_from("<I", d, off(BASE + 0x1CD854 + 4 * k))[0]
    for x in cs.disasm(d[off(tgt):off(tgt) + 0x40], tgt):
        m = re.match(r"edx, (0x[0-9a-f]+|\d+)$", x.op_str)
        if x.mnemonic == "mov" and m: slots.add(int(m.group(1), 0))
        if x.mnemonic in ("ret", "jmp"): break
check("D3 002ED6F0's arms decode (planted: slot 15 for 'C' must appear) and never give 33 or 39",
      15 in slots and not ({33, 39} & slots), str(sorted(slots)))
t3 = T(0x32F170)
check("D3 0032F170 gives slots 1, 8, 5 only", [s for s in t3 if s.startswith("mov dword ptr [r8], ")] ==
      ["mov dword ptr [r8], 1", "mov dword ptr [r8], 8", "mov dword ptr [r8], 5"])
# D4
L = T(0x36ED50)
seq = [s for s in L if s in ("mov ecx, 0x21", "lea ecx, [r12 + 0x21]", "mov ecx, 0x27", "call 0x32e400", "call 0x32e620")]
check("D4 0036ED50: size+request slot 0x21, then size+request slot 0x27",
      seq == ["mov ecx, 0x21", "call 0x32e400", "lea ecx, [r12 + 0x21]", "call 0x32e620",
              "mov ecx, 0x27", "call 0x32e400", "mov ecx, 0x27", "call 0x32e620"], str(seq))
cb = [rip(x) for x in whole(0x36ED50) if x.mnemonic == "lea" and rip(x) in (0x36EAB0, 0x36E9F0)]
check("D4 key +0x14, handles +0xC / +0x10, callbacks 0036EAB0 then 0036E9F0",
      "movsx r15, word ptr [rcx + 0x14]" in L and "mov dword ptr [rdi + 0xc], ebx" in L
      and "mov dword ptr [rdi + 0x10], ebx" in L and cb == [0x36EAB0, 0x36E9F0])
# D5
for c in (0x36EAB0, 0x36E9F0):
    check("D5 callback %08X calls 002DF450" % c, "call 0x2df450" in T(c))
check("D5 002DF450 -> 001DC130 -> 00210B30, 002111F0", T(0x2DF450)[:1] == ["jmp 0x1dc130"]
      and "call 0x210b30" in T(0x1DC130) and "call 0x2111f0" in T(0x1DC130))
check("D5 002111F0 = mov rcx, [rcx+0x20]; jmp 0021C680", T(0x2111F0)[:2] == ["mov rcx, qword ptr [rcx + 0x20]", "jmp 0x21c680"])
# D6
def installs(ctor, vt): return any(x.mnemonic == "lea" and rip(x) == vt for x in whole(ctor))
def rtti(vt):
    col = q(vt - 8); td = BASE + struct.unpack_from("<I", d, off(col) + 12)[0]
    return cstr(td + 16)
check("D6 0021BDB0 installs 00907FF0 = ShoutAudioController; 0021CC10 installs 00908200 = StreamAudioController",
      installs(0x21BDB0, 0x907FF0) and installs(0x21CC10, 0x908200)
      and rtti(0x907FF0) == ".?AVShoutAudioController@@" and rtti(0x908200) == ".?AVStreamAudioController@@",
      "%s %s" % (rtti(0x907FF0), rtti(0x908200)))
# D7
check("D7 001DC2E0 -> 00211270 = mov rcx, [rcx+0x18]; jmp 0021D770",
      "call 0x211270" in T(0x1DC2E0) and T(0x211270)[:2] == ["mov rcx, qword ptr [rcx + 0x18]", "jmp 0x21d770"])
callers = set()
p = tro
while True:
    p = d.find(b"\xe8", p, tro + trs)
    if p < 0: break
    va_ = BASE + tva + p - tro
    if va_ + 5 + struct.unpack_from("<i", d, p + 1)[0] == 0x2DF660:
        f = STARTS[bisect.bisect_right(STARTS, va_) - 1]
        if any(x.address == va_ and x.mnemonic == "call" for x in cs.disasm(d[off(f):off(va_) + 5], f)): callers.add(f)
    p += 1
check("D7 002DF660's callers are 003B8670, 003E9C10, 003EADE0", sorted(callers) == [0x3B8670, 0x3E9C10, 0x3EADE0],
      str(["%08X" % c for c in sorted(callers)]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
