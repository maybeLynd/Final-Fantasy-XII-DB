# Interior citations: the-settings-command-table.md's entry-cited functions (OPUS, 2026-10-01)

The page named 36 F-frontier functions only at their entry. OPUS read all 36 from the certified image and anchored all 36.
None was skipped: no function's whole work is its entry instruction.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `01DF176C`/`01DF1770`, `01DF18C8`/`01DF18CC`, `01DF1A24`/`01DF1A28`;
- `01F80164`/`01F80168`, `01F802C0`/`01F802C4`, `01F8041C`/`01F80420`;
- `0209BE80`, `0215E6E0`, `022CAE90`, `02B62D80`, `02B62D88`, `01E0C1E0`, `01EED410`, `02064AB0`;
- the code pointers `0023E770` and `0022F8B0`.

The constants were read from the image:

| address | value |
|---|---|
| `008C5B2C` | 0.001 |
| `00D108C4` | 1.3962634 |
| `00D108B4` | 0.27 |
| `01CEBB68` | 0.25 |
| `008F311C` | 3.0 |
| `01CEBBA8` | 1.0 |
| `01CEBC9C` | -1.0 |

**Self-correction on re-read.** These sentences were tightened against the bytes before applying:
- `00231400`: the index word is the stack word at `+0xA2`, read after `00233050`/`00233110`. The y it replaces belongs to
  a stack copy of the point.
- `00290060`: `002C63D0` takes the `+0x10F80` object.
- `0032CA70`: which output float is compared (the one written through `r9`) and which feeds `003CC480` (the one written
  through `r8`); the 0.27 float passed to `00230C00`.

**Verification.** [`settings_interior.py`](settings_interior.py) re-decodes every function first. All 135 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](settings_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 36 now measure A; none remains in the frontier (3,760 at measurement). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`);
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.** These are body statements, not meanings. What the singletons (`00796E20`, `00198790`, `00210B30`,
`001B1C00`), the globals and the callees are for stays with the page, or stays open. `00861F14`, `00202B70`, `003CC130`,
`003CC480` and the `0022F830` query are named by address only. `00231400`'s plane and grid wording describes the
arithmetic, not what the grid is.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
