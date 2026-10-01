"""w5_inverted.py - W-5: what the "Inverted" render passes are for (FABLE, Claude Opus 5.5, 2026-09-27). Static + DATA.

  V1 each of the five Inverted name objects (CelInverted 02D37A60, MaterialPostEffectInverted 02D38000,
     RenderAtmosphereInverted 02D37FC0, RenderCameraMotionBlurInverted 02D376A0, RenderFXAAInverted 02D37860) is read,
     over a raw rip-displacement sweep of .text, by exactly its start-up initializer, one selector and one atexit stub.
  V2 all five selectors test the same thing: bit 1 of the dword at +0xC of the render-target descriptor they then bind
     (atmosphere 0065871B, cel 00658ABF, material 00659B48, motion blur 00659DE4, FXAA 0065A888).
  V3 each selector is called from slot 6 of one PhyreEngine post-effect class's vtable (RTTI class name read from the
     complete-object locator): PAtmospherics, PCelShading, PMaterialPostEffect, PMotionBlur, PFXAA.
  V4 only PFXAA is built by game code: its vtable writer 00645DB0 is called at 0018CFD5, and its selector is also
     called directly by game code (0065A630 <- 0018FDA8, 00191E38). The other four classes' vtables are written by one
     function each, and each of those has no rel32 caller and exactly one pointer (its class descriptor).
  V5 the image names 13 effect files (".fx.phyre" strings); none is an atmosphere, cel, material-post-effect or
     motion-blur effect, and PhyreFXAA.fx.phyre is one of them.
  V6 (DATA, skipped without D:/FFXII_TZA_extract) PhyreFXAA.fx.phyre carries the techniques RenderFXAA and RenderRGBL
     and no Inverted technique, and none of the shipped shader assets contains the string "Inverted". Positive
     control: RenderFXAA is found, in exactly that file.
Prints PASS/FAIL/SKIP per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def va(o):
    for vs, v, rs, ro in secs:
        if ro <= o < ro + rs: return BASE + v + o - ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
import bisect
FS = sorted(SIZES)
def owner(a):
    i = bisect.bisect_right(FS, a) - 1
    return FS[i] if i >= 0 and a < FS[i] + SIZES[FS[i]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
T0, TO, TS = [(BASE + v, ro, rs) for vs, v, rs, ro in secs if v == 0x1000][0]
tb = d[TO:TO + TS]
def rip_sites(targets):
    """raw sweep: every 4-byte displacement whose rip target (end of a 7-byte lea/mov) is in targets, confirmed by
    decoding the instruction that ends right after it."""
    out = {t: [] for t in targets}
    for i in range(3, len(tb) - 4):
        t = T0 + i + 4 + struct.unpack_from("<i", tb, i)[0]
        if t in out:
            for back in (3, 2):
                x = next(cs.disasm(tb[i - back:i + 4], T0 + i - back), None)
                if x and x.size == back + 4 and "rip" in x.op_str: out[t].append(T0 + i - back); break
    return out
def rel32_callers(t): return [T0 + i for i in range(len(tb) - 5) if tb[i] in (0xE8, 0xE9) and T0 + i + 5 + struct.unpack_from("<i", tb, i + 1)[0] == t]
def ptrs(t):
    p = struct.pack("<Q", t); r = []; i = d.find(p)
    while i >= 0: r.append(va(i)); i = d.find(p, i + 1)
    return r

NAMES = {0x2D37A60: ("CelInverted", 0x164BB0, 0x6587F0), 0x2D38000: ("MaterialPostEffectInverted", 0x164DF0, 0x659A90),
         0x2D37FC0: ("RenderAtmosphereInverted", 0x164F70, 0x658470), 0x2D376A0: ("RenderCameraMotionBlurInverted", 0x164FD0, 0x659C20),
         0x2D37860: ("RenderFXAAInverted", 0x1650F0, 0x65A640)}
sites = rip_sites(set(NAMES))
v1 = {}
for obj, (txt, init, sel) in NAMES.items():
    own = sorted({owner(s) for s in sites[obj]})
    atexit = [o for o in own if o not in (init, sel)]
    ok = len(sites[obj]) == 3 and init in own and sel in own and len(atexit) == 1 and 0x8B0000 <= atexit[0] < 0x8B1000
    # the initializer passes the literal text: lea rdx -> the string, then this object in rcx
    ini = dis(init, init + 0x20); lit = [int(m.group(1), 16) for v in ini.values() for m in [re.search(r"lea rdx, \[rip \+ (0x[0-9a-f]+)\]", v)] if m]
    ia = [a for a, v in ini.items() if v.startswith("lea rdx, [rip")]
    s = d[off(ia[0] + 7 + lit[0]):off(ia[0] + 7 + lit[0]) + 40].split(b"\0")[0].decode() if lit else None
    v1[txt] = ok and s == txt
check("V1 each Inverted name object has exactly three readers: its initializer, one selector, one atexit stub", all(v1.values()), str(v1))

TESTS = {0x65871B: 0x658470, 0x658ABF: 0x6587F0, 0x659B48: 0x659A90, 0x659DE4: 0x659C20, 0x65A888: 0x65A640}
v2 = {}
for a, sel in TESTS.items():
    w = dis(a, a + 8); ks = sorted(w); first = w.get(a, ""); second = w[ks[1]] if len(ks) > 1 else ""
    v2["%08X" % a] = bool(re.fullmatch(r"mov e(ax|di), dword ptr \[r(di|bx|bp|15) \+ 0xc\]", first)) and second in ("shr eax, 1", "shr edi, 1") and owner(a) == sel
check("V2 all five selectors test bit 1 of the descriptor's dword +0xC", all(v2.values()), str(v2))

def rtti_name(vt):
    col = struct.unpack_from("<Q", d, off(vt - 8))[0]
    td = BASE + struct.unpack_from("<I", d, off(col) + 12)[0]
    return d[off(td) + 16:off(td) + 96].split(b"\0")[0].decode()
SLOT6 = {0x658470: (0x65B270, 0xD628A0, ".?AVPAtmospherics@PPostProcessing@Phyre@@"),
         0x6587F0: (0x65B340, 0xD627B0, ".?AVPCelShading@PPostProcessing@Phyre@@"),
         0x659A90: (0x65B750, 0xD62940, ".?AVPMaterialPostEffect@PPostProcessing@Phyre@@"),
         0x659C20: (0x65B820, 0xD62170, ".?AVPMotionBlur@PPostProcessing@Phyre@@"),
         0x65A640: (0x65B590, 0xD625D0, ".?AVPFXAA@PPostProcessing@Phyre@@")}
v3 = {}
for sel, (meth, vt, nm) in SLOT6.items():
    cl = [owner(c) for c in rel32_callers(sel)]
    v3[nm.split("@")[0][4:]] = (meth in cl and struct.unpack_from("<Q", d, off(vt + 0x30))[0] == meth
                                and ptrs(meth) == [vt + 0x30] and rtti_name(vt) == nm)
check("V3 each selector is called from slot 6 of its PhyreEngine post-effect class (RTTI)", all(v3.values()), str(v3))

vsites = rip_sites({vt for _, vt, _ in SLOT6.values()})
fxaa_writers = sorted({owner(s) for s in vsites[0xD625D0]})
game_fxaa = [owner(c) for c in rel32_callers(0x645DB0)]
sel_fxaa_callers = sorted({owner(c) for c in rel32_callers(0x65A640)})
direct = [owner(c) for c in rel32_callers(0x65A630)]
four = {}
for sel, (meth, vt, nm) in SLOT6.items():
    if vt == 0xD625D0: continue
    w = sorted({owner(s) for s in vsites[vt]})
    four[nm.split("@")[0][4:]] = len(w) == 1 and rel32_callers(w[0]) == [] and len(ptrs(w[0])) == 1
check("V4 only PFXAA is built and driven by game code; the other four classes are reachable only through a class-descriptor pointer",
      0x645DB0 in fxaa_writers and game_fxaa == [0x18CD90] and 0x65A630 in sel_fxaa_callers and sorted(direct) == [0x18FD70, 0x191DA0]
      and all(four.values()), "fxaa writers %s; four %s" % (["%08X" % w for w in fxaa_writers], four))

fx = sorted(set(m.decode() for m in re.findall(rb"[ -~]{4,}\.fx\.phyre", d)))
bad = [f for f in fx if re.search(r"(?i)atmos|cel|material|motion", f)]
check("V5 the image names 13 effect files, none an atmosphere / cel / material / motion-blur effect; PhyreFXAA is one",
      len(fx) == 13 and bad == [] and any(f.endswith("/PhyreFXAA.fx.phyre") for f in fx), "%d names, bad %s" % (len(fx), bad))

SH = Path("D:/FFXII_TZA_extract/gamedata/d3d11/artdata/shaders")
if SH.exists():
    files = sorted(SH.iterdir()); fxaa = (SH / "phyrefxaa.fx.phyre").read_bytes()
    inv = [f.name for f in files if b"Inverted" in f.read_bytes()]
    rf = [f.name for f in files if b"RenderFXAA" in f.read_bytes()]
    check("V6 PhyreFXAA.fx.phyre has RenderFXAA and RenderRGBL and no Inverted technique; no shader asset contains 'Inverted'",
          b"RenderFXAA\0" in fxaa and b"RenderRGBL" in fxaa and inv == [] and rf == ["phyrefxaa.fx.phyre"] and len(files) == 99,
          "files %d, Inverted in %s, RenderFXAA in %s" % (len(files), inv, rf))
else:
    print("SKIP  V6 D:/FFXII_TZA_extract not present")
print("FAILS", fails)
sys.exit(1 if fails else 0)
