"""S-47 (OPUS, 2026-09-26): the overlapping-copy import boundary on source movement (RL-8/RL-5 path), executed in the CRT
routine the game actually binds.

The exposure (s47-runtime-per-invariant-exposure.md, RL-8; SECTION-07 M07-7): 'the shipped mover hands overlapping ranges to the
CRT memcpy import, and what the CRT does with them is not established'. M07-7's shape: destination 0x300003C0, source 0x30000500,
length 0x400 (a 0x100 hole before a 0x400 source; the ranges overlap). SECTION-07 stopped at the import entry: 'Windows CRT behavior
needs exact dependency evidence; substituting host memmove would conceal the question.'

What this runs - no substitute:
  1. The authority image's import of memcpy (IAT 008C2A68) names VCRUNTIME140.dll. The image directory ships no VCRUNTIME140.dll,
     so the loader binds the host's System32 copy (the application directory is searched first, and it has none).
  2. That DLL's exact bytes (SHA-256 and FileVersion recorded) are loaded into this process from a byte-identical copy under another
     file name (the Python runtime has its own vcruntime140.dll loaded; the copy guarantees the System32 bytes run). The mapped
     .text is compared with the file before anything runs.
  3. The memcpy export is called through ctypes on the host CPU - the DLL's own code, not an emulation - over:
       - M07-7's exact shape (same distance, same length, same 0x40-alignment residues of both addresses);
       - every size class the routine's dispatch distinguishes, both overlap directions, several distances;
       - every dispatch path: the routine reads two globals of its own (the ISA level and the 'favor' bits, set by the DLL's own
         initialisation from CPUID). Each run records the host values, then forces each path by writing those globals, and
         restores them.
     Expected result of every copy: the destination holds the source's ORIGINAL bytes (memmove semantics). Any difference is
     recorded as a failure with its shape.
  4. Static: memcpy's export is one instruction, jmp to memmove's entry - byte-verified.
Evidence class: native execution of the dependency's exact code on the host CPU; the game image itself is not executed here
(SECTION-07's run supplies the arguments). live_game false. Writes result.json.
"""
import ctypes
import hashlib
import json
import os
import random
import shutil
import struct
import sys

import pefile

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
SYS = r"C:\Windows\System32\vcruntime140.dll"
COPY = os.path.join(os.environ.get("TEMP", HERE), "opus_s47_vcrt_sys_copy.dll")
res = {"live_game": False}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ---- 1. the import and the absence of an app-local CRT ----
assert sha(EXE) == EXE_SHA, "authority image mismatch"
pe = pefile.PE(EXE, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
imp = {(d.dll.decode(), i.name.decode()): "%08X" % i.address for d in pe.DIRECTORY_ENTRY_IMPORT for i in d.imports if i.name in (b"memcpy", b"memmove")}
appdir = os.path.dirname(EXE)
res["import"] = {"exe_sha256": EXE_SHA, "slots": {"%s!%s" % k: v for k, v in imp.items()},
                 "app_local_vcruntime140": [f for f in os.listdir(appdir) if f.lower().startswith("vcruntime140")]}

# ---- 2. the DLL's bytes ----
dpe = pefile.PE(SYS)
ver = {k.decode(): v.decode() for k, v in dpe.FileInfo[0][0].StringTable[0].entries.items() if k in (b"FileVersion", b"ProductVersion")}
ex = {e.name.decode(): e.address for e in dpe.DIRECTORY_ENTRY_EXPORT.symbols if e.name}
MEMCPY, MEMMOVE = ex["memcpy"], ex["memmove"]
code = dpe.get_memory_mapped_image()
jmp = code[MEMCPY:MEMCPY + 5]
jmp_target = MEMCPY + 5 + struct.unpack("<i", jmp[1:5])[0] if jmp[0] == 0xE9 else None
shutil.copyfile(SYS, COPY)
assert sha(COPY) == sha(SYS)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.LoadLibraryW.restype = ctypes.c_void_p
k32.GetModuleFileNameW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint]
h = k32.LoadLibraryW(COPY)
assert h, ctypes.get_last_error()
buf = ctypes.create_unicode_buffer(520)
k32.GetModuleFileNameW(h, buf, 520)
text = [s for s in dpe.sections if s.Name.rstrip(b"\0") == b".text"][0]
mapped = ctypes.string_at(h + text.VirtualAddress, text.Misc_VirtualSize)
filetext = code[text.VirtualAddress:text.VirtualAddress + text.Misc_VirtualSize]
# relocations may patch .text; compare with the image rebased to the loaded address
dpe2 = pefile.PE(SYS)
dpe2.relocate_image(h)
reltext = dpe2.get_memory_mapped_image()[text.VirtualAddress:text.VirtualAddress + text.Misc_VirtualSize]
res["dll"] = {"path": SYS, "sha256": sha(SYS), "version": ver, "loaded_from": buf.value, "loaded_base": "%X" % h,
              "text_mapped_equals_file": mapped == reltext, "text_bytes": len(mapped), "text_identical_unrelocated": mapped == filetext,
              "memcpy_rva": "%X" % MEMCPY, "memmove_rva": "%X" % MEMMOVE, "memcpy_bytes": jmp.hex(),
              "memcpy_is_jmp_to_memmove": jmp_target == MEMMOVE}
assert mapped == reltext

# the two dispatch globals, read from memmove's own instructions (rip-relative cmp / test)
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
isa = favor = None
for i in md.disasm(code[MEMMOVE:MEMMOVE + 0x200], MEMMOVE):
    if "rip +" in i.op_str:
        tgt = i.address + i.size + int(i.op_str.split("rip + ")[1].split("]")[0], 16)
        if i.mnemonic == "cmp" and isa is None:
            isa = tgt
        elif i.mnemonic == "test" and favor is None:
            favor = tgt
res["dispatch_globals"] = {"isa_rva": "%X" % isa, "favor_rva": "%X" % favor}
ISA = ctypes.c_int.from_address(h + isa)
FAV = ctypes.c_int.from_address(h + favor)
host = (ISA.value, FAV.value)
res["dispatch_globals"]["host_values"] = {"isa": host[0], "favor": host[1]}

fn = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(h + MEMCPY)

# ---- 3. the matrix ----
ARENA = 0x400000
arena = (ctypes.c_ubyte * (ARENA + 0x1000))()
abase = (ctypes.addressof(arena) + 0xFFF) & ~0xFFF
rng = random.Random(4747)
pattern = bytes(rng.randrange(256) for _ in range(ARENA))


def one(dst_off, src_off, n):
    ctypes.memmove(abase, pattern, ARENA)                      # host copy only to seed the arena, never under test
    want = bytearray(pattern)
    want[dst_off:dst_off + n] = pattern[src_off:src_off + n]
    r = fn(abase + dst_off, abase + src_off, n)
    got = ctypes.string_at(abase, ARENA)
    return got == bytes(want) and r == abase + dst_off


SIZES = list(range(1, 0x41)) + [0x7F, 0x80, 0x81, 0xFF, 0x100, 0x101, 0x1FF, 0x3FF, 0x400, 0x401, 0x1000, 0x2000, 0x2001, 0x4000,
                                 0x10000, 0x180000, 0x180001]
DIST = [1, 3, 8, 0x10, 0x1F, 0x20, 0x3F, 0x40, 0x41, 0x100, 0x140]
PATHS = [("host", host[0], host[1])] + [("isa=%d favor=%d" % (a, f), a, f) for a in (0, 1, 2, 3, 5) for f in (0, 2)]
M07 = (0x300003C0, 0x30000500, 0x400)
m_dst = 0x100000 + (M07[0] & 0xFFF)
m_src = m_dst + (M07[1] - M07[0])
fails, runs, m07 = [], 0, {}
try:
    for name, a, f in PATHS:
        ISA.value, FAV.value = a, f
        m07[name] = one(m_dst, m_src, M07[2])
        runs += 1
        for n in SIZES:
            for d in DIST:
                if n + d + 0x2000 > ARENA:
                    continue
                for mis in (0, 5):
                    lo = 0x1000 + mis
                    for direction, (do, so) in (("down", (lo, lo + d)), ("up", (lo + d, lo))):
                        runs += 1
                        if not one(do, so, n):
                            fails.append({"path": name, "len": n, "dist": d, "dir": direction, "misalign": mis})
finally:
    ISA.value, FAV.value = host
res["M07_7"] = {"shape": {"dst": "%08X" % M07[0], "src": "%08X" % M07[1], "len": "%X" % M07[2]},
                "arena_dst_low12": "%03X" % (m_dst & 0xFFF), "arena_src_low12": "%03X" % (m_src & 0xFFF),
                "same_0x40_residues": ((abase + m_dst) & 0x3F, (abase + m_src) & 0x3F) == (M07[0] & 0x3F, M07[1] & 0x3F),
                "memmove_semantics_per_path": m07}
res["matrix"] = {"paths": [p[0] for p in PATHS], "sizes": SIZES, "distances": DIST, "misalign": [0, 5], "directions": ["down", "up"],
                 "copies": runs, "failures": fails[:50], "failure_count": len(fails)}
res["restored"] = (ISA.value, FAV.value) == host

# ---- control: the same checker, handed a plain forward byte copier, must catch overlap ----
def naive(dst, src, n):
    for i in range(n):
        ctypes.memset(dst + i, ctypes.c_ubyte.from_address(src + i).value, 1)
    return dst


real_fn, fn = fn, naive
ctl = {"up_len_0x40_dist_8": one(0x1008, 0x1000, 0x40), "down_len_0x40_dist_8": one(0x1000, 0x1008, 0x40)}
fn = real_fn
res["control_naive_forward_copier"] = ctl

# ---- static census: every other x64 vcruntime140.dll on this host ----
seen = {}
for root in ("C:\\Program Files", "C:\\Program Files (x86)", "C:\\Windows\\System32", "D:\\"):
    for dp, dn, fs in os.walk(root):
        if dp.count(os.sep) - root.count(os.sep) > 6:
            dn[:] = []
            continue
        for f in fs:
            if f.lower() == "vcruntime140.dll":
                q = os.path.join(dp, f)
                try:
                    hsh = sha(q)
                    if hsh in seen:
                        continue
                    e = pefile.PE(q)
                    if e.FILE_HEADER.Machine != 0x8664:
                        continue
                    xs = {x.name.decode(): x.address for x in e.DIRECTORY_ENTRY_EXPORT.symbols if x.name}
                    img = e.get_memory_mapped_image()
                    b = img[xs["memcpy"]:xs["memcpy"] + 5]
                    j = xs["memcpy"] + 5 + struct.unpack("<i", b[1:5])[0] if b[0] == 0xE9 else None
                    v = {k.decode(): w.decode() for k, w in e.FileInfo[0][0].StringTable[0].entries.items() if k == b"FileVersion"}
                    seen[hsh] = {"path": q, "version": v.get("FileVersion"), "memcpy_rva": "%X" % xs["memcpy"], "memmove_rva": "%X" % xs["memmove"],
                                 "same_rva": xs["memcpy"] == xs["memmove"], "jmp_to_memmove": j == xs["memmove"]}
                except Exception as err:  # noqa - unreadable copies are recorded, not skipped silently
                    seen[q] = {"path": q, "error": str(err)[:80]}
res["census_x64_vcruntime140"] = sorted(seen.values(), key=lambda x: x.get("version") or "")
cases = {
    "import_is_VCRUNTIME140_memcpy_at_008C2A68_and_no_app_local_copy": res["import"]["slots"].get("VCRUNTIME140.dll!memcpy") == "008C2A68"
        and res["import"]["app_local_vcruntime140"] == [],
    "loaded_code_is_the_System32_file": res["dll"]["text_mapped_equals_file"],
    "memcpy_export_is_one_jmp_to_memmove": res["dll"]["memcpy_is_jmp_to_memmove"],
    "M07_7_shape_copies_as_memmove_on_every_path": all(m07.values()) and res["M07_7"]["same_0x40_residues"],
    "matrix_every_copy_is_memmove_on_every_path": not fails,
    "dispatch_globals_restored": res["restored"],
    "control_checker_catches_a_forward_copier_on_upward_overlap": ctl["up_len_0x40_dist_8"] is False and ctl["down_len_0x40_dist_8"] is True,
    "census_every_x64_copy_exports_memcpy_as_memmove": bool(res["census_x64_vcruntime140"])
        and all(c.get("same_rva") or c.get("jmp_to_memmove") for c in res["census_x64_vcruntime140"]),
}
res["cases"] = cases
res["ok"] = all(cases.values())
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({k: res[k] for k in ("import", "dll", "dispatch_globals")}, indent=1))
print("copies:", runs, "failures:", len(fails))
print("control:", ctl)
for c in res["census_x64_vcruntime140"]:
    print("census:", c)
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
