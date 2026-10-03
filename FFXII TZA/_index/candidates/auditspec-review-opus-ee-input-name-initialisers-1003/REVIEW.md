# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-input-name-initialisers-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-INPUT-NAME-INITIALISERS-1003` · Package: `_index/candidates/opus-ee-input-name-initialisers-1003/` (rows committed in `3a61a9fcd`, reviewed at HEAD `050fd9350`) · Page: `15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 319 rows are correct against the bytes. The lead overstates how far members differ only at the anchor; the narrowing below corrects that sentence. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** `fam_rows.py check` was run in place with `-B`; check mode writes nothing. It ran under the analysis venv python and exited 0:
  `members 319, committed rows 319, declared exclusions 0` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`.
  - The output is identical to the committed `fam_rows_check.out`.
  - The working-tree `fam_rows.py` is an uncommitted later revision, shared with other packages. It adds a value-dedup and moves the per-member extraction into `derive_all`. The HEAD-committed text was run against the same rows through an in-memory exec and also gave FAILS 0.
- **What the checker tests.**
  - It re-derives each row from the image (`ex_registry_node`: capstone over image bytes; node = the rip target of the +0x4 `lea rcx`; name = the C string at qword `[node+8]`; callee = the +0xB call). It compares all six columns with `rows.tsv` and fails a non-member row, a missing row or an anchor outside the census extent.
  - The form test is looser than the README says. It checks mnemonics at positions 0, 1, 2, 3 and 5 only. It does not check `add rsp, 0x28` at position 4, the tail target `00808B90` or the 32-byte size.
  - Independent census (disw.py image reader, not retool or fam_rows): all 319 members have one masked form at size 0x20, `sub rsp,0x28 / lea rcx,[rip+X] / call T / lea rcx,[rip+X] / add rsp,0x28 / jmp T`, and the tail jump goes to `00808B90` in 319 of 319. The looser test therefore hides no defect here.
- **Controls' sensitivity: the printed controls are tautologies.**
  - `ok1` compares the extractor's value for row 0 with a row chosen *because* its value differs. `ok2` compares an anchor with that anchor + 1. Neither runs the row comparison.
  - With an image-blind extractor that echoes `rows.tsv`, an in-memory harness still printed both controls "refused" and FAILS 0 (T6).
  - The comparison itself is sensitive. These in-memory mutations of row 159 (`0016BFE0`) each failed: value swapped with row 160 (FAILS 2), name replaced (FAILS 1, image `Key_Right_Alt` vs row `Key_Right_Control`), anchor + 1 (FAILS 1), mnemonic changed (FAILS 1), row deleted (FAILS 1).
  - So the ruling's "refuses a swapped value" holds through the comparison loop, not through the printed controls. See the notes.
- **Sampled rows.** 20 rows, evenly spread at 0-based data-row indices 0, 17, 33, 50, 67, 84, 100, 117, 134, 151, 167, 184, 201, 218, 234, 251, 268, 285, 301 and 318. Each was decoded independently, with all five registries covered.
  - The entry is 32 bytes, with the anchor `lea` at entry + 4 (`0016ABA4` ... `0016D544`).
  - The node is that lea's rip target.
  - The qword at node + 8 is file-backed and points at the stated name, for example `01F44DC0` -> `01CD7D48` "JoypadAxis", `01F46C28` -> `01CD8644` "Key_Z" and `01F47368` -> "Button_Triangle".
  - The call target equals the row's callee.
  - **20 of 20 exact.**
  - The semantic claim was checked on `008760A0`: the insert walks its list comparing the bytes at `[node+8]` with each element's `[+8]`, so qword +0x8 is indeed the compared key.
  - Nodes are unique across all 319 rows. 140 names recur across registries (for example "Button_2" in both the channel and the joypad lists), so the node, not the name, is what distinguishes a member.
- **Excluded sample.** `excluded.tsv` is empty (0 declared exclusions), so there was nothing to sample. Every member in the family TSV derives a row.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction unique to the member: the +0x4 `lea`, whose node is unique per member.
  - Each row states member-specific values read from the image: the node and its registered name. The shared shape is stated once in the lead.
  - A committed checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead, in spec.json `lead` and the page section.** Members do not differ only in the node. An independent census over all 319 found three varying instructions:
- the +0x4 node `lea`;
- the +0xB insert call (five targets, which give the grouping);
- the +0x10 `lea rcx, [teardown]`, which has 319 distinct targets, each member's own node-unlink teardown (for example `008B98F0` for `0016ABA0`, a member of `registry-unlink-teardowns`).

Replace:

> What differs from member to member is the node that + 0x4 `lea` loads, and therefore the name the node carries at qword `+0x8`, the key the insert compares.

with:

> What differs from member to member is the node that + 0x4 `lea` loads (and with it the name the node carries at qword `+0x8`, the key the insert compares), the insert called at + 0xB (one of five, the grouping below), and the teardown that + 0x10 `lea` hands to `00808B90` (each member has its own node-unlink teardown, listed in the members TSV's `dtor` column). The rows anchor the node `lea`; they do not state the teardown.

**Notes (non-blocking):**
- Control repair: make the two controls pass mutated copies of `rows.tsv` (a swapped value, a moved anchor) through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes, so that an extractor which stops reading the image fails. Today's controls cannot fail while the extractor returns anything at all.
- The README's "a member whose body leaves the 32-byte form is refused" claims more than the code checks (see above). It is true of the current image only by the census.
