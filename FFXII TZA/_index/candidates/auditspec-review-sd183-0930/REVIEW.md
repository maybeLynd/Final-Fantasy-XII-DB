# REVIEW: sd183-steering-modes-0930

- **Package:** `sd183-steering-modes-0930` (SWE2-ORACLE `8acf79ac7`)
- **Task:** `ORACLE-REQ-AUDITSPEC-SD183-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of ORACLE)
- **Verdict: ACCEPT**

## Controls re-run

`sd183_steering_modes.py` → `rerun_sd183_steering_modes.out`: identical to the committed `.out`
(CR ignored), `FAILS 0`; package dir clean.

## Independent verification (`own_checks_*.out`; own loader, sha256-asserted)

### Store census — widened past the band, `own_checks_1.out`

- The record's S10 census is `st`-tainted dword stores in `00330000–00341FFF`. I added the two
  patterns it could miss image-wide:
  - **`mov dword [reg+0x80], src`**: 127 sites. Zero in `002F0000–00341FFF`; every out-of-band
    site inspected is a different record type (struct init/copy families at `002DB6*`,
    `002DC3CD`, `00265C6E`, field pairs elsewhere). No hidden steering-word write.
  - **`st = unit+0x80` aliases**: the five functions the record names (`002FDC30`, `00325BB0`,
    `00304850`, `003105D0`, `003291B0`) all materialise `+0x80` into a register but store
    nothing at disp 0 — confirmed by my own scan.
- Mode-bit writers verified byte-exact: `0033CD7C` `and eax,0x1F` + xor-insert at `0033CD7F`
  (`0033CC80`), `003346CD` `and [rdi],0xFFFFFFE6` / `003346D4` `or [rdi],6` (`003343D0`,
  mode 6 preserving the countdown), `0033E272` `and [rdi],0xFFFF8000` (`0033E1F0`, clears
  mode+countdown → mode 0), `0033D3AF` `and eax,0xFFFF815F / or eax,0x140` (`0033D200`'s
  countdown arm = 10, mode bits preserved — the record's correction of the "order word"
  misreading is right).

### Callers — own E8/E9 image-wide scan

- `0033CC80`: exactly two callers, `0033B156` and `0033B582`, both inside `0033A720` (the
  obstacle-avoidance chooser). Matches "only from `0033A720`".
- `00339F00`: exactly one caller, `0033BF8D` in `SolveDefaultStep`, gated by
  `test dword[rdi],0x7FE0; jne` at `0033BF47` — the countdown gate is real.
- `003343D0` ← `00337F51`; `0033E1F0` ← `0033EC75`/`0033ED5E`. No stray paths into the mode
  writers.
- Mode bodies `0033CEF0`/`0033D200`/`0033BAA0`/`0033CDE0`/`0033CE60` are called only from the
  dispatcher switch and the chooser — `and eax,0x1F; cmp al,{1,2,3,4,6,5}` verified at
  `0033A03B..0A6`. Modes 1 and 4 share `0033CEF0` exactly as claimed.

### Reader census — provenance-bounded (`own_checks_readers.out`)

248 `and/test …,0x1F` sites image-wide; tracing the operand back to `[ctx+0x100]`/`[ctx+0x108]`
loads or `lea [x+0x80]` aliases yields 7 sites: the dispatcher's six and `0033CD7C` (the
writer masking its own argument — not a reader). `003343D0`'s guard at `00334441`
(`and eax,0x1F; cmp al,6; je`) confirmed manually — `rdi ← [ctx+0x100]` at `003343F2`. No
other code reads the five mode bits anywhere in the image.

### `01EED4C0` chooser table

48 rows × 6 float32, degrees {0,30,45,90,120,180}; rows 24–47 all-zero. Structure matches the
record's `profile·6 + (bit3 ? 0 : 3) + speed-band` indexing claim.

### The stubs decide real tests

- `00335B60` — a genuine nav-mesh probe: builds segment quads via `00203170`/`00202E90`/
  `00202B70`/`00202FE0`/`00202B10`, calls the `003357B0` cast with flag-masked args.
- `0033D660` — a two-actor blocking test: `00265090` footprint radii summed into `xmm6`,
  `rdi+0x1A8` range, flag gates on `+0x698`/`+0xE68` records, `00334C90` separation compare.
  The stubs were honestly declared; both bodies are the clearance tests the record describes.

### E1 variant re-run — the record's declared gap closed (`own_checks_variant.out`)

The package fixture had `0208E6A0=0` (null unit), so only the arm-6 path ran. I extended it on
my own harness (same stub set, `rvimg.py`):

| `01E0C2B8` | unit count | order | `[698rec+5]` | word after |
|---|---|---|---|---|
| 1 | 0 | — | — | `0xC1` (arm **6**) |
| 0 | 1 | `0x4022` | 0 | `0xA1` (arm **5**) |
| 0 | 1 | `0x4023` | 0 | `0xC1` (arm 6) |
| 0 | 1 | `0x4022` | 1 | `0xC1` (arm 6) |
| 1 | 1 | `0x4022` | 0 | `0xC1` (arm 6) |

The arm-5 path fires only when all three gates hold (`00253B90` returns 1 when
`01E0C2B8 == 0`; `byte[[unit+0x698]+5] == 0`; `word[unit+0x714] == 0x4022`) — the record's
reading is exact, including the direction of the force-fight test. The previously unexercised
branch is now executed evidence.

## Limits carried over

- `00335B60`/`0033D660` remain stubbed in E3/E4 — real geometry decides the orbit-end branch;
  now confirmed as genuine clearance tests, not misdescribed.
- `0033BC80` height branch read-not-executed; mode-5's post-arm behaviour is read, not run.
- An alias the census cannot see (a `st` copy passed through an unrelated cell) is still not
  excluded — narrowed by the two widened patterns above but not eliminated.

**Verdict: ACCEPT** — mode layout, dispatcher gate, mode bodies' arithmetic, mode-bit writers,
the `01EED4C0` table and the arm-5 arm-6 split all verified on the bytes; the one declared
fixture gap (null unit) is now exercised and confirms the reading.
