# EXP-216 — display-list append chain `2B4730`/`3A1DB0`/`36F360` promoted real

**Status:** complete — **523/523 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`d0bdfc304277cc62fbcd1457b4df3c833117dcd402b92f52415cc1cb5aa947a8`),
zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..215; 521 inherited cases + 2 new direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-215 kept the display-list append scripted: `2B4730` unconditionally
dereferences `q[0209CC48]` (ctx48), `q[0209E5A0]` (command-list cursor)
and the double-buffer ring globals around `0x2EBEFC0`–`0x2EBEFFF`, none
of which were planted. This round plants them and promotes the whole
append chain — the publish drain, the double-buffer ring flip, and the
command-stream terminator/bookkeeping helper.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `002B4730` | display-list drain/append — `rdx = q[0209CC50]-0x10` (pending record header), `q[0209CC50] = rdx`, `d[rdx+0xC] = 1`; `r8 = q[0209E5A0]` list cursor, `edx = (rdx - r8)>>4` = record count → `d[r8] = count|0x10000000` header, `d[r8+4]=0`, `d[r8+8]=0x10000000`, `d[r8+0xC] = count<<16 | 0x6C008150` cmd; terminator record at `r8+(count+1)*0x10`: `q[+0]=0x10000000`, `d[+8]=0x15000000`, `d[+0xC]=0x13000000`; `q[0209E5A0] += 0x10`; `q[ctx48+8] += movsxd(cursor-low32)&~0xF` align-add; then real `3A1DB0`; `ecx!=0` tail: `q[0209CC48] = 02EDF9C0 + d[02EDF050]*24` slot-table entry and both cursors restored from `q[slot+8]` |
| `003A1DB0` | double-buffer ring flip — `cur = d[02EBEFF0]` → writes `1-cur`; `rcx = q[02EBEFC0 + cur*24]` current slot base, `edx = (q[02EBEFC8+cur*24] - rcx)>>4` record count → `36F360`; then `q[02EBEFE0](slot1 cursor cell) = q[02EBEFD8]` (slot start reset) |
| `0036F360` | command-stream terminator + bookkeeping — early out on `edx==0`; walks to the `0x30000000` last-record header (`r9 = rcx + edx*0x10`), `d[r9-0x10]` checked `==0x30000000`, count capped at `0x200`; writes `q[r9]=0x10000000` terminator + `q[r9+8]=0`; fixed-BSS bookkeeping cell `d[02EBA3F8]` rewritten (masked cursor, count, then `0x100` on completion) |

## Call sites now real

- `0x2AA6xx` region — `2A9F00`'s `d[ctxo+0x10D4]>=0x14` batch flush
  now chains into the real append/ring-flip path (still gated ≥0x14;
  the two direct-entry cases exercise the full body deterministically).
- Direct entry `rcx=1` (`b4730-flush`) additionally covers the
  ebx-gated ring-slot-table cursor-restore tail; `rcx=0`
  (`b4730-noflip`) verifies it is skipped.

## New fixtures (disclosed)

- `ctx48o` — allocates a `ctx48` object and plants
  `q[0209CC48] = ctx48o`, `q[ctx48o+8] = case.c48c` (scalar `ctx48`
  gate still supported for arm-level callers).
- `b4730p` — direct-entry display-list fixture: `q[0209CC50]` points
  `listcur+0x30` inside the `q[0209E5A0]` list buffer (two pending
  records), ring-buffer `ringbuf` allocated, ring globals planted:
  `02EBEFC0`=slot0 base, `02EBEFC8`=slot0 end (+0x20 → count 2),
  `02EBEFD8`=slot1 base (+0x800), `02EBEFE0`=slot1 cursor,
  `02EBEFF0`=current slot 0, `d[ringbuf+0x10]=0x30000000` last-record
  header.
- `q[0209E5A0]` — command-list cursor, always planted (0x1000 buffer).

## Verified outputs (asserted)

- List records: `d[lc]=0x10000002`, `d[lc+8]=0x10000000`,
  `d[lc+0xC]=0x6C028150`, terminator `q[lc+0x30]=0x10000000` /
  `d[+0x38]=0x15000000` / `d[+0x3C]=0x13000000`, drained header
  `d[lc+0x2C]=1`.
- Cursors: `q[0209CC50]` → drained head (`lc+0x20`);
  `q[0209E5A0]` → `lc+0x40` (noflip) or `q[slot+8]` (flush);
  `q[ctx48o+8]` += `(lc+0x40)&~0xF` low32.
- Ring: `d[02EBEFF0]` 0→1, `q[02EBEFE0]` reset to slot1 base
  (`ringbuf+0x800`), `q[ringbuf+0x20]=0x10000000` terminator patch.
- Flush tail: `q[0209CC48]` → `02EDF9C0 + d[02EDF050]*24` slot
  entry, both cursors restored from `q[slot+8]`/`+0x10`.

## Corrections of record

- `2B4730`'s ctx48 use is a **qword align-add** `q[ctx48+8] += cursor
  & ~0xF`, not a pointer chase — a scalar ctx48 gate is insufficient,
  hence the `ctx48o` object fixture.
- `36F360`'s several RIP-relative bookkeeping accesses all resolve to
  the **same cell** `0x2EBA3F8` (write masked cursor, write count,
  read twice, final `0x100`) — a single compact ring-state dword, not
  three cells.
- `3A1DB0` reads the **current** slot record (count from its own
  pointer pair) but resets the **other** slot's write cursor — the
  flip prepares the previously-idle buffer for the next batch.

## Still scripted / not claimed

`2AFDC0` render-submit internals, `17FC90`/`17F7C0` emit internals,
`2AEB20` nested catch-all, `2B1FB0`, `17FD30`/`2B1ED0`/`17F880`/
`17F850`/`17FA10`/`17FB00`/`17F920`/`17F9C0`/`17F940`/`17FAE0`/`17F8C0`
font shims, `39C4A0`, `2AC2F0` decoder, `808C40` cookie. Ring-slot table
`02EDF9C0` + slot buffers are fixture-planted; no live-game claim —
`NATIVE-REPLAY`, `live_game: false`.

## Verification

`python check.py` → 523/523 pass, zero unexpected faults; three
independent runs → byte-identical `result.json` SHA256
`d0bdfc304277cc62fbcd1457b4df3c833117dcd402b92f52415cc1cb5aa947a8`.
