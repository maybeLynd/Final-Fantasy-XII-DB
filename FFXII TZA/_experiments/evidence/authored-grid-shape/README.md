# One authored navigation-grid header changes the conditional constructor shape

The locally extracted `alc0102.mpk` map pack has a 3,200-byte navigation slot 4.
Its grid header is `05 05 0a 0a 3f 00 0d 00 ...`: cell sizes 5×5,
10 columns ×10 rows, and signed origins (63,13). The supplied rectangle is
therefore 50×50. All 100 cell-table entries in this sample point to bounded,
`0xFF`-terminated lists of valid region IDs. The full MPK and slot-4 SHA256 are
in `source.json`; the raw slot is retained in `slot4.bin`. This is one sample,
not a rerun or prevalence statement about FABLE's 461-section census.
The source record also pins the reference executable and exact Python/Capstone
tool identities used to decode it.

Exact shipping instructions in 00384160 (372 bytes) bind the dataset root at
02AEDFB0 and rebase its +0x20 grid reference and the grid's own +8/+0xC
references. The bounded original decoder 0020E600 and encoder 0020E620 are
retained. The prior complete 00383740 getter reads the root's +0x20 grid
reference and obtains signed16 origins and byte sizes/counts from that header;
its exact source hash is pinned. This establishes the source/data layout
connection. It does **not** observe a game session loading this pack.

Applying the prior complete 003924B0 source formula to this positive finite
rectangle gives the following **conditional f32 arithmetic**, using the intended
named sqrtf/floorf semantics:

| description | refined size | cell size | grid | allocation argument |
|---|---:|---:|---:|---:|
| original `floorf(refined)+1.0f` | 3.125 | 4 | 13×13 | 6,289 |
| omit floor, retain +1 | 3.125 | 4.125 | 12×12 | 5,364 |

The initial sqrtf result rounds to about 3.01511335 and gives 16 preliminary
cells along each axis. Testing its nearest two f32 neighbours on each side
leaves both final shapes unchanged, so this example does not depend on an
initial sqrt boundary. The numbers are calculated, **not** results of executing
the imported math DLL, original builder, or allocator. They show an authored
header for which the simplified formula predicts a different grid if that
header reaches the builder. No ordinary caller frequency, initialized pointer,
allocation, budget guarantee, map loading or live effect is claimed. The exact
archive-to-extraction provenance is not independently proven here; the local
copy is identified by its full-file SHA and validated against the original
code's layout and the earlier documented map-pack slot convention.

The first checker mistakenly asserted that the decoder's entry instruction
was `add`; the exact source starts with `mov eax,ecx`, then `add rax,[base]`.
`historical-checker-site-failure/` retains the rejected checker and failure.
No validation existed at that point. The corrected checker asserts both exact
instructions, rereads the image and MPK, validates all 100 lists, and checks
both conditional shapes plus the nearby-float control. `validation.json` is
`PASS_STATIC_AUTHOR_CASE`; new B/native/live runs: zero.

OPUS and FABLE own canonical propagation; independent SPEC review is pending.
PC OFF; image, extraction, game, save and configuration untouched. The complete
L1+L2 goal and final acceptance/audit remain open.

Player version: one area’s map data gives a 50×50 space. Following the game
code’s rounding recipe divides it into 13×13 cells; the simplified recipe
would divide it into 12×12. This explains why the correction can matter to a
real map file, while leaving actual in-game loading to separate evidence.
