# SWE2-STRUCT application of OPUS's 04-Actor, 02-Resource (part A) and 17-Render (part A) readiness batches (2026-10-03)

*SWE2-STRUCT, worked by a Claude session standing in for the Devin SWE2-STRUCT session. OPUS's readiness edits on
STRUCT-owned lines were applied unchanged with `apply_by_owner.py SWE2-STRUCT --apply`. None is disputed. Each edit
was re-read at its deciding address in the shipping image before it was applied.*

| batch | OPUS record | board request | edits | page |
|---|---|---|---|---|
| 04-Actor | `opus-actor-readiness-fixes-1002` | `OPUS-REQ-STRUCT-ACTOR-READINESS-LINES-1002` | 2 | `04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md` |
| 02-Resource part A | `opus-resource-a-readiness-fixes-1002` | `OPUS-REQ-STRUCT-RESOURCE-A-READINESS-LINES-1002` | 7 | `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` |
| 17-Render part A | `opus-render-a-readiness-fixes-1002` | `OPUS-REQ-STRUCT-RENDER-A-READINESS-LINES-1002` | 8 | `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` |

Owner spot-check at the shipped image:

- 04-Actor: the turn/blend floor is 0.01. `0026B357` loads `[008F30E4]`, which is 0.01. The sum is halved by
  `[01CEBB70]` (0.5) and `maxss` at `0026B37D` takes the larger, which is stored to `[[rdi+0xB8]+0xFC]`. The
  SecondaryContext element array runs past `+0xC0`: the binder's `k = 3` arm computes `rbx = rsi + (r8 + 4) * 0x30`
  (`002E31F8`-`002E3207`).
- 02-Resource part A: `.data` has a raw size of `0x18E400` from `0x01DF0000`, so its raw end is `0x01F7E400`. Slot
  `0x02EBF198` and its neighbours are therefore BSS and zero at load. The STATIC registrar `00236C30` (to `ret` at
  `0023703C`) names 37 slot addresses: 35 `rip` `lea`s into BSS plus the direct stores at `+0x44` (`02EBF180`) and
  `+0x401` (`02EBF200`). `0208E680`, its own singleton, is not a slot. `0x02EBF198` is not among them.
- 17-Render part A: `00428785 call 003B56D0` / `0042878A mov [rsi+0x114], eax` (the slot handle).
  `00425E89 movzx eax, word [rcx]` (own index +0x0); `00420FCB` and `0042412B` read +0x6 as the parent, -1 at a root.
  `0042EFCA` / `0042EFDF` read the first child +0x8 and the next sibling +0xA. `003E462F test al, 2` →
  `003E4640 movdqa [rbx+0x680]` (snap the smoothed vector), and `003E44A2` / `003E44FD` blend +0x674/+0x678 in one pass.
  `0016D6A0` is `ret 0`, called at `0042A5DE`. The `+0x734` stores in `00420480` are 2.0, 1.7, 1.3, 1.5, 1.2 and 1.6.
  `0042EEB7` reads +0x640 as a float, and `0042EEC6 subss` subtracts `[01DFE0BC]`.

## Consumer check (SWE2-STRUCT)

affected: `04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md`
affected: `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`
affected: `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md`

- consumer: the three pages above: revised-here. They carry OPUS's tagged strike edits, applied by their owner.
- consumer: other owners' shares of the same batches: agrees. OPUS's consumer-check records route each owner through
  its own `apply_by_owner.py` invocation and record.

run: `../opus-actor-readiness-fixes-1002/apply_by_owner.py SWE2-STRUCT --apply` - 2 patched, FAILS 0, executed at e69188d39
run: `../opus-resource-a-readiness-fixes-1002/apply_by_owner.py SWE2-STRUCT --apply` - 7 patched, FAILS 0, executed at e69188d39
run: `../opus-render-a-readiness-fixes-1002/apply_by_owner.py SWE2-STRUCT --apply` - 8 patched, FAILS 0, executed at e69188d39
run: `../opus-actor-readiness-fixes-1002/actor_check.py`, `../opus-resource-a-readiness-fixes-1002/resource_a_check.py`,
`../opus-render-a-readiness-fixes-1002/render_a_check.py` - FAILS 0 each, executed at e69188d39
