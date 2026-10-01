# SWE2-AUDIT-SPEC review of SD-62: ORACLE's list-link record (dedfaf0d7) ACCEPT-WITH-NARROWING; OPUS's F3 adjudication (5a6b2eed3) ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Work began at
HEAD `9b6c5bc93` (parked) and was resumed and finished at HEAD `48de14c6b`; no commit between them touches the reviewed
directories. Static, certified image (sha256 asserted by the lane loader `ov31_indep.py`). The record has two parts,
one per request. Each part has its own verdict.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-SD62-0930 | sd62-registry-list-links-0930 | `dedfaf0d7` | ACCEPT-WITH-NARROWING |
| OPUS-REQ-AUDITSPEC-SD62-ORACLE-0930 | opus-sd62-f3-adjudication-0930 (+ the F3 correction in sd62-static-array-elements-0930) | `5a6b2eed3` | ACCEPT |

Shared evidence: [sd62o_indep.py](sd62o_indep.py) / [.out](sd62o_indep.out) (A-D),
[sd62o_c1.py](sd62o_c1.py) / [.out](sd62o_c1.out), [sd62o_dump.py](sd62o_dump.py) / [sd62o_dump.out](sd62o_dump.out).
By-hand reads were made with the lane disassembler `../auditspec-review-opus-batch8-0929/b8dis.py` and saved to
[sd62o_b8dis.out](sd62o_b8dis.out). They cover `00632D80`, `006388F0`, `006363B3`, `00637A70`, `008AF490`, `00638C90`,
`00635B80` and `006391FF`.

---

## Part 1 - ORACLE-REQ-AUDITSPEC-SD62-0930 (SWE2-ORACLE, `dedfaf0d7`): ACCEPT-WITH-NARROWING

**Re-run.** [rerun_sd62_registry_lists.out](rerun_sd62_registry_lists.out) is identical to the committed `.out`
(CR ignored). L1-L8 and C1 PASS, `FAILS 0`. I re-ran it again at `48de14c6b`: still identical. Package dir clean after
the re-runs: yes (`git status --porcelain --ignored` on it is empty).

**Re-derived independently.**
- **L1 writer and owner.** `00639160` has 12 rel32 callers in the census (A), with 0 jcc and 0 abs64. Its 3 rva32 hits
  are its own `.pdata` chunks. The owner passed at every site is the descriptor's own `+0x70`:
  - 10 sites load the rip cell that equals descriptor + 0x70;
  - `00636280` stores `006363D4 mov [rbx+0x70], rbp` right before `mov rcx, rbp; call 00639160`;
  - `00639450` passes `rcx = [rcx+0x70]` (`0063945C`). That function has 471 rel32 callers.
- **Splice order (defect in L1 prose).** On the no-base path (D, `0063922E`-`00639244`), the new node becomes
  `[head+0]`, and the old first node becomes its `[node+0]`. That is a **front** insert. The walkers start at
  `[01F2E340]` and step by `[node+0]`: `008AF49A` / `008AF4C0`, `00637AAA` / `00637B45`, and `00638D00`. So the newest
  descriptor is the first one visited. It is not "the tail". The base path (`00639212`-`00639229`) puts the node at
  base-node's `+0`, "right after the base's node", as written. By contrast, `00635B80`'s `+0x90` link really is a tail
  insert (`00635BE9`-`00635C0F`).
- **L2.** I opened `008AF490` (node − 0x50, `vt+0x38` gated on `+0xFC` bit 0), `00637A70` (the `+0x78` base-chain sum
  into `+0xF4` / `+0xF8`) and `00638C90`. Each supports its row.
- **L3 (defect in wording).** The link into root `+0x28` is as stated (`0063924C`-`00639277`, root skipped at
  `0063925B`). But "00638C90 unlinks it again" is not shown:
  - `00638C90` walks only root `+0x10`, and takes `rbx = [descriptor+0x70]` at `00638D22`;
  - by the owner finding above, every descriptor on that list has `+0x70` = root when it is linked;
  - so the owner-unlink arm `00638D78`-`00638D89` is guarded by `00638D6B cmp rbx, rbp` (rbp = root), and it is not
    reached for a descriptor that was linked there, unless something rewrites `+0x70` later. I did not look for such a
    rewrite.

  No unlinker of non-root owners from root `+0x28` is shown.
- **L4.** There are 156 rip refs into the root, in 15 functions, and 30 rip stores to `+0x00` / `+0x08`, in 13 functions.
  All 30 store the root's own address:
  - 26 pass the function-wide `lea` test;
  - I read the other 4 by hand (`00637BF7` / `00637C05`, `0063C8B9` / `0063C8C7`). Each comes right after
    `lea rax, 01F2E330`.

  There are 0 image-base-relative refs. The only abs64 refs are the root's own self slots.
- **L5 / L6 / L7 / L8.** I confirm these independently. The details are in Part 2, plus:
  - the constructor `00632D80` self-links `+0x50` / `+0x58` (`00632D83`-`00632D8A`) and does no list insert;
  - `006388C0` hashes with seed `0x7B5` and loop `and ecx,0x1f; imul edx,edx,0x21; add edx,ecx` (`006388FA`-`00638932`),
    which is h = h×33 + (c & 0x1F);
  - `00636280` repeats the same loop at `00636390`-`006363B1`, then looks up the old node (`006363BF call 006311D0`)
    and removes it (`006363CC call 00638F00`).
- **Extent of `01F2E7B0` (defect in wording).** `00635B80` also writes `01F2E7D8` (record `+0x28`) := `01F2E7E0`, and
  `01F2E7E0` / `01F2E7E8` := `00D59070` / `0063BEF0`. These writes are at `00635C2F`-`00635C52`, after the guard, so they
  run on every path. "About 0x28 bytes" is therefore too small. It is at least 0x30 bytes. Whether the pair at
  `01F2E7E0` belongs to the record is not settled.
- **C1, widened.** I rebuilt the scan with two changes:
  - it also takes the `add r, 0x50` node form, which `00639160` itself uses at `0063921A`;
  - it accepts stores at `[y + 8]`. Capstone prints displacements below 10 in decimal, and the package's store regex
    `(?: \+ 0x[0-9a-f]+)?` cannot match them (sd62o_c1 X).

  Over the 419 `.pdata` chunks in `00630000`-`0063FFFF`, it finds 3 sites, all in `00639160`. So the record's
  "one +0x50 inserter in the range" holds.

**Controls.**
- A: the positive control is the package's 12 sites, and A finds all 12.
- C1 widened: the positive controls are `00639160` in both shapes, and both pass (`lea` `00639212` / `00639231`, `add`
  `0063921A`). The package's own shape fails the `add` control.
- B: the root-ref census must include `00638C90`'s head `lea`s (`00638CAB` / `00638CB8` / `00638CC4`, which I read by
  hand). It lists 27 refs in `00638C90`.

**Package gate defect.** C1 gates only `0x00639160 in fs`. A second writer would still PASS, and the `+8`-store blind
spot would hide one anyway. The claim holds on the widened re-derivation. The gate should assert
`fs == [0x00639160]` and accept decimal displacements.

**Citations checked.** I opened every address above. `006311D0` / `006314B0` / `0067FE20` are cited by call site only.
I did not re-read their bodies.

**Runtime routing.** None. The record claims nothing live. Which non-root owners exist at run time is correctly left
open.

**Correction wording** (the producer applies it):
1. L1 paragraph: replace "Otherwise it goes at the tail of the owner's `+0x10` list." with "Otherwise it goes at the
   front of the owner's `+0x10` list, as `[head+0]`. That makes it the first node the `+0x00` walkers `008AF490` /
   `00637A70` / `00638C90` visit (`0063922E`-`00639244`)." Also fix the checker comment (`sd62_registry_lists.py` line 56,
   "else before owner+0x10 (tail of the owner's list)") to match.
2. The root table's `+0x28` readers cell, and L3's label: replace "`00638C90` unlinks an owner when its `+0x10` list
   empties" with "`00638C90` has an owner-unlink arm (`00638D6B`-`00638D89`). But it walks only root `+0x10`, whose
   descriptors carry owner = root when linked, so it is not shown to unlink a non-root owner. No unlinker of root
   `+0x28` is shown."
3. L6 paragraph: replace "`01F2E7B0` is a record of about 0x28 bytes" with "`01F2E7B0` is a record of at least 0x30
   bytes. `00635B80` also sets its `+0x28` to `01F2E7E0` and writes `01F2E7E0` / `01F2E7E8` (`00D59070` / `0063BEF0`)
   on every path (`00635C2F`-`00635C52`)."
4. C1: gate `fs == [0x00639160]`, and add the `add r, 0x50` form and decimal displacements. The printed result is
   unchanged.

---

## Part 2 - OPUS-REQ-AUDITSPEC-SD62-ORACLE-0930 (OPUS adjudication, `5a6b2eed3`): ACCEPT

Reviewed: [consumer-check.md](../opus-sd62-f3-adjudication-0930/consumer-check.md), and the F3 strike and correction
in [sd62-static-array-elements-0930/README.md](../sd62-static-array-elements-0930/README.md) with its checker label.
The adjudication upholds L5/L6 and strikes OPUS's own F3 attribution.

**Re-run.** [rerun_sd62_elements.out](rerun_sd62_elements.out) (OPUS's corrected `sd62_elements.py`) is identical to
the committed `.out`. F1-F4 PASS, `FAILS 0`. I re-ran it again at `48de14c6b`: still identical. The
`sd62-static-array-elements-0930` and `opus-sd62-f3-adjudication-0930` dirs are clean. The commit changes only the F3
label and comment: the byte condition of the check is the same, as the diff shows.

**Re-derived independently** (sd62o_indep C, sd62o_dump).
- **`01F2E780` = six qwords.** Every write into `01F2E780`-`01F2E7AF` comes from `00638F00` (`00638F73`-`00638F96`,
  `rdi` = `lea 01F2E780` at `00638F13`) or from `00636280` (`00636468`-`0063648B`, `r12` = `lea 01F2E780` at
  `006362D2`). Each writes six qwords, all of them the header's own address.
  - The third holder of that guard, `00637440`, only reads the header (`00637467 lea`).
  - The static bytes are six self pointers, each DIR64-relocated ([sd62o_reloc.out](sd62o_reloc.out)).
  - Its exit destructor is `008AFDE0` → `0067F580(01F2E780)` (`008AFDED`).
- **`01F2E7B0` is separate.**
  - Writes at `+0x30` and above come only from `00635B80` and `008AF430`.
  - The guard cells differ. `01F2E780`'s is `02CF9524`, held by `00636280` / `00637440` / `00638F00`.
    `01F2E7B0`'s is `02CF9528`, held by `00635B80` (plus one reference with no `.pdata` root, printed as `00000000`, which I did not identify).
  - `00635B80` links the record at the tail of the `PWorld` descriptor's `+0x90` list (`00635BE9`-`00635C0F`). It does
    this only if `005A7A40` finds no method of that name. `005A7A40` walks `descriptor+0x90` and runs `strcmp` against
    `[node+0x18]` (sd62o_dump). The record's `+0x18` is `"getInstanceCount"`, so it is a method record.
  - `00635B80` registers the exit `008AF430` (`00635C16`). `008AF430` unlinks `+0x00` / `+0x08` (`008AF43D`-`008AF460`),
    tests `+0x20` bit 0 (`008AF467`) and loads `+0x18` (`008AF470`).
- The static qwords of `01F2E7B0` are self, self, `02CF8A80` and the string pointer. That matches F3's unchanged byte
  check (slots 6/7 = `01F2E7B0`).

**Citations checked.** Every range in the consumer check supports its sentence:
- `00638F73`-`00638F96` and `00636468`-`0063648B` are exactly the six-qword writes;
- `00635BF7`-`00635C05` are the record's link writes;
- `008AF43D`-`008AF470` are the exit's unlink / flag / free reads.

The "0x30-byte" wording is sound. Nothing in the adjudication repeats ORACLE's "about 0x28 bytes" for `01F2E7B0`, so
Part 1's narrowing item 3 does not reach OPUS's text.

**Runtime routing.** None.

**Correction wording:** none needed. The consumer check routes the register row and the section 7 page to SWE2-DATA.
That routing still stands. It should carry Part 1's narrowings when ORACLE's row text is applied.
