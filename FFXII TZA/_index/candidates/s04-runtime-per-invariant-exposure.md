# S-04 runtime: per-invariant stub exposure is empty (OPUS, 2026-09-25)

**Row:** S-04 encoded-id space and class registry. AUDIT-SEM re-scored the runtime cell **MIXED** on
2026-09-25, with the qualifier *"no per-invariant stub-exposure analysis yet"*. The binding gap still reads
*"validator arms 2–32 unexecuted"*. The contract is `00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md`.
Its I1–I6 are the SECTION-05 overlay text, owner-merged in the worktree and waiting for FRONTIER to publish it.
This note scores nothing. It follows `s04-runtime-stub-free-execution.md` (block 235).

## The entries and what each one calls

Call lists are from each function's full body, taking the extent from `Tools/work/graph/functions.tsv`.

| entry | calls | executed by | stubs on its calls |
|---|---|---|---|
| `00322C50` validator | `00309440` only | **EXP-143** (all 32 arms), N05 | none: *"the validator and `00309440` are pure leaf code"* |
| `0031C5D0` fill | `0020E600`, `002F9860`, `00309440`, `00309EC0`, `0030AE30`, `0030B0E0`, `0031E9A0`, `00322C50`, `00323890` | **N05** | none: *"zero application-callee substitutions"* |
| `0035D330` / `0035D380` wrappers | `0016D6A0`, `0031C5D0`, memset `00861EC0` | **N05** | memset is an **import**, bridged to a host memset (the thunk stays original) |
| `002F9860` | `0020E600` | **N05** | none |
| `0030B6A0` relocation patcher | **no calls** (195-byte body) | **EXP-189**; the static-init chain's scripted boundaries (`2DDE60`, `237DF0`, host `sqrtf`, cookie check) are not its callees | none |
| `0031E9A0` equipment gate | `0031E9F0` | **EXP-100**, which runs `0031E9F0` real | none |

## Per invariant

| inv. | executed by | can a stub reach it? |
|---|---|---|
| **I1** (tag selects the input lane; class 12 returns −2) | EXP-143 (all arms), N05 one baseline per class | **no**: the validator is leaf code |
| **I2** (three validation domains) | EXP-143, N05; SECTION-05 R143 | **no** |
| **I3** (rebase width) | N05 | **no**: the rebase runs with no substitution |
| **I4** (rebase resets `state+57C8..5A47` using the full pointer) | N05 (above-4 GiB fixtures) | **no** |
| **I5** (direct fill vs wrapper failure; the wrapper clears the record) | N05 | the wrapper's clear **is** the bridged memset. The bridge implements memset's semantics and the thunk runs original, so this is an import substitution, **not an application stub** |
| **I6** (borrowed results; two lifetimes) | N05 / S05 | **no** for the aliasing claims. The contract itself leaves allocation and reentrancy lifetime open |

## For the scorer

**The exposure set is empty.** The only substitution anywhere on S-04's entries is the imported memset under I5.
That is the same class of bridge EXP-150 used in its hook (`00861EC0`), and the class S-10's MET was granted
alongside.

**The binding gap is stale.** EXP-143 executes all 32 arms.

`live_game` is false in every record.
