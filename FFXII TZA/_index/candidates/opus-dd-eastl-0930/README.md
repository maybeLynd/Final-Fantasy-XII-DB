# OPUS DD owner read: the EASTL page and the version-stamps page move to DOCUMENTED (OPUS, 2026-09-30)

Board task `OPUS-DD-UNCLAIMED-15-99-0930`. The checker is `eastl_dd_check.py` (output `eastl_dd_check.out`,
`FAILS 0`), static, from the certified image.

## eastl-strings-containers-and-the-logging-allocator.md: PARTIAL → DOCUMENTED

Page: [eastl-strings-containers-and-the-logging-allocator.md](../../../23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md).

- **Status line.** The version stays OUT OF EVIDENCE BOUNDARY (BS-5), with UQ-306 SUPERSEDED as its duplicate. Both
  pointers are on the status line, and §7 states the limit in the body.
- **Corrected: the "attribute allocations by name" claim, in three places (§2, §6, §10's follow-on).** BS-6 already
  answered on the page that the constructor keeps no name. N1: `001EDF00` is 14 bytes; it stores the vtable
  `00902720` and returns, and never reads `rdx`. The build ships the class, not the capability.
- **Read: `001FF6B0`** (was "not read"). F1: it makes a JsonBox value an object (type 3; a `0x38`-byte map whose
  allocator is named `EASTL map`), then tail-jumps to the find `001FF4F0`. This matches
  [what the console tunes](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md).
- **Corrected: "20 callers" → 17 calling functions, 669 call sites (F2).** §3 and §10 already said 17.
- **Anchored: the atexit line (A1).** The destructor is an `008Axxxx` body passed to the wrapper `00808B90` by tail
  jump. The worksheet had read this line as a contradiction; it is not one.

## version-stamps-and-what-loading-normalises.md: PARTIAL → DOCUMENTED

Page: [version-stamps-and-what-loading-normalises.md](../../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md).

- **SD-41** is closed OUT OF EVIDENCE BOUNDARY (SWE2-DATA, reviewed ACCEPT by SWE2-AUDIT-SPEC). §6 now states the
  limit in the body.
- **SD-42** is answered (no field read of the header copies).
- The UQ-271 / V-1 line and the banner are brought current.
