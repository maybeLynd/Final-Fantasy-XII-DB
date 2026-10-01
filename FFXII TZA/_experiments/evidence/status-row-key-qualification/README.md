# Status name key and adjacent byte: source-bound correction

Result **A_ROW_KEY_AND_BYTE_BOUNDARY_QUALIFIED, pending independent review and
canonical owner incorporation**. No live experiment or isolated native execution.
Consumers: OPUS StatusDefinitionRecord and FABLE Status_Periodic_Terminal /
field-record schema; ASTRA's status-watch preparation is corrected in this package.

The retained US table has32 rows of40 bytes. Each row starts with a **two-byte
name key0x2800+row**, not an independently established one-byte ID. The next byte
varies: row0 hasFF, row3 has1B, row6 has1A and row31 hasFF. Accordingly their first
dwords are00FF2800,001B2803,001A2806 and00FF281F. A fixed001B28 prefix failed before
publication and was never accepted. This result does not call the whole dword a
name reference.

`source.json` pins the previously retained status table and the exact same full
US battle_pack entry (281128B, SHA d1bb89aa...), plus the new text-bank5/directory
slices. The archive index and selected compressed blocks remain identified by
`preflight-source-before.json`; the entire31GB archive has not been hashed. No
other language is newly examined. The32 name strings are independently decoded
from that same entry using the measured bank offsets/count/end sentinel and
full terminated packed blocks. Keys split as bank=word>>11, entry=word&7FF; row0
is KO, row3 Stop, row6 Doom and row31 X-Zone. This is representation/name
correspondence, not a screenshot or an observation of presentation.

**Direct original readers, not only a sibling-table analogy.** The verified
shipping executable73461d... has status-registry references to02EBF118 in the
query arm. It resolves records+0x0C through0020E600, multiplies stride+8 by query
row index+4 and then reads **word[record+0]** at0031E1D4 to shift11 and select a
bank through02EBF170. The second pass reads the same word at0031E20E and masks7FF
to select the entry. Their resolver result is stored in query+0x18 at0031E228.
The arm separately builds rbp from02EBF118/stride/row; **0031E248 reads byte[rbp+2]**
and0031E24C writes query+0x24. This corroborates the existing u16 nameWord and
separate u8 effectIdSlot02 type. What the effect byte indexes remains open;
the sparse11/12/14..1F bytes' meaning/readers remain open too.

**Capture failure and repair.** The first attempted range0031E1C0 begins inside
the call at0031E1BE; a decoder can consume its entire slice and still invent
plausible instructions. The proposed end0031C7FE likewise cuts the and at0031C7F9.
No failed transcript was accepted. `failed-boundary.txt` and `failed-collect.py`
retain that attempt. The repair starts from the exact function entry0031C5D0
also present in the image's RuntimeFunction directory and decodes its8136-byte
code prefix to the return at0031E597. The RuntimeFunction span extends128 bytes
further; those bytes are not asserted to be code. `query-function-code.bin`
preserves the actual code, and bounded transcripts are selected only from its
instruction boundaries. Focused controls reject both original invalid endpoints.
No other earlier instrument conclusion is retracted by this failed new capture.

`qualify.py` checks hashes, full original instructions, direct status/text registry
identities, widths and bank strings. Its7 rejecting controls include the wrong
fixed dword prefix, both bad endpoints, shifted string origin, transcript mismatch,
and a widened effect read even after repinning its code hash. It executes the
**actual retained old reducer** with a counterfactual changed key high byte: the
old reducer still reports42 sparse values. The new full-key predicate rejects it.
A changed+2 byte leaves the name word unchanged; this separation control is
explicitly counterfactual, not a valid shipping definition.

The existing `../status-watch-preflight/check.py` now checks the full name word
and adds the high-byte mutation. All eight previous controls remain (the low-byte
case label is corrected); the impacted run reports9. Original check, observation,
validation, directory and source are frozen here with Git provenance to
80c11162580b34d63bbd9b18704431ebb30535ec. Raw status bytes,42 sparse values, Stop/Doom
counts, coverage intervals and execute-only observer limits are unchanged.
No new reader, universal no-reader or live status semantics was established.

Propagation is **PENDING**: own preflight prose/checker are repaired; fields.tsv
already has the correct widths, but its nameWord primary citation should cite
this direct status arm; the field-record page still labels+0 asu8 id and needs its
owner's correction. The thirty-two-statuses page's corrected u16 name key agrees.
`consumer-check.json` records exact preimages and pending owner requests. An owner
return or an automated PASS does not constitute canonical acceptance.

No game process, control session, memory API, debugger or native-input library was
opened. Saves, configuration and reference binaries were only protected/read or
untouched; no restoration writes were necessary. Tool/interpreter/executable
identities and raw limits are retained. Run qualify.py from the repo root using
the existing project Python; no general platform or reconstruction was built.
