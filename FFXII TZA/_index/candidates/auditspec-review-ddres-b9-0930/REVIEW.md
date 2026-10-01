# SWE2-AUDIT-SPEC review - DD residue batch 9: VBF index + area-nmb pages

Task: `OPUS-REQ-AUDITSPEC-DDRES-B9-0930`. Package: `_index/candidates/swe2contract-ddres-b9-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `b9_vbf_nmb.py` re-run on this host: FAILS 0 (incl. N8 - the .fst name read `002E03F5 mov r9,[r10+r8*8+0x1D68B00]` with r8 written once from the argument at `002DF9C2`).
- Spot-verified on the certified image: `00324510` is a small 3-arm dispatcher (the dormant kind-26 assembler claim is consistent with its body shape - arms selected on `ecx` 1/2/other).
- The batch's dispositions (index record layout sec.3a, MD5 path keys via `0019AEE0`/`001F47D0`, 15+1 reader handles, per-64KiB-block zlib, kind-26 resolution chain `0032E620`->`0032E870`->`0032E070`->`0046E030`->`002DF780`, size-array end 2963) are all mechanically re-checked by the package control against the image, the installed VBF and the .fst files.

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
