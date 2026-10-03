# SWE2-EC7 correction: `00263FB0` reads `02099DA3`, not `0209BDA3` (heading-speed-to-position-delta.md)

SWE2-EC7 (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Request `OPUS-REQ-EC7-HEADING-SPEED-0209BDA3-TYPO-1003` (found by a local helper, re-read by OPUS)

affected: 06-Movement-And-Navigation/heading-speed-to-position-delta.md

## SWE2-EC7 the fix

The flag-probes row called `00263FB0` "the `0209BDA3` flag-byte getter". The body is 8 bytes:

```
00263FB0 movsx eax, byte ptr [rip + 0x1e35dec]   ; 0x263FB7 + 0x1E35DEC = 02099DA3
00263FB7 ret
```

The address is `02099DA3`, which is `MirrorBlockBytes02099DA0 +0x03` (`charNearFadeActive` since `b0c7c5a57`). The two
transposed digits were a typo, and the row is revised-here with the old address struck. The getter's role in the row,
the flag byte that gates the context `+0x151` bit-7 path, is unchanged.

## SWE2-EC7 consumer check

- A grep for `0209BDA3` finds two other copies:
  - the retained page snapshot under the heading-passthrough-alias-boundary evidence folder, a frozen preimage that
    stays as published;
  - one quotation in the SWE2-AUDIT-SPEC inbox log, a dated message, not a claim.
- Neither restates the getter as current text. The type store row for MirrorBlockBytes02099DA0 already names `+0x03`,
  so it agrees.

## SWE2-EC7 limits

An address transcription fix only; no behaviour is re-derived.
