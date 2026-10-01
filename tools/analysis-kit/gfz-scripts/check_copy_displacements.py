#!/usr/bin/env python3
"""check_copy_displacements.py - fields declared from an unrolled block copy's displacement.

**A BLOCK COPY'S DISPLACEMENT IS NOT A FIELD.** A compiler unrolls a structure copy into a run of
`movups` stepping 16 bytes at a time, and each step carries a displacement that looks exactly like
a field offset: correctly aligned, plausibly sized, and cited from a real instruction in a real
body. Read one out of its run and you get a field that does not exist.

This corpus has recorded that mistake **three times**, each found by hand and each after the row
was published:

* `CharacterRenderObject` - nine offsets at a perfect `0x10` stride inside `+0x80`, which are the
  `movups` steps of the constructor's `0x318` block copy. Stride, count and alignment all read as
  corroboration for a lattice of 16-byte elements that does not exist.
* the save payload map - one unrolled `0x200`-byte copy read as **eight** 16-byte fields, recorded
  in `BattleUnit`'s own store text as the precedent.
* `SaveImageHeader.vec4StoreHead30` - a 12-byte row at `+0x30`, `TYPE RESOLVED / HIGH`, whose
  16-byte `movups` turns out to be one step of an unrolled WHOLE-HEADER copy in all three bodies it
  was cited from (23, 18 and 24 `movups` around it). It overlapped three elements of a real array.

Three by hand is enough. This finds the rest mechanically.

THE TEST, and why it is deliberately narrow. A row is flagged when an address in its evidence
column decodes to a 16-byte move (`movups`/`movaps`/`movdqu`/`movdqa`) that sits inside a RUN of
such moves whose displacements step uniformly. A single `movups` is not suspicious - vectors are
copied one at a time all over this engine. What is suspicious is a step in a *sequence*, because
only a bulk copy produces one.

    python check_copy_displacements.py --self-test
    python check_copy_displacements.py

**A FLAG IS A CANDIDATE.** The instruction is real and the row may still be right: a field can be
genuinely written by one step of a copy that happens to be unrolled. What the flag says is that the
citation does not establish it, which is a different claim and the one worth checking.
"""
import argparse
import collections
import io
import os
import re
import sys

import kit_paths as KP
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM
from capstone.x86 import X86_REG_RSP, X86_REG_RBP

import check_literal_citations as CLC
import member_reach_scan as MRS

STORE = os.path.join(KP.DB, "_types", "fields.tsv")
WIDE_MOV = ("movups", "movaps", "movdqu", "movdqa")

#: How many 16-byte moves in a row before it is a copy rather than a few vectors.
RUN_MIN = 4
#: How far around the cited address to look for the run.
WINDOW = 0x60


def runs_at(img, md, sizes, starts, va):
    """(is_wide_move, run_length) for the instruction at `va`, using its containing body."""
    import bisect
    k = bisect.bisect_right(starts, va) - 1
    if k < 0:
        return False, 0
    fn = starts[k]
    if not (fn <= va < fn + sizes[fn]):
        return False, 0
    _s, b = img.at(fn, sizes[fn])
    if not b:
        return False, 0
    here = None
    wide = []
    for i in md.disasm(b, fn):
        if i.mnemonic in WIDE_MOV:
            wide.append(i.address)
            if i.address == va:
                here = i.address
    if here is None:
        return False, 0
    near = [a for a in wide if abs(a - here) <= WINDOW]
    return True, len(near)


def body_copy_profile(img, md, sizes, fn):
    """(largest wide-move cluster, count of OTHER object stores) for a whole body.

    The second number is the narrowing. A body that merely CONTAINS an unrolled copy proves
    nothing about a row - `TextDrawState.penX` cites `002AE610`, whose copy run is 26 long and
    has nothing to do with `penX`, which that body writes directly. The row is only undermined
    when the cited body writes the object THROUGH THE COPY AND NOWHERE ELSE, so stores that are
    neither wide moves nor stack traffic are counted and a non-zero count clears the row.
    """
    if fn not in sizes:
        return 0, 1
    _s, b = img.at(fn, sizes[fn])
    if not b:
        return 0, 1
    wide, other = [], 0
    for i in md.disasm(b, fn):
        if i.mnemonic in WIDE_MOV:
            wide.append(i.address)
            continue
        ops = i.operands
        if i.mnemonic.startswith("mov") and len(ops) == 2 and ops[0].type == CS_OP_MEM:
            base = ops[0].mem.base
            if base not in (X86_REG_RSP, X86_REG_RBP, 0):
                other += 1
    best = 0
    for a in wide:
        best = max(best, sum(1 for x in wide if abs(x - a) <= WINDOW))
    return best, other



def pure_copy_helpers(img, md, sizes):
    """Bodies that are NOTHING BUT a block copy: wide moves and a ret.

    `00202C70` is four `movups` load/store pairs and a `ret`, and it has 52 callers. A row that
    rests on it has an extent and no type: a shared copier moves `0x40` bytes for anybody, so the
    displacements inside it carry no more meaning than `memcpy`'s do. Image-wide there are only a
    handful of these, which is what makes the rule safe to state as a rule.
    """
    out = {}
    for fn, sz in sizes.items():
        if not (8 <= sz <= 96):
            continue
        _s, b = img.at(fn, sz)
        if not b:
            continue
        wide, ok = 0, True
        for i in md.disasm(b, fn):
            if i.mnemonic in WIDE_MOV:
                wide += 1
                continue
            if i.mnemonic in ("ret", "nop", "int3"):
                continue
            ok = False
            break
        if ok and wide >= 4:
            out["%08X" % fn] = wide // 2 * 16
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=STORE)
    ap.add_argument("--exe", default=CLC.EXE)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    img = CLC.Image(a.exe)
    sizes, _names = MRS.load_funcs()
    starts = sorted(sizes)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    # operands are needed to tell an object store from stack traffic in body_copy_profile()
    md.detail = True

    if a.self_test:
        ok = True
        # The known case: vec4StoreHead30's citations are all inside long copy runs.
        for va, want in ((0x00583C59, True), (0x0057E375, True), (0x00229C75, True)):
            isw, n = runs_at(img, md, sizes, starts, va)
            good = isw and (n >= RUN_MIN) == want
            ok = ok and good
            print("  %08X  wide=%-5s run=%-3d  %s" % (va, isw, n, "ok" if good else "BROKEN"))
        # A control in the other direction: an ordinary instruction must not look like a copy.
        isw, n = runs_at(img, md, sizes, starts, 0x00583E8A)   # mov byte ptr [rdi+r8*4+0x20]
        ok = ok and not isw
        print("  %-50s %s" % ("a byte store is not a wide move", "ok" if not isw else "BROKEN"))
        print("  %s" % ("all controls behave" if ok else "AT LEAST ONE CONTROL IS BROKEN"))
        return 0 if ok else 2

    raw = io.open(a.store, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in raw else "\n"
    flagged = []
    entry_flagged = []
    helper_flagged = []
    rows = 0
    helpers = pure_copy_helpers(img, md, sizes)
    for line in raw.split(eol):
        f = line.split("\t")
        if len(f) < 9:
            continue
        rows += 1
        # BOTH COLUMNS, because the corpus puts citations in either. Reading only `evidence` missed
        # the very row this checker was written for: `SaveImageHeader.vec4StoreHead30` carries its
        # three addresses in `meaning`, so a check that looked at `evidence` alone reported the
        # store clean of the defect it exists to find.
        ev = f[5] + " " + f[8]
        cited = sorted(set(re.findall(r"\b(0[0-9A-Fa-f]{7})\b", ev)))
        if not cited:
            continue
        # EVERY cited address must be a copy step, not merely one of them. A row that also cites a
        # bit-mask or a comparison is established by THAT, and the copy address is incidental.
        # `SpawnRecord.lifecycleFlags` reads "and-mask clears 0xFFFFFF7A ... test bit-2" and was
        # flagged only because one of its several addresses sits in a copy run - which turned the
        # output into 34 rows of mostly-sound citations instead of a short list worth reading.
        # THE BLIND SPOT THIS CHECK CARRIED UNTIL 2026-09-19. `runs_at` asks whether the cited
        # address IS a wide move, so a row that cites its functions BY ENTRY escapes every test
        # below: `all_copy` goes false on the first entry address and the row is never considered.
        # `SavePayload.replicatedVec4RecordSpan2008` - 23,306 bytes, the LARGEST `TYPE RESOLVED`
        # span in the store - cites `00229B40` and `005844A0`, both function entries, and both
        # bodies contain nothing but one compiler-unrolled `memcpy`. Citing a function instead of
        # an instruction made the biggest claim in the store invisible to the instrument written
        # to check exactly that claim.
        # A citation to a PURE copy helper establishes an extent and never a type.
        used = [h for h in cited if h in helpers]
        if used:
            rest = [h for h in cited if h not in used]
            helper_flagged.append((f[0], f[1], f[2], f[3], f[6], used[0], helpers[used[0]], rest))

        ents = [h for h in cited if int(h, 16) in sizes]
        if ents and len(ents) == len(cited):
            prof = [body_copy_profile(img, md, sizes, int(h, 16)) for h in ents]
            if min(r for r, _o in prof) >= RUN_MIN and all(o == 0 for _r, o in prof):
                entry_flagged.append(
                    (f[0], f[1], f[2], f[3], f[6], " ".join(ents), max(r for r, _o in prof))
                )

        best, all_copy = 0, True
        for h in cited:
            isw, n = runs_at(img, md, sizes, starts, int(h, 16))
            if isw and n >= RUN_MIN:
                best = max(best, n)
            else:
                all_copy = False
        if all_copy and best >= RUN_MIN:
            flagged.append((f[0], f[1], f[2], f[3], f[6], cited[0], best))

    print("rows with an evidence address : %d" % rows)
    print("rows whose EVERY citation is a copy step : %d" % len(flagged))
    print()
    # THE NARROWING THAT MAKES THIS ACTIONABLE. A row whose size is 16 or more can legitimately BE
    # the thing the copy moves - `transformBankA` is three 4x4 matrices and its own store text says
    # they are published by an unrolled sequence, so a long run there is corroboration, not doubt.
    # A row SMALLER than the move cannot have been established by it: a 16-byte `movups` says
    # nothing about a 4-byte field at its displacement. That is exactly the shape of the three
    # defects found by hand - `vec4StoreHead30` was 12 bytes cited from a 16-byte move.
    sharp = [r for r in flagged if int(r[2]) < 16]
    broad = [r for r in flagged if int(r[2]) >= 16]

    print("=== SHARPEST: the row is SMALLER than the 16-byte move that cites it ===")
    for t, o, sz, nm, rd, h, n in sorted(sharp, key=lambda r: -r[6]):
        print("  %-26s %-8s %-4s %-22s %-22s %s run=%d" % (t, o, sz, nm[:22], rd[:22], h, n))
    if not sharp:
        print("  none")
    print()
    print("=== BROADER: row is 16+ bytes, so the copy may be moving the row itself ===")
    for t, o, sz, nm, rd, h, n in sorted(broad, key=lambda r: -r[6])[:12]:
        print("  %-26s %-8s %-4s %-22s %-22s %s run=%d" % (t, o, sz, nm[:22], rd[:22], h, n))
    if len(broad) > 12:
        print("  ... and %d more" % (len(broad) - 12))
    print()
    by_type = collections.Counter(t for t, _o, _s, _n, _r, _h, _c in flagged)
    if by_type:
        print("by type:", ", ".join("%s x%d" % (t, c) for t, c in by_type.most_common(8)))
    print()
    print("=== CITED BY FUNCTION ENTRY ONLY, and every such body is dominated by a copy run ===")
    print("    (these never reached the tests above - see the comment in main())")
    for t, o, sz, nm, rd, hs, n in sorted(entry_flagged, key=lambda r: -int(r[2])):
        print("  %-26s %-8s %-6s %-30s %-16s %s maxrun=%d" % (t, o, sz, nm[:30], rd[:16], hs, n))
    if not entry_flagged:
        print("  none")
    print()
    print("=== CITES A PURE BLOCK-COPY HELPER (extent yes, type no) ===")
    print("    %d such helper(s) exist image-wide. `others` is what else the row cites - a row with"
          % len(helpers))
    print("    a second, type-bearing citation may be perfectly sound; one with none is not.")
    for t_, o, sz, nm, rd, h, n, rest in sorted(helper_flagged, key=lambda r: len(r[7])):
        print("  %-24s %-8s %-5s %-26s %-16s %s copies %dB  others=%s"
              % (t_, o, sz, nm[:26], rd[:16], h, n, ",".join(rest) if rest else "NONE"))
    if not helper_flagged:
        print("  none")
    print()
    print("A FLAG IS A CANDIDATE, not a defect. The instruction is real and the row may still be")
    print("right - a field can be written by one step of a copy that happens to be unrolled. The")
    print("flag says the CITATION does not establish it, which is the claim worth checking.")
    return 1 if sharp else 0


if __name__ == "__main__":
    sys.exit(main())
