"""The built world for S-02's stub-free world-tick run (OPUS, 2026-09-25, block 318).

Whole SHA-asserted image mapped; NO application stub. The world the tick runs in is BUILT, not zeroed, wherever a shipped
initialiser exists: world.json 'inits' are shipped functions run before the tick (the CRT startup routine 00809124, the string
pool 0019CDE0, the movement-body pool 003DAE30). world.json 'fixes' are zero-filled blocks planted behind singleton cells whose
own constructors belong to the engine's boot (listed in the README). Emulation environment: a TEB (gs:) with stack bounds, and
TLS set up from the PE TLS directory as the loader does.
IMPORTS: every IAT slot points at a unique trap; only the imports in BRIDGED are serviced, each by name:
  memory / CRT: memset memcpy memmove malloc free _aligned_malloc _aligned_free, and a faithful __stdio_common_vs*printf*
    (printf_bridge.py) over the emulated va_list;
  maths: sqrtf sinf cosf atan2f;
  OS: events / critical sections / SRW / condition variables (success, no blocking), GetCurrentThreadId, CloseHandle,
    GetModuleHandle (a handle) and GetProcAddress (0 - not found, so the CRT takes its own fallback), onexit registration
    (success - process exit is not reached), OutputDebugStringA (recorded), and a DETERMINISTIC clock
    (QueryPerformanceCounter +1000 per call at 10 MHz; GetTickCount +16).
Any other import stops the run by name."""
import collections
import csv
import hashlib
import json
import math
import os
import struct
import sys

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RAX,
                               UC_X86_REG_XMM0, UC_X86_REG_XMM1, UC_X86_REG_R9)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
GRAPH = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph"
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = 0x120000
STACK, STACK_SZ, RET, HEAP, BRIDGE, FIX = 0x70000000, 0x100000, 0x71000000, 0x73000000, 0x74000000, 0x76000000
TICK = 0x314020
BRIDGED = {"memset", "memcpy", "memmove", "malloc", "free", "sqrtf", "sinf", "cosf", "atan2f", "_aligned_malloc", "_aligned_free",
           "tanf", "asinf", "acosf", "atanf", "expf", "logf", "log10f", "floorf", "ceilf", "powf", "fmodf"}
OSRET = {"CreateEventA": 0x1234, "CreateEventW": 0x1234, "SetEvent": 1, "ResetEvent": 1, "WaitForSingleObject": 0,
         "WaitForSingleObjectEx": 0, "EnterCriticalSection": 0, "LeaveCriticalSection": 0, "InitializeCriticalSection": 0,
         "InitializeCriticalSectionAndSpinCount": 1, "InitializeCriticalSectionEx": 1, "DeleteCriticalSection": 0,
         "GetCurrentThreadId": 1, "ReleaseSemaphore": 1, "CloseHandle": 1,
         "_register_onexit_function": 0, "_crt_atexit": 0, "atexit": 0,
         "GetModuleHandleW": 0x7FFA0000, "GetModuleHandleA": 0x7FFA0000, "GetProcAddress": 0,
         "__vcrt_InitializeCriticalSectionEx": 1, "InitializeSRWLock": 0, "AcquireSRWLockExclusive": 0,
         "ReleaseSRWLockExclusive": 0, "InitializeConditionVariable": 0, "WakeAllConditionVariable": 0,
         "SleepConditionVariableCS": 1, "SleepConditionVariableSRW": 1}
BRIDGED |= {"__acrt_iob_func", "__stdio_common_vfprintf", "OutputDebugStringA", "QueryPerformanceCounter", "QueryPerformanceFrequency", "GetTickCount", "GetTickCount64", "timeGetTime"}
BRIDGED |= set(OSRET) | {"__stdio_common_vsnprintf_s", "__stdio_common_vsprintf", "__stdio_common_vsprintf_s"}
import printf_bridge

raw = open(EXE, "rb").read()
graph = collections.defaultdict(set)
for r in csv.DictReader(open(GRAPH + r"\edges.tsv", encoding="utf-8"), delimiter="\t"):
    if r["callee_external"] != "true":
        graph[int(r["caller"], 16)].add(int(r["callee"], 16))


def closure(s):
    seen, st = set(), [s]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        st.extend(graph[x])
    return seen


EXTRA = [int(x, 16) for x in json.load(open(os.path.join(HERE, "world.json")))["extra_allowed"]]
ALLOWED = closure(TICK) | {0x863BF0, 0x866D60, 0x866B90}
for e in EXTRA:
    ALLOWED |= closure(e)
FSTARTS = set(int(l.split("\t")[0], 16) for l in open(GRAPH + r"\functions.tsv", encoding="utf-8", errors="replace")
              if l[:1] in "0123456789ABCDEF")
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
secs, off = [], pe + 24 + optsz
for _ in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((va + IMG, vs, ra, rs))
    off += 40


def import_slots():
    def r2o(rva):
        for v, vs, ra, rs in secs:
            if v - IMG <= rva < v - IMG + max(vs, rs):
                return ra + rva - (v - IMG)
    imp_rva = struct.unpack_from("<I", raw, pe + 24 + 112 + 8)[0]
    out, dd = [], r2o(imp_rva)
    while True:
        oft, ts, fc, name, ft = struct.unpack_from("<IIIII", raw, dd)
        if not (oft or name or ft):
            return out
        th, i = r2o(oft or ft), 0
        while True:
            e = struct.unpack_from("<Q", raw, th + 8 * i)[0]
            if e == 0:
                break
            nm = "ord%d" % (e & 0xFFFF) if e >> 63 else raw[r2o(e) + 2:raw.index(b"\x00", r2o(e) + 2)].decode()
            out.append((IMG + ft + 8 * i, nm))
            i += 1
        dd += 20


def make():
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for v, vs, ra, rs in secs:
        lo, hi = v & ~0xFFF, (v + max(vs, rs) + 0xFFF) & ~0xFFF
        uc.mem_map(lo, hi - lo)
        uc.mem_write(v, raw[ra:ra + min(rs, max(vs, rs))])
    uc.mem_map(STACK, STACK_SZ)
    uc.mem_map(RET, 0x1000)
    uc.mem_map(HEAP, 0x1000000)
    uc.mem_map(BRIDGE, 0x2000)
    uc.mem_map(FIX, 0x400000)
    uc.mem_write(RET, bytes([0xF4]))
    uc.mem_write(BRIDGE, bytes([0xC3]) * 0x2000)
    TEB = 0x7FF00000                                   # a TEB for gs: (__chkstk reads gs:[0x10] = stack limit)
    uc.mem_map(TEB, 0x2000)
    uc.mem_write(TEB + 0x08, struct.pack('<QQ', STACK + STACK_SZ, STACK))
    uc.mem_write(TEB + 0x30, struct.pack('<Q', TEB))
    uc.msr_write(0xC0000101, TEB)
    # thread-local storage, set up as the loader does: the PE TLS directory's template copied into one block,
    # TEB+0x58 -> slot array, slot[_tls_index] -> block; _tls_index (AddressOfIndex) written 0 for the main image
    tls_rva, tls_sz = struct.unpack_from("<II", raw, pe + 24 + 112 + 9 * 8)
    if tls_rva:
        def img_off(va):
            for v, vs, ra, rs in secs:
                if v <= va < v + rs:
                    return ra + va - v
        tstart, tend, tidx, tcb, zfill = struct.unpack_from("<QQQQI", raw, img_off(IMG + tls_rva))
        tmpl = raw[img_off(tstart):img_off(tstart) + (tend - tstart)]
        TLSB = TEB + 0x1000
        uc.mem_map(0x7FE00000, 0x100000)
        uc.mem_write(0x7FE00000, tmpl + bytes(zfill))
        uc.mem_write(TLSB, struct.pack("<Q", 0x7FE00000))
        uc.mem_write(TEB + 0x58, struct.pack("<Q", TLSB))
        uc.mem_write(tidx, struct.pack("<I", 0))
    BR = {}
    for i, (slot, name) in enumerate(import_slots()):
        uc.mem_write(slot, struct.pack("<Q", BRIDGE + 4 * i))
        BR[BRIDGE + 4 * i] = name
    return uc, BR


def fxf(u, r):
    return struct.unpack("<f", struct.pack("<I", u.reg_read(r) & 0xFFFFFFFF))[0]


def run(mode, arg2=0, fixes=None, trace_n=30, count=20000000, inits=None, pre_tick=None, tick_hook=None):
    uc, BR = make()
    st = {"bad": [], "faults": [], "trace": collections.deque(maxlen=trace_n), "heap": HEAP, "entered": set(), "imports": collections.Counter()}
    cur = FIX
    for cell, size in (fixes or []):
        uc.mem_write(int(cell, 16), struct.pack("<Q", cur))
        cur += (size + 0xFFF) & ~0xFFF

    def on_code(u, a, n, _):
        st["trace"].append(a)
        if a in BR:
            nm = BR[a]
            st["imports"][nm] += 1
            if nm not in BRIDGED:
                st["bad"].append("import " + nm)
                u.emu_stop()
                return
            rcx, rdx, r8 = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
            if nm == "memset":
                u.mem_write(rcx, bytes([rdx & 0xFF]) * r8); u.reg_write(UC_X86_REG_RAX, rcx)
            elif nm in ("memcpy", "memmove"):
                u.mem_write(rcx, bytes(u.mem_read(rdx, r8)) if r8 else b""); u.reg_write(UC_X86_REG_RAX, rcx)
            elif nm in ("malloc", "_aligned_malloc"):
                al = rdx if nm == "_aligned_malloc" and rdx else 16
                st["heap"] = (st["heap"] + al - 1) & ~(al - 1)
                p = st["heap"]; st["heap"] += (rcx + 0xF) & ~0xF
                u.reg_write(UC_X86_REG_RAX, p)
            elif nm in ("free", "_aligned_free"):
                pass
            elif nm in OSRET:
                u.reg_write(UC_X86_REG_RAX, OSRET[nm])
            elif nm == "__acrt_iob_func":                    # stdin/stdout/stderr tokens for the stdio sink below
                u.reg_write(UC_X86_REG_RAX, 0x7FFB0000 + (rcx & 0xFF) * 0x10)
            elif nm == "__stdio_common_vfprintf":            # (options, stream, format, locale, va): formatted, recorded as output
                rsp = u.reg_read(UC_X86_REG_RSP)
                va = struct.unpack("<Q", bytes(u.mem_read(rsp + 0x28, 8)))[0]
                txt = printf_bridge.format_va(u, printf_bridge.cstr(u, r8), va)
                st.setdefault("stdout", []).append(txt[:120])
                u.reg_write(UC_X86_REG_RAX, len(txt))
            elif nm == "OutputDebugStringA":                 # a debugger sink: recorded, no process effect
                st.setdefault("debug_out", []).append(printf_bridge.cstr(u, rcx)[:120])
            elif nm == "QueryPerformanceCounter":          # deterministic clock: +1000 ticks per call (a declared fixture)
                st["qpc"] = st.get("qpc", 10_000_000) + 1000
                u.mem_write(rcx, struct.pack("<q", st["qpc"])); u.reg_write(UC_X86_REG_RAX, 1)
            elif nm == "QueryPerformanceFrequency":
                u.mem_write(rcx, struct.pack("<q", 10_000_000)); u.reg_write(UC_X86_REG_RAX, 1)
            elif nm in ("GetTickCount", "GetTickCount64", "timeGetTime"):
                st["tick"] = st.get("tick", 100000) + 16
                u.reg_write(UC_X86_REG_RAX, st["tick"])
            elif nm.startswith("__stdio_common_vs"):
                rsp = u.reg_read(UC_X86_REG_RSP)
                if nm == "__stdio_common_vsnprintf_s":        # (options, buf, bufsize, maxcount, fmt, locale, va)
                    buf, size, maxc = rdx, r8, u.reg_read(UC_X86_REG_R9)
                    fmt, va = struct.unpack("<Q", bytes(u.mem_read(rsp + 0x28, 8)))[0], struct.unpack("<Q", bytes(u.mem_read(rsp + 0x38, 8)))[0]
                else:                                          # (options, buf, bufsize, fmt, locale, va)
                    buf, size, maxc = rdx, r8, None
                    fmt, va = u.reg_read(UC_X86_REG_R9), struct.unpack("<Q", bytes(u.mem_read(rsp + 0x30, 8)))[0]
                txt = printf_bridge.format_va(u, printf_bridge.cstr(u, fmt), va)
                lim = size - 1 if size else 0
                if maxc not in (None, 0xFFFFFFFFFFFFFFFF) and maxc < lim:
                    lim = maxc
                w = txt[:lim]
                u.mem_write(buf, w + b"\0")
                u.reg_write(UC_X86_REG_RAX, len(w) if len(txt) <= lim else 0xFFFFFFFFFFFFFFFF)
                st.setdefault("formatted", []).append(w[:60])
            else:
                x = fxf(u, UC_X86_REG_XMM0)
                x2 = fxf(u, UC_X86_REG_XMM1)
                y = {"sqrtf": lambda: math.sqrt(x) if x >= 0 else float("nan"), "sinf": lambda: math.sin(x),
                     "cosf": lambda: math.cos(x), "atan2f": lambda: math.atan2(x, x2), "tanf": lambda: math.tan(x),
                     "asinf": lambda: math.asin(x) if -1 <= x <= 1 else float("nan"),
                     "acosf": lambda: math.acos(x) if -1 <= x <= 1 else float("nan"), "atanf": lambda: math.atan(x),
                     "expf": lambda: math.exp(x), "logf": lambda: math.log(x) if x > 0 else float("-inf"),
                     "log10f": lambda: math.log10(x) if x > 0 else float("-inf"), "floorf": lambda: math.floor(x),
                     "ceilf": lambda: math.ceil(x), "powf": lambda: math.pow(x, x2), "fmodf": lambda: math.fmod(x, x2)}[nm]()
                u.reg_write(UC_X86_REG_XMM0, struct.unpack("<I", struct.pack("<f", y))[0])
            return
        if a in FSTARTS:
            st["entered"].add(a)
            if a not in ALLOWED:
                st["bad"].append("%08X" % a)
                u.emu_stop()

    def on_bad(u, ac, a, n, v, _):
        st["faults"].append("%08X" % a)
        return False

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_bad)
    sp = STACK + STACK_SZ - 0x1000 - 8
    for init in (inits or []):                       # real initialisers, run before the tick (the idle world is BUILT, not zeroed)
        uc.mem_write(sp, struct.pack("<Q", RET))
        uc.reg_write(UC_X86_REG_RSP, sp)
        uc.reg_write(UC_X86_REG_RCX, 0)
        try:
            uc.emu_start(int(init, 16), RET, count=count)
        except UcError as e:
            st["faults"].append("init %s: %s" % (init, e))
        if uc.reg_read(UC_X86_REG_RIP) != RET or st["bad"] or st["faults"]:
            st["faults"].append("init %s did not return" % init)
            return False, st, uc
    if pre_tick:                                     # planted state AFTER the world is built (e.g. a staged request)
        pre_tick(uc)
    if tick_hook:                                    # instrumentation that must see the tick only
        tick_hook(uc, st)
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, mode)
    uc.reg_write(UC_X86_REG_RDX, arg2)
    try:
        uc.emu_start(TICK, RET, count=count)
    except UcError as e:
        st["faults"].append(str(e))
    ok = uc.reg_read(UC_X86_REG_RIP) == RET and not st["bad"] and not st["faults"]
    return ok, st, uc


