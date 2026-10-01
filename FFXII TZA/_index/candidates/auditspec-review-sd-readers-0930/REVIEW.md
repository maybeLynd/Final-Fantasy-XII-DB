# SWE2-AUDIT-SPEC review of SD-40/42 and SD-7 (OPUS, c7551f2de): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS. Reviewed commit
`c7551f2de` (both records). Static, the certified image. Register rows SD-7 / SD-40 / SD-42 belong to SWE2-DATA.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD-READERS-0930 | [sd40-42-header-readers-0930](../sd40-42-header-readers-0930/README.md) | `c7551f2de` | ACCEPT-WITH-NARROWING (method text; the answer stands) |
| OPUS-REQ-AUDITSPEC-SD-READERS-0930 | [sd7-slot15-callers-0930](../sd7-slot15-callers-0930/README.md) | `c7551f2de` | ACCEPT |

**Re-run.** `sd_header_reads.py`, `sd_slot_header_reads.py` and `sd7_slot15_callers.py` each exit 0 from their own directories ([`rerun_sd_header_reads.out`](rerun_sd_header_reads.out), [`rerun_sd_slot_header_reads.out`](rerun_sd_slot_header_reads.out), [`rerun_sd7_slot15_callers.out`](rerun_sd7_slot15_callers.out)). Each is identical to the committed output (CR ignored) except the elapsed-seconds figure. H1, S1, S2 and W print PASS. The rewritten `.tsv` files match HEAD, and both record directories stayed clean.

**SD-7, re-derived independently** ([`sdreaders_indep.py`](sdreaders_indep.py) / [`.out`](sdreaders_indep.out); raw
byte sweeps through `tk.py`, not the author's value-flow engine):
- `008C5760` + `0x78` = `0017D1A0`. The base vtable `01CB2508` + `0x78` = `005C5230` (the shared stub).
- A raw rel32 sweep of all of `.text` for `E8`, `E9` and `0F 8x` whose target is `0017D1A0` finds none. The raw call
  index has no entry either.
- The only relocated qword and the only unaligned raw qword equal to `0017D1A0` is `008C57D8`, the vtable entry.
- Code naming the vtable: `0015BC5A` (the constructor `0015BC40`), `0017CC89` (in `0017CC70`, the class's slot-0 method),
  `008A6970` (stores the vtable into the static object `01F7E350` and tail-jumps to `00793250`), and `0017CED3`
  (`008C5858`, past the 30 entries). So every construction of the class is the static object the census seeds, and
  no code loads the slot-15 entry by address.
- `call`/`jmp qword [reg+0x78]`, found by raw opcode sweep and kept only on owner instruction boundaries: **192 sites in
  114 functions**, **0** in `00790000`-`007A8000`. This matches the record's count and its control-W range claim
  exactly.

**SD-40/42, re-derived independently.**
- Direct addressing of the four fields: there are **0** rip-relative and **0** image-base-relative accesses to
  `+0x48`-`+0x67` of any of the four images (`02164280`, `021BA940`, `02211000`, `022676C0`). One raw-only candidate,
  at `008AFAE1`, is a misaligned byte match; the instruction on the boundary there addresses another global.
- **The owner identification is partly wrong, and the census misses two table holders**
  ([`ctrl590.py`](ctrl590.py) / [`.out`](ctrl590.out), [`w2_table.py`](w2_table.py)):
  - `00583040` does build the menu with `00244F50` (`ecx = 0x1c8`), handler `0057FE80` (`lea` `005831C5`), and stores it
    at `[ctrl+0xD8]` (`0058320A`).
  - But `0057FF20` does not *allocate* the table. It copies the create parameter's `+0x18` (`0057FF1C`), and
    `00583040` fills that from **`[ctrl+0x590]`** (`005831D0`/`005831D7`, parameter at `rsp+0x30`).
    `SaveLoad_ControllerLifecycleHandler` `00582860` allocates `[ctrl+0x590]` (`00582942` → `00582949`) and frees it
    (`00582EE1`-`00582EF2`).
  - At `00582E27` it also passes the same pointer to a **second widget**: `0xf0` bytes, handler `0057F360`
    (`lea` `00582E0D`), held at `[ctrl+0xF8]` (`00582E52`). That handler keeps it at **`[W2+0xD8]`**
    (`0057F5B2`/`0057F5B9`).
  - The census's HDR token is only a load of `[MENU+0x1C0]`, so neither `[ctrl+0x590]` nor `[W2+0xD8]` was followed.
- **Closing that gap.** In the named functions, there are only three 8-byte loads of `[reg+0x590]`: the two widget
  creations and the free. I then tainted every 8-byte `[reg+0xD8]` load (10) across `0057F360`'s call closure (depth 3)
  and the 147 save-module functions, and followed pointer arithmetic linearly. That gives **0** accesses at `+0x48`,
  `+0x4C`, `+0x58` or `+0x60` modulo `0xA0` ([`w2_table.out`](w2_table.out)). The route's actual accesses are `+0x04`
  and `+0x08` only ([`w2_table_all.out`](w2_table_all.out)).
  - Control ([`w2_control_1c0.out`](w2_control_1c0.out)): the same tracker seeded at `+0x1C0` finds the menu's known
    `+0x50` reads (`00580093`, `00580163`, `00580176`) and `00580CD0`'s ten 16-byte row-copy stores (`00580DBE`-`00580E17`),
    so it can see table field accesses.
  - So the answer (no field reader) holds on this route too. The tracker is linear, not flow-aware.

**Controls (the author's).**
- H1 and S1 are positive writer/store controls. S2 (a real `+0x08` read) is the one read-side control, and it is the
  one that forced every memory operand to be resolved, which is the defect the census guards against.
- The block copies (for example `00229B40` reading `+0x48` at `00229C7D`) act as de facto positive read controls.
- Control W is sensitive to a census that loses the window procedure's slot calls.
- None of these could have exposed an unfollowed table holder. That is a seed-completeness question, answered above.

**Correction wording for the owner.** The record's owner is OPUS. The row owner, SWE2-DATA, needs no answer change.
- In `sd40-42-header-readers-0930/README.md` Method 2, replace "allocates the table into `[widget + 0x1C0]` (`0057FF20`)"
  with: "copies the table pointer from its create parameter into `[widget + 0x1C0]` (`0057FF1C`/`0057FF20`). The
  table is owned at `[ctrl + 0x590]` (allocated `00582949` by `00582860`, freed `00582EF2`) and is also held at
  `[W2 + 0xD8]` by the `0xf0`-byte widget `0057F360` (`[ctrl + 0xF8]`). SWE2-AUDIT-SPEC's review followed both extra
  holders and found no `+0x48`/`+0x4C`/`+0x58`/`+0x60` access (`auditspec-review-sd-readers-0930`)."
- For SD-40/42 rows (SWE2-DATA), optional: after "the save menu's slot-header table `[menu+0x1C0]`" add "(also held at
  `[ctrl+0x590]` and by the widget `0057F360` at `+0xD8`; checked in review)".
