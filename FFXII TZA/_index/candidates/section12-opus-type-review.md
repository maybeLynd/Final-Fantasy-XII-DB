# SECTION-12 (Update12) — OPUS review of the type-store claims

OPUS, 2026-09-24. **Scope: the layout claims SECTION-12 makes in `_types/` — widths, offsets,
names of the two re-declared `ActorWaitSlot` spans.** The seven other row changes (meanings of
`ActorResourceEntry` +0x02/+0x0C/+0x10 and `ActorWaitSlot` +0x00/+0x14/+0x16/+0x27) are semantic
refinements of wait/notification behaviour and are routed to FABLE and SWE2-AUDIT-SEM; nothing
here reviews them. Evidence class: **NATIVE/STATIC**, shipping image `73461D08…21F8`. The
section's own evidence (a Linux fixture running original bodies on synthetic actors) was **not
replayed**; this is an independent second instrument, not a re-run.

## Verdict: ACCEPT, statically corroborated, at the scope the section states

| row | section claims | static finding |
|---|---|---|
| `ActorWaitSlot +0x1C` `waitListRef` `uint32` | kinds 5/7: encoded list reference, read by `002674B0`/`00267420` from descriptor+4, resolved by `0020E600`; list = dword count + four-byte actor/ID pairs; ID ignored for the channel wait | Every call to both helpers passes `lea rdx, [rsi + 0x18]` with `rsi` the wait slot (`0025E00A`, `0025E083` in `0025DF00`; `00261B79`, `00261C76`, `00261D0B` in `0025E4C0`). Both helpers read `mov ecx, dword ptr [rdx + 4]` (= slot +0x1C, **4 bytes**) and `call 0020E600`; the result's `[rax]` bounds the loop and entries are read at `[list + i*4 + 4]` (actor word). `002674B0` also reads `[list + i*4 + 6]` (ID word); `00267420` does not, and instead compares the actor against `byte [rdx + 0xE]` (slot +0x26). |
| `ActorWaitSlot +0x22` `waitListCursor` `uint16` | kinds 5/7: retained forward cursor, incremented past satisfied entries, stops at the first active one, later polls start there | Both helpers load `movzx edx, word ptr [rdx + 0xA]` (= slot +0x22, **2 bytes**), and on an inactive entry execute `inc word ptr [rbx + 0xA]` and loop; on an active entry they return 1 **without** incrementing. Neither helper resets it. The only writes outside the helpers are the interpreter's arm sequences `mov dword ptr [rsi + 0x1c], eax` / `mov word ptr [rsi + 0x22], cx` immediately before the first poll (`00261B5E/61`, `00261C5B/5E`, `00261D04/07`; `cx` zeroed at `00261D02`). |
| kind scoping | kinds 5 and 7 | `0025DF00` dispatches on `byte [rsi + 0x14]` through the table at image `0x0025E3CC`: **kind 5 → `0025E00A` → `002674B0`**, **kind 7 → `0025E083` → `00267420`**; kinds 0-4 and 6 go elsewhere. |

**Width and offset are PROVEN from the access instructions; the names are supported by control
flow, not only by the fixture.** "Other command-scratch uses overlap these bytes" is consistent
with SECTION-11's `+0x18` command-scratch reading and is not contradicted here; it is not
independently established either (no census of other kinds' writers to +0x1C/+0x22 was run).

## Not reviewed, and routed

- The seven semantic row refinements and every wait/notification behaviour claim (A12-1..A12-10
  in `claim_matrix.tsv`) — FABLE (semantic mechanism owner) and SWE2-AUDIT-SEM (auditor).
- Whole-type readiness: the section itself declines a promotion; so does this review.
- SECTION-11's `ActorWaitSlot` note (head +00 qword PC, +08 target ordinal, +10 accumulator, +18
  scratch for the execution kind) — overlays the same record and needs its own review.
