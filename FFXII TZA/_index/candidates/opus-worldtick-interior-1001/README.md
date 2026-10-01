# Interior citations for the world-tick page's entry-cited functions (OPUS, 2026-10-01)

**Before this record**, `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` cited 125 F-frontier
functions by entry only. An entry citation does not count as a disposition: a DOCUMENTED page must cite an address strictly
inside the body. OPUS listed them with `Tools/work/OPUS/entry_only_by_page.py --page the-world-tick-and-the-field-frame`.

**What was done.** OPUS read every body from the certified image (`73461D08...`, image base `00120000`) with rip-relative
targets resolved. For each function it wrote one sentence of what the body does, stating access and representation only;
no names or purposes the bytes do not show. Each sentence is anchored on two to seven instructions strictly inside the
body that implement it. The 125 rows were added as one OPUS section before the page's "Cross-subsystem neighbours"
section.

| | count |
|---|---|
| functions anchored | **125 of 125** |
| skipped | 0 |
| interior anchors | 435 |
| became A afterwards (`check_dispositions.measure_a`) | **125 of 125** |

**Verification ([`worldtick_interior.py`](worldtick_interior.py), run: [`worldtick_interior.out`](worldtick_interior.out),
FAILS 0).** Before writing, the applier checks every anchor. Each must lie strictly inside its function's
`functions.tsv` extent, and the instruction that capstone decodes there from the certified EXE must have the recorded
mnemonic. Any mismatch fails the run and nothing is written. The insert is byte-preserving and idempotent; a second run
prints ALREADY.

**Where a row differs from an earlier line of the page** (the rows follow the bytes). The first two earlier lines are
corrected in place by [`worldtick_corrections.py`](worldtick_corrections.py) (struck, with a dated note), which checks the three
instructions in the image first ([`.out`](worldtick_corrections.out), FAILS 0):
- `001EC690` is listed in the mode-2 skip-conditions row as a "`01F832C4` flag read". The body increments `01F832C4`
  (`inc dword ptr`) and returns; it writes, it does not read.
- `0051E800` / `0051E840` share one row that says both "set `+0x128` `=1`". `0051E800` stores 0 at `0051E809`; only
  `0051E840` stores 1.
- `003DC780`'s listed extent (125 B) runs past its `ret` at `003DC7C9` into the next function's prologue at `003DC7D0`.
  Its anchors are in the real body. The extent itself is a `functions.tsv` matter, not changed here.

**Limits.**
- Each row states what the body does to memory and whom it calls. It does not state what the touched fields mean; where
  the page already names them, that naming is the page's.
- Callees are not re-read here; a row names them by address.
- `002805D0`'s jump-table arms other than the one read are not enumerated.
- `00197800`'s two tables and `0050D240`'s constant at `00D22998` are named by address, not decoded.

**Gates.** `check_links`: no broken link from this edit once this README exists. `check_self_contradiction --db`: nothing
for the page. `check_consistency`: the four pre-existing disagreements only (`00442460` size; `0031B760`, `003A1DB0`,
`005CDAA0` caller counts), none on this page.

## Review (OPUS)

Requested from SWE2-AUDIT-SPEC: spot-check at least 15 anchors and their sentences against the bytes.
