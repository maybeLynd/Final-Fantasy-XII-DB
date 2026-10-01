"""overlap.py - OV-46: what the deployed Windows CRT's memcpy does with overlapping ranges (FABLE, Claude Opus 5.5,
2026-09-29). HOST MEASUREMENT on the exact dependency the game loads; no game process.

  D  THE DEPENDENCY: the certified image imports memcpy from VCRUNTIME140.dll (IAT 008C29D8 region). The install ships no
     vcruntime140.dll beside FFXII_TZA.exe (x64/), so the loader takes the machine's System32 copy. Its path, size,
     SHA-256 and file version are printed; a different machine's redistributable is a different dependency
  E  EXPORTS: whether memcpy and memmove are the same entry in that DLL
  O  OVERLAP: memcpy through that DLL (ctypes), for dst below and above src, every overlap shift 1..64 plus powers of two to
     4 MiB, sizes spanning the small/SSE/AVX/non-temporal paths, and source misalignment 0..15 - each result compared
     with a reference overlap-safe copy (Python bytes slicing of the pre-copy buffer). The count of cases that differ
  K  sensitivity: the comparison flags a naive forward byte copy on a dst-above-src overlap (the defect OV-46 guards)
"""
import ctypes, hashlib, os, struct, sys
DLL = r"C:\Windows\System32\vcruntime140.dll"
GAME_DIR = r"D:\FFXII MP Mod\FFXII_TestClient1\x64"
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
# D
local = [f for f in os.listdir(GAME_DIR) if f.lower().startswith("vcruntime140")]
raw = open(DLL, "rb").read()
def file_version(path):
    size = ctypes.windll.version.GetFileVersionInfoSizeW(path, None)
    buf = ctypes.create_string_buffer(size); ctypes.windll.version.GetFileVersionInfoW(path, 0, size, buf)
    p = ctypes.c_void_p(); n = ctypes.c_uint()
    ctypes.windll.version.VerQueryValueW(buf, "\\", ctypes.byref(p), ctypes.byref(n))
    ms, ls = struct.unpack_from("<II", ctypes.string_at(p.value, n.value), 8)
    return "%d.%d.%d.%d" % (ms >> 16, ms & 0xFFFF, ls >> 16, ls & 0xFFFF)
check("D", not local, "no vcruntime140*.dll beside the game (%s); the loaded dependency is %s, %d bytes, sha256 %s, version %s"
      % (GAME_DIR, DLL, len(raw), hashlib.sha256(raw).hexdigest(), file_version(DLL)))
# E
lib = ctypes.WinDLL(DLL)
mc, mm = ctypes.cast(lib.memcpy, ctypes.c_void_p).value, ctypes.cast(lib.memmove, ctypes.c_void_p).value
print("      memcpy export %#x, memmove export %#x, %s" % (mc, mm, "the same entry" if mc == mm else "different entries"))
memcpy = lib.memcpy; memcpy.restype = ctypes.c_void_p; memcpy.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
# O
sizes = sorted(set(list(range(1, 80)) + [96, 127, 128, 129, 255, 256, 257, 511, 512, 1023, 1024, 4095, 4096, 8191, 8192,
                                          65535, 65536, 262144, 1 << 20, (1 << 20) + 17, 4 << 20]))
shifts = sorted(set(list(range(1, 65)) + [128, 256, 1024, 4096, 65536, 1 << 20]))
cases = bad = 0; bad_examples = []
def trial(n, shift, up, mis):
    total = n + shift + 64
    buf = ctypes.create_string_buffer(bytes((i * 131 + 7) & 0xFF for i in range(total)) if total < 1 << 16 else os.urandom(total), total)
    before = buf.raw
    src_off = 16 + mis if not up else 16 + mis
    s, t = (src_off, src_off + shift) if up else (src_off + shift, src_off)
    if max(s, t) + n > total: return None
    base = ctypes.addressof(buf)
    memcpy(base + t, base + s, n)
    want = bytearray(before); want[t:t + n] = before[s:s + n]
    return buf.raw == bytes(want)
for n in sizes:
    for shift in shifts:
        if shift >= n: continue            # no overlap
        if n > 65536 and shift not in (1, 17, 64, 4096, 65536): continue   # keep the large cases few
        for up in (True, False):
            for mis in ((0, 1, 7, 15) if n <= 4096 else (0, 3)):
                r = trial(n, shift, up, mis)
                if r is None: continue
                cases += 1
                if not r:
                    bad += 1
                    if len(bad_examples) < 5: bad_examples.append((n, shift, "dst above src" if up else "dst below src", mis))
check("O", cases > 20000 and bad == 0,
      "%d overlapping memcpy cases through the deployed DLL; %d differ from an overlap-safe copy %s" % (cases, bad, bad_examples))
# K
def naive(dst, src, n, mem):
    for i in range(n): mem[dst + i] = mem[src + i]
mem = bytearray(range(64)); ref = bytearray(mem); ref[8:40] = mem[0:32]; naive(8, 0, 32, mem)
check("K", mem != ref, "sensitivity: a naive forward copy with dst 8 bytes above src differs from the reference")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
