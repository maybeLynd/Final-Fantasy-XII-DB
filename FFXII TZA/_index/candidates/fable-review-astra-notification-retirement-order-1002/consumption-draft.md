# Consumption draft: notification-retirement-order (OV-10)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft covers the accepted scope only: [REVIEW.md](REVIEW.md), ACCEPT-WITH-NARROWING. It keeps the packet's limits.
No page has been edited. Leads were counted with
`git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c` at c0bf8acd5.

## Pages FABLE leads (FABLE may edit)

### A. `01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md`

Lead: **FABLE (4)**. The other subjects are SWE2-CONTRACT 2, FRONTIER 2, OPUS 1 and the SECTION-12 overlay 1.

**A1. Section 3: a new paragraph block.** Insert it directly after the paragraph that ends "No shipped deadlock,
automatic retry or higher recovery is inferred.":

> **The end notification is attempted before the finishing entry's own slot is free.** *(2026-10-02, FABLE, on its
> independent review of ASTRA's `notification-retirement-order` packet; record
> [`fable-review-astra-notification-retirement-order-1002`] (page-relative link: `../../_index/candidates/fable-review-astra-notification-retirement-order-1002/REVIEW.md`).)*
> In a head-entry removal, `003DB2A0` first calls the unhook `003DC1B0`. The unhook relinks the neighbours and
> clears entry `+0x11`, and writes nothing on the actor. Next comes the mode-3 attempt through `003DC0D0`. Only after
> that does the removal relink the index onto the free list and publish it as the free head `+0x60`. Every path from
> the attempt's return passes both of those steps.
>
> The attempt is made only when all of these hold:
>
> - the entry is the list head;
> - its mode `+0x10` is 3;
> - its signed channel byte `+0x02` is not negative;
> - its requester word `+0x06` is not `0x8000`;
> - the requester resolves to a non-null actor.
>
> **Two refusals come first.** The posted descriptor selects function 0. `003DBCF0` checks that id against the
> requester's function count before anything else, as an unsigned compare: a zero count returns 3. Only then does
> it test the requester's free head: `0xFF` returns 2. Neither refusal calls anything or writes outside its own
> stack.
>
> **So a self-requested notification on a full pool is lost.** Take a requester that is the removing actor itself,
> with its free list already empty. The notification is refused with 2 before the slot being retired becomes
> allocatable. This holds under these conditions:
>
> - the entry is a valid head mode-3 entry;
> - the function count is positive;
> - the entry's flags `+0x12` are 0 or 1 (flags 2 and above also cross `00263050`, whose effects are not
>   established);
> - actor, entry-pool and frame storage are stable and disjoint;
> - calls return normally under the ABI;
> - there is no concurrent writer.
>
> This is a conditional reading of the original code, not an observed full pool.
>
> **The removal's return is not a delivery result.** It is bit 0 of the entry's `+0x12` byte, read before the
> attempt. The attempt's own result is overwritten unread. With flags 1 the removal returns 1 even when the
> notification was refused. Index `0xFF` returns a constant 1 without reading an entry.
>
> **An observer has to read the attempt itself.** It must read the requester, the requester's free head and the call
> origin at the attempt: `003DBCF0` + 0x36, with return origin `003DC0D0` + 0x57. Spare capacity seen after the
> removal does not show that capacity existed when the notification was allocated.
>
> **Still open:**
>
> - whether shipped play reaches a full self-pool;
> - actor lifetime and reuse;
> - concurrent mutation;
> - cancel / re-entry scheduling;
> - the success and effects of the insertion helpers on a non-`0xFF` free head.

**A2. Section 7, the OV-10 item.** Add an indented sub-bullet. Leave the box unticked.

OLD:

```
- [ ] **OV-10.** Real authored input bounds and higher recovery/delivery policy for exhausted notification capacity.
```

NEW:

```
- [ ] **OV-10.** Real authored input bounds and higher recovery/delivery policy for exhausted notification capacity.
  - *Qualified 2026-10-02 (FABLE, review of ASTRA `notification-retirement-order`):* the end notification is attempted
    before the removed slot is relinked and published, so the capacity that matters is the requester's free head at
    the attempt (section 3). A runtime observation for the residue counts only when it is taken at the attempt, with
    the requester and the call origin. Capacity seen after the removal does not count.
```

### B. `01-Script-VM-Native-Bridge/CONTRACT-interpreter-core.md`

Lead: **FABLE (3)**. The other subjects are SWE2-FRONTIER 2 and the SECTION-12 overlay 1.

This is in "Cross-actor request scheduling — SECTION-12". The OLD text spans a line break.

OLD:

```
filed-only insertion. Notifications use the requester's ordinary entry capacity and can fail
without undoing target progress.
```

NEW:

```
filed-only insertion. Notifications use the requester's ordinary entry capacity and can fail
without undoing target progress. A mode-3 end notification is attempted before the removed entry is relinked onto
the free list, so a self-requested notification on an already-full pool is refused even though the removal then
frees a slot. The removal's return is the entry's `+0x12` bit 0, not a delivery result
([the actor request] (page-relative link: `Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md`) §3; conditional
static reading, premises there).
```

## Pages FABLE does not lead (route, do not edit)

### Route to OPUS: `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`

Lead: **OPUS (6)**. The other subjects are single commits by FABLE, SWE2-STRUCT, SWE2-EC7 and others.

The packet names OPUS for the pool/post/return contract. Proposed addition after the end of the `003DC0D0` row's
third cell in the function table ("… a null result returns without the call"):

> Its caller `003DB2A0` makes this call before it relinks the removed index onto the free list and publishes it at
> `+0x60`, and it discards the result. `003DBCF0` checks function id 0 against the count first (a zero count returns
> 3), then the free head (`0xFF` returns 2), with no calls or object writes on either refusal. The removal returns
> entry `+0x12` bit 0. Index `0xFF` returns a constant 1. (FABLE review
> `fable-review-astra-notification-retirement-order-1002`.)

### Route to OPUS: `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md`

Lead: **OPUS (6)**. The other subjects are FABLE 5, FRONTIER 4 and SWE2-EC7 2.

The removal table has two row corrections, both bytes-level and outside this packet's own claim. They come from
this review's checks "non-head walk" and "notification gate".

OLD:

```
| walk to find it | `003DB326`–`003DB33F` | linear from the head through `003DB550`, so removal is O(list) |
```

NEW:

```
| look for it | `003DB2A0` + 0x86 – + 0x9F | not a walk: every iteration passes the removed index itself to `003DB550` (`mov edx, esi`), so a non-head entry is unlinked only when its own `next` byte equals its index, returns with no unlink when that byte is `0xFF`, and otherwise repeats the same iteration |
```

OLD:

```
| release a payload | `003DB36B`, `003DB371` | only when `entry+0x06 != 0x8000` **and** `state == 3` |
```

NEW:

```
| end notification | `003DB36B`, `003DB371` | the mode-3 end notification through `003DC0D0`, attempted before the free-list relink; only when the signed channel byte is non-negative, `entry+0x06 != 0x8000` **and** `entry+0x10 == 3` (`+0x10` is the request mode) |
```

### Route to SWE2-CONTRACT: `01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`

Lead: **SWE2-CONTRACT (7)**. The other subjects are FRONTIER 4, OPUS 3, "Database" 3, and FABLE 1 among the
singles.

OLD:

```
`AllocateAndSubmitEntry` returns 2 when the free list is exhausted (`003DBD32`) and 3 when the id is
out of range;
```

NEW:

```
`AllocateAndSubmitEntry` returns 3 when the id is out of range, tested first as an unsigned compare against the
function count, and 2 when the free list is exhausted (`003DBD32`); neither refusal calls anything or writes the
actor;
```

## OPEN-QUESTIONS.md, row OV-10 (do not edit; qualification note)

The row is PARTLY ANSWERED, and its residue stays OPEN as a runtime item carried by
FABLE-REQ-ASTRA-OV10-OV42-REACHABILITY ("probe `003DBD32`, return `003DC127`"). The packet does not change its
status.

It does need a qualification. The probe counts only for the removal case when:

- the requester at the probe is the removing actor (or the named requester);
- the return origin is the `003DC0D0` call;
- the free head is read at the attempt.

Spare capacity after the removal is not evidence, because the slot is relinked after the attempt. The row's "both
producers ignore the allocation return" also stands: re-derived here, the removal overwrites `003DC0D0`'s result
unread. OV-16 is handled by the request-cancel-notification review.
