---
system: Static initialisers and teardowns - how the image builds and unbuilds its global objects
category: 24-Compiler-And-CRT-Runtime
status: DOCUMENTED — the teardown and initialiser families measured; the owners of the 224 list heads (UQ-329), the +0x20 flag (UQ-330) and the atexit-ordering question (UQ-331: the normal quit ends in ExitProcess and never runs the chain) answered 2026-09-17; the owners of the 224 list heads (UQ-329) and the +0x20 flag (UQ-330) answered 2026-09-17
owner_layer: CodeDomain:Runtime.Static* / Phyre.Reflection static registration
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every member body disassembled from the shipping EXE and compared by instruction form
    with constants dropped; external call targets counted with intra-body branches excluded
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-static-teardown-1 - the page IS the measurement. 224 members all 82 bytes,
    186 byte images, ONE form image; exactly one external target across all of them, 00584730
    x224, which is operator delete. The unlink sequence and the conditional free are read from the
    body, not inferred.
  crossref_clean: false
  reopened_count: 0
function_families:
  - "static intrusive-list teardowns | C | members/static-intrusive-list-teardowns.tsv | 224 | not this game's code: compiler-generated static-teardown routines for objects held in an intrusive doubly-linked list. PROVED BY INSTRUCTION FORM - 224 members all 82 bytes, 186 byte images but ONE form image; what varies is the address of the list head each one unlinks from. Shape: unlink the node ([rcx+8]=rax ; [rax]=rcx), reset head and tail to point at the head itself, test a flag byte, conditionally call operator delete. CONTROL: exactly ONE external target across all 224 members - 00584730 x224. THE BOUNDARY: the teardown is emitted by the toolchain from a static object's declaration; a reconstruction declaring the same statics gets it from its own compiler. NOT dispositioned: 00584730, and whatever object each teardown destroys."
  - "empty-destructor static-teardown wrappers | C | members/empty-dtor-teardown-wrappers.tsv | 145 | not this game's code: compiler- or template-generated per-static teardown wrappers. PROVED BY FORM + REGISTRATION - 145 members, all 12 bytes, ONE instruction form (lea rcx,[a static]; jmp 0016D6A0); a census-wide scan finds exactly 185 sites of that form, every one a function entry address-taken by a .CRT$XI initialiser's lea rcx,[member] feeding the atexit wrapper 00808B90 - and BOTH spellings count (call 00808B90, or add rsp,N ; jmp 00808B90; the superseded selector matched only call, which is how the gap-40 list in _index/candidates/cfg-guard-adapter-gap-40.tsv arose). The other 40 same-form bodies are owned by sibling rows on a registration-provenance discriminator: 36 by xc-registered library teardowns (the CRT/library statics' wrappers of this form) and 4 by NativeAdapter.StaticAddressTailCall - so the form is 185-strong, this family is 145, and nothing matching the form stays frontier. 0016D6A0 IS AN ICF-FOLDED ret 0 - a shared empty destructor, not a Control Flow Guard check: every member uses the direct E9 encoding and none goes through __guard_check_icall_fptr 008C31C0, which a real guard check requires the loader to rewrite (instrumented yes, enforced no - see Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md); the family's earlier name is corrected by this row. THE BOUNDARY: each member is a fixed shape around a varying static; a reconstruction that writes the same declarations gets them from its own toolchain. SEMANTIC JOIN, not membership: 144 of the 145 are the teardown half of the declared Phyre serialization scalar-conversion initialisers pairs - that page's members/guard-adapter-registrars.tsv maps each adapter to its node, (source,destination) PType pair and routine; the 145th pairs with the generic initialiser 00165F80. The conversion-tree machinery (bootstrap lookup 0059A030, ordered-insert 0067F700 - 155 callers, shared Phyre/ordered-container code) is authored middleware, documented on the image-hardening page, and deliberately not a generated family. NOT dispositioned: the per-static object meaning; 0016D6A0 itself is declared under ScriptVM.VerbAdapter as the shared ret-0. Selector: members/select_empty_dtor_teardowns.py"
  - "float32-to-float16 static initialisers | C | members/float32-to-float16-static-initialisers.tsv | 69 | not this game's code: compiler- or template-generated. PROVED BY FORM - 69 members, all 29 bytes, 69 byte images collapse to ONE form - each converts a DIFFERENT float constant and stores to a DIFFERENT global, which is exactly the pair of constants a form comparison drops. CONTROL: exactly ONE external target, 006E0220 x69. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: 006E0220, the conversion routine itself."
  - "scalar deleting destructors that call free | C | members/scalar-deleting-destructors-free.tsv | 65 | not this game's code: compiler- or template-generated. PROVED BY FORM - 61 members, all 52 bytes, 30 byte images collapse to ONE form. CONTROL: 00809950 - the CRT free import stub - x61, one per member. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: the per-type destructor each member calls before freeing. 001C2670 left the family 2026-09-16, since measured as A (A beats a declaration). 5 member(s) left the family 2026-09-17, since measured as A (A beats a declaration): 001E1D90 00204AF0 00204BD0 00204C70 0020D010. 12 member(s) joined the family 2026-09-17: same 52-byte form, found on the live frontier by the committed selector (select_lifecycle_teardown_batch.py); the regenerated members file holds all 65, each still {free 00809950 + exactly one per-type destructor}."
  - "scalar deleting destructors via the shared base destructor | C | members/scalar-deleting-destructors-shared-base.tsv | 37 | not this game's code: compiler- or template-generated. PROVED BY FORM - 37 members, all 62 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: every member calls exactly two targets - the shared base destructor 00212CE0 x37 and the CRT free import stub 00809950 x37. Each installs the member's own vtable pointer, calls the shared base destructor, tests the deletion flag, calls free(this, size) with a member-specific size, returns this. THE BOUNDARY: the vtable immediate and the size immediate vary per member; the shape does not. NOT dispositioned: what 00212CE0 destructs, and which classes these destructors belong to. Selector: members/select_lifecycle_teardown_batch.py."
  - "scalar deleting destructors, inlined-dtor spelling | C | members/scalar-deleting-destructors-inlined-dtor.tsv | 24 | not this game's code: compiler- or template-generated. PROVED BY FORM - 27 members, all 43 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: the only external target is 00809950 (CRT free) x27 - the destructor body is inlined to a vtable-pointer store, so no destructor call remains. test dl,1 gates the free; edx carries the member-specific size. THE BOUNDARY: the vtable immediate and the size immediate vary per member. NOT dispositioned: which classes these are. Selector: members/select_lifecycle_teardown_batch.py. 3 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. A re-run of members/select_lifecycle_teardown_batch.py drops exactly these from this list and would admit 72 more; only the A departures are applied here."
  - "two-deallocator scalar deleting destructors | C | members/two-deallocator-deleting-destructors.tsv | 12 | not this game's code: compiler- or template-generated - the BQ-26 population of the two-bit deleting-dtor idiom documented in 2.1a. PROVED BY FORM - 12 members, all 66 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: every member calls exactly {00584730 x12, 0016D6A0 x12} - flags bit 0 gates deallocation, bit 2 selects the sized-delete path (edx = member-specific size; callee 0016D6A0 is the ICF-folded ret-0 shared stub per the empty-destructor row above and section 2.1a) over the _aligned_free wrapper 00584730. THE BOUNDARY: the vtable immediate and the size immediate vary per member. NOT dispositioned: which classes these are. Selector: members/select_lifecycle_teardown_batch.py."
  - "intrusive-list node-teardown loops (115-byte form) | C | members/intrusive-list-node-teardowns-115b.tsv | 43 | not this game's code: compiler- or template-generated container teardown. PROVED BY FORM - 43 members, all 115 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: each member makes exactly one external direct call - the member's node teardown, one of 00220390 (x32) or 001AF2B0 (x11) - plus one indirect call through the owner object's vtable slot [rax+0x18] which is deliberately outside the direct-target census. The loop walks the intrusive node list at [rcx] until exhaustion. THE BOUNDARY: which teardown helper and which vtable slot vary by container type; the loop skeleton does not. NOT dispositioned: the two teardown helpers, the virtual callee, and the node layout. Selector: members/select_lifecycle_teardown_batch.py."
  - "MSVC dynamic-initialiser stubs (assorted statics) | C | members/msvc-dynamic-initialiser-stubs.tsv | 43 | not this game's code: compiler-generated dynamic-initialiser stubs, the generic remainder of the 530-body 32-byte form (sub rsp,0x28 / lea rcx,[object] / call <ctor> / lea rcx,[dtor] / add rsp,0x28 / jmp 00808B90). PROVED BY FORM - ONE instruction form, only the three operands vary; every member constructs one static object and atexit-registers its teardown through the CRT wrapper 00808B90. NO COMMON OWNER, AND THAT IS THE POINT OF THIS ROW: the 44 bodies spread over 30 distinct callees across the whole image - they are one-off statics of assorted subsystems, not a registry. THE NAMED SUBSETS OF THE SAME FORM ARE THEIR OWN FAMILIES: the 319 PInputs semantic-registry initialisers (Input-Name-Registry), the 110 name-only class registrations tail-jumping 00639450 (Reflection-And-Class-Metadata), and the 56 pre-existing NameRegistryEntry initialisers (Generated-Families). THE BOUNDARY: the form is the toolchain's; a reconstruction declaring the same statics gets these from its own compiler. NOT dispositioned: the 30 callees, the per-object destructors, and the objects themselves. Selector: members/select_static_init_form.py 1 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv."
  - "registry-unlink static teardowns (95-byte form) | C | members/registry-unlink-teardowns.tsv | 327 | not this game's code: compiler-generated static-teardown routines. PROVED BY FORM + REGISTRATION PROVENANCE - 328 members, all 95 bytes, ONE skeleton (79 of 95 positions invariant); every member is the destructor operand registered by a re-derived Group-A 32-byte dynamic-initialiser, and a census-wide skeleton scan finds no unregistered twins. BODY: installs the object's vtable, walks the singly-linked registry headed at 02EA06D8 (the documented Phyre::PLOD::PLODMetricType list-head form), splices out the node, returns. SIBLING of the 224-member 82-byte doubly-linked family - different list shape, different code. THE BOUNDARY: the toolchain emits these from static object declarations; a reconstruction declaring the same statics gets them from its own compiler. NOT dispositioned: the per-object type meaning, and the shared registry semantics the list heads implement. Selector: members/select_registry_unlink_teardowns.py 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 008BCF20"
  - "atexit teardown-registration stubs | C | members/atexit-teardown-registration-stubs.tsv | 30 | not this game's code: the minimal dynamic-initialiser form - lea rcx,[teardown fn]; jmp 00808B90 - registers a static object's teardown without constructing anything (POD or elsewhere-initialised statics). PROVED BY FORM - 30 members, all 12 bytes, ONE skeleton; every lea target is a .text teardown function and every member sits in the .CRT$XI initialiser array. One sibling outside the family: 00160310 shares the skeleton but is already declared under the NativeAdapter static-address tail-call family. NOT dispositioned: the 30 teardown targets. Selector: members/select_xc_array_clusters.py"
  - "record-ctor 00662C00 static initialisers | C | members/record-ctor-00662c00-initialisers.tsv | 28 | not this game's code: compiler-generated initialisers that call the shared 3-field record ctor 00662C00 (stores {ptr,0,byte}), call the atexit wrapper, ret. PROVED BY FORM + CONTROL - 28 members, all 43 bytes, ONE skeleton, census twins zero; every member is a .CRT$XI entry whose call set is exactly {00662C00, 00808B90}. NOT dispositioned: 00662C00's record type and the 28 objects. Selector: members/select_xc_array_clusters.py"
  - "record-ctor 00616210 static initialisers | C | members/record-ctor-00616210-initialisers.tsv | 33 | not this game's code: compiler-generated initialisers calling the larger record ctor 00616210 (which delegates to the tag-dispatched init 0062CD40, cmp r8d,0x32) then tail-jumping the atexit wrapper. PROVED BY CONTROL - 33 members in three generated body shapes (77/89/91 bytes), every member a .CRT$XI entry calling exactly {00616210} and tail-jumping 00808B90; per-size skeletons have no census twins. NOT dispositioned: 00616210/0062CD40 and the 33 objects. Selector: members/select_xc_array_clusters.py"
  - "counter-append static-table initialisers | C | members/counter-append-initialisers.tsv | 18 | not this game's code: compiler-generated initialisers that append one static's address to a counted pointer table (load count, store object at head[count], bump count) then tail-jump the atexit wrapper. PROVED BY FORM - 19 members, all 54 bytes, ONE skeleton, census twins zero; every member a .CRT$XI entry. NOT dispositioned: the 19 tables and the objects they collect. Selector: members/select_xc_array_clusters.py. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the animation channel binding page (46c98f222) DOCUMENTED; exact A removal - the named selector rewrites every XC-array cluster file and is not re-run for one removal; addresses and causing pages in the record."
  - "zero-init record static initialisers | C | members/zeroinit-record-initialisers.tsv | 16 | not this game's code: compiler-generated initialisers that zero a 0x30-byte static record then tail-jump the atexit wrapper. PROVED BY FORM - 16 members, all 57 bytes, ONE skeleton, census twins zero. NOT dispositioned: the 16 records. Selector: members/select_xc_array_clusters.py"
  - "record-ctor 006D58D0 static initialisers | C | members/record-ctor-006d58d0-initialisers.tsv | 9 | not this game's code: compiler-generated initialisers calling the flag-set record ctor 006D58D0 (bts eax,0x1f marks the flag word) then tail-jumping the atexit wrapper. PROVED BY FORM + CONTROL - 9 members, all 230 bytes, ONE skeleton, census twins zero; call set exactly {006D58D0}. NOT dispositioned: 006D58D0's record type and the 9 objects. Selector: members/select_xc_array_clusters.py"
  - "callback-record 006155B0 registrars | C | members/callback-record-006155b0-registrars.tsv | 6 | not this game's code: compiler-generated registration stubs - lea r9/r8/rdx with three .text function pointers and rcx with the static object, tail-jumping the registrar 006155B0 (stores the record at [rcx+0x400]). PROVED BY FORM + CONTROL - 6 members, all 33 bytes, ONE skeleton, census twins zero; tail set exactly {006155B0}. NOT dispositioned: 006155B0 and the 18 callback targets. Selector: members/select_xc_array_clusters.py"
  - "ctor 00808FE4 callback-pair initialisers | C | members/ctor-00808fe4-initialisers.tsv | 5 | not this game's code: compiler-generated initialisers calling the multi-arg helper 00808FE4 with {object, size, flag, two function pointers} then tail-jumping the atexit wrapper. PROVED BY FORM + CONTROL - 5 members, all 60 bytes, ONE skeleton, census twins zero; call set exactly {00808FE4}. NOT dispositioned: 00808FE4 and the 10 callback targets. Selector: members/select_xc_array_clusters.py"
  - "alloc-record 0067FFB0 static initialisers | C | members/alloc-record-0067ffb0-initialisers.tsv | 8 | not this game's code: compiler-generated initialisers calling the aligned-size record ctor 0067FFB0 (lea eax,[rdx+7]; and eax,~7 - rounds a byte size to 8) then tail-jumping the atexit wrapper. PROVED BY CONTROL - 8 members in two generated body shapes (59/68 bytes); call set exactly {0067FFB0}, census twins zero. NOT dispositioned: 0067FFB0's record type and the 8 objects. Selector: members/select_xc_array_clusters.py"
  - "cloned grow-helper static initialisers | C | members/grow-helper-initialisers.tsv | 6 | not this game's code: compiler-generated initialisers calling one of the three byte-identical cloned helpers 006BFC60 / 006C2380 / 006B8D20 (sub rsp,8; mov r10,[rcx+8]; test; lea eax,[r10+0x11] - a capacity-growth head emitted per type) then tail-jumping the atexit wrapper. PROVED BY CONTROL - 12 members in two body shapes (66/86 bytes); every member's call set is a subset of the three clones, census twins zero. NOT dispositioned: the three helper bodies and the 12 objects. Selector: members/select_xc_array_clusters.py 6 member(s) left on the 2026-09-20 selector re-run, no longer derived by the selector (returned to the frontier undeclared): 00167050, 001670A0, 00167190, 001671E0, 00167230, 00167280"
  - "zero-init three-qword static initialisers | C | members/zeroinit-3q-initialisers.tsv | 3 | not this game's code: compiler-generated initialisers that zero three qwords of a static then tail-jump the atexit wrapper. PROVED BY FORM - 3 members, all 35 bytes, ONE skeleton, census twins zero. NOT dispositioned: the 3 records. Selector: members/select_xc_array_clusters.py"
  - "ctor 0060DF70 static initialisers | C | members/ctor-0060df70-initialisers.tsv | 2 | not this game's code: compiler-generated initialisers calling the record ctor 0060DF70 then tail-jumping the atexit wrapper. PROVED BY FORM + CONTROL - 2 members, all 49 bytes; call set exactly {0060DF70}, census twins zero. NOT dispositioned: 0060DF70 and the 2 objects. Selector: members/select_xc_array_clusters.py"
  - "xc-registered library teardowns | C | members/xc-registered-library-teardowns.tsv | 190 | teardowns of library/toolchain-owned statics, membership derived from REGISTRATION not form: every member is the rcx operand a .CRT$XI initialiser loads immediately before its call/jump to the atexit wrapper 00808B90, and the members TSV names that registering initialiser per row - 100% registered, zero assumed. Verified library anchors per group: 60 x jmp 005DDD60 (the documented unregister of the Phyre render-pass registry at 02CBF998) + 56 x inlined unlinks referencing 02CBF998 directly + 36 x jmp the shared ret-0 stub 0016D6A0 + 19 x jmp [IAT] resolving to KERNEL32!DeleteCriticalSection (paired with the declared CriticalSection initialisers) + 13 x unlink from the documented PUtility module list 02CACC90 + 6 x tail-jump eh_vector_destructor_iterator 00809054. Selector: members/select_xc_registered_teardowns.py"
  - "xc-registered static-object teardowns | B | members/xc-registered-static-teardowns.tsv | 107 | class-explained by REGISTRATION: every member is the rcx teardown operand a .CRT$XI initialiser registers with atexit wrapper 00808B90 - the members TSV names the registering initialiser per row, which is also the pointer to the static object the pair owns. The object owner is NOT proven library for these (GFZ labels hint at SEAD/Phyre/CRT for many but were not verified), so the honest letter is B: each is a teardown routine of a static whose identity follows from its paired initialiser. Selector: members/select_xc_registered_teardowns.py. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the authored reference lifetime page (dd651efd2) DOCUMENTED; exact A removal - the named selector rewrites every XC-array cluster file and is not re-run for one removal; addresses and causing pages in the record."
---

# Static initialisers and teardowns

> How an image with thousands of global objects builds them before `main` and takes them apart
> after it, and why that machinery is **1,000+ functions** nobody writes by hand.

## 1. What this is

A C++ image with global objects needs two things the language does not give it for free: something
to construct each object before the program runs, and something to destroy it afterwards. MSVC
emits **one small function per object for each half** and registers the second with `atexit`.

This page exists because that machinery is **large** - and because it is the clearest case in the
database of functions that must be *dispositioned* rather than *explained*. Nobody needs to read
224 unlink routines to reproduce FFXII; they need to know the pattern exists, what it does, and
that their own compiler will emit it.

## 2. The teardown family - measured, not assumed

**224 functions, every one exactly 82 bytes.** A byte comparison gives 186 distinct images; a
comparison of *instruction forms* with constants dropped gives **one**. The constant that varies is
the address of the list head.

```asm
sub  rsp, 0x38
mov  qword ptr [rsp+0x20], -2          ; EH state
mov  rcx, [<listHead>]                 ; node->prev
mov  rax, [<listHead+8>]               ; node->next
mov  [rcx+8], rax                      ; prev->next = next
mov  [rax],   rcx                      ; next->prev = prev
lea  rax, [<listHead>]
mov  [<listHead>],   rax               ; head = &head
mov  [<listHead+8>], rax               ; tail = &head   -- the list is now empty
test byte ptr [<flag>], 1
je   done
mov  rcx, [<owned>]
call 00584730                          ; operator delete
done:
add  rsp, 0x38
ret
```

**Control: exactly one external target across all 224 members**, `00584730` × 224 - which is
`operator delete` (`test rcx, rcx / jne 0019C570 / ret`, tail-calling the `_aligned_free` import
stub).

**The flag test is the part a reconstruction must not simplify.** The node is *always* unlinked; the
free is *conditional*. An object that was never heap-allocated is unlinked and not freed, and the
same routine serves both.

## 3. The initialiser half lives with what it registers

The matching initialisers are declared on
[the Phyre reflection page](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
because their bodies are Phyre-specific: **254 functions, all 53 bytes, one instruction form**, each
installing a vftable into a static descriptor and **tail-jumping to `atexit`** (`00808B90`) with its
type's teardown.

> **The two halves are not symmetric in what they leave behind.** Each initialiser **calls its own
> per-type constructor** - 254 distinct targets, one per member, all still in the frontier. The
> teardowns call **one** shared `operator delete`. So dispositioning the teardowns disposes of 224
> functions; dispositioning the initialisers disposes of 254 wrappers and leaves 254 constructors
> untouched.

### The .CRT$XI cluster sweep and what it leaves

Beyond the Phyre pair above, the twelve `function_families` rows at the top of this page declare
the remaining multi-member shape clusters inside the `.CRT$XI` array (1,172 entries) — every one a
compiler-emitted wrapper proven by decoded call/tail set plus a census-wide skeleton check
(`members/select_xc_array_clusters.py`). After all of them, **83 frontier array members in 82
distinct (size, call-set, tail-set) shapes** remain: a singleton tail with no shared form left to
declare, listed with its per-member call and tail sets in
[`members/xc-initializer-leftovers.tsv`](members/xc-initializer-leftovers.tsv). Each of those is a
one-off initialiser that needs individual reading rather than a shape family. (Four former rows —
`0016C280`/`0016C2C0`/`0016C300`/`0016C340`, the 64-byte descriptor-registration flag variant —
became a declared family on the class-descriptor page once both halves of their provenance,
ctor and teardown, were declared: see `descriptor-flag-registrars.tsv` there.)

The other direction of the table — the teardowns the initialisers register — is covered by the last
two `function_families` rows. [`members/select_xc_registered_teardowns.py`](members/select_xc_registered_teardowns.py)
decodes every `.CRT$XI` body, takes the `rcx` operand loaded immediately before the call or jump to
`00808B90`, and finds **298 frontier teardowns so registered** (superset of FABLE's 288-strong
scratch list — the image, not the list, is the authority). Of those, **190** verify a library or
toolchain anchor (the Phyre render-pass registry unregister `005DDD60` and its inlined form at
`02CBF998`, the shared `ret 0` stub, `KERNEL32!DeleteCriticalSection` through the IAT, the PUtility
module list `02CACC90`, `eh_vector_destructor_iterator`) and are declared **C**; the remaining
**108** are declared **B** — explained as a class by their registration, with each row's
registering-initialiser column carrying the audit pointer back to the object that owns it.

## 4. Modding notes

- **Do not hook a teardown to detect object destruction.** It runs at process exit, after the game
  has stopped, and it may not free anything - the flag decides.
- **The list head is the identity.** Two teardowns differ only by which head they unlink from (the owner of each head is in [`members/static-intrusive-list-teardown-owners.tsv`](members/static-intrusive-list-teardown-owners.tsv), §5 UQ-329), so
  the head address is the only way to tell which object a given routine belongs to.
- A reconstruction **declares the statics and gets all of this from its own toolchain.** Reproducing
  these 478 functions by hand would be reproducing the compiler.

## 5. What is not known

- [x] ~~**UQ-329.** Which object each of the 224 list heads belongs to. The heads are known by address; the
      objects are not named.~~
      ***ANSWERED 2026-09-17 (FABLE): every head is a node of the Phyre reflection registry, and the owner of each is named in [`members/static-intrusive-list-teardown-owners.tsv`](members/static-intrusive-list-teardown-owners.tsv).** Each of the 224 teardowns is passed to `atexit` by exactly one of 51 class-registration functions (the `lea` census over every rip-relative operand in `.text`), and every registration sits inside MSVC's thread-safe static guard (`_Init_thread_header` `008092FC` and `_Init_thread_footer` `0080929C` around a guard dword), so the objects are function-local statics built on first use. 216 of the heads are name nodes: the block calls `00632FB0(node, owner, name, flags)`, which self-links prev and next, stores the owning class descriptor at `+0x10`, the name string at `+0x18` and the flags dword at `+0x20` (`00632FBA`..`00632FCF`), then links the node into the owner's list at `+0xA0` unless a same-named entry is already there (`005A03CD`..`005A0406` in the first initialiser), and registers the teardown. The names are method names (`GetTime`, `appendAnimation`, `compile`, `getAnimationChannel`, and so on) and the 47 owners are the `PClassDescriptor` statics of Phyre classes, read from the vftable each owner has installed: `PClassDescriptorConcrete` for 151 of the nodes (PAnimationSet, PAnimationClip, PNode, PLight, PMesh, PPhysicsRigidBody, PCamera, PEntity and others), `PClassDescriptorWithoutDefaultConstructor` for 32 (PMaterial, PMeshInstance, PScheduler and others), `PClassDescriptorWrapper` for 18 (PTimer, Vector2, Vector3, Point3, Vector4, Quat, PMatrix4x3) and `PClassDescriptorForType` for 15 (PApplication, PCameraProjection). The other 8 heads are the `.data` nodes (`01F2DFB0`..`01F2E7B0`) that four registration functions (`00634830`, `00635470`, `00635980`, `00635B80`) append inline to five global lists (`02CF8500`, `02CF8818`, `02CF8A10`, `02CF8A20`, `02CF8B10`), each list referenced by no other function. The heads live in `.bss` (216) or zero `.data` (8), which is why the file image shows no list. Static; 224 of 224 attributed.*
- [x] ~~**UQ-330.** What the flag byte at `<listHead+0x20>` is set by, and whether any shipped object ever takes
      the free path. **The branch is read from the body; neither arm has been observed taking.**~~
      ***ANSWERED 2026-09-17 (FABLE): the flag is bit 0 of the node's flags dword, stored by `00632FB0` from the constant its caller passes, it means the name was copied to the heap, and no shipped static sets it, so the free path is never taken.** `00632FB0` stores its fourth argument at `+0x20` (`00632FCF`) and, when bit 0 is set, measures the name, allocates a copy through `0017D260`, copies it and stores the copy at `+0x18` (`00632FD3`..`00633026`); the teardown's `test byte [head+0x20], 1` and `operator delete([head+0x18])` free exactly that copy. No other code references any of the 224 flag bytes (rip-target census). The constant that reaches `00632FB0` was resolved at every site inside the 51 registration functions: 216 direct calls pass `r9d` = 0; the 175 calls through the data-member constructors `00632960`, `00632A10`, `00632A70`, `00632BE0` and `00668E10` pass their sixth argument, a constant 0, 2, 8, 10, 16 or 18 (`00632BE0` adds 0x20), and `00632B30` masks bit 0 off (`00632B89`); the eight `.data` nodes are built inline with the flag left at its zero image value. Image-wide, all 1,067 sites into the node initialiser resolve to constants without bit 0 except the constructors that forward their own argument, so a heap-copied name arises only for descriptors created at run time from non-literal names, never for these statics. Static; nothing executed.*
- [x] ~~**UQ-331.** Whether `atexit` ordering matters to anything in this image.~~
      ***NARROWED 2026-09-17 (FABLE): for this family the order cannot matter, because every teardown touches static storage only and frees nothing.** Each of the 224 unlinks one node (prev's next and next's prev rewritten, then the node pointed at itself) whose storage is `.bss` or zero `.data` (UQ-329), and its only free is the never-taken name copy (UQ-330). A neighbour torn down earlier is a self-linked node in static storage, not freed memory, and the owner descriptors are statics that none of these routines destroys, so the writes land in live storage whichever order the C runtime chooses (registrations run last-in first-out). Open is the image-wide half: whether any other registered teardown reads state a peer has already torn down, which needs the remaining `atexit` families read, and whether the process reaches the `atexit` chain at all rather than ending in `ExitProcess`, a termination-path question outside this page.*
      ***ANSWERED 2026-09-17 (FABLE): it cannot matter on the normal quit, because that quit never runs the chain; it can matter only on the paths that call the CRT's `exit`, and within this family not even there.** The atexit wrapper `00808B90` is the CRT's `atexit` over `_onexit` `00808B40` (the `neg` / `sbb` / `neg` / `dec` normalisation of its result), which registers into the executable's own onexit table through the runtime imports `_initialize_onexit_table` and `_register_onexit_function`; that table is drained only by the runtime's `exit` (`_cexit`, or the return from the entry point). The entry `007980A0` ends the normal quit elsewhere: after the message loop leaves on `WM_QUIT` (`0079869A`), it runs the game's own teardown (`0061C540`, `005FE190`, `005A0840`), closes its handles, frees its arguments, and calls `ExitProcess(0)` at `0079887F` (`xor ecx, ecx` at `0079887D`), or relaunches itself through `CreateProcessA` (`00798817`) and then `ExitProcess`; it never returns and never calls `exit` on that path. `ExitProcess` terminates the process without the runtime's exit sequence, so the table the 224 teardowns and every other registrant sit in is not executed on a normal quit (a reading of the documented runtime, tier 6, joined to the image's own call). The runtime's `exit` is reached at nine sites only: `0079814B`, when `SteamAPI_RestartAppIfNecessary` reports a restart at start-up, before anything below has been constructed, and eight error exits in `00369860`, `0036B670`, `0036B730`, `0036B7F0`, `0036B8B0`, `0036CB00` and `008272D0`. On those paths the chain runs last-registered first, and for this family the order is harmless (the narrowing above: static storage only, nothing freed). So the ordering question has no shipped consequence outside a start-up restart or a fatal error, and none within this family at all. Static; the entry read with its imports resolved.*

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

Five crossings are reported against this page, thirteen edges, and **eleven of them are fan-out from
one citation**. This section accounts for all five, and two of the thirteen turn out to be facts the
page was missing rather than noise.

**Where they come from.** §5 cites the entry `007980A0` to explain why the atexit chain never runs on
the normal quit. That function is not a static initialiser — it is the program's **main body**, 2,153
bytes, reached from the SEH-guarded wrapper `007A3770` (`007A377E`/`007A378D`) below the CRT entry
`00808EE4`, and it makes **56 direct calls**. Citing it by entry therefore imports every layer it
touches, which is the whole of the game's startup.

**ELEVEN EDGES ARE STARTUP, NOT THE CITED CLAIM.** The quit tail this page cites begins at the
`WM_QUIT` test `0079869A` (`cmp dword [rbp-0x68], 0x12`). Every one of these calls is **before** it:

| layer | call sites inside `007980A0` |
|---|---|
| PlatformOnlineAchievements | `0079812D` → `0020CD30`, `00798162` → `0079FA00`, `007981EA` → `001F3ED0` |
| Save_Load_Settings | `00798257` → `001DE050`, `0079826B` → `001DED50` |
| Platform | `00798291`, `007982C2`, `007983A4`, `007983D0` → `0019A510`; `007985F6` → `007979B0` |
| Input | `0079861A` → `0079E520` |

**This page owns nothing in any of them.** They are `main` calling each subsystem's own
initialisation, and the mechanism this page documents — the `__xc` tables and the `atexit` chain — is
precisely the mechanism these calls **do not** use. That is the point of the §5 sentence they were
imported by.

**TWO EDGES ARE ON PATHS THIS PAGE DOCUMENTS, AND IT DID NOT NAME THEM.**

- **`007986AB` → `0020CD80` (PlatformOnlineAchievements) is inside the quit tail**, between the
  `WM_QUIT` test and the game teardown `0061C540` this page already names — `007986A5` calls an
  import with `0x80000000`, then `007986AB`, then `007986B0` → `00865660`, then `007986BF` →
  `0061C540`. So the normal quit runs an online-layer call **before** the teardown sequence §5
  describes, and the description stopped short of it.
- **`005A0840` → `00677520` (Resource).** `005A0840` is one of the three teardowns §5 names; this is
  its own call into the resource layer.

Both are **CLIENT** crossings: the shutdown path consults those layers, and neither layer owns
anything here. Naming them is the accounting; it is also two steps of the normal quit that this
page's own account was missing.

*Method note, because it is the reusable part: citing a shared entry imports all of its callees'
layers. The fix here was not to withdraw the citation but to say which region of the body the claim
concerns — `0079869A` onward — and to check every imported edge against that boundary. Eleven fell
outside it and two did not, and the two that did not were worth having.*

## 6. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 224 members, one instruction form, 82 bytes each | `family_prover.py --forms` over the tagged frontier group; 186 byte images collapse to 1 | 1 |
| exactly one external target, `00584730` × 224 | external call/jmp census with intra-body branches excluded | 1 |
| `00584730` is `operator delete` | its complete 10-byte body: `test rcx, rcx / jne 0019C570 / ret`, and `0019C570` is the `_aligned_free` import stub resolved through the PE import directory | 1 |
| the unlink sequence and the conditional free | the complete body above, read instruction by instruction | 1 |

## 7. Related

- [`../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md) - the import stub `00584730` tail-calls, and where `_aligned_free` was resolved
- [`../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) - the initialiser half, and the four other generated reflection families

## SWE2-EC7-19 update (2026-05-15) — `00632BE0` ICF-folded `??_G` cluster window

`00632BE0` (170 B) is the sibling constructor in the same family as batch-17's `00632C90`: it base-constructs `rbx = rcx+8` via `00632FB0` with the `[rsp+0x78]` flags `| 0x20` (`00632C10`..`00632C1F`), stores `[rbx+0x28] = r8`, self-links the `+0x38` node, and installs vtable `00D580B0` (RTTI locator → `01D14A40`) (`00632C24`..`00632C3A`). After saving `dword[r14+0x28]` it runs the `[[rsi]+0x40]` post-construction hook on `rsi` and restores the dword (`00632C4D`..`00632C60`), then re-patches the vtable to `00D580D8` (the "PAc"-family vtable) and stores `[r14+0x58] = [rsp+0x80]` (`00632C64`..`00632C75`), returning `r14` — the derived layer completing its own construction over the base's vtable row.

## SWE2-EC7-34 update (2026-09-19) - `0059A030`

`0059A030` (884 B) is the static-init driver - the `02CA9D91` once-flag gate, then 17 sequential `0059xxxx` init calls (`00592770` through `0059A368`). Interior anchor `0059A04D` (the `00592770` call).

## SWE2-EC7-35 update (2026-09-19) - `0067F700`

`0067F700` (712 B) is the call-free CRT `_Tree` node relink - `byte[+0x10]&1` nil-flag walk, pointer-chasing `[[rcx+0x10]]` compares, the MSVC tree rebalance skeleton. Interior anchor `0067F730` (the loop-head byte test).

## SWE2-EC7-113 update (2026-09-21) - `00865660` measured

`00865660` (73 B) is the
`02EB3860` singleton
teardown `007980A0` runs:
when the global is live the
object's vtable relatches to
`01CCFBC0` (RTTI
`01D496F0`, slot 0
`00865550`), a set bit 0 of
`byte[+8]` runs the IAT
import `008C3178`
(`01CCBFFE`) on it, the
0x20 block goes back through
`00809950`, and the global
zeroes - the
destruct-and-detach order a
static object's teardown
needs.
Interior anchor `00865693`
(the `00809950` free call).

## SWE2-EC7-114 update (2026-09-21) - `007A4240` / `007A3D70` measured

`007A4240` (9 B) is the
two-field latch `007980A0`
runs on the application
object: `qword[+0x20] = rdx`
and `byte[+0x28] = 1` - the
same `+0x20`/`+0x28` pair
`007A4250`'s thread-create
initialises, written here
with the thread argument.
Interior anchor `007A4244`
(the `+0x28` flag store).

`007A3D70` (65 B) is the
mode-select `0079E520` runs:
`edx` clamps into
`{0, 1, 2}` (anything above
2 answers slot 0), the
chosen `qword[+ecx*8]`
object parks at `+0x30`, its
`vtable[+0x10]` runs, and
the tail jumps
`vtable[+0x18]` - a three-
slot mode swap with paired
enter/exit virtuals.
Interior anchor `007A3D93`
(the `+0x30` select store).

## SWE2-EC7-115 update (2026-09-21) - `007979B0` measured

`007979B0` (101 B) is the
CPU-count step `007980A0`
runs: IAT `008C21B8` gets
the current process,
`008C2230` reads the
affinity mask, a
`rcx & (rcx-1)` loop
popcounts it, and a zero
mask falls back to
`008C2220` (system info,
`[rsp+0x40]`); a count
above 1 goes to `005A0AE0`.
The worker-count decision
the app init consults.
Interior anchor `007979E4`
(the popcount loop).
