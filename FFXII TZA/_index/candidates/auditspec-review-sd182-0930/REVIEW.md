# REVIEW: sd182-nav-transform-pair-0930

- **Package:** `sd182-nav-transform-pair-0930` (SWE2-ORACLE, commit `8acf79ac7`)
- **Task:** `ORACLE-REQ-AUDITSPEC-SD182-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of ORACLE)
- **Verdict: ACCEPT-WITH-NARROWING**

## Controls re-run

`sd182_nav_transform_pair.py` re-executed via `rerun_sd182.py` (output + TSV written into this
review dir, keeping the package dir clean): output text-identical to committed `.out` (CRLF
only), `sd182-subrecord-pairs.tsv` identical (832 rows), `FAILS 0`, 46 s. Image sha256 asserted.

## Independent derivation (`sd182_rederive.out`, own loader + .pdata roots)

- **S6 index-idiom census:** 28 `x*144` index forms image-wide in 21 roots; **only** the five
  claimed roots (`0022CC50`, `0022D4B0`, `0022D7E0`, `0022DE60`, `0022F8B0`) add a qword at
  `+0x18`. Confirmed exactly.
- **Cell refs (C):** `02EC1370` rip 2, `02EC1378` rip 4, `0209A678` rip 7, `0209A680` rip 1;
  zero image-base, zero abs64, zero rva32 forms.
- **Taint scan (B):** over all 33 relevant roots — **0 writes through a subrecord pointer, 0
  through a table pointer**. All three positive controls flag correctly (after my own
  instrument fix: the syn3 `mov rax,[rip]` control originally seeded `rax` manually and the
  scan immediately discarded it; now the load seeds via the real `rip→TABLE_CELLS` rule and
  flags `movss [r8+0x10]`).
- **Loader read (00232380):** 16 stores via r9 into the table + 2 stack saves = 18 stores;
  none into the chunk. `002F6AB0` YM00 walk: chunk = file+0x10+off·16, zero-size skip at
  `002F6CB5`, tags 0x1F/0x11 → `00232380(obj+0x40)` / `(obj+0xA8)`. All verified.
- **Consumer callers (D):** `00380FA0` ← `0022CD59`/`0022D5D2`; `00381EB0` ← `0022F968`/
  `00381CF3` (∈ `00381AC0`, a vector-distance routine — read; benign). `0026E116` is a
  table-cell *reader* thunk (`cmp [0209A670],0; cmovne rcx,[0209A678]; jmp 00231400`), not a
  writer — consistent with the read-only claim.

## Data claims spot-verified

- 89,330 subrecords / inverse test / negative control reproduce via the package script
  (byte-identical TSV).
- **Narrowing — "Every shipped .mpk has a YM00 section (461)" is false as written.** My own
  census of `D:\FFXII_TZA_extract`: **550 `.mpk` files, 461 contain `YM00` bytes, 89 do not**
  (the 89 are no-nav packs — small files whose slot-8 section is absent, e.g.
  `alc0100.mpk`, a mostly-zero 62 KB pack). Correct wording: "461 of the 550 shipped `.mpk`
  files carry a YM00 section" — the script silently skips packs without one, which the README
  already implements but not states. The 89 absentees are consistent with "no nav shapes"
  rather than hidden sections: no compression was found (no zlib streams; headers are plain
  section tables).

## Limits

- The S6/taint argument bounds writes *through the index idiom*; a whole-file `memcpy` or
  relocation pass is not excluded statically (the record states this).
- "Inverse" restated as file-byte equality within float32 rounding — verified as a data claim,
  not a semantic proof of matrix inverse intent.

**Verdict: ACCEPT-WITH-NARROWING** — the core answer (transform pair is authored in the map
pack, `+0x50` = inverse of `+0x10` in file bytes, engine never writes them) is verified on the
bytes, the full taint census and the data corpus; narrowed on the ".mpk count" wording only.
