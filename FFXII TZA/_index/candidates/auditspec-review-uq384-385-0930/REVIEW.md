# SWE2-AUDIT-SPEC review - UQ-384/385: PrimitiveRendererD3D11 at [01FC35F8]

Task: `OPUS-REQ-AUDITSPEC-UQ384-385-0930`. Package: `_index/candidates/swe2struct-uq384-385-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `uq384_385.py` re-run: 41 checks, FAILS 0.
- Spot-verified `0021037B`: `mov qword ptr [rip+0x1DB3276], rdx` resolves to `01FC35F8` exactly - the claimed sole writer. `[01FC35F8]` = `02CC0410 + 0x18C0` embedded PrimitiveRendererD3D11 per the record.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
