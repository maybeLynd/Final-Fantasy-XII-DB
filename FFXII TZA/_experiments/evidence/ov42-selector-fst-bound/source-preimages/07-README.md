# OV-10: the request's authored bounds and the (absent) recovery policy, from prior art (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-10, `01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` §7):** "Real
authored input bounds and higher recovery/delivery policy for exhausted notification capacity."

## Authored input bounds: answered

- **The channel.** This is the input the page calls "a genuine precondition". UQ-54 (ANSWERED 2026-09-25, FABLE) enumerates
  every producer of a request channel:
  - the `REQ` / `REQEW` / `REQSW` immediates: 0–7;
  - `REQALL` / `REQIALL`: 0–7 and 1–5;
  - the 20 native `003DBB60` sites and 4 thunk sites: immediates or record-derived values, 0–7;
  - the three sysreq verbs: 675 sites, all 1–7.

  So **every shipped channel is 0–7**; none is negative and none is above 7. DATA's census
  (`25-EBP-Script-Container/Bytecode-And-Opcodes/members/req-channel-census.tsv`) agrees: its constant channels span 0–7.
- **The function id is checked natively.** `003DBCF0` checks it against the function count (§2), so it needs no authored
  bound.
- **The target** is resolved through the manager (§1).

## Recovery for exhausted notification capacity: answered, there is none

§3 of the page reads it from the bytes. The notification comes from the requester's ordinary finite entry pool, and **both
notification producers ignore the allocation's return**. There is no retry, no fallback and no error path: the
notification is lost, and the caller's kind-4 wait stays parked. The page's controls with the caller's capacity exhausted
show exactly that.

"No higher recovery" is the policy. A reimplementation that adds one changes behaviour.

## Residue (runtime)

Whether shipped play ever exhausts an actor's entry pool (the peak number of outstanding requests against the pool size) is
a live or runtime question. The proposal is to record it as RT under the runtime rule, since the static claim is tier 1.
