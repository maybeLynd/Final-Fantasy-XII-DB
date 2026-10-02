# Original pre-keyed cache insertion and conditional node-key copy

**Method A, STATIC_ONLY. No FF12 instructions executed/emulated, no live game.
Producer evidence; independent review and canonical consumption pending.**

Question: does insertion derive/mask a pathname key, or receive and preserve a
precomputed numeric key? Which original native operations establish the new
node's key storage? This is an OV33E2 resource/cache prerequisite, not a whole
collision, archive-missing or lifetime verdict.

H1 applies the lookup normalizer's31-bit domain to the insertion entry. H2
separates the full32 pre-keyed insertion interface from the actual caller domain.
Existing normalizer evidence answers neither actual insertion input provenance
nor downstream node-copy effects. Original code suffices for the bounded
interface/copy/field-preservation questions; natural domains remain separate.

For the player: when FF12 registers a resource for later lookup, this entry
receives a numeric key. It does not itself turn a pathname into that key.
Knowing the lookup naming rules therefore does not identify every resource
which could be registered through this interface.

## Reference and raw inputs

EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base120000h. Capture01 preserves1D6A20..1D6A6D,20B680..20B83B and
20B5F0..20B675 (653 original bytes). Its driver is
`17226afad980fa02d38476c1e55a3ced69e67fd0171d59420c60c21f8b1af38c`.

The first source proof was valid at forwarding scope. It left the tree helper
opaque. Instead of promoting that boundary to native effects, additive
capture02 reads full1AE9B0..1AEAFC,1AE850..1AE9A8,20BA70..20BB0C and
16D840..16DA54 (1364 additional bytes). Driver
`6afb9ec3d2538d456df680fdb96372090d18419e6bb10c20ca58346d06231d99`.
Both actual captures are terminal0, with raw stdout/stderr, exact interpreter,
EXE, wrapper, reviewed adapter and decoded annotations retained.

`result-01.json`, original receipts, `prove-key-forwarding-01.py` and
`control-forwarding-01.py` remain immutable historical producer evidence.
`producer-01-disposition.json` records **VALID_SCOPED_SUPERSEDED_ADDITIVELY**,
not invalidation. No old capture was repeated; original instructions were not
executed. Prior accepted prefix/normalizer samples were not repeated.

## Established interface and storage facts

| Boundary | Key and other parameters |
|---|---|
|1D6A20|ECX is precomputed key32, saved EBP then forwarded EDX. Incoming RDX is a distinct pointer carrier; R8D and R9D forward numeric size/value32 and kind32. Getter20C700 supplies the service receiver.|
|20B680|Key in EDX/EBP and saved DWORD entry SP+10h. Seven pushes+SUB40h put it at current SP+88h; entry fifth argument SP+28h becomes current SP+A0h, the numeric kind.|
|Existing-key preparation|Unsigned full-DWORD key comparisons; EDX=EBP passed to20C300. Replacement effects remain a named native boundary.|
|New descriptor/map preparation|20B5F0 receives the exact saved DWORD key address. No own full-width stack write overlaps the key home before this call.|
|20B5F0|Reads full DWORD; unsigned JB/JAE comparisons; insertion preparation copies it to private pair+0, seeds QWORD pair+8=0 and passes the pair to1AE9B0. Returned value slot is node+28h.|

No local hash/prefix processing or31-bit mask is applied to that supplied key
value path. The MOV widths/carriers preserve bit31 as well as all lower bits.
This is a fixed-width invariant, not sampled original-code executions. The
source model key80000000h remains80000000h at the forwarding boundaries; a
31-bit mask would instead yield0. No natural high-bit entry was observed.

All five supplied original new-node copy sites in1AE9B0,1AE850 and20BA70 load
16 bytes from the same pair pointer and store them into node20h..30h. Under a
valid fresh nonwrapping30h node, their pointer+20h guard takes the copy arm.
The first four bytes are the full DWORD key; the payload pointer occupies28h.

Complete16D840 is a leaf with no calls. Every actual w/rw span lies in node/
header links and colour bytes0h..19h. Under valid node/header identities,
disjoint allocations and no alias/interference, balancing leaves20h..30h
unchanged. The caller's descriptor-pointer write through returned slot28h
changes the value pointer, not key20h.

**Conditional key-storage implication:** stable original input-pair contents,
readable private frames, valid fresh disjoint30h allocation/nonwrapping address,
valid ordered pointer-linked nodes/header, normal returns and ABI preservation
establish that these original new-node copies and balancing preserve the
pair's full32 key. This is not an unconditional guarantee across unknown
allocator callbacks or arbitrary malformed state. In particular, pointer
carrier preservation alone does not prove input-memory contents stay stable.

The lookup normalizer's domain therefore cannot, by itself, prove the insertion
entry's caller domain. Actual caller derivation may still restrict every natural
key to31 bits. No collision/archive absence/native cache occupancy conclusion
follows here.

## Producer validity and discriminating controls

Producer01 terminal0:
`867b3a4ea40b0944a79c8d458d3ca0285037500d2471e8e4857cdac57bb5e3f3`.
Final producer02 terminal0:
`8ec0b0d0750ad45a552950cbcd871ba8ea3716d86e20d7ffd036a0f56a5cedcb`.

Final producer verifies both actual capture paths, the archived checked initial
proof, current EXE/raw original bytes, seven full local CFGs, exact ABI/value
operations, register carriers, dominance, full-width private key-home writes,
all five pair-copy alternatives and the complete leaf balancing write spans
before producing `result-02.json`. Memory roles are re-derived through the
shared reviewed adapter. Capstone register metadata is used only for carriers.

Initial controls01 validate forwarding producer01: four actual disposable CLI
refusals, including a coherently changed pair-key source. They are historical
controls for that exact archived driver, not reruns of final producer02.

Final controls02 terminal0, driver
`b26880a1f5a55cdec7a30a3053c21f3bc2086c0d3c6364a1dd1153cc8b5a46a5`.
Five actual final-producer refusals cover failed storage capture, incomplete
storage wrapper, missing storage source, failed archived positive despite exit
metadata elsewhere, and coherent balancing write changed from colour18h to
key20h. Each must terminate nonzero with its exact diagnostic and no result.
Five required status/completion gates precede output on the actual invocation.
These are tool controls, not original FF12 execution or independent acceptance.

In a disposable restored packet in the repository, run the existing analysis
venv's `python -B prove.py fresh-result.json`. Reconstruct control cases using
their hash-bound inherited base files, retained overlays and explicit removals.
Do not execute into published inputs/results. Check actual status and raw
diagnostics; file presence or printed success does not replace the receipt.

## Consumer changes and required open limits

FABLE: separate path-derived lookup-key bounds from insertion's pre-keyed
interface. Consume conditional new-node key copy/header preservation only with
stable input, allocator, valid tree/ABI and normal-return premises. Keep the six
archive-missing candidates, original caller domain, natural requests/collisions,
runtime kindFF paths and eviction/lifetime open.

OPUS: key32 is distinct from data pointer, size/value32 and kind32; map key is
the DWORD at node20h, value pointer at28h. Qualify new-node copy/balance effects;
replacement20C300/20B0F0, locks/getter/allocator callbacks, all-caller semantics,
source-pair stability and actual initialization remain named obligations.

SPEC: independently derive ABI/frame/key carrier and all native copy branches,
verify full-width header spans rather than offset-start tests, reproduce final
producer/controls and inspect the archived forwarding version's narrower scope.
No effect is justified merely by a helper name or stub.

All owned bounded capture/proof/control processes terminal. No PC/game/native
instrumentation/save/config/reference or peer-owned consumer changes. Historical
four runtime-needs eliminations unchanged; no whole OV row closed. Full L1+L2
goal ACTIVE/NOT_MET; K14 closed, EXP127 invalid, parked menu budget spent and
extension unapproved. Publication/review waits block this packet's delivery,
not unrelated science.
