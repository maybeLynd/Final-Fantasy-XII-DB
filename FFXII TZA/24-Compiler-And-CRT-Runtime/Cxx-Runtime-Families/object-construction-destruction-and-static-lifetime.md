---
system: C++ object construction, destruction and static lifetime — the four runtime families
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain — CompilerGeneratedCpp / CxxObjectLifecycle / CxxStandardLibrary / Microsoft
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 48 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
origin: category 24's four undocumented C++ runtime families, 915 functions with no mechanism document
function_families:
  - "counted-buffer field replace, 98-byte spelling | C | members/counted-buffer-field-replace-98b.tsv | 21 | not this game's code: compiler- or template-generated counted-buffer machinery around the page's documented deallocator. The record is {dword size|own-flag, qword buf} with bit 31 as the ownership flag. PROVED BY FORM - 21 members, all 98 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: each member calls exactly three external targets - a member-specific getter returning {size|flags, buf}, a member-specific allocator, and 00584730 x21 (the page's if(this)_aligned_free wrapper) conditional on the own-flag and a different-pointer test; then commits {size, ptr} into the record. THE BOUNDARY: which getter and allocator vary per member; the idiom does not. NOT dispositioned: the getters, the allocators, and the record type's identity. Selector: members/select_counted_buffer_ops.py"
  - "counted-buffer field replace, 99-byte spelling | C | members/counted-buffer-field-replace-99b.tsv | 20 | not this game's code: compiler- or template-generated - the second spelling of the 98-byte row's idiom (edx-side flag test, cmp rcx,rax). PROVED BY FORM - 20 members, all 99 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: each member calls a member-specific getter, a member-specific or shared allocator (006BC4C0 x16 is shared), and 00584730 x20 under the same own-flag gate; commits {size, ptr}. THE BOUNDARY and NOT-dispositioned are as the 98-byte row. Selector: members/select_counted_buffer_ops.py"
  - "counted-buffer list materialisation, 222-byte form | C | members/counted-buffer-list-materialisation.tsv | 17 | not this game's code: compiler- or template-generated. PROVED BY FORM - 17 members, all 222 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: external targets are exactly {0017D260 x17, 00584730 x17} - count the intrusive list rooted at a member-specific global, allocate count*8 via 0017D260, zero-fill (rep stosq), conditional-free the record's old buffer under the own-flag, commit {count, ptr}, then copy the list links into the array; returns 0 or 0xD. THE BOUNDARY: which global's list varies per member. NOT dispositioned: 0017D260, the record type, and the element type. Selector: members/select_counted_buffer_ops.py"
  - "counted-buffer release-and-clear, 68-byte form | C | members/counted-buffer-release-and-clear.tsv | 12 | not this game's code: compiler- or template-generated. PROVED BY FORM - 12 members, all 68 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: the only external target is 00584730 x12 - if the record's own-flag is clear, free the buffer; either way zero the {size, ptr} fields. THE BOUNDARY: the record type is shared machinery; nothing varies but the call target (which does not vary). NOT dispositioned: the record type's identity. Selector: members/select_counted_buffer_ops.py"
  - "ref-flag handle store with release, 109-byte form | C | members/refflag-handle-store-with-release.tsv | 15 | not this game's code: compiler- or template-generated handle machinery over the page's ref-flag record {dword size|own-flag, qword ptr}. PROVED BY FORM - 15 members, all 109 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: reject a bit31-set r8d with return 5; if the record's stored ptr differs from rdx and the own-flag is clear, btr the flag and call a member-specific release on the old ptr; commit {size=r8|bit31, ptr=rdx}; return 0. CONTROL: exactly one external call per member - the member-specific release (15 distinct). NOT dispositioned: the release implementations and the record type's identity. Selector: members/select_refflag_and_container_ops.py"
  - "ref-flag handle reset, 69-byte form | C | members/refflag-handle-reset.tsv | 13 | not this game's code: compiler- or template-generated - the reset sibling of the store row above, over the same {size|own-flag, ptr} record. PROVED BY FORM - 13 members, all 69 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: if the own-flag is clear, btr it and call a member-specific release on the stored ptr; either way zero the record's {size, ptr} fields. CONTROL: exactly one external call per member - the member-specific release (10 distinct; 005B7EF0 x3, 005B7E80 x2 subset-shared). NOT dispositioned: the release implementations and the record type's identity. Selector: members/select_refflag_and_container_ops.py"
  - "intrusive virtual node-dispose loop, 93-byte form | C | members/intrusive-virtual-node-dispose-loop.tsv | 12 | not this game's code: compiler- or template-generated - the virtual-dispatch sibling of the intrusive-list teardown loops. PROVED BY FORM - 12 members, all 93 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: walk the intrusive circular list rooted at [rcx], calling the node-dispose virtual [rdi+0x10] vtable slot +0x18 on (node, 0x18) on each node until back at the head. CONTROL: no direct external targets - the disposer is reached indirectly through the member vtable slot. NOT dispositioned: the node type, its vtable, and the disposer implementation. Selector: members/select_refflag_and_container_ops.py"
  - "malloc record emplace adapters, 144-byte form | C | members/malloc-record-emplace-adapters.tsv | 14 | not this game's code: compiler- or template-generated container machinery. PROVED BY FORM - 14 members, all 144 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: malloc(0x18) via 0085E730, optional member-specific record init, push the record into the caller's capacity-bounded container (in-place when spare capacity, else growth via shared 001AB570), then fetch via shared 0018B4E0 and tail-jump shared 0018AFF0 with the result and the record. CONTROL: 0085E730 x14, 001AB570 x14, 0018B4E0 x14, 0018AFF0 x14 shared, plus ONE member-specific init call each (14 distinct). NOT dispositioned: the four shared implementations and the member init calls - this row disposes of the adapter, not the adapted. Selector: members/select_refflag_and_container_ops.py"
  - "ref-flag inverted-bit aligned-free reset, 43-byte form | C | members/refflag-invertedbit-alignedfree-returntrue.tsv | 6 | not this game's code: compiler- or template-generated - the aligned-free sibling of the ref-flag rows above: same guarded-free-and-clear operation, but the release is the shared aligned-free wrapper 00584730 rather than a member-specific release. PROVED BY FORM - 6 members, all 43 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: load [rdx+0x30]; if the record's flag bit (inverted-test on the stored dword) selects the free, call 00584730 on the record pointer; zero the {+0x18, +0x30} fields; return 1. CONTROL: exactly one external call per member - shared 00584730 x6. NOT dispositioned: the shared free wrapper and the record type's identity. Selector: members/select_refflag_alignedfree_siblings.py"
  - "ref-flag dword-flag aligned-free reset, 61-byte form | C | members/refflag-dwordflag-alignedfree-reset-returntrue.tsv | 7 | not this game's code: compiler- or template-generated - the second aligned-free sibling spelling, reading the flag from [rdx] (shr eax,0x12, inverted bit) rather than [rdx+0x30]. PROVED BY FORM - 7 members, all 61 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: if the flag selects the free and the stored ptr is non-null, call 00584730 on it; zero {ptr, size} and the flag dword; return 1. CONTROL: exactly one external call per member - shared 00584730 x7. NOT dispositioned: the shared free wrapper and the record type's identity. Selector: members/select_refflag_alignedfree_siblings.py"
  - "ref-flag aligned-free init adapters, 98-byte form | C | members/nativeadapter-refflagsiblingalignedfreeinit.tsv | 5 | not this game's code: compiler- or template-generated - the longest aligned-free sibling spelling: the ref-flag release plus member init and finalise calls around it. PROVED BY FORM - 5 members, all 98 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton: call two member ops on arg1; if ref flag bit31 is set and the masked count is > 1, call shared 00584730 on [rbx+0x40] and zero {ptr, size}; call a member op on this; return 1. CONTROL: 00584730 x5 shared, plus member-specific ops (14 target-instances, distinct per member). NOT dispositioned: the shared free wrapper, the member-specific ops, and the record type's identity. Selector: members/select_teardown_form_clusters_3.py"
  - "counted aligned-free loop plus self-free, 104-byte form | C | members/nativeadapter-countedalignedfreeloopself.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 104 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if this null return; counted loop over edx elements at [this+8] stride  0x10: free each ref-flagged pointer via shared aligned-free 00584730;  then free this itself via 00584730. CONTROL: 1 external target(s): 1 shared across all 4 members (00584730). NOT dispositioned: the shared implementation(s) 00584730. Selector: members/select_teardown_form_clusters_4.py"
  - "ref-flag aligned-free clear-fields, 58-byte form | C | members/nativeadapter-refflagalignedfreeclear.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 58 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if [this] bit31 is clear, free [this+X] via shared 00584730; zero the  pointer/size fields. CONTROL: 1 external target(s): 1 shared across all 4 members (00584730). NOT dispositioned: the shared implementation(s) 00584730. Selector: members/select_teardown_form_clusters_4.py"
  - "ref-flag bounded element op, 164-byte form | C | members/nativeadapter-refflagsiblingboundedlookup.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 164 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: ref-flag counted element op: bound arg2 against [this]&~bit31, pick the  inline-vs-heap element pointer, call a member lookup; on failure either  return 0xD or free the range via shared 00584730 + member fixup. CONTROL: 5 external target(s): 1 shared across all 4 members (00584730), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00584730. Selector: members/select_teardown_form_clusters_4.py"
  - "ref-flag bounded element op (second spelling), 135-byte form | C | members/nativeadapter-refflagsiblingboundedlookup2.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 135 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: ref-flag counted element op, second spelling: min(arg2,[this]&~bit31);  call a member lookup on [this+8]; on failure return 0xD else shrink the  range and free the tail via shared 00584730. CONTROL: 5 external target(s): 1 shared across all 4 members (00584730), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00584730. Selector: members/select_teardown_form_clusters_4.py"
  - "dynamic-offset ref-flag bounded op, 114-byte form | C | members/nativeadapter-dynamicoffsetrefflagbounded.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 114 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: compute an element pointer at arg1+([this+0x18]+([this+0x48]-[[rax]+0xF4])  scaled); bound arg3 against its ref-flag count; call a member lookup; on  failure return 0xD else call a member op with (elem,result,arg3). CONTROL: 8 external target(s): 8 member-specific or subset-shared. NOT dispositioned: the member-specific targets. Selector: members/select_teardown_form_clusters_4.py"
  - "ref-flag counted 72-stride accessor, 58-byte form | C | members/nativeleaf-refflag72strideaccessor.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 58 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if [this+0x20]&~bit31 > 1 index the heap array at [this+0x28] else the  inline buffer this+0x28; return &elem[arg2] at 72-byte stride +4. CONTROL: 0 external target(s). NOT dispositioned: nothing beyond the members themselves. Selector: members/select_teardown_form_clusters_4.py"
  - "ref-flag counted 40-stride accessor, 67-byte form | C | members/nativeleaf-refflag40strideaccessor.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 67 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if arg2 >= [this+0x18]&~bit31 return 0; index heap [this+0x20] or inline  this+0x20 at 40-byte stride; return [elem+8]. CONTROL: 0 external target(s). NOT dispositioned: nothing beyond the members themselves. Selector: members/select_teardown_form_clusters_4.py"
  - "intrusive-list walk with per-node vcall slot 3, 115-byte form | C | members/nativeleaf-listwalkvcallslot3.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 115 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: walk the intrusive list at [this+0x18]; per node call a member op with  (this,[node]) then vcall [this+0x30] slot 3 with r8=0x58. CONTROL: 3 external target(s): 3 member-specific or subset-shared. NOT dispositioned: the member-specific targets. Selector: members/select_teardown_form_clusters_4.py"
  - "flagged teardown chain, 73-byte form | C | members/nativeadapter-flaggedteardownchain.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 73 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if [this+0xB8]!=0 call shared 005CD6D0 on this+0x90; then call a member  teardown on +0x58 and +0x20; tail-dispatch to a member finisher. CONTROL: 9 external target(s): 1 shared across all 4 members (005CD6D0), 8 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 005CD6D0. Selector: members/select_teardown_form_clusters_4.py"
  - "container pop-front, 161-byte form | C | members/nativeadapter-containerpopfront.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 161 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if [this+0x48] nonzero: take head [this+0x30]->+0x20, dec the count, call  shared 0016D6D0 + 0016DA60 on the node, vcall [this+0x50] slot 3 with  r8=0x28, then shared 00199DB0 on this+0x58; optionally call a member op. CONTROL: 7 external target(s): 3 shared across all 4 members (0016D6D0, 0016DA60, 00199DB0), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 0016D6D0/0016DA60/00199DB0. Selector: members/select_teardown_form_clusters_4.py"
  - "counted record-insert loop, 146-byte form | C | members/nativeadapter-countedemberloop.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 146 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if [this+0x90]==0 and arg1 nonzero: call a member op then loop arg1 times  calling shared 00199DB0 on this+0x20 with a stack record, stepping the  record source by 0xA. CONTROL: 5 external target(s): 1 shared across all 4 members (00199DB0), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00199DB0. Selector: members/select_teardown_form_clusters_4.py"
  - "bump-allocator pop leaf, 17-byte form | C | members/nativeleaf-bumpallocpop.tsv | 2 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 17 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: rax=[this+0x10]; store to [this+0x30]; advance [this+0x10] by 0x10;  return. CONTROL: 0 external target(s). NOT dispositioned: nothing beyond the members themselves. Selector: members/select_teardown_form_clusters_4.py 2 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-running members/select_teardown_form_clusters_4.py gives this list exactly."
  - "multi-record vtable-install initialiser, 387-byte form | C | members/nativeadapter-multirecordvtableinit.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 387 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: zero three qwords of the out record; install member vtables via shared  ctor stub 001EDF00 on this+0x18 and a stack record; zero-init the  this+0x20 sub-record; then run the longer init pipeline via shared  00199DB0/005CC8A0/005CD0A0. CONTROL: 8 external target(s): 4 shared across all 4 members (00199DB0, 001EDF00, 005CC8A0, 005CD0A0), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00199DB0/001EDF00/005CC8A0/005CD0A0. Selector: members/select_teardown_form_clusters_4.py"
  - "lazy singleton alloc-and-init, 66-byte form | C | members/nativeadapter-lazysingletonallocinit.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 66 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if the member rip global is null: allocate a member-sized record via  shared 00210EC0, init it via a member op, store it to the global. CONTROL: 5 external target(s): 1 shared across all 4 members (00210EC0), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00210EC0. Selector: members/select_teardown_form_clusters_4.py"
  - "bounded range copy-and-compare, 404-byte form | C | members/nativeadapter-boundedrangecopycompare.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 404 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: bounded copy/compare over the [r8] range into [rcx+8]-anchored storage: per window call member ops and shared 0016D720/0016D840/001A3100 with shared 00861ED2 (memcmp) verification; 404B five-call pipeline. CONTROL: 8 external target(s): 4 shared across all 4 members (0016D720, 0016D840, 001A3100, 00861ED2), 4 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 0016D720/0016D840/001A3100/00861ED2. Selector: members/select_teardown_form_clusters_4.py"
  - "ref-flag aligned-free release-this, 60-byte form | C | members/nativeadapter-refflagsiblingalignedfreereleasethis.tsv | 5 | not this game's code: compiler- or template-generated - the this-pointer spelling of the aligned-free sibling (the earlier rows read the record through rdx). PROVED BY FORM - 5 members, all 60 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton: if this->+8 ref flag bit31 is set and [this+0x10] non-null, call shared 00584730 on it; zero {ptr, flag} fields. CONTROL: exactly one external call per member - shared 00584730 x5. NOT dispositioned: the shared free wrapper and the record type's identity. Selector: members/select_teardown_form_clusters_3.py"
  - "ref-flag aligned-free release tail-call, 93-byte form | C | members/nativeadapter-refflagsiblingalignedfreetail.tsv | 5 | not this game's code: compiler- or template-generated - the teardown sibling that ends in a member finisher instead of returning. PROVED BY FORM - 5 members, all 93 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton: call a member teardown on this; call a second member op; if the ref flag releases, call shared 00584730 on [rbx+0x20], zero the fields, and tail-call a member finisher on this. CONTROL: 00584730 x5 shared, plus member-specific ops (14 target-instances). NOT dispositioned: the shared free wrapper and the member-specific ops. Selector: members/select_teardown_form_clusters_3.py"
  - "vector destroy-and-deallocate loops, 149-byte form | C | members/nativeleaf-vectordestroydeallocloop.tsv | 5 | not this game's code: compiler- or template-generated - the std::vector _Destroy + _Deallocate sequence for a 0x18-byte element type. PROVED BY FORM - 5 members, all 149 bytes, 3 byte image(s) collapsing to ONE instruction-form skeleton: iterate [begin,end) calling vcall slot 0 (the element destructor) per 0x18B element, then release the buffer through allocator vcall [r9+0x18] with the byte size computed by the /24 magic multiply (movabs 0x2AAAAAAAAAAAAAAB). CONTROL: no direct external targets - both calls are indirect vtable dispatches. NOT dispositioned: the element destructor, the allocator, and the vector type's identity. Selector: members/select_teardown_form_clusters_3.py"
  - "vector buffer-release adapters, 86-byte form | C | members/nativeleaf-vectorbufferrelease.tsv | 5 | not this game's code: compiler- or template-generated - the deallocate-only sibling of the 149 B loop (elements already destroyed). PROVED BY FORM - 5 members, all 86 bytes, 3 byte image(s) collapsing to ONE instruction-form skeleton: compute the element count via the /24 magic multiply and release the buffer through allocator vcall [r9+0x18]. CONTROL: no direct external targets - the release is an indirect vtable dispatch. NOT dispositioned: the allocator and the vector type's identity. Selector: members/select_teardown_form_clusters_3.py"
---

# C++ object construction, destruction and static lifetime

> Four CodeDomain labels — `CompilerGeneratedCpp` 417, `CxxObjectLifecycle` 226,
> `CxxStandardLibrary` 167, `Microsoft` 106 — cover **916 functions** *(corrected 2026-09-14:
> R109 added one `CxxObjectLifecycle` member at GN161; the other three labels are unchanged)* and had no mechanism document
> between them. This is what they actually do, and whether the labels were earned or applied by shape.

**Earned.** Seven mechanisms were re-derived from the image and every one scores **100 %** against
its own label. One label's *name* is not supported by any evidence and is called out.

## 1. What the player sees

Nothing, until it goes wrong — and then everything at once.

When you load a save, FFXII rebuilds a world: every character, every piece of equipment, every sound
bank, every texture handle. When you leave a zone it takes that world apart again. The code in this
document is the machinery that does the building and the taking-apart — not the game logic that
decides *what* to build, but the plumbing that actually calls the constructor, installs the object's
behaviour table, and later frees the memory.

It runs at three different times, and the difference matters to anyone injecting code:

- **Before the title screen.** 1,172 objects are constructed before `main` even starts.
- **The first time something is asked for.** Another 1,681 are built lazily, on first use — which is
  why the first cast of a spell in a session can hitch slightly and the second never does.
- **Whenever an object dies.** Every C++ object in the game is destroyed through one of 226 small
  functions that take a hidden flag saying "and free the memory too".

If any of it is disturbed, the symptom is not a graphical glitch. It is a crash on a loading screen,
or a hang with no error at all.

## 2. Native mechanism

### 2.1 The deleting destructor — 226 functions, one idiom, two spellings

MSVC gives every class with a virtual destructor a hidden extra method: the **scalar deleting
destructor**, which occupies slot 0 of the vtable. It receives the object in `rcx` and a **flag in
`edx`** whose bit 0 means *"and free the storage"*. This is the single most common shape in the four
families.

**Spelling A — the destructor's work is inlined**, so the flag can be tested where it arrives:

```asm
001D70A0  push  rbx
001D70A6  lea   rax, [rip + 0x7292C3]     ; -> 00900370, the vtable
001D70AD  mov   rbx, rcx                  ; save this
001D70B0  mov   qword ptr [rcx], rax      ; install the vtable
001D70B3  test  dl, 1                     ; <-- the flag, still in edx
001D70B6  je    0x1D70C2
001D70B8  mov   edx, 0x90                 ; the object's size
001D70BD  call  0x809950                  ;     free(this, 0x90)
001D70C2  mov   rax, rbx                  ; return this
001D70CA  ret
```

**Spelling B — the destructor calls an inner destructor first.** That call clobbers `rdx`, so the
compiler must move the flag to a callee-saved register before making it:

```asm
00195530  mov   qword ptr [rsp+8], rbx
0019553A  mov   ebx, edx                  ; <-- the flag moves to ebx
0019553C  mov   rdi, rcx
0019553F  call  0x195180                  ;     the real destructor
00195544  test  bl, 1                     ; <-- tested there instead
00195547  je    0x195556
00195549  mov   edx, 0x98
0019554E  mov   rcx, rdi
00195551  call  0x809950
00195556  mov   rax, rdi
00195563  ret
```

**Both spellings are the same mechanism**, and the difference is forced by the calling convention,
not chosen. All **226** functions carrying a deleting-destructor label perform the flag test —
**226 of 226**. The sub-labels then record *which deallocator* is used, and that distinction is real:

| sub-label | n | deallocator |
|---|---:|---|
| `CompilerGeneratedCpp.ScalarDeletingDestructor` | 88 | `00809950` (`free`) directly |
| `CxxObjectLifecycle.ScalarDeletingDestructor.Free` | 63 | inner destructor, then `00809950` |
| `CxxObjectLifecycle.DeletingDestructor.AlignedOrGuardedFree` | 53 | an aligned/guarded path, not `free` |
| `CxxObjectLifecycle.ScalarDeletingDestructor.VtableFree` | 9 | vtable install, then `free` |
| `CxxObjectLifecycle.DeletingDestructor.VtableAlignedOrGuardedFree` | 10 | vtable install, aligned path |
| `Microsoft.MSVCCRT_STL_Runtime.StreamDeletingDestructor` | 3 | a stream object's |

The 63 `AlignedOrGuardedFree` members were the group that looked wrong until their bodies were read:
they all do the flag test, they simply reach the deallocator through a different route.

### 2.1a A second flag bit chooses the deallocator — and it covers 1,608 functions

Some destructors test **bit 2** as well, and the two sides call different things:

```asm
0018581C  test  dl, 1                     ; free at all?
0018581F  je    0x185839                  ;   no -> just return this
00185821  test  dl, 4                     ; which deallocator?
00185824  jne   0x18582E
00185826  call  0x584730                  ; bit 2 CLEAR -> if (this) _aligned_free(this)
0018582C  jmp   0x185839
0018582E  mov   edx, 0xD8                 ; bit 2 SET   -> operator delete(this, 0xD8)
00185833  call  0x16D6A0
00185839  mov   rax, rbx                  ; return this
```

`00584730` is `if (this) _aligned_free(this)` — a null check in front of the imported
`_aligned_free` at `0019C570`. So **bit 2 selects the sized `operator delete` over `_aligned_free`**,
which is precisely what the GFZ's own label `DeletingDestructor.AlignedOrGuardedFree` says.

**The population is 1,608 functions, and the label is on 63 of them.** The other 1,545 are labelled
elsewhere — **1,410 Phyre**, 94 Audio, 33 Input — because they are owner- or middleware-tagged, not
because the mechanism differs. Measured across all 1,606 with a resolvable branch, the split is
absolute:

| side | first call | n |
|---|---|---:|
| bit 2 **set** | `0016D6A0` | **1,606 of 1,606** |
| bit 2 **clear** | `00584730` (→ `_aligned_free`) 1,494 · `007AD450` 93 · `0085E710` 19 | 1,606 |

> **On the bit-2 path this destructor frees nothing.** `0016D6A0` is the three-byte `ret 0` that
> `/OPT:ICF` folded roughly 273 `ret`-bodied functions onto — the disabled CFG check stub is one of
> them, and the sized `operator delete` this site calls is another. **The address has no single
> identity**, and reading it as `_guard_check_icall` here would be wrong: the call passes
> `rcx = this, edx = size`. Whatever the sized delete was meant to be, in the shipped binary it
> returns immediately. Only the `_aligned_free` side actually releases memory.

### 2.2 Objects built before the game starts — 101 functions, and a registration proves it

MSVC registers dynamic initializers in a table the CRT walks before `main`. That table is a
**registration, not a shape**, so it settles the label without argument. It lives at
`0x008C31D8`–`0x008C5678` and holds **1,172 non-null entries, every one of which is a known function
entry**.

| label | n | in the registration table |
|---|---:|---:|
| `CompilerGeneratedCpp.StaticObjectInitializer` | 90 | **90 (100 %)** |
| `CompilerGeneratedCpp.StaticZeroInitObjectInitializer` | 11 | **11 (100 %)** |

`StaticZeroInit` is the variant whose object is zero-filled rather than value-constructed.

**The other 1,071 registered initializers carry different labels**, mostly Phyre and game code, and
that is correct: being *registered* makes a function an initializer, but the four families claim only
the ones the compiler generated wholesale.

### 2.3 Objects built on first use — 140 functions, a different mechanism entirely

The lazily-constructed statics do **not** appear in that table, because their whole point is to be
built later. They are recognised by the guard call instead:

| label | n | calls `_Init_thread_header` (`008092FC`) | in the CRT table |
|---|---:|---:|---:|
| `CompilerGeneratedCpp.ThreadSafeStaticRecordAccessor` | 117 | **117 (100 %)** | 0 |
| `CompilerGeneratedCpp.ThreadSafeStaticObjectInitializer` | 23 | **23 (100 %)** | 0 |
| `CompilerGeneratedCpp.GuardedStaticObjectTeardown` + `StaticContainerTeardown.*` | 88 | **0** | 0 |

**Perfect separation in both directions.** The eager labels are 100 % registered and 0 % guarded; the
lazy labels are 100 % guarded and 0 % registered; and the teardown labels are neither, which is right
— tearing an object down does not take the construction guard.

An accessor is the little function that stands in front of a lazy static: median body **115 bytes**,
always the same shape — take the guard, construct if you won this race, return the address. There are
**117** of them, and the [lazy-statics document](../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md)
describes what happens when one is interrupted.

### 2.4 Installing an object's behaviour table — 85 functions

`CxxObjectLifecycle.VtableInstall*` and `DerivedConstructorVtableInstall` name the constructor
fragment that writes a vtable pointer into an object. The mechanical signature is a `lea` of a
`.rdata` address followed by a store of that register into the object:

```asm
lea  rax, [rip + <disp>]        ; the vtable, in .rdata
mov  qword ptr [rcx], rax       ; or [rcx + n] for a base subobject
```

| label | n | does the RIP-`lea` → object store |
|---|---:|---:|
| `CxxObjectLifecycle.VtableInstallStub` / `VtableInstallTailCall` | 60 | **60 (100 %)** |
| `CxxObjectLifecycle.DerivedConstructorVtableInstall` | 25 | **25 (100 %)** |

The `+n` form is a base-class subobject getting its own vtable during construction of a derived
class — which is why a *derived* constructor label exists separately.

### 2.5 The Microsoft family

106 functions, of which **49 carry recovered symbol names** — `sprintf`, `underflow`, `_Reset_back`,
`_Set_back`, and eight copies of `scheduler_resource_allocation_error`. That last group is the
**Concurrency Runtime**, which ships in the binary whether or not the game uses it. The names are
tier-3 evidence and are the strongest thing in this family; the remaining 57 carry only the label.

## 3. Key addresses

| Address | Working name | Role |
|---|---|---|
| `0x008C31D8`–`0x008C5678` | CRT dynamic-initializer table | 1,172 entries, all real function entries |
| `008092FC` | `_Init_thread_header` | claims a lazy static's guard; 707 callers image-wide |
| `0080929C` | `_Init_thread_footer` | publishes it |
| `00809950` | `free` (thunk → `00210EB0`) | the sized deallocator every spelling-A destructor calls |
| `0016D6A0` | the ICF-folded `ret 0` stub | on the "guarded free" path of all 63 `AlignedOrGuardedFree` destructors. **Not specifically `_guard_check_icall`** — see the note below |
| `001D70A0` | a spelling-A deleting destructor | 43 B — the whole idiom in one screen |
| `00195530` | a spelling-B deleting destructor | 52 B — flag saved in `ebx` across the inner call |
| `00185800` | a two-deallocator deleting destructor | 66 B — `Phyre.SceneCamera`; tests `dl,1` then `dl,4` |
| `00584730` | `if (this) _aligned_free(this)` | 10 B — the bit-2-clear deallocator for 1,494 of them |
| `0019C570` | `_aligned_free` | imported thunk |

Addresses are Ghidra image base `0x00120000`.

## 4. Data structures and formulas

**The deleting destructor's contract**, which is what a modder hooking one has to honour:

```c
void *X::`scalar deleting destructor'(X *this /*rcx*/, unsigned int flags /*edx*/)
{
    /* ... run the destructor body, possibly by calling an inner dtor ... */
    if (flags & 1)                       /* test dl,1  /  test bl,1 after mov ebx,edx */
        free(this, sizeof(X));           /* edx = size, rcx = this */
    return this;                         /* mov rax, this */
}
```

The size passed in `edx` is a **compile-time constant per class** (`0x90`, `0x98`, `0xD8` in the
examples above), so a deleting destructor also tells you the exact size of its object.

**The vector form** adds bit 2:

```c
if (flags & 1) {
    if (flags & 4)  free(base, size);          /* array: free the whole block  */   // <- corrected 2026-10-02, OPUS - wrong: bit 2 set calls 0016D6A0 (ret 0) with the size and frees nothing, bit 2 clear calls 00584730 (_aligned_free); 00185800+0x33 and 00185800+0x26, and BQ-26's answer
    else            destroy_and_free_each();   /* scalar path                  */
}
```

**Walking the eager initializers by hand:**

```c
for (u64 *e = (u64 *)0x008C31D8; e < (u64 *)0x008C5678; e++)
    if (*e) ((void (*)(void))*e)();      /* 1,172 non-null entries */
```

## 5. Call chain

```
CRT startup
  -> walk 0x008C31D8 .. 0x008C5678         1,172 registered initializers
     -> StaticObjectInitializer (90) / StaticZeroInit (11)
        -> the object's constructor
           -> VtableInstall* (85)          writes the vtable pointer

first use of a lazy static
  -> ThreadSafeStaticRecordAccessor (117)
     -> _Init_thread_header  008092FC      take the guard
        -> ThreadSafeStaticObjectInitializer (23)
     -> _Init_thread_footer  0080929C      publish

object death, from anywhere in the engine
  -> vtable slot 0 = the deleting destructor (226)
     -> inner destructor (spelling B only)
     -> free 00809950  or the aligned/guarded path via 0016D6A0   <- corrected 2026-10-02, OPUS - 0016D6A0 is ret 0 and frees nothing; the freeing paths are 00809950 (free) and 00584730 (_aligned_free)
```

**Upstream:** everything. These are called from every subsystem, which is exactly why they carry a
`CodeDomain` and not an owner.

**Do not confuse with:**

- [`../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md)
  — the 3,895 `CompilerGeneratedEH` funclets are a *fifth* family and a different mechanism: they run
  during unwinding, not during construction or destruction.
- [`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
  — describes *when* the 1,172 run. This describes *what the individual entries are*.
- A destructor that is **owner-tagged rather than CodeDomain-tagged.** 178 functions perform the
  deleting-destructor idiom and carry a `PrimaryOwner` instead — 99 Audio, 42 Phyre, 17
  `NativeRoutine`, 8 Input. That is the layer separation working, not a gap: a destructor for an
  Audio object is Audio-owned, and its *shape* being compiler-generated does not change that.

## 6. Modding notes

- **Never hook a deleting destructor without preserving `edx`.** Bit 0 decides whether the memory is
  freed. Clear it and you leak the object; set it when the caller did not and you free memory the
  caller still holds.
- **A deleting destructor tells you `sizeof`.** The `mov edx, imm` immediately before the free call is
  the class's exact size — often the fastest way to size a structure you are reversing.
- **Two spellings, one meaning.** If the flag is not in `dl` when you look, find the `mov <reg>, edx`
  near the top; the test is on that register.
- **The "guarded free" path goes through `0016D6A0`, which is a `ret 0` in the shipped game**, so
  that indirection costs nothing and can be hooked freely. **Do not read the address as
  `_guard_check_icall`** — the CFG stub is only one of roughly 273 `ret`-bodied functions `/OPT:ICF`
  folded onto those three bytes, and here the call is passing `rcx = this, edx = size`, which is a
  deallocator signature, not a CFG check. The GFZ's name for the address privileges one of its 273
  identities; this document uses the neutral one, agreeing with
  [the audio boundary document](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md).
- **Inject after `main`.** 1,172 initializers must have run; the table at `0x008C31D8` is walkable if
  you want to know exactly which.
- **The 117 accessors are the safest read-only probes in the binary.** Each returns the address of one
  lazy static and has no side effect after the first call.
- **XIIOnline:** none of this is replicable state. It is object plumbing; what matters across clients
  is what the objects *hold*, and that belongs to whichever subsystem owns them.

## 7. What is not known

- [x] ~~**`CxxStandardLibrary.NativeQualified` (52) is not supported by its own name.** "Qualified"
      implies a recovered qualified symbol, and **all 52 have `name_source: DEFAULT`** — no symbol at
      all. Whatever those functions are, the label's justification is not visible in the snapshot.~~
      **BQ-22 ANSWERED 2026-09-22 (FABLE): both halves reproduce — 52 rows selected, 52 placeholder
      names — and the label is not merely unsupported but WRONG for at least two members.
      `001A2130` is a game manager/object constructor with its own vtables `008F6500`/`008F6600`,
      and `00200BF0` sits in the authored-parameter read chain; both call PhyreEngine's resource
      layer, which standard-library code does not. **The other 50 are untested individually and
      this does not classify them.** See the section in §6 above. **BQ-22.**
- [x] The remaining `CxxStandardLibrary` sub-labels — `ContainerAllocatorSupport` 40,
      `StdRegex.Runtime` 21, `OrderedContainerRuntime.*` 19, `StringHeapAlgorithms` 6 — were not
      tested. Each names a specific std mechanism and each is checkable against upstream MSVC STL
      source, which is tier 6. **BQ-23.**
      *Narrowed 2026-09-22 (FABLE): a cheaper test that COULD have falsified them does not, and it
      is the same test that condemned `NativeQualified`.* Upstream comparison is still what would
      confirm these labels; it is not what would refute one. **A `std` body does not call the
      game's own owned subsystems**, so any member that does is mislabelled whatever an upstream
      diff would say — and that is exactly how `BQ-22`'s two counter-examples were found.

      | label | members | members calling a game-owned body |
      |---|--:|--:|
      | `CxxStandardLibrary.NativeQualified` *(control)* | 52 | **2** — `001A2130`, `00200BF0` |
      | `ContainerAllocatorSupport` | 40 | **0** |
      | `StdRegex.Runtime` | 21 | **0** |
      | `OrderedContainerRuntime.*` | **30** | **0** |
      | `StringHeapAlgorithms` | 6 | **0** |

      **The control is what makes the zeros mean anything**: the same pass, on the same tables,
      returns `NativeQualified`'s two known offenders, so a zero is the label's property and not
      the test's blindness. **But passing a falsification test is not confirmation** — these four
      are consistent with being standard-library code and remain unconfirmed as such, which is why
      ~~this row stays open and tier 6 stays the decider~~ *(answered: see the BQ-23 answer below, 2026-09-27, at tier 6; 2026-10-02, OPUS)*.

      > **One figure to reconcile, flagged rather than adopted.** This row records
      > `OrderedContainerRuntime.*` at **19**; the current `graph/functions.tsv` gives **30**,
      > spread over fifteen distinct sub-labels (`UniqueInsert` 10, `HintAwareUniqueInsert` 6, the
      > bare label 2, and twelve singletons — `TreeDestroy*`, `TreeClone*`, `RedBlackTree*`,
      > `CompositeKeyUniqueInsert`, `StringKeyFindOrDefaultInsert`, `RootListTreeDestroy`). **The
      > other three counts match exactly (40, 21, 6), so this is not a parsing difference.** It is
      > the kind of drift `AC-6` exists for, and belongs to whoever re-runs that census rather
      > than being silently overwritten here.
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): compared at tier 6, and no member is left unmatched.** Against upstream MSVC STL (the VS2015 v140 headers, installed for this) and EASTL: `StringHeapAlgorithms` 6 and 31 of `ContainerAllocatorSupport` carry MSVC markers (2026-09-27 first pass); 18 `OrderedContainerRuntime` members are EASTL rbtree code and 3 MSVC `_Tree`; the 9 left over are 7 more EASTL subtree routines and 2 Phyre packed-colour tree functions ([`bq23-tier6-b/`](../../_index/candidates/bq23-tier6-b/README.md)); 6 allocator members are VS2015 `_Tree::_Buynode0` / `_List::_Buynode0` ([`bq23-tier6-c/`](../../_index/candidates/bq23-tier6-c/README.md)); and the 24 regex-span members are VS2015 `<regex>` - `_Parser`, `_Matcher` and `_Builder` members plus five generic functions regex pulls in - 24 of 24 at high confidence with a clean confusion matrix and negative sample ([`bq23-tier6-d/`](../../_index/candidates/bq23-tier6-d/README.md)). The labels that name the wrong library or family are corrected by SWE2-EC7, the label owner.*
- [x] The 57 `Microsoft` functions with no recovered symbol. **BQ-24.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md. See the register row.*
- [x] ~~`CxxObjectLifecycle.ConditionalTeardownReturnTrue` (28) and
      `CompilerGeneratedCpp.StaticContainerTeardown.IndirectAllocator` (60) — 88 teardown functions,
      confirmed only negatively (they do not take the construction guard).~~ **BQ-25 ANSWERED 2026-09-19 (OPUS)** - the 60 are `atexit`-registered static-container teardowns freeing through the allocator vtable slot `+0x18`; the 28 are a virtual method in a shared vtable layout, not a CRT teardown. See the section at the end of this page.
- [x] ~~The **vector** deleting destructor form (`flags & 4`) has no label in any of the four
      families.~~ **ANSWERED 2026-09-02, and the question's framing was wrong** — it is **not** the
      vector form. Only **14 of 1,608** members contain any backward branch, and a vector deleting
      destructor must iterate over the array. Bit 2 selects the **deallocator**, exactly as the
      `AlignedOrGuardedFree` label says. The population is **1,608**, of which 63 carry that label and
      1,545 are owner- or Phyre-tagged. §11. **BQ-26.**
- [x] Why the sized `operator delete` path resolves to a `ret 0`. On the bit-2 branch **nothing is
      freed**, and 1,606 functions take that branch under some flag value. Either those objects are
      never deleted with bit 2 set, or the engine leaks them by design. **BQ-27.**
- [x] ~~What `007AD450` (93 members) and `0085E710` (19) are — the two minority deallocators on the
      bit-2-clear side.~~ **BQ-28 ANSWERED 2026-09-13 (FABLE): each is its library's own aligned free, and both sets of destructors are that library's classes.** **`0085E710` is Bullet's `btAlignedFreeInternal`**, matched line for line with `btAlignedAllocator.cpp`: `if (!ptr) return; gNumAlignedFree++; sAlignedFreeFunc(ptr);` — the counter is `02EAF6C8` and the hook slot `01F44CF8`. Its siblings sit beside it: `btAlignedAllocInternal` `0085E680` (`gNumAlignedAllocs` `02EAF6C4`, hook `01F44CF0`); `btAlignedAllocDefault` `0085E630` (over-allocate, store the original pointer at `result − 8`); `btAlignedFreeDefault` `0085E6F0` (`free(*(p − 8))`); and the two setters `btAlignedAllocSetCustom` `0085E690` / `btAlignedAllocSetCustomAligned` `0085E6C0`. All of them are already members of the Bullet row of [the inventory](../../23-Third-Party-Libraries/third-party-middleware-inventory.md). **All 19 of its deleting destructors belong to Bullet classes** (`btRigidBody`, `btCollisionObject`, `btCompoundShape`, `btBvhTriangleMeshShape`, `btQuantizedBvh`, `btAxisSweep3`, …: 19 classes, one each) — Bullet's `BT_DECLARE_ALIGNED_ALLOCATOR` `operator delete`. At run time the hook is not Bullet's default. Phyre's physics start-up `006A4100` installs both setters (`006A43A0`–`006A43BA`): aligned `0069ECB0` and plain `0069ECC0` allocation into `0017D260`, and free `0069ECD0` → `00584730`. **So a Bullet object ends in the same `_aligned_free` as the majority path.** **`007AD450` is SEAD's aligned free**: `(*[02EAD0B8])(*(p − 8))`. Its allocation twin `007AD460` obtains the block through `[02EAD0B0]`, stamps **`0x5EAD5EAD`** (`SEAD`) at `+0`, a tag at `+4` and the total size at `+8`, and stores the original pointer at `result − 8`. The unaligned pair uses a `0x10` header (`007AD550` / `007AD540`), `007AD5A0` reallocates, and `007AD620` is the setter writing both slots. The setter's one caller is SEAD's initialiser `007A4D50` (`007A4E39`); it refuses if either of the configuration's first two words is null (`007A4E23`–`007A4E33`). FFXII's audio start-up `00210760` fills those words with `00210EC0` → the `malloc` import and `00210EB0` → the `free` import (`0021082A`–`00210853`). The same initialiser also points libogg / Tremor's C allocator slots `01F41CF8`–`01F41D10` (read by `007B9D70`…`007BA770` and `007F41A0`…) at SEAD's own heap wrappers (`007A4E3E`–`007A4E72`). **93 of `007AD450`'s 98 direct callers have the deleting-destructor shape, and every one has an `SQEX::Sd::` RTTI class** (Driver, Lay, `FixedList` / `FixedQueue` / `List` containers, `SeadObject<…>`, `DynamicValue<…>`, `NameBuffer`). The other 5 lie inside the SEAD span. Instrument: `ec7/dealloc_classes.py`. **BQ-28.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The deleting-destructor idiom and its two spellings | complete bodies of `001D70A0`, `00195530`, `0019B500` | 1 |
| All 226 deleting-destructor labels perform the flag test | whole-image disassembly, flag followed through a register copy from `edx` | 1 |
| The sub-labels record which deallocator is used | all 63 `AlignedOrGuardedFree` route through `0016D6A0`; all 88 `ScalarDeletingDestructor` call `00809950` | 1 |
| The CRT table has 1,172 entries, all function entries | direct read of `0x008C31D8`–`0x008C5678`; reproduces the static-init document exactly | 1 |
| 90/90 and 11/11 eager initializers are registered | set intersection of the labels with the table | 1 |
| 117/117 and 23/23 lazy labels call `_Init_thread_header`; 0 are registered | whole-image call census; the 707 total reproduces the lazy-statics document exactly | 1 |
| 85/85 vtable-install labels store a RIP-`lea` pointer into an object | whole-image disassembly | 1 |
| 49 `Microsoft` functions carry recovered MSVC/Concurrency symbols | snapshot `name_source: ANALYSIS` | 3 |
| `00809950` is `free` | recovered name; a 5-byte thunk to `00210EB0` | 3 |

**Both instruments were validated against existing documents before use.** The CRT table census
returns 1,172 and the guard census returns 707 — the exact figures the static-initialization and
lazy-statics documents already publish, derived independently here. An instrument that could not
reproduce a known number would not be trusted for an unknown one.

**Superseded readings:** two, both mine and both in the measurement rather than the material. See §10.

## 9. Related

- [`../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](../Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md) — the 707 guard callers, and the hang that follows a mistimed detour
- [`../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md) — when the 1,172 run
- [`../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) — B-2, the population audit this one follows in method
- [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) — why `0016D6A0` is inert
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) — 4,275 addresses tied to a class and slot; slot 0 is where these destructors live

## 10. Falsification pass 2026-09-02 — two defects, both in the test rather than the code

**Attack chosen.** These four labels were assigned by *shape*, and shape was demonstrably not
diagnostic for 1,762 functions in the funclet block. So: re-derive each named mechanism from the
image with instruments the labels never saw, and test **both directions** — how many members match,
and how many non-members match too.

### DEFECT 6: the detector was built from one instance of the idiom

The first census looked for `test dl, 1` and scored `CxxObjectLifecycle.ScalarDeletingDestructor` at
**0 of 135** — which reads as "this label is wrong for every member it has". It is not wrong for any
of them. Those destructors call an inner destructor first; that call clobbers `rdx`; so the compiler
moves the flag to a callee-saved register and tests it there (`mov ebx, edx` … `test bl, 1`). The
detector could not see the *more common* spelling of the thing it was detecting.

Fixed by following the flag through a register copy and by using the call to the deallocator — the
part that cannot be spelled two ways — as the primary diagnostic. **0 of 135 became 135 of 135.**

Found by reading four bodies instead of trusting a rate. A 0 % score on a label with 135 members is
not a finding, it is an instrument report.

### DEFECT 7: one instrument applied to two different mechanisms

The same census lumped every static-related label together — eager initializers *and* lazy accessors
— and tested the lot against `_Init_thread_header`, scoring **58.1 %**. That number is meaningless:
the eager ones are registered in a table and are *supposed* to score zero on the guard test, and the
lazy ones are guarded and are supposed to score zero on the table test.

Tested separately against the mechanism each label actually names, every group is perfect:

| label | own instrument | score |
|---|---|---|
| `StaticObjectInitializer` | CRT registration table | **90 / 90** |
| `StaticZeroInitObjectInitializer` | CRT registration table | **11 / 11** |
| `ThreadSafeStaticRecordAccessor` | `_Init_thread_header` | **117 / 117** |
| `ThreadSafeStaticObjectInitializer` | `_Init_thread_header` | **23 / 23** |
| teardown labels | neither | **0 / 88**, correctly |

**A blended rate over two mechanisms measures nothing.** The 58.1 % was not evidence that the labels
were half-earned; it was evidence that I had built one test for two questions.

### SURVIVED: seven mechanisms, all 100 %

226/226 deleting destructors · 90/90 and 11/11 eager initializers · 117/117 and 23/23 lazy
accessors and initializers · 60/60 and 25/25 vtable installs. Every label that names a mechanism
specific enough to test, passes on every member.

### SURVIVED: the other direction

178 functions perform the deleting-destructor idiom without carrying one of these labels. That looked
like under-inclusion until they were classified properly: **99 are `PrimaryOwner:Audio`, 42 Phyre, 17
`NativeRoutine`, 8 Input.** They are not unlabelled — they are *owner*-tagged, and the two layers are
disjoint by design. A destructor for an Audio object is Audio's; its compiler-generated shape does not
transfer it to a CodeDomain family. **The layer separation is doing exactly what it exists to do.**

Likewise 1,071 of the 1,172 registered initializers sit outside these families, and 566 of the 707
guard callers do too — the lazy-statics document already reports that three quarters of the latter
are PhyreEngine building its own type schema.

### FOUND: one label whose name is not supported

`CxxStandardLibrary.NativeQualified`, 52 functions. "Qualified" asserts a recovered qualified symbol,
and **all 52 have `name_source: DEFAULT`** — the snapshot holds no symbol for any of them. ~~The
functions may well be standard-library code; the *name of the label* claims evidence that is not
there.~~ Filed as **BQ-22** rather than defended.

#### `BQ-22` answered — the label is not merely unsupported, it is WRONG for at least two members (FABLE, 2026-09-22)

**Both halves of the original statement reproduce**: the label selects exactly **52** rows and
**52 of 52** carry a `FUN_` placeholder name. *What was still open is whether they are standard-
library code anyway. At least two are not, and this database already says so.*

**The discriminator is what they call.** Standard-library code does not call PhyreEngine's resource
layer. Two of the 52 do:

| member | size | calls | and it is already documented as |
|---|--:|---|---|
| `001A2130` | 1,564 B | `001A9050` | **a game manager/object constructor** — [game-application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) lists it under *manager/object constructors*, with `001EDF00` ×17 and its own vtables `008F6500` / `008F6600`, and its § says it *“names EASTL strings”* |
| `00200BF0` | 609 B | `00597970`, `00598100`, `0059BD40`, `0059F4A0` — four Phyre serialisation bodies | part of the authored-parameter read chain, cited on [how a sound request becomes a voice](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md) reading `Common.mDofApertureFnumber` |

> **So the label is a misattribution, not just an unjustified name.** A function with its own
> vtables that constructs a game manager is not `std`, whatever the tag says.

**What the measurement does NOT say is that all 52 are mislabelled**, and the shape evidence cuts
both ways. *For the label:* the 52 show the template-clone signature — four bodies of exactly 43
bytes, three of 270, three of 116, three of 101 — and their callees include bodies tagged
`Microsoft.MSVCCRT_STL_Runtime` and `Runtime.ContainerStringSupport`. *Against it:* **13 of the 52
have no caller at all**, the median member has **one** caller, and **none of the 52 calls only
other members of its own label**. **Two counter-examples are enough to retire the label's claim;
the other 50 are untested individually and this does not classify them.**

> **Controls.** The pass reproduces the published figures before reading anything else — 52 rows
> selected, 52 placeholder names — and the two counter-examples are confirmed against pages
> written independently of this label. **Static: the function/edge tables and the database's own
> prose, nothing executed.**

### What was tried and did not break anything

- **Both instruments were validated against published figures first.** The CRT table read returns
  1,172; the guard census returns 707. Both match existing documents exactly, derived independently.
  This is the third block in a row where checking against an existing document changed the outcome.
- **Looked for the vector deleting destructor.** `00185800` tests `dl,1` and then `dl,4` — ~~the array~~
  ~~form~~ not the array form — and carries none of these four labels. One instance found; ~~the population is unmeasured~~ *(answered: see BQ-26, ANSWERED 2026-09-02 - the population is 1,608 and bit 2 selects the deallocator; 2026-10-02, OPUS)*
  (**BQ-26**).
- **Avoided the call graph entirely.** 689 `Thunk.*` functions are graph sinks, so any measurement
  routed through call paths would truncate silently. Every census here is over instruction bytes or a
  data table.

### Status

`DOCUMENTED`, one falsification pass. Extended by §11.

## 11. Falsification pass 2026-09-02 (second) — BQ-26, and the question's own name was the hypothesis

**Attack chosen.** §7 filed the two-bit flag form as *"the vector deleting destructor"* and noted one
instance. That name was never measured — it came from what MSVC's second flag bit is called in some
references. So: enumerate the form from the image, record which bits and what each branch calls, and
only then decide what the bit means.

### DEFECT 8: the first census returned 1,616 and the shape said no

The first sweep promoted any register receiving `edx` to "the flag register", anywhere in the body.
In a 3 KB function that happens by accident. It returned **1,616 functions with a median body of 92
bytes and a maximum of 3,175**, 1,412 of them Phyre.

**The tool ran and reported nothing wrong. The shape of the answer did.** A 3,175-byte
compiler-generated destructor does not exist, so the population could not be what it claimed.
Tightened three ways — the flag copy must precede the first call, the function must return `this`,
and the body must be under 400 bytes — the population became **1,608**, median 92 B, **maximum 317 B**.

**Cross-checked against an instrument that has never seen a flag test:** the recovered vtable index.
**1,607 of the 1,608 are recovered virtual methods.** A loose detector does not produce that.

### REFUTED: it is not the vector form

A vector deleting destructor iterates over array elements. **Only 14 of the 1,608 contain any backward
branch at all.** There is no iteration, so there is no array. The name in BQ-26 was wrong, and it was
wrong because it was inherited from a reference rather than measured here.

### What bit 2 actually does — and the GFZ named it correctly

Measured over all 1,606 members with a resolvable branch: the bit-2-set side calls `0016D6A0` in
**1,606 of 1,606** cases; the bit-2-clear side calls `00584730` (1,494), `007AD450` (93) or
`0085E710` (19). Reading `00584730` settles it — it is `if (this) _aligned_free(this)`, a null check
in front of the imported `_aligned_free`.

**Bit 2 selects the sized `operator delete` over `_aligned_free`.** That is exactly what
`DeletingDestructor.AlignedOrGuardedFree` says. **The label was right; it is simply applied to 63 of
1,608.** The rest are Phyre and owner-tagged, which is the layer separation again — the third time in
three blocks that an apparent classification gap has turned out to be it working.

### And a consequence worth more than the audit

`0016D6A0` is the three-byte `ret 0` that `/OPT:ICF` folded ~273 `ret`-bodied functions onto. So on
the bit-2 path **these destructors free nothing at all** — 1,606 functions whose sized-delete branch
is a no-op. Either the engine never passes bit 2, or it leaks those objects deliberately. Filed as
**BQ-27**; it is checkable at runtime against the unmodified test client.

### A limit on a claim this document already made

§4 says the `mov edx, imm` before the free gives the class's exact size. That is verified at the
sized-delete call site of the destructors read in §2.1 (`0x90`, `0x98`, `0xD8`). It is **not** a
reliable bulk census: sweeping the first `mov edx, imm` in each of the 1,608 returns `0x100` for
1,186 of them, which is not 1,186 classes of 256 bytes — it is catching a different instruction.
**The claim holds per call site and not as a population statistic**, and the difference is stated here
rather than left for a reader to trip over.

### Status

`DOCUMENTED`, two falsification passes. What would kill it: a deleting-destructor label whose body has
no flag test under any register; a `StaticObjectInitializer` absent from `0x008C31D8`–`0x008C5678`; a
`ThreadSafeStatic*` member that never calls `008092FC`; a bit-2 member that iterates over an array;
or a runtime trace showing `0016D6A0` reached with a live object and memory actually released.

## A base vtable, 26 derived classes, and a correction to this section's first version

> **RETRACTED, same day.** The first version of this section said **"ICF folds vtables, not only
> functions — 26 classes on one 3-slot table"**, and concluded that the 26 shared a single folded
> vtable and therefore that **"none of the 26 overrides slot 1 or slot 2."** Both are wrong. There are
> **26 distinct vtables**, and **25 of them override exactly those two slots.** What is true is much
> narrower and is set out below. The reasoning that produced the error is kept at the end, because it
> is a reusable mistake.

### What is actually there

`01CD6268` begins an array of **26 four-slot vtables on a `0x20` pitch**, running to `01CD6588`:

```
01CD6268  0086CE50 dtor | ICF_FoldedRetStub | _purecall  | -> 01D4DFE8
01CD6288  0086CF40 dtor | 00874080          | 00873170   | -> 01D4E078
01CD62A8  0086CEF0 dtor | 00873FE0          | 00873100   | -> 01D4E108
01CD62C8  0086CEA0 dtor | 00873FB0          | 00873090   | -> 01D4E198
...                                                       (26 records)
```

**Only the first has `_purecall` and the folded `ret` stub in slots 1 and 2.** The other 25 carry real
implementations in both. Slot 3 of every record points into a per-class `.rdata` structure at
`01D4Dxxx`–`01D4Exxx`, each beginning `1` followed by pointers into `01C2Exxx`.

So `01CD6268` is a **base class whose two virtual methods are pure**, and the other 25 are derived
classes that implement them. The base's own slot 1 being the `ret` stub rather than a body is the
usual outcome of `/OPT:ICF` folding an empty implementation.

### The 26 destructors, and why they all install the base vtable

Each of the 26 vtables holds a **different** scalar deleting destructor at slot 0, in the band
`0086CE50`–`0086D620` on an 80-byte pitch. Every one of them writes **the base vtable `01CD6268`**
into the object, then frees using **its own class's size**:

| size | classes |
|---|---:|
| `0x28` (40 B) | **20** |
| `0x40` (64 B) | 4 |
| `0x38` (56 B) | 2 |

That combination — restore the *base* vptr, free the *derived* size — is what MSVC emits for a
derived class that adds no destructor body of its own: the vptr is rewound to the base before the
base destructor would run, while the deallocation size stays the derived one. **It is not evidence of
a shared or folded vtable**, which is exactly what the first version of this section read it as.

**The sized-delete branch still frees nothing.** All 26 route the bit-2 path to `0016D6A0`, the
three-byte `ret` — so these are 26 concrete, **sized** instances of **BQ-27**, which is the part of
the first version that survives.

### Probable identity, not claimed

The same address band holds **35 Phyre input class names** — `PInputSource`, `PInputSourceJoypadAxis`,
`PInputSourceKey`, the three `PInputSourceMotionAngularVelocity*`, the four `PInputSourceMotionQuat*`,
`PInputSourceTouchPinch`, the three `PInputSourceVisionTracker*` and so on — each referenced by
exactly one registration function on a `0xA0` pitch from `0086B2B0` to `0086C3C0`, alongside
reflection field names `m_name`, `m_inputSources`, `m_typeSemantic`, `m_invert`, `m_scale`,
`m_joypadAxisSemantic`, `m_positiveButtonSemantic`.

**Exactly 26 of the 35 are `PInputSource` and its subclasses**, which matches the 26 vtables. A
matching count would prove nothing on its own, so the registrars were read for a second, independent
quantity: each passes its class's **object size** in `r9d`.

| size | `PInputSource*` registrars | the 26 destructors |
|---|---:|---:|
| `0x28` | **20** | **20** |
| `0x40` | **4** | **4** |
| `0x38` | **2** | **2** |

**The size multisets are identical**, and the shape 20/2/4 across three values is distinctive enough
that agreement by coincidence is implausible. Named, with their sizes:

- `0x38` — `PInputSourceJoypadAxis`, `PInputSourceMouseButton`
- `0x40` — `PInputSourceJoypadButton`, `PInputSourceKey`, `PInputSourceMouseDeltaX`, `PInputSourceMouseDeltaY`
- `0x28` — `PInputSource` itself and the nineteen motion / quaternion / touch / vision-tracker sources

**So the family is identified: these 26 vtables are `PInputSource` and its 25 subclasses.** The base
with two pure virtuals is `PInputSource`, whose registrar also reports `0x28`.

**The per-class mapping is still not established.** No registrar contains any reference into
`01CD6268`–`01CD65A8` — checked across all 35 — so nothing joins an individual name to an individual
vtable. Within a size band the members are interchangeable on present evidence, and **no row of the
26 is individually named here.** The missing link is whatever writes a class's vtable into its
descriptor at run time; the registrars install only the descriptor's own vtable (`01CD0xxx`).

### The mistake, kept

The first reading came from a scan that recorded, for each destructor, the target of its
`lea rax, [rip+…]`. All 26 gave `01CD6268`, and that was taken as "26 classes, one vtable". **The
measurement was correct and the inference was not**: in MSVC a destructor's vptr store names the
class whose destructor is *about to run next*, not the class the function belongs to. The check that
would have caught it immediately is the one that did, hours later — **asking where each destructor's
own address appears in `.rdata`.** Twenty-six distinct answers on a regular pitch is a vtable array;
one answer would have been a shared vtable.

**A scan that reads one field of a structure will describe that field faithfully and the structure
wrongly.**

## The two `basic_filebuf` vtables, member by member — 2026-09-14 (NOCALLER-INSTALLERS)

`008F3EC8` is the `std::basic_filebuf<char>` vtable and `008F38F0` the `wchar_t` twin — the
index's `basic_filebuf` slot-0 entries (`0019B500`/`00195530`, the deleting destructors above)
are their first members. Twenty of the twenty-two no-caller members are the filebuf overrides;
slots 5, 8 and 9 hold the **base** `basic_streambuf` defaults (`showmanyc`, `xsgetn`, `xsputn`),
which filebuf does not override. The narrow and wide classes also share slots 1 and 2 — the same
two 15-byte guard-thunks appear in both vtables, so they are type-independent paths, not per
character-type code.

| slot | `char` (`008F3EC8`) | `wchar_t` (`008F38F0`) | role | interior |
|---:|---|---|---|---|
| 1 | `0019B800` | `0019B800` | shared 15-B guard-thunk — `je`+tail `jmp` through `008C2B28` | `0019B80C` |
| 2 | `0019B8A0` | `0019B8A0` | shared 15-B guard-thunk — tail `jmp` through `008C2B30` | `0019B8AC` |
| 3 | `0019BAD0` | `00197B40` | the big fill routine (684/706 B): conversion-state frame, `00195CF0`, three CRT-import calls | `0019BB11` / `00197B91` |
| 4 | `0019BD80` | `00197E10` | get-area walk on `+0x38`/`+0x50`/`+0x68`/`+0x70`/`+0x80` buffer pointers | `0019BDEC` / `00197E8F` |
| 6 | `0019C490` | `00199320` | put/get pointer recompute on `+0x20`/`+0x30`/`+0x38`/`+0x50` | `0019C49D` / `00199320` |
| 7 | `0019C130` | `00198FC0` | the big drain routine (861/864 B): mirror of slot 3's shape, `00195670` | `0019C196` / `0019902A` |
| 10 | `0019BE30` | `001987A0` | seek-off family: arg-offset arithmetic on `+0x30…0x48`, `0019B580`/`00195940` | `0019BE77` / `001987E8` |
| 11 | `0019BF10` | `00198880` | seek-pos family: same shape as slot 10, `+0x74` flag | `0019BF44` / `001988B4` |
| 12 | `0019BFF0` | `00198ED0` | set-buffer family: `+0x38…0x58`/`+0x68` pointer rewrite | `0019C023` / `00198EF6` |
| 13 | `0019C0E0` | `00198F60` | sync/flush tail: `+0x18`/`+0x80` write-out through one CRT import | `0019C108` / `00198F96` |

`00197B40`'s group also lists `00197930` (80 B, `00194F50` plus two CRT imports, interior
`00197940`) and `00198FC0` is the wide drain above — the two groups' overlap is slots 1/2 only.
These are statically-linked CRT bodies reached only through the filebuf vtable; nothing in
`.text` `lea`s either table, because the CRT constructs the objects internally.


## The `00900F20` `basic_stringbuf` vtable — NOCALLER-INSTALLERS, 2026-09-14 (FRONTIER)

`00900F20` is the `std::basic_stringbuf<char>` vtable (RTTI locator `01CED3D0` →
`.?AV?$basic_stringbuf@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@`), installed by the
constructor's own `lea rax, [00900F20]` at `001DE45A` — the one code reference to the table.
Six of its fourteen slots are the no-caller frontier members; the other eight hold the shared
`008088xx` CRT stubs (the base `basic_streambuf` defaults, same pattern as the filebuf tables
above):

| slot | address | role | interior |
|---:|---|---|---|
| 0 | `001DE450` | the deleting destructor — installs this vtable then calls `001DF8C0` | `001DE45A` |
| 3 | `001DFA80` | overflow/pback family: mode flags at `+0x70` gate the `+0x38`/`+0x40`/`+0x50` buffer walk | `001DFA87` |
| 4 | `001DFCF0` | get-area bound check: `+0x38` head vs `[+0x18]` limit, `edx == -1` EOF arm | `001DFCFA` |
| 6 | `001E0390` | `+0x38` head plus `+0x50` offset walk — the showmanyc-class query | `001E039C` |
| 10 | `001DFE20` | seek-off: walks `+0x40` chain with the arg offset | `001DFE2D` |
| 11 | `001DFFC0` | seek-pos: `r8` position pair + `+0x40` head | `001DFFC2` |

Like the filebuf pair, nothing calls these directly — the CRT reaches them through the vtable
on the internally-constructed `stringbuf` objects (`std::stringstream` internals).

## `BQ-27` — static reading was not exhausted, and it settles 262 of 607 call sites (OPUS, 2026-09-14)

This page sends `BQ-27` to a live breakpoint: *"Either the engine never passes bit 2, or it leaks
those objects by design … **Static reading cannot.**"* **Static reading gets most of the way.** Read
from the shipping executable at the authority hash `73461D08…9721F8`.

### The branch requires TWO bits, which the disjunction never said

`0016D6A0` is `c2 00 00` — `ret 0` — then `int3` padding. A worked destructor, `0017CC70`:

```
0017CC99  test dil, 1       ; bit 0 - delete at all?
0017CC9D  je   0017CCBE     ;   no -> skip entirely
0017CC9F  test dil, 4       ; bit 2 - SIZED delete?
0017CCA3  jne  0017CCB0     ;   yes ->
0017CCA5  call 00584730     ;   no  -> ordinary operator delete(ptr)   <- corrected 2026-10-02, OPUS - 00584730 is if (p) _aligned_free(p): jne 0019C570, and 0019C570 is jmp [008C2B70] = _aligned_free; no operator delete is imported
0017CCB0  mov  edx, 0x1140  ; the object size
0017CCB8  call 0016D6A0     ; -> ret 0
```

**Reaching the `ret 0` needs bit 0 AND bit 2.** Bit 2 alone fails the first test and skips the delete.

### Where the flag is readable, it never carries both

**2,471 bodies call `0016D6A0`**; 1,659 are in `rtti/methods.tsv`, at vtable **slot 7** (1,219) and
**slot 0** (371). So a deleting-destructor call is `call qword [reg + 0x38]` or `call qword [reg]`.
Every such site in every listed body:

| | sites | flag literal | computed | literal values |
|---|---:|---:|---:|---|
| slot 7, `[reg + 0x38]` | 172 | 35 | 137 | `0`×30, `1`×4, `0x14`×1 |
| slot 0, `[reg]` | 435 | 227 | 208 | `1`×87, `3`×69, `0`×67, `4`×4 |

> **No literal has bit 0 and bit 2 both set.** `5` and `7` occur at none of the 262 sites, and the
> four passing `4` have bit 0 **clear** — they skip the delete rather than take the sized path.

The population is a **superset** of deleting-destructor calls — slot 0 and slot 7 of every vtable —
which is what makes the negative usable: a literal `5` or `7` reaching a destructor would appear here.

### What is left

**345 sites compute the flag** (137 slot 7, 208 slot 0). The proposed instrument — one breakpoint on
`0016D6A0` with `rcx` non-null — is still right, and is now aimed at **345 call sites rather than the
whole engine**, with a prediction to falsify: *nothing reaches it*.

*Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): 345 becomes **61**.* A deleting destructor's flag is an `unsigned int`
passed in `edx`, and all 263 literal flags here are written as 32-bit `edx`. **217 of the 345 sites write the full
64-bit `rdx`** as their last argument write: a qword load, an address `lea`, a 64-bit copy or 64-bit arithmetic. The
slot's method at those sites takes a pointer-sized second parameter, so it is not a deleting destructor.
Reaching definitions of `rdx` over each function's CFG then settle 19 more and show 47 where a path from a call reaches it
with no `rdx` write, so the method takes no second argument. The live target is the remaining **61** sites: 34 pass the
enclosing function's own incoming `rdx` through, and 27 compute a 32-bit flag.
Per-site list and control: [`bq27-arg-width`](../../_index/candidates/bq27-arg-width/README.md).

### Not claimed

Not that the branch is unreachable — only that no **literal** flag reaches it. Not which of the 345
computed sites are destructor calls. Not that `0016D6A0` is `operator delete(void*, size_t)`: it is
the address `/OPT:ICF` folded ~273 `ret`-bodied functions onto, so its identity is a fold.

*(Read by OPUS 2026-09-14. `BQ-27` stays open on the 345. What changes is that "static reading
cannot" was wrong — the cheaper evidence had not been exhausted before the live test was proposed,
which is the order this project's own routing rule asks for.)*


## Interior citation — frontier hub `001AB570` (2026-09-18, SWE2-EC7)

`001AB570` — 318 B, 9 A-measured callers at census; `vector<void*>::insert` with grow, the
8-byte-element sibling of the string-insert family. Interior verified against the shipping
image: when `[rcx+8] != [rcx+0x10]` there is spare capacity — the tail elements are shuffled
one slot up via the indirect move call at [`001AB5BB`](../../_index/ADDRESS-INDEX.md), the new element is stored,
and `[rcx+8]` advances by 8. When full, `sar r9,3` / `lea ebp,[r9+r9]` at `001AB5DD`–`001AB5F0`
compute `capacity = (end-begin)/8`, `newcap = 2*capacity` (minimum 1); the allocator object at
`[rcx+0x18]` is invoked through vtable slot `+0x10` (`001AB613`, `edx = newcap*8` bytes), the
head and tail ranges are copied by two more indirect moves (`001AB628`, `001AB652`), the old
buffer is released through slot `+0x18` (`001AB681`), and the `{begin, cur, end}` triple at
`+0x00`/`+0x08`/`+0x10` is rewritten at `001AB68C`–`001AB6A1`. The in-place branch rounds the
move count down to a multiple of 8 (`and rax, ~7` at `001AB5B4`) — the copy runs in whole
elements only.
Presentation's `001BD4A0` and `001BDD20` call the same insert — the `vector<void*>` shape is
shared CRT machinery, not a Presentation contract.

### Interior citation — frontier hub 005CD6D0 (2026-09-18, SWE2-EC7)

**005CD6D0** (37 B, 4 A-measured callers) — the teardown chain's shared implementation §46's family-28 row names "NOT dispositioned". Clears a flag byte at `[rcx]`, reads `[rcx+8]` ~~(the module's callback slot), calls the CRT's `[008C23CC]` IAT entry (the wake/sync primitive the family-28 teardowns all funnel to), and zeroes `[rcx+0x10]`~~, a handle it closes through `CloseHandle`, and clears the byte `[rcx+0x10]` *(corrected 2026-10-02, OPUS: `005CD6D0+0x15` is `call [008C23E0]`, the `KERNEL32` import `CloseHandle`)*. The "flagged teardown" members (`00677520` chain) collapse to exactly this once the slot guard drops. In-scope: flag clear [`005CD6DA`](../../_index/ADDRESS-INDEX.md); IAT call [`005CD6E5`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## BQ-25 answered: the 88 are identified positively, and they are two unrelated things (2026-09-19, OPUS)

*The row's complaint was exact — `0/88` on both construction instruments is a correct negative and
not an identification. Both groups are now identified by **what reaches them**, which is the evidence
a negative could never supply. They turn out to have nothing to do with each other beyond the word
"teardown".*

**Both groups are byte-uniform templates.** All 28 `ConditionalTeardownReturnTrue` bodies are exactly
44 bytes and **one** distinct instruction-mnemonic sequence; all 60
`StaticContainerTeardown.IndirectAllocator` bodies are exactly 72 bytes and **one** sequence.
**And all 88 have zero direct callers** — nothing in the image `call`s any of them, which is why a
call-graph instrument could only ever answer negatively. They are reached by address, and the two
groups are reached in two different ways.

### The 60 are registered with `atexit`, which is what settles them

Each of the 60 is the target of **exactly one** rip-relative `lea`, from **60 distinct host
functions** of 228–240 bytes in the `0015Cxxx` family — 60 hosts, 60 thunks, one apiece. Each host
ends the same way ([`0015C62B`](../../_index/ADDRESS-INDEX.md) in `0015C560`):

```
lea  rcx, [rip + ...]      ; the thunk
mov  byte ptr [rdi], 0
add  rsp, 0x20
pop  rdi
jmp  0x808b90              ; atexit
```

**`jmp atexit` with the thunk in `rcx`** — a static initialiser registering its own destructor to run
at process exit. That is a positive identification of "teardown" in the only sense the word has.

What the thunk then does is uniform across all 60: it loads a global **begin/end pointer pair**,
takes `end - begin`, and **if the count is more than one and `begin` is non-null** calls
**`qword ptr [rax + 0x18]`** — the allocator's virtual deallocate. `[rax+0x18]` is the call in
**60 of 60**, with no other call in any body. So: *free a static container's block through its
allocator's vtable, at exit.*

### The 28 are a virtual method, not a teardown of that kind

They are referenced **only as 8-byte VAs in `.rdata`**, 28 sites for 28 thunks, and never by a `lea`
and never called. The sites are runs of contiguous function pointers — vtables — and the population
proves it rather than a sample does. Taking each site's neighbours across **all 28**:

| slot | value | in how many |
|---|---|---|
| `−2` | `0062EFD0` | **28 / 28** |
| `−1` | `0062F080` | **28 / 28** |
| `+3` | `00660570` | **28 / 28** |
| `+4` | `005C5230` | 25 / 28 |
| `+1` | `0063FC60` | 16 / 28 |
| `−4`, `−3`, `+2` | *(all different)* | 1 / 28 |

**Three slots hold the same function in every one of the 28 tables while the slots either side of the
thunk vary per table.** That is a shared base-class layout with per-class overrides, and it makes the
thunk **one slot of a common interface, implemented 28 times** — not a CRT teardown at all.

The body matches: it null-checks its object argument, calls **exactly one** callee — **28 thunks, 28
distinct callees**, one per class — and returns `al = 1`. ~~A conditional destroy-and-report-success
virtual.~~ **Corrected 2026-09-29 (SWE2-EC7, FABLE family ruling R4):** it constructs, it does not destroy.
RTTI names the slot: see "The 28 construct" below.

*(A caution on the table: `+5` is `_guard_check_icall` in 28/28 too, which is not a plausible vtable
slot. It is most likely the first qword **past** the table rather than a member of it, so it is
recorded and not used.)*

### What is still open

The two groups should not share a label. ~~**NOT CLAIMED:** which interface the 28 implement~~ *(answered: see "The 28 construct" below - the class-descriptor interface, corrected 2026-09-29; 2026-10-02, OPUS)* — the
three constant slots (`0062EFD0`, `0062F080`, `00660570`) name it and none of the three has been
read; what the 28 per-class callees destroy; and which containers the 60 hosts own. The `mov qword
ptr [rsp+0x20], 0xFFFFFFFFFFFFFFFE` both groups open with is an MSVC EH-state slot and says only that
both were compiled with exceptions enabled — it distinguishes nothing, and an earlier reading of this
session took it as evidence the 28 were unwind funclets, which the `.rdata` vtable runs refute.

### The 28 construct: slot 10 (`+0x50`) of the Phyre class descriptor (corrected 2026-09-29, SWE2-EC7)

*FABLE family ruling R4 ([`fable-family-ruling-0929`](../../_index/candidates/fable-family-ruling-0929/README.md)).*
RTTI names the interface that the three constant neighbours pointed at. In `rtti/methods.tsv` **all 28** are slot 10
(`+0x50`) of a Phyre class-descriptor vtable: 27 of `PClassDescriptorConcrete<T>` and one of
`PClassDescriptorWithoutDefaultConstructor<PScheduler>`. The neighbours agree with that slot map on the
[class-descriptor page](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md):
`−2` is `+0x40` (`AttachMember`, `0062EFD0`) and `+3` is `+0x68` (the shared `00660570`). That page names slot 10 the
class's **placement default constructor**, `if (rdx) T::T(rdx); return 1`. So the one callee in each body is class
`T`'s constructor, called out of line, and nothing is destroyed. The first two members read confirm it: each callee
calls its base-class constructor and then zero-initialises the object's fields.

This answers two of the NOT CLAIMED items above. The 28 implement the class-descriptor interface, and their callees
construct. Which containers the 60 hosts own is still open. The 17 of the 28 that are declared as a family sit in the row
renamed `Phyre.PClassDescriptorConcrete.PlacementCtorConditionalReturnTrue` from `CxxObjectLifecycle.ConditionalTeardownReturnTrue`
(renamed on [generated-function-families.md](../Generated-Families/generated-function-families.md); its acceptance by form
stands). The other 11 are measured A. Regression:
[`rename_check.py`](../../_index/candidates/ec7-family-ruling-exec-0929/rename_check.py).

## SWE2-EC7-36 update (2026-09-19) - `00195940`

`00195940` (649 B) is a CRT init/fini body - `008C2618`/`008C2650`/`008C2DA8`/`008C2F40` import run, `00210EB0`/`00195670`/`00808C40`. Interior anchor `00195AB9` (an `00808C40` call).

## SWE2-EC7-36 update (2026-09-19) - `0019B580`

`0019B580` (633 B) is the sibling CRT body - `008C2618`/`008C2788`/`008C2DA8`/`008C2F40` import run, same `00210EB0`/`00195670`/`00808C40` calls. Interior anchor `0019B6E9` (an `00808C40` call).

## The missing destructors are not a gap — 35 of 39 types do not own their storage (2026-09-19, OPUS)

*`types.tsv` records a constructor for 64 types and a destructor for 26. Read as a coverage figure
that is an alarming asymmetry: **39 types have a constructor and no destructor.** Read as an
ownership question it is almost entirely correct, and the four that are not resolve to two.*

**Where the 39 get their storage**, from their own `allocation_site` rows:

| origin | count | is a missing destructor a defect? |
|---|--:|---|
| `INTERIOR` (a field or array inside a parent) | 16 | **No** — the parent owns it |
| `IMAGE` (`.data`/`.bss`, present from load) | 14 | **No** — nothing allocated it |
| `CALLER` (the caller supplies the bytes) | 4 | **No** — the caller owns it |
| `POOL` (a slot in a preallocated block) | 1 | **No** — the pool owns it |
| **`HEAP`** | **2** | **This is the only case where the question is real** |
| unstated | 2 | needs the row filled before it can be judged |

**So 35 of the 39 are correct by construction.** A type that never allocates has nothing to release,
and recording a destructor for it would be the error. *"39 types have no destructor"* is the kind of
figure that looks like a finding and is an artifact of counting.

### The two heap types, and both are allocate-once-never-free

`GameSettingConfig` says so already: *"malloc(0x65C), the pointer stored to `01F82D20` at
`00798261`. **Allocated once and never released.**"*

`CharacterRenderRecord`'s array was not established, and now is. Its `0x48930` block is allocated at
`003325E7` and published to `022C6F28`. **372 bodies in the image reference that pointer. Not one of
them calls a deallocator** — checked against `0036A140`, `00809950`, `00210EB0`, `0019C590`,
`0078A960` ~~and `0085E730`~~, the free/dealloc entries this corpus has identified, and the `malloc` stub `0085E730` *(corrected 2026-10-02, OPUS: `0085E730` is `jmp [008C2B40]`, the `malloc` import, not a free)*. The array is taken
once and held for the life of the process.

**That is a contract fact, not an absence.** A reimplementation may allocate this block at startup
and never track it; there is no teardown path to reproduce, and adding one would diverge from the
engine. The same holds for the settings object.

### THE TWO UNSTATED ROWS RESOLVE TO ONE NON-OWNER AND ONE REDIRECTED QUESTION

Both were *unstated* only to my classifier, which keyed on a prefix:

* **`Mt19937State`** reads *"MIXED BY INSTANCE"* — the gameplay stream is `IMAGE` (`.bss` at
  `02EB3870`), the graphics-noise stream is `CALLER` (supplied in `rcx` to `0018D740`). **Both
  instances are non-owning**, so it joins the 35: **36 of 39 correct by construction.**
* **`FieldRecordTable`** is `RESOURCE`, and its row already flags the release as open.

**That open question is not answered here, but it is pointed somewhere better.** The row says the
storage is *"reached through `*(02ADD100)`"*, which reads as a pointer dereference. **The slot does
not hold a pointer.** Nine bodies reference it and two write it, and both writes store a **32-bit**
value into the qword: `00378B80` is ten bytes — `mov eax, ecx` / `mov [rip+…], rax` / `ret`, a
setter that **zero-extends its argument** — and `00378540` stores `rsi`, itself a small integer
(`lea ecx, [rsi+1]` feeds a call two instructions earlier). A user-mode heap pointer in this image
does not fit in 32 bits, so **`02ADD100` holds a handle or index, not the buffer**.

So the buffer is the resource system's to own and release, addressed by that handle, and **no
deallocator appears among the nine because the slot never holds the thing that would be freed.**
Looking for a free near this slot was always going to come back empty. **NOT CLAIMED:** what the
handle indexes, or whether the resource system releases the buffer — that is the same question,
now asked in the right place.

**NOT CLAIMED:** that no free exists anywhere. The test is a hand-listed set of deallocator entries,
so a release through an unlisted wrapper, or through a function pointer, would not appear — the same
indirect-call limit that bounds every other sweep on this page. What is claimed is that **no direct
call to any known deallocator occurs in any of the 372 bodies that can see the pointer**, which is a
strong negative over a large population rather than a failure to find one.

## SWE2-EC7-44 update (2026-09-19) - `00195CF0`

`00195CF0` (255 B) is the conversion-state fill routine's helper - `008C2618` import calls, `00195670`/`00861EC0`. Interior anchor `00195D1F` (a `00195670` call).

## SWE2-EC7-44 update (2026-09-19) - `00194F50`

`00194F50` (270 B) is ~~a sound-request body~~ `std::use_facet<std::codecvt<wchar_t, char, _Mbstatet>>`, a C++ standard-library body - `008C25F0`/`008C2628`/`008C2630`/`008C2658` import calls, `00808850`/`00861ECC`. Interior anchor `00194F73` (~~an `00808850` call~~ the `_Lockit` call) *(corrected 2026-10-02, OPUS: `00194F50+0x23` constructs a `_Lockit` through `008C25F0`, `00194F50+0x36` reads `codecvt<wchar_t>::id` from `008C2768` and `00194F50+0x96` calls `_Getcat` through `008C2658`; `00808850` is called at `00194F50+0xEB`)*.

## SWE2-EC7-49 update (2026-09-19) - `001DF8C0`

`001DF8C0` (193 B) is the base teardown the deleting destructor calls - `00210EB0` plus four `008C2DA8` import calls. Interior anchor `001DF90D` (the `00210EB0` call).

## SWE2-EC7-77 update (2026-09-20) - `00209B50` CRT free-path validator measured

`00209B50` (111 B) is the CRT block-free guard: `r8 >
0xFFFFFFFFFFFFFFF` traps to the `008C2DA8` invalid-parameter handler;
`r8*16 >= 0x1000` additionally requires `edx & 0x1F == 0` (alignment),
`[rdx-8]` to sit below `rdx`, and the `rdx - [rdx-8]` gap in
`8..0x27` - each violation calls the handler and `int3`s. Clean
blocks tail `00210EB0`.
Interior anchor `00209B77` (the `test dl, 0x1f` alignment gate).

## SWE2-EC7-110 update (2026-09-20) - `001BCFB0` measured

`001BCFB0` (138 B) is the
sentinel-list clear `001BD4A0`
and `001BDAC0` run: `rdx +
0x28` is the list head, the
walk follows `[rbx]` links
until the sentinel address
returns, and each node passes
through the virtual
`vtable[qword[rdi + 0x10] +
0x18](node, 0x20)` - the
0x20-byte typed free. The tail
then jumps through
`vtable[qword[r14 + 0x30] +
0x18](rbp, 0x40)` for the
0x40-byte container itself -
two destruction sizes on one
vtable slot.
Interior anchor `001BCFF0`
(the link-walk loop head).

## SWE2-EC7-111 update (2026-09-20) - `00195180` measured

`00195180` (118 B) is the
destructor `00195440`,
`001954B0` and `001993B0`
reach (`00195530` is the
vtable slot pointing at it):
the `008F38F0` vtable (RTTI
`01CEC408`) latches first,
then a live `qword[+0x80]`
with `qword[+0x18]` pointing
back at `rbx + 0x70` unlinks
the intrusive node -
`[[+0x18]]` and `[[+0x38]]`
both receive `qword[+0x88]`
and `dword[[+0x50]]` gets the
remaining span
`(+0x90 - +0x88) >> 1`.
`byte[+0x7C]` armed runs the
`001969D0` detach, and the
tail jumps through the
`008C2678` IAT for the base
teardown.
Interior anchor `001951B3`
(the unlink span read).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page cites the destructors, allocators and serialisation bodies that object lifetime runs through. Their
callers are clients across the image, and every one of them is **SERVICE**.

- **Audio and SEAD, 217 edges: SEAD's own allocators.**
  - The aligned free `007AD450` (98 audio callers) and allocation `007AD460` (43), the unaligned pair `007AD550` /
    `007AD540`, the reallocation `007AD5A0`, and the setter `007AD620`.
  - The configuration comes from SEAD's initialiser `007A4D50`, which FFXII's audio start-up `00210760` fills; the
    console's `001DBA40` also reaches `00210760`.
  - The shared teardown `005CD6D0` has six audio callers, and `007F41A0` and `007B9D70` sit in SEAD's driver band.

  Which objects the sound engine builds is the 18 pages' subject.
- **Resource, 63 edges.**
  - The four Phyre serialisation bodies `00597970`, `00598100`, `0059BD40` and `0059F4A0` are called by the resource
    loaders (`0019EAA0`, `001A0CF0`-`001A0F80`, `001D9A40`), and reach `001D6AA0` / `002150D0`.
  - `001A9050`, `AddMotion_LoadResources` and `00210760` call the resource request helpers `001D6E80`-`001D6FA0`.
  - The vector grow `001AB570` is also called by the asset-manifest parser.
  - The map-table requester `00378540` issues `0032E400` / `0032E620`.
- **Presentation, 8 edges.** `001BD4A0` constructs and resets character render objects
  (`CharacterRenderObject_Construct`, `CharacterRenderObject_ResetState`). `AddMotion_LoadResources` parses its file,
  and `001BC190` / `001BDAC0` reach these bodies.
- **Input, 5; CoreRuntimeScheduling, 3; Save_Load_Settings, 1; Script_VM_Native_Bridge, 1; WorldAreaField, 1;
  RNG_Random_Selection, 1 — MECHANICAL.** Each is one more caller of a shared lifetime helper:
  - the destructor `001993B0`, from `0017D670` and `001E0F40`;
  - the serialisers, from `0079FB10`;
  - `00873FE0` / `00874080`;
  - `001BDAC0`, from the frame step;
  - `001DF8C0`, from `GameSettingConfig_SerializeText`;
  - `00660570`, from `00510740`;
  - `00378540`, from `WorldAreaField_BootMapTables`;
  - `GraphicsNoiseMT19937_SeedState`, from its time-and-clock seeder.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 slice OPUS-P22-SLICE-24-99).*

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-object-construction-destruction-and-stat-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00199320` | 99 B | loads the word pointer at qword `[qword +0x38]` of `rcx` and, when it is non-null and below itself plus twice the sign-extended dword at `[qword +0x50]` (unsigned `jae`), returns the zero-extended word it points at; otherwise calls vtable slot `+0x38` of `rcx` and, when its word result is not 0xFFFF, calls vtable slot `+0x20` with that word as `edx` and returns the word, else returns 0xFFFF | `00199343`, `00199345`, `00199359`, `00199364`, `00199372` |
| `001E0F40` | 36 B | calls the callee at `001E0F40` + 0x4 and returns when it returns null; otherwise calls the same callee again (`001E0F40` + 0xE) and tail-jumps `001993B0` with that second result as `rcx` | `001E0F44`, `001E0F4C`, `001E0F4E`, `001E0F5A` |

`00199390` (19 B, no direct call; vtable slot 1 of `std::exception` and `std::bad_cast`) returns the stored message pointer `+8`, or the string at `008F35F8` ("Unknown exception") when it is NULL - `exception::what`.

Interior anchor `0019939E` (function `00199390`).

`0019B940` (80 B, no direct call; `std::basic_filebuf<char>` vtable slot 14) fetches the locale's `codecvt` facet (`0019B2F0`, the facet lookup by id), and when the `MSVCP140` import `codecvt_base::always_noconv` (slot `008C2638`) says no conversion is needed clears the converter pointer `+0x68`; otherwise stores the facet there and tail-jumps to `basic_streambuf::_Init` (slot `008C27B0`) - the converter set-up `imbue` runs.

Interior anchor `0019B95B` (function `0019B940`).
