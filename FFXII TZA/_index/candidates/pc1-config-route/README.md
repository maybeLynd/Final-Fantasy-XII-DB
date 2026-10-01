# PC-1: FF12CONFIG is read from the archive, and the stream resolver has no loose-file route (FABLE, Claude Opus 5.5, 2026-09-27)

**Clause (PC-1):** "whether `001D6F20` reads the archive entry or a loose file is not traced." The same question is
open on [how a path is resolved to bytes](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md)
§8 ("which route serves loose files", "what route 1's manager is"). One line on
[the BigFile index page](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md)
§7 is also answered here: what `005CCAB0` and `0079B1E0` open with `CreateFileA`.

**Answer: the archive entry.** `FF12CONFIG` comes out of `FFXII_TZA.vbf`, either directly through the package lookup
or as the RAM file cache's copy of it. No loose-file route exists in the chain.

## The chain (`pc1_route.py`, 7 checks, FAILS 0; output `pc1_route.out`)

1. **The open (R1, R2).** The config loader `00408C30` calls `001D6F20("PS2Data/SQUARE_FF12/FF12CONFIG", 1)`.
   That builds the 0x30-byte source record through `00597930`, with selector byte `+0x18` = 1, and runs the resolver
   `0059EE90`.
2. **Two routes, no third (R3).** The resolver stores a source in only two fields:
   - **route 1**, `001D6D20`, into the size source `+0x20` (`0059EFEA`);
   - **route 2**, the package resolver `0019B1F0` / `0019AEE0`, into the object source `+0x10` (`0059F197`).

   It never sets the `+8` handle. A route-2 miss logs `[FFXII_ERROR] Big file open failed` and returns 10.
3. **Route 1 is a RAM file cache (R4).** Its enable byte `01F83440` has one writer, `0020C610` (`0020C695`, always 1).
   That function first calls `GlobalMemoryStatusEx` and sets a budget at `01F83448`: total physical memory ÷ 3,
   clamped to 32 MB–4 GB.
   - Its fill is route 2's own success path: a route-2 hit with `r12b` set is committed into the cache through
     `0059A9B0` (`0059F1B7`), the commit-and-release the FST page reads.
   - So the cache holds copies of package entries. This settles the path page's hypothesis about route 1's manager.
4. **Route 2 is the one archive (R5).** The five-slot package mount `0019B070` (construct `001F4060`, BigFile load
   `001F4340`, freed on failure) has one call site image-wide, `0017CEF6`, which mounts `../FFXII_TZA.vbf`.
5. **No loose-file open (R6).** `CreateFileA` is the only `CreateFile*` import, and it is referenced at exactly two
   sites:
   - `005CCAE8` in `005CCAB0`, with `"Minidump file saved to %s"`;
   - `0079B298` in `0079B1E0`, with `"%s_%d_%d_%d_%d_%d_%d.dmp"` and `"Create dump file filed..."`.

   **Both are minidump writers.**
6. **FF12CONFIG takes route 1 first (R7).** The path passes the resolver's character filter. That filter is nine
   single-character tests on the last five characters, any match sending the path to route 2; the control shows it
   catches `.mab`, `.webm` and `.bin`.

## Limits

- **Static.** Whether a given run's cache already holds the entry is a runtime state; either way the bytes are the
  archive's.
- **"No loose-file route" is scoped** to this resolver: its two source stores, the one mount site and the
  `CreateFile*` census. CRT stdio (`fopen` / `_wfopen`) is used elsewhere in the image, which is how the BigFile page
  reads the index. Nothing here sends a `001D6F20` path to it.
- **The mod scene's loose-file loaders** (`dinput8.dll`, noted on the FST page) are outside the shipped image.

## Also recorded (a qualification, not a correction)

The path page's §8 control describes the filter as a dot four or five characters from the end. The bytes carry nine
tests (`0059EF4B`–`0059EFA9`): the dot at −4 or −5, but also `m`, `a`, `b` at −3, −2, −1 and `w`, `e`, `b`, `m` at
−4 … −1. The page's prediction (three- and four-character extensions go to route 2; `.phyre` reaches route 1) holds
under either reading.

## Files

- `pc1_route.py` and `pc1_route.out`.
- `consumer-check.md`.
