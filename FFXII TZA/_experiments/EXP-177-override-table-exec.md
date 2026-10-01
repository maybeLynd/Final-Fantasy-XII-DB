# EXP-177 — `0x209A3E0` bit-override mux family execution-validated

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; the
`3ED0xx` init calls inside `26E960` are scripted boundaries (tagged
`s3ed***`, return 0). No claim of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **190/190, stable ×3**
(three independent processes).

## Correction to EXP-173 record

`22F8B0`'s mask-merge reads base **`0x209A3E0`**, not `0x209A2D0`
(that is `230A40`'s table). The read-trace addresses cited in EXP-173
(`0x209A3E0`/`0x209A5E0`) were in fact consistent with this base.
`22F8B0` reads entry `0x209A3E0 + ((flags>>0xD&0x1F)+0x20)*8` — i.e.
absolute range `0x209A4E0..0x209A5D8`.

## The `0x209A3E0` table is a per-group bit-override mux `{A, B}`

Entry layout: `{d A = override-enable mask, d B = override bits}`.
`22F8B0` merges `merged = (B & A) | (flags & ~A)` — bits where A=1 take
the table value, bits where A=0 pass the entity's own `d[ent+4]`
through. Skip iff merged bit31.

- **`26E130(idx)`** — `A = 0` (release all overrides) + sweep.
- **`26E150(base,count)`** — `A = 0` for `count` slots, sweep each.
- **`26E850(slot, shift, width)`** — `A &= ~(((1<<width)-1) << shift)`:
  release a bit-field override. Proven: `0x1234` → `0x1204` for
  shift 4 width 3; B untouched.
- **`26E880(slot, val, shift, width)`** — `A |= field_mask`,
  `B = (B & ~field_mask) | (val << shift)`: install an override.
  Proven: A `0x1234`→`0x1274`, B `0xAAAABBBB`→`0xAAAABBDB` for
  val 5 shift 4 width 3.
- **`26E8C0`** — `q[0x209A660] = rcx` (one pointer store).

## `26E960(ctx)` — the egrid installer

Executed with `3ED0xx` init calls stubbed (disclosed boundary):

- `q[0x209A670] = ctx` **before** the null check — null stores 0 and
  early-outs (proven both ways).
- `q[0x209A678] = ctx+0x40`, `q[0x209A680] = ctx+0xA8` — the two
  sub-contexts `26E100`/`22F8B0` consume.
- For lane 0 only: `q[0x209A690] = q[q[ctx+0x40]+0x30]`,
  `q[0x209A6A8] = q[q[ctx+0x40]+0x38]` — pulls two pointers out of the
  first sub-record.
- `d[0x209A6FC] = 1`, `d[0x209A708] = 1`, `f[0x209A6F4]` = image const
  `f[0x8B5778]`, `d[0x209A6D0] = 3ED0B0()` ret.
- Clears the table: observed **0x50 `3278D0` sweeps** (entries
  `0x209A3E0..0x209A658` lo dwords → 0), then `3ED020` ×3 on
  `0x209A6F0`, `3ECFD0(0x209A370)`, `3ED140`, `3B6BA0`, tail
  `jmp 3ED7B0`.

## `22F8B0` mux executed both directions

- `t22f8b0-muxin`: entity flags 0 but A=B=bit31 → merged bit31 →
  **skipped** (table can *inject* the skip flag).
- `t22f8b0-muxoff`: entity flags bit31 but A=bit31, B=0 → merged 0 →
  **tested** (table can *clear* the flag). Fills the EXP-173 gap —
  the merge was previously only exercised with a zeroed table.

## Callers (static)

`26E150`+`26E130` pairs at `0x3791DB/0x37922C/0x37927B`; `26E880`/`26E850`
bulk-init calls throughout `0x3791FE..0x379607` — a table-builder
function in `0x379100..0x379700`. `26E8C0` called once from `0x2F6DEC`.
