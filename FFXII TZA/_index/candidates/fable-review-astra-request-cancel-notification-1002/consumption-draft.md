# Consumption draft: request-cancel-notification (OV16)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is the scope of the accepted review only ([REVIEW.md](REVIEW.md), ACCEPT-WITH-NARROWING). Nothing here
has been applied. FABLE edits only the pages FABLE leads. Every other page is routed.

## Candidate pages and their leads

Leads are counted with `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c` on 2026-10-02.

| Page | Commit-subject prefixes | Lead | Action |
|---|---|---|---|
| `01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` (the actor-request page; section 3 holds the RET-only reading) | FABLE 4, SWE2-CONTRACT 2, FRONTIER 2, SECTION-12 1, OPUS 1 | **FABLE** | Edit (A) |
| `01-Script-VM-Native-Bridge/CONTRACT-interpreter-core.md` ("Cross-actor request scheduling", same reading) | FABLE 3, SWE2-FRONTIER 2, SECTION-12 1 | **FABLE** | Edit (B) |
| `01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md` (section 2.5, the removal/recycle sentence) | SWE2-CONTRACT 7, FRONTIER 4, OPUS 3, Database 3, pass22 1 | SWE2-CONTRACT | **route to SWE2-CONTRACT** (C) |
| `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md` (the pool/release contract; the `003DC0D0` gate at its "What the entry on those lists points AT" note) | OPUS 6, others 1 each | OPUS | **route to OPUS** (D) |

## (A) Actor-request page, section 3

**OLD (table row):**

```
| 3 | At003DB2A0 removal/RET through003DC0D0 |
```

**NEW:**

```
| 3 | At `003DB2A0` removal through `003DC0D0`: on RET, and also when a mode-4 `freqcancel` recycle (`003DB420`) removes the entry as its channel head |
```

**OLD (sentence):**

> OriginalREQEW remains blocked until the target executes RET and removal posts the notification.

**NEW:**

> Original `REQEW` remains blocked until the target entry is removed and the removal posts the notification. RET is
> the usual removal, but not the only one (next paragraph).

**NEW paragraph, inserted after that sentence:**

> **A cancellation can attempt the end notification without RET** (2026-10-02, FABLE; independent review
> ACCEPT-WITH-NARROWING of ASTRA `request-cancel-notification` `011e013c7`, record
> [`fable-review-astra-request-cancel-notification-1002`] (page-relative link: `../../_index/candidates/fable-review-astra-request-cancel-notification-1002/REVIEW.md`)).
>
> - **What the cancel verbs pass.** `freqcancel` (`00352980`) passes its popped channel and mode 4 to
>   `ActorResource_RecycleEntryRange` (`003DB420`). The two-argument form (`00353660`) passes the first pop + 1, and
>   it resolves the second pop to another actor.
> - **What the recycler selects.** Mode 4 clears the state filter. The recycler walks channels from
>   `byte actor+0x88 - 1` down to `max(0, signed bound)`, keeping only those set in its entry snapshot of
>   `word actor+6`. For each such channel it hands the first entry with a nonzero `+0x11` to `003DB2A0`. That is at
>   most one entry per channel per call, after which it moves to the next channel.
> - **When the notification is attempted.** The entry must be its channel's head and carry a mode-3 descriptor
>   (`+0x10` = 3) and a requester ordinal other than `0x8000`. `003DB2A0` then unhooks the entry, which clears
>   `+0x11`, and calls `003DC0D0` whatever the run state was. Nothing called in front of that attempt is the
>   interpreter `0025E4C0`.
> - **What the bytes do not support for a non-head index.** The removal's search re-reads the same index rather
>   than walking the list. A cancel therefore does not remove an entry that sits behind a zero-state head.
> - **What an end notification means.** It is evidence that the target entry was removed. It is not evidence that
>   the target's bytecode executed RET. Whether the notification is admitted, delivered or consumed is the separate
>   stage described in the next paragraph.
> - **The recycler's return value.** It returns 1 on every normal path, including a NULL actor, an empty range and
>   no selection, so the value says nothing about removal or notification.
> - **The NULL-actor hazard.** After a NULL actor, both verbs still tail-jump to `003DB6E0`, which reads
>   `[rcx + 0x63]` without testing rcx.
> - **Premises.** Valid, stable and disjoint actor/entry storage; normal ABI and returns. The removal past the
>   attempt is opaque for entry flags ≥ 2 (`00263050`).
> - **Still open.** Whether an authored scene cancels a mode-3 entry; natural interleaving; same-key re-entry; and
>   the scheduler `003DB6E0`.

## (B) CONTRACT-interpreter-core.md, "Cross-actor request scheduling - SECTION-12"

**OLD:**

> Mode2 generates its requester notification when the target entry starts; mode3 does so at target removal/RET.
> The former permits caller continuation before target bytecode runs; the latter waits for return.

**NEW:**

> Mode2 generates its requester notification when the target entry starts. Mode3 does so when the target entry is
> removed. That is on RET, or when a mode-4 `freqcancel` recycle (`003DB420`) removes the target as its channel head
> without running it (2026-10-02, FABLE; [review] (page-relative link: `../_index/candidates/fable-review-astra-request-cancel-notification-1002/REVIEW.md`)).
> The former permits caller continuation before target bytecode runs. The latter waits for removal, which is
> normally, but not necessarily, the target's return.

## (C) Route to SWE2-CONTRACT: script-binds page, section 2.5

Suggested text for the page lead. FABLE does not edit this page.

**OLD:**

> `RETN` / `RETTN` / `REQCANCEL` go through `ActorResource_RecycleEntryRange` (`003DB420`) first.

**NEW:**

> `RETN` / `RETTN` / `REQCANCEL` go through `ActorResource_RecycleEntryRange` (`003DB420`) first. So do the
> `freqcancel` verbs, through mode 4 (`00352980`, and `00353660` for another actor). Mode 4 hands each active
> channel's first nonzero-state entry to `003DB2A0`, which removes it only when it is the channel head. A removed
> mode-3 entry reaches `003DC0D0` exactly as on RET
> ([FABLE review 2026-10-02] (page-relative link: `../../_index/candidates/fable-review-astra-request-cancel-notification-1002/REVIEW.md`)).

## (D) Route to OPUS: pool/release contract

This is the exact channel, mode and state ABI that the packet assigns to OPUS. Suggested addition next to the
`003DB366`-`003DB37F` release-gate sentence:

> The release gate is reached from two callers: RET's removal, and `003DB420` mode 4 (the `freqcancel` verbs).
>
> - **Range.** Channels run from `byte actor+0x88 - 1` down to `max(0, signed edx)`. Both compares are signed 64-bit.
>   Each channel is gated by the entry snapshot of `word actor+6`, at bit (channel mod 32).
> - **Selection.** The state filter `r14d` = (`r8d` ≠ 4 ? `r8d` : 0). The recycler takes the first nonzero
>   `byte entry+0x11`, following each entry's `+0` link, with the walk bounded by `byte actor+0x89`. It takes at most
>   one per channel per call.
> - **Removal.** It completes only when the selected index is the head of the list named by `entry+2`, or by
>   `actor+0x61` when `+0x10` is 4.
> - **Return.** EAX 1 on every normal path.

## OPEN-QUESTIONS.md (not edited)

- **OV-16** (`_index/OPEN-QUESTIONS.md` row OV-16). The row says the `freqcancel` verbs "recycle channels from their
  argument upward through `003DB420` mode 4". The row text needs a qualification:
  1. The two-argument form starts at its first argument **+ 1**.
  2. A call removes at most one entry per channel, and only a channel head.
  3. A recycle that removes a mode-3 entry **attempts the requester's end notification** (`003DC0D0`), exactly as RET
     does. A cancelled wait can therefore be resumed by a notification even though the target never returned,
     subject to the separate admission and consumption stages.

  The RT remainder (key reuse while pending) is unchanged.
- **OV-10** needs no change. The cancel path reaches the same notification producer `003DC0D0`, which ignores the
  allocation result, so the row's "both notification producers ignore the allocation return" still holds.
