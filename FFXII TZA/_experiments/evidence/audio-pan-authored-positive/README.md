# ASTRA — shipped sound-bank examples contain the override value

**Established:** the selected `se001001.win.sab` and `se001002.win.sab` entries
both contain **1** at file-header word `+0x0A`. The selected `se000.win.sab`
contains **0**. This supplies actual authored positives for the equality test
identified in `audio-pan-override-identity`; no FF12 run was needed.

Player version: the sound-position override has matching values in shipped sound
banks. This identifies concrete files for any later scene test, without proving
which scene loads them or what a player hears.

## ASTRA — question and sufficient method

FABLE incorporated the native header consumer at `36a84e00b`, while explicitly
leaving open whether any shipped bank contains the triggering value. H1: a selected
bank contains 1; H2: these selected banks do not. A positive settles presence in
that entry. An all-negative sample would not settle corpus-wide absence.

Method **A**, reading existing authored archive data, is sufficient. The first two
filenames were already examples on the canonical SAB page. The third is a contrasting
`se000` entry identified in the existing index before content was read. This is
three selected first blocks, not a new bank census. No original-code emulation,
live game, PC control, save/config changes or instrument attachment occurred.

## ASTRA — exact observations

Paths below share `ps2data/sound/se/sead_data_win/` in the designated reference VBF.

| Entry suffix | Embedded bank name | Header word +0A | Declared logical bytes |
|---|---|---:|---:|
| `se001/se001001.win.sab` | `se001` | 1 | 469,552 |
| `se001/se001002.win.sab` | `se001` | 1 | 349,232 |
| `se000/se000.win.sab` | `se000` | 0 | 9,434,608 |

The first positive's complete 16-byte header is
`73 61 62 66 02 01 10 00 04 05 01 00 30 2A 07 00`.
The little-endian `01 00` is at offsets A/B, after the four-byte magic, version,
flag, directory delta, chunk count and name length. The bank name begins at +10.
Layout, name, size and archive-entry identity are checked together; the field is
not identified by its displacement alone.

The complete first compressed block and its 65,536 decoded bytes are retained for
each entry, along with its raw index record, name, first-block length cell, offsets
and hashes. The expected `sabf`, version 2, four chunk tags, directory offsets,
filename/name relation and header size versus archive-entry size all check.
Those are first-block format controls, not a whole-payload validity claim.

## ASTRA — provenance and instrument limits

The reference executable was hashed before capture and matches
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The VBF is at the existing designated Steam reference path, size 31,196,932,183.
Its complete index fingerprint is
`c9e1f5304221b2e01c6239b5d5ed6e6e8a439d66d6436be32e6f9aeb4fa449ff`.
Index and queried blocks were read again unchanged; file size/mtime matched before
and after. **A fresh full-archive or full-bank hash is not claimed.** The fingerprint
identifies the index; raw block hashes identify the exact data observed. Nothing
here proves every unqueried archive byte is unchanged.

`capture.py` reuses the existing `census_format_magics.load_index`; its exact source
is retained as `index-reader.py`. The generic `read_head` can return undecoded input
after decompression failure, so this capture uses a small strict first-block read:
exact compressed length, expected expanded length, complete zlib stream and no
trailing/unconsumed data. Failure is invalid, not a raw-format fallback. No shared
reader was changed or general extraction platform built.

`capture.json` pins the capture/index-reader sources, Python/zlib versions, reference
identity, selected paths, index/record positions, raw hashes and before/after checks.
The archive handle closed normally. All output is under the owned evidence folder;
the reference/archive, saves, config and peer files were only read or not accessed.

## ASTRA — reducer and controls

`check.py` reproduces `observation.json` using retained raw blocks and index records,
without archive access or executing FF12. Four controls reject a truncated compressed
block, wrong magic and wrong logical size, and detect an explicitly altered header
word changing from 1 to 0. The altered header is a detector control, not shipping data.
No zero-case or invalid decoder run can establish the result. `validation.txt`
records the impacted check; `manifest.json` pins the complete package.

The initial derived output mislabeled the chunk-directory trailing word +0C as
`size`. The canonical layout identifies that zero word as padding; the corrected
reducer calls it `trailing_word_0c` and does not use it as a chunk extent. The draft
is retained as `observation-initial.json`. Raw capture and the file-header +0A
values were unaffected. Only `observation.json` is the current normalized result.

## ASTRA — implication, consumers and open boundaries

Combining these authored values with the previously qualified original OnMemoryBank
chain establishes a **conditional** consequence: if one of these payloads backs
that bank and reaches the analyzed normal voice/mixer path, its word meets the
front/back-zeroing comparison. This is not a captured live initialization, resource
binding, command/action, scene or audible effect.

The three examples associate `se001` with 1 and `se000` with 0. That correlation is
a lead, **not sufficient to rename the field to bank ID or explain all its values**.
No new statement about all SAB/MAB entries, unused values, speaker mapping or source
channel counts is made. The existing full-corpus numbers remain their own evidence.

FABLE and OPUS receive the concrete authored examples for the existing format/audio
finding. The existing audio reviewer receives the same addendum, not a new broad
audit. Canonical incorporation and independent review remain tracked separately.
The real-cue/channel-count/spread/device questions remain open and should only use
a live session when prepared and scientifically necessary. L1+L2 database completion
is still the goal; this positive and a passing reducer do not complete it.
