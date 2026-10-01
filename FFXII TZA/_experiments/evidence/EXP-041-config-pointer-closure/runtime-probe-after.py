#!/usr/bin/env python3
"""runtime_probe.py - read-only runtime inspection of the live game, driven by the type store.

Why this exists
---------------
Charter section 26 gates reconstruction readiness on runtime validation, and the coverage report
says only 13 of 211 documents (6.16 %) cite any live-process evidence. The database is built almost
entirely from static analysis. This is the instrument that closes that gap: it attaches to a running
`FFXII_TZA.exe`, resolves a database VA directly, and dumps a type's fields **using the names and
offsets already recorded in `_types/`** - the "Runtime Inspector" of charter section 13.

It is READ-ONLY BY CONSTRUCTION. It opens the process with `PROCESS_VM_READ |
PROCESS_QUERY_INFORMATION` and never requests write access. It cannot modify the game even by
mistake, which is the point: a validation instrument that can perturb its subject is not a
validation instrument.

Why database VAs work directly
------------------------------
`FFXII_TZA.exe` has **ImageBase 0x00120000** and **DYNAMIC_BASE (ASLR) CLEAR** in its
DllCharacteristics (0x8120), with relocations still shipped. The module therefore loads at its
preferred base and **a database VA is a runtime address, unmodified**. Verified from the PE header,
not assumed - and re-verified at attach time as this tool's first positive control.

(`HIGH_ENTROPY_VA` is set while `DYNAMIC_BASE` is clear, which is inert: high entropy has no meaning
without dynamic relocation. It corroborates the "untuned build" reading already on record.)

Two positive controls, both mandatory
-------------------------------------
The database's standing rule is that an absence claim needs a control positive for the instrument
being tested. Reading memory has two independent ways to silently produce garbage, so there are two:

1. **Base control** - the main module's load address must equal the PE ImageBase. If it does not,
   every VA in the database is wrong for this process and the tool REFUSES to report anything.
2. **Read control** - a known-constant `.rdata` location is read and compared. `0x01CCD300` holds
   Lua's `LUAC_TAIL`, the six bytes `19 93 0D 0A 1A 0A`. If that does not come back exactly, the
   read path is broken and results are refused.

Without control 2, a failing `ReadProcessMemory` that returns zeroes is indistinguishable from a
field that is genuinely zero - and "the field is 0" is exactly the kind of claim this tool exists to
make.

Usage
-----
    runtime_probe.py --attach                       attach, run both controls, report and exit
    runtime_probe.py --deref 0x01F82D20 --type GameSettingConfig
    # 0x01F82D20 stores the pointer; --at takes an actual object address.
    runtime_probe.py --check _experiments/<file>.tsv
    runtime_probe.py --read 0x01DFE0B4 --size 12
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import io
import os
import struct
import sys

IMAGE_BASE = 0x00120000
CONTROL_ADDR = 0x01CCD300
CONTROL_BYTES = bytes([0x19, 0x93, 0x0D, 0x0A, 0x1A, 0x0A])   # Lua LUAC_TAIL
CONTROL_WHAT = "LUAC_TAIL at 0x01CCD300"
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
psapi = ctypes.WinDLL("psapi", use_last_error=True)


def die(m, code=2):
    sys.stderr.write("runtime_probe: %s\n" % m)
    raise SystemExit(code)


def find_process(name_fragment):
    arr = (wt.DWORD * 4096)()
    got = wt.DWORD()
    if not psapi.EnumProcesses(ctypes.byref(arr), ctypes.sizeof(arr), ctypes.byref(got)):
        die("EnumProcesses failed")
    hits = []
    for i in range(got.value // ctypes.sizeof(wt.DWORD)):
        pid = arr[i]
        if not pid:
            continue
        h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if not h:
            continue
        try:
            buf = ctypes.create_unicode_buffer(512)
            n = wt.DWORD(512)
            if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(n)):
                if name_fragment.lower() in buf.value.lower():
                    hits.append((pid, buf.value))
        finally:
            k32.CloseHandle(h)
    return hits


def module_base(h):
    mods = (ctypes.c_void_p * 1024)()
    got = wt.DWORD()
    if not psapi.EnumProcessModules(h, ctypes.byref(mods), ctypes.sizeof(mods), ctypes.byref(got)):
        return None
    return mods[0]                      # first module is always the EXE itself


class Probe(object):
    def __init__(self, h):
        self.h = h

    def read(self, va, size):
        buf = (ctypes.c_ubyte * size)()
        got = ctypes.c_size_t(0)
        ok = k32.ReadProcessMemory(self.h, ctypes.c_void_p(va), ctypes.byref(buf),
                                   ctypes.c_size_t(size), ctypes.byref(got))
        if not ok or got.value != size:
            return None
        return bytes(bytearray(buf))


def load_fields(store, type_name):
    p = os.path.join(store, "fields.tsv")
    if not os.path.exists(p):
        die("missing %s" % p)
    out = []
    with io.open(p, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        for ln in fh:
            if not ln.strip():
                continue
            r = dict(zip(head, ln.rstrip("\n").split("\t")))
            if r["type"] == type_name:
                out.append(r)
    return out


def find_store():
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(8):
        c = os.path.join(root, "Database", "FFXII TZA", "_types")
        if os.path.isdir(c):
            return c
        root = os.path.dirname(root)
    die("could not locate Database/FFXII TZA/_types")


def num(x):
    x = (x or "").strip()
    return int(x, 16) if x.lower().startswith("0x") else (int(x) if x else 0)


def resolve(p, expr):
    """Resolve an address expression.

    Plain  : 0x01DFE0B4
    Deref  : [0x01F82D20]+0x48   - read the pointer, add the offset

    Most state worth validating sits behind a singleton pointer, so a probe that could only take
    absolute addresses would be unable to check any of it. Returns (address, note) or (None, why).
    """
    expr = expr.strip()
    if not expr.startswith("["):
        return num(expr), ""
    end = expr.index("]")
    ptr_va = num(expr[1:end])
    rest = expr[end + 1:].strip()
    off = num(rest[1:]) if rest.startswith("+") else 0
    raw = p.read(ptr_va, 8)
    if raw is None:
        return None, "pointer at 0x%X unreadable" % ptr_va
    inst = struct.unpack("<Q", raw)[0]
    if inst == 0:
        return None, "pointer at 0x%X is NULL - object not constructed" % ptr_va
    return inst + off, "via 0x%X -> 0x%X" % (ptr_va, inst)


def decode(raw, ctype):
    try:
        if ctype in ("int32", "uint32"):
            v = struct.unpack("<i" if ctype == "int32" else "<I", raw[:4])[0]
            return "%d (0x%08X)" % (v, v & 0xFFFFFFFF)
        if ctype == "uint16":
            v = struct.unpack("<H", raw[:2])[0]
            return "%d (0x%04X)" % (v, v)
        if ctype == "uint8":
            return "%d (0x%02X)" % (raw[0], raw[0])
        if ctype == "float":
            return repr(struct.unpack("<f", raw[:4])[0])
        if ctype.startswith("wchar_t["):
            s = raw.split(b"\x00\x00")[0]
            return repr(s.decode("utf-16-le", "replace").rstrip("\x00"))
        if ctype.startswith("int32["):
            n = min(6, len(raw) // 4)
            vals = struct.unpack("<%di" % n, raw[:4 * n])
            return "[%s%s]" % (", ".join(str(v) for v in vals), ", ..." if len(raw) > 4 * n else "")
    except Exception:
        pass
    return raw[:16].hex() + ("..." if len(raw) > 16 else "")


PAGE = 0x1000


def dump_range(p, va, size, path):
    """Page-chunked read to a file. Unreadable pages become zeros AND are counted.

    A single ReadProcessMemory over a multi-megabyte span fails completely if one page inside it
    is not committed, which for a BSS sweep is the normal case rather than the exception. Chunking
    keeps the readable pages; **counting the holes keeps the result honest**, because a snapshot
    silently full of zeros would diff clean against anything.
    """
    holes = 0
    got = 0
    with open(path, "wb") as f:
        off = 0
        while off < size:
            n = min(PAGE, size - off)
            b = p.read(va + off, n)
            if b is None:
                f.write(b"\x00" * n)
                holes += 1
            else:
                f.write(b)
                got += n
            off += n
    return got, holes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--attach", action="store_true")
    ap.add_argument("--type")
    ap.add_argument("--at")
    ap.add_argument("--deref", help="read a pointer at this VA and use it as the instance address")
    ap.add_argument("--read")
    ap.add_argument("--size", type=int, default=16)
    ap.add_argument("--check")
    ap.add_argument("--dump", help="write raw bytes to this file instead of hex to stdout")
    ap.add_argument("--store")
    a = ap.parse_args()

    hits = find_process(a.process)
    if not hits:
        die("no process matching %r is running.\n"
            "  This tool validates against the LIVE game; it cannot fabricate a runtime observation.\n"
            "  Launch FFXII_TZA.exe, then re-run." % a.process, code=3)
    if len(hits) > 1:
        sys.stderr.write("runtime_probe: %d matching processes; using pid %d\n"
                         % (len(hits), hits[0][0]))
    pid, path = hits[0]
    h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not h:
        die("OpenProcess failed for pid %d (error %d). Try an elevated shell."
            % (pid, ctypes.get_last_error()))
    try:
        base = module_base(h)
        p = Probe(h)
        print("attached  pid %d  %s" % (pid, path))
        print("module base           0x%016X" % (base or 0))
        print("PE ImageBase          0x%016X" % IMAGE_BASE)

        ok_base = (base == IMAGE_BASE)
        print("CONTROL 1 base match  %s" % ("PASS - database VAs are runtime addresses"
                                            if ok_base else "FAIL"))
        if not ok_base:
            die("base control FAILED: module loaded at 0x%X, not 0x%X. Every database VA would be "
                "wrong for this process. Refusing to report." % (base or 0, IMAGE_BASE))

        got = p.read(CONTROL_ADDR, len(CONTROL_BYTES))
        ok_read = (got == CONTROL_BYTES)
        print("CONTROL 2 read path   %s  (%s)"
              % ("PASS" if ok_read else "FAIL: got %r" % (got,), CONTROL_WHAT))
        if not ok_read:
            die("read control FAILED. A broken read returns zeroes, which is indistinguishable "
                "from a field that is genuinely zero. Refusing to report.")
        print()

        if a.attach and not (a.type or a.read or a.check):
            return 0

        if a.read:
            va = num(a.read)
            if a.dump:
                got, holes = dump_range(p, va, a.size, a.dump)
                print("%08X..%08X  %d byte(s) written, %d unreadable page(s)"
                      % (va, va + a.size, got, holes))
                return 0
            raw = p.read(va, a.size)
            print("%08X  %s" % (va, raw.hex() if raw else "<unreadable>"))
            return 0

        if a.type:
            store = a.store or find_store()
            fields = load_fields(store, a.type)
            if not fields:
                die("type %r not in the store" % a.type)
            if a.deref:
                pv = num(a.deref)
                raw = p.read(pv, 8)
                if not raw:
                    die("could not read the pointer at 0x%X" % pv)
                inst = struct.unpack("<Q", raw)[0]
                print("pointer at %08X -> instance 0x%016X" % (pv, inst))
                if inst == 0:
                    die("the singleton pointer is NULL in this process - the object does not exist "
                        "yet. That is a real observation, not a tool failure.")
            elif a.at:
                inst = num(a.at)
            else:
                die("--type needs --at <VA> or --deref <pointer VA>")
            print()
            print("%-8s %-24s %-14s %s" % ("offset", "name", "ctype", "value"))
            for f in fields:
                off, sz = num(f["offset"]), num(f["size"])
                raw = p.read(inst + off, min(sz, 64))
                print("%-8s %-24s %-14s %s"
                      % (f["offset"], f["name"], f["ctype"],
                         decode(raw, f["ctype"]) if raw else "<unreadable>"))
            return 0

        if a.check:
            rows = []
            with io.open(a.check, encoding="utf-8") as fh:
                head = fh.readline().rstrip("\n").split("\t")
                for ln in fh:
                    if ln.strip() and not ln.startswith("#"):
                        rows.append(dict(zip(head, ln.rstrip("\n").split("\t"))))
            npass = nfail = 0
            print("%-6s %-10s %-8s %-18s %-18s %s" %
                  ("id", "address", "kind", "expected", "observed", "result"))
            for r in rows:
                va, note = resolve(p, r["address"])
                kind = r["kind"]
                if va is None:
                    print("%-6s %-10s %-8s %-18s %-18s %s"
                          % (r["id"], r["address"][:10], kind, r["expect"], "-", "ERROR " + note))
                    nfail += 1
                    continue
                sz = {"u8": 1, "u16": 2, "u32": 4, "i32": 4, "f32": 4, "ptr": 8}.get(kind, 4)
                raw = p.read(va, sz)
                if raw is None:
                    obs, res = "<unreadable>", "ERROR"
                else:
                    obs = decode(raw, {"u8": "uint8", "u16": "uint16", "u32": "uint32",
                                       "i32": "int32", "f32": "float",
                                       "ptr": "ptr"}.get(kind, "uint32"))
                    if kind == "ptr":
                        obs = "0x%016X" % struct.unpack("<Q", raw)[0]
                    exp = r["expect"].strip()
                    res = "PASS" if (exp == "*" or exp in obs) else "FAIL"
                if res == "PASS":
                    npass += 1
                elif res == "FAIL":
                    nfail += 1
                print("%-6s %-10s %-8s %-18s %-18s %s"
                      % (r["id"], r["address"][:10], kind, r["expect"], obs, res))
            print()
            print("%d pass, %d fail, %d row(s)" % (npass, nfail, len(rows)))
            print("Record the outcome in the experiment's .md companion, including failures. "
                  "A failed expectation is evidence that the database is wrong, not noise.")
            return 1 if nfail else 0
    finally:
        k32.CloseHandle(h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
