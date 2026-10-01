# X-8: the linked JsonBox is 0.6.2 (FABLE, Claude Opus 5.5, 2026-09-27)

**Correction first.** FABLE's X-8 record of the same day ([`x8-library-versions/`](../x8-library-versions/README.md))
settled JsonBox to "the 0.6 line" and called the fork tag unrecoverable, "because the port replaced the only containers
that differ". That was wrong. One of the 0.6.1 → 0.6.2 differences is `String32` (`include/JsonBox/Convert.h`), which
went from `std::basic_string<int32_t>` to `std::vector<int32_t>`. That difference is still visible in the image.

## The reading (`jsonbox_062.py`, 5 checks, FAILS 0; output `jsonbox_062.out`, run with the upstream clone)

1. **Upstream (tier 6).**
   - **U1:** 0.6 → 0.6.1 changes only comments.
   - **U2:** 0.6.1 → 0.6.2 turns `String32` from `basic_string<int32_t>` into `vector<int32_t>`. This is besides the
     `Array` / `Object` wrappers, which the game's EASTL port replaced.
   - **U3:** after 0.6.2, the untagged master changes `src/Value.cpp` only inside `Value::getToString` (0.6.2 lines
     478–507). Every other changed file is a build script or documentation.
2. **The `String32` in the image is the vector (I1).** `readString`'s backslash-u arm (in `00201EB0`) appends the
   decoded code point as `if (end < cap) { *end = v; end += 4; } else insert(...)` (`002023FB`–`00202414`, helper
   `001A4250`). **No terminator is written.** A `basic_string` append always writes one. So the build is 0.6.2 or
   later.
3. **Later master is invisible (I2).**
   - JsonBox's `true` / `false` / `null` literals become one EASTL-string global per translation unit (12 in all).
   - Only two functions read more than one kind of them: the writer `001FF210` (a 7-way type switch) and the parser
     `00200E60`.
   - `getToString` reads all three, so it is not linked. Master's one code change therefore cannot show.

**So JsonBox is 0.6.2**, the last tag. The untagged later master differs only in unlinked code and build files.

## Limits

- **Static, against upstream at tier 6.** The reading assumes the game's port did not itself change `String32` from
  `basic_string` to `vector`. That would be a gratuitous edit, but it is not excluded.
- If the port did, the image fits 0.6 through 0.6.2 as the 2026-09-27 record said.

## Files

- `jsonbox_062.py`, `jsonbox_062.out` and `consumer-check.md`.
