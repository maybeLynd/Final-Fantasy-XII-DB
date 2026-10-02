# Consumer check: 01-Script-VM contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-01-VALUES-1002. Cloud wave 4 mapped `01-Script-VM-Native-Bridge/` from a text snapshot
(session `session_01EHPGLJXLf4LQ9idMivvB2A`; report `cloud-reports/re-readiness/01-scriptvm.md` in
maybeLynd/Final-Fantasy-XII-DB, ce22721b; rated NOT YET). Its 60 value items and its count items were page-text only.
A local read-only pass decided them at the shipping image and in the shipped data; six could not be decided
statically. OPUS re-checked the deciding instructions (`scriptvm_check.py`).

What the bytes show:
- The interpreter's default arm requests a stop (`0025E555`).
- The system-stop request start marks every actor (`00226C7A`).
- The family table is filled with `01F26720`, then four slots are overridden (`003DC2D5`).
- The phase byte `+0x15` has two writers (`0026230B`; `00261B97`, which stores the word `0x107`).
- A negative command never reaches the signed bound, because the command is masked with `and 0xfff` (`0026220C`).
- The 0x740 records sit at the qword `022C6F28`, with no `020FB7xx` base.
- Several census counts are off: 1,288 single-callback records, 212 table commands and a `0xAF6`-byte global space.

The pass drafted 165 strike edits (`apply_01scriptvm.py`). OPUS applies the 100 on its own lines across 16 pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 4 on the binding page are held, while SWE2-CONTRACT's ACTIVE SWE2AUDITSPEC-REQ-CONTRACT-RC13-CLAIMS-ROW-0930 edits
  its claims table.
- 19 go to SWE2-FRONTIER, on the overlay carriers.
- 15 go to FABLE.
- 9 go to SWE2-EC7.
- 7 go to SWE2-DATA. Its ATEL page is open under three ACTIVE SN-1 tasks; that page's uncommitted edit is SWE2-DATA's
  and is not part of this commit.
- 6 go to SWE2-CONTRACT.
- 5 go to FRONTIER, as its own lines.

- **Affected:** 01-Script-VM-Native-Bridge/CONTRACT-native-command-lifecycle.md, 01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md, 01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md, 01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md, 01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md, 01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md, 01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-standard-motion-verbs.md, 01-Script-VM-Native-Bridge/README.md, 01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md, 01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md, 01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md, 01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md, 01-Script-VM-Native-Bridge/Verb-Dispatch/what-each-script-verb-touches.md, 01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md, 01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md, 01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the sixteen OPUS-led and shared 01 pages (OPUS lines) | revised-here |
  | the binding page (claims table under SWE2-CONTRACT's ACTIVE edit) | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 4 edits) |
  | the interpreter-core contract, the bridge contract and the lifecycle page (overlay carriers) | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER` and `FRONTIER`, 24 edits) |
  | FABLE's pages and lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 15 edits) |
  | EC7's lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 9 edits) |
  | the ATEL debug-companions page (open under SWE2-DATA) and the undecided census counts | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 7 edits) |
  | SWE2-CONTRACT's lines (bed8dcd91) | routed-to-SWE2-CONTRACT (request with `apply_by_owner.py SWE2-CONTRACT`, 6 edits) |
  | RE repo `docs/readiness/01-scriptvm.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-scriptvm-readiness-fixes-1002/scriptvm_check.py, verified at 31f29775a: 12 instructions decode as cited, FAILS 0 ([`scriptvm_check.out`](scriptvm_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (100), FAILS 0.
