# S-05 runtime: "nothing executed" is out of date for one of its three contracts (OPUS, 2026-09-25)

**Row:** S-05, the shared transform workbench. The runtime cell reads NOT MET. The binding gap cell
reads *"types PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap"*. The `types` half is
stale too: AUDIT-SEM re-scored `types` to MET on 2026-09-22. This note scores nothing.

The registry (`important-subsystems.tsv`) gives S-05 three contracts.

| contract | executed? | evidence |
|---|---|---|
| `CONTRACT-transform-primitives.md` | **yes, stub-free** | **EXP-115**: `00398F90` TransformPointByWorkbenchMatrix (68 insns, **0 calls**), `00397910` ComposeTransforms (1 call, to `00808C40`) and `__security_check_cookie` `00808C40`, **all real**, with no stubs. 24/24 cases, 21/21 mutants on the shipped bytes, stable ×3. A byte-exact compare of the whole `022D8F80..022D9330` globals window. It follows an earlier independent instrument, `diff_transform.py` (123 + 123 cases, 0 mismatches). |
| `CONTRACT-transform-workbench-save-restore.md` | **no record** | `0036D930` (save) and `0036D8E0` (restore) are **call-free leaf loops**, re-read this session in block 214: a variadic save of up to 32 `{pointer, 16 bytes}` slots and the restore that copies them back. A stub-free execution needs no harness beyond the 32-slot arrays; this is a candidate for ORACLE. |
| `CONTRACT-shared-transform-workbench.md` (TW-1..TW-6) | **not by execution** | TW-1..TW-6 are layout and ownership statements (no static bytes, 16-byte rows, one established matrix, arguments rather than state, no owner, a separate record table). Their evidence is a census, which is the right instrument for statements about who touches what. Execution would test the primitives that TW-3 names, and EXP-115 does that. |

**For the scorer.** The primitives contract meets the no-stub precedent (S-10's class). The save/restore
contract is unexecuted but trivially executable. The workbench contract's invariants are census
claims, not behaviour. How a subsystem row weighs three contracts of different kinds is the scorer's
ruling.
