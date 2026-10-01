---
experiment: EXP-058
title: exact acceptance predicate of the runtime-format header helper
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies runtime-format header predicate 00255260; save-image-buffers covers whole-buffer clear, getter and copy, not header acceptance.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original eight-byte header predicate, synthetic inputs, no stubs; no whole-load acceptance claim.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-058-save-validator-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-058: exact acceptance predicate of the runtime-format header helper

**Result:** ten isolated original-code controls passed; an ignored-size mutant
was detected. ASTRA, 2026-09-11. No game process or save file was accessed.

## Question and method

The [save-image page](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)
marks `00255260` unusable because the decompiler displayed an empty conditional and
an unconditional true return. This package replaces that uncertainty with direct
execution of all paths in the original 45-byte body. It tests unconditional
acceptance against exact magic/size validation, including null and empty inputs.

[check.py](evidence/EXP-058-save-validator-controls/check.py) verifies the certified
EXE hash, extracts `00255260..0025528C`, and executes it without dependency stubs in
fresh Unicorn memory. Inputs are a null pointer or two dwords followed by an
`A5`-filled page. Read/write hooks cover non-stack mapped memory, and the script
checks return EAX, exact input read addresses/widths, no writes, the full input
page, return sentinel, RSP advancement by eight and all supplied nonvolatile
registers. A 100-instruction cap must reach the expected return boundary.

Exact [results](evidence/EXP-058-save-validator-controls/result.json),
[disassembly](evidence/EXP-058-save-validator-controls/disassembly.txt), original
bytes and executed source identities are bound by the
[manifest](evidence/EXP-058-save-validator-controls/manifest.json).

## Predicate and short-circuit reads

The local operation is exactly:

```text
if pointer == null: return true
first = u32(pointer + 0)
if first == 0 and u32(pointer + 4) == 0: return true
if first != 0x0131F3EA: return false
return u32(pointer + 4) == 0x00004818
```

The return is a full EAX zero or one. Null requires no input reads. A nonzero
first dword other than the magic rejects after one dword read; the second dword is
not touched. A zero first dword and the exact magic each cause the second dword
to be read. No data bytes are written and no callees are invoked.

| Input pair | Original result |
|---|---|
| null pointer | true; no input reads |
| 00000000 / 00000000 | true |
| 0131F3EA / 00004818 | true |
| 00000000 / 00004818 | false |
| 0131F3EA / 00000000 | false |
| 0131F3EA / 00004817 | false |
| 0131F3EA / 00004819 | false |
| 0131F3EB / 00004818 | false |
| FFFFFFFF / FFFFFFFF | false |
| 20050223 / 00001538 | false |

The private mutant replaces `SETE AL` at `00255283` with an unconditional `MOV
AL,1` and padding of the same extent. It still performs the size read and returns
normally, but incorrectly accepts size `4819`; the semantic assertion detects it.
The original cases and mutation control passed on first execution.

## Scope and integration

This helper is neither an always-true function nor a general checksum validator.
It accepts an absent/zero pair and otherwise requires exact constants; it never
reads beyond the first eight input bytes and never calls the checksum helper
from [EXP-057](EXP-057-save-checksum-controls.md).

The existing [header-access evidence](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-header-accesses.tsv)
places its argument at image `+0x68` in caller `00280140` (`00280372`). The
[payload field map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)
records the same magic and `4818` size at image `+0x68/+0x6C`, written by
`00253A80` for the image-backed state block. That is existing static context;
this experiment does not execute that caller, initializer or a whole load.

FABLE should replace the active "unusable/outcome not visible" description with
this bounded predicate, preserving the historical decompiler failure. OPUS should
record the two-u32 input contract, short-circuit reads and exact returns alongside
the image-backed block evidence. A local true return on null or all-zero input
does not establish that a complete missing/zero save is accepted by the game.
Caller reactions, other format gates, CRC validation and container decoding remain
outside this package.
