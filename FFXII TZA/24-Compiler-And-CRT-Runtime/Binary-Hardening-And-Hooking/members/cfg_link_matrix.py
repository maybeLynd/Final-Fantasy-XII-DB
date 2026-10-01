"""cfg_link_matrix.py - S-2 by reconstruction: which MSVC compile/link flags reproduce this image's CFG header signature
(FABLE, Claude Opus 5.5, 2026-09-26). Evidence class: RECONSTRUCTION with the local toolchain, kept separate from the
page's static reading.

The shipped signature, read by debug_directory.py and the load config, is:
- DllCharacteristics 0x8120 (no DYNAMIC_BASE, no GUARD_CF);
- GuardFlags 0x00000100 (CF_INSTRUMENTED alone);
- GuardCFFunctionTable 0 and GuardCFFunctionCount 0.
This script compiles one C file that holds an address-taken function table, twice: with /guard:cf and without it. It
links seven ways and reads each result's headers.
  X1 a guard-compiled object linked WITHOUT /guard:cf and with /DYNAMICBASE:NO reproduces the signature exactly.
  X2 a NON-guard object linked the same way also reproduces it. CF_INSTRUMENTED comes from the CRT's own guard-aware
     objects, not from the game's code. This agrees with VC_FEATURE's 49 guard-aware objects out of 1,296, and with
     section 9a: only the static CRT consults the guard slot.
  X3 /guard:cf at link time with /DYNAMICBASE:NO still builds a function table and sets GUARD_CF, from either object.
     Switching ASLR off does not empty the table, so the 2026-09-22 model ("/guard:cf with ASLR disabled") does not
     reproduce the image.
  X4 controls:
     - /guard:cf with the default link builds a table and sets GUARD_CF;
     - the plain default link sets DYNAMIC_BASE (0x8160), so /DYNAMICBASE:NO is what clears 0x40;
     - the DLL CRT (msvcrt.lib) gives the same signature as the static CRT.
Limit, stated: the game was linked by linker 14.0 (Rich header: build 24215, VS2015 Update 3); this runs whatever
vcvars64 provides (printed). The one visible version difference is the .gfids section. The game's linker merged the
objects' .gfids$y input into it unconverted (debug_directory.py D3), while the local linker drops that input in a
non-/guard:cf link. Both are what a link that did not process CFG would do.
Usage: python cfg_link_matrix.py [path-to-vcvars64.bat]. Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import os, struct, subprocess, sys, tempfile
VCVARS = sys.argv[1] if len(sys.argv) > 1 else r"C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
if not os.path.exists(VCVARS):
    check("toolchain present", False, VCVARS); print("FAILS", fails); sys.exit(1)
W = tempfile.mkdtemp(prefix="cfgmatrix_")
open(os.path.join(W, "t.c"), "w").write(
    "static int f1(int x){return x+1;}\nstatic int f2(int x){return x*2;}\n"
    "int (*tbl[2])(int) = {f1, f2};\nint main(int argc, char**argv){ return tbl[argc&1](argc); }\n")
LINKS = {  # name: (object, link flags)
 "A": ("tg.obj", "/DYNAMICBASE:NO"),
 "F": ("tn.obj", "/DYNAMICBASE:NO"),
 "G": ("tn.obj", "/DYNAMICBASE:NO /NODEFAULTLIB:libcmt.lib msvcrt.lib"),
 "B": ("tg.obj", "/guard:cf /DYNAMICBASE:NO"),
 "E": ("tn.obj", "/guard:cf /DYNAMICBASE:NO"),
 "C": ("tg.obj", ""),
 "D": ("tg.obj", "/guard:cf"),
}
bat = ['@echo off', 'call "%s" >nul 2>nul' % VCVARS, "cd /d \"%s\"" % W,
       "cl /nologo /c /O2 /guard:cf t.c /Fotg.obj >nul", "cl /nologo /c /O2 t.c /Fotn.obj >nul"]
bat += ["link /nologo %s /OUT:%s.exe %s >%s.txt 2>&1" % (o, n, f, n) for n, (o, f) in LINKS.items()]
bat += ["link 2>&1 | findstr /C:\"Linker Version\" > ver.txt"]
open(os.path.join(W, "m.bat"), "w").write("\r\n".join(bat) + "\r\n")
subprocess.run(["cmd", "/c", os.path.join(W, "m.bat")], capture_output=True)
ver = open(os.path.join(W, "ver.txt")).read().strip() if os.path.exists(os.path.join(W, "ver.txt")) else "?"
print("   toolchain:", ver)
def hdr(p):
    d = open(p, "rb").read(); pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
    osz = struct.unpack_from("<H", d, pe + 20)[0]; opt = pe + 24
    dllc = struct.unpack_from("<H", d, opt + 70)[0]
    secs = [struct.unpack_from("<IIII", d, pe + 24 + osz + i * 40 + 8) for i in range(n)]
    def off(rva):
        for vs, va, rs, ro in secs:
            if va <= rva < va + max(vs, rs): return rva - va + ro
    lc = off(struct.unpack_from("<I", d, opt + 112 + 80)[0])
    tbl, cnt = struct.unpack_from("<QQ", d, lc + 0x80); fl = struct.unpack_from("<I", d, lc + 0x90)[0]
    return dllc, fl, tbl, cnt
H = {}
for n in LINKS:
    p = os.path.join(W, n + ".exe")
    H[n] = hdr(p) if os.path.exists(p) else None
    print("   %s %-48s %s" % (n, "%s %s" % LINKS[n], ("dllchar %04X GuardFlags %08X table %X count %d" % H[n]) if H[n] else "NOT BUILT"))
SIG = lambda h: h is not None and h[0] == 0x8120 and h[1] == 0x100 and h[2] == 0 and h[3] == 0
check("X1 guard-compiled object, no /guard:cf link, /DYNAMICBASE:NO: 0x8120 / 0x100 / table 0", SIG(H["A"]))
check("X2 the same from a NON-guard object, static and DLL CRT: CF_INSTRUMENTED comes from the CRT", SIG(H["F"]) and SIG(H["G"]))
tbl_on = lambda h: h is not None and h[0] & 0x4000 and h[3] > 0
check("X3 /guard:cf link with /DYNAMICBASE:NO still builds a table and sets GUARD_CF", tbl_on(H["B"]) and tbl_on(H["E"]))
check("X4 controls: /guard:cf default builds a table; the plain default sets DYNAMIC_BASE",
      tbl_on(H["D"]) and H["C"] is not None and H["C"][0] & 0x40 and not H["C"][0] & 0x4000)
print("FAILS", fails)
sys.exit(1 if fails else 0)
