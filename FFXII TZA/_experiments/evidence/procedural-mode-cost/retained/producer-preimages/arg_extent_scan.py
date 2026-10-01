#!/usr/bin/env python3
"""arg_extent_scan.py - how far into its first argument does a function actually reach?

WHY THIS EXISTS. When a caller hands `object + 0xA0` to a function, the type store has to decide how
many bytes that sub-object occupies. The cheap answer is the distance to the next offset anybody
happened to touch - and that answer is wrong in both directions. It over-claims when nothing lives
there, and it UNDER-claims when the callee reaches further than the caller ever does: `003F80D0` is
handed `object+0xA0D0` and reads its own `+0x984`, which is `object+0xAA54`, past a field the store
had already declared separately.

So the extent of a sub-object is a property of its callee, not of its neighbours. This measures it:
`rcx` on entry is tainted, the same small propagation as `singleton_field_scan` is applied, and every
displacement used off the taint is reported, along with the highest one - the floor on the extent.

    python arg_extent_scan.py --self-test
    python arg_extent_scan.py 003F8EC0
    python arg_extent_scan.py 003F8EC0 --depth 1        also follow calls that pass the taint on

DEPTH. At `--depth 0` (the default) the scan stops at the function's own body. At `--depth 1` it also
enters a callee when the tainted register is that callee's `rcx` at the call - which is how a thin
dispatcher's real extent is found - and adds that callee's reach. It does not go further, and it does
not follow a pointer LOADED from the object: `[rcx+8]` is a different object, and its fields are not
this one's.

A FLOOR, ALWAYS. The result says "this function touches at least this far". It never says the object
ends there, because a sibling function may reach further - which is exactly why the caller-side
number was untrustworthy in the first place.

CONTROLS. `--self-test` checks three functions whose reach is known by hand from the bytes:
`00273A20` reaches only `+0x00` (nine bytes: a null test), `004FE3C0` reaches `+0x10` (it clears
three qwords), and `003F80D0` reaches `+0x984` (a single `test byte ptr [rcx+0x984], 1`). The last is
the case that motivated the script.
"""
import argparse
import collections
import os
import struct
import sys

import kit_paths as KP

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_WRITE
    from capstone.x86 import (X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP,
                              X86_REG_INVALID, X86_REG_RCX, X86_REG_RBX, X86_REG_RBP,
                              X86_REG_RSI, X86_REG_RDI, X86_REG_R12, X86_REG_R13,
                              X86_REG_R14, X86_REG_R15)
except ImportError:
    sys.stderr.write("arg_extent_scan: needs capstone (pip install capstone)\n")
    raise SystemExit(2)

EXE = os.path.join(KP.WORK, "exe", "FFXII_TZA.exe")
GRAPH = os.path.join(KP.WORK, "graph", "functions.tsv")

# Windows x64 callee-saved registers: these survive a call, so taint on them must too.
NONVOLATILE = frozenset((X86_REG_RBX, X86_REG_RBP, X86_REG_RSI, X86_REG_RDI,
                         X86_REG_R12, X86_REG_R13, X86_REG_R14, X86_REG_R15))


class Image(object):
    def __init__(self, path):
        d = open(path, "rb").read()
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        opt = struct.unpack_from("<H", d, pe + 20)[0]
        self.base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
        self.secs = []
        for i in range(nsec):
            o = pe + 24 + opt + i * 40
            vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
            self.secs.append((va, vsz, ptr, rsz))
        self.d = d

    def read(self, va, n):
        r = va - self.base
        for sva, vsz, ptr, rsz in self.secs:
            if sva <= r < sva + rsz:
                avail = rsz - (r - sva)
                return self.d[ptr + (r - sva):ptr + (r - sva) + min(n, avail)]
        return None


def load_functions():
    fns = {}
    with open(GRAPH, encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            try:
                entry, size = int(f[0], 16), int(f[2])
            except (ValueError, IndexError):
                continue
            if size > 0:
                fns[entry] = (size, f[1])
    return fns


def reach(img, md, fns, entry, depth, seen=None):
    """offset -> {'r','w','lea','widths','sites'} for everything reached off rcx-at-entry."""
    if seen is None:
        seen = set()
    if entry in seen or entry not in fns:
        return {}, {}
    seen.add(entry)
    size, name = fns[entry]
    code = img.read(entry, min(size, 0x8000))
    if not code:
        return {}, {}
    out = collections.defaultdict(
        lambda: {"r": 0, "w": 0, "lea": 0, "widths": set(), "sites": []})
    arrays = collections.defaultdict(
        lambda: {"n": 0, "scales": set(), "widths": set(), "sites": []})
    tainted = {X86_REG_RCX}
    try:
        insns = list(md.disasm(code, entry))
    except Exception:
        return {}, {}
    for ins in insns:
        ops = ins.operands
        for op in ops:
            if op.type != X86_OP_MEM or op.mem.base == X86_REG_RIP:
                continue
            if op.mem.base not in tainted or ins.mnemonic == "nop":
                continue
            if op.mem.index != X86_REG_INVALID:
                # INDEXED: [base + index*scale + disp]. The displacement is an ARRAY BASE, not a
                # field, and the scale is a lower bound on the stride - MSVC folds a multiply into
                # the index (lea r,[r+r*4] then *8 gives a 0x28 stride), so `scale` under-reports.
                # Kept apart from the field table for exactly that reason, and reported so an
                # object that is mostly an array does not read as an object that is mostly empty.
                d = op.mem.disp
                if 0 <= d <= 0x400000:
                    a = arrays[d]
                    a["scales"].add(op.mem.scale)
                    a["widths"].add(op.size)
                    a["n"] += 1
                    if len(a["sites"]) < 3:
                        a["sites"].append((ins.address, name,
                                           "%s %s" % (ins.mnemonic, ins.op_str)))
                continue
            d = op.mem.disp
            if d < 0 or d > 0x400000:
                continue
            rec = out[d]
            if ins.mnemonic == "lea":
                rec["lea"] += 1
            else:
                rec["widths"].add(op.size)
                if op.access & CS_AC_WRITE:
                    rec["w"] += 1
                else:
                    rec["r"] += 1
            if len(rec["sites"]) < 4:
                rec["sites"].append((ins.address, name,
                                     "%s %s" % (ins.mnemonic, ins.op_str)))

        if ins.mnemonic == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[0].reg in tainted and ops[1].type == X86_OP_IMM:
            d = ops[1].imm
            if 0 < d <= 0x400000:
                rec = out[d]
                rec["lea"] += 1
                if len(rec["sites"]) < 4:
                    rec["sites"].append((ins.address, name,
                                         "%s %s" % (ins.mnemonic, ins.op_str)))

        # a call or tail jump that passes the taint on as ITS rcx
        if depth > 0 and ins.mnemonic in ("call", "jmp") and ops and ops[0].type == X86_OP_IMM \
                and X86_REG_RCX in tainted:
            sub, subarr = reach(img, md, fns, ops[0].imm, depth - 1, seen)
            for d, rec in subarr.items():
                a = arrays[d]
                a["n"] += rec["n"]; a["scales"] |= rec["scales"]; a["widths"] |= rec["widths"]
                for x in rec["sites"]:
                    if len(a["sites"]) < 3:
                        a["sites"].append(x)
            for d, rec in sub.items():
                dst = out[d]
                dst["r"] += rec["r"]
                dst["w"] += rec["w"]
                dst["lea"] += rec["lea"]
                dst["widths"] |= rec["widths"]
                for s in rec["sites"]:
                    if len(dst["sites"]) < 4:
                        dst["sites"].append(s)

        if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                and ops[1].type == X86_OP_REG and ops[1].reg in tainted:
            tainted.add(ops[0].reg)
        elif ins.mnemonic == "call":
            # NOT a full clear. The Windows x64 ABI makes RBX, RBP, RSI, RDI and R12-R15
            # callee-saved, and `mov rbx, rcx` before a call is the single most common way a
            # function keeps its first argument. Clearing everything here made 003F8EC0 - 284 bytes
            # that spend most of their length working on [rbx + 0x52xx] - report that it "reaches
            # nothing off its first argument", which is how the largest unexplained span on
            # ManagerSingleton0209BE80 stayed unexplained. Volatile registers still die.
            tainted &= NONVOLATILE
        else:
            for op in ops:
                if op.type == X86_OP_REG and (op.access & CS_AC_WRITE) and op.reg in tainted:
                    tainted.discard(op.reg)
    return out, arrays


def members_of(img, md, fns, slot, at, window=6, static=False):
    """Every function an embedded sub-object's address is handed to.

    A sub-object reached only through its parent's pointer slot has no callers of its own in a call
    graph: the call site passes `parent + 0xNNN`, and nothing records that the argument was this
    object. So its member functions are found the only way they can be - by taking each site where
    that address is formed and reading forward to the call it feeds.

    `window` is how many instructions after the address is formed a call still counts. Short on
    purpose: the point is the call the address was computed FOR, not the next call in the function.
    """
    import singleton_field_scan as SFS
    sfns = SFS.functions()
    acc = SFS.accessors_for(img, md, sfns, slot, static)
    found, _loaders = SFS.scan(img, md, slot, sfns, acc, static)
    sites = found.get(at, {}).get("sites", [])
    out = []
    for va, fname, _txt in sites:
        owner = owner_of(fns, va)
        if owner is None:
            continue
        code = img.read(owner[0], owner[1])
        if not code:
            continue
        seen_site = False
        n = 0
        for ins in md.disasm(code, owner[0]):
            if ins.address == va:
                seen_site = True
                continue
            if not seen_site:
                continue
            n += 1
            if n > window:
                break
            if ins.mnemonic in ("call", "jmp") and ins.operands \
                    and ins.operands[0].type == X86_OP_IMM:
                out.append((va, fname, ins.address, ins.operands[0].imm))
                break
    return out


def owner_of(fns, addr):
    best = None
    for entry, (size, _n) in fns.items():
        if entry <= addr < entry + size and (best is None or entry > best[0]):
            best = (entry, size)
    return best


def print_arrays(arr):
    if not arr:
        return
    print()
    print("  INDEXED ACCESSES - an array base, not a field. `scale` is a LOWER BOUND on the stride:")
    print("  MSVC folds a multiply into the index (lea r,[r+r*4] then *8 is a 0x28 stride), so a")
    print("  scale of 8 can mean any multiple of 8. Declaring a stride needs the lea read by hand.")
    print("  %-10s %5s %-10s %-8s %s" % ("base", "uses", "scales", "widths", "site"))
    for d in sorted(arr):
        rec = arr[d]
        sc = ",".join(str(x) for x in sorted(rec["scales"]))
        w = ",".join(str(x) for x in sorted(rec["widths"])) or "-"
        st = rec["sites"][0] if rec["sites"] else (0, "", "")
        print("  +0x%-8X %5d %-10s %-8s %08X %s" % (d, rec["n"], sc, w, st[0], st[2][:40]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fn", nargs="?")
    ap.add_argument("--via-slot", help="a .data pointer slot, e.g. 0x0209BE80")
    ap.add_argument("--at", help="the offset of the embedded sub-object, e.g. 0xA0")
    ap.add_argument("--static", action="store_true",
                    help="the slot address IS the object (formed by lea), not a pointer slot")
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--depth", type=int, default=0)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = Image(a.exe)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    fns = load_functions()

    if a.self_test:
        ok = True
        for entry, want, why in ((0x00273A20, 0x000, "nine bytes: a null test on [rcx]"),
                                 (0x004FE3C0, 0x010, "clears three qwords"),
                                 (0x003F80D0, 0x984, "one test byte ptr [rcx+0x984], 1"),
                                 (0x003F8EC0, 0x52C6, "keeps rcx in rbx ACROSS a call - the "
                                  "callee-saved case a full clear at a call loses entirely")):
            r, _a = reach(img, md, fns, entry, 0)
            got = max(r) if r else -1
            good = (got == want)
            ok = ok and good
            print("  %08X  highest +0x%-5X expected +0x%-5X %s  %s"
                  % (entry, got, want, "ok" if good else "CONTROL BROKEN", why))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    if a.via_slot and a.at:
        slot, at = int(a.via_slot, 16), int(a.at, 16)
        mem = members_of(img, md, fns, slot, at, static=a.static)
        print("slot %08X, sub-object +0x%X: %d member call site(s)" % (slot, at, len(mem)))
        print()
        union = collections.defaultdict(
            lambda: {"r": 0, "w": 0, "lea": 0, "widths": set(), "sites": []})
        uarr = collections.defaultdict(
            lambda: {"n": 0, "scales": set(), "widths": set(), "sites": []})
        callees = []
        for site, owner, callva, callee in mem:
            if callee not in callees:
                callees.append(callee)
            print("  %08X in %-22s -> call %08X at %08X"
                  % (site, fns.get(owner_of(fns, site)[0], (0, "?"))[1][:22], callee, callva))
        print()
        for callee in callees:
            r, ra = reach(img, md, fns, callee, a.depth)
            for d, rec in ra.items():
                u = uarr[d]
                u["n"] += rec["n"]; u["scales"] |= rec["scales"]; u["widths"] |= rec["widths"]
                for x in rec["sites"]:
                    if len(u["sites"]) < 3:
                        u["sites"].append(x)
            for d, rec in r.items():
                u = union[d]
                u["r"] += rec["r"]; u["w"] += rec["w"]; u["lea"] += rec["lea"]
                u["widths"] |= rec["widths"]
                for x in rec["sites"]:
                    if len(u["sites"]) < 4:
                        u["sites"].append(x)
        if not union:
            print("  no member reaches anything off the object")
            return 0
        hi = max(union)
        print("  %d distinct callee(s); highest displacement +0x%X -> at least 0x%X bytes"
              % (len(callees), hi,
                 hi + (max(union[hi]["widths"]) if union[hi]["widths"] else 1)))
        print()
        print("  %-10s %5s %5s %4s %-8s %s"
              % ("offset", "reads", "writes", "lea", "widths", "site"))
        for d in sorted(union):
            rec = union[d]
            w = ",".join(str(x) for x in sorted(rec["widths"])) or "-"
            st = rec["sites"][0] if rec["sites"] else (0, "", "")
            print("  +0x%-8X %5d %5d %4d %-8s %08X %s"
                  % (d, rec["r"], rec["w"], rec["lea"], w, st[0], st[2][:40]))
        print()
        print_arrays(uarr)
        print()
        print("A FLOOR: the union of what these members touch, not the object's extent.")
        return 0

    if not a.fn:
        ap.error("give a function address, --via-slot/--at, or --self-test")
    entry = int(a.fn, 16)
    r, ra = reach(img, md, fns, entry, a.depth)
    size, name = fns.get(entry, (0, "?"))
    print("%08X %s (%d B), depth %d" % (entry, name, size, a.depth))
    if not r:
        print("  reaches nothing off its first argument")
        return 0
    print("  highest displacement touched: +0x%X  ->  at least 0x%X bytes"
          % (max(r), max(r) + max(max(x["widths"]) if x["widths"] else 1
                                 for x in r.values())))
    print()
    print("  %-10s %5s %5s %4s %-8s %s" % ("offset", "reads", "writes", "lea", "widths", "site"))
    for d in sorted(r):
        rec = r[d]
        w = ",".join(str(x) for x in sorted(rec["widths"])) or "-"
        s = rec["sites"][0] if rec["sites"] else (0, "", "")
        print("  +0x%-8X %5d %5d %4d %-8s %08X %s"
              % (d, rec["r"], rec["w"], rec["lea"], w, s[0], s[2][:40]))
    print_arrays(ra)
    print()
    print("A FLOOR: this is what THIS function touches. A sibling may reach further.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
