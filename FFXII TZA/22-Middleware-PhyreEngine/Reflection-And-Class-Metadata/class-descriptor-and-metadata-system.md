---
system: Phyre reflection — class descriptors and member metadata
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre.Reflection
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 3
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
function_families:
  - "PClassDescriptorForType deleting destructors | C | members/pclassdescriptor-deleting-destructors.tsv | 1148 | not this game's code: PhyreEngine's PClassDescriptorForType<T> reflection template, one instantiation per registered type, emitted through the MSVC C++ deleting-destructor idiom. THE FAMILY IS PROVED BY BYTES, NOT BY THE TAG: all 1,149 bodies are exactly 92 bytes with one shared 12-byte prefix, and masking the four operands that must vary leaves TWO byte images differing at exactly ONE offset - the object-size immediate, 0x100 for 1,145 and 0x108 for 4. THE BOUNDARY: a reconstruction that instantiates the same template gets these for free from its own compiler. What is NOT dispositioned is named in the members file - the single shared base destructor 00633390 (still in the frontier), the 400 distinct vftables the members install, and whatever each descriptor describes. 2026-09-30 (SWE2-EC7, GI re-status): 1 member left the family, since measured as A (A beats a declaration) after SWE2-FRONTIER c97af7156 re-statused the 13 GI pages PARTIAL -> DOCUMENTED; exact A removal, no re-runnable selector named."
  - "PClassDataMember deleting destructors | C | members/pclassdatamember-deleting-destructors.tsv | 138 | not this game's code: compiler- or template-generated. PROVED BY FORM - 138 members, all 82 bytes, the MSVC deleting-destructor idiom over PClassDataMember, sibling of the PClassDescriptorForType family already declared here; 2 byte images collapse to ONE form. CONTROL: three shared targets, each x138 - 006332A0 the base destructor, 00584730 operator delete, and 0016D6A0. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: 006332A0, 00584730 and 0016D6A0, all still in the frontier."
  - "AbstractClassDescriptor base-aware constructors | C | members/abstract-class-descriptor-base-aware-constructors.tsv | 132 | not this game's code: compiler- or template-generated. PROVED BY FORM - 133 members, all 163 bytes, 56 byte images collapse to ONE instruction form - the members differ only in constants. CONTROL: six shared targets including 006372A0, 006373D0 and 00632D80, each x133. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: the six shared targets, and the descriptor each member builds. 1 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv."
  - "PClassDescriptorConcrete static initialisers | C | members/pclassdescriptor-static-initialisers.tsv | 254 | not this game's code: compiler-generated static-initialiser registrations, one per concrete PClassDescriptor. PROVED BY INSTRUCTION FORM - 254 members all 53 bytes, 237 byte images but ONE form image. Shape: lea the static descriptor, call this type's constructor, clear flag bit 1, install the vftable, and TAIL-JUMP TO atexit registering this type's teardown. CONTROL: all 254 tail-jump to 00808B90 (atexit). NOT DISPOSITIONED, AND IT IS THE LARGER HALF: each member calls ITS OWN per-type constructor - 254 distinct external targets, one per member, EVERY ONE STILL IN THE FRONTIER. This row disposes of the registration wrapper, not of what it constructs."
  - "AbstractClassDescriptor constructors | C | members/abstract-class-descriptor-constructors.tsv | 178 | not this game's code: PhyreEngine generated constructors for the abstract class-descriptor template. PROVED BY INSTRUCTION FORM - 182 members all 152 bytes, 47 byte images but ONE form image (figure corrected 2026-09-18 under OPUS-NOTE-SWE2-EC7-ABSTRACTDESC-48-BYTE-IMAGES: 48 was the family_prover byte-scan count - the scan desyncs on the literal E8 immediate byte of `mov r9d, 0xE8` at member offset 58, skipping the REX of the lea at offset 64 and leaving its disp32 unmasked, which splits 00690950/00690AA0; the operand-aware wildcard used by verify_form_families.py and members/gen_form_note.py merges them), with the standard MSVC constructor prologue and EH state -2. THE BOUNDARY: the constructor body is the template's; a reconstruction instantiating the same template gets it from its own compiler. NOT dispositioned: 006373D0, and the descriptor each member builds. 4 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv."
  - "reflection object traversal adapters | C | members/object-traversal-adapters.tsv | 304 | not this game's code: PhyreEngine generated adapters, one per bound type. PROVED BY BYTES AND RESTRICTED BY THEM - two variants of one idiom: 188 at 46 B traverse the object directly; 116 at 75-76 B add a member offset with a null guard and differ only in that offset immediate; all 304 call ONE target, 0063E2E0. EXTENDED 2026-09-17: joined by 6 same-form frontier members of the 76 B variant (005A0E30, 005A12A0, 005A1920, 005A2140, 005A2390, 005A26A0). 1 member(s) of the tag group are EXCLUDED BY ADDRESS because they are a different idiom: 0063E2C0 (29 B) takes a DYNAMIC offset from the class descriptor at [rcx+0xF4] rather than a constant; it is a different idiom and is excluded. THE BOUNDARY: each member adds a constant offset and delegates; a reconstruction that binds the same types gets these from the same generator. NOT dispositioned: the shared implementations they delegate to, and whatever object or member each adapter names."
  - "registry-fetch reflection traversal adapters | C | members/registry-fetch-traversal-adapters.tsv | 84 | not this game's code: PhyreEngine generated adapters, one per bound type - the registry-fetching siblings of the 298-member traversal row above. PROVED BY FORM - two instruction-form skeletons, each ONE operand-aware byte image: 70 bytes x69 (xor ecx,ecx clears the getter argument before the flag test) and 68 bytes x15 (no clear). Every member tests its flag argument r8b, calls a member-specific registry getter, then delegates to the shared Reflection.ObjectTraversal 0063E2E0(registry, object, flag) and returns true - the flag selects the traversal direction, and in BOTH spellings the getter and the traversal are each emitted twice (the compiler duplicated the flag-true and flag-false tails rather than sharing them). CONTROL: each member's external direct calls are exactly {one member-specific getter x2, 0063E2E0 x2}; 84 distinct getters across the family. THE BOUNDARY: which getter (which bound type) varies per member; the adapter shape does not. NOT dispositioned: the getters, the traversal implementation's contract, and what each adapter registers. Selector: members/select_registry_fetch_traversal_adapters.py"
  - "PDataMemberMetadata static teardowns | C | members/data-member-metadata-static-teardowns.tsv | 853 | not this game's code: compiler-generated from PhyreEngine's reflection templates - one per static PDataMemberMetadata instance, emitted through the MSVC static-teardown / destructor-thunk idiom. PROVED BY BYTES, NOT BY THE TAG: all 853 bodies are exactly 12 bytes and mask to ONE distinct byte image. Shape: lea rcx, [<static metadata object>] ; jmp 00633240. THE BOUNDARY: the member installs a constant and tail-calls; it has no logic of its own, and a reconstruction that instantiates the same templates gets these from its own compiler. NOT dispositioned: 00633240, the shared implementation every member tail-calls, which is still in the frontier; and the static objects and vftables the members name."
  - "PClassDescriptor static teardowns | C | members/class-descriptor-static-teardowns.tsv | 404 | not this game's code: compiler-generated from PhyreEngine's reflection templates - one per static PClassDescriptor instance, emitted through the MSVC static-teardown / destructor-thunk idiom. PROVED BY BYTES, NOT BY THE TAG: all 404 bodies are exactly 26 bytes and mask to ONE distinct byte image. Shape: lea rax, [<vftable>] ; lea rcx, [<static descriptor>] ; mov [<static descriptor>], rax ; jmp 00633390. THE BOUNDARY: the member installs a constant and tail-calls; it has no logic of its own, and a reconstruction that instantiates the same templates gets these from its own compiler. NOT dispositioned: 00633390, the shared implementation every member tail-calls, which is still in the frontier; and the static objects and vftables the members name."
  - "PClassDescriptorForType destructor thunks | C | members/pclassdescriptor-destructor-thunks.tsv | 384 | not this game's code: compiler-generated from PhyreEngine's reflection templates - the NON-deleting destructor, one per instantiation. ITS CONSUMER IS THE UNWINDER, NOT STATIC TEARDOWN (corrected 2026-09-13, FABLE-REQ-OPUS-DTORTHUNK-WORDING; the earlier wording borrowed the static-teardown idiom from the two rows above, where it is correct, and it is not correct here): each of the 384 has EXACTLY ONE direct caller and all 384 of those callers are CompilerGeneratedEH unwind funclets, and NONE of the 384 is stored as a pointer anywhere in initialised data - 0 vtable slots, verified against 10,434 code addresses that ARE stored. A reader hooking these for exit teardown would never see one fire on a normal exit; normal-exit teardown is the separate 26-byte family in the row above. PROVED BY BYTES, NOT BY THE TAG: all 384 bodies are exactly 15 bytes and mask to ONE distinct byte image. Shape: lea rax, [<vftable>] ; mov [rcx], rax ; jmp 00633390. THE BOUNDARY: the member installs a constant and tail-calls; it has no logic of its own, and a reconstruction that instantiates the same templates gets these from its own compiler. NOT dispositioned: 00633390, the shared implementation every member tail-calls, which is still in the frontier; and the static objects and vftables the members name."
  - "PType name-only class-registration initialisers | C | members/name-only-class-registration-initialisers.tsv | 110 | not this game's code: compiler-generated dynamic-initialiser stubs - the minimal members of the 315-registrar set documented in member-registration-and-the-recovered-field-schema.md, each registering one class descriptor BY NAME ONLY. PROVED BY FORM - 110 members, all 32 bytes, ONE instruction form (sub rsp,0x28 / lea rcx,[descriptor] / call 006388C0 / lea rcx,[descriptor] again / add rsp,0x28 / jmp 00639450); only the descriptor operand varies. CONTROL: every callee is 006388C0 PType_FindOrRegisterByName and every tail-jump is 00639450, the shared class-registration finaliser that sets the +0xFC registered bit; the second lea re-loads the SAME descriptor for the finaliser in all 110 - it is not a dtor. THE BOUNDARY: the form is the toolchain's; a reconstruction registering the same classes gets these from its own compiler. SIBLINGS, NOT MEMBERS: the 254 PClassDescriptorConcrete static initialisers declared above are the OTHER registration variant - 53 bytes, per-type constructor, vftable install, atexit tail - and the 420 atexit-tailed stubs of the same 32-byte form are registry initialisers of other subsystems (see static-init-form-530). NOT dispositioned: 006388C0 and 00639450 themselves, and which class each descriptor names. Selector: 24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/members/select_static_init_form.py"
  - "two-member class-descriptor registrars (m_count + m_els) | C | members/two-member-descriptor-registrars.tsv | 38 | not this game's code: compiler-generated thread-safe guarded initialisers, each building one Phyre class descriptor that registers exactly two members named m_count and m_els - the count + elements pair of a resizable-array-style reflection layout. PROVED BY FORM PLUS THE MEMBER-NAMED LITERALS - 38 members, all 815 bytes, 545 byte positions identical; every member contains disp32 references to BOTH 00D27728 'm_count' and 00D32DC0 'm_els', each literal unique in the image, passed to the member-registration calls 00632960/00632A10. CONTROL: all 38 call the three descriptor constructors 006372A0, 006373D0 and 00632D80 - the same three targets the accepted AbstractClassDescriptor base-aware constructors family names as its controls - plus _Init_thread_header 008092FC exactly four times each. THE BOUNDARY: a SIBLING of the constructor families, not a member - these are the guarded registration bodies that CALL the constructors; a reconstruction registering the same two-member types gets these from its own compiler. NOT dispositioned: the called constructors and member-registration helpers, the descriptor each body builds, and which array-like type each describes. Selector: members/select_two_member_descriptor_registrars.py"
  - "descriptor-flag registration initialisers | C | members/descriptor-flag-registrars.tsv | 34 | not this game's code: compiler-generated dynamic-initialiser stubs - the 64-byte flag variant of the atexit-registered descriptor-registration idiom. PROVED BY FORM PLUS BOTH-HALVES PROVENANCE - 34 members, all 64 bytes, 39 byte positions identical over the full set (the 25 varying positions are exactly the object/record/dtor/flag disp32 and call/jmp rel32 operands), census-wide skeleton scan finds NO unselected twins; every member calls a declared AbstractClassDescriptor constructor (base-aware or plain), installs an .rdata record pointer into a descriptor static, clears bit1 and sets bit3 of the object's +0xFC flag word, then registers the object's declared static teardown through the atexit wrapper 00808B90. TWO POPULATIONS, ONE ENCODING: the frontier remainder of OPUS's measured 331-body run 0016AB00..0016D540 (4 bodies, objects at 0x100 stride 02EB9070..02EB9370) and the 64-byte cluster of the atexit-anchor tail-643 worklist (30 bodies, objects across the descriptor-static bands 02CBxxxx/02CFxxxx/02D3xxxx/02E3xxxx/02E4xxxx/02E5xxxx/02EAxxxx). THE BOUNDARY: the toolchain emits the wrapper from the static declaration; a reconstruction declaring the same statics gets it from its own compiler. NOT dispositioned: the constructors and teardowns (declared elsewhere), the descriptor objects and .rdata records, and the flag-word semantics. Selector: members/select_descriptor_flag_registrars.py"
  - "guarded class-registration stubs | C | members/guarded-class-registration-stubs.tsv | 99 | not this game's code: compiler-generated thread-safe class-registration stubs - the stubs of the Phyre/PType registration tree, one per registered class payload. PROVED BY CALL-SET SIGNATURE, NOT BY SIZE (members span 129..3757 B because each registers a different member set): every member calls _Init_thread_header 008092FC and _Init_thread_footer 0080929C around its payload, registers a teardown through the atexit wrapper 00808B90, and every OTHER call target is already-explained code - a declared family member, an A-measured helper, or one of the shared frontier machinery helpers (006388C0 PType find/register x87, 00632960 member-reg x74, 005A7A40 x27, 00632FB0 x26, 006B66C0/006B67D0 x18, 00632D80/0063DC80/0063DF90/0063DFA0 x17, 00632A70 x15, 00632C90 x14, 00639160 x8, 005A0470 x6, 00632BE0 x6, 005CC8A0 x4, 00225690/00584730/00616210/006B6820/006B8D20 x2) - the family's shared-target control. SELF-BOUNDING: the same predicate over the whole census matches these plus only bodies already owned (Phyre module families x152, the 38 two-member m_count/m_els registrars - this family's specialised sibling) or A-measured. THE BOUNDARY: the toolchain emits the stub from the static declaration; a reconstruction registering the same classes gets these from its own compiler. NOT dispositioned: the shared machinery helpers (frontier), and the descriptors/member sets each stub registers. Selector: members/select_guarded_class_registrars.py. 2026-09-18: 76→75 - member 005A02D0 has since been measured as A and is dropped by the selector seed exclusion (A beats a declaration). 2 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 005B4E00, 00613800; 1 member joined the family 2026-09-20 by cascade demotion from the orchestrators row: 00617E60 2 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. A re-run of members/select_guarded_class_registrars.py now differs beyond these departures (it would move 2 entries in from the orchestrator list and admit 1 more); only the A departures are applied here (selector-drift.tsv in the same record). 2026-09-29, FABLE ruling e862a1dae (_index/candidates/fable-gcr-split-ruling-0929), applied by SWE2-EC7: ONE family. The row formerly named 'guarded class-registration orchestrators' (25 members) is retired into this one, and this row's 'leaf bodies' wording is retired with it: the split counted whether a stub's auxiliary calls met another member, so it moved bodies whenever another family's bookkeeping moved, and it named no kind of code. The members TSV keeps the fact as an information column (auxiliary callees of the guarded form, whoever owns them: 76 of 99). The unified selector re-run - the fixpoint unchanged - reproduces all 97 previous members, admits the 2 frontier bodies withheld on 2026-09-29 and drops none: 72 + 25 + 2 = 99; addresses in _index/candidates/ec7-gcr-unify-0929. 2026-09-30 (SWE2-EC7, accounting-state ruling round, record _index/candidates/ec7-accounting-predicate-audit-0930): DERIVED family (FABLE ruling on SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930, point 2): membership is defined by accounting state (what its callees' explanations are), so it is computed last, as a fixed point after every identity family; it is never a closure or membership input for an identity family, and its membership moving when accounting changes is expected and reported separately, not as drift."
  - "descriptor-flag registration initialisers, compact encoding | C | members/descriptor-flag-registrars-compact.tsv | 5 | not this game's code: compiler-generated dynamic-initialiser stubs - the 53-byte compact encoding of the same registration idiom: sub/lea obj/call ctor/`and dword [obj+0xFC],~2` (clears bit1 only - no bit3 set)/lea record/lea dtor/mov [obj],rax/jmp 00808B90. PROVED BY FORM PLUS BOTH-HALVES PROVENANCE - 5 members, 34 of 53 byte positions identical; a census-wide scan finds 228 bodies of this encoding of which 223 are ALREADY DECLARED (222 by PClassDescriptorConcrete static initialisers - it is that family's encoding - plus 1 A-measured) leaving exactly the 5 frontier members - THE DISCRIMINATOR FROM THE 223 TWINS IS PRIOR OWNERSHIP, not provenance: the twins satisfy the identical predicate (declared base-subobject ctor, declared teardown, flag=obj+0xFC, tail=00808B90); each member calls a declared AbstractClassDescriptor ctor and registers a declared teardown (4 in xc-registered-static-teardowns, 1 in class-descriptor-static-teardowns). THE BOUNDARY: as above - toolchain-emitted wrapper, reconstruction gets it from its own compiler. Selector: members/select_descriptor_flag_registrars_compact.py"
  - "flag-selected reflection traversal adapters | C | members/flag-selected-traversal-adapters.tsv | 11 | not this game's code: PhyreEngine generated adapters, one per bound type - the static-descriptor siblings of the registry-fetch traversal row above. PROVED BY FORM - 11 members, all 46 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: lea a member-specific static descriptor into rcx, then call the shared Reflection.ObjectTraversal 0063E2E0 twice - once with r8b=1, once with r8d=0 - selected by the caller's r8b flag (the compiler duplicated the flag-true and flag-false tails); returns 1. CONTROL: 0063E2E0 is the only external direct target, x11 (twice per member); member identity is the lea'd static, not a call. NOT dispositioned: the member descriptors and the traversal implementation's contract - this row disposes of the adapter, not the adapted. Selector: members/select_flag_selected_traversal.py"
  - "Phyre object-lifecycle lookup adapters, 69-byte form | C | members/object-lifecycle-lookup-adapters.tsv | 6 | not this game's code: compiler- or template-generated Phyre adapters. PROVED BY FORM - 6 members, all 69 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: if rdx non-null, call shared Phyre.Reflection.ObjectLifecycleDispatch 0063BC00 on a member-specific rip record; on a non-null result store this in the stack slot and call a member-specific op on (this, result); return 1. CONTROL: 0063BC00 x6 shared plus ONE member-specific op each (00615D80 x2 subset-shared, 4 distinct others). NOT dispositioned: the shared implementation and the member-specific ops - this row disposes of the adapter, not the adapted. Selector: members/select_descriptor_siblings_2.py"
  - "Phyre shared-runtime identity dispatch adapters, 118-byte form | C | members/shared-runtime-identity-dispatch-adapters.tsv | 6 | not this game's code: compiler- or template-generated Phyre adapters. PROVED BY FORM - 6 members, all 118 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: call shared Phyre.Reflection.SharedRuntime 00639850 through a global vtable slot; compare the result identity/field against this+off and arg3; call a member-specific op on the matching branch; return 0. CONTROL: 00639850 x6 shared plus member-specific ops (006A5950 x3 subset-shared, 3 distinct others). NOT dispositioned: the shared implementation and the member-specific ops. Selector: members/select_descriptor_siblings_2.py"
  - "Phyre static-descriptor singleton lazy-init adapters, 150-byte form | C | members/static-descriptor-singleton-lazyinit-adapters.tsv | 7 | not this game's code: compiler- or template-generated - the magic-static spelling of the descriptor singleton. PROVED BY FORM - 7 members, all 150 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: bounds-check a global index table, call shared CRT init 008092FC then shared Phyre.Reflection.StaticDescriptorSingleton 0062FF50; or-flag a global tag twice via member ops; call shared 0080929C; install a member rip pointer and return it. CONTROL: 008092FC x7, 0062FF50 x7 and 0080929C x7 shared, plus member-specific ops (4 distinct). NOT dispositioned: the shared implementations and the member-specific ops. Selector: members/select_descriptor_siblings_2.py"
  - "Phyre static-descriptor singleton lazy-init adapters, 132-byte form | C | members/nativeadapter-staticdescriptorsingletonlazyinit2.tsv | 5 | not this game's code: compiler- or template-generated - the second magic-static spelling of the descriptor singleton, fetching the singleton through a member getter and the descriptor through shared 006301F0 (the 150 B row calls 0062FF50 instead). PROVED BY FORM - 5 members, all 132 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton: TLS-indexed init counter via gs:[0x58]; bound-check then call shared CRT once-init 008092FC; fetch the member singleton via a member getter, tag it |1 into a member rip cell; call shared 006301F0 for the descriptor and store it; register the teardown via shared 0080929C; return the member rip descriptor address. CONTROL: 008092FC x5, 006301F0 x5 and 0080929C x5 shared, plus ONE member-specific getter each. NOT dispositioned: the shared implementations and the member getters. Selector: members/select_descriptor_siblings_3.py"
  - "Phyre static-descriptor singleton lazy-init (third spelling), 122-byte form | C | members/nativeadapter-staticdescriptorsingletonlazyinit3.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 122 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: TLS-indexed init guard via _Init_thread_header 008092FC; on first pass  tag two member rip slots with |1 and register teardown via  _Init_thread_footer-shaped 0080929C; return the member descriptor  address. Third lazy-init spelling: no 0062FF50/006301F0 helper call. CONTROL: 2 external target(s): 2 shared across all 4 members (0080929C, 008092FC). NOT dispositioned: the shared implementation(s) 0080929C/008092FC. Selector: members/select_descriptor_siblings_4.py"
  - "descriptor-or-field select tail-dispatch, 35-byte form | C | members/nativeadapter-descriptorfieldselecttail.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 35 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: rax=[this+0x30]; select rax or a member rip descriptor via cmovne;  tail-dispatch to shared 005CDAA0 with ecx=2 and a member rip arg. CONTROL: 1 external target(s): 1 shared across all 4 members (005CDAA0). NOT dispositioned: the shared implementation(s) 005CDAA0. Selector: members/select_descriptor_siblings_4.py"
  - "Phyre singleton-alloc descriptor-install adapters, 58-byte form | C | members/nativeadapter-singletonallocdescriptorinstall.tsv | 5 | not this game's code: compiler- or template-generated - the eager sibling of the lazy-init spellings: allocate an 8-byte record via shared 001A1470 on a member global container (after the conventional call to the ICF-folded ret-0 stub 0016D6A0, ecx=1), install a member rip descriptor pointer at [rax], and store rax into a member global. PROVED BY FORM - 5 members, all 58 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton. CONTROL: 0016D6A0 x5 and 001A1470 x5 shared; member identity is the rip descriptor and the two member globals. NOT dispositioned: the shared implementations and the member globals. Selector: members/select_descriptor_siblings_3.py"
  - "PClassDescriptorConcrete<T> placement default constructors, slot 10 (+0x50) | B | members/pclassdescriptorconcrete-placement-default-ctors.tsv | 123 | class-explained (FABLE family ruling R2, 2026-09-29, _index/candidates/fable-family-ruling-0929; declared by SWE2-EC7, record _index/candidates/ec7-family-ruling-exec-0929): slot 10 (+0x50) of the Phyre reflection template PClassDescriptorConcrete<T> is the class's placement default constructor - construct a default T at the given address when it is non-null, and return 1 (`if (rdx) T::T(rdx); return 1`, the carried-table slot map on this page). MEMBERSHIP, both halves read from the image by members/select_descriptor_placement_ctors.py: (1) RTTI - every appearance of the body in rtti/methods.tsv is slot 10 of a PClassDescriptorConcrete<...> vtable; (2) SHAPE - one trailing ret, test rdx,rdx then je, and al = 1 at the ret on both the null path and the constructed path (join or hoisted spelling); not A, not in another family, not UC-1. CONTROLS: positive - all 108 already-explained bodies of the same RTTI population (30 A, 78 declared in seven other rows) pass the shape half; negative - the xor al,al stub 00657140 that sits at +0x50 on the abstract classes is refused by the shape; 15 census bodies outside the RTTI population also pass the shape and none is admitted, so the RTTI slot is the discriminator. 123 members, 12-124 B in 67 distinct sizes (form-diverse, which is why no form family reached them); 30 call a base or member constructor inside. WHAT B COVERS: the wrapper - the slot's role, the null test and the return value. NOT COVERED: the inlined T::T in each member is class T's default constructor. It is explained, or not, with class T's own type entry, not by this row, and so are the base or member constructors it calls. Not C: for game classes the inlined constructor is game code."
---

# Phyre reflection — class descriptors and member metadata

> **4,557 functions — roughly one in every eight in the whole game — exist only to describe the
> game's own C++ classes to itself.** This is the largest single mechanism in the executable,
> and almost none of it is game logic.

## 1. What the player sees

Nothing. Directly, this system has no player-visible behaviour at all — and that is worth
saying plainly rather than inventing a player-facing story for it.

What it *causes* is visible everywhere: it is the reason FFXII can load a character, an
animation, a material or a scene out of a data file and end up with a working object in memory.
Every asset the game loads is matched against a description of the type it is supposed to
become. When a mod swaps an asset and the game accepts it, this is the layer that accepted it.
When the game refuses an edited asset outright, this is usually the layer that refused.

For a modder the practical consequence is: **the engine knows the name, type and byte offset of
every field of every reflected class**, and that description lives in the executable rather than
in the asset files.

## 2. Native mechanism

### The type hierarchy

Read directly from the vftable assignments in the destructors:

```
PType
  +-- PClassDescriptor
        +-- PClassDescriptorAbstract
        +-- PClassDescriptorConcrete<T>
        +-- PClassDescriptorForType<T>
```

`FUN_00633390` proves the top two links: it assigns `Phyre::PClassDescriptor::vftable` on entry
and `Phyre::PType::vftable` on exit — the standard MSVC base-class destructor chain, so
`PClassDescriptor` derives from `PType`.

### One static initializer per reflected class

```c
void FUN_001603e0(void)                     // a PClassDescriptorConcrete static initializer
{
    FUN_005a7ed0(&DAT_02cad140);            // construct the descriptor in place
    _DAT_02cad23c = _DAT_02cad23c & 0xFFFFFFFD;   // clear flag bit 1
    _DAT_02cad140 = Phyre::PClassDescriptorConcrete<Phyre::PAnimation::PAnimatableComponent>
                    ::vftable;
    atexit(FUN_008a8e20);                   // register the matching teardown
    return;
}
```

Each reflected class gets a **global descriptor singleton**, constructed by a generated
initializer at process start and torn down through `atexit`.

> **Extended 2026-09-02 — the descriptor is eager, its field list is not.** This section is
> correct about the descriptor *object*. It does not cover the field records inside it, and those
> are built **lazily**: 680 of the 682 `PClassDataMember` registrations execute behind a
> one-time-initialisation guard, the first time the class is touched. So a descriptor exists from
> startup with an **empty member list**, which fills in on first use. The registration ABI, the
> attribute bits and the recovered field schema — 682 records, 173 named classes, real byte
> offsets — are in
> [`member-registration-and-the-recovered-field-schema.md`](member-registration-and-the-recovered-field-schema.md).
> Nothing else in this document is affected; the `atexit` pairing proof stands.

**The `atexit` call is the proof of pairing.** `FUN_008a8e20` is exactly the function the GFZ
independently tagged `Reflection.ClassDescriptorStaticTeardown`. The initializer/teardown
correspondence is not inferred from naming or address adjacency — it is a direct call reference.

### Member metadata teardown

```c
void FUN_008aa000(void) { FUN_00633240(&DAT_02cb0a40); return; }   // one per data member

void FUN_00633240(undefined8 *self, ...)                           // shared helper
{
    *self = Phyre::PClassDataMember::vftable;
    if ((longlong *)self[1] != self + 1) { ... }  // detach an intrusive list node
    FUN_006b6700(self + 7);                       // destroy an embedded string (the name)
    if ((*(byte *)(self + 5) & 1) != 0) { ... }
    return;
}
```

`PClassDataMember` is the per-field descriptor. It carries an **embedded string** — the field's
name — and sits in an intrusive linked list hanging off its owning class descriptor.

**830 functions are one-line teardown thunks of this exact shape**, one per reflected data
member.

### What a class descriptor holds

From the destructor `FUN_00633390`, which must release every owned member:

| Offset | Released by | Inferred content |
|---|---|---|
| `+0x00` | vftable slot | `PClassDescriptor` → `PType` on exit |
| `+0x0C` | `FUN_006b6700` | embedded string (the class name) |
| `+0x0E` | `FUN_0063d640` | a sub-object, destroyed first |
| `+0x10` | intrusive list walk | list #1 |
| `+0x12` | intrusive list walk | list #2 |
| `+0x14` | intrusive list walk | list #3 |
| `+0x16` | intrusive list walk | list #4 |
| `+0x1D` | compared to `DAT_02CF8260` | a generation / registration counter |

**Four separate intrusive linked lists.** Their individual roles are not established — see §7.

> **Unit correction 2026-09-02 — the offsets in this block and in §4 are qword indices, not byte
> offsets.** The decompiler prints `param_1[0x10]` on an `undefined8 *` and they were transcribed
> as `+0x10`. In bytes the four lists are **`+0x80`, `+0x90`, `+0xA0`, `+0xB0`** — confirmed
> independently by the attach path, which links a member into `cls+0x80` with its tail at
> `cls+0x88`, and by the reset helper `0063D550`. That helper re-initialises **six** lists, so
> there are two more at `+0x50` and `+0x60` that this destructor does not walk. The sub-object is
> at byte `+0x70` and the counter at `+0xE8`, both confirmed directly in the destructor's operands.
>
> **Two further corrections, one of them to the first version of this note.** The entry this table
> calls an *embedded string (class name)* is **neither a string nor the name**: byte `+0x60` is a
> sixth intrusive **list**, self-linked by the reset helper and cleared in the destructor by
> `006B6700` — which is a list-unlink loop, not a string destructor. **The type name is a plain
> `char *` at byte `+0x30`**: `PType_FindOrRegisterByName` (`006388C0`) loads it with
> `mov rsi,[rcx+0x30]`, returns early when it is null, and hashes the bytes it points at. The
> first version of this note said the name was at `+0x60` — that was arithmetic on this table's
> own mislabelled index rather than a reading of the binary, and it was wrong in exactly the way
> the note was written to warn about. A modder using `+0x0C` as a byte offset reads the wrong
> memory; so does one using `+0x60` for the name. Derivation in
> [`member-registration-and-the-recovered-field-schema.md`](member-registration-and-the-recovered-field-schema.md) §8.

### The generated families and their sizes

**Family counts corrected 2026-09-02 (§9).** The total was verified exactly; the split between the
named families and the remainder was not. Previous values are shown struck.

| Family | Count | Was | Avg bytes |
|---|---:|---:|---|
| `PClassDescriptorForType.DeletingDestructor` | **1,149** | ~~1,054~~ | 92 |
| `DataMemberMetadataStaticTeardown` | **853** | ~~830~~ | ~10 |
| `ClassDescriptorStaticTeardown` | **404** | ~~372~~ | ~10 |
| `PClassDescriptorForType.DestructorThunk` | **384** | ~~352~~ | — |
| `ObjectTraversalAdapter` | 299 | 299 | — |
| `PClassDescriptorConcrete.StaticInitializer` | **255** | ~~227~~ | — |
| `GeneratedMetadataRoutine` | **189** | ~~173~~ | — |
| `AbstractClassDescriptor.Constructor` | **182** | ~~157~~ | — |
| `PClassDataMember.DeletingDestructor` | 138 | 138 | — |
| `AbstractClassDescriptor.BaseAwareConstructor` | **133** | ~~128~~ | — |
| *(remaining 32 reflection families)* | **571** | ~~827~~ | — |
| **Reflection total** | **4,557** | 4,557 | 92 |

There are **42** distinct `Phyre.Reflection.*` code-domain components in total; the ten above are the
largest.

~~**2,134 RTTI classes** are present in the binary~~ — **superseded 2026-09-08, see §14: the count is
2,248, and the run that produced 2,134 failed to demangle about three quarters of the names.** The
order-of-magnitude point stands: the descriptor families and the class corpus are comparable in size.
**But "roughly one descriptor set per reflected class" is now measured rather than assumed** — 409
types are reflected, §12.

### The deleting-destructor family

```c
undefined8 * FUN_005847e0(undefined8 *self, ulonglong flags, ...)
{
    *self = Phyre::PClassDescriptorForType<Phyre::PSerialization::PBinary::PClusterHeaderBase>
            ::vftable;
    FUN_00633390();                          // base PClassDescriptor destructor
    if ((flags & 1) != 0) {                  // bit 0 = "also free the storage"
        if ((flags & 4) == 0)  FUN_00584730(self);        // -> _aligned_free
        else                   _guard_check_icall(self, 0x100, ...);
    }
    return self;
}
```

This is the MSVC **scalar deleting destructor** convention: bit 0 of the flags word means
"delete after destructing". Bit 2 selects a Control Flow Guard-mediated path instead of the
direct `_aligned_free`.

**Phyre descriptors are allocated with aligned allocation**, not plain `operator new`.

## 3. Key addresses

| Address | Role | Verified |
|---|---|---|
| `00633390` | `PClassDescriptor` base destructor (500 bytes) | ✅ read |
| `00633240` | `PClassDataMember` destructor helper | ✅ read |
| `00584730` | aligned-free wrapper | ✅ read |
| `005847E0` / `00584950` / `00584A40` | `PClassDescriptorForType<T>` deleting destructors | ✅ read |
| `001603E0` / `00160420` / `00160480` | `PClassDescriptorConcrete<T>` static initializers | ✅ read |
| `008AA000` / `008AA010` / `008AA020` | data-member teardown thunks | ✅ read |
| `008A8E20` / `008A8E40` / `008A8E60` | class-descriptor teardown thunks | ✅ read (via atexit link) |
| `0063E2E0` | `Reflection.ObjectTraversal` shared helper | ⚠ decompile incomplete — *read from the disassembly 2026-09-14: the reflected byte-order walk, §7 Q-4* |
| `005A7ED0` | `AbstractClassDescriptor.Constructor` | ✅ read (called from initializer) |
| `0063D640` | descriptor sub-object destructor | not read |
| `006B6700` | ~~embedded-string destructor~~ **intrusive-list unlink loop** | ✅ read 2026-09-14 (OPUS, pass 13) |
| `02CF8260` | global compared against descriptor `+0x1D` | — |

## 4. Data structures and formulas

```
PType                                    base of the reflection type hierarchy

PClassDescriptor : PType
  +0x00   ptr    vftable
  +0x0C   str    embedded string (class name)
  +0x0E   ptr    sub-object, destroyed via 0063D640
  +0x10   list   intrusive list #1
  +0x12   list   intrusive list #2
  +0x14   list   intrusive list #3
  +0x16   list   intrusive list #4
  +0x1D   i32    counter compared against DAT_02CF8260

PClassDataMember
  +0x00   ptr    vftable
  +0x08   node   intrusive list node (self-referential when empty)
  +0x28   flags  bit 0 tested during teardown
  +0x38   str    embedded string (member name)
```

**Scalar deleting destructor flags** (MSVC convention, confirmed in body):

```
flags bit 0  (0x1)   free the storage after destructing
flags bit 2  (0x4)   use the CFG-mediated delete path instead of _aligned_free

destruct(self, flags):
    self.vftable = PClassDescriptorForType<T>::vftable
    PClassDescriptor::~PClassDescriptor(self)
    if (flags & 1):
        if (flags & 4) == 0:  _aligned_free(self)
        else:                 _guard_check_icall(self, 0x100, ...)
    return self
```

**Empty intrusive list test** (used throughout):

```
isEmpty(list)  iff  *list == list        a list head points at itself when empty
```

## 5. Call chain

```
process start
  -> CRT static initializers
     -> PClassDescriptorConcrete<T> static initializer      (227 of these)
        -> AbstractClassDescriptor constructor (005A7ED0)
        -> install PClassDescriptorConcrete<T>::vftable
        -> atexit(ClassDescriptorStaticTeardown)            <- the pairing proof

runtime
  -> asset load / object traversal
     -> Reflection.ObjectTraversal (0063E2E0)
        -> walk the descriptor's member lists

process exit
  -> atexit chain
     -> ClassDescriptorStaticTeardown       (372)
     -> DataMemberMetadataStaticTeardown    (830)
        -> PClassDataMember destructor (00633240)
```

**Upstream:** the CRT's static-initializer table at startup.
**Downstream:** serialization, asset loading, and the Lua object bindings — everything that
needs to know a type's shape.

**Do not confuse with:** MSVC RTTI (`TypeDescriptor` / `RTTICompleteObjectLocator`), which is a
*compiler* facility present in the same binary. Phyre reflection is a separate, hand-rolled
system that happens to describe many of the same classes. Both exist; they are not the same data.

## 6. Modding notes

- **The type descriptions are in the EXE, not the assets.** Adding a field to a reflected class
  is a code change, not a data change — there is a generated descriptor, initializer, teardown
  and destructor per class, all compiled in.
- **Descriptors are aligned allocations.** Anything hooking their lifetime must use
  `_aligned_free`, not `free`.
- **One in eight functions in the binary is this system.** When a call graph or coverage sweep
  looks overwhelming, most of it is 92-byte generated stubs, not logic to understand.
- **`atexit` order governs teardown.** Descriptor teardown runs at process exit through the CRT
  chain; a mod that unloads earlier will race it.
- **XIIOnline:** this layer is pure local type metadata. It carries no game state and nothing here
  needs to cross the wire. It matters only because asset-shape disagreements between clients
  surface as load failures here rather than as gameplay divergence.

## 7. What is not known

- [x] What the four intrusive lists at `+0x10`, `+0x12`, `+0x14`, `+0x16` each hold — members,
      base classes, interfaces, instances? **Q-1.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (Q-1), by reference and with one list left:*
      the four heads are the qword indices of **byte offsets `+0x80`, `+0x90`, `+0xA0` and `+0xB0`** (the unit correction
      under §4's table). The sibling page traced three of them instruction by instruction
      ([member registration and the recovered field schema](member-registration-and-the-recovered-field-schema.md)):
      - **`+0x80` holds the fields.** `AttachMember` `0062EFD0` links the 682 field registrations.
      - **`+0x90` holds the reflected methods**, linked at `005AD8F0` (`"playOnce"` and 219 others).
      - **`+0xA0` holds the script bridge**, the subset published to the script VM, linked at `005B2860` (`"GetGlobalTime"`).
        *Amended 2026-09-25 (FABLE, Claude Opus 5.5):* these records are **static functions, not a subset of `+0x90`'s
        methods**. Every register-formed `+0xA0` insert is followed by a `PFunctionCallerConcrete`, which takes no
        receiver; every `+0x90` insert whose caller type was resolved has a `PMethodCallerConcrete`. The script-VM
        attribution comes from the writers' domain tags and is not re-tested.
      - ~~**`+0xB0` is not identified.** No descriptor virtual touches it, and the base destructor drains it without freeing
        (the [descriptor contract](CONTRACT-phyre-class-descriptor.md)). That residue is register row **BL-8**, together
        with `+0x60`.~~ **2026-09-25 (FABLE, Claude Opus 5.5): `+0x60` is the annotation list** — the `PAnnotatable`
        base sits there — and no annotation is attached to a descriptor in this image. **`+0xB0` is still unnamed**, and
        no insert into it was found in any swept shape. Both are argued in the
        [descriptor contract](CONTRACT-phyre-class-descriptor.md)'s §14 item 1; `+0xB0` stays with register row
        **BL-8**.
- [x] What `DAT_02CF8260` counts and what the `+0x1D` comparison decides. **Q-2.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (Q-2):* **it is the class-descriptor id
      allocator, and the comparison decides whether a dying descriptor gives its id back.** `+0x1D` is a qword index, so
      the field is byte `+0xE8`.
      - **Stamping.** Thirteen functions copy the counter into the object's `+0xE8` and then increment it:
        `006316C0`…`00632780` (ten), `00632C90`, `00632D80` and `00636280`. The first is typical: read `006317D9`, store
        `006317DF`, increment `006317EC`, and `+0xEC = −1` at `006317F8`.
      - **Release.** The shared base destructor `00633390` computes `+0xE8 + 1` and, **only if that equals the counter**,
        decrements it (`006333BF`–`006333D3`). So an id is reclaimed only when the most recently numbered descriptor dies,
        and the counter otherwise stays a high-water mark.
      - **Consumer.** `00638AE0` (called from `005A08E0`) is the counter's one reader outside the constructor and destructor
        family. It allocates `counter + 1` 24-byte entries (`00634350`), indexed by id with a spare root entry at `counter`,
        and walks the registry list (`006373D0` → `+0x10`, node at descriptor `+0x50`). For each descriptor it records
        itself, its base's id (base pointer `+0x78`), its depth, and a descendant count on every ancestor. A breadth-by-depth
        pass then writes each descriptor's **pre-order index into `+0xEC`**, so a class's descendants occupy the indices
        right after its own: the interval numbering an `isKindOf` range test uses. The pass stores the total in `02CF8264`
        (`00638C40`). Which caller tests those intervals was not traced.
      
      The `+0x1D` row in §4's table is this id, not a registration generation.

      ### How a descriptor gets into that list — 2026-09-21 (FABLE)

      The walk above was read; **the insertion was not**. `00639160(registry, descriptor)` is it, and
      it has three properties worth having.

      **Registration is by name, and the list is name-unique by construction.** It takes the class
      name from `descriptor+0x30` and calls `0063BA10(registry, name)` — the string-keyed record
      lookup [the cluster-header page](../Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md)
      already names. The **same** descriptor under that name means already registered and the call
      returns; a **different** one raises `005CDAA0(2, 00D58870, name)` (`00639192`–`006391AD`); only
      *not found* inserts.

      ***The insert is base-adjacent.*** If `descriptor+0x78` — the base — is non-null **and that
      base's `+0x70` is the same registry**, the node at `descriptor+0x50` is spliced in next to the
      **base's** node (`00639208`–`0063922C`); otherwise it is linked at the **head** of the
      registry's list (`0063922E`–`00639244`). So the list is ordered with a derived class sitting
      next to its base. *Bounded, because the obvious consequence is not there:* `00638AE0` does
      **not** depend on that order — it rebuilds each class's depth from the base pointer `+0x78`
      — so this is a property of the list, not a correction to its one documented reader.

      ***And a registry publishes itself lazily.*** `rbp` holds the list's first entry **before** the
      insert and is zero when the list was empty (`006391C6`–`006391D7`). When it was empty, and this
      registry is not the one `006373D0()` returns, the registry links **itself** — through its own
      `+0x00` / `+0x08` node — into a list at `006373D0()+0x28` (`0063924C`–`00639277`). **A registry
      appears in the global chain only once it has a member.** A reimplementation that builds a
      registry and registers nothing into it gets a registry that is never reachable, silently.

      The **mode** at registry `+0x20` selects diagnostics: `1` calls `0063E410(descriptor)`; `2`
      also emits `005CDAA0(1, 00D588B8, name)` before it; any other value skips both
      (`006391D4`–`006391FF`).

      **A transcription fix on the sibling page, and it matters to `UQ-293`.** The finaliser
      `00639450` re-runs **exactly** the constructor's initialisation of the descriptor's `+0x08`
      block: `[+0x08] = [+0x10] = [+0x18] =` the address of `+0x08`, `u32 [+0x20] = 0`,
      `ptr [+0x28] = 0` — **five stores**, of which
      [the member-registration page](member-registration-and-the-recovered-field-schema.md)'s excerpt
      shows two. So `+0x08`–`+0x28` is **one initialisation unit**, not a bare list head, which is
      what that excerpt invites. ~~***`UQ-293`'s "what the `+8` list holds" is still open*** — what
      would settle it is an insertion site that adjusts a node pointer **by 8**, the way
      `lea rbp, [rax-0x50]` does for the registry list here. I did not find one.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **UQ-293** was answered on 2026-09-21. The `+8` block is the descriptor's membership record in a global by-name container: registration hashes the class name and, on a miss, writes the hash to `+0x20` and the name pointer to `+0x28` before inserting `descriptor + 8`.*
- [x] ~~The full `PClassDataMember` layout — the type and offset fields a modder would most want.~~
      **Q-3 ANSWERED — reconciled 2026-09-12 (FABLE):** the layout was recovered from the constructor
      on the sibling page and never carried back here:
      [`member-registration-and-the-recovered-field-schema.md`](member-registration-and-the-recovered-field-schema.md)
      §4 — `+0x20` name pointer, `+0x28` attribute bitfield, **`+0x30` `PType *` (the type)**,
      **`+0x48` the field offset inside the owning object**, `+0x18` the owning descriptor, two
      intrusive lists at `+0x08` / `+0x38`. **Q-3.**
- [x] What `Reflection.ObjectTraversal` (`0063E2E0`) traverses; the decompilation is incomplete
      (see §8). **Q-4.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (Q-4), read from the disassembly:* **it
      walks an object's reflected data members to convert their byte order in place.**
      - **The walk.** `0063E2E0(descriptor, object, flag)` builds a context {0, the instance size `+0x38`, object, flag}.
        For the class and then each base through `+0x78` (`0063E351`) it walks the **field list `+0x80`**, forwards when
        `flag` is set (`0063E310`) and backwards when it is clear (`0063E370`). It hands each field to `0063CE80`.
      - **Each field.** `0063CE80` asks the field for its type (field slot 1), skips fields by flag bits `+0x28`, and
        computes the field's address as `object + field +0x48 − owner +0xF4`. Array or pointer kinds (type `+0x5C`) get
        their count and address from type slots 4 and 7. It then calls `0059FDB0(type, address, count, flag)`.
      - **Each element.** `0059FDB0` steps through the elements by the type's size `+0x38` and calls **type vtable slot 0**
        on each.
      - **What slot 0 does.** For the scalar type objects it is a byte swap in place:
        - `PUInt32` (`00D311B0`) → `005CB140`: `mov eax, [rdx] ; bswap eax ; mov [rdx], eax`;
        - `PInt32` → `0063E050`: the same by shifts;
        - `double` → `0063E0D0`: eight bytes reversed;
        - `bool` → `0061ECF0`: `mov al, 1 ; ret`, since one byte has nothing to swap.
      - **What recursion reaches.** A class-typed field recurses, because a class descriptor's slot 0 calls back into
        `0063E2E0`, so the whole object graph is converted. Of the 331 `Concrete<T>` vtables, 243 have one of the 298
        traversal adapters as slot 0 and 88 share `0062AF80`, which calls `0063E2E0` too. `ForType<T>`'s non-adapter
        `0062ADF0` does the same.
      - **Why it exists.** The cluster loader accepts big-endian `PHYR` files and records that it swapped the header
        ([cluster header contract](../Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md)).
      
      **Not established:** which of the two list orders serves which direction (load or save), and the call path from the
      big-endian flag to these walks. `0059FDB0`'s other callers are `0059C5E3` and `0059D674`.
- [x] ~~The difference between `PClassDescriptorConcrete<T>` and `PClassDescriptorForType<T>`.~~
      **ANSWERED 2026-09-08, §11.** `ForType<T>` is the common base: **392 types have both, 0 have a
      leaf form without a `ForType<T>`**, and 17 have only a `ForType`. The leaf form says how the
      type may be constructed. **Q-5.**
- [x] ~~Why `PClassDescriptorForType` needs both a `DeletingDestructor` family (1,054) and a
      separate `DestructorThunk` family (352).~~ **ANSWERED 2026-09-13 (FABLE), §15:** different consumers. The 1,149 deleting
      destructors are vtable slot 7 (0 direct callers, one qword reference each). The 384 thunks are in no vtable, have no data
      reference and **no direct caller** — **no ordinary edge reaches them at all**; what transfers control to each is a tail
      jump from a compiler-generated unwind funclet, and it is those funclets' **instructions** that say when — **315** reload
      the object from the parent frame (`mov rcx, [rdx + 0x60]`), **69** name a static (`lea rcx, [static]`). *Restated
      2026-09-15 under FINAL-AUDIT pass 6: the earlier wording, "are each reached once, by a tail jump from an
      exception-unwind funclet", put the reachability claim on the unwind edge, which is the banned inference. §15's reading
      is unchanged — the 315/69 instruction split is what carried it all along.*
      Normal-exit teardown is the third, inlined family. **Q-6.**
- [x] ~~Whether the RTTI classes and the reflected classes are the same set.~~ **ANSWERED
      2026-09-08, §12 — NO, and neither contains the other.** 409 types are reflected of 2,248 RTTI
      classes, and **only 114 of those 409 (27.9 %) carry RTTI of their own**; the rest are plain
      structs. Reflection here exists to serialise, not to dispatch. (The `2,134` figure is
      superseded — §14.) **Q-7.**

> **Crossing into Platform — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `005A08E0`, the caller named above, also
> records the engine start time. At `005A0A63` it calls a timer and stores the result at `02CB60E8`, a few calls
> before `00638AE0`. The timer is `QueryPerformanceCounter` divided by the frequency held at `02CB6120`, which gives seconds
> as a double; the ledger files it under Platform. The timer has nothing to do with class metadata.
> [The fifteen modules](../Subsystem-Map/the-fifteen-modules-registered-before-main.md) names the walker's other
> platform-layer calls.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `PClassDescriptor` derives from `PType` | `FUN_00633390` assigns `PClassDescriptor::vftable` on entry, `PType::vftable` on exit | 1 |
| One global descriptor per reflected class, built by a static initializer | complete body of `FUN_001603e0` | 1 |
| Initializer and teardown are paired | `atexit(FUN_008a8e20)` — a direct call, not an inference | 1 |
| `PClassDataMember` holds the member name as an embedded string | `FUN_006b6700(self+7)` string destructor in `FUN_00633240` | 1 |
| Descriptors use aligned allocation | `_aligned_free` in `FUN_00584730` | 1 |
| MSVC scalar-deleting-destructor flag convention | `flags & 1` / `flags & 4` branches in `FUN_005847e0` | 1 |
| Family counts | GFZ `CodeDomain` tag census over all 38,161 functions | 3 |
| 2,134 RTTI classes | independent MSVC RTTI walk (`rtti_recover.py`) | 4 |

### A decompiler artifact that must not be mistaken for evidence

Several bodies in this family decompile with **empty `if` and `while` blocks**:

```c
if ((longlong *)param_1[1] != param_1 + 1) {
}
while (plVar7 = plVar6, plVar7 != (longlong *)0x0) {
}
```

Those are not no-ops in the binary — Ghidra dropped the block contents, typically at tail calls.
**No claim in this document rests on an empty block.** `Reflection.ObjectTraversal` (`0063E2E0`)
decompiles to a bare `do { } while(true)` and is therefore recorded as *unread* in §3, not
summarised. *(Read from the disassembly instead, 2026-09-14 — §7 Q-4.)*

### Two identical functions, two different body hashes — proven

`005847E0` and `00584950` decompile to **character-identical C**, including the same
`PClusterHeaderBase` vftable and the same three calls. Their 92-byte bodies were extracted from
the shipping EXE and compared directly:

```
005847E0  sha256 56195d71c3c39dff...
00584950  sha256 63774d042344beb0...
identical? False    differing offsets: [28, 29, 36, 37, 57, 58, 73, 74]
```

Exactly 8 bytes differ, in four adjacent pairs — the low halves of four rel32 displacements:

| Offset | A | B | delta |
|---|---|---|---|
| `0x1C` | `0xFD40` | `0xFBD0` | `0x170` |
| `0x24` | `0xEB88` | `0xEA18` | `0x170` |
| `0x39` | `0xFF13` | `0xFDA3` | `0x170` |
| `0x49` | `0x8E73` | `0x8D03` | `0x170` |

Every delta equals `0x170` — precisely the distance between the two function addresses. No
opcode or immediate differs.

**Consequence, and it is a methodology finding rather than trivia: a body-bytes SHA-256 cannot
identify clones.** Any two copies of the same source at different addresses hash differently
whenever the body contains a relative call or a RIP-relative reference — which these all do.
Deduplicating this database by body hash would silently undercount duplication. This is why the
evidence hierarchy carries a distinct *exact-body clone* tier rather than folding it into hash
equality.

## 9. Related

- [`../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md) — the 1,219 binding stubs that consume these descriptors
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the clone tier this section justifies
- [`../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) — the consumer: asset load matched against type descriptions

## 9. Falsification pass 2026-09-02

**Attack chosen.** Two claims here are exactly checkable, so both were recomputed from scratch
rather than re-read: the headline count of **4,557** reflection functions, and the byte-level clone
proof in §8, which asserts *"exactly 8 bytes differ"* with a stated delta.

### SURVIVED exactly: the 4,557 count

Summing every distinct `GFZ.V121.CodeDomain.Phyre.Reflection.*` component across all 38,161
functions gives **4,557** — matching the headline to the unit. The census also shows **4,557 tag
instances across 4,557 distinct functions**, so no function is double-counted through multiple
reflection tags, which the raw sum alone would not have ruled out.

### CORRECTED: the family breakdown misfiles 256 functions

The *total* is right; the *split* is not. Eight of the ten named families are undercounted, always
in the same direction, and the shortfall is absorbed by the `(remaining)` row:

```
ten named families   document 3,730    census 3,986    +256
(remaining)          document   827    census   571    -256
total                document 4,557    census 4,557       0
```

**The direction is the diagnostic.** Eight families low, two exact, none high. A counting-method
difference would scatter in both directions; a one-sided shortfall that the remainder exactly
absorbs means the family rows and the total were **produced by two different queries**, and only the
total was checked. The corrected table is in §2.

This is the third time in this database that a recorded figure has disagreed with a fresh
derivation. The other two — a 14-minute-stale export, and audit markers mistaken for code-domain
tags — both resolved in favour of the recorded figure. **This one resolves against it**, which is
why each such disagreement has to be chased rather than assumed either way.

### SURVIVED exactly: the eight-byte clone proof

`005847E0` and `00584950` were re-extracted from the shipping EXE and compared byte by byte.
Differing offsets: **28, 29, 36, 37, 57, 58, 73, 74** — identical to the recorded set, four adjacent
pairs, no opcode or immediate among them.

One clarification on direction. The table reads the delta as `A - B = 0x170`. Taken as
`B - A` the value is **-0x170**, and the sign is the point: the *later* function's rel32
displacements are **smaller** by exactly the distance between the two functions, which is what it
means for both to point at the **same absolute target**. The identical relationship was found
independently on 2026-09-02 in
[`../../99-Unresolved-Residual/the-unresolved-158.md`](../../99-Unresolved-Residual/the-unresolved-158.md)
§8b, where two 7,440-byte functions `0x7810` apart carried 395 displacement fields all shifted by
`-0x7810`.

### EXTENDED: there is a third clone, and it is not identical

§3 lists `005847E0`, `00584950` **and `00584A40`** as one family, but §8 proves only the pair.
`00584A40` is also 92 bytes and differs from `005847E0` at **the same eight offsets** — but not by
the same amounts:

| Offset | delta (`00584950`) | delta (`00584A40`) | |
|---|---:|---:|---|
| `+0x1C` | `-0x170` | **`-0xB0`** | **different target** |
| `+0x24` | `-0x170` | `-0x260` | same target |
| `+0x39` | `-0x170` | `-0x260` | same target |
| `+0x49` | `-0x170` | `-0x260` | same target |

`0x00584A40 - 0x005847E0 = 0x260`. Three of the four displacements shift by exactly that distance,
so those three calls resolve to the same absolute targets. **The fourth does not**: at `+0x1C` the
shift is `-0xB0`, so that call site points somewhere else. `00584A40` is the same generated shape
bound to a **different function at one site** — a near-clone, not a clone.

### The method this yields

The comparison generalises into a usable instrument, and it is the constructive counterpart to §8's
finding that a body hash cannot identify clones:

```
for each differing displacement field between two same-size functions A and B:
    delta == -(addr(B) - addr(A))   ->  both reference the SAME absolute target
    delta != -(addr(B) - addr(A))   ->  this site differs; it is where the two functions diverge
```

A body hash says only "different". This says **which call sites differ and which do not**, using
nothing but the two bodies and their addresses. It found the divergent site in `00584A40`
immediately, and the same test isolated the two informative bytes among 1,228 in the residual
twins.

---

## 10. `0063BC00` — the most-called undocumented function in the game (2026-09-08)

**373 call sites in 369 distinct functions, and until now not one document named it.** It was found
by asking the new knowledge index for *the highest-connectivity callee that no document cites*:

```sql
SELECT e.callee, COUNT(DISTINCT e.caller) FROM edges e JOIN functions f ON f.entry = e.callee
 WHERE e.caller_is_eh = 0 AND f.is_generated = 0 AND f.thunk != 'true' AND f.body_bytes > 40
 GROUP BY e.callee
HAVING (SELECT COUNT(*) FROM citations c WHERE c.resolved_entry = e.callee) = 0
 ORDER BY 2 DESC
```

It is 112 bytes, and it is read in full:

```asm
0063BC00  cmp   qword ptr [rcx + 0xd8], 0
0063BC11  jne   0x63bc63                    ; -> return self->+0xD8, already resolved
0063BC13  mov   eax, [rcx + 0xfc]           ; the flags word
0063BC1B  js    0x63bc3d                    ; bit 31 set -> skip preparation entirely
0063BC1D  bt    eax, 0x1e
0063BC21  jb    0x63bc29                    ; bit 30 set -> the virtual prepare already ran
0063BC23  mov   rax, [rcx]
0063BC26  call  qword ptr [rax + 0x60]      ; vtable slot 12: prepare
0063BC29  xor   edx, edx / call 0x639a60    ; (self, 0)
0063BC33  xor   edx, edx / call 0x639c80    ; (self, 0)
0063BC3D  mov   rcx, [rbx + 0xc0]           ; the base pointer
0063BC47  je    0x63bc63                    ; base NULL -> return +0xD8, which is 0 here
0063BC49  or    dword ptr [rbx + 0xfc], 0x20000000    ; bit 29: "handed out"
0063BC53  movsxd rax, dword ptr [rbx + 0xf8]          ; a SIGNED 32-bit offset
0063BC5A  add   rax, rcx
0063BC62  ret                               ; -> base + offset
```

```c
void *ClassDescriptor_Resolve(PClassDescriptor *self)
{
    if (self->resolved_D8) return self->resolved_D8;      /* already a real pointer */
    uint32_t f = self->flags_FC;
    if (!(f & 0x80000000)) {                              /* bit 31 = do not prepare */
        if (!(f & 0x40000000)) self->vtbl->slot_0x60(self);   /* bit 30 = prepare done */
        Sub_639A60(self, 0);
        Sub_639C80(self, 0);
    }
    void *base = self->base_C0;
    if (!base) return NULL;
    self->flags_FC |= 0x20000000;                         /* bit 29 = pointer handed out */
    return (char *)base + (int32_t)self->offset_F8;       /* SIGNED */
}
```

**This is the getter for the class's DEFAULT OBJECT, built on demand.** The control flow above is
read correctly and is unchanged; what was wrong was the name on `+0xC0`.

> **CORRECTED 2026-09-19 (OPUS).** This paragraph used to read *"lazy resolution of a descriptor to
> a real address ... an object loaded from a cluster is known as base + signed offset until
> somebody asks for it"*. `+0xC0` is not the block the descriptor lives in. It is the class's
> **default buffer**, and that is the engine's own term for it, printed at `00D584A0`:
> *"Class '%s' has a position dependant constructor and should be marked as having no default
> constructor to avoid usage of the default buffer"*. What `0063BC00` returns is a pointer to a
> default-constructed instance of the class, adjusted by the signed `+0xF8` so it points at the
> sub-object rather than the allocation. `+0xD8` really is an override checked first, and that
> part stands.

So `Sub_639A60` in the pseudocode is not "preparing a cluster": it is **building the default
object**, and it is the reason the call is guarded by bit 31 — the buffer only has to be built once
per class. `+0xF8` is the same signed adjustment `0063C910` applies in the other direction when it
copies the buffer into a new instance (`rbx = instance - [desc+0xF8]`), which is what makes the two
readings one mechanism instead of two.

### `00639A60` — building the default buffer, once per class

`00639A60` is called only from `0063BC00` above and from `0063C910`, the function that gives every
new Phyre object its initial bytes. Both call it with the descriptor and both skip it when flags
bit 31 is already set; `00639A60` **sets that bit itself, at its own exit** (`00639C55`), so the
work below happens exactly once per class and every later instantiation is just the copy.

```
00639A66  rax = [desc+0xC0]                 ; the default buffer; NULL -> nothing to do
00639A79  rcx = [desc+0xC8]                 ; the second buffer;  NULL -> nothing to do
00639A8E  ebx = [desc+0xFC] ; js out        ; bit 31 -> already built
00639AA7  esi = [desc+0xF8] ; r12 = rax+esi ; the adjusted instance pointer
00639AB6  if (flags & 1)  -> 0063CB80 only, then set bit 31 and return
00639AD8  memset([desc+0xC8], 0xA5, [desc+0x38])
00639AEC  memset([desc+0xC0], 0xA5, [desc+0x38])
00639AF1  if (flags & 2)  -> set bit 31 and return          ; the two buffers stay 0xA5
00639B20  al = vtbl->slot_0x50(desc, [desc+0xC8])           ; default-construct into buffer 2
00639B25  if (!al) -> 0063CB80 BUILDS IT ANYWAY, then bit 31 ; false only on the 19 stub classes
00639B2C  if (flags & 8)  -> skip to 00639B7B               ; without a default ctor: no compare
00639B3E       vtbl->slot_0x50(desc, [desc+0xC0])           ; default-construct into buffer 1
00639B52  if (memcmp([desc+0xC8], [desc+0xC0], size))       ; the two must agree BYTE FOR BYTE
00639B6A      printf("Class '%s' has a position dependant constructor ...", [desc+0x30])
00639B78  vtbl->slot_0x58(desc, r12)                        ; destruct the buffer-1 object
00639B8C  memcpy([desc+0xC0], [desc+0xC8], size)            ; buffer 2's bytes become the default
00639B9A  vtbl->slot_0x58(desc, r15)                        ; destruct the buffer-2 object
00639BA9  for each registered member (the list at desc+0x80):
00639C2D      memcpy(r12 + member->offset_48 - [owner+0xF4], <member type's default>, size_38)
00639C55  flags |= 0x80000000
```

**Constructing the same class twice at two addresses and requiring the bytes to match** is what the
two buffers are for: any byte that differs is one the constructor derived from the object's own
address, and such a class is told to opt out of the mechanism. The third buffer `+0xD0` is
registered by the same family and **no reader of it is identified here**; it is left open rather
than assumed to be a third construction.

### Every bit ever set on a descriptor's `+0xFC`, and the one that never is

**2026-09-19 (OPUS),** from `Tools/analysis-kit/gfz-scripts/scan_descriptor_flag_bits.py`. The
question was narrow: `PCluster::create` tests `[desc+0xFC] & 8` at `0063A99A` and, when set,
refuses to allocate and prints *"Class '%s' has no default constructor and cannot be allocated
with PCluster::create()"* (`00D58750`). RTTI marks **35** of the 315 classes
`PClassDescriptorWithoutDefaultConstructor` or its `Header` variant. **Is bit 3 how that mark
reaches the runtime?**

**An image-wide sweep cannot answer it.** Scanning every `mov`/`or` on a `[reg+0xFC]` operand
reports bit 3 set at **18 sites**, and every one is an unrelated structure that also has a field
at that displacement — attribution by displacement, with no tie to the type, which is exactly
what addendum `bw` exists to name. So the census below is **tied**: it reuses the descriptor
taint, seeding registers provably holding a known descriptor and propagating through moves,
spills, pointer arithmetic and argument slots to a fixpoint before looking at `+0xFC` at all.

| bit | sites | set by | meaning |
|---|--:|---|---|
| **1** | 315 | every class's own descriptor constructor | short-circuits `00639A60` at `00639AF4` |
| **27** | 1 | `00639EEF`, inside `00639C80` | layout-validation result |
| **28** | 1 | `0063A0E2`, inside `00639C80` | layout-validation result; `00639CB4` clears **27 and 28 together** at entry |
| **29** | 1 | `0063BC49` | the default-object pointer has been handed out |
| **30** | 1 | `00639465` | members registered — the `+0x60` vcall is skipped when set |
| **31** | 1 | `00639C55` | the default buffer has been built |
| **3** | **0** | — | **never set on any descriptor-tied path** |

> **CORRECTED 2026-09-25 (OPUS) — bit 3 IS set, by 35 static initialisers; the tie had a blind spot.** The census seeds
> *registers* holding a descriptor, and every class's static initialiser edits its descriptor by **absolute address** —
> `and dword [rip→desc+0xFC], ~2`, or `mov eax,[rip→desc+0xFC] ; and/or eax,… ; mov [rip→desc+0xFC], eax` — with no
> register holding the descriptor at all. `scan_descriptor_flag_rip.py` attributes those accesses exactly, because the
> 315 static descriptor objects are known: **298 initialisers** edit the word (260 in place, 38 through `eax`), and the
> per-template edits are the table in "The table the object carries" above: **bit 1 cleared on all 298, bit 3 set on
> 35, bit 2 set on 4.** The same sweep finds **27 `or` writes in 26 member registrars** setting **bit 4** (`0x10`, the
> three `Header` classes' registrars) and **bit 5** (`0x20`, 24 classes) — two bits this table never listed; their
> meaning is NOT CLAIMED. The tied census stands for what it measured; its silence on bit 3 was the instrument's.
>
> *2026-09-26 (FABLE, Claude Opus 5.5), from `NS-1`:*
> - **The packed-namespace class word `w7` is a file copy of this word's low byte.** 115 of 115 joined classes
>   agree on bits 1–3, and bit 4 sits on exactly the `Header` classes.
> - **Bits 4 and 5 have no reader that was found.** Image-wide, no instruction isolates either bit of a `+0xFC` word
>   in the reflection or loader code, directly or after a load. Control: the same sweep finds `PCluster::create`'s
>   bit-3 test.
> - Their meaning therefore stays NOT CLAIMED, and there is no use in this build to claim it from. See
>   [`ns1_w7_flags.py`](../../_index/candidates/ns1-class-word-w7/ns1_w7_flags.py).

**Controls:** the census must find the four flag writes already established here — bit 1 in the
constructors, bit 29 at `0063BC49`, bit 30 at `00639465`, bit 31 at `00639C55`. All four found.
A census that missed them would say nothing by staying silent on bit 3.

**It also corrected a figure the untied sweep gave.** Image-wide, bit 30 looks set at two sites,
`006363E0` and `00639465`; only the second is descriptor-tied.

### Two questions closed with negatives

**Where a Phyre class's constructor is — not here.** The `ctor` cell is empty for all 315 of
these classes in `_types/types.tsv`, and this is what a search for it found, recorded so nobody
repeats it:

* **`PCluster::create` calls no constructor.** It computes `size × count` from `[desc+0x38]`,
  bump-allocates through `00639510`, takes `[rax+0x58]` as the base and then calls `0063C910`
  once per instance — which adjusts by `[desc+0xF8]` and `memcpy`s the default buffer in. That is
  the whole creation path.
* **The function-class map does not supply one either.** Of the 315, every class has 3–16 bodies
  on its `installs` route, but almost all of them install a *descriptor* template instantiation.
  Filtering to bodies that install the **class's own** vtable, and excluding the descriptor
  constructor, the known destructor and anything that also sits in a vtable slot, leaves a
  candidate for only **44** classes — and at least one candidate (`005A9480`) is shared between
  `PAnimatableComponent` and `PAnimationTargetBlenderController`, so even those are not per-class.

**So the cells stay empty.** Two thirds of these classes are non-polymorphic and have no vtable to
install, which is consistent with there being nothing to find by this route; but "consistent with"
is not evidence, and 315 cells asserting an absence this search cannot establish would be worse
than 315 empty ones.

**Why 69 descriptor constructors have no class name, and why they never will.** How `r8` is set
at the descriptor-constructor call splits the 384 with no exceptions:

| | how the name reaches `r8` | classes |
|---|---|--:|
| **315** | `lea r8, [rdata]` — a static string | recoverable |
| **69** | `mov r8, [rip+X]` — a pointer loaded from a **`.bss` global** | not in the image |

Those globals are zero in the image and the same body lazily fills them from a runtime value:
`005B4E00` loads `02CB5BC8`, tests it, `cmove`s in a register computed earlier and stores it back
at `005B4F3F` — **the only writer of that global in the image.** The size is computed too
(`lea r9d, [r15+0x10]` with `r15` zeroed). **The control** is a backward-scan recovery written
specifically to reach them: it reproduces all 315 named rows exactly, 315 agree and 0 disagree,
and recovers none of the 69. An instrument that reproduces everything it should and still cannot
see these is telling you something about them, not about itself.

### And the reads: only three bits are both written and read

**2026-09-19 (OPUS),** `scan_descriptor_flag_reads.py`, the same tie and the same boundary. Five
previously established reads are the control — `0063A99A` (bit 3), `0063C93D`/`0063C941` (31, 30),
`0063BC19` (31), `00639AB6` (0) — and all five were found. The complete descriptor-tied read set
is eleven instructions in six functions.

| bit | written | read | verdict |
|---|---|---|---|
| **0** | ~~never~~ **`00632F18`**, in the `PClassDescriptorDynamic` constructor `00632E80` (2026-09-25) | 3 sites | **live** — a runtime-built descriptor sets it and calls `00639A60` at once, which takes this arm to `0063CB80`; the tie did not seed that constructor's `rsi` |
| 1 | 315 constructors; **cleared by 298 static initialisers** (2026-09-25) | 3 sites | live — carried by the 17 abstract classes |
| **3** | ~~never~~ **35 static initialisers** (2026-09-25) | 3 sites | **live** — `PCluster::create`'s refusal is armed for the 35 classes without a default constructor |
| **27** | `00639EEF` | **never** | **write-only** — the layout validation's answer, discarded |
| **28** | `0063A0E2` | **never** | **write-only** — the same |
| **29** | `0063BC49` | **never** | **write-only** — *"pointer handed out"*, nobody asks |
| 30 | `00639465` | 2 sites | live |
| 31 | `00639C55` | 3 sites | live |

*(2026-09-25: the next sentence leaned on the `+0x50` stub, which was the Abstract table's. Bit 0 IS set - by `PClassDescriptorDynamic`'s constructor `00632E80` at `00632F18`, which then calls `00639A60` itself - so the bit-0 arm serves runtime-built descriptors; for the 315 static descriptors no write sets it, and `00639AB9` falls through into the construct-and-compare arm for 263 of them.)* ~~**Bit 0 being read but never set independently confirms** what the `+0x50` stub already implied:~~
`00639A60` always takes the `je` at `00639AB9` into the memset path, so `0063CB80` always builds
the buffer. Two unrelated measurements, the same conclusion.

**Bits 27 and 28 are the fourth disarmed arm.** `00639C80` — 1,160 bytes, recursing through the
whole base chain, memsetting the third buffer and comparing — computes a result that **nothing
reads**. The work happens; the answer goes nowhere.

**Bit 29 is a fifth**, and a smaller one: `0063BC00` records that it has handed out the default
pointer, and no code consults it.

> *(2026-09-25: the construct-and-compare arm and the bit-3 refusal are ARMED — see the corrections above. What survives of this block is bits 27, 28 and 29: computed, and read by nothing.)* **The validation half of this system is disarmed at both ends.** The arms that would *report*
> are unreachable because their bits are never set; the results that *are* computed land in bits
> nobody reads. What still runs is the object-making half: the default buffer, the `memcpy` at
> `0063C974`, member registration.

### Three arms of this machinery are compiled in and disarmed in this build

> **WITHDRAWN 2026-09-25 (OPUS): all three arms below are ARMED.** Each row's reason was measured on the Abstract base
> table or by a census blind to absolute-address writes: `+0x50` constructs and returns 1 on 263 classes with bit 3 clear,
> so `00639A60` constructs twice and compares, and the diagnostic at `00D584A0` fires if the bytes differ; and bit 3 is set
> on 35 classes, so `PCluster::create` refuses them. **A reconstruction DOES have to reproduce both.** Whether any class
> in this image actually trips the diagnostic is a runtime question, not asked here. The table and its paragraphs are kept
> as written, struck through where they are wrong.

This is the pattern the bit-3 negative completes, and it is worth stating as one thing rather
than three:

| arm | why it cannot run |
|---|---|
| `00639A60`'s **construct-and-compare** — build the class into two buffers and `memcmp` them | ~~vtable `+0x50` is the same `xor al,al; ret` stub on all 315, so the `false` branch is always taken~~ — the Abstract table's value; ARMED |
| the **"position dependant constructor"** diagnostic (`00D584A0`) | ~~it is inside that arm~~ — ARMED with it |
| `PCluster::create`'s **"no default constructor" refusal** (`00D58750`) | ~~bit 3 is never set~~ — set by 35 initialisers; ARMED |

All three are the **validation** half of the reflection system: the part that checks a class is
well-behaved rather than the part that makes objects. The object-making half — the default buffer
built by `0063CB80`, the `memcpy` at `0063C974`, the member registration — runs normally.

**Two consequences.** ~~A reconstruction does not have to reproduce the validation half.~~ *(Withdrawn 2026-09-25: it does.)* And — the
harder one, learned by getting it wrong — **a property must not be inferred from an arm that
never runs.** The retraction above did exactly that: it read "no class has a default constructor"
off a slot whose return is a constant in this build. A constant return tells you the arm is dead;
it tells you nothing about the classes.

### `+0xD0` has a reader

Recorded this morning as *"registered by the same family and no reader of it is identified"*.
`00639C80` — the function both `0063C910` and `0063BC00` call immediately after `00639A60` —
null-tests `[desc+0xD0]` at `00639CA6`, `memset`s it at `00639CE4` and uses it alongside `+0xC8`
through the comparison that follows. So the third buffer is the layout validation's own, and
bits 27–28 are where its answer lands.

`00639C80` also **propagates flags up the inheritance chain**: it recurses into the parent's
`00639A60` and `00639C80` (`00639F21`/`00639F2B`, `00639F5A`/`00639F64`) and then ORs the
parent's whole `+0xFC` into the child's at `00639DB0`. What it validates is not claimed here.

### `0063CB80` — the same buffer, built without a constructor

`+0x50` returns **false on every class measured**, so `00639A60` always hands off to `0063CB80`
rather than giving up. (*What the false means is not what this page first said — see the
retraction under the slot table.*) That function builds the same buffer out of inheritance
and registration instead of construction:

```
0063CBA0  r12 = [desc+0xC0] + [desc+0xF8]        ; the adjusted buffer pointer
0063CBAA  rdi = [desc+0x78]                      ; THE PARENT DESCRIPTOR
0063CBB6  rbp = 0063BB10(parent)                 ; ... and the parent's own default object
0063CBF8  memcpy(r12 - parent->offset_F8, rbp, min(parent->size_38, ...))
0063CBFD  for each registered member (the list at desc+0x80):
0063CCD9      memcpy(r12 + member offset, <member type's default>, size)
```

So the buffer is built without ever running a constructor: **its parent's default object,
then every registered member's default on top, and `0xA5` everywhere else.** Everything the two
memsets poisoned and neither the parent nor a registered member covers stays `0xA5`. That is a
reading of the code, not a measurement of the bytes — `AQ-17` is queued to read one, and its
first target is `PDeferredLightingBase`, whose vtable `+0x50` is `00657140`, three bytes of
`xor al, al; ret`.

The per-member copy at the end of `00639A60` is the part that matters to a field map: each registered member's
slot in the default object is overwritten with **that member type's own default object**, fetched
through `0063BB10` → `0063BC00`, at `member->offset_48` minus the owning class's `+0xF4`
adjustment. So a class's default bytes are its constructor's output with every registered member's
default layered on top.

### The three buffers, and the vtable slots that use them

`0063DC80`, `0063DF90` and `0063DFA0` are three consecutive one-instruction setters —
`mov [rcx+0xC0], rdx`, `mov [rcx+0xC8], rdx`, `mov [rcx+0xD0], rdx` — and **each is called from the
same 384 descriptor constructors**. The descriptor constructor nulls all three first
(`00632E16`/`1D`/`24`), so they are one family. The full inventory — class, registered instance
size and all three buffer addresses, each read from the class's own constructor body — is
[`members/phyre-class-default-buffers.tsv`](members/phyre-class-default-buffers.tsv), 384 rows.
`members/phyre-default-instances.tsv` covers 173 of those classes and agrees with it on every
`+0xC0` address.

| vtable slot | what it does | how it was established |
|---|---|---|
| `+0x50` | **the class's placement default constructor**: `if (rdx) T::T(rdx); return 1` (`PDeferredLightingBase`: `0063F9A0` → `006458A0`). The `xor al, al ; ret` stub `00657140` only on the 17 abstract classes and 2 without a default constructor. *Corrected 2026-09-25 — this cell said "the same stub on all 315", read from the Abstract base table; see "The table the object carries" below* | called twice by `00639A60` with the two buffers |
| `+0x58` | destruct an instance at a given address | called on both constructed objects after the comparison |
| `+0x60` | register the class's members | for `PDeferredLightingBase` the slot holds a thunk to `006488A0`, **the exact caller `phyre-field-schema.tsv` already records** for that class's eight members |

The `+0x60` row is an independent tie rather than a restatement: the field schema recovered
`006488A0` by walking the member registrar's callers, and the vtable was read from
`00644330`/`00644337` in the descriptor constructor. Neither derives from the other. (`+0x60` is
one of the slots the base and derived tables share, so the re-key below does not move it.)

### The table the object carries — re-keyed 2026-09-25 (OPUS)

**Every descriptor vtable this page reported before 2026-09-25 was the BASE CLASS's table.** The
descriptor constructor this page reads — `006442E0` for `PDeferredLightingBase`, whose `lea` at
`00644330` the row above cites, and one per class — is the constructor of
`PClassDescriptorAbstract<T>`. It stamps the Abstract
table and sets `+0xFC` bit 1. **The descriptor object's own table is stamped after it returns**, by
the class's one static initialiser, in MSVC's derived-constructor shape:

```
001643F0  lea  rcx, [02D34840]          ; the PDeferredLightingBase descriptor object
001643FB  call 006442E0                 ; PClassDescriptorAbstract<T> ctor: stamps 00D5A4C8, +0xFC |= 2
00164400  and  dword [02D3493C], ~2     ; +0xFC: clear the abstract bit
00164407  lea  rax, [00D5A638]
00164415  mov  [02D34840], rax          ; the object's table: PClassDescriptorConcrete<T>
```

**The RTTI Complete Object Locator at `[vt-8]` settles it without any slot numbering.** Over the
315: the table the constructor stamps is `PClassDescriptorAbstract<T>` on **315 of 315**, and the
table the initialiser stamps is the template RTTI instantiated for the class on **298 of 298** —
`Concrete` 260, `WithoutDefaultConstructor` 34, `Header` 3, `HeaderWithoutDefaultConstructor` 1. The
other **17** (the `ForType-only` rows) are never restamped. They carry the Abstract table and keep
bit 1, and they are the abstract classes. Found answering FABLE on `PAtmospherics`: FABLE's slot 10
(`00640280`) was the Concrete table's, and mine (`00657140`) was the Abstract's.

**On the 298 restamped tables, what moved:**

- `+0x18` and `+0x38` differ on all 298, and `+0x50` on 296.
- `+0x58` differs on 4: exactly the four `Header` classes. Their destroy slot is member-wise
  (`005A3E50`: dispatch the descriptor's `+0x78` over the instance), not `mov al,1; ret`.
- `+0x20`, `+0x28`, `+0x30`, `+0x40`, `+0x48`, `+0x60` and `+0x68` do not move, so every control
  below that joins on those slots stands.

The generator (`gen_phyre_descriptor_vtables.py`) now records the carried table, keeps the old value
as `abstract_base_vtable`, and gains a control **C7**: RTTI names both tables and the flag edit
tracks the restamp, on 315 of 315. **C3 is re-read by hand on the carried table.**

**The initialiser's `+0xFC` edit names three bits by the engine's own template names:**

| carried template | classes | initialiser's edit to `+0xFC` |
|---|--:|---|
| `Concrete` | 260 | clear `0x2` |
| `WithoutDefaultConstructor` | 34 | clear `0x2`, set `0x8` |
| `Header` | 3 | clear `0xA`, set `0x4` |
| `HeaderWithoutDefaultConstructor` | 1 | clear `0x2`, set `0xC` |
| `Abstract` (never restamped) | 17 | none — bit 1 stays set |

So **bit 1 = abstract, bit 2 = header, bit 3 = without a default constructor**. Bit 3 is the bit
`PCluster::create` tests at `0063A99A`, and the bit `00639A60` tests at `00639B2C` to skip the
compare.

### The descriptor vtable, measured across every class that has one

Reading the vtable out of all 384 descriptor constructors (315 yield both a class name and a
vtable from a straight-line read), then following each to the table its static initialiser stamps,
turns the three rows above into a distribution, in
[`members/phyre-class-descriptor-vtable.tsv`](members/phyre-class-descriptor-vtable.tsv). *Figures
re-measured 2026-09-25 on the carried table. Where the Abstract table gave a different figure, it
is struck through.*

| slot | distinct values over 315 classes | what that means |
|---|---|---|
| `+0x18` | **262** (~~1 — `0063F850`~~, the Abstract table's) | per class on the carried table; not named here |
| `+0x20` | **315** | the class's **script-VM object push adapter** — 297 of the 315 are members of the documented 304-member `object-push-adapters` family, and the size split measured here (21 B ×194, 31 B ×115) is that family's own documented split of 188 and 116 |
| `+0x28` | **315** | the class's **object-pointer accessor getter**: 26 bytes, `*out = PObjectAccessor<T>::Get()`. **The strongest tie on this page** — resolve the callee in the accessor page's 747-entry address-to-bound-type table, built from RTTI xrefs and never from a vtable, and **314 of 315 are present with the bound type's leaf name equal to the class name, 0 mismatches** |
| `+0x30` | **315** | the class's **nullable object push adapter** — 287 in the 295-member `nullable-object-push-adapters` family, 16 and 7 in two documented siblings, 5 stubs |
| `+0x38` | **315** | the **descriptor's own deleting destructor**: install a base vtable at `[rcx]`, then `call 00633390`, which this page's sibling already names the `PClassDescriptor` base destructor. **315 of 315** make that call |
| `+0x40` | **1** — `0062EFD0` | `AttachMember`. **The control**: this page's sibling established the same value on **1,186 of 1,187** descriptor vtables by a different route |
| `+0x50` | **267** (~~1 — `00657140`~~) | **the class's placement default constructor**; the `00657140` stub on 19 |
| `+0x58` | **124** (~~121~~) | **destroy an instance** — `00639A60` calls it on both objects it builds. Still not a per-class column: the values are shared thunks selected by *how* the class is destroyed, and what selects between them is below |
| `+0x60` | **315** | the class's member registrar. **The second control**: followed through its thunk it reproduces `phyre-field-schema.tsv`'s `caller` column on **173 of 173** covered classes, **0 disagreements** |
| `+0x68` | **2** — `00660570` × 314 | shared |

> **WITHDRAWN 2026-09-25 (OPUS) — the two blocks below and the paragraph after them were measured
> on the Abstract base table** (see "The table the object carries" above), and their conclusions
> do not survive:
>
> - On the carried table, `+0x50` is a **placement default constructor on 296 of 315**, and the
>   `00657140` stub on 19: the 17 abstract classes, plus `PClassCallableMethodScript` and
>   `PRandomGenerator`, both `WithoutDefaultConstructor`.
> - For the 315 static descriptors, `00639A60` never runs during construction: the Abstract
>   constructor's whole forward call closure, 14 bodies, never reaches it, so it sees the carried
>   table. (`PClassDescriptorDynamic`'s constructor `00632E80` does call it directly, but that is
>   a different descriptor kind with its own table and bit 0 set.)
>
> **Its construct-and-compare arm IS reachable** for every class whose `+0x50` constructs and whose
> bit 3 is clear. That is 263 classes (260 `Concrete` plus 3 `Header`), all of whose `+0x50` bodies
> end `mov al, 1 ; ret`. **The "position dependant
> constructor" diagnostic can fire. `0063CB80` builds only where `+0x50` returns false or flags bit 0
> is set.**
>
> The second block's point, that the template name and not a string near a call states
> default-constructibility, stands. Its supporting claim that "no slot separates the groups" does
> not: on the carried table `+0x50`, and `+0xFC` bit 3, separate them. The blocks are kept as
> written, for the record.

> ~~**`+0x50` is the same three bytes for every one of the 315 classes: `00657140`, which is
> `xor al, al ; ret`.**~~ It is the slot `00639A60` calls to default-construct an object into the
> class's default buffer. ~~It returns false on every class, so that arm is **dead code in this
> build**.~~

> **RETRACTED THE SAME DAY (OPUS).** This block first read the `bool` as *"does this class have a
> default constructor"*, from the wording of the diagnostic string at `00D584A0`, and concluded
> that **no Phyre class has one**. That is wrong. RTTI instantiates a descriptor template per
> class and the template name states exactly that property:
>
> | descriptor template | classes |
> |---|--:|
> | `PClassDescriptorConcrete<T>` | **260** |
> | `PClassDescriptorWithoutDefaultConstructor<T>` | **34** |
> | `PClassDescriptorForType<T>` only — the abstract bases | 17 |
> | `PClassDescriptorHeader<T>` | 3 |
> | `PClassDescriptorHeaderWithoutDefaultConstructor<T>` | 1 |
>
> **260 classes the engine itself calls `Concrete` carry the identical `00657140` stub, and no
> slot in the descriptor vtable separates the two groups** — `+0x18`, `+0x40`, `+0x50` and `+0x68`
> are constant across both. So whatever `+0x50` asks, it is not that question; the engine answers
> that one with a template name, and **35 classes** are the ones marked without a default
> constructor. The per-class value is the `descriptor_template` column of the table.
>
> **A string near a call is a hint about the call. A name the compiler emitted for the type is
> evidence about the type, and where they disagree the name wins.** Everything mechanical
> survives untouched: the stub is measured, the branch is measured, `0063CB80` always runs.

~~Three things follow, and none of them needed a new assumption. The construct-and-compare arm of
`00639A60` is **unreachable in this build**, so the `"position dependant constructor"` diagnostic
at `00D584A0` can never fire. **Every** default buffer is therefore built by `0063CB80` — the
parent class's default object, then each registered member's own default, over `0xA5` everywhere
else. And what was said above about `PDeferredLightingBase`'s 16 KiB staying `0xA5` is not special
to that class: it is the shape of every Phyre default buffer in the image.~~ **Withdrawn
2026-09-25.** The default buffer is built by the class's own constructor, run twice and compared,
for 263 classes; every one of those `+0x50` bodies ends `mov al, 1 ; ret`. The 35 without a default
constructor have bit 3 set and are never compared:

- 24 construct once and return 1;
- 9 are 8-byte tail jumps (`mov rcx, rdx ; jmp <ctor>`) whose return value is the callee's, not
  read here;
- 2 are the stub.

`0063CB80` builds wherever `+0x50` returns false. For the 17 abstract classes it is left
`0xA5`, since bit 1 returns at `00639AF4` before any construction. What was said about
`PDeferredLightingBase`'s buffer staying `0xA5` rested on the stub, and `PDeferredLightingBase` is
`Concrete`, so it is withdrawn too. What the buffer holds after `006458A0` runs is not measured
here.

#### `+0x58`, and what selects between its 124 values (OPUS, re-measured 2026-09-25)

*Re-measured 2026-09-25 on the carried table: the four `Header` classes moved (3 from trivial, 1 from direct) into a fifth, member-wise form. The Abstract-table figures are struck through.*

| form | classes | body |
|---|--:|---|
| **trivial** | **83** (~~86~~) | `0061ECF0` and clones, three bytes: `mov al, 1 ; ret` — nothing to destroy |
| **direct call** | **86** (~~87~~) | `sub rsp ; mov rcx,rdx ; call <D> ; mov al,1 ; ret` — `D` is the class's non-virtual destructor, and those 86 addresses are now in the table's `s58_destroy` column |
| **through the object's own vtable** (~~slot 0~~) | 111 | adjust the pointer (113 of the 114 by `-8`), then `mov rax,[rcx] ; call [rax + 8k]` - ~~`call [rax]` for all~~ slot 0 for the 87 on `0063FC60`, **slot 3** (`call [rax + 0x18]`) for the 23 physics shapes on `0068C4E0`, **slot 2** for `PScheduler` on `00680910` (corrected 2026-09-28, OPUS, `_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py`) |
| **bespoke** | 31 | 43 to 102 bytes, not reduced to one of the three |
| **member-wise** | **4** (new) | the four `Header` classes: fetch a magic static (`006372B0`) and dispatch the descriptor's own `+0x78` over the instance (`005A3E50`, 79 B); `PParameterBuffer`'s `005D18C0` then frees `[inst+0x18]` through `005F03A0`. Counted with *bespoke* by the generator, which reports **35** unreduced |

**The control is a cross-tabulation against RTTI, which knows nothing about descriptors.** Whether
a class is polymorphic is recorded in `Tools/work/rtti/methods.tsv`:

| dispatch form | has an RTTI vtable | has none |
|---|--:|--:|
| indirect, through a vtable slot (~~slot 0~~; 0, 3 or 2 by thunk) | **111** | 0 |
| direct call | 0 | **86** |
| trivial | 0 | **83** |
| bespoke / unreduced | 0 | **35** |

**Every class destroyed through a vtable has one; every class destroyed directly or not at all has
none.** A form read off the thunk and a fact read off RTTI agree on all 315 — once three classes
are held out rather than counted: `PPhysicsRigidBodyBullet` (`00689FC0`), `PSamplerStateD3D11`
(`006132E0`) and `PScriptableComponent` (`0063FC60`) make an indirect call while RTTI records no
vtable for them. The first two are bespoke bodies whose indirect call may not be a destructor
dispatch at all; **the third shares the standard `-8` thunk with 87 others and is the one worth
following.** None of the three is read as virtual.

This is what fills the `dtor` cell for all 315 classes in `_types/types.tsv`, where none of them
had one.

**The four per-class slots are named above, and none of them is named from its position.** Each
join is against an artifact built by a different route: the accessor page's bound-type table
(RTTI xrefs), two adapter-family membership lists, and this page's own identification of
`00633390`. The `+0x28` join is a **name** agreement — the string the descriptor constructor
`lea`s against a table derived from mangled RTTI — on 314 of 315 with nothing disagreeing.

What each slot's four sibling implementations *do internally* is a separate question and is not
claimed here; what is claimed is which class each one belongs to.

### The descriptor object, in bytes

| offset | meaning | anchor |
|---|---|---|
| `+0x00` | vtable | `0016609E`, `0063BC23` |
| `+0x30` | the class name, a C string | `lea r8` at the `00632D80` call; printed by the diagnostics |
| `+0x38` | instance size; the length of every memset/memcpy over the buffers | `00632DB4`, `00639AD2` |
| `+0xC0` | **the default buffer** — a full-size instance every new object is copied from | set by `0063DC80`; built by `00639A60`; copied at `0063C974` |
| `+0xC8` | the **second** construction, compared byte for byte against `+0xC0` | set by `0063DF90`; `00639A79` |
| `+0xD0` | a third buffer registered by the same family; **no reader identified** | set by `0063DFA0` |
| `+0xD8` | resolved-pointer override; non-null short-circuits everything | `0063BC06` |
| `+0xF8` | **signed** `int32` offset from `+0xC0` | `0063BC53` |
| `+0xFC` | flags — **every bit ever set on a descriptor is enumerated below**; bit 31 *the default buffer has been built*, bit 30 *members registered*, bit 29 *pointer handed out*, bits 27–28 the layout-validation result, bit 1 set by every class's own constructor | `0063BC13`, `00639C55`, `00166090` |

### One descriptor per class, built before `main`

```asm
00166080  lea  rcx, [rip + …]        ; -> 02E404B0, in BSS
0016608B  call 0x67e5d0              ; constructor
00166090  and  dword ptr [02E405AC], 0xfffffffd     ; = descriptor + 0xFC, clear bit 1
00166097  lea  rax, [rip + …]        ; -> 00D6DE78, the vtable
001660A5  mov  qword ptr [02E404B0], rax
001660B0  jmp  0x808b90              ; register the destructor
```

`02E405AC − 02E404B0 = 0xFC` **exactly**, which is how the flags field above was anchored rather
than guessed. Walking the RTTI at `00D6DE78 − 8` names the object:

```
vtable 00D6DE78 -> .?AV?$PClassDescriptorConcrete@VPWorldMatrix@Phyre@@@Phyre@@
                 = Phyre::PClassDescriptorConcrete<Phyre::PWorldMatrix>
```

**The descriptor singletons are in BSS, not `.data`** — a raw read of `02E404B0` returns *nothing on
disk*, because the offset is past the section's `SizeOfRawData`. The values above come from the
initialiser that writes them, not from the image.

### What the callers do with it

```asm
; 005CE120 = Phyre::PClassDescriptorWithoutDefaultConstructor<PMeshInstanceAttachPoint>, vtable slot 10
005CE12A  lea  rcx, [rip + …] ; -> 02E404B0   (the PWorldMatrix descriptor)
005CE134  call 0x63bc00
005CE139  lea  rcx, [rip + …] ; -> 02CB6E80
005CE143  call 0x63bc00
005CE148  test rdi, rdi / test rax, rax      ; both must resolve
005CE157  mov  [rbx], rdi / mov [rbx+8], rax / mov dword [rbx+0x10], 0
005CE165  mov  al, 1                         ; -> true
```

A caller resolves **two** descriptor singletons and, if both succeed, writes `{ptrA, ptrB, 0}` into
an out-parameter and returns `true`. **What that triple is for is not established** — `DK-2`.

*Answered 2026-09-14 (FABLE), DK-2:* **the triple is a `PMeshInstanceAttachPoint`, constructed in place.** Slot 10 of
`PClassDescriptorWithoutDefaultConstructor<T>` stands in for the default constructor these classes lack. It resolves, through
`0063BC00`, an object for each reference its real constructor needs. If the out pointer is non-null it constructs a `T`
there, and it returns whether that was possible; a null out pointer only asks. Two sibling bodies prove the reading
because they install the class's **own** vtable in the out buffer:

- `005D6E00`, slot 10 of `WithoutDefaultConstructor<PDynamicMeshInstance>`, resolves the
  `PClassDescriptorConcrete<PDynamicGeometry::PModifierNetworkDynamicMesh>` singleton `02E58060` (vtable `00D812F0`, set by
  `00167330`) and adjusts the result by −8 to a base pointer. It then writes `00D498B0`, whose RTTI is
  `Phyre::PRendering::PDynamicMeshInstance`, to `[out]`, that pointer to `+0x08`, and 0 to `+0x10`.
- `005CE850`, slot 10 of `WithoutDefaultConstructor<PModifierNetworkDynamicMeshInstance>`, does the same and then
  **overwrites `[out]` with `00D498D0`** (RTTI `PModifierNetworkDynamicMeshInstance`), zeroing `+0x10`, `+0x18` and `+0x20`.
  That is an inlined base-then-derived constructor chain.

So `005CE120`'s `{ptrA, ptrB, 0}` is the attach point's fields as its constructor sets them. `ptrA` is the object resolved for
the `PWorldMatrix` descriptor `02E404B0`, `ptrB` the one for `02CB6E80`, and `+0x10` is 0. `02CB6E80` is
`WithoutDefaultConstructor<PMeshInstance>`: its initialiser `00161400` installs vtable `00D3FE70`, and that class's own slot 10
is `005D51C0`. **Not established:** the attach point's field names, what the zero at `+0x10` counts, and which caller invokes
slot 10 (no `[vtable + 0x50]` call site was traced).
Fifteen distinct slot-10 bodies among the 38 classes call `0063BC00`. `PAssetReference`'s `00674BE0` first fetches its
descriptor from `006372A0`. These are the fifteen RTTI-identified callers of `DK-1`. The script is
[`members/wdc_slot10.py`](members/wdc_slot10.py).

> ### A number that matches, and is not yet a finding
>
> `0063BC00` has **369 distinct callers**. The RTTI names **331 `PClassDescriptorConcrete<T>` plus
> 38 `PClassDescriptorWithoutDefaultConstructor<T>` = 369** — the instantiable descriptor forms.
>
> **The equality is exact and it is recorded here as unproven.** The test that would confirm it
> failed to: only **15 of the 369** callers carry an RTTI identity at all, and all 15 are slot 10 of
> `WithoutDefaultConstructor<T>` — 15 of the 38 such classes, not 38 of 38. **A coincidence in two
> counts is a lead, not a mechanism.** `DK-1`.

## 11. `Q-5` answered — `Concrete<T>` versus `ForType<T>`

Section 7 listed *"the difference between `PClassDescriptorConcrete<T>` and
`PClassDescriptorForType<T>`"* as unknown. It is measurable directly from the recovered RTTI:

| form | classes |
|---|---:|
| `PClassDescriptorForType<T>` | **409** |
| `PClassDescriptorAbstract<T>` | 386 |
| `PClassDescriptorConcrete<T>` | 331 |
| `PClassDescriptorWithoutDefaultConstructor<T>` | 38 |
| `PClassDescriptorWrapper<T>` | 15 |
| `PClassDescriptorHeader<T>` | 3 |
| `PClassDescriptorHeaderWithoutDefaultConstructor<T>`, `ForClassDescriptor`, `Dynamic`, `Base`, `PClassDescriptor` | 1 each |
| **all descriptor forms** | **1,187** of 2,248 RTTI classes (52.8 %) |

Taking the distinct `T` of each form and intersecting them:

```
T with PClassDescriptorForType<T>                          409
T with Abstract<T> | Concrete<T> | WithoutDefaultCtor<T>    392
T in BOTH                                                   392
T only in a leaf form                                         0     <-- decisive
T only in ForType                                            17
```

> **Zero types have a leaf descriptor without a `ForType<T>`.** `ForType<T>` is the common base of
> all three leaf forms, and the leaf chosen says how the type may be *constructed* — abstract, plain
> concrete, or concrete without a default constructor. The 17 `ForType`-only types are described but
> never instantiated through a leaf: `Phyre::PBase`, `Phyre::PClassDescriptor` itself,
> `Phyre::PMatrix4`, `Phyre::PMatrix4x3` and 13 more.

**`Q-5` is answered.**

## 12. `Q-7` answered — reflected classes and RTTI classes are *not* the same set

Section 7 asked whether the RTTI classes and the reflected classes are the same set. **They are not,
and neither contains the other.**

| | count | of | share |
|---|---:|---:|---:|
| RTTI classes in the image | 2,248 | — | — |
| distinct `T` reflected (`ForType<T>` exists) | 409 | 2,248 | 18.2 % |
| …of those, `T` **also carries its own RTTI** | **114** | 409 | **27.9 %** |
| …`T` with **no RTTI of its own** | **295** | 409 | 72.1 % |

> **Reflection is not polymorphism.** Nearly three quarters of the reflected types have no MSVC
> TypeDescriptor, because they are plain structs with no virtual functions —
> `CD3D11_BLEND_DESC`, `D3D11_DEPTH_STENCILOP_DESC`, `D3D11_RENDER_TARGET_BLEND_DESC`, and engine
> value types such as `Phyre::PAnimation::PAnimationChannel`. Phyre reflects them anyway, because
> reflection here exists to *serialise*, not to *dispatch*.

**409 is a lower bound**, not a census: a type whose `ForType<T>` descriptor was folded away would
not appear. `Q-7` is answered as far as the instrument reaches, and the direction of the answer —
*not the same set, and reflection is the larger idea* — does not depend on the exact number.

## 13. `00633240` and `006332A0` are byte-identical twins with opposite reachability

Section 3 lists `00633240` as the `PClassDataMember` destructor helper. **There are two of them**,
93 bytes each, and their bodies are identical instruction for instruction — both install the
`PClassDataMember` vtable at `00D580B0`, walk the intrusive list at `+8`, ~~destroy the embedded string
at `+0x38` through `006B6700`~~ **clear the intrusive list at `+0x38` through `006B6700`**, and conditionally free `[+0x18]` when `[+0x20] & 1`.

> **⚠ Corrected 2026-09-14 (OPUS), pass 13 — independent re-derivation.** `006B6700` is a list-unlink
> loop and destroys no string: while `[head] != head` it takes `node = link - 8`, relinks
> `prev->next` and `next->prev`, and **self-links the removed node's `+0x08`/`+0x10` pair**; it frees
> nothing and calls nothing. This page's §3 note already said so — *"a list-unlink loop, not a
> string destructor"* — and the correction had not reached this sentence or the Key-addresses row.

What is *not* identical is how they are reached:

| | `E8` call sites | `E9` tail-jump sites | total |
|---|---:|---:|---:|
| `00633240` | **0** | **703** | 703 |
| `006332A0` | 138 | 194 | 332 |
| | | | **1,035** |

> **`00633240` has zero call sites.** Every one of its 703 references is a tail jump, so an
> `E8`-only reading of the reflection teardown path finds this function unreachable and the pair
> under-counted by **two thirds**. This is the third time in this database that the `E9` instrument
> produced the only correct answer; the [Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md)
> block was the second.

Neither address — nor `0063BC00` — appears as a raw qword anywhere in the image, against a control
that does: `005C5230`, the default widget handler, occurs **2,527** times in `.rdata`. **So none of
the three is in a vtable**, and the deleting-destructor thunks reach the twins by jump, exactly as the
family counts in §2 imply.

## 14. The `2,134` in §2 is superseded

§2 reports **2,134 RTTI classes** and §8 records it as tier-4 evidence. The current recovery reports
**2,248**, and the difference is not growth:

```
classes.tsv.pre-as9a   2,133 rows   names like "$00$0BA::?$SeadObject"
classes.tsv (current)  2,248 rows   names like "Phyre::PClassDescriptorConcrete<class Phyre::PWorldMatrix>"
names common to both     573
```

**Only 573 of the names survive between the two tables.** The earlier run's demangler failed on
about three quarters of the corpus, so the old table was not merely smaller — most of its rows were
unusable as identities. The current table is corroborated independently: walking the RTTI by hand
from the vtable at `00D6DE78` yields `.?AV?$PClassDescriptorConcrete@VPWorldMatrix@Phyre@@@Phyre@@`,
the same class the table names.

**Use 2,248.** Every count in §11 and §12 above is derived from the current table.

## 9. Audit pass 1 - 2026-09-13 (OPUS): the deleting-destructor family, proved by bytes

*(Static only - every candidate body compared byte for byte, and each shared callee identified from
its own body rather than from its name. Nothing executed.)*

The largest single shape in the EC-7 frontier: **1,149 functions, every one exactly 92 bytes, all
sharing one 12-byte prefix.**

### The proof is a masked byte comparison, not the tag

The checkpoint tag chose the candidates. It did not establish the family - **the day before, the
same class of tag was shown to under-count the thunk layer by 181**
([the thunk layer](../../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
§11). So the family was proved instead:

> Mask the four operands that **must** vary - the vftable `lea` disp32 and the three `call` rel32s -
> and compare the remaining bytes. **1,149 members collapse to TWO distinct byte images, and those
> two differ at exactly ONE offset**: byte 65, the object-size immediate. **0x100** for 1,145
> members, **0x108** for four (`005A4010`, `005D1DC0`, `006CEFC0`, `006D9EA0`).

One operand-slot layout across all 1,149. That is a generated body, and it is generated from one
template.

The shape is the MSVC deleting destructor: install the vftable, call the base destructor, then
branch on the hidden flags argument - bit 0 "delete", bit 2 "array".

### The two callees, identified from their bodies

| callee | body | what it is |
|---|---|---|
| `00584730` | `test rcx, rcx / jne 0019C570 / ret` | **`operator delete`**, null-guarded, tail-calling the import stub for `_aligned_free` |
| `0016D6A0` | **`ret 0`** - three bytes | **does nothing.** See below |
| `00633390` | 500 B | the **shared base destructor**, installing vftable `00D581C0` and touching a refcount at `+0xE8` and a global at `02CF8260` *(2026-09-14, FABLE: not a refcount — the descriptor id; see Q-2 in §7)* |

### ⚠ `0016D6A0` is a folded no-op with at least two identities

The array-delete arm passes the object size (`mov edx, 0x100`) and calls `0016D6A0`, whose entire
body is **`ret`**. The size is computed, passed, and discarded.

**The census names that address `_guard_check_icall`** - and
[the thunk layer](../../24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
§12 independently showed that the image's `GuardCFFunctionTable` and `GuardCFFunctionCount` are both
**0**, so the Control Flow Guard check *is* a no-op in this build. Both readings are consistent with
a three-byte `ret`, and **they cannot both be the whole story**: a CFG check and an array-delete
helper are different functions with different signatures.

**The natural explanation is identical COMDAT folding** - MSVC's `/OPT:ICF` merges functions with
identical bodies, and every no-op compiles to the same `ret`. *Labelled as inference:* what is
**measured** is that the body is `ret`, and that it is called from two contexts with incompatible
argument conventions. What is **inferred** is that the linker folded them.

Either way the consequence for a reconstruction is the same and is worth stating plainly: **the
array-delete arm of every one of these 1,149 destructors frees nothing**, and a reconstruction that
implements it as a real `operator delete[]` will free memory the shipped game does not.

This is recorded in
[duplicated function names](../../00-Engine-Core-Runtime/duplicated-function-names-and-how-to-resolve-them.md),
which is the page for exactly this problem.

### One base destructor, four hundred vftables

All 1,149 members call **the same** `00633390`. They install **400 distinct vftables**. So this is
not one deleting destructor per class - it is roughly **2.9 members per vftable**, consistent with
per-instantiation emission that the linker did not fold.

**`00633390` stays in the frontier and is not dispositioned by this row.** Neither are the 400
vftables, nor anything a descriptor describes. A row that disposes of 1,149 wrappers has said
nothing about the object they wrap.

**Not claimed.** The remaining `Phyre.Reflection.*` populations - `DataMemberMetadataStaticTeardown`
(853), `ClassDescriptorStaticTeardown` (404), `PClassDescriptorForType.DestructorT` (384) and the
rest of the 6,736 Phyre-tagged frontier functions *(6,735 when written; the Phyre tag family grew
by one at GN161)* - are **untouched**; each needs its own byte proof
and none inherits this one. Nothing executed.

## 10. Audit pass 2 - 2026-09-13 (OPUS): three more generated families, and a negative that matters more

*(Static only - a masked byte comparison run across every large tag group in the frontier, not just
the ones that turned out to be families. Nothing executed.)*

### Three groups are one shape each, at 100%

| family | members | body | shape |
|---|---:|---:|---|
| `PDataMemberMetadata` static teardowns | **853** | 12 B | `lea rcx, [static object]` ; `jmp 00633240` |
| `PClassDescriptor` static teardowns | **404** | 26 B | `lea rax, [vftable]` ; `lea rcx, [static object]` ; `mov [static object], rax` ; `jmp 00633390` |
| `PClassDescriptorForType` destructor thunks | **384** | 15 B | `lea rax, [vftable]` ; `mov [rcx], rax` ; `jmp 00633390` |

**Each masks to exactly ONE byte image across every member**, on one body size. **1,641 functions**,
declared **C**.

Two of the three tail-call `00633390` - **the same shared base destructor the 1,149 deleting
destructors call** (§9). Four families, one implementation underneath. **That implementation is
still in the frontier and is dispositioned by none of them**, which is the point the members files
repeat: these rows dispose of stubs that install a constant and jump.

### ✖ The negative is the more useful half, and it corrects my own routing

The same prover was run over **every** large frontier group, not only the ones that worked:

| group | members | distinct sizes | distinct shapes | largest shape |
|---|---:|---:|---:|---:|
| `NativeRoutine.AcyclicDirectCall.Bounded.Conditional` | 1,331 | 292 | **1,158** | 1.6% |
| `NativeRoutine.BoundedLoop.DirectCallOnly` | 1,108 | 274 | **1,077** | 0.5% |
| `NativeRoutine.AcyclicDirectCall.ExtendedBounded` | 1,081 | 480 | **1,023** | 2.4% |
| `NativeAdapter.BoundedDirectCall.Single.Linear` | 562 | 132 | **509** | 0.7% |
| `NativeDispatch.BoundedComputedCall.Acyclic.Branching` | 499 | 173 | **437** | 2.4% |
| `ThirdParty.Rendering.PPFX` | 343 | 317 | **343** | 0.3% |

**Roughly one shape per member.** These are not families. They are hundreds of individually
distinct functions that happen to share a *classifier's* label.

> **I routed several of these to FABLE as "candidate B families, because a shared tag is a shared
> shape."** That sentence is wrong and the prover disproves it. **A shared tag is a shared
> classification. Only shared bytes are a shared shape**, and a B row over 1,331 structurally
> distinct bodies could not answer B's question - *could ignorance of this family prevent
> reproducing FFXII?* - because there is no "this family" to be ignorant of. The routing note has
> been corrected and the lanes re-described.

`ThirdParty.Rendering.PPFX` is the sharpest case: **343 members, 343 distinct shapes.** The
`ThirdParty` tag makes it a C *candidate* in the frontier census, and it is still 343 individual
functions that one row cannot dispose of. **A C disposition needs the upstream named and the
boundary stated, and neither follows from a tag.**

### Where this leaves the middleware bucket

Of the 6,736 Phyre-tagged frontier functions, **2,790 are now declared** across four families
(1,149 + 853 + 404 + 384). The remainder is not more of the same: `ObjectPointerAccessor` (323) has
**two body sizes and 323 distinct masked images**, because those bodies differ by *field-offset
immediates* rather than by call targets - structurally one idiom, and **my mask cannot prove it**, so
it stays undeclared until an instrument that can.

**Not claimed.** Nothing about what any descriptor, metadata object or vftable *means*; nothing
about `00633240` or `00633390`; and no `Native*` group. Nothing executed.

## 11. Audit pass 3 - 2026-09-13 (OPUS): two more form-proved families

*(Static only. Nothing executed.)*

| family | members | body | byte images | **form images** |
|---|---:|---:|---:|---:|
| `PClassDescriptorConcrete` static initialisers | **254** | 53 B | 237 | **1** |
| `AbstractClassDescriptor` constructors | **182** | 152 B | 47 | **1** |

Both were invisible to a byte comparison and collapse to a **single instruction form**.

The static initialiser is the other half of the teardown family in §10 - it installs the vftable
into the static descriptor and **tail-jumps to `atexit`** registering the matching teardown. **All
254 tail-jump to `00808B90`.**

> **The larger half of this group is not dispositioned and the members file says so by count.**
> Each initialiser **calls its own per-type constructor** - **254 distinct external targets, one per
> member, every one still in the frontier.** The row disposes of 254 registration wrappers and
> leaves 254 constructors exactly where they were. *A family whose members each call something
> different has dispositioned the calling, not the called.*

## 15. `Q-6` answered — three consumers, and only two get an out-of-line destructor (2026-09-13, FABLE)

*(Static only — the census run `ec7/dtor_families.py` over the GFZ tags, `rtti/methods.tsv`, `rtti/vtables.tsv`, a raw
`E8`/`E9` edge scan, a whole-file qword scan and `graph/edges.tsv`. Nothing executed.)*

**The two families are not redundant: each is the destructor of a different consumer.** Which functions reach them
settles it:

| | `DeletingDestructor` | `DestructorThunk` |
|---|---|---|
| members | **1,149**, all 92 B | **384**, all 15 B |
| in a vtable | **all 1,149, at slot 7** | **none** |
| references to the address | **exactly one qword each** (its vtable) | **none** |
| direct callers | **0** | **0** — and `COVERAGE-DIMENSIONS` excludes EH-funclet edges from the call graph (3,834 of them), so the unwind tail jump below is **not** one |
| body | complete destructor inlined, then `flags & 1` → free (§2) | `lea rax, [vftable]` ; `mov [rcx], rax` ; `jmp 00633390` — no free |
| what transfers control | a virtual `delete` through slot 7 | a tail jump from an unwind funclet — **read from the funclets' instructions, not counted as an edge** (315 parent-frame reloads, 69 statics) |

- **The deleting destructor serves the vtable.** A virtual `delete` or a virtual destructor call goes through slot 7, and
  the flag word decides whether the storage is released. Nothing calls one directly.
- **The thunk serves the exception unwinder.** All 384 callers are `Unwind@` funclets (`CompilerGeneratedEH`), each a
  single tail jump. **315** reload the object from the parent frame (`mov rcx, [rdx + 0x60]`); **69** name a static
  descriptor directly (`lea rcx, [static]`). So a thunk runs only when an exception unwinds through a scope that has
  already constructed a `PClassDescriptorForType<T>`, and it must not free, because the storage is a frame slot or a
  static.
- **Normal-exit teardown needs neither.** It is the separate 26-byte static-teardown family (404 members, §10), registered
  through `atexit` by the static initialisers (§11), with the same vftable install and the jump to `00633390` emitted inline.

**375 of the 384 thunks install a vftable that a deleting destructor also installs.** The pairing is per instantiation;
the counts differ because a type gets a thunk only when some constructing scope has an unwind action for it.

> **Correction MADE, 2026-09-13 — this note is retired 2026-09-18 (OPUS).** It used to read *"Correction routed, not
> made here"* and quote the thunk row as saying the 384 are *"emitted through the MSVC static-teardown /
> destructor-thunk idiom"*. **The row has not said that since 2026-09-13.** It now opens with "ITS CONSUMER IS THE
> UNWINDER, NOT STATIC TEARDOWN", names `FABLE-REQ-OPUS-DTORTHUNK-WORDING`, and carries the census this section
> establishes: one direct caller each, all 384 callers `CompilerGeneratedEH` unwind funclets, none stored as a pointer
> in initialised data.
>
> The note outlived the thing it asked for, and **a stale routing note is worse than no note**: it sends the next reader
> to correct text that is already correct, and it makes a resolved item look open on the board. Kept rather than deleted
> so the sequence stays legible.
>
> **The phrase is still in rows 30 and 31, and there it is right.** Those two families — the 853 `PDataMemberMetadata`
> teardowns and the 404 `PClassDescriptor` teardowns — *are* registered through `atexit` and *do* run at normal exit.
> The idiom was never wrong; borrowing it for the thunks was.

**`BU-4` falls out of the same census.** The 384 behave identically — one byte image (§10) and one target, `00633390`,
for all 384. **They are not graph sinks**: `graph/edges.tsv` records exactly one outgoing edge (to `00633390`) and one
incoming edge (from the funclet) for each of the 384. That is unlike the `Thunk.*` forwarders the thunk-layer page measures.

**Not claimed.** Nothing about which constructor owns each funclet (the funclet → parent join through `FuncInfo` was
not walked), and nothing about `00633390` itself.

## `DK-1` — a mechanism, and the RTTI test was the wrong instrument (OPUS, 2026-09-14)

§10 asks whether *"`0063BC00` has exactly 369 distinct callers, and the RTTI names exactly 369
instantiable descriptor classes"* is a mechanism or a coincidence, and records the confirming test as
**failed**: only **15 of the 369** callers carry an RTTI identity, all slot 10 of
`WithoutDefaultConstructor<T>`. *"A coincidence in two counts is a lead, not a mechanism."*

**The lead was right and the instrument was wrong.** Read from the shipping image at the authority
hash `73461D08…9721F8`.

### The callers are four templates, not 369 functions

Disassembling every caller and reducing each body to its **mnemonic sequence** — registers kept,
every numeric literal ignored:

| body size | callers | instructions | distinct mnemonic sequences |
|---:|---:|---:|---:|
| 249 B | **162** | 55 | **1** |
| 282 B | **104** | 64 | **1** |
| 270 B | **70** | 65 | **1** |
| 260 B | 9 | 62 | **1** |
| 69 B | 6 | 20 | **1** |

**369 callers collapse to 23 distinct sequences, and 345 of them to four.** Within every one of those
four sizes the sequence is *unique* — one hundred and sixty-two bodies with the same fifty-five
instructions in the same order.

The raw bytes are all different, and that is the tell rather than a counter-argument: consecutive
stubs differ in a single `rel32` (`e8 fb91 0e00`, `e8 fb90 0e00`, `e8 fb8f 0e00` — consecutive
targets) and in their immediates. **That is a template instantiated once per class, carrying a
class-specific constant and a class-specific call target.**

### Which explains the failed test rather than contradicting it

Only `WithoutDefaultConstructor<T>` instantiations carry an RTTI record of their own; the 331
`Concrete<T>` ones do not. So **15 of 369 is what an RTTI probe should return here**, and it is
evidence about RTTI coverage, not about whether the count is a mechanism. The original test asked
*"do the callers identify themselves?"*; the question needed *"were the callers generated from one
shape?"*

### The control

The shape test blanks **only numeric literals**. Register allocation, instruction selection and order
are all preserved, so two functions matching means the compiler emitted the same code. A coincidence
of counts does not produce 162 bodies with an identical 55-instruction sequence. **Also measured: 369
distinct callers across 373 call sites** — four callers reach it twice — so the caller count is not an
artefact of a shared helper being counted once per site.

### Not claimed

**Which** class each stub belongs to is not established here — that needs the class-specific immediate
resolved against the descriptor table, and this section does not do it. The claim is that the 369 are
generated per class, not which 369.

*(Read by OPUS 2026-09-14. `DK-1` is answered: **a mechanism.** The two counts match because the
compiler emitted one stub per instantiable class.)*


## The `0016AB00`–`0016D540` run, reconciled — 327 absorbed, 4 declared (2026-09-16, SWE2-EC7;
extended to 34 on the tail-643 pass, 2026-09-17)

OPUS measured a 331-body dynamic-initialiser run sharing the `atexit` tail `00808B90` and queued it
for declaration. By the time the package ran, newer families had already absorbed 327 of the 331:
the 319 PInputs semantic-name-registry initialisers, 6 MSVC-generic dynamic-initialiser stubs, and
2 Phyre module-utility registrars. The frontier remainder was the four 64-byte flag-variant
bodies `0016C280`/`0016C2C0`/`0016C300`/`0016C340`.

The tail-643 pass then found 30 more bodies with the identical instruction encoding — only the
operand immediates differ — so the family was extended to **34 members** by deriving the skeleton
over the union (39 of 64 fixed positions; a census-wide scan of 64-byte bodies finds exactly those
34, self-bounding). The 30 new members span the descriptor-static bands `02CBxxxx`–`02EAxxxx`;
the original four sit at a `0x100` stride `02EB9070`–`02EB9370`. A third encoding also exists:
the **53-byte compact form** (5 members, `descriptor-flag-registrars-compact.tsv`) which clears
bit1 of `+0xFC` but does not set bit3 — and which is itself the encoding of the 222-member
`PClassDescriptorConcrete static initialisers` family (the same scan finds all 228; the other
223 satisfy the identical provenance predicate and are already owned — the discriminator is
prior ownership, not the constructor class).

The four controls OPUS required, answered for the remainder (the full 34 answer the same way —
the selector re-measures every skeleton match, not just the seeds):

- **Outbound calls:** each member's call set is exactly `{<declared AbstractClassDescriptor
  ctor>, 00808B90}` — base-aware or plain constructors, generated reflection machinery, no game
  code. (The original four's ctors are `00877BE0`/`00877C90`/`00877D40`/`00877DF0`; the extended
  thirty use the `005D9xxx`/`005DAxxx`/`0061xxxx`/`0067xxxx`/`006Axxxx`/`006Bxxxx`/`006Cxxxx`/
  `00791B70` declared-ctor range.)
- **Shared globals:** each member touches exactly two `.data` addresses — the descriptor static it
  constructs and its `+0xFC` flag word — plus one `.rdata` record pointer. None of these cells is
  shared with a live subsystem; they are the private statics the toolchain initialises, and each
  flag word is provably `object + 0xFC`. (The original four objects sit at a strict `0x100`
  stride `02EB9070`–`02EB9370`; the extended thirty span `02CB6580`–`02EA5380`.)
- **Boundary:** the census-wide skeleton scan over every 64-byte body finds exactly the 34
  members — the form is self-bounding. The original run's neighbours (`0016AAC0` below,
  `0016D560` above) are declared `PClassDescriptorConcrete static initialisers` members, so the
  span edges match OPUS's measure. The crossing the run makes into Input is already
  dispositioned: `0016D540` and the 318 other absorbed stubs call the PInputs semantic-registry
  append bodies (`00879570` and siblings) — an initialiser→registry edge owned by the PInputs
  semantic-name-registry initialisers family on the Input-Name-Registry page, not reflection
  metadata.
- **Provenance pairing:** every member's `lea rcx` dtor operand is a member of a declared
  teardown family — `PClassDescriptor static teardowns` for all 34 plus the compact form's
  `xc-registered-static-teardowns` — so both halves of each register/teardown pair are generated
  and no half is left dangling.

## The `00639A60` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00639A60` (~411 B) — EH-frame body opening `mov rax, [rcx+0xC0];
test rax, rax` (`00639A66`/`00639A70`) — a descriptor payload pointer
at `+0xC0` is probed before dispatch.

| member | role | interior |
| --- | --- | --- |
| `0063CB80` | descriptor body | [`0063CB80`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `00808B90` tail-643 worklist, decomposed (2026-09-17, SWE2-EC7)

OPUS's `atexit-anchor-tail-643.tsv` lists 643 bodies that reference the MSVC `atexit`
wrapper `00808B90`. The anchor is NOT provenance — it only proves the body registers
something at exit — so the worklist was decomposed by form, not declared wholesale:

- **428 already owned / 10 A-measured** at this pass: the tail is mostly stragglers of
  families that landed after OPUS's snapshot (PInputs semantic-name-registry stubs, EASTL
  string initialisers, the module families, the record-ctor static-initialiser forms).
- **64-byte descriptor-flag registrars — 34 members** (this page): the 4 originals plus
  30 tail bodies sharing the identical encoding; union-derived skeleton self-bounds.
- **53-byte compact descriptor-flag registrars — 5 members** (this page): the compact
  encoding is the `PClassDescriptorConcrete static initialisers` family's own form. All
  223 census twins satisfy the identical provenance predicate (same base-subobject ctor
  families, same teardown families, same flag op) — the discriminator is **prior
  ownership** (222 declared by PClassDescriptorConcrete, 1 A-measured), not constructor
  provenance; the five members are simply the unowned remainder of the same idiom.
- **Guarded class-registration stubs — one family** (this page; counted as 76 + 26 in two rows until FABLE's
  2026-09-29 ruling made the split an information column): the
  call-signature family `_Init_thread_header`/`_Init_thread_footer`/`00808B90` with every
  other call target already explained (declared, A-measured, shared machinery, or a family
  member). The census-wide predicate matches no unowned body.
- **Pure magic-static singleton guards — 18 members** (Lazy-Static-Initialization page):
  call set is exactly the guard pair plus `00808B90`, payload inlined.

The **48 tail bodies left frontier** after this decomposition are the ones whose aux callees
are NOT yet explained: ~35 unguarded subsystem stubs calling frontier helpers (several are
themselves the pure-guard stubs' callers — `00163DB0`→`00631A60` etc.), a dozen guarded
stubs that also call other guarded bodies, and whose private aux targets (`006343E0`, `00633100`, `0067FF40`, `005CD4F0`,
`00615840`, `005DC200`, `008653B0`…) have no provenance yet, and singleton forms. Declaring
them on the shared `00808B90` edge alone would be exactly the bulk disposition the task
prohibits — each needs its aux callees dispositioned first, or its own form family.


## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-17)

*Classes per [`PASS22-WHAT-ACCOUNTING-MEANS`](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2.
The caller set is from `edges.tsv`; both bodies below are read, not inferred.*

- **Audio — CLIENT.** Eleven edges reach `005CD4F0` from the Audio layer, including `00212050`,
  `002120E0`, `00212300` and `00219C40`. **`005CD4F0` is a nine-byte second-argument rebasing
  thunk** — `lea rdx, [rcx + 0x20]` then `jmp 005CD450` (`005CD4F0`/`005CD4F4`) — so it supplies
  the `+0x20` sub-object as the acquire's second argument while `rcx` stays the owner block; it
  carries no behaviour of its own. *(Label corrected 2026-09-19 per OPUS review — an adjustor
  thunk adjusts `this`; this one adjusts `rdx`.)*
  **What the layer uses it FOR** is `005CD450`, which is a lock acquire: `lock xadd dword [rcx +
  0x18], 1` counts the waiter (`005CD46C`), `lock cmpxchg dword [rbx], 1` takes the flag at the
  thunk's `+0x20` sub-object when it is zero (`005CD473`), and on contention the uncontended arm is
  skipped and the handle at `+8` is waited on with an INFINITE timeout, the result tested against
  `0x80` — `WAIT_ABANDONED` (`005CD47E`–`005CD48B`). So the Audio layer is **taking this
  subsystem's lock**, not reading its metadata.
  *Evidence tier: READ BODY for `005CD4F0` and `005CD450`; the eleven call sites rest on `edges.tsv`
  alone.*

> **This also gives one of the tail-643 aux targets its provenance.** The section above lists
> `005CD4F0` among "private aux targets … have no provenance yet". It has one now: a second-argument
> rebasing thunk onto the `005CD450` acquire. That does not settle the other aux targets in that list, and it is
> not offered as a form family — it is one body read because pass 22 asked what the Audio edges
> were.


### Interior citation — frontier hub `005A7A40` (2026-09-18, SWE2-EC7)

`005A7A40` — 110 B, 47 callers: the by-name node lookup the registration stubs
share (x27 in the call-set signature above). Read from the shipping image: walks
the intrusive circular list at `[rcx+0x90]` — head equal to the sentinel
self-pointer means empty — comparing each node's `[r9+0x18]` C-string byte-wise
against `rdx` at [`005A7A74`](../../_index/ADDRESS-INDEX.md); a hit returns the
node, exhaustion returns 0. The find half of the descriptor registry's
find-or-register pair.
### Interior citation — frontier hub 00632C90 (2026-09-18, SWE2-EC7)

**00632C90** (66 B; heads the ICF-folded cluster of identical scalar-deleting destructors at `00632C90`/`00632CE0`/`00632D30`, 4 A-measured callers) — `??_G` scalar-deleting destructor for the class whose vtable is **00D30168**: stores the vtable (`lea rax,[rip+0x6fd4bf]` → `[rcx]`), then under flag bit 0 dispatches the free — bit 2 selects sized delete `0016C6A0` with `edx = 0x50` (the class size), otherwise unsized `00583730` — and returns the object. The descriptor record this deletes is 0x50 bytes, matching the `+0x50` self-chain the family-28 ctor writes. In-scope: vtable store [`00632CA9`](../../_index/ADDRESS-INDEX.md); delete-branch calls [`00632CB6`](../../_index/ADDRESS-INDEX.md)/[`00632CC3`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-19 update (2026-05-15) — `00639160` guarded registration-call helper

`00639160` (299 B) is the registration-splice sibling of the guarded class-registration stubs this page's family row describes: `rsi=[rdx+0x30]` and `0063BA10(rsi)` resolve the candidate — a non-null result differing from `rdi` tails to `005CDAA0` with the `00D58870` report string and `ecx=2` (`0063916F`..`006391AD`). On the null arm it reads the `[rbx+0x10]` link (`rbp = rax-0x50`, both cmove-nulled on the self-link), dispatches `[rbx+0x20]` kind `1` → `0063E410(rdi)` / kind `2` → `005CDAA0` with `00D588B8` and `ecx=kind-1` (`006391B2`..`006391FA`), then splices the `+0x50` list node — relinking `rdx`'s `+0x50` pair when `[rdx+0x70]==rbx`, else appending `rdi+0x50` into `[rbx+0x10]`'s list (`006391FF`..`00639244`) — and when `rbp` was null links `rbx` into the `006373D0()` singleton's `+0x28` list (`00639256`..`00639277`). The intrusive-list splice the registration stubs wrap.

## SWE2-EC7-39 update (2026-09-19) - `0063CB80`

`0063CB80` (411 B) is a class-metadata body - `0063BB10`/`00861EBA` pairs plus `0063C0C0` and three vcalls. Interior anchor `0063CBB6` (a `0063BB10` call).

## SWE2-EC7-46 update (2026-09-19) - `005DC200`

`005DC200` (236 B) is a body - `005CC900`/`00808FE4`/`00861EC0`/`00874D60`. Interior anchor `005DC220` (a `005CC900` call).

## SWE2-EC7-51 update (2026-09-19) - `006343E0`

`006343E0` (179 B) is an aux target of guarded registration stubs that also call other guarded bodies - `0017D260` single call. Interior anchor `0063440B` (the `0017D260` call).

## SWE2-EC7-58 update (2026-09-19) - `0062EFD0`

`0062EFD0` (166 B) is the `AttachMember` body the class-descriptor page names - `00597220`/`0063C0C0`. Interior anchor `0062F006` (a `0063C0C0` call).

## SWE2-EC7-60 update (2026-09-19) - `0063E0D0`

`0063E0D0` (157 B) is the `PTypeDefault<double>` byte-reversal the class-descriptor page names - call-free mask/shift chain (`0xff00000000`/`0xff00`/shr 8/16). Interior anchor `0063E113` (the `0xff00000000` mask `movabs`).


## SWE2-EC7-69 update (2026-09-19) - `006B6700` intrusive-list unlink measured

`006B6700` (71 B) measured - the page's "intrusive-list unlink loop" is
exact: it walks the head at `[rcx]`, and while the head is not self-linked
it recovers the record as `link - 8`, splices the embedded link out
(`[link.next+8] = link.prev`, `[link.prev] = link.next` through the `+8`/`+0x10`
slots), then self-links the node and loops until the head points at itself.
Call-free; every descriptor dtor in the `008AFxxx`/`00633xxx` clusters runs
it on the `+0x38` embedded list.
Interior anchor `006B6736` (the `[rcx+8] = rax` splice store).

## SWE2-EC7-78 update (2026-09-20) - `006B67D0` + `006B66C0` list-node helpers measured

`006B67D0` (22 B) is the intrusive list-head insert: the `rdx+8`
node is spliced between `[rcx]`'s head and its old first link -
four stores (`[rdx]=[rcx]`'s target, `[rdx+8]=rcx`, `[rcx]=rdx`,
`[oldhead+8]=rdx`).
Interior anchor `006B67DE` (the `[rcx] = rdx` splice).

`006B66C0` (37 B) is the matching ctor: `+8`/`+0x10` form the
circular empty head, vtable `00D80930` (RTTI `01D33110`, `[0] =
006B6780`) is installed at `[rcx]`, and `+0x18`/`+0x20`/`+0x28`
take the three args.
Interior anchor `006B66CB` (the vtable lea).

## SWE2-EC7-80 update (2026-09-20) - `005A0470` member-name find measured

`005A0470` (110 B) is the string find the descriptor callers run:
`rdx` NULL returns 0; else it walks the circular list headed at
`rcx+0xA0` (node `[r9]` next, wrap-to-head collapses to 0), comparing
each node's `[r9+0x18]` C string byte-for-byte against `rdx` until
NUL or mismatch; the matching node returns, else 0.
Interior anchor `005A04A4` (the byte compare).

## SWE2-EC7-117 update (2026-09-21) - `006B67F0` measured

`006B67F0` (48 B) is the
find-by-field `00639C80`
runs on the intrusive list
at `[rcx]` (nodes at
`link - 8`): walks until
`qword[+0x18] == rdx` and
returns the node or 0 -
the same walk shape as the
`01F401E8` drains.
Interior anchor `006B6803`
(the `+0x18` compare).

## SWE2-EC7-119 update (2026-09-21) - the asset-reference registrations measured

`00675DA0` (333 B) is one
`005A08E0` registration
block: `0063DC90` binds the
`00676F50`/`00677470`
method pair on `02D3E780`,
then `00632960` fields
`"m_id"` (type 0x10,
offset 8) and
`"m_targetAssetType"`
(0x12, 0) under the
`02EAED3C`-indexed TLS
counter guard, tailing
`00639450`.
Interior anchor `00675E4B`
(the `"m_id"` `00632960`).

`00675740` (1626 B) is the
asset-reference class on
`02D3E680`: the same
guarded idiom fields
`"m_id"` (0x10, 0x30),
`"m_asset"` (0x12, 0x38),
`"m_assetType"` (0x12,
0x40), registers methods
`"getID"`, `"getAsset"`,
`"getAssetType"`,
`"GetAssetReferenceByID"`,
`"GetAssetReferenceByAsset"`
through `00632FB0`, and
stamps the `02D3E9D0`
handler record (vtable
`00D6C378`) via
`00633100` before the
`02D3E960` link.
Interior anchor `00675999`
(the `"getID"` `00632FB0`).

## SWE2-EC7-120 update (2026-09-21) - the descriptor-object idiom measured

`0063DC90` (9 B) is the
two-field setter the
registration blocks call:
`[rcx + 0x40] = rdx`,
`[rcx + 0x48] = r8` - the
method-pair slot write
`00675DA0` ran for the
`00676F50`/`00677470` pair.
Interior anchor `0063DC94`
(the `+0x48` store).

`0063C5E0` and `0063C1A0`
(77 B each) are twin
unregister idioms
`00639C80` drives: when
`+0xFC`'s sign bit is set
they return `+0xD0`/`+0xC8`
untouched; otherwise bit 30
gates a `vtable[+0x60]`
call, then `00639A60(rcx,
0)` and `00639C80(rcx, 0)`
run and the `+0xD0`/`+0xC8`
cell returns.
Interior anchor `0063C604`
(the `00639A60` call);
interior anchor `0063C1C4`
(the same).

`0063AE50` (412 B) resizes
the `+0x110` buffer family:
when `+0x38` exceeds
`btr(+0x108, 31)` it
allocates `edi` bytes via
`0017D260`, copies
`min(edi, oldcap)` bytes,
frees the old `+0x110`
under ownership, runs
`00627BD0` on the `+0x118`
and `+0x128` slices,
`00861EC0` zero-fills the
`+0x110`/`+0x120`/`+0x130`
tails, then republishes the
three into `+0xC0`/`+0xC8`/
`+0xD0`; alloc failure
returns 0xD.
Interior anchor `0063AEBF`
(the `0017D260` call).

`0063A4C0` (121 B) is the
`+0x78`-chain ancestry
check `006393A0` calls:
null `rdx` or a
`00597220(rdx)` hit both
return 0; else `r8`'s
`vtable[+0x8]` produces a
node whose `+0x78` chain is
walked for `rcx`, vetoed by
`r9d` bit 1 and by
`byte[+0xFC] & 2`.
Interior anchor `0063A4FF`
(the `vtable[+8]` call).

`00639850` (490 B) is the
masked blit `0059D940` and
nine others call: `+0xFC`
bit 28 early-outs, the
unregister idiom runs twice
(`vtable[+0x60]` on bit 30,
`00639A60`/`00639C80`), then
per `r14` row it blends
`r11d = +0x38` bytes as
`dst = (mask & src) |
(~mask & dst)` - SSE2
`movdqu`/`pandn`/`pand`/
`por` at 32 B a step over
`rdi`-mask, `rbp`-source,
`rbx`-dest, with a byte
tail; `rbx` starts at
`rdx - movsxd(+0xF8)`.
Interior anchor `00639970`
(the `movdqu` blend loop).

## SWE2-EC7-121 update (2026-09-21) - the `02CF82E0` registry-table init and name-tree insert measured

`006344A0` (156 B) is the
registry-table init
`005A08E0` calls: the three
byte slots `02CF8FA0`,
`+1`, `+2` store to
`02CF8330`/`+0x338`/`+0x340`,
`02CF836C |= 0x20`, then
`00639160(02CF82E0,
02CF8270)` runs and bit 30
of `02CF836C` sets. When
the call's bit-0 result is
set it triple-self-links
the `02CF8278` sentinel
(`02CF8278`/`+8`/`+0x10`,
zero `+0x18`/`+0x20`) and
tails `006388C0`.
Interior anchor `006344E3`
(the `00639160` call).

`006314B0` (251 B) is the
by-name tree insert inside
`006388C0`'s registration:
`byte[rdx+0x18] & 1` parity
bumps the `[rbx+0x10]`
count, `rdx+8` links back
to `rcx`, then the walk
descends the `+0x18` child
table comparing
`u32[+0x20]` name lengths
first and `memcmp`-ing the
`[+0x28]`/`[+8]` strings on
a tie, descending on the
`bit-31` of the comparison
sign; at an empty child it
stores `rbx` into
`[r9 + rax*8]` and bumps
`[rbx+0x10]` by
`r9 + (byte & 1)`.
Interior anchor `00631540`
(the string-compare loop).

`00633100` (30 B) is the
link-record ctor
`00675740` calls: it
stores `rdx` at `[rcx+8]`,
installs vtable `00D58098`
(`[0] = 00634310`, RTTI
`01D14A90`), sets
`[rdx+0x28] |= 4` and
back-links `[rdx+0x50] =
rcx`.
Interior anchor `0063310E`
(the `+0x28` flag or).
