#!/usr/bin/env python3
"""gen_ptr_census_ctor.py - seed a PTR-route census from the ALLOCATION, not from the slot.

THE GAP THIS CLOSES, and it affects every `PTR` row in the store.

`gen_ptr_census.py` and `gen_ptr_census_depth1.py` both begin the same way: find
`mov rX, [rip -> ADDR]`, and track rX. That seeding is what makes them work, and it is also why
neither has ever seen a lazy singleton's CONSTRUCTOR. The shipped idiom is

    cmp  qword ptr [ADDR], 0        the guard
    mov  ecx, <size>
    call <malloc thunk>             the object arrives in RAX
    mov  rcx, rax                   ... and the ctor runs on RAX
    call <ctor>
    mov  qword ptr [ADDR], rax      only NOW does the object reach the slot

Every field the constructor writes is written before the store, through a register that never
came from the slot. A slot-seeded census cannot see any of it, and the constructor is usually the
densest writer the type has.

MEASURED, not argued. `BootSingleton01F7F598` (`PTR 01F7F598`, 0xDD8):

    gen_ptr_census_depth1.py, slot-seeded :  3 accesses at  2 offsets
    this tool, allocation-seeded          : 66 accesses at 52 offsets

and all 52 lie inside the declared 0xDD8 extent, 0 outside - a coherence check on the extent as
well as a gain. The symptom to recognise elsewhere: `PostProcessParamContext` censuses as 37
accesses that are ALL READS and no writes. An object nothing writes is impossible; the writer is
the constructor and the instrument could not see it.

METHOD.
  1. Find the guard function: one that both TESTS `[ADDR]` against zero and STORES to `[ADDR]`.
  2. Inside it, take the direct call whose return feeds that store - the allocation - and seed
     RAX at offset 0 from it.
  3. Track forward exactly as pass 1 does, and follow direct calls that pass the object in an
     argument register, to --depth levels.

WHAT IT STILL CANNOT SEE, stated so a zero is not misread: indirect calls, a constructor reached
through a vtable, and any access at a computed offset with no literal displacement. It also
reports nothing for a type whose slot has no guard function, which is not the same as a type with
no constructor.

CONTROLS, both required or the output is discarded:
  * BootSingleton01F7F598 must find MORE offsets than the slot-seeded census (>= 40).
  * FrameMarkerSingleton01F82C80's constructor is known by hand - eleven inline field writes at
    001D6306-001D6341, no separate ctor call - so this tool must recover exactly those offsets:
    +0x00, +0x04, +0x08, +0x0C, +0x10, +0x14, +0x16, +0x1C, +0x24, +0x2C30, +0x2C34.

usage: gen_ptr_census_ctor.py --type <name> [--depth N]  |  --all
"""
import argparse
import collections
import reg_tracking as RT
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

import capstone  # noqa: E402
from capstone.x86 import (X86_OP_IMM, X86_OP_MEM, X86_OP_REG,  # noqa: E402
                          X86_REG_RIP, X86_REG_RAX)

X = capstone.x86
SAVED = {X.X86_REG_RBX, X.X86_REG_RBP, X.X86_REG_RDI, X.X86_REG_RSI,
         X.X86_REG_R12, X.X86_REG_R13, X.X86_REG_R14, X.X86_REG_R15}
ARG = [X.X86_REG_RCX, X.X86_REG_RDX, X.X86_REG_R8, X.X86_REG_R9]

# A 64-bit register and its 32/16/8-bit views are DIFFERENT capstone enums, and that matters here:
# the teardown idiom is `xor edi, edi` followed by `mov [slot], rdi`. Comparing the raw enums misses
# it and the destructor reads as a creator, so every register is normalised to its 64-bit parent.
_R64 = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
        "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]


def _build_parent():
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    want = {}
    for full in _R64:
        if full.startswith("r") and full[1:].isdigit():
            views = {full, full + "d", full + "w", full + "b"}
        else:
            stem = full[1:]
            views = {full, "e" + stem, stem, stem[0] + "l", stem + "l"}
        want[full] = views
    out = {}
    for reg in range(1, X.X86_REG_ENDING):
        try:
            nm = md.reg_name(reg)
        except capstone.CsError:
            continue
        if not nm:
            continue
        for full, views in want.items():
            if nm in views:
                out[reg] = getattr(X, "X86_REG_" + full.upper())
                break
    return out


PARENT = _build_parent()


def p64(reg):
    return PARENT.get(reg, reg)


CONTROL_GAIN = ("BootSingleton01F7F598", 40)
CONTROL_EXACT = ("FrameMarkerSingleton01F82C80",
                 {0x00, 0x04, 0x08, 0x0C, 0x10, 0x14, 0x16, 0x1C, 0x24, 0x2C30, 0x2C34})
# A CONTROL MUST EXERCISE THE RULE IT IS GUARDING. The two above were written before the tracker
# followed sub-object constructors, and neither touches that path: FrameMarker's ctor is fully
# inline and takes no sub-object base at all, so it would pass unchanged however badly the new
# rule behaved. ManagerSingleton0209BE80's ctor 00291750 hands four sub-object bases out with
# `lea rcx, [rdi + N]` - read by hand at 00291788, 002917C2, 00291794 and 002917AA - so requiring
# them is a control ON THE FOLLOWING RULE rather than on the seeding it was bolted onto.
CONTROL_SUBOBJECT = ("ManagerSingleton0209BE80", {0x5380, 0x57E0, 0x7EA0, 0x8FA0})


def load():
    d, base, secs = G.load_pe(G.EXE)
    sizes, names = {}, {}
    f = io.open(G.FUNCS, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.split("\t")
        try:
            sizes[int(p[0], 16)] = int(p[2])
            names[int(p[0], 16)] = p[1]
        except (ValueError, IndexError):
            pass
    return d, base, secs, sizes, names


def routes(db):
    rows = list(csv.reader(io.open(os.path.join(db, "_types", "types.tsv"),
                                   encoding="utf-8", newline=""), delimiter="\t"))
    h = rows[0]
    iR, iT, iS = h.index("route"), h.index("type"), h.index("size")
    out = []
    for r in rows[1:]:
        for alt in (r[iR] or "").split("|"):
            p = alt.split()
            if len(p) >= 2 and p[0] == "PTR":
                addr = int(p[1].split("+")[0], 16)
                try:
                    size = int(r[iS], 16)
                except ValueError:
                    size = None
                out.append((r[iT], addr, size))
    return out


class Image(object):
    def __init__(self):
        self.d, self.base, self.secs, self.sizes, self.names = load()
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True
        self._ins = {}

    def blob(self, va, n):
        r = va - self.base
        for nm, sva, vs, ra, rs in self.secs:
            if nm == ".text" and sva <= r < sva + max(vs, rs):
                o = r - sva
                if o < rs:
                    return self.d[ra + o: ra + o + n]
        return None

    def ins(self, va):
        if va in self._ins:
            return self._ins[va]
        n = self.sizes.get(va)
        out = []
        if n:
            b = self.blob(va, n)
            if b:
                out = list(self.md.disasm(b, va))
        self._ins[va] = out
        return out

    @staticmethod
    def rip(i, o):
        if o.type == X86_OP_MEM and o.value.mem.base == X86_REG_RIP:
            return i.address + i.size + o.value.mem.disp
        return None

    def guard_of(self, slot, size=None):
        """Every function that stores a register to the slot, and which one to seed from.

        A SLOT USUALLY HAS MORE THAN ONE STORER, and the first one found is the wrong one to
        return. `ManagerSingleton0209BE80` is stored by FUN_0028F2F0, its TEARDOWN, and by
        FUN_0028F8B0, which allocates `mov ecx, 0x10FD0` and publishes. Returning whichever came
        first out of a dict made a 69,584-byte type look allocation-less. So: collect them all,
        and prefer a storer with a SIZED allocation over one without, and a non-null store over a
        null one.

        Seeding RAX at the storer's entry is also wrong - RAX is the object only AFTER the
        allocation returns. The allocation is identified positively as the call preceded by
        `mov ecx, <imm>` where the immediate IS the type's declared size, which ties the seed to
        the type rather than to call order.
        """
        found = []
        for entry in self.sizes:
            ins = self.ins(entry)
            tests = False
            store_at = None
            store_reg = None
            for n, i in enumerate(ins):
                for o in i.operands:
                    if self.rip(i, o) != slot:
                        continue
                    if i.mnemonic in ("cmp", "test"):
                        tests = True
                    elif (i.mnemonic == "mov" and i.operands[0] is o
                          and len(i.operands) == 2 and i.operands[1].type == X86_OP_REG):
                        if store_at is None:
                            store_at, store_reg = n, i.operands[1].reg
            if store_at is None:
                continue

            # Null-ness is a REACHING-DEFINITIONS question. FUN_0018D3F0 creates
            # PostProcessParamContext and its allocation-failure arm does `xor edx,edx`
            # immediately before the shared store; a linear "was it just zeroed" test calls the
            # constructor a teardown and suppresses its 102 offsets. So: every definition of the
            # stored register must be a zeroing. FUN_0028F2F0, whose only definition of rdi is
            # `xor edi,edi`, still reads as a teardown under this rule.
            defs = []
            for n in range(store_at):
                i = ins[n]
                if not i.operands or i.operands[0].type != X86_OP_REG:
                    if i.mnemonic == "call":
                        defs.append(("call", None))
                    continue
                if p64(i.operands[0].reg) != p64(store_reg):
                    continue
                zero = (i.mnemonic == "xor" and len(i.operands) == 2
                        and i.operands[1].type == X86_OP_REG
                        and p64(i.operands[1].reg) == p64(i.operands[0].reg))
                defs.append(("def", zero))
            real = [z for kind, z in defs if kind == "def"]
            if p64(store_reg) not in SAVED:
                last_def = max((n for n, (k, _z) in enumerate(defs) if k == "def"), default=-1)
                if any(d[0] == "call" for d in defs[last_def + 1:]):
                    real.append(False)
            stores_null = bool(real) and all(real)

            alloc = start = None
            pending_size = None
            for n in range(store_at):
                i = ins[n]
                if (i.mnemonic == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG
                        and p64(i.operands[0].reg) == X.X86_REG_RCX
                        and i.operands[1].type == X86_OP_IMM):
                    pending_size = i.operands[1].imm
                    continue
                if i.mnemonic == "call":
                    if pending_size is not None and (size is None or pending_size == size):
                        if i.operands and i.operands[0].type == X86_OP_IMM:
                            alloc = i.operands[0].imm
                        start = i.address + i.size
                        break
                    pending_size = None
            found.append((entry, alloc, start, tests, stores_null))

        if not found:
            return None, None, None, False, False, []
        # prefer: a sized allocation, then a non-null store, then the lowest address
        best = sorted(found, key=lambda f: (f[2] is None, f[4], f[0]))[0]
        return best + (found,)

    def track(self, entry, seed, depth, maxdepth, seen, agg, start=None, origin=0):
        """`origin` is the offset within the object that `seed` points at on entry.

        A CONSTRUCTOR HANDS SUB-OBJECTS THEIR OWN BASE, NOT THE PARENT'S.
        ManagerSingleton0209BE80's ctor 00291750 does `lea rcx, [rdi + 0x5380]` and calls a
        sub-object constructor with it. Following only callees that receive offset ZERO - which
        is what this did - stops at the parent's own writes and returns 7 offsets for a
        69,584-byte type. Following `base + N` with `origin = N` records the sub-object's fields
        at their true offsets in the parent, which is exactly the EMBED relationship.
        """
        if (entry, seed, origin) in seen or depth > maxdepth:
            return
        seen.add((entry, seed, origin))
        held = {seed: origin}
        pend = []
        # REGISTERS PROVABLY HOLDING ZERO. A contiguous run of stores of a zeroed register is a
        # CLEAR, and its stride is the width the compiler chose to zero with, not a field
        # boundary. BootSingleton01F7F598 +0xD00/+0xD08 needed a hand-written exemption for
        # exactly that - 00186CD0's `xor r12d,r12d` then two `mov qword [rsi+0xd00/0xd08], r12`
        # over four floats each written by its own `movss`. The tracker can see it; the width
        # checker, which reads a TSV, cannot.
        zero = set()
        for i in self.ins(entry):
            if start is not None and i.address < start:
                continue
            for oi, o in enumerate(i.operands):
                if o.type == X86_OP_MEM and o.value.mem.base in held:
                    # THE KIND IS TAKEN HERE, where the operand is still in hand. It cannot be
                    # recovered from the printed text later: `cmp dword ptr [rbx+0x120], 0` reads
                    # and does not write, and only the operand's access flags say so.
                    kd = RT.op_kind(i, o, oi)
                    isz = (kd == "w" and len(i.operands) == 2
                           and i.operands[1].type == X86_OP_REG
                           and p64(i.operands[1].reg) in zero)
                    agg[held[o.value.mem.base] + o.value.mem.disp].append(
                        (o.size, i.address, entry, i.mnemonic, i.op_str, kd, isz))
            # A TAIL CALL IS A CALL. Following `call` only made three of ManagerSingleton0209BE80's
            # sub-object constructors invisible: 0028A080 and 0028CA30 are thirteen-byte
            # forwarders that end in `jmp`, and the census reached 0 offsets for each until they
            # were read by hand. An intra-function `jmp` is control flow; a `jmp` to another
            # function ENTRY is a call whose return is the caller's, so it is followed with the
            # same argument registers. Added 2026-09-19 (OPUS).
            #
            # ITS MEASURED YIELD ON THE CURRENT POPULATION IS ZERO, and that is stated rather
            # than left for someone to assume otherwise. Verified to FIRE - the walk now reaches
            # 00861EC0 through both forwarders, and did not before - but the offset counts across
            # all thirteen PTR types are unchanged to the digit. The reason is that both tail
            # targets are MEMSET, which writes through an index register, and a displacement
            # tracker records `[base + disp]` and not `[base + index]`. The change is kept
            # because it is correct, not because it paid.
            tail = (i.mnemonic == "jmp" and i.operands
                    and i.operands[0].type == X86_OP_IMM
                    and not (entry <= i.operands[0].imm
                             < entry + self.sizes.get(entry, 0)))
            if ((i.mnemonic == "call" or tail) and i.operands
                    and i.operands[0].type == X86_OP_IMM):
                for ar in ARG:
                    if ar in held:
                        pend.append((i.operands[0].imm, ar, held[ar]))
            if (i.mnemonic == "mov" and len(i.operands) == 2
                    and i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG
                    and i.operands[1].reg in held):
                held[i.operands[0].reg] = held[i.operands[1].reg]
                continue
            if i.mnemonic == "lea" and len(i.operands) == 2 and i.operands[1].type == X86_OP_MEM:
                m = i.operands[1].value.mem
                if m.base in held and not m.index:
                    held[i.operands[0].reg] = held[m.base] + m.disp
                    continue
            try:
                _r, w = i.regs_access()
            except capstone.CsError:
                w = []
            for r in w:
                held.pop(r, None)
            if i.mnemonic == "call":
                for r in list(held):
                    if r not in SAVED:
                        held.pop(r, None)
            # Maintained last, so it describes the state the NEXT instruction sees. Only ever
            # used to explain a store away, never to admit one, so erring cautious costs a tag.
            if (i.mnemonic in ("xor", "sub") and len(i.operands) == 2
                    and i.operands[0].type == X86_OP_REG
                    and i.operands[1].type == X86_OP_REG
                    and i.operands[0].reg == i.operands[1].reg):
                # NORMALISED TO THE 64-BIT PARENT, and this is not a nicety: the shipped
                # idiom is `xor r12d, r12d`, a 32-bit xor that zeroes all 64 bits of r12, and
                # the store two instructions later names `r12`. Without normalising, the known
                # case - BootSingleton01F7F598 +0xD00/+0xD08 - came back UNMARKED while twelve
                # other rows were marked, which is how the omission was caught.
                # `p64` is this file's own normaliser, built for the sibling idiom
                # `xor edi, edi` then `mov [slot], rdi` and documented above.
                zero.add(p64(i.operands[0].reg))
            else:
                for r in w:
                    zero.discard(p64(r))
                if i.mnemonic == "call":
                    zero = {r for r in zero if r in SAVED}
        for t, r, off in pend:
            self.track(t, r, depth + 1, maxdepth, seen, agg, None, off)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--db", default=G.DB)
    ap.add_argument("--out", default=None,
                    help="write the census as a standard 8-column *-accesses.tsv (needs --type)")
    a = ap.parse_args()

    img = Image()
    want = [r for r in routes(a.db) if a.all or r[0] == a.type]
    if not want:
        print("no PTR route named %r" % a.type)
        return 2

    verdict = {}
    for name, slot, size in want:
        guard, alloc, start, tested, isnull, allst = img.guard_of(slot, size)
        agg = collections.defaultdict(list)
        if guard is not None:
            img.track(guard, X86_REG_RAX, 0, a.depth, set(), agg, start)
        inside = sorted(k for k in agg if size is None or 0 <= k < size)
        outside = [k for k in agg if not (size is None or 0 <= k < size)]
        total = sum(len(agg[k]) for k in inside)
        verdict[name] = set(inside)
        print("%s: PTR %08X size %s"
              % (name, slot, ("0x%X" % size) if size else "UNRESOLVED"))
        if guard is None:
            print("    NO CREATOR FOUND - no function stores a register to this slot, so there")
            print("    is no allocation to seed from. NOT the same as 'no constructor': the")
            print("    object may be created by a caller and handed in, or stored indirectly.")
            print()
            continue
        print("    %s %08X  allocation %s  object live from %s  null-guard %s  depth %d"
              % ("TEARDOWN (stores NULL)" if isnull else "creator", guard,
                 ("%08X" % alloc) if alloc else "(not sized-call)",
                 ("%08X" % start) if start else "(not found)",
                 "yes" if tested else "not on the slot", a.depth))
        if isnull:
            print("      the stored register is provably zeroed before the store, so this")
            print("      function DESTROYS the singleton. Nothing is seeded from it.")
        if len(allst) > 1:
            print("      %d functions store to this slot: %s"
                  % (len(allst), ", ".join("%08X%s%s" % (e, "(sized)" if st else "",
                                                         "(null)" if z else "")
                                           for e, _a, st, _t, z in allst)))
        print("    %d access(es) at %d offset(s) inside the extent, %d outside"
              % (total, len(inside), len(outside)))
        if a.type and not a.all:
            for k in inside:
                sz, addr, fn, mn, ops, _kd, _z = agg[k][0]
                print("      +0x%-5X w%-2d x%-2d %08X in %08X  %s %s"
                      % (k, sz, len(agg[k]), addr, fn, mn, ops[:52]))
        print()

        if a.out and a.type and not a.all:
            # THE ARTIFACT. Until now this tool printed and wrote nothing, and that had a
            # measurable cost: BootSingleton01F7F598's eight rows cite THIS tool - 66 accesses
            # at 52 offsets, against the 3 at 2 offsets a slot-seeded scan reaches - while the
            # census registered for it in check_census_widths.py was the slot-seeded file, 5
            # accesses at 3 offsets. The map named a file, the file existed, so every artifact
            # check passed; the gate was simply comparing the type against the WEAKER of two
            # censuses because the stronger one could not be written down.
            rows, seen = [], set()
            for k in inside:
                for sz, addr, fn, mn, ops, kd, isz in agg[k]:
                    if (addr, k) in seen:
                        continue
                    seen.add((addr, k))
                    rows.append((fn, addr, k, kd, mn + " " + ops, isz, sz))
            # A SINGLE ZERO STORE IS NOT A CLEAR; A CONTIGUOUS RUN AT ONE WIDTH IS. Initialising
            # one genuine field to zero looks identical to the first store of a clear, so only
            # the run is marked - the shape that cannot be a field list, because its stride is
            # the compiler's chosen store width. Threshold two, which is what
            # BootSingleton01F7F598's +0xD00/+0xD08 has.
            at = collections.defaultdict(set)
            for fn, addr, k, kd, txt, isz, sz in rows:
                if isz and sz:
                    at[(fn, sz)].add(k)
            clear = {(fn, k) for (fn, sz), offs in at.items() for k in offs
                     if (k - sz) in offs or (k + sz) in offs}
            rows.sort(key=lambda x: (x[2], x[1]))
            with io.open(a.out, "w", encoding="utf-8", newline="") as fh:
                fh.write("function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n")
                for fn, addr, k, kd, txt, isz, sz in rows:
                    fh.write("%08X\t%s\t%08X\t0x%X\t%s\t%s\tctor-seeded %08X%s\t\n"
                             % (fn, img.names.get(fn, ""), addr, k, kd, txt, slot,
                                " zeroclear" if (fn, k) in clear else ""))
            ncl = sum(1 for r in rows if (r[0], r[2]) in clear)
            print("    of those, %d marked `zeroclear` (a contiguous zeroed-register run)" % ncl)
            print("    wrote %s  (%d access(es) at %d offset(s), %d function(s))"
                  % (a.out, len(rows), len({r[2] for r in rows}), len({r[0] for r in rows})))

    if a.all:
        cname, cmin = CONTROL_GAIN
        got = len(verdict.get(cname, ()))
        ok1 = got >= cmin
        print("CONTROL  %-34s expect >= %d offsets   got %-4d %s"
              % (cname, cmin, got, "PASS" if ok1 else "FAIL"))
        ename, eset = CONTROL_EXACT
        have = verdict.get(ename, set())
        ok2 = eset <= have
        print("CONTROL  %-34s expect 11 ctor offsets  got %-4d %s"
              % (ename, len(have & eset), "PASS" if ok2 else "FAIL"))
        sname, sset = CONTROL_SUBOBJECT
        shave = verdict.get(sname, set())
        ok3 = sset <= shave
        print("CONTROL  %-34s expect 4 sub-object bases got %-4d %s"
              % (sname, len(shave & sset), "PASS" if ok3 else "FAIL"))
        if not (ok1 and ok2 and ok3):
            print()
            print("A CONTROL FAILED -> DISCARD THE TABLE. Seeding from the allocation has not")
            print("been shown to recover constructors whose fields are already known by hand.")
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
