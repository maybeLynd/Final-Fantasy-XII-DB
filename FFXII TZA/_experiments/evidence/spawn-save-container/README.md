# Original SAFH container and save-codec boundary

ASTRA, 2026-09-13. [Spawn page section26](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#26-the-safh-save-body-is-compressed-then-encrypted--astra-2026-09-13).

Player version: FF12 compresses its save data and then encrypts it. The small
header number chooses a rotation of a fixed game title before the key is made.
Decoding that wrapper and validating the game state are different operations.

Method A only. Claim/hypotheses: distinguish compression from transformation,
identify header+8 and preserve actual container rejection versus image validation.
Existing V9/V10, earlier scans and zlib library identity were read first. No save
file, live game, provider call or PC-control session was used. No reconstruction.
Ten collected original bodies and two reused from
[storage completion](../spawn-storage-completion/README.md), all against EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000, Capstone5.0.7. Instructions carry their actual bytes and body hashes.

The page records the source recipe: mode0 writer866200 ->87AF40, zlib compressor
level9 ->865AE0, CryptoAPI RC4; reader8666B0 ->865D90 ->865840, matching RC4 setup
->80C5A0/80C5C0, zlib uncompress. Header+8 selects a left rotation of32 fixed
ASCII title bytes, after which byte31 is overwritten with NUL; MD5 hashes31 bytes
and CryptDeriveKey requests128-bit RC4. Both complete helper bodies show the
same setup. Chunk size1000, exact-multiple termination, API failures and cleanup
are retained. Caller capacity checks and full-source consumption are not invented.

Source checks cover full bytes/fresh decoding/local branch targets, import and
order/gate anchors, and four terminated literals. The rotation examples are
source-derived arithmetic, NOT original-code execution or a native roundtrip.
Two guessed UTF-16 extraction lengths omitted terminators and were rejected before
writing an accepted literal receipt. Their sources and failure notes remain;
accepted extraction uses a bounded code-unit scan. No zero-case run is called a
passing experiment. The broad earlier spans are labelled data spans, not string
lengths. LF normalization of recorded scripts is reversible through manifest.json.

Primary API references identify [MD5/RC4 constants](https://learn.microsoft.com/en-us/windows/win32/seccrypto/alg-id),
[the requested key size and derivation](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptderivekey),
and [the acquisition retry flag](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptacquirecontextw).
[zlib1.2.11 uncompr.c](https://github.com/madler/zlib/blob/v1.2.11/uncompr.c)
corroborates the identified decompression wrapper. The compression source URL
could not be retrieved; compressor identity instead uses shipping init parameters,
its named deflateInit_ body, version literal and existing library disposition.
This is not an assertion of a full source/binary equivalence audit.

FABLE/OPUS own V9/V10, middleware wording, types and contract propagation.
Review/consumer agreement remains pending. Native compression/provider/file and
allocation effects, physical save roundtrip, initialized delivery and L12/L13
remain separate. No full mutation campaign or laboratory changes were needed.
Full L1/L2 completion and final reviews remain required.
