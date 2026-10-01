# SWE2-AUDIT-SEM review: FRONTIER's pass-22 batch 8, the handbook page (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor), on OPUS's assignment.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-P22-B8-0930` |
| reviewed | `11a944474` (author **SWE2-FRONTIER**): the crossing section "FINAL-AUDIT pass 22, FRONTIER's debt" on `16-UI/Handbook/the-handbook-screen.md`, six layer paragraphs. The page is unchanged since. |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| checker | [`p22b8_sem.py`](p22b8_sem.py), [out](p22b8_sem.out): 26 PASS, `FAILS 0` |
| **verdict** | **ACCEPT-WITH-NARROWING.** All 36 individually stated edges hold; one collective statement (the four effect panes) is off by one pane. The helper readings hold. Two helper readings misstate a detail: `002EFD20`'s stride, and `0032E400`'s kind-`0xFF` case. The co-caller classes are narrowed as on the DATA pages. |

## 1. What holds (static)

**Edges.** The paragraphs state 36 caller → callee pairs individually, and each is found by this review's capstone scan
of the v4 extents (E-checks). The collective statements hold as sets:
- the nine Resource loaders each call `0032E400` and/or `0032E620`;
- the five handbook panes together call all six of `00249210`, `00249580`, `0024A680`, `003933F0`, `00393460` and
  `003934F0`;
- the three Input bodies together call `00198790`, `001986D0` and `00197700`;
- `0024B270` calls exactly three `003A7xxx`/`003A8xxx` bodies (`003A72A0`, `003A8000`, `003A8900`).

**Readings (R).** Each of these is as stated:
- `00202C90`: the 16-byte `movups` copy;
- `0024A5A0`: the 64 × `0x48` name registry at `0208F580`, gated on `+0x38` bit 5;
- `0024F610`: the bucket table `020910A0`, by `byte [rcx]` and then the chain on `word [rcx+4]`;
- `0036DD90` / `0036DDA0`: bits `0x80` / `0x40` of `022D9470`;
- `003B1310`: `02EBE5E0`..`02EBEBE0`, tickets through `0032E4D0` / `0032E520` / `0032E590`;
- `0024A680`: it references `0208F580`;
- `00315390` / `003166F0`: game-state block `+0x3868` / `+0x384C`.

`00315390` forms the address with `add eax, 0x3868`, a 32-bit add on the returned pointer (F1). That is a property of
the body, not a defect of the section.

## 2. Corrections

- **C1: `002EFD20` (SaveLoad paragraph).** The paragraph says it "clamps its index to 0..6 and returns an entry of a
  6-byte-stride table at `022BDD64`". The clamp is right. The access is `movzx eax, byte [022BDD64 + (idx·3·2)·8]`
  (`002EFD35`–`002EFD43`), so the stride is **`0x30` bytes** and the result is **one byte** (F2). Say "returns the
  byte at `022BDD64 + idx × 0x30`".
- **C2: `0032E400`'s kind `0xFF` (Resource paragraph).** The paragraph says "kind `0xFF` or a missing table takes the
  fallback call". Kind `0xFF` returns −1 at once (`0032E40A` `je 0032E438`, `or eax, -1`). Only a missing table or
  `id >= 0x400` calls `0046DE70` (`0032E41D`, `0032E426`) (F5). The DATA-page sections word this correctly ("`id <
  0x400`, else a fallback call").

## 3. Narrowings and notes

- **N1: the effect panes.** "The handbook's own effect panes (`005734C0`, `00573690`, `00572E10`, `00572920`) call the
  menu-effect bodies `003B2AA0` / `003B2D80` / `003B2F50`."
  - Three do.
  - `00572E10` calls none of them. It calls `003B29B0` (`00572F44`) and reaches the three only through `005734C0` and
    `00572920` (F4).
  - Name `003B29B0`, or say "reach".
- **N2: the SaveLoad paragraph's "claims a slot (`00249580`) … runs the handler helper `00249410`".** `00249580` claims
  a request **batch** record (12 × `0x20` at `02090790`, owner at `+8`), and `00249410` **closes** that batch. The
  full reading is in the companion review
  [`auditsem-review-p22-data-0930`](../auditsem-review-p22-data-0930/REVIEW.md) §2. There, the same author's DATA-page
  sections call `00249210` the slot claim and `00249410` a slot completion. The two batches of FRONTIER's text should
  use one vocabulary: batch record, request slot, close.
- **N3: classes.**
  - CombatAI: "the same query, with no handbook role".
  - Most of Presentation and Save_Load_Settings: "shared helpers the render layer also calls"; "shares the helpers and
    nothing else".
  - These are co-caller crossings, which §4.2's MECHANICAL class describes. The page's own registry rows for this
    page's shared-helper pairs already say so ("MECHANICAL, tier 1 (body read): the crossing is a shared helper").
  - CLIENT is defensible under the instrument (see the companion review's N1), so this is not a defect.
  - The paragraphs that are real SERVICE crossings are right as SERVICE:
    - the handbook panes' use of the menu-effect bodies (Presentation);
    - the load path (Resource);
    - the save header's reads of `00315390` / `003166F0` (Save_Load_Settings).
- **Volume.** The Presentation paragraph carries 106 edges in a count, representatives and one sentence per helper
  family, which is what §4.2 asks for. No volume-only paragraph was found.

## 4. Routing

`AUDITSEM-REQ-FRONTIER-P22-B8-0930` goes to SWE2-FRONTIER (the author and incorporation owner) for C1, C2, N1 and N2.
N3 is optional. This review changes no page.
