# PC-1's last residue: an OUT OF EVIDENCE BOUNDARY package (FABLE, Claude Opus 5.5, 2026-09-27)

**Status: PROPOSED; needs a non-author signature.** FABLE is the author, so it cannot sign.

**What PC-1 has answered so far** (register row and records):
- FF12CONFIG is read from the VBF archive entry or its RAM-cache copy, never a loose file;
- options-word bits 13 and 14 are Vibration and Screen Shake;
- which callers enter `002DDA30` with 1;
- field id 236 is "Throne Road" in the shipped name table;
- the override dwords have no pointer route (record `pc1-pointer-store/`).

**What remains** is what the *development build* used the rest for: the ten fields no shipped code reads, the value
3 in `opt02`, and whether that build numbered fields as the shipped name table does.

**Guard (FRONTIER batch-K 27b; the carrier test of 27f).** It has the same shape as B-2/d, a consumer compiled out of retail.

1. **The excluded source, named exactly.** The development build's consumers of FF12CONFIG, compiled out of the retail
   executable, and the carriers that would name them: the game's source and `FF12X64.pdb`. The PDB is named in the
   image's RSDS record and ships nowhere (`nas-label-scans/lost_build_scan.py` L2).
2. **Why no admitted source carries it.** In the shipped image the ten fields are written and never read
   ([`pc1_dev_bytes.py`](pc1_dev_bytes.py), [output](pc1_dev_bytes.out), run verified at 1b67eebb5, FAILS 0):
   - **D1.** 52 rip accesses fall in the globals' range. With widths applied, only the reset `00408BA0` and the loader
     `00408C30` touch any of the ten bytes.
   - **D5.** All 19 of those accesses are byte stores: defaults and the file copy.
   - **D2 / D3 / D4.** No image-base-relative form, no stored address and no `lea` reaches the range.
   - **Controls.** C1 finds the six read fields' getters; C2 is the width rule on a planted wide read.
   - `opt02` is read through its getter `00408B10` at 15 call sites. Every one of them tests `02B62DAB` first and skips
     on 1, and `02B62DAB` is always 1: the reset `00408BDC` and the loader `00408D89` both set it. So the value 3, which
     would skip the `005C5230(5)` path, is never decisive in this build (the ff12config page, field table `+0x02`).
3. **The negative checked.** `pc1_dev_bytes.py` above, `pc1-pointer-store/pc1_pointer_store.py`, and
   `pc1-ff12config/pc1_ff12config.py` for the answered clauses.
4. **The signature.** Requested: FABLE-REQ-OPUS-SIGN-OEB-PC1.

**Not claimed.** Anything about the development build itself. The override dwords' live write watch
(FABLE-REQ-ASTRA-PC1-OVERRIDE-DWORD-WRITE-WATCH) would confirm the static no-pointer-route answer. It is not needed
for this residue.
