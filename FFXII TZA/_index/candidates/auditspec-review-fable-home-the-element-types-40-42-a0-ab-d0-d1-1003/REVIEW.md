# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-element-types-40-42-a0-ab-d0-d1-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-ELEMENT-TYPES-40-42-A0-AB-D0` · Package: `_index/candidates/fable-home-the-element-types-40-42-a0-ab-d0-d1-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 7 sentences are exact, and six rows stand.

`003B6DE0` was not a frontier body. `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` has documented it since `04875b533` (2026-09-16), interior addresses included (lines 669–684). It is a summoner/party-list routine, not part of the effect element types. Remove its row from this page.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 7 functions, 35 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 354, and the rows at lines 360–366 match `rows.json` byte for byte.
- **rows.json.** 7 rows, 35 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Raw references.** Every entered_from site is a direct call:
  - `00376A20`: `004615AE` = `00461270` + 0x33E;
  - `00376A50`: `004615A0` (+0x330);
  - `00377090`: `00461488` (+0x218), and also `004614C6` (+0x256);
  - `00377130`: `00461384` (+0x114);
  - `00377160`: `0046147B` (+0x20B);
  - `003B49E0`: `00464EE2` = `00464BD0` + 0x312;
  - `003B6DE0`: `003B7048` = `003B6F80` + 0xC8, plus `003B6F45` in `003B6F30` and a `jmp` from the 5-byte `003B6F70`.

**Semantic pass, all 7 rows:**

- **`00376A20` and `00376A50` (0x25 B each): exact.** `movzx edx, cl` gives the 0x90 stride through `rdx*9*2*8` from `02ADBB40`. Then `test ecx, ecx` (the full register), `cmp [rec], ecx`, and `movss xmm0, [rec+0x2C]` (`+0x28` respectively). Otherwise `xorps`.
- **`00377090` (0x34 B): exact.** After the same guards: `and dx, 1` / `and word [rec+0x54], 0xFFFB` / `shl dx, 2` / `or word [rec+0x54], dx`.
- **`00377130` and `00377160`: exact.** `movaps xmm0, [rdx]` / `movdqa [rec+0x80]` (`+0x60` respectively). A failed guard writes nothing.
- **`003B49E0` (0x48 B): exact.**
  - `movzx edx, cl` gives `*3 <<5`, a 0x60 stride, added to qword `[02B404E0]`. There is no `ecx != 0` test, and the sentence claims none.
  - `cmp [rec], ecx` / `jne ret`. Then it zeroes `+4`, byte `+0x2E`, `+0x3C` and `+0x34`. `+0x38` = 1.0 (`01CEBBA8`) / `cvtdq2ps(movzx word +0x2A)`.
- **`003B6DE0` (0xED B): exact.**
  - `test edx, edx` / `jns`; a negative count becomes 0, and `cmovg` caps it at 0x20. The count goes to `[02EBCC60]`.
  - Loop one: `02EBCBE0[i]` = `[r8]`, then `003B6E48 call ActorHandle_ResolveRegistryEntryByPackedId` (+0x68). On a hit it does `and byte [rax+9], 0xF7` / `or 4` and stores to `02EBCAC0[i]`.
  - Loop two compacts the pointers on byte `+9` bit 3 and sets the bit.
  - Then `[02EBCC70]` = `ecx`, `[02EBCC68]` = the result of +0xD1 (`003B6EB1`, the same resolver) on `ecx`, and `[02EBCBC0]` = the packed count.

**Host fit:**

- **`00376A20`, `00376A50`, `00377090`, `00377130`, `00377160`.** They fit. Line 67 gives the `0xA1` walk `00461270` (3,820 B), which "calls `001827B0`/`00182830` and the `00376350`–`00377100` helper family". These are members of that `02ADBB40` keyed-record family: `00377130` and `00377160` sit just past the stated range, and the other three lie inside it.
- **`003B49E0`.** It fits. `00464BD0` is the `0x41` colour-filter apply (line 135). It keeps "one record in a 64-slot pool (`02B404E0`, `0x60` bytes)", and this body resets one record of that pool.
- **`003B6DE0`: the defect.**
  - On this page `003B6F80` appears only in the pass-22 ActorEntity neighbour list (line 281) and in OPUS's interior row (line 343). That row describes an actor-record gather ("encodes `rcx` through `ActorHandle_EncodeRegistryEntry` … walks ordinals … `Actor_StopRequestedMovement`").
  - `the-record-behind-every-actor.md` already reads `003B6DE0` in full. Line 669: "`003B6DE0`, the routine `003B6F80` hands its list to. The first loop resolves each handle and **clears bit 3 while setting bit 2** (`and 0xF7` at `003B6E52`, `or 4` at `003B6E56`)…". Line 684: "the summoner `003B6DE0` stores there" (`02EBCC68`). `git log -S` dates that text to `04875b533`, 2026-09-16.
  - So the README's "No page cited these functions" is false for this row. The text sits in an indented block on that page, which a census that skips code blocks would miss; that cause is not verified.
- **Advisory (not a defect).** The same `02ADBB40` family is now split across two pages. Its float reader `003769F0` (the `+8` field) was homed on `effect-element-type-dispatch.md` in `5a7a7f97e`, while these five sit here. A one-line cross-reference in either section would help.
- **Advisory (tool).** The applier's caller test is a substring test that the applied row satisfies by itself. Every caller here is also cited outside the section.

## SWE2-AUDIT-SPEC narrowing

1. **N1.** Delete the `003B6DE0` row (page line 366) from `the-element-types-40-42-a0-ab-d0-d1.md`. It is already documented on `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md`. If an anchored one-line statement is wanted, the sentence is accurate and may be added there instead, entered from `003B6F80` + 0xC8 (that page cites `003B6F80` at lines 655 and 669).
2. Correct the README's row count to 6 and regenerate `homing_applier.out`.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
