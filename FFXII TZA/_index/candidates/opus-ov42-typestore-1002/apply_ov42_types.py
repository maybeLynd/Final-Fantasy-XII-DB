"""apply_ov42_types.py [--apply] - OPUS consumes FABLE's routed type-store text from its reviews of ASTRA's
ov42-effective-id-source, ov42-sequence-queue-source and ov42-kind-row-coherence packets (OPUS, 2026-10-02).

- _types/fields.tsv: three reader lists widened (AuthoredTableHeader +0x08 / +0x0C, BattleRuntimeUnitRecord +0x010).
- 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md: a new OPUS section, the inverse reader (three
  row-to-index divides over the action table) and its stride precondition.
- 08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md: the null-O1 case qualified in section 2.5, and a new
  OPUS section, the effective-id getter beside its owner resolver.
OPUS re-read every cited instruction at the bytes first (ov42_check.py). Idempotent; fields.tsv has mixed EOLs, so
rows are edited by splitlines(keepends=True) and only the evidence cell's end changes.
"""
import io
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
FIELDS = "_types/fields.tsv"
REG = "02-Resource-And-Asset-Pipeline/authored-data-table-registry.md"
SCR = "08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md"
REV = "_index/candidates/fable-review-astra-ov42-"
TAG = " || READERS ADDED 2026-10-02 (OPUS, from FABLE's reviews of ASTRA ov42-sequence-queue-source / ov42-kind-row-coherence): "

ROWS = {
    ("AuthoredTableHeader", "0x08"): TAG + "00306760 + 0x152 and + 0xC7, 00306BD0 + 0xAC - each a movzx feeding an "
    "UNSIGNED 32-bit div (a divide, not a multiply: the inverse reader turns a row pointer back into an index). "
    "Precondition recordStride > 0: no zero test precedes the div.",
    ("AuthoredTableHeader", "0x0C"): TAG + "00306760 + 0x13F and + 0xB4, 00306BD0 + 0x99 - each resolved through "
    "0020E600 and subtracted from a row pointer's low 32 bits; the +0x08 read that follows reloads 02EBF138 separately.",
    ("BattleRuntimeUnitRecord", "0x010"): " || READER ADDED 2026-10-02 (OPUS, from FABLE's review of ASTRA "
    "ov42-effective-id-source): 00387090 + 0x7E, the effective-id getter's 0x9F substitution (taken only when a record "
    "is selected and the owner's +0x714 is 0x9F).",
}

REG_SECTION = """
## The inverse reader: three row-to-index divides over the action table (OPUS, 2026-10-02)

From FABLE's reviews of ASTRA's [`ov42-sequence-queue-source`](../""" + REV + """sequence-queue-source-1002/REVIEW.md)
and [`ov42-kind-row-coherence`](../""" + REV + """kind-row-coherence-1002/REVIEW.md), both ACCEPT-WITH-NARROWING.
- OPUS re-read the six descriptor reads, the divides and the queue store at the bytes
  ([`ov42_check.py`](../_index/candidates/opus-ov42-typestore-1002/ov42_check.py)).
- The classifier's selector values and the return use rest on FABLE's review evidence (`rv_kindrow.py`).

The usual access multiplies an index by the slot `02EBF138` header's `+0x08` stride. Three sites run it backwards:
they turn a row pointer into an index.
- **The sites.** `00306760` + 0x138 .. + 0x158 (the kind-4 arm), `00306760` + 0xAD .. + 0xCD (the kind-3 arm) and
  `00306BD0` + 0x92 .. + 0xB2.
- **The arithmetic.** D = (low32(row) - low32(`0020E600`(header `+0x0C`))) mod 2^32 (a 32-bit `sub`), then an
  UNSIGNED 32-bit `div` by the zero-extended u16 header `+0x08`, with EDX zeroed first.
- **Two descriptor loads.** Each site loads the `02EBF138` QWORD twice, with the lookup call between the loads:
  `+0x0C` comes from the first load and `+0x08` from the second. Equality and stability are not established.
- **Precondition: recordStride > 0.** No zero test sits between the WORD load and the `div`. A zero stride would
  fault (#DE in emulation; a source prediction, not an observed fault).
- **What each site does with the quotient.**
  - Kind 4 at `00306760` narrows the quotient to its low 16 bits. FFFF becomes a queue DWORD FFFFFFFF; anything else
    becomes (w - 0xD0) mod 2^32, stored at `022C2178` (`00306760` + 0x174).
  - Kind 3 passes the full 32-bit quotient on as EDX.
  - `00306BD0` classifies the full 32-bit quotient (`add eax, -0x94`, unsigned `cmp eax, 0x7f`, a 128-byte selector).
    It publishes kind 4 exactly for q 208..225, and kind 7 for every q outside 148..275.
- **Return use at `00306BD0` + 0x86.**
  - The RAX / flags of the callee `0032FC30` are never read: a 16-byte leaf overwrites RAX, and + 0x92 overwrites it
    again.
  - The `0032F6E0` return is tested (+ 0x57).
- **Open, as the register's OV-42 states.** Row-to-kind / caller / owner consistency. A quotient equals an action id
  only for a row on the descriptor's stride grid.
"""

SCR_OLD = ("`GetEffectiveActionId` (`00387090`) and the two\nformula entry points then read `+0x10` instead of `0x9F`, "
           "so preview and resolution agree on the\nsame draw.")
SCR_NEW = ("`GetEffectiveActionId` (`00387090`) and the two\nformula entry points then read `+0x10` instead of `0x9F`, "
           "so preview and resolution agree on the\nsame draw *(qualified 2026-10-02, OPUS: only when the getter "
           "selects a record; when its first owner lookup returns null, it returns `0x9F` itself - see \"The "
           "effective-id getter beside its owner resolver\" below)*.")

SCR_SECTION = """
## The effective-id getter beside its owner resolver (OPUS, 2026-10-02)

From FABLE's review of ASTRA's [`ov42-effective-id-source`](../../""" + REV + """effective-id-source-1002/REVIEW.md)
(ACCEPT-WITH-NARROWING). OPUS re-read both bodies at the bytes
([`ov42_check.py`](../../_index/candidates/opus-ov42-typestore-1002/ov42_check.py)).

- **Owner resolver `BattleStats_FindOwningBattleUnit` (83 B), NULLABLE.**
  - RCX = a stats-record query. A NULL query returns RAX = 0 before any registry call.
  - Otherwise it returns the FIRST registry unit whose QWORD `+0x698` equals the query, as a full 64-bit pointer, or 0.
    "First" is by index order: null entries are skipped, the count is re-read at each step, and the compare is signed.
- **Effective-id getter `00387090` (149 B), OWNER-BACKED.**
  - RCX = the same query. It returns EAX = a zero-extended u16.
  - **Precondition: the second resolver call (O2) is non-null.** There is no NULL guard: a null O2 still reads
    WORD `[0 + 0x714]`.
  - **It makes two separate resolver calls.**
    - O1 is stored to QWORD `02EBF188` (0 included). It selects the `BattleRuntimeUnitRecord`: from the `0208DE80`
      bank by O1 `+0xEA9`, or, when query `+5` is 0, from the `0208D480` bank by query byte `+4`, with no O1 call.
    - O2 supplies `BattleUnit +0x714`.
    - O1 == O2 is not guaranteed.
  - **Result.** O2 `+0x714`, except that `0x9F` with a selected record becomes the record's WORD `+0x10`.
    - The record pointer is 0 only for a null O1, and then the getter returns `0x9F` itself.
    - The byte index is not bounded against the banks' sizes.
"""

EDITS_MD = [(REG, None, REG_SECTION), (SCR, SCR_OLD, SCR_NEW), (SCR, None, SCR_SECTION)]


def tsv(apply):
    p = os.path.join(DB, FIELDS)
    lines = io.open(p, encoding="utf-8", newline="").read().splitlines(keepends=True)
    done = fails = 0
    for (typ, off), add in ROWS.items():
        idx = [i for i, l in enumerate(lines) if l.split("\t")[:2] == [typ, off]]
        if len(idx) != 1:
            print("FAIL row", typ, off, "x%d" % len(idx))
            fails += 1
            continue
        i = idx[0]
        body = lines[i].rstrip("\r\n")
        eol = lines[i][len(body):]
        if add.strip() in body:
            print("SKIP", typ, off)
            continue
        lines[i] = body + add + eol
        done += 1
        print("APPLY" if apply else "WOULD", typ, off)
    if apply and done:
        io.open(p, "w", encoding="utf-8", newline="").write("".join(lines))
    return fails


def md(apply):
    fails = 0
    for page, old, new in EDITS_MD:
        p = os.path.join(DB, page)
        t = io.open(p, encoding="utf-8", newline="").read()
        key = next(l for l in new.strip().splitlines() if l.strip() and (old is None or l not in old))
        if key in t:
            print("SKIP", page)
            continue
        if old is None:
            nt = t.rstrip("\r\n") + "\n" + new
        else:
            o, n = old, new
            if o not in t and o.replace("\n", "\r\n") in t:
                o, n = o.replace("\n", "\r\n"), n.replace("\n", "\r\n")
            if t.count(o) != 1:
                print("FAIL anchor x%d" % t.count(o), page)
                fails += 1
                continue
            nt = t.replace(o, n)
        if apply:
            io.open(p, "w", encoding="utf-8", newline="").write(nt)
        print("APPLY" if apply else "WOULD", page)
    return fails


if __name__ == "__main__":
    a = "--apply" in sys.argv
    print("FAILS %d" % (tsv(a) + md(a)))
