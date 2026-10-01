---
experiment: EXP-057
title: save checksum recurrence, covered bytes and source buffer
status: COMPLETE - bounded isolated original-code evidence
contract: ../19-Save-Load-Settings/CONTRACT-save-image-buffers.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original CRC helper and active getter without stubs; finalizer segment entered with injected destination and frame, earlier effects omitted.
contract_coverage: Original active-buffer getter 002EF640 and distinct active/staging identities in a checksum segment; no whole-image clear, copy, submission or full finalizer execution.
tool: evidence/EXP-057-save-checksum-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-057: save checksum recurrence, covered bytes and source buffer

**Result:** seven helper controls and eight finalizer-segment controls passed;
a one-byte-short range mutant was detected. ASTRA, 2026-09-11. No game process or
save file was accessed.

## Question and setup

The [save-image page](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)
leaves the checksum algorithm open as V-4 because the finalizer decompilation was
elided. This experiment tests the original recurrence and the finalizer's exact
source, interval, result destinations and order. Opposing hypotheses are a whole
image checksum versus a bounded prefix, and checksumming the selected output
buffer versus always reading the active buffer.

[check.py](evidence/EXP-057-save-checksum-controls/check.py) verifies the certified
EXE hash and extracts original checksum helper `003BB220` (160 bytes), active-buffer
getter `002EF640` (8), and complete finalizer `00583D60` (622). The helper and getter
execute without stubs. Finalizer execution starts at `00583F81` with an explicitly
supplied RDI destination and synthetic stack, and stops at `00583FA3` before the
cookie check/epilogue. Earlier finalizer operations are retained as static context
in the [disassembly](evidence/EXP-057-save-checksum-controls/disassembly.txt), but
are **not executed** or credited with establishing the injected state.

Active `02164280` and capture-staging `021BA940` each receive a full `0x56690`-byte
fixture. The active image has a deterministic byte pattern; staging is filled with
`A5`. This deliberate difference makes source/destination confusion detectable.
[Results](evidence/EXP-057-save-checksum-controls/result.json) retain helper inputs,
read ranges, outgoing checksum arguments, original write events and expected values.
The [manifest](evidence/EXP-057-save-checksum-controls/manifest.json) binds original
bodies, exact executed source, disassembly and results.

## Checksum helper

The original helper takes RCX data and EDX length. For a **signed nonpositive**
32-bit length it returns zero without reading the data pointer. The empty, `FFFFFFFF`
and `80000000` length controls use a null pointer and all return normally without
input reads. A positive length consumes exactly that many bytes in increasing
address order, with no input writes.

The recurrence is the reflected CRC-32 polynomial `EDB88320`, initial state
`FFFFFFFF`, eight right-shift/XOR steps per byte, and a final complement:

```text
state = 0xFFFFFFFF
for each input byte:
    state ^= byte
    repeat 8 times:
        state = (state >> 1) ^ (0xEDB88320 if (state & 1) else 0)
return state ^ 0xFFFFFFFF
```

Independent Python `zlib.crc32` controls agree for zero and FF single bytes,
`123456789` (result `CBF43926`) and all 256 byte values. The input-read hooks verify
exact byte addresses and widths; the helper reaches the caller return sentinel
with RSP advanced by eight. These small inputs test the same original body used
by the full finalizer interval.

## Finalizer interval and stores

At `00583F81` the original finalizer calls the active-buffer getter. RCX becomes
`active + 8`; the pointer subtraction at `00583F8A` gives low dword `FFFFFFF8`,
and adding `E200` produces EDX **`E1F8`**. Thus the checksum input is exactly:

```text
active image [0x0008, 0xE200)    length 0xE1F8 = 57,848 bytes
```

The original helper returns the CRC in EAX. The finalizer then writes, in order:

1. Dword `destination + 0xE200` receives the CRC.
2. Dword `destination + 0x0000` receives its bitwise complement.

The destination is the RDI selected earlier in the finalizer. The retained full
body shows R8D nonzero selecting capture staging and zero selecting active at
`00583D93..00583DA4`; the checksum segment calls the **active** getter again
regardless. The experiment supplies both destination values directly, with no
claim of having executed the earlier selection or metadata/party loops.

With staging selected, both stores affect staging but the checksum reads still
come from the distinct active fixture. With active selected, the same CRC results;
its two destination stores lie outside the input interval. Full active/staging
image comparisons check that no other bytes change in this segment.

## Discriminating controls

| Fixture change | CRC response |
|---|---|
| Output destination active versus distinct staging | identical CRC; stores follow destination |
| Flip active byte 0 or 7 | unchanged; first eight bytes excluded |
| Flip active byte 8 | changed; first included byte |
| Flip active byte E1FF | changed; last included byte |
| Flip active byte E200 | unchanged; checksum destination excluded |
| Flip active byte 5668F | unchanged; end of full image excluded |

Every finalizer-segment control checks the original helper call's exact pointer
and length, contiguous one-byte reads, the ordered pair of writes, both complete
images and the expected stop boundary. RSP, caller return sentinel, RDI and the
other supplied nonvolatile registers survive the segment.

The private mutant changes the finalizer's length-producing LEA constant from
`E200` to `E1FF`, shortening the interval by one byte. It executes and reaches the
same stop normally, but the read count is `E1F7` and the expected call/write/memory
comparison rejects it. All original cases passed on the first run.

## Meaning and remaining boundaries

V-4 now has original-code evidence for the exact recurrence and this finalizer's
range. This checksum does **not** cover the whole `0x56690`-byte save image. That
observation does not prove that the remaining bytes lack other integrity checks:
validators and the SAFH container pipeline are outside this experiment.

A tool reproducing this local operation must keep the active input distinct from
the selected output and store both the CRC and its complement. This is not yet a
complete external save-editing recipe: container decoding/encoding, earlier
finalizer effects, native buffer synchronization and load-time acceptance remain
separate requirements.

The retained finalizer also contains a direct OR of destination byte `+0x57` with
1 at `00583F63`, conditional on `00236760()` returning nonzero. This is a static
writer lead relevant to [EXP-056](EXP-056-save-normalize-roundtrip.md), not an
executed proof of when the native normalization flag becomes set. FABLE receives
that lead together with the checksum evidence; OPUS receives the field-width and
source/destination contract for structured integration.
