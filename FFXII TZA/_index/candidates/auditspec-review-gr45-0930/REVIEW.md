# SWE2-AUDIT-SPEC review of GR-4 / GR-5 (gr4-gr5-action-row-readers-0930 at 8259918bb): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `8259918bb` (lane SWE2-STRUCT; the record's only commit), [README](../gr4-gr5-action-row-readers-0930/README.md),
`gr4_gr5_row_readers_check.py` and `rowflow.py`. Measured at HEAD 48de14c6b (a parked draft started at 9b6c5bc93; its
outputs reproduce identically at 48de14c6b). Static, certified image (sha256 asserted by [img45.py](img45.py)).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-GR45-0930 | gr4-gr5-action-row-readers-0930 | `8259918bb` | ACCEPT-WITH-NARROWING |

Both answers stand: `+0x28` has one reader (`0030A209` in `0030A190`), and nothing in the image reads `+0x0B`. The
narrowing is about wording: one count, what the positive control exercises, and a call chain with a hop missing.

**Re-run.** [rerun_gr4_gr5_row_readers_check.out](rerun_gr4_gr5_row_readers_check.out) is identical to the committed
`.out` (CR ignored): S0-S8 and N1 PASS, `FAILS 0`. `git status --porcelain --ignored` on the package directory shows
nothing. My runs used `python -B`.

**Re-derived independently.**
- **References** ([gr45_refs.py](gr45_refs.py) / [.out](gr45_refs.out)). All references to the registry
  `02EBF038..02EBF13F` are rip-relative: **0** image-base-relative, **0** indexed, **0** stored 64-bit pointers to a slot.
  - The action slot has **720** distinct instructions: 688 `load8` plus 31 `mov` with a segment prefix (all qword
    loads), and the binder's `lea` at `00237FD5`.
  - The package's "722 loads" counts (retool function, site) pairs. Three sites (`00305133`, `0030514F`, `0030515E`)
    lie in two overlapping retool extents, `00305080` and `00305110`. The disassembly shows `00305080` ends at the
    `ret` at `0030510E`.
  - `0030A190` has 2 raw callers, `0030C8F1` and `0030CCC3` (E8). There are no jcc callers and no stored pointer.
- **An independent reader census with a different method** ([gr45_census.py](gr45_census.py) /
  [.out](gr45_census.out)). It imports nothing from the package or the kit. It types each base register backward by
  reaching definitions, where rowflow tracks the row pointer forward. A base counts as a row only when it comes from
  `call 0020E600` with rcx = `[H + 0xC]` of a qword rip load of `02EBF138`.
  - Scope: 151 `.pdata` functions hold the 720 slot sites. With their E8/E9/jcc callees to 3 levels, that is 525
    functions, and 23 jump tables with 292 arms are decoded.
  - **+0x0B:** 255 covering accesses (byte, word, dword, qword or 16-byte, exact or modulo 60); **0 row-reaching**.
  - **+0x0A (control):** 5 row-reaching, exactly `002F962B`, `00309054`, `00309178`, `00309D7E` and `0031DBD2`, all
    byte reads.
  - **+0x28 (control):** 1 row-reaching, `0030A209` in `0030A190`. There the row arrives only as an argument, through
    the callers.
  - **Escapes:** 642 non-stack register stores, **0** holding a row. **Indirect calls:** 29, **0** with a row in
    rcx/rdx/r8/r9. **Stack-slot stores of a row:** 1, `00303A34 mov [rsp+0x30], r8`, the same single store as the
    package's (A4 in [gr45_reach.out](gr45_reach.out)).
- **Residue both instruments leave untyped** ([gr45_residue.py](gr45_residue.py) / [.out](gr45_residue.out)). 156
  `+0x0B`-covering accesses have a leaf my census cannot follow: callee-saved entry values, a stack slot the function
  never stores, a non-stack load, a jump-table arm with no predecessor, or an indirectly called function.
  - On 99 of them rowflow walked the function and holds no tag. The other 57 are in functions rowflow never entered,
    because it handed no tag there.
  - Read by hand:
    - `00301DD0` (36 accesses): 16-byte `movups` element moves `[rbx + r8 + 8]` → `[r14 + rax*8 + 8]`. rowflow's
      16-byte copy detector records none through a row.
    - `00307300`: `or dword [r14 + 8], 0x100/0x200/0x400/0x800` flag writes, which are writes and not row reads.
    - `00304A46 movss xmm0, [rbp + 0xB]`: an rbp-frame local, among `[rbp - 9]`, `[rbp - 5]` and `[rbp - 0x19]`.
  - I read nothing that could be a row. This residue is the limit of the census, stated here, not a finding.
- **Transfers rowflow does not follow** ([gr45_extra.py](gr45_extra.py) / [.out](gr45_extra.out), X1). There are 15
  in the 194 walked functions.
  - 11 are jump-table bytes decoded as code, past the real ends of `00307300` and `003176E0` (retool's extent runs over
    the table).
  - 2 are the `00305080`/`00305110` overlap. The `jmp 0030517E` with rcx = row lands inside `00305110`, which rowflow
    walks itself. Its accesses there are `+0x2C`.
  - 1 is a real conditional tail call, `002E809A jne 00426FA0`, carrying only the header (H) in r8. Neither
    `00426FA0` nor its callee `00426220` reads r8.
  - None hands a row on.
- **Row-returning functions** (X2). rowflow records 17. The 9 with raw callers match retool's direct-caller index
  exactly: no unknown caller, and no stored pointer to any of them. The other 8 have no rel32 caller and are stored in
  the dispatch table at `01EFA5C0..` (`00387FD0`, `00388FE0`, `0038A9D0`, `0038AA90`, `0038B010`, `0038B220`,
  `0038C940`, `0038F970`).
  - That table is called at `003859FF` and `003863D0`, `call [reg + rax*8 + 0x1DDA5C0 displacement]` with reg = image
    base. At both sites the next instruction does not read eax (`cmp dword [rip -> 02AEDFB8], 1`). So the returned
    row is discarded, as S5 says.
- **Binder.** `00237FC0` passes the slot's address to `003845F0`. That function stores the header into `[rcx]` (the
  slot) and rebases the header's `+0xC`, `+0x10`, `+0x18`, `+0x1C` and `+0x14` (the last through `0020E620` and the
  `003846F0` loop). It stores the header pointer nowhere else.
- **S6.** `0030A190` read whole (`0030A190..0030A241`) matches S6 as written: a null row returns -1; `id = (row - base)
  / [H+8]`; the `0xD0 <= id <= 0xF1` test; `[022C2160] - 5 <= 1` unsigned; `movzx eax, word [rbx+0x28]` at
  `0030A209`; the `+0x24` fallback with the `0xFFFF`, `+0x0C` bit 30 and sign tests.
- **S8 from the shipped bytes without pack.py** ([gr45_data.py](gr45_data.py) / [.out](gr45_data.out)). The file is
  us `battle_pack.bin`: directory entry `0x3C` gives section `0x13210` ('st2e'), 543 rows of stride 60 at +0x20.
  - `+0x28` is non-zero on 26 rows, all in `0xD0..0xF1`, each `120 + (id - 0xD0)` (120..153). It is zero on `0xE6`,
    `0xE8`, `0xE9`, `0xEB`, `0xEC`, `0xEE`, `0xEF` and `0xF0`.
  - `+0x29` is non-zero on 0 rows, and `+0x24` is 210 on every id of the span.
  - `+0x0B` is non-zero on rows 182..207, all contiguous, and `+0x0A` is 0 there. All 13 pairs equal the summon rows'
    `+0x0A`.

**Controls.**
- My census's `+0x0A` and `+0x28` runs are sensitive to the defect under test ("a census that stays in the slot bodies
  misses a row handed as an argument"). `0030A209` is found only through the caller-argument route. The census's
  first version had a block-start bug that lost `002F962B`, and this control caught it. The stack-store route is
  controlled by `00303A34`, which it re-finds.
- **The package's own S2 control is narrower than S1/S2 imply.** Over all 60 offsets, rowflow finds 311 hits at depth
  3 and 279 at depth 0. Turning returns off leaves 311; stripping outgoing stack arguments leaves 311 (A1). Of the hop
  census's 232 sites, 221 are found with no call followed (A2). So the control exercises the call-argument hand-off
  (11 sites). It has **no positive** for the return route or the stack-argument route. No hit in this image depends
  on either.

**Citations checked.**
- `0030A209`, `022C2160`, the two callers and `0030CCCF mov [rbx+0x24], eax` (the handle) support their sentences.
- `0031A230 -> 002FCAC0` (`lea r11, [rip -> 02EC19C0]`, `cmp edx, 0x18`) supports its sentence.
- `002FCBF0` (`mov word [rbx+0x20], di`; `call 002FC860`, which sets `esi = 0xB`) supports its sentence.
- The README's "passes it through `00328360` to `002FCBF0`" drops a hop. `00328360` is `cmp ecx, -1 / jmp 0042FCE0`,
  and `0042FCE6` is `jmp 002FCBF0`. The checker's docstring has the full chain.

**Correction wording** (the producer applies; the answer itself is unchanged):
1. S0: replace "There are 722 qword loads of `02EBF138` by rip, in 129 functions" with "There are 719 distinct qword
   loads of `02EBF138` by rip (retool counts 722 because `00305133`, `0030514F` and `0030515E` lie in both of the
   overlapping extents `00305080` and `00305110`)". Make the same change in the checker's S0 message if it is
   re-issued.
2. After S2, add: "This control exercises the call-argument hand-off (11 of the 232 sites need a call hop). No site
   depends on the return route or on outgoing stack arguments, so those two routes have no positive control in this
   image."
3. GR-4 first bullet: "`0030CBE0` passes it through `00328360` → `0042FCE0` → `002FCBF0` (two tail jumps)".
4. Limits: add "Conditional tail calls (a jcc to another function) are not handed tags. There is one in the walked set,
   `002E809A` → `00426FA0`, and it carries only the header in r8, which is not read."
