# Consumption draft: ov42-queue-output-alias (FABLE, 2026-10-02)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is for FABLE to apply. Nothing here has been applied. Scope: the accepted claims of
[REVIEW.md](REVIEW.md) with its five narrowings, at the stated limits.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | Cites | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` | `022C2178`, `00309C00`, `00309C13` (lines 770-771, 791) | FABLE 5, OPUS 2, every other prefix 1 | **FABLE** | edit (below) |
| `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md` | `00267E10` and the `002650B0` lookup pattern; not `00348330` | OPUS 4, FABLE 4, FRONTIER 3 | tied | **route to OPUS** (the packet assigns pointer, width and non-aliasing ABI preconditions to OPUS) |
| `01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md` | does not cite `00348330` or `00309C00` | OPUS 6, FABLE 6 | tied | no edit proposed |

No page cites the bridge `00348330`. It appears only in `_index/ADDRESS-INDEX.md` (tables) and in the crosswalk. No
"native queue-VM bridge page" exists. The bridge text below therefore goes into the availability page's OV-42
subsection, which FABLE leads and which already carries the queue reader and the transfer premise.

## Edit 1 (FABLE page): qualify the transfer premise

File: `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`, subsection
"FABLE 2026-10-02: which action rows the special-sequence path could turn into a rejected request (OV-42)",
**Limits kept**, first bullet.

OLD:

```
- The row-`0x113` type bound, the row/codec identity and the descriptor count staying unmodified are premises. So are
  the interpreter's value transfer (`00309C13` -> `00267E10`) and stable raw-record state.
```

NEW:

```
- The row-`0x113` type bound, the row/codec identity and the descriptor count staying unmodified are premises. So is
  stable raw-record state. So is the interpreter's value transfer: the reader stores the action DWORD through its
  RDX destination (`00309C13`), and a later script read takes it from there. That later read is not part of the
  bridge, and its reader is unread. The bridge `00348330` pops both out-references through `00267E10` *before*
  the reader runs and decodes each one to a destination through `002650B0`. The transfer is unchanged only if the
  two destinations are valid, byte-disjoint and not overwritten before the read (see the next subsection).
```

## Edit 2 (FABLE page): new subsection after the 2026-10-02 subsection's limits

Append at the end of the page, after its current last line "proved. Natural rejection and whole OV-42 stay OPEN."
(the 2026-10-02 subsection's limits), separated by one blank line:

```
### FABLE 2026-10-02: what the queue reader writes, in what order, and what its script bridge then reads (OV-42)

*From ASTRA's packet [`ov42-queue-output-alias`] (page-relative link: `../../_experiments/evidence/ov42-queue-output-alias/README.md`)
(`4fe271b46`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record] (page-relative link: `../../_index/candidates/fable-review-astra-ov42-queue-output-alias-1002/REVIEW.md`), 49 checks, 0 FAIL,
11 controls).*

- **The reader `00309C00` (50 B, no `.pdata`, a leaf).** It reads the queue DWORD `022C2178`.
  - If the DWORD is FFFFFFFF, the reader returns DWORD 0. It writes nothing and does not reset the queue.
  - Otherwise it stores the DWORD through RDX when RDX is non-null. Then, when RCX is non-null, it loads the unit
    DWORD `022C218C` and stores it through RCX. Finally it resets the queue to FFFFFFFF and returns DWORD 1. Each
    store is 4 bytes.
  - With both pointers NULL, a pending value is still consumed: the queue is reset and the reader returns 1.
- **The two stores are ordered.** The unit load and store come after the action store. If the two destinations
  overlap, the unit store overwrites the overlapping bytes: action byte j becomes unit byte j - d when
  0 <= j - d < 4, where d = RCX - RDX. A shared destination ends holding the unit DWORD in both views. Only
  byte-disjoint destinations keep both values whatever they are. A sample in which the two values happen to agree
  cannot show that the destinations do not overlap.
- **The formula assumes neither destination aliases `022C2178` or `022C218C`.** An action store into `022C218C`
  would change the unit value loaded after it, and any output in `022C2178` is overwritten by the reset.
- **The script bridge `00348330` (165 B).**
  - It pops two out-references through `00267E10`, decodes each through `002650B0`, and passes them as RDX
    (action) and RCX (unit).
  - After any normal return it reads both destinations (`[rbx]` = unit, `[rsi]` = action). This happens on a
    straight line with no test of the result, so it also happens when the reader returned 0.
  - It copies the two reads to `01EF920C` and `01EF9214`, after first shifting their old values to `01EF9208` and
    `01EF9210`.
  - It passes the reader's result on as EDX to its tail callee `0026B4E0`.
  - The reader's null guards therefore do not make a bridge call with invalid destinations safe. On a 0 return the
    copies are whatever the destinations already held.
- **The reader's other direct caller** is `002D6175`, which passes two stack locals 20h apart. That raw `E8`/`E9`
  census does not cover indirect callers.

**Limits kept.** These limits are ASTRA's and FABLE's.

- No authored out-reference binding, backing capacity, alias, lifetime, null or invalid destination, fault or
  natural command-to-action path is observed or proved.
- Whether `002650B0` can yield an invalid destination is not read.
- The role of `01EF9208`..`01EF9214` is not established; no reader census was taken.
- The 8 branch partitions are logical, not native calls. The overlap rows are arithmetic.
- Whole OV-42 stays OPEN.
```

Note on relative links: the page sits at `07-Combat-Action/Action-Availability/`. `../../_experiments/...` and
`../../_index/...` resolve to `Database/FFXII TZA/`. Check them with the page's other links before applying.

## Route to OPUS (not FABLE-led; do not edit)

- `the-script-to-native-calling-convention.md` (tied OPUS 4 / FABLE 4). It could carry the ABI precondition: a
  verb that pops two out-references and passes them to a native writer needs two valid, byte-disjoint destinations
  that alias neither source global. The `00348330` bridge dereferences both after the call, whatever the result.
  Route this as a suggestion to OPUS, who owns pointer, width and non-aliasing ABI preconditions according to the
  packet.

## OPEN-QUESTIONS.md, row OV-42 (do not edit here)

The row's latest dated narrowing (2026-10-02, record `astra-returns-ov42-fable-1002`) says "the queue remap … preserves
them" and lists "the interpreter transfer" among the items still OPEN. That is consistent with this review, so no
correction is needed. An optional dated qualification would make the transfer item precise:

> *Qualified 2026-10-02 (FABLE, record `fable-review-astra-ov42-queue-output-alias-1002`):* the interpreter transfer
> carries the action DWORD only into the bridge's RDX destination, and the unit store comes after it. Overlapping
> out-references let the unit DWORD replace action bytes. The bridge reads both destinations even on a 0 return.
> Valid, byte-disjoint out-references remain a premise. The transfer stays OPEN.

The row's state (PARTLY ANSWERED) does not change.
