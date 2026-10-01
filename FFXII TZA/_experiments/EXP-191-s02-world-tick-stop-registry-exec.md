# EXP-191 — S-02 runtime: world tick `00314020` + system-stop registry execution record

Identity: `SWE2-ORACLE-UNIT-INSTALL-EXEC`
Board: `OPUS-REQ-ORACLE-S02-RUNTIME-WORLD-TICK-AND-STOP-REGISTRY`
Harness: `_experiments/evidence/s02-world-tick-stop-registry-exec/check.py` (Unicorn native replay; synthetic fixtures + disclosed stubs — MODEL-PROVEN setup / NATIVE-REPLAY bodies; `live_game: false`)
Result: **37/37, stable ×3** (three separate processes), zero faults.
Contracts covered: `CONTRACT-world-simulation-tick.md` (WT-1..WT-6), `CONTRACT-system-stop-registry.md` (SS-1..SS-7).

Executed bodies (all shipped bytes, entry-intercepted callees only):
`00226B30` init · `00225CD0` start/cancel · `00225EB0` stop-sweep · `00226280` apply · `00314410` latch · `0025BFB0` drain · `00314020` world tick · real leaf callees `263FF0`/`358940`/`359B80`/`861EC0`(memset).

## Stop-registry findings

### `00226B30` — init (leaf)

Verified: dirty `01FD46D0`/`01FD46D4` bitset/byte571 cleared; 56-record sweep writes `q[+0]=-1`, `b[+0x14]=0`; combined[0..1] at `01FD46A0`/`01FD46B8` get `q0=-1`, `d[+0x10]=-1`, `b[+0x14]=0`. (SS-6 baseline, `ss-init`.)

### `00225CD0` — start/cancel (`ecx`=idx, `edx`=fade)

- `b[01FD46D0]=1` dirty; `d[01FD46D4] &= ~(1<<idx)` — **clears** the pending bit (SS-6 producer).
- 3-manager fan-out: `263FF0(m)` = `02098E10 + m*0x288` (corrected base — doc had `0208E688`), gate `b[obj+0x10]&1`, rows `w[+0x1DE]`..`+w[+0x1D6]` via `358940` (ptr-array `q[obj+8]`, `d[arr]` bound, `q[arr+8+i*8]`=row) then `359B80` (row→`q[+0x30]`, 0 arm skips).
- Per row: `or d[+0x114]|=bit`, `and d[+0x110]&=~bit`; chain `q[row+0xC0]`: `or +0x178/+0x16C/+0x160`, `and +0x174/+0x168/+0x15C`; rax arm: `or rax+0x60/+0x58/+0x5C`, `and +0x54/+0x4C/+0x50`. Row writes verified (`ss-start*`).
- Record: `q[recA]=-1`, `q[recB]=-1`, `b14=0` both, `d[recB+0x10]=fade` (SS-4 producer).
- idx dispatch: `0`→`2DDC30`?`182DA0`; `0xC`→`182D60`; `0xD`→`recB q0 &= ~bit41` then `182D40`; `0xF`→`182D40`; else none. (`ss-start`, `-idx0`, `-idxd`.)

### `00225EB0` — stop-sweep

28-iteration scan of the active bitset: each **set** bit → clear it, dirty=1, same actor fan-out, record reset (`q0=-1`, bankB `-1`, `d10=-1`, `b14=0`), same idx dispatch. Idle bitset → no writes, no calls (`ss-stop`, `ss-stop-idle`).

### `00226280` — apply

- Gate: `b[01FD46D0]==0` → early `ret`, zero calls, zero writes (`ss-apply-gated`; SS-6 consumer).
- Loop `rax=01FD4410..01FD46B0` stride `0x18` (28 slots — bound is the cursor's own immediate; SS-3): `rdi &= q[rax-0x2B0]` (bank A), `rbx &= q[rax-0x10]` (bank B), `d[rax]` fade `>=0` → `ecx=min(ecx,edx)` then `d[rax]=-1` (consumed, SS-4); `q[rax-0x10] |= bit41` writeback (SS-5).
- Tail: `movups [01FD46A0]={rdi,q[rsp+0x40]}`, `movsd [01FD46B0]=q[rsp+0x48]`, `movups [01FD46B8]={rbx,q[rsp+0x28]}`, `movsd [01FD46C8]=q[rsp+0x30]`, `b[01FD46D0]=0`.
- **SS-1 verified two ways**: (a) `UC_HOOK_MEM_READ` on `01FD46D4` range during the whole apply → **zero reads** (`ss-apply-watch`); (b) identical combined/fade results with bitset `0` vs `0xFFFFFFFF` (`ss-apply-bits0`/`bitsff`/`ss-apply-bitset-invariance`).
- **SS-2**: AND semantics — all-ones banks → combined `~0`; any zero lane → 0 (`ss-apply-full`).
- **SS-4**: min-fade observed live as `226640`'s `edx` = `min(0x55,0x30)=0x30` (`ss-apply`); `-1` skips (all-`-1` → `edx=0` via `r12d=cmovns`).
- **SS-5**: `recB7 = 0x1 | (1<<41)` verified.
- Bit-test fan-out builds `w[0209215E]`/`w[0209215B]`/`w[02092162]` mask words and drives effectors `2E24C0`/`2E24E0` (bit39), `2EA8B0/E0` (bit24→edx), `25A5D0` (bit30), `226640` (`ecx`=bits8..D-all-set flag, `edx`=fade min — `ss-apply-full` gives `ecx=1`), `2547C0/840` (u16 masks), `35B4B0/510` (bit29→`cl` 5/0xFF), `2DF370`×3/`2DF640`×2 (bits 32/33/35/40/44 msgs), `2EBBF0` (bit35). All stubbed, args captured.
- `b[01FD46D1]` byte571: `!=0` → cleared by apply (`ss-apply-571`, fade arg 9 reached callee).

## World-tick findings (`00314020`, `ecx`=mode)

- **WT-1** — mode consulted five times: mode-0-only `358C60`+`3DF760`(edx=1..5)+substep loops; mode-1 slots 3..4 block; post-loop `2623A0` dispatch (mode0→slots 0..4, mode1→3..4, mode2→none); `358EE0(mode)` tail. All three modes' call sets verified (`wt-mode0/1/2`).
- **WT-2** — `0025BFB0` drain runs **before** the first mode test, under all modes (`wt-drain-live` under mode1: `26CE60(2),(0)` + `2628B0(2),(0)` with mask `0x5`, mask cleared).
- **WT-3** — `d[022C2548]=1` on entry, `=0` before ret in every mode (cannot leak within this body; the image-wide 3-access census remains a static claim — the two writes are verified, the count is not re-censused here).
- **WT-4** — `d[01EED060]` latched request consumed once: `cmovns` → stored `-1` (`wt-latched`, `wt-mode*`). `d[01EED064]>=0` → `17D280`×2 + `32FC30(edx=req, ecx=0)` then `-1` (`wt-deferred`). `00314410` first-writer-wins: `d[01EED060]<0` → `26A5F0(4)` then store; `>=0` → untouched (`wt-latch-store`/`held`).
- **WT-5** — five slots (`cmp ebx,5`), sixteen substeps (`cmp esi,0x10`): `267310`-gated calls `234590`/`25D9E0`/`3DB1F0` reach **80 = 16×5** with gate=1, **5** with gate=0 (substep 0 is ungated — `test esi,esi; je` runs the calls). `2E0D90`/`268D00` run only at `esi==0`. Note: the `267310` gate is **inverted** vs the naive reading — `test eax; je` *skips* the slot calls.
- **WT-6 — executed** (second pass, real bodies + stubbed leaf layer):
  - `267310` = 5-insn leaf: `b[02098E10 + i*0x288 + 0x201]` — a per-slot flag byte; both arms verified (`wt6-gate-on`/`-off`).
  - `234590`: `test ecx,ecx; jne` → slots ≠0 are a **9-insn epilogue** (zero calls). Slot 0 → `02089340` flagword writes + ~37-callee chain (`wt6-234590-s0`/`-s3`).
  - `234520`: `test ecx,ecx; jne` → same early-ret. Slot 0 → `23B040`/`313DB0`/`319090`/`16D6A0` + one-shot callback `call q[0208E6A8]` then clears the cell (`wt6-234520-s0` verified with a planted `ret`-stub).
  - `25D9E0`: real work **every** slot (obj flag bytes `+0x10/+0x11`, publish `q[02099D70]=obj`, counters `d[+0x24]++`/`d[+0x38]++`) — but two arms are slot-0-only: `25B740` inside the row loop and `25B600` at the tail (`wt6-25d9e0-s0`/`-s3`).
  - `3DB1F0` (second inner loop): all slots; `3DB6E0(row)` fires per row **unconditionally** + `b[row+0x63]>>=1`; `b[+0x63]` gates only the inner `b[q[+0xA0]+0x11+k*0x14]==1→2` scan (`wt6-3db1f0-s2`/`-idle`).
  - In-context (`wt-mode0-wt6`, all five bodies real): `234590`/`234520`/`25D9E0`/`3DB1F0` entered **80×** each (16 substeps × 5 slots), `267310` **150×** (both inner loops), while the slot-0 chains fire only **16×** (`32A150`×32 = 2/substep; `313DB0`/`319090`/`25B740`/`25B600`×16). **WT-6 confirmed and refined**: `234590`+`234520` are slot-0-only; `25D9E0` works all slots but still carries slot-0-only arms.
  - Measured interaction: with all-stub callees the flagword ends `0x10D`, so `234520`'s `(d&5)==1` callback gate stays closed in-tick — the callback fires in the direct case only.
- Tail: `228480` `eax!=0` → skips `36FD90`; `362DA0` `eax!=0` → skips `362DB0`+xmm/minss timing block (`wt-tail-branch` vs `wt-mode0` traces).

## Drain detail (`0025BFB0`)

Mask `d[02099ABC]`, two passes over bit-values `0x10..1` (5 bits): pass1 gated on `mask&1` → `26CE60(4..0)` per set bit; pass2 unconditional → `2628B0(4..0)` per set bit + `mask &= ~bit`. `xmm` cells `0209A1F0`/`0209A200` zeroed between passes. Zero mask → immediate ret, no calls.

## Scripted boundaries (all disclosed, args captured)

WT-6 second pass: `267310`/`234590`/`234520`/`25D9E0`/`3DB1F0` run **real** in the `wt6-*` /
`wt-mode0-wt6` cases (a `realbodies` case key bypasses the stub for those addresses); their ~95
leaf callees stay scripted (`w*` tags). In the base tick cases they remain `t*` stubs.

Registry msgs: `182D60`/`182D40`/`182DA0`/`2DDC30`(ret). Apply effectors: `2E24C0`/`2E24E0`/`2EA8B0`/`2EA8E0`/`25A5D0`/`226640`/`2547C0`/`254840`/`35B4B0`/`35B510`/`2DF370`/`2DF640`/`2EBBF0`. Drain `26CE60`/`2628B0`; latch `26A5F0`. Tick callees (~50): `16D6A0`/`3EB9A0`/`3DAA20`/`3DA2F0`/`3DD210`/`17D280`(alloc-stub)/`32FC30`/`3DAA40`/`46AFA0`/`358C60`/`268650`/`25D650`/`255810`/`37D890`/`25D640`/`234590`/`25D9E0`/`3DB1F0`/`234520`/`2E0D90`/`3DF760`/`267310`(ret)/`268D00`/`2623A0`/`358EE0`/`2E09A0`/`359800`/`3DE640`/`2E0940`/`37C1A0`/`3E7EC0`/`228480`(ret)/`36FD90`/`2F1770`/`2EF910`/`36E1E0`/`3DEB30`/`3DF670`/`3606E0`/`362850`/`362DA0`(ret)/`362DB0`/`265760`/`259AF0`/`2DEBA0`/`361700`/`3E7650`/`25D950`/`263660`/`2EEEB0`/`3DAC70`.

## Fixture (all synthetic, disclosed)

Registry slots `slots{}` per-index a/b masks + dword10/b14; manager array at `02098E10` (3 mgrs × rows; `b[obj+0x10]`=1, head/count, ptr-array rows with `q[+0x30]=0`, chain obj at `row+0xC0`); statics `01FD46D0/D4`, `01EED060/64`, `022C2548`, `02099ABC`, `0209A1F0/0200` (0xAA/0xBB-prefilled to prove zeroing).

## Invariant outcomes

| Inv | Result | Evidence |
|---|---|---|
| SS-1 | **executed** | zero bitset reads (mem-read hook) + bitset-invariance |
| SS-2 | **executed** | AND semantics ~0→~0, 0-lane→0 |
| SS-3 | **executed** | 28-slot cursor `01FD4410..01FD46B0` stride `0x18`; only `q0` ANDed |
| SS-4 | **executed** | fade min 0x30 via `226640` edx; per-slot `-1` writeback |
| SS-5 | **executed** | `recB |= bit41` unconditional |
| SS-6 | **executed** | dirty=0 → early ret; producers set dirty=1 |
| SS-7 | partially | 3-manager loop iterated unconditionally; per-request reach bit not isolated |
| WT-1 | **executed** | 5 consults; mode-specific call sets for 0/1/2 |
| WT-2 | **executed** | drain before mode consult, observed under mode1 |
| WT-3 | **executed** (in-body) | TIP 1→0 lifecycle; image-wide census not re-verified |
| WT-4 | **executed** | latch consume `-1`; deferred `32FC30(edx)` + `-1`; `314410` FWW |
| WT-5 | **executed** | `cmp 5`/`cmp 0x10` immediates; 80 vs 5 call counts |
| WT-6 | **executed** | 234590/234520 slot-0-only (9-insn epilogues); 25D9E0 all-slot + slot-0-only arms; counts 80/150/16 in-tick |

## Addendum - OPUS replays adopted (SWE2-ORACLE, 2026-09-30)

Adopted under `ORACLE-NOTICE-OPUS-287-S02-REPLAY-TO-ADOPT`. The text above is unchanged; these later records supersede
two of its cells.
- **WT-4 / `0026A5F0`.** The stub this record used for `0026A5F0` is superseded. OPUS ran it as shipped code on WT-4
  in a copy of this harness (`fc379f25f`, `_index/candidates/s02-opus-replay-26a5f0-and-reach/`). Case
  `wt-latch-store-real` passes, and 61/66 cases are identical over three runs. All 37 original cases pass. The
  published `check.py` is untouched.
- **S-02 exposure SS-7:** the "partially" row is superseded. OPUS showed this record ran `00225CD0`'s hard-wired 3-manager loop,
  which is not the per-request reach (`2211cd101`, block 260). `00226BE0` then ran as the prelude calls it, for all 28
  stop slots: slot 11 alone reaches 3, and the manager loop walks exactly the computed breadth (`5bde53415`,
  `_index/candidates/s02-opus-replay-stop-reach-executed/`, block 331).
- **Correction carried from the replay.** The staged patch note said `00227680` makes no calls. That is wrong: ids
  0/12/13/15/17 leave it into live-state reads (`fc379f25f`).
- **Status.** SWE2-AUDIT-SEM scored S-02 runtime MET (`3c8bcc7af`). Evidence class of the adopted runs:
  NATIVE-REPLAY, OPUS-executed, not re-run by ORACLE.
