# R1: UC-1 bodies inside the library spans, 2026-09-29 (SWE2-EC7)

Executes R1 of [`fable-family-ruling-0929`](../fable-family-ruling-0929/README.md) (`4e32dd8df`). A UC-1 body enters a
library (C) family only as a **separately declared row** that passes four tests. Task `SWE2-EC7-UC1-SPAN-ROWS-0929`.

**Result:**

| family | UC-1 bodies in span | T1 | T2 | T3 | declared | stays frontier |
|---|---:|---|---|---|---:|---:|
| PPFX | 733 | 733 pass | holds | 731 pass, **2 fail** | **731** | 2 (T3) |
| SEAD | 1 | pass | holds | pass | **1** | 0 |
| libvpx VP8 decoder | 4 | pass | holds | pass | **4** | 0 |
| libvorbis | 17 | 17 pass | **FAILS** | 17 pass | 0 | **17** (T2) |

In all, **736** UC-1 bodies move from frontier to C and **19** stay frontier. That leaves 59 UC-1 bodies frontier in
all, of which 40 lie outside every library span. Each row is on its parent library's page, directly after the
parent row.

Inputs: shipping EXE sha256 `73461D08...21F8`, census `graph/functions.tsv` plus the UC-1 bands, and
`rtti/methods.tsv`. Every result was also produced on a **clean extract of HEAD `2c840bfe4`**, and it is identical:
`uc1-span-tests.tsv` byte for byte, and the test-2 runs and comparison.

## Test 1: strictly inside the span, with a listed member on each side (per body)

`uc1_span_tests.py` looks up the family's own members file for the nearest listed member below and above each body,
both inside the span the declaring selector states (PPFX `006DA880`-`007911E0`, SEAD `007A4380`-`007F41A0`, libvorbis
`008800C0`-`008958B0`, libvpx `0016DDD0`-`0017C890`). All 755 bodies pass.

*Negative control:* for every family, the census entry just below the span is refused by the same test.

## Test 2: the family's own boundary controls, re-run with the UC-1 bodies included (per family)

Each family's committed selector was run twice into scratch. The out-run is the selector as committed, which leaves
UC-1 bodies out. The in-run replaces only the selector's own `uc1_band.frontier_starts()` exclusion, so the UC-1 bodies
**of that family's span** are in its population (`t2_scratch_selector.py`, env `UC1IN=LO:HI`). `t2_compare.py` checks
three things: that the in-run finishes with every assertion holding; that each control names the same outside
targets and zones; and that the members grow by exactly the span's UC-1 bodies. Logs are `t2-<family>-{in,out}.txt`,
and the verdicts are in `t2-compare.txt`.

- **PPFX holds.** `select_ppfx.py` admits all 733, and its asserts hold: 25 source files, and the edge at `007911E0`
  is `PFramework`, not `PPFX`. The outbound, inbound and globals controls name the same 44 targets and the same zones.
  One count moves: `00861F6E`, an existing CRT import target, gains one caller (42 -> 43).
- **SEAD holds.** `select_audio_libraries.py`, with SEAD's body included, admits it (1136 -> 1137). The outbound (53
  targets) and globals controls are byte-identical.
- **libvpx holds.** `select_libvpx.py` admits all 4 (116 -> 120). Its interface-table, control-map and DSP-kernel
  assertions hold, and the outbound and inbound controls are byte-identical.
- **libvorbis FAILS.** The same selector, with libvorbis's 17 bodies included, stops on its own closure assertion:
  **15 of the 17 are "joined by nothing"**, meaning no call, lea, registry slot or `_ogg_` hook joins them to the
  object. That is the family's boundary control failing with the UC-1 bodies included. **The whole family stays
  frontier (17 bodies), and the test is not relaxed.** This run is also the negative control for test 2: the procedure
  can fail, and here it does.

## Test 3: callers and callees stay inside the span or run to documented entry points (per body)

References come from a **raw index**, not from `graph/edges.tsv`:
- every census body (listed plus UC-1) and every unlisted code block, decoded linearly for call, jmp, jcc and loop
  targets and rip-relative operands;
- an image-wide `.text` byte scan for `E8`/`E9` rel32, `0F 80-8F` rel32 and `EB`/`70-7F` rel8 hitting a UC-1 start (kept
  as `raw-only` when no decoded instruction explains the hit);
- the DIR64 base relocations;
- 4-byte RVA cells in `.rdata`, `_RDATA`, `.data` and `.text`.

An RVA cell is dropped only when it is provably something else: a half of a relocated 64-bit pointer (`00D38900` holds
the pointer `005CF670`, which is also the RVA of `006EF670`), or bytes inside a decoded instruction. `.pdata` records
are unwind data, not references.

A reference passes when its source lies in the span, or in the family's documented entry mechanism. That means the
caller set its own selector allows (PPFX: client `006Cxxxx`, static initialisers `0016xxxx`, unwind `008A`-`008B`;
libvpx: client `0067xxxx`), or the libvpx interface table and control map at `01CDB290`/`01CDB320` that the parent row
names as its fingerprint. A data cell that nothing attributes to the family fails the body. Callees pass when they are
inside the span or among the outside targets the family's listed members already reach.

- PPFX: 731 pass. **114 are referenced, all from inside the span, and 617 are referenced by nothing.** No member has an
  outside caller, so the documented-caller allowance was never needed. **2 fail:** `00710000` and `00710050`, whose
  RVAs (`005F0000`, `005F0050`) turn up as values in data outside the span (`00F12C78` and 245 more cells; `008EAC80`,
  `008EC020`). These are probably coincidences with round numbers, but the instrument cannot exclude them, so both
  **stay frontier**.
- SEAD: the one reference is a rip-relative operand inside the span.
- libvpx: all 4 are held in the control map at `01CDB320`, and `0016EFF0` is also branched to from inside the span.
- libvorbis: all 17 are referenced by nothing, which is consistent with its test-2 failure.
- Callees: every body passes.

*Negative controls* (`t13-run.txt`): the same reference test, run over each family's **listed** members, fails
452/1610 PPFX, 181/1127 SEAD, 57/116 libvorbis and 29/116 libvpx. So it is stricter than the families' own
membership rules and it does fail. Of the 40 UC-1 bodies outside every span, 39 fail it. The two PPFX failures above
are the in-population instance.

**Where the ruling needs judgement, stated for the audit:**
1. A body **referenced by nothing** passes test 3 vacuously. The ruling's exclusion is for a body "reached only from
   game code", and these are reached from nowhere. They enter by position (test 1) and by the family's controls (test
   2) alone. This covers 617 of PPFX's 731.
2. The libvpx control map counts as a documented entry point, because the parent row names it as the decoder's
   fingerprint and `select_libvpx.py` asserts it.

## Test 4: the series break, with its own count (per row, enforced by the gate)

Each row's note carries "N UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29" with its own
N (731, 1, 4). **`check_dispositions.py` now enforces that shape**, and it is the only route in: a row naming a UC-1
body is refused unless:
- its note carries that phrase;
- it is letter C;
- it holds **only** UC-1 bodies;
- N equals its member count.

The self-test grows 13 -> 18 cases: one positive, and four refusals (a plain row, a B row, a mixed row, a wrong
count). The report line "of which UC-1 ... band" now prints the UC-1 bodies still frontier, followed by a line with how
many R1 rows dispositioned. The population identity (34,269 listed + 795 UC-1) is unchanged. The gate edit was staged
offline and goes out in the same commit as the rows.

## Result (check_dispositions, same tree)

C 16,888 -> 17,624 (+736), frontier 5,624 -> 4,888, UC-1 frontier 795 -> 59, families accepted 335 -> 338, refused 0.

## Files

`uc1_span_tests.py` (tests 1 and 3; `--write` writes the three members files), `uc1-span-tests.tsv` (one row per body
with every test result), `t13-run.txt`, `t2_compare.py`, `t2_scratch_selector.py`, `t2-*.txt`, `t2-compare.txt`.
Members: `PostEffects-Yebis-PPFX/members/ppfx-span-uc1.tsv`, `18-Audio/members/sead-span-uc1.tsv`,
`23-Third-Party-Libraries/members/libvpx-vp8-decoder-uc1.tsv`.

**Review:** T2, so SWE2-AUDIT-SEM audits each row (`reviews` field). The gate change is a canonical acceptance rule,
so OPUS may adjudicate it.
