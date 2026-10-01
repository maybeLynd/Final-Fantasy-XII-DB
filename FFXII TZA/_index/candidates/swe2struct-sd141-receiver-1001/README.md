# SD-141 receiver/consumer trace — `00604750`'s `r14` and the 0x598-byte snapshot (SWE2-STRUCT, 2026-10-01)

Answers [`OPUS-REQ-STRUCT-SD141-CONSUMERS-1001`](../auditspec-review-sd141-0930/REVIEW.md):
the receiver type of `00604750`'s `r14`, the receiver of the 0x598-byte snapshot it builds at
`rbp+0x270`, and the readers of the staged slots' `+0x550`/`+0x554` and of `[r14+0x5D4]` /
`[r14+0x5DC]`, handed-on bases included. Static, the certified image; checker
[`sd141_receiver.py`](sd141_receiver.py) / [.out](sd141_receiver.out), FAILS 0.

## The receivers

- **`r14`** = the CPU-visible (mapped) address of a slot in a **D3D11 ring of buffers**.
  `006097B0(rbx, &out)` at `00604BEC` returns it at `00604BF9`; it picks the next ring index
  (`[rbx+4]+1 mod [rbx+0x18]&0x7fffffff`), busy-waits on `slot+0xC` via `005CCB80`, and maps via
  `00626060(rbx, index, &out)` at `00609849`. `rbx` is the 80-byte ring record
  `rsi+0x4A8 + cursor*80` (`00604929..00604931`). Commit: `0062C300` at `00606071`, writeback
  `next-index -> [rbx+4]`, mapped flag `-> [rbx+8]` at `006060C9/006060CD`. Per UQ-22's scene-wide
  map the mapped layout is `SceneWideParameterConstantBuffer` (0x5F0 B); `+0x5D4`/`+0x5DC` are
  `mShadowFlyingFadeSpeed` / `mShadowFlyingFadeRange`.
- **The snapshot** (`rbp+0x270`, 0x598 B) is a frame-local struct owned by `00604750`'s receiver
  `this` (`rsi = arg0`, `006047D7`). `006084B0(rdi=snapshot)` fills it: its `+0x2A0` tail is the
  verbatim 0x2C0-byte copy of global block `02CB8160` (leaf `005DEC50`, reads at
  `005DF3A0`/`005DF3AC`), so the flying-fade pair `02CB8410`/`02CB8414` lands at snapshot
  `+0x550`/`+0x554`.
- **`this`** owns: `+0x488` u16 element stride, `+0x490` element array (busy counter at `+4`),
  `+0x498` element count, `+0x4A8` the 80-byte ring-buffer record array, `+0x4B0` the lock
  (`005CD4F0`/`005CD820`), `+0x4D8` the cursor, and `+0x4E0` the **two 0x598-byte staged slots**.

## Readers (complete CPU-side census)

| destination | readers | verdict |
|---|---|---|
| snapshot `+0x550`/`+0x554` | `00605F66`/`00605F88` (`movss` → `r14+0x5D4`/`+0x5DC`); memcpy `006048C2` and `005DF3E0` at `00604913` read the bytes wholesale into the two staged slots | CPU reads exist |
| staged slot `+0x550`/`+0x554` (`this+0x1030`/`+0x15C8`) | **none** — `00604750` is the only function containing an imm-`0x598` multiply; no `.text` operand carries `disp 0x1030`/`0x15C8`/`0x1034`/`0x15CC` on a same-receiver base (the one non-stack `+0x1030` hit, `002BEED0`, shares zero fingerprint fields); the slot pointer never escapes the two copy calls | **write-only staging for the pair bytes** |
| `[r14+0x5D4]`/`[+0x5DC]` | no CPU read-backs — `r14` is write-only inside `00604750` (291 stores, 0 non-`lea` loads) | GPU-side only |

## Answer

The flying-fade pair's **only consumer is the GPU**: `00604750` copies it from the snapshot into the
mapped `SceneWideParameterConstantBuffer` at `+0x5D4`/`+0x5DC` each call. Per OPUS's
[`sd141-gpu-consumers-1001`](../sd141-gpu-consumers-1001/README.md) record (uncommitted at trace
time), 517 `phyredefaultlitshader.fx` blobs mark both variables D3D_SVF_USED — the same 517 that
read the non-flying pair. The two staged slots at `this+0x4E0`/`+0xA78` receive the pair bytes as
part of the whole-struct copies but nothing reads those bytes back: the staging double-buffer is
write-only for this pair (it may still serve whole-struct consumers — the slot pointer just never
leaves `00604750`'s copy calls on any path).

Entry to `00604750` is indirect: both raw `rel32` candidates decode mid-instruction (false
positives), and the only data reference is a `.rdata` rva32 jump-table entry pointing at the
`0x6048D0` case arm — consistent with a message/switch dispatch, same pattern as the order-handler
table at `01EEC460`.

## Limits

- Which `this` type owns the ring (`rsi`) is not named in the type store; the field census above is
  the structural signature (+0x488/+0x490/+0x498/+0x4A8/+0x4B0/+0x4D8/+0x4E0).
- The staged slots' other bytes (the non-pair 0x594) are equally un-read by CPU code — the "no
  reader" finding is for the pair fields specifically; a consumer taking `this` could still read
  them via the cursor formula, but only `00604750` computes it.
- The GPU-side claim rests on OPUS's blob census, not re-derived here.
