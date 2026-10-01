"""vp8_lifetime.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. The release cells of VpxVp8DecoderContext
('vp8_destroy 0016E210 (not read here)') and Vp8DecoderInstance ('not read here'), read from the bytes:

  V1 vp8_destroy 0016E210: when ctx+0x1A8 (useFrameThreads) is zero and pbi = ctx+0x1B0 is non-null, it calls 00171790(pbi,
     pbi+0x1E74 mbRows) when pbi+0x4380 is non-zero, then 00172160(pbi), then 00172750(pbi + 0x12C0), then frees the
     vpx_memalign original pointer [pbi-8] through the CRT free import (IAT 008C2B48); then it frees [ctx-8] the same way and
     returns 0. With useFrameThreads non-zero only the context is freed (the frame-thread arm is compiled out); its only
     writer stores 0 (the field row), so pbi[0] is released whenever it exists
  V2 vpx_codec_destroy 0016DDD0: null ctx -> 8; iface (+0x08) or priv (+0x30) null -> err 1; otherwise it calls
     iface+0x18 (the interface slot holding 0016E210) on priv, then nulls +0x08, +0x00, +0x30 and stores err 0
  V3 its direct callers are exactly two: 0016DFB0, the failure arm after iface+0x10 (init) returns non-zero (0016DF93 /
     0016DF9B), and 0067AAAB inside the channel teardown 0067A9B0, on the codec context at +0x2A8 of the channel
  V4 the only image qword equal to 0016E210 is the interface slot 01CDB2A8 (01CDB290 + 0x18)
  Not established: when 0067A9B0 runs in play, what 00171790 / 00172160 / 00172750 each release in full.
  S  REGRESSION: neither release cell still reads 'not read here' (FAILS before the patch)
Usage: python vp8_lifetime.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
FREE = 0x8C2B48
v1 = (at(0x16E216)[:2] == ("cmp", "dword ptr [rcx + 0x1a8], 0") and at(0x16E220)[:2] == ("jne", "0x16e26d")
      and at(0x16E227)[:2] == ("mov", "rbx, qword ptr [rcx + 0x1b0]") and at(0x16E231)[:2] == ("je", "0x16e268")
      and at(0x16E233)[:2] == ("cmp", "dword ptr [rbx + 0x4380], 0") and at(0x16E23A)[:2] == ("je", "0x16e24a")
      and at(0x16E23C)[:2] == ("mov", "edx, dword ptr [rbx + 0x1e74]") and at(0x16E245)[:2] == ("call", "0x171790")
      and at(0x16E24D)[:2] == ("call", "0x172160") and at(0x16E252)[:2] == ("lea", "rcx, [rbx + 0x12c0]")
      and at(0x16E259)[:2] == ("call", "0x172750") and at(0x16E25E)[:2] == ("mov", "rcx, qword ptr [rbx - 8]")
      and at(0x16E262)[2] == FREE and at(0x16E272)[:2] == ("mov", "rcx, qword ptr [rdi - 8]") and at(0x16E276)[2] == FREE
      and at(0x16E27C)[:2] == ("xor", "eax, eax") and at(0x16E283)[0] == "ret")
check("V1", v1, "vp8_destroy 0016E210 releases pbi (00171790 when +0x4380, 00172160, 00172750(+0x12C0), free [pbi-8]) then frees [ctx-8]")
v2 = (at(0x16DDD9)[:2] == ("test", "rcx, rcx") and at(0x16DDDE)[:2] == ("lea", "eax, [rcx + 8]")
      and at(0x16DDE7)[:2] == ("mov", "rax, qword ptr [rcx + 8]") and at(0x16DDF0)[:2] == ("mov", "rcx, qword ptr [rcx + 0x30]")
      and at(0x16DDF9)[:2] == ("call", "qword ptr [rax + 0x18]") and at(0x16DDFE)[:2] == ("mov", "qword ptr [rbx + 8], rax")
      and at(0x16DE02)[:2] == ("mov", "qword ptr [rbx], rax") and at(0x16DE05)[:2] == ("mov", "qword ptr [rbx + 0x30], rax")
      and at(0x16DE09)[:2] == ("mov", "dword ptr [rbx + 0x10], eax") and at(0x16DE12)[:2] == ("mov", "eax, 1"))
check("V2", v2, "vpx_codec_destroy 0016DDD0 calls iface+0x18 on priv (+0x30) and nulls the context")
text = next(s for s in SECS if s[0] == b".text"); tlo = B + text[2]
callers = []
for i in range(off(tlo), off(tlo) + text[3] - 5):
    if d[i] in (0xE8, 0xE9):
        v = tlo + i - off(tlo)
        if v + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x16DDD0:
            try:
                x = next(cs.disasm(d[i:i + 5], v))
                if x.mnemonic in ("call", "jmp"): callers.append(v)
            except StopIteration: pass
v3 = (callers == [0x16DFB0, 0x67AAAB] and at(0x16DF93)[:2] == ("call", "qword ptr [r10 + 0x10]") and at(0x16DF9B)[:2] == ("je", "0x16dfbc")
      and at(0x16DFA9)[:2] == ("mov", "rcx, rdi") and at(0x67AA9D)[:2] == ("lea", "rcx, [rdi + 0x2a8]") and 0x67A9B0 < 0x67AAAB < 0x67A9B0 + 390)
check("V3", v3, "direct callers of 0016DDD0: %s (init-failure arm; channel teardown 0067A9B0 on +0x2A8)" % ["%08X" % c for c in callers])
q = struct.pack("<Q", 0x16E210); hits = []; i = d.find(q)
while i >= 0:
    for nm, vs, va, rs, ro in SECS:
        if ro <= i < ro + rs: hits.append(B + va + i - ro)
    i = d.find(q, i + 1)
check("V4", hits == [0x1CDB2A8] and struct.unpack_from("<Q", d, off(0x1CDB2A0))[0] == 0x16E110,
      "qwords equal to 0016E210: %s (interface 01CDB290 +0x18, after init at +0x10)" % ["%08X" % h for h in hits])
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/vp8-decoder-lifetime/vp8_lifetime.py"
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
CTX = ("vp8_destroy 0016E210 - READ 2026-09-28 (OPUS, %s V1-V4): frees the context's vpx_memalign original pointer [ctx-8] through "
       "the CRT free import (0016E276), after releasing pbi[0] (Vp8DecoderInstance) when useFrameThreads +0x1A8 is zero. Reached only "
       "through the interface slot 01CDB290+0x18, called by vpx_codec_destroy 0016DDD0 (0016DDF9), which then nulls the codec "
       "context's iface/name/priv; 0016DDD0 has two direct callers - the init-failure arm 0016DFB0 and the channel teardown "
       "0067A9B0 (0067AAAB, on its +0x2A8 codec context). When that teardown runs in play is not established" % REC)
INST = ("vp8_destroy 0016E210 - READ 2026-09-28 (OPUS, %s V1-V3): with the context's useFrameThreads zero (its only writer stores "
        "0) and pbi[0] non-null, it calls 00171790(pbi, mbRows +0x1E74) when +0x4380 is non-zero, then 00172160(pbi), then "
        "00172750(pbi + 0x12C0), then frees the vpx_memalign original pointer [pbi-8] (0016E262); the instance dies with its "
        "decoder context (see VpxVp8DecoderContext). What each of the three callees releases in full is not established here" % REC)
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "VpxVp8DecoderContext" and c[6] == "vp8_destroy 0016E210 (not read here)":
            c[6] = "~~vp8_destroy 0016E210 (not read here)~~ " + CTX; tl[i] = "\t".join(c) + e
        if c[0] == "Vp8DecoderInstance" and c[6] == "not read here":
            c[6] = "~~not read here~~ " + INST; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
t = {cells(l)[0]: cells(l) for l in tl}
ok = all(REC in t[k][6] and not re.sub(r"~~.*?~~", "", t[k][6]).strip().lower().startswith(("not read", "vp8_destroy 0016e210 (not read"))
         for k in ("VpxVp8DecoderContext", "Vp8DecoderInstance"))
check("S", ok, "both release cells are read (no longer 'not read here')")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
