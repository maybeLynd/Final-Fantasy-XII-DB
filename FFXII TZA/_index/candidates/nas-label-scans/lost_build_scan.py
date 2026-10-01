"""lost_build_scan.py - requirement 3 for the LOST-BUILD rows of NO ADMISSIBLE SOURCE package 2 (B-2/d, BS-5, UQ-36,
UQ-39): does anything shipped carry the build artefacts that would answer them? (FABLE, Claude Opus 5.5, 2026-09-26)

The shipped set is:
- the retail files in the install's x64 folder (the twelve dated with the game, listed below);
- FileSizeTables/ and ConfigData/;
- the full nine-language extract of FFXII_TZA.vbf (D:/FFXII_TZA_extract).
The mod's own files (dinput8.dll, the trampoline, modules/, scripts/, hook.*) are excluded, except as a control.
  L1 no build artefact ships. No file has a build-output extension (.pdb .map .obj .o .lib .a .exp .ilk .elf .irx), and
     no file begins with a PDB, ELF, COFF-archive or MSVC-object signature.
     Control (sensitivity): the same detector, pointed at the mod's modules/ folder, finds XIIOnlineNet.pdb by its
     magic.
  L2 the one PDB the image names (its RSDS record: ...\\x64_Retail\\FF12X64.pdb) is nowhere in the shipped set. The
     name occurs in FFXII_TZA.exe's RSDS record (control) and as no file name.
  L3 only retail executables ship. The x64 folder's executables are FFXII_TZA.exe and FFXII_TZA_GameSetting.exe; the
     extract holds no PE image (MZ...PE) at all. There is no debug or PS2 build of the game.
  L4 no PS2 SDK or EASTL version identifier is in the image. There are zero strings beginning "sce", zero "libvu0",
     zero "EASTL_VERSION", and the image's eight eastl strings carry no version number.
     Control: the same string pass finds the eight eastl strings, and zlib's own "1.2.11".
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
INSTALL = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII MP Mod/FFXII_TestClient1")
EXTRACT = Path(sys.argv[2] if len(sys.argv) > 2 else "D:/FFXII_TZA_extract")
RETAIL = ["CSteamworks.dll", "FFXII_TZA.exe", "FFXII_TZA_GameSetting.exe", "SettingsLoc.xml", "SharpDX.DXGI.dll",
          "SharpDX.DirectInput.dll", "SharpDX.dll", "Steamworks.NET.dll", "d3dcompiler_47.dll", "steam_api.dll",
          "steam_api64.dll", "xinput1_3.dll"]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
if not (INSTALL / "x64").exists() or not EXTRACT.exists():
    check("inputs present", False, "%s / %s" % (INSTALL, EXTRACT)); print("FAILS", fails); sys.exit(1)
EXT = {".pdb", ".map", ".obj", ".o", ".lib", ".a", ".exp", ".ilk", ".elf", ".irx"}
SIGS = [(b"Microsoft C/C++ MSF 7.00", "pdb"), (b"\x7fELF", "elf"), (b"!<arch>\n", "archive")]
def sniff(p):
    try:
        with open(p, "rb") as f: h = f.read(32)
    except OSError: return None
    for sig, nm in SIGS:
        if h.startswith(sig): return nm
    if len(h) >= 4 and h[:2] in (b"\x64\x86", b"\x4c\x01") and h[2:4] != b"\x00\x00" and p.suffix.lower() in (".obj", ".o", ""):
        return "coff-obj"
    return None
shipped = [INSTALL / "x64" / f for f in RETAIL if (INSTALL / "x64" / f).exists()]
for sub in ("FileSizeTables", "ConfigData"):
    shipped += [Path(dp) / f for dp, dn, fn in os.walk(INSTALL / sub) for f in fn]
shipped += [Path(dp) / f for dp, dn, fn in os.walk(EXTRACT) for f in fn]
bad_ext = [str(p) for p in shipped if p.suffix.lower() in EXT]
bad_sig = [(str(p), s) for p in shipped for s in [sniff(p)] if s]
pe = []
for p in shipped:
    if p.parent == INSTALL / "x64": continue
    try:
        with open(p, "rb") as f: h = f.read(0x40)
        if h[:2] == b"MZ" and len(h) >= 0x40:
            with open(p, "rb") as f:
                f.seek(int.from_bytes(h[0x3C:0x40], "little"));
                if f.read(4) == b"PE\0\0": pe.append(str(p))
    except OSError: pass
print("   shipped files scanned: %d (x64 retail %d)" % (len(shipped), sum(1 for p in shipped if p.parent == INSTALL / "x64")))
check("L1 no build artefact ships (extension or signature)", not bad_ext and not bad_sig and len(shipped) > 80000,
      "ext %s sig %s" % (bad_ext[:3], bad_sig[:3]))
mod = [(p.name, sniff(p)) for p in (INSTALL / "x64" / "modules").iterdir() if p.is_file()]
check("L1 control: the detector finds the mod's own PDB by its magic", ("XIIOnlineNet.pdb", "pdb") in mod, str([m for m in mod if m[1]]))
exe = (INSTALL / "x64" / "FFXII_TZA.exe").read_bytes()
check("L2 FF12X64.pdb is named in the exe's RSDS record and ships as no file",
      exe.count(b"\\x64_Retail\\FF12X64.pdb") == 1 and not any(p.name.lower() == "ff12x64.pdb" for p in shipped))
exes = sorted(p.name for p in shipped if p.parent == INSTALL / "x64" and p.suffix.lower() == ".exe")
check("L3 only the two retail executables ship, and the extract holds no PE image",
      exes == ["FFXII_TZA.exe", "FFXII_TZA_GameSetting.exe"] and pe == [], "%s; PE in extract %s" % (exes, pe[:3]))
strs = [m.group(1) for m in re.finditer(rb"([\x20-\x7e]{4,120})\x00", exe)]
sce = [s for s in strs if s.startswith(b"sce")]
eastl = [s for s in strs if re.search(rb"eastl", s, re.I)]
check("L4 no sce* string, no libvu0, no EASTL_VERSION, and no version number in the eight eastl strings",
      sce == [] and exe.count(b"libvu0") == 0 and exe.count(b"EASTL_VERSION") == 0 and len(eastl) == 8
      and not any(re.search(rb"\d+\.\d+", s) for s in eastl), "%d eastl strings" % len(eastl))
check("L4 control: the string pass finds zlib's own version", exe.count(b"1.2.11") >= 1)
print("FAILS", fails)
sys.exit(1 if fails else 0)
