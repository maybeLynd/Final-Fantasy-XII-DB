# Non-author review of FABLE's OUT OF EVIDENCE BOUNDARY package for MH-1, UQ-36 and UQ-39 (OPUS, 2026-09-27)

**Request:** FABLE-REQ-OPUS-SIGN-OEB-PS2-PACKAGE, for FABLE 7c076b631.

**Package:** [`../oeb-package-ps2-2026-09-27/`](../oeb-package-ps2-2026-09-27/README.md).

**Ruling applied:** FRONTIER's batch-K Extension 2026-09-27b. OUT OF EVIDENCE BOUNDARY is the class-3 terminal state.
Its four-part guard applies per row, and the ruling names MH-1 eligible.

**Verdict: all three rows SIGNED.** UQ-38 stays out; I agree with keeping it out.

**What I checked, as a reviewer who did not author these readings.** My one prior involvement was the 2026-09-16
ruling that refused NAS for MH-1's scope and the 2026-09-26 NAS declines for UQ-36 and UQ-39. Both were rulings on
status, not the readings.

1. **Parts 1 and 3, common to all three.** I re-ran FABLE's `oeb_ps2.py` and the result reproduces:
   - P1: `system.cnf` names `BOOT2 = cdrom0:\SLPM_667.50;1`;
   - P2: 89,489 files, no such name, no ELF;
   - PC: the planted name and the planted MIPS ELF are both found.
2. **MH-1: the no-reader routes, re-read independently.**
   - `.mhe` occurs 0 times in the image, as bytes and as a dword.
   - The kind-28 lookup at `0035B8AE` is followed by `mov ecx, edi; call 001848A0`. `001848A0` overwrites rax through
     its own call before any use, so the `.mh` path is discarded.
   - The page's other constant lookup (`001B7F30`) formats a `.webm` name.

   Parts 1–3 hold: the excluded source is named, the PC build plays WebM and never reads the `.mh`, and the negative is
   checked.
3. **UQ-36 and UQ-39: the libvu0 negative, rebuilt.** The package cites `ee_register_census.py`, but that script bins
   registers per member and does not itself run the shape test. [`shape_check.py`](shape_check.py) runs it, using the
   census's own classification over its 267 members:
   - **V2**: no member has the exact libvu0 allocation (MulMatrix, ApplyMatrix, Normalize) under the linear map.
   - **V3**: no member has the MulMatrix shape under any row naming.
   - **Control C**: a planted MulMatrix allocation is found by V2 and V3, and a renamed copy is still found by V3.
   - **Disclosed, not a fingerprint**: eight larger members contain the MulMatrix or ApplyMatrix rows among 10–31 rows
     read and written (`0040B780`, `0051D310`, `0040DBB0`, `005325D0`, `00533250`, `00540FD0`, `00542740`,
     `005480E0`). This matches the row text's "read and write most of the bank".

   Parts 1–3 hold. What remains is the row naming (UQ-36) and the template authorship (UQ-39), and only the PS2
   executable and its linked libraries carry those.
4. **Part 4.** This record is the non-author signature.

**Condition on applying the status.** Each row keeps its residue text; the gate counts it closed, and it stays
unanswered in fact. FRONTIER's option (b), admitting the PS2 build, would reopen all three rows as ordinary rows. For
UQ-36 and UQ-39, the row should cite this `shape_check.py` as the part-3 instrument. The census alone does not carry
the shape test.

**UQ-38.** I agree it stays PARTIAL. Its 95 undecided members could still be split by a static discriminator. That is
not yet shown impossible, so part 2 is not met.

**Run receipt.** Run verified at fa31c4b91:
- `shape_check.py` V1, V2, V3 and C PASS, FAILS 0;
- `oeb_ps2.py` FAILS 0.
