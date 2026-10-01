# UQ-213 — what each VU1 microprogram draws, and who uses it

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.** Table: `uq213-programs.tsv` (57 rows,
all `read`). Control: `uq213_programs.py` (4 checks, FAILS 0). Detail: [`findings.md`](findings.md) and
[`partials.md`](partials.md), which supersedes findings §5. Correction record: [`consumer-check.md`](consumer-check.md).

**How a program draws.** In this port each PS2 VU1 microprogram is an x86 function. A GiVmax command's VIF1 packet
uploads a template, meaning GIF tag cells plus a payload, and calls the program. No program carries a tag constant of
its own: a scan of all 57 finds none, and the same scan does find tags in the builders. Instead, the program copies
a tag cell its template uploaded, stamps the vertex count into it, and hands the chain to the callback. So what a
program draws is the primitive of the tag cell it selects, and the table traces that selection for each program.

**The population is 57, not the page's 47.**
- The four registrars `003A34D0` / `003A33B0` (program in `r9`) and `003A35E0` / `003A2F70` (in `r8`) have 104 call
  sites. They register 44 programs.
- The templates install 35 programs.
- The union is 57 (U1–U2). The page counted only the 29 registered through `003A34D0` / `003A35E0`, and so missed
  ten (U3). Those ten are the programs of effect types `0x8C`, `0x8E`, `0x8F`, `0x90`, `0x92` and `0x95`.

**What they draw** (57 rows):

| primitive | programs |
|---|---:|
| `TRIANGLE_STRIP` `0x05C` (IIP+TME+ABE) | 26 |
| `TRIANGLE_STRIP` `0x054` (TME+ABE, one textured quad per loop) | 6 |
| `LINE` `0x049` (IIP+ABE) | 6 |
| `TRIANGLE_FAN` `0x05D` (IIP+TME+ABE) | 4, one of which (`004758E0`) takes `0x5D` or `0x4D` from its caller's A+D PRIM write |
| `POINT` `0x040` | 5, the second programs of effect types `0x80`, `0x82`, `0x83`, `0x86` and `0x87` |
| `LINE` `0x059`, `LINE_STRIP` `0x04A` | 2 each |
| `TRIANGLE_FAN` `0x045`, `SPRITE` `0x056` | 1 each |
| mixed | 2: `004B1190` and `004C8320` |
| no GS output of their own | 2: `004DF440` and `004DCC00`, the first programs of the `0x68` / `0x69` packets; the second programs draw |

**Who uses each.** The table's `used_by` column names, per program:
- the effect element types (UQ-204's table, which now lists the second POINT programs too);
- the template families;
- any other registrar caller.

**The control (U4).** For the programs whose tag the page had decoded, the table agrees with `vif1-gif-tags.tsv`:
types `0x68` / `0x69` `0x05C`, type `0xA3` `0x049`, and type `0xA9` `0x05C`.

**Why the row is not ticked yet.** The answer is complete, but UQ-213's page box also sits in five retained evidence
copies of the VU1 page, which the question checker reads. Ticking the live box would leave those copies STALE, and a
receipt cannot be edited. The fix is asked of FRONTIER in `FABLE-REQ-FRONTIER-CHECKLISTS-SKIP-RETAINED-PREIMAGES`. The
row carries the answer as "established, pending" until then.
