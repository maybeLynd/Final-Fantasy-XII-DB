#!/usr/bin/env python3
"""singleton_field_scan.py - every offset the IMAGE uses on a singleton, taken from the bytes.

WHY THIS EXISTS. A pointer-slot singleton has no declaration to read: it is a `void*` in `.data`, and
what it is made of exists only as the displacements the code uses after loading it. So the field map
of such an object is not something to be transcribed from prose - prose is where the twenty-one
offsets this store cited for `ManagerSingleton0209BE80` came from, while the type store held nothing
at all. This measures them instead.

HOW. For each function that loads the slot (`mov reg, [rip+disp]` resolving to the slot's address), a
deliberately small taint runs forward to the end of the function body:

* the destination register of that load is tainted;
* `mov r2, r1` with `r1` tainted taints `r2`;
* ANY other write to a register clears its taint, including the implicit writes of `call`;
* every memory operand `[tainted + disp]` (no index) is recorded, with its width and whether the
  instruction reads or writes it.

WHAT IT DELIBERATELY DOES NOT DO, because the point is a floor nobody has to distrust:

* it does not follow the pointer into callees, so an offset only a callee touches is missed;
* it does not resolve `[tainted + index*scale + disp]`, because the displacement of an indexed
  access is the base of an array, not a field - a different claim needing a stride;
* it does not survive a `call`, so it under-counts rather than inventing continuity across one;
* it does not merge adjacent offsets into a span. Two dwords are two dwords until something says
  otherwise.

Every one of those makes the output a LOWER BOUND. An offset it reports is used; an offset it misses
may still exist. That asymmetry is the whole design: a field map built from this can be trusted not
to contain anything the image does not do.

    python singleton_field_scan.py --self-test
    python singleton_field_scan.py --slot 0x0209BE80
    python singleton_field_scan.py --slot 0x0209BE80 --min-refs 2

CONTROL. `--self-test` scans `0209BE80` and requires three offsets that are known independently of
this script: `+0x10F68`, which the per-frame update gate's contract calls the subsystem enable flags;
`+0xAA44`, which the boot path sets to 1 at `0028F911`; and `+0x5380`, a sub-object the first version
of this script LOST - it is reached by `add rcx, 0x5380` at `0028E2AB` rather than by a `lea`, so
address arithmetic outside a memory operand was invisible. Six sibling sub-objects were present and
that one was not, which is exactly the shape of a silent under-count: the output looked complete.
"""
import argparse
import collections
import os
import struct
import sys

import kit_paths as KP

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_AC_READ, CS_AC_WRITE
    from capstone.x86 import (X86_OP_MEM, X86_OP_REG, X86_OP_IMM, X86_REG_RIP,
                              X86_REG_INVALID, X86_REG_RAX,
                              X86_REG_RBX, X86_REG_RBP, X86_REG_RSI, X86_REG_RDI,
                              X86_REG_R12, X86_REG_R13, X86_REG_R14, X86_REG_R15)
except ImportError:
    sys.stderr.write("singleton_field_scan: needs capstone (pip install capstone)\n")
    raise SystemExit(2)

# How many sites to keep per offset. This used to be a hard 6 and that was a SILENT TRUNCATION, not
# a display limit: `arg_extent_scan --via-slot` builds a sub-object's MEMBER SET from these sites, so
# an object with more than six address-taking sites lost members without saying so. +0x8FA0 had
# exactly six kept and a seventh, 0028E220, which tail-jumps to 002BDCE0 - the only function that
# WRITES the three pointers its other members merely read. The question "who writes them?" was
# unanswerable because of this constant.
SITE_CAP = 64

EXE = os.path.join(KP.WORK, "exe", "FFXII_TZA.exe")
GRAPH = os.path.join(KP.WORK, "graph", "functions.tsv")

# Windows x64 callee-saved registers. `mov rbx, rcx` before a call is the commonest way a function
# keeps a pointer, so taint on these MUST survive a call - clearing them all cost this scan real
# offsets, and cost arg_extent_scan a whole 0x52C6-byte sub-object.
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


def functions():
    out = []
    with open(GRAPH, encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            try:
                entry, size = int(f[0], 16), int(f[2])
            except (ValueError, IndexError):
                continue
            if 0 < size <= 0x8000:
                out.append((entry, size, f[1]))
    return out



def accessors_for(img, md, fns, slot, static=False):
    """Functions whose whole body is `mov rax, [rip -> slot]` then `ret`.

    THE BLIND SPOT THIS CLOSES. A scan that only follows functions which load the slot THEMSELVES
    sees nothing of a singleton reached through a `GetInstance()` accessor - and that is the ordinary
    C++ shape. `01F7F598` is loaded directly by three functions and returned by `00189120`, which has
    117 callers; the store's 44 field rows for that singleton all come from a function this scan
    could not see, because the object arrives in `rcx` from the accessor and the slot is never
    mentioned. `0209BE80` happens to have no accessor, which is the only reason the first version of
    this script worked at all.
    """
    out = set()
    for entry, size, _name in fns:
        if size > 0x20:
            continue
        code = img.read(entry, size)
        if not code:
            continue
        try:
            ins = list(md.disasm(code, entry))
        except Exception:
            continue
        if len(ins) < 2:
            continue
        a, b = ins[0], ins[1]
        if b.mnemonic != "ret":
            continue
        ops = a.operands
        if (len(ops) != 2 or ops[0].type != X86_OP_REG
                or ops[1].type != X86_OP_MEM or ops[1].mem.base != X86_REG_RIP):
            continue
        target = a.address + a.size + ops[1].mem.disp
        if a.mnemonic == "mov" and not static and target == slot:
            out.add(entry)            # `mov rax, [slot]; ret` - the slot HOLDS the object
        elif a.mnemonic == "lea" and static and target == slot:
            out.add(entry)            # `lea rax, [obj]; ret`  - the slot IS the object
    return out


def scan(img, md, slot, fns, accessors=None, static=False, span=0):
    """offset -> {"r": n, "w": n, "widths": set, "sites": [(va, fname, text)]}"""
    found = collections.defaultdict(lambda: {"r": 0, "w": 0, "lea": 0, "widths": set(), "sites": []})
    loaders = set()
    accessors = accessors or set()
    for entry, size, name in fns:
        code = img.read(entry, size)
        if not code:
            continue
        try:
            insns = list(md.disasm(code, entry))
        except Exception:
            continue
        # cheap pre-filter: the slot's address must be a rip target somewhere in the body
        direct = any(op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP
                     and (ins.address + ins.size + op.mem.disp) == slot
                     for ins in insns for op in ins.operands)
        viacall = any(ins.mnemonic in ("call", "jmp") and ins.operands
                      and ins.operands[0].type == X86_OP_IMM
                      and ins.operands[0].imm in accessors for ins in insns)

        # THE THIRD PATTERN, and for small static structs it is the ONLY one. A compiler addressing
        # a static object's fields does not load a base at all - each field gets its own
        # RIP-relative operand, `mov eax, [rip -> base+k]`. `BattleFormulaScratch` has 45 declared
        # rows and ZERO functions that form its base; all 43 of its dword-aligned addresses are
        # referenced individually, by 47 functions for the first one alone. Without this the scan
        # reports such a type as untouched, which is the most misleading answer it can give.
        if static and span:
            for ins in insns:
                for op in ins.operands:
                    if op.type != X86_OP_MEM or op.mem.base != X86_REG_RIP:
                        continue
                    t = ins.address + ins.size + op.mem.disp
                    if not (slot <= t < slot + span):
                        continue
                    if ins.mnemonic == "nop":
                        continue
                    rec = found[t - slot]
                    if ins.mnemonic == "lea":
                        rec["lea"] += 1
                    else:
                        rec["widths"].add(op.size)
                        if op.access & CS_AC_WRITE:
                            rec["w"] += 1
                        else:
                            rec["r"] += 1
                    if len(rec["sites"]) < SITE_CAP:
                        rec["sites"].append((ins.address, name,
                                             "%s %s" % (ins.mnemonic, ins.op_str)))
                    loaders.add(entry)

        if not (direct or viacall):
            continue
        tainted = set()
        for ins in insns:
            ops = ins.operands
            # 1. does this instruction bring the object into a register?
            #
            # `mov` for a POINTER SLOT: the slot holds the object, so loading it yields the object.
            # `lea` for a STATIC object: the slot IS the object, so its ADDRESS is what is formed.
            # Getting this wrong is silent in one direction - a static scan that still matched `mov`
            # found only what the accessor path happened to reach, and reported the rest as absent.
            want = "lea" if static else "mov"
            loaded = None
            if ins.mnemonic == want and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP \
                    and (ins.address + ins.size + ops[1].mem.disp) == slot:
                loaded = ops[0].reg
                loaders.add(entry)
                if static:
                    # For a STATIC object the base address IS the thing formed, so the forming
                    # instruction is a site at offset 0. Without this, `arg_extent_scan --via-slot
                    # ... --at 0` has no sites to build a member set from, and an object whose whole
                    # usage is `lea rcx,[obj]; call helper` looks like an object nobody touches.
                    rec = found[0]
                    rec["lea"] += 1
                    if len(rec["sites"]) < SITE_CAP:
                        rec["sites"].append((ins.address, name,
                                             "%s %s" % (ins.mnemonic, ins.op_str)))

            # 1b. a call to an accessor returns the singleton in rax
            acc_ret = (ins.mnemonic in ("call", "jmp") and ins.operands
                       and ins.operands[0].type == X86_OP_IMM
                       and ins.operands[0].imm in accessors)
            if acc_ret:
                loaders.add(entry)

            # 2. record uses of an already-tainted base BEFORE this instruction's writes apply
            for op in ops:
                if op.type != X86_OP_MEM or op.mem.base == X86_REG_RIP:
                    continue
                if op.mem.base not in tainted:
                    continue
                if ins.mnemonic == "nop":
                    # `nop dword ptr [rax]` is alignment padding. Its operand is never read, and
                    # counting it invented a +0x00 field on the first run of this script.
                    continue
                if op.mem.index != X86_REG_INVALID:
                    continue          # indexed: an array base, not a field
                d = op.mem.disp
                if d < 0 or d > 0x400000:
                    continue
                rec = found[d]
                if ins.mnemonic == "lea":
                    # NOT an access: the address is taken. That is a different claim - an embedded
                    # sub-object handed to an initialiser - and merging it with reads would give a
                    # scalar field a width of 8 it never had.
                    rec["lea"] += 1
                else:
                    rec["widths"].add(op.size)
                    if op.access & CS_AC_WRITE:
                        rec["w"] += 1
                    else:
                        rec["r"] += 1
                if len(rec["sites"]) < SITE_CAP:
                    rec["sites"].append((ins.address, name,
                                         "%s %s" % (ins.mnemonic, ins.op_str)))

            # 2b. `add tainted, imm` is address arithmetic too, and the first version of this
            # script missed it. The per-frame gate reaches the sub-object at +0x5380 with
            # `add rcx, 0x5380` at 0028E2AB rather than a lea, so that whole sub-object was absent
            # from the census while its six siblings were present. Recorded like a lea - the address
            # is taken - and the taint still dies below, because the register no longer holds the
            # base.
            if ins.mnemonic == "add" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[0].reg in tainted and ops[1].type not in (X86_OP_MEM, X86_OP_REG):
                d = ops[1].imm
                if 0 < d <= 0x400000:
                    rec = found[d]
                    rec["lea"] += 1
                    if len(rec["sites"]) < SITE_CAP:
                        rec["sites"].append((ins.address, name,
                                             "%s %s" % (ins.mnemonic, ins.op_str)))

            # 3. propagate, then kill
            if ins.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG \
                    and ops[1].type == X86_OP_REG and ops[1].reg in tainted:
                tainted.add(ops[0].reg)
            elif loaded is not None:
                tainted.add(loaded)
            else:
                if ins.mnemonic == "call":
                    tainted &= NONVOLATILE   # volatile registers are gone; callee-saved survive
                    if acc_ret:
                        tainted.add(X86_REG_RAX)
                else:
                    for op in ops:
                        if op.type == X86_OP_REG and (op.access & CS_AC_WRITE) \
                                and op.reg in tainted:
                            tainted.discard(op.reg)
    return found, loaders



def compare_to_store(found, tname, store_dir):
    """Offsets the image uses that the type store does not describe.

    A byte-level census and a hand-built field map are independent, so where they AGREE each is
    evidence for the other, and where they disagree one of them is wrong. The interesting case is an
    offset the image demonstrably uses that lands inside a row whose own name says nothing was ever
    seen there - `BootSingleton01F7F598` had three.

    An offset the store declares and the scan does not find is NOT reported: the scan is a floor, and
    a field reached only through a pointer loaded from the object, or only by indexed access, is
    invisible to it by design.
    """
    import csv
    path = os.path.join(store_dir, "fields.tsv")
    rows = []
    with open(path, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="	"):
            if r["type"] == tname:
                try:
                    rows.append((int(r["offset"], 16), int(r["size"]), r["name"]))
                except (ValueError, TypeError):
                    pass
    if not rows:
        print("  the store declares no fields for %s" % tname)
        return 0
    rows.sort()
    inside, uncovered, unobserved = 0, [], []
    for off in sorted(found):
        hit = [r for r in rows if r[0] <= off < r[0] + r[1]]
        if not hit:
            uncovered.append(off)
        elif "unobserved" in hit[0][2] or "unattributed" in hit[0][2]:
            unobserved.append((off, hit[0]))
        else:
            inside += 1
    print()
    print("  against %s (%d row(s)):" % (tname, len(rows)))
    print("    inside a NAMED field      : %d  <- corroboration, both censuses agree" % inside)
    print("    inside an UNOBSERVED span : %d  <- the store says nothing is here" % len(unobserved))
    print("    covered by no row at all  : %d" % len(uncovered))
    for off, (b, sz, nm) in unobserved:
        print("      +0x%-6X in %s (+0x%X, %d B)" % (off, nm, b, sz))
    for off in uncovered:
        print("      +0x%-6X NOT COVERED" % off)
    return len(unobserved) + len(uncovered)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", default="0x0209BE80")
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--min-refs", type=int, default=1)
    ap.add_argument("--span", default="0",
                    help="with --static, the object's size: enables detection of fields "
                         "addressed individually by their own RIP-relative operand")
    ap.add_argument("--static", action="store_true",
                    help="the address IS the object (a .data/.bss instance reached by lea), not a pointer slot")
    ap.add_argument("--against", help="a type name in the store to diff the census against")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = Image(a.exe)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    fns = functions()

    if a.self_test:
        acc = accessors_for(img, md, fns, 0x0209BE80)
        found, loaders = scan(img, md, 0x0209BE80, fns, acc)
        ok = True
        for off, why in ((0x10F68, "the per-frame gate's subsystem enable flags"),
                         (0xAA44, "set to 1 by the boot path at 0028F911"),
                         (0x5380, "a sub-object reached by ADD, not lea - the case v1 missed")):
            hit = off in found
            ok = ok and hit
            print("  +0x%-6X %-8s %s" % (off, "found" if hit else "MISSING", why))
        print("  distinct offsets: %d, loader functions: %d" % (len(found), len(loaders)))

        # STATIC MODE NEEDS ITS OWN CONTROL, because its failure is silent in the worst way: a
        # static scan that still matches `mov` finds whatever the accessor path reaches and reports
        # everything else as absent. That is exactly what happened on 2026-09-18 - the line choosing
        # the mnemonic never landed, the scan ran clean, and a published SavePayload row said
        # "nothing reached through the accessor touches the payload" when 17 offsets do.
        # 02EB3870 (Mt19937State) is reached by `lea` from three functions and by no accessor, so it
        # is zero under the broken form and three under the correct one.
        sfound, sload = scan(img, md, 0x02EB3870, fns,
                             accessors_for(img, md, fns, 0x02EB3870, True), True)
        sok = len(sload) == 3 and 0 in sfound
        ok = ok and sok
        print("  static mode: %d loader(s) via lea, offset 0 %s   %s"
              % (len(sload), "recorded" if 0 in sfound else "MISSING",
                 "ok" if sok else "STATIC MODE IS MATCHING THE WRONG MNEMONIC"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    slot = int(a.slot, 16)
    acc = accessors_for(img, md, fns, slot, a.static)
    found, loaders = scan(img, md, slot, fns, acc, a.static, int(a.span, 0))
    if acc:
        print("accessor(s) returning this slot: %s"
              % ", ".join("%08X" % x for x in sorted(acc)))
    rows = [(off, r) for off, r in found.items()
            if (r["r"] + r["w"] + r["lea"]) >= a.min_refs]
    rows.sort()
    print("slot %08X: %d function(s) load it; %d distinct offset(s) used off the loaded pointer"
          % (slot, len(loaders), len(found)))
    print()
    print("%-10s %5s %5s %4s %-10s %s"
          % ("offset", "reads", "writes", "lea", "widths", "first site"))
    for off, r in rows:
        w = ",".join(str(x) for x in sorted(r["widths"]))
        site = r["sites"][0] if r["sites"] else (0, "", "")
        print("+0x%-8X %5d %5d %4d %-10s %08X %s"
              % (off, r["r"], r["w"], r["lea"], w or "-", site[0], site[2][:40]))
    if a.against:
        compare_to_store(found, a.against, os.path.join(KP.DB, "_types"))
    print()
    print("A LOWER BOUND, by construction: the taint does not enter callees, does not survive a")
    print("call, and ignores indexed accesses. Every offset here is used; offsets may be missing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
