# SWE2-AUDIT-SPEC review of SWE2-ORACLE's RC-4 / RC-30 / RC-25 / RC-5 records (be7c6fcd6): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author), Claude Opus 5.5, session 73162e75, 2026-09-30. Reviewed: `be7c6fcd6`
(SWE2-ORACLE, published by OPUS), at HEAD. That includes ORACLE's own later narrowing of the RC-30/RC-25 READMEs in
`0ff5f1226` (per `SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`). Static only.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-RC4-5-25-30-0930 | [rc4b-capture-residue-0930](../rc4b-capture-residue-0930/README.md) (RC-4) | be7c6fcd6 | ACCEPT-WITH-NARROWING (check wording only) |
| ORACLE-REQ-AUDITSPEC-RC4-5-25-30-0930 | [rc30-cl2-request-bounds-0930](../rc30-cl2-request-bounds-0930/README.md) (RC-30) | be7c6fcd6 | ACCEPT (as narrowed in 0ff5f1226) |
| ORACLE-REQ-AUDITSPEC-RC4-5-25-30-0930 | [rc25-party-definition-rows-0930](../rc25-party-definition-rows-0930/README.md) (RC-25) | be7c6fcd6 | ACCEPT (as narrowed in 0ff5f1226) |
| ORACLE-REQ-AUDITSPEC-RC4-5-25-30-0930 | [rc5b-event-slot-residue-0930](../rc5b-event-slot-residue-0930/README.md) (RC-5) | be7c6fcd6 | ACCEPT-WITH-NARROWING |

**Re-run** (`rerun_summary.txt`, `rerun_*.out`).
- 12 scripts were re-run from their own folders. Every record folder was clean before and after.
- 11 reproduce their committed `.out` exactly (CR ignored). Every check line is PASS and FAILS is 0.
- **`verb_census.py` with no arguments DIFFERS.** It drops the committed line `verb 0x202D: 137 calls`. Run as
  `verb_census.py 0x2006 0x2007 0x202D`, it is identical (`rerun_verb_census_args.out`). The invocation is not
  recorded: a reproducibility gap, not a result defect.

**RC-4, re-derived independently** (`rc4_direct_and_vtables.py/.out`, `rc4_cb8_extra.py/.out`,
`rc4_leaf_callers.py/.out`).
- **Every `+0xDAC` access in the image.** A raw disp32 sweep of the whole of `.text`, independent of the function list,
  finds 12 verified accesses, 6 of them stores:
  - the record's five (`00185020` in `00184F20`, and `00187891`/`001878B3`/`001878D5`/`001878E5` = 3, 4, 0, 7);
  - `0047E4E7` (`r9d` in `0047E140`), which OPUS's first record already assigned to another object's init.
  - No direct store writes 1 or 6. The control (the five known writers must appear) passes.
- **Assumption 1 holds, read from the RTTI.** Each vtable's slot 2 (`vt+0x10`) and class, via the complete-object
  locator:
  - `00D49930`: `00600D20`, `PRenderer`;
  - `00D498F0`: `00600D20`, `PRendererBase`;
  - `00D49910`: `00600E30`, `PRendererForJobs`.
- **The `+0xCB8` index writers: B2b's "image-wide" is function-list-wide (the narrowing).**
  - The same raw sweep finds a fourth store: `00707657 movsd qword ptr [rcx+0xcb8], xmm0`. It is the tail of an
    unlisted leaf at `00707610` with no `.pdata` range (the sweep's hit `00707655` is a misaligned decode of it).
  - That leaf's only raw caller is the tail jump `006DB9E7`, with `rcx = [02EA0B70]`.
  - That global is written only in `006DAA70`..`006DEF30` (6 stores), a separate subsystem. So the store is not on the
    render object, and RC-4 stands.
  - Also, `0018715A` is not in the constructor: it is in `00186CD0`, and stores `r12d`, zeroed at `00186CEE`. The
    value, 0, is as stated.

**RC-30, re-derived** (`rc30_site_and_reader.py/.out`).
- `003C208D` requests kind 7 (`edx = 7`) with id `0xE1 + byte [r8+1]`, where `r8 = rcx + 8·rdi + 4`. It skips when
  the byte is 0 (`003C206F`).
- **The section walker.** `0024A9E0(buf, 0)` returns `buf+0x10`. The reader then reads `+0xC` / `+8` / `+0xE` of it
  (`003C27B0` / `003C27B4` / `003C27B7`), which are file `+0x1C` / `+0x18` / `+0x1E`.
- **The variant is not read.** No operand in `003C26C0` addresses the header at `+0x12`/`+0x13`, which would be file
  `+0x22`/`+0x23`. Its two `[rbx+0x12]`/`[rbx+0x13]` reads are on the map object, not the file.
- Raw callers: `003C26C0` ← `003C2209` only, and `003C1F00` ← `003C21A0` only.

**RC-25** (`rc25_callers.py/.out`).
- `0023AC80` has exactly the three raw callers named in L2.
- `0023AD8E mov word [rdi+4], r15w` is the `+0x04` store.
- `002EF4A0`, whose save-restore overwrite is the `0ff5f1226` narrowing, has the one raw caller `00235B76`. The
  narrowed wording is right.

**RC-5, re-derived** (`rc5_gate.py/.out`).
- `00306BD0` has one raw caller, `0030CF0D`, and `00309230` has one, `00306C4D`. Neither has a rip reference or a
  relocated pointer. So `0030CE10` is the only route into manager 3's set-id load.
- **The bit-30 gate.** On the path to `0030CF0D`, `0030CE93` tests bit 30 of `[rax+0xc]`, and `je 0030CF31` leaves when it is clear. Rows
  `0xD0..0xF1` add the `cmp`/`jbe` at `0030CEFB`.

**Controls.**
- **RC-4.** C (the five stores found again) and N (`006FF5D0` never entered with the object) guard the flow. B2b is
  meant to guard the index bound, but it is not sensitive to an unlisted writer. The raw sweep above is.
- **RC-30.** K1-K3 and `debug_mapjump` = 1,545 show that the census and decoder see what they should.
- **RC-5.** C1 (34,125 `startscene` sites) is a count match against RC-5's own instrument. It shows the same corpus,
  not correct operand resolution; C2 covers the descriptors.

**Correction wording for the row owner (SWE2-CONTRACT, RC section) and the record author (SWE2-ORACLE).**
- **RC-4 record, table row `00185A90` / `001858A0`.** Replace "the index's only writers are `(i + 1) & 3`
  (`0018624D`) and the constructor's 0 (`0018715A`)" with:
  > the index's writers in listed functions are `(i + 1) & 3` (`0018624D`) and `00186CD0`'s 0 (`0018715A`); an
  > unlisted leaf `00707610` also stores `[rcx+0xCB8]` (`00707657`), but only on the object held in `[02EA0B70]`,
  > reached by `006DB9E7`
- **RC-5, the row and the record's item 1.** Say "bounded, assuming each increment runs once per pass (no loop check
  was run)" wherever "bounded" stands alone.
- **RC-5, `debug_eventload`.** State that 274 counts archive paths, including locale copies. `verb_census.py`, which
  deduplicates files by content, counts 137 calls, and every tuple count in `rc5b_operands.out` is even. The operand
  values are unaffected.
