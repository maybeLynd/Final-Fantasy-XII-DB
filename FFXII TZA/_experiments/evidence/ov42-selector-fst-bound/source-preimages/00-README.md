# What each FABLE request to ASTRA cannot settle from static evidence (FABLE, Claude Opus 5.5, 2026-09-30)

User rule, 2026-09-30: neither FABLE nor OPUS may declare a question "ASTRA/live-only" because its register row says RT.
The request must state the **specific fact** that A (image) / B (authored data) / original-code evidence cannot
resolve, and **ASTRA has final method-selection authority** for the empirical closure.

This record applies the rule to FABLE's open requests to ASTRA. For each request it gives one of two things:
- the fact that no static reading can supply, with the reason; or
- **static work remains**: FABLE takes that part back and does it before any live work is asked.

Wherever a request names probe sites, breakpoints or watches, they are **suggestions**. ASTRA chooses the method,
including a static or original-code method if ASTRA finds one. A request's "decision" list says what each possible
result would settle; it does not bind the method.

## FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929 (record `../ov-rt-probes-0929/`, commit `88d789a71`)

| item | fact no static reading supplies | or: static work FABLE takes back |
|---|---|---|
| (1) OV-5/8 (c), base `01F83530` | none stated by FABLE. This item is AQ-ARENA's remainder; its fact is stated (or not) in `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`, and FABLE adds no claim that it is live-only | - |
| (2) OV-5/8 (d), over-reservation | **withdrawn from ASTRA.** Every in-image writer the census reaches keeps reserved <= total (notes section 2); the open part is whether a copy through a passed pointer writes region A, which is an original-code question | FABLE: invert the census - every store whose base register can hold a pointer into the state block `021B290C` region A (memcpy-style copies, the save-image load into `02164280`, the snapshot restore `0030FAA0`), with a positive control; then answer (d) statically |
| (3) OV-16, same-key reuse | whether, in shipped script execution, an issuer re-arms a request with the same (channel, continuation offset) **before** its requestee consumes the earlier one. That order is set by the interleaving of two script threads across frames, which depends on each requestee's script progress, not on a single code path | FABLE first: the authored scripts (B) can show which request sites could re-arm at all (a non-waiting request inside a loop, or reachable twice without a wait). If none can, OV-16 closes statically and the probe is not needed. Only the candidates that remain need an observation |
| (4) OV-19, owner requests | only the deferred-free case: whether an owner is deleted while its read is in flight. That is the order of a delete against an IO completion, and it depends on host IO time | the rest (issue/completion order) is static and already answered in the notes; the timing half settles no claim |
| (5) OV-29, title assets | whether the title is torn down while a ticket is still pending, or message 16 arrives after teardown. Both depend on when the player leaves the title relative to host IO completion | - |
| (6) OV-33 (i), writer set of `0215EFF4` | **withdrawn from ASTRA.** A write watch here would test the completeness of a static census; that is static work | FABLE: census every store through the pointer `01F82CC0` (every load of the cell and every store through the loaded register), with a control |
| (6) OV-33 (ii), (iii) | whether a request in shipped play takes a status-less exit or returns a negative status. That depends on which ids the running game requests | FABLE first: the requested ids come partly from authored data (B). Where the id set is static, check it against the file-size tables; only ids built at run time remain for an observation |

## Other open FABLE requests to ASTRA (READY)

| request | fact no static reading supplies | or: static work FABLE takes back |
|---|---|---|
| `FABLE-REQ-ASTRA-UQ146-IN-PROCESS-FORMATTER-READ` | the stack use of the **installed** ucrtbase.dll's own frames. That is host library code outside the certified image; its version varies by machine | - (ASTRA may choose to read the installed DLL's code instead of running it) |
| `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` | whether battle play reaches "summoner KO while the summon is active". That depends on AI and player actions | FABLE first: whether a summoner KO ends the summon **before** the recompute `003135C0` can see it is a code-order question; FABLE reads the summon teardown path and its order against the recompute. If the summon always ends first, UQ-147 closes statically |
| `FABLE-REQ-ASTRA-PC1-OVERRIDE-DWORD-WRITE-WATCH` | none, for shipped code. The only writer a watch could find that static reading cannot is code outside the image | **withdrawn to FABLE**: the census so far is rip-relative only. FABLE runs the image-base-relative and pointer-derived store census for `01E02804`/`01E02810` before any watch is asked |
| `FABLE-REQ-ASTRA-OV10-OV42-REACHABILITY` | (OV-10) the largest number of requests one actor has outstanding at once under shipped scripts and events. That is a run-time concurrency, not a code path. (OV-42) whether a negative index reaches the owner submit in play. That depends on the run-time id | - |
| `FABLE-REQ-ASTRA-OV21-BANK-REACHABILITY` | whether two owners register the same key concurrently, and whether the bank fills. Both depend on run-time load concurrency | - |
| `FABLE-NOTICE-ASTRA-GG1-SHARPER-CAPTURE` | a notice; it already leaves the method to ASTRA | - |
| `FABLE-REQ-ASTRA-RT-REMAINDERS-0929` | superseded by the probes request above; to be closed by its assignee | - |

## Older FABLE requests to ASTRA (BLOCKED)

The fifteen BLOCKED requests were filed before this rule. They are `LEDGER`, `STATE-ROUNDTRIP`, `REGFILE-REUSE`,
`KIND-INDEX-TRACE`, `OLD-SAVE-LOAD`, `EO3-PATH-POINTER`, `REAR-HALF-VOICE-PAN-LISTENING-TEST`,
`MT-CURSOR-ACROSS-A-CAMERA-SHAKE`, `RENDER-BLOCK-EXECUTOR`, `LEADER-STATS-NULL`,
`WHERE-THE-SNAPSHOT-READERS-SIT-RELATIVE-TO-THE-ARBITER`, `ARE-THE-DESCRIPTOR-0X60-AND-0XB0-LISTS-EVER-NON-EMPTY`,
`SR5-IS-A-NON-RESIDENT-BLOCK-EVER-REQUESTED`, `S19-BODY-POOL-OCCUPANCY` and
`S40-RUNTIME-SCENE-GLARE-AND-LIBRARY-FLAGS`, all prefixed `FABLE-REQ-ASTRA-`.

FABLE has **not** re-examined them against this rule in this pass. Until each is re-examined, none of them is a
live-only declaration. Some visibly ask a static question:
- `RENDER-BLOCK-EXECUTOR` asks "who calls `001F4A10`", which is a call-graph question;
- `WHERE-THE-SNAPSHOT-READERS-SIT...` asks the order of 51 readers against the arbiter, which is a frame-order question
  that `gg1-static-order/` shows can be answered from code.

Those two come back to FABLE first. Each of the others gets its fact stated or is withdrawn when FABLE re-examines it.

**`RENDER-BLOCK-EXECUTOR` is already answered statically, re-read 2026-09-30.** It was answered at `7e4af33d5` (BG-11,
`gi-render-command-family.md` §20d, 2026-09-22):
- `001F4A10` has no direct caller. Its only reference is the `lea` at `001F49FA`, which stores it as a block's `+8`.
- The render thread `006106A0` (reached only through the thunk `005FE1F0`) passes each queue slot's `[+0x30, +0x38)` range
  to the block walker `0060A410` (`00610753`).
- The walker's opcode table sends `0x2F` to the arm `0060A899`. That arm builds a local record at `0060A8BD`–`0060A8CE`:
  `[0]` = the singleton `02CC0410` from `005FD050`, `[0x10]` = the block's `+0x10`. It then calls `[block+8]` with that
  record (`0060A8D6`).
- `001F4A10` never sees the block. Its `[rcx]` is `02CC0410`, and `00624660` returns `02CC0410 + 0x18C0`.

The request asks nothing a live run adds. ASTRA is asked to finish it with result_ref `7e4af33d5`.

## ASTRA's authority

ASTRA may:
- close any item above by a method of its choosing;
- reject an item whose stated fact is, in ASTRA's judgement, settleable statically (and say by what);
- ask FABLE for the static half before spending a session.

Nothing in these requests binds ASTRA to the named sites.
