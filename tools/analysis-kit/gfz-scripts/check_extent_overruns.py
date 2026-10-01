"""check_extent_overruns.py -- functions.tsv body-extent overrun audit.

OPUS-FUNCLIST-EXTENT-OVERRUN / SWE2.

`functions.tsv` is a Ghidra export (`DumpFullCoverageGraph.java`):
`body_bytes = f.getBody().getNumAddresses()`.  Some Ghidra function bodies
overlap the start of the next listed function, so `body_bytes` is not a safe
byte-range bound for `[entry, entry+body_bytes)` on those rows.

This instrument enumerates the defect population two ways:

  strict  - the rule OPUS published in
            `01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md`:
            decode the extent; take the FIRST `int3` run that is followed by a
            non-`int3` instruction still inside the extent; flag the function
            when that successor is 16-byte aligned or is itself a listed
            entry.  Reproduces 36 = 23 listed-boundary + 13 unlisted-boundary
            and the 4,468 "bytes counted twice" figure
            (= sum of `extent_end - first_int3_address` over the 36;
            equivalently 4,308 post-boundary bytes + 160 padding bytes).

  overlap - the plain defect census: `entry + body_bytes > next listed entry`.
            Returns 29.  The strict rule sees 23 of them; 6 merges have no
            qualifying `int3` boundary inside the decode window (the padding
            ends exactly AT the next entry leaving an undecodable tail, the
            body ends with a jump exactly at the next entry with no padding
            at all, or an embedded switch table desyncs the linear decode
            before the pad is reached).

Adjudication, applied per row:

  merge   - the extent swallows bytes that begin the next listed function.
            Every one of the 29 overlap cases ends its own control flow at or
            before the listed boundary (unconditional `jmp`/`ret`, or `int3`
            padding to the boundary), and no branch issued before the padding
            reaches into the swallowed range.  Corrected extent =
            last own instruction end (pad excluded, matching the file's
            convention where ordinary functions exclude their `int3` tail).

  legit   - the 13 strict-rule rows whose boundary is NOT a listed entry.
            In every case an instruction issued before the padding branches
            exactly to the boundary: the pad is an interior MSVC alignment
            pad and the post-pad code is the same function.  Extent correct;
            no correction.

Usage:  python check_extent_overruns.py [--tsv out.tsv]

Rows written: entry, name, listed size, end, pad, boundary, boundary-listed,
prev mnemonic, pre-pad branch-exact-hit, overlap into next entry,
corrected end (merges only), verdict, detector (strict|overlap-only).
"""
import argparse
import csv
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import uc1_band
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))  # Database/Tools
EXE = os.path.join(ROOT, "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "work", "graph", "functions.tsv")


def load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", d, off + 8)
        secs.append((va + base, vs, ra, rs))
        off += 40

    def rd(va, n):
        for sva, vs, ra, rs in secs:
            if sva <= va < sva + max(vs, rs):
                o = va - sva
                return None if o >= rs else d[ra + o: ra + o + n]
        return None
    return rd


def load_functions(path):
    rows = []
    with io.open(path, encoding="utf-8", errors="replace") as f:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) > 2:
                try:
                    rows.append((int(p[0], 16), p[1], int(p[2])))
                except ValueError:
                    pass
    # UC-1 band (2026-09-28) when the input is the shared census.
    if os.path.realpath(path) == os.path.realpath(FUNCS):
        _b = uc1_band.load()
        rows = [(e, n, s) for e, n, s in rows if e not in _b["removed"]]
        rows = [(e, n, _b["extend"].get(e, e + s) - e) for e, n, s in rows]
        rows += [(st, "UC1-FRONTIER-%08X" % st, sz)
                 for st, sz in _b["frontier"].items()]
    rows.sort()
    return rows


def first_int3_run(ins):
    """Index pair (first, last) of the first decoded int3 run that is followed
    by a non-int3 instruction, or None."""
    for k, i in enumerate(ins[:-1]):
        if i.mnemonic != "int3" or ins[k + 1].mnemonic == "int3":
            continue
        j = k
        while j >= 0 and ins[j].mnemonic == "int3":
            j -= 1
        return j + 1, k
    return None


def last_int3_run_end(ins):
    """Address just past the last int3 of the LAST decoded int3 run, or None.
    Used for the overlap-only cases where the run ends exactly at a listed
    entry and the few overrun bytes cannot decode."""
    for k in range(len(ins) - 1, -1, -1):
        if ins[k].mnemonic == "int3":
            j = k
            while j >= 0 and ins[j].mnemonic == "int3":
                j -= 1
            return ins[j + 1].address, ins[k].address + 1
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", help="write the enumeration here")
    a = ap.parse_args()

    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        from capstone.x86 import X86_OP_IMM
    except ImportError:
        sys.exit("capstone required")

    rd = load_pe(EXE)
    fns = load_functions(FUNCS)
    listed = {e for e, _n, _s in fns}
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True

    rows = []
    strict_entries = set()
    for i, (e, name, size) in enumerate(fns):
        code = rd(e, size)
        if not code:
            continue
        ins = list(md.disasm(code, e))
        end = e + size
        nxt_entry = fns[i + 1][0] if i + 1 < len(fns) else None
        overlap = end - nxt_entry if nxt_entry and end > nxt_entry else 0

        run = first_int3_run(ins)
        strict = False
        pad = bnd = None
        if run:
            pad = ins[run[0]].address
            bnd = ins[run[1]].address + 1
            if bnd < end and (bnd % 16 == 0 or bnd in listed):
                strict = True
        if strict:
            strict_entries.add(e)

        # adjudication ------------------------------------------------------
        verdict = det = None
        corrected = ""
        prev_mn = ""
        exact = 0
        if strict:
            det = "strict"
            # the instruction just before the pad
            pi = run[0] - 1
            prev_mn = ins[pi].mnemonic if pi >= 0 else "-"
            # does any pre-pad branch hit the boundary exactly?
            for q in ins:
                if q.address >= pad:
                    break
                if q.mnemonic == "call" or q.mnemonic == "jmp" or q.mnemonic.startswith("j"):
                    for o in q.operands:
                        if o.type == X86_OP_IMM and o.imm == bnd:
                            exact += 1
            if bnd in listed or overlap:
                verdict = "merge"
                corrected = "%08X" % pad
            elif exact:
                verdict = "legitimate body (interior alignment pad)"
            else:
                verdict = "UNRESOLVED - inspect"
        elif overlap:
            det = "overlap-only"
            # own code end: last decodable instruction end, else the run's pad start
            if ins:
                corrected = "%08X" % (ins[-1].address + ins[-1].size)
            lr = last_int3_run_end(ins)
            if lr and lr[1] == nxt_entry:
                pad, bnd = lr
                corrected = "%08X" % pad
            verdict = "merge"
        else:
            continue

        covered = 0
        if overlap:
            j = i + 1
            while j < len(fns) and fns[j][0] < end:
                covered += 1
                j += 1

        rows.append({
            "entry": "%08X" % e, "name": name, "size": size,
            "end": "%08X" % end,
            "pad": "%08X" % pad if pad else "-",
            "boundary": "%08X" % bnd if bnd else "-",
            "boundary_listed": "yes" if bnd in listed else "no" if bnd else "-",
            "prev": prev_mn,
            "prepad_branch_hits_boundary": exact if strict else "-",
            "overlap_into_next": overlap,
            "covered_listed_entries": covered if overlap else "-",
            "next_entry": "%08X" % nxt_entry if nxt_entry else "-",
            "corrected_end": corrected,
            "verdict": verdict, "detector": det,
        })

    strict_rows = [r for r in rows if r["detector"] == "strict"]
    merges = [r for r in rows if r["verdict"] == "merge"]
    legit = [r for r in rows if r["verdict"].startswith("legitimate")]
    print("strict rule hits        : %d (boundary listed %d, unlisted %d)"
          % (len(strict_rows),
             sum(1 for r in strict_rows if r["boundary_listed"] == "yes"),
             sum(1 for r in strict_rows if r["boundary_listed"] == "no")))
    print("overlap census          : %d merges total (%d strict + %d overlap-only)"
          % (len(merges), sum(1 for r in merges if r["detector"] == "strict"),
             sum(1 for r in merges if r["detector"] == "overlap-only")))
    print("legitimate bodies       : %d" % len(legit))
    twice = sum(int(r["end"], 16) - int(r["pad"], 16)
                for r in strict_rows if r["pad"] != "-")
    print("bytes counted twice     : %d (= end - first int3 run, over the 36)"
          % twice)

    if a.tsv:
        cols = ["entry", "name", "size", "end", "pad", "boundary",
                "boundary_listed", "prev", "prepad_branch_hits_boundary",
                "overlap_into_next", "covered_listed_entries",
                "next_entry", "corrected_end",
                "verdict", "detector"]
        with io.open(a.tsv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, cols, delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print("wrote %s (%d rows)" % (a.tsv, len(rows)))


if __name__ == "__main__":
    main()
