# UQ-193: the rest of the callers' contract with the render root's reference container (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (UQ-193):** "Caller responsibility for preventing stale/out-of-range IDs, resource admission, source
ownership and other generic-container construction paths" (render-event-selection-evidence.md, section 5).

The stale-id clause was answered earlier the same day (`_index/candidates/uq193-release-sites/`): every caller of the
release `0051BA40` resets the record's stored id to -1. This record answers the other three clauses.

## Other construction paths: none (K1)

The container is the render root's 64 reference slots. `RenderResourceRoot_InitializeSubcontainers` `0041E3A0` builds it
at `0041E470` through `0051B9D0`, which is `lea r8, [rcx + 0x30]; mov edx, 0x40; jmp 0051F170`.
- `0051F170` has no other caller.
- `0051B9D0` has no other caller.
- No data pointer holds either.

So the generic container this page describes is constructed exactly once.

## Resource admission: one function, two callers, one rule (K2, K3)

**The function.** `0051BA80(container, id, source, …)` is the only admission. Its contract:

| id passed | what happens |
|---|---|
| -1 | capacity check `0051F150`, then a new slot from `0051F080`: the `slot \| 0x10000` id of section 7 |
| any other id | the slot is looked up by `0051F240`, and its entry rebuilt in place by `0041CA70` (`PresentationEntry_RebuildDerivedResourcePointers`) |
| a live id whose initialisation fails | the slot is released (`0051F190`) |

**The callers.** It is called only twice, and each passes the render record's own stored id:

| call site | function | id | slot |
|---|---|---|---|
| `004247AD` | `00424550` | `[record+0xC8]` | the pending entry |
| `00425244` | `00424D80` | `[record+0xC4]` | the current entry |

**The rule.** A caller either passes -1 to admit a new resource or passes the id it already holds to refresh it. The
stale-id answer shows that those stored ids are always either -1 or live, because every release resets them. So no
caller can re-admit through a stale id.

## Source ownership: the record's own resource (K2)

At both call sites the source (`r8`) is the render record's own resource entry: `[record+0x10]`, resolved through
`0020E600`. The container slot therefore refers to a resource the record owns and does not own it itself; the record's
lifecycle bounds it.

Section 10 of the page ("Concrete cleanup and linked-resource effects") covers what the release does to that link.

## Limits

- **Static.** Nothing was executed.
- **The record's own lifecycle.** How the record's resource `[record+0x10]` is itself admitted and released belongs to
  the render-record pool pages, not to this container.

## Files

- `uq193_container.py`, 3 checks, FAILS 0.
- `consumer-check.md`.
