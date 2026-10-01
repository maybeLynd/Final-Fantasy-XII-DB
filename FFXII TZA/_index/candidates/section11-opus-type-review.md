# SECTION-11 (Update11) — OPUS review of the type-store claims

OPUS, 2026-09-24. **Scope: widths, offsets, storage class and route of the rows SECTION-11 changes
in `_types/`.** Meanings of behaviour (what the ordinal selects, what POPA/PUSHA do with the
accumulator, the lifecycle phase values) are routed to FABLE and SWE2-AUDIT-SEM and are not
reviewed here. Evidence class **NATIVE/STATIC**, image `73461D08…21F8`; the section's fixture was
not replayed — this is a second, independent instrument.

## Receiver identity first

Every access below is through `rsi` in `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`) or
`0025DF00`. **`rsi` is an `ActorWaitSlot` at every one of its nine writes in `0025E4C0`**: at entry
`0025E4E6 mov rsi, r8` (the sole caller `0025DF00` passes the current slot) and six recomputations
`lea rsi, [rax + rcx*8]` with `rax = [r15 + 0xA8]`, `rcx = movsx([r15 + 0x11]) * 5` — the actor
record's `+0xA8` slot array at stride 0x28, indexed by its current-slot byte (`00261250..00261260`,
`002612C7..002612D6`); the other two are the epilogue `pop`s.

## Verdict: ACCEPT for every layout claim

| row | section claims | static finding |
|---|---|---|
| `ActorWaitSlot +0x00` 4 → **8** bytes, `u64 / kind-discriminated` | runnable bytecode keeps a full instruction pointer here; other kinds keep a low-dword key | `0025E4C0`: **1 qword read** (`00261273 mov r14, qword ptr [rsi]`, and at entry `0025E4E9 mov r14, qword ptr [r8]`) and **13 qword writes** (`0025F5ED mov qword ptr [rsi], r14` …). `0025DF00`'s kind-4 arm (`0025E091`) reads **only the low dword** `mov r8d, dword ptr [rsi]`. Both halves of the claim hold. |
| `+0x04` span removed | absorbed by the widened +0x00 | follows from the qword accesses above |
| `+0x08` `nativeTargetOrdinal` `i32` (was `unobservedSpan0004` u8[8]) | a saved dword | **1 dword read, 9 dword writes** (`0025F39D`, `0025F3E1` …); no other width |
| `+0x10` `accumulator` `i32` (was unobserved u8[4]) | a dword read and written by the request opcodes | **1 dword read, 4 dword writes** (`0025F322`, `0025F35E` …) |
| `VmValueStack`: `STATIC 02099AC0`, allocation IMAGE (was CALLER frame) | the interpreter's value stack is one image-backed global, depth reset at every entry | `0025E4D8 mov dword ptr [rip+0x1e3b5e1], r11d` resolves to **`02099AC0`** with `r11d = 0` (`0025E4D2`). A census of every rip-relative reference in every listed body finds **345 references to `02099AC0`** — 109 `lea`, 123 reads, 20 `inc`, 93 writes — **all 345 inside `0025E4C0`**. The old "caller frame, lifetime of the interpreter frame" reading is refuted, as the section says. `-0x8`/`-0x4`/`+0x284`/`+0x288` are neighbouring statics (other functions), not members. |
| `VmValueStack` readiness `TYPE RESOLVED` → `SIGNATURE RESOLVED` | conservative after the lifetime correction | Not a layout regression — size 0x284 and the four array offsets are retained — so a reviewer could keep TYPE RESOLVED. **Deferred to the auditor; OPUS does not re-promote.** |

`ActorWaitSlot +0x0C/+0x15/+0x18` and `VmValueStack +0x000` change **meaning text only**; routed.

## Consistency with SECTION-12

SECTION-12 declares `+0x1C` / `+0x22` inside the same record's `+0x18` scratch that SECTION-11
calls command-specific (`section12-opus-type-review.md`). The two overlays agree on every byte they
both touch; neither contradicts the other's layout.
