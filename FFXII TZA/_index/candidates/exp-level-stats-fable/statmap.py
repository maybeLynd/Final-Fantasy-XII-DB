"""statmap.py - PKG-GP-EXP-LEVEL-UP E4: which named attribute each of the four f32 base stats becomes
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC, read from BattleStats_RebuildEffectiveStatsAndAffinityState (002FEF30).

  R  THE OUTPUT BASE: rdi = the stats record (rcx); rsi = the caller's block (rdx), or `lea rsi, [rdi + 0x24]` when it is
     null (002FEFAB). The same block receives max HP at [rsi] (clamped 0x7FFF, 002FF805) and max MP at [rsi + 4] (clamped
     999, 002FF824), which are the field map's +0x24 / +0x28 - so rsi + k is record + 0x24 + k on the default path
  F  THE FOUR FLOATS: `cvttss2si` reads +0x10 into r12d (002FF0C2), +0x14 into r13d (002FF0CD), +0x18 into r8d then the
     slot [rsp + 0x2c] (002FF099 / 002FF0BD), +0x1C into r9d then the slot [rsp + 0x30] (002FF0B7 / 002FF0C8)
  S  THE STORES, each clamped to [.. , 99] (r15d = 0x63 at 002FF829): r12b -> [rsi + 6] (002FF840), r13b -> [rsi + 7]
     (002FF85A), the [rsp + 0x2c] value -> [rsi + 8] (002FF874), the [rsp + 0x30] value -> [rsi + 9] (002FF88E);
     the next three stores ([rsi + 0xA .. 0xC]) clamp to 255 instead
  So on the default path: +0x10 -> +0x2A Strength, +0x14 -> +0x2B Magick Power, +0x18 -> +0x2C Vitality, +0x1C -> +0x2D
  Speed (the attack page's names; Strength and Magick Power confirmed there by the Reduce*To70Percent writers, Vitality and
  Speed from function names only). Equipment and licence bonuses are added to the same four accumulators in between.
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
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
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
# decode the whole body from its entry, so no listing starts mid-instruction
body = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in cs.disasm(d[off(0x2FEF30):off(0x2FEF30) + 0xB2B], 0x2FEF30)}
at = lambda w: [a for a, s in w.items() if body.get(a) != s]
r = at({0x2FEF63: "mov rsi, rdx", 0x2FEF6B: "mov rdi, rcx", 0x2FEFAB: "lea rsi, [rdi + 0x24]",
        0x2FF7F5: "mov r9d, 0x7fff", 0x2FF805: "mov dword ptr [rsi], r15d", 0x2FF817: "mov r9d, 0x3e7", 0x2FF824: "mov word ptr [rsi + 4], r8w"})
check("R", not r, "rsi = rdi + 0x24 by default; max HP at [rsi] (<= 0x7FFF), max MP at [rsi + 4] (<= 999)%s" % (" MISMATCH %s" % r if r else ""))
f = at({0x2FF0C2: "cvttss2si r12d, dword ptr [rdi + 0x10]", 0x2FF0CD: "cvttss2si r13d, dword ptr [rdi + 0x14]",
        0x2FF099: "cvttss2si r8d, dword ptr [rdi + 0x18]", 0x2FF0BD: "mov dword ptr [rsp + 0x2c], r8d",
        0x2FF0B7: "cvttss2si r9d, dword ptr [rdi + 0x1c]", 0x2FF0C8: "mov dword ptr [rsp + 0x30], r9d"})
check("F", not f, "the four f32 reads and their accumulators%s" % (" MISMATCH %s" % f if f else ""))
s = at({0x2FF829: "mov r15d, 0x63", 0x2FF83C: "cmovg r12d, r15d", 0x2FF840: "mov byte ptr [rsi + 6], r12b",
        0x2FF851: "cmovg r13d, r15d", 0x2FF85A: "mov byte ptr [rsi + 7], r13b",
        0x2FF855: "mov r8d, dword ptr [rsp + 0x2c]", 0x2FF86B: "cmovg r8d, r15d", 0x2FF874: "mov byte ptr [rsi + 8], r8b",
        0x2FF86F: "mov r9d, dword ptr [rsp + 0x30]", 0x2FF885: "cmovg r9d, r15d", 0x2FF88E: "mov byte ptr [rsi + 9], r9b",
        0x2FF8D6: "mov r11d, 0xff", 0x2FF8F2: "mov byte ptr [rsi + 0xa], r8b"})
check("S", not s, "stores [rsi + 6..9] clamp to 99; [rsi + 0xA..] to 255%s" % (" MISMATCH %s" % s if s else ""))
# K: on the PARTY path the accumulators are only added to between read and store. The party arm ends with
# `jmp 0x2ff3d0` at 002FF0DC; the code in [002FF0E1, 002FF3D0) is the enemy arm, which fills the same accumulators
# from its row bytes (so they carry the same meaning). From 002FF3D0 to the stores, every write is an add (bonuses), or
# the clamp's own `mov ..., ebp` for a negative value.
import re
acc = r"(r12d?|r13d?|dword ptr \[rsp \+ 0x(2c|30)\])"
tail = sorted((a, t) for a, t in body.items() if 0x2FF3D0 <= a < 0x2FF88E and re.match(r"\w+ " + acc + ",", t))
bad = [(a, t) for a, t in tail if not (t.startswith("add ") or t.endswith(", ebp") or t.startswith(("cmp ", "test ", "cmovg ")))]
check("K", body.get(0x2FF0DC) == "jmp 0x2ff3d0" and not bad and any(t.startswith("add r12d") for a, t in tail),
      "party arm jumps to 002FF3D0; from there the accumulators see only adds before their stores: %s"
      % (["%08X %s" % w for w in tail] if not bad else "BAD %s" % bad))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
