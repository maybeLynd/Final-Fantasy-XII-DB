# Actor ordinal to category and request preset

**Question.** For the one retained US `asp_a03` actor 25 `ラバナ_通常_NPC01`, does the native allocator/initializer connect its directory entry to kind-table row 6 and the request-word preset enabling `talkhold` / `talkterm`? FABLE's `ov16-motion-functions-fable-0930/README.md` §4 explicitly left the header-count-to-carve link unread. This package answers that source/data premise. It does not answer the parked function's natural cancellation/reentry timing.

**Player view.** The map data places this NPC in the category whose initial preset enables both conversation scripts. The native category comes from where the NPC sits in ordered category groups. The printed category label agrees here, but changing that label alone would not change this assignment path.

## Method and identity

Method A is sufficient: inspect exact shipping instructions and one retained archive member, prove the loop's ordinal invariant, and check the descriptor binding and preset branch. No original instructions execute; no FF12, emulator, native harness or PC-control session runs. No new corpus census or FABLE sample experiment is repeated.

EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base `0x120000`. `source-01.json`, `source-binding-01.json`, `source-setup-01.json` preserve exact bytes, boundaries, annotations and hashes for allocator `2679F0`, initializer `266530`, preset `266BD0`, filer `268EA0`, pre-preset region initializer `266AD0` and manager entry `26CE60`. Both native kind/switch data tables and the region switch are separately captured and checked against that EXE. All three actual capture paths use the reviewed shared access-role adapter, including store, LEA/address-only and read/modify/write controls.

Raw map input: `asp_a03-US-original-01.ebp`, 80,000 bytes, SHA-256 `e92d26899e523429695a97686732abdc46b518487f2870e4ba258fef16977a15`. `archive-member-01.json` identifies the archive by its 31,196,932,183-byte size, 11,995,716-byte header digest and exact member record/name/offsets. The two retained compressed blocks are strictly decoded and agree byte-for-byte with this map input. **There is no complete archive hash or assertion of installation authenticity.** This is precise header/selected-member provenance, not a live-resource binding observation. Archive handles close after the bounded read.

## Established source/data result

The native allocator reads the signed DWORD header `+14` offset, then a WORD row count and successive WORD counts. This member has eight rows and counts `[9,11,0,0,0,4,72,0]`, summing to the DWORD directory count 96. The closed original allocator CFG supports this induction:

1. Before row 0, ordinal counter `EBX`, row `R10D` and count-byte offset `RDI` are zero, and `R8` points at the native kind table.
2. For row `k`, each inner iteration publishes the record pointer in `pool[1 + old EBX]`, increments `EBX`, stamps the low five bits of actor `+3` from `k`, stamps the upper three from the native table's kind, and advances by the rounded native size. The WORD count controls exactly how many iterations occur.
3. The outer step increments `k`, adds 2 to the count offset and 4 to the native table pointer. A zero-count row skips the inner loop but still advances the row.

Therefore ordinal `i` belongs to row `k` exactly when `sum(count[:k]) <= i < sum(count[:k+1])`, under the stated valid-input premises. Row 6 spans ordinals **24–95**, so actor 25 is row 6. The shipping row has kind 3, sub 0 and size 1,760 bytes; the stamp is `+3 = 0x66`.

The same pool and ordinal are passed to `266530`. It selects `RBX = pool[1+i]` at `26656A`, then binds `actor+40` to `desc + signedDWORD(desc+18) + 4 + 48*i` for this version-11 member. Actor 25's exact directory entry is section offset `D2A4`. CP932 decoding is strict and its raw name bytes are preserved. The pre-preset helper's original row-6 path does not overwrite `+3` or the volatile ordinal carrier. Original `266BD0` selects its row-6 switch target and writes **`0x30004`** at `266C12`: bits 16 and 17 are set. Original `268EA0` tests those masks for the conversation-script gates.

The six direct later request-word AND/OR writes in `266530` preserve bits 16/17. **This is not a proof of final flags after transitive callbacks or the initializer's `266ACA → 3DB280` tail.** Those effects and natural scene initialization remain separate.

The directory's WORD `+4` is 6 in this exact input. The assignment/binding/preset path does not use it as an independent selector. A labelled synthetic data countermodel changes this field to 7 while leaving counts and ordinal fixed: the source-derived row stays 6 and its preset stays `0x30004`. This does not prove that malformed labelled data occurs in the game or that every shipping directory label matches its count-prefix row.

## Validation and failed hypotheses

`prove-03` / `result-02.json` is the current producer-valid result. `control-02` / `control-result-02.json` passes three actual CLI prerequisite refusals, seven focused synthetic source controls, two data-interpretation refusals and the label countermodel. These are producer checks, not independent acceptance or native samples. Missing binding status, a failed capture exit and a missing compressed input block cannot produce a semantic result. Source controls cover count width, ordinal-row advance, stride, native table identity, pre-preset category overwrite, missing preset bit and an unsupported tail. Strict archive decoding separately refuses truncated and wrong-length zlib data.

The initial proof failed because the initializer exits by a tail to `3DB280`; it produced no result. The exact failed driver, receipt and correction are retained. The repaired proof explicitly bounds that tail and leaves its effects open. The first control run changed only a printed store operand, leaving the access annotation inconsistent. It failed before a control result; its history and receipt remain. The corrected control changes both representations and verifies refusal. A preliminary console preview used the wrong name-pool origin; the actual proof uses `pool+nameOff`, exact raw CP932 identity, and a wrong-origin regression. No published or valid source result was overwritten.

## Limits, consumers and remaining work

Assume valid, stable, disjoint descriptor/pool/frame storage, adequate allocation, normal native ABI/returns and a manager count covering ordinal 25. This is not all malformed-input safety, allocation placement, ownership/lifetime, loaded pointer identity, scheduling, successful command acceptance, or the actual initial/final state of a running scene. Later callbacks, the tail and natural `talkterm` wait/cancel/reentry/receipt timing are open.

**Required consumers:** FABLE may replace the unread count-prefix/carve premise for this actor with this bounded source/data proof; preserve OV-16's actual timing gap. OPUS may incorporate the ordinal/category/descriptor and preset-point qualifications in its owned types/contracts. SPEC must independently review the original loops, switch/volatile-carrier reasoning, archive provenance and real prerequisite/control paths. Producer validity, immutable publication integrity and independent acceptance remain distinct. No peer-owned page is edited here; full L1+L2 completion is not asserted.
