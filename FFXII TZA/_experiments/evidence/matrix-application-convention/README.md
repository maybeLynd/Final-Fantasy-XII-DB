# Specify matrix storage and the vector's side together

The shared original00217060 leaf applies this exact flat-float indexing:

```text
output[j] = X*m[j] + Y*m[4+j] + Z*m[8+j] + W*m[12+j]    j=0..3
```

This is an index formula; each product/add is an original SSE f32 operation, with
Y+X summed first, then Z, then W. It permits **a row vector multiplied on the left
of a row-major matrix**, equivalently **a column-major matrix multiplied on the
left of a column vector**. The leaf cannot establish one universal engine storage
convention by itself. Type, caller and producer representation remain separate.

EXP219 describes this same helper as "out = mat × in" and "row-major float math".
That pairing needs the vector/storage convention stated. Under ordinary row-major
storage and a column-vector `mat * in`, it would give a different result. This is
a functional transpose risk, rather than a new function disposition or type census.

The existing committed GS evidence fcbffd545c30575039e80afc272680d6d71e9a38 already
distinguishes the two. Input(1,2,3,1) and flat matrix:

```text
2  0  0  0
0  3  0  0
0  0  4  0
10 20 30 2
```

give original pre-divide(12,26,42,2), then the GS writer gives(6,13,21,1).
Treating those printed rows as a matrix left-multiplying a column vector instead
gives(2,6,12,142). The existing case's products/sums are exactly representable,
so this discriminator introduces no f64/f32 equivalence claim. The existing finite
cancellation case separately preserves instruction-order sensitivity.

Method A reuses existing method-B evidence; **no new experiment or replay**.
source.json pins original committed source/raw/observation/validation/manifest
blobs and the new EXP219 consumer preimage. check.py validates the actual235B leaf
hash, all16 matrix byte operands, four vector operands, original nonidentity
intermediate output and competing convention. observation.json gives per-component
byte offsets. Prior producer validation and independent acceptance stay distinct.

The first new checker rejected `[rdx + 4]` because it expected textual
`[rdx + 0x4]`. Old checker/failure are retained in historical-checker-format-failure.
No original evidence or prior acceptance changed. The corrected checker compares
decoded register/base/displacement/4B width; its smallest regression binds the
actual rejected shipping instruction. The new qualification passes after that fix.

Limits: supplied matrix/vector and isolated original composition, no original
initialisation, native rendering, all-engine convention, global transpose defect,
type/ownership attribution or new scope for EXP219's remaining native-effect stubs.
ORACLE producer, OPUS existing representation consumer, FABLE if adopting this
shorthand, and independent SPEC receive the finding; propagation remains pending.

Cleanup: read-only committed artifacts/reference; no game/PC/input/attachment or
save/config/reference writes. Live permission/setup budget unchanged. L1+L2 NOT_MET.

Player version: writing a matrix in rows does not by itself say how a point is
multiplied through it. Getting the side wrong moves the point incorrectly. The
existing original-code capture already supplies the example needed to clarify it.
