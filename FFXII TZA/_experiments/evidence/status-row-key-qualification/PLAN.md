# Status row identity: qualify the two-byte key, preserve adjacent effect byte

Question: does the retained row's first-byte correspondence establish a separate
ID field, or is it the low byte of the current type's two-byte name key? Does a
four-byte interpretation wrongly include the independently copied effect byte?
Consumer: OPUS StatusDefinitionRecord and FABLE's field-record/current status page;
ASTRA's sparse-slot preflight must stop describing an embedded standalone ID.

Existing evidence: immutable status-watch-preflight raw table/hash, current
fields.tsv nameWord at+0 width2 and effectIdSlot02 at+2 width1, older field schema
u8 ID, and shipping status-add byte-copy address31E248. The proposed fixed dword
001B2800+row failed already: rows0/6/31 carry different third bytes.

Method A is sufficient. Reuse the retained table; compare the exact same US
battle_pack entry identity and extract only its bank5 text plus bounded original
instruction bytes. No game launch, input, live instrumentation or native execution.
Do not rerun accepted captures. No broad static sweep or lab change.

Discriminator: all32 two-byte values equal2800+row and independently resolve to
32 status names in bank5; third bytes vary and original code reads+2 as a BYTE
into a separate destination. A sibling text-key idiom alone cannot establish this
table's native reader; disclose if only representation/name correspondence is proved.

Controls: exact entry/table/executable hashes; complete bounded decode; text-bank
count/end sentinel and full strings, including KO/Stop/Doom/X-Zone; corruption of
name key's high byte must fail the revised reducer although the old byte-only
control accepts it. Mutating+2 must leave the two-byte key unchanged. This does
not mean the effect byte is semantically arbitrary. Retain all prior sparse-slot,
coverage and observer limits and historical8 controls; no semantic reader closure.

Budget: one bounded retained-table/resource/code reduction and focused correction.
Stop on source mismatch, ambiguous block boundaries or unsupported receiver identity;
return exact residue rather than invent a four-byte field. Save/config/reference
restoration: none needed for read-only offline work; record no native API use.
Review: independent AUDIT-SPEC, then FABLE/OPUS owner propagation; routed is pending.
