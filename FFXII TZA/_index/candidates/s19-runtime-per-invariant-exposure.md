# S-19 runtime: per-invariant stub exposure for EXP-087 (OPUS, 2026-09-25, block 302)

**Row:** S-19, the movement body pool and the separation pass. The runtime cell is MIXED with the qualifier "no
per-invariant stub-exposure analysis yet". The binding gap reads "types PARTIAL and nothing executed …". This note
scores nothing.

## Two contracts, one record

| contract | executed by | substitutions |
|---|---|---|
| `06-Movement-And-Navigation/CONTRACT-movement-body-pool.md` | **EXP-087** runs these as shipped bytes: the creator `002E3500` (release-old → alloc → the store at `actor+0x138` → all five consumers), the five consumers, the alloc-time initialisers `00380B80` / `003DA830`, consumer 5's leaves `003DA710` / `006C0520` / `003DB130` / `003DB120` / `003DAF20`, and consumer 2's whole chain `003590D0` / `00263F10` / `00263FF0` / `003587C0` / `003589B0` / `002672B0` | two **application stubs** with controlled `eax`: the deep predicates `00265680` and `0037C860`, both inside consumer 2 (`002681E0`). **Import bridges:** `memset`, `cosf`, `sinf`, through their real IAT slots |
| `06-Movement-And-Navigation/CONTRACT-separation-pass.md` (P-1..P-7) | **none.** Its §13 says: "No experiment executes these six bodies" | coverage gap |

## Per invariant (body pool)

| contract item | executed | can a substitution reach it? |
|---|---|---|
| precondition: the record must have a secondary context (`+0xC0`) | EXP-087 | **no** |
| invariant: **at most one body per record** (the creator releases any existing body first) | EXP-087: the creator, real | **no** |
| postcondition: `+0x138` holds the allocation result, NULL included | EXP-087, including mutant `002E3546` (`actor+0x138` = the actor pointer) | **no** |
| the universal: **every consumer re-loads the chain and guards each hop**; finding 1 (FIVE consumers); finding 2 ("guards each hop" exact for the first dereference only) | EXP-087: all five consumers real, including the kind-gate mutant at `00268391` that faults at VA `0x50` | **no** for the guards. The two stubbed predicates sit **after** consumer 2's hop checks: `002681E0` tests `[rec+0xC0]` and the kind byte first, then calls `00265680` / `0037C860` to choose the value it writes to `[rec+0xC0]+0x153` and `[[rec+0xC0]+0x138]+0x80` (read in block 296). They can change **which value** consumer 2 writes, not whether a hop is guarded |

## For the scorer

- **No application stub reaches a body-pool invariant.** The two stubbed predicates decide consumer 2's output value
  (a mode byte), which the contract does not claim. The import bridges supply trig and memset only. The record itself
  says the cos / sin outputs carry no semantic claim.
- **The separation pass (P-1..P-7) is unexecuted.** That is coverage, not exposure.
- **Stale text:** "types PARTIAL and nothing executed", against the MET types cell and EXP-087.
- `live_game` is false.
