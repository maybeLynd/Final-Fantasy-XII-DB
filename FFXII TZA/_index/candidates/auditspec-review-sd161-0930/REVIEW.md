# SWE2-AUDIT-SPEC review of achievement counter 11's writers (OPUS, b7689491e + 1e9e5c1ba): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
[sd161-counter11-writers-0930](../sd161-counter11-writers-0930/README.md) at b7689491e and the correction 1e9e5c1ba
(the README as it stands at HEAD), measured at HEAD 17a959c94 (the first worker's checker re-run was at HEAD
3cae47364; the package is unchanged between them). Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD161-0930 | `_index/candidates/sd161-counter11-writers-0930/` | `b7689491e`, `1e9e5c1ba` | ACCEPT-WITH-NARROWING |

**Re-run.**
- `sd161_check.py` -> [rerun_sd161_check.out](rerun_sd161_check.out): identical to the committed `.out` (ignoring
  CR), Z1-Z6 PASS, `FAILS 0`. Z1 only parses the committed census output.
- The census itself, re-run once (1,302 s) with the checker header's command, output sent here
  ([rerun_sd161_objflow.out](rerun_sd161_objflow.out); the 1.5 MB `rerun_sd161_objflow.tsv` is for the coordinator to
  drop, not publish). The `.out` is identical to the committed one apart from the timing figures, and the `.tsv` is
  byte-identical (ignoring CR): 1115 root functions, `REGION` 4, `INDEXED-BELOW` 202, `INDEXED-UNKNOWN` 163, and
  "369 in 41 functions" that can reach the field.
- `objflow.py --base` diff (b7689491e): `STATE_ABS = base if given else IMG_LO`, and the getter split is now
  `split(":", 1)`, so a negative K parses. That is the whole change.
- Package dir after the re-runs: `git status --porcelain` shows only the two files that were untracked before
  this review (`consumer-check.md`, `sd161_objflow.tsv`). They are the author's, not mine. Neither is committed:
  `consumer-check.md` is the correction's consumer record, and the `.tsv` is by design not published.

**Re-derived independently** ([sd161_indep.py](sd161_indep.py) / [sd161_indep.out](sd161_indep.out); whole-function
decoder [lin.py](lin.py); dumps `dump_*.out`).
- **The field.** `020927C0` has 32 rip-relative references. The only store is `00253990`, which writes
  `002EF640()` + 0x8200, and `002EF640` is `lea rax, [02164280]`. So the record is `0216C480` and the field is
  `0216FCDC` = image `+0xBA5C` ([dump_a.out](dump_a.out)).
- **No direct reference to the field.** The window `0216FCC0..0216FCF0` has no rip-relative reference, no
  image-base-relative displacement, and no abs64 or rva32 cell anywhere in the file.
- **Who forms the image's address.** Only 4 rip-relative `lea`s, at `002EF57C`, `002EF5F6`, `002EF640` and
  `002EF656`, plus the pointer cells `020927C0` and `02092758` (the census follows both). `002EF57C` copies the image
  out to `022676C0`; it does not write the image.
- **Z1-Z3 hold.**
  - `002EF5F0` and `002EF650` are `memset(02164280, 0, 0x56690)`, and `002EF650` then calls `00253A80`.
  - `00253A80` is `memset([02092758], 0, 0x58)` and then `memset([020927C0], 0, 0x4818)`. The second one covers
    `+0x385C`.
- **Z6 holds.**
  - `002EF4A0` copies `02166480` -> `021B290C`, 0xC0 x 0x80 bytes (image `+0x4E68C` onward).
  - `00229B40`'s first loop copies image `+0x4E68C` -> `+0x2200`, 0x6000 bytes, ending at `+0x8200`.
- **The correction's load writers.**
  - `00583C00` copies `[[02CA99B8]+0x588]` to `002EF640()`, 0x1C4 x 0x80 + 0x40 = 0xE240 bytes
    ([dump_583c00.out](dump_583c00.out)). That covers image `+0xBA5C`. Confirmed.
  - The call chain `003BA7B0` -> `00862590` (called at `003BA882`, `003BA8AE`, `003BABB0`) -> `00866A00` (called at
    `008625A4`) exists. Its destination was not traced here, and the README says the same.
- **The census's own "can reach" list** (committed `sd161_objflow.out`: `stores that can reach [0x385c, 0x3860): 369
  in 41 functions`; 4 REGION, the rest INDEXED-BELOW or INDEXED-UNKNOWN). I read the functions to bound them:
  - **Cannot reach the field.**
    - `00252610` / `002527B0`: indices clamped to 0..0x64 or 0..0x1F.
    - The bit and flag helpers `00315820`, `00315910`, `00315A20`, `00315A90`, `00315B50`, `00315CD0`,
      `00315E90`, `00316930` and `00316A50`. Their range checks cap them at `+0x3603`, `+0x3349`, `+0x336B`,
      `+0x33EB`, `+0x33F9`, `+0x3803` and `+0x3847`–`+0x384B`. `00315910` / `00315B50` use the word tables at `00D10630` / `00D10640`;
      their largest bit is 0x1EF.
    - `0032AB60`..`0032ADF0`: range checks, based at image `+0x200`.
    - `003C5E50`, `003C60F0` and `003C8670` go through `002551B0`, whose index is <= 0x180, so they end at
      `+0x3244`.
    - `00229B40`, `002EF4A0` and `005844A0` are fixed-extent copies ending at image `+0x8200`, or starting at
      `+0x4E68C` or higher. `005844A0` also clears from `+0xE240`.
    - `00583D60` writes image `+0x20..+0x44`.
    - `003266C0`, `0030B180` and `003279B0` are based at `[02EBF190]` = image `+0x4E68C` (written by `00238A80` and
      `00233C10`) plus non-negative offsets. `0030B6A0` writes `rcx + 0x57C8` onward, and its only two callers
      (`00233C3A`, `00238A99`) pass that same image `+0x4E68C`.
  - **Reaches the field:** `00583C00`, the backup restore. The census listed it: 12 INDEXED-UNKNOWN rows, `.out`
    line 316 onward.
  - **Not bounded inside the function** (the index comes from the caller):
    - `00315AD0`'s kind-6 entry: bit set/clear at `+0x3604 + edx`, which reaches at edx 0x258..0x25B. Its caller
      `00577638` bounds edx by a data word, `[r14+8]`.
    - `00252D40` and `00254E00`: u16 bit indices into `+0x3244` / `+0x32C4`, which reach at bits 12480..12511 and
      11456..11487.
    - `0046B290`, `0046B350`, `0046B3F0` and `0046B490`: signed indices from image `+0x200`, which reach only at
      byte offsets of about 0xA800 or more.
    - `003112F0`: copies only values that are non-negative at their own width, to `r8 + [0xBC, 0x17C)`, with r8
      from 7 callers.

**Controls.** Defect: a direct rip or image-base-relative writer of the field that the census missed. The same scans
return known positives: the 32 references to `020927C0` (the census also counts 32), and the image-base-relative
table reads at `00D10640` and handle writes at `02EA9510` ([control_ibrel.out](control_ibrel.out)). Defect: a writer
that the census listed and the README left out. Control: the census's own reach list, bounded function by function
above. It turned up `00583C00`, the backup restore.

**Citations checked.** Z1-Z6 addresses match the bytes. The correction's `CONTRACT-storage-read-completion.md`
§5 gives `0x1C4 x 0x80 + 0x40 = 0xE240`, which matches `00583C00`.

**Defects (wording, not measurement).**
1. The correction gives the wrong reason for the miss. It says the census "did not see" the load writers "because it
   follows the record pointer and they write through a destination pointer". The census did see `00583C00`: it is
   in the reach list as INDEXED-UNKNOWN, through the getter `002EF640`. The original limit ("No function in the
   census copies a saved file back into the image") was already contradicted by the census's own output.
2. The headline overreaches: "every writer this census and AB-8 find stores 0 or a non-negative value". The census
   finds 369 stores in 41 functions that can reach the field. Only the 4 REGION rows were classified.
3. The Limits bullet names only the 202 INDEXED-BELOW stores. It does not mention the 163 INDEXED-UNKNOWN ones.

**Runtime routing.** None proposed. What the caller-bounded indices above take at run time is a static question
about their callers, not a live one.

**Correction wording.**
- Replace "**So every writer this census and AB-8 find stores 0 or a non-negative value.** On a new game the check
  passes the first time it runs." with: "**Every store this census places at a known offset on the field is a
  memset to 0, and AB-8's accessor writers store only non-negative values.** So a new game starts counter 11 at 0.
  The census's other 365 stores that can reach the field were bounded by SWE2-AUDIT-SPEC (review 2026-09-30). All
  cannot reach it except three groups: the backup restore `00583C00`, which copies the backup's bytes over image
  `[0, 0xE240)`; the bit helpers `00315AD0`, `00252D40` and `00254E00` and the `0046B290`–`0046B490` family, whose
  index is bounded only by their callers; and `003112F0`, which stores only values that are non-negative at their
  width. Until those callers are bounded, the first evaluation passes unless one of them sets the field's sign bit
  first."
- In the correction, replace "this census did not see them, because it follows the record pointer and they write
  through a destination pointer" with: "the census listed `00583C00` (INDEXED-UNKNOWN, reached through the getter
  `002EF640`) but the record did not classify it; the storage-read chain writes through a destination pointer the
  census does not follow".
- In the last Limit, replace "It reports its `INDEXED-BELOW` stores (202, …)" with "It reports 202 `INDEXED-BELOW`
  and 163 `INDEXED-UNKNOWN` stores that can reach the field (bounded in the SWE2-AUDIT-SPEC review, 2026-09-30)".
