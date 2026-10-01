# SD-21: the unread remainder of the mix path, read (OPUS, 2026-09-30)

Register row SD-21 was registered by SWE2-DATA (`f7a3292bd`, sqex-sd-sound-driver-architecture.md §2a/§2b/§2e). It
lists five unread parts:
- the two SIMD decode kernels inside `007E0B60`;
- the eleven other `CoreSourceVoice` slots, and the six each on `CoreSubmixVoice` / `CoreMasterVoice`;
- the pool take `007DF750`;
- what distinguishes the factory's two paths;
- who calls start / queue after the factory returns.

This record reads all five. It is static. The checker is `sd21_mix_remainder.py` (output
`sd21_mix_remainder.out`, `FAILS 0`). It uses `Tools/analysis-kit/gfz-scripts/retool.py`.
**Status proposed: ANSWERED (static).**

## The core voice interface (OPUS, V1-V7)

The vtables are `01CB8290` `CoreMasterVoice` (7 slots), `01CB82D0` `CoreSubmixVoice` (7) and `01CB8360`
`CoreSourceVoice` (17), each named by RTTI. Fields are named by offset only.

| slot | `CoreMasterVoice` | `CoreSubmixVoice` | `CoreSourceVoice` |
|---|---|---|---|
| 0 | deleting destructor: class destructor, then the SEAD free `007AD450` | same | same |
| 1 | type id **1** | type id **2** | type id **3** |
| 2 | `s16 [+0x74]` | `s16 [+0xCC]` | `[+0xB0]` queued-buffer count (§2c) |
| 3 | under a lock, sets byte `+0x70` and rewrites an array through `007AECE0` | same, byte `+0xC8` | **start** `007E2710` (state ← 3, §2b) |
| 4 | returns 1 (the shared stub `007BD590`) | `[+0x88]` send count | under the lock, state ← **2** (stop) |
| 5 | get entry `r8`: only index 0, returns `{0, [+0x5C]}` | get 16-byte send `r8` from `+0x38` (bounds `+0x88`) | state ← **4**, plus fields `+0x88` / `+0x290` (flush) |
| 6 | set float `[+0x5C]` (index 0 only) | set send `r8`'s float level | set floats `+0x100` and `+0x104` |
| 7–16 | — | — | 7: set `+0x108`, refused in states 0 and 4 · 8: write the `+0x10C` array (`007AECE0`) · 9: **enqueue** `007E0A40` (§2c) · 10: get `+0x100` · 11: write an array through `007AECE0` · 12 / 13: get `+0xAC` / `+0x90` · 14: send count `+0x268` · 15: get 16-byte send from `+0x218` · 16: set a send's float level |

## Pool, factory and callers (OPUS, F1-F3)

- **The pool take `007DF750`.** Under the pool's critical section (imports `EnterCriticalSection` / `LeaveCriticalSection`),
  it pops the free-list head `[pool + 0x30]` (next link at `node + 0`), counts it in `[pool + 0x48]`, and returns the
  node or null.
- **The factory `007AEA20`'s two paths.** Its 10th argument (byte `[rsp + 0xa8]`) chooses:
  - **flag 0:** a pooled voice from pool `02EAD250`, registered by `007AF380` in list `02EAD2A0` under lock `02EAD138`;
  - **flag set:** a `0x2B8`-byte, 16-aligned allocation through the SEAD allocator hook (`007AD460`, header
    `0x5EAD5EAD`), zeroed, registered by `007AF490` in list `02EAD300` under lock `02EAD160`.
  - Both paths construct it with `007E0650`, take a second node from pool `02EAD200`, and open it with the caller's
    callback (`007E0980`).
  - By caller (SD-20): `ExternalSourceVoice` passes 1 (the heap path), `Voice` passes 0 (the pool), and
    `HCAMixerVoice` passes a variable.
- **Who starts and queues a created voice.** The owners call through the voice they keep at `owner + 0x68` (`+0x48`
  for `HCAMixerVoice`):

| owner | start (slot 3) | queue (slot 9) |
|---|---|---|
| `ExternalSourceVoice` | `007B9050` (right after creating, `007B9355`), `007B9AF0` | `007B9590` |
| `CRI::HCAMixerVoice` | `007DCE20` (`007DD011`, after queueing) | `007DCE20` (`007DD007`) |
| `Voice` | `007EDA60`, `007EDAB0` | `007EAA60` |

## The SIMD kernels (OPUS, K1-K3)

The page's "two SIMD decode kernels" are two source-format paths (16-bit and the other format, §2a). Each exists in
a unity-rate and a resampled form, and each is specialised on the source channel count `r9d`:
- `cmp r9d, 1` / `cmp r9d, 2` at `007E100E` / `007E108D` (unity), `007E1378` / `007E143A` (resampled) and `007E1796` /
  `007E1882`, plus `cmp r9d, 4` at `007E19CF`;
- then a general case that accumulates channel contributions with `addps` (16 of them in the body).

**Every variant computes the same thing per output frame** (K2, the unity mono 16-bit case at `007E1020`–`007E1086`):
1. the source sample, widened with `cvtdq2ps` and broadcast,
2. times the 8-wide per-output-channel gain vector (`xmm8` / `xmm7`, the `+0x10C` table with the format scale folded in,
   §2a),
3. times the ramped gain (`xmm6`, stepped by `xmm12` each frame).

The result is stored as **8 output channels, two `movaps`, 32 bytes, at the output stride**. The position double
`+0x98` advances by the step each frame. The body holds 48 such paired stores (K3). So the kernels spread each source
frame over 8 output channels with per-channel gain and a per-tick gain ramp. The resampled forms interpolate the
sample first, with the linear arithmetic §2a already reads.

## Limits (OPUS)

- **The kernels, by pattern.** Only one variant is read instruction by instruction (K2). The others are identified by
  dispatch and store pattern (K1, K3), not re-read one by one.
- **Pattern-found callers.** The start / queue call sites are found by pattern: a call through `+0x18` / `+0x48` on a
  value loaded from `owner + 0x68` / `+0x48`. A caller that holds the voice elsewhere is not listed.
- **Field names.** Fields are named by offset. What `+0x100` / `+0x104` / `+0x108` mean (volume, pan, pitch are the
  obvious readings) is not claimed.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
