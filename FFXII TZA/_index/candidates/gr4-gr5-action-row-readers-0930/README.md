# GR-4 answered, GR-5 answered: action row `+0x28` has one reader, `+0x0B` has none (OPUS, 2026-09-30)

Register rows GR-4 and GR-5 ask who reads two bytes of the 60-byte action definition row, the table behind registry
slot `02EBF138`. The page is [the action definition row](../../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md),
§2.2 and §7. The earlier censuses (the UQ-106 hop census and the UQ-80 instrument) found no reader of either byte. Neither
followed a row pointer handed to a callee, and neither looked for a copied row.

This record starts from the pointer side, like the [GR-1 record](../gr1-wait-slot-settled-0930/README.md). It finds every
place a row pointer is formed from the slot and follows each one forward over the control-flow graph. The walk goes
through call arguments, outgoing stack arguments, returns and stack slots. It lists every access covering `+0x0A`, `+0x0B`
or `+0x28`, plus every escape to memory and every block copy. The method is static, from the certified image. The checker is
`gr4_gr5_row_readers_check.py` (output `gr4_gr5_row_readers_check.out`, **`FAILS 0`**). It uses the kit's `retool.py`,
`regval.py` and `ptrtaint.py`, plus this record's `rowflow.py`. That file is a CFG dataflow that keeps row offsets and
kills overwritten registers, with a union at every join. Its docstring states what it follows and what it does not.

## The answer (OPUS)

**GR-4: `+0x28` has exactly one reader, `BattleAction_GetPresentationParameter` (`0030A190`, word read at `0030A209`).**
The function receives a row pointer and turns it back into the action id (`(row − base) / 60`). The id must be
`0xD0`–`0xF1`, and the special-sequence state `022C2160` must be 5 or 6 (the cinematic is on screen or ending,
[the mode ladder](../../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2d). In that case
it returns the word at `+0x28`. Otherwise it returns the `+0x24` word, unless that word is `0xFFFF`, has bit 15 set, or
`+0x0C` has bit 30 set; then it returns −1. The value is an **effect id**, and it has two callers:

- `0030CBE0` passes it through ~~`00328360` to `002FCBF0`~~ `00328360` → `0042FCE0` → `002FCBF0` (two tail jumps) *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr45-0930/REVIEW.md) item 3)*. That function queues an effect request: the id goes into a node at
  `+0x20`, and `002FC860` submits the node as resource kind `0xB`. The handle is stored at the caller's record `+0x24`.
- `0030C890` passes it through `0031A230` to `002FCAC0`. That function tests whether the effect fits the effect budget: it
  adds the per-id cost from the `02EC19C0` table, over the active list plus this id, and checks the total is at most `0x18`.
  The result goes into bits 3–4 of its record's `+0x2C`.

The shipped data fits this exactly. Over the 543 rows, `+0x28` is non-zero on 26 rows, and all of them have ids in
`0xD0`–`0xF1`. Each value is `120 + (id − 0xD0)`, and `+0x29` is 0 on every row, so the word read returns the byte. Eight
ids inside that span carry 0: `0xE6`, `0xE8`, `0xE9`, `0xEB`, `0xEC`, `0xEE`, `0xEF` and `0xF0`. The id-to-file step
(`magic\mNNNN.efx` through the path arrays `01E18670` / `01EBE740`) is not re-derived here. It is cited from
[the element types 60–74](../../../17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md), "Ability
names". That page already names `0030A190` as the `+0x28` reader.

**In player terms:** when a Quickening or a Concurrence plays its full-screen cinematic, the game loads that move's own
visual effect, and `+0x28` is its effect number (120–153). Before and after the cinematic, the same moves use the shared
effect in `+0x24` (210 on every id of the span). Editing `+0x28` changes which effect the cinematic shows. It affects nothing
else.

**GR-5: nothing in the image reads `+0x0B`.** The only accesses that cover `+0x0A`–`+0x0B` through a row pointer are the
five known MP-cost reads, and each one is a **byte** read of `+0x0A`: `002F962B`, `00309054`, `00309178`, `00309D7E` and
`0031DBD2`. No word read at `+0x0A`, dword read at `+0x08`, or wider access covers `+0x0B`. The row pointer never escapes to
memory, and the row is never block-copied. The only access at an unknown row offset is `00320DE9`
(`[row + r9 + 2]`), and there `r9` is 0 or 1 (`regval`), which reaches `+0x02` / `+0x03` only.

The data explains the byte's content, but no code uses it. It is non-zero only on rows 182–207 (`0xB6`–`0xCF`, the 26
Esper ultimates, Painflare … Final Eclipse), where `+0x0A` is 0. Rows `182 + 2k` and `183 + 2k` both carry the `+0x0A` of
summon row `0x106 + k` (1, 1, 1, 2, 2, 3, 1, 2, 3, 2, 2, 3, 3). That is the summon's Mist-charge count, so each ultimate
repeats its Esper's summon cost.

**In player terms:** each Esper's two ultimate moves carry a copy of how many MP bars that Esper's summon costs. The game
never looks at the copy: the summon's cost comes from the summon row. Editing `+0x0B` changes nothing in play.

| step | what it shows |
|---|---|
| **S0** | The table is reached only through its slot. ~~There are 722 qword loads of `02EBF138` by rip, in 129 functions.~~ There are 719 distinct qword loads of `02EBF138` by rip (retool counts 722 because `00305133`, `0030514F` and `0030515E` lie in both of the overlapping extents `00305080` and `00305110`). *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr45-0930/REVIEW.md) item 1; the checker's S0 message is not re-issued)* The only other reference is the binder's `lea` (`00237FC0` → `003845F0`), and the loaded header is accessed only at `+4`, `+8` and `+0xC`. |
| **S1** | rowflow walks 194 functions at depth 3 and finds 225 row-pointer formations, 153 hand-offs into 75 callees, and 15 stack-argument hand-offs. It finds **0 escapes** of the header, reference, base or row (dword or wider) and **0 copies** (16-byte accesses, `rep movs`, `memcpy`). The only tagged argument at an indirect call is the header in `r9` at `rand()` (IAT `008C3098`), and `rand()` takes no arguments. |
| **S2** | Positive control over all 60 offsets. All **232/232** sites of the hop census (`members/action-row-reader-hops.tsv`) reappear at their offsets. So do the 11 readers found after it: `+0x04`, `+0x05`, `+0x1D`, `+0x1F`, `+0x20`, `+0x24`, `+0x30` ×2, `+0x38`, `+0x39` and `+0x3A`. This control exercises the call-argument hand-off (11 of the 232 sites need a call hop). No site depends on the return route or on outgoing stack arguments, so those two routes have no positive control in this image. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr45-0930/REVIEW.md) item 2)* |
| **S3** | Accesses covering `+0x0A`, `+0x0B` or `+0x28`: the five MP-cost byte reads (controls) and the word read `0030A209`. None covers `+0x0B`. There is one unknown-offset access, `00320DE9`, whose index is 0 or 1. |
| **S4** | Depth 5 walks 195 functions and adds no access. |
| **S5** | The kit instrument: `ptrtaint`, MONOTONE, seeded at the 225 formations, disps `[0x28, 0x0B]`, width-cover, depth 3. The four functions that return a row leave it in rax by accident, and they have no direct callers. The run reaches 538 functions and produces 329 accesses and escapes. The only row read among them is `0030A209`. `regval` types 75 bases as a constant, a non-stack load or another call's return. For 187, no row pointer reaches the function; for 66, the base holds none at the site (rowflow's state there). The residue is **0**. Control: with disp `0x0A`, the same run re-finds the five MP reads. |
| **S6** | `0030A190` read whole: the id test, the `022C2160` gate and the `+0x24` fallback, as above. |
| **S7** | `0030A190` has two callers, `0030C890@0030C8F1` and `0030CBE0@0030CCC3`, and `rcx` is a row at both. The result goes to the effect-budget test and to the effect request (resource kind `0xB`). |
| **S8** | Data: the 26 rows, `120 + (id − 0xD0)`, `+0x29` all zero, and `+0x0B` on rows 182–207 equal to the summon rows' `+0x0A`, pair by pair. |
| **N1** | Negative control: without following calls, `0030A209` disappears. The row reaches `0030A190` as an argument, so a census that stays inside the slot-referencing bodies cannot see it. In `0030CBE0` the direct call `0030CCC3` sits after the forward `jmp` at `0030CCAC`, and the hop census's linear walk follows that jump past the call. The other route, through `0030C890`, is two calls deep. |

## Limits

- The walk does not see indirect calls' targets. The only tagged argument that reaches one is the header, at `rand()`.
  Recipe slots dispatched through tables reference the slot themselves, so they are roots.
- Taint through non-stack memory is not followed. S1 shows no store of any tag, so no row pointer can be reloaded from
  memory.
- rbp-based outgoing stack arguments are not followed, and neither is code outside retool's function extents.
- Conditional tail calls (a jcc to another function) are not handed tags. There is one in the walked set,
  `002E809A` → `00426FA0`, and it carries only the header in r8, which is not read. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr45-0930/REVIEW.md) item 4)*
- Row offsets are taken modulo the 60-byte stride, which over-reports and never hides an access.
- "No reader" for `+0x0B` means no reader in the executable. The event scripts, a debugger, or an external mod reading the
  table are outside the image.
- The effect-id-to-file mapping is cited from the effect page, not re-derived here. So is the meaning of `022C2160`
  states 5 and 6, which comes from the mode ladder.

## Contradiction with the page, and consumers (routed, not edited here)

- [The action definition row](../../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md) (FABLE) says
  `+0x28` has no reader in five places: the §2.2 `+0x28` row, the §2.3 bullet ("every non-padding field … except `+0x0B`,
  `+0x21` and `+0x28`"), the §4 comment `quickeningIndex (120..153, reader not found)`, and the §7 GR-4 box. **That
  contradicts both this record and the effect page**, which already cites `0030A190` for `+0x28`. The fix is to name
  `0030A190` with the gate and the effect-id meaning, which answers GR-4. For GR-5, the page's `+0x0A` row and §7 can say
  that `+0x0B` is authored and unread, and that it repeats the summon cost.
- Register rows **GR-4** and **GR-5**, via a DATA restatement request.
- **GR-6** (evidence only, not answered here): the same `0030A190` returns the `+0x24` word as an effect id exactly when
  bit 15 is **clear** (and `+0x0C` bit 30 is clear). Those are the 436-row population GR-6 asks about, so for the
  presentation caller they select an effect loaded as resource kind `0xB`. The timeline branches `00325476` / `00325968`
  that GR-6 names were not read here.
- `_types`: no `ActionDefinitionRow` type row exists, so nothing is routed there.
