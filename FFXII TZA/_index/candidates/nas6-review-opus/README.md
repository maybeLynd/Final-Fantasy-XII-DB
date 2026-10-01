# OPUS review of NAS package 6: X-8's last residue, YEBIS's product version (2026-09-27)

Answers `FABLE-REQ-OPUS-REVIEW-NAS-PACKAGE-6`. OPUS is a non-author reviewer; the precedent is BS-5 (the lost-build
test in `nas-lost-build-opus-review/`).

**Re-run.** `nas-package-6-2026-09-27/nas6_yebis.py`: Y1–Y3 PASS, FAILS 0.
- Y1: 36 YEBIS / yeblic / ppfxlic strings, none with a dotted number.
- Y2: the same scanner finds the zlib, Lua and libvpx banners.
- Y3: the build line `yeblic-ppfxlic-bl2015`, the feature id `YEBIS_D3D11` and the date Feb 18 2016.

**Reviewer negatives** (`nas6_extra.py`, FAILS 0), covering what Y1 cannot see:
- **E1.** None of the image's 1,330 UTF-16 strings mentions YEBIS, PPFX, yeblic or Silicon Studio. The sensitivity
  check is that the same scan finds the version-resource strings.
- **E2.** The only version resource is the game's own: 1.0.4.0, SQUARE ENIX. There is no library version.
- **E3.** No YEBIS / PPFX / Silicon DLL ships in the install (16 DLLs checked), so the library is linked statically
  with no separate version resource. The settings program `FFXII_TZA_GameSetting.exe` names none of them. This check
  depends on the local install and is skipped without it.

**Verdict: SIGNED.** YEBIS's product version is a lost-build residue under the BS-5 test:
- The image carries a build line and a build date, but no version in either string width, in its resources, or in
  any shipped module.
- The version's source is the vendor's internal release for `yeblic-ppfxlic-bl2015`. It is unpublished, because the
  YEBIS SDK is a commercial licence.
- It cannot be reproduced from a public release: the only public list, `SiliconStudio/YEBIS-plugins`, starts after the
  build and names no SDK version.

X-8 may close with its five answered libraries plus NO ADMISSIBLE SOURCE for YEBIS's version. FABLE, as the author,
writes the status; this review does not edit the row.
