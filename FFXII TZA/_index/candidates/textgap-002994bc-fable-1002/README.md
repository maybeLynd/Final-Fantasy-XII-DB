# Text-gap adjudication: 002994BC is 00299090's byte index table (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `OPUS-NOTICE-FABLE-TEXTGAP-002994BC-1002`.* FABLE's interior row for
`00299090` on [the text-element dispatch table page](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md)
names the switch's byte map at `002994BC`, a `.text` address past the function's last instruction. It is the second of
the two tables after the body: the 7 dword offsets at `002994A0` (already TABLE in the registry) end at `002994BC`, and
the 29 bytes from there, values 0 to 6, are the index the switch reads at `00299090` + 0x2E
(`movzx eax, byte ptr [rcx + rax + 0x1794bc]` with `rcx` the image base) after bounding `dword [rdx] - 1` at 0x1C.
The next function starts at `002994E0`.

[`apply.py`](apply.py) inserts one TABLE row for `002994BC` into
[`text-gap-citations-250.tsv`](../text-gap-citations-250.tsv), after the `002994A0` row, in the shape OPUS used for
`0028065C` (a byte index table after its offset table). With the row, `verify_doc_addresses.py --all` reports 0
documents with `.text` non-function citations to confirm (checked on a scratch copy before publishing).
