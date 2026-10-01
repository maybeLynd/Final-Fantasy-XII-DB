# Effect-context publication: local exception-dispatch boundary

Question: does the shipping exception dispatcher metadata for the call
continuations in `003B3CA0` name a local language cleanup handler that could
restore the previous published effect context on abnormal exit?

H1: the applicable entry or its chain names a handler. H2: the chain ends in
a handler-free root, so this local metadata supplies only stack/register
unwinding and no local language cleanup dispatch. Either result leaves outer
handlers, actual exceptions, initialized state and global restoration by other
code unresolved. Existing original instructions already establish the three
normal-path calls (`0024ED80`, `003A9490`, `0024ED80`); do not repeat them.

Method A: certified shipping PE bytes, existing original call-byte evidence,
and manual decoding of the exception directory entry and chain at each call
continuation. Cross-check with the pinned pefile decoder. This is a claim about
exception-dispatch metadata, admitted by FINAL-AUDIT-PROTOCOL's 2026-09-16
pass-6 ruling; the metadata will not be used to prove normal reachability,
function extents, actor class, lifetime or native effects.

Controls: an actual shipping handler-bearing entry must be detected by both
readers; a private chain redirect to that entry must change the result and
reject the no-local-handler hypothesis. Validate spans, chain bounds/cycles,
version and raw bytes. Do not modify the image. Stop once the local dispatcher
question is settled; no live setup or general exception platform.

Reference EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `0x120000`. OPUS owns canonical effect/ABI contract consumption;
FABLE must review the pass-6 claim boundary if promotion is requested.
