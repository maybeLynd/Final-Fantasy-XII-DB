#!/usr/bin/env python3
"""actor_field_scan.py - find actor-record fields the constructor never touches.

The problem
-----------
`ActorStorageRecord`'s layout in `_types/` came from `ActorStorage_InitializeRecord`'s own stores.
That recovers everything the constructor initialises - and nothing else. The record is up to 1,760
bytes and the store declares 0x11C of it, leaving a **1,476-byte undeclared tail**: fields written
later, by the systems that actually use an actor.

The instrument
--------------
The record carries a proven discriminator at `+0x03`:

    packedKindAndSequence = (kind << 5) | (sequence & 0x1F)

so code that decodes an actor's kind looks like

    movzx  eax, byte ptr [rcx + 3]
    shr    eax, 5                       ; or:  and eax, 0x1F

**A function containing that sequence is handling an actor record**, and the register the byte was
read through held an actor pointer at that instant. Every `[thatreg + disp]` access in the same
function is then a candidate field.

What this is NOT
----------------
The taint is a **linear forward scan** with invalidation on write to the register. It does not
follow control flow, so a register reloaded from something else on a path this scan did not model
would produce a false offset. Results are therefore **candidates**, and the tool measures its own
reliability instead of asserting it:

**the control is the constructor's own header.** The 31 offsets already proven to be fields must
come back out of this scan. The recovery rate against that known set is printed on every run, and
it is the number that says how much the new offsets are worth.
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM
import kit_paths as KP  # noqa: E402
import uc1_band  # noqa: E402

ROOT = KP.ROOT
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
STORE = os.path.join(ROOT, "Database", "FFXII TZA", "_types")

MAX_OFF = 0x6E0          # the largest per-kind record, from the table at 01E0C328
VOLATILE = frozenset(("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"))


def load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40

    def rd(va, n):
        r = va - base
        for sva, vs, ra, rs in secs:
            if sva <= r < sva + max(vs, rs):
                o = r - sva
                return None if o >= rs else d[ra + o: ra + o + n]
        return None
    return rd


def load_functions(path):
    out = {}
    f = io.open(path, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                out[int(p[0], 16)] = (int(p[2]), p[8] if len(p) > 8 else "")
            except ValueError:
                pass
    # UC-1 band on the shared census only (2026-09-28 series break).
    if os.path.realpath(path) == os.path.realpath(FUNCS):
        _b = uc1_band.load()
        for e in _b["removed"]:
            out.pop(e, None)
        for e, en in _b["extend"].items():
            if e in out:
                out[e] = (en - e, out[e][1])
        for st, sz in _b["frontier"].items():
            out[st] = (sz, "")
    return out


def base64_name(md, i, reg):
    """The 64-bit name of a register, so `eax`/`ax`/`al` all invalidate `rax`."""
    try:
        return md.reg_name(i.reg_name(reg) and reg)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--store", default=STORE)
    ap.add_argument("--min-funcs", type=int, default=2,
                    help="report an offset only when this many functions touch it")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    rd = load_pe(a.exe)
    funcs = load_functions(a.funcs)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    # 64-bit canonical names, so a write to eax kills rax
    def canon(n):
        n = n.lower()
        m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
             "ebp": "rbp", "esp": "rsp", "ax": "rax", "bx": "rbx", "cx": "rcx", "dx": "rdx",
             "si": "rsi", "di": "rdi", "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx",
             "ah": "rax", "bh": "rbx", "ch": "rcx", "dh": "rdx", "sil": "rsi", "dil": "rdi",
             "bpl": "rbp", "spl": "rsp"}
        if n in m:
            return m[n]
        if n.startswith("r") and n.endswith(("d", "w", "b")) and n[1:-1].isdigit():
            return "r" + n[1:-1]
        return n

    hits = []            # (entry, reg) - a function that decoded an actor kind
    for entry in sorted(funcs):
        size = funcs[entry][0]
        if size <= 0 or size > 0x20000:
            continue
        code = rd(entry, size)
        if code is None:
            continue
        ins = list(md.disasm(code, entry))
        for n, i in enumerate(ins):
            if i.mnemonic not in ("movzx", "mov"):
                continue
            if len(i.operands) != 2:
                continue
            dst, src = i.operands
            if dst.type != X86_OP_REG or src.type != X86_OP_MEM:
                continue
            mem = src.value.mem
            if mem.disp != 3 or mem.index != 0 or mem.base == 0:
                continue
            if "byte" not in i.op_str:
                continue
            dreg = canon(i.reg_name(dst.value.reg))
            # the discriminator decode must follow within a few instructions
            for j in range(n + 1, min(n + 6, len(ins))):
                k = ins[j]
                if k.mnemonic in ("shr", "and") and len(k.operands) == 2 and \
                        k.operands[0].type == X86_OP_REG and \
                        canon(k.reg_name(k.operands[0].value.reg)) == dreg and \
                        k.operands[1].type == X86_OP_IMM and \
                        ((k.mnemonic == "shr" and k.operands[1].value.imm == 5) or
                         (k.mnemonic == "and" and k.operands[1].value.imm in (0x1F, 0xE0))):
                    hits.append((entry, canon(md.reg_name(mem.base)), n, ins))
                    break

    # --- enumerate accesses on the pointer register ------------------------------------------
    # Three instruments have now been measured against the same control, the constructor's own
    # field set:
    #
    #   forward taint, no copy propagation (2026-09-08, abandoned)   4 of 41 known offsets
    #   crude "every [reg+disp] anywhere in the function"           70 offsets, 47/47 control
    #   forward taint WITH copy propagation (this one)              50 offsets, 41/41 of the
    #                                                               constructor's own offsets
    #
    # The crude version was kept because its recall looked perfect. Its over-count is not noise:
    # `0026AEA3 mov rcx,[rcx+0xB8]` loads the MOVEMENT CONTEXT into the very register that held
    # the actor, so every later `[rcx+disp]` in that function is a context field filed as an
    # actor field. That is a systematic error with a named cause, not a random one.
    #
    # What runs now is a straight-line forward taint IN ADDRESS ORDER:
    #   * seed the base register at EVERY kind decode in the function, not only the first;
    #   * `mov rA, rB` propagates - which is exactly what the 2026-09-08 taint lacked, and why
    #     that one scored 4 of 41;
    #   * any other write to a register kills it; a call kills the volatiles.
    # It does not follow control flow, so it still UNDER-counts across branches.
    #
    # The five offsets it does not re-find - 0x044, 0x05C, 0x068, 0x0E8, 0x107 - are exactly the
    # ones the CRUDE scan itself promoted into `_types/`. The control's denominator therefore
    # contains its predecessor's output; against the constructor's own 41 offsets this scan is
    # 41 of 41. Those five are recorded as unconfirmed rather than deleted.
    off_funcs = collections.defaultdict(set)
    off_kind = collections.defaultdict(collections.Counter)
    off_size = collections.defaultdict(collections.Counter)
    seeded = collections.defaultdict(set)
    per_fn = {}
    for entry, reg, at, ins in hits:
        seeded[entry].add((at, reg))
        per_fn[entry] = ins
    for entry, ins in per_fn.items():
        seedmap = collections.defaultdict(set)
        for at, reg in seeded[entry]:
            seedmap[at].add(reg)
        tainted = set()
        for n, i in enumerate(ins):
            tainted |= seedmap.get(n, set())
            for op in i.operands:
                if op.type == X86_OP_MEM and op.value.mem.base and op.value.mem.index == 0                         and canon(md.reg_name(op.value.mem.base)) in tainted:
                    d = op.value.mem.disp
                    if 0 <= d <= MAX_OFF:
                        off_funcs[d].add(entry)
                        off_size[d][op.size] += 1
                        is_w = (i.operands and op is i.operands[0] and i.mnemonic in
                                ("mov", "add", "or", "and", "xor", "sub", "inc", "dec"))
                        off_kind[d]["w" if is_w else "r"] += 1
            if i.mnemonic == "call":
                tainted -= VOLATILE
                continue
            wnames = set(canon(md.reg_name(r)) for r in i.regs_access()[1])
            if i.mnemonic == "mov" and len(i.operands) == 2 and                i.operands[0].type == X86_OP_REG and i.operands[1].type == X86_OP_REG:
                dst = canon(i.reg_name(i.operands[0].value.reg))
                src = canon(i.reg_name(i.operands[1].value.reg))
                if src in tainted:
                    tainted.add(dst)
                else:
                    tainted.discard(dst)
                wnames.discard(dst)
            tainted -= wnames

    # --- the control: does the scan re-find the constructor's known fields? ------------------
    # The control must be the CONSTRUCTOR-proven offsets and nothing else. An earlier version
    # scored against every ActorStorageRecord row minus a hard-coded list of six, and that broke
    # the moment rows arrived from anywhere else: on 2026-09-10 fourteen offsets recovered from
    # the resource/wait-slot readers and from the region map joined the store, and the control
    # silently fell from 41/41 to 45/59 while the scan itself had not changed at all.
    #
    # So the set is DERIVED from provenance: a row belongs to the control exactly when its
    # evidence names `ActorStorage_InitializeRecord`. Every other row is reported separately and
    # is explicitly not a control - scoring against rows this scan, or a reader of some other
    # function, produced would let the tool grade itself.
    known, other = set(), {}
    fp = os.path.join(a.store, "fields.tsv")
    if os.path.exists(fp):
        for line in io.open(fp, encoding="utf-8").read().splitlines()[1:]:
            p = line.split("\t")
            if p and p[0] == "ActorStorageRecord" and len(p) > 8:
                try:
                    off = int(p[1], 16)
                except ValueError:
                    continue
                if "ActorStorage_InitializeRecord" in p[8]:
                    known.add(off)
                else:
                    other[off] = p[3]
    found_known = sorted(o for o in known if o in off_funcs)
    # The store's ActorStorageRecord rows are NOT one population. Most came from the
    # constructor's own stores; a handful were promoted by an EARLIER RUN OF THIS SCAN. Scoring
    # against the union would let the tool grade itself, so the two are printed apart.
    ctor = known

    print("functions that decode (kind << 5 | seq) at +0x03 : %d" % len(set(h[0] for h in hits)))
    print("decode sites (a function may have several)        : %d" % len(hits))
    print("distinct offsets touched through a tainted actor pointer : %d" % len(off_funcs))
    print()
    print("CONTROL - the constructor's own %d field offsets" % len(ctor))
    if ctor:
        hit = len(ctor & set(off_funcs))
        print("  re-found by this scan : %d of %d  (%.1f %%)"
              % (hit, len(ctor), 100.0 * hit / len(ctor)))
        miss = sorted(ctor - set(off_funcs))
        if miss:
            print("  NOT re-found          : %s" % ", ".join("0x%03X" % m for m in miss))
        print("  A low rate here means the taint is weak and every NEW offset below is worth")
        print("  proportionally less. The rate is the tool's own error bar.")
    if other:
        hit = sorted(o for o in other if o in off_funcs)
        miss = sorted(o for o in other if o not in off_funcs)
        print()
        print("SEPARATE - %d store row(s) whose evidence is NOT the constructor." % len(other))
        print("  Not a control: some were promoted by an earlier run of this very scan, and the")
        print("  rest come from readers this instrument's anchor cannot reach by construction.")
        print("  re-confirmed : %s" % (", ".join("0x%03X" % m for m in hit) or "none"))
        print("  unconfirmed  : %s" % (", ".join("0x%03X" % m for m in miss) or "none"))
        print("  Unconfirmed does not mean refuted - it means this instrument does not reach it.")
    print()

    # "New" means not declared ANYWHERE in the store for this type - both populations, not just
    # the control set, or every row whose evidence is a reader would be re-reported as a discovery.
    declared = known | set(other)
    new = [(o, off_funcs[o]) for o in sorted(off_funcs)
           if o not in declared and len(off_funcs[o]) >= a.min_funcs]
    print("NEW candidate offsets touched by >= %d function(s) : %d" % (a.min_funcs, len(new)))
    print()
    print("  offset   funcs  reads  writes  operand sizes")
    for o, fs in new[:60]:
        print("  0x%03X %7d %6d %7d  %s" % (o, len(fs), off_kind[o]["r"], off_kind[o]["w"],
                                            dict(off_size[o])))
    if len(new) > 60:
        print("  ... %d more" % (len(new) - 60))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("offset\tfunctions\treads\twrites\tsizes\tknown\n")
            for o in sorted(off_funcs):
                f.write("0x%03X\t%d\t%d\t%d\t%s\t%s\n"
                        % (o, len(off_funcs[o]), off_kind[o]["r"], off_kind[o]["w"],
                           ",".join("%d" % k for k in sorted(off_size[o])),
                           "yes" if o in known else "no"))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
