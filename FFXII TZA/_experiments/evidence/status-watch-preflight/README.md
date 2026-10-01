# Sparse status-slot watch: source-bound preparation correction

Result: **PREPARATION_CORRECTION, NO_LIVE_RESULT**. Consumers: OPUS structural
types/contracts; FABLE Status_Periodic_Terminal; FRONTIER experiment preparation.
Source request: `OPUS-REQ-ASTRA-STATUS-DEFINITION-SPARSE-SLOT-SPAN-LIVE-WATCH`.
No game launch, process inspection, input, attach, native call or experimental
write occurred in this package. No status reader or universal non-reader is
established.

The question is whether sparse authored definition bytes have a reader missed
by the static census. Competing explanations include a reader on the selected
transition, a reader on some other path, or no read during that selected state.
Method A is sufficient to correct the proposed row, coverage and detector
assumptions before committing a live observation. It cannot decide reader
reachability or the bytes' meaning.

`source.json` identifies the exact installed Steam VBF entry, complete selected
entry hash, archive index and selected compressed-block hashes, extractor hash
and table/directory slices. Whole31GB archive content was not hashed. The US
entry is281128B; directory+0x40 points to0x1B178. Its1312B st2e slice has32 rows,
stride40, records+0x20; all32 complete u16 name keys equal0x2800+row. Other languages were not
examined. Row6's beat100, row2's45, row8's120, Stop's clear-mask bit17 and
X-Zone's7FFFFFFC are positive structural/value controls.

The42/448 non-FF aggregate and range25..31 reproduce. This does not by itself
identify the values as status IDs or establish that FF is a runtime sentinel.

| row ID | current canonical name¹ | populated sparse offsets and bytes | proposed+14 single8B misses |
|---:|---|---|---|
|3|Stop|16:31,17:29,1C:31|1C|
|6|Doom|none|no populated-byte positive control|
|14|Immobilize|14:28,15:30,1C:29|1C|
|26|Float|14:31,15:31,1A:31,1C:30|1C|

Offsets are hexadecimal; values decimal. The request's “row3 Doom has four” is
not supported: row3 has three, row6 has zero. ¹Names were initially cross-referenced
to `10-Status-Periodic-Terminal/the-thirty-two-statuses.md`. The later bounded
`../status-row-key-qualification` independently decodes the same US entry's bank5
and qualifies original reads of the two-byte name word and separate+2 effect byte.
The original first-byte match did not prove a standalone u8 ID field. Complete
name keys and populated-byte counts come directly from the retained shipping table.

The14 sparse slots are11,12,14..1F. `observation.json` includes every populated
coordinate and byte-interval coverage for1/4/8B starting14. These are pure byte
intervals, **not qualified hardware encodings/alignment specifications**. Even
the widest proposed interval14..1B misses1C in rows3/14/26 and excludes11/12 in
every row. A15B interval11..1F is a reducer positive; it is not a single-watch
hardware configuration.

`observer.json` freezes the existing hwbp.py `set_slots` function and whole-source
hash. It initializes DR7 to zero and only sets local enable bits; the source
explicitly selects RW00/LEN00, execute conditions. It cannot be used as a
qualified read-watch detector. This is a static capability finding, not a
failed/attempted live installation. No general watcher backend was built.

`check.py` reconstructs the table and coverage, checks the frozen observer
source, and now rejects nine corruptions/invalid controls: wrong directory target,
count, stride, truncation, changed name-key low/high bytes, empty watch budget,
empty Doom positive and incomplete Stop coverage. Run with the existing project
Python. PASS means these preparation checks ran; `semantic_live_closure` is empty.

Correction 2026-09-27: the high-byte control rejects a name-key corruption the
first-byte-only predicate accepted. All original eight controls remain, with the
low-byte label corrected; original receipts/checker/observation are retained in
`../status-row-key-qualification` and original commit80c11162580b34d63bbd9b18704431ebb30535ec.
No sparse coordinate/count, raw source, coverage or observer result changed.

For a future C experiment, the consumer must prepare a named status/state/save
and normal apply/remove or expire trigger; fresh actual table/row pointer identity
and lifetime checks; complete declared watched-byte coverage; a qualified read
observer with in-session positive detection and baseline; accepted/executed
transition proof; bounded event/time budgets; game responsiveness/fatal-dialog
checks; stop, detach and save/config restoration. A scoped positive can establish
a reader on that path. A scoped negative can establish only no detected reads
within the stated qualified coverage/state/window, never universal authored-dead.
The completed S19 input stop-loss remains a separate blocker for new setup.

Affected claims: correct row/count in the pending runtime request; retain the
valid42-byte population; remove universal-dead closure from acceptance criteria;
keep `_types/fields.tsv` semantic gaps open until supported consumer adjudication.
Peer canonical files remain under their owners. Raw evidence, normalized
observation and focused controls are preserved; no cleanup/restoration writes
were needed because the game was never touched.
