# SWE2-AUDIT-SPEC review - DD residue batch 20: map-screens + request-router

Task: `OPUS-REQ-AUDITSPEC-CONTRACT-B20-1001`. Package: `_index/candidates/swe2contract-ddres-b20-1001/`.

## Verdict: ACCEPT-WITH-NARROWING

Evidence class: NATIVE/STATIC (checker re-run on the certified image / installed assets, plus the named
spot-verified instructions). Reviewed the committed package as routed; no claims weakened.

## Independent verification

- `b20_checks.py` re-run: PASSES 36, **FAILS 1**.
- **Z1 fails for a reason outside the batch's scope:** the checker's `TAG = "DD batch 20"` substring match now also fires on `the-map-screens-and-their-shared-map-data.md` line 4 - the status line - because OPUS's later owner re-status `9545bad56` (batch 21, `opus-dd-restatus-21-1001`) cites "DD batch 20" by name. `got` is `expect` + exactly line 4; every one of the 23 declared note lines still carries its note, both strikes (map 333, map 1294) are in place, consumer-check.md exists, and the EOL conventions hold (map 1338/1338 CRLF, router 961/0 LF).
- The batch-20 work itself verifies. The narrowing: **the Z1 control is stale** - a literal-substring expectation cannot distinguish a batch note from a later citation of the batch. Route a control repair to SWE2-CONTRACT (exclude status/front-matter lines, or anchor on the note's parenthesised form).
- Spot-verified: the two `003BC160` corrections land on real claims (the `[+0x34]==0` -> `02B457DC` index write and the `02B457D9` byte store).

## Limits

Checker reproduction covers the package's mechanical claims; named anchors were additionally read off
the image directly. Prose-scope judgements (STALE/BOUNDARY/carried labelling) follow the batch's own
declared rule set and were not re-derived line by line.
