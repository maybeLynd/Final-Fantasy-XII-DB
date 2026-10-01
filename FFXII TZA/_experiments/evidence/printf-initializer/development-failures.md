# ASTRA — retained extraction failures; no semantic acceptance

This package uses static file reads only. No failed preparation below executed
FF12 instructions or created a live test process. No conclusions from another
experiment depended on this new checker.

- An exploratory Python import failed because `pefile` is not installed. Reused
  the existing `ext_string_probe.sections` parser; no dependency installation.
- A first exploratory import-name reader asked for a fixed 150 bytes near the
  end of `.rdata` and correctly failed its raw-section boundary guard. The
  retained extractor reads the actual NUL-terminated name byte by byte, bounded
  to 256 bytes and raw-backed section membership. No partial import map passed.
- First `check.py --capture --mutations` failed **before writing reference.json**
  at `assert state == {0x2EAECF4}`. That expected address was an arithmetic error
  in this new checker. `check.before-state-address-correction.py` is the exact
  rejected source. Independent decoding of all three original operands returned:

```text
00808DAA + length6  + 026A5F48 = 02EAECF8  (read)
00808DC3 + length10 + 026A5F2B = 02EAECF8  (write1)
00808E01 + length10 + 026A5EED = 02EAECF8  (write2)
```

The correction changes the expected address to `02EAECF8`, retains all three
independent instruction checks and records the state field's actual four-byte
width. It does not turn displacement `026A5EED` into an absolute address, or
infer actual live initialization from static bytes. The full focused extraction
and corrupted-evidence controls are rerun after this correction.
