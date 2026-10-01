---
experiment: EXP-033
title: Original action-ID gate boundary
status: VALIDATED — isolated original local branch execution
date_designed: 2026-09-11
method: B - isolated original-code execution
live_game: false
contract: ../07-Combat-Action/CONTRACT-commit-action.md
---

# EXP-033 — the normal range ends at0x21E

The commit page's assembly annotation describes `cmp di,r13w` as comparison with
0x21F while the prose says IDs below0x21F. An initial concern was that unsigned JA
would include0x21F. The original executable falsifies that interpretation:
`0030F798: mov r13d,0x21e`. The first gate at0030F7A1 compares DI against0x21E and
branches above it into the modular extended-range check. The prose range is right;
the quoted constant is wrong. Do not change the accepted normal range to include
0x21F while correcting the annotation.

## Method and boundaries

[check.py](evidence/EXP-033-commit-id-boundary/check.py) verifies the designated
executable SHA256, extracts the570-byte function at0030F760 from its PE section and
preserves the exact [bytes](evidence/EXP-033-commit-id-boundary/function.bin) and
[disassembly](evidence/EXP-033-commit-id-boundary/disassembly.txt). A fresh Unicorn
instance per case executes the original bytes beginning at0030F798 with injected
RDI and RAX=0. It stops before any call/store at one of three declared boundaries:
0030F7A7 (normal path before handle operations),0030F7F2 (extended path before commit)
or0030F981 (reject path before return-zero instruction). Missing boundaries or the
instruction limit cannot pass. No native downstream effects or full-function return
are claimed; the skipped function prologue, resolver and setup are explicit.

Eleven original cases cover0,0x21D,0x21E,0x21F,0x220,0x3FFF,0x4000,0x4165,0x4166,
0x4167,0xFFFF. They follow the expected normal0..0x21E, extended0x4000..0x4166 and
rejected surrounding values. These are boundary controls, not a65536-value census.
R13 is0x21E at every recorded endpoint.

Two private byte mutants are detected: increasing the threshold to0x21F changes
the0x21F case, and changing JA to JAE changes the0x21E case. Each case has a new
emulator and immutable original bytes remain unchanged. No reference file or process
was written. [Results](evidence/EXP-033-commit-id-boundary/result.json) preserve every
visited instruction and mutant mismatch; the [manifest](evidence/EXP-033-commit-id-boundary/manifest.json)
preserves source and evidence identities. The initially missing Unicorn import was
resolved using the already installed ASTRA library; no initial emulation ran.

## Affected claim

Return to FABLE: correct the comparison annotation in
[the commit page](../07-Combat-Action/the-moment-an-action-is-committed.md) to0x21E.
Its existing below0x21F and0x4000..0x4166 ranges agree with these original-code
controls. This does not establish target resolution, handle effects, command timing,
enmity behavior or live combat. Those require their own contracts and evidence.
