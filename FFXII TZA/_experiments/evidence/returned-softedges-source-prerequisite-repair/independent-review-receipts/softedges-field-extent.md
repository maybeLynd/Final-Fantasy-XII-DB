# SWE2-AUDIT-SPEC review of ASTRA phyretext-softedges-field-extent (5bbbe5528): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: ASTRA's packet
`_experiments/evidence/phyretext-softedges-field-extent/` at `5bbbe5528`, Method A (static only). Reference EXE
`73461D08…21F8` (re-hashed by `fe_exe.py`), shipped asset `D:/FFXII_TZA_extract/gamedata/d3d11/artdata/shaders/phyretext.fx.phyre`.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SOFTEDGES-FIELD-EXTENT-0930 | ASTRA-PUBLISH-SOFTEDGES-FIELD-EXTENT-0930 | `5bbbe5528` | ACCEPT (scoped exactly as the packet scopes it) |

**Clause by clause** (numbers from this directory's `.out` files)

- *Exact PhyreText.* The shipped file on D: is 44,634 B, SHA `f67d4492…a767a4cf`, byte-identical to the retained copy
  (`fe_file.out`). My own header walk closes exactly: data 14,408, fixup tables start 44,208, and 44,208 + 4 + 303 + 119
  = 44,634 = file length. List 12 is class 43, 12 objects, 156 object bytes, 164 array bytes, starting at 29224,
  arrays at 29380.
- *Class 43 / packed 13 B vs native 24 B.* I read the namespace without EA-3 code (`fe_file2.py`). The string base is
  8628, pinned by three class-name offsets. Class 43 = `PShaderParameterDefinition`, packed width 13, 6 members. `m_name`
  is at +4 (width 1, `PString`) and `m_bufferLoc` at +5 (width 4, type class 44). Native side, read from the EXE
  (`fe_exe.out`): lookup `0018D240` walks 0x18-byte entries comparing the name at +8, then a second array at
  [rcx+0x58]/[rcx+0x50], and returns the first match. The copy reads `word [rax+0x10]` (offset) and `word [rax+0x12]`
  (size), i.e. `m_bufferLoc` at native +0x10 with `m_offset` +0 / `m_size` +2. The two layouts are not interchangeable.
- *Inherited m_offset 44 -> 38.* Class 44's parent word is 38 (0x26). Class 38 `PShaderParameterCaptureBufferLocation`
  holds `m_offset` at 0 (width 2). Class 44 holds `m_size` at 2 (width 2).
- *12 records / name fixups, entry (0x80000004, 8, 0, 138).* The 12 decoded array fixups (the reducer's CU-3 decode,
  not re-implemented) all carry key 0x80000004 (`m_name`'s offset 4 with the high bit). Their indices are 0..11 once
  each, and their 12 array offsets equal exactly the 12 NUL-string starts that I found myself in the 164-byte region
  (`fe_controls.out`). Index 8 -> offset 138 -> `softEdges` at 29518. The EXE clears that key bit at `0059C4D9`
  (`btr ebx, 0x1f`) and adds entry+0x0C to the array base at `0059C5A4`/`0059C5A8`. Record 8 at 29328 is
  `0000400100a0000800b8000000`: capture offset 160, size word 8, masked 8. Controls: `textColor` 16, `alphaThreshold` 4.
- *`001D03C6` outer+8, `001EA5C1` receiver+0x118, masked copy `001EA609`, memcpy import.* `001D03C3 mov rdi, rcx` /
  `001D03C6 add rcx, 8` / `001D03CA call 001EA3C0`. In `001EA3C0` the only write to rsi is `001EA3DC mov rsi, rcx`
  (entry rcx unchanged before it); rsi is callee-saved across the 12 intervening calls; `pop rsi` only in the epilogue.
  `001EA5AD lea rdx` -> `00901B18` "softEdges"; `001EA5C1 lea r10, [rsi+0x118]`; `and dx, 0x1fff`; refuse
  (ebp = 3) unless offset + size <= `dword [rbx]` and offset >= 4; then `rcx = rbx + offset`, `rdx = r10`,
  `r8d = size` and `call 00861EBA` -> `jmp [008C2A68]` = `VCRUNTIME140.dll!memcpy`. The resource slots `01DFDE00` /
  `01DFDE08` point to the PhyreText.fx.phyre / tuffysdf.fgen.phyre paths. 8 + 0x118 = 0x120. The first AE0 byte
  needs length > 0x9C0 (2496) and the whole dword needs >= 0x9C4 (2500).
- *Conditional exclusion outer+0x120..0x127 only.* This holds for the shipped definition via the `001D03C6` route. A
  stronger fact, independently: no record in this file exceeds 64 bytes, so no definition in this asset can reach AE0
  from +0x120. The OPEN items (membership, resource success, destination aliasing, constructor return,
  metadata/lifetime, natural action) remain open; this review adds nothing to them.

**Scope note (not a defect).** `001EA3C0` has three raw callers (`fe_exe.out`, E8/E9/jcc byte sweep; 0 rip refs,
0 relocs): `001D03CA` (the reviewed route), `001C1E04` in `001C1D40` (receiver `rdi+0x118`) and `001C2BFD` in `001C2980`
(receiver = 0x230-stride element + 0x108). The packet claims only the first route and never states that the caller is
unique. A consumer must not read "outer+0x120" as covering the other two receivers.

**Re-run.** `reduce-softedges-field-extent.py` into a fresh path: exit 0; the result equals `field-extent-result-02.json`
in all 1,460 leaves (`rerun_reduce.out`, `rerun-result.json`). The packet dir was clean before and after.

**Controls** (`fe_controls.out`, all on in-memory or disposable copies, since removed)

- Size word 0x9C0 -> no AE0 byte; 0x9C1 -> first byte; 0x9C3 -> not whole; 0x9C4 -> whole. The threshold is exact on
  both sides. 0x29C1 masks to 0x9C1, as the EXE's `and dx, 0x1fff` does. An offset-word change alone (size 8) does not
  move the source extent, which is correct: the source is receiver+0x118, not the capture offset.
- Refused: name `XoftEdges`; class-44 parent word 0; class-44 `m_size` member offset 2 -> 0; record bytes 8 and 1 swapped
  (caught by the named-size controls). My first `m_size` mutation hit another class's same-named member (name offset
  0x822 is shared by members 7/65/124/137) and was accepted. That was my instrument's error, not a reducer gap.
- CLI: unchanged copy passes; incomplete wrapper, missing caller capture (an uncaught FileNotFoundError, still exit 1
  with no result), changed asset and changed `001EA5C1` args text are all refused.
- Checker limit (`fe_capture_bytes.out`). All 1,530 instructions in the four retained captures match the EXE bytes and a
  fresh decode, so the claims stand. The reducer, however, ties instructions to the EXE only through the capture's
  mnemonic/args text and a span hash computed from the same file. A bytes-only change at `001EA5C1` (disp 0x118 ->
  0x9C8, hash recomputed, text kept) still passes, and the reducer's source offset 0x120 is a constant. The receipt
  therefore rests on the captures matching the EXE, which this review checked directly.

**Suggested limit wording for ASTRA (optional; the claims need no correction).** "The reducer checks retained
instruction text and span hashes; it does not re-read the EXE, and its source offset 0x120 is a constant. The +0x120
source is established for the `001D03C6` route only; `001EA3C0`'s other callers `001C1E04` and `001C2BFD` pass other
receivers."
