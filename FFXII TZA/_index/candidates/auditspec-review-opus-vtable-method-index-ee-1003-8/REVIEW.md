# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-vtable-method-index-ee-1003-8)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · at HEAD `f54822cb280713ac81cf91fc9ddb3756b11bbcea` · Task: `OPUS-REQ-AUDITSPEC-OPUS-VTABLE-METHOD-INDEX-EE-1003-8-FB30C` · Package: `_index/candidates/opus-vtable-method-index-ee-1003-8/` · Page: `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` (block "... cloud-drafted, opus-vtable-method-index-ee-1003-8)", committed in 51ad88762; page unchanged from there to HEAD)

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 13 rows hold clause by clause against the certified image. Two optional precision notes are given below; neither blocks.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 13 functions, 65 anchors`, `ALREADY` and `FAILS 0`, and exited 0. This matches the committed `interior_applier.out`, and all 13 texts appear on the page verbatim.
- `rows.json` has 13 rows and 65 anchors. The README reports rejected 0, skipped 0 and missing 47.
- Applier control: a scratch copy of the unmodified applier was run on a mutated `rows.json`.
  - Mutations: `006007B0`'s first anchor was relabelled `nop`, `007E96A0`'s last anchor was moved to the entry, and a pipe was added to `008585E0`.
  - Result: exactly those three `VERIFY FAIL` lines, `FAILS 3`, exit 1, and the page untouched.
- Pattern rows: none. Every row was read by hand. Two copy maps and one jump table were extracted mechanically to support the hand reading.
- Image: `rvlib.Img` (sha-checked, base 0x00120000, section-aware). Every body was decoded to its true end.
  - `007D5BD0`: the `.pdata` extent runs past the stated size into the body's own jump table, which ends at `007D5F44`, the `.pdata` end.
  - `007E96A0`: the extent adds the second of its two trailing `00809728` stubs.
- RTTI: 12 of 13 rows match the appendix's class and slot, each with one vtable hit. `006007B0` is not an appendix method; it has no `.rdata` qword and is named on the page only at its entry.

### SWE2-AUDIT-SPEC: the 13 rows (read by hand, to the end of each body)

Constants and imports confirmed in the image:
- `008C5B2C` = 0.001, `01CB75AC` = 24000, `01CB75A8` = 23999, `008F8180` = 10.0, `008F3110` = 0.99, `008C5B40` = 255, `00D6B96C` = 65535.
- `00861EA2` / `00861EA8` are `jmp [IAT]` thunks to `XInputGetState` / `XInputSetState`.

Row by row:
- `006007B0` exact. The fifth and sixth arguments are entry+0x28 and +0x30. The ring-slot write really is untested: a null slot leads to a write at `[0+0x40]`.
- `00654830` exact. All 23 statics are in the stated order.
- `006BAB40` exact. `005C5230` is `xor eax,eax; ret`, so the two "returns the first non-zero" exits (`006BAC3C`, `006BAC57`) can never be taken in this image. The row states the test the body makes, not an outcome, so this is not a defect.
- `007A1790` exact.
- `007A2140` exact. The reviewer read this row in full:
  - The `GetVersionExA` record is 0x94 B. The (2, 6, 1) test is on `+0x10` / `+4` / `+8`.
  - `XInputSetState` receives the words `byte*65535/255` and (byte `+0x99` > 0)*65535.
  - The foreground test runs against `02EA5248`, with byte `02EA5213` cleared or set.
  - The connected and disconnected branches call `005CDAA0(2, 01CB3858 / 01CB3890, 0079CEC0(rcx), dword [rcx+0x458])`.
  - The four signed `/128` stores use `cdq` / `and 0x7F` / `sar 7`, and two of them are negated.
  - The bit-to-byte map for `+0x43C`..`+0x44B` and the trailing 16-byte copy and `007A15A0` call are as stated.
- `007D5BD0` exact. All 53 entries of the jump table at image base + `0x6B5E70` were checked.
  - Keys 0–11, 3 and 32 are as stated.
  - The 30 record keys map to `0x228 + 0x30j` with no mismatch.
  - Keys 12, 16, 20, 24, 28, 33, 37, 41, 45 and 49 return.
  - The min/max NaN handling and "NaN is kept" are right.
- `007E96A0` exact. "Calls `00809728`" and "the same" cover both trailing stubs.
- `00833CD0` exact. The 4x-unrolled loop indexing and the remainder loop are right.
- `00834970` exact.
- `00837120` exact. Both "unread" out slots (`rbp+0xF`, `rbp+0xB`) are never read.
- `0083A070` exact. The copy map was extracted mechanically, and every run matches.
- `00853C90` exact. The copy map was extracted mechanically, including the byte-to-dword store at `+0x1EC`. The return string at `01CCF378` is confirmed.
- `008585E0` exact. The `rcx` home slot is confirmed unwritten.
- Anchors: all 65 sit strictly inside their bodies and decode as recorded. Each anchor does what its row says.

*Optional precision notes (non-blocking):*
- `007A2140`: the closing "then copies `S` to `rcx+0x45C` and calls `007A15A0(rcx)`" also runs when dword `S+0` equals `[rcx+0x45C]` (`je 007A23FA`). Read as following the "if … differs" clause it is right, but it can also be read as part of that clause. "In either case, then copies…" would remove the ambiguity.
- `007E96A0`: the bound "k+1 >= 0x100" is `cmp rcx,0x100` / `jae` on a sign-extended value (`007E97DD`, `007E983E`), so a negative k+1 also calls the stub. "(unsigned)" would make it exact.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 section 2, FRONTIER 1e64e4042)

Measured at HEAD with `progress.py`'s own helpers: `index_only_headings`, `strip_index_only`, `evidence_bearing`, `family_rule_inputs`, `cite_credits` and `doc_credits`.
- The appendix is the only `ee_index_only` heading, and stripping it removes the appendix. This block is its own `##` section outside it.
- The page is evidence-bearing, and the in-scope family overlap is 0.
- **All 13 credit engine_explained, and only through this block.**
  - Without the block, the stripped page credits 0 of the 13, and no other page credits any of them.
  - Every crediting cite is a row's interior anchor.
  - The bodies are 671–760 B.
  - `check_dispositions.evaluate` places 13 of 13 in `a_set` and `explained_set`, and 0 in `frontier_set`.

### SWE2-AUDIT-SPEC: the scoped-row ruling (auditspec-ruling-scoped-ee-row-1003, at HEAD)

No row opens with `Scope:` or carries `scoped row: set-exact`. `doc_credits` with `scoped_out` puts all 13 in the plain set and 0 in the scoped set. These are full exact rows, so the ruling sets no condition here.

- Limits: static evidence only. The cloud draft and OPUS's re-read are not independent review; this record is.
  - Twelve rows were read in a forked context of the same reviewer (FABLE). The reviewer re-read `007A2140` in full.
  - The scratch scripts and dumps (`rd.py`, `jt7.py`, `cpmap.py`, `dump7_8.txt`, `c8.txt`) are not committed.
