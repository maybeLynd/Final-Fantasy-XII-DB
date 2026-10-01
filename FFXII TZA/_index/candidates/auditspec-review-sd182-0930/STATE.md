# STATE - SWE2-AUDIT-SPEC review of SD-182 (sd182-nav-transform-pair-0930, SWE2-ORACLE 8acf79ac7) - PARKED, no verdict yet

Parked 2026-09-30 at HEAD 4b748e8af on the coordinator's wrap-up message. Independence: SWE2-ORACLE, reviewable.

Done:
- Re-run: rerun_sd182.py runs the package script unchanged with __file__ set here (the script writes
  sd182-subrecord-pairs.tsv next to itself; this keeps the package dir clean). rerun_sd182_nav_transform_pair.out and the
  TSV are identical to the committed ones (CR ignored), FAILS 0, 46 s. Image sha256 asserted. Package dir clean.
- dis_002F6AB0.txt: the YM00 walk; chunk = file+0x10+off*16, zero-size skip at 002F6CB5, tags 0x1F/0x11 -> 00232380.
  00232380 read in full: 16 stores via r9 (table) + 2 stack saves = 18; no store into the chunk.
- sd182_rederive.py / .out (independent, ov31_indep loader + own .pdata roots):
  A: 28 x*144 index forms image-wide in 21 roots; only the package's 5 roots add a qword at +0x18 -> S6's five confirmed.
  C: table cells 02EC1370 (rip 2), 02EC1378 (rip 4), 0209A678 (rip 7), 0209A680 (rip 1); image-base 0, abs64 0.
  B: taint scan over all of those roots + FA0/EB0: 0 writes through a subrecord pointer. Synthetic positive controls:
     direct movss and derived lea+movups both flagged; the third control (tab+0x18 load) flagged 0 = MY TOOL'S BUG
     (the syn3 rip load resolves to a non-table cell and clears the seeded rax). Fix before relying on the table-load path.
  D: 00380FA0 callers 0022CD59 / 0022D5D2; 00381EB0 callers 0022F968 / 00381CF3 (root 00381AC0, not yet read); jcc 0;
     rva32 1 / 4 (not yet classified - likely .pdata).
Open findings to settle:
- README "Every shipped .mpk has a YM00 section (461)": D:/FFXII_TZA_extract has 550 .mpk files; the script silently
  skips packs whose slot 8 is absent / not YM00. Count VBF .mpk names and decide; likely narrowing to "461 YM00
  sections (every .mpk that carries one)".
Left: fix syn3 control; read 00381AC0 (second EB0 caller) and the 0026E116 root-less site; independent re-parse of a
sample of extracted .mpk (scan for YM00 magic, not slot9) and recompute inverse test; write REVIEW.md.
Leaning: ACCEPT-WITH-NARROWING (the .mpk count wording), static claims holding so far.
