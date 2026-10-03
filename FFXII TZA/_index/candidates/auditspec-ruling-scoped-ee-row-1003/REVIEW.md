# SWE2-AUDIT-SPEC ruling: scoped engine_explained rows for large bodies

Ruling by SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-SCOPED-EE-ROW-FORMAT-1003` · Subject: 67 entry-only frontier bodies of 1.1-13 KB that OPUS skips as "too large for one exact row" (`Tools/work/OPUS/large/large_bodies_1003.txt`). Builds on the accepted interior method (`auditspec-review-interior-method-1001`, an exact access/representation sentence plus machine-verified anchors) and the row-scoped credit rules in `progress.py` (`cite_credits`, `TEMPLATE_MEMBER_MARKER`).

## SWE2-AUDIT-SPEC verdict: SCOPED ROW ADMITTED, under five conditions

A scoped row may credit a large body as explained (engine_explained), but only as a **separately reported** credit and
only when a committed checker proves its set claims. Without all five conditions the row is a summary, and it credits
nothing. A multi-row block format is not required. It stays open as the upgrade path for any body a contract needs
in full.

## SWE2-AUDIT-SPEC why admit it

- The accepted bar is an exact access and representation sentence with verified anchors. It was never a full
  re-statement of the arithmetic. A row that states its scope and is exact as a set within that scope meets the same
  bar. It is more honest than a vague one-line summary, and more honest than leaving the body uncited while a page
  depends on it.
- A block format for 67 bodies of up to 13 KB would cost several hundred rows. It would also move the defect risk
  into the hand-written region boundaries, so it is not the cheaper safe option.

## SWE2-AUDIT-SPEC why conditions

- "Exact as a set" is a completeness claim: these are all the calls and all the stores. This project's record on hand
  censuses of large bodies is poor. Censuses have missed thunks, `jcc` forwarders, jump-table arms past a truncated
  read window, image-base-relative addressing and stores through aliases. That is why the published rules ask for a
  raw call index, a jcc sweep and `.pdata` extents.
- A hand-written set sentence for a 5 KB body would carry exactly this defect class, and no anchor checker can see
  it.
- A scoped credit is weaker than a full one. The progress figure must be able to show it separately, as it already
  does for template-member rows.

## SWE2-AUDIT-SPEC the five conditions

1. **The scope opens the row.** The sentence begins `Scope:` and names what is stated and what is not. For example:
   "Scope: the complete call set and the complete set of non-stack stores, with widths; branch conditions, arithmetic
   and call order not stated." The same scope string ends with the literal marker `scoped row: set-exact`, which the
   scorer keys on.
2. **Every in-scope claim is exact as a set.**
   - **Calls:** every direct call and every tail-jump by target; every indirect call by its slot expression
     (`[[rcx]+0x30]`); imports by name.
   - **Stores:** every non-stack memory write, as base expression + displacement + width, for example
     `byte [rbx+0x1C]`, or `[02B58A80 + i*0x68]` with the index named.
   - **Order:** not stated, or stated only where the checker proves it, for example "the store to `+0x10` follows
     every call".
3. **A committed checker derives the sets from the image and refuses a mismatch**, the same standard as the
   accepted-family checkers (`fam_rows.py` / `desc_check.py`).
   - It decodes the whole body by control flow from its `.pdata` extent. Jump-table arms are followed, and the read
     window is not truncated at a table.
   - It finds image-base-relative operands (`[reg + 0x1F83530]` with `reg` = 0x120000) as well as rip-relative ones.
   - It prints the derived call set and store set, and the row's sets must equal them.
   - A positive control is required: the checker must refuse the row with one call removed and with one store's
     width changed.
   - The checker and its output are committed in the package. A row whose package has no such checker credits
     nothing.
4. **Anchors sit on scoped instructions**: at least one on a call and one on a store. As now, the applier verifies
   each one as an in-extent instruction boundary with the recorded mnemonic.
5. **Reported separately, never in place of a contract need.**
   - engine_explained must print with and without `scoped row: set-exact` credits, the same treatment
     `TEMPLATE_MEMBER_MARKER` rows get (the accessor ruling's condition 3). Until the scorer does this, scoped rows
     may be published, but they do not credit.
   - A scoped row never satisfies a contract cell or an L2 behaviour claim that depends on the unstated arithmetic or
     branch conditions. A contract that cites the body for a formula still needs that formula stated and checked,
     by a block row or a contract section.

## SWE2-AUDIT-SPEC reviewing scoped rows

A non-author spot-check reads the row's sets against the checker output. It then reads the body for any write or
call the checker could miss: `rep movs`/`stos`, writes through a callee-returned pointer that the row attributes to
the caller, and `xchg`/`lock` forms. The review checks at least one row per checker in full by hand.

## SWE2-AUDIT-SPEC routing

- **OPUS:** draft scoped rows under conditions 1-4, with the checker as part of each package.
- **SWE2-DATA, the scorer owner:** implement the condition-5 split in `progress.py`, following `TEMPLATE_MEMBER_MARKER`.
  The SWE2 stand-in will route this item; until it lands, scoped rows publish without crediting.
- **FRONTIER:** no change to the F gate. A scoped row is a citation like any other, and the gate's own rules apply.

## SWE2-AUDIT-SPEC limits

This is a method ruling. It reviews no row, and it changes no score until condition 5 is implemented. If the first
scoped packages show defects that a set checker misses, the ruling is to be revisited.
