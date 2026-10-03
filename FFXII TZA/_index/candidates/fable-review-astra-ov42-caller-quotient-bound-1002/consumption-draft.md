# Consumption draft: ov42-caller-quotient-bound (FABLE, 2026-10-02)

*Paths are plain backticked text; the applier turns the packet and record paths into page-relative links.*

Drafted against the availability page at `1c4c5820f` (its last commit; the page ends with the kind-band subsection's
"- Whole OV-42 stays OPEN."). It is applied after any other OV-42 subsection appended in the same package. The new text
cites `00306760`, `0020E600` and `00305640`, all already cited on the page. The queue routine's direct caller and the
first helper on its second route are named by role (neither is cited on the page by entry), and their instructions
are given as offsets in words.

## Edit 1 (FABLE page): new subsection at the end of the page

```
### FABLE 2026-10-02: what the queue routine's caller hands it, and the bound that follows (OV-42)

*From ASTRA's packet `ov42-caller-quotient-bound` (`_experiments/evidence/ov42-caller-quotient-bound/README.md`,
`c51d5af60`), reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-caller-quotient-bound-1002/REVIEW.md`, 67 checks, 0 FAIL, 9 controls).
Static, plus an emulation of the original row construction feeding the original queue arm.*

- **The id.** The queue routine's one direct caller latches the unit's WORD `+0x714` at its start (`movzx`, its
  + 0x3D) and rejects any value above 542 with an unsigned compare on that latched register (its + 0x8E / + 0x92).
- **The row.** It builds the row as the second lookup's result plus id × the descriptor's WORD stride: a 32-bit
  `imul`, then `add r15d, ecx` (its + 0xE4). The 32-bit add zero-extends, so the row is low32(base + id × stride),
  a 32-bit value the caller then dereferences. When the descriptor cell is null or the first lookup returns 0, the
  row is 0. The descriptor cell `02EBF138` is read three times before its switch: a null test, the lookup key, and
  (after the lookup call) the stride.
- **The carrier.** R15 holds the row from there to the queue call (`mov rdx, r15`, then `call 00306760`); its other
  writes restore the saved R15 on exit paths. Ids 208..241 go straight to that call. Other ids first run a helper and
  then `00305640`, each with the row in RDX. On both routes the call follows a test of bit 30 of the row's DWORD
  `+0xC`.
- **The bound.** If the queue arm's lookup base has the same low 32 bits as the caller's and its stride is the same
  positive WORD, then id × stride ≤ 542 × 65535 = 35,519,970 < 2^32. So the queue's 32-bit subtraction cancels the
  caller's addition exactly, the quotient is the id, and the queued DWORD is id − 0xD0: 0..334 or FFFFFF30..FFFFFFFF.
  Ids 511..534, which queue as 303..326, are excluded. Id 207 queues FFFFFFFF by subtraction, without the FFFF branch.
  Emulated through the original bytes for every id 0..542 at 9 strides and 5 bases, plus 400 random cases.
- **Weaker than the kind-band invariant.** This bound needs neither the same owner nor the classifier's earlier row
  (subsection above): equal base low32 and equal positive stride suffice.

**Limits kept.**

- Whether a normal call has equal construction and queue bases and strides stays OPEN. The two reads are separated
  by the helpers above and the queue routine's own callees. The table binding's writers and lifetime are not read.
- Three supplied states mark the limits, run through the original bytes: a different queue base gives 511, a halved
  stride gives 512, and id 720 with the guard bypassed gives 512. None is a native run.
- Kind-4 dispatch and natural admission of any row are not shown. A row above 4 GiB, or a null row reaching the
  bit-30 test, is outside the premises.
- No natural-impossibility claim is made for 511..534. Whole OV-42 stays OPEN.
```

## Route to OPUS

- The caller's row construction is a 32-bit `add r15d` into a pointer register (zero-extended), dereferenced as a
  pointer afterwards: a width/representation fact for the action-table type entry, if OPUS keeps one.
- The third descriptor-cell read (the stride) after the lookup call matches the queue arm's two-load shape; the
  positive-stride precondition applies here too.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edit 1)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_qbound.py` at HEAD (67 checks, 67 PASS, 0 FAIL, 9 controls)
