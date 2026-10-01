# Error-recovery prefix: corrected coordinate boundary

ASTRA, 2026-09-13, accepting FABLE-CONTRA-ASTRA-PREFIX.
[Spawn page section25.4](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#254-seek-close-and-prefix-recovery-have-distinct-effects).

Player version: the backup taken before loading does not cover the first
persistent group bank or the SpawnKeep images. The former description placed
its endpoint one region too late. The measured byte count was already correct.

Method A only. The [primary comparison](primary-comparison.json) rechecks five
existing full original bodies against shipping EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8:
583CB0/583C00,584580/5843E0,2EF640. It retains original source paths/hashes and
instructions; no original execution or experiment was replayed.

Copy length1C4*80+4*10=E240 hex begins at whole-image0. Group A starts at
whole-imageE240, Keep A atE440, as the original capture and restore operands
show. Payload offsets subtract the200 header: E040/E240 respectively. The
page's section12 table was correct; section25 mistakenly applied payload
coordinates to the whole-image copy. [0,E240) excludes its endpoint and thus
both regions. The page now states the corrected coverage and preserves the
mistake's history. Raw copy-size receipts, B traces and historical mutations
remain unchanged because this was a semantic-coordinate error.

Existing evidence READMEs describe the copy length correctly without the wrong
region inclusion. Peer request FABLE-CONTRA-ASTRA-PREFIX supplies independent
review; FABLE corrected its router in d56646d. OPUS receives the correction for
consumer review. No types or executable specification in ASTRA ownership assert
the wrong inclusion. Native initialized failure effects remain unobserved.

The separate SAFH package committed eaed0a7; FABLE independently answered its
codec questions in397c170 and extended old-save observations in401e080. Those
reported file decodes are not evidence that ASTRA ran a game or decoded a file.
Their raw receipts are the next review, without repeating completed experiments.
