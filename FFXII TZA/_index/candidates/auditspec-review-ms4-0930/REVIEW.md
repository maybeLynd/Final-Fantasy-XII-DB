# SWE2-AUDIT-SPEC review - MS-4: the preload page's message 14

Task: `OPUS-REQ-AUDITSPEC-MS4-0930`. Package: `_index/candidates/opus-ms4-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `ms4_check.py` re-run: FAILS 0 (M1-M5: the container procedure's 0x20 arm sends {14,0,index,0} with index = `003BC160()` in mode 6 else `003C0380(field)`; `003CB4F0` takes id 14 to its preload arm; senders `00292AB2`/`003CB835` plus static struct `00246BFF->01E0C0E0`).

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
