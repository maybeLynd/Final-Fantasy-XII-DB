# Matrix transform: vector snapshot, matrix overlap and wrapper staging

**PASS_STATIC_ONLY — A. No new original-code or live execution.**
Primary source is exact committed GS capture `fcbffd545c30575039e80afc272680d6d71e9a38`,
whose source bytes/hash are checked against its manifest. Shipping image SHA
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Complete leaf `00217060`235B, RET21714A; wrapper `00202B70`31B, RET202B8E.
`source.json` retains raw bodies and decoded memory operands; source/consumer
preimages are retained unchanged.

Does the leaf stage all inputs, snapshot only the vector, or expose matrix reads
to its stores? Does the wrapper differ? Composer397910 has a separate alias
campaign; it was not replayed or used as a guarantee for this different leaf.
All claims assume normal ABI and arguments disjoint from private stack frames;
the leaf saves XMM6/XMM7 there before finishing its input reads.

The leaf loads X,Z,W,Y at217064/21706C/217086/217090, **all before** first output
store2170CE. Output may overlap the vector without changing the four snapshots
**when the matrix is disjoint from output**, memory stable and buffers valid.
Do not extend that to vector storage also lying in matrix words later overwritten.

Matrix reads are interleaved, not snapshotted. For `out = matrix + 8` bytes,
store2170CE changes word2 before read2170FF. Store21710D changes word3, but
read217104 already cached that word. This exact order matters; no arbitrary
partial-overlap guarantee follows.

Conditional exact finite example: input(1,2,3,1), matrix diagonal2/3/4 and final
row10/20/30/2. Disjoint result12/26/42/2; outputmatrix+8 gives12/26/**54**/2.
A per-column loop reloading matrix words after prior stores wrongly gives W=28.
These are source-derived calculations with exactly representable small values,
**not** new native alias executions.

Wrapper202B70 saves original output in RBX, passes private `rsp+20` to the leaf,
loads all16 result bytes at202B83 then copies them to output at202B86. All leaf
matrix reads complete before caller output changes. Under normal ABI/arguments
not overlapping private scratch, caller output can overlap vector or matrix
without the leaf's late-read hazard. This is a local guarantee, not engine-wide.

Leaf217069 puts its output address in RAX. Wrapper consumes it while the temporary
is valid but never replaces RAX with original output. At entry stack S, scratch
is S-18h; after return RSP=S+8 while RAX still names scratch. That residue does
**not** establish a declared C return type, caller use or later overwrite. A
usable caller-owned returned-output pointer is not promised; destination is
filled by the16-byte copy before frame teardown.

Current scripted-camera page §2.4 compose step3 says the call "returns the matrix"
and copies its first16B. The leaf writes a transformed **four-float vector**, not
the64B source matrix. FABLE should correct that exact description from this proof.
Camera timing/caller state/presentation are outside scope. OPUS owns primitive
ABI/alias qualifications; the existing correct vector/storage pairing is retained.

`check.py` validates body hashes, four input/output footprints, sole wrapper call,
read-after-write hazard and cached-word negative control, stack staging/copy and
RAX residue. Its conditional nonidentity calculation is not an emulator agreeing
with its fixture. No new B/C case, library effect, allocator/caller occurrence,
live lifetime/reuse, exceptional-float campaign, concurrent-writer safety or
all-engine alias census. Valid stable buffers and normal/private-frame ABI are
preconditions. Owner propagation and independent acceptance remain pending.

Read-only artifacts; PC OFF, no game/input/instrument/save/config/reference change.
Spent menu allowance unchanged. Accepted L1+L2/required reviews/final audit NOT_MET.
