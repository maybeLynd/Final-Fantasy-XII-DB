# SWE2-AUDIT-SPEC review of SD-63 (sd63-scene-parameter-layout-0930 at ce6a553b2): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `ce6a553b2`. Record: [sd63-scene-parameter-layout-0930](../sd63-scene-parameter-layout-0930/README.md).
Static.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD63-0930 | sd63-scene-parameter-layout-0930 | ce6a553b2 | ACCEPT |

**Re-run.** `sd63_scene_layout.py` from its own directory: F1-F3 PASS, `FAILS 0`, identical to the committed `.out`
ignoring CR ([rerun_sd63_scene_layout.out](rerun_sd63_scene_layout.out)). The record directory stayed clean.

**Re-derived independently** ([sd63_rederive.py](sd63_rederive.py) / [sd63_rederive.out](sd63_rederive.out), plus a
full read of `005FD2A0`, 703 bytes).
- **The table.** I decoded the 16-byte source entries straight from the file bytes, with the name qword at
  `00D3EB30 + 16i`. They give the same 23 names, indices and type codes as the checker's table. Entry 23 is not a
  parameter, so the loop bound 0x17 (`005FD317`) is the table's real end.
  - Code 49: the five matrices.
  - Code 52: the five resources.
  - Code 1: the five pairs (`NearFarPlane` and the four width/height values).
  - Code 0: five scalars.
  - Code 2: `GlobalAmbientColor`.
  - Code 3: `EyeDirWS` and `EyePosWS`.

  The record's type-code readings are labelled as interpretations, and they are consistent with this grouping.
- **The body.** I read the loop and its targets:
  - records at `02CB7DA8` (`rdi`, which is record + 8 of an array whose base `02CB7DA0` is stored at `02CB8450`);
  - the string pool at `02CBC390`;
  - the count `0x80000017` at `02CB8448`;
  - byte stores at `rdi−6` / `rdi−5`, word `rdi+8` cleared, and word `rdi+0xA` masked to its top 3 bits.

  After the loop:
  - `005FD700(ecx = 8, rdx = [02CB8450], r8d = count, r9 = &size, [rsp+0x20] = 006372B0())` computes the layout;
  - the size is rounded to 16 and stored as a word at `02CB8458`;
  - a buffer of size × ((n + 1) & ~1) is allocated, stored at `02CB8460` and zeroed.

  All of this HOLDS.
- **The fifth argument's class.** The checker tests only that it comes from `006372B0`, not its class. `006372B0`
  returns the static `01F2E0D0`, whose first file qword is vtable `00D26BE0`, RTTI `Phyre::PClassLayoutInterface`.
  HOLDS.

**The limit "`005FD700` is not read" can now be closed.** I read it: 269 bytes. After its helpers `00607990` /
`00609BF0` compute a layout of 12-byte entries, it walks the 24-byte records (`r9 = records + 0x12`, stride 0x18)
and does three things:
- it writes each record's word at record + 0x10 (the README's "word `+0x08`") from the entry's first word;
- it ORs the entry's second word into the low 13 bits of record + 0x12 (the README's "word `+0x0A`"), keeping the
  3 top bits the body preserved;
- it stores the total size through `r9`.

So the cleared word is indeed filled by the layout, as the README inferred. The low 13 bits of the other word are
also filled by the layout, which the README did not say. Whether that first word is a byte offset is still a
reading; that it is the layout's per-entry output is now shown.

**Not covered by the record (no claim made).** After the buffer, `005FD2A0` also allocates n × 0x50-byte objects
(constructed by `00615550`), gives each a type-8 check through `00628050` and the dword `0x5E4`, clears 0xB30 bytes of
another global, and calls `005CD0A0`. The record answers what the body lays out; this tail is outside the question.

**Controls.** F1 prints the whole table from the image, so it is sensitive to a wrong table base or stride. F3 is a set
of point checks. The per-record layout reading rests on the 005FD700 read above.

**Verdict.** ACCEPT. The row can take the closed limit as additional text: "005FD700 writes record +0x10 and the
low 13 bits of record +0x12 from its layout helper's 12-byte entries, and the total size through its fourth argument."
