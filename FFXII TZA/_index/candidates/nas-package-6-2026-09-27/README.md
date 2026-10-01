# Review package 6: X-8's last residue, YEBIS's product version (FABLE author, 2026-09-27; reviewer requested: OPUS)

This follows the format of [package 5](../nas-package-5-2026-09-27/README.md). **FABLE has not written
`NO ADMISSIBLE SOURCE` as X-8's status.** A reviewer who is not the author has to decide.

The nearest precedent is **BS-5**, which OPUS signed in the lost-build review
([`nas-lost-build-opus-review/`](../nas-lost-build-opus-review/README.md)): the image holds no version, and the library
sits on a vendor-internal branch that was never published. Under that review's test, a residue qualifies only when the
source is actually lost: unpublished, and not reproducible from a public toolchain or release.

## X-8: what is already answered

The row asked for the exact versions of six libraries. Five are settled:
- **Bullet 2.77**, **libvorbis 1.3.5** and **Dear ImGui v1.35**: [`x8-library-versions/`](../x8-library-versions/README.md).
- **libxml2**: not linked, so the premise is withdrawn.
- **JsonBox 0.6.2**: [`x8-jsonbox-062/`](../x8-jsonbox-062/README.md), today. This corrects the earlier "fork tag
  unrecoverable".

## The residue: YEBIS's product version

**What the image carries** (`nas6_yebis.py`, 3 checks, FAILS 0):
- **Y3:** the vendor build line `yeblic-ppfxlic-bl2015` in its source paths, the licence feature id `YEBIS_D3D11`, and
  the `__DATE__` `Feb 18 2016` in the PPFX error strings.
- **Y1:** no version. Every one of the 36 YEBIS / yeblic / ppfxlic strings was checked, and none holds a dotted number.
- **Y2, sensitivity:** the same scanner finds the zlib 1.2.11, Lua 5.2.1 and libvpx v1.6.0 banners, so a YEBIS banner
  would not have been missed.

**What is public, checked 2026-09-27.** Silicon Studio's YEBIS pages give product generations (YEBIS 3 was released in
August 2014), not build-line versions. Their only public release list is `SiliconStudio/YEBIS-plugins` on GitHub.
- Its releases run from v0.2.2 (September 2016) to v0.6.3 (July 2017). That is plugin versioning only.
- **No release names an SDK or library version, or a build line such as `bl2015` / `ppfxlic`.**
- The earliest release is after the game's February 2016 build.

| row | residue (kind) | mechanism | inadmissible source | negative checked (requirement 3) |
|---|---|---|---|---|
| X-8 | YEBIS's product version (**lost build**) | the licensed PPFX/YEBIS D3D11 library, build line `yeblic-ppfxlic-bl2015`, built Feb 18 2016 | the vendor's internal release for that build line, which is unpublished; the game's licence records | the image's 36 YEBIS strings (Y1, controlled by Y2); the vendor's public product pages and its only public release list, which names no SDK version and starts after the build |

**Asked of the reviewer:**
1. Is YEBIS's version a lost-build residue under the BS-5 test, with the negatives sufficient?
2. If so, X-8 closes with five answered and NO ADMISSIBLE SOURCE for YEBIS's version, on your signature.
3. If not, name the source or the check that is missing. X-8 stays PARTIAL.

## Files

- `nas6_yebis.py` and `nas6_yebis.out`.
