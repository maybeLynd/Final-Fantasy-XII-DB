# Storage inner-read destination/cursor alias

Question: can the inner read guarantee the cursor advances by the copied byte count if its destination overlaps the cursor? Competing explanations are invariant advancement versus feedback from writing cursor metadata before incrementing/reloading it. Named consumers: OPUS/FABLE storage-read contract, SWE2-CONTRACT differential-domain qualification, SPEC independent review.

Method B executes the verified **116-byte pure original leaf at `00866A00`** with injected disposable memory/entry ABI. Reference executable SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`. Source/reader and DLL identities, read-back input registers/objects/stack, all visited instruction PCs, reads, provider writes, committed write bytes, returns and nonvolatile restoration are preserved in `raw.json`. There are no calls/stubs. The same shipping bytes run in each case. Each execution has a 128-instruction budget and stops at the injected return sentinel; failed identity/control would stop subsequent cases.

Shared byte vector is four bytes `0A 14 28 3C`, cursor starts at 0. Destination is either disjoint or the cursor's own low byte. The original byte store at `00866A4D` precedes the original dword cursor increment at `00866A54`; another iteration reloads the cursor at `00866A3D`.

| Requested count | Destination | Actual copy stores | Returned boolean | Final cursor | Relevant evidence |
|---:|---|---:|---:|---:|---|
| 1 | Disjoint control | 1 | 1 | 1 | destination `0A`, then cursor 1 |
| 1 | Cursor alias | 1 | 1 | 11 | byte store changes cursor to 10; increment changes it to 11 |
| 2 | Disjoint control | 2 | 1 | 2 | next cursor read is 1; source bytes `0A 14` |
| 2 | Cursor alias | 1 | 0 | 11 | next cursor read is 11, beyond the four-byte vector; short read |
| 0 | Cursor alias, no-copy control | 0 | 1 | 0 | no source/destination copy or cursor load/increment |

The count-1 alias case returns success **even though the final destination's first byte is `0B`, not `0A`**, because the cursor increment overwrites the aliased byte after the copy. This narrows the contract's unqualified cursor-advance and final copied-content guarantees. Its boolean still reflects the number of performed copy iterations in these cases; the evidence does not replace it with a partial-byte return.

Consumer change required: qualify the ordinary “cursor moved by the same partial amount”/copied-content statements with separation from cursor metadata, or state the demonstrated alias behavior explicitly. Preserve normal disjoint results and short-read semantics. The current 77-command differential has no destination/cursor alias cases; that limits its domain, not a claim its reconstruction is wrong within the tested domain. A consumer asserting this boundary should bind store-before-increment/reload order and preserve the precise source bytes; don't fix only a summary or silently sanitize the original behavior.

Scope: selected low-byte exact cursor alias, counts 0/1/2, and disjoint controls only. No other partial overlaps, whole storage/wrapper/backend effects, actual files/saves, native CPU parity, all malformed memory safety, normal caller reachability or observed game corruption. No changed source-code mutant was needed: input alias versus disjoint state and the zero-copy case directly discriminate the hypotheses. Memory/ABI was explicitly injected; this is an isolated original-code intervention, not unmodified gameplay.

Cleanup: all emulator instances disposable, no PC/game/process/input/instrument/save/configuration/reference binary or peer consumer change. Reader stops/ABI restoration and unchanged source vector/global identity were checked. `check.py` validates retained observations without rerunning the leaf. Independent review/consumer agreement remain separate from own checks/publication; full L1+L2 is NOT_MET.

Learned rule: stop once these writes/reloads settle the alias hypothesis. Do not run a live save-loading session to restate this bounded result or replay the existing 77-command suite without an affected change. Any future claim about normal caller separation needs its own source/caller proof.
