#!/usr/bin/env python3
"""struct_map.py - map a structure's fields by what the code actually READS and WRITES.

Written 2026-09-02 after making the same mistake twice in two passes: a 36-byte record had
4 header bytes and 16 bytes of masks accounted for, and the remaining 16 were labelled
"analog axis bytes" because that label was already in hand. The writer covers eight of them.

Leftover space is not evidence of what occupies it. This tool exists so that judgement is not
made by hand:

  * every offset is reported with its access **role** (read / write) and operand size
  * offsets that are **read but never written** are listed separately
  * byte ranges inside the stride that **nothing touches** are listed as UNACCOUNTED

An unaccounted range is a question, never a label.

WHAT THIS TOOL CANNOT SEE - read this before trusting an UNACCOUNTED range
-------------------------------------------------------------------------
It only follows a base that is materialised **inside the function being scanned** - a
`lea reg,[rip+BASE]` or a `mov reg,[any+FIELD]`. A structure reached through a **pointer passed
as an argument** is invisible to it, and most structures are reached that way.

On its first real target it reported 640 of 660 bytes UNACCOUNTED while the record was in fact
heavily used - the writers received the record as a parameter. So:

    UNACCOUNTED means "no access reachable from this taint source", NOT "unused".

Reading it as "unused" would commit exactly the error this tool exists to prevent. Treat a large
UNACCOUNTED span as a prompt to find the other callers, not as a finding.

Two ways to name the structure:

  --base VA        registers that receive `lea reg, [rip+disp]` -> VA, and anything derived
                   from them by add/lea, are tainted.
  --via-field D    registers loaded by `mov reg, [any + D]` are tainted (a pointer field, e.g.
                   0x698). Bias with --bias if two paths reach one object at different offsets.

  struct_map.py --base 0x022CAE98 --stride 0x294
  struct_map.py --via-field 0x6A0 --stride 0x250
"""
import argparse, bisect, collections, io, struct, sys
import kit_paths as KP  # noqa: E402
import os

# Windows x64 calling convention: a call destroys these and preserves everything else.
VOLATILE = frozenset(("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"))

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    from capstone.x86 import X86_OP_MEM, X86_OP_REG, X86_REG_RIP
except ImportError:
    sys.exit("capstone is required: pip install capstone")

EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
NONWRITE = {"cmp", "test", "push", "jmp", "je", "jne", "ja", "jb", "jae", "jbe",
            "jg", "jl", "jge", "jle", "ret", "nop"}
WRITERS = {"mov", "or", "and", "xor", "add", "sub", "inc", "dec", "movss", "movsd", "movups"}


def load_image(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from('<I', d, 0x3C)[0]
    n = struct.unpack_from('<H', d, pe + 6)[0]
    optsz = struct.unpack_from('<H', d, pe + 20)[0]
    base = struct.unpack_from('<Q', d, pe + 24 + 24)[0]
    off = pe + 24 + optsz
    secs = []
    for i in range(n):
        o = off + i * 40
        secs.append((d[o:o+8].rstrip(b'\0').decode(), struct.unpack_from('<I', d, o+12)[0],
                     struct.unpack_from('<I', d, o+8)[0], struct.unpack_from('<I', d, o+20)[0],
                     struct.unpack_from('<I', d, o+16)[0]))
    return d, base, secs


def load_funcs(path):
    fs = []
    for i, l in enumerate(io.open(path, encoding="utf-8", errors="replace")):
        if i == 0:
            continue
        p = l.rstrip("\n").split("\t")
        if len(p) > 3 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                fs.append((int(p[0], 16), int(p[2]), p[1], p[3]))
            except ValueError:
                pass
    fs.sort()
    return fs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--functions", default=FUNCS)
    ap.add_argument("--base", type=lambda x: int(x, 16), help="array base VA (hex)")
    ap.add_argument("--via-field", type=lambda x: int(x, 0), help="pointer field displacement")
    ap.add_argument("--bias", type=lambda x: int(x, 0), default=0)
    ap.add_argument("--stride", type=lambda x: int(x, 0), default=0)
    ap.add_argument("--max-offset", type=lambda x: int(x, 0), default=0x1000)
    a = ap.parse_args(argv)
    if not a.base and a.via_field is None:
        ap.error("give --base or --via-field")

    d, imgbase, secs = load_image(a.exe)
    text = [s for s in secs if s[0] == '.text'][0]
    TVA, TSZ, TRAW, TRSZ = text[1] + imgbase, text[2], text[3], text[4]
    fs = load_funcs(a.functions)
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

    fields = collections.defaultdict(lambda: {"r": 0, "w": 0, "sz": set(), "fn": set()})
    for e, sz, nm, ow in fs:
        if not (TVA <= e < TVA + TSZ) or sz <= 0 or sz > 20000:
            continue
        o = TRAW + (e - TVA)
        taint = {}
        for ins in md.disasm(d[o:o+sz], e):
            ops = ins.operands
            if ins.mnemonic == "call":
                # A call destroys only the VOLATILE registers. Clearing everything was wrong and
                # it inflated the one number this tool exists to report: dropping a base held in
                # rbx or rdi across a call hides every later access through it, so a range that is
                # merely unreached after the first call was printed as UNACCOUNTED. Found when a
                # vtable-seeded sweep of a 0x668 object missed a write the document already knew
                # about - `mov rdi, rcx` then a call, and +0x664 vanished. Restoring the ABI rule
                # took that sweep from 51 accesses over 23 displacements to 144 over 63.
                # actor_field_scan.py, which built the installed censuses, already did this right.
                for _r in list(taint):
                    if md.reg_name(_r) in VOLATILE:
                        del taint[_r]
            # --- taint sources -------------------------------------------------
            if ins.mnemonic == "lea" and a.base and len(ops) == 2 and \
               ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
                if ins.address + ins.size + ops[1].mem.disp == a.base:
                    taint[ops[0].reg] = 0; continue
            if ins.mnemonic == "mov" and a.via_field is not None and len(ops) == 2 and \
               ops[0].type == X86_OP_REG and ops[1].type == X86_OP_MEM and \
               ops[1].size == 8 and ops[1].mem.disp == a.via_field:
                taint[ops[0].reg] = a.bias; continue
            # --- propagation ---------------------------------------------------
            if ins.mnemonic in ("mov", "add", "lea") and len(ops) == 2 and \
               ops[0].type == X86_OP_REG:
                src = ops[1]
                if src.type == X86_OP_REG and src.reg in taint:
                    taint[ops[0].reg] = taint[src.reg]; continue
                if src.type == X86_OP_MEM and src.mem.base in taint and ins.mnemonic == "lea":
                    taint[ops[0].reg] = taint[src.mem.base] + src.mem.disp; continue
            # --- accesses ------------------------------------------------------
            for oi, op in enumerate(ops):
                # The base may arrive in the INDEX register: `lea rax,[rip+BASE]` then
                # `movzx eax, byte ptr [rcx + rax]`, where rcx holds record*stride.
                # Missing this made the tool's first run near-empty and, usefully, exposed
                # that the accessors did not all share one base constant.
                hit = None
                if op.type == X86_OP_MEM and op.size in (1, 2, 4, 8):
                    if op.mem.base in taint:
                        hit = taint[op.mem.base]
                    elif op.mem.index in taint and op.mem.scale == 1:
                        hit = taint[op.mem.index]
                if hit is not None:
                    off = hit + op.mem.disp
                    if a.stride:
                        off %= a.stride
                    if 0 <= off < a.max_offset:
                        f = fields[off]
                        f["sz"].add(op.size); f["fn"].add(nm)
                        if oi == 0 and ins.mnemonic in WRITERS:
                            f["w"] += 1
                        else:
                            f["r"] += 1
            if ins.mnemonic not in NONWRITE and ops and ops[0].type == X86_OP_REG:
                taint.pop(ops[0].reg, None)

    if not fields:
        print("no tainted accesses found - check --base / --via-field")
        return 1
    print("offset   size  reads  writes  functions")
    covered = []
    for off in sorted(fields):
        f = fields[off]
        w = max(f["sz"])
        covered.append((off, w))
        print("  +0x%03X  %-4s %6d %7d  %s" % (off, "/".join(str(s) for s in sorted(f["sz"])),
                                               f["r"], f["w"], len(f["fn"])))
    ro = [o for o in sorted(fields) if fields[o]["w"] == 0]
    print("\nread but NEVER written: %d offset(s)" % len(ro))
    if ro:
        print("   " + ", ".join("+0x%03X" % o for o in ro))
    if a.stride:
        seen = bytearray(a.stride)
        for off, w in covered:
            for i in range(off, min(off + w, a.stride)):
                seen[i] = 1
        gaps, i = [], 0
        while i < a.stride:
            if not seen[i]:
                j = i
                while j < a.stride and not seen[j]:
                    j += 1
                gaps.append((i, j - i)); i = j
            else:
                i += 1
        total = sum(g[1] for g in gaps)
        print("\nUNACCOUNTED inside the %d-byte stride: %d byte(s) in %d range(s)"
              % (a.stride, total, len(gaps)))
        for off, ln in gaps:
            print("   +0x%03X .. +0x%03X   (%d bytes)" % (off, off + ln - 1, ln))
        print("\n   An unaccounted range is a QUESTION, not a label.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
