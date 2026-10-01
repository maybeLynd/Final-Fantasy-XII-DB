"""pc1_route.py - PC-1: FF12CONFIG is read from the FFXII_TZA.vbf archive entry (or the RAM cache's copy of it); the
stream resolver has no loose-file route (FABLE, Claude Opus 5.5, 2026-09-27). Static read of the authorised exe.

  R1 the config loader 00408C30 opens "PS2Data/SQUARE_FF12/FF12CONFIG" (00D121D8) with 001D6F20(path, 1) (00408C88).
  R2 001D6F20 builds the 0x30-byte source record through 00597930(obj, path, flag != 0, 1) (001D6F4D), which stores
     the selector byte +0x18 = 1 (00597954) and calls the resolver 0059EE90 with r8b passed through (0059795D).
  R3 the resolver has two routes and no third: route 1 = 001D6D20 (0059EFE5) into the size source +0x20; route 2 =
     the package resolver 0019B1F0 / 0019AEE0 (0059F187-0059F192) into the object source +0x10; a route-2 miss logs
     "[FFXII_ERROR] Big file open failed" (00D27948) and returns 10 (0059F1D1). A route-2 hit, when r12b is set,
     is committed through 0059A9B0 (0059F1B7).
  R4 route 1 is a RAM file cache: its enable byte 01F83440 has one writer, 0020C610 (0020C695, always 1), which sizes
     the cache from GlobalMemoryStatusEx (IAT 008C2118) - total physical / 3, clamped to [32 MB, 4 GB] - into 01F83448.
  R5 the package slots hold only the archive: the five-slot mount 0019B070 (0x1F4060 construct, 0x1F4340 BigFile
     load, freed on failure) has one call site image-wide (0017CEF6, raw rel32 + rip sweep), which mounts
     "../FFXII_TZA.vbf" (008C5868).
  R6 no loose-file open exists outside CRT stdio: CreateFileA (IAT 008C2178) is referenced at exactly two sites, both
     minidump writers (005CCAB0: "Minidump file saved to %s"; 0079B1E0: "%s_%d_%d_%d_%d_%d_%d.dmp"); no import is
     CreateFileW / CreateFile2 / NtCreateFile.
  R7 the FF12CONFIG path passes the resolver's route-1 character filter (0059EF4B-0059EFA9: nine single-character
     tests on the last five characters, each sending the path to route 2 on a match) - and the control shows the
     filter is sensitive: "x.mab", "a.webm" and "foo.bin" are sent to route 2.
Exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
d = EXE.read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(n):
    b = pe + 24 + opt + i * 40
    SECS.append((d[b:b + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, b + 8))
def off(v):
    for _, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def cstr(v): o = off(v); return d[o:o + 80].split(b"\0")[0].decode("latin-1")
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

a = at(0x408C85, 0x408C94)
check("R1 00408C30 opens PS2Data/SQUARE_FF12/FF12CONFIG with 001D6F20(path, 1)",
      a.get(0x408C85) == "lea edx, [rsi + 1]" and a.get(0x408C88) == "lea rcx, [rip + 0x909549]"
      and a.get(0x408C8F) == "call 0x1d6f20" and cstr(0xD121D8) == "PS2Data/SQUARE_FF12/FF12CONFIG", cstr(0xD121D8))

b = at(0x1D6F3E, 0x1D6F52); c = at(0x597954, 0x597962)
check("R2 001D6F20 -> 00597930(obj, path, flag != 0, 1): selector +0x18 = 1, r8b passed to 0059EE90",
      b.get(0x1D6F40) == "mov r9b, 1" and b.get(0x1D6F49) == "setne r8b" and b.get(0x1D6F4D) == "call 0x597930"
      and c.get(0x597954) == "mov byte ptr [rcx + 0x18], r9b" and c.get(0x59795D) == "call 0x59ee90")

r = at(0x59EFD2, 0x59EFF3); s = at(0x59F187, 0x59F1D6)
whole = at(0x59EE90, 0x59F1E2)
src_stores = sorted("%08X" % k for k, v in whole.items()
                    if re.match(r"mov (?:q|d)word ptr \[r15(?: \+ (?:8|0x10|0x20))?\], ", v))
check("R3 two routes: 001D6D20 -> +0x20, 0019B1F0/0019AEE0 -> +0x10; a miss logs Big file open failed and returns 10; "
      "a hit with r12b commits through 0059A9B0",
      r.get(0x59EFE5) == "call 0x1d6d20" and r.get(0x59EFEA) == "mov qword ptr [r15 + 0x20], rax"
      and s.get(0x59F187) == "call 0x19b1f0" and s.get(0x59F192) == "call 0x19aee0"
      and s.get(0x59F197) == "mov qword ptr [r15 + 0x10], rax" and s.get(0x59F1C3) == "lea rdx, [rip + 0x78877e]"
      and s.get(0x59F1D1) == "mov eax, 0xa" and s.get(0x59F1AB) == "test r12b, r12b" and s.get(0x59F1B7) == "call 0x59a9b0"
      and cstr(0xD27948).startswith("[FFXII_ERROR] Big file open failed")
      and src_stores == ["0059EFEA", "0059EFF6", "0059F197", "0059F1A8"],
      "stores to the record's +0 / +8 / +0x10 / +0x20: %s (the +8 handle is never set here)" % src_stores)

# raw sweeps over .text: rel32 E8/E9 to a target, rip-relative disp32 to a target (any opcode, 4-byte disp at end-4)
tx = next(sn for sn in SECS if sn[0] == ".text"); _, tvs, tva, trs, tro = tx
def rel32_sites(t):
    out = []
    for o in range(tro, tro + trs - 5):
        if d[o] in (0xE8, 0xE9):
            v = BASE + tva + (o - tro)
            if v + 5 + struct.unpack_from("<i", d, o + 1)[0] == t: out.append(v)
    return out
def ff15_sites(t):
    out = []
    for o in range(tro, tro + trs - 6):
        if d[o] == 0xFF and d[o + 1] in (0x15, 0x25):
            v = BASE + tva + (o - tro)
            if v + 6 + struct.unpack_from("<i", d, o + 2)[0] == t: out.append(v)
        if d[o] in (0x48, 0x4C) and d[o + 1] == 0x8B and (d[o + 2] & 0xC7) == 0x05:
            v = BASE + tva + (o - tro)
            if v + 7 + struct.unpack_from("<i", d, o + 3)[0] == t: out.append(v)
    return out
w = at(0x20C628, 0x20C69B)
flag_refs = []
for o in range(tro, tro + trs - 7):                                   # byte stores C6 05 disp32 imm8 / 88 05 disp32
    v = BASE + tva + (o - tro)
    if d[o] == 0xC6 and d[o + 1] == 0x05 and v + 7 + struct.unpack_from("<i", d, o + 2)[0] == 0x1F83440: flag_refs.append(v)
    if d[o] == 0x88 and (d[o + 1] & 0xC7) == 0x05 and v + 6 + struct.unpack_from("<i", d, o + 2)[0] == 0x1F83440: flag_refs.append(v)
check("R4 route 1 is a RAM cache: 01F83440's one writer 0020C695 stores 1 after GlobalMemoryStatusEx sizes the budget",
      w.get(0x20C628) == "mov dword ptr [rsp + 0x20], 0x40" and w.get(0x20C630) == "call qword ptr [rip + 0x6b5ae2]"
      and w.get(0x20C655) == "mov eax, 0x2000000" and w.get(0x20C693) == "mov al, 1"
      and w.get(0x20C695) == "mov byte ptr [rip + 0x1d76da5], al" and flag_refs == [0x20C695],
      "byte-store writers of 01F83440: %s" % ["%08X" % v for v in flag_refs])

m = rel32_sites(0x19B070); mm = at(0x19B0AF, 0x19B0EA); k = at(0x17CEE7, 0x17CEFB)
check("R5 the five-slot mount 0019B070 has one call site (0017CEF6), mounting ../FFXII_TZA.vbf",
      m == [0x17CEF6] and mm.get(0x19B0C6) == "call 0x1f4060" and mm.get(0x19B0E5) == "call 0x1f4340"
      and k.get(0x17CEEF) == "lea rdx, [rip + 0x748972]" and cstr(0x8C5868) == "../FFXII_TZA.vbf",
      "rel32 sites=%s" % ["%08X" % v for v in m])

cf = ff15_sites(0x8C2178)
imp_names = []
imp_rva = struct.unpack_from("<I", d, pe + 24 + 0x78)[0]           # data directory 1 (import) in the PE32+ optional header
o = off(BASE + imp_rva)
while True:
    oft, _, _, name_rva, ft = struct.unpack_from("<IIIII", d, o)
    if name_rva == 0: break
    to = off(BASE + (oft or ft))
    while True:
        e = struct.unpack_from("<Q", d, to)[0]
        if e == 0: break
        if not e >> 63: imp_names.append(cstr(BASE + (e & 0x7FFFFFFF) + 2))
        to += 8
    o += 20
dumps = at(0x79B24B, 0x79B252).get(0x79B24B) == "lea rdx, [rip + 0x1518326]" and cstr(0x1CB3578).endswith(".dmp") \
        and at(0x5CCB4D, 0x5CCB54).get(0x5CCB4D) == "lea rdx, [rip + 0x76942c]" and cstr(0xD35F80).startswith("Minidump file saved")
check("R6 CreateFileA is referenced at exactly two sites, both minidump writers; no other CreateFile* import",
      cf == [0x5CCAE8, 0x79B298] and dumps and [x for x in imp_names if "CreateFile" in x] == ["CreateFileA"]
      and not any(x in ("NtCreateFile", "ZwCreateFile") for x in imp_names),
      "sites=%s imports=%s" % (["%08X" % v for v in cf], [x for x in imp_names if "Create" in x and "File" in x]))

f = at(0x59EF4B, 0x59EFAB)
TESTS = [(-4, "."), (-3, "m"), (-2, "a"), (-1, "b"), (-5, "."), (-4, "w"), (-3, "e"), (-2, "b"), (-1, "m")]
def route2_by_filter(p):
    return len(p) <= 3 or any(len(p) >= -k and p[k] == ch for k, ch in TESTS if not (k == -5 and len(p) <= 4))
jes = [v for v in f.values() if v == "je 0x59f000"]
check("R7 FF12CONFIG passes the route-1 character filter (nine je-to-route-2 tests); the filter catches .mab/.webm/.bin",
      len(jes) == 9 and "cmp al, 0x2e" in f.values() and "cmp r8b, 0x62" in f.values() and "cmp r8b, 0x6d" in f.values()
      and not route2_by_filter("PS2Data/SQUARE_FF12/FF12CONFIG")
      and all(route2_by_filter(x) for x in ("x.mab", "a.webm", "foo.bin")),
      "je count=%d" % len(jes))
print("FAILS", fails)
sys.exit(1 if fails else 0)
