# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-contract-widget-object-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-WIDGET-OBJECT-HOMING-1002` · Package: `_index/candidates/opus-contract-widget-object-homing-1002/` · Page: `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). Rows `002D6DE0` and `003FACF0` are exact (read in full). Row `00568BB0` (read in full, 0x423 bytes) states a stored colour wrongly. See below.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing / notes

**Defect (row `00568BB0`).** (1) Element `+0x48`: the row gives byte `+0x343` as the top byte whenever byte `+0x353` is non-zero. The bytes do that only when word `+0x350` is non-zero (`00568C90` `cmp word [rdi+0x350],0` / `je 0x568cc4`). When it is zero, the top byte is byte `+0x350`, which is 0 (`00568CC4` `movzx eax, byte [rdi+0x350]`). (2) Elements `+0x20` and `+0x28` (the non-zero-`r9d` path): the row says only that they are "filled ... from the entry's byte `+0x14` and qwords `+0` / `+8`", and that the `002CC8D0` top-byte rule applies to "each of these colourings". In the bytes, each stored colour (`+0x24`) has a base value: the element's dword `+0xC`, or `002DD7E0(2)` when entry byte `+0x14` is 0 or byte `+0x15` is 2 (`00568E2B`..`00568E41`, `00568F05`..`00568F1B`). It is then **replaced outright by `002DD7E0(6)`** when entry byte `+0x17` is 1 (element `+0x20`, `00568EC5`) or 2 (element `+0x28`, `00568FA8`). That replacement discards the `002CC8D0` adjustment the row says is stored. Also, each `002CC8D0` gate tests one value of byte `+0x33E`: 0 for elements `+0/+8/+0x10` with 0x60, 1 for `+0x20` and 2 for `+0x28` with 0x80. The row says "equal to 0, 1 or 2". **Repair:** state the `+0x48` colour as "dword `+0x354` when byte `+0x353` is 0; else the element colour with top byte `+0x343` when word `+0x350` is non-zero, or `+0x350` (0) when it is zero". For elements `+0x20`/`+0x28`, add the base colour rule and the `002DD7E0(6)` replacement on byte `+0x17` = 1 / 2. Pair each `002CC8D0` gate with its own `+0x33E` value. Then re-run `interior_applier.py`.
