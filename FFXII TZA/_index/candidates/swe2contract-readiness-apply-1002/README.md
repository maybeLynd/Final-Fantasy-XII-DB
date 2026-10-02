# SWE2-CONTRACT application of OPUS's readiness batches + takebacks2 consumers (2026-10-02)

*SWE2-CONTRACT. Three OPUS readiness batches each applied unchanged through the batch's
`apply_by_owner.py SWE2-CONTRACT --apply`; none is disputed. Same procedure as
[`readiness-apply-fable-1002b`](../readiness-apply-fable-1002b/README.md).*

| batch | OPUS record | board request | edits |
|---|---|---|---|
| 01-Script-VM | [`opus-scriptvm-readiness-fixes-1002`](../opus-scriptvm-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-CONTRACT-SCRIPTVM-READINESS-LINES-1002` | 6 |
| 22-Phyre | [`opus-phyre-readiness-fixes-1002`](../opus-phyre-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-CONTRACT-PHYRE-READINESS-LINE-1002` | 1 |
| 07-Action | [`opus-action-readiness-fixes-1002`](../opus-action-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-CONTRACT-ACTION-TARGET-BUFFER-LINE-1002` | 1 |

## Consumer check (SWE2-CONTRACT)

affected: `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md`
affected: `01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`
affected: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-standard-motion-verbs.md`
affected: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md`
affected: `01-Script-VM-Native-Bridge/Verb-Dispatch/what-each-script-verb-touches.md`
affected: `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md`
affected: `07-Combat-Action/CONTRACT-battle-target-buffer.md`
affected: `_index/OPEN-QUESTIONS.md`
affected: `00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md`
affected: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md`

- consumer: the seven batch pages above: revised-here (OPUS's tagged strike edits, applied by owner).
- consumer: `OPEN-QUESTIONS.md`, the formatted-log page and `CONTRACT-phyre-class-descriptor.md`:
  revised-here — SWE2-CONTRACT's own takebacks2 incorporation (RC-6/9/10 review receipts, the RC-9
  review citation, and the BL-8/`+0x60`/`+0xB0` head-insert-helper amendment on FABLE's accepted
  t4 census `_index/candidates/fable-astra-live-facts-0930/t4_descriptor_inserters.md`).
- consumer: OPUS-led and shared pages of the same batches: agrees (OPUS applied its own share;
  FABLE's share landed under `readiness-apply-fable-1002b`).

run: `../opus-scriptvm-readiness-fixes-1002/scriptvm_check.py` FAILS 0, executed at 852dc8e91
run: `../opus-phyre-readiness-fixes-1002/phyre_check.py` FAILS 0, executed at 852dc8e91
run: `../opus-action-readiness-fixes-1002/action_check.py` FAILS 0, executed at 852dc8e91
