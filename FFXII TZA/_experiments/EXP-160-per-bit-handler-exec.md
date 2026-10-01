---
id: EXP-160
title: "Per-bit handler 30E130 — edge-gated tracking arrays + notify fan-out"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp160_check.py
result: 117/117 (stable x3)
---

# EXP-160 — `30E130` per-bit handler, executed

`0030E130` is the per-bit callback `30FED0` dispatches from its
changed/cleared bitmaps (EXP-159). 149 insns. It mutates two 128-bit
tracking arrays on the rec and fans out to stat-block handlers on edge
transitions.

## Signature and arm table

`30E130(rec=rcx, bit=dl, arg3=r8, notify=r9, arm=stack)`:

- `rbx = rec + (bit>>3)`, `esi = 1<<(bit&7)` — byte+bit addressing into
  two 16-byte arrays at `rec+0x68` and `rec+0x78`.
- arm decode: `0`→clear `+0x68`, `1`→clear `+0x78`, `2`→set `+0x68`,
  `3`→set `+0x78` — each edge-gated (set skips if already set, clear
  skips if already clear; no-op → bail before any work).
- Bound: `322C50(0x1D, bit)` — cls-`0x1D` bound resolves to
  `d[q[0x2EBF040]+4]` — a runtime descriptor cell (null in the shipped
  image → bound 0 → everything rejects; planted `0x80` in fixture).

## Transition work (executed)

On a real transition (pre-state `b[+0x68]|b[+0x78]` vs post-state
differ):

1. `861EC0(rsp+0x50, 0, 0x148)` — memset a 0x148 stat block (same size
   `3848E0` resets in EXP-154).
2. `call rax` pair: `ebx = arm∈{2,3}` → set-arms `386AE0`, clear-arms
   `386A50` — `(rec, bit, blk)`. `386AE0` real (→`3848E0`, `31B860`×2,
   `384B10` scripted — indirect call).
3. `b[rsp+0x7C]&1` → `3112F0(blk, 0, rec, 0xFFFF, notify)` scripted
   blk-notify.
4. `~(notify>>1)&1` → second pair `46A720`/`46A790` `(rec, bit)` →
   scripted `46AB10`.
5. `bit ∈ [0x68,0x71]` → `3279B0(rec, armset ? 1 : -1)` scripted.
6. `notify bit9 == 0` → **recurse `30FED0(rec, notify)`** — bounded:
   `30FED0` ORs `0x202` into the notify it passes down, so the
   recursion can never re-enter `30E130`'s tail.
7. Arms 0/2 (`+0x68`) additionally call `30EA40(rec, bit, arg3)` real
   (→`20E600`×2 + `387020` leaf).

## Proven

- `set78`/`set68`/`clr78`/`clr68`: byte writes and handler-pair
  selection (`386AE0` on set, `386A50`/`h86a50` on clear), `30EA40`
  only on `+0x68` arms.
- `noedge`: pre-set bit + set arm → no memset, no handlers.
- `oob`: `bit=0x90` ≥ bound → bail.
- `notify0`: bit9 clear → `fed0` recursion fired (scripted boundary
  intercept recorded the call); `46A790` fired on the `~(0>>1)&1` gate.
- `bit68`: bit `0x68` → `3279B0` intercept.
- `fed0-watch`/`fed0-watch2` (EXP-159 cases) now drive real `30E130`
  — `he130` tag ×2/×1 for watch bits {0,2}/{7}.

## Real layer added

`30E130`, `30EA40`, `387020`, `386AE0`, `46A720`, `46A790`. Scripted
(disclosed): `384B10` (indirect call), `3112F0`, `3279B0`, `46AB10`,
inbound `30FED0` (kept scripted — six existing asserts consume the
boundary; the callee body is separately proven by `fed0-*`).

## Boundary disclosure

`q[0x2EBF040]` bound cell and all fixture recs planted; scripted
boundaries listed above. MODEL-PROVEN/NATIVE-REPLAY only.
