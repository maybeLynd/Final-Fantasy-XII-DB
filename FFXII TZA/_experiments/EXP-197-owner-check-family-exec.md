# EXP-197 — Owner-check family `0030B770`/`0030B7F0`/`0030B9B0`/`0030B8E0` + arm carriers `00300140`/`003299B0` execution

**Status:** complete — **271/271 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256 `3281128f…`), zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..196; 238 inherited + 33 new `b770-*`/`b7f0-*`/`d470-*`/`b9b0-*`/
`b8e0-*`/`b140-*`/`k99b0-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Executes the auto-status cascade's owner-check family and two arm carriers as
shipped bytes — the bodies the EXP-104 run scripted as `~sb9`/`~sb8`/`~s014`/
`~s99b` plus the accessor EXP-104's table called a "context carrier":

- `0030B770` — global owner-flag composer (leaf).
- `0030B7F0` — per-object flag composer; calls `0017D470` twice.
- `0030B9B0` — CASC eligibility wrapper (`30AB40` pair count + both composers).
- `0030B8E0` — second wrapper: fires only on `0030B7F0`'s **high** word.
- `0017D470` — singleton mode accessor: `d[001D50D0() + 0xC20]`.
- `001D50D0` — lazy singleton getter behind `q[01F81428]`.
- `00300140` — CASC "unlink-mark" carrier (conditional `003105D0` + field
  clears + `q[obj]` bit14 semantics).
- `003299B0` — msg-id carrier: `002EB030` node write + `d[obj+0x5C]` store.
- `002EB030` — entity-node marker reset; may kick `002EB0D0`.

Scope corrections while scoping (recorded because they reverse EXP-104's
labels): `0017D470` is a 0x14-byte accessor (`001D50D0()` → `d[+0xC20]`), not a
context carrier; `00301140`/`00312280`/`00300FC0` form one shared
unlink-carrier tail family (~1085B head + tails) and stay scripted for a
separate package; `003BBD00`'s CRT/string closure stays scripted; `0024FE30`
stays scripted pending confirmation of its `30E360`-side call path.

## New executed facts

### `0030B770()` — global owner flags (no args)

Returns `d[local]` built from two globals:

| ret bit | source |
|---|---|
| 0 | `d[02089340] & 0x3080` nonzero (bits 7,12,13) |
| 1 | `b[022C2158] & 1` |
| 2 | `d[02089340]` bit 10 |
| 3 | `d[02089340]` bit 9 |
| 4 | `d[02089340]` bit 11 |

(`b770-zero`/`g3080`/`b7`/`ownb`/`bits`/`all` — full 5-bit map verified,
`owngl=0x1E80`+`ownb=1` → `0x1F`.)

### `0030B7F0(objrow, edx)` — per-object flags → packed dword

Early-outs: `rcx==0` or `d[obj] & 0x10` clear → ret 0 (`b7f0-null`,
`b7f0-noflg`). Then:

| lo bit | source |
|---|---|
| 0 | `d[obj]` bit 8 (`b7f0-lo` → 1) |
| 1 | `d[obj]` bit 30 **and** `edx != 0` (`b7f0-edx` → 3) |
| 3 | `b[obj+4] & 0x20` **and** `d[022C2160] - 5 > 1` (unsigned — values 5,6
    suppress: `b7f0-b4in`/`b4out`) |
| 4 | `q[obj+0x698]` nonnull **and** `b[rec+5]==0` **and** `b[rec+4]==0x1A`
    (`b7f0-rec1a` → 0x10) |

| hi bit | source |
|---|---|
| 0 | `0017D470()==1` **and** `q[obj+0x698]` nonnull **and** `b[rec+5]==0`
    (`b7f0-sgl1` → `0x10000`; `b7f0-sglgate` with `b[rec+5]=1` → 0) |
| 1 | `0017D470()==2` — `or bx, ax` ors the raw return (`b7f0-sgl2` →
    `0x20000`) |

`0017D470` is invoked **twice** per call (`b7f0-sgl1` asserts both entries).

### `0017D470()` / `001D50D0()` — singleton mode accessor

- `001D50D0`: `q[01F81428]` nonnull → return it; else `00210EC0(0x10E8)` alloc
  → `001CCB20(ptr)` ctor → store `q[01F81428]` → return. `d470-null` drives
  the alloc arm (both stubs logged once, singleton cell holds the block);
  `d470-sgl` drives the fast path (no alloc).
- `0017D470`: `ret d[singleton + 0xC20]` — the game-mode dword.

### `0030B9B0(row, row2)` / `0030B8E0(row, row2)` — the two wrappers

- `edi = (0030AB40(row, row2, 0) > 1)` when both args nonnull, else 0.
  `0030AB40` (already real) resolves each row's entity via `q[+0x10]`→`263C20`,
  requires `b[row] & 0x10` on both, then `ret = (computed == ebp) + 1` ∈ {1,2}
  (`b9b0-pair` drives ret 2 via `d[rec+0x64]` bit5 — `edx` bit1 arm of
  `0030B7F0` enabled).
- `0030B9B0` returns `(w(0030B770()) || w(0030B7F0(row, edi))) ? 1 : 0` —
  **low words only** (`b9b0-glob` → 1 via global bit1; `b9b0-null`/`none` → 0).
- `0030B8E0` returns 1 iff `0030B7F0`'s **high** word is nonzero — the
  `0030B770` result's high word is structurally 0 (`b8e0-lo` proves a nonzero
  low word returns 0; `b8e0-sgl`/`sgl2` → 1 via the `0017D470` arms).

### `00300140(objrow, edx)` — unlink-mark carrier (CASC arm)

- `edx != 0` → `003105D0(objrow)` first (stub — `b140-td`).
- Clears `q[+0x6F8]`, `d[+0x748]`, `d[+0x770]`, `q[+0x750]`, `d[+0x74C]` to 0;
  `d[+0x788] &= ~0x400`; `d[+0x6B0] &= ~2` (all verified against planted
  nonzero values — `b140-edx0`).
- `q[obj]` bit14 clear is **sentinel-gated**: when `q[obj] & 0x4000`, the
  clear is skipped iff `w[obj+0xBA0] == 0x113` (`b140-edx0` keeps bit14,
  `b140-clear` with `0x55` clears it); when bit14 is already clear the
  sentinel is `0x95`.
- Always sets `d[obj+4] |= 0x200000`.

### `003299B0(objrow, edx=msg, r8d)` + `002EB030(node, msg)`

- `edx == -1` → immediate ret, nothing written (`k99b0-minus1`).
- `ebx = (edx & 0xFFF) >= 0x100 ? edx | 0x5000 : edx` (`k99b0-low` → 0x50,
  `k99b0-hi` → 0x5300).
- `002EB030(q[obj+0x10], ebx)`: `b[node+0xD] &= ~1`, `b[node+0xF5] = 0xFF`,
  `d[node+0xEC] = 0`, `d[node+0xF0] = ebx`; `b[node+0x18] != 1` kicks
  `002EB0D0(node, q[node+0xC0], ebx, 1, -1.0f)` (`k99b0-kick` — scripted,
  args verified: rcx=node, rdx=planted `q[+0xC0]`, r8d=msg, r9d=1).
- Back on the row: `d[obj+0x5C] = ebx`; `d[obj+0x2C]` = `r8d` then cleared to 0.

### Inherited-call sites now real in `0030E360`/`0030BC0`/`00300CE0`/`00300530`

- `bc0-veto`, `ce0-veto`, `s530-veto`, `e360-owner-bail` now veto via the real
  composers: `ownb=1` drives `0030B770` bit1 → `0030B9B0`/`0030BC0` bail.
  `s530-veto` additionally records that `0030B9B0`'s nonzero vetoes **before**
  `0030B8E0` is reached.
- `e360-owner-chk`/`owner2-chk` assert real `0030B9B0`/`0030B8E0` entry counts
  via REAL-entry logging.

## Fixtures added (synthetic, disclosed)

`owngl` → `d[02089340]`; `ownb` → `b[022C2158]`; `g2160` → `d[022C2160]`;
`sgl` → `q[01F81428]` = planted block with `d[+0xC20]` = mode (absent → the
real lazy-alloc arm runs through `n210ec0`/`c1ccb20` stubs); `ent_b`/`ent_q`
→ `q[objrow+0x10]` entity node bytes/qwords; `row2` → second member row
(`flags`, `d{}`, `eb{}` entity bytes, `rec{}` `q[+0x698]` bytes) for
`0030AB40`'s pair compare. New stubs: `002EB0D0` (`kb0d0`, arg-capture),
`00210EC0` (returns a lazily-alloc'd harness block), `001CCB20` (returns its
arg — ctor-returns-this).

## Still scripted (disclosed, unchanged)

`00300FC0`/`00301140`/`00312280` (the shared ~1085B unlink carrier family —
next package), `003112F0` (executed in EXP-149 scope; the EXP-104 stub site is
unchanged), `003284D0` (`002FA3B0`/`003BBD00` formatter family), `0024FE30`,
`003BBD00`, `002EB0D0`, `003105D0`, `00210EC0`, `001CCB20`, `0046A800`,
CRT/import thunks.
