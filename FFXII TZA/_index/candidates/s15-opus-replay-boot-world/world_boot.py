"""The boot world for S-15 (OPUS, 2026-09-26): block 332's emulator (s21-opus-replay-applier-stub-free/world.py) with the WHOLE
image allowed - imports are the only boundary - and the process-start models below installed in this order (a later model's
answer for the same import wins; each module's docstring states what it answers):
  s36 os_model (fresh install: folders, files, platform), s36 msvcp_wide (wide streams), crt_bridge_boot (the S-40 C-runtime
  bridge with a full C sscanf), narrow_streams (msvcp140 narrow streams over the game's own stringbuf, calling its virtuals
  through guest calls), file_bridge (read-only fopen / fread / fseek over the install folder), boot_model (process start:
  CRT, threads recorded not run, IME/COM, a failing Steam, command line, display 1920x1080, en-US, resources from the PE),
  mem_files (memory-only writable files), sync_model (single-thread semaphores / events, strict), boot_misc (CryptoAPI MD5,
  sticky keys, memory status, timer caps, strcspn, toupper, a failing audio-endpoint CoCreateInstance, GetCurrentThread).
Then the CRT's pre-C initialisers (008C5688..008C5698) and C++ initialisers (1,172 at 008C31D8..008C5678) run as shipped.
Nothing is written to disk. A 512 MiB heap at 0x40000000 backs malloc."""
import bisect
import collections
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
WDIR = os.path.join(CAND, "s21-opus-replay-applier-stub-free")
sys.path.insert(0, WDIR)
_cwd = os.getcwd(); os.chdir(WDIR)
import world as W                                             # noqa: E402
os.chdir(_cwd)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(CAND, "s36-opus-replay-arbiter-input-gate"))
import pefile                                                  # noqa: E402
import capstone                                                # noqa: E402
from unicorn import UC_HOOK_BLOCK                              # noqa: E402
from unicorn.x86_const import UC_X86_REG_RSP                   # noqa: E402

rows = {}
for _l in open(os.path.join(W.GRAPH, "functions.tsv"), encoding="utf-8", errors="replace"):
    _c = _l.split("\t")
    try:
        rows[int(_c[0], 16)] = _c[1]
    except ValueError:
        pass
_st = sorted(rows)


def fn(a):
    k = bisect.bisect_right(_st, a) - 1
    return "%08X %s" % (_st[k], rows[_st[k]]) if k >= 0 else "%X" % a


W.ALLOWED = set(W.FSTARTS)                                     # the whole image; imports are the boundary
S = W.Session([], [])
uc = S.uc
q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
d4 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
LOG = []
import os_model, msvcp_wide                                    # noqa: E402,E401
os_model.install(W, uc, LOG)
msvcp_wide.install(W, uc, LOG)
import crt_bridge_boot                                         # noqa: E402
crt_bridge_boot.install(W, uc, LOG)
import narrow_streams                                          # noqa: E402
narrow_streams.install(W, uc, LOG)
import file_bridge                                             # noqa: E402
file_bridge.install(W, uc, LOG)
import boot_model                                              # noqa: E402
_, THREADS = boot_model.install(W, uc, LOG)
import mem_files                                               # noqa: E402
MEMF = mem_files.install(W, uc, LOG, boot_model.install.LAST)
import sync_model                                              # noqa: E402
SYNC, SYNCSTOP = sync_model.install(W, uc, LOG)
import boot_misc                                               # noqa: E402
boot_misc.install(W, uc, LOG)
HEAP = 0x40000000
uc.mem_map(HEAP, 0x20000000)
S.st["heap"] = HEAP
uc.ctl_flush_tb()
IB = 0x120000
img = pefile.PE(W.EXE, fast_load=True).get_memory_mapped_image()
PRE = [struct.unpack_from("<Q", img, a - IB)[0] for a in (0x8C5688, 0x8C5690, 0x8C5698)]
XC = [struct.unpack_from("<Q", img, a - IB)[0] for a in range(0x8C31D8, 0x8C5678, 8)]
CRT = {"pre_c": 0, "cpp": 0, "failed": []}
for _k, _f in enumerate(PRE + XC):
    if _f == 0:
        continue
    _ok = S.call(_f)
    CRT["pre_c" if _k < len(PRE) else "cpp"] += 1
    if not _ok:
        CRT["failed"].append(("%08X" % _f, str((S.st["bad"] or S.st["faults"])[:1])))

# a shadow call stack for the reports: function entries by stack pointer (blocks that are function starts push)
FSET = set(rows)
SHADOW = []


def _blk(u, a, n, _):
    sp = u.reg_read(UC_X86_REG_RSP)
    while SHADOW and SHADOW[-1][1] < sp:
        SHADOW.pop()
    if a in FSET:
        while SHADOW and SHADOW[-1][1] <= sp:
            SHADOW.pop()
        SHADOW.append((a, sp))


uc.hook_add(UC_HOOK_BLOCK, _blk)
uc.ctl_flush_tb()


def shadow():
    return [fn(a)[:40] for a, _ in SHADOW]


TRAPNAMES = {0x74000000 + 4 * i: n for i, (_sl, n) in enumerate(W.import_slots())}
