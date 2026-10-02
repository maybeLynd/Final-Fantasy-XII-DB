# Third-Party Libraries

**Engine category.** Bullet physics, Lua, EASTL containers, WebM/MKV/Vorbis/VP8 media, zlib, math kernels.

| | |
|---|---|
| Classification source | CodeDomain: Bullet / Lua / EASTL / Media / Math |
| Functions | ~1,000 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md`](LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md) -
  **DOCUMENTED, tier 1.** `0016F070` is eight bytes and hands back libvpx's codec interface at
  `01CDB290`, whose name field **is** the `WebM Project VP8 Decoder v1.6.0` banner the inventory pins
  the version from. Its control map holds eleven `{id, handler}` pairs, and **four of those handlers
  are absent from the function census** - the stored qword is their only reference. **Four more control
  ids are unconditionally refused** by one shared six-byte body.
- [`PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md`](PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md) —
  ~~**DOCUMENTED, tier 2, one falsification pass.**~~ **AUDITED, tier 2** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. Answers **BK-3**. The release build folded the
  assertion reporter to `ret` but could not delete the arguments already pushed, so **26 source paths
  and 1,857 call sites survive** — enough to attribute **193 compiled functions to the source file
  they were written in**, 188 of them beyond RTTI's reach. Recovers Yebis/PPFX's four-directory
  source tree, both middleware build systems (Bamboo for Yebis, Jenkins for Phyre), and the map to
  FFXII TZA's bloom and depth of field.

- [`third-party-middleware-inventory.md`](third-party-middleware-inventory.md) -
  **DOCUMENTED, tier 2.** ~~Eleven libraries, 690 functions.~~ At least twelve libraries, 827 tagged functions *(corrected 2026-10-02, OPUS: the inventory's 2026-10-01 re-status and its lead)*. Includes **YEBIS**, commercial
  post-effect middleware with a **licence-expiry check** in the shipping game, and a Dear ImGui
  debug menu compiled into retail.

- [`Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`](Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md) — the Phyre-to-Bullet rigid-body seam — **AUDITED**
- [`EASTL/eastl-strings-containers-and-the-logging-allocator.md`](EASTL/eastl-strings-containers-and-the-logging-allocator.md) — EASTL strings, containers and the logging allocator — **AUDITED**
- [`Lua-Core/the-lua-loader-and-what-it-accepts.md`](Lua-Core/the-lua-loader-and-what-it-accepts.md) — the Lua chunk loader and what it accepts — **AUDITED**
- [`Lua-Core/CONTRACT-lua-chunk-loader.md`](Lua-Core/CONTRACT-lua-chunk-loader.md) — **CONTRACT READY**
- *(corrected 2026-10-02, OPUS: four pages this list omitted, added with the status each page's own front matter states)*

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
