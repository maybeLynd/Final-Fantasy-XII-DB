# Matrix consumer checker: identity guard missing

**CONFIRMED offline checker gap; no matrix semantic retraction.** The canonical
published `matrix-alias-consumers/alias_check.py` passed all five obligations
(`L1`, `L2`, `L3`, `W1`, `S`, `FAILS 0`) in both prepared controls:

- exact reference image SHA256
  `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`;
- disposable memory copy with just DOS-reserved byte `0x28` XORed by 1,
  producing a different whole-image SHA256, with the complete cited
  `00217060` 235-byte and `00202B70` 31-byte spans unchanged.

This executes the **published Python checker**, not FF12 machine instructions.
Its image and page reads are explicitly supplied from disposable memory and
canonical Git blobs in child processes. No checker source byte was changed.
The path supplied as `__file__` is its original canonical path, so its ordinary
path calculation still requests the existing reference-file location. Only the
two expected image/page reads are permitted. Raw actual stdout, exit status,
input hashes, patch identity, body hashes, dependency blobs and cleanup are
retained. Both children exited, and the original file hash remained unchanged.

The gap is specific: the producer labels the input a certified EXE but does not
verify that identity itself before decoding. A filename is not a hash receipt.
The controlled wrong-identity input passes, so the procedure lacks that guard.
This does **not** show a wrong matrix result: the cited bodies deliberately stay
correct. It does not invalidate the original static alias/staging proof on the
known reference, establish what input a historical run used, or turn the scalar
model into native execution.

Required owner repair: check the exact expected image hash before decode, add a
wrong-identity rejection control, and correct the producer/run procedure and
receipt. Route the fix through OPUS and the existing independent consumer review
`OPUS-REQ-AUDITSEM-REVIEW-MATRIX-ALIAS`; no peer-owned producer/page was edited.
Publication `d1677918b` is real incorporation, while its primary README explicitly
states PENDING REVIEW. The control passing is not independent acceptance.

Run `check.py` to verify the retained controls without repeating them. Inputs and
results are immutable once frozen. No game, PC control, save/config/reference
write or native DLL call was used.

Player version: the matrix result still stands. I found that its verification
script trusted a file's label instead of confirming it was the right game build;
the owner needs to add that check before the result's final review.
