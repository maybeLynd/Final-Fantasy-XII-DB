#!/usr/bin/env python3
"""minidump_triage.py - what killed the reference session, from the dump the game writes itself.

Why this is here
----------------
`EO-2` recorded that the autonomous reference session ends on its own a few tens of seconds after
launch. Measuring the exit code sharpened it to **`0xE06D7363`**, the MSVC unhandled-C++-exception
code - and the game drops a `Dump_*.dmp` beside its executable when it goes. The mod clients'
directory holds twenty of them, so this is a standing condition on this machine rather than
something the harness provoked.

There is no `cdb.exe` here, so this parses the minidump directly: header, stream directory,
exception record, and the module list needed to say **which module the faulting address is in**.

Two things this got wrong on the first attempt, both recorded rather than quietly fixed
-----------------------------------------------------------------------------------------
1. **`ModuleNameRva` is at offset 20 of `MINIDUMP_MODULE`, not 32.** Reading the wrong field
   produced pages of mojibake that looked like module names. A parser that prints garbage instead
   of failing is worse than one that refuses.
2. **It slurped the whole file.** These dumps are full-memory: the one under test is **2.0 GB**,
   and reading it took longer than the tool's own timeout. It now seeks.

What it does NOT do
-------------------
No symbols, no stack walk, no C++ exception-object decoding. It answers *what code, at what address,
in which module* - which turns "it crashes" into an address the static database can be pointed at.
Anything beyond that is a claim this tool cannot support.
"""
import argparse
import glob
import os
import struct
import sys

KNOWN = {
    0xE06D7363: "MSVC unhandled C++ exception (a throw nobody caught)",
    0xC0000005: "access violation",
    0xC0000094: "integer divide by zero",
    0xC000001D: "illegal instruction",
    0x80000003: "breakpoint",
    0xC00000FD: "stack overflow",
}
# param[0] of an MSVC throw is the EH magic; param[1] is the exception object, param[2] the
# ThrowInfo. A NULL object with the magic present is the signature of a RETHROW.
EH_MAGIC = (0x19930520, 0x19930521, 0x19930522, 0x01994000)


def at(f, off, n):
    f.seek(off)
    return f.read(n)


def u32(f, off):
    return struct.unpack("<I", at(f, off, 4))[0]


def u64(f, off):
    return struct.unpack("<Q", at(f, off, 8))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump", nargs="?", help="a .dmp file; default = the newest beside the game")
    ap.add_argument("--dir",
                    default=r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64")
    ap.add_argument("--modules", action="store_true", help="list every loaded module")
    a = ap.parse_args()

    path = a.dump
    if not path:
        cands = sorted(glob.glob(os.path.join(a.dir, "Dump_*.dmp")), key=os.path.getmtime)
        if not cands:
            print("no Dump_*.dmp in %s" % a.dir)
            return 1
        path = cands[-1]

    size = os.path.getsize(path)
    with open(path, "rb") as f:
        if at(f, 0, 4) != b"MDMP":
            print("not a minidump")
            return 1
        print("dump    %s  (%.2f GB)" % (os.path.basename(path), size / (1 << 30)))
        nstreams = u32(f, 8)
        dir_rva = u32(f, 12)
        st = {}
        for i in range(nstreams):
            t, sz, rva = struct.unpack("<III", at(f, dir_rva + i * 12, 12))
            st[t] = (sz, rva)

        if 6 not in st:
            print("no exception stream -- this dump was not written by a crash")
            return 1
        _sz, rva = st[6]
        tid = u32(f, rva)
        exc = rva + 8
        code = u32(f, exc)
        flags = u32(f, exc + 4)
        addr = u64(f, exc + 16)
        nparams = u32(f, exc + 24)
        params = [u64(f, exc + 32 + 8 * i) for i in range(min(nparams, 15))]

        print()
        print("thread        %d" % tid)
        print("code          0x%08X   %s" % (code, KNOWN.get(code, "unrecognised")))
        print("flags         0x%08X%s" % (flags, "  NONCONTINUABLE" if flags & 1 else ""))
        print("address       0x%016X   (the raiser, not the culprit)" % addr)
        for i, p in enumerate(params):
            note = ""
            if i == 0 and p in EH_MAGIC:
                note = "   <- MSVC EH magic: this is a real C++ throw"
            if i == 1:
                note = "   <- exception object" + (" is NULL: RETHROW with none in flight" if not p
                                                   else "")
            if i == 2 and not p:
                note = "   <- ThrowInfo NULL, consistent with a rethrow"
            print("param[%d]      0x%016X%s" % (i, p, note))

        if 4 not in st:
            return 0
        _msz, mrva = st[4]
        n = u32(f, mrva)
        mods = []
        for i in range(n):
            o = mrva + 4 + i * 108                 # MINIDUMP_MODULE is 108 bytes on x64
            base = u64(f, o)
            sz = u32(f, o + 8)
            name_rva = u32(f, o + 20)              # NOT +32 -- that is VersionInfo
            nlen = u32(f, name_rva)
            if nlen > 4096:                        # refuse rather than print mojibake
                mods.append((base, sz, "<name length %d rejected>" % nlen))
                continue
            name = at(f, name_rva + 4, nlen).decode("utf-16-le", "replace")
            mods.append((base, sz, name))
        mods.sort()

        print()
        owner = [m for m in mods if m[0] <= addr < m[0] + m[1]]
        if owner:
            base, sz, name = owner[0]
            print("faulting module   %s" % name)
            print("                  base 0x%016X  size 0x%X  offset +0x%X" % (base, sz, addr - base))
            if os.path.basename(name).lower() == "ffxii_tza.exe":
                print("                  -> DATABASE VA 0x%08X" % addr)
        else:
            print("faulting address is in none of the %d listed modules" % len(mods))

        print()
        print("modules loaded    %d" % len(mods))
        # A third-party instrumentation module in a supposedly clean process is the finding.
        WATCH = ("xiionline", "trampoline", "tkmalloc", "simplelog", "dinput8", "xinput",
                 "dynamorio", "drrun", "dr_", "drmemory", "detour", "reshade", "specialk")
        # Path matters, not just the name. The first version flagged System32's `dinput8.dll` and
        # `XINPUT9_1_0.dll`, plus the game's OWN shipped `xinput1_3.dll`, as injected -- three
        # false positives in one report. A module under System32/SysWOW64, or in the game's own
        # directory, is the platform or the game, not instrumentation.
        gamedir = os.path.dirname(os.path.abspath(a.dir)).lower()
        def suspect(path):
            low = path.lower()
            if r"\windows\system32" in low or r"\windows\syswow64" in low:
                return False
            if os.path.dirname(low).startswith(gamedir):
                return False
            return any(k in os.path.basename(low) for k in WATCH)
        flagged = [m for m in mods if suspect(m[2])]
        if flagged:
            print("INSTRUMENTATION / INJECTED MODULES PRESENT:")
            for base, sz, name in flagged:
                print("  0x%016X  %s" % (base, name))
        else:
            print("no watched instrumentation module in the list")
        if a.modules:
            print()
            for base, sz, name in mods:
                print("  0x%016X  %8X  %s" % (base, sz, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
