# SWE2-AUDIT-SPEC review - render null-group: the 0041CF00 zero-rcx call's unreachability

Task: `OPUS-REQ-AUDITSPEC-RENDER-NULL-GROUP-0930`. Package: `_index/candidates/opus-render-null-group-0930/`.

## Verdict: ACCEPT

Evidence class: NATIVE/STATIC. The package's control(s) were re-executed on this host against the
certified image / installed assets, and the named anchors were read off the image directly.

## Independent verification

- `null_group_check.py` re-run: FAILS 0 (N1-N5: bit 0x1000 of payload +0xC is set only by `0041D4D0` after an intervening condition, so the null-rcx arm cannot reach `00372280` with a live group).
- `0041CF00` head verified: the loop initialises `rcx`/`r8d` to 0 under the word bound `[rbx+0x28]` - consistent with the recorded shape.

## Limits

Checker reproduction carries the package's mechanical claims; semantic prose-scope judgements follow
each record's own declared scope. Any narrowing is named above; none is a weakening of the claims.
