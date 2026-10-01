"""hp_lethal_checks.py - PKG-GP-HP-LETHAL: the bytes behind four stale-text corrections (FABLE, Claude Opus 5.5, 2026-09-28).
STATIC, certified image; nothing executed. Each check rejects the wording it corrects.

  S  SECOND HP STORE (G1): the status transition 0030E360 calls the stat recompute 0030FED0 (0030E828), whose body stores
     [unit + 0x48] at 00310508 (the same field 00300749 writes), after its own cap computation (003104E8..00310506:
     max HP +0x24, doubled on bit 28). So "00300749 is the only write of current HP on this path" is false for the path.
  E  00469BB0 (G2): it posts event 0x10 through the battle event poster 0046AB10 (mov edx, 0x10 / call at 00469BF2).
     "What 00469BB0 is: not established" is rejected.
  R  THE REWARDS TAIL (G8): 00312280's last call before the stack-cookie check is 00317090 (003125BC), which tail-jumps to
     00253770 with ecx = 0x11 and its amount from the reward rows +0xE70 / +0xE78; 00253770 is `jmp 00316A50`, the achievement
     counter update. Nothing after the drop placement (00319CA0 at 003125B4) retires or frees the unit, so "retire the unit"
     and "closes the record" are rejected.
  K  G7: the status word has exactly the 32 statuses of the-thirty-two-statuses page (read from that page's table); none
     is a revive-on-KO status (checked by name). This is a text check of the canonical table, not of the image.
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(DB, "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
SZ = {}
def dis(a, b):
    o = {}
    for x in cs.disasm(d[off(a):off(b)], a): o[x.address] = ("%s %s" % (x.mnemonic, x.op_str)).strip(); SZ[x.address] = x.size
    return o
def covered(c, lo, hi):
    a = lo
    while a < hi:
        if a not in c: return False
        a += SZ[a]
    return True
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())

st = dis(0x30E360, 0x30F200); fe = dis(0x3104E8, 0x31050E); hp = dis(0x300740, 0x300750)
check("S", st.get(0x30E828) == "call 0x30fed0" and at(fe, {0x3104FD: "mov eax, dword ptr [rbx + 0x24]", 0x310500: "bt edx, 0x1c",
      0x310506: "add eax, eax", 0x310508: "mov dword ptr [rbx + 0x48], eax"}) and "[r" in hp.get(0x300749, "") and "+ 0x48]" in hp.get(0x300749, ""),
      "0030E828 %r; 00310508 %r; 00300749 %r - two stores of +0x48 on the lethal path" % (st.get(0x30E828), fe.get(0x310508), hp.get(0x300749)))
ev = dis(0x469BE6, 0x469BF7)
check("E", at(ev, {0x469BEA: "mov edx, 0x10", 0x469BF2: "call 0x46ab10"}), "00469BB0 posts event 0x10 via 0046AB10: %s" % at(ev, {0x469BEA: "mov edx, 0x10", 0x469BF2: "call 0x46ab10"}))
tail = dis(0x3125B4, 0x3125D9); ach = dis(0x317090, 0x3170DE); jmp = dis(0x253770, 0x253775)
calls_after_drop = [tail[a] for a in sorted(tail) if a > 0x3125B4 and tail[a].startswith("call")]
check("R", at(ach, {0x3170BA: "mov rax, qword ptr [rcx + 0xe78]", 0x3170C4: "mov rax, qword ptr [r8 + 0xe70]", 0x3170D3: "mov ecx, 0x11",
      0x3170D8: "jmp 0x253770"}) and jmp.get(0x253770) == "jmp 0x316a50" and calls_after_drop == ["call 0x317090", "call 0x808c40"]
      and covered(tail, 0x3125B4, 0x3125D9) and tail.get(0x3125D8) == "ret",
      "calls after the drop spawn: %s (0x808c40 = the stack-cookie check); 00317090 -> 00253770(0x11, ...) -> %s" % (calls_after_drop, jmp.get(0x253770)))
page = open(os.path.join(DB, "10-Status-Periodic-Terminal", "the-thirty-two-statuses.md"), encoding="utf-8").read()
rows = re.findall(r"^\| (\d+) \| ([^|]+?) \| ", page, re.M)
first = {}
for i, nm in rows:
    first.setdefault(int(i), nm.strip())
names = [first[i] for i in range(32)] if len(first) >= 32 else []
revive = [nm for nm in names if re.search(r"reraise|auto-?life|revive|renew", nm, re.I)]
check("K", len(names) == 32 and names[0] == "KO" and names[31] == "X-Zone" and not revive,
      "32 statuses %s .. %s; revive-on-KO names among them: %s" % (names[:1], names[-1:], revive))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
