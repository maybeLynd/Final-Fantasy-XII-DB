# Consumer check: 24-CRT contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-24-VALUES-1002. Cloud wave 5 mapped `24-Compiler-And-CRT-Runtime/` from a text snapshot
(session `session_0137yPRG7XTM3wFKHbcLxYsK`; report `cloud-reports/re-readiness/24-crt.md` in
maybeLynd/Final-Fantasy-XII-DB; rated NOT YET). Its 104 value items were page-text only. A local read-only pass decided
most of them at the shipping image. It left the counts that depend on a tag or members file, and the items that need
Ghidra project state or semantics. OPUS re-checked the deciding instructions (`crt_check.py`).

What the bytes show:
- A built lazy-static guard is negative as a signed int (`008092C5`), and the `<` branch is the slow path
  (`00189D43`).
- The unhandled-exception filter is installed at `007980F7`.
- The init lock releases before construction and sleeps on a condition variable (`0080940B`), so unrelated statics do
  not queue.
- The arena accounting stays two elements; `00369DAD` writes a different field. This is consistent with 1ff7875c4 and
  FABLE's 2026-10-02 answer.
- The name buffer is NUL-terminated at `+0x3B` (`0036C696`).
- Several "unknown" bodies are named CRT functions: `use_facet`, `strncpy`, an intrusive-list empty.

The pass drafted 118 strike edits (`apply_24crt.py`). OPUS applies 83 of them across 12 pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 8 on the exception-funclet page are held while OPUS's own cloud F task OPUS-CLOUD-F-INTERIOR-W24-1002 holds that
  page (`apply_by_owner.py OPUS-HELD`).
- 17 go to SWE2-EC7.
- 6 go to FABLE.
- 3 go to FRONTIER and SWE2-FRONTIER.
- 1 goes to SWE2-DATA.

- **Affected:** 24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md, 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md, 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md, 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md, 24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md, 24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md, 24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md, 24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md, 24-Compiler-And-CRT-Runtime/README.md, 24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md, 24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md, 24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the twelve OPUS-led and shared 24 pages (OPUS lines) | revised-here |
  | the exception-funclet page (held for OPUS's own F task) | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 8 edits) |
  | the static-initialiser and generated-family pages, and EC7's lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 17 edits) |
  | FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 6 edits) |
  | FRONTIER's lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER` and `SWE2-FRONTIER`, 3 edits) |
  | DATA's line and the members TSV header | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 1 edit) |
  | RE repo `docs/readiness/24-crt.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-crt-readiness-fixes-1002/crt_check.py, verified at 80da775cb: 6 instructions decode as cited, FAILS 0 ([`crt_check.out`](crt_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (83), FAILS 0.
