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
    FUN_006b6700(self + 7);                       // destroy an embedded string (the name)   // <- corrected 2026-10-02, OPUS - 006B6700 unlinks every node of the list at +0x38 (006B6710-006B6744); no string
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
| ~~`+0x0C`~~ `+0x60` | `FUN_006b6700` | ~~embedded string (the class name)~~ a sixth intrusive list *(corrected 2026-10-02, OPUS: qword indices, see the unit correction below; `00633557` passes `+0x60` to the list-unlink `006B6700`; the name is the `char *` at `+0x30`, `006388CA`)* |
| ~~`+0x0E`~~ `+0x70` *(corrected 2026-10-02, OPUS: `006333DC`)* | `FUN_0063d640` | a sub-object, destroyed first |
| ~~`+0x10`~~ `+0x80` *(corrected 2026-10-02, OPUS: `006334B2`)* | intrusive list walk | list #1 |
| ~~`+0x12`~~ `+0x90` *(corrected 2026-10-02, OPUS: `006333E6`)* | intrusive list walk | list #2 |
| ~~`+0x14`~~ `+0xA0` *(corrected 2026-10-02, OPUS: `0063344E`)* | intrusive list walk | list #3 |
| ~~`+0x16`~~ `+0xB0` *(corrected 2026-10-02, OPUS: `0063352C`)* | intrusive list walk | list #4 |
| ~~`+0x1D`~~ `+0xE8` *(corrected 2026-10-02, OPUS: `006333BF mov eax, [rcx+0xe8]` against `02CF8260` at `006333C7`)* | compared to `DAT_02CF8260` | a generation / registration counter |

**Four separate intrusive linked lists.** Their individual roles are not established — see §7. *(answered: see the unit correction below - six lists, four walked - and CONTRACT-phyre-class-descriptor.md's destructor correction, 2026-09-12; 2026-10-02, OPUS)*

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
| `0063D640` | descriptor sub-object destructor | ~~not read~~ *(answered: see CONTRACT-phyre-class-descriptor.md, 0063D640 takes (rcx = the sub-object, rdx = the descriptor); 2026-10-02, OPUS)* |
| `006B6700` | ~~embedded-string destructor~~ **intrusive-list unlink loop** | ✅ read 2026-09-14 (OPUS, pass 13) |
| `02CF8260` | global compared against descriptor ~~`+0x1D`~~ `+0xE8` *(corrected 2026-10-02, OPUS: byte offset, `006333BF`)* | — |

## 4. Data structures and formulas

```
PType                                    base of the reflection type hierarchy

PClassDescriptor : PType
  +0x00   ptr    vftable
  +0x0C   str    embedded string (class name)   <- corrected 2026-10-02, OPUS - qword index; byte +0x60 is a list cleared by 006B6700 (00633557), the name is the char * at byte +0x30 (006388CA)
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
  +0x38   str    embedded string (member name)   <- corrected 2026-10-02, OPUS - an intrusive list head cleared by 006B6700 (00633278-0063327C); the name pointer is at +0x20
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
     -> PClassDescriptorConcrete<T> static initializer      (227 of these)   <- corrected 2026-10-02, OPUS - 255 in the ledger, 254 in the family file (section 2's table)
        -> AbstractClassDescriptor constructor (005A7ED0)
        -> install PClassDescriptorConcrete<T>::vftable
        -> atexit(ClassDescriptorStaticTeardown)            <- the pairing proof

runtime
  -> asset load / object traversal
     -> Reflection.ObjectTraversal (0063E2E0)
        -> walk the descriptor's member lists

process exit
  -> atexit chain
     -> ClassDescriptorStaticTeardown       (372)   <- corrected 2026-10-02, OPUS - 404 (section 2's table, the ledger)
     -> DataMemberMetadataStaticTeardown    (830)   <- corrected 2026-10-02, OPUS - 853 (section 2's table, the ledger)
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
| ~~2,134 RTTI classes~~ 2,248 RTTI classes *(corrected 2026-10-02, OPUS: superseded by §14, as §2 already says; `classes.tsv` has 2,248 rows)* | independent MSVC RTTI walk (`rtti_recover.py`) | 4 |

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

`+0x50` ~~returns **false on every class measured**, so `00639A60` always hands off to `0063CB80`~~ returns false only on some classes, so `00639A60` hands off to `0063CB80` only then or when flags bit 0 is set *(corrected 2026-10-02, OPUS: `00639AB6`-`00639ABE` and `00639B20`-`00639B25`; slot `+0x50` of all 331 `Concrete<T>` vtables is a per-class construct body, never the `xor al, al` stub `00657140`; the WITHDRAWN block above)*
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
> survives untouched: the stub is measured, the branch is measured, ~~`0063CB80` always runs~~ `0063CB80` runs only on flags bit 0 or a false `+0x50` *(corrected 2026-10-02, OPUS: `00639AB6`-`00639ABE`, `00639B20`-`00639B25`)*.

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
| `+0xD0` | a third buffer registered by the same family; ~~**no reader identified**~~ a byte mask over the instance, built by `00639C80` *(corrected 2026-10-02, OPUS: zero-filled at `00639CD8`-`00639CE4`; CONTRACT-phyre-class-descriptor.md, purpose read 2026-09-25)* | set by `0063DFA0` |
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
at `+0x38` through `006B6700`~~ **clear the intrusive list at `+0x38` through `006B6700`**, and conditionally free ~~`[+0x18]` when `[+0x20] & 1`~~ member `+0x20` when member `+0x28` bit 0 is set *(corrected 2026-10-02, OPUS: the offsets were relative to the node at member `+0x08`: `00633261 lea rdi, [rcx+8]`, `00633282 test byte ptr [rdi+0x20], 1`, `00633288 mov rcx, [rdi+0x18]`)*.

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

**00632C90** (~~66 B; heads the ICF-folded cluster of identical scalar-deleting destructors~~ 226 B, a `PClassDescriptor` constructor *(corrected 2026-10-02, OPUS: it self-links `+0x08`/`+0x50`/`+0x60`, stores the name at `+0x30`, stamps `00D581C0` at `00632CD7` and zeroes `+0xF0`/`+0xF8`, ending at `00632D71`; the destructor described next is not at this address)* at `00632C90`/`00632CE0`/`00632D30`, 4 A-measured callers) — `??_G` scalar-deleting destructor for the class whose vtable is **00D30168**: stores the vtable (`lea rax,[rip+0x6fd4bf]` → `[rcx]`), then under flag bit 0 dispatches the free — bit 2 selects sized delete `0016C6A0` with `edx = 0x50` (the class size), otherwise unsized `00583730` — and returns the object. The descriptor record this deletes is 0x50 bytes, matching the `+0x50` self-chain the family-28 ctor writes. In-scope: vtable store [`00632CA9`](../../_index/ADDRESS-INDEX.md); delete-branch calls [`00632CB6`](../../_index/ADDRESS-INDEX.md)/[`00632CC3`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-19 update (2026-05-15) — `00639160` guarded registration-call helper

`00639160` (299 B) is the registration-splice sibling of the guarded class-registration stubs this page's family row describes: `rsi=[rdx+0x30]` and `0063BA10(rsi)` resolve the candidate — a non-null result differing from `rdi` tails to `005CDAA0` with the `00D58870` report string and `ecx=2` (`0063916F`..`006391AD`). On the null arm it reads the `[rbx+0x10]` link (`rbp = rax-0x50`, both cmove-nulled on the self-link), dispatches `[rbx+0x20]` kind `1` → `0063E410(rdi)` / kind `2` → `005CDAA0` with `00D588B8` and `ecx=kind-1` (`006391B2`..`006391FA`), then splices the `+0x50` list node — relinking `rdx`'s `+0x50` pair when `[rdx+0x70]==rbx`, else ~~appending~~ linking `rdi+0x50` at the head of `[rbx+0x10]`'s list *(corrected 2026-10-02, OPUS: `r14 = rbx+0x10` is the sentinel, `006391C2`; `00639244 mov [r14], rdx` makes the node the first, next being node `+0`, as `006B6710` walks it)* (`006391FF`..`00639244`) — and when `rbp` was null links `rbx` into the `006373D0()` singleton's `+0x28` list (`00639256`..`00639277`). The intrusive-list splice the registration stubs wrap.

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

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-class-descriptor-and-metadata-system-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00219C40` | 90 B | passes `rcx + 0xB8` to the 9-byte thunk that adds `+0x20` as the second argument, decrements dword `[rdx + 0x58]` and, when it reaches 0, calls virtual slot `+0x10` of `rdx` and then a 161-byte routine with `(rcx + 0x20, rdx)`; it always ends by tail-jumping a 32-byte release on `rcx + 0xB8` | `00219C5C`, `00219C61`, `00219C70`, `00219C7A`, `00219C95` |
| `005A3E50` | 79 B | stores the result of a 98-byte getter and the pointer `00D2D310` into a stack pair, calls virtual slot `+0x78` of `rcx` with `(rcx, rdx, &pair)`, and returns 1 in `al` | `005A3E6A`, `005A3E74`, `005A3E8E`, `005A3E92` |
| `005CB140` | 9 B | byte-swaps dword `[rdx]` in place and returns 1 in `al` | `005CB142`, `005CB144`, `005CB146` |
| `005CE120` | 95 B | passes `02E404B0` and then `02CB6E80` to a 112-byte lookup; when either result is null it returns 0 in `al`, otherwise, when `rdx` is non-null, it stores the two results to qwords `[rdx]` and `[rdx + 8]` and 0 to dword `[rdx + 0x10]`, and returns 1 | `005CE134`, `005CE143`, `005CE14B`, `005CE15A`, `005CE172` |
| `005D18C0` | 115 B | stores the result of a 98-byte getter and the pointer `00D2D310` into a stack pair and calls virtual slot `+0x78` of `rcx` with `(rcx, rdx, &pair)`; then, when bit 31 of dword `[rdx + 0x10]` is clear, passes qword `[rdx + 0x18]` and that dword to a 104-byte release; it zeroes qword `+0x18` and dword `+0x10` and returns 1 in `al` | `005D18FE`, `005D1907`, `005D1918`, `005D191F`, `005D1923` |
| `006132E0` | 65 B | when qword `[rdx + 0x20]` is non-null it calls that object's virtual slot `+0x10` and zeroes the qword; it then clears bit 7 of dword `[rdx + 0x1C]`, calls `_guard_check_icall` with `rdx` and returns 1 in `al` | `006132F9`, `006132FE`, `00613301`, `00613309`, `00613313` |
| `00633240` | 93 B | stores `00D580B0` to qword `[rcx]`; when qword `[rcx + 8]` does not point at `rcx + 8` it calls virtual slot `+0x48` of qword `[rcx + 0x18]` with `rcx` as the second argument; it then passes `rcx + 0x38` to a 71-byte routine and, when bit 0 of byte `[rcx + 0x28]` is set, passes qword `[rcx + 0x20]` to a 10-byte null-guarded forwarder | `0063325E`, `00633265`, `00633274`, `0063327C`, `00633282` |
| `006332A0` | 93 B | stores `00D580B0` to qword `[rcx]`; when qword `[rcx + 8]` does not point at `rcx + 8` it calls virtual slot `+0x48` of qword `[rcx + 0x18]` with `rcx` as the second argument; it then passes `rcx + 0x38` to a 71-byte routine and, when bit 0 of byte `[rcx + 0x28]` is set, passes qword `[rcx + 0x20]` to a 10-byte null-guarded forwarder | `006332BE`, `006332C5`, `006332D4`, `006332DC`, `006332E2` |
| `0063E050` | 52 B | reverses the byte order of dword `[rdx]` with masks and shifts (`0xFF00`, `<< 16`, `<< 8`, `>> 8`, `>> 24`), stores it back and returns 1 in `al` | `0063E055`, `0063E06E`, `0063E075`, `0063E080` |
| `0063FC60` | 31 B | takes `rdx - 8` as an object (null when `rdx` is null), calls its first virtual slot with `edx = 0` and returns 1 in `al` | `0063FC66`, `0063FC6D`, `0063FC76`, `0063FC78` |
| `00674BE0` | 93 B | passes the address from an 8-byte getter to a 112-byte lookup and returns 0 in `al` when it is null; otherwise, when `rdx` is non-null, it calls a 124-byte routine with `(rdx, 0, lookup result, getter address)`, and returns 1 | `00674C03`, `00674C0E`, `00674C18`, `00674C2A`, `00674C30` |
| `00676F50` | 216 B | when qword `[r9 + 8]` is null it scans the table at qword `[r9]` (count = dword `[table]` AND `0x7FFFFFFF`, entries from qword `[table + 8]` when the count is above 1, else inline at `table + 8`) for the first non-null entry whose qword `+0x50` is `02D3E780` and caches it in `[r9 + 8]`, returning 7 when the table is null, empty or has no match; with the cached entry it gets a buffer from a 12-byte allocator called with `(2, 2)` and, when non-null, stores into its first word the byte-swapped 16-bit index `(rcx - qword [entry + 0x58]) / 24` (signed), stores the buffer to qword `[rdx]` and `0x80000002` to dword `[r8]`; it returns 0 (also when the allocation fails) | `00676FB1`, `00676FD8`, `00676FE8`, `00677014`, `0067701E` |
| `00677470` | 175 B | byte-swaps word `[rdx]` into an index; when qword `[r9 + 8]` is null it scans the table at qword `[r9]` (count = dword `[table]` AND `0x7FFFFFFF`, entries from qword `[table + 8]` when the count is above 1, else inline at `table + 8`) for the first non-null entry whose qword `+0x50` is `02D3E780` and caches it in `[r9 + 8]`, returning 7 when the table is null, empty or has no match; with the cached entry it takes the 24-byte record `qword [entry + 0x58] + index * 24`, stores the record's qword `+0x10` to `[rcx]` and `rcx` to that qword, and returns 0 | `00677488`, `006774D0`, `006774ED`, `00677510`, `00677515` |
| `00680910` | 32 B | takes `rdx - 8` as an object (null when `rdx` is null), calls its virtual slot `+0x10` with `edx = 0` and returns 1 in `al` | `00680916`, `0068091D`, `00680926`, `00680929` |
| `00689FC0` | 102 B | calls virtual slot `+8` of qword `[rdx + 0x118]` and the first virtual slot of qword `[rdx + 0x120]`, each with `edx = 1` and only when the pointer is non-null, then zeroes qwords `+0x120`, `+0x118` and `+0xC8`, passes `rdx` to a 109-byte routine and returns 1 in `al` | `00689FE6`, `00689FFD`, `0068A001`, `0068A00F`, `0068A019` |
| `0068C4E0` | 32 B | takes `rdx - 8` as an object (null when `rdx` is null), calls its virtual slot `+0x18` with `edx = 0` and returns 1 in `al` | `0068C4E6`, `0068C4ED`, `0068C4F6`, `0068C4F9` |

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-class-descriptor-and-metadata-system-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00164100` | 119 B | calls `00632780` with the addresses `02CF8A80` and `02CF8270` and 0; then clears bit `0x2` and sets bit `0x8` of dword `02CF8B7C`, stores the addresses `02CF8E20`, `02CF8E40` and `02CF8E60` to qwords `02CF8B40`, `02CF8B48` and `02CF8B50`, stores the address `00D56D10` to qword `02CF8A80`, and tail-jumps to `00808B90` with the address `008AF170` | `00164115`, `00164138`, `0016414C`, `00164160`, `00164172` |
| `005D1500` | 39 B | calls `006388C0` with the address `02CB9C00`, ORs 0x20 into dword `02CB9CFC` and tail-jumps to `00639450` with the address `02CB9C00` | `005D150B`, `005D1510`, `005D1522` |
| `005D7060` | 39 B | calls `006388C0` with the address `02CB7CA0`, ORs 0x20 into dword `02CB7D9C` and tail-jumps to `00639450` with the address `02CB7CA0` | `005D706B`, `005D7070`, `005D7082` |
| `0060F2D0` | 116 B | calls `00630180` with the incoming registers and then slot `+8` of the returned object's vtable; when `rdx` equals `rcx` + 8, `r8d` is 1 and that slot's result is non-null it calls `00639850(result, rcx + 8, 1)`, otherwise `006C7D00(rcx, rdx, r8d)`; returns 0 | `0060F2F1`, `0060F2FC`, `0060F305`, `0060F318`, `0060F328` |
| `0063AA50` | 123 B | when byte `+0xFC` of `r8` has bit `0x8` set, calls `005CDAA0(1, the address 00D58750, qword r8+0x30)` and takes 0 as the value; otherwise calls `00639510` with the incoming `rcx`, dword `r8+0x38`, 1, `r8` and 0 as the fifth (stack) argument and, when it returns a record, takes its qword `+0x58` and calls `0063C910(r8, that)`; finally stores the value to qword `[rdx]` and `r8` to qword `rdx+8` and returns `rdx` | `0063AA5F`, `0063AA7F`, `0063AA98`, `0063AAAC`, `0063AABC` |
| `006777D0` | 120 B | reads dword `+4` of the thread-local block indexed by dword `02EAED3C` (through `gs:[0x58]`); when dword `02D3ECF8` is greater than it (signed) it calls `008092FC` with the address `02D3ECF8` and, only when `02D3ECF8` is then -1, stores `006372A0()` OR 1 to qword `02D3ECE8`, zeroes qword `02D3ECF0` and calls `0080929C` with the address `02D3ECF8`; every path returns the address `02D3ECE8` | `006777F8`, `00677807`, `00677815`, `0067781E`, `00677837` |
| `0068D700` | 80 B | when `rdx` is non-null zeroes qword `[rdx]`, stores `006372A0()` to qword `rdx+8`, zeroes qword `rdx+0x10`, stores a second `006372A0()` result to qword `rdx+0x18` and zeroes dword `rdx+0x20`; returns `al` = 1 on both paths | `0068D720`, `0068D727`, `0068D72C`, `0068D73D`, `0068D741` |
| `006AF4F0` | 112 B | when `r8` is non-null walks the 16-byte entries from qword `rcx+0x20` (count: dword `rcx+0x18` with its top bit cleared, `btr 0x1f`), following each entry's chain from qword `+8` through qword `+0x78` links, and when it meets `r8` copies that 16-byte entry to `[rdx]`; when `r8` is null or not found it zeroes qword `[rdx]` and stores `006372A0()` to qword `rdx+8`; returns `rdx` | `006AF505`, `006AF520`, `006AF525`, `006AF53E`, `006AF557` |
| `006CEE50` | 79 B | calls `006372B0` with the incoming registers, builds a stack pair (the address `00D2D310`, that result) and calls slot `+0x78` of `rcx`'s vtable with `rcx`, `rdx` and the pair's address; returns `al` = 1 | `006CEE6A`, `006CEE7B`, `006CEE8E`, `006CEE92` |
| `006D9E30` | 79 B | calls `006372B0` with the incoming registers, builds a stack pair (the address `00D2D310`, that result) and calls slot `+0x78` of `rcx`'s vtable with `rcx`, `rdx` and the pair's address; returns `al` = 1 | `006D9E4A`, `006D9E5B`, `006D9E6E`, `006D9E72` |

## Per-member rows: which reflected data member each metadata teardown destroys (OPUS, 2026-10-03)

The family `PDataMemberMetadata static teardowns` (frontmatter: 853 members; 803 get a row here) shares one 12-byte form, shown in section 2 and not repeated per row: `lea rcx, [X]` then a tail jump to a `PClassDataMember` destructor helper (`00633240`, or 006332A0 for members registered through the array constructor). Members differ only at that first instruction, the static object X, so the anchor is the entry `lea` itself (SWE2-AUDIT-SPEC's family sentence, as adopted by OPUS in `opus-ee-rulings-1003`, allows the entry instruction when members differ there). Each row states X and the data member X describes. Both are read from the image: the one registration that loads X with `lea rcx, [X]` immediately before a call to a data-member constructor (`00632960`, or the array form `00632A10`) is decoded from its function's own entry; the `lea r9` there is the member's name and an immediate `mov dword ptr [rsp + 0x20]` its offset (given as passed in a register otherwise). [`fam_rows.py`](../../_index/candidates/opus-ee-metadata-teardowns-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-metadata-teardowns-1003/rows.tsv). A body that leaves the form, a registration that is not unique or unnamed, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members without a unique named registration get no row; they are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-metadata-teardowns-1003/excluded.tsv).

### Registered through constructor `00632960` (641, OPUS)

| member | distinguishing instruction | static object X | the data member X describes |
|---|---|---|---|
| 008AA000 | `008AA000` `lea` | `02CB0A40` | member "m_animationSet", offset 0x20 (constructor 00632960, called at 005AD994) |
| 008AA010 | `008AA010` `lea` | `02CB2700` | member "m_animationSet", offset 0x10 (constructor 00632960, called at 005B0E38) |
| 008AA020 | `008AA020` `lea` | `02CB0B70` | member "m_animationTargetBlenderController", offset 0x70 (constructor 00632960, called at 005ADB11) |
| 008AA030 | `008AA030` `lea` | `02CB0B10` | member "m_animationWeightedBlenderController", offset 0x38 (constructor 00632960, called at 005ADA9F) |
| 008AA040 | `008AA040` `lea` | `02CB1A50` | member "m_baseObject", offset 0x18 (constructor 00632960, called at 005AF8C7) |
| 008AA050 | `008AA050` `lea` | `02CB19F0` | member "m_baseObjectType", offset 0x10 (constructor 00632960, called at 005AF854) |
| 008AA060 | `008AA060` `lea` | `02CB2210` | member "m_binding", offset passed in a register (constructor 00632960, called at 005B064A) |
| 008AA070 | `008AA070` `lea` | `02CB24B0` | member "m_channelCount", offset 0x2 (constructor 00632960, called at 005B0808) |
| 008AA090 | `008AA090` `lea` | `02CB2510` | member "m_constantChannelCount", offset 0x4 (constructor 00632960, called at 005B087B) |
| 008AA0A0 | `008AA0A0` `lea` | `02CB21B0` | member "m_constantChannelEndTime", offset 0x2C (constructor 00632960, called at 005B05DC) |
| 008AA0B0 | `008AA0B0` `lea` | `02CB2150` | member "m_constantChannelStartTime", offset 0x28 (constructor 00632960, called at 005B0569) |
| 008AA0D0 | `008AA0D0` `lea` | `02CB3C60` | member "m_count", offset passed in a register (constructor 00632960, called at 005B4F9A) |
| 008AA0E0 | `008AA0E0` `lea` | `02CB3A30` | member "m_count", offset passed in a register (constructor 00632960, called at 005B52CA) |
| 008AA0F0 | `008AA0F0` `lea` | `02CB40C0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B55FA) |
| 008AA100 | `008AA100` `lea` | `02CB5010` | member "m_count", offset passed in a register (constructor 00632960, called at 005B593A) |
| 008AA110 | `008AA110` `lea` | `02CB4750` | member "m_count", offset passed in a register (constructor 00632960, called at 005B5C7A) |
| 008AA120 | `008AA120` `lea` | `02CB42F0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B5FAA) |
| 008AA130 | `008AA130` `lea` | `02CB5240` | member "m_count", offset passed in a register (constructor 00632960, called at 005B62DA) |
| 008AA140 | `008AA140` `lea` | `02CB4BB0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B660A) |
| 008AA150 | `008AA150` `lea` | `02CB5470` | member "m_count", offset passed in a register (constructor 00632960, called at 005B693A) |
| 008AA160 | `008AA160` `lea` | `02CB56A0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B6C6A) |
| 008AA170 | `008AA170` `lea` | `02CB4DE0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B6F9A) |
| 008AA180 | `008AA180` `lea` | `02CB4980` | member "m_count", offset passed in a register (constructor 00632960, called at 005B72CA) |
| 008AA190 | `008AA190` `lea` | `02CB58D0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B75FA) |
| 008AA1A0 | `008AA1A0` `lea` | `02CB3E90` | member "m_count", offset passed in a register (constructor 00632960, called at 005B792A) |
| 008AA1B0 | `008AA1B0` `lea` | `02CB45A0` | member "m_count", offset passed in a register (constructor 00632960, called at 005B7D28) |
| 008AA1C0 | `008AA1C0` `lea` | `02CB29C0` | member "m_dataSource", offset passed in a register (constructor 00632960, called at 005B0EFD) |
| 008AA1E0 | `008AA1E0` `lea` | `02CB2AF0` | member "m_destSlotArray", offset 0x8C (constructor 00632960, called at 005B1058) |
| 008AA1F0 | `008AA1F0` `lea` | `02CB22D0` | member "m_destSlotArrayIndex", offset passed in a register (constructor 00632960, called at 005B09C5) |
| 008AA2F0 | `008AA2F0` `lea` | `02CB2880` | member "m_id", offset 0x4 (constructor 00632960, called at 005B1281) |
| 008AA300 | `008AA300` `lea` | `02CB1B80` | member "m_index", offset 0x30 (constructor 00632960, called at 005AFA1E) |
| 008AA310 | `008AA310` `lea` | `02CB2A20` | member "m_inputCount", offset 0x8 (constructor 00632960, called at 005B0F70) |
| 008AA330 | `008AA330` `lea` | `02CB1990` | member "m_instanceObject", offset 0x8 (constructor 00632960, called at 005AF7E2) |
| 008AA340 | `008AA340` `lea` | `02CB1930` | member "m_instanceObjectType", offset passed in a register (constructor 00632960, called at 005AF76F) |
| 008AA370 | `008AA370` `lea` | `02CB2330` | member "m_interp", offset 0x2 (constructor 00632960, called at 005B0A38) |
| 008AA390 | `008AA390` `lea` | `02CB2570` | member "m_interpCountLength", offset 0x6 (constructor 00632960, called at 005B08EE) |
| 008AA3A0 | `008AA3A0` `lea` | `02CB1680` | member "m_keyCount", offset 0x60 (constructor 00632960, called at 005AF242) |
| 008AA3B0 | `008AA3B0` `lea` | `02CB1C50` | member "m_keyCount", offset passed in a register (constructor 00632960, called at 005AFB8C) |
| 008AA3C0 | `008AA3C0` `lea` | `02CB16E0` | member "m_keyType", offset 0x38 (constructor 00632960, called at 005AF30D) |
| 008AA3D0 | `008AA3D0` `lea` | `02CB32F0` | member "m_keyType", offset passed in a register (constructor 00632960, called at 005B201E) |
| 008AA3E0 | `008AA3E0` `lea` | `02CB3740` | member "m_localBase", offset 0x1C (constructor 00632960, called at 005B2B07) |
| 008AA3F0 | `008AA3F0` `lea` | `02CB37A0` | member "m_localRange", offset 0x20 (constructor 00632960, called at 005B2B7A) |
| 008AA400 | `008AA400` `lea` | `02CB1B20` | member "m_name", offset 0x28 (constructor 00632960, called at 005AF9AB) |
| 008AA410 | `008AA410` `lea` | `02CB2270` | member "m_name", offset 0x30 (constructor 00632960, called at 005B06BC) |
| 008AA420 | `008AA420` `lea` | `02CB3290` | member "m_nodeCentricReIndex", offset 0x10 (constructor 00632960, called at 005B22B6) |
| 008AA430 | `008AA430` `lea` | `02CB3350` | member "m_nodeName", offset 0x8 (constructor 00632960, called at 005B2090) |
| 008AA440 | `008AA440` `lea` | `02CB38C0` | member "m_offset", offset 0x1C (constructor 00632960, called at 005B2D27) |
| 008AA450 | `008AA450` `lea` | `02CB3680` | member "m_parent", offset 0x10 (constructor 00632960, called at 005B2A21) |
| 008AA460 | `008AA460` `lea` | `02CB3800` | member "m_parent", offset 0x10 (constructor 00632960, called at 005B2C41) |
| 008AA470 | `008AA470` `lea` | `02CB36E0` | member "m_parentBase", offset 0x18 (constructor 00632960, called at 005B2A94) |
| 008AA490 | `008AA490` `lea` | `02CB2B50` | member "m_persistentBufferOffset", offset 0x90 (constructor 00632960, called at 005B10CB) |
| 008AA4A0 | `008AA4A0` `lea` | `02CB2BB0` | member "m_preprocessBufferOffset", offset 0x94 (constructor 00632960, called at 005B113E) |
| 008AA4B0 | `008AA4B0` `lea` | `02CB2E20` | member "m_preprocessBufferSize", offset 0x50 (constructor 00632960, called at 005B1827) |
| 008AA4C0 | `008AA4C0` `lea` | `02CB3860` | member "m_scale", offset 0x18 (constructor 00632960, called at 005B2CB4) |
| 008AA4D0 | `008AA4D0` `lea` | `02CB2D50` | member "m_slotArrayElementsRequired", offset 0x38 (constructor 00632960, called at 005B1716) |
| 008AA510 | `008AA510` `lea` | `02CB2390` | member "m_sourceChannelIndex", offset 0x14 (constructor 00632960, called at 005B0B09) |
| 008AA550 | `008AA550` `lea` | `02CB0980` | member "m_speed", offset 0xC (constructor 00632960, called at 005B27B6) |
| 008AA560 | `008AA560` `lea` | `02CB2450` | member "m_spuBindingSize", offset passed in a register (constructor 00632960, called at 005B0795) |
| 008AA570 | `008AA570` `lea` | `02CB2CF0` | member "m_targetBlender", offset 0x30 (constructor 00632960, called at 005B16A3) |
| 008AA580 | `008AA580` `lea` | `02CB3230` | member "m_targetIndex", offset 0xC (constructor 00632960, called at 005B2243) |
| 008AA5A0 | `008AA5A0` `lea` | `02CB2820` | member "m_time", offset passed in a register (constructor 00632960, called at 005B120E) |
| 008AA5B0 | `008AA5B0` `lea` | `02CB26A0` | member "m_timeController", offset 0x20 (constructor 00632960, called at 005B0D73) |
| 008AA5C0 | `008AA5C0` `lea` | `02CB27C0` | member "m_timeController", offset 0x20 (constructor 00632960, called at 005B13C3) |
| 008AA5D0 | `008AA5D0` `lea` | `02CB0860` | member "m_timeIntervalController", offset 0x10 (constructor 00632960, called at 005B265F) |
| 008AA5F0 | `008AA5F0` `lea` | `02CB08C0` | member "m_timeScaleOffsetController", offset 0x38 (constructor 00632960, called at 005B26D1) |
| 008AA600 | `008AA600` `lea` | `02CB15B0` | member "m_times", offset 0x48 (constructor 00632960, called at 005AF131) |
| 008AA650 | `008AA650` `lea` | `02CB23F0` | member "m_valueWidthAndKeyCount", offset 0x10 (constructor 00632960, called at 005B0B7C) |
| 008AA660 | `008AA660` `lea` | `02CB09E0` | member "m_weight", offset 0x8 (constructor 00632960, called at 005B2829) |
| 008AD010 | `008AD010` `lea` | `02CE3D10` | member "m_alphaThreshold", offset 0x74 (constructor 00632960, called at 005E5C12) |
| 008AD020 | `008AD020` `lea` | `02CE8640` | member "m_arrayElementCount", offset passed in a register (constructor 00632960, called at 005E9856) |
| 008AD030 | `008AD030` `lea` | `02CE73C0` | member "m_baseLevel", offset 0x14 (constructor 00632960, called at 005E74A5) |
| 008AD040 | `008AD040` `lea` | `02CE7360` | member "m_borderColor", offset 0x10 (constructor 00632960, called at 005E7432) |
| 008AD050 | `008AD050` `lea` | `02CE3940` | member "m_bounds", offset 0x38 (constructor 00632960, called at 005E576F) |
| 008AD060 | `008AD060` `lea` | `02CE86A0` | member "m_bufferLoc", offset 0x10 (constructor 00632960, called at 005E98C4) |
| 008AD070 | `008AD070` `lea` | `02CE96E0` | member "m_bufferLoc", offset 0x10 (constructor 00632960, called at 005EA985) |
| 008AD080 | `008AD080` `lea` | `02CE9350` | member "m_code", offset passed in a register (constructor 00632960, called at 005EA5ED) |
| 008AD0A0 | `008AD0A0` `lea` | `02CE7E30` | member "m_computeEntryPoint", offset 0x18 (constructor 00632960, called at 005E9F40) |
| 008AD0B0 | `008AD0B0` `lea` | `02CE7E90` | member "m_computeProfile", offset 0x2C (constructor 00632960, called at 005E9FAF) |
| 008AD0C0 | `008AD0C0` `lea` | `02CE8A40` | member "m_computeProgram", offset 0x18 (constructor 00632960, called at 005E9B53) |
| 008AD0D0 | `008AD0D0` `lea` | `02CE8C90` | member "m_constantBuffer", offset 0x10 (constructor 00632960, called at 005E964F) |
| 008AD0E0 | `008AD0E0` `lea` | `02CE8400` | member "m_constantBufferLocation", offset 0x4 (constructor 00632960, called at 005E8A4E) |
| 008AD0F0 | `008AD0F0` `lea` | `02CE8700` | member "m_constantBufferLocation", offset 0x14 (constructor 00632960, called at 005E9933) |
| 008AD110 | `008AD110` `lea` | `02CE8070` | member "m_contextVariantCsIndex", offset 0x10 (constructor 00632960, called at 005E3E76) |
| 008AD120 | `008AD120` `lea` | `02CE7FB0` | member "m_contextVariantFpIndex", offset 0x8 (constructor 00632960, called at 005E3D98) |
| 008AD130 | `008AD130` `lea` | `02CE8010` | member "m_contextVariantGsIndex", offset 0xC (constructor 00632960, called at 005E3E07) |
| 008AD140 | `008AD140` `lea` | `02CE7EF0` | member "m_contextVariantIndex", offset passed in a register (constructor 00632960, called at 005E3CBA) |
| 008AD160 | `008AD160` `lea` | `02CE7F50` | member "m_contextVariantVpIndex", offset 0x4 (constructor 00632960, called at 005E3D29) |
| 008AD170 | `008AD170` `lea` | `02CEBFB0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EB95A) |
| 008AD180 | `008AD180` `lea` | `02CECF00` | member "m_count", offset passed in a register (constructor 00632960, called at 005EBC9A) |
| 008AD190 | `008AD190` `lea` | `02CEBD80` | member "m_count", offset passed in a register (constructor 00632960, called at 005EBFDA) |
| 008AD1A0 | `008AD1A0` `lea` | `02CEC640` | member "m_count", offset passed in a register (constructor 00632960, called at 005EC31A) |
| 008AD1B0 | `008AD1B0` `lea` | `02CEC1E0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EC65A) |
| 008AD1C0 | `008AD1C0` `lea` | `02CEC410` | member "m_count", offset passed in a register (constructor 00632960, called at 005EC99A) |
| 008AD1D0 | `008AD1D0` `lea` | `02CEB6F0` | member "m_count", offset passed in a register (constructor 00632960, called at 005ECCDA) |
| 008AD1E0 | `008AD1E0` `lea` | `02CEB920` | member "m_count", offset passed in a register (constructor 00632960, called at 005ED00A) |
| 008AD1F0 | `008AD1F0` `lea` | `02CEA110` | member "m_count", offset passed in a register (constructor 00632960, called at 005ED33A) |
| 008AD200 | `008AD200` `lea` | `02CECCD0` | member "m_count", offset passed in a register (constructor 00632960, called at 005ED66A) |
| 008AD210 | `008AD210` `lea` | `02CEC870` | member "m_count", offset passed in a register (constructor 00632960, called at 005ED99A) |
| 008AD220 | `008AD220` `lea` | `02CEBB50` | member "m_count", offset passed in a register (constructor 00632960, called at 005EDCCA) |
| 008AD230 | `008AD230` `lea` | `02CEB290` | member "m_count", offset passed in a register (constructor 00632960, called at 005EDFFA) |
| 008AD240 | `008AD240` `lea` | `02CEAC00` | member "m_count", offset passed in a register (constructor 00632960, called at 005EE32A) |
| 008AD250 | `008AD250` `lea` | `02CEA7A0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EE65A) |
| 008AD260 | `008AD260` `lea` | `02CEA9D0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EE98A) |
| 008AD270 | `008AD270` `lea` | `02CEA570` | member "m_count", offset passed in a register (constructor 00632960, called at 005EECBA) |
| 008AD280 | `008AD280` `lea` | `02CEAE30` | member "m_count", offset passed in a register (constructor 00632960, called at 005EEFEA) |
| 008AD290 | `008AD290` `lea` | `02CEB4C0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EF31A) |
| 008AD2A0 | `008AD2A0` `lea` | `02CEA340` | member "m_count", offset passed in a register (constructor 00632960, called at 005EF64A) |
| 008AD2B0 | `008AD2B0` `lea` | `02CE9EE0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EF97A) |
| 008AD2C0 | `008AD2C0` `lea` | `02CEB0E0` | member "m_count", offset passed in a register (constructor 00632960, called at 005EFD76) |
| 008AD2D0 | `008AD2D0` `lea` | `02CECB20` | member "m_count", offset passed in a register (constructor 00632960, called at 005F00C8) |
| 008AD2E0 | `008AD2E0` `lea` | `02CE3CB0` | member "m_cubeMapFactor", offset 0x70 (constructor 00632960, called at 005E5B9F) |
| 008AD2F0 | `008AD2F0` `lea` | `02CE3C50` | member "m_cubeMapIntensity", offset 0x6C (constructor 00632960, called at 005E5B2C) |
| 008AD310 | `008AD310` `lea` | `02CE9050` | member "m_dataBlock", offset 0x18 (constructor 00632960, called at 005E85DA) |
| 008AD320 | `008AD320` `lea` | `02CE91D0` | member "m_dataBlock", offset 0x10 (constructor 00632960, called at 005E869F) |
| 008AD330 | `008AD330` `lea` | `02CE8ED0` | member "m_dataBlock", offset 0x18 (constructor 00632960, called at 005E919A) |
| 008AD340 | `008AD340` `lea` | `02CE85E0` | member "m_dataType", offset 0x3 (constructor 00632960, called at 005E97EB) |
| 008AD350 | `008AD350` `lea` | `02CE9620` | member "m_dataType", offset 0x16 (constructor 00632960, called at 005EA8A4) |
| 008AD360 | `008AD360` `lea` | `02CE9CE0` | member "m_depth", offset 0x30 (constructor 00632960, called at 005EAF08) |
| 008AD370 | `008AD370` `lea` | `02CE4190` | member "m_destination", offset passed in a register (constructor 00632960, called at 005E648D) |
| 008AD380 | `008AD380` `lea` | `02CE2680` | member "m_dynamicMesh", offset 0x8 (constructor 00632960, called at 005E3F38) |
| 008AD390 | `008AD390` `lea` | `02CE38E0` | member "m_dynamicMeshInstance", offset 0x30 (constructor 00632960, called at 005E56FD) |
| 008AD3A0 | `008AD3A0` `lea` | `02CE2BB0` | member "m_effect", offset passed in a register (constructor 00632960, called at 005E4642) |
| 008AD3B0 | `008AD3B0` `lea` | `02CE27A0` | member "m_effectFile", offset 0x8 (constructor 00632960, called at 005E40D7) |
| 008AD3C0 | `008AD3C0` `lea` | `02CE2800` | member "m_effectFileFromBasePath", offset 0x10 (constructor 00632960, called at 005E4145) |
| 008AD3D0 | `008AD3D0` `lea` | `02CE2860` | member "m_effectSource", offset 0x68 (constructor 00632960, called at 005E41B3) |
| 008AD3E0 | `008AD3E0` `lea` | `02CE3020` | member "m_effectVariant", offset passed in a register (constructor 00632960, called at 005E4B37) |
| 008AD3F0 | `008AD3F0` `lea` | `02CE4590` | member "m_effectVariant", offset 0x8 (constructor 00632960, called at 005E6DA2) |
| 008AD410 | `008AD410` `lea` | `02CE9800` | member "m_elementCount", offset passed in a register (constructor 00632960, called at 005EAB2E) |
| 008AD420 | `008AD420` `lea` | `02CE9860` | member "m_elementSize", offset 0x4 (constructor 00632960, called at 005EABA1) |
| 008AD580 | `008AD580` `lea` | `02CE93B0` | member "m_entry", offset 0x8 (constructor 00632960, called at 005EA65F) |
| 008AD5A0 | `008AD5A0` `lea` | `02CE3AD0` | member "m_extraFlag", offset 0x5C (constructor 00632960, called at 005E5960) |
| 008AD5B0 | `008AD5B0` `lea` | `02CE3B30` | member "m_extraZBias", offset 0x60 (constructor 00632960, called at 005E59D3) |
| 008AD5C0 | `008AD5C0` `lea` | `02CE3B90` | member "m_farPlane", offset 0x64 (constructor 00632960, called at 005E5A46) |
| 008AD5D0 | `008AD5D0` `lea` | `02CE30E0` | member "m_flag", offset 0x10 (constructor 00632960, called at 005E4C18) |
| 008AD5E0 | `008AD5E0` `lea` | `02CE3A70` | member "m_flags", offset 0x58 (constructor 00632960, called at 005E58ED) |
| 008AD5F0 | `008AD5F0` `lea` | `02CE7480` | member "m_flags", offset 0x1C (constructor 00632960, called at 005E758B) |
| 008AD600 | `008AD600` `lea` | `02CE98C0` | member "m_flags", offset 0x8 (constructor 00632960, called at 005EAC14) |
| 008AD610 | `008AD610` `lea` | `02CE9920` | member "m_format", offset passed in a register (constructor 00632960, called at 005EAFD3) |
| 008AD620 | `008AD620` `lea` | `02CE7CB0` | member "m_fragmentEntryPoint", offset 0x8 (constructor 00632960, called at 005E9D86) |
| 008AD630 | `008AD630` `lea` | `02CE7D10` | member "m_fragmentProfile", offset 0x24 (constructor 00632960, called at 005E9DF5) |
| 008AD640 | `008AD640` `lea` | `02CE8980` | member "m_fragmentProgram", offset 0x8 (constructor 00632960, called at 005E9A6F) |
| 008AD650 | `008AD650` `lea` | `02CE7D70` | member "m_geometryEntryPoint", offset 0x10 (constructor 00632960, called at 005E9E63) |
| 008AD660 | `008AD660` `lea` | `02CE7DD0` | member "m_geometryProfile", offset 0x28 (constructor 00632960, called at 005E9ED2) |
| 008AD670 | `008AD670` `lea` | `02CE89E0` | member "m_geometryProgram", offset 0x10 (constructor 00632960, called at 005E9AE1) |
| 008AD680 | `008AD680` `lea` | `02CE9BC0` | member "m_height", offset 0x2C (constructor 00632960, called at 005EAD55) |
| 008AD690 | `008AD690` `lea` | `02CE9C80` | member "m_height", offset 0x2C (constructor 00632960, called at 005EAE95) |
| 008AD6A0 | `008AD6A0` `lea` | `02CE8B10` | member "m_importantState", offset passed in a register (constructor 00632960, called at 005EA395) |
| 008AD6B0 | `008AD6B0` `lea` | `02CE35C0` | member "m_index", offset 0x12 (constructor 00632960, called at 005E6A96) |
| 008AD6C0 | `008AD6C0` `lea` | `02CE97A0` | member "m_index", offset 0x17 (constructor 00632960, called at 005EAA6B) |
| 008AD6D0 | `008AD6D0` `lea` | `02CE9230` | member "m_indexDataBlock", offset 0x10 (constructor 00632960, called at 005E875F) |
| 008AD6E0 | `008AD6E0` `lea` | `02CE3620` | member "m_inputSet", offset 0x13 (constructor 00632960, called at 005E6B09) |
| 008AD6F0 | `008AD6F0` `lea` | `02CE3880` | member "m_instanceSegment", offset 0x28 (constructor 00632960, called at 005E568B) |
| 008AD700 | `008AD700` `lea` | `02CE2D60` | member "m_largestShaderPassCount", offset 0x38 (constructor 00632960, called at 005E4867) |
| 008AD710 | `008AD710` `lea` | `02CE3750` | member "m_localToWorldMatrix", offset 0x8 (constructor 00632960, called at 005E5509) |
| 008AD720 | `008AD720` `lea` | `02CE72A0` | member "m_lodBias", offset 0x8 (constructor 00632960, called at 005E734C) |
| 008AD730 | `008AD730` `lea` | `02CE39A0` | member "m_lodLevel", offset 0x40 (constructor 00632960, called at 005E57E1) |
| 008AD740 | `008AD740` `lea` | `02CE7120` | member "m_magFilter", offset 0x1 (constructor 00632960, called at 005E7180) |
| 008AD750 | `008AD750` `lea` | `02CE3820` | member "m_materialSet", offset 0x20 (constructor 00632960, called at 005E5619) |
| 008AD760 | `008AD760` `lea` | `02CE7300` | member "m_maxAnisotropy", offset 0xC (constructor 00632960, called at 005E73BF) |
| 008AD770 | `008AD770` `lea` | `02CE7420` | member "m_maxLevel", offset 0x18 (constructor 00632960, called at 005E7518) |
| 008AD780 | `008AD780` `lea` | `02CE2AF0` | member "m_maxLightCount", offset 0x70 (constructor 00632960, called at 005E450B) |
| 008AD790 | `008AD790` `lea` | `02CE9A40` | member "m_maxMipLevel", offset 0x14 (constructor 00632960, called at 005EB12C) |
| 008AD7A0 | `008AD7A0` `lea` | `02CE9980` | member "m_memoryType", offset 0x9 (constructor 00632960, called at 005EB046) |
| 008AD7B0 | `008AD7B0` `lea` | `02CE36F0` | member "m_mesh", offset passed in a register (constructor 00632960, called at 005E5497) |
| 008AD7C0 | `008AD7C0` `lea` | `02CE42B0` | member "m_meshInstance", offset 0x28 (constructor 00632960, called at 005E6641) |
| 008AD7E0 | `008AD7E0` `lea` | `02CE70C0` | member "m_minFilter", offset passed in a register (constructor 00632960, called at 005E710D) |
| 008AD7F0 | `008AD7F0` `lea` | `02CE99E0` | member "m_mipmapCount", offset 0x10 (constructor 00632960, called at 005EB0B9) |
| 008AD810 | `008AD810` `lea` | `02CE4660` | member "m_msaaType", offset 0x9 (constructor 00632960, called at 005E6FC2) |
| 008AD820 | `008AD820` `lea` | `02CE2F60` | member "m_name", offset passed in a register (constructor 00632960, called at 005E5359) |
| 008AD830 | `008AD830` `lea` | `02CE3E30` | member "m_name", offset 0x80 (constructor 00632960, called at 005E5D6A) |
| 008AD840 | `008AD840` `lea` | `02CE3500` | member "m_name", offset 0x8 (constructor 00632960, called at 005E69B0) |
| 008AD850 | `008AD850` `lea` | `02CE8520` | member "m_name", offset 0x8 (constructor 00632960, called at 005E970D) |
| 008AD860 | `008AD860` `lea` | `02CE95C0` | member "m_name", offset 0x8 (constructor 00632960, called at 005EA831) |
| 008AD870 | `008AD870` `lea` | `02CE3560` | member "m_nameHash", offset 0x10 (constructor 00632960, called at 005E6A23) |
| 008AD880 | `008AD880` `lea` | `02CE9740` | member "m_nameHash", offset 0x14 (constructor 00632960, called at 005EA9F8) |
| 008AD890 | `008AD890` `lea` | `02CE2B50` | member "m_numSupportedShaderLODLevels", offset 0x74 (constructor 00632960, called at 005E457A) |
| 008AD8A0 | `008AD8A0` `lea` | `02CE82E0` | member "m_offset", offset passed in a register (constructor 00632960, called at 005E8811) |
| 008AD8C0 | `008AD8C0` `lea` | `02CE3080` | member "m_parameterBuffer", offset 0x8 (constructor 00632960, called at 005E4BA9) |
| 008AD8D0 | `008AD8D0` `lea` | `02CE8280` | member "m_parameterBufferFrequenciesRequired", offset passed in a register (constructor 00632960, called at 005E848F) |
| 008AD8E0 | `008AD8E0` `lea` | `02CE4530` | member "m_parameterBufferSize", offset passed in a register (constructor 00632960, called at 005E6EF8) |
| 008AD8F0 | `008AD8F0` `lea` | `02CE8220` | member "m_parameterBufferSize", offset 0x38 (constructor 00632960, called at 005E8424) |
| 008AD960 | `008AD960` `lea` | `02CE8B70` | member "m_parameterType", offset passed in a register (constructor 00632960, called at 005E93E5) |
| 008AD970 | `008AD970` `lea` | `02CE8580` | member "m_parameterType", offset 0x2 (constructor 00632960, called at 005E977C) |
| 008AD980 | `008AD980` `lea` | `02CE7970` | member "m_passType", offset passed in a register (constructor 00632960, called at 005E7EEE) |
| 008AD9B0 | `008AD9B0` `lea` | `02CE7B90` | member "m_platformsAreInclude", offset 0x48 (constructor 00632960, called at 005E81A5) |
| 008AD9C0 | `008AD9C0` `lea` | `02CE9480` | member "m_profile", offset 0x20 (constructor 00632960, called at 005EA76B) |
| 008AD9D0 | `008AD9D0` `lea` | `02CE3140` | member "m_remapFrom", offset 0x18 (constructor 00632960, called at 005E4C8B) |
| 008AD9E0 | `008AD9E0` `lea` | `02CE31A0` | member "m_remapTo", offset 0x20 (constructor 00632960, called at 005E4CFE) |
| 008AD9F0 | `008AD9F0` `lea` | `02CE34A0` | member "m_renderDataType", offset passed in a register (constructor 00632960, called at 005E693E) |
| 008ADA00 | `008ADA00` `lea` | `02CE46C0` | member "m_renderTargetFlags", offset 0xC (constructor 00632960, called at 005E7035) |
| 008ADA10 | `008ADA10` `lea` | `02CE9680` | member "m_renderType", offset passed in a register (constructor 00632960, called at 005EA913) |
| 008ADA20 | `008ADA20` `lea` | `02CE9110` | member "m_rwDataBlock", offset 0x18 (constructor 00632960, called at 005E8C6A) |
| 008ADA30 | `008ADA30` `lea` | `02CE8F90` | member "m_rwDataBlock", offset 0x18 (constructor 00632960, called at 005E8E1A) |
| 008ADA40 | `008ADA40` `lea` | `02CE9170` | member "m_rwIndirectArgsBuffer", offset 0x20 (constructor 00632960, called at 005E8CDC) |
| 008ADA50 | `008ADA50` `lea` | `02CE90B0` | member "m_rwStructuredBuffer", offset 0x10 (constructor 00632960, called at 005E8BF8) |
| 008ADA60 | `008ADA60` `lea` | `02CE8F30` | member "m_rwStructuredBuffer", offset 0x10 (constructor 00632960, called at 005E8DA8) |
| 008ADA70 | `008ADA70` `lea` | `02CE8BD0` | member "m_samplerState", offset 0x8 (constructor 00632960, called at 005E9457) |
| 008ADAC0 | `008ADAC0` `lea` | `02CE2620` | member "m_size", offset passed in a register (constructor 00632960, called at 005E3BF5) |
| 008ADAE0 | `008ADAE0` `lea` | `02CE8340` | member "m_size", offset 0x2 (constructor 00632960, called at 005E88C5) |
| 008ADAF0 | `008ADAF0` `lea` | `02CE8460` | member "m_size", offset 0x8 (constructor 00632960, called at 005E8ABD) |
| 008ADB00 | `008ADB00` `lea` | `02CE9D40` | member "m_size", offset 0x28 (constructor 00632960, called at 005EB339) |
| 008ADB10 | `008ADB10` `lea` | `02CE41F0` | member "m_source", offset 0x8 (constructor 00632960, called at 005E64FF) |
| 008ADB20 | `008ADB20` `lea` | `02CE4250` | member "m_sourceMatrixIndex", offset 0x10 (constructor 00632960, called at 005E656E) |
| 008ADB30 | `008ADB30` `lea` | `02CE3D70` | member "m_specialRenderOrder", offset 0x78 (constructor 00632960, called at 005E5C85) |
| 008ADB40 | `008ADB40` `lea` | `02CE3DD0` | member "m_specialTextureWrapType", offset 0x7C (constructor 00632960, called at 005E5CF8) |
| 008ADB50 | `008ADB50` `lea` | `02CE3BF0` | member "m_specularIntensity", offset 0x68 (constructor 00632960, called at 005E5AB9) |
| 008ADBA0 | `008ADBA0` `lea` | `02CE8FF0` | member "m_structuredBuffer", offset 0x10 (constructor 00632960, called at 005E8568) |
| 008ADBB0 | `008ADBB0` `lea` | `02CE8E70` | member "m_structuredBuffer", offset 0x10 (constructor 00632960, called at 005E9128) |
| 008ADBC0 | `008ADBC0` `lea` | `02CE26E0` | member "m_supportedLightMask", offset passed in a register (constructor 00632960, called at 005E3FFA) |
| 008ADBE0 | `008ADBE0` `lea` | `02CE2740` | member "m_supportedShadowCasterMask", offset 0x4 (constructor 00632960, called at 005E4069) |
| 008ADC10 | `008ADC10` `lea` | `02CE9290` | member "m_texture", offset 0x10 (constructor 00632960, called at 005E8EDF) |
| 008ADC20 | `008ADC20` `lea` | `02CE92F0` | member "m_texture", offset 0x10 (constructor 00632960, called at 005E8F9F) |
| 008ADC30 | `008ADC30` `lea` | `02CE8CF0` | member "m_texture", offset 0x10 (constructor 00632960, called at 005E925F) |
| 008ADC40 | `008ADC40` `lea` | `02CE8D50` | member "m_texture", offset 0x10 (constructor 00632960, called at 005E931F) |
| 008ADC50 | `008ADC50` `lea` | `02CE8DB0` | member "m_texture", offset 0x10 (constructor 00632960, called at 005E958F) |
| 008ADC60 | `008ADC60` `lea` | `02CE8C30` | member "m_textureBufferIndex", offset 0x4 (constructor 00632960, called at 005E94CA) |
| 008ADC70 | `008ADC70` `lea` | `02CE9AA0` | member "m_textureFlags", offset 0x18 (constructor 00632960, called at 005EB19F) |
| 008ADC80 | `008ADC80` `lea` | `02CE2EA0` | member "m_tweakableParameterBufferSize", offset 0x60 (constructor 00632960, called at 005E49F3) |
| 008ADCB0 | `008ADCB0` `lea` | `02CE83A0` | member "m_type", offset 0x2 (constructor 00632960, called at 005E8985) |
| 008ADCC0 | `008ADCC0` `lea` | `02CE84C0` | member "m_type", offset 0xC (constructor 00632960, called at 005E8B2C) |
| 008ADCF0 | `008ADCF0` `lea` | `02CE2F00` | member "m_untweakableParameterBufferSize", offset 0x62 (constructor 00632960, called at 005E4A62) |
| 008ADD10 | `008ADD10` `lea` | `02CE8E10` | member "m_unusedPointer", offset 0x10 (constructor 00632960, called at 005E905F) |
| 008ADD20 | `008ADD20` `lea` | `02CE2FC0` | member "m_value", offset 0x8 (constructor 00632960, called at 005E53C7) |
| 008ADD40 | `008ADD40` `lea` | `02CE7BF0` | member "m_vertexEntryPoint", offset passed in a register (constructor 00632960, called at 005E9CA9) |
| 008ADD50 | `008ADD50` `lea` | `02CE7C50` | member "m_vertexProfile", offset 0x20 (constructor 00632960, called at 005E9D18) |
| 008ADD60 | `008ADD60` `lea` | `02CE8920` | member "m_vertexProgram", offset passed in a register (constructor 00632960, called at 005E99FD) |
| 008ADD70 | `008ADD70` `lea` | `02CE9B60` | member "m_width", offset 0x28 (constructor 00632960, called at 005EACE2) |
| 008ADD80 | `008ADD80` `lea` | `02CE9C20` | member "m_width", offset 0x28 (constructor 00632960, called at 005EAE22) |
| 008ADD90 | `008ADD90` `lea` | `02CE4310` | member "m_worldMatrix", offset 0x10 (constructor 00632960, called at 005E66B3) |
| 008ADDA0 | `008ADDA0` `lea` | `02CE7240` | member "m_wrapR", offset 0x4 (constructor 00632960, called at 005E72D9) |
| 008ADDB0 | `008ADDB0` `lea` | `02CE7180` | member "m_wrapS", offset 0x2 (constructor 00632960, called at 005E71F3) |
| 008ADDC0 | `008ADDC0` `lea` | `02CE71E0` | member "m_wrapT", offset 0x3 (constructor 00632960, called at 005E7266) |
| 008AE950 | `008AE950` `lea` | `02CF6430` | member "AlphaToCoverageEnable", offset passed in a register (constructor 00632960, called at 00613902) |
| 008AE960 | `008AE960` `lea` | `02CF5750` | member "AntialiasedLineEnable", offset 0x24 (constructor 00632960, called at 00614367) |
| 008AE970 | `008AE970` `lea` | `02CF5E50` | member "BackFace", offset 0x24 (constructor 00632960, called at 00613E39) |
| 008AE980 | `008AE980` `lea` | `02CF5FC0` | member "BlendEnable", offset passed in a register (constructor 00632960, called at 00614742) |
| 008AE9C0 | `008AE9C0` `lea` | `02CF5510` | member "DepthBias", offset 0xC (constructor 00632960, called at 006140CD) |
| 008AE9D0 | `008AE9D0` `lea` | `02CF5570` | member "DepthBiasClamp", offset 0x10 (constructor 00632960, called at 0061413C) |
| 008AE9E0 | `008AE9E0` `lea` | `02CF5630` | member "DepthClipEnable", offset 0x18 (constructor 00632960, called at 0061421A) |
| 008AE9F0 | `008AE9F0` `lea` | `02CF5B90` | member "DepthEnable", offset passed in a register (constructor 00632960, called at 00613B32) |
| 008AEA50 | `008AEA50` `lea` | `02CF54B0` | member "FrontCounterClockwise", offset 0x8 (constructor 00632960, called at 0061405E) |
| 008AEA60 | `008AEA60` `lea` | `02CF5DF0` | member "FrontFace", offset 0x14 (constructor 00632960, called at 00613DCA) |
| 008AEA70 | `008AEA70` `lea` | `02CF6490` | member "IndependentBlendEnable", offset 0x4 (constructor 00632960, called at 00613971) |
| 008AEA80 | `008AEA80` `lea` | `02CF56F0` | member "MultisampleEnable", offset 0x20 (constructor 00632960, called at 006142F8) |
| 008AEAA0 | `008AEAA0` `lea` | `02CF62C0` | member "RenderTargetWriteMask", offset 0x1C (constructor 00632960, called at 00614A45) |
| 008AEAB0 | `008AEAB0` `lea` | `02CF5690` | member "ScissorEnable", offset 0x1C (constructor 00632960, called at 00614289) |
| 008AEAC0 | `008AEAC0` `lea` | `02CF55D0` | member "SlopeScaledDepthBias", offset 0x14 (constructor 00632960, called at 006141AB) |
| 008AEB00 | `008AEB00` `lea` | `02CF5CD0` | member "StencilEnable", offset 0xC (constructor 00632960, called at 00613C7D) |
| 008AEB40 | `008AEB40` `lea` | `02CF5D30` | member "StencilReadMask", offset 0x10 (constructor 00632960, called at 00613CEC) |
| 008AEB50 | `008AEB50` `lea` | `02CF5D90` | member "StencilWriteMask", offset 0x11 (constructor 00632960, called at 00613D5B) |
| 008AEC60 | `008AEC60` `lea` | `02CF6620` | member "m_blendDesc", offset 0x60 (constructor 00632960, called at 00617FD8) |
| 008AEC80 | `008AEC80` `lea` | `02CF50E0` | member "m_computeParameterLocation", offset 0x220 (constructor 00632960, called at 00617C59) |
| 008AEC90 | `008AEC90` `lea` | `02CF5260` | member "m_computeTexParameterLocation", offset 0x2A0 (constructor 00632960, called at 00617E21) |
| 008AECA0 | `008AECA0` `lea` | `02CF69A0` | member "m_constantBufferSize", offset 0x28 (constructor 00632960, called at 006181B0) |
| 008AECB0 | `008AECB0` `lea` | `02CF6D50` | member "m_count", offset passed in a register (constructor 00632960, called at 00618B0A) |
| 008AECC0 | `008AECC0` `lea` | `02CF6F80` | member "m_count", offset passed in a register (constructor 00632960, called at 00618E3A) |
| 008AECD0 | `008AECD0` `lea` | `02CF6800` | member "m_d3dFormat", offset 0x14 (constructor 00632960, called at 00618576) |
| 008AECE0 | `008AECE0` `lea` | `02CF65C0` | member "m_depthDesc", offset 0x2C (constructor 00632960, called at 00617F65) |
| 008AECF0 | `008AECF0` `lea` | `02CF6B20` | member "m_dimX", offset 0x80 (constructor 00632960, called at 006178A2) |
| 008AED00 | `008AED00` `lea` | `02CF6B80` | member "m_dimY", offset 0x84 (constructor 00632960, called at 00617915) |
| 008AED10 | `008AED10` `lea` | `02CF6BE0` | member "m_dimZ", offset 0x88 (constructor 00632960, called at 00617988) |
| 008AED40 | `008AED40` `lea` | `02CF5020` | member "m_fragmentParameterLocation", offset 0x1E0 (constructor 00632960, called at 00617B75) |
| 008AED50 | `008AED50` `lea` | `02CF51A0` | member "m_fragmentTexParameterLocation", offset 0x260 (constructor 00632960, called at 00617D3D) |
| 008AED60 | `008AED60` `lea` | `02CF5080` | member "m_geometryParameterLocation", offset 0x200 (constructor 00632960, called at 00617BE7) |
| 008AED70 | `008AED70` `lea` | `02CF5200` | member "m_geometryTexParameterLocation", offset 0x280 (constructor 00632960, called at 00617DAF) |
| 008AED80 | `008AED80` `lea` | `02CF6A00` | member "m_globalConstantBufferIndex", offset 0x2C (constructor 00632960, called at 00618223) |
| 008AED90 | `008AED90` `lea` | `02CF6AC0` | member "m_inputLayout", offset 0x78 (constructor 00632960, called at 00618358) |
| 008AEDA0 | `008AEDA0` `lea` | `02CF6860` | member "m_inputSlot", offset 0x18 (constructor 00632960, called at 006185E9) |
| 008AEDB0 | `008AEDB0` `lea` | `02CF6560` | member "m_rasterDesc", offset 0x4 (constructor 00632960, called at 00617EF2) |
| 008AEDC0 | `008AEDC0` `lea` | `02CF6740` | member "m_renderType", offset 0x8 (constructor 00632960, called at 00618490) |
| 008AEDD0 | `008AEDD0` `lea` | `02CF66E0` | member "m_semantic", offset passed in a register (constructor 00632960, called at 0061841D) |
| 008AEDE0 | `008AEDE0` `lea` | `02CF67A0` | member "m_semanticIndex", offset 0x10 (constructor 00632960, called at 00618503) |
| 008AEDF0 | `008AEDF0` `lea` | `02CF6A60` | member "m_shaderProfile", offset 0x70 (constructor 00632960, called at 00618296) |
| 008AEE00 | `008AEE00` `lea` | `02CF4F60` | member "m_state", offset 0x30 (constructor 00632960, called at 00617A91) |
| 008AEE10 | `008AEE10` `lea` | `02CF6680` | member "m_stencilRef", offset 0x188 (constructor 00632960, called at 0061804B) |
| 008AEE30 | `008AEE30` `lea` | `02CF4FC0` | member "m_vertexParameterLocation", offset 0x1C0 (constructor 00632960, called at 00617B03) |
| 008AEE40 | `008AEE40` `lea` | `02CF5140` | member "m_vertexTexParameterLocation", offset 0x240 (constructor 00632960, called at 00617CCB) |
| 008B08D0 | `008B08D0` `lea` | `02D370C0` | member "m_ambientColor", offset 0x40D0 (constructor 00632960, called at 0064892E) |
| 008B08E0 | `008B08E0` `lea` | `02D37C60` | member "m_asymmetry", offset 0x8C (constructor 00632960, called at 0064826C) |
| 008B08F0 | `008B08F0` `lea` | `02D37C00` | member "m_atmosphereStart", offset 0x88 (constructor 00632960, called at 006481FD) |
| 008B0900 | `008B0900` `lea` | `02D37D20` | member "m_betaM", offset 0xA0 (constructor 00632960, called at 0064834A) |
| 008B0910 | `008B0910` `lea` | `02D37CC0` | member "m_betaR", offset 0x90 (constructor 00632960, called at 006482DB) |
| 008B0920 | `008B0920` `lea` | `02D38380` | member "m_count", offset passed in a register (constructor 00632960, called at 0064ABBA) |
| 008B0930 | `008B0930` `lea` | `02D37A00` | member "m_edgeColor", offset 0x74 (constructor 00632960, called at 0064886A) |
| 008B0940 | `008B0940` `lea` | `02D37000` | member "m_effectMaterial", offset 0x10 (constructor 00632960, called at 00649101) |
| 008B0960 | `008B0960` `lea` | `02D37060` | member "m_enabled", offset 0x41 (constructor 00632960, called at 00649170) |
| 008B0970 | `008B0970` `lea` | `02D37560` | member "m_focusBlurRange", offset 0x58 (constructor 00632960, called at 00648DDC) |
| 008B0980 | `008B0980` `lea` | `02D374A0` | member "m_focusPlaneDistance", offset 0x50 (constructor 00632960, called at 00648CFE) |
| 008B0990 | `008B0990` `lea` | `02D37500` | member "m_focusRange", offset 0x54 (constructor 00632960, called at 00648D6D) |
| 008B09A0 | `008B09A0` `lea` | `02D37300` | member "m_fogAmount", offset 0x40F8 (constructor 00632960, called at 00648BC8) |
| 008B09B0 | `008B09B0` `lea` | `02D37360` | member "m_fogColor", offset 0x40E0 (constructor 00632960, called at 00648C37) |
| 008B09C0 | `008B09C0` `lea` | `02D37240` | member "m_fogDistance", offset 0x40F0 (constructor 00632960, called at 00648AEA) |
| 008B09D0 | `008B09D0` `lea` | `02D372A0` | member "m_fogNearDistance", offset 0x40F4 (constructor 00632960, called at 00648B59) |
| 008B09E0 | `008B09E0` `lea` | `02D37F00` | member "m_fogParameters", offset 0xDC (constructor 00632960, called at 00648575) |
| 008B09F0 | `008B09F0` `lea` | `02D37940` | member "m_gamma", offset 0x60 (constructor 00632960, called at 0064878C) |
| 008B0A00 | `008B0A00` `lea` | `02D376C0` | member "m_glowAmountScale", offset 0x5C (constructor 00632960, called at 00648E9E) |
| 008B0A10 | `008B0A10` `lea` | `02D37780` | member "m_glowLuminanceScale", offset 0x64 (constructor 00632960, called at 00648F7C) |
| 008B0A20 | `008B0A20` `lea` | `02D37720` | member "m_glowLuminanceThreshold", offset 0x60 (constructor 00632960, called at 00648F0D) |
| 008B0A30 | `008B0A30` `lea` | `02D37180` | member "m_instantLightIntensity", offset 0x4108 (constructor 00632960, called at 00648A0C) |
| 008B0A40 | `008B0A40` `lea` | `02D371E0` | member "m_instantLightScatteringIntensity", offset 0x410C (constructor 00632960, called at 00648A7B) |
| 008B0A50 | `008B0A50` `lea` | `02D37120` | member "m_instantLightsEnabled", offset 0x41D0 (constructor 00632960, called at 0064899D) |
| 008B0A60 | `008B0A60` `lea` | `02D37DE0` | member "m_invHM", offset 0xC4 (constructor 00632960, called at 00648428) |
| 008B0A70 | `008B0A70` `lea` | `02D37D80` | member "m_invHR", offset 0xC0 (constructor 00632960, called at 006483B9) |
| 008B0A80 | `008B0A80` `lea` | `02D379A0` | member "m_lightColor", offset 0x64 (constructor 00632960, called at 006487FB) |
| 008B0A90 | `008B0A90` `lea` | `02D37880` | member "m_lineThickness", offset 0x58 (constructor 00632960, called at 006486AE) |
| 008B0AA0 | `008B0AA0` `lea` | `02D37AE0` | member "m_marchStepFactor", offset 0x54 (constructor 00632960, called at 0064979D) |
| 008B0AB0 | `008B0AB0` `lea` | `02D37A80` | member "m_minReflectionDirZ", offset 0x50 (constructor 00632960, called at 0064972E) |
| 008B0AD0 | `008B0AD0` `lea` | `02D37BA0` | member "m_radius", offset 0x84 (constructor 00632960, called at 0064818E) |
| 008B0AE0 | `008B0AE0` `lea` | `02D37F60` | member "m_renderDebugTextures", offset 0x61 (constructor 00632960, called at 006485E4) |
| 008B0AF0 | `008B0AF0` `lea` | `02D37EA0` | member "m_sunDir", offset 0xCC (constructor 00632960, called at 00648506) |
| 008B0B00 | `008B0B00` `lea` | `02D37E40` | member "m_sunIntensity", offset 0xC8 (constructor 00632960, called at 00648497) |
| 008B0B10 | `008B0B10` `lea` | `02D378E0` | member "m_threshold", offset 0x5C (constructor 00632960, called at 0064871D) |
| 008B0B20 | `008B0B20` `lea` | `02D37620` | member "m_velocityScale", offset 0xD10 (constructor 00632960, called at 00649035) |
| 008B1500 | `008B1500` `lea` | `02D3C9C0` | member "m_count", offset passed in a register (constructor 00632960, called at 00668C7A) |
| 008B1510 | `008B1510` `lea` | `02D3DD70` | member "m_count", offset passed in a register (constructor 00632960, called at 00668FAA) |
| 008B1520 | `008B1520` `lea` | `02D3D4B0` | member "m_count", offset passed in a register (constructor 00632960, called at 006692DA) |
| 008B1530 | `008B1530` `lea` | `02D3DFA0` | member "m_count", offset passed in a register (constructor 00632960, called at 0066960A) |
| 008B1540 | `008B1540` `lea` | `02D3D910` | member "m_count", offset passed in a register (constructor 00632960, called at 0066993A) |
| 008B1550 | `008B1550` `lea` | `02D3DB40` | member "m_count", offset passed in a register (constructor 00632960, called at 00669C6A) |
| 008B1560 | `008B1560` `lea` | `02D3D280` | member "m_count", offset passed in a register (constructor 00632960, called at 00669F9A) |
| 008B1570 | `008B1570` `lea` | `02D3CBF0` | member "m_count", offset passed in a register (constructor 00632960, called at 0066A2CA) |
| 008B1580 | `008B1580` `lea` | `02D3D760` | member "m_count", offset passed in a register (constructor 00632960, called at 0066A6C8) |
| 008B1590 | `008B1590` `lea` | `02D3CEA0` | member "m_count", offset passed in a register (constructor 00632960, called at 0066AA15) |
| 008B15A0 | `008B15A0` `lea` | `02D3D0D0` | member "m_count", offset passed in a register (constructor 00632960, called at 0066AD65) |
| 008B15C0 | `008B15C0` `lea` | `02D3B150` | member "m_dataSize", offset 0x78 (constructor 00632960, called at 00665990) |
| 008B15D0 | `008B15D0` `lea` | `02D3B020` | member "m_dataSize", offset 0x70 (constructor 00632960, called at 006664A0) |
| 008B15E0 | `008B15E0` `lea` | `02D3BFB0` | member "m_defaultMaterials", offset 0x60 (constructor 00632960, called at 00666CEA) |
| 008B1610 | `008B1610` `lea` | `02D3B2D0` | member "m_elementCount", offset 0x4 (constructor 00632960, called at 00665794) |
| 008B1620 | `008B1620` `lea` | `02D3B400` | member "m_elementCount", offset 0x4 (constructor 00632960, called at 00665B41) |
| 008B1630 | `008B1630` `lea` | `02D3B600` | member "m_elementCount", offset 0x8 (constructor 00632960, called at 00666024) |
| 008B1640 | `008B1640` `lea` | `02D3B860` | member "m_elementCount", offset 0x8 (constructor 00632960, called at 006661D5) |
| 008B16D0 | `008B16D0` `lea` | `02D3C400` | member "m_gatherIndex", offset 0x24 (constructor 00632960, called at 006671F5) |
| 008B16E0 | `008B16E0` `lea` | `02D3BC50` | member "m_hierarchyMatrixIndex", offset 0xC (constructor 00632960, called at 00667878) |
| 008B16F0 | `008B16F0` `lea` | `02D3C0E0` | member "m_hierarchyMatrixIndex", offset passed in a register (constructor 00632960, called at 006679AE) |
| 008B1700 | `008B1700` `lea` | `02D3B660` | member "m_indexCount", offset 0xC (constructor 00632960, called at 00666097) |
| 008B1710 | `008B1710` `lea` | `02D3C5A0` | member "m_indexCount", offset passed in a register (constructor 00632960, called at 00667544) |
| 008B1720 | `008B1720` `lea` | `02D3AF50` | member "m_indexData", offset 0x40 (constructor 00632960, called at 00667363) |
| 008B1730 | `008B1730` `lea` | `02D3C540` | member "m_indexFormat", offset 0x31 (constructor 00632960, called at 006674D5) |
| 008B1750 | `008B1750` `lea` | `02D3C340` | member "m_lodIndex", offset 0x1C (constructor 00632960, called at 0066710F) |
| 008B1760 | `008B1760` `lea` | `02D3C1A0` | member "m_materialIndex", offset passed in a register (constructor 00632960, called at 00666F1E) |
| 008B1780 | `008B1780` `lea` | `02D3C200` | member "m_matrixIndex", offset 0x4 (constructor 00632960, called at 00666F91) |
| 008B17B0 | `008B17B0` `lea` | `02D3B980` | member "m_maximumIndex", offset 0x4 (constructor 00632960, called at 0066632A) |
| 008B17C0 | `008B17C0` `lea` | `02D3B210` | member "m_memoryType", offset 0x1D (constructor 00632960, called at 006656B2) |
| 008B17D0 | `008B17D0` `lea` | `02D3B800` | member "m_memoryType", offset 0xD (constructor 00632960, called at 00666162) |
| 008B17E0 | `008B17E0` `lea` | `02D3B7A0` | member "m_mesh", offset 0x8 (constructor 00632960, called at 00665E73) |
| 008B1810 | `008B1810` `lea` | `02D3B920` | member "m_minimumIndex", offset passed in a register (constructor 00632960, called at 006662B7) |
| 008B1820 | `008B1820` `lea` | `02D3C790` | member "m_offset", offset passed in a register (constructor 00632960, called at 00667B61) |
| 008B1830 | `008B1830` `lea` | `02D3B080` | member "m_offsetInIndexBuffer", offset 0x68 (constructor 00632960, called at 00666513) |
| 008B1840 | `008B1840` `lea` | `02D3B1B0` | member "m_offsetInVertexBuffer", offset 0x70 (constructor 00632960, called at 00665A03) |
| 008B1850 | `008B1850` `lea` | `02D3BCB0` | member "m_pad", offset 0x1C (constructor 00632960, called at 006678EB) |
| 008B1880 | `008B1880` `lea` | `02D3C7F0` | member "m_renderDataType", offset 0x8 (constructor 00632960, called at 00667BD4) |
| 008B18A0 | `008B18A0` `lea` | `02D3C3A0` | member "m_shapeIndex", offset 0x20 (constructor 00632960, called at 00667182) |
| 008B18E0 | `008B18E0` `lea` | `02D3C140` | member "m_skeletonMatrixIndex", offset 0x2 (constructor 00632960, called at 00667A21) |
| 008B1900 | `008B1900` `lea` | `02D3B540` | member "m_startStreamIndex", offset passed in a register (constructor 00632960, called at 00665F3E) |
| 008B1910 | `008B1910` `lea` | `02D3B5A0` | member "m_streamCount", offset 0x4 (constructor 00632960, called at 00665FB1) |
| 008B1920 | `008B1920` `lea` | `02D3C850` | member "m_streamSet", offset 0x11 (constructor 00632960, called at 00667C47) |
| 008B1950 | `008B1950` `lea` | `02D3B270` | member "m_stride", offset passed in a register (constructor 00632960, called at 00665721) |
| 008B1960 | `008B1960` `lea` | `02D3B3A0` | member "m_stride", offset passed in a register (constructor 00632960, called at 00665ACE) |
| 008B1970 | `008B1970` `lea` | `02D3B8C0` | member "m_type", offset 0xC (constructor 00632960, called at 00666248) |
| 008B1980 | `008B1980` `lea` | `02D3C730` | member "m_type", offset 0x10 (constructor 00632960, called at 00667AF2) |
| 008B19C0 | `008B19C0` `lea` | `02D3C6D0` | member "m_vertexCount", offset 0x18 (constructor 00632960, called at 006676C1) |
| 008B19F0 | `008B19F0` `lea` | `02D3C670` | member "m_vertexFormat", offset 0x30 (constructor 00632960, called at 0066764E) |
| 008B1D40 | `008B1D40` `lea` | `02D3E910` | member "m_asset", offset 0x38 (constructor 00632960, called at 0067584C) |
| 008B1D70 | `008B1D70` `lea` | `02D3E970` | member "m_assetType", offset 0x40 (constructor 00632960, called at 006758BE) |
| 008B1D80 | `008B1D80` `lea` | `02D3E8B0` | member "m_id", offset 0x30 (constructor 00632960, called at 006757D9) |
| 008B1D90 | `008B1D90` `lea` | `02D3EBE0` | member "m_id", offset 0x8 (constructor 00632960, called at 00675E4B) |
| 008B1DA0 | `008B1DA0` `lea` | `02D3EC40` | member "m_targetAssetType", offset passed in a register (constructor 00632960, called at 00675EB9) |
| 008B1E50 | `008B1E50` `lea` | `02D3F6B0` | member "m_aspect", offset 0xC8 (constructor 00632960, called at 0067895A) |
| 008B1E60 | `008B1E60` `lea` | `02D3F5F0` | member "m_farPlane", offset 0xBC (constructor 00632960, called at 006787B1) |
| 008B1E70 | `008B1E70` `lea` | `02D3F530` | member "m_localToWorldMatrix", offset 0xB0 (constructor 00632960, called at 006786CB) |
| 008B1E80 | `008B1E80` `lea` | `02D3F590` | member "m_nearPlane", offset 0xB8 (constructor 00632960, called at 0067873E) |
| 008B1E90 | `008B1E90` `lea` | `02D3F470` | member "m_projectionMatrix", offset 0x30 (constructor 00632960, called at 006785E6) |
| 008B1EA0 | `008B1EA0` `lea` | `02D3F410` | member "m_viewMatrix", offset passed in a register (constructor 00632960, called at 00678573) |
| 008B1EB0 | `008B1EB0` `lea` | `02D3F4D0` | member "m_viewProjectionMatrix", offset 0x70 (constructor 00632960, called at 00678659) |
| 008B2000 | `008B2000` `lea` | `02E40010` | member "m_baselineOffset", offset 0xC (constructor 00632960, called at 0067D1C7) |
| 008B2010 | `008B2010` `lea` | `02E40150` | member "m_bitmapFontTexture", offset 0x30 (constructor 00632960, called at 0067D370) |
| 008B2020 | `008B2020` `lea` | `02E3FB60` | member "m_characterCode", offset passed in a register (constructor 00632960, called at 0067D43E) |
| 008B2040 | `008B2040` `lea` | `02E402C0` | member "m_count", offset passed in a register (constructor 00632960, called at 0067D9AA) |
| 008B2060 | `008B2060` `lea` | `02E3FEF0` | member "m_fontSize", offset 0x4 (constructor 00632960, called at 0067D072) |
| 008B2070 | `008B2070` `lea` | `02E3FD50` | member "m_height", offset 0x18 (constructor 00632960, called at 0067D67F) |
| 008B2080 | `008B2080` `lea` | `02E3FF50` | member "m_isSDF", offset passed in a register (constructor 00632960, called at 0067D0E1) |
| 008B2090 | `008B2090` `lea` | `02E3FC20` | member "m_kernOffset", offset 0x8 (constructor 00632960, called at 0067D524) |
| 008B20A0 | `008B20A0` `lea` | `02E3FBC0` | member "m_kernPairs", offset 0x4 (constructor 00632960, called at 0067D4B1) |
| 008B20C0 | `008B20C0` `lea` | `02E3FFB0` | member "m_lineSpacing", offset 0x8 (constructor 00632960, called at 0067D154) |
| 008B20E0 | `008B20E0` `lea` | `02E3FE90` | member "m_rotated", offset 0x2C (constructor 00632960, called at 0067D7DC) |
| 008B2100 | `008B2100` `lea` | `02E3FCF0` | member "m_width", offset 0x14 (constructor 00632960, called at 0067D60C) |
| 008B21F0 | `008B21F0` `lea` | `02E406D0` | member "m_matrix", offset passed in a register (constructor 00632960, called at 0067E9B6) |
| 008B24E0 | `008B24E0` `lea` | `02E42830` | member "m_defaultEntryPoint", offset 0x40 (constructor 00632960, called at 00682624) |
| 008B24F0 | `008B24F0` `lea` | `02E42320` | member "m_entryPoint", offset 0x60 (constructor 00632960, called at 00681EED) |
| 008B2500 | `008B2500` `lea` | `02E42380` | member "m_entryPoint", offset passed in a register (constructor 00632960, called at 00682849) |
| 008B2510 | `008B2510` `lea` | `02E42950` | member "m_executionInterval", offset 0x54 (constructor 00632960, called at 0068277C) |
| 008B2530 | `008B2530` `lea` | `02E423E0` | member "m_handler", offset 0x8 (constructor 00632960, called at 006828B7) |
| 008B2540 | `008B2540` `lea` | `02E428F0` | member "m_isPersistent", offset 0x50 (constructor 00632960, called at 00682709) |
| 008B2550 | `008B2550` `lea` | `02E422C0` | member "m_nameAsString", offset 0x58 (constructor 00632960, called at 00681E7F) |
| 008B2560 | `008B2560` `lea` | `02E42770` | member "m_onLoadEntryPoint", offset 0x30 (constructor 00632960, called at 00682540) |
| 008B2570 | `008B2570` `lea` | `02E427D0` | member "m_onUnloadEntryPoint", offset 0x38 (constructor 00632960, called at 006825B2) |
| 008B2580 | `008B2580` `lea` | `02E42260` | member "m_script", offset 0x50 (constructor 00632960, called at 00681E11) |
| 008B25B0 | `008B25B0` `lea` | `02E42890` | member "m_sourceName", offset 0x48 (constructor 00632960, called at 00682696) |
| 008B3620 | `008B3620` `lea` | `02E4BEE0` | member "m_amount", offset 0x20 (constructor 00632960, called at 006940E6) |
| 008B3630 | `008B3630` `lea` | `02E4B8F0` | member "m_angularDamping", offset 0xC4 (constructor 00632960, called at 00696B79) |
| 008B3640 | `008B3640` `lea` | `02E4CB30` | member "m_characterControllers", offset 0x50 (constructor 00632960, called at 0069844B) |
| 008B3650 | `008B3650` `lea` | `02E4BA70` | member "m_collisionGroup", offset 0xE0 (constructor 00632960, called at 00696D3E) |
| 008B3660 | `008B3660` `lea` | `02E4CCB0` | member "m_collisionObject", offset 0x20 (constructor 00632960, called at 00698674) |
| 008B3670 | `008B3670` `lea` | `02E4BE20` | member "m_collisionObjectA", offset passed in a register (constructor 00632960, called at 00694009) |
| 008B3680 | `008B3680` `lea` | `02E4BE80` | member "m_collisionObjectB", offset 0x10 (constructor 00632960, called at 00694077) |
| 008B3690 | `008B3690` `lea` | `02E4CD10` | member "m_collisionObjectClassDescriptor", offset 0x28 (constructor 00632960, called at 006986E6) |
| 008B36A0 | `008B36A0` `lea` | `02E4A260` | member "m_collisionRadius", offset 0x10 (constructor 00632960, called at 006942FB) |
| 008B36B0 | `008B36B0` `lea` | `02E4A380` | member "m_contactEpsilon", offset 0x1C (constructor 00632960, called at 00694448) |
| 008B36C0 | `008B36C0` `lea` | `02E4CC50` | member "m_contactNormal", offset 0x10 (constructor 00632960, called at 00698601) |
| 008B36D0 | `008B36D0` `lea` | `02E4CBF0` | member "m_contactPoint", offset passed in a register (constructor 00632960, called at 0069858E) |
| 008B36E0 | `008B36E0` `lea` | `02E4D200` | member "m_count", offset passed in a register (constructor 00632960, called at 00698B98) |
| 008B36F0 | `008B36F0` `lea` | `02E4C480` | member "m_density", offset 0x10 (constructor 00632960, called at 00697498) |
| 008B3700 | `008B3700` `lea` | `02E4B0A0` | member "m_dynamicFriction", offset passed in a register (constructor 00632960, called at 0069565E) |
| 008B3710 | `008B3710` `lea` | `02E4BAD0` | member "m_enabled", offset 0xE9 (constructor 00632960, called at 00696DB1) |
| 008B3720 | `008B3720` `lea` | `02E4B340` | member "m_equationCoefficient", offset 0x70 (constructor 00632960, called at 00695A79) |
| 008B3730 | `008B3730` `lea` | `02E4A8C0` | member "m_forward", offset 0xE8 (constructor 00632960, called at 00694C79) |
| 008B3740 | `008B3740` `lea` | `02E4AD40` | member "m_graphicsOffset", offset 0x48 (constructor 00632960, called at 006951D7) |
| 008B3750 | `008B3750` `lea` | `02E4A6E0` | member "m_gravity", offset 0x28 (constructor 00632960, called at 00694A3C) |
| 008B3760 | `008B3760` `lea` | `02E4C9B0` | member "m_gravity", offset passed in a register (constructor 00632960, called at 00698280) |
| 008B3770 | `008B3770` `lea` | `02E4A130` | member "m_halfExtents", offset 0x70 (constructor 00632960, called at 00693F49) |
| 008B3780 | `008B3780` `lea` | `02E4A200` | member "m_height", offset 0x78 (constructor 00632960, called at 0069422C) |
| 008B3790 | `008B3790` `lea` | `02E4AC20` | member "m_height", offset 0xF8 (constructor 00632960, called at 0069507F) |
| 008B37A0 | `008B37A0` `lea` | `02E4AF90` | member "m_height", offset 0x78 (constructor 00632960, called at 0069559C) |
| 008B37B0 | `008B37B0` `lea` | `02E4C7B0` | member "m_height", offset 0x80 (constructor 00632960, called at 006978DC) |
| 008B37C0 | `008B37C0` `lea` | `02E4C8F0` | member "m_height", offset 0x80 (constructor 00632960, called at 00697A8C) |
| 008B37D0 | `008B37D0` `lea` | `02E4C3C0` | member "m_hollow", offset 0x8 (constructor 00632960, called at 006973B2) |
| 008B37E0 | `008B37E0` `lea` | `02E4B580` | member "m_inertiaTensor", offset 0x58 (constructor 00632960, called at 0069674B) |
| 008B37F0 | `008B37F0` `lea` | `02E4B640` | member "m_initialAngularVelocity", offset 0x78 (constructor 00632960, called at 00696831) |
| 008B3800 | `008B3800` `lea` | `02E4B5E0` | member "m_initialLinearVelocity", offset 0x68 (constructor 00632960, called at 006967BE) |
| 008B3810 | `008B3810` `lea` | `02E4B520` | member "m_initialOrientation", offset 0x48 (constructor 00632960, called at 006966D8) |
| 008B3820 | `008B3820` `lea` | `02E4B4C0` | member "m_initialPosition", offset 0x38 (constructor 00632960, called at 00696665) |
| 008B3830 | `008B3830` `lea` | `02E4ADA0` | member "m_invGraphicsOffset", offset 0x88 (constructor 00632960, called at 0069524A) |
| 008B3840 | `008B3840` `lea` | `02E4A9E0` | member "m_isOnGround", offset 0x105 (constructor 00632960, called at 00694DD2) |
| 008B3850 | `008B3850` `lea` | `02E4A980` | member "m_jump", offset 0x104 (constructor 00632960, called at 00694D5F) |
| 008B3860 | `008B3860` `lea` | `02E4ABC0` | member "m_jumpHeight", offset 0xF4 (constructor 00632960, called at 0069500C) |
| 008B3870 | `008B3870` `lea` | `02E4CB90` | member "m_kinematicRigidBodies", offset 0x58 (constructor 00632960, called at 006984BD) |
| 008B3880 | `008B3880` `lea` | `02E4B890` | member "m_linearDamping", offset 0xC0 (constructor 00632960, called at 00696B06) |
| 008B38B0 | `008B38B0` `lea` | `02E4B3A0` | member "m_mass", offset 0xE4 (constructor 00632960, called at 0069650C) |
| 008B38C0 | `008B38C0` `lea` | `02E4C420` | member "m_mass", offset 0xC (constructor 00632960, called at 00697425) |
| 008B38D0 | `008B38D0` `lea` | `02E4B460` | member "m_massFrameTransform", offset 0x8 (constructor 00632960, called at 006965F2) |
| 008B38E0 | `008B38E0` `lea` | `02E4B760` | member "m_material", offset 0x98 (constructor 00632960, called at 00696987) |
| 008B38F0 | `008B38F0` `lea` | `02E4C4E0` | member "m_material", offset 0x18 (constructor 00632960, called at 0069750A) |
| 008B3900 | `008B3900` `lea` | `02E4AA40` | member "m_maxSlopeAngle", offset 0xF0 (constructor 00632960, called at 00694E45) |
| 008B3910 | `008B3910` `lea` | `02E4A3E0` | member "m_minimumCameraDistance", offset 0x20 (constructor 00632960, called at 006944B7) |
| 008B3920 | `008B3920` `lea` | `02E4B9B0` | member "m_model", offset 0xC8 (constructor 00632960, called at 00696C59) |
| 008B3930 | `008B3930` `lea` | `02E4C950` | member "m_models", offset 0x48 (constructor 00632960, called at 00698211) |
| 008B3940 | `008B3940` `lea` | `02E4A500` | member "m_nearCameraYAdjust", offset 0x34 (constructor 00632960, called at 00694604) |
| 008B3950 | `008B3950` `lea` | `02E4AAA0` | member "m_next", offset passed in a register (constructor 00632960, called at 00694EB3) |
| 008B3960 | `008B3960` `lea` | `02E4B280` | member "m_next", offset passed in a register (constructor 00632960, called at 0069593F) |
| 008B3970 | `008B3970` `lea` | `02E4B950` | member "m_next", offset passed in a register (constructor 00632960, called at 00696BE7) |
| 008B3980 | `008B3980` `lea` | `02E4BA10` | member "m_nextKinematicRigidBody", offset 0xD8 (constructor 00632960, called at 00696CCB) |
| 008B3990 | `008B3990` `lea` | `02E4AC80` | member "m_radius", offset 0xFC (constructor 00632960, called at 006950F2) |
| 008B39A0 | `008B39A0` `lea` | `02E4C670` | member "m_radius", offset 0x70 (constructor 00632960, called at 00697729) |
| 008B39D0 | `008B39D0` `lea` | `02E4B160` | member "m_restitution", offset 0x8 (constructor 00632960, called at 00695744) |
| 008B39E0 | `008B39E0` `lea` | `02E4A860` | member "m_right", offset 0xE4 (constructor 00632960, called at 00694C06) |
| 008B39F0 | `008B39F0` `lea` | `02E4B220` | member "m_rigidBodies", offset 0x8 (constructor 00632960, called at 006958D1) |
| 008B3A00 | `008B3A00` `lea` | `02E4B400` | member "m_rigidBodyType", offset 0xE8 (constructor 00632960, called at 0069657F) |
| 008B3A10 | `008B3A10` `lea` | `02E4A800` | member "m_rotate", offset 0xE0 (constructor 00632960, called at 00694B93) |
| 008B3A20 | `008B3A20` `lea` | `02E4AB60` | member "m_scale", offset 0x18 (constructor 00632960, called at 00694F99) |
| 008B3A30 | `008B3A30` `lea` | `02E4B830` | member "m_scale", offset 0x88 (constructor 00632960, called at 00696A93) |
| 008B3A40 | `008B3A40` `lea` | `02E4C5A0` | member "m_scale", offset 0x50 (constructor 00632960, called at 006975F0) |
| 008B3A50 | `008B3A50` `lea` | `02E4AE00` | member "m_scriptHandler", offset 0x118 (constructor 00632960, called at 006952BC) |
| 008B3A60 | `008B3A60` `lea` | `02E4BB30` | member "m_scriptHandler", offset 0x100 (constructor 00632960, called at 00696E23) |
| 008B3A70 | `008B3A70` `lea` | `02E4B1C0` | member "m_shape", offset 0x70 (constructor 00632960, called at 00695808) |
| 008B3A90 | `008B3A90` `lea` | `02E4A440` | member "m_smoothingRate", offset 0x24 (constructor 00632960, called at 00694526) |
| 008B3AA0 | `008B3AA0` `lea` | `02E4A4A0` | member "m_springTension", offset 0x30 (constructor 00632960, called at 00694595) |
| 008B3AB0 | `008B3AB0` `lea` | `02E4AB00` | member "m_startPosition", offset 0x8 (constructor 00632960, called at 00694F26) |
| 008B3AC0 | `008B3AC0` `lea` | `02E4B100` | member "m_staticFriction", offset 0x4 (constructor 00632960, called at 006956D1) |
| 008B3AD0 | `008B3AD0` `lea` | `02E4A2C0` | member "m_targetDistance", offset 0x14 (constructor 00632960, called at 0069436A) |
| 008B3AE0 | `008B3AE0` `lea` | `02E4A320` | member "m_targetHeight", offset 0x18 (constructor 00632960, called at 006943D9) |
| 008B3AF0 | `008B3AF0` `lea` | `02E4A740` | member "m_targetNode", offset 0xC8 (constructor 00632960, called at 00694AAE) |
| 008B3B00 | `008B3B00` `lea` | `02E4B6A0` | member "m_targetNode", offset 0xA0 (constructor 00632960, called at 006968A3) |
| 008B3B10 | `008B3B10` `lea` | `02E4A7A0` | member "m_targetWorldMatrix", offset 0xD0 (constructor 00632960, called at 00694B20) |
| 008B3B20 | `008B3B20` `lea` | `02E4B700` | member "m_targetWorldMatrix", offset 0xA8 (constructor 00632960, called at 00696915) |
| 008B3B30 | `008B3B30` `lea` | `02E4CA10` | member "m_timeStep", offset 0x10 (constructor 00632960, called at 006982F3) |
| 008B3B40 | `008B3B40` `lea` | `02E4C540` | member "m_transform", offset 0x20 (constructor 00632960, called at 0069757D) |
| 008B3B90 | `008B3B90` `lea` | `02E4A920` | member "m_velocity", offset 0xEC (constructor 00632960, called at 00694CEC) |
| 008B3BA0 | `008B3BA0` `lea` | `02E4ACE0` | member "m_world", offset 0xD8 (constructor 00632960, called at 00695164) |
| 008B3BB0 | `008B3BB0` `lea` | `02E4B2E0` | member "m_world", offset 0x10 (constructor 00632960, called at 006959B1) |
| 008B3BC0 | `008B3BC0` `lea` | `02E4CAD0` | member "m_worldMax", offset 0x24 (constructor 00632960, called at 006983D9) |
| 008B3BD0 | `008B3BD0` `lea` | `02E4CA70` | member "m_worldMin", offset 0x14 (constructor 00632960, called at 00698366) |
| 008B4090 | `008B4090` `lea` | `02E4DF40` | member "m_count", offset passed in a register (constructor 00632960, called at 006A8728) |
| 008B40A0 | `008B40A0` `lea` | `02E4DBD0` | member "m_enabled", offset 0x50 (constructor 00632960, called at 006A8159) |
| 008B40B0 | `008B40B0` `lea` | `02E4DAA0` | member "m_localToWorldMatrix", offset 0x18 (constructor 00632960, called at 006A7FEA) |
| 008B40C0 | `008B40C0` `lea` | `02E4DB00` | member "m_previousLocalToWorldMatrix", offset 0x20 (constructor 00632960, called at 006A8058) |
| 008B40E0 | `008B40E0` `lea` | `02E4DA40` | member "m_type", offset passed in a register (constructor 00632960, called at 006A7F78) |
| 008B4180 | `008B4180` `lea` | `02E4E340` | member "m_min", offset 0x48 (constructor 00632960, called at 006A993C) |
| 008B4190 | `008B4190` `lea` | `02E4E2E0` | member "m_previousLocalToWorldMatrix", offset 0x18 (constructor 00632960, called at 006A98CD) |
| 008B41A0 | `008B41A0` `lea` | `02E4E3A0` | member "m_size", offset 0x58 (constructor 00632960, called at 006A99AB) |
| 008B41D0 | `008B41D0` `lea` | `02E4E590` | member "m_classDescriptor", offset 0x8 (constructor 00632960, called at 006AA010) |
| 008B41E0 | `008B41E0` `lea` | `02E4E530` | member "m_object", offset passed in a register (constructor 00632960, called at 006A9F9E) |
| 008B42E0 | `008B42E0` `lea` | `02E4E9A0` | member "m_componentType", offset 0x10 (constructor 00632960, called at 006AAD8F) |
| 008B42F0 | `008B42F0` `lea` | `02E4E8E0` | member "m_entity", offset 0x8 (constructor 00632960, called at 006AACAF) |
| 008B4300 | `008B4300` `lea` | `02E4E940` | member "m_next", offset passed in a register (constructor 00632960, called at 006AAD1D) |
| 008B4540 | `008B4540` `lea` | `02E4EC50` | member "m_firstComponent", offset passed in a register (constructor 00632960, called at 006AB946) |
| 008B4550 | `008B4550` `lea` | `02E4ECB0` | member "m_worldMatrix", offset 0x8 (constructor 00632960, called at 006AB9B8) |
| 008B4640 | `008B4640` `lea` | `02E4F390` | member "m_height", offset 0xD0 (constructor 00632960, called at 006AD137) |
| 008B46D0 | `008B46D0` `lea` | `02E4F810` | member "m_FOV", offset 0xD0 (constructor 00632960, called at 006AD999) |
| 008B48B0 | `008B48B0` `lea` | `02E4FD00` | member "m_count", offset passed in a register (constructor 00632960, called at 006AE91A) |
| 008B4960 | `008B4960` `lea` | `02E50060` | member "m_name", offset 0x28 (constructor 00632960, called at 006AFCB2) |
| 008B5520 | `008B5520` `lea` | `02E51F70` | member "m_firstChild", offset 0x10 (constructor 00632960, called at 006B4E40) |
| 008B5530 | `008B5530` `lea` | `02E52090` | member "m_localMatrix", offset 0x20 (constructor 00632960, called at 006B4F93) |
| 008B5540 | `008B5540` `lea` | `02E520F0` | member "m_name", offset 0x60 (constructor 00632960, called at 006B5005) |
| 008B5550 | `008B5550` `lea` | `02E51FD0` | member "m_next", offset passed in a register (constructor 00632960, called at 006B4EAE) |
| 008B5560 | `008B5560` `lea` | `02E51F10` | member "m_parent", offset 0x8 (constructor 00632960, called at 006B4DCE) |
| 008B5570 | `008B5570` `lea` | `02E52030` | member "m_worldMatrix", offset 0x18 (constructor 00632960, called at 006B4F20) |
| 008B5DC0 | `008B5DC0` `lea` | `02E585B0` | member "m_count", offset passed in a register (constructor 00632960, called at 006BCDDA) |
| 008B5DD0 | `008B5DD0` `lea` | `02E58A10` | member "m_count", offset passed in a register (constructor 00632960, called at 006BD11A) |
| 008B5DE0 | `008B5DE0` `lea` | `02E587E0` | member "m_count", offset passed in a register (constructor 00632960, called at 006BD44A) |
| 008B5E20 | `008B5E20` `lea` | `02E58160` | member "m_modifierNetwork", offset passed in a register (constructor 00632960, called at 006BCAAD) |
| 008B5E60 | `008B5E60` `lea` | `02E58280` | member "m_modifierOutputsAreConsumed", offset 0x10 (constructor 00632960, called at 006BCC06) |
| 008B5E70 | `008B5E70` `lea` | `02E581C0` | member "m_segmentInputGroupStart", offset 0x8 (constructor 00632960, called at 006BCB20) |
| 008B5E90 | `008B5E90` `lea` | `02E58220` | member "m_segmentOutputGroupStart", offset 0xC (constructor 00632960, called at 006BCB93) |
| 008B61B0 | `008B61B0` `lea` | `02E58F20` | member "m_color", offset passed in a register (constructor 00632960, called at 006BEDFA) |
| 008B61C0 | `008B61C0` `lea` | `02E590A0` | member "m_innerConeAngle", offset 0x28 (constructor 00632960, called at 006BEFC4) |
| 008B61D0 | `008B61D0` `lea` | `02E591C0` | member "m_innerRange", offset 0x34 (constructor 00632960, called at 006BF11D) |
| 008B61E0 | `008B61E0` `lea` | `02E59160` | member "m_intensity", offset 0x30 (constructor 00632960, called at 006BF0AA) |
| 008B61F0 | `008B61F0` `lea` | `02E59040` | member "m_lightType", offset 0x20 (constructor 00632960, called at 006BEF51) |
| 008B6200 | `008B6200` `lea` | `02E58F80` | member "m_localToWorldMatrix", offset 0x10 (constructor 00632960, called at 006BEE6C) |
| 008B6210 | `008B6210` `lea` | `02E59100` | member "m_outerConeAngle", offset 0x2C (constructor 00632960, called at 006BF037) |
| 008B6220 | `008B6220` `lea` | `02E59220` | member "m_outerRange", offset 0x38 (constructor 00632960, called at 006BF190) |
| 008B6230 | `008B6230` `lea` | `02E59280` | member "m_scatteringIntensity", offset 0x3C (constructor 00632960, called at 006BF203) |
| 008B6240 | `008B6240` `lea` | `02E58FE0` | member "m_shadowCaster", offset 0x18 (constructor 00632960, called at 006BEEDE) |
| 008B68B0 | `008B68B0` `lea` | `02E5A230` | member "m_count", offset passed in a register (constructor 00632960, called at 006C1ABA) |
| 008B68D0 | `008B68D0` `lea` | `02E59F30` | member "m_farPlane", offset 0xC8 (constructor 00632960, called at 006C1899) |
| 008B68E0 | `008B68E0` `lea` | `02E5A0C0` | member "m_light", offset passed in a register (constructor 00632960, called at 006C17DC) |
| 008B68F0 | `008B68F0` `lea` | `02E5A000` | member "m_shadowCasterType", offset 0x8 (constructor 00632960, called at 006C16FB) |
| 008B6910 | `008B6910` `lea` | `02E5A060` | member "m_zbias", offset 0x50 (constructor 00632960, called at 006C176E) |
| 008B69B0 | `008B69B0` `lea` | `02E5AB90` | member "m_count", offset passed in a register (constructor 00632960, called at 006C399A) |
| 008B69C0 | `008B69C0` `lea` | `02E5A7C0` | member "m_elementSize", offset 0x8 (constructor 00632960, called at 006C3612) |
| 008B69E0 | `008B69E0` `lea` | `02E5A8E0` | member "m_list", offset 0x4 (constructor 00632960, called at 006C37C1) |
| 008B69F0 | `008B69F0` `lea` | `02E5A940` | member "m_modifierNetwork", offset passed in a register (constructor 00632960, called at 006C340D) |
| 008B6A20 | `008B6A20` `lea` | `02E5A820` | member "m_renderStream", offset 0x10 (constructor 00632960, called at 006C3684) |
| 008B6A30 | `008B6A30` `lea` | `02E5A880` | member "m_source", offset passed in a register (constructor 00632960, called at 006C374E) |
| 008B6C00 | `008B6C00` `lea` | `02E5B3D0` | member "m_blendRange", offset 0x30 (constructor 00632960, called at 006C5C54) |
| 008B6C10 | `008B6C10` `lea` | `02E5B9B0` | member "m_count", offset passed in a register (constructor 00632960, called at 006C63CA) |
| 008B6C20 | `008B6C20` `lea` | `02E5B800` | member "m_count", offset passed in a register (constructor 00632960, called at 006C67C8) |
| 008B6C40 | `008B6C40` `lea` | `02E5B550` | member "m_isEnabled", offset 0x60 (constructor 00632960, called at 006C5E18) |
| 008B6C60 | `008B6C60` `lea` | `02E5B4F0` | member "m_lodBlendType", offset 0x48 (constructor 00632960, called at 006C5DA9) |
| 008B6C70 | `008B6C70` `lea` | `02E5B110` | member "m_lodGroup", offset passed in a register (constructor 00632960, called at 006C607D) |
| 008B6C80 | `008B6C80` `lea` | `02E5B490` | member "m_lodMetricType", offset 0x40 (constructor 00632960, called at 006C5D36) |
| 008B6C90 | `008B6C90` `lea` | `02E5B370` | member "m_maxBounds", offset 0x10 (constructor 00632960, called at 006C5BE5) |
| 008B6CA0 | `008B6CA0` `lea` | `02E5B240` | member "m_maximumThreshold", offset 0x1C (constructor 00632960, called at 006C61ED) |
| 008B6CC0 | `008B6CC0` `lea` | `02E5B310` | member "m_minBounds", offset passed in a register (constructor 00632960, called at 006C5B76) |
| 008B6CD0 | `008B6CD0` `lea` | `02E5B1E0` | member "m_minimumThreshold", offset 0x18 (constructor 00632960, called at 006C617E) |
| 008B6CE0 | `008B6CE0` `lea` | `02E5B430` | member "m_shaderLODLevelDistance", offset 0x34 (constructor 00632960, called at 006C5CC3) |
| 008B6DE0 | `008B6DE0` `lea` | `02E5BD10` | member "m_localToWorldMatrix", offset 0x8 (constructor 00632960, called at 006C8414) |
| 008B6DF0 | `008B6DF0` `lea` | `02E5BCB0` | member "m_occluder", offset passed in a register (constructor 00632960, called at 006C83A2) |
| 008B6F80 | `008B6F80` `lea` | `02E5C1B0` | member "m_entryPoint", offset 0x20 (constructor 00632960, called at 006CD0FF) |
| 008B6F90 | `008B6F90` `lea` | `02E5C150` | member "m_script", offset 0x28 (constructor 00632960, called at 006CD091) |
| 008B7040 | `008B7040` `lea` | `02E5C590` | member "m_entryCount", offset 0x20 (constructor 00632960, called at 006CDB3C) |
| 008B7050 | `008B7050` `lea` | `02E5C530` | member "m_quarryComponent", offset 0x18 (constructor 00632960, called at 006CDACD) |
| 008B7060 | `008B7060` `lea` | `02E5C4D0` | member "m_trigger", offset 0x10 (constructor 00632960, called at 006CDA5B) |
| 008B7070 | `008B7070` `lea` | `02E5C470` | member "m_triggerReceiverComponent", offset passed in a register (constructor 00632960, called at 006CD9E9) |
| 008B70A0 | `008B70A0` `lea` | `02E5C870` | member "m_entryHandler", offset 0x28 (constructor 00632960, called at 006CE293) |
| 008B70B0 | `008B70B0` `lea` | `02E5C8D0` | member "m_exitHandler", offset 0x40 (constructor 00632960, called at 006CE305) |
| 008B70C0 | `008B70C0` `lea` | `02E5C810` | member "m_script", offset 0x18 (constructor 00632960, called at 006CE221) |
| 008B72A0 | `008B72A0` `lea` | `02E5ED10` | member "m_codeIndex", offset 0x8 (constructor 00632960, called at 006D205B) |
| 008B72B0 | `008B72B0` `lea` | `02E9F960` | member "m_count", offset passed in a register (constructor 00632960, called at 006D252A) |
| 008B72C0 | `008B72C0` `lea` | `02E9FB90` | member "m_count", offset passed in a register (constructor 00632960, called at 006D285A) |
| 008B72D0 | `008B72D0` `lea` | `02E9F730` | member "m_count", offset passed in a register (constructor 00632960, called at 006D2B8A) |
| 008B72E0 | `008B72E0` `lea` | `02E5E700` | member "m_dataBlock", offset passed in a register (constructor 00632960, called at 006D219D) |
| 008B72F0 | `008B72F0` `lea` | `02E5E8E0` | member "m_elementSize", offset 0x10 (constructor 00632960, called at 006D1767) |
| 008B7300 | `008B7300` `lea` | `02E5EDE0` | member "m_elementSize", offset passed in a register (constructor 00632960, called at 006D1CFC) |
| 008B7340 | `008B7340` `lea` | `02E5E940` | member "m_info", offset 0x14 (constructor 00632960, called at 006D17DA) |
| 008B7350 | `008B7350` `lea` | `02E5F430` | member "m_infoPacket", offset 0x48 (constructor 00632960, called at 006D134E) |
| 008B7360 | `008B7360` `lea` | `02E5EF60` | member "m_inputCount", offset 0xC (constructor 00632960, called at 006D19FE) |
| 008B7370 | `008B7370` `lea` | `02E5EB90` | member "m_inputCount", offset 0x8 (constructor 00632960, called at 006D1E38) |
| 008B73C0 | `008B73C0` `lea` | `02E5F550` | member "m_isCompiled", offset 0x58 (constructor 00632960, called at 006D14A7) |
| 008B73D0 | `008B73D0` `lea` | `02E5E9A0` | member "m_modifier", offset passed in a register (constructor 00632960, called at 006D0DDE) |
| 008B73E0 | `008B73E0` `lea` | `02E5E820` | member "m_modifier", offset 0x8 (constructor 00632960, called at 006D1681) |
| 008B73F0 | `008B73F0` `lea` | `02E5EB30` | member "m_modifier", offset passed in a register (constructor 00632960, called at 006D1DC5) |
| 008B7400 | `008B7400` `lea` | `02E5EEA0` | member "m_modifierCodeCount", offset 0x4 (constructor 00632960, called at 006D1918) |
| 008B7410 | `008B7410` `lea` | `02E5EF00` | member "m_modifierInstanceCount", offset 0x8 (constructor 00632960, called at 006D198B) |
| 008B7430 | `008B7430` `lea` | `02E5EFC0` | member "m_outputCount", offset 0xE (constructor 00632960, called at 006D1A71) |
| 008B7440 | `008B7440` `lea` | `02E5EBF0` | member "m_outputCount", offset 0xC (constructor 00632960, called at 006D1EAB) |
| 008B7460 | `008B7460` `lea` | `02E5EA00` | member "m_persistentStateOffset", offset 0x8 (constructor 00632960, called at 006D0E51) |
| 008B7470 | `008B7470` `lea` | `02E5EC50` | member "m_persistentStateOffset", offset passed in a register (constructor 00632960, called at 006D1F75) |
| 008B7480 | `008B7480` `lea` | `02E5EE40` | member "m_size", offset passed in a register (constructor 00632960, called at 006D18A5) |
| 008B7490 | `008B7490` `lea` | `02E5E640` | member "m_source", offset passed in a register (constructor 00632960, called at 006D22DE) |
| 008B74A0 | `008B74A0` `lea` | `02E5F150` | member "m_spuModifierCodeSize", offset 0x1C (constructor 00632960, called at 006D1C3C) |
| 008B74B0 | `008B74B0` `lea` | `02E5EA60` | member "m_stateBlockOffset", offset 0xC (constructor 00632960, called at 006D0EC4) |
| 008B74C0 | `008B74C0` `lea` | `02E5ECB0` | member "m_stateBlockOffset", offset 0x4 (constructor 00632960, called at 006D1FE8) |
| 008B74D0 | `008B74D0` `lea` | `02E5E880` | member "m_stream", offset 0xC (constructor 00632960, called at 006D16F4) |
| 008B74E0 | `008B74E0` `lea` | `02E5E6A0` | member "m_stream", offset 0x4 (constructor 00632960, called at 006D2351) |
| 008B7510 | `008B7510` `lea` | `02E5F220` | member "m_totalInputCount", offset 0x18 (constructor 00632960, called at 006D10D0) |
| 008B7520 | `008B7520` `lea` | `02E5F360` | member "m_totalOutputElementSize", offset passed in a register (constructor 00632960, called at 006D126A) |
| 008B7530 | `008B7530` `lea` | `02E5F490` | member "m_totalPersistentStateSize", offset 0x50 (constructor 00632960, called at 006D13C1) |
| 008B7540 | `008B7540` `lea` | `02E5F090` | member "m_totalPersistentStateSize", offset 0x14 (constructor 00632960, called at 006D1B56) |
| 008B7550 | `008B7550` `lea` | `02E5F4F0` | member "m_totalStateBlockSize", offset 0x54 (constructor 00632960, called at 006D1434) |
| 008B7560 | `008B7560` `lea` | `02E5F0F0` | member "m_totalStateBlockSize", offset 0x18 (constructor 00632960, called at 006D1BC9) |
| 008B7570 | `008B7570` `lea` | `02E5E7C0` | member "m_type", offset passed in a register (constructor 00632960, called at 006D160E) |
| 008B7580 | `008B7580` `lea` | `02E5E760` | member "m_vertexStream", offset 0x8 (constructor 00632960, called at 006D220F) |
| 008B78D0 | `008B78D0` `lea` | `02EA0A20` | member "m_edgeCount", offset 0x8 (constructor 00632960, called at 006DA12F) |
| 008B78E0 | `008B78E0` `lea` | `02EA0AE0` | member "m_maxBounds", offset 0x20 (constructor 00632960, called at 006DA20D) |
| 008B78F0 | `008B78F0` `lea` | `02EA0A80` | member "m_minBounds", offset 0x10 (constructor 00632960, called at 006DA19E) |
| 008B7900 | `008B7900` `lea` | `02EA0960` | member "m_planeCount", offset passed in a register (constructor 00632960, called at 006DA051) |
| 008B7910 | `008B7910` `lea` | `02EA09C0` | member "m_vertexCount", offset 0x4 (constructor 00632960, called at 006DA0C0) |
| 008B85A0 | `008B85A0` `lea` | `02EAC340` | member "m_autoClear", offset 0x50 (constructor 00632960, called at 0079554C) |
| 008B85B0 | `008B85B0` `lea` | `02EACB70` | member "m_inputMap", offset passed in a register (constructor 00632960, called at 00795627) |
| 008B9680 | `008B9680` `lea` | `02EB7970` | member "m_count", offset passed in a register (constructor 00632960, called at 0086E60A) |
| 008B9690 | `008B9690` `lea` | `02EB7740` | member "m_count", offset passed in a register (constructor 00632960, called at 0086E94A) |
| 008B96C0 | `008B96C0` `lea` | `02EB6F50` | member "m_id", offset 0x18 (constructor 00632960, called at 0086DB71) |
| 008B96F0 | `008B96F0` `lea` | `02EB6FB0` | member "m_invert", offset 0x1C (constructor 00632960, called at 0086DBE0) |
| 008B9700 | `008B9700` `lea` | `02EB71F0` | member "m_joypadAxisSemantic", offset 0x30 (constructor 00632960, called at 0086DD19) |
| 008B9710 | `008B9710` `lea` | `02EB72B0` | member "m_modifierButtonSemantic", offset 0x30 (constructor 00632960, called at 0086E1E2) |
| 008B9720 | `008B9720` `lea` | `02EB7370` | member "m_modifierButtonSemantic", offset 0x30 (constructor 00632960, called at 0086E322) |
| 008B9730 | `008B9730` `lea` | `02EB7310` | member "m_modifierKeySemantic", offset 0x38 (constructor 00632960, called at 0086E255) |
| 008B9740 | `008B9740` `lea` | `02EB73D0` | member "m_modifierKeySemantic", offset 0x38 (constructor 00632960, called at 0086E395) |
| 008B9750 | `008B9750` `lea` | `02EB7250` | member "m_mouseButtonSemantic", offset 0x30 (constructor 00632960, called at 0086E119) |
| 008B9760 | `008B9760` `lea` | `02EB7430` | member "m_name", offset 0x8 (constructor 00632960, called at 0086D705) |
| 008B9770 | `008B9770` `lea` | `02EB7190` | member "m_negativeButtonSemantic", offset 0x38 (constructor 00632960, called at 0086DE55) |
| 008B9780 | `008B9780` `lea` | `02EB70D0` | member "m_negativeKeySemantic", offset 0x38 (constructor 00632960, called at 0086DF95) |
| 008B9790 | `008B9790` `lea` | `02EB7130` | member "m_positiveButtonSemantic", offset 0x30 (constructor 00632960, called at 0086DDE2) |
| 008B97A0 | `008B97A0` `lea` | `02EB7070` | member "m_positiveKeySemantic", offset 0x30 (constructor 00632960, called at 0086DF22) |
| 008B97B0 | `008B97B0` `lea` | `02EB7010` | member "m_scale", offset 0x20 (constructor 00632960, called at 0086DC4F) |
| 008B97C0 | `008B97C0` `lea` | `02EB6EF0` | member "m_typeSemantic", offset 0x10 (constructor 00632960, called at 0086DB02) |
| 008BDDC0 | `008BDDC0` `lea` | `02EB9950` | member "m_bounds", offset 0x18 (constructor 00632960, called at 00878862) |
| 008BDDD0 | `008BDDD0` `lea` | `02EB98F0` | member "m_cachedPosition", offset 0x8 (constructor 00632960, called at 008787F0) |
| 008BDDE0 | `008BDDE0` `lea` | `02EB9470` | member "m_center", offset passed in a register (constructor 00632960, called at 0087817E) |
| 008BDDF0 | `008BDDF0` `lea` | `02EB9A70` | member "m_center", offset passed in a register (constructor 00632960, called at 00878A0A) |
| 008BDE10 | `008BDE10` `lea` | `02EB96B0` | member "m_currentObjectCount", offset 0x30 (constructor 00632960, called at 00878430) |
| 008BDE20 | `008BDE20` `lea` | `02EB9C50` | member "m_dynamicOctree", offset 0x78 (constructor 00632960, called at 00878C3B) |
| 008BDE30 | `008BDE30` `lea` | `02EB94D0` | member "m_halfSize", offset 0x10 (constructor 00632960, called at 008781F1) |
| 008BDE40 | `008BDE40` `lea` | `02EB9AD0` | member "m_halfSize", offset 0x10 (constructor 00632960, called at 00878A79) |
| 008BDE50 | `008BDE50` `lea` | `02EB9590` | member "m_level", offset 0x24 (constructor 00632960, called at 008782D7) |
| 008BDE60 | `008BDE60` `lea` | `02EB95F0` | member "m_maxLevel", offset 0x28 (constructor 00632960, called at 0087834A) |
| 008BDE70 | `008BDE70` `lea` | `02EB9B90` | member "m_maxLevel", offset 0x24 (constructor 00632960, called at 00878B57) |
| 008BDE80 | `008BDE80` `lea` | `02EB9530` | member "m_maxRadius", offset 0x20 (constructor 00632960, called at 00878264) |
| 008BDE90 | `008BDE90` `lea` | `02EB9A10` | member "m_next", offset 0x20 (constructor 00632960, called at 00878946) |
| 008BDEA0 | `008BDEA0` `lea` | `02EB9650` | member "m_objectsPerLevel", offset 0x2C (constructor 00632960, called at 008783BD) |
| 008BDEB0 | `008BDEB0` `lea` | `02EB9B30` | member "m_objectsPerLevel", offset 0x20 (constructor 00632960, called at 00878AE8) |
| 008BDEC0 | `008BDEC0` `lea` | `02EB9890` | member "m_octree", offset passed in a register (constructor 00632960, called at 0087877D) |
| 008BDED0 | `008BDED0` `lea` | `02EB9BF0` | member "m_octree", offset 0x28 (constructor 00632960, called at 00878BC9) |
| 008BDEE0 | `008BDEE0` `lea` | `02EB9770` | member "m_octreeChildren", offset 0x40 (constructor 00632960, called at 00878515) |
| 008BDEF0 | `008BDEF0` `lea` | `02EB97D0` | member "m_octreeData", offset 0x38 (constructor 00632960, called at 00878587) |
| 008BDF00 | `008BDF00` `lea` | `02EB9830` | member "m_parent", offset 0x48 (constructor 00632960, called at 008785F9) |
| 008BDF10 | `008BDF10` `lea` | `02EB99B0` | member "m_prev", offset 0x28 (constructor 00632960, called at 008788D4) |
| 008BDF20 | `008BDF20` `lea` | `02EB9710` | member "m_totalObjectCount", offset 0x34 (constructor 00632960, called at 008784A3) |
| 008C1530 | `008C1530` `lea` | `02EBA140` | member "m_count", offset passed in a register (constructor 00632960, called at 0087A05A) |
| 008C1550 | `008C1550` `lea` | `02EB9F60` | member "m_inputMap", offset 0x10 (constructor 00632960, called at 00879DF1) |

### Registered through constructor `00632A10` (162, OPUS)

| member | distinguishing instruction | static object X | the data member X describes |
|---|---|---|---|
| 008AA080 | `008AA080` `lea` | `02CB2070` | member "m_channels", offset 0x8 (constructor 00632A10, called at 005B0448) |
| 008AA0C0 | `008AA0C0` `lea` | `02CB20E0` | member "m_constantChannels", offset 0x18 (constructor 00632A10, called at 005B04E1) |
| 008AA1D0 | `008AA1D0` `lea` | `02CB3480` | member "m_deferredLoad", offset 0x30 (constructor 00632A10, called at 005B1F43) |
| 008AA200 | `008AA200` `lea` | `02CB3D00` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B50A8) |
| 008AA210 | `008AA210` `lea` | `02CB3AD0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B53D8) |
| 008AA220 | `008AA220` `lea` | `02CB4160` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B570A) |
| 008AA230 | `008AA230` `lea` | `02CB50B0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B5A4A) |
| 008AA240 | `008AA240` `lea` | `02CB47F0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B5D87) |
| 008AA250 | `008AA250` `lea` | `02CB4390` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B60B7) |
| 008AA260 | `008AA260` `lea` | `02CB52E0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B63E7) |
| 008AA270 | `008AA270` `lea` | `02CB4C50` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B6717) |
| 008AA280 | `008AA280` `lea` | `02CB5510` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B6A47) |
| 008AA290 | `008AA290` `lea` | `02CB5740` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B6D77) |
| 008AA2A0 | `008AA2A0` `lea` | `02CB4E80` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B70A7) |
| 008AA2B0 | `008AA2B0` `lea` | `02CB4A20` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B73D7) |
| 008AA2C0 | `008AA2C0` `lea` | `02CB5970` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B7707) |
| 008AA2D0 | `008AA2D0` `lea` | `02CB3F30` | member "m_els", offset 0x8 (constructor 00632A10, called at 005B7A38) |
| 008AA2E0 | `008AA2E0` `lea` | `02CB28E0` | member "m_events", offset passed in a register (constructor 00632A10, called at 005B1496) |
| 008AA350 | `008AA350` `lea` | `02CB2C80` | member "m_instanceTargetNodes", offset 0x18 (constructor 00632A10, called at 005B161C) |
| 008AA480 | `008AA480` `lea` | `02CB2DB0` | member "m_persistentBuffer", offset 0x40 (constructor 00632A10, called at 005B179F) |
| 008AA4E0 | `008AA4E0` `lea` | `02CB2FD0` | member "m_slotArrayIndices", offset 0x20 (constructor 00632A10, called at 005B1ADB) |
| 008AA4F0 | `008AA4F0` `lea` | `02CB2E80` | member "m_slotArrays", offset 0x58 (constructor 00632A10, called at 005B18AB) |
| 008AA500 | `008AA500` `lea` | `02CB33B0` | member "m_slotBlockList", offset 0x18 (constructor 00632A10, called at 005B1E38) |
| 008AA520 | `008AA520` `lea` | `02CB14D0` | member "m_sourceWeights", offset 0x28 (constructor 00632A10, called at 005AEF65) |
| 008AA530 | `008AA530` `lea` | `02CB35B0` | member "m_sourceWeights", offset 0x28 (constructor 00632A10, called at 005B2515) |
| 008AA540 | `008AA540` `lea` | `02CB1540` | member "m_sources", offset 0x18 (constructor 00632A10, called at 005AF050) |
| 008AA590 | `008AA590` `lea` | `02CB2F60` | member "m_targets", offset 0x10 (constructor 00632A10, called at 005B1A42) |
| 008AA5E0 | `008AA5E0` `lea` | `02CB1BE0` | member "m_timeKeys", offset 0x8 (constructor 00632A10, called at 005AFB08) |
| 008AA620 | `008AA620` `lea` | `02CB4520` | member "m_u", offset 0x8 (constructor 00632A10, called at 005B7C6D) |
| 008AA640 | `008AA640` `lea` | `02CB1610` | member "m_valueKeys", offset 0x50 (constructor 00632A10, called at 005AF1BA) |
| 008AD090 | `008AD090` `lea` | `02CE9410` | member "m_compileOptions", offset 0x10 (constructor 00632A10, called at 005EA6E3) |
| 008AD100 | `008AD100` `lea` | `02CE2A10` | member "m_contextSwitches", offset 0x48 (constructor 00632A10, called at 005E43FC) |
| 008AD150 | `008AD150` `lea` | `02CE2A80` | member "m_contextVariantSwitches", offset 0x58 (constructor 00632A10, called at 005E448E) |
| 008AD300 | `008AD300` `lea` | `02CE37B0` | member "m_currentPose", offset 0x10 (constructor 00632A10, called at 005E5592) |
| 008AD400 | `008AD400` `lea` | `02CE28C0` | member "m_effectVariants", offset 0x18 (constructor 00632A10, called at 005E4237) |
| 008AD430 | `008AD430` `lea` | `02CEC050` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EBA6A) |
| 008AD440 | `008AD440` `lea` | `02CECFA0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EBDAA) |
| 008AD450 | `008AD450` `lea` | `02CEBE20` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EC0EA) |
| 008AD460 | `008AD460` `lea` | `02CEC6E0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EC42B) |
| 008AD470 | `008AD470` `lea` | `02CEC280` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EC76B) |
| 008AD480 | `008AD480` `lea` | `02CEC4B0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005ECAAB) |
| 008AD490 | `008AD490` `lea` | `02CEB790` | member "m_els", offset 0x8 (constructor 00632A10, called at 005ECDE7) |
| 008AD4A0 | `008AD4A0` `lea` | `02CEB9C0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005ED117) |
| 008AD4B0 | `008AD4B0` `lea` | `02CEA1B0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005ED448) |
| 008AD4C0 | `008AD4C0` `lea` | `02CECD70` | member "m_els", offset 0x8 (constructor 00632A10, called at 005ED777) |
| 008AD4D0 | `008AD4D0` `lea` | `02CEC910` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EDAA7) |
| 008AD4E0 | `008AD4E0` `lea` | `02CEBBF0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EDDD7) |
| 008AD4F0 | `008AD4F0` `lea` | `02CEB330` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EE107) |
| 008AD500 | `008AD500` `lea` | `02CEACA0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EE437) |
| 008AD510 | `008AD510` `lea` | `02CEA840` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EE767) |
| 008AD520 | `008AD520` `lea` | `02CEAA70` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EEA97) |
| 008AD530 | `008AD530` `lea` | `02CEA610` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EEDC7) |
| 008AD540 | `008AD540` `lea` | `02CEAED0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EF0F7) |
| 008AD550 | `008AD550` `lea` | `02CEB560` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EF427) |
| 008AD560 | `008AD560` `lea` | `02CEA3E0` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EF757) |
| 008AD570 | `008AD570` `lea` | `02CE9F80` | member "m_els", offset 0x8 (constructor 00632A10, called at 005EFA87) |
| 008AD590 | `008AD590` `lea` | `02CE7A40` | member "m_entryPoints", offset 0x18 (constructor 00632A10, called at 005E8004) |
| 008AD800 | `008AD800` `lea` | `02CE4450` | member "m_modifierNetworkInstances", offset 0x18 (constructor 00632A10, called at 005E6BE0) |
| 008AD8B0 | `008AD8B0` `lea` | `02CE44C0` | member "m_packedSwitches", offset passed in a register (constructor 00632A10, called at 005E6CCB) |
| 008AD910 | `008AD910` `lea` | `02CE9550` | member "m_parameterDefinitions", offset 0x10 (constructor 00632A10, called at 005EA515) |
| 008AD920 | `008AD920` `lea` | `02CE8140` | member "m_parameterDefinitionsForPasses", offset 0x18 (constructor 00632A10, called at 005E8315) |
| 008AD930 | `008AD930` `lea` | `02CE8840` | member "m_parameterLocations", offset 0x10 (constructor 00632A10, called at 005EA090) |
| 008AD940 | `008AD940` `lea` | `02CE88B0` | member "m_parameterLocations", offset 0x10 (constructor 00632A10, called at 005EA2C0) |
| 008AD990 | `008AD990` `lea` | `02CE80D0` | member "m_passes", offset 0x8 (constructor 00632A10, called at 005E8283) |
| 008AD9A0 | `008AD9A0` `lea` | `02CE7B20` | member "m_platforms", offset 0x38 (constructor 00632A10, called at 005E8128) |
| 008ADA80 | `008ADA80` `lea` | `02CE2CF0` | member "m_sceneRenderPassLookup", offset 0x28 (constructor 00632A10, called at 005E47EA) |
| 008ADA90 | `008ADA90` `lea` | `02CE2C80` | member "m_sceneRenderPasses", offset 0x18 (constructor 00632A10, called at 005E4758) |
| 008ADAA0 | `008ADAA0` `lea` | `02CE3A00` | member "m_segmentContext", offset 0x48 (constructor 00632A10, called at 005E5865) |
| 008ADAB0 | `008ADAB0` `lea` | `02CE79D0` | member "m_shaders", offset 0x8 (constructor 00632A10, called at 005E7F72) |
| 008ADB60 | `008ADB60` `lea` | `02CE3680` | member "m_streamBindings", offset 0x38 (constructor 00632A10, called at 005E6860) |
| 008ADB70 | `008ADB70` `lea` | `02CE94E0` | member "m_streamDefinitions", offset 0x0 (constructor 00632A10, called at 005EA474) |
| 008ADB80 | `008ADB80` `lea` | `02CE81B0` | member "m_streamDefinitionsForPasses", offset 0x28 (constructor 00632A10, called at 005E83A7) |
| 008ADB90 | `008ADB90` `lea` | `02CE8AA0` | member "m_streamLocations", offset 0x20 (constructor 00632A10, called at 005E9BD7) |
| 008ADBD0 | `008ADBD0` `lea` | `02CE2930` | member "m_supportedLightTypes", offset 0x28 (constructor 00632A10, called at 005E42CE) |
| 008ADBF0 | `008ADBF0` `lea` | `02CE29A0` | member "m_supportedShadowCasterTypes", offset 0x38 (constructor 00632A10, called at 005E4365) |
| 008ADC00 | `008ADC00` `lea` | `02CE2C10` | member "m_switches", offset 0x8 (constructor 00632A10, called at 005E46C6) |
| 008ADC90 | `008ADC90` `lea` | `02CE2DC0` | member "m_tweakableShaderParameterDefinitions", offset 0x40 (constructor 00632A10, called at 005E48F2) |
| 008ADCA0 | `008ADCA0` `lea` | `02CE45F0` | member "m_tweakableShaderParameterDefinitions", offset 0x10 (constructor 00632A10, called at 005E6E2E) |
| 008ADCD0 | `008ADCD0` `lea` | `02CEB060` | member "m_u", offset 0x8 (constructor 00632A10, called at 005EFCBB) |
| 008ADCE0 | `008ADCE0` `lea` | `02CECAA0` | member "m_u", offset 0x8 (constructor 00632A10, called at 005F000D) |
| 008ADD00 | `008ADD00` `lea` | `02CE2E30` | member "m_untweakableShaderParameterDefinitions", offset 0x50 (constructor 00632A10, called at 005E497D) |
| 008ADD30 | `008ADD30` `lea` | `02CE7AB0` | member "m_variantsFoldingTable", offset 0x28 (constructor 00632A10, called at 005E8096) |
| 008AEC70 | `008AEC70` `lea` | `02CF6930` | member "m_compiledCode", offset 0x18 (constructor 00632A10, called at 00618128) |
| 008AED20 | `008AED20` `lea` | `02CF6DF0` | member "m_els", offset 0x8 (constructor 00632A10, called at 00618C18) |
| 008AED30 | `008AED30` `lea` | `02CF7020` | member "m_els", offset 0x8 (constructor 00632A10, called at 00618F47) |
| 008AEE20 | `008AEE20` `lea` | `02CF68C0` | member "m_streams", offset passed in a register (constructor 00632A10, called at 006186B6) |
| 008B0950 | `008B0950` `lea` | `02D38420` | member "m_els", offset 0x8 (constructor 00632A10, called at 0064ACCA) |
| 008B0AC0 | `008B0AC0` `lea` | `02D38020` | member "m_postEffects", offset passed in a register (constructor 00632A10, called at 0064925B) |
| 008B14E0 | `008B14E0` `lea` | `02D3B0E0` | member "m_buffers", offset 0x20 (constructor 00632A10, called at 00665913) |
| 008B14F0 | `008B14F0` `lea` | `02D3AFB0` | member "m_buffers", offset 0x18 (constructor 00632A10, called at 00666423) |
| 008B15B0 | `008B15B0` `lea` | `02D3B4D0` | member "m_data", offset 0x18 (constructor 00632A10, called at 00665C63) |
| 008B15F0 | `008B15F0` `lea` | `02D3BE60` | member "m_defaultPose", offset 0x30 (constructor 00632A10, called at 00666B33) |
| 008B1600 | `008B1600` `lea` | `02D3B6C0` | member "m_dynamicStreams", offset 0x10 (constructor 00632A10, called at 00665D53) |
| 008B1650 | `008B1650` `lea` | `02D3CA60` | member "m_els", offset 0x8 (constructor 00632A10, called at 00668D88) |
| 008B1660 | `008B1660` `lea` | `02D3DE10` | member "m_els", offset 0x8 (constructor 00632A10, called at 006690B8) |
| 008B1670 | `008B1670` `lea` | `02D3D550` | member "m_els", offset 0x8 (constructor 00632A10, called at 006693E7) |
| 008B1680 | `008B1680` `lea` | `02D3E040` | member "m_els", offset 0x8 (constructor 00632A10, called at 00669717) |
| 008B1690 | `008B1690` `lea` | `02D3D9B0` | member "m_els", offset 0x8 (constructor 00632A10, called at 00669A47) |
| 008B16A0 | `008B16A0` `lea` | `02D3DBE0` | member "m_els", offset 0x8 (constructor 00632A10, called at 00669D77) |
| 008B16B0 | `008B16B0` `lea` | `02D3D320` | member "m_els", offset 0x8 (constructor 00632A10, called at 0066A0A7) |
| 008B16C0 | `008B16C0` `lea` | `02D3CC90` | member "m_els", offset 0x8 (constructor 00632A10, called at 0066A3D7) |
| 008B1740 | `008B1740` `lea` | `02D3C4D0` | member "m_indices", offset 0x8 (constructor 00632A10, called at 00667454) |
| 008B1770 | `008B1770` `lea` | `02D3B9E0` | member "m_materials", offset passed in a register (constructor 00632A10, called at 006665F9) |
| 008B1790 | `008B1790` `lea` | `02D3BED0` | member "m_matrixNames", offset 0x40 (constructor 00632A10, called at 00666BC5) |
| 008B17A0 | `008B17A0` `lea` | `02D3BF40` | member "m_matrixParents", offset 0x50 (constructor 00632A10, called at 00666C6A) |
| 008B17F0 | `008B17F0` `lea` | `02D3BD10` | member "m_meshSegments", offset passed in a register (constructor 00632A10, called at 0066695E) |
| 008B1870 | `008B1870` `lea` | `02D3C070` | member "m_ps2DLIndices", offset 0x70 (constructor 00632A10, called at 00666E3D) |
| 008B1890 | `008B1890` `lea` | `02D3B730` | member "m_segments", offset 0x20 (constructor 00632A10, called at 00665DEC) |
| 008B18C0 | `008B18C0` `lea` | `02D3BDF0` | member "m_skeletonBounds", offset 0x20 (constructor 00632A10, called at 00666A95) |
| 008B18D0 | `008B18D0` `lea` | `02D3BD80` | member "m_skeletonMatrices", offset 0x10 (constructor 00632A10, called at 00666A03) |
| 008B18F0 | `008B18F0` `lea` | `02D3C260` | member "m_skinBones", offset 0x8 (constructor 00632A10, called at 00667015) |
| 008B1930 | `008B1930` `lea` | `02D3B330` | member "m_streams", offset 0x8 (constructor 00632A10, called at 00665818) |
| 008B1940 | `008B1940` `lea` | `02D3B460` | member "m_streams", offset 0x8 (constructor 00632A10, called at 00665BC5) |
| 008B1990 | `008B1990` `lea` | `02D3D6E0` | member "m_u", offset 0x8 (constructor 00632A10, called at 0066A60D) |
| 008B19A0 | `008B19A0` `lea` | `02D3CE20` | member "m_u", offset 0x8 (constructor 00632A10, called at 0066A95A) |
| 008B19B0 | `008B19B0` `lea` | `02D3D050` | member "m_u", offset 0x8 (constructor 00632A10, called at 0066ACAA) |
| 008B19D0 | `008B19D0` `lea` | `02D3AEE0` | member "m_vertexData", offset 0x30 (constructor 00632A10, called at 006672D4) |
| 008B19E0 | `008B19E0` `lea` | `02D3C600` | member "m_vertexData", offset 0x20 (constructor 00632A10, called at 006675CD) |
| 008B2030 | `008B2030` `lea` | `02E40070` | member "m_characterInfo", offset 0x10 (constructor 00632A10, called at 0067D24B) |
| 008B2050 | `008B2050` `lea` | `02E40360` | member "m_els", offset 0x8 (constructor 00632A10, called at 0067DAB7) |
| 008B20B0 | `008B20B0` `lea` | `02E400E0` | member "m_kerningInfo", offset 0x20 (constructor 00632A10, called at 0067D2E9) |
| 008B2520 | `008B2520` `lea` | `02E42700` | member "m_functionNames", offset 0x20 (constructor 00632A10, called at 006824B9) |
| 008B2590 | `008B2590` `lea` | `02E42620` | member "m_scriptChunk32", offset passed in a register (constructor 00632A10, called at 00682390) |
| 008B25A0 | `008B25A0` `lea` | `02E42690` | member "m_scriptChunk64", offset 0x10 (constructor 00632A10, called at 00682427) |
| 008B3A80 | `008B3A80` `lea` | `02E4B7C0` | member "m_shapes", offset 0xB0 (constructor 00632A10, called at 00696A0B) |
| 008B3B60 | `008B3B60` `lea` | `02E4D180` | member "m_u", offset 0x8 (constructor 00632A10, called at 00698ADD) |
| 008B3F10 | `008B3F10` `lea` | `02E4D730` | member "m_buffer", offset passed in a register (constructor 00632A10, called at 006A734E) |
| 008B40D0 | `008B40D0` `lea` | `02E4DB60` | member "m_triggerReceivers", offset 0x8 (constructor 00632A10, called at 006A80DC) |
| 008B40F0 | `008B40F0` `lea` | `02E4DEC0` | member "m_u", offset 0x8 (constructor 00632A10, called at 006A866D) |
| 008B48C0 | `008B48C0` `lea` | `02E4FDA0` | member "m_els", offset 0x8 (constructor 00632A10, called at 006AEA27) |
| 008B48D0 | `008B48D0` `lea` | `02E4FB80` | member "m_instances", offset 0x18 (constructor 00632A10, called at 006AE725) |
| 008B5DF0 | `008B5DF0` `lea` | `02E58650` | member "m_els", offset 0x8 (constructor 00632A10, called at 006BCEEB) |
| 008B5E00 | `008B5E00` `lea` | `02E58AB0` | member "m_els", offset 0x8 (constructor 00632A10, called at 006BD227) |
| 008B5E10 | `008B5E10` `lea` | `02E58880` | member "m_els", offset 0x8 (constructor 00632A10, called at 006BD557) |
| 008B5E30 | `008B5E30` `lea` | `02E58350` | member "m_modifierNetworkInputRenderStreams", offset 0x48 (constructor 00632A10, called at 006BC891) |
| 008B5E40 | `008B5E40` `lea` | `02E582E0` | member "m_modifierNetworkInputs", offset 0x38 (constructor 00632A10, called at 006BC7F8) |
| 008B5E50 | `008B5E50` `lea` | `02E583C0` | member "m_modifierNetworkOutputs", offset 0x58 (constructor 00632A10, called at 006BC92F) |
| 008B5E80 | `008B5E80` `lea` | `02E58430` | member "m_segmentInputs", offset 0x68 (constructor 00632A10, called at 006BC9C8) |
| 008B68C0 | `008B68C0` `lea` | `02E5A2D0` | member "m_els", offset 0x8 (constructor 00632A10, called at 006C1BC7) |
| 008B6900 | `008B6900` `lea` | `02E59F90` | member "m_splits", offset 0x10 (constructor 00632A10, called at 006C1673) |
| 008B69D0 | `008B69D0` `lea` | `02E5AC30` | member "m_els", offset 0x8 (constructor 00632A10, called at 006C3AAB) |
| 008B6A00 | `008B6A00` `lea` | `02E5A9A0` | member "m_modifierUserData", offset 0x8 (constructor 00632A10, called at 006C3496) |
| 008B6A10 | `008B6A10` `lea` | `02E5AA10` | member "m_persistentState", offset 0x18 (constructor 00632A10, called at 006C3534) |
| 008B6C30 | `008B6C30` `lea` | `02E5BA50` | member "m_els", offset 0x8 (constructor 00632A10, called at 006C64D7) |
| 008B6C50 | `008B6C50` `lea` | `02E5B2A0` | member "m_levels", offset 0x50 (constructor 00632A10, called at 006C5AFD) |
| 008B6CB0 | `008B6CB0` `lea` | `02E5B170` | member "m_meshInstances", offset 0x8 (constructor 00632A10, called at 006C6101) |
| 008B6CF0 | `008B6CF0` `lea` | `02E5B780` | member "m_u", offset 0x8 (constructor 00632A10, called at 006C670D) |
| 008B7310 | `008B7310` `lea` | `02E9FA00` | member "m_els", offset 0x8 (constructor 00632A10, called at 006D2637) |
| 008B7320 | `008B7320` `lea` | `02E9FC30` | member "m_els", offset 0x8 (constructor 00632A10, called at 006D2967) |
| 008B7330 | `008B7330` `lea` | `02E9F7D0` | member "m_els", offset 0x8 (constructor 00632A10, called at 006D2C97) |
| 008B7380 | `008B7380` `lea` | `02E5F5B0` | member "m_inputElementCountSources", offset 0x60 (constructor 00632A10, called at 006D1530) |
| 008B73A0 | `008B73A0` `lea` | `02E5EAC0` | member "m_inputs", offset 0x10 (constructor 00632A10, called at 006D0F48) |
| 008B73B0 | `008B73B0` `lea` | `02E5F280` | member "m_inputs", offset 0x20 (constructor 00632A10, called at 006D115B) |
| 008B7420 | `008B7420` `lea` | `02E5F1B0` | member "m_modifiers", offset 0x8 (constructor 00632A10, called at 006D1048) |
| 008B7450 | `008B7450` `lea` | `02E5F2F0` | member "m_outputs", offset 0x30 (constructor 00632A10, called at 006D11ED) |
| 008B76A0 | `008B76A0` `lea` | `02EA0670` | member "m_weights", offset passed in a register (constructor 00632A10, called at 006D8F8B) |
| 008B96A0 | `008B96A0` `lea` | `02EB7A10` | member "m_els", offset 0x8 (constructor 00632A10, called at 0086E71A) |
| 008B96B0 | `008B96B0` `lea` | `02EB77E0` | member "m_els", offset 0x8 (constructor 00632A10, called at 0086EA5A) |
| 008B96D0 | `008B96D0` `lea` | `02EB75C0` | member "m_inputActions", offset passed in a register (constructor 00632A10, called at 0086DA26) |
| 008B96E0 | `008B96E0` `lea` | `02EB7490` | member "m_inputSources", offset 0x10 (constructor 00632A10, called at 0086D789) |
| 008C1540 | `008C1540` `lea` | `02EBA1E0` | member "m_els", offset 0x8 (constructor 00632A10, called at 0087A16A) |
| 008C1560 | `008C1560` `lea` | `02EB9FC0` | member "m_inputMaps", offset passed in a register (constructor 00632A10, called at 00879E71) |

## Per-member rows: the vtable each descriptor destructor thunk restores, and its reflected type (OPUS, 2026-10-03)

The family `PClassDescriptorForType destructor thunks` (frontmatter: 384 members; 384 get a row here) shares one form, not repeated per row: `lea rax, [V]`, `mov qword ptr [rcx], rax`, then a tail jump to the shared descriptor destructor `00633390`. Members differ only at the first instruction, the vtable V the thunk stores back into the object before the shared destructor runs, so the anchor is the entry `lea` (the family sentence OPUS adopted in `opus-ee-rulings-1003` allows the entry instruction when members differ there). Each row states V and the class whose MSVC RTTI complete-object locator precedes V, read from the certified image: the template argument T of `PClassDescriptor*<T>`, or the decorated name when it is a template type. [`fam_rows.py`](../../_index/candidates/opus-ee-descriptor-dtor-thunks-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-descriptor-dtor-thunks-1003/rows.tsv). A body that leaves the form, a vtable without a locator, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-descriptor-dtor-thunks-1003/excluded.tsv).

### All 384 thunks (OPUS)

| member | distinguishing instruction | vtable V restored | reflected type (RTTI before V) |
|---|---|---|---|
| 00597EC0 | `00597EC0` `lea` | `00D24898` | Phyre::PSerialization::PBinary::PClusterHeader |
| 00597ED0 | `00597ED0` `lea` | `00D24540` | Phyre::PSerialization::PBinary::PClusterHeaderBase |
| 00597EE0 | `00597EE0` `lea` | `00D246F0` | Phyre::PSerialization::PBinary::PClusterHeaderD3D11 |
| 00597EF0 | `00597EF0` `lea` | `00D24A48` | Phyre::PSerialization::PBinary::PInternal::PInstanceListHeader |
| 005A99C0 | `005A99C0` `lea` | `00D32DD0` | decorated `V?$PArray@I$03@Phyre@@` |
| 005A99D0 | `005A99D0` `lea` | `00D32BB8` | decorated `V?$PArray@M$03@Phyre@@` |
| 005A99E0 | `005A99E0` `lea` | `00D331C0` | decorated `V?$PArray@PEAVPAnimationChannel@PAnimation@Phyre@@$07@Phyre@@` |
| 005A99F0 | `005A99F0` `lea` | `00D33F90` | decorated `V?$PArray@PEAVPAnimationDataSource@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A00 | `005A9A00` `lea` | `00D337B0` | decorated `V?$PArray@VPAnimationChannelTarget@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A10 | `005A9A10` `lea` | `00D333B8` | decorated `V?$PArray@VPAnimationConstantChannel@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A20 | `005A9A20` `lea` | `00D34188` | decorated `V?$PArray@VPAnimationDataSourceListEntry@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A30 | `005A9A30` `lea` | `00D33BA0` | decorated `V?$PArray@VPAnimationEvent@PAnimation@Phyre@@$03@Phyre@@` |
| 005A9A40 | `005A9A40` `lea` | `00D34380` | decorated `V?$PArray@VPAnimationNetworkInstanceTarget@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A50 | `005A9A50` `lea` | `00D34578` | decorated `V?$PArray@VPAnimationSlotArray@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A60 | `005A9A60` `lea` | `00D33D98` | decorated `V?$PArray@VPAnimationSlotFilterDeferredLoad@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A70 | `005A9A70` `lea` | `00D339A8` | decorated `V?$PArray@VPAnimationSlotListIndex@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A80 | `005A9A80` `lea` | `00D34770` | decorated `V?$PArray@VPBlendableAnimationSource@PAnimation@Phyre@@$07@Phyre@@` |
| 005A9A90 | `005A9A90` `lea` | `00D32FC8` | decorated `V?$PArray@VPQWord@Phyre@@$0BA@@Phyre@@` |
| 005A9AA0 | `005A9AA0` `lea` | `00D335B0` | decorated `V?$PSharray@PEAVPAnimationClip@PAnimation@Phyre@@@Phyre@@` |
| 005A9AB0 | `005A9AB0` `lea` | `00D29A38` | Phyre::PAnimation::PAnimatableComponent |
| 005A9AC0 | `005A9AC0` `lea` | `00D2C4D0` | Phyre::PAnimation::PAnimationAdditiveBlenderController |
| 005A9AD0 | `005A9AD0` `lea` | `00D2B060` | Phyre::PAnimation::PAnimationBlenderController |
| 005A9AE0 | `005A9AE0` `lea` | `00D29928` | Phyre::PAnimation::PAnimationChannel |
| 005A9AF0 | `005A9AF0` `lea` | `00D29198` | Phyre::PAnimation::PAnimationChannelBase |
| 005A9B00 | `005A9B00` `lea` | `00D27DE8` | Phyre::PAnimation::PAnimationChannelTarget |
| 005A9B10 | `005A9B10` `lea` | `00D2C558` | Phyre::PAnimation::PAnimationChannelTimes |
| 005A9B20 | `005A9B20` `lea` | `00D28A78` | Phyre::PAnimation::PAnimationClip |
| 005A9B30 | `005A9B30` `lea` | `00D2B298` | Phyre::PAnimation::PAnimationClipBinding |
| 005A9B40 | `005A9B40` `lea` | `00D2BB18` | Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap |
| 005A9B50 | `005A9B50` `lea` | `00D2C200` | Phyre::PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache |
| 005A9B60 | `005A9B60` `lea` | `00D2A470` | Phyre::PAnimation::PAnimationConstantChannel |
| 005A9B70 | `005A9B70` `lea` | `00D280B8` | Phyre::PAnimation::PAnimationController |
| 005A9B80 | `005A9B80` `lea` | `00D2C0A8` | Phyre::PAnimation::PAnimationDataSource |
| 005A9B90 | `005A9B90` `lea` | `00D29F18` | Phyre::PAnimation::PAnimationDataSourceListEntry |
| 005A9BA0 | `005A9BA0` `lea` | `00D2B3A8` | Phyre::PAnimation::PAnimationEvent |
| 005A9BB0 | `005A9BB0` `lea` | `00D2CA90` | Phyre::PAnimation::PAnimationEventController |
| 005A9BC0 | `005A9BC0` `lea` | `00D2C3C0` | Phyre::PAnimation::PAnimationEventList |
| 005A9BD0 | `005A9BD0` `lea` | `00D2CED0` | Phyre::PAnimation::PAnimationHierarchyNode |
| 005A9BE0 | `005A9BE0` `lea` | `00D2CCE0` | Phyre::PAnimation::PAnimationNetworkInstance |
| 005A9BF0 | `005A9BF0` `lea` | `00D2A980` | Phyre::PAnimation::PAnimationNetworkInstanceTarget |
| 005A9C00 | `005A9C00` `lea` | `00D2AB88` | Phyre::PAnimation::PAnimationSet |
| 005A9C10 | `005A9C10` `lea` | `00D2B9F0` | Phyre::PAnimation::PAnimationSlotArray |
| 005A9C20 | `005A9C20` `lea` | `00D29E08` | Phyre::PAnimation::PAnimationSlotFilter |
| 005A9C30 | `005A9C30` `lea` | `00D28C78` | Phyre::PAnimation::PAnimationSlotFilterDeferredLoad |
| 005A9C40 | `005A9C40` `lea` | `00D2B100` | Phyre::PAnimation::PAnimationSlotListIndex |
| 005A9C50 | `005A9C50` `lea` | `00D2CFE0` | Phyre::PAnimation::PAnimationSpuTargetBlenderController |
| 005A9C60 | `005A9C60` `lea` | `00D286B8` | Phyre::PAnimation::PAnimationTargetBlenderController |
| 005A9C70 | `005A9C70` `lea` | `00D2B888` | Phyre::PAnimation::PAnimationWeightedBlenderController |
| 005A9C80 | `005A9C80` `lea` | `00D284B0` | Phyre::PAnimation::PBlendableAnimationSource |
| 005A9C90 | `005A9C90` `lea` | `00D28D78` | Phyre::PAnimation::PTimeController |
| 005A9CA0 | `005A9CA0` `lea` | `00D29700` | Phyre::PAnimation::PTimeIntervalController |
| 005A9CB0 | `005A9CB0` `lea` | `00D2A268` | Phyre::PAnimation::PTimeScaleOffsetController |
| 005DCFF0 | `005DCFF0` `lea` | `00D4D338` | decorated `V?$PArray@PEAVPEffectVariant@PRendering@Phyre@@$07@Phyre@@` |
| 005DD000 | `005DD000` `lea` | `00D4E100` | decorated `V?$PArray@PEAVPModifierNetworkInstance@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 005DD010 | `005DD010` `lea` | `00D4D140` | decorated `V?$PArray@PEAVPSceneRenderPass@PRendering@Phyre@@$07@Phyre@@` |
| 005DD020 | `005DD020` `lea` | `00D4D920` | decorated `V?$PArray@PEBVPContextSwitch@PRendering@Phyre@@$07@Phyre@@` |
| 005DD030 | `005DD030` `lea` | `00D4D530` | decorated `V?$PArray@PEBVPLightType@PRendering@Phyre@@$07@Phyre@@` |
| 005DD040 | `005DD040` `lea` | `00D4D728` | decorated `V?$PArray@PEBVPShadowCasterType@PRendering@Phyre@@$07@Phyre@@` |
| 005DD050 | `005DD050` `lea` | `00D4CB58` | decorated `V?$PArray@VPContextVariantFoldingTable@PRendering@Phyre@@$03@Phyre@@` |
| 005DD060 | `005DD060` `lea` | `00D4CD50` | decorated `V?$PArray@VPMaterialSwitch@PRendering@Phyre@@$07@Phyre@@` |
| 005DD070 | `005DD070` `lea` | `00D4B7A8` | decorated `V?$PArray@VPMatrix4@Phyre@@$03@Phyre@@` |
| 005DD080 | `005DD080` `lea` | `00D4DF08` | decorated `V?$PArray@VPMeshInstanceSegmentContext@PRendering@Phyre@@$07@Phyre@@` |
| 005DD090 | `005DD090` `lea` | `00D4DB18` | decorated `V?$PArray@VPNodeContext@PRendering@Phyre@@$07@Phyre@@` |
| 005DD0A0 | `005DD0A0` `lea` | `00D4CF48` | decorated `V?$PArray@VPSceneRenderPass@PRendering@Phyre@@$07@Phyre@@` |
| 005DD0B0 | `005DD0B0` `lea` | `00D4C768` | decorated `V?$PArray@VPShader@PRendering@Phyre@@$07@Phyre@@` |
| 005DD0C0 | `005DD0C0` `lea` | `00D4C180` | decorated `V?$PArray@VPShaderParameterCaptureBufferLocation@PRendering@Phyre@@$01@Phyre@@` |
| 005DD0D0 | `005DD0D0` `lea` | `00D4BD90` | decorated `V?$PArray@VPShaderParameterCaptureBufferLocationType@PRendering@Phyre@@$01@Phyre@@` |
| 005DD0E0 | `005DD0E0` `lea` | `00D4BF88` | decorated `V?$PArray@VPShaderParameterCaptureBufferLocationTypeConstantBuffer@PRendering@Phyre@@$03@Phyre@@` |
| 005DD0F0 | `005DD0F0` `lea` | `00D4BB98` | decorated `V?$PArray@VPShaderParameterDefinition@PRendering@Phyre@@$07@Phyre@@` |
| 005DD100 | `005DD100` `lea` | `00D4C378` | decorated `V?$PArray@VPShaderPass@PRendering@Phyre@@$07@Phyre@@` |
| 005DD110 | `005DD110` `lea` | `00D4C960` | decorated `V?$PArray@VPShaderPassInfo@PRendering@Phyre@@$07@Phyre@@` |
| 005DD120 | `005DD120` `lea` | `00D4B9A0` | decorated `V?$PArray@VPShaderStreamDefinition@PRendering@Phyre@@$07@Phyre@@` |
| 005DD130 | `005DD130` `lea` | `00D4B5B0` | decorated `V?$PArray@VPString@Phyre@@$07@Phyre@@` |
| 005DD140 | `005DD140` `lea` | `00D4C570` | decorated `V?$PSharray@I@Phyre@@` |
| 005DD150 | `005DD150` `lea` | `00D4DD10` | decorated `V?$PSharray@PEBVPMeshInstanceSegmentStreamBinding@PRendering@Phyre@@@Phyre@@` |
| 005DD160 | `005DD160` `lea` | `00D3B780` | Phyre::PRendering::PConstantBuffer |
| 005DD170 | `005DD170` `lea` | `00D36738` | Phyre::PRendering::PConstantBufferBase |
| 005DD180 | `005DD180` `lea` | `00D36DF8` | Phyre::PRendering::PContextVariantFoldingTable |
| 005DD190 | `005DD190` `lea` | `00D413A0` | Phyre::PRendering::PDynamicMeshInstance |
| 005DD1A0 | `005DD1A0` `lea` | `00D3F608` | Phyre::PRendering::PEffect |
| 005DD1B0 | `005DD1B0` `lea` | `00D381F8` | Phyre::PRendering::PEffectVariant |
| 005DD1C0 | `005DD1C0` `lea` | `00D40078` | Phyre::PRendering::PForwardShadowRenderer |
| 005DD1D0 | `005DD1D0` `lea` | `00D42650` | Phyre::PRendering::PIndirectArgsBuffer |
| 005DD1E0 | `005DD1E0` `lea` | `00D3FCC0` | Phyre::PRendering::PIndirectArgsBufferBase |
| 005DD1F0 | `005DD1F0` `lea` | `00D3E8B8` | Phyre::PRendering::PMaterial |
| 005DD200 | `005DD200` `lea` | `00D3C940` | Phyre::PRendering::PMaterialSwitch |
| 005DD210 | `005DD210` `lea` | `00D3F550` | Phyre::PRendering::PMeshInstance |
| 005DD220 | `005DD220` `lea` | `00D361C0` | Phyre::PRendering::PMeshInstanceAttachPoint |
| 005DD230 | `005DD230` `lea` | `00D3B3F0` | Phyre::PRendering::PMeshInstanceBounds |
| 005DD240 | `005DD240` `lea` | `00D37920` | Phyre::PRendering::PMeshInstanceSegmentContext |
| 005DD250 | `005DD250` `lea` | `00D41DE8` | Phyre::PRendering::PMeshInstanceSegmentStreamBinding |
| 005DD260 | `005DD260` `lea` | `00D367F0` | Phyre::PRendering::PModifierNetworkDynamicMeshInstance |
| 005DD270 | `005DD270` `lea` | `00D3A418` | Phyre::PRendering::PNodeContext |
| 005DD280 | `005DD280` `lea` | `00D3ADA8` | Phyre::PRendering::PParameterBuffer |
| 005DD290 | `005DD290` `lea` | `00D39498` | Phyre::PRendering::PParameterBufferBase |
| 005DD2A0 | `005DD2A0` `lea` | `00D3D500` | Phyre::PRendering::PRenderTarget |
| 005DD2B0 | `005DD2B0` `lea` | `00D39050` | Phyre::PRendering::PRenderTargetBase |
| 005DD2C0 | `005DD2C0` `lea` | `00D36BB8` | Phyre::PRendering::PSamplerState |
| 005DD2D0 | `005DD2D0` `lea` | `00D40398` | Phyre::PRendering::PSamplerStateBase |
| 005DD2E0 | `005DD2E0` `lea` | `00D3C380` | Phyre::PRendering::PSceneRenderPass |
| 005DD2F0 | `005DD2F0` `lea` | `00D41A58` | Phyre::PRendering::PSceneWideParameterBuffer |
| 005DD300 | `005DD300` `lea` | `00D3D810` | Phyre::PRendering::PShader |
| 005DD310 | `005DD310` `lea` | `00D416A0` | Phyre::PRendering::PShaderComputeProgram |
| 005DD320 | `005DD320` `lea` | `00D3E460` | Phyre::PRendering::PShaderFragmentProgram |
| 005DD330 | `005DD330` `lea` | `00D40420` | Phyre::PRendering::PShaderGeometryProgram |
| 005DD340 | `005DD340` `lea` | `00D3CEA0` | Phyre::PRendering::PShaderParameterCaptureBufferByteAddressBuffer |
| 005DD350 | `005DD350` `lea` | `00D41090` | Phyre::PRendering::PShaderParameterCaptureBufferDataBlock |
| 005DD360 | `005DD360` `lea` | `00D42140` | Phyre::PRendering::PShaderParameterCaptureBufferIndexDataBlock |
| 005DD370 | `005DD370` `lea` | `00D3DEA0` | Phyre::PRendering::PShaderParameterCaptureBufferLocation |
| 005DD380 | `005DD380` `lea` | `00D3FBB0` | Phyre::PRendering::PShaderParameterCaptureBufferLocationSize |
| 005DD390 | `005DD390` `lea` | `00D41118` | Phyre::PRendering::PShaderParameterCaptureBufferLocationType |
| 005DD3A0 | `005DD3A0` `lea` | `00D42268` | Phyre::PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 005DD3B0 | `005DD3B0` `lea` | `00D3DF28` | Phyre::PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer |
| 005DD3C0 | `005DD3C0` `lea` | `00D3BB20` | Phyre::PRendering::PShaderParameterCaptureBufferRWStructuredBuffer |
| 005DD3D0 | `005DD3D0` `lea` | `00D36120` | Phyre::PRendering::PShaderParameterCaptureBufferRWTexture2D |
| 005DD3E0 | `005DD3E0` `lea` | `00D377D8` | Phyre::PRendering::PShaderParameterCaptureBufferRWTexture3D |
| 005DD3F0 | `005DD3F0` `lea` | `00D39190` | Phyre::PRendering::PShaderParameterCaptureBufferSampler |
| 005DD400 | `005DD400` `lea` | `00D3B130` | Phyre::PRendering::PShaderParameterCaptureBufferStream |
| 005DD410 | `005DD410` `lea` | `00D3A4A0` | Phyre::PRendering::PShaderParameterCaptureBufferStructuredBuffer |
| 005DD420 | `005DD420` `lea` | `00D3F2A8` | Phyre::PRendering::PShaderParameterCaptureBufferTexture2D |
| 005DD430 | `005DD430` `lea` | `00D40C18` | Phyre::PRendering::PShaderParameterCaptureBufferTexture3D |
| 005DD440 | `005DD440` `lea` | `00D3C9C8` | Phyre::PRendering::PShaderParameterCaptureBufferTextureBase |
| 005DD450 | `005DD450` `lea` | `00D41C40` | Phyre::PRendering::PShaderParameterCaptureBufferTextureCubeMap |
| 005DD460 | `005DD460` `lea` | `00D3FAA0` | Phyre::PRendering::PShaderParameterCaptureConstantBuffer |
| 005DD470 | `005DD470` `lea` | `00D38168` | Phyre::PRendering::PShaderParameterDefinition |
| 005DD480 | `005DD480` `lea` | `00D3AE30` | Phyre::PRendering::PShaderPass |
| 005DD490 | `005DD490` `lea` | `00D40100` | Phyre::PRendering::PShaderPassBase |
| 005DD4A0 | `005DD4A0` `lea` | `00D42A30` | Phyre::PRendering::PShaderPassInfo |
| 005DD4B0 | `005DD4B0` `lea` | `00D39A40` | Phyre::PRendering::PShaderPassParameterLocationTypes |
| 005DD4C0 | `005DD4C0` `lea` | `00D36920` | Phyre::PRendering::PShaderPassParameterLocationTypesBase |
| 005DD4D0 | `005DD4D0` `lea` | `00D3C060` | Phyre::PRendering::PShaderPassParameterLocationTypesConstantBuffer |
| 005DD4E0 | `005DD4E0` `lea` | `00D3D150` | Phyre::PRendering::PShaderPassStateBase |
| 005DD4F0 | `005DD4F0` `lea` | `00D3C720` | Phyre::PRendering::PShaderProgramBase |
| 005DD500 | `005DD500` `lea` | `00D3AF40` | Phyre::PRendering::PShaderProgramParamsAndStreams |
| 005DD510 | `005DD510` `lea` | `00D36CE8` | Phyre::PRendering::PShaderSource |
| 005DD520 | `005DD520` `lea` | `00D39E80` | Phyre::PRendering::PShaderStreamDefinition |
| 005DD530 | `005DD530` `lea` | `00D3D270` | Phyre::PRendering::PShaderVertexProgram |
| 005DD540 | `005DD540` `lea` | `00D3E130` | Phyre::PRendering::PShadowRenderer |
| 005DD550 | `005DD550` `lea` | `00D3DDA0` | Phyre::PRendering::PStructuredBuffer |
| 005DD560 | `005DD560` `lea` | `00D38D90` | Phyre::PRendering::PStructuredBufferBase |
| 005DD570 | `005DD570` `lea` | `00D3D588` | Phyre::PRendering::PTexture2D |
| 005DD580 | `005DD580` `lea` | `00D374E0` | Phyre::PRendering::PTexture2DBase |
| 005DD590 | `005DD590` `lea` | `00D38B38` | Phyre::PRendering::PTexture3D |
| 005DD5A0 | `005DD5A0` `lea` | `00D3FFF0` | Phyre::PRendering::PTexture3DBase |
| 005DD5B0 | `005DD5B0` `lea` | `00D42000` | Phyre::PRendering::PTextureCommonBase |
| 005DD5C0 | `005DD5C0` `lea` | `00D40E98` | Phyre::PRendering::PTextureCubeMap |
| 005DD5D0 | `005DD5D0` `lea` | `00D3AD08` | Phyre::PRendering::PTextureCubeMapBase |
| 006162F0 | `006162F0` `lea` | `00D55658` | decorated `V?$PArray@E$00@Phyre@@` |
| 00616300 | `00616300` `lea` | `00D55850` | decorated `V?$PArray@VPStreamInputDescD3D11@PRendering@Phyre@@$07@Phyre@@` |
| 00616310 | `00616310` `lea` | `00D50EB8` | Phyre::PRendering::PConstantBufferD3D11 |
| 00616320 | `00616320` `lea` | `00D52248` | Phyre::PRendering::PIndirectArgsBufferD3D11 |
| 00616330 | `00616330` `lea` | `00D51400` | Phyre::PRendering::PRenderTargetD3D11 |
| 00616340 | `00616340` `lea` | `00D52660` | Phyre::PRendering::PSamplerStateD3D11 |
| 00616350 | `00616350` `lea` | `00D512D8` | Phyre::PRendering::PShaderComputeProgramD3D11 |
| 00616360 | `00616360` `lea` | `00D50A90` | Phyre::PRendering::PShaderFragmentProgramD3D11 |
| 00616370 | `00616370` `lea` | `00D50FE8` | Phyre::PRendering::PShaderGeometryProgramD3D11 |
| 00616380 | `00616380` `lea` | `00D50BF8` | Phyre::PRendering::PShaderPassD3D11 |
| 00616390 | `00616390` `lea` | `00D502D8` | Phyre::PRendering::PShaderPassStateD3D11 |
| 006163A0 | `006163A0` `lea` | `00D525D8` | Phyre::PRendering::PShaderProgramD3D11 |
| 006163B0 | `006163B0` `lea` | `00D50360` | Phyre::PRendering::PShaderVertexProgramD3D11 |
| 006163C0 | `006163C0` `lea` | `00D519B8` | Phyre::PRendering::PStreamInputDescD3D11 |
| 006163D0 | `006163D0` `lea` | `00D52018` | Phyre::PRendering::PStreamInputLayoutD3D11 |
| 006163E0 | `006163E0` `lea` | `00D51598` | Phyre::PRendering::PStructuredBufferD3D11 |
| 006163F0 | `006163F0` `lea` | `00D51238` | Phyre::PRendering::PTexture2DD3D11 |
| 00616400 | `00616400` `lea` | `00D50250` | Phyre::PRendering::PTexture3DD3D11 |
| 00616410 | `00616410` `lea` | `00D51CB0` | Phyre::PRendering::PTextureCubeMapD3D11 |
| 006462C0 | `006462C0` `lea` | `00D63568` | decorated `V?$PArray@PEAVPPostEffectBase@PPostProcessing@Phyre@@$07@Phyre@@` |
| 006462D0 | `006462D0` `lea` | `00D5AB98` | Phyre::PPostProcessing::PAtmospherics |
| 006462E0 | `006462E0` `lea` | `00D5F218` | Phyre::PPostProcessing::PAtmosphericsBase |
| 006462F0 | `006462F0` `lea` | `00D597C8` | Phyre::PPostProcessing::PAtmosphericsD3D11 |
| 00646300 | `00646300` `lea` | `00D5DAE8` | Phyre::PPostProcessing::PCelShading |
| 00646310 | `00646310` `lea` | `00D5C5A0` | Phyre::PPostProcessing::PCelShadingBase |
| 00646320 | `00646320` `lea` | `00D5D080` | Phyre::PPostProcessing::PCelShadingD3D11 |
| 00646330 | `00646330` `lea` | `00D5CEF8` | Phyre::PPostProcessing::PDeferredLighting |
| 00646340 | `00646340` `lea` | `00D5A1C8` | Phyre::PPostProcessing::PDeferredLightingBase |
| 00646350 | `00646350` `lea` | `00D5BF38` | Phyre::PPostProcessing::PDeferredLightingD3D11 |
| 00646360 | `00646360` `lea` | `00D596C8` | Phyre::PPostProcessing::PDepthOfField |
| 00646370 | `00646370` `lea` | `00D5D940` | Phyre::PPostProcessing::PDepthOfFieldBase |
| 00646380 | `00646380` `lea` | `00D5EC00` | Phyre::PPostProcessing::PDepthOfFieldD3D11 |
| 00646390 | `00646390` `lea` | `00D5EE50` | Phyre::PPostProcessing::PFXAA |
| 006463A0 | `006463A0` `lea` | `00D5D798` | Phyre::PPostProcessing::PFXAABase |
| 006463B0 | `006463B0` `lea` | `00D5E338` | Phyre::PPostProcessing::PFXAAD3D11 |
| 006463C0 | `006463C0` `lea` | `00D5CD68` | Phyre::PPostProcessing::PGlow |
| 006463D0 | `006463D0` `lea` | `00D5A5A0` | Phyre::PPostProcessing::PGlowBase |
| 006463E0 | `006463E0` `lea` | `00D5BFC0` | Phyre::PPostProcessing::PGlowD3D11 |
| 006463F0 | `006463F0` `lea` | `00D5B4C0` | Phyre::PPostProcessing::PGlowGPUBase |
| 00646400 | `00646400` `lea` | `00D5B7F8` | Phyre::PPostProcessing::PLowResParticles |
| 00646410 | `00646410` `lea` | `00D5B908` | Phyre::PPostProcessing::PMLAA |
| 00646420 | `00646420` `lea` | `00D59C70` | Phyre::PPostProcessing::PMLAABase |
| 00646430 | `00646430` `lea` | `00D5AC20` | Phyre::PPostProcessing::PMLAAD3D11 |
| 00646440 | `00646440` `lea` | `00D5C518` | Phyre::PPostProcessing::PMaterialPostEffect |
| 00646450 | `00646450` `lea` | `00D5E2B0` | Phyre::PPostProcessing::PMeshParticleSystemBase |
| 00646460 | `00646460` `lea` | `00D5AE28` | Phyre::PPostProcessing::PMotionBlur |
| 00646470 | `00646470` `lea` | `00D5F000` | Phyre::PPostProcessing::PMotionBlurBase |
| 00646480 | `00646480` `lea` | `00D59AF0` | Phyre::PPostProcessing::PMotionBlurD3D11 |
| 00646490 | `00646490` `lea` | `00D5E5C8` | Phyre::PPostProcessing::PPostEffectBase |
| 006464A0 | `006464A0` `lea` | `00D5D9D8` | Phyre::PPostProcessing::PPostEffectManager |
| 006464B0 | `006464B0` `lea` | `00D5D2C0` | Phyre::PPostProcessing::PScreenSpaceAmbientOcclusion |
| 006464C0 | `006464C0` `lea` | `00D5BB10` | Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionBase |
| 006464D0 | `006464D0` `lea` | `00D5C6C8` | Phyre::PPostProcessing::PScreenSpaceAmbientOcclusionD3D11 |
| 006464E0 | `006464E0` `lea` | `00D5B6E0` | Phyre::PPostProcessing::PScreenSpaceReflection |
| 006464F0 | `006464F0` `lea` | `00D598E8` | Phyre::PPostProcessing::PScreenSpaceReflectionBase |
| 00646500 | `00646500` `lea` | `00D5A758` | Phyre::PPostProcessing::PScreenSpaceReflectionD3D11 |
| 00662CB0 | `00662CB0` `lea` | `00D697E8` | decorated `V?$PArray@E$03@Phyre@@` |
| 00662CC0 | `00662CC0` `lea` | `00D6A9A0` | decorated `V?$PArray@H$03@Phyre@@` |
| 00662CD0 | `00662CD0` `lea` | `00D6A1C0` | decorated `V?$PArray@VPDataBlockD3D11@PGeometry@Phyre@@$07@Phyre@@` |
| 00662CE0 | `00662CE0` `lea` | `00D6AB98` | decorated `V?$PArray@VPDynamicSegmentDesc@PDynamicMesh@PGeometry@Phyre@@$03@Phyre@@` |
| 00662CF0 | `00662CF0` `lea` | `00D6A5B0` | decorated `V?$PArray@VPMeshSegment@PGeometry@Phyre@@$07@Phyre@@` |
| 00662D00 | `00662D00` `lea` | `00D6A7A8` | decorated `V?$PArray@VPSkeletonJointBounds@PGeometry@Phyre@@$03@Phyre@@` |
| 00662D10 | `00662D10` `lea` | `00D69FC8` | decorated `V?$PArray@VPSkinBoneRemap@PGeometry@Phyre@@$01@Phyre@@` |
| 00662D20 | `00662D20` `lea` | `00D699E0` | decorated `V?$PArray@VPVertexStream@PGeometry@Phyre@@$07@Phyre@@` |
| 00662D30 | `00662D30` `lea` | `00D6A3B8` | decorated `V?$PSharray@PEAVPMaterial@PRendering@Phyre@@@Phyre@@` |
| 00662D40 | `00662D40` `lea` | `00D69BD8` | decorated `V?$PSharray@VPDataBlockBufferD3D11@PGeometry@Phyre@@@Phyre@@` |
| 00662D50 | `00662D50` `lea` | `00D69DD0` | decorated `V?$PSharray@VPIndexDataBlockBufferD3D11@PGeometry@Phyre@@@Phyre@@` |
| 00662D60 | `00662D60` `lea` | `00D66578` | Phyre::PGeometry::PDataBlock |
| 00662D70 | `00662D70` `lea` | `00D65D78` | Phyre::PGeometry::PDataBlockBase |
| 00662D80 | `00662D80` `lea` | `00D64E48` | Phyre::PGeometry::PDataBlockBufferD3D11 |
| 00662D90 | `00662D90` `lea` | `00D657F0` | Phyre::PGeometry::PDataBlockD3D11 |
| 00662DA0 | `00662DA0` `lea` | `00D63978` | Phyre::PGeometry::PDynamicDataBlock |
| 00662DB0 | `00662DB0` `lea` | `00D65520` | Phyre::PGeometry::PDynamicMesh |
| 00662DC0 | `00662DC0` `lea` | `00D65888` | Phyre::PGeometry::PDynamicMesh::PDynamicSegmentDesc |
| 00662DD0 | `00662DD0` `lea` | `00D66058` | Phyre::PGeometry::PIndexDataBlock |
| 00662DE0 | `00662DE0` `lea` | `00D643C0` | Phyre::PGeometry::PIndexDataBlockBase |
| 00662DF0 | `00662DF0` `lea` | `00D64AC0` | Phyre::PGeometry::PIndexDataBlockBufferD3D11 |
| 00662E00 | `00662E00` `lea` | `00D655A8` | Phyre::PGeometry::PIndexDataBlockD3D11 |
| 00662E10 | `00662E10` `lea` | `00D65998` | Phyre::PGeometry::PMaterialSet |
| 00662E20 | `00662E20` `lea` | `00D646A0` | Phyre::PGeometry::PMesh |
| 00662E30 | `00662E30` `lea` | `00D652D8` | Phyre::PGeometry::PMeshSegment |
| 00662E40 | `00662E40` `lea` | `00D63F88` | Phyre::PGeometry::PMeshSegmentBase |
| 00662E50 | `00662E50` `lea` | `00D64A38` | Phyre::PGeometry::PMeshSegmentD3D11 |
| 00662E60 | `00662E60` `lea` | `00D663C8` | Phyre::PGeometry::PShape |
| 00662E70 | `00662E70` `lea` | `00D65EF0` | Phyre::PGeometry::PSkeletonJointBounds |
| 00662E80 | `00662E80` `lea` | `00D66970` | Phyre::PGeometry::PSkinBoneRemap |
| 00662E90 | `00662E90` `lea` | `00D650D8` | Phyre::PGeometry::PVertexStream |
| 00675420 | `00675420` `lea` | `00D6BA78` | Phyre::PAssetReference |
| 00675430 | `00675430` `lea` | `00D6BC90` | Phyre::PAssetReferenceImport |
| 006784C0 | `006784C0` `lea` | `00D6C618` | Phyre::PCamera |
| 006784D0 | `006784D0` `lea` | `00D6C888` | Phyre::PCameraProjection |
| 0067CBF0 | `0067CBF0` `lea` | `00D6DA60` | decorated `V?$PArray@VPBitmapFontCharInfo@PText@Phyre@@$03@Phyre@@` |
| 0067CC00 | `0067CC00` `lea` | `00D6D2D0` | Phyre::PText::PBitmapFont |
| 0067CC10 | `0067CC10` `lea` | `00D6D5B8` | Phyre::PText::PBitmapFontCharInfo |
| 0067E680 | `0067E680` `lea` | `00D6DD68` | Phyre::PWorldMatrix |
| 006816D0 | `006816D0` `lea` | `00D6EC98` | Phyre::PScripting::PAsyncProcessHeader |
| 006816E0 | `006816E0` `lea` | `00D6EAE8` | Phyre::PScripting::PClassCallableMethodScript |
| 006816F0 | `006816F0` `lea` | `00D6F120` | Phyre::PScripting::PScheduler |
| 00681700 | `00681700` `lea` | `00D6F2B8` | Phyre::PScripting::PScript |
| 00681710 | `00681710` `lea` | `00D6F090` | Phyre::PScripting::PScriptCallbackHandler |
| 006917D0 | `006917D0` `lea` | `00D7AB98` | decorated `V?$PSharray@PEAVPPhysicsShape@PPhysics@Phyre@@@Phyre@@` |
| 006917E0 | `006917E0` `lea` | `00D757B8` | Phyre::PPhysics::PPhysicsBox |
| 006917F0 | `006917F0` `lea` | `00D746A0` | Phyre::PPhysics::PPhysicsBoxBase |
| 00691800 | `00691800` `lea` | `00D74FA8` | Phyre::PPhysics::PPhysicsBoxBullet |
| 00691810 | `00691810` `lea` | `00D749C0` | Phyre::PPhysics::PPhysicsCallbackData |
| 00691820 | `00691820` `lea` | `00D75930` | Phyre::PPhysics::PPhysicsCapsule |
| 00691830 | `00691830` `lea` | `00D74728` | Phyre::PPhysics::PPhysicsCapsuleBase |
| 00691840 | `00691840` `lea` | `00D75030` | Phyre::PPhysics::PPhysicsCapsuleBullet |
| 00691850 | `00691850` `lea` | `00D74B58` | Phyre::PPhysics::PPhysicsCharacterCamera |
| 00691860 | `00691860` `lea` | `00D71600` | Phyre::PPhysics::PPhysicsCharacterController |
| 00691870 | `00691870` `lea` | `00D75F50` | Phyre::PPhysics::PPhysicsCharacterControllerBase |
| 00691880 | `00691880` `lea` | `00D70770` | Phyre::PPhysics::PPhysicsCharacterControllerBullet |
| 00691890 | `00691890` `lea` | `00D73F58` | Phyre::PPhysics::PPhysicsCylinder |
| 006918A0 | `006918A0` `lea` | `00D72960` | Phyre::PPhysics::PPhysicsCylinderBase |
| 006918B0 | `006918B0` `lea` | `00D73518` | Phyre::PPhysics::PPhysicsCylinderBullet |
| 006918C0 | `006918C0` `lea` | `00D73490` | Phyre::PPhysics::PPhysicsInterface |
| 006918D0 | `006918D0` `lea` | `00D71770` | Phyre::PPhysics::PPhysicsInterfaceBase |
| 006918E0 | `006918E0` `lea` | `00D72A50` | Phyre::PPhysics::PPhysicsInterfaceBullet |
| 006918F0 | `006918F0` `lea` | `00D75638` | Phyre::PPhysics::PPhysicsMaterial |
| 00691900 | `00691900` `lea` | `00D71B60` | Phyre::PPhysics::PPhysicsMesh |
| 00691910 | `00691910` `lea` | `00D76470` | Phyre::PPhysics::PPhysicsMeshBase |
| 00691920 | `00691920` `lea` | `00D70F58` | Phyre::PPhysics::PPhysicsMeshBullet |
| 00691930 | `00691930` `lea` | `00D73ED0` | Phyre::PPhysics::PPhysicsModel |
| 00691940 | `00691940` `lea` | `00D735A0` | Phyre::PPhysics::PPhysicsPlane |
| 00691950 | `00691950` `lea` | `00D71C70` | Phyre::PPhysics::PPhysicsPlaneBase |
| 00691960 | `00691960` `lea` | `00D72AD8` | Phyre::PPhysics::PPhysicsPlaneBullet |
| 00691970 | `00691970` `lea` | `00D73290` | Phyre::PPhysics::PPhysicsRigidBody |
| 00691980 | `00691980` `lea` | `00D70958` | Phyre::PPhysics::PPhysicsRigidBodyBase |
| 00691990 | `00691990` `lea` | `00D72408` | Phyre::PPhysics::PPhysicsRigidBodyBullet |
| 006919A0 | `006919A0` `lea` | `00D71A00` | Phyre::PPhysics::PPhysicsShape |
| 006919B0 | `006919B0` `lea` | `00D765F8` | Phyre::PPhysics::PPhysicsShapeBase |
| 006919C0 | `006919C0` `lea` | `00D70CD8` | Phyre::PPhysics::PPhysicsShapeBullet |
| 006919D0 | `006919D0` `lea` | `00D73DD8` | Phyre::PPhysics::PPhysicsSphere |
| 006919E0 | `006919E0` `lea` | `00D72850` | Phyre::PPhysics::PPhysicsSphereBase |
| 006919F0 | `006919F0` `lea` | `00D73408` | Phyre::PPhysics::PPhysicsSphereBullet |
| 00691A00 | `00691A00` `lea` | `00D71068` | Phyre::PPhysics::PPhysicsTaperedCapsule |
| 00691A10 | `00691A10` `lea` | `00D76570` | Phyre::PPhysics::PPhysicsTaperedCylinder |
| 00691A20 | `00691A20` `lea` | `00D70860` | Phyre::PPhysics::PPhysicsWorld |
| 00691A30 | `00691A30` `lea` | `00D731C8` | Phyre::PPhysics::PPhysicsWorldBase |
| 00691A40 | `00691A40` `lea` | `00D756C0` | Phyre::PPhysics::PPhysicsWorldBullet |
| 00691A50 | `00691A50` `lea` | `00D72380` | Phyre::PPhysics::PRaycastResult |
| 006A7240 | `006A7240` `lea` | `00D7B300` | Phyre::PString |
| 006A7C50 | `006A7C50` `lea` | `00D7BD38` | decorated `V?$PSharray@PEAVPTriggerReceiverComponent@PGameplay@Phyre@@@Phyre@@` |
| 006A7C60 | `006A7C60` `lea` | `00D7B7B8` | Phyre::PGameplay::PTrigger |
| 006A9830 | `006A9830` `lea` | `00D7C198` | Phyre::PGameplay::PQuarryComponent |
| 006A9F00 | `006A9F00` `lea` | `00D7C500` | Phyre::PTypedObject |
| 006AAA40 | `006AAA40` `lea` | `00D7C930` | Phyre::PComponent |
| 006AB730 | `006AB730` `lea` | `00D7CDB8` | Phyre::PEntity |
| 006AD090 | `006AD090` `lea` | `00D7D420` | Phyre::PCameraOrthographic |
| 006AD900 | `006AD900` `lea` | `00D7D800` | Phyre::PCameraPerspective |
| 006ADF70 | `006ADF70` `lea` | `00D7E118` | decorated `V?$PArray@VPTypedObject@Phyre@@$07@Phyre@@` |
| 006ADF80 | `006ADF80` `lea` | `00D7DB40` | Phyre::PInstancesComponent |
| 006AFC10 | `006AFC10` `lea` | `00D7E598` | Phyre::PNameComponent |
| 006B04A0 | `006B04A0` `lea` | `00D7E968` | Phyre::PRandom::PRandomGenerator |
| 006B3FF0 | `006B3FF0` `lea` | `00D80048` | Phyre::PScene::PNode |
| 006B85E0 | `006B85E0` `lea` | `00D80AE0` | Phyre::PRendering::PMeshSegmentContext |
| 006BBC20 | `006BBC20` `lea` | `00D82008` | decorated `V?$PArray@PEBE$07@Phyre@@` |
| 006BBC30 | `006BBC30` `lea` | `00D823F8` | decorated `V?$PArray@VPModifierNetworkDynamicMeshSegment@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006BBC40 | `006BBC40` `lea` | `00D82200` | decorated `V?$PArray@VPRenderStream@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006BBC50 | `006BBC50` `lea` | `00D817A0` | Phyre::PDynamicGeometry::PModifierNetworkDynamicMesh |
| 006BBC60 | `006BBC60` `lea` | `00D81420` | Phyre::PDynamicGeometry::PModifierNetworkDynamicMeshSegment |
| 006BEC30 | `006BEC30` `lea` | `00D82A48` | Phyre::PRendering::PLight |
| 006C0FB0 | `006C0FB0` `lea` | `00D83C98` | decorated `V?$PArray@VPShadowSplit@PShadowCaster@PRendering@Phyre@@$07@Phyre@@` |
| 006C0FC0 | `006C0FC0` `lea` | `00D83240` | Phyre::PRendering::PShadowCaster |
| 006C0FD0 | `006C0FD0` `lea` | `00D833E8` | Phyre::PRendering::PShadowCaster::PShadowSplit |
| 006C3040 | `006C3040` `lea` | `00D84E58` | decorated `V?$PArray@PEBVPBase@Phyre@@$07@Phyre@@` |
| 006C3050 | `006C3050` `lea` | `00D84568` | Phyre::PDynamicGeometry::PModifierNetworkInstance |
| 006C3060 | `006C3060` `lea` | `00D841F0` | Phyre::PDynamicGeometry::PModifierNetworkInstanceInput |
| 006C3070 | `006C3070` `lea` | `00D843B0` | Phyre::PDynamicGeometry::PModifierNetworkInstancePacketInput |
| 006C5290 | `006C5290` `lea` | `00D86198` | decorated `V?$PArray@VPLODLevel@PLOD@Phyre@@$07@Phyre@@` |
| 006C52A0 | `006C52A0` `lea` | `00D85FA0` | decorated `V?$PSharray@PEAVPMeshInstance@PRendering@Phyre@@@Phyre@@` |
| 006C52B0 | `006C52B0` `lea` | `00D85408` | Phyre::PLOD::PLODGroup |
| 006C52C0 | `006C52C0` `lea` | `00D851A0` | Phyre::PLOD::PLODLevel |
| 006C8300 | `006C8300` `lea` | `00D865F8` | Phyre::POccluderGeometry::POccluderGeometryInstance |
| 006CCFF0 | `006CCFF0` `lea` | `00D89D20` | Phyre::PGameplay::PScriptableComponent |
| 006CD950 | `006CD950` `lea` | `00D89FC8` | Phyre::PGameplay::PTriggerReceiverTypeCallbackData |
| 006CE090 | `006CE090` `lea` | `00D8A398` | Phyre::PGameplay::PTriggerReceiverComponent |
| 006D01D0 | `006D01D0` `lea` | `00D8CF88` | decorated `V?$PArray@VPModifierAndInputs@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006D01E0 | `006D01E0` `lea` | `00D8D180` | decorated `V?$PArray@VPModifierNetworkBuffer@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006D01F0 | `006D01F0` `lea` | `00D8CD90` | decorated `V?$PArray@VPRenderStreamInput@PDynamicGeometry@Phyre@@$03@Phyre@@` |
| 006D0200 | `006D0200` `lea` | `00D8B3B0` | Phyre::PDynamicGeometry::PModifierAndInputs |
| 006D0210 | `006D0210` `lea` | `00D8BD08` | Phyre::PDynamicGeometry::PModifierNetwork |
| 006D0220 | `006D0220` `lea` | `00D8B200` | Phyre::PDynamicGeometry::PModifierNetworkBuffer |
| 006D0230 | `006D0230` `lea` | `00D8AE20` | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket |
| 006D0240 | `006D0240` `lea` | `00D8AB40` | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_Buffer |
| 006D0250 | `006D0250` `lea` | `00D8B948` | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode |
| 006D0260 | `006D0260` `lea` | `00D8BE08` | Phyre::PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance |
| 006D0270 | `006D0270` `lea` | `00D8AFC8` | Phyre::PDynamicGeometry::PRenderStream |
| 006D0280 | `006D0280` `lea` | `00D8ACF0` | Phyre::PDynamicGeometry::PRenderStreamInput |
| 006D8EE0 | `006D8EE0` `lea` | `00D8D850` | Phyre::PDynamicGeometry::PMorphModifierWeightsUserDataObject |
| 006D9FB0 | `006D9FB0` `lea` | `00D8DE98` | Phyre::POccluderGeometry::POccluderGeometryObject |
| 007930A0 | `007930A0` `lea` | `01CB0D98` | Phyre::PFramework::PApplication |
| 007930B0 | `007930B0` `lea` | `01CB0EC0` | Phyre::PFramework::PApplicationViewport |
| 007930C0 | `007930C0` `lea` | `01CB0A50` | Phyre::PFramework::PDebugUtils |
| 007930D0 | `007930D0` `lea` | `01CB1068` | Phyre::PFramework::PInputMapper |
| 0086C650 | `0086C650` `lea` | `01CD69D8` | decorated `V?$PArray@PEAVPInputAction@PInputs@Phyre@@$07@Phyre@@` |
| 0086C660 | `0086C660` `lea` | `01CD67E0` | decorated `V?$PArray@PEAVPInputSource@PInputs@Phyre@@$07@Phyre@@` |
| 0086C670 | `0086C670` `lea` | `01CD0DD0` | Phyre::PInputs::PInputAction |
| 0086C680 | `0086C680` `lea` | `01CD1E48` | Phyre::PInputs::PInputMap |
| 0086C690 | `0086C690` `lea` | `01CD0ED8` | Phyre::PInputs::PInputSource |
| 0086C6A0 | `0086C6A0` `lea` | `01CD2AA0` | Phyre::PInputs::PInputSourceJoypadAxis |
| 0086C6B0 | `0086C6B0` `lea` | `01CD1F80` | Phyre::PInputs::PInputSourceJoypadButton |
| 0086C6C0 | `0086C6C0` `lea` | `01CD16C0` | Phyre::PInputs::PInputSourceKey |
| 0086C6D0 | `0086C6D0` `lea` | `01CD09F8` | Phyre::PInputs::PInputSourceMotionAngularVelocityX |
| 0086C6E0 | `0086C6E0` `lea` | `01CD0F60` | Phyre::PInputs::PInputSourceMotionAngularVelocityY |
| 0086C6F0 | `0086C6F0` `lea` | `01CD17E8` | Phyre::PInputs::PInputSourceMotionAngularVelocityZ |
| 0086C700 | `0086C700` `lea` | `01CD2108` | Phyre::PInputs::PInputSourceMotionLinearAccelerationX |
| 0086C710 | `0086C710` `lea` | `01CD2BA8` | Phyre::PInputs::PInputSourceMotionLinearAccelerationY |
| 0086C720 | `0086C720` `lea` | `01CD3678` | Phyre::PInputs::PInputSourceMotionLinearAccelerationZ |
| 0086C730 | `0086C730` `lea` | `01CD0578` | Phyre::PInputs::PInputSourceMotionQuatW |
| 0086C740 | `0086C740` `lea` | `01CD3700` | Phyre::PInputs::PInputSourceMotionQuatX |
| 0086C750 | `0086C750` `lea` | `01CD3FA0` | Phyre::PInputs::PInputSourceMotionQuatY |
| 0086C760 | `0086C760` `lea` | `01CCFE28` | Phyre::PInputs::PInputSourceMotionQuatZ |
| 0086C770 | `0086C770` `lea` | `01CD3578` | Phyre::PInputs::PInputSourceMouseButton |
| 0086C780 | `0086C780` `lea` | `01CD3EA0` | Phyre::PInputs::PInputSourceMouseDeltaX |
| 0086C790 | `0086C790` `lea` | `01CCFF28` | Phyre::PInputs::PInputSourceMouseDeltaY |
| 0086C7A0 | `0086C7A0` `lea` | `01CD2278` | Phyre::PInputs::PInputSourceTouchDragX |
| 0086C7B0 | `0086C7B0` `lea` | `01CD2CA8` | Phyre::PInputs::PInputSourceTouchDragY |
| 0086C7C0 | `0086C7C0` `lea` | `01CD0A80` | Phyre::PInputs::PInputSourceTouchPinch |
| 0086C7D0 | `0086C7D0` `lea` | `01CD0600` | Phyre::PInputs::PInputSourceTouchRotate |
| 0086C7E0 | `0086C7E0` `lea` | `01CD10E8` | Phyre::PInputs::PInputSourceTouchTwoFingerDragX |
| 0086C7F0 | `0086C7F0` `lea` | `01CD18F8` | Phyre::PInputs::PInputSourceTouchTwoFingerDragY |
| 0086C800 | `0086C800` `lea` | `01CD3E18` | Phyre::PInputs::PInputSourceVisionTrackerX |
| 0086C810 | `0086C810` `lea` | `01CD45E8` | Phyre::PInputs::PInputSourceVisionTrackerY |
| 0086C820 | `0086C820` `lea` | `01CD04F0` | Phyre::PInputs::PInputSourceVisionTrackerZ |
| 00874D70 | `00874D70` `lea` | `01CD73C0` | Phyre::PVision::PVisionMoveTracker |
| 00874D80 | `00874D80` `lea` | `01CD7018` | Phyre::PVision::PVisionMoveTrackerBase |
| 00874D90 | `00874D90` `lea` | `01CD71B0` | Phyre::PVision::PVisionMoveTrackerWin32 |
| 00875950 | `00875950` `lea` | `01CD75D8` | Phyre::PVision::PVisionTracker |
| 00875960 | `00875960` `lea` | `01CD77F8` | Phyre::PVision::PVisionTrackerBase |
| 00875970 | `00875970` `lea` | `01CD7920` | Phyre::PVision::PVisionTrackerWin32 |
| 00878030 | `00878030` `lea` | `01CD9190` | Phyre::PHierarchy::POctree |
| 00878040 | `00878040` `lea` | `01CD9338` | Phyre::PHierarchy::POctreeChildren |
| 00878050 | `00878050` `lea` | `01CD8FF0` | Phyre::PHierarchy::POctreeData |
| 00878060 | `00878060` `lea` | `01CD8CA0` | Phyre::PHierarchy::POctreeWorld |
| 00879AE0 | `00879AE0` `lea` | `01CD9E90` | decorated `V?$PArray@PEAVPInputMap@PInputs@Phyre@@$07@Phyre@@` |
| 00879AF0 | `00879AF0` `lea` | `01CD9A68` | Phyre::PGame::PGameConfig |

## Per-member rows: the class name and size each base-aware descriptor constructor registers (OPUS, 2026-10-03)

The family `AbstractClassDescriptor base-aware constructors` (frontmatter: 132 members; 132 get a row here) shares one form, not repeated per row. It calls the two context getters, passes them to the shared descriptor constructor `00632D80` with the class name in `r8`, the instance size in `r9d` and two dword stack arguments, stores its own `PClassDescriptorAbstract<T>` vtable, sets bit `0x2` of dword `+0xFC`, and calls the three member-registration helpers `0063DC80`, `0063DF90` and `0063DFA0`, each with its own `lea rdx` argument. What differs from member to member is the name and size it passes, the two stack dwords (at + 0x2B and + 0x38), the vtable it stores (+ 0x56), and the three `lea rdx` arguments (+ 0x67, + 0x76 and + 0x85). The rows anchor the name `lea`; they do not state the others. Each row anchors the `lea r8, [S]` before the `00632D80` call (the member's distinguishing instruction) and states S, the class-name string at S, and the immediate size from `mov r9d`. All are read from the certified image. [`fam_rows.py`](../../_index/candidates/opus-ee-base-aware-ctors-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-base-aware-ctors-1003/rows.tsv). A body without exactly one `00632D80` call, a name that is not a clean string, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-base-aware-ctors-1003/excluded.tsv).

### All 132 constructors (OPUS)

| member | distinguishing instruction | name string S | class name and instance size passed |
|---|---|---|---|
| 00597730 | `00597776` `lea` | `00D244A8` | "PClusterHeaderBase", size 0x48 |
| 00597880 | `005978C6` `lea` | `00D24A28` | "PInstanceListHeader", size 0x24 |
| 005A81F0 | `005A8236` `lea` | `00D2D060` | "PAnimationChannelTarget", size 0x38 |
| 005A82A0 | `005A82E6` `lea` | `00D2C3A0` | "PAnimationChannelTimes", size 0x18 |
| 005A8350 | `005A8396` `lea` | `00D287C0` | "PAnimationClip", size 0x38 |
| 005A8400 | `005A8446` `lea` | `00D2B0E0` | "PAnimationClipBinding", size 0x8 |
| 005A84B0 | `005A84F6` `lea` | `00D2B908` | "PAnimationClipBindingChannelMap", size 0x4 |
| 005A8560 | `005A85A6` `lea` | `00D2C060` | "PAnimationClipBindingDataBlockCache", size 0x18 |
| 005A87F0 | `005A8836` `lea` | `00D29BC8` | "PAnimationDataSourceListEntry", size 0x98 |
| 005A88A0 | `005A88E6` `lea` | `00D2B180` | "PAnimationEvent", size 0x8 |
| 005A89F0 | `005A8A36` `lea` | `00D2C1C8` | "PAnimationEventList", size 0x10 |
| 005A8AA0 | `005A8AE6` `lea` | `00D2CC98` | "PAnimationHierarchyNode", size 0x10 |
| 005A8B50 | `005A8B96` `lea` | `00D2CB80` | "PAnimationNetworkInstance", size 0x78 |
| 005A8C00 | `005A8C46` `lea` | `00D2A770` | "PAnimationNetworkInstanceTarget", size 0x30 |
| 005A8CB0 | `005A8CF6` `lea` | `00D2AA00` | "PAnimationSet", size 0x30 |
| 005A8D60 | `005A8DA6` `lea` | `00D2B7E8` | "PAnimationSlotArray", size 0x8 |
| 005A8EB0 | `005A8EF6` `lea` | `00D288B0` | "PAnimationSlotFilterDeferredLoad", size 0x10 |
| 005A8F60 | `005A8FA6` `lea` | `00D2AFC8` | "PAnimationSlotListIndex", size 0x18 |
| 005A91F0 | `005A9236` `lea` | `00D282D8` | "PBlendableAnimationSource", size 0x80 |
| 005D8FC0 | `005D9006` `lea` | `00D36370` | "PConstantBufferBase", size 0xC |
| 005D9070 | `005D90B6` `lea` | `00D368F8` | "PContextVariantFoldingTable", size 0x14 |
| 005D9120 | `005D9166` `lea` | `00D40F18` | "PDynamicMeshInstance", size 0x18 |
| 005D91D0 | `005D9216` `lea` | `00D3E8A8` | "PEffect", size 0x78 |
| 005D9280 | `005D92C6` `lea` | `00D37B18` | "PEffectVariant", size 0x68 |
| 005D9470 | `005D94B6` `lea` | `00D3F5D0` | "PIndirectArgsBufferBase", size 0x8 |
| 005D9520 | `005D9566` `lea` | `00D3E448` | "PMaterial", size 0x28 |
| 005D95D0 | `005D9616` `lea` | `00D3C510` | "PMaterialSwitch", size 0x10 |
| 005D9680 | `005D96C6` `lea` | `00D3E810` | "PMeshInstance", size 0xC8 |
| 005D9730 | `005D9776` `lea` | `00D42E30` | "PMeshInstanceAttachPoint", size 0x18 |
| 005D97E0 | `005D9826` `lea` | `00D3AD88` | "PMeshInstanceBounds", size 0x30 |
| 005D9930 | `005D9976` `lea` | `00D41970` | "PMeshInstanceSegmentStreamBinding", size 0x18 |
| 005D9A80 | `005D9AC6` `lea` | `00D3A080` | "PNodeContext", size 0x10 |
| 005D9BD0 | `005D9C16` `lea` | `00D38F88` | "PParameterBufferBase", size 0x4 |
| 005D9D20 | `005D9D66` `lea` | `00D389F8` | "PRenderTargetBase", size 0x10 |
| 005D9E70 | `005D9EB6` `lea` | `00D3FD40` | "PSamplerStateBase", size 0x20 |
| 005D9F20 | `005D9F66` `lea` | `00D3BEB0` | "PSceneRenderPass", size 0x50 |
| 005DA070 | `005DA0B6` `lea` | `00D3D2F0` | "PShader", size 0x40 |
| 005DA4E0 | `005DA526` `lea` | `00D3DAA8` | "PShaderParameterCaptureBufferLocation", size 0x2 |
| 005DAA90 | `005DAAD6` `lea` | `00D3ACD8` | "PShaderParameterCaptureBufferStream", size 0x18 |
| 005DAD20 | `005DAD66` `lea` | `00D3C520` | "PShaderParameterCaptureBufferTextureBase", size 0x10 |
| 005DAF10 | `005DAF56` `lea` | `00D37A58` | "PShaderParameterDefinition", size 0x18 |
| 005DB060 | `005DB0A6` `lea` | `00D3FA20` | "PShaderPassBase", size 0x30 |
| 005DB110 | `005DB156` `lea` | `00D424F8` | "PShaderPassInfo", size 0x30 |
| 005DB260 | `005DB2A6` `lea` | `00D36448` | "PShaderPassParameterLocationTypesBase", size 0x10 |
| 005DB3B0 | `005DB3F6` `lea` | `00D3CCE8` | "PShaderPassStateBase", size 0x4 |
| 005DB460 | `005DB4A6` `lea` | `00D3C270` | "PShaderProgramBase", size 0x1 |
| 005DB510 | `005DB556` `lea` | `00D3A9C0` | "PShaderProgramParamsAndStreams", size 0x20 |
| 005DB5C0 | `005DB606` `lea` | `00D367B8` | "PShaderSource", size 0x28 |
| 005DB670 | `005DB6B6` `lea` | `00D39AC0` | "PShaderStreamDefinition", size 0x18 |
| 005DB7C0 | `005DB806` `lea` | `00D3DB80` | "PShadowRenderer", size 0x10 |
| 005DB910 | `005DB956` `lea` | `00D386B8` | "PStructuredBufferBase", size 0x14 |
| 005DBC40 | `005DBC86` `lea` | `00D41B88` | "PTextureCommonBase", size 0x28 |
| 00615170 | `006151B6` `lea` | `00D51920` | "PStreamInputDescD3D11", size 0x20 |
| 00615220 | `00615266` `lea` | `00D51F80` | "PStreamInputLayoutD3D11", size 0x18 |
| 00645000 | `00645046` `lea` | `00D5E3B8` | "PPostEffectBase", size 0x50 |
| 006450B0 | `006450F6` `lea` | `00D5D778` | "PPostEffectManager", size 0x28 |
| 00661BD0 | `00661C16` `lea` | `00D65D00` | "PDataBlockBase", size 0x20 |
| 00661C80 | `00661CC6` `lea` | `00D64BA8` | "PDataBlockBufferD3D11", size 0x48 |
| 00661DD0 | `00661E16` `lea` | `00D66BD0` | "PDynamicDataBlock", size 0x28 |
| 00661E80 | `00661EC6` `lea` | `00D65508` | "PDynamicMesh", size 0x38 |
| 00661F30 | `00661F76` `lea` | `00D65748` | "PDynamicSegmentDesc", size 0x10 |
| 00662080 | `006620C6` `lea` | `00D642C8` | "PIndexDataBlockBase", size 0x14 |
| 00662130 | `00662176` `lea` | `00D64888` | "PIndexDataBlockBufferD3D11", size 0x48 |
| 00662280 | `006622C6` `lea` | `00D65870` | "PMaterialSet", size 0x10 |
| 00662330 | `00662376` `lea` | `00D64598` | "PMesh", size 0x80 |
| 00662480 | `006624C6` `lea` | `00D63E88` | "PMeshSegmentBase", size 0x30 |
| 006625D0 | `00662616` `lea` | `00D66048` | "PShape", size 0x38 |
| 00662680 | `006626C6` `lea` | `00D65E00` | "PSkeletonJointBounds", size 0x20 |
| 00662730 | `00662776` `lea` | `00D66800` | "PSkinBoneRemap", size 0x4 |
| 006627E0 | `00662826` `lea` | `00D64F38` | "PVertexStream", size 0x18 |
| 006751A0 | `006751E6` `lea` | `00D6BA60` | "PAssetReference", size 0x50 |
| 00675250 | `00675296` `lea` | `00D6BC70` | "PAssetReferenceImport", size 0x18 |
| 00678370 | `006783B6` `lea` | `00D6C608` | "PCamera", size 0xC0 |
| 0067CA70 | `0067CAB6` `lea` | `00D6D2B8` | "PBitmapFont", size 0x38 |
| 0067CB20 | `0067CB66` `lea` | `00D6D598` | "PBitmapFontCharInfo", size 0x30 |
| 0067E5D0 | `0067E616` `lea` | `00D6DD50` | "PWorldMatrix", size 0x30 |
| 00681200 | `00681246` `lea` | `00D6EC78` | "PAsyncProcessHeader", size 0x28 |
| 00681350 | `00681396` `lea` | `00D6F078` | "PScheduler", size 0x2F8 |
| 00681400 | `00681446` `lea` | `00D6F110` | "PScript", size 0x58 |
| 006814B0 | `006814F6` `lea` | `00D6F060` | "PScriptCallbackHandler", size 0x18 |
| 0068F430 | `0068F476` `lea` | `00D747A8` | "PPhysicsCallbackData", size 0x28 |
| 0068F6C0 | `0068F706` `lea` | `00D74938` | "PPhysicsCharacterCamera", size 0x208 |
| 0068F810 | `0068F856` `lea` | `00D75B30` | "PPhysicsCharacterControllerBase", size 0x130 |
| 0068FBE0 | `0068FC26` `lea` | `00D715E0` | "PPhysicsInterfaceBase", size 0x18 |
| 0068FD30 | `0068FD76` `lea` | `00D75500` | "PPhysicsMaterial", size 0xC |
| 0068FFC0 | `00690006` `lea` | `00D73D38` | "PPhysicsModel", size 0x18 |
| 006902F0 | `00690336` `lea` | `00D70658` | "PPhysicsRigidBodyBase", size 0x118 |
| 006904E0 | `00690526` `lea` | `00D76368` | "PPhysicsShapeBase", size 0x68 |
| 006909F0 | `00690A36` `lea` | `00D73078` | "PPhysicsWorldBase", size 0x60 |
| 00690B40 | `00690B86` `lea` | `00D72068` | "PRaycastResult", size 0x30 |
| 006A7190 | `006A71D6` `lea` | `00D6FD28` | "PString", size 0x8 |
| 006A7BA0 | `006A7BE6` `lea` | `00D7B7A0` | "PTrigger", size 0x58 |
| 006A9E50 | `006A9E96` `lea` | `00D7C4E8` | "PTypedObject", size 0x10 |
| 006AA970 | `006AA9B6` `lea` | `00D7C918` | "PComponent", size 0x18 |
| 006AB680 | `006AB6C6` `lea` | `00D7CDA8` | "PEntity", size 0x38 |
| 006B03F0 | `006B0436` `lea` | `00D7E948` | "PRandomGenerator", size 0x1 |
| 006B3F40 | `006B3F86` `lea` | `00D80038` | "PNode", size 0x68 |
| 006BBB70 | `006BBBB6` `lea` | `00D81370` | "PModifierNetworkDynamicMeshSegment", size 0x18 |
| 006BEB80 | `006BEBC6` `lea` | `00D82A34` | "PLight", size 0x40 |
| 006C0D50 | `006C0D96` `lea` | `00D837B0` | "PShadowCaster", size 0x80 |
| 006C0E00 | `006C0E46` `lea` | `00D833D0` | "PShadowSplit", size 0xE8 |
| 006C2E40 | `006C2E86` `lea` | `00D84540` | "PModifierNetworkInstance", size 0x28 |
| 006C2F90 | `006C2FD6` `lea` | `00D84380` | "PModifierNetworkInstancePacketInput", size 0x8 |
| 006C4EC0 | `006C4F06` `lea` | `00D853F0` | "PLODGroup", size 0x68 |
| 006C4F70 | `006C4FB6` `lea` | `00D85188` | "PLODLevel", size 0x38 |
| 006C8250 | `006C8296` `lea` | `00D86808` | "POccluderGeometryInstance", size 0x10 |
| 006CD8A0 | `006CD8E6` `lea` | `00D89F98` | "PTriggerReceiverTypeCallbackData", size 0x28 |
| 006CFBA0 | `006CFBE6` `lea` | `00D8B390` | "PModifierAndInputs", size 0x20 |
| 006CFC50 | `006CFC96` `lea` | `00D8BC48` | "PModifierNetwork", size 0x70 |
| 006CFD00 | `006CFD46` `lea` | `00D8B1E0` | "PModifierNetworkBuffer", size 0x18 |
| 006CFDB0 | `006CFDF6` `lea` | `00D8AD70` | "PModifierNetworkInfoPacket", size 0x20 |
| 006CFE60 | `006CFEA6` `lea` | `00D8AA88` | "PModifierNetworkInfoPacket_Buffer", size 0x2 |
| 006CFF10 | `006CFF56` `lea` | `00D8B918` | "PModifierNetworkInfoPacket_ModifierCode", size 0x20 |
| 006CFFC0 | `006D0006` `lea` | `00D8BCD0` | "PModifierNetworkInfoPacket_ModifierInstance", size 0x20 |
| 006D0070 | `006D00B6` `lea` | `00D8AFB0` | "PRenderStream", size 0x10 |
| 006D0120 | `006D0166` `lea` | `00D8ACD0` | "PRenderStreamInput", size 0x8 |
| 006D8E30 | `006D8E76` `lea` | `00D8D818` | "PMorphModifierWeightsUserDataObject", size 0x10 |
| 006D9F00 | `006D9F46` `lea` | `00D8DE78` | "POccluderGeometryObject", size 0x30 |
| 00791AC0 | `00791B06` `lea` | `01CB0D80` | "PApplication", size 0x1130 |
| 00791B70 | `00791BB6` `lea` | `01CB0EA0` | "PApplicationViewport", size 0x38 |
| 00791C20 | `00791C66` `lea` | `01CB09D0` | "PDebugUtils", size 0x58 |
| 00791CD0 | `00791D16` `lea` | `01CB1050` | "PInputMapper", size 0x2C8 |
| 0086B2B0 | `0086B2F6` `lea` | `01CD0D20` | "PInputAction", size 0x28 |
| 0086B360 | `0086B3A6` `lea` | `01CD1C98` | "PInputMap", size 0x18 |
| 0086B410 | `0086B456` `lea` | `01CD0D30` | "PInputSource", size 0x28 |
| 00874C10 | `00874C56` `lea` | `01CD6FF8` | "PVisionMoveTrackerBase", size 0x8 |
| 00875800 | `00875846` `lea` | `01CD77D8` | "PVisionTrackerBase", size 0x8 |
| 00877BE0 | `00877C26` `lea` | `01CD9180` | "POctree", size 0x50 |
| 00877C90 | `00877CD6` `lea` | `01CD9320` | "POctreeChildren", size 0x288 |
| 00877D40 | `00877D86` `lea` | `01CD8FD8` | "POctreeData", size 0x38 |
| 00877DF0 | `00877E36` `lea` | `01CD8C88` | "POctreeWorld", size 0xC8 |
| 00879A30 | `00879A76` `lea` | `01CD9A50` | "PGameConfig", size 0x18 |

## Per-member rows: the class descriptor each of the reflection object traversal adapters loads (OPUS, 2026-10-03)

The family `reflection object traversal adapters` (frontmatter: 304 members; 304 get a row here) shares two forms, stated here once and not repeated per row (the census row above). In 188 members (46 B), `lea rcx, [X]` comes first, then the flag selects one of two calls to the shared traversal `0063E2E0`, with `r8b` set to 1 or 0. In 116 members (75-76 B), the object pointer is offset by a constant member offset (`add rdx, 8`, or `inc rdx` in three members) and null-guarded, and each flag path then does `lea rcx, [X]` and calls `0063E2E0`. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (every load of it in the body names the same X). Each row anchors the first such `lea`, the member's distinguishing instruction, and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-traversal-adapters-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-traversal-adapters-1003/rows.tsv). A member whose loads name more than one X, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-traversal-adapters-1003/excluded.tsv).

### All 304 members (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 005A2B10 | `005A2B2C` `lea` | `02CAF0E0` | PTimeScaleOffsetController |
| 005A2E70 | `005A2E74` `lea` | `02CADC50` | PAnimationConstantChannel |
| 005A32B0 | `005A32B4` `lea` | `02CAE450` | PAnimationNetworkInstanceTarget |
| 005A3440 | `005A3444` `lea` | `02CAE660` | PAnimationSet |
| 005A37A0 | `005A37BC` `lea` | `02CAD340` | PAnimationBlenderController |
| 005A3850 | `005A3854` `lea` | `02CAE760` | PAnimationSlotListIndex |
| 005A39D0 | `005A39D4` `lea` | `02CADB40` | PAnimationClipBinding |
| 005A3A90 | `005A3A94` `lea` | `02CAE050` | PAnimationEvent |
| 005A3F60 | `005A3F7C` `lea` | `02CAEDE0` | PAnimationWeightedBlenderController |
| 005A40E0 | `005A40E4` `lea` | `02CAE860` | PAnimationSlotArray |
| 005A4170 | `005A4174` `lea` | `02CAD940` | PAnimationClipBindingChannelMap |
| 005A4600 | `005A461C` `lea` | `02CADE50` | PAnimationDataSource |
| 005A4780 | `005A4784` `lea` | `02CADA40` | PAnimationClipBindingDataBlockCache |
| 005A4870 | `005A4874` `lea` | `02CAE150` | PAnimationEventList |
| 005A49D0 | `005A49EC` `lea` | `02CAD240` | PAnimationAdditiveBlenderController |
| 005A4AA0 | `005A4AA4` `lea` | `02CAD740` | PAnimationChannelTimes |
| 005A5140 | `005A515C` `lea` | `02CADF50` | PAnimationEventController |
| 005A52E0 | `005A52FC` `lea` | `02CAE550` | PAnimationNetworkInstance |
| 005A54C0 | `005A54DC` `lea` | `02CAE250` | PAnimationHierarchyNode |
| 005A55A0 | `005A55BC` `lea` | `02CAEBE0` | PAnimationSpuTargetBlenderController |
| 005A58F0 | `005A58F4` `lea` | `02CAD640` | PAnimationChannelTarget |
| 005CDE20 | `005CDE24` `lea` | `02CB6380` | PConstantBufferBase |
| 005CDE90 | `005CDEAC` `lea` | `02CB7180` | PModifierNetworkDynamicMeshInstance |
| 005CDFA0 | `005CDFA4` `lea` | `02CB9600` | PShaderPassParameterLocationTypesBase |
| 005CE200 | `005CE204` `lea` | `02CB78A0` | PSamplerState |
| 005CE3F0 | `005CE3F4` `lea` | `02CBAB00` | PShaderSource |
| 005CE480 | `005CE484` `lea` | `02CB7BA0` | PContextVariantFoldingTable |
| 005CE920 | `005CE924` `lea` | `02CBB800` | PTexture2DBase |
| 005CEA70 | `005CEA74` `lea` | `02CBAA00` | PShaderParameterCaptureBufferRWTexture3D |
| 005CEC80 | `005CEC84` `lea` | `02CB6D80` | PMeshInstanceSegmentContext |
| 005CF230 | `005CF234` `lea` | `02CB9500` | PShaderParameterDefinition |
| 005CF260 | `005CF264` `lea` | `02CB6780` | PEffectVariant |
| 005CF7D0 | `005CF7D4` `lea` | `02CBBB00` | PTexture3D |
| 005CF8C0 | `005CF8C4` `lea` | `02CBB500` | PStructuredBufferBase |
| 005CFB30 | `005CFB34` `lea` | `02CB75A0` | PRenderTargetBase |
| 005CFD00 | `005CFD04` `lea` | `02CBA200` | PShaderParameterCaptureBufferSampler |
| 005CFE40 | `005CFE44` `lea` | `02CB7380` | PParameterBufferBase |
| 005D01E0 | `005D01E4` `lea` | `02CB9700` | PShaderPassParameterLocationTypes |
| 005D0570 | `005D0574` `lea` | `02CBAE00` | PShaderStreamDefinition |
| 005D0850 | `005D0854` `lea` | `02CB7280` | PNodeContext |
| 005D0880 | `005D0884` `lea` | `02CBA300` | PShaderParameterCaptureBufferStructuredBuffer |
| 005D0D00 | `005D0D04` `lea` | `02CBBC00` | PTextureCubeMapBase |
| 005D0E30 | `005D0E34` `lea` | `02CB7480` | PParameterBuffer |
| 005D0E60 | `005D0E64` `lea` | `02CB9A00` | PShaderPass |
| 005D0E90 | `005D0E94` `lea` | `02CBAC00` | PShaderProgramParamsAndStreams |
| 005D1140 | `005D1144` `lea` | `02CB9C00` | PShaderParameterCaptureBufferStream |
| 005D1340 | `005D1344` `lea` | `02CB7080` | PMeshInstanceBounds |
| 005D1590 | `005D1594` `lea` | `02CB6480` | PConstantBuffer |
| 005D1840 | `005D1844` `lea` | `02CBA400` | PShaderParameterCaptureBufferRWStructuredBuffer |
| 005D1D00 | `005D1D04` `lea` | `02CB9800` | PShaderPassParameterLocationTypesConstantBuffer |
| 005D20D0 | `005D20D4` `lea` | `02CB79A0` | PSceneRenderPass |
| 005D22B0 | `005D22B4` `lea` | `02CBAD00` | PShaderProgramBase |
| 005D2530 | `005D2534` `lea` | `02CB6A80` | PMaterialSwitch |
| 005D2560 | `005D2564` `lea` | `02CB9D00` | PShaderParameterCaptureBufferTextureBase |
| 005D2920 | `005D2924` `lea` | `02CBA500` | PShaderParameterCaptureBufferByteAddressBuffer |
| 005D2CE0 | `005D2CE4` `lea` | `02CB9B00` | PShaderPassStateBase |
| 005D2E00 | `005D2E04` `lea` | `02CBAF00` | PShaderVertexProgram |
| 005D3060 | `005D3064` `lea` | `02CB76A0` | PRenderTarget |
| 005D30B0 | `005D30B4` `lea` | `02CBB900` | PTexture2D |
| 005D32F0 | `005D32F4` `lea` | `02CB9000` | PShader |
| 005D38A0 | `005D38A4` `lea` | `02CBB600` | PStructuredBuffer |
| 005D39B0 | `005D39B4` `lea` | `02CB9100` | PShaderParameterCaptureBufferLocation |
| 005D39E0 | `005D39E4` `lea` | `02CBA600` | PShaderParameterCaptureBufferRWByteAddressBuffer |
| 005D3C30 | `005D3C34` `lea` | `02CBB300` | PShadowRenderer |
| 005D3FD0 | `005D3FD4` `lea` | `02CBB000` | PShaderFragmentProgram |
| 005D4310 | `005D4314` `lea` | `02CB6B80` | PMaterial |
| 005D4690 | `005D4694` `lea` | `02CB9F00` | PShaderParameterCaptureBufferTexture2D |
| 005D4790 | `005D4794` `lea` | `02CB6E80` | PMeshInstance |
| 005D4800 | `005D4804` `lea` | `02CB6680` | PEffect |
| 005D4B80 | `005D4B84` `lea` | `02CB9E00` | PShaderParameterCaptureConstantBuffer |
| 005D4BB0 | `005D4BB4` `lea` | `02CB9200` | PShaderParameterCaptureBufferLocationSize |
| 005D4BE0 | `005D4BE4` `lea` | `02CB6880` | PIndirectArgsBufferBase |
| 005D5150 | `005D5154` `lea` | `02CBBA00` | PTexture3DBase |
| 005D5190 | `005D5194` `lea` | `02CBB400` | PForwardShadowRenderer |
| 005D5210 | `005D5214` `lea` | `02CB9900` | PShaderPassBase |
| 005D5470 | `005D5474` `lea` | `02CB77A0` | PSamplerStateBase |
| 005D54C0 | `005D54C4` `lea` | `02CBB100` | PShaderGeometryProgram |
| 005D5DC0 | `005D5DC4` `lea` | `02CBA000` | PShaderParameterCaptureBufferTexture3D |
| 005D61D0 | `005D61D4` `lea` | `02CBBD00` | PTextureCubeMap |
| 005D6390 | `005D6394` `lea` | `02CBA700` | PShaderParameterCaptureBufferDataBlock |
| 005D63C0 | `005D63C4` `lea` | `02CB9300` | PShaderParameterCaptureBufferLocationType |
| 005D65B0 | `005D65CC` `lea` | `02CB6580` | PDynamicMeshInstance |
| 005D6990 | `005D6994` `lea` | `02CBB200` | PShaderComputeProgram |
| 005D6C70 | `005D6C74` `lea` | `02CB7CA0` | PSceneWideParameterBuffer |
| 005D6E90 | `005D6E94` `lea` | `02CBA100` | PShaderParameterCaptureBufferTextureCubeMap |
| 005D7030 | `005D7034` `lea` | `02CB6C80` | PMeshInstanceSegmentStreamBinding |
| 005D7250 | `005D7254` `lea` | `02CBB700` | PTextureCommonBase |
| 005D73C0 | `005D73C4` `lea` | `02CBA800` | PShaderParameterCaptureBufferIndexDataBlock |
| 005D7400 | `005D7404` `lea` | `02CB9400` | PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 005D7870 | `005D7874` `lea` | `02CB6980` | PIndirectArgsBuffer |
| 005D7A90 | `005D7A94` `lea` | `02CB7AA0` | PShaderPassInfo |
| 005D80E0 | `005D80E4` `lea` | `02CBA900` | PShaderParameterCaptureBufferRWTexture2D |
| 005D8140 | `005D8144` `lea` | `02CB6F80` | PMeshInstanceAttachPoint |
| 00610F30 | `00610F34` `lea` | `02CF1E40` | PTexture3DD3D11 |
| 00610FC0 | `00610FC4` `lea` | `02CF1540` | PShaderPassStateD3D11 |
| 00611130 | `00611134` `lea` | `02CF1940` | PShaderVertexProgramD3D11 |
| 00611690 | `00611694` `lea` | `02CF1A40` | PShaderFragmentProgramD3D11 |
| 006117A0 | `006117A4` `lea` | `02CF1440` | PShaderPassD3D11 |
| 00611B40 | `00611B44` `lea` | `02CF2440` | PConstantBufferD3D11 |
| 00611C50 | `00611C54` `lea` | `02CF1B40` | PShaderGeometryProgramD3D11 |
| 00611FF0 | `00611FF4` `lea` | `02CF1D40` | PTexture2DD3D11 |
| 006120A0 | `006120A4` `lea` | `02CF1C40` | PShaderComputeProgramD3D11 |
| 00612240 | `00612244` `lea` | `02CF2040` | PRenderTargetD3D11 |
| 006123A0 | `006123A4` `lea` | `02CF2240` | PStructuredBufferD3D11 |
| 006128C0 | `006128C4` `lea` | `02CF1640` | PStreamInputDescD3D11 |
| 00612B90 | `00612B94` `lea` | `02CF1F40` | PTextureCubeMapD3D11 |
| 00612DE0 | `00612DE4` `lea` | `02CF1740` | PStreamInputLayoutD3D11 |
| 00612F80 | `00612F84` `lea` | `02CF2340` | PIndirectArgsBufferD3D11 |
| 00613250 | `00613254` `lea` | `02CF1840` | PShaderProgramD3D11 |
| 00613330 | `00613334` `lea` | `02CF2140` | PSamplerStateD3D11 |
| 0063EB60 | `0063EB7C` `lea` | `02D34C40` | PDepthOfField |
| 0063EC90 | `0063ECAC` `lea` | `02D369A0` | PAtmosphericsD3D11 |
| 0063ED40 | `0063ED5C` `lea` | `02D364A0` | PScreenSpaceReflectionBase |
| 0063EE10 | `0063EE2C` `lea` | `02D35040` | PMotionBlurD3D11 |
| 0063F060 | `0063F07C` `lea` | `02D356A0` | PMLAABase |
| 0063F430 | `0063F44C` `lea` | `02D34840` | PDeferredLightingBase |
| 0063F890 | `0063F8AC` `lea` | `02D35AA0` | PGlowBase |
| 0063F9E0 | `0063F9FC` `lea` | `02D366A0` | PScreenSpaceReflectionD3D11 |
| 0063FCB0 | `0063FCCC` `lea` | `02D368A0` | PAtmospherics |
| 0063FD90 | `0063FDAC` `lea` | `02D358A0` | PMLAAD3D11 |
| 0063FFD0 | `0063FFEC` `lea` | `02D34F40` | PMotionBlur |
| 00640530 | `0064054C` `lea` | `02D35BA0` | PGlowGPUBase |
| 006406C0 | `006406DC` `lea` | `02D365A0` | PScreenSpaceReflection |
| 00640790 | `006407AC` `lea` | `02D36AA0` | PLowResParticles |
| 00640990 | `006409AC` `lea` | `02D357A0` | PMLAA |
| 00640B50 | `00640B6C` `lea` | `02D35300` | PScreenSpaceAmbientOcclusionBase |
| 00640F80 | `00640F9C` `lea` | `02D34A40` | PDeferredLightingD3D11 |
| 00641110 | `0064112C` `lea` | `02D35DA0` | PGlowD3D11 |
| 00641670 | `0064168C` `lea` | `02D36BA0` | PMaterialPostEffect |
| 006416C0 | `006416DC` `lea` | `02D361A0` | PCelShadingBase |
| 00641890 | `006418AC` `lea` | `02D35500` | PScreenSpaceAmbientOcclusionD3D11 |
| 00641DB0 | `00641DCC` `lea` | `02D35CA0` | PGlow |
| 00641F20 | `00641F3C` `lea` | `02D34940` | PDeferredLighting |
| 00642000 | `0064201C` `lea` | `02D363A0` | PCelShadingD3D11 |
| 00642290 | `006422AC` `lea` | `02D35400` | PScreenSpaceAmbientOcclusion |
| 006427D0 | `006427EC` `lea` | `02D35EA0` | PFXAABase |
| 00642880 | `0064289C` `lea` | `02D34B40` | PDepthOfFieldBase |
| 00642990 | `00642994` `lea` | `02D36CA0` | PPostEffectManager |
| 00642A20 | `00642A3C` `lea` | `02D362A0` | PCelShading |
| 00643180 | `0064319C` `lea` | `02D359A0` | PMeshParticleSystemBase |
| 006431F0 | `0064320C` `lea` | `02D360A0` | PFXAAD3D11 |
| 006433E0 | `006433FC` `lea` | `02D34740` | PPostEffectBase |
| 006438A0 | `006438BC` `lea` | `02D34D40` | PDepthOfFieldD3D11 |
| 006439D0 | `006439EC` `lea` | `02D35FA0` | PFXAA |
| 00643AA0 | `00643ABC` `lea` | `02D34E40` | PMotionBlurBase |
| 00643C80 | `00643C9C` `lea` | `02D367A0` | PAtmosphericsBase |
| 0065E8B0 | `0065E8B4` `lea` | `02D3A840` | PMeshSegmentBase |
| 0065EB00 | `0065EB04` `lea` | `02D3A240` | PIndexDataBlockBase |
| 0065ED70 | `0065ED74` `lea` | `02D3A640` | PMesh |
| 0065EFF0 | `0065EFF4` `lea` | `02D39840` | PMeshSegmentD3D11 |
| 0065F020 | `0065F024` `lea` | `02D39940` | PIndexDataBlockBufferD3D11 |
| 0065F2E0 | `0065F2E4` `lea` | `02D39B40` | PDataBlockBufferD3D11 |
| 0065F5E0 | `0065F5E4` `lea` | `02D3ADE0` | PVertexStream |
| 0065F850 | `0065F854` `lea` | `02D3A940` | PMeshSegment |
| 0065FC80 | `0065FC9C` `lea` | `02D3A140` | PDynamicMesh |
| 0065FCD0 | `0065FCD4` `lea` | `02D39A40` | PIndexDataBlockD3D11 |
| 0065FFC0 | `0065FFC4` `lea` | `02D39C40` | PDataBlockD3D11 |
| 006600E0 | `006600E4` `lea` | `02D3A040` | PDynamicSegmentDesc |
| 00660290 | `00660294` `lea` | `02D3A440` | PMaterialSet |
| 00660810 | `00660814` `lea` | `02D39D40` | PDataBlockBase |
| 00660930 | `00660934` `lea` | `02D3A540` | PSkeletonJointBounds |
| 00660B60 | `00660B64` `lea` | `02D3A340` | PIndexDataBlock |
| 00660D30 | `00660D34` `lea` | `02D3ACE0` | PShape |
| 00660F50 | `00660F54` `lea` | `02D39E40` | PDataBlock |
| 00661410 | `00661414` `lea` | `02D3A740` | PSkinBoneRemap |
| 00661690 | `00661694` `lea` | `02D39F40` | PDynamicDataBlock |
| 00674A50 | `00674A54` `lea` | `02D3E680` | PAssetReference |
| 00677FA0 | `00677FA4` `lea` | `02D3F210` | PCamera |
| 006781D0 | `006781EC` `lea` | `02D3F310` | PCameraProjection |
| 0067C740 | `0067C744` `lea` | `02E3FA60` | PBitmapFont |
| 0067C970 | `0067C974` `lea` | `02E3F960` | PBitmapFontCharInfo |
| 0067E350 | `0067E354` `lea` | `02E404B0` | PWorldMatrix |
| 00680440 | `00680444` `lea` | `02E41070` | PClassCallableMethodScript |
| 00680650 | `00680654` `lea` | `02E41270` | PAsyncProcessHeader |
| 006808E0 | `006808E4` `lea` | `02E41170` | PScriptCallbackHandler |
| 00680950 | `0068096C` `lea` | `02E41370` | PScheduler |
| 00680AE0 | `00680AE4` `lea` | `02E41470` | PScript |
| 00687F70 | `00687F74` `lea` | `02E49FD0` | PPhysicsCharacterControllerBullet |
| 00688060 | `00688064` `lea` | `02E494D0` | PPhysicsWorld |
| 00688170 | `00688174` `lea` | `02E489D0` | PPhysicsRigidBodyBase |
| 00688420 | `0068843C` `lea` | `02E495D0` | PPhysicsShapeBullet |
| 00688630 | `0068864C` `lea` | `02E499D0` | PPhysicsMeshBullet |
| 00688680 | `0068869C` `lea` | `02E490D0` | PPhysicsTaperedCapsule |
| 00689180 | `00689184` `lea` | `02E47ED0` | PPhysicsCharacterController |
| 00689210 | `0068922B` `lea` | `02E481D0` | PPhysicsInterfaceBase |
| 006893E0 | `006893FC` `lea` | `02E48DD0` | PPhysicsShape |
| 00689430 | `0068944C` `lea` | `02E485D0` | PPhysicsMesh |
| 00689610 | `0068962C` `lea` | `02E487D0` | PPhysicsPlaneBase |
| 00689F70 | `00689F74` `lea` | `02E493D0` | PRaycastResult |
| 0068A0D0 | `0068A0D4` `lea` | `02E49CD0` | PPhysicsRigidBodyBullet |
| 0068A460 | `0068A47C` `lea` | `02E48ED0` | PPhysicsSphereBase |
| 0068A5A0 | `0068A5BC` `lea` | `02E47FD0` | PPhysicsCylinderBase |
| 0068A630 | `0068A64B` `lea` | `02E49ED0` | PPhysicsInterfaceBullet |
| 0068A6E0 | `0068A6FC` `lea` | `02E49AD0` | PPhysicsPlaneBullet |
| 0068B2C0 | `0068B2C4` `lea` | `02E492D0` | PPhysicsWorldBase |
| 0068B370 | `0068B374` `lea` | `02E48BD0` | PPhysicsRigidBody |
| 0068B550 | `0068B56C` `lea` | `02E49BD0` | PPhysicsSphereBullet |
| 0068B5A0 | `0068B5BB` `lea` | `02E482D0` | PPhysicsInterface |
| 0068B6A0 | `0068B6BC` `lea` | `02E498D0` | PPhysicsCylinderBullet |
| 0068B770 | `0068B78C` `lea` | `02E488D0` | PPhysicsPlane |
| 0068C470 | `0068C48C` `lea` | `02E48FD0` | PPhysicsSphere |
| 0068C520 | `0068C524` `lea` | `02E486D0` | PPhysicsModel |
| 0068C550 | `0068C56C` `lea` | `02E480D0` | PPhysicsCylinder |
| 0068CDC0 | `0068CDDC` `lea` | `02E478D0` | PPhysicsBoxBase |
| 0068CE10 | `0068CE2C` `lea` | `02E47AD0` | PPhysicsCapsuleBase |
| 0068D040 | `0068D044` `lea` | `02E48AD0` | PPhysicsCallbackData |
| 0068D430 | `0068D44C` `lea` | `02E47CD0` | PPhysicsCharacterCamera |
| 0068D880 | `0068D89C` `lea` | `02E496D0` | PPhysicsBoxBullet |
| 0068D8D0 | `0068D8EC` `lea` | `02E497D0` | PPhysicsCapsuleBullet |
| 0068DF50 | `0068DF54` `lea` | `02E483D0` | PPhysicsMaterial |
| 0068DF80 | `0068DF84` `lea` | `02E49DD0` | PPhysicsWorldBullet |
| 0068E160 | `0068E17C` `lea` | `02E479D0` | PPhysicsBox |
| 0068E1B0 | `0068E1CC` `lea` | `02E47BD0` | PPhysicsCapsule |
| 0068E680 | `0068E684` `lea` | `02E47DD0` | PPhysicsCharacterControllerBase |
| 0068ED30 | `0068ED4C` `lea` | `02E484D0` | PPhysicsMeshBase |
| 0068EDE0 | `0068EDFC` `lea` | `02E491D0` | PPhysicsTaperedCylinder |
| 0068EE30 | `0068EE4C` `lea` | `02E48CD0` | PPhysicsShapeBase |
| 006A6F10 | `006A6F14` `lea` | `02E4D630` | PString |
| 006A7990 | `006A7994` `lea` | `02E4D940` | PTrigger |
| 006A9470 | `006A9474` `lea` | `02E4E1E0` | PQuarryComponent |
| 006A9C10 | `006A9C14` `lea` | `02E4E430` | PTypedObject |
| 006AA6F0 | `006AA6F4` `lea` | `02E4E720` | PComponent |
| 006AB2F0 | `006AB2F4` `lea` | `02E4EAF0` | PEntity |
| 006ACD40 | `006ACD5C` `lea` | `02E4F290` | PCameraOrthographic |
| 006AD5B0 | `006AD5CC` `lea` | `02E4F710` | PCameraPerspective |
| 006ADC70 | `006ADC74` `lea` | `02E4F900` | PInstancesComponent |
| 006AF970 | `006AF974` `lea` | `02E4FF60` | PNameComponent |
| 006B0210 | `006B0214` `lea` | `02E50160` | PRandomGenerator |
| 006B3BC0 | `006B3BDC` `lea` | `02E518D0` | PNode |
| 006B6940 | `006B6944` `lea` | `02E522F0` | PMeshSegmentContext |
| 006BB450 | `006BB454` `lea` | `02E57F60` | PModifierNetworkDynamicMeshSegment |
| 006BB990 | `006BB9AC` `lea` | `02E58060` | PModifierNetworkDynamicMesh |
| 006BE810 | `006BE814` `lea` | `02E58DB0` | PLight |
| 006C06E0 | `006C06E4` `lea` | `02E59DC0` | PShadowCaster |
| 006C0900 | `006C0904` `lea` | `02E59CC0` | PShadowSplit |
| 006C27E0 | `006C27E4` `lea` | `02E5A4C0` | PModifierNetworkInstanceInput |
| 006C2A10 | `006C2A14` `lea` | `02E5A5C0` | PModifierNetworkInstancePacketInput |
| 006C2C30 | `006C2C34` `lea` | `02E5A6C0` | PModifierNetworkInstance |
| 006C48D0 | `006C48D4` `lea` | `02E5AD00` | PLODLevel |
| 006C4BD0 | `006C4BD4` `lea` | `02E5AE00` | PLODGroup |
| 006C8030 | `006C8034` `lea` | `02E5BBB0` | POccluderGeometryInstance |
| 006CCDB0 | `006CCDCC` `lea` | `02E5C050` | PScriptableComponent |
| 006CD6B0 | `006CD6B4` `lea` | `02E5C370` | PTriggerReceiverTypeCallbackData |
| 006CDD80 | `006CDD84` `lea` | `02E5C710` | PTriggerReceiverComponent |
| 006CE8D0 | `006CE8D4` `lea` | `02E5E330` | PModifierNetworkInfoPacket_Buffer |
| 006CEAE0 | `006CEAE4` `lea` | `02E5DD30` | PRenderStreamInput |
| 006CEC00 | `006CEC04` `lea` | `02E5E430` | PModifierNetworkInfoPacket |
| 006CEEC0 | `006CEEC4` `lea` | `02E5DE30` | PRenderStream |
| 006CF120 | `006CF124` `lea` | `02E5DF30` | PModifierNetworkBuffer |
| 006CF370 | `006CF374` `lea` | `02E5E030` | PModifierAndInputs |
| 006CF5A0 | `006CF5A4` `lea` | `02E5E130` | PModifierNetworkInfoPacket_ModifierCode |
| 006CF7D0 | `006CF7D4` `lea` | `02E5E540` | PModifierNetwork |
| 006CF8C0 | `006CF8C4` `lea` | `02E5E230` | PModifierNetworkInfoPacket_ModifierInstance |
| 006D7170 | `006D7174` `lea` | `02E9FDF0` | PMorphModifierWeightsUserDataObject |
| 006D9CB0 | `006D9CB4` `lea` | `02EA0850` | POccluderGeometryObject |
| 00791230 | `00791234` `lea` | `02EA9400` | PDebugUtils |
| 00791470 | `0079148C` `lea` | `02EA5660` | PApplication |
| 00791610 | `0079162C` `lea` | `02EA5380` | PApplicationViewport |
| 00791820 | `00791824` `lea` | `02EA5560` | PInputMapper |
| 00867310 | `0086732C` `lea` | `02EB6BF0` | PInputSourceVisionTrackerZ |
| 008673C0 | `008673DC` `lea` | `02EB62F0` | PInputSourceMotionQuatW |
| 00867470 | `0086748C` `lea` | `02EB59F0` | PInputSourceTouchRotate |
| 00867A80 | `00867A9C` `lea` | `02EB63F0` | PInputSourceMotionAngularVelocityX |
| 00867B30 | `00867B4C` `lea` | `02EB5AF0` | PInputSourceTouchPinch |
| 00867F80 | `00867F9C` `lea` | `02EB6CF0` | PInputAction |
| 00868030 | `0086804C` `lea` | `02EB52F0` | PInputSource |
| 00868150 | `0086816C` `lea` | `02EB64F0` | PInputSourceMotionAngularVelocityY |
| 00868260 | `0086827C` `lea` | `02EB5DF0` | PInputSourceTouchTwoFingerDragX |
| 00868890 | `008688AC` `lea` | `02EB53F0` | PInputSourceKey |
| 008689B0 | `008689CC` `lea` | `02EB65F0` | PInputSourceMotionAngularVelocityZ |
| 00868A60 | `00868A7C` `lea` | `02EB5EF0` | PInputSourceTouchTwoFingerDragY |
| 00869060 | `00869064` `lea` | `02EB6DF0` | PInputMap |
| 00869160 | `0086917C` `lea` | `02EB54F0` | PInputSourceJoypadButton |
| 00869230 | `0086924C` `lea` | `02EB66F0` | PInputSourceMotionLinearAccelerationX |
| 008693A0 | `008693BC` `lea` | `02EB5BF0` | PInputSourceTouchDragX |
| 00869A00 | `00869A1C` `lea` | `02EB55F0` | PInputSourceJoypadAxis |
| 00869AB0 | `00869ACC` `lea` | `02EB67F0` | PInputSourceMotionLinearAccelerationY |
| 00869B60 | `00869B7C` `lea` | `02EB5CF0` | PInputSourceTouchDragY |
| 0086A1D0 | `0086A1EC` `lea` | `02EB56F0` | PInputSourceMouseButton |
| 0086A240 | `0086A25C` `lea` | `02EB68F0` | PInputSourceMotionLinearAccelerationZ |
| 0086A330 | `0086A34C` `lea` | `02EB5FF0` | PInputSourceMotionQuatX |
| 0086A930 | `0086A94C` `lea` | `02EB69F0` | PInputSourceVisionTrackerX |
| 0086A9A0 | `0086A9BC` `lea` | `02EB57F0` | PInputSourceMouseDeltaX |
| 0086AA30 | `0086AA4C` `lea` | `02EB60F0` | PInputSourceMotionQuatY |
| 0086B0A0 | `0086B0BC` `lea` | `02EB6AF0` | PInputSourceVisionTrackerY |
| 0086B150 | `0086B16C` `lea` | `02EB61F0` | PInputSourceMotionQuatZ |
| 0086B200 | `0086B21C` `lea` | `02EB58F0` | PInputSourceMouseDeltaY |
| 00874740 | `00874744` `lea` | `02EB7BD0` | PVisionMoveTrackerBase |
| 008748D0 | `008748D4` `lea` | `02EB7DD0` | PVisionMoveTrackerWin32 |
| 00874A60 | `00874A64` `lea` | `02EB7CD0` | PVisionMoveTracker |
| 008753B0 | `008753B4` `lea` | `02EB7F60` | PVisionTrackerBase |
| 00875540 | `00875544` `lea` | `02EB8160` | PVisionTrackerWin32 |
| 008756D0 | `008756D4` `lea` | `02EB8060` | PVisionTracker |
| 008773E0 | `008773E4` `lea` | `02EB9270` | POctreeWorld |
| 00877610 | `00877614` `lea` | `02EB9170` | POctreeData |
| 00877860 | `00877864` `lea` | `02EB9070` | POctree |
| 00877AC0 | `00877AC4` `lea` | `02EB9370` | POctreeChildren |
| 00879800 | `00879804` `lea` | `02EB9E60` | PGameConfig |
| 005A0E30 | `005A0E4C` `lea` | `02CADD50` | PAnimationController |
| 005A12A0 | `005A12BC` `lea` | `02CAECE0` | PAnimationTargetBlenderController |
| 005A1920 | `005A193C` `lea` | `02CAEEE0` | PTimeController |
| 005A2140 | `005A215C` `lea` | `02CAEFE0` | PTimeIntervalController |
| 005A2390 | `005A23AC` `lea` | `02CAD140` | PAnimatableComponent |
| 005A26A0 | `005A26BC` `lea` | `02CAEA60` | PAnimationSlotFilter |

## Per-member rows: the class descriptor each of the PType name-only class-registration initialisers loads (OPUS, 2026-10-03)

The family `PType name-only class-registration initialisers` (frontmatter: 110 members; 91 get a row here) shares one shape, stated here once and not repeated per row: `lea rcx, [X]`, a call to `006388C0`, `lea rcx, [X]` again and a tail jump to `00639450`. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (every load of it in the body names the same X). Each row anchors the first such `lea`, the member's distinguishing instruction, and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-name-only-registration-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-name-only-registration-1003/rows.tsv). A member whose loads name more than one X, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Nineteen members that derive are left without a row by a declared skip (spec.json `skip`), each with its reason in [`excluded.tsv`](../../_index/candidates/opus-ee-name-only-registration-1003/excluded.tsv): `00875E10`, a caller in another layer, calls each of them, and citing them here would pull that caller edge into the page.

### All 91 members (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 00584D10 | `00584D14` `lea` | `02CAA0A0` | PClusterHeader |
| 005A3400 | `005A3404` `lea` | `02CAE450` | PAnimationNetworkInstanceTarget |
| 005A4280 | `005A4284` `lea` | `02CAE860` | PAnimationSlotArray |
| 005A5710 | `005A5714` `lea` | `02CAE250` | PAnimationHierarchyNode |
| 005CE620 | `005CE624` `lea` | `02CB78A0` | PSamplerState |
| 005CFB60 | `005CFB64` `lea` | `02CBBB00` | PTexture3D |
| 005D12D0 | `005D12D4` `lea` | `02CB9A00` | PShaderPass |
| 005D1BB0 | `005D1BB4` `lea` | `02CB6480` | PConstantBuffer |
| 005D26D0 | `005D26D4` `lea` | `02CBAD00` | PShaderProgramBase |
| 005D3250 | `005D3254` `lea` | `02CBAF00` | PShaderVertexProgram |
| 005D3480 | `005D3484` `lea` | `02CB76A0` | PRenderTarget |
| 005D34B0 | `005D34B4` `lea` | `02CBB900` | PTexture2D |
| 005D3DB0 | `005D3DB4` `lea` | `02CBB600` | PStructuredBuffer |
| 005D3FB0 | `005D3FB4` `lea` | `02CBB300` | PShadowRenderer |
| 005D43A0 | `005D43A4` `lea` | `02CBB000` | PShaderFragmentProgram |
| 005D5280 | `005D5284` `lea` | `02CB6880` | PIndirectArgsBufferBase |
| 005D58A0 | `005D58A4` `lea` | `02CBB400` | PForwardShadowRenderer |
| 005D5A80 | `005D5A84` `lea` | `02CBB100` | PShaderGeometryProgram |
| 005D6530 | `005D6534` `lea` | `02CBBD00` | PTextureCubeMap |
| 005D6CA0 | `005D6CA4` `lea` | `02CBB200` | PShaderComputeProgram |
| 005D7D40 | `005D7D44` `lea` | `02CB6980` | PIndirectArgsBuffer |
| 00611110 | `00611114` `lea` | `02CF1E40` | PTexture3DD3D11 |
| 00612550 | `00612554` `lea` | `02CF2040` | PRenderTargetD3D11 |
| 00612640 | `00612644` `lea` | `02CF2240` | PStructuredBufferD3D11 |
| 006130D0 | `006130D4` `lea` | `02CF2340` | PIndirectArgsBufferD3D11 |
| 006177D0 | `006177D4` `lea` | `02CF2440` | PConstantBufferD3D11 |
| 006177F0 | `006177F4` `lea` | `02CF2140` | PSamplerStateD3D11 |
| 006179C0 | `006179C4` `lea` | `02CF1A40` | PShaderFragmentProgramD3D11 |
| 006179E0 | `006179E4` `lea` | `02CF1B40` | PShaderGeometryProgramD3D11 |
| 00618700 | `00618704` `lea` | `02CF1D40` | PTexture2DD3D11 |
| 00618720 | `00618724` `lea` | `02CF1F40` | PTextureCubeMapD3D11 |
| 0063EC70 | `0063EC74` `lea` | `02D34C40` | PDepthOfField |
| 0063EF40 | `0063EF44` `lea` | `02D369A0` | PAtmosphericsD3D11 |
| 0063F200 | `0063F204` `lea` | `02D35040` | PMotionBlurD3D11 |
| 0063F350 | `0063F354` `lea` | `02D356A0` | PMLAABase |
| 0063FBE0 | `0063FBE4` `lea` | `02D366A0` | PScreenSpaceReflectionD3D11 |
| 0063FFB0 | `0063FFB4` `lea` | `02D368A0` | PAtmospherics |
| 006400A0 | `006400A4` `lea` | `02D358A0` | PMLAAD3D11 |
| 00640200 | `00640204` `lea` | `02D34F40` | PMotionBlur |
| 006406A0 | `006406A4` `lea` | `02D35BA0` | PGlowGPUBase |
| 00640970 | `00640974` `lea` | `02D365A0` | PScreenSpaceReflection |
| 00640AB0 | `00640AB4` `lea` | `02D36AA0` | PLowResParticles |
| 00640CE0 | `00640CE4` `lea` | `02D357A0` | PMLAA |
| 00640E90 | `00640E94` `lea` | `02D35300` | PScreenSpaceAmbientOcclusionBase |
| 00641350 | `00641354` `lea` | `02D34A40` | PDeferredLightingD3D11 |
| 00641430 | `00641434` `lea` | `02D35DA0` | PGlowD3D11 |
| 00641940 | `00641944` `lea` | `02D36BA0` | PMaterialPostEffect |
| 00641A70 | `00641A74` `lea` | `02D35500` | PScreenSpaceAmbientOcclusionD3D11 |
| 00641F70 | `00641F74` `lea` | `02D35CA0` | PGlow |
| 00642130 | `00642134` `lea` | `02D34940` | PDeferredLighting |
| 00642250 | `00642254` `lea` | `02D363A0` | PCelShadingD3D11 |
| 00642580 | `00642584` `lea` | `02D35400` | PScreenSpaceAmbientOcclusion |
| 00642950 | `00642954` `lea` | `02D35EA0` | PFXAABase |
| 00642D20 | `00642D24` `lea` | `02D362A0` | PCelShading |
| 00643340 | `00643344` `lea` | `02D359A0` | PMeshParticleSystemBase |
| 006433C0 | `006433C4` `lea` | `02D360A0` | PFXAAD3D11 |
| 006439B0 | `006439B4` `lea` | `02D34D40` | PDepthOfFieldD3D11 |
| 00643C50 | `00643C54` `lea` | `02D35FA0` | PFXAA |
| 0065F5A0 | `0065F5A4` `lea` | `02D39B40` | PDataBlockBufferD3D11 |
| 0065FA20 | `0065FA24` `lea` | `02D3A940` | PMeshSegment |
| 00660CD0 | `00660CD4` `lea` | `02D3A340` | PIndexDataBlock |
| 00661170 | `00661174` `lea` | `02D39E40` | PDataBlock |
| 00666360 | `00666364` `lea` | `02D39940` | PIndexDataBlockBufferD3D11 |
| 006882A0 | `006882A4` `lea` | `02E49FD0` | PPhysicsCharacterControllerBullet |
| 006888E0 | `006888E4` `lea` | `02E495D0` | PPhysicsShapeBullet |
| 00688B30 | `00688B34` `lea` | `02E499D0` | PPhysicsMeshBullet |
| 00689320 | `00689324` `lea` | `02E47ED0` | PPhysicsCharacterController |
| 006893C0 | `006893C4` `lea` | `02E481D0` | PPhysicsInterfaceBase |
| 006897B0 | `006897B4` `lea` | `02E48DD0` | PPhysicsShape |
| 006898B0 | `006898B4` `lea` | `02E485D0` | PPhysicsMesh |
| 0068A3A0 | `0068A3A4` `lea` | `02E49CD0` | PPhysicsRigidBodyBullet |
| 0068AB40 | `0068AB44` `lea` | `02E49ED0` | PPhysicsInterfaceBullet |
| 0068AB60 | `0068AB64` `lea` | `02E49AD0` | PPhysicsPlaneBullet |
| 0068BA40 | `0068BA44` `lea` | `02E49BD0` | PPhysicsSphereBullet |
| 0068BA60 | `0068BA64` `lea` | `02E482D0` | PPhysicsInterface |
| 0068BC30 | `0068BC34` `lea` | `02E498D0` | PPhysicsCylinderBullet |
| 0068BC50 | `0068BC54` `lea` | `02E488D0` | PPhysicsPlane |
| 0068C700 | `0068C704` `lea` | `02E48FD0` | PPhysicsSphere |
| 0068C7F0 | `0068C7F4` `lea` | `02E480D0` | PPhysicsCylinder |
| 0068DB00 | `0068DB04` `lea` | `02E496D0` | PPhysicsBoxBullet |
| 0068DB20 | `0068DB24` `lea` | `02E497D0` | PPhysicsCapsuleBullet |
| 0068E140 | `0068E144` `lea` | `02E49DD0` | PPhysicsWorldBullet |
| 0068E480 | `0068E484` `lea` | `02E479D0` | PPhysicsBox |
| 0068E4A0 | `0068E4A4` `lea` | `02E47BD0` | PPhysicsCapsule |
| 006B8910 | `006B8914` `lea` | `02E522F0` | PMeshSegmentContext |
| 00874830 | `00874834` `lea` | `02EB7BD0` | PVisionMoveTrackerBase |
| 008749C0 | `008749C4` `lea` | `02EB7DD0` | PVisionMoveTrackerWin32 |
| 00874B50 | `00874B54` `lea` | `02EB7CD0` | PVisionMoveTracker |
| 00875290 | `00875294` `lea` | `02EB8060` | PVisionTracker |
| 008754A0 | `008754A4` `lea` | `02EB7F60` | PVisionTrackerBase |
| 00875630 | `00875634` `lea` | `02EB8160` | PVisionTrackerWin32 |

## Per-member rows: the registry-fetch function each traversal adapter calls, and the class it returns (OPUS, 2026-10-03)

The family `registry-fetch reflection traversal adapters` (frontmatter: 84 members; 15 get a row here) shares one shape, stated here once and not repeated per row: on each path the adapter calls a registry-fetch function and hands its result with the object to the shared traversal `0063E2E0`. What differs from member to member is that fetch function: no two members call the same one. Each row anchors the adapter's first call to it (the member's distinguishing instruction) and states the fetch function and the class whose descriptor it constructs and returns. The class name is read from the certified image: the `lea r8, [name]` before the fetch function's first call to a descriptor constructor (`00632C90` or `00632D80`). The fetch function is printed as a bare address, not a citation. [`fam_rows.py`](../../_index/candidates/opus-ee-registry-fetch-adapters-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-registry-fetch-adapters-1003/rows.tsv). Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-registry-fetch-adapters-1003/excluded.tsv).

### All 15 adapters (OPUS)

| member | distinguishing instruction | registry-fetch function called | class whose descriptor it returns |
|---|---|---|---|
| 005A0C00 | `005A0C0E` `call` | 005A02D0 | PTimer |
| 0062ADF0 | `0062ADFE` `call` | 00613800 | CD3D11_BLEND_DESC |
| 0062AE40 | `0062AE4E` `call` | 00613A30 | CD3D11_DEPTH_STENCIL_DESC |
| 0062AE90 | `0062AE9E` `call` | 00613E80 | CD3D11_RASTERIZER_DESC |
| 0062AEE0 | `0062AEEE` `call` | 006143B0 | D3D11_DEPTH_STENCILOP_DESC |
| 0062AF30 | `0062AF3E` `call` | 00614640 | D3D11_RENDER_TARGET_BLEND_DESC |
| 006B2EA0 | `006B2EAE` `call` | 006B0760 | Matrix3 |
| 006B2EF0 | `006B2EFE` `call` | 006B08A0 | Matrix4 |
| 006B2F40 | `006B2F4E` `call` | 006B09E0 | PMatrix4 |
| 006B2F90 | `006B2F9E` `call` | 006B0B20 | Point3 |
| 006B2FE0 | `006B2FEE` `call` | 006B0EC0 | Quat |
| 006B3030 | `006B303E` `call` | 006B1320 | Vector2 |
| 006B3080 | `006B308E` `call` | 006B1600 | Vector3 |
| 006B30D0 | `006B30DE` `call` | 006B19A0 | Vector4 |
| 006B3AC0 | `006B3ACE` `call` | 006B33F0 | PMatrix4x3 |

## Per-member rows: the vtable each guarded class-registration stub installs, and its reflected type (OPUS, 2026-10-03)

The family `guarded class-registration stubs` (frontmatter: 99 members; 43 get a row here) shares a pattern, not a form (129 to 3757 bytes), stated here once and not repeated per row. Under the thread-safe static-init guard (`008092FC` / `0080929C`), each stub constructs one or more static Phyre metadata objects and registers members and teardowns. Members differ in far more than the anchored instruction. Each row anchors the body's first `lea rax, [V]` whose following `mov` stores V into a static object X that the body also loads with a `lea`, and states V and the class V's MSVC RTTI complete-object locator names, read from the certified image: the template argument T for a `PClassDescriptor*<T>`, otherwise the decorated class.
- In 25 rows, X is the static class descriptor the body constructs. In 15, it is built through `00632D80` and V is its `PClassDescriptorAbstract<T>` vtable, which a later store replaces with `PClassDescriptorConcrete<T>`. In 10, it is built through `00632C90` and V is its `PClassDescriptorWrapper<T>` vtable.
- In the other 18, the body constructs no class descriptor. X is a static data-member object in 15 rows (`PClassDataMember*<…>`), a `PTypeDefault<unsigned int>` in `006315B0`, and a `PNamedSemanticDescriptorForType<…>` in `00661A70` and `006D5810`. [`fam_rows.py`](../../_index/candidates/opus-ee-guarded-registration-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-guarded-registration-1003/rows.tsv). Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-guarded-registration-1003/excluded.tsv).

### All 43 stubs (OPUS)

| member | distinguishing instruction | first vtable V stored into a lea-loaded static | class named by the RTTI locator before V (T for a class descriptor) |
|---|---|---|---|
| 005B5130 | `005B51D9` `lea` | `00D32C40` | decorated `V?$PArray@M$03@Phyre@@` |
| 005B7790 | `005B7839` `lea` | `00D33050` | decorated `V?$PArray@VPQWord@Phyre@@$0BA@@Phyre@@` |
| 005EBB00 | `005EBBA9` `lea` | `00D4E188` | decorated `V?$PArray@PEAVPModifierNetworkInstance@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 005ED1A0 | `005ED249` `lea` | `00D4B830` | decorated `V?$PArray@VPMatrix4@Phyre@@$03@Phyre@@` |
| 005EFB10 | `005EFBB9` `lea` | `00D4C5F8` | decorated `V?$PSharray@I@Phyre@@` |
| 005EFE60 | `005EFF09` `lea` | `00D4DD98` | decorated `V?$PSharray@PEBVPMeshInstanceSegmentStreamBinding@PRendering@Phyre@@@Phyre@@` |
| 006143B0 | `0061442A` `lea` | `00D546C8` | D3D11_DEPTH_STENCILOP_DESC |
| 00618080 | `0061812D` `lea` | `00D54D68` | decorated `.?AV?$PClassDataMemberPhyreArray@E@Phyre@@` |
| 00618620 | `006186BB` `lea` | `00D54CE8` | decorated `.?AV?$PClassDataMemberPhyreArray@VPStreamInputDescD3D11@PRendering@Phyre@@@Phyre@@` |
| 00618970 | `00618A19` `lea` | `00D556E0` | decorated `V?$PArray@E$00@Phyre@@` |
| 006315B0 | `0063167C` `lea` | `00D311B0` | decorated `.?AV?$PTypeDefault@I@Phyre@@` |
| 00635DC0 | `00635F9D` `lea` | `00D58EC0` | decorated `.?AV?$PClassDataMemberArrayDynamic@V?$PSharray@VPString@Phyre@@@Phyre@@@Phyre@@` |
| 00661A70 | `00661AEF` `lea` | `00D69710` | decorated `.?AV?$PNamedSemanticDescriptorForType@VPRenderDataType@PGeometry@Phyre@@@Phyre@@` |
| 00665870 | `00665918` `lea` | `00D69068` | decorated `.?AV?$PClassDataMemberPhyreSharray@VPDataBlockBufferD3D11@PGeometry@Phyre@@@Phyre@@` |
| 00666380 | `00666428` `lea` | `00D68EF8` | decorated `.?AV?$PClassDataMemberPhyreSharray@VPIndexDataBlockBufferD3D11@PGeometry@Phyre@@@Phyre@@` |
| 00667230 | `006672D9` `lea` | `00D68E50` | decorated `.?AV?$PClassDataMemberPhyreArray@VPDataBlockD3D11@PGeometry@Phyre@@@Phyre@@` |
| 00668AE0 | `00668B89` `lea` | `00D69870` | decorated `V?$PArray@E$03@Phyre@@` |
| 00668E10 | `00668EB9` `lea` | `00D6AA28` | decorated `V?$PArray@H$03@Phyre@@` |
| 0066A460 | `0066A509` `lea` | `00D6A440` | decorated `V?$PSharray@PEAVPMaterial@PRendering@Phyre@@@Phyre@@` |
| 00696470 | `00696A10` `lea` | `00D79E18` | decorated `.?AV?$PClassDataMemberPhyreSharray@PEAVPPhysicsShape@PPhysics@Phyre@@@Phyre@@` |
| 00698930 | `006989D9` `lea` | `00D7AC20` | decorated `V?$PSharray@PEAVPPhysicsShape@PPhysics@Phyre@@@Phyre@@` |
| 006A72B0 | `006A7353` `lea` | `00D7B5D8` | decorated `.?AV?$PClassDataMemberArrayDynamic@VPString@Phyre@@@Phyre@@` |
| 006AE350 | `006AE72A` `lea` | `00D7E070` | decorated `.?AV?$PClassDataMemberPhyreArray@VPTypedObject@Phyre@@@Phyre@@` |
| 006B0760 | `006B07DA` `lea` | `00D7F960` | sce::Vectormath::Scalar::Aos::Matrix3 |
| 006B08A0 | `006B091A` `lea` | `00D7FA70` | sce::Vectormath::Scalar::Aos::Matrix4 |
| 006B09E0 | `006B0A5A` `lea` | `00D7FB80` | Phyre::PMatrix4 |
| 006B0B20 | `006B0BA6` `lea` | `00D7F628` | sce::Vectormath::Scalar::Aos::Point3 |
| 006B0EC0 | `006B0F46` `lea` | `00D7F850` | sce::Vectormath::Scalar::Aos::Quat |
| 006B1320 | `006B13A9` `lea` | `00D7F3E0` | sce::Vectormath::Scalar::Aos::Vector2 |
| 006B1600 | `006B1686` `lea` | `00D7F510` | sce::Vectormath::Scalar::Aos::Vector3 |
| 006B19A0 | `006B1A26` `lea` | `00D7F738` | sce::Vectormath::Scalar::Aos::Vector4 |
| 006B33F0 | `006B346F` `lea` | `00D7FE58` | Phyre::PMatrix4x3 |
| 006BC750 | `006BC7FD` `lea` | `00D81E30` | decorated `.?AV?$PClassDataMemberPhyreArray@PEAE@Phyre@@` |
| 006BCC40 | `006BCCE9` `lea` | `00D82090` | decorated `V?$PArray@PEBE$07@Phyre@@` |
| 006C3380 | `006C349B` `lea` | `00D84DC8` | decorated `.?AV?$PClassDataMemberPhyreArray@PEAVPBase@Phyre@@@Phyre@@` |
| 006C3800 | `006C38A9` `lea` | `00D84EE0` | decorated `V?$PArray@PEBVPBase@Phyre@@$07@Phyre@@` |
| 006C6560 | `006C6609` `lea` | `00D86028` | decorated `V?$PSharray@PEAVPMeshInstance@PRendering@Phyre@@@Phyre@@` |
| 006D0D50 | `006D0F4D` `lea` | `00D8CA88` | decorated `.?AV?$PClassDataMemberPhyreArray@VPRenderStreamInput@PDynamicGeometry@Phyre@@@Phyre@@` |
| 006D0FA0 | `006D104D` `lea` | `00D8CC18` | decorated `.?AV?$PClassDataMemberPhyreArray@VPModifierAndInputs@PDynamicGeometry@Phyre@@@Phyre@@` |
| 006D5810 | `006D588F` `lea` | `00D8D7B8` | decorated `.?AV?$PNamedSemanticDescriptorForType@VPModifier@PDynamicGeometry@Phyre@@@Phyre@@` |
| 006D8EF0 | `006D8F90` `lea` | `00D31C50` | decorated `.?AV?$PClassDataMemberPhyreArray@M@Phyre@@` |
| 00879D60 | `00879E76` `lea` | `01CD9E20` | decorated `.?AV?$PClassDataMemberPhyreArray@PEAVPInputMap@PInputs@Phyre@@@Phyre@@` |
| 00879EC0 | `00879F69` `lea` | `01CD9F18` | decorated `V?$PArray@PEAVPInputMap@PInputs@Phyre@@$07@Phyre@@` |

## Per-member rows: the class descriptor each of the flag-selected reflection traversal adapters loads (OPUS, 2026-10-03)

The family `flag-selected reflection traversal adapters` (frontmatter: 11 members; 11 get a row here) shares one shape, stated here once and not repeated per row: `lea rcx, [X]`, then a call to the shared traversal `0063E2E0` with the flag in `r8b` normalised to 1 or 0. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (every load of it in the body names the same X). Each row anchors the first such `lea`, the member's distinguishing instruction, and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-flag-selected-adapters-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-flag-selected-adapters-1003/rows.tsv). A member whose loads name more than one X, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-flag-selected-adapters-1003/excluded.tsv).

### All 11 members (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 00584750 | `00584754` `lea` | `02CA9FA0` | PClusterHeaderBase |
| 005849B0 | `005849B4` `lea` | `02CA9DA0` | PClusterHeaderD3D11 |
| 00584C20 | `00584C24` `lea` | `02CAA0A0` | PClusterHeader |
| 00584EC0 | `00584EC4` `lea` | `02CA9EA0` | PInstanceListHeader |
| 005A1140 | `005A1144` `lea` | `02CAD040` | PBlendableAnimationSource |
| 005A1650 | `005A1654` `lea` | `02CAD840` | PAnimationClip |
| 005A17F0 | `005A17F4` `lea` | `02CAE960` | PAnimationSlotFilterDeferredLoad |
| 005A1C60 | `005A1C64` `lea` | `02CAD540` | PAnimationChannelBase |
| 005A22A0 | `005A22A4` `lea` | `02CAD440` | PAnimationChannel |
| 005A27C0 | `005A27C4` `lea` | `02CAE350` | PAnimationDataSourceListEntry |
| 00674CD0 | `00674CD4` `lea` | `02D3E780` | PAssetReferenceImport |

## Per-member rows: the vtable each two-member descriptor registrar installs, and its reflected type (OPUS, 2026-10-03)

The family `two-member class-descriptor registrars (m_count + m_els)` (frontmatter: 38 members; 38 get a row here) shares one 815-byte form, stated here once and not repeated per row. Under the thread-safe static-init guard (`008092FC` / `0080929C`), each stub constructs its static class descriptor through `00632D80`, stores the `PClassDescriptorAbstract<T>` vtable into it, calls the three member-registration helpers, then replaces that vtable with `PClassDescriptorConcrete<T>`, and goes on to register the `m_count` and `m_els` members and their teardowns. Members differ in every per-class operand of that form (53 instructions: the descriptor, its guard variables, both vtables, the helper arguments, the element descriptor and the teardowns). Each row anchors the first of them that names the class, the `lea rax, [V]` at + 0xA9 whose following `mov` stores the `PClassDescriptorAbstract<T>` vtable V into the descriptor. It states V and T, the template argument named by V's MSVC RTTI complete-object locator, read from the certified image. [`fam_rows.py`](../../_index/candidates/opus-ee-two-member-registrars-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-two-member-registrars-1003/rows.tsv). Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-two-member-registrars-1003/excluded.tsv).

### All 38 registrars (OPUS)

| member | distinguishing instruction | vtable V installed | reflected type (RTTI before V) |
|---|---|---|---|
| 005B5AE0 | `005B5B89` `lea` | `00D33838` | decorated `V?$PArray@VPAnimationChannelTarget@PAnimation@Phyre@@$07@Phyre@@` |
| 005B5E10 | `005B5EB9` `lea` | `00D33440` | decorated `V?$PArray@VPAnimationConstantChannel@PAnimation@Phyre@@$07@Phyre@@` |
| 005B6140 | `005B61E9` `lea` | `00D34210` | decorated `V?$PArray@VPAnimationDataSourceListEntry@PAnimation@Phyre@@$07@Phyre@@` |
| 005B6470 | `005B6519` `lea` | `00D33C28` | decorated `V?$PArray@VPAnimationEvent@PAnimation@Phyre@@$03@Phyre@@` |
| 005B67A0 | `005B6849` `lea` | `00D34408` | decorated `V?$PArray@VPAnimationNetworkInstanceTarget@PAnimation@Phyre@@$07@Phyre@@` |
| 005B6AD0 | `005B6B79` `lea` | `00D34600` | decorated `V?$PArray@VPAnimationSlotArray@PAnimation@Phyre@@$07@Phyre@@` |
| 005B6E00 | `005B6EA9` `lea` | `00D33E20` | decorated `V?$PArray@VPAnimationSlotFilterDeferredLoad@PAnimation@Phyre@@$07@Phyre@@` |
| 005B7130 | `005B71D9` `lea` | `00D33A30` | decorated `V?$PArray@VPAnimationSlotListIndex@PAnimation@Phyre@@$07@Phyre@@` |
| 005B7460 | `005B7509` `lea` | `00D347F8` | decorated `V?$PArray@VPBlendableAnimationSource@PAnimation@Phyre@@$07@Phyre@@` |
| 005ECB40 | `005ECBE9` `lea` | `00D4CBE0` | decorated `V?$PArray@VPContextVariantFoldingTable@PRendering@Phyre@@$03@Phyre@@` |
| 005ECE70 | `005ECF19` `lea` | `00D4CDD8` | decorated `V?$PArray@VPMaterialSwitch@PRendering@Phyre@@$07@Phyre@@` |
| 005ED4D0 | `005ED579` `lea` | `00D4DF90` | decorated `V?$PArray@VPMeshInstanceSegmentContext@PRendering@Phyre@@$07@Phyre@@` |
| 005ED800 | `005ED8A9` `lea` | `00D4DBA0` | decorated `V?$PArray@VPNodeContext@PRendering@Phyre@@$07@Phyre@@` |
| 005EDB30 | `005EDBD9` `lea` | `00D4CFD0` | decorated `V?$PArray@VPSceneRenderPass@PRendering@Phyre@@$07@Phyre@@` |
| 005EDE60 | `005EDF09` `lea` | `00D4C7F0` | decorated `V?$PArray@VPShader@PRendering@Phyre@@$07@Phyre@@` |
| 005EE190 | `005EE239` `lea` | `00D4C208` | decorated `V?$PArray@VPShaderParameterCaptureBufferLocation@PRendering@Phyre@@$01@Phyre@@` |
| 005EE4C0 | `005EE569` `lea` | `00D4BE18` | decorated `V?$PArray@VPShaderParameterCaptureBufferLocationType@PRendering@Phyre@@$01@Phyre@@` |
| 005EE7F0 | `005EE899` `lea` | `00D4C010` | decorated `V?$PArray@VPShaderParameterCaptureBufferLocationTypeConstantBuffer@PRendering@Phyre@@$03@Phyre@@` |
| 005EEB20 | `005EEBC9` `lea` | `00D4BC20` | decorated `V?$PArray@VPShaderParameterDefinition@PRendering@Phyre@@$07@Phyre@@` |
| 005EEE50 | `005EEEF9` `lea` | `00D4C400` | decorated `V?$PArray@VPShaderPass@PRendering@Phyre@@$07@Phyre@@` |
| 005EF180 | `005EF229` `lea` | `00D4C9E8` | decorated `V?$PArray@VPShaderPassInfo@PRendering@Phyre@@$07@Phyre@@` |
| 005EF4B0 | `005EF559` `lea` | `00D4BA28` | decorated `V?$PArray@VPShaderStreamDefinition@PRendering@Phyre@@$07@Phyre@@` |
| 005EF7E0 | `005EF889` `lea` | `00D4B638` | decorated `V?$PArray@VPString@Phyre@@$07@Phyre@@` |
| 00618CA0 | `00618D49` `lea` | `00D558D8` | decorated `V?$PArray@VPStreamInputDescD3D11@PRendering@Phyre@@$07@Phyre@@` |
| 00669140 | `006691E9` `lea` | `00D6A248` | decorated `V?$PArray@VPDataBlockD3D11@PGeometry@Phyre@@$07@Phyre@@` |
| 00669470 | `00669519` `lea` | `00D6AC20` | decorated `V?$PArray@VPDynamicSegmentDesc@PDynamicMesh@PGeometry@Phyre@@$03@Phyre@@` |
| 006697A0 | `00669849` `lea` | `00D6A638` | decorated `V?$PArray@VPMeshSegment@PGeometry@Phyre@@$07@Phyre@@` |
| 00669AD0 | `00669B79` `lea` | `00D6A830` | decorated `V?$PArray@VPSkeletonJointBounds@PGeometry@Phyre@@$03@Phyre@@` |
| 00669E00 | `00669EA9` `lea` | `00D6A050` | decorated `V?$PArray@VPSkinBoneRemap@PGeometry@Phyre@@$01@Phyre@@` |
| 0066A130 | `0066A1D9` `lea` | `00D69A68` | decorated `V?$PArray@VPVertexStream@PGeometry@Phyre@@$07@Phyre@@` |
| 0067D810 | `0067D8B9` `lea` | `00D6DAE8` | decorated `V?$PArray@VPBitmapFontCharInfo@PText@Phyre@@$03@Phyre@@` |
| 006AE780 | `006AE829` `lea` | `00D7E1A0` | decorated `V?$PArray@VPTypedObject@Phyre@@$07@Phyre@@` |
| 006BCF80 | `006BD029` `lea` | `00D82480` | decorated `V?$PArray@VPModifierNetworkDynamicMeshSegment@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006BD2B0 | `006BD359` `lea` | `00D82288` | decorated `V?$PArray@VPRenderStream@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006C1920 | `006C19C9` `lea` | `00D83D20` | decorated `V?$PArray@VPShadowSplit@PShadowCaster@PRendering@Phyre@@$07@Phyre@@` |
| 006D2390 | `006D2439` `lea` | `00D8D010` | decorated `V?$PArray@VPModifierAndInputs@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006D26C0 | `006D2769` `lea` | `00D8D208` | decorated `V?$PArray@VPModifierNetworkBuffer@PDynamicGeometry@Phyre@@$07@Phyre@@` |
| 006D29F0 | `006D2A99` `lea` | `00D8CE18` | decorated `V?$PArray@VPRenderStreamInput@PDynamicGeometry@Phyre@@$03@Phyre@@` |

## Per-member rows: the class descriptor each of the PClassDescriptor static teardowns loads (OPUS, 2026-10-03)

The family `PClassDescriptor static teardowns` (frontmatter: 404 members; 311 get a row here) shares one shape, stated here once and not repeated per row: each loads its class descriptor X into rcx, stores a vtable pointer at qword [X] and tail-jumps to the descriptor destructor 00633390. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (every load of it in the body names the same X). Each row anchors the first such `lea`, the member's distinguishing instruction, and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-descriptor-static-teardowns-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-descriptor-static-teardowns-1003/rows.tsv). A member whose loads name more than one X, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-descriptor-static-teardowns-1003/excluded.tsv).

### All 311 members (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 008A8E20 | `008A8E27` `lea` | `02CAD140` | PAnimatableComponent |
| 008A8E40 | `008A8E47` `lea` | `02CAD240` | PAnimationAdditiveBlenderController |
| 008A8E60 | `008A8E67` `lea` | `02CAD340` | PAnimationBlenderController |
| 008A8E80 | `008A8E87` `lea` | `02CAD440` | PAnimationChannel |
| 008A8EA0 | `008A8EA7` `lea` | `02CAD540` | PAnimationChannelBase |
| 008A8EC0 | `008A8EC7` `lea` | `02CAD640` | PAnimationChannelTarget |
| 008A8EE0 | `008A8EE7` `lea` | `02CAD740` | PAnimationChannelTimes |
| 008A8F00 | `008A8F07` `lea` | `02CAD840` | PAnimationClip |
| 008A8F20 | `008A8F27` `lea` | `02CADB40` | PAnimationClipBinding |
| 008A8F40 | `008A8F47` `lea` | `02CAD940` | PAnimationClipBindingChannelMap |
| 008A8F60 | `008A8F67` `lea` | `02CADA40` | PAnimationClipBindingDataBlockCache |
| 008A8F80 | `008A8F87` `lea` | `02CADC50` | PAnimationConstantChannel |
| 008A8FA0 | `008A8FA7` `lea` | `02CADD50` | PAnimationController |
| 008A8FC0 | `008A8FC7` `lea` | `02CADE50` | PAnimationDataSource |
| 008A8FE0 | `008A8FE7` `lea` | `02CAE350` | PAnimationDataSourceListEntry |
| 008A9000 | `008A9007` `lea` | `02CAE050` | PAnimationEvent |
| 008A9020 | `008A9027` `lea` | `02CADF50` | PAnimationEventController |
| 008A9040 | `008A9047` `lea` | `02CAE150` | PAnimationEventList |
| 008A9060 | `008A9067` `lea` | `02CAE250` | PAnimationHierarchyNode |
| 008A9080 | `008A9087` `lea` | `02CAE550` | PAnimationNetworkInstance |
| 008A90A0 | `008A90A7` `lea` | `02CAE450` | PAnimationNetworkInstanceTarget |
| 008A90C0 | `008A90C7` `lea` | `02CAE660` | PAnimationSet |
| 008A90E0 | `008A90E7` `lea` | `02CAE860` | PAnimationSlotArray |
| 008A9100 | `008A9107` `lea` | `02CAEA60` | PAnimationSlotFilter |
| 008A9120 | `008A9127` `lea` | `02CAE960` | PAnimationSlotFilterDeferredLoad |
| 008A9140 | `008A9147` `lea` | `02CAE760` | PAnimationSlotListIndex |
| 008A9160 | `008A9167` `lea` | `02CAEBE0` | PAnimationSpuTargetBlenderController |
| 008A9180 | `008A9187` `lea` | `02CAECE0` | PAnimationTargetBlenderController |
| 008A91A0 | `008A91A7` `lea` | `02CAEDE0` | PAnimationWeightedBlenderController |
| 008A91C0 | `008A91C7` `lea` | `02CAD040` | PBlendableAnimationSource |
| 008A91E0 | `008A91E7` `lea` | `02CAEEE0` | PTimeController |
| 008A9200 | `008A9207` `lea` | `02CAEFE0` | PTimeIntervalController |
| 008A9220 | `008A9227` `lea` | `02CAF0E0` | PTimeScaleOffsetController |
| 008AAE70 | `008AAE77` `lea` | `02CB6480` | PConstantBuffer |
| 008AAE90 | `008AAE97` `lea` | `02CB6380` | PConstantBufferBase |
| 008AAEB0 | `008AAEB7` `lea` | `02CB7BA0` | PContextVariantFoldingTable |
| 008AAED0 | `008AAED7` `lea` | `02CB6580` | PDynamicMeshInstance |
| 008AAEF0 | `008AAEF7` `lea` | `02CB6680` | PEffect |
| 008AAF10 | `008AAF17` `lea` | `02CB6780` | PEffectVariant |
| 008AAF30 | `008AAF37` `lea` | `02CBB400` | PForwardShadowRenderer |
| 008AAF50 | `008AAF57` `lea` | `02CB6980` | PIndirectArgsBuffer |
| 008AAF70 | `008AAF77` `lea` | `02CB6880` | PIndirectArgsBufferBase |
| 008AAF90 | `008AAF97` `lea` | `02CB6B80` | PMaterial |
| 008AAFB0 | `008AAFB7` `lea` | `02CB6A80` | PMaterialSwitch |
| 008AAFD0 | `008AAFD7` `lea` | `02CB6E80` | PMeshInstance |
| 008AAFF0 | `008AAFF7` `lea` | `02CB6F80` | PMeshInstanceAttachPoint |
| 008AB010 | `008AB017` `lea` | `02CB7080` | PMeshInstanceBounds |
| 008AB030 | `008AB037` `lea` | `02CB6D80` | PMeshInstanceSegmentContext |
| 008AB050 | `008AB057` `lea` | `02CB6C80` | PMeshInstanceSegmentStreamBinding |
| 008AB070 | `008AB077` `lea` | `02CB7180` | PModifierNetworkDynamicMeshInstance |
| 008AB090 | `008AB097` `lea` | `02CB7280` | PNodeContext |
| 008AB0B0 | `008AB0B7` `lea` | `02CB7480` | PParameterBuffer |
| 008AB0D0 | `008AB0D7` `lea` | `02CB7380` | PParameterBufferBase |
| 008AB0F0 | `008AB0F7` `lea` | `02CB76A0` | PRenderTarget |
| 008AB110 | `008AB117` `lea` | `02CB75A0` | PRenderTargetBase |
| 008AB130 | `008AB137` `lea` | `02CB78A0` | PSamplerState |
| 008AB150 | `008AB157` `lea` | `02CB77A0` | PSamplerStateBase |
| 008AB170 | `008AB177` `lea` | `02CB79A0` | PSceneRenderPass |
| 008AB190 | `008AB197` `lea` | `02CB7CA0` | PSceneWideParameterBuffer |
| 008AB1B0 | `008AB1B7` `lea` | `02CB9000` | PShader |
| 008AB1D0 | `008AB1D7` `lea` | `02CBB200` | PShaderComputeProgram |
| 008AB1F0 | `008AB1F7` `lea` | `02CBB000` | PShaderFragmentProgram |
| 008AB210 | `008AB217` `lea` | `02CBB100` | PShaderGeometryProgram |
| 008AB230 | `008AB237` `lea` | `02CBA500` | PShaderParameterCaptureBufferByteAddressBuffer |
| 008AB250 | `008AB257` `lea` | `02CBA700` | PShaderParameterCaptureBufferDataBlock |
| 008AB270 | `008AB277` `lea` | `02CBA800` | PShaderParameterCaptureBufferIndexDataBlock |
| 008AB290 | `008AB297` `lea` | `02CB9100` | PShaderParameterCaptureBufferLocation |
| 008AB2B0 | `008AB2B7` `lea` | `02CB9200` | PShaderParameterCaptureBufferLocationSize |
| 008AB2D0 | `008AB2D7` `lea` | `02CB9300` | PShaderParameterCaptureBufferLocationType |
| 008AB2F0 | `008AB2F7` `lea` | `02CB9400` | PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 008AB310 | `008AB317` `lea` | `02CBA600` | PShaderParameterCaptureBufferRWByteAddressBuffer |
| 008AB330 | `008AB337` `lea` | `02CBA400` | PShaderParameterCaptureBufferRWStructuredBuffer |
| 008AB350 | `008AB357` `lea` | `02CBA900` | PShaderParameterCaptureBufferRWTexture2D |
| 008AB370 | `008AB377` `lea` | `02CBAA00` | PShaderParameterCaptureBufferRWTexture3D |
| 008AB390 | `008AB397` `lea` | `02CBA200` | PShaderParameterCaptureBufferSampler |
| 008AB3B0 | `008AB3B7` `lea` | `02CB9C00` | PShaderParameterCaptureBufferStream |
| 008AB3D0 | `008AB3D7` `lea` | `02CBA300` | PShaderParameterCaptureBufferStructuredBuffer |
| 008AB3F0 | `008AB3F7` `lea` | `02CB9F00` | PShaderParameterCaptureBufferTexture2D |
| 008AB410 | `008AB417` `lea` | `02CBA000` | PShaderParameterCaptureBufferTexture3D |
| 008AB430 | `008AB437` `lea` | `02CB9D00` | PShaderParameterCaptureBufferTextureBase |
| 008AB450 | `008AB457` `lea` | `02CBA100` | PShaderParameterCaptureBufferTextureCubeMap |
| 008AB470 | `008AB477` `lea` | `02CB9E00` | PShaderParameterCaptureConstantBuffer |
| 008AB490 | `008AB497` `lea` | `02CB9500` | PShaderParameterDefinition |
| 008AB4B0 | `008AB4B7` `lea` | `02CB9A00` | PShaderPass |
| 008AB4D0 | `008AB4D7` `lea` | `02CB9900` | PShaderPassBase |
| 008AB4F0 | `008AB4F7` `lea` | `02CB7AA0` | PShaderPassInfo |
| 008AB510 | `008AB517` `lea` | `02CB9700` | PShaderPassParameterLocationTypes |
| 008AB530 | `008AB537` `lea` | `02CB9600` | PShaderPassParameterLocationTypesBase |
| 008AB550 | `008AB557` `lea` | `02CB9800` | PShaderPassParameterLocationTypesConstantBuffer |
| 008AB570 | `008AB577` `lea` | `02CB9B00` | PShaderPassStateBase |
| 008AB590 | `008AB597` `lea` | `02CBAD00` | PShaderProgramBase |
| 008AB5B0 | `008AB5B7` `lea` | `02CBAC00` | PShaderProgramParamsAndStreams |
| 008AB5D0 | `008AB5D7` `lea` | `02CBAB00` | PShaderSource |
| 008AB5F0 | `008AB5F7` `lea` | `02CBAE00` | PShaderStreamDefinition |
| 008AB610 | `008AB617` `lea` | `02CBAF00` | PShaderVertexProgram |
| 008AB630 | `008AB637` `lea` | `02CBB300` | PShadowRenderer |
| 008AB650 | `008AB657` `lea` | `02CBB600` | PStructuredBuffer |
| 008AB670 | `008AB677` `lea` | `02CBB500` | PStructuredBufferBase |
| 008AB690 | `008AB697` `lea` | `02CBB900` | PTexture2D |
| 008AB6B0 | `008AB6B7` `lea` | `02CBB800` | PTexture2DBase |
| 008AB6D0 | `008AB6D7` `lea` | `02CBBB00` | PTexture3D |
| 008AB6F0 | `008AB6F7` `lea` | `02CBBA00` | PTexture3DBase |
| 008AB710 | `008AB717` `lea` | `02CBB700` | PTextureCommonBase |
| 008AB730 | `008AB737` `lea` | `02CBBD00` | PTextureCubeMap |
| 008AB750 | `008AB757` `lea` | `02CBBC00` | PTextureCubeMapBase |
| 008AE730 | `008AE737` `lea` | `02CF2440` | PConstantBufferD3D11 |
| 008AE750 | `008AE757` `lea` | `02CF2340` | PIndirectArgsBufferD3D11 |
| 008AE770 | `008AE777` `lea` | `02CF2040` | PRenderTargetD3D11 |
| 008AE790 | `008AE797` `lea` | `02CF2140` | PSamplerStateD3D11 |
| 008AE7B0 | `008AE7B7` `lea` | `02CF1C40` | PShaderComputeProgramD3D11 |
| 008AE7D0 | `008AE7D7` `lea` | `02CF1A40` | PShaderFragmentProgramD3D11 |
| 008AE7F0 | `008AE7F7` `lea` | `02CF1B40` | PShaderGeometryProgramD3D11 |
| 008AE810 | `008AE817` `lea` | `02CF1440` | PShaderPassD3D11 |
| 008AE830 | `008AE837` `lea` | `02CF1540` | PShaderPassStateD3D11 |
| 008AE850 | `008AE857` `lea` | `02CF1840` | PShaderProgramD3D11 |
| 008AE870 | `008AE877` `lea` | `02CF1940` | PShaderVertexProgramD3D11 |
| 008AE890 | `008AE897` `lea` | `02CF1640` | PStreamInputDescD3D11 |
| 008AE8B0 | `008AE8B7` `lea` | `02CF1740` | PStreamInputLayoutD3D11 |
| 008AE8D0 | `008AE8D7` `lea` | `02CF2240` | PStructuredBufferD3D11 |
| 008AE8F0 | `008AE8F7` `lea` | `02CF1D40` | PTexture2DD3D11 |
| 008AE910 | `008AE917` `lea` | `02CF1E40` | PTexture3DD3D11 |
| 008AE930 | `008AE937` `lea` | `02CF1F40` | PTextureCubeMapD3D11 |
| 008AFEF0 | `008AFEF7` `lea` | `02D368A0` | PAtmospherics |
| 008AFF10 | `008AFF17` `lea` | `02D367A0` | PAtmosphericsBase |
| 008AFF30 | `008AFF37` `lea` | `02D369A0` | PAtmosphericsD3D11 |
| 008AFF50 | `008AFF57` `lea` | `02D362A0` | PCelShading |
| 008AFF70 | `008AFF77` `lea` | `02D361A0` | PCelShadingBase |
| 008AFF90 | `008AFF97` `lea` | `02D363A0` | PCelShadingD3D11 |
| 008AFFB0 | `008AFFB7` `lea` | `02D34940` | PDeferredLighting |
| 008AFFD0 | `008AFFD7` `lea` | `02D34840` | PDeferredLightingBase |
| 008AFFF0 | `008AFFF7` `lea` | `02D34A40` | PDeferredLightingD3D11 |
| 008B0010 | `008B0017` `lea` | `02D34C40` | PDepthOfField |
| 008B0030 | `008B0037` `lea` | `02D34B40` | PDepthOfFieldBase |
| 008B0050 | `008B0057` `lea` | `02D34D40` | PDepthOfFieldD3D11 |
| 008B0070 | `008B0077` `lea` | `02D35FA0` | PFXAA |
| 008B0090 | `008B0097` `lea` | `02D35EA0` | PFXAABase |
| 008B00B0 | `008B00B7` `lea` | `02D360A0` | PFXAAD3D11 |
| 008B00D0 | `008B00D7` `lea` | `02D35CA0` | PGlow |
| 008B00F0 | `008B00F7` `lea` | `02D35AA0` | PGlowBase |
| 008B0110 | `008B0117` `lea` | `02D35DA0` | PGlowD3D11 |
| 008B0130 | `008B0137` `lea` | `02D35BA0` | PGlowGPUBase |
| 008B0150 | `008B0157` `lea` | `02D36AA0` | PLowResParticles |
| 008B0170 | `008B0177` `lea` | `02D357A0` | PMLAA |
| 008B0190 | `008B0197` `lea` | `02D356A0` | PMLAABase |
| 008B01B0 | `008B01B7` `lea` | `02D358A0` | PMLAAD3D11 |
| 008B01D0 | `008B01D7` `lea` | `02D36BA0` | PMaterialPostEffect |
| 008B01F0 | `008B01F7` `lea` | `02D359A0` | PMeshParticleSystemBase |
| 008B0210 | `008B0217` `lea` | `02D34F40` | PMotionBlur |
| 008B0230 | `008B0237` `lea` | `02D34E40` | PMotionBlurBase |
| 008B0250 | `008B0257` `lea` | `02D35040` | PMotionBlurD3D11 |
| 008B0270 | `008B0277` `lea` | `02D34740` | PPostEffectBase |
| 008B0290 | `008B0297` `lea` | `02D36CA0` | PPostEffectManager |
| 008B02B0 | `008B02B7` `lea` | `02D35400` | PScreenSpaceAmbientOcclusion |
| 008B02D0 | `008B02D7` `lea` | `02D35300` | PScreenSpaceAmbientOcclusionBase |
| 008B02F0 | `008B02F7` `lea` | `02D35500` | PScreenSpaceAmbientOcclusionD3D11 |
| 008B0310 | `008B0317` `lea` | `02D365A0` | PScreenSpaceReflection |
| 008B0330 | `008B0337` `lea` | `02D364A0` | PScreenSpaceReflectionBase |
| 008B0350 | `008B0357` `lea` | `02D366A0` | PScreenSpaceReflectionD3D11 |
| 008B0BA0 | `008B0BA7` `lea` | `02D39E40` | PDataBlock |
| 008B0BC0 | `008B0BC7` `lea` | `02D39D40` | PDataBlockBase |
| 008B0BE0 | `008B0BE7` `lea` | `02D39B40` | PDataBlockBufferD3D11 |
| 008B0C00 | `008B0C07` `lea` | `02D39C40` | PDataBlockD3D11 |
| 008B0C20 | `008B0C27` `lea` | `02D39F40` | PDynamicDataBlock |
| 008B0C40 | `008B0C47` `lea` | `02D3A140` | PDynamicMesh |
| 008B0C60 | `008B0C67` `lea` | `02D3A040` | PDynamicSegmentDesc |
| 008B0C80 | `008B0C87` `lea` | `02D3A340` | PIndexDataBlock |
| 008B0CA0 | `008B0CA7` `lea` | `02D3A240` | PIndexDataBlockBase |
| 008B0CC0 | `008B0CC7` `lea` | `02D39940` | PIndexDataBlockBufferD3D11 |
| 008B0CE0 | `008B0CE7` `lea` | `02D39A40` | PIndexDataBlockD3D11 |
| 008B0D00 | `008B0D07` `lea` | `02D3A440` | PMaterialSet |
| 008B0D20 | `008B0D27` `lea` | `02D3A640` | PMesh |
| 008B0D40 | `008B0D47` `lea` | `02D3A940` | PMeshSegment |
| 008B0D60 | `008B0D67` `lea` | `02D3A840` | PMeshSegmentBase |
| 008B0D80 | `008B0D87` `lea` | `02D39840` | PMeshSegmentD3D11 |
| 008B0DA0 | `008B0DA7` `lea` | `02D3ACE0` | PShape |
| 008B0DC0 | `008B0DC7` `lea` | `02D3A540` | PSkeletonJointBounds |
| 008B0DE0 | `008B0DE7` `lea` | `02D3A740` | PSkinBoneRemap |
| 008B0E00 | `008B0E07` `lea` | `02D3ADE0` | PVertexStream |
| 008B1AC0 | `008B1AC7` `lea` | `02D3E680` | PAssetReference |
| 008B1AE0 | `008B1AE7` `lea` | `02D3E780` | PAssetReferenceImport |
| 008B1DB0 | `008B1DB7` `lea` | `02D3F210` | PCamera |
| 008B1DD0 | `008B1DD7` `lea` | `02D3F310` | PCameraProjection |
| 008B1F80 | `008B1F87` `lea` | `02E3FA60` | PBitmapFont |
| 008B1FA0 | `008B1FA7` `lea` | `02E3F960` | PBitmapFontCharInfo |
| 008B2110 | `008B2117` `lea` | `02E404B0` | PWorldMatrix |
| 008B22C0 | `008B22C7` `lea` | `02E41270` | PAsyncProcessHeader |
| 008B22E0 | `008B22E7` `lea` | `02E41070` | PClassCallableMethodScript |
| 008B2300 | `008B2307` `lea` | `02E41370` | PScheduler |
| 008B2320 | `008B2327` `lea` | `02E41470` | PScript |
| 008B2340 | `008B2347` `lea` | `02E41170` | PScriptCallbackHandler |
| 008B26D0 | `008B26D7` `lea` | `02E479D0` | PPhysicsBox |
| 008B26F0 | `008B26F7` `lea` | `02E478D0` | PPhysicsBoxBase |
| 008B2710 | `008B2717` `lea` | `02E496D0` | PPhysicsBoxBullet |
| 008B2730 | `008B2737` `lea` | `02E48AD0` | PPhysicsCallbackData |
| 008B2750 | `008B2757` `lea` | `02E47BD0` | PPhysicsCapsule |
| 008B2770 | `008B2777` `lea` | `02E47AD0` | PPhysicsCapsuleBase |
| 008B2790 | `008B2797` `lea` | `02E497D0` | PPhysicsCapsuleBullet |
| 008B27B0 | `008B27B7` `lea` | `02E47CD0` | PPhysicsCharacterCamera |
| 008B27D0 | `008B27D7` `lea` | `02E47ED0` | PPhysicsCharacterController |
| 008B27F0 | `008B27F7` `lea` | `02E47DD0` | PPhysicsCharacterControllerBase |
| 008B2810 | `008B2817` `lea` | `02E49FD0` | PPhysicsCharacterControllerBullet |
| 008B2830 | `008B2837` `lea` | `02E480D0` | PPhysicsCylinder |
| 008B2850 | `008B2857` `lea` | `02E47FD0` | PPhysicsCylinderBase |
| 008B2870 | `008B2877` `lea` | `02E498D0` | PPhysicsCylinderBullet |
| 008B2890 | `008B2897` `lea` | `02E482D0` | PPhysicsInterface |
| 008B28B0 | `008B28B7` `lea` | `02E481D0` | PPhysicsInterfaceBase |
| 008B28D0 | `008B28D7` `lea` | `02E49ED0` | PPhysicsInterfaceBullet |
| 008B28F0 | `008B28F7` `lea` | `02E483D0` | PPhysicsMaterial |
| 008B2910 | `008B2917` `lea` | `02E485D0` | PPhysicsMesh |
| 008B2930 | `008B2937` `lea` | `02E484D0` | PPhysicsMeshBase |
| 008B2950 | `008B2957` `lea` | `02E499D0` | PPhysicsMeshBullet |
| 008B2970 | `008B2977` `lea` | `02E486D0` | PPhysicsModel |
| 008B2990 | `008B2997` `lea` | `02E488D0` | PPhysicsPlane |
| 008B29B0 | `008B29B7` `lea` | `02E487D0` | PPhysicsPlaneBase |
| 008B29D0 | `008B29D7` `lea` | `02E49AD0` | PPhysicsPlaneBullet |
| 008B29F0 | `008B29F7` `lea` | `02E48BD0` | PPhysicsRigidBody |
| 008B2A10 | `008B2A17` `lea` | `02E489D0` | PPhysicsRigidBodyBase |
| 008B2A30 | `008B2A37` `lea` | `02E49CD0` | PPhysicsRigidBodyBullet |
| 008B2A50 | `008B2A57` `lea` | `02E48DD0` | PPhysicsShape |
| 008B2A70 | `008B2A77` `lea` | `02E48CD0` | PPhysicsShapeBase |
| 008B2A90 | `008B2A97` `lea` | `02E495D0` | PPhysicsShapeBullet |
| 008B2AB0 | `008B2AB7` `lea` | `02E48FD0` | PPhysicsSphere |
| 008B2AD0 | `008B2AD7` `lea` | `02E48ED0` | PPhysicsSphereBase |
| 008B2AF0 | `008B2AF7` `lea` | `02E49BD0` | PPhysicsSphereBullet |
| 008B2B10 | `008B2B17` `lea` | `02E490D0` | PPhysicsTaperedCapsule |
| 008B2B30 | `008B2B37` `lea` | `02E491D0` | PPhysicsTaperedCylinder |
| 008B2B50 | `008B2B57` `lea` | `02E494D0` | PPhysicsWorld |
| 008B2B70 | `008B2B77` `lea` | `02E492D0` | PPhysicsWorldBase |
| 008B2B90 | `008B2B97` `lea` | `02E49DD0` | PPhysicsWorldBullet |
| 008B2BB0 | `008B2BB7` `lea` | `02E493D0` | PRaycastResult |
| 008B3E90 | `008B3E97` `lea` | `02E4D630` | PString |
| 008B3F20 | `008B3F27` `lea` | `02E4D940` | PTrigger |
| 008B4160 | `008B4167` `lea` | `02E4E1E0` | PQuarryComponent |
| 008B41B0 | `008B41B7` `lea` | `02E4E430` | PTypedObject |
| 008B4200 | `008B4207` `lea` | `02E4E720` | PComponent |
| 008B4310 | `008B4317` `lea` | `02E4EAF0` | PEntity |
| 008B4620 | `008B4627` `lea` | `02E4F290` | PCameraOrthographic |
| 008B46B0 | `008B46B7` `lea` | `02E4F710` | PCameraPerspective |
| 008B46E0 | `008B46E7` `lea` | `02E4F900` | PInstancesComponent |
| 008B48E0 | `008B48E7` `lea` | `02E4FF60` | PNameComponent |
| 008B4970 | `008B4977` `lea` | `02E50160` | PRandomGenerator |
| 008B5200 | `008B5207` `lea` | `02E518D0` | PNode |
| 008B5800 | `008B5807` `lea` | `02E522F0` | PMeshSegmentContext |
| 008B5CF0 | `008B5CF7` `lea` | `02E58060` | PModifierNetworkDynamicMesh |
| 008B5D10 | `008B5D17` `lea` | `02E57F60` | PModifierNetworkDynamicMeshSegment |
| 008B5EA0 | `008B5EA7` `lea` | `02E58DB0` | PLight |
| 008B65B0 | `008B65B7` `lea` | `02E59DC0` | PShadowCaster |
| 008B65D0 | `008B65D7` `lea` | `02E59CC0` | PShadowSplit |
| 008B6920 | `008B6927` `lea` | `02E5A6C0` | PModifierNetworkInstance |
| 008B6940 | `008B6947` `lea` | `02E5A4C0` | PModifierNetworkInstanceInput |
| 008B6960 | `008B6967` `lea` | `02E5A5C0` | PModifierNetworkInstancePacketInput |
| 008B6B00 | `008B6B07` `lea` | `02E5AE00` | PLODGroup |
| 008B6B20 | `008B6B27` `lea` | `02E5AD00` | PLODLevel |
| 008B6D60 | `008B6D67` `lea` | `02E5BBB0` | POccluderGeometryInstance |
| 008B6F60 | `008B6F67` `lea` | `02E5C050` | PScriptableComponent |
| 008B7020 | `008B7027` `lea` | `02E5C370` | PTriggerReceiverTypeCallbackData |
| 008B7080 | `008B7087` `lea` | `02E5C710` | PTriggerReceiverComponent |
| 008B70F0 | `008B70F7` `lea` | `02E5E030` | PModifierAndInputs |
| 008B7110 | `008B7117` `lea` | `02E5E540` | PModifierNetwork |
| 008B7130 | `008B7137` `lea` | `02E5DF30` | PModifierNetworkBuffer |
| 008B7150 | `008B7157` `lea` | `02E5E430` | PModifierNetworkInfoPacket |
| 008B7170 | `008B7177` `lea` | `02E5E330` | PModifierNetworkInfoPacket_Buffer |
| 008B7190 | `008B7197` `lea` | `02E5E130` | PModifierNetworkInfoPacket_ModifierCode |
| 008B71B0 | `008B71B7` `lea` | `02E5E230` | PModifierNetworkInfoPacket_ModifierInstance |
| 008B71D0 | `008B71D7` `lea` | `02E5DE30` | PRenderStream |
| 008B71F0 | `008B71F7` `lea` | `02E5DD30` | PRenderStreamInput |
| 008B75F0 | `008B75F7` `lea` | `02E9FDF0` | PMorphModifierWeightsUserDataObject |
| 008B78B0 | `008B78B7` `lea` | `02EA0850` | POccluderGeometryObject |
| 008B79B0 | `008B79B7` `lea` | `02EA5660` | PApplication |
| 008B79D0 | `008B79D7` `lea` | `02EA5380` | PApplicationViewport |
| 008B79F0 | `008B79F7` `lea` | `02EA9400` | PDebugUtils |
| 008B7A10 | `008B7A17` `lea` | `02EA5560` | PInputMapper |
| 008B91E0 | `008B91E7` `lea` | `02EB6CF0` | PInputAction |
| 008B9200 | `008B9207` `lea` | `02EB6DF0` | PInputMap |
| 008B9220 | `008B9227` `lea` | `02EB52F0` | PInputSource |
| 008B9240 | `008B9247` `lea` | `02EB55F0` | PInputSourceJoypadAxis |
| 008B9260 | `008B9267` `lea` | `02EB54F0` | PInputSourceJoypadButton |
| 008B9280 | `008B9287` `lea` | `02EB53F0` | PInputSourceKey |
| 008B92A0 | `008B92A7` `lea` | `02EB63F0` | PInputSourceMotionAngularVelocityX |
| 008B92C0 | `008B92C7` `lea` | `02EB64F0` | PInputSourceMotionAngularVelocityY |
| 008B92E0 | `008B92E7` `lea` | `02EB65F0` | PInputSourceMotionAngularVelocityZ |
| 008B9300 | `008B9307` `lea` | `02EB66F0` | PInputSourceMotionLinearAccelerationX |
| 008B9320 | `008B9327` `lea` | `02EB67F0` | PInputSourceMotionLinearAccelerationY |
| 008B9340 | `008B9347` `lea` | `02EB68F0` | PInputSourceMotionLinearAccelerationZ |
| 008B9360 | `008B9367` `lea` | `02EB62F0` | PInputSourceMotionQuatW |
| 008B9380 | `008B9387` `lea` | `02EB5FF0` | PInputSourceMotionQuatX |
| 008B93A0 | `008B93A7` `lea` | `02EB60F0` | PInputSourceMotionQuatY |
| 008B93C0 | `008B93C7` `lea` | `02EB61F0` | PInputSourceMotionQuatZ |
| 008B93E0 | `008B93E7` `lea` | `02EB56F0` | PInputSourceMouseButton |
| 008B9400 | `008B9407` `lea` | `02EB57F0` | PInputSourceMouseDeltaX |
| 008B9420 | `008B9427` `lea` | `02EB58F0` | PInputSourceMouseDeltaY |
| 008B9440 | `008B9447` `lea` | `02EB5BF0` | PInputSourceTouchDragX |
| 008B9460 | `008B9467` `lea` | `02EB5CF0` | PInputSourceTouchDragY |
| 008B9480 | `008B9487` `lea` | `02EB5AF0` | PInputSourceTouchPinch |
| 008B94A0 | `008B94A7` `lea` | `02EB59F0` | PInputSourceTouchRotate |
| 008B94C0 | `008B94C7` `lea` | `02EB5DF0` | PInputSourceTouchTwoFingerDragX |
| 008B94E0 | `008B94E7` `lea` | `02EB5EF0` | PInputSourceTouchTwoFingerDragY |
| 008B9500 | `008B9507` `lea` | `02EB69F0` | PInputSourceVisionTrackerX |
| 008B9520 | `008B9527` `lea` | `02EB6AF0` | PInputSourceVisionTrackerY |
| 008B9540 | `008B9547` `lea` | `02EB6BF0` | PInputSourceVisionTrackerZ |
| 008B97D0 | `008B97D7` `lea` | `02EB7CD0` | PVisionMoveTracker |
| 008B97F0 | `008B97F7` `lea` | `02EB7BD0` | PVisionMoveTrackerBase |
| 008B9810 | `008B9817` `lea` | `02EB7DD0` | PVisionMoveTrackerWin32 |
| 008B9830 | `008B9837` `lea` | `02EB8060` | PVisionTracker |
| 008B9850 | `008B9857` `lea` | `02EB7F60` | PVisionTrackerBase |
| 008B9870 | `008B9877` `lea` | `02EB8160` | PVisionTrackerWin32 |
| 008BDD20 | `008BDD27` `lea` | `02EB9070` | POctree |
| 008BDD40 | `008BDD47` `lea` | `02EB9370` | POctreeChildren |
| 008BDD60 | `008BDD67` `lea` | `02EB9170` | POctreeData |
| 008BDD80 | `008BDD87` `lea` | `02EB9270` | POctreeWorld |
| 008C14E0 | `008C14E7` `lea` | `02EB9E60` | PGameConfig |

## Per-member rows: the class name and size each AbstractClassDescriptor constructor registers (OPUS, 2026-10-03)

The family `AbstractClassDescriptor constructors` (frontmatter: 178 members; 178 get a row here) shares one form, not repeated per row: it calls the context getter `006373D0`, passes its result to the shared descriptor constructor `00632D80` with the class name in `r8`, the instance size in `r9d` and a descriptor pointer as a stack argument, stores the concrete vtable at qword `+0`, sets bit `0x2` of dword `+0xFC`, and calls the three member-registration helpers `0063DC80`, `0063DF90` and `0063DFA0` (all 178 members make exactly these five calls, in this order). What differs from member to member is the name and size it passes. Each row anchors the `lea r8, [S]` before the `00632D80` call (the member's distinguishing instruction) and states S, the class-name string at S, and the immediate size from `mov r9d`. All are read from the certified image. [`fam_rows.py`](../../_index/candidates/opus-ee-abstract-descriptor-ctors-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-abstract-descriptor-ctors-1003/rows.tsv). A body without exactly one `00632D80` call, a name that is not a clean string, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-abstract-descriptor-ctors-1003/excluded.tsv).

### All 178 constructors (OPUS)

| member | distinguishing instruction | name string S | class name and instance size passed |
|---|---|---|---|
| 00597690 | `005976D0` `lea` | `00D24880` | "PClusterHeader", size 0x54 |
| 005977E0 | `00597820` `lea` | `00D246D0` | "PClusterHeaderD3D11", size 0x54 |
| 005A7ED0 | `005A7F10` `lea` | `00D29808` | "PAnimatableComponent", size 0x108 |
| 005A7F70 | `005A7FB0` `lea` | `00D2C308` | "PAnimationAdditiveBlenderController", size 0x38 |
| 005A8010 | `005A8050` `lea` | `00D2AE98` | "PAnimationBlenderController", size 0x28 |
| 005A80B0 | `005A80F0` `lea` | `00D29780` | "PAnimationChannel", size 0x68 |
| 005A8150 | `005A8190` `lea` | `00D28E80` | "PAnimationChannelBase", size 0x48 |
| 005A8610 | `005A8650` `lea` | `00D2A240` | "PAnimationConstantChannel", size 0x58 |
| 005A86B0 | `005A86F0` `lea` | `00D27E68` | "PAnimationController", size 0x28 |
| 005A8750 | `005A8790` `lea` | `00D2BE80` | "PAnimationDataSource", size 0x18 |
| 005A8950 | `005A8990` `lea` | `00D2C958` | "PAnimationEventController", size 0x28 |
| 005A8E10 | `005A8E50` `lea` | `00D29B28` | "PAnimationSlotFilter", size 0x40 |
| 005A9010 | `005A9050` `lea` | `00D2CCB0` | "PAnimationSpuTargetBlenderController", size 0x20 |
| 005A90B0 | `005A90F0` `lea` | `00D28480` | "PAnimationTargetBlenderController", size 0x20 |
| 005A9150 | `005A9190` `lea` | `00D2B6C0` | "PAnimationWeightedBlenderController", size 0x38 |
| 005A92A0 | `005A92E0` `lea` | `00D28A60` | "PTimeController", size 0x10 |
| 005A9340 | `005A9380` `lea` | `00D29670` | "PTimeIntervalController", size 0x28 |
| 005A93E0 | `005A9420` `lea` | `00D2A010` | "PTimeScaleOffsetController", size 0x20 |
| 005D8F20 | `005D8F60` `lea` | `00D3B118` | "PConstantBuffer", size 0x50 |
| 005D9330 | `005D9370` `lea` | `00D3FA08` | "PForwardShadowRenderer", size 0x10 |
| 005D93D0 | `005D9410` `lea` | `00D42108` | "PIndirectArgsBuffer", size 0x28 |
| 005D99E0 | `005D9A20` `lea` | `00D36400` | "PModifierNetworkDynamicMeshInstance", size 0x28 |
| 005D9B30 | `005D9B70` `lea` | `00D3A9A8` | "PParameterBuffer", size 0x20 |
| 005D9C80 | `005D9CC0` `lea` | `00D3D138` | "PRenderTarget", size 0x50 |
| 005D9DD0 | `005D9E10` `lea` | `00D36620` | "PSamplerState", size 0x28 |
| 005D9FD0 | `005DA010` `lea` | `00D41648` | "PSceneWideParameterBuffer", size 0x8 |
| 005DA120 | `005DA160` `lea` | `00D41290` | "PShaderComputeProgram", size 0x90 |
| 005DA1C0 | `005DA200` `lea` | `00D3E110` | "PShaderFragmentProgram", size 0x80 |
| 005DA260 | `005DA2A0` `lea` | `00D3FD58` | "PShaderGeometryProgram", size 0x80 |
| 005DA300 | `005DA340` `lea` | `00D3CA48` | "PShaderParameterCaptureBufferByteAddressBuffer", size 0x20 |
| 005DA3A0 | `005DA3E0` `lea` | `00D40CA0` | "PShaderParameterCaptureBufferDataBlock", size 0x18 |
| 005DA440 | `005DA480` `lea` | `00D41CC0` | "PShaderParameterCaptureBufferIndexDataBlock", size 0x18 |
| 005DA590 | `005DA5D0` `lea` | `00D3F480` | "PShaderParameterCaptureBufferLocationSize", size 0x4 |
| 005DA630 | `005DA670` `lea` | `00D40D50` | "PShaderParameterCaptureBufferLocationType", size 0x4 |
| 005DA6D0 | `005DA710` `lea` | `00D41D20` | "PShaderParameterCaptureBufferLocationTypeConstantBuffer", size 0x10 |
| 005DA770 | `005DA7B0` `lea` | `00D3DAD0` | "PShaderParameterCaptureBufferRWByteAddressBuffer", size 0x28 |
| 005DA810 | `005DA850` `lea` | `00D3B2C0` | "PShaderParameterCaptureBufferRWStructuredBuffer", size 0x20 |
| 005DA8B0 | `005DA8F0` `lea` | `00D42B60` | "PShaderParameterCaptureBufferRWTexture2D", size 0x18 |
| 005DA950 | `005DA990` `lea` | `00D37010` | "PShaderParameterCaptureBufferRWTexture3D", size 0x18 |
| 005DA9F0 | `005DAA30` `lea` | `00D38BE8` | "PShaderParameterCaptureBufferSampler", size 0x18 |
| 005DAB40 | `005DAB80` `lea` | `00D3A050` | "PShaderParameterCaptureBufferStructuredBuffer", size 0x20 |
| 005DABE0 | `005DAC20` `lea` | `00D3E7E8` | "PShaderParameterCaptureBufferTexture2D", size 0x18 |
| 005DAC80 | `005DACC0` `lea` | `00D406A0` | "PShaderParameterCaptureBufferTexture3D", size 0x18 |
| 005DADD0 | `005DAE10` `lea` | `00D418E8` | "PShaderParameterCaptureBufferTextureCubeMap", size 0x18 |
| 005DAE70 | `005DAEB0` `lea` | `00D3F3D0` | "PShaderParameterCaptureConstantBuffer", size 0x18 |
| 005DAFC0 | `005DB000` `lea` | `00D3A998` | "PShaderPass", size 0x2C0 |
| 005DB1C0 | `005DB200` `lea` | `00D39388` | "PShaderPassParameterLocationTypes", size 0x20 |
| 005DB310 | `005DB350` `lea` | `00D3B908` | "PShaderPassParameterLocationTypesConstantBuffer", size 0x20 |
| 005DB720 | `005DB760` `lea` | `00D3CFA0` | "PShaderVertexProgram", size 0x98 |
| 005DB870 | `005DB8B0` `lea` | `00D3D8F8` | "PStructuredBuffer", size 0x68 |
| 005DB9C0 | `005DBA00` `lea` | `00D3D1D0` | "PTexture2D", size 0x188 |
| 005DBA60 | `005DBAA0` `lea` | `00D36CD0` | "PTexture2DBase", size 0x30 |
| 005DBB00 | `005DBB40` `lea` | `00D383E0` | "PTexture3D", size 0x90 |
| 005DBBA0 | `005DBBE0` `lea` | `00D3F9F8` | "PTexture3DBase", size 0x38 |
| 005DBCF0 | `005DBD30` `lea` | `00D40A68` | "PTextureCubeMap", size 0x350 |
| 005DBD90 | `005DBDD0` `lea` | `00D3A870` | "PTextureCubeMapBase", size 0x30 |
| 00614A90 | `00614AD0` `lea` | `00D50E10` | "PConstantBufferD3D11", size 0x50 |
| 00614B30 | `00614B70` `lea` | `00D52198` | "PIndirectArgsBufferD3D11", size 0x28 |
| 00614BD0 | `00614C10` `lea` | `00D512B8` | "PRenderTargetD3D11", size 0x50 |
| 00614C70 | `00614CB0` `lea` | `00D525B8` | "PSamplerStateD3D11", size 0x28 |
| 00614D10 | `00614D50` `lea` | `00D51210` | "PShaderComputeProgramD3D11", size 0x90 |
| 00614DB0 | `00614DF0` `lea` | `00D50970` | "PShaderFragmentProgramD3D11", size 0x80 |
| 00614E50 | `00614E90` `lea` | `00D50F38` | "PShaderGeometryProgramD3D11", size 0x80 |
| 00614EF0 | `00614F30` `lea` | `00D50A70` | "PShaderPassD3D11", size 0x2C0 |
| 00614F90 | `00614FD0` `lea` | `00D50210` | "PShaderPassStateD3D11", size 0x190 |
| 00615030 | `00615070` `lea` | `00D525A0` | "PShaderProgramD3D11", size 0x78 |
| 006150D0 | `00615110` `lea` | `00D50228` | "PShaderVertexProgramD3D11", size 0x98 |
| 006152D0 | `00615310` `lea` | `00D51358` | "PStructuredBufferD3D11", size 0x68 |
| 00615370 | `006153B0` `lea` | `00D51200` | "PTexture2DD3D11", size 0x188 |
| 00615410 | `00615450` `lea` | `00D50200` | "PTexture3DD3D11", size 0x90 |
| 006154B0 | `006154F0` `lea` | `00D51C28` | "PTextureCubeMapD3D11", size 0x350 |
| 00643E80 | `00643EC0` `lea` | `00D5A7E8` | "PAtmospherics", size 0x288 |
| 00643F20 | `00643F60` `lea` | `00D5EED0` | "PAtmosphericsBase", size 0x288 |
| 00643FC0 | `00644000` `lea` | `00D596A8` | "PAtmosphericsD3D11", size 0x288 |
| 00644060 | `006440A0` `lea` | `00D5D818` | "PCelShading", size 0xC0 |
| 00644100 | `00644140` `lea` | `00D5C2E8` | "PCelShadingBase", size 0xC0 |
| 006441A0 | `006441E0` `lea` | `00D5CED8` | "PCelShadingD3D11", size 0xC0 |
| 00644380 | `006443C0` `lea` | `00D5BB90` | "PDeferredLightingD3D11", size 0x4330 |
| 00644420 | `00644460` `lea` | `00D595E0` | "PDepthOfField", size 0xD0 |
| 006444C0 | `00644500` `lea` | `00D5D760` | "PDepthOfFieldBase", size 0x80 |
| 00644560 | `006445A0` `lea` | `00D5EA40` | "PDepthOfFieldD3D11", size 0xD0 |
| 00644600 | `00644640` `lea` | `00D5EC80` | "PFXAA", size 0x70 |
| 006446A0 | `006446E0` `lea` | `00D5D6D0` | "PFXAABase", size 0x70 |
| 00644740 | `00644780` `lea` | `00D5E228` | "PFXAAD3D11", size 0x70 |
| 006447E0 | `00644820` `lea` | `00D5CBC8` | "PGlow", size 0xD8 |
| 00644880 | `006448C0` `lea` | `00D5A378` | "PGlowBase", size 0xA0 |
| 00644920 | `00644960` `lea` | `00D5BD20` | "PGlowD3D11", size 0xD8 |
| 006449C0 | `00644A00` `lea` | `00D5B250` | "PGlowGPUBase", size 0xD8 |
| 00644B00 | `00644B40` `lea` | `00D5B644` | "PMLAA", size 0xB0 |
| 00644BA0 | `00644BE0` `lea` | `00D598D0` | "PMLAABase", size 0xB0 |
| 00644C40 | `00644C80` `lea` | `00D5A908` | "PMLAAD3D11", size 0xB0 |
| 00644CE0 | `00644D20` `lea` | `00D5C2D0` | "PMaterialPostEffect", size 0x68 |
| 00644D80 | `00644DC0` `lea` | `00D5E210` | "PMeshParticleSystemBase", size 0x3248 |
| 00644E20 | `00644E60` `lea` | `00D5AB80` | "PMotionBlur", size 0xD70 |
| 00644EC0 | `00644F00` `lea` | `00D5EDB0` | "PMotionBlurBase", size 0xD68 |
| 00644F60 | `00644FA0` `lea` | `00D597A8` | "PMotionBlurD3D11", size 0xD70 |
| 00645160 | `006451A0` `lea` | `00D5D100` | "PScreenSpaceAmbientOcclusion", size 0x68 |
| 00645200 | `00645240` `lea` | `00D5B7C8` | "PScreenSpaceAmbientOcclusionBase", size 0x68 |
| 006452A0 | `006452E0` `lea` | `00D5C4E8` | "PScreenSpaceAmbientOcclusionD3D11", size 0x68 |
| 00645340 | `00645380` `lea` | `00D5B540` | "PScreenSpaceReflection", size 0xB0 |
| 006453E0 | `00645420` `lea` | `00D59760` | "PScreenSpaceReflectionBase", size 0xB0 |
| 00645480 | `006454C0` `lea` | `00D5A568` | "PScreenSpaceReflectionD3D11", size 0xB0 |
| 00661B30 | `00661B70` `lea` | `00D66290` | "PDataBlock", size 0x88 |
| 00661D30 | `00661D70` `lea` | `00D65628` | "PDataBlockD3D11", size 0x88 |
| 00661FE0 | `00662020` `lea` | `00D65EC8` | "PIndexDataBlock", size 0x80 |
| 006621E0 | `00662220` `lea` | `00D654F0` | "PIndexDataBlockD3D11", size 0x80 |
| 006623E0 | `00662420` `lea` | `00D651C8` | "PMeshSegment", size 0xC0 |
| 00662530 | `00662570` `lea` | `00D648A8` | "PMeshSegmentD3D11", size 0xC0 |
| 00678420 | `00678460` `lea` | `00D6C868` | "PCameraProjection", size 0xD0 |
| 006812B0 | `006812F0` `lea` | `00D6EAC0` | "PClassCallableMethodScript", size 0x68 |
| 0068F250 | `0068F290` `lea` | `00D75610` | "PPhysicsBox", size 0x88 |
| 0068F2F0 | `0068F330` `lea` | `00D74598` | "PPhysicsBoxBase", size 0x80 |
| 0068F390 | `0068F3D0` `lea` | `00D74E68` | "PPhysicsBoxBullet", size 0x88 |
| 0068F4E0 | `0068F520` `lea` | `00D75620` | "PPhysicsCapsule", size 0x90 |
| 0068F580 | `0068F5C0` `lea` | `00D745A8` | "PPhysicsCapsuleBase", size 0x88 |
| 0068F620 | `0068F660` `lea` | `00D74E80` | "PPhysicsCapsuleBullet", size 0x90 |
| 0068F770 | `0068F7B0` `lea` | `00D71448` | "PPhysicsCharacterController", size 0x190 |
| 0068F8C0 | `0068F900` `lea` | `00D70528` | "PPhysicsCharacterControllerBullet", size 0x190 |
| 0068F960 | `0068F9A0` `lea` | `00D73D48` | "PPhysicsCylinder", size 0x88 |
| 0068FA00 | `0068FA40` `lea` | `00D72588` | "PPhysicsCylinderBase", size 0x80 |
| 0068FAA0 | `0068FAE0` `lea` | `00D73260` | "PPhysicsCylinderBullet", size 0x88 |
| 0068FB40 | `0068FB80` `lea` | `00D73248` | "PPhysicsInterface", size 0xA0 |
| 0068FC90 | `0068FCD0` `lea` | `00D72628` | "PPhysicsInterfaceBullet", size 0xA0 |
| 0068FDE0 | `0068FE20` `lea` | `00D717F0` | "PPhysicsMesh", size 0x90 |
| 0068FE80 | `0068FEC0` `lea` | `00D76238` | "PPhysicsMeshBase", size 0x78 |
| 0068FF20 | `0068FF60` `lea` | `00D70A90` | "PPhysicsMeshBullet", size 0x90 |
| 00690070 | `006900B0` `lea` | `00D73278` | "PPhysicsPlane", size 0x88 |
| 00690110 | `00690150` `lea` | `00D71868` | "PPhysicsPlaneBase", size 0x80 |
| 006901B0 | `006901F0` `lea` | `00D72640` | "PPhysicsPlaneBullet", size 0x88 |
| 00690250 | `00690290` `lea` | `00D730F8` | "PPhysicsRigidBody", size 0x128 |
| 006903A0 | `006903E0` `lea` | `00D72200` | "PPhysicsRigidBodyBullet", size 0x128 |
| 00690440 | `00690480` `lea` | `00D71758` | "PPhysicsShape", size 0x70 |
| 00690590 | `006905D0` `lea` | `00D709D8` | "PPhysicsShapeBullet", size 0x70 |
| 00690630 | `00690670` `lea` | `00D73D28` | "PPhysicsSphere", size 0x80 |
| 006906D0 | `00690710` `lea` | `00D72570` | "PPhysicsSphereBase", size 0x78 |
| 00690770 | `006907B0` `lea` | `00D731A8` | "PPhysicsSphereBullet", size 0x80 |
| 00690810 | `00690850` `lea` | `00D70B30` | "PPhysicsTaperedCapsule", size 0x88 |
| 006908B0 | `006908F0` `lea` | `00D76350` | "PPhysicsTaperedCylinder", size 0x88 |
| 00690950 | `00690990` `lea` | `00D70550` | "PPhysicsWorld", size 0xE8 |
| 00690AA0 | `00690AE0` `lea` | `00D75518` | "PPhysicsWorldBullet", size 0xE8 |
| 006A9720 | `006A9760` `lea` | `00D7C178` | "PQuarryComponent", size 0x68 |
| 006ACFF0 | `006AD030` `lea` | `00D7D400` | "PCameraOrthographic", size 0xD8 |
| 006AD860 | `006AD8A0` `lea` | `00D7D7E0` | "PCameraPerspective", size 0xD8 |
| 006ADED0 | `006ADF10` `lea` | `00D7DB20` | "PInstancesComponent", size 0x28 |
| 006AFB70 | `006AFBB0` `lea` | `00D7E580` | "PNameComponent", size 0x30 |
| 006BBAD0 | `006BBB10` `lea` | `00D81778` | "PModifierNetworkDynamicMesh", size 0x78 |
| 006C2EF0 | `006C2F30` `lea` | `00D841C8` | "PModifierNetworkInstanceInput", size 0x20 |
| 006CCF50 | `006CCF90` `lea` | `00D89D00` | "PScriptableComponent", size 0x40 |
| 006CDFF0 | `006CE030` `lea` | `00D8A370` | "PTriggerReceiverComponent", size 0x58 |
| 0086B4C0 | `0086B500` `lea` | `01CD2948` | "PInputSourceJoypadAxis", size 0x38 |
| 0086B560 | `0086B5A0` `lea` | `01CD1E20` | "PInputSourceJoypadButton", size 0x40 |
| 0086B600 | `0086B640` `lea` | `01CD1600` | "PInputSourceKey", size 0x40 |
| 0086B6A0 | `0086B6E0` `lea` | `01CD09B0` | "PInputSourceMotionAngularVelocityX", size 0x28 |
| 0086B740 | `0086B780` `lea` | `01CD0DA0` | "PInputSourceMotionAngularVelocityY", size 0x28 |
| 0086B7E0 | `0086B820` `lea` | `01CD1690` | "PInputSourceMotionAngularVelocityZ", size 0x28 |
| 0086B880 | `0086B8C0` `lea` | `01CD1EC8` | "PInputSourceMotionLinearAccelerationX", size 0x28 |
| 0086B920 | `0086B960` `lea` | `01CD2960` | "PInputSourceMotionLinearAccelerationY", size 0x28 |
| 0086B9C0 | `0086BA00` `lea` | `01CD3440` | "PInputSourceMotionLinearAccelerationZ", size 0x28 |
| 0086BA60 | `0086BAA0` `lea` | `01CD0458` | "PInputSourceMotionQuatW", size 0x28 |
| 0086BB00 | `0086BB40` `lea` | `01CD3468` | "PInputSourceMotionQuatX", size 0x28 |
| 0086BBA0 | `0086BBE0` `lea` | `01CD3D88` | "PInputSourceMotionQuatY", size 0x28 |
| 0086BC40 | `0086BC80` `lea` | `01CD4540` | "PInputSourceMotionQuatZ", size 0x28 |
| 0086BCE0 | `0086BD20` `lea` | `01CD33B8` | "PInputSourceMouseButton", size 0x38 |
| 0086BD80 | `0086BDC0` `lea` | `01CD3D70` | "PInputSourceMouseDeltaX", size 0x40 |
| 0086BE20 | `0086BE60` `lea` | `01CD4558` | "PInputSourceMouseDeltaY", size 0x40 |
| 0086BEC0 | `0086BF00` `lea` | `01CD1F60` | "PInputSourceTouchDragX", size 0x28 |
| 0086BF60 | `0086BFA0` `lea` | `01CD2A00` | "PInputSourceTouchDragY", size 0x28 |
| 0086C000 | `0086C040` `lea` | `01CD09D8` | "PInputSourceTouchPinch", size 0x28 |
| 0086C0A0 | `0086C0E0` `lea` | `01CD04D0` | "PInputSourceTouchRotate", size 0x28 |
| 0086C140 | `0086C180` `lea` | `01CD0E50` | "PInputSourceTouchTwoFingerDragX", size 0x28 |
| 0086C1E0 | `0086C220` `lea` | `01CD1740` | "PInputSourceTouchTwoFingerDragY", size 0x28 |
| 0086C280 | `0086C2C0` `lea` | `01CD3D50` | "PInputSourceVisionTrackerX", size 0x28 |
| 0086C320 | `0086C360` `lea` | `01CD44B0` | "PInputSourceVisionTrackerY", size 0x28 |
| 0086C3C0 | `0086C400` `lea` | `01CD0438` | "PInputSourceVisionTrackerZ", size 0x28 |
| 00874B70 | `00874BB0` `lea` | `01CD73A0` | "PVisionMoveTracker", size 0x8 |
| 00874CC0 | `00874D00` `lea` | `01CD7120` | "PVisionMoveTrackerWin32", size 0x8 |
| 00875760 | `008757A0` `lea` | `01CD7B68` | "PVisionTracker", size 0x8 |
| 008758B0 | `008758F0` `lea` | `01CD7900` | "PVisionTrackerWin32", size 0x8 |

## Per-member rows: the class descriptor each of the PClassDescriptorConcrete static initialisers loads (OPUS, 2026-10-03)

The family `PClassDescriptorConcrete static initialisers` (frontmatter: 254 members; 254 get a row here) shares one shape, stated here once and not repeated per row: each loads its class descriptor X into rcx and calls its own descriptor-constructor wrapper, clears bit 0x2 of dword [X+0xFC], stores the concrete vtable at qword [X], and tail-jumps to 00808B90 with rcx = its static teardown (the atexit registration); all 254 have exactly this nine-instruction form. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (the first `lea rcx` in the body; the second loads the member's teardown, part of the shared form). Each row anchors the first such `lea`, the member's distinguishing instruction, and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-descriptor-static-initialisers-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-descriptor-static-initialisers-1003/rows.tsv). A member whose loads name more than one X, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-descriptor-static-initialisers-1003/excluded.tsv).

### All 254 members (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 001603E0 | `001603E4` `lea` | `02CAD140` | PAnimatableComponent |
| 00160420 | `00160424` `lea` | `02CAD240` | PAnimationAdditiveBlenderController |
| 00160480 | `00160484` `lea` | `02CAD440` | PAnimationChannel |
| 001604C0 | `001604C4` `lea` | `02CAD540` | PAnimationChannelBase |
| 00160500 | `00160504` `lea` | `02CAD640` | PAnimationChannelTarget |
| 00160540 | `00160544` `lea` | `02CAD740` | PAnimationChannelTimes |
| 00160580 | `00160584` `lea` | `02CAD840` | PAnimationClip |
| 00160620 | `00160624` `lea` | `02CAD940` | PAnimationClipBindingChannelMap |
| 00160660 | `00160664` `lea` | `02CADA40` | PAnimationClipBindingDataBlockCache |
| 001606A0 | `001606A4` `lea` | `02CADC50` | PAnimationConstantChannel |
| 001606E0 | `001606E4` `lea` | `02CADD50` | PAnimationController |
| 00160740 | `00160744` `lea` | `02CAE350` | PAnimationDataSourceListEntry |
| 00160780 | `00160784` `lea` | `02CAE050` | PAnimationEvent |
| 001607C0 | `001607C4` `lea` | `02CADF50` | PAnimationEventController |
| 00160800 | `00160804` `lea` | `02CAE150` | PAnimationEventList |
| 00160860 | `00160864` `lea` | `02CAE550` | PAnimationNetworkInstance |
| 001608A0 | `001608A4` `lea` | `02CAE450` | PAnimationNetworkInstanceTarget |
| 001608E0 | `001608E4` `lea` | `02CAE660` | PAnimationSet |
| 00160920 | `00160924` `lea` | `02CAE860` | PAnimationSlotArray |
| 00160960 | `00160964` `lea` | `02CAEA60` | PAnimationSlotFilter |
| 001609A0 | `001609A4` `lea` | `02CAE960` | PAnimationSlotFilterDeferredLoad |
| 001609E0 | `001609E4` `lea` | `02CAE760` | PAnimationSlotListIndex |
| 00160A20 | `00160A24` `lea` | `02CAEBE0` | PAnimationSpuTargetBlenderController |
| 00160A60 | `00160A64` `lea` | `02CAECE0` | PAnimationTargetBlenderController |
| 00160AA0 | `00160AA4` `lea` | `02CAEDE0` | PAnimationWeightedBlenderController |
| 00160AE0 | `00160AE4` `lea` | `02CAD040` | PBlendableAnimationSource |
| 00160B20 | `00160B24` `lea` | `02CAEEE0` | PTimeController |
| 00160B60 | `00160B64` `lea` | `02CAEFE0` | PTimeIntervalController |
| 00160BA0 | `00160BA4` `lea` | `02CAF0E0` | PTimeScaleOffsetController |
| 00161140 | `00161144` `lea` | `02CB6480` | PConstantBuffer |
| 00161180 | `00161184` `lea` | `02CB6380` | PConstantBufferBase |
| 001611C0 | `001611C4` `lea` | `02CB7BA0` | PContextVariantFoldingTable |
| 00161240 | `00161244` `lea` | `02CB6680` | PEffect |
| 001612C0 | `001612C4` `lea` | `02CBB400` | PForwardShadowRenderer |
| 00161300 | `00161304` `lea` | `02CB6980` | PIndirectArgsBuffer |
| 00161340 | `00161344` `lea` | `02CB6880` | PIndirectArgsBufferBase |
| 001613C0 | `001613C4` `lea` | `02CB6A80` | PMaterialSwitch |
| 00161480 | `00161484` `lea` | `02CB7080` | PMeshInstanceBounds |
| 001614C0 | `001614C4` `lea` | `02CB6D80` | PMeshInstanceSegmentContext |
| 00161500 | `00161504` `lea` | `02CB6C80` | PMeshInstanceSegmentStreamBinding |
| 00161580 | `00161584` `lea` | `02CB7280` | PNodeContext |
| 00161690 | `00161694` `lea` | `02CB78A0` | PSamplerState |
| 001616D0 | `001616D4` `lea` | `02CB77A0` | PSamplerStateBase |
| 00161710 | `00161714` `lea` | `02CB79A0` | PSceneRenderPass |
| 00161750 | `00161754` `lea` | `02CB7CA0` | PSceneWideParameterBuffer |
| 00161790 | `00161794` `lea` | `02CB9000` | PShader |
| 00161890 | `00161894` `lea` | `02CBA500` | PShaderParameterCaptureBufferByteAddressBuffer |
| 001618D0 | `001618D4` `lea` | `02CBA700` | PShaderParameterCaptureBufferDataBlock |
| 00161910 | `00161914` `lea` | `02CBA800` | PShaderParameterCaptureBufferIndexDataBlock |
| 00161950 | `00161954` `lea` | `02CB9100` | PShaderParameterCaptureBufferLocation |
| 00161990 | `00161994` `lea` | `02CB9200` | PShaderParameterCaptureBufferLocationSize |
| 001619D0 | `001619D4` `lea` | `02CB9300` | PShaderParameterCaptureBufferLocationType |
| 00161A10 | `00161A14` `lea` | `02CB9400` | PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 00161A50 | `00161A54` `lea` | `02CBA600` | PShaderParameterCaptureBufferRWByteAddressBuffer |
| 00161A90 | `00161A94` `lea` | `02CBA400` | PShaderParameterCaptureBufferRWStructuredBuffer |
| 00161AD0 | `00161AD4` `lea` | `02CBA900` | PShaderParameterCaptureBufferRWTexture2D |
| 00161B10 | `00161B14` `lea` | `02CBAA00` | PShaderParameterCaptureBufferRWTexture3D |
| 00161B50 | `00161B54` `lea` | `02CBA200` | PShaderParameterCaptureBufferSampler |
| 00161B90 | `00161B94` `lea` | `02CB9C00` | PShaderParameterCaptureBufferStream |
| 00161BD0 | `00161BD4` `lea` | `02CBA300` | PShaderParameterCaptureBufferStructuredBuffer |
| 00161C10 | `00161C14` `lea` | `02CB9F00` | PShaderParameterCaptureBufferTexture2D |
| 00161C50 | `00161C54` `lea` | `02CBA000` | PShaderParameterCaptureBufferTexture3D |
| 00161CD0 | `00161CD4` `lea` | `02CBA100` | PShaderParameterCaptureBufferTextureCubeMap |
| 00161D10 | `00161D14` `lea` | `02CB9E00` | PShaderParameterCaptureConstantBuffer |
| 00161D50 | `00161D54` `lea` | `02CB9500` | PShaderParameterDefinition |
| 00161D90 | `00161D94` `lea` | `02CB9A00` | PShaderPass |
| 00161DD0 | `00161DD4` `lea` | `02CB9900` | PShaderPassBase |
| 00161E10 | `00161E14` `lea` | `02CB7AA0` | PShaderPassInfo |
| 00161E50 | `00161E54` `lea` | `02CB9700` | PShaderPassParameterLocationTypes |
| 00161E90 | `00161E94` `lea` | `02CB9600` | PShaderPassParameterLocationTypesBase |
| 00161ED0 | `00161ED4` `lea` | `02CB9800` | PShaderPassParameterLocationTypesConstantBuffer |
| 00161F10 | `00161F14` `lea` | `02CB9B00` | PShaderPassStateBase |
| 00161F50 | `00161F54` `lea` | `02CBAD00` | PShaderProgramBase |
| 00161F90 | `00161F94` `lea` | `02CBAC00` | PShaderProgramParamsAndStreams |
| 00162010 | `00162014` `lea` | `02CBAE00` | PShaderStreamDefinition |
| 00162090 | `00162094` `lea` | `02CBB300` | PShadowRenderer |
| 001620D0 | `001620D4` `lea` | `02CBB600` | PStructuredBuffer |
| 00162110 | `00162114` `lea` | `02CBB500` | PStructuredBufferBase |
| 00162150 | `00162154` `lea` | `02CBB900` | PTexture2D |
| 00162190 | `00162194` `lea` | `02CBB800` | PTexture2DBase |
| 001621D0 | `001621D4` `lea` | `02CBBB00` | PTexture3D |
| 00162210 | `00162214` `lea` | `02CBBA00` | PTexture3DBase |
| 00162250 | `00162254` `lea` | `02CBB700` | PTextureCommonBase |
| 00162290 | `00162294` `lea` | `02CBBD00` | PTextureCubeMap |
| 001622D0 | `001622D4` `lea` | `02CBBC00` | PTextureCubeMapBase |
| 00162BD0 | `00162BD4` `lea` | `02CF2440` | PConstantBufferD3D11 |
| 00162C10 | `00162C14` `lea` | `02CF2340` | PIndirectArgsBufferD3D11 |
| 00162C70 | `00162C74` `lea` | `02CF2140` | PSamplerStateD3D11 |
| 00162D70 | `00162D74` `lea` | `02CF1440` | PShaderPassD3D11 |
| 00162DB0 | `00162DB4` `lea` | `02CF1540` | PShaderPassStateD3D11 |
| 00162E70 | `00162E74` `lea` | `02CF1640` | PStreamInputDescD3D11 |
| 00162EF0 | `00162EF4` `lea` | `02CF2240` | PStructuredBufferD3D11 |
| 00162F30 | `00162F34` `lea` | `02CF1D40` | PTexture2DD3D11 |
| 00162F70 | `00162F74` `lea` | `02CF1E40` | PTexture3DD3D11 |
| 00162FB0 | `00162FB4` `lea` | `02CF1F40` | PTextureCubeMapD3D11 |
| 00164230 | `00164234` `lea` | `02D368A0` | PAtmospherics |
| 00164270 | `00164274` `lea` | `02D367A0` | PAtmosphericsBase |
| 001642B0 | `001642B4` `lea` | `02D369A0` | PAtmosphericsD3D11 |
| 001642F0 | `001642F4` `lea` | `02D362A0` | PCelShading |
| 00164330 | `00164334` `lea` | `02D361A0` | PCelShadingBase |
| 00164370 | `00164374` `lea` | `02D363A0` | PCelShadingD3D11 |
| 001643B0 | `001643B4` `lea` | `02D34940` | PDeferredLighting |
| 001643F0 | `001643F4` `lea` | `02D34840` | PDeferredLightingBase |
| 00164430 | `00164434` `lea` | `02D34A40` | PDeferredLightingD3D11 |
| 00164470 | `00164474` `lea` | `02D34C40` | PDepthOfField |
| 001644B0 | `001644B4` `lea` | `02D34B40` | PDepthOfFieldBase |
| 001644F0 | `001644F4` `lea` | `02D34D40` | PDepthOfFieldD3D11 |
| 00164530 | `00164534` `lea` | `02D35FA0` | PFXAA |
| 00164570 | `00164574` `lea` | `02D35EA0` | PFXAABase |
| 001645B0 | `001645B4` `lea` | `02D360A0` | PFXAAD3D11 |
| 001645F0 | `001645F4` `lea` | `02D35CA0` | PGlow |
| 00164630 | `00164634` `lea` | `02D35AA0` | PGlowBase |
| 00164670 | `00164674` `lea` | `02D35DA0` | PGlowD3D11 |
| 001646B0 | `001646B4` `lea` | `02D35BA0` | PGlowGPUBase |
| 001646F0 | `001646F4` `lea` | `02D36AA0` | PLowResParticles |
| 00164730 | `00164734` `lea` | `02D357A0` | PMLAA |
| 00164770 | `00164774` `lea` | `02D356A0` | PMLAABase |
| 001647B0 | `001647B4` `lea` | `02D358A0` | PMLAAD3D11 |
| 001647F0 | `001647F4` `lea` | `02D36BA0` | PMaterialPostEffect |
| 00164830 | `00164834` `lea` | `02D359A0` | PMeshParticleSystemBase |
| 00164870 | `00164874` `lea` | `02D34F40` | PMotionBlur |
| 001648B0 | `001648B4` `lea` | `02D34E40` | PMotionBlurBase |
| 001648F0 | `001648F4` `lea` | `02D35040` | PMotionBlurD3D11 |
| 00164930 | `00164934` `lea` | `02D34740` | PPostEffectBase |
| 00164970 | `00164974` `lea` | `02D36CA0` | PPostEffectManager |
| 001649B0 | `001649B4` `lea` | `02D35400` | PScreenSpaceAmbientOcclusion |
| 001649F0 | `001649F4` `lea` | `02D35300` | PScreenSpaceAmbientOcclusionBase |
| 00164A30 | `00164A34` `lea` | `02D35500` | PScreenSpaceAmbientOcclusionD3D11 |
| 00164A70 | `00164A74` `lea` | `02D365A0` | PScreenSpaceReflection |
| 00164AB0 | `00164AB4` `lea` | `02D364A0` | PScreenSpaceReflectionBase |
| 00164AF0 | `00164AF4` `lea` | `02D366A0` | PScreenSpaceReflectionD3D11 |
| 00165480 | `00165484` `lea` | `02D39E40` | PDataBlock |
| 001654C0 | `001654C4` `lea` | `02D39D40` | PDataBlockBase |
| 00165500 | `00165504` `lea` | `02D39B40` | PDataBlockBufferD3D11 |
| 00165540 | `00165544` `lea` | `02D39C40` | PDataBlockD3D11 |
| 00165580 | `00165584` `lea` | `02D39F40` | PDynamicDataBlock |
| 001655E0 | `001655E4` `lea` | `02D3A040` | PDynamicSegmentDesc |
| 00165620 | `00165624` `lea` | `02D3A340` | PIndexDataBlock |
| 00165660 | `00165664` `lea` | `02D3A240` | PIndexDataBlockBase |
| 001656A0 | `001656A4` `lea` | `02D39940` | PIndexDataBlockBufferD3D11 |
| 001656E0 | `001656E4` `lea` | `02D39A40` | PIndexDataBlockD3D11 |
| 00165720 | `00165724` `lea` | `02D3A440` | PMaterialSet |
| 00165760 | `00165764` `lea` | `02D3A640` | PMesh |
| 001657A0 | `001657A4` `lea` | `02D3A940` | PMeshSegment |
| 001657E0 | `001657E4` `lea` | `02D3A840` | PMeshSegmentBase |
| 00165820 | `00165824` `lea` | `02D39840` | PMeshSegmentD3D11 |
| 00165860 | `00165864` `lea` | `02D3ACE0` | PShape |
| 001658A0 | `001658A4` `lea` | `02D3A540` | PSkeletonJointBounds |
| 001658E0 | `001658E4` `lea` | `02D3A740` | PSkinBoneRemap |
| 00165920 | `00165924` `lea` | `02D3ADE0` | PVertexStream |
| 00165FA0 | `00165FA4` `lea` | `02D3F210` | PCamera |
| 00166040 | `00166044` `lea` | `02E3F960` | PBitmapFontCharInfo |
| 001660C0 | `001660C4` `lea` | `02E41270` | PAsyncProcessHeader |
| 00166180 | `00166184` `lea` | `02E41470` | PScript |
| 001661C0 | `001661C4` `lea` | `02E41170` | PScriptCallbackHandler |
| 00166270 | `00166274` `lea` | `02E479D0` | PPhysicsBox |
| 001662B0 | `001662B4` `lea` | `02E478D0` | PPhysicsBoxBase |
| 001662F0 | `001662F4` `lea` | `02E496D0` | PPhysicsBoxBullet |
| 00166370 | `00166374` `lea` | `02E47BD0` | PPhysicsCapsule |
| 001663B0 | `001663B4` `lea` | `02E47AD0` | PPhysicsCapsuleBase |
| 001663F0 | `001663F4` `lea` | `02E497D0` | PPhysicsCapsuleBullet |
| 00166430 | `00166434` `lea` | `02E47CD0` | PPhysicsCharacterCamera |
| 00166470 | `00166474` `lea` | `02E47ED0` | PPhysicsCharacterController |
| 001664B0 | `001664B4` `lea` | `02E47DD0` | PPhysicsCharacterControllerBase |
| 001664F0 | `001664F4` `lea` | `02E49FD0` | PPhysicsCharacterControllerBullet |
| 00166530 | `00166534` `lea` | `02E480D0` | PPhysicsCylinder |
| 00166570 | `00166574` `lea` | `02E47FD0` | PPhysicsCylinderBase |
| 001665B0 | `001665B4` `lea` | `02E498D0` | PPhysicsCylinderBullet |
| 00166610 | `00166614` `lea` | `02E481D0` | PPhysicsInterfaceBase |
| 00166650 | `00166654` `lea` | `02E49ED0` | PPhysicsInterfaceBullet |
| 00166690 | `00166694` `lea` | `02E483D0` | PPhysicsMaterial |
| 001666D0 | `001666D4` `lea` | `02E485D0` | PPhysicsMesh |
| 00166710 | `00166714` `lea` | `02E484D0` | PPhysicsMeshBase |
| 00166750 | `00166754` `lea` | `02E499D0` | PPhysicsMeshBullet |
| 00166790 | `00166794` `lea` | `02E486D0` | PPhysicsModel |
| 001667D0 | `001667D4` `lea` | `02E488D0` | PPhysicsPlane |
| 00166810 | `00166814` `lea` | `02E487D0` | PPhysicsPlaneBase |
| 00166850 | `00166854` `lea` | `02E49AD0` | PPhysicsPlaneBullet |
| 00166890 | `00166894` `lea` | `02E48BD0` | PPhysicsRigidBody |
| 001668D0 | `001668D4` `lea` | `02E489D0` | PPhysicsRigidBodyBase |
| 00166910 | `00166914` `lea` | `02E49CD0` | PPhysicsRigidBodyBullet |
| 00166950 | `00166954` `lea` | `02E48DD0` | PPhysicsShape |
| 001669B0 | `001669B4` `lea` | `02E495D0` | PPhysicsShapeBullet |
| 001669F0 | `001669F4` `lea` | `02E48FD0` | PPhysicsSphere |
| 00166A30 | `00166A34` `lea` | `02E48ED0` | PPhysicsSphereBase |
| 00166A70 | `00166A74` `lea` | `02E49BD0` | PPhysicsSphereBullet |
| 00166AB0 | `00166AB4` `lea` | `02E490D0` | PPhysicsTaperedCapsule |
| 00166AF0 | `00166AF4` `lea` | `02E491D0` | PPhysicsTaperedCylinder |
| 00166B30 | `00166B34` `lea` | `02E494D0` | PPhysicsWorld |
| 00166B70 | `00166B74` `lea` | `02E492D0` | PPhysicsWorldBase |
| 00166BB0 | `00166BB4` `lea` | `02E49DD0` | PPhysicsWorldBullet |
| 00166BF0 | `00166BF4` `lea` | `02E493D0` | PRaycastResult |
| 00166C90 | `00166C94` `lea` | `02E4D630` | PString |
| 00166CD0 | `00166CD4` `lea` | `02E4D940` | PTrigger |
| 00166D10 | `00166D14` `lea` | `02E4E1E0` | PQuarryComponent |
| 00166D90 | `00166D94` `lea` | `02E4E720` | PComponent |
| 00166DD0 | `00166DD4` `lea` | `02E4EAF0` | PEntity |
| 00166E20 | `00166E24` `lea` | `02E4F290` | PCameraOrthographic |
| 00166E60 | `00166E64` `lea` | `02E4F710` | PCameraPerspective |
| 00166EA0 | `00166EA4` `lea` | `02E4F900` | PInstancesComponent |
| 00166F60 | `00166F64` `lea` | `02E518D0` | PNode |
| 00166FD0 | `00166FD4` `lea` | `02E522F0` | PMeshSegmentContext |
| 00167330 | `00167334` `lea` | `02E58060` | PModifierNetworkDynamicMesh |
| 00167370 | `00167374` `lea` | `02E57F60` | PModifierNetworkDynamicMeshSegment |
| 001673B0 | `001673B4` `lea` | `02E58DB0` | PLight |
| 00167560 | `00167564` `lea` | `02E59DC0` | PShadowCaster |
| 001675A0 | `001675A4` `lea` | `02E59CC0` | PShadowSplit |
| 00167750 | `00167754` `lea` | `02E5A6C0` | PModifierNetworkInstance |
| 00167790 | `00167794` `lea` | `02E5A4C0` | PModifierNetworkInstanceInput |
| 001677D0 | `001677D4` `lea` | `02E5A5C0` | PModifierNetworkInstancePacketInput |
| 001678D0 | `001678D4` `lea` | `02E5AE00` | PLODGroup |
| 00167910 | `00167914` `lea` | `02E5AD00` | PLODLevel |
| 00167CB0 | `00167CB4` `lea` | `02E5C710` | PTriggerReceiverComponent |
| 00167CF0 | `00167CF4` `lea` | `02E5E030` | PModifierAndInputs |
| 00167D30 | `00167D34` `lea` | `02E5E540` | PModifierNetwork |
| 00167D70 | `00167D74` `lea` | `02E5DF30` | PModifierNetworkBuffer |
| 00167E10 | `00167E14` `lea` | `02E5E330` | PModifierNetworkInfoPacket_Buffer |
| 00167E50 | `00167E54` `lea` | `02E5E130` | PModifierNetworkInfoPacket_ModifierCode |
| 00167E90 | `00167E94` `lea` | `02E5E230` | PModifierNetworkInfoPacket_ModifierInstance |
| 00167ED0 | `00167ED4` `lea` | `02E5DE30` | PRenderStream |
| 00167F10 | `00167F14` `lea` | `02E5DD30` | PRenderStreamInput |
| 00167FA0 | `00167FA4` `lea` | `02E9FDF0` | PMorphModifierWeightsUserDataObject |
| 00169320 | `00169324` `lea` | `02EA9400` | PDebugUtils |
| 00169360 | `00169364` `lea` | `02EA5560` | PInputMapper |
| 0016A360 | `0016A364` `lea` | `02EB6CF0` | PInputAction |
| 0016A3A0 | `0016A3A4` `lea` | `02EB6DF0` | PInputMap |
| 0016A400 | `0016A404` `lea` | `02EB55F0` | PInputSourceJoypadAxis |
| 0016A440 | `0016A444` `lea` | `02EB54F0` | PInputSourceJoypadButton |
| 0016A480 | `0016A484` `lea` | `02EB53F0` | PInputSourceKey |
| 0016A4C0 | `0016A4C4` `lea` | `02EB63F0` | PInputSourceMotionAngularVelocityX |
| 0016A500 | `0016A504` `lea` | `02EB64F0` | PInputSourceMotionAngularVelocityY |
| 0016A540 | `0016A544` `lea` | `02EB65F0` | PInputSourceMotionAngularVelocityZ |
| 0016A580 | `0016A584` `lea` | `02EB66F0` | PInputSourceMotionLinearAccelerationX |
| 0016A5C0 | `0016A5C4` `lea` | `02EB67F0` | PInputSourceMotionLinearAccelerationY |
| 0016A600 | `0016A604` `lea` | `02EB68F0` | PInputSourceMotionLinearAccelerationZ |
| 0016A640 | `0016A644` `lea` | `02EB62F0` | PInputSourceMotionQuatW |
| 0016A680 | `0016A684` `lea` | `02EB5FF0` | PInputSourceMotionQuatX |
| 0016A6C0 | `0016A6C4` `lea` | `02EB60F0` | PInputSourceMotionQuatY |
| 0016A700 | `0016A704` `lea` | `02EB61F0` | PInputSourceMotionQuatZ |
| 0016A740 | `0016A744` `lea` | `02EB56F0` | PInputSourceMouseButton |
| 0016A780 | `0016A784` `lea` | `02EB57F0` | PInputSourceMouseDeltaX |
| 0016A7C0 | `0016A7C4` `lea` | `02EB58F0` | PInputSourceMouseDeltaY |
| 0016A800 | `0016A804` `lea` | `02EB5BF0` | PInputSourceTouchDragX |
| 0016A840 | `0016A844` `lea` | `02EB5CF0` | PInputSourceTouchDragY |
| 0016A880 | `0016A884` `lea` | `02EB5AF0` | PInputSourceTouchPinch |
| 0016A8C0 | `0016A8C4` `lea` | `02EB59F0` | PInputSourceTouchRotate |
| 0016A900 | `0016A904` `lea` | `02EB5DF0` | PInputSourceTouchTwoFingerDragX |
| 0016A940 | `0016A944` `lea` | `02EB5EF0` | PInputSourceTouchTwoFingerDragY |
| 0016A980 | `0016A984` `lea` | `02EB69F0` | PInputSourceVisionTrackerX |
| 0016A9C0 | `0016A9C4` `lea` | `02EB6AF0` | PInputSourceVisionTrackerY |
| 0016AA00 | `0016AA04` `lea` | `02EB6BF0` | PInputSourceVisionTrackerZ |
| 0016AA40 | `0016AA44` `lea` | `02EB7CD0` | PVisionMoveTracker |
| 0016AAC0 | `0016AAC4` `lea` | `02EB8060` | PVisionTracker |
| 0016D560 | `0016D564` `lea` | `02EB9E60` | PGameConfig |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-class-descriptor-and-metadata-system-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00631A60` | 474 B | Constructs the object at `rcx` and returns it: on first use (the guard dword `02CF94EC` greater than the thread's epoch read through `gs:[0x58]` and the index at `02EAED3C`) it calls `008092FC` on the guard and, when the guard then reads -1, self-links the static record at `01F2E330` (qwords `01F2E330`/`01F2E338`, `01F2E340`/`01F2E348`, `01F2E358`/`01F2E360`, dword `01F2E350` zero), registers `008AF490` through `00808B90` and calls `0080929C` on the guard; it then self-links the list heads at `+8` (three qwords), `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0` and `+0xB0`, zeroes the dword `+0x20` (bytes `+0x24`..`+0x27` are not written) and the qwords `+0x28`, `+0x40`, `+0x48` and `+0xC0` to `+0xE0`, stores `00D569B8` to `+0x30`, 0x60 and 8 to dwords `+0x38`/`+0x3C`, `01F2E330` and `rdx` to `+0x70`/`+0x78`, the counter at `02CF8260` to `+0xE8` (then increments it), `r8d` to `+0xF0`, -1 to `+0xEC`, zeroes `+0xF4` to `+0xFF`, and leaves the vtable pointer at `+0` as `00D56A38` (written over `00D581C0`). | `00631AA9`, `00631AED`, `00631B87`, `00631BCD`, `00631C24` |
| `006458A0` | 800 B | Calls `006461B0` on `rcx`, sets the vtable pointer `00D61EA0`, fills 0x80 entries of 0x80 bytes from `+0x50` and one more at `+0x4050` with the same fixed pattern (zeros and 1.0 floats, with 50.0 at entry `+0x54`, 100.0 at `+0x58` and the largest finite float at `+0x70`), writes 0.2 to the floats `+0x40D0` to `+0x40D8`, 1.0 to `+0x40DC`, `+0x40EC`, `+0x40FC`, `+0x4104`, `+0x4108` and `+0x410C`, 100.0 to `+0x40F0` and 20.0 to `+0x40F4`, and zero to the other dwords up to `+0x412F`, constructs the member at `+0x4130` with `00615CD0`, zeroes the qwords `+0x4158` to `+0x41C8`, sets byte `+0x41D0` to 1 and writes 1, 1, 2, 2 into the member's bytes `+0` to `+3` and sets bit `0x40` of its dword `+0x1C`, each of these five writes done only when bit `0x80` of that dword is clear, returning `rcx`. | `006458C0`, `00645938`, `00645977`, `00645AEF`, `00645BA7` |

## No-reference bodies homed by owning class (FABLE, 2026-10-03)

*No page cited these functions and nothing calls them directly: each is a virtual method, entered through its owning class's vtable, and this page documents that class. Each sentence states what the body does (access and representation, not purpose) and ends with the vtable slot and owning class from `rtti-methods.tsv`; the anchors are instructions inside the body that do it. Handed over by SWE2-EC7 and read whole by FABLE against the certified image; verified by [`apply.py`](../../_index/candidates/fable-noref-class-descriptor-and-metadata-system-1003/apply.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005A1110` | 38 B | stores the address `00D312F0` (the `PAnimationHierarchyNode` vtable, in `.rdata`) to qwords `+0x10`, `+0x38` and `+0x58` of the object in `rdx` and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<PBlendableAnimationSource>`, `PClassDescriptorConcrete<PBlendableAnimationSource>` and `PClassDescriptorForType<PBlendableAnimationSource>` | Interior anchor `005A111C`; Interior anchor `005A1123`; Interior anchor `005A1127`; Interior anchor `005A112B`; Interior anchor `005A112F` |
| `005A1580` | 19 B | calls `005A9E70` with the object in `rdx` as `rcx` and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<PAnimationClip>`, `PClassDescriptorConcrete<PAnimationClip>` and `PClassDescriptorForType<PAnimationClip>` | Interior anchor `005A1584`; Interior anchor `005A1587`; Interior anchor `005A158C` |
| `005A2280` | 19 B | calls `005A9D80` with the object in `rdx` as `rcx` and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<PAnimationChannel>`, `PClassDescriptorConcrete<PAnimationChannel>` and `PClassDescriptorForType<PAnimationChannel>` | Interior anchor `005A2284`; Interior anchor `005A2287`; Interior anchor `005A228C` |
| `005A3EA0` | 19 B | tail-jumps through the qword at `+0x100` of the descriptor object in `rcx` (a field, not its vtable) with `rcx` = the second argument, `rdx` = the third, `r8` unchanged and `r9` = the descriptor; vtable slot 15 of `PClassDescriptorHeader<PAnimationClipBinding>`, `PClassDescriptorHeader<PModifierNetworkInfoPacket>`, `PClassDescriptorHeader<POccluderGeometryObject>` and `PClassDescriptorHeaderWithoutDefaultConstructor<PParameterBuffer>` | Interior anchor `005A3EA3`; Interior anchor `005A3EA6`; Interior anchor `005A3EA9`; Interior anchor `005A3EAC` |
| `005A44E0` | 13 B | stores qword 0 at `[rdx]` when `rdx` is non-NULL and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorConcrete<PAnimationEvent>`, `<PAnimationSlotArray>`, `<PModifierNetworkInstancePacketInput>`, `<PVisionMoveTracker>` and `<PVisionTracker>`, and `PClassDescriptorHeader<PAnimationClipBinding>` | Interior anchor `005A44E3`; Interior anchor `005A44E7`; Interior anchor `005A44EA` |
| `005D2C60` | 21 B | when `rdx` is non-NULL stores qword 0xFF at `[rdx]` and qword 0 at `[rdx+8]`, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorWithoutDefaultConstructor<PShaderParameterCaptureBufferTextureBase>` | Interior anchor `005D2C63`; Interior anchor `005D2C67`; Interior anchor `005D2C6E`; Interior anchor `005D2C72` |
| `006110B0` | 86 B | calls `0062BAB0` with the object in `rdx`; when bit 31 of that object's dword `+0x78` is clear it calls `00619070` with qword `+0x80` and that dword; it then stores 0 to qword `+0x80` and dword `+0x78`, calls `00616B40` with the object, and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<PShaderVertexProgramD3D11>`, `PClassDescriptorForType<PShaderVertexProgramD3D11>` and `PClassDescriptorWithoutDefaultConstructor<PShaderVertexProgramD3D11>` | Interior anchor `006110C5`; Interior anchor `006110D0`; Interior anchor `006110D7`; Interior anchor `006110E4`; Interior anchor `006110F8` |
| `00613530` | 66 B | when `rdx` is non-NULL stores 0 to qwords `+0`, `+0x10` and `+0x20` through `+0x68` and to dwords `+8`, `+0x18` and `+0x70` of that object, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorWithoutDefaultConstructor<PShaderProgramD3D11>` | Interior anchor `00613533`; Interior anchor `00613537`; Interior anchor `0061353A`; Interior anchor `0061354C`; Interior anchor `0061356B` |
| `0062F880` | 24 B | when `rdx` is non-NULL stores `rdx` itself at qwords `+0` and `+8`, 0 at dword `+0x10` and 0 at qword `+0x18`, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorWithoutDefaultConstructor<PWorld>` | Interior anchor `0062F883`; Interior anchor `0062F887`; Interior anchor `0062F88A`; Interior anchor `0062F88E`; Interior anchor `0062F891` |
| `00688000` | 51 B | calls `006A49A0`, `006A4710` and `00691DF0` in turn, each with the object in `rdx` as `rcx`, and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<PPhysicsWorld>`, `PClassDescriptorConcrete<PPhysicsWorld>` and `PClassDescriptorForType<PPhysicsWorld>` | Interior anchor `00688015`; Interior anchor `0068801D`; Interior anchor `00688025`; Interior anchor `0068802B` |
| `006A9450` | 28 B | calls `006AAA50` with the object in `rdx` as `rcx` and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<PQuarryComponent>`, `PClassDescriptorConcrete<PQuarryComponent>` and `PClassDescriptorForType<PQuarryComponent>` | Interior anchor `006A945D`; Interior anchor `006A9460`; Interior anchor `006A9465` |
| `006AA6C0` | 35 B | calls `006ACA70` with qword `+8` of the object in `rdx` when that qword is non-NULL, and returns 1 in `al` on both paths; vtable slot 11 of `PClassDescriptorAbstract<PComponent>`, `PClassDescriptorConcrete<PComponent>` and `PClassDescriptorForType<PComponent>` | Interior anchor `006AA6CD`; Interior anchor `006AA6D1`; Interior anchor `006AA6D6`; Interior anchor `006AA6DC` |
| `006AA7F0` | 35 B | takes count = dword `+0x70`, cursor = qword `+0x58` and value = qword `+0x50` of the object in `rdx`, reads the stride once as the dword at `+0x38` of the value, and for count iterations stores the value at qword `+0x10` of the cursor and advances the cursor by the stride; it returns 0; vtable slot 14 of `PClassDescriptorAbstract<PComponent>` and `PClassDescriptorConcrete<PComponent>` | Interior anchor `006AA7F3`; Interior anchor `006AA7FF`; Interior anchor `006AA803`; Interior anchor `006AA807`; Interior anchor `006AA810` |
| `006B2E40` | 11 B | tail-jumps to `006843D0` with `rcx` = the second argument and `rdx` = the third; vtable slot 4 of `PClassDescriptorWrapper<Vector3>` | Interior anchor `006B2E43`; Interior anchor `006B2E46` |
| `006CD6A0` | 12 B | returns 0 when `rdx` is NULL and the qword at `[rdx]` otherwise; vtable slot 8 of `PNamedSemanticDescriptorForDynamicType<PTriggerType>` and `<PSceneRenderPassType>`, and `PNamedSemanticDescriptorForType<PAnimationKeyDataType>`, `<PModifier>`, `<PRenderDataType>` and `<PTextureFormatBase>` | Interior anchor `006CD6A3`; Interior anchor `006CD6A5`; Interior anchor `006CD6A8` |
| `006CE820` | 25 B | when `rdx` is non-NULL stores 0 to the four qwords `+0` through `+0x18` of that object, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorConcrete<PModifierNetworkInfoPacket_ModifierCode>` and `<PModifierNetworkInfoPacket_ModifierInstance>`, and `PClassDescriptorHeader<PModifierNetworkInfoPacket>` | Interior anchor `006CE823`; Interior anchor `006CE827`; Interior anchor `006CE832`; Interior anchor `006CE836` |
| `006D98C0` | 13 B | returns 0 when `rdx` is NULL and the qword at `[rdx+8]` otherwise; vtable slot 8 of `PNamedSemanticDescriptorForDynamicType<PContextSwitch>` and ten PNamedSemanticDescriptorForType instantiations (PInputAxisSemantic, PInputChannelSemantic, PInputJoypadButtonSemantic, PInputKeySemantic, PInputMouseButtonSemantic, PInputTypeSemantic, PLODBlendType, PLODMetricType, PLightType, PShadowCasterType) | Interior anchor `006D98C3`; Interior anchor `006D98C5`; Interior anchor `006D98C8` |
| `006D9E80` | 31 B | when `rdx` is non-NULL stores 0 to qwords `+0`, `+8`, `+0x10` and `+0x20` and to dwords `+0x18` and `+0x28` of that object, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorHeader<POccluderGeometryObject>` | Interior anchor `006D9E83`; Interior anchor `006D9E87`; Interior anchor `006D9E92`; Interior anchor `006D9E99` |
| `008773B0` | 44 B | calls `00878070` with `rdx` + 0x78 and then with `rdx` + 0x28, and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<POctreeWorld>`, `PClassDescriptorForType<POctreeWorld>` and `PClassDescriptorWithoutDefaultConstructor<POctreeWorld>` | Interior anchor `008773C2`; Interior anchor `008773C6`; Interior anchor `008773CB`; Interior anchor `008773CF` |
| `008775E0` | 34 B | with no NULL test takes `n` = qword `+0x20` and `p` = qword `+0x28` of the object in `rdx`, stores `n` at qword `+0x20` of `p` and `p` at qword `+0x28` of `n`, points the object's own qwords `+0x20` and `+0x28` back at the object, stores qword 0 at `+0`, and returns 1 in `al`; vtable slot 11 of `PClassDescriptorAbstract<POctreeData>`, `PClassDescriptorForType<POctreeData>` and `PClassDescriptorWithoutDefaultConstructor<POctreeData>` | Interior anchor `008775E4`; Interior anchor `008775E8`; Interior anchor `008775EC`; Interior anchor `008775F2`; Interior anchor `008775FA` |
| `008779E0` | 67 B | when `rdx` is non-NULL stores 0 to qword `+0x10`, dword `+0x18` and dword `+0`, copies dwords `+0x14` and `+0x18` (both already 0 from those stores) to dwords `+4` and `+8`, stores 0 to dwords `+0x20`, `+0x24` and `+0x34` and qwords `+0x38`, `+0x40` and `+0x48`, 10 to dword `+0x28` and qword 1 to `+0x2C`, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorWithoutDefaultConstructor<POctree>` | Interior anchor `008779E7`; Interior anchor `008779F0`; Interior anchor `008779F6`; Interior anchor `008779FF`; Interior anchor `00877A06` |
| `00879980` | 20 B | when `rdx` is non-NULL stores 0 to dword `+0` and qwords `+8` and `+0x10` of that object, and returns 1 in `al` on both paths; vtable slot 10 of `PClassDescriptorConcrete<PGameConfig>` and `<PInputMap>`, and `PClassDescriptorWithoutDefaultConstructor<PStreamInputLayoutD3D11>` | Interior anchor `00879983`; Interior anchor `00879987`; Interior anchor `0087998D`; Interior anchor `00879991` |

## No-reference bodies homed by the table that reaches them (FABLE, 2026-10-03)

*No page cited these functions and no census-listed instruction calls or jumps to them: each is reached through data or through code this page documents. Each sentence states what the body does (access and representation, not purpose) and ends with the reference that reaches it; the anchors are instructions inside the body that do it. Handed over by SWE2-EC7 and read whole by FABLE against the certified image; verified by [`apply.py`](../../_index/candidates/fable-noref-class-descriptor-and-metadata-system-data-1003/apply.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic, and every named reference holds or forms the body's address at the bytes.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005C4CC0` | 7 B | returns dword `[rcx]` with bit 31 cleared (`btr`); stored to qword `02CB3B30` by `005B5130` + 0x2BB, after `00632A10` has built the member object at `02CB3AD0`, and 70 other sites form it the same way | Interior anchor `005C4CC2` |
| `00671250` | 29 B | with n = dword `[rcx]` with bit 31 cleared, returns qword `+8` when n is above 1, the address `rcx` + 8 when n is 1, and 0 when n is 0; stored to qword `02CECB08` by `005EFE60` + 0x203, and 9 other sites form it the same way | Interior anchor `00671252`; Interior anchor `00671256`; Interior anchor `0067125B`; Interior anchor `00671260`; Interior anchor `00671268` |
| `00677A50` | 19 B | copies qwords `+0x38` and `+0x40` to `[rdx]` and `[rdx+8]` and returns `rdx`; stored to stack `+0x48` by `00675740` + 0x393 | Interior anchor `00677A54`; Interior anchor `00677A58`; Interior anchor `00677A5E` |
| `006A77C0` | 43 B | with `p` = qword `[rcx]`: returns 0 when `p` is null; with `p`'s bit 0 subtracted, returns 1 when the result is 0 and otherwise the length of the string there plus 1; stored to qword `02E4D790` by `006A72B0` + 0xB1 | Interior anchor `006A77C8`; Interior anchor `006A77CE`; Interior anchor `006A77DA`; Interior anchor `006A77E0`; Interior anchor `006A77E5` |
| `006A77F0` | 13 B | returns qword `[rcx]` minus its own bit 0 (the low bit of byte `[rcx]`); stored to qword `02E4D798` by `006A72B0` + 0xF4 | Interior anchor `006A77F3`; Interior anchor `006A77F6`; Interior anchor `006A77F9` |
| `006AF4E0` | 11 B | returns qword `+0x20` plus the zero-extended `edx` times 16; stored to qword `02E4FA98` by `006AE350` + 0x1BF | Interior anchor `006AF4E2`; Interior anchor `006AF4E6` |
| `006B2E60` | 9 B | stores the float `xmm1` to dword `+0xC` and returns `rcx`; stored to qword `02E51028` by `006B0EC0` + 0x413, and 1 other site forms it the same way | Interior anchor `006B2E65` |
| `006B2E70` | 8 B | stores the float `xmm1` to dword `[rcx]` and returns `rcx`; stored to qword `02E50968` by `006B0B20` + 0x1D6, and 4 other sites form it the same way | Interior anchor `006B2E74` |
| `006B2E80` | 9 B | stores the float `xmm1` to dword `+4` and returns `rcx`; stored to qword `02E509C8` by `006B0B20` + 0x295, and 4 other sites form it the same way | Interior anchor `006B2E85` |
| `006B2E90` | 9 B | stores the float `xmm1` to dword `+8` and returns `rcx`; stored to qword `02E50A28` by `006B0B20` + 0x354, and 3 other sites form it the same way | Interior anchor `006B2E95` |
| `006B3AA0` | 21 B | copies dwords `[rdx]`, `[rdx+4]` and `[rdx+8]` to dwords `+0x20`, `+0x24` and `+0x28` and returns `rcx`; stored to qword `02E51728` by `006B33F0` + 0x1D6 | Interior anchor `006B3AA2`; Interior anchor `006B3AA8`; Interior anchor `006B3AAE`; Interior anchor `006B3AB1` |
| `008AF500` | 15 B | stores the `.rdata` address `00D26BE0` to qword `01F2E0D0` and returns; passed as the `rcx` argument of the `00808B90` exit registration by `006372B0` + 0x48 | Interior anchor `008AF507` |
| `008B1D50` | 26 B | stores the `.rdata` address `00D6C378` to qword `02D3E9D0` and tail-jumps to `00633770` with `rcx` = `02D3E9D0`; passed as the `rcx` argument of the `00808B90` exit registration by `00675740` + 0x1FB | Interior anchor `008B1D57`; Interior anchor `008B1D5E`; Interior anchor `008B1D65` |
