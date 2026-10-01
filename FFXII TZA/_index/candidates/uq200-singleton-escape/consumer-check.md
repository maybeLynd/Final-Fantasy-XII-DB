# Affected-consumer check: UQ-200 answered; the same-day "same bank on every call" narrowing corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `singleton_escape.py` beside this file (7 checks, FAILS 0).

This morning's narrowing rested on a one-hop receiver census, which counted calls made with the singleton in `rcx`. It
concluded that nothing writes a non-zero value to `+0x1C`, so the slot-13 writer "takes the same arm on every call".
That census keyed on `call` and missed two tail-jump forwarders. `001821F0` jumps into `00185A10`, which writes 1.

| consumer | what it said | state |
|---|---|---|
| `17-Presentation-Rendering/Character-Rendering/character-render-object.md` UQ-200 box, the census bullet | "Within the census nothing writes a non-zero value … takes the same arm on every call" | revised-here (struck, dated correction beside it) |
| same box, the `+0x1D` bullet | "… while the writer's byte stays 0" | revised-here (clause struck) |
| same page, "Slot 13 read", the "global parity byte" table (bank A when 0, bank B otherwise) | the bank mapping | agrees. The mapping is unchanged; what the byte is, is now answered. |
| same page, UQ-201 (the banks' shader parameters) | uploader banks by `+0x1D` | agrees. `+0x1D` is the pass command's captured `+0x1C`. |
| `_index/OPEN-QUESTIONS.md` UQ-200 | PARTIAL, with this morning's narrowing | revised-here (ANSWERED; the previous status kept as history, and the new status says why it was wrong) |

A search for "same arm on every call", "same bank on every call" and "nothing writes a non-zero" over every `.md` finds
no other consumer.
