# Selected gambit bank exported into compatibility records

Method **A**, 2026-09-13. Claim: identify exactly what `00234ED0` prepares before
the two `0x6000`-byte compatibility copies. Distinguishing evidence: the complete
shipping function's source and destination operands, signed selector loads and
loop bounds. No emulator or live setup was needed to settle those operands.

**Player version:** saving copies the currently selected gambit set into each
character's older record. If compatibility import later runs, that set becomes
bank 0 and is selected; the other two sets are prepared from authored presets.
This is the native conversion rule, not an observed older-save load.

[primary.json](primary.json) retains every instruction byte, address and operand
for `00234ED0`, 489 bytes, SHA-256
`46ce76ee451bd778e2ac3782e52c397a1556df03e5450ff760620256b68cf57b`.
Reference executable SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `00120000`; collector and Capstone identity are retained.

For stable `B = *(02EBF190)`, the normal initialized interpretation is:

```
for i = 0..39:
    selected = signed_i32(B + 0x7370 + 4*i)
    source = B + 0x5B10 + (3*i + selected)*0x34
    destination = B + 0x90 + i*0x1C8
    copy 0x34 bytes, in order: 16, 16, 16, 4
```

The function reloads `B` for every one of five unrolled records. RAX advances
`0x8E8` per group, R9 advances `0x14` from `0x7374` to `0x7414`, and R10 advances
15 banks. Eight iterations write 40 separate 52-byte spans: `0x820` bytes total.
All bank bytes, including padding, are copied without a content conversion.
The complete body contains no calls and only the loop's conditional branch.
It does not change the selected-bank array or prepare banks 1/2.

**Boundaries:** selection is sign-extended, not clamped. This function has no
null or index guard. Out-of-range indices can address a different record or
other memory; under overlapping injected states the ordered moves must not be
replaced with an assumed snapshot. No such state was injected or executed.
Stable binding and initialized selectors remain native caller preconditions.

The already collected [importer and writers](../spawn-old-save-boundary/README.md)
provide the other direction. `00235AF0`, after a qualifying compatibility mismatch
and `002EF4A0`'s `0x6000` copy, copies the old per-record set to bank 0, rebuilds
banks 1/2, and zeros **selected-bank indices** at `+0x7370`. The earlier receipt's
generic `counters` interval label meant this array; its addresses and raw bytes
remain correct. This meaning is also documented in the existing
[battle-state field map](../../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md).
The importer does not write padding byte `+0x33` of its two rebuilt banks.

`005844A0` and `00229B40` call this exporter before their compatibility copy.
The former skips both when the current block's first byte is zero. The latter
also has a separate `0x8000` modern block capture. The joined source rule does
not mean that every modern load replaces the other sets: the importer has its
four-field mismatch gate, described in the preceding package.

[check.json](check.json) records fresh decoding of all 489 bytes, every unrolled
copy operand, signed selector loads, the complete loop, and exact reused
importer/writer bodies. Address arithmetic is a source normalization check,
**not original-code execution**. The first check used the wrong filename for
the retained importer and stopped with `StopIteration` before producing a pass;
[rejected-check.py](rejected-check.py) preserves it. The corrected check requires
the expected address and byte count in `helpers.json`; no game experiment was
repeated. The package has no B cases, live observations or file decodes.

FABLE/OPUS own propagation through save/gambit prose, types and executable
contracts. Their review remains pending. The next sufficient method for actual
old-save party/gambit and L-13 session state is **C**, using ordinary load and
initialized binding controls. No claim here establishes live scheduling,
historical-build code, title-load state, authored callback effects or player
presentation. Full L1/L2 and required final reviews remain incomplete.
