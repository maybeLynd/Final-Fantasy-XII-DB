# OV-14: the other wait kinds answered by cross-reference; the service half needs a scope (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-14, `01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` §8):** "Establish
other wait kinds and nonempty external service behavior at the required grain."

## Half 1, the other wait kinds: answered by prior art

[The actor-request page](../../../01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md)
§5 enumerates every wait-slot kind, with its input and resume condition:

| kind | resumes when |
|---|---|
| 0, ≥ 8 | never dispatched |
| 1 / 2 | runs the interpreter |
| 3 | the matching target entry is absent |
| 4 | the matching detached notification is present and removed |
| 5 | the actor/ID list cursor reaches the end |
| 6 | the selected channel bit is clear |
| 7 | the actor/channel list cursor reaches the end |

- **Producers.** §7 of that page names every producer of the list waits: `REQALL` / `REQIALL` arm kind 7, and `REQWAITALL` arms
  kind 5. It includes an image-wide store census with its control.
- **The script page's own wait.** The native command wait (family 0 command 0) is §3 of the script page. What its skip
  predicate reads is OV-15's answer (8764d1109).
- **Proposal.** Mark this half ANSWERED with those two links.

## Half 2, "nonempty external service behavior at the required grain": needs a scope

The script page mentions services only as "configured idle service branches". It names no service, and the box names no
grain. It is a completeness phrase, and it cannot be answered or falsified as written.

**Proposed ruling, for FRONTIER:** either name the services (for example, the outer `0025D9E0` frame pipeline's service
calls) so the row becomes a specific enumeration, or declare it a limit of the section's claim under the class-1 pattern.
FABLE does not waive it by relabelling.
