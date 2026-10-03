# SWE2-AUDIT-SPEC review: ASTRA OV-10 notification retirement order

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV10-NOTIFICATION-RETIREMENT-1002` · Package: `_experiments/evidence/notification-retirement-order/`
(publisher commit `e46090c35`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The loss is conditional, as the package states. It requires a same-actor requester, head mode 3, flags 0 or 1 and
stable disjoint records.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`003DB2A0` (`ActorResource_RemoveActiveEntry`):**
  - On a valid head it calls `3DC1B0` (unlink and clear).
  - For a channel entry (`ebp >= 0`) with WORD `+6 != 8000h` and byte `+10h == 3`, it posts through `3DC0D0`
    (`003DB37D`).
  - Only **after** that does it relink the free list (`call 3DB650`, `003DB3F0`) and publish the freed index as the
    free head (`mov [rbx+60h],sil`, `003DB3F9`).
- **`003DC0D0`** builds a request record (`402h`, `80000000h`, …) and calls `3DBCF0` (`003DC122`).
- **`003DBCF0`:**
  - The function-0 admission (`word [rdx+4]` vs `dword [[rcx+48h]]`) returns 3 **before** the capacity check.
  - A free head of `FFh` (`[rcx+60h]`) returns 2 with no call and no own object write.
  - In a self-full pool the notification is therefore lost before the slot being removed is freed.
- **The outer removal's EAX** is the saved `byte [entry+12h] & 1` (`r14d`), not the delivery result. So flags 1
  can return 1 despite the loss. Flags ≥ 2 call native `263050`, whose effects stay OPEN.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-02, `357329c0`) re-run: exit 0, output **byte-identical** to `result-01.json`.
- `control.py` (`487223f2`) re-run: `control-result-01.json` **byte-identical**. Its three CLI refusals are
  missing capture receipt, failed capture exit and missing retained identity.

## SWE2-AUDIT-SPEC consumer note

The actor-request page 3 and pool-order prose should say "attempted before the slot is freed". It should not say
"delivered".
