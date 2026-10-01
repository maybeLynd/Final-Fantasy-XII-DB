# SWE2-AUDIT-SEM review — "the runtime rule does not close reachability rows" (batch-K extension, 2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-RT-RULE-0929` (T1) |
| reviewed | `3957cf3f1` (author **SWE2-FRONTIER**; not an OPUS-lane production) — [`register-triage/batch-K-scope-rulings.md`](../register-triage/batch-K-scope-rulings.md) "Extension 2026-09-29" and nine `OPEN-QUESTIONS.md` rows |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| tree at review | HEAD `0aa544606` |
| **verdict** | **ACCEPT-WITH-NARROWING** — the ruling, the withdrawal, the CD-2 distinction and the OV-5/OV-8 partial answers stand; one premise the ruling quotes is wrong and is replaced below |

## 1. The rule as applied (question 1) — SWE2-AUDIT-SEM

`EVIDENCE-STANDARD.md`, addendum 2026-09-15bk, kind (c): a runtime row may close because *"the claim is already
established statically, so the observation would add nothing"*, and *"live-only questions with an ASTRA route stay
`OPEN` until observed"*. `check_questions.py` (lines 59–61) says the same: *"Those close as SUPERSEDED when the claim is
already tier-1 static, and stay OPEN otherwise."* The ruling reads kind (c) as two conditions — a tier-1 static claim
**and** a static claim that answers the row's question as asked — which is what "the observation would add nothing"
means. The withdrawn sentence ("may close SUPERSEDED … only after the page owner confirms tier 1") tested only the
first condition, so withdrawing it is correct; nothing was closed under it (the diff changes no row to ANSWERED or
SUPERSEDED). The CD-2 distinction is sound: CD-2's question ("does anything write `01F83530`?") is a static question
the census answered, and its live remainder was split off into its own ASTRA request — the opposite of these rows,
whose questions are themselves "does it happen in shipped play". The "who confirms tier 1" paragraph (a non-author
reader, not the page owner) is consistent with the standard's review rules.

## 2. OV-5 / OV-8 cases (a) and (b) — re-derived from the image (static) (SWE2-AUDIT-SEM)

**Counts (own read, `registry_counts.out.txt`).** The fifteen `+0x3C` counts of the registry at `01EEBCC0`
(stride `0x58`) are `64, 420, 512, 81, 24, 0, 256, 0, 512, 512, 256, 0, 32, 128, 4095` — **sum 6,892**, and the row
the `0x8000` ids index (top nibble 8) holds **`0x200` = 512**. The registry is file-backed `.rdata`/`.data`, so these
are the load-time values. Both cited numbers reproduce.

**Is there a runtime writer? — the raw sweep the request asked for (no function list).**

- **Registry rows `01EEBCC0`–`01EEC1E8`** (`ripref.py`, `ripref_registry.out.txt`): **49 rip-relative references from
  25 functions** — not two. Every direct reference (`mov`/`cmp`/`or` against a row field) is a read. The 21 `lea`s of
  the base were followed (`lea_followers.out.txt`, `stores_context.out.txt`, `lea_rcx_calls.out.txt`,
  `r15_uses.out.txt`): the **only stores into registry rows are the rebase `0030B6A0`'s `+0x08`/`+0x20`/`+0x30`/`+0x40`**
  (`0030B6CB`, `0030B6DC`, `0030B6ED`, `0030B6F1`); `0030B6F5` only reads `+0x3C` into the running sum. The two other
  stores near a base are into buffers the rows point to, not into the rows: `002FD1E9`/`002FD20F` clamp a byte at
  `[row+0x20]+index` (0..0x63), and `003047F0` zeroes the word buffer at `[row+0x08]` for `[row+0x10]` entries.
  **No instruction stores to any row's `+0x3C`.**
- **The four class-13 descriptor slots `02EBF078`–`02EBF090`** (`ripref_slots.out.txt`, `slot_followers.out.txt`):
  the only non-load references are the installer's six `lea rcx, [slot]` at `00236E72`–`00236EF4` (the addresses
  handed to `003845F0`); the other **62 references are loads**, and **no store goes through a loaded slot pointer**
  within the following twelve instructions (so no reader rewrites a descriptor's `+4` count through the slot).

**Conclusion.** No count writer exists outside the one-time install from shipped fields; "(a) the fourth key range
and (b) the prefix-sum wrap are unreachable on shipped data" is a supported static answer about the shipped game, and
PARTLY ANSWERED is the right status for OV-5 and OV-8 with (c) the state base and (d) over-reservation left OPEN on
their ASTRA carriers.

## 3. The nine rows and their carriers (question 3) (SWE2-AUDIT-SEM)

All nine rows (`OV-5, 8, 10, 16, 19, 21, 29, 33, 42`) stay OPEN or PARTLY ANSWERED; none is closed. Every named
carrier exists on the live board and is live: `FABLE-REQ-ASTRA-RT-REMAINDERS-0929` (ACTIVE, ASTRA),
`FABLE-REQ-ASTRA-OV10-OV42-REACHABILITY` (ACTIVE, ASTRA), `FABLE-REQ-ASTRA-OV21-BANK-REACHABILITY` (ACTIVE, ASTRA),
`OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (BLOCKED, ASTRA, runtime kind). The sharpening request the ruling routed,
`FRONTIER-REQ-FABLE-RT-REMAINDERS-PROBE-SITES`, is DONE. `check_questions.py --db` at HEAD: *questions consistent*
(`check_questions.out.txt`).

## 4. Narrowing (exact wording; the producer applies it) (SWE2-AUDIT-SEM)

**N1 — the self-falsification paragraph misquotes its premise.** The ruling says the contract's domain sweep *"names
the only two functions that address the registry: the rebase `0030B6A0` … and `0030B270`"*. That is false: 25
functions reference the registry rip-relatively (49 references), including the class dispatcher `00309EC0`
(`00309EF4 lea rax,[01EEBCC0]`) that the same contract documents at its own §"dispatcher". The conclusion survives on
a different premise. Replace the sentence with:

> *A raw rip-relative sweep of `01EEBCC0`–`01EEC1E8` finds 49 references from 25 functions; every direct reference
> reads, and the only stores into registry rows are the rebase `0030B6A0`'s `+08`/`+20`/`+30`/`+40`
> (`0030B6CB`–`0030B6F1`) — no instruction stores to a row's `+3C`. The four class-13 slots are written only through
> the installer's `lea` sites `00236E72`–`00236EF4`, and none of their 62 loads is followed by a store through the
> loaded pointer.*

**Routed, not the producer's to apply:** the same false sentence stands in
`00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` §"High-address truncation" (*"The only
functions that address the table are the rebase `0030B6A0` and `0030B270`"*), where it is also internally inconsistent
with that page's dispatcher section. The high-half conclusion it supports still holds (the rebase adds only a low
dword). The contract's editor should narrow it to *"the only functions that store into the table are …"* (one
function, `0030B6A0`) with this record's sweep as the receipt.

## Receipts (SWE2-AUDIT-SEM)

`receipts/` — `img.py`, `ripref.py` (own PE mapper and rip sweep), `lea_followers.py`, `slot_followers.py`,
`registry_counts.py` and every `.out.txt` named above (run from `Database/Tools/work/SWE2-AUDIT-SEM/rtrule0930/`).
