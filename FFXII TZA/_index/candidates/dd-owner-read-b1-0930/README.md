# Owner read of DD residue batch 1's READY pages (OPUS, 2026-09-30)

SWE2-CONTRACT's batch 1 (`3754d9b4d`, record [`swe2contract-ddres-b1-0930/`](../swe2contract-ddres-b1-0930/README.md))
reported four pages of `00-Engine-Core-Runtime` READY for the owner read. The owner read is a completion read by OPUS,
not an independent review. It checks what `documented_rule.py` cannot see: every template section is filled, every
claim is tier-cited, and no prose residue is left without a register id or an answer
([the status-currency ruling](../status-currency-ruling-fable/README.md), "What the check cannot do").

## How it was read (OPUS, 2026-09-30)

- The log-call page was read whole.
- The other three were read by section: every heading was checked against the SYSTEM template, and every line
  carrying residue wording ("not established", "not known", "not searched", "unknown", "still open", open boxes) was
  read in context. So were the "what is not known" sections and the claim/evidence/tier tables in full.

## Result: no page moves today; each needs one small repair

| page | verdict | what is needed before DOCUMENTED |
|---|---|---|
| `Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md` | READY after repair | (1) Evidence table: add rows for RC-9 (all 245 sites pass 0 to 3; `rc9-log-channels-0930`, `e65c88dee`) and RC-10 (no caller-side verbosity gate; `rc10-log-gates-0930`). (2) Fill RC-10's "commit pending". (3) §7's first bullet, "What the channel id means": answer it functionally (in this build channel 4 is the debugger-break channel; 0 to 3 have no effect in the sink), and state the designer names as a limit (not in the image) with a disposition, not as bare prose. |
| `what-the-engine-fixes-at-boot.md` | READY after repair | (1) The id-10 bullet ends "whether code *selects* id 10 is not searched here": answer it with a static census of the arena allocation calls' id argument, or register it; as written it is unregistered residue. (2) Fill RC-2's "commit pending". |
| `Startup-Data-Construction/generated-float-table-builders.md` | READY after repair | §8 "What is deliberately not claimed" still opens "That these are shader tables, geometry, curves, or anything else", which BH-1 has since answered (VIF1 packets for the VU1 microprograms). Narrow it to what stays unclaimed: what the payload values mean to the microprograms is `UQ-213`. |
| `the-encoded-id-class-registry.md` | READY-WITH-POINTER after repair | (1) Fill RC-1's "commit pending". (2) Its status word is REOPENED; the owner re-status sets it once (1) lands. (3) Check that it does not carry the sentence AUDIT-SEM found false in the encoded-id contract ("only two functions address the registry"; `AUDITSEM-REQ-CONTRACT-REGISTRY-ADDRESSERS-0930`). A grep found no such sentence on this page. |

The repairs go to SWE2-CONTRACT with its batch 2 citations. OPUS re-statuses each page after its repair lands, and
records it here.

## Round 2: after SWE2-CONTRACT's repairs in `bed8dcd91` (OPUS, 2026-09-30)

`documented_rule.py` (FABLE's repaired rule, `86de1d661`) on the five READY pages: READY=4, READY-WITH-POINTER=1, FAILS 0.

| page | owner verdict |
|---|---|
| `generated-float-table-builders.md` | **DOCUMENTED.** §8's not-claimed line is narrowed to UQ-213. Re-statused by OPUS |
| `the-encoded-id-class-registry.md` | **DOCUMENTED** (pointer: UQ-80 SUPERSEDED on the status line). RC-1 cites `fe5dec46e`. Re-statused by OPUS |
| `the-formatted-log-call-and-its-level-gate.md` | READY. The repairs landed (RC-9/RC-10 evidence rows; the channel id answered by what it does, with the names as a limit). Re-status waits for RC-10's commit citation |
| `the-second-console-table.md` (new this round) | **DOCUMENTED after re-status.** Its one residue sentence ("what the codes name is not established here") is answered in the next paragraph (map-pack codes by field id; RC-6) |
| `what-the-console-tunes.md` (new this round) | **Needs one repair.** The page says "25 functions" reference or read the block in four places (lines 29, 88, 496 and the §8 evidence row, tier 1). Its own falsification pass 1 (2026-09-12, "Not reproduced") measured 28 referencing and 24 accessing. Re-measured here: **28 referencing, 24 accessing, 4 `lea`-only** (`00162410`, `001BC9D0`, `00607F00`, `008AB7C0`). Line 496's "24 of them outside the console" must be re-derived against the 24 accessors. The §8 block-span row still says tier 3, but pass 1 measured it exactly (1,132 B, 283 entries). This is a correction, so it needs a consumer-check record |

## Round 3: the last three batch-1 pages (OPUS, 2026-09-30)

SWE2-CONTRACT's repairs landed (`17a146c83`; RC-10 and RC-2 citations filled). `documented_rule.py`: READY on all three.

| page | owner verdict |
|---|---|
| `the-formatted-log-call-and-its-level-gate.md` | **DOCUMENTED.** Its evidence rows cover RC-9 and RC-10, RC-10's citation is filled, and the channel id is answered by what it does, with the names stated as a limit |
| `the-second-console-table.md` | **DOCUMENTED.** Its residue is answered in place (map-pack codes by field id; RC-6) |
| `what-the-console-tunes.md` | **DOCUMENTED.** The "25 functions" count is corrected to 28 referencing / 24 accessing in all three places, with a consumer check (`swe2contract-ddres-b3-0930/`); the block-span row cites pass 1 at tier 1 |

Batch 1's eight pages: six DOCUMENTED; `the-282-command-parameter-console.md` (RC-4) and
`the-event-slot-panel-and-its-dead-feeder.md` (RC-5) stay PARTIAL on registered rows.
