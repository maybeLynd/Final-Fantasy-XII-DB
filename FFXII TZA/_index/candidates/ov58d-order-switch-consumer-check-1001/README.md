# OV58D order-switch correction — consumer check (EVIDENCE-POLICY 4a)

Consumer-check record for the additive repair of the OV58D caller-cone and
residue records under `ASTRA-RETURN-STRUCT-OV58D-ORDER-SWITCH-1001`.

Refuted claim: message `0x4049`/`0x404A` reach `0030E360` via arms
`002FDF18`/`002FDF5A` with `r8b = 0xF8`/`0xD9`, out of the callee's `id <= 31`
contract. Correct decode: the dispatch at `002FDDA0` is a two-stage MSVC
compressed switch (selector byte `002FE54C+idx`, arm RVA `002FE534+4*sel` +
`0x120000`); `0x4049`/`0x404A` take selector 1 to arm `002FDE7B`, a 29-byte
local arm containing no call instruction. The two `0030E360` call sites sit
in arms `002FDF18`/`002FDF5A` serving `0x4051-0x4070` and `0x4071-0x4090`
with `r8b` in `0..31`.

Affected: `Database/FFXII TZA/_index/candidates/ov58d-pointer-flow-0930/CALLER-CONE-0030E360-0930.md`
Affected: `Database/FFXII TZA/_index/candidates/ov58d-pointer-flow-0930/RESIDUE-BOUNDS-0930.md`

## Consumers

| Consumer | What it carries | Agreement |
|---|---|---|
| `ov58d-pointer-flow-0930/RESIDUE-BOUNDS-0930.md` | the same refuted claim as a residue update | agrees — revised-here in the same publish; original text preserved struck. |
| `ov58d-pointer-flow-0930/README.md` | cites the residue-record result only | agrees — the residue existence/routing claim is unaffected; no edit needed. |
| `status-recursion-index-bound/dependencies/CALLER-CONE-0030E360-0930.md` | frozen vendored preimage of the uncorrected record | agrees — left untouched as dependency evidence; that package proves `0030E6C7` bounded `0..31` independently of the refuted line. |
| `fable-astra-live-facts-0930/t3b_ov58d_region_a.md` | cites residue existence ("unbounded indexed-writer residue is routed to SWE2-STRUCT"), not the arm decode | agrees — no F8/D9 or `002FDF18`/`002FDF5A` citation; its named-reach exception update is `ASTRA-RETURN-FABLE-OV58D-ORDER-SWITCH-1001` (board READY). |
| OPUS consumer task `ASTRA-RETURN-OPUS-OV58D-ORDER-SWITCH-1001` (board READY) | may cite bounded args at the two identified sites | agrees — this repair only narrows the site domains; OPUS's own task applies it. |
| `OPEN-QUESTIONS` OV-5/OV-8 | quote the residue routing | agrees — wording owned by FABLE; residue existence unchanged. |
| `_types` store / route rows | — | agrees — no row carries the claim (grep-verified). |
| Derived mirrors (`knowledge.sqlite`, `questions.json`) | may mirror the old text | agrees — stale by design; regenerated downstream, not edited. |

## Regression

- `Database/FFXII TZA/_experiments/evidence/ov58d-order-switch/prove-ov58d-order-switch.py`
  re-decodes the switch against the pinned EXE and compares every captured
  byte; its recorded result is `PRODUCER_CHECKED_STATIC_REFUTATION` with
  answer `REFUTED`.
- run: `818e85de6` (packet + independent byte review ACCEPT commit; ancestor
  of HEAD).
- Five recorded controls in the same directory (`failed-capture`,
  `wrong-0x4049-selector`, `changed-status-subtract`,
  `missing-selector-table`, `wrong-store-role`) all terminate with the
  expected refusal and produce no result.
- Independent recheck performed during this repair (logged in the
  caller-cone correction appendix): selector/arm table bytes read from the
  image reproduce the packet map; `002FDE7B` disassembles to 29 bytes with
  no `call`.
