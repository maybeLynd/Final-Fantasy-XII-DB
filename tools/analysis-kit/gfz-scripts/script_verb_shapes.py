#!/usr/bin/env python3
"""script_verb_shapes.py - classify the 1,224 script verb handlers by SHAPE.

Why shape and not prose
-----------------------
`script-verbs-undocumented` reports **1,158 of 1,224** script verbs whose native handler no document
cites. Reading 1,158 functions one at a time is not a plan. The charter's completion disposition
**B** is: *a proven member of an understood family, with the shape, the enumeration method and a
reproducible count stated.* This is the enumeration method.

The population is mostly tiny - 849 of 1,224 handlers are under 64 bytes - so most of it is
wrappers, and a wrapper's whole behaviour IS its shape.

The cut is CONTROL FLOW, because that is what decides whether a handler can be reimplemented by
reading it once:

    BRANCHING    has a conditional branch of its own              -> disposition D
    ---- everything below has NO conditional branch anywhere ---- -> disposition B
    CONST        no call, no jump, no memory operand
    TAILJUMP     no call; one unconditional `jmp` to a fixed target
    CALL1        exactly one direct call
    LINEAR       several calls, still no branching
    OTHER        did not decode - **reported, never folded into a family**

**A first version cut on call/jump counts instead and dropped 53 % of the population into OTHER**,
including `setvelr` and `sin` - plainly straight-line wrappers with two calls each. A taxonomy that
cannot classify half its population is measuring the taxonomy, not the population.

The extent a shape is read over
-------------------------------
A shape is only as good as the bytes it is read over. **29 listed function extents in
`functions.tsv` run past the real end of their body and into the next function** - adjudicated
per row in `_index/FUNCTION-EXTENT-ERRATA.tsv` and independently reviewed (see `_inbox/SWE2.md`).
Decoding a handler for its listed size therefore walks into a neighbour, and the neighbour's
instructions are attributed to the handler.

**Ten of the 1,166 distinct verb handlers carry a corrected extent, and four change family** once
the body ends where the body ends. All four are inside the straight-line group, so the B/D
disposition split does not move - but the detail was wrong in a way that mattered: three rows named
a **call target that belongs to the next function** (`00267E10`/`00267DB0` for `enable`,
`lookat_maxvelr_limit_unlock` and `hidecomplete`), and `moveblurcaptureonce` fell through to the
`LINEAR` catch-all with *"no call, no branching"* when it is a plain `TAILJUMP`.

The cut is taken from the **adjudicated errata**, not from the strict heuristic that found it. The
heuristic - *first `int3` run followed by a listed entry or a 16-byte-aligned instruction* - is a
**shape detector, not a census**: it sees 23 of the 29 overruns, and it would also cut 13 bodies
whose `int3` run is an **interior alignment pad** that a branch inside the same function jumps over.
A per-row verdict is the only thing that separates those two populations, so this reads the verdicts.
"""
import argparse
import collections
import io
import os
import struct
import sys

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_IMM, X86_OP_MEM, X86_REG_RIP
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
TSV = os.path.join(ROOT, "Database", "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch",
                   "scriptvm-dispatch.tsv")
ERRATA = os.path.join(ROOT, "Database", "FFXII TZA", "_index", "FUNCTION-EXTENT-ERRATA.tsv")


def load_corrected_ends(path):
    """entry -> corrected_end, for the adjudicated `merge` rows only.

    A `legitimate body` row deliberately has no corrected_end: its `int3` run is an interior
    alignment pad that a branch inside the same function jumps over, so cutting there would
    truncate a real body. Reading only the merge verdicts keeps those bodies whole.
    """
    out = {}
    if not os.path.exists(path):
        return out
    with io.open(path, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        ie, ice, iv = head.index("entry"), head.index("corrected_end"), head.index("verdict")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) > iv and p[iv] == "merge" and p[ice].strip():
                out[p[ie].strip().upper()] = int(p[ice], 16)
    return out


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


def classify(md, ins):
    """Return (family, detail). Every rule is checked against the WHOLE body.

    The families are cut on **control flow**, because that is the property that decides whether a
    handler can be reimplemented by reading it once. A first version cut them on call/jump counts
    instead - CONST, TAILJUMP, CALL1 - and dropped **53 % of the population into OTHER**, including
    `setvelr` and `sin`, which are plainly straight-line wrappers with two calls each. A taxonomy
    that cannot classify half its population is measuring the taxonomy, not the population.
    """
    if not ins:
        return "OTHER", "no instructions decoded"
    calls = [i for i in ins if i.mnemonic == "call"]
    jmps = [i for i in ins if i.mnemonic == "jmp"]
    cond = [i for i in ins if i.mnemonic[0] == "j" and i.mnemonic != "jmp"]
    mem = [i for i in ins if any(o.type == X86_OP_MEM for o in i.operands)]

    if cond:
        return "BRANCHING", "%d conditional branch(es), %d call(s)" % (len(cond), len(calls))

    # No conditional branch anywhere: the handler is a straight line. Sub-shapes, most specific
    # first, so each row says as much as the body supports.
    if not calls and not jmps and not mem:
        return "CONST", "no call, no jump, no memory - a constant or a bare ret"
    if not calls and len(jmps) == 1 and jmps[0].operands[0].type == X86_OP_IMM:
        return "TAILJUMP", "-> %08X" % jmps[0].operands[0].value.imm
    if len(calls) == 1 and calls[0].operands[0].type == X86_OP_IMM:
        return "CALL1", "-> %08X%s" % (calls[0].operands[0].value.imm,
                                       ", then tail-jump" if jmps else "")
    if calls:
        direct = [c for c in calls if c.operands[0].type == X86_OP_IMM]
        return "LINEAR", "%d call(s) (%d direct), no branching" % (len(calls), len(direct))
    return "LINEAR", "no call, no branching, %d memory operand(s)" % len(mem)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--tsv", default=TSV)
    ap.add_argument("--errata", default=ERRATA)
    ap.add_argument("--no-errata", action="store_true",
                    help="read every handler for its listed extent, as this script did before the "
                         "overrun census; for reproducing the old rows, not for publishing")
    ap.add_argument("--out", default=None)
    ap.add_argument("--show", type=int, default=0)
    a = ap.parse_args()

    rd = load_pe(a.exe)
    corrected = {} if a.no_errata else load_corrected_ends(a.errata)
    sizes = {}
    f = io.open(a.funcs, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) > 2:
            try:
                sizes[p[0]] = int(p[2])
            except ValueError:
                pass

    rows = []
    for line in io.open(a.tsv, encoding="utf-8", errors="replace").read().splitlines():
        if not line.strip() or line.startswith("#") or line.startswith("call_id"):
            continue
        rows.append(line.split("\t"))

    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    fam = collections.Counter()
    fam_verbs = collections.Counter()
    seen = {}
    out = []
    cut = 0
    for r in rows:
        h = r[3]
        if h not in seen:
            size = sizes.get(h, 0)
            end = corrected.get(h.strip().upper())
            if end is not None and int(h, 16) < end < int(h, 16) + size:
                size = end - int(h, 16)   # the body ends where the errata says it ends
                cut += 1
            code = rd(int(h, 16), size) if size else None
            ins = list(md.disasm(code, int(h, 16))) if code else []
            seen[h] = classify(md, ins) + (size,)
        family, detail, size = seen[h]
        fam_verbs[family] += 1
        out.append((r[0], r[1], r[2], h, size, family, detail))
    for h, (family, _, _) in seen.items():
        fam[family] += 1

    nverbs, nh = len(rows), len(seen)
    print("script verbs                 : %d" % nverbs)
    print("distinct handlers            : %d  (%d verbs share a handler with another verb)"
          % (nh, nverbs - nh))
    print("extents cut at the real body : %d  (%s)"
          % (cut, "adjudicated merge rows in FUNCTION-EXTENT-ERRATA.tsv" if corrected
             else "--no-errata: listed extents, neighbours included"))
    print()
    print("  family      handlers   share   verbs    share")
    for k in ("CONST", "TAILJUMP", "CALL1", "LINEAR", "BRANCHING", "OTHER"):
        print("  %-10s %7d  %5.1f %% %7d  %5.1f %%"
              % (k, fam[k], 100.0 * fam[k] / nh, fam_verbs[k], 100.0 * fam_verbs[k] / nverbs))
    explained = sum(fam[k] for k in ("CONST", "TAILJUMP", "CALL1", "LINEAR"))
    print()
    print("  STRAIGHT-LINE (no conditional branch anywhere) : %d of %d handlers (%.1f %%)"
          % (explained, nh, 100.0 * explained / nh))
    print("     -> disposition B: the whole behaviour is the call chain, readable in one pass")
    print("  BRANCHING (has control flow of its own)        : %d of %d handlers (%.1f %%)"
          % (fam["BRANCHING"], nh, 100.0 * fam["BRANCHING"] / nh))
    print("     -> disposition D: each needs reading; this is the real remaining work")
    print("  UNCLASSIFIED                                   : %d" % fam["OTHER"])

    if a.show:
        print("\n  samples")
        shown = collections.Counter()
        for cid, verb, args, h, size, family, detail in out:
            if shown[family] < a.show:
                shown[family] += 1
                print("    %-9s %-28s %s  %4d B  %s" % (family, verb[:28], h, size, detail))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("call_id\tverb\targs\thandler\tbody_bytes\tfamily\tdetail\n")
            for row in out:
                f.write("%s\t%s\t%s\t%s\t%d\t%s\t%s\n" % row)
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
