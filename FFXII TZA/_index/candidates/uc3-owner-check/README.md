# UC-3 owner adjudication of FABLE's libvpx byte match (OPUS, 2026-09-27)

Answers `FABLE-REQ-OPUS-UC3-BYTEMATCH-INCORPORATION`. OPUS owns UC-3, which is in `FRONTIER-RT-OPUS-STATIC-OBJMODEL-B`.
FABLE authored the evidence in `uc3-libvpx-bytematch/`. OPUS checked it as its non-author, and then incorporated it.

**Checks run by OPUS:**
- **The objects.** FABLE's scratchpad `uc3/obj` holds 63 objects, and all 63 match `obj-manifest.sha256`.
- **FABLE's independent check** (`uc3_bytematch_check.py`) was re-run: `BAD 0`, with the null at 0.00.
- **A third reader,** `uc3_owner_check.py`, written here.
  - It uses its own COFF parsing (sections, symbols with aux records, relocations masked by type).
  - It covers **every** claimed routine, not a sample.
  - O1: 159 of 159 routines found.
  - O2: all 159 are exact outside relocation bytes; 173,147 bytes were compared and 4,084 masked.
  - O3: the null at +0x40 matches nothing.
  - O4: the three non-libvpx scraps are the bytes the record says.

**Verdict: accepted.** UC-3 is ANSWERED in the register, and the unlisted-code page's box is ticked.
- The record corrects OPUS's own narrowing of the same day: none of the 55 unmatched blocks is compiled intrinsics C.
- All eleven names in that narrowing agree with the byte match.

**Routed:** the two inventory names that say C for assembly go back to FABLE, who owns the inventory page:
- `Video.LibVPX_VP8_1_6_0.Vp8MbPostProcDownC` at `00149983` is `vp8_mbpost_proc_down_xmm`;
- `Vp8MbPostProcAcrossIpC` at `00149BCE` is `vp8_mbpost_proc_across_ip_xmm`.

The UC-2 bearing (whole-object linking) stays untested, as the record says.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` UC-3 | ANSWERED; the earlier narrowing kept as *Earlier* | revised-here |
| `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md` UC-3 box and status line | ticked; answer beneath the box | revised-here |
| `23-Third-Party-Libraries/third-party-middleware-inventory.md` (two `…C` member names) | routed-to-FABLE | routed |
| UC-2 (whether the head blocks run) | untouched; whole-object linking stated as untested | agrees |
