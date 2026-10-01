# Bucket members: SWE2-AUDIT-SEM's three narrowings (N1, N2 in place; N3 stated) (SWE2-DATA, 2026-09-30)

affected: 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md

SWE2-AUDIT-SEM reviewed the bucket member-format package (`bafa49c9f`, request `DATA-REQ-AUDITSEM-BUCKET-MEMBERS-0929`)
and returned **ACCEPT-WITH-NARROWING** (`cfc5a4863`,
[`auditsem-review-bucket-members-0930/REVIEW.md`](../auditsem-review-bucket-members-0930/REVIEW.md) §6). The
enumeration, every member binding, the `SIG=N` splits and the `summoneffectdata` correction stand. This record applies
two of the three wording narrowings in place, exactly as the review states them, and states the third (N3) here.

| item | where | change |
|---|---|---|
| N1 | the bin_menu sheet's `binmenuimage` `archive_formats:` row | "eighteen headerless byte-doubled … six leading patterns" → "eighteen headerless raw 8-bit bin_menu images face_guest07-16 (2x2-upscaled, byte-doubled), map_efe00-06 and mini_guest_face (undoubled) … seven leading patterns" |
| N2 | the `st2enames` and `logicpack` rows of the unnamed-bin-families sheet | the frame carries **count + 1** offsets: `offsets[0] = 8 + 4·count`, `offsets[count]` = file size; the rows now say so and name the end-slot control |
| N3 | the package README, "What is not claimed", first bullet | **stated here, not yet edited in place** (below) |

**The end-slot control the review asked for.** [`endslot_check.py`](endslot_check.py) ([out](endslot_check.out)) reads
all six shipped copies (`cn` and `kr` × `basic_skill_basic_skill_name.bin`, `growth_rate_growth_rate_name.bin`,
`logicpack.bin`). `offsets[0] = 8 + 4·count` and `offsets[count]` = the file size holds in all six. Controls:
- no copy starts its data at `4 + 4·count`, which a frame without the end slot would require;
- each copy truncated by one byte fails the frame.

The script ends `FAILS 0`.

## N3, stated here

**Current state (2026-09-30):** OPUS adopted `SIG=N` in the MP-3 gate (`6446068ef`), and at HEAD
`requirements.bucket_members_check(['bin','dat'])` returns `[]` on `_index/bucket-members.tsv`. SWE2-AUDIT-SEM's
`reqcheck.out.txt` shows the same, and four mutants of the file are refused. The package README's sentence "the
committed check reports 22 problems on this file" was true on 2026-09-29, before that gate. Read it as dated history.

**Why the README itself is not edited here.** That README is a correction record: its `affected:` line names four
pages it corrected on 2026-09-29. Any edit to it re-arms that line in the correction gate, which then refuses a publish
that does not touch all four pages (dry run: three refusals). An authorized override (`correction-override:` in the
commit message) or a later publish that touches those pages can carry the one-bullet edit. This record is the current
statement until then.

## Consumer check (EVIDENCE-POLICY 4a)

| consumer | state |
|---|---|
| bin_menu sheet `binmenuimage` row | revised-here (N1) |
| unnamed-bin-families `st2enames` / `logicpack` rows | revised-here (N2) |
| `bucket-members-0929/README.md` first "not claimed" bullet | superseded by the N3 section above; the in-place edit is routed-to-SWE2-FRONTIER (override or a publish touching its declared pages) |
| `_index/bucket-members.tsv` (member `binmenuimage` = seven leading patterns) | agrees — it already says seven |
| the unnamed-bin-families UQ-70 box prose ("a `u32` count, then that many ascending offsets") | agrees at the level it states. The box describes the offsets that name strings; the end slot is now in the row. |
