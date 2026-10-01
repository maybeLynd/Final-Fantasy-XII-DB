#!/usr/bin/env python3
"""unlisted_admissions.py - which unlisted code blocks become MEASURED bodies, row by row.

Why this exists
---------------
`functions.tsv` lists 34,270 non-funclet bodies. **244,619 bytes of executing code in the same
`.text` span are not in that list at all** - see
`99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`. Every
coverage figure this database reports divides by 34,270, so that code is in neither the numerator
nor the denominator: it is not explained and it is not counted as unexplained.

**UC-1 decided what to do about it, 3-0 (FABLE, OPUS, ASTRA), 2026-09-13: option (1) - admit the
distinct shipping bodies into the measured population as unexplained frontier, with a dated
population change and a recorded series break.** Not a D exception: inventing an exclusion for
unexplained engine code is the one outcome a completion rule must not allow.

This is the instrument that produces the admitted set. It does not change any denominator by
itself; it emits the rows, and `progress.py` consumes the count.

What a row can be
-----------------
A splitter block is a code RUN, not a proven function entry, so each block is adjudicated:

    table         (ADDED 2026-09-25, OPUS) the block opens with >= 3 image-base-relative dword RVAs
                  landing inside the predecessor: the predecessor's INLINE JUMP TABLE, which is
                  data. Tested first, because a table follows the function's last instruction and
                  so passes the `body` rule below whenever that instruction is a `ret`/`jmp`. 427
                  rows first published as `body` were tables. **Not admitted.**

    body          the block begins where the previous listed body genuinely ENDED - its
                  predecessor's last instruction is a terminator (`ret`/`jmp`/`int3`/`ud2`/`hlt`,
                  and `repz ret`, the AMD-preferred return encoding), or something in the image
                  references the block's first byte. **Admitted: +1 to the population.**

    continuation  the predecessor's last instruction is NOT a terminator and nothing references
                  the block. Execution falls straight in, so this is the TAIL of an under-sized
                  recorded body, not a second function. **Not admitted; it extends an extent.**

    ambiguous     the predecessor ends in `call`. Execution returns from the call into these
                  bytes *unless the callee is `noreturn`*, which is not tested here. **Not
                  admitted, and never silently dropped** - reported every run as a declared
                  uncertainty band on the population.

The band is the point
---------------------
The splitter's control scored **precision 0.984, recall 0.926** against 28,368 known bodies. Recall
below 1 does NOT make the count a lower bound when precision is also below 1 - the errors run both
ways. So this prints a **range**, never a single proved count, and nothing downstream may hardcode
one. (ASTRA's UC-1 vote makes this binding: *"Do not hardcode 1309 as a proved body count or strict
lower bound. Use the actual admitted, deduplicated body rows for N."*)

A block is not yet a body, and this instrument says so
------------------------------------------------------
**The admitted rows are NOT wired into any denominator, and this tool does not do it.** An
independent test says a splitter block is not function-shaped: does a linear decode walk from the
first byte to the last? The **34,270 listed bodies are the control**, and they are banded by size
because a long range has more chance to hit an embedded jump table:

    size band     listed bodies     admitted blocks
    1-64 B            100.0 %            79.2 %
    64-256 B           99.8 %            40.6 %
    256-1024 B         98.7 %            22.0 %
    1024-4096 B        97.7 %            39.1 %
    4096+ B            92.6 %            44.4 %

Size is therefore not the explanation: the gap is widest in the band where listed bodies are
essentially perfect. The bytes themselves are largely real code - `001505C0` opens
`push rbp; mov rbp, rsp`, and the big head-of-`.text` blocks are dense SSE with REX prefixes - so
this is not a claim that the region is data. It is a claim about the **boundaries**: a block
frequently begins mid-instruction or spans more than one function, so **a block count is not a body
count** and admitting 1,302 of them as 1,302 bodies is not supported by anything measured here.

*(A rescue test - retry the decode at start+1..+15 - was run and discarded: its control rescued
**400 of 400** deliberately corrupted listed bodies, so "some shift decodes" is a property of almost
any byte range and evidence of nothing.)*

Reconciliation with the extent errata
-------------------------------------
`_index/FUNCTION-EXTENT-ERRATA.tsv` corrects 29 listed bodies whose recorded extent runs PAST their
own end into the next function - the opposite error to the under-sized bodies that produce
`continuation` rows here. Both are read from the same `functions.tsv`, so a body whose extent the
errata shortens is re-measured with the corrected end before its successor block is adjudicated.
"""
import argparse
import bisect
import collections
import io
import os
import struct
import sys

import capstone
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
BLOCKS = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code", "unlisted-code-blocks.tsv")
ERRATA = os.path.join(DB, "_index", "FUNCTION-EXTENT-ERRATA.tsv")
OUT = os.path.join(DB, "99-Unresolved-Residual", "Unlisted-Code", "unlisted-body-admissions.tsv")

IMAGE = 0x00120000
# `repz ret` is a RETURN - the AMD-preferred encoding. Omitting it cost this page 3 blocks and
# 802 bytes, misfiled as "the predecessor did not return" when it plainly did.
TERMINATORS = ("ret", "jmp", "int3", "ud2", "hlt", "repz ret")


def load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    optsz = struct.unpack_from("<H", d, pe + 20)[0]
    secs, o = [], pe + 24 + optsz
    for _ in range(nsec):
        name = d[o:o + 8].rstrip(b"\0").decode("ascii", "replace")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        secs.append((name, va, vs, ra, rs))
        o += 40
    return d, pe, secs


def make_off(secs):
    def off(va):
        r = va - IMAGE
        for _n, sva, vs, ra, rs in secs:
            if sva <= r < sva + max(vs, rs):
                k = r - sva
                return None if k >= rs else ra + k
        return None
    return off


def reference_routes(d, pe, secs, off):
    """Every address in the image that something points at, kept per route.

    The routes disagree about what they can see, which is the point: a block reached only by a
    relative `call` is invisible to the relocation table, and a block whose only reference is a
    64-bit pointer in `.data` is invisible to a text scan.

    Returns (ref_unwind, ref_code, ref_reloc).  **Only ref_code and ref_reloc are admissible
    evidence under FINAL-AUDIT-PROTOCOL pass 6** - the exception directory is unwind metadata,
    which may never support a semantic claim.  Route 1 is still computed and reported
    (`unwind_listed` in the TSV) because being absent from the other two routes while present in
    .pdata is diagnostic - but it no longer feeds `referenced`, and a block listed ONLY by the
    unwinder now verdicts on its predecessor's terminator alone.
    (OPUS-REQ-SWE2-EC7-UNLISTED-REFERENCED-ROUTES, 2026-09-17: the union folded route 1 into
    `referenced`, contaminating exactly one verdict=body row and making the column unusable as
    evidence.)
    """
    magic = struct.unpack_from("<H", d, pe + 24)[0]
    ddoff = pe + 24 + (112 if magic == 0x20B else 96)
    ref_unwind, ref_code, ref_reloc = set(), set(), set()

    # 1. the exception directory - every function with unwind data announces its own range.
    #    pass 6: .pdata is never evidence. Informational only.
    exc_rva, exc_sz = struct.unpack_from("<II", d, ddoff + 3 * 8)
    po = off(IMAGE + exc_rva)
    if po is not None:
        for i in range(exc_sz // 12):
            b, e, _u = struct.unpack_from("<III", d, po + i * 12)
            if b or e:
                ref_unwind.add(IMAGE + b)

    # 2. direct rel32 call/jmp and RIP-relative lea, decoded out of .text by opcode
    text = next((s for s in secs if s[0] == ".text"), None)
    if text:
        _n, tva, _vs, tpr, trs = text
        for k in range(tpr, tpr + trs - 5):
            if d[k] in (0xE8, 0xE9):
                disp = struct.unpack_from("<i", d, k + 1)[0]
                ref_code.add(IMAGE + tva + (k - tpr) + 5 + disp)
        for k in range(tpr, tpr + trs - 8):
            if d[k] in (0x48, 0x4C) and d[k + 1] == 0x8D and (d[k + 2] & 0xC7) == 0x05:
                disp = struct.unpack_from("<i", d, k + 3)[0]
                ref_code.add(IMAGE + tva + (k - tpr) + 7 + disp)

    # 3. the base relocation table - every absolute 64-bit address the loader must fix up
    rel_rva, rel_sz = struct.unpack_from("<II", d, ddoff + 5 * 8)
    ro = off(IMAGE + rel_rva)
    if ro is not None:
        p = ro
        while p < ro + rel_sz:
            page, sz = struct.unpack_from("<II", d, p)
            if sz == 0:
                break
            for q in range(p + 8, p + sz, 2):
                e = struct.unpack_from("<H", d, q)[0]
                if e >> 12 == 10:                      # IMAGE_REL_BASED_DIR64
                    o2 = off(IMAGE + page + (e & 0xFFF))
                    if o2 is not None:
                        ref_reloc.add(struct.unpack_from("<Q", d, o2)[0])
            p += sz
    return ref_unwind, ref_code, ref_reloc


def load_bodies(path, errata):
    """entry -> body_bytes for the non-funclet listed bodies, with errata extents applied."""
    sizes = {}
    with io.open(path, encoding="utf-8", errors="replace") as f:
        head = f.readline().rstrip("\n").split("\t")
        ie, inm, ib = head.index("entry"), head.index("name"), head.index("body_bytes")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) > ib and p[ib].isdigit() and not p[inm].startswith(("Unwind@", "Catch_All@")):
                a = int(p[ie], 16)
                end = errata.get(a)
                sizes[a] = (end - a) if end and a < end < a + int(p[ib]) else int(p[ib])
    return sizes


def load_errata(path):
    out = {}
    if not os.path.exists(path):
        return out
    with io.open(path, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        ie, ice, iv = head.index("entry"), head.index("corrected_end"), head.index("verdict")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) > iv and p[iv] == "merge" and p[ice].strip():
                out[int(p[ie], 16)] = int(p[ice], 16)
    return out


def load_blocks(path):
    rows = []
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if p[0] == "start_va":
                continue
            rows.append((int(p[0], 16), int(p[1])))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=FUNCS)
    ap.add_argument("--blocks", default=BLOCKS)
    ap.add_argument("--errata", default=ERRATA)
    ap.add_argument("--out", default=None, help="write the per-row admissions TSV")
    a = ap.parse_args()

    d, pe, secs = load_pe(a.exe)
    off = make_off(secs)
    errata = load_errata(a.errata)
    sizes = load_bodies(a.funcs, errata)
    entries = sorted(sizes)
    blocks = load_blocks(a.blocks)
    ref_unwind, ref_code, ref_reloc = reference_routes(d, pe, secs, off)
    ref = ref_code | ref_reloc                    # pass-6-admissible routes only
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    def last_mnemonic(va, n):
        o = off(va)
        if o is None:
            return "NO-BYTES"
        ins = list(md.disasm(d[o:o + n], va))
        if not ins:
            return "DECODE-EMPTY"
        # a recorded size that ends mid-instruction is itself evidence the extent is wrong
        if ins[-1].address + ins[-1].size != va + n:
            return "DECODE-SHORT"
        return ins[-1].mnemonic

    def decodes_to_end(va, n):
        """Does a linear decode reach the last byte? The listed bodies are the control."""
        o = off(va)
        if o is None or n <= 0:
            return False
        ins = list(md.disasm(d[o:o + n], va))
        return bool(ins) and ins[-1].address + ins[-1].size == va + n

    def table_run(start, n, prev):
        """Leading image-base-relative RVAs into the predecessor: its inline jump table.

        ADDED 2026-09-25 (OPUS). A `switch` compiled as `mov ecx,[base + idx*4 + T] ; add rcx,base ;
        jmp rcx` leaves T - dword RVAs of the function's own arms - right after the function's last
        instruction, so a block that follows a `ret` can be DATA. 427 `body` rows first published
        here were exactly that (00277851: RVA 0x156D85 -> 00276D85, inside 00276D30). Tested from the
        first 4-aligned offset; a run of >= 3 consecutive dwords landing in [prev, start) is the
        test, and 0 of 31,739 listed bodies meet it against their own predecessors (the control).
        """
        if prev is None:
            return 0, start
        a = (start + 3) & ~3
        run = 0
        while a + 4 <= start + n:
            o = off(a)
            if o is None:
                break
            v = struct.unpack_from("<I", d, o)[0] + IMAGE
            if not (prev <= v < start):
                break
            run += 1
            a += 4
        return run, a

    out_rows = []
    verdicts = collections.Counter()
    vbytes = collections.Counter()
    for start, n in blocks:
        i = bisect.bisect_right(entries, start) - 1
        # A block the function list has since grown over is not unlisted any more. Say so rather
        # than walking back past the covering body to an older predecessor (2026-09-25, OPUS:
        # 005806B9 is inside 0057FE80 once that body's listed size became 2,360 bytes).
        covering = entries[i] if i >= 0 and entries[i] + sizes[entries[i]] > start else None
        while i >= 0 and entries[i] + sizes[entries[i]] > start:
            i -= 1
        prev = entries[i] if i >= 0 else None
        mnem = last_mnemonic(prev, sizes[prev]) if prev is not None else "NO-PREDECESSOR"
        reffed = start in ref                      # admissible routes only
        routes = "+".join(n for n, s in (("rel32/lea", ref_code), ("dir64", ref_reloc),
                                       ("pdata", ref_unwind)) if start in s) or "-"
        aligned = (start % 16 == 0)
        trun, tend = table_run(start, n, prev)

        if covering is not None:
            verdict, why = "covered", ("inside listed %08X, which the function list has grown to "
                                       "cover since the block census" % covering)
        elif trun >= 3:
            verdict, why = "table", ("inline jump table of %08X: %d image-base RVAs into it; "
                                     "remainder %d B not classified" % (prev, trun, start + n - tend))
        elif mnem in TERMINATORS or prev is None:
            verdict, why = "body", "predecessor ends in %s" % mnem
        elif reffed:
            verdict, why = "body", "referenced despite fall-through from %s" % mnem
        elif mnem == "call":
            verdict, why = "ambiguous", "predecessor ends in call; callee noreturn not tested"
        elif start in ref_unwind:
            verdict, why = "continuation", ("falls through from %s; listed only by .pdata, "
                                            "which pass 6 bans as evidence" % mnem)
        else:
            verdict, why = "continuation", "falls through from %s, unreferenced" % mnem

        verdicts[verdict] += 1
        vbytes[verdict] += n
        out_rows.append((start, n, prev, mnem, reffed, routes, aligned,
                         decodes_to_end(start, n), verdict, why))

    nlisted = len(sizes)
    body, cont, amb = verdicts["body"], verdicts["continuation"], verdicts["ambiguous"]
    tab = verdicts["table"]
    print("listed non-funclet bodies        : %d" % nlisted)
    print("unlisted code blocks adjudicated : %d  (%d bytes)"
          % (len(blocks), sum(n for _s, n in blocks)))
    print()
    for k in ("table", "covered", "body", "continuation", "ambiguous"):
        print("  %-13s %5d block(s) %8d B" % (k, verdicts[k], vbytes[k]))
    print()
    print("ADMITTED to the measured population : %d" % body)
    print("  not admitted - continuations       : %d  (they extend an existing extent)" % cont)
    print("  not admitted - ambiguous           : %d  (declared uncertainty, never dropped)" % amb)
    print("  not admitted - tables              : %d  (the predecessor's inline jump table - data)" % tab)
    # The gate: does a block look like a function body at all? Banded, against the listed control.
    bands = [(1, 64), (64, 256), (256, 1024), (1024, 4096), (4096, 1 << 30)]
    admitted = [(s, n) for s, n, _p, _m, _r, _rt, _a, _dc, v, _w in out_rows if v == "body"]
    unwind_only = [r for r in out_rows if r[5] == "pdata"]
    print("reference routes: rel32/rip-lea %d | dir64 %d | .pdata %d (pass 6: inadmissible," %
          (len(ref_code), len(ref_reloc), len(ref_unwind))
          + " reported as `routes` but never counted in `referenced`)")
    print("  blocks listed ONLY by .pdata: %d  (referenced=no by construction)" % len(unwind_only))

    def full_rate(pairs, lo, hi):
        sel = [(s, n) for s, n in pairs if lo <= n < hi]
        if not sel:
            return None, 0
        ok = sum(1 for s, n in sel if decodes_to_end(s, n))
        return 100.0 * ok / len(sel), len(sel)

    print()
    print("DOES A BLOCK LOOK LIKE A BODY? linear decode reaching the last byte,")
    print("  with the %d listed bodies as the control, banded by size:" % nlisted)
    print("      size band        listed    admitted")
    lrates, arates = [], []
    for lo, hi in bands:
        lr, _ = full_rate(list(sizes.items()), lo, hi)
        ar, an = full_rate(admitted, lo, hi)
        lrates.append("%.1f" % lr if lr is not None else "-")
        arates.append("%.1f" % ar if ar is not None else "-")
        print("   %6d-%-9s  %6s    %6s   (%d admitted)"
              % (lo, ("%d" % hi) if hi < (1 << 30) else "up",
                 "%.1f %%" % lr if lr is not None else "-",
                 "%.1f %%" % ar if ar is not None else "-", an))
    print()
    print("population change IS NOT APPLIED, and this tool does not apply it.")
    print("  %d..%d is where the denominator WOULD land - but the table above says a splitter"
          % (nlisted + body, nlisted + body + amb))
    print("  block is not function-shaped, so a block count is not a body count. The bytes are")
    print("  real code; the BOUNDARIES are not established. Admitting them one-block-one-body")
    print("  would be an unsupported bulk disposition. The mechanism is ready; the input is not.")

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Per-row adjudication of the unlisted code blocks, for the UC-1 population "
                    "change.\n")
            f.write("# Voted 3-0 (FABLE, OPUS, ASTRA) 2026-09-13: admit distinct bodies as "
                    "unexplained frontier,\n")
            f.write("# never as a D exception. `body` rows are admitted; `continuation` rows "
                    "extend an existing\n")
            f.write("# extent; `ambiguous` rows are a declared uncertainty band and are never "
                    "silently dropped.\n")
            f.write("# Regenerate with gfz-scripts/unlisted_admissions.py --out <this file>.\n")
            f.write("# `table` rows (added 2026-09-25, OPUS) open with >= 3 image-base RVAs into the "
                    "predecessor: its\n# inline jump table - data, not admitted. Control: 0 of the "
                    "listed bodies meet the test.\n")
            f.write("# `decodes_to_end` is the body-shape gate: a linear decode from the first "
                    "byte reaching the\n")
            f.write("# last. Listed bodies pass %s %% by size band; the admitted rows pass\n"
                    % "/".join(lrates))
            f.write("# %s %% (computed on this run; tables are not admitted). A `no` does not "
                    "mean the bytes are data - it means the\n" % "/".join(arates))
            f.write("# BOUNDARY is not established, which is why no denominator has moved.\n")
            f.write("# `referenced` counts only the two pass-6-admissible routes - rel32 call/jmp"
                    " + RIP lea, and\n")
            f.write("# base-relocation DIR64. `routes` names every route that lists the block;"
                    " `pdata` (the PE\n")
            f.write("# exception directory) is unwind metadata, banned as evidence under FINAL-"
                    "AUDIT-PROTOCOL\n")
            f.write("# pass 6, so a `pdata` route never makes `referenced` yes. Split per"
                    " OPUS-REQ-SWE2-EC7-\n")
            f.write("# UNLISTED-REFERENCED-ROUTES, 2026-09-17 - the earlier union made exactly"
                    " one body row\n")
            f.write("# look referenced on unwind data alone.\n")
            f.write("start_va\tbytes\tprev_entry\tprev_last_ins\treferenced\troutes\taligned16"
                    "\tdecodes_to_end\tverdict\twhy\n")
            for s, n, prev, mnem, reffed, routes, aligned, dec, verdict, why in out_rows:
                f.write("%08X\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                        % (s, n, ("%08X" % prev) if prev is not None else "-", mnem,
                           "yes" if reffed else "no", routes,
                           "yes" if aligned else "no",
                           "yes" if dec else "no", verdict, why))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
