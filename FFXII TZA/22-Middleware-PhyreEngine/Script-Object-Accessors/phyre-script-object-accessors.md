---
system: Phyre script object accessors — the type-checked script→engine object bridge
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain — Phyre.ScriptVM.ObjectPointerAccessor / ObjectReferenceAccessor
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 1
function_families:
  - "script-VM object push adapters | C | members/object-push-adapters.tsv | 304 | not this game's code: PhyreEngine generated adapters, one per bound type. PROVED BY BYTES AND RESTRICTED BY THEM - two variants of one idiom: 188 at 21 B push the object directly; 116 at 31 B add a member offset with a null guard (cmove to 0) and differ ONLY in that offset immediate - 8, 1, 0x30, 0x10 - which is why a mask over call/lea operands alone reports them as four shapes; all 304 tail-jump to ONE target, 00684080. 1 member(s) of the tag group are EXCLUDED BY ADDRESS because they are a different idiom: 0063A110 (51 B) makes a VIRTUAL call through [rcx+8] instead of pushing directly; it is a different idiom and is excluded. THE BOUNDARY: each member adds a constant offset and delegates; a reconstruction that binds the same types gets these from the same generator. NOT dispositioned: the shared implementations they delegate to, and whatever object or member each adapter names."
  - "optional-pointer context dispatch adapters | C | members/optional-pointer-context-dispatch-adapters.tsv | 70 | not this game's code: compiler- or template-generated. PROVED BY FORM - 70 members, all 80 bytes, ONE byte image across all 70. CONTROL: the SAME three targets as the nullable push adapters on this page - 00684080, 0080F420 and 00810620 - each x70, plus ONE member-specific target each (73 distinct targets in all; verified per member under OPUS-NOTE-SWE2-EC7-OPTPTR-CONTROL-ABRIDGED). THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: those three shared implementations and the 70 member-specific targets - this row disposes of the adapter, not the adapted."
  - "context-acquire three-argument dispatch adapters | C | members/context-acquire-three-arg-dispatch-adapters.tsv | 70 | not this game's code: compiler- or template-generated. PROVED BY FORM - 70 members, all 47 bytes, ONE byte image across all 70. CONTROL: 00684080 x70 shared, plus ONE member-specific target each. THE BOUNDARY: each member is a fixed shape around a varying constant or target, and a reconstruction that writes the same declarations gets it from its own toolchain. NOT dispositioned: 00684080 and the 70 member-specific targets - this row disposes of the adapter, not the adapted."
  - "script-VM object pointer accessors | C | members/object-pointer-accessors.tsv | 323 | not this game's code: PhyreEngine generated accessors, one per bound field. PROVED BY INSTRUCTION FORM RATHER THAN BYTES, which is a weaker claim and is stated as one - a byte comparison gives 323 distinct images because each member carries its own FIELD OFFSET, while comparing decoded forms with constants dropped collapses the group to TWO forms matching its two body sizes (301 B (203) and 302 B (120)), with 75 instructions in both variants. CONTROL, external targets only with intra-body branches excluded: 00811130 x646, 00812960 x646, 008119F0 x646 and 00682980 x323 - three at exactly TWICE the member count and one at exactly ONCE. WHAT VARIES within a form is the field offset and the type descriptor address; a form match is evidence of a shared shape and NOT evidence that the constants are irrelevant - here they are the whole payload. THE BOUNDARY: a reconstruction binding the same fields gets these from the same generator. NOT dispositioned: the four shared implementations, and whatever field each accessor reaches."
  - "script-VM object reference accessors | C | members/object-reference-accessors.tsv | 264 | not this game's code: PhyreEngine generated accessors, one per bound field. PROVED BY INSTRUCTION FORM RATHER THAN BYTES, which is a weaker claim and is stated as one - a byte comparison gives 264 distinct images because each member carries its own FIELD OFFSET, while comparing decoded forms with constants dropped collapses the group to TWO forms matching its two body sizes (249 B (160) and 282 B (104)), with 55 and 64 instructions. CONTROL, external targets only with intra-body branches excluded: 00812960 x528, 00682980 x264, 00811130 x264 and 0063BC00 x264 - one at exactly TWICE the member count and three at exactly ONCE. WHAT VARIES within a form is the field offset and the type descriptor address; a form match is evidence of a shared shape and NOT evidence that the constants are irrelevant - here they are the whole payload. THE BOUNDARY: a reconstruction binding the same fields gets these from the same generator. NOT dispositioned: the four shared implementations, and whatever field each accessor reaches."
  - "script-VM nullable object push adapters | C | members/nullable-object-push-adapters.tsv | 295 | not this game's code: PhyreEngine generated adapters, one per bound type. PROVED BY BYTES AND RESTRICTED BY THEM - one idiom: load the pointed-to object, branch to a null push when it is null, otherwise add the member offset and push. The sub-shapes differ only in that offset immediate (none, 8, 1, 0x30, 0x10); all 295 reach the same three targets - 00684080, 0080F420 and 00810620 - EXACTLY 295 times each, one per member. 4 member(s) of the tag group are EXCLUDED BY ADDRESS because they are a different idiom: four members are different idioms and are excluded: 0063D010 (71 B) and 0063D3C0 (68 B) take a DYNAMIC offset from the class descriptor at [rcx+0xF4] rather than a constant; 006A9D10 (57 B) loads a further indirection; 0079A6C0 (91 B) makes a virtual call and moves 16 bytes. THE BOUNDARY: each member adds a constant offset and delegates; a reconstruction that binds the same types gets these from the same generator. NOT dispositioned: the shared implementations they delegate to, and whatever object or member each adapter names."
  - "optional-pointer context dispatch adapters, static-descriptor spelling | C | members/optptr-static-descriptor-dispatch-adapters.tsv | 16 | not this game's code: compiler- or template-generated. PROVED BY FORM - 16 members, all 60 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: no registry getter - a member-specific static descriptor is lea'd into r8 and [r8] is tested directly; non-null tail-jumps to the member forwarder thunk (00684080 x11, its clone 00684090 x5), else calls 0080F420 and tail-jumps 00810620. Sibling spelling of the 80-byte optional-pointer row above, which fetches via a member getter. CONTROL: 0080F420 x16 and 00810620 x16 shared, plus 00684080/00684090 shared - every member reaches exactly one of the two cloned thunks. THE BOUNDARY: the member descriptor varies; the dispatch shape does not. NOT dispositioned: the three shared implementations and the member descriptors - this row disposes of the adapter, not the adapted. Selector: members/select_optptr_dispatch_siblings.py"
  - "member-vcall optional-pointer dispatch adapters | C | members/member-vcall-optptr-dispatch-adapters.tsv | 12 | not this game's code: compiler- or template-generated. PROVED BY FORM - 12 members, all 119 bytes, ONE operand-aware byte image and ONE instruction-form skeleton: call a member-specific getter on rdx, indirect-call [rdi+8] on its result, then the same optional-pointer dispatch as the rows above with a member-specific descriptor; returns 1 in every path. CONTROL: the SAME three shared targets - 00684080, 0080F420 and 00810620 - each x12, plus ONE member-specific getter each (10 distinct). THE BOUNDARY: the getter and descriptor vary per member; the dispatch shape does not. NOT dispositioned: the three shared implementations, the member getters, and the member descriptors - this row disposes of the adapter, not the adapted. Selector: members/select_optptr_dispatch_siblings.py"
  - "optional-pointer offset-add dispatch adapters, 64-byte form | C | members/optptr-offsetadd-dispatch-adapters.tsv | 8 | not this game's code: compiler- or template-generated - sibling spelling of the static-descriptor optional-pointer row above: rdx=[r8]+member displacement and r8=a member-specific record; non-null tail-jumps shared 00810620, else calls 0080F420 with edx=0x19 and tail-jumps a cloned forwarder (00684080 x6, 00684090 x2). PROVED BY FORM - 8 members, all 64 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x8 and 00810620 x8 shared, plus 00684080/00684090 shared - every member reaches exactly one of the two cloned thunks. NOT dispositioned: the shared implementations and the member records - this row disposes of the adapter, not the adapted. Selector: members/select_optptr_dispatch_siblings_2.py"  # <- corrected 2026-10-02, OPUS - branch sense: the null path calls 0080F420 with edx=1 then tail-jumps 00810620 (lua_pushnil), the non-null path tail-jumps the forwarder (005A0ED2-005A0EFB)
  - "optional-pointer member-call dispatch adapters, 75-byte form | C | members/optptr-membercall-dispatch-adapters.tsv | 8 | not this game's code: compiler- or template-generated - sibling spelling: rdi=[r8] saved, a member-specific op is called, and the non-null path tail-jumps shared 00810620 with rdx=rdi while the null path calls 0080F420 (edx=0x19) and tail-jumps a member-specific op. PROVED BY FORM - 8 members, all 75 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x8 and 00810620 x8 shared, plus member-specific ops (00684130 x2 subset-shared, 6 distinct others). NOT dispositioned: the shared implementations and the member-specific ops - this row disposes of the adapter, not the adapted. Selector: members/select_optptr_dispatch_siblings_2.py"  # <- corrected 2026-10-02, OPUS - branch sense: null calls 0080F420 with edx=1 and tail-jumps 00810620, non-null tail-jumps the member forwarder with rdx=rdi (006B2B8B-006B2BB6)
  - "optional-pointer member-call result-dispatch adapters, 78-byte form | C | members/optptr-membercall-resultdispatch-adapters.tsv | 6 | not this game's code: compiler- or template-generated - the 75-byte sibling plus one more move: the member call's result is forwarded in r8 to the true-path tail 00810620; the null path calls 0080F420 (edx=0x19) and tail-jumps the cloned forwarder 00684080. PROVED BY FORM - 6 members, all 78 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x6, 00810620 x6 and 00684080 x6 shared, plus member-specific ops (5 distinct). NOT dispositioned: the shared implementations and the member-specific ops. Selector: members/select_optptr_dispatch_siblings_2.py"  # <- corrected 2026-10-02, OPUS - branch sense: null calls 0080F420 with edx=1 and tail-jumps 00810620, non-null tail-jumps 00684080 (005A0B9B-005A0BC9)
  - "optional-pointer member-call vcall dispatch adapters, 87-byte form | C | members/optptr-membercall-vcall-dispatch.tsv | 7 | not this game's code: compiler- or template-generated - sibling spelling: a member op on rdx, an indirect member vcall on its result, then on the non-null path call shared 00810580 with edx=0x10 followed by a member op; returns 1 in every path. PROVED BY FORM - 7 members, all 87 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x7 and 00810580 x7 shared, plus member-specific ops (7 distinct). NOT dispositioned: the shared implementations and the member-specific ops. Selector: members/select_optptr_dispatch_siblings_2.py"
  - "optional-pointer member-call forward adapters, 45-byte form | C | members/optptr-membercall-forward-adapters.tsv | 6 | not this game's code: compiler- or template-generated - the forward-only sibling: call a member op, then tail-jump the cloned forwarder 00684080 with (rdx, result-in-r8, rdi). PROVED BY FORM - 6 members, all 45 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 00684080 x6 shared, plus member-specific ops (6 distinct). NOT dispositioned: the shared forwarder and the member-specific ops. Selector: members/select_optptr_dispatch_siblings_2.py"
  - "tagged out-record member vcall adapters, 94-byte form | C | members/tagged-outrecord-vcall-adapters.tsv | 8 | not this game's code: compiler- or template-generated - leaf adapter: a member indirect vcall on rdx; if the out pointer equals a member-specific rip tag or-ed with 1, store the result record {1, rcx} into it; return 1 on store, 0 otherwise. PROVED BY FORM - 8 members, all 94 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: no direct external targets - member identity is carried by the indirect vcall and the member tag. NOT dispositioned: the member vcall targets and tags. Selector: members/select_optptr_dispatch_siblings_2.py"
  - "tagged out-record member vcall advance adapters, 113-byte form | C | members/tagged-outrecord-vcall-advance-adapters.tsv | 6 | not this game's code: compiler- or template-generated - the 94-byte sibling with an incremented input field (add [rax+0x30],1) before the member vcall; same tagged out-record store and return convention. PROVED BY FORM - 6 members, all 113 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: no direct external targets. NOT dispositioned: the member vcall targets and tags. Selector: members/select_optptr_dispatch_siblings_2.py"
  - "descriptor-forward tail-call adapters, 21-byte form | C | members/nativeadapter-descriptorforwardtailcall.tsv | 5 | not this game's code: compiler- or template-generated - the minimal spelling of the descriptor-forward idiom: shuffle (this=arg1->rcx, arg3->rdx), lea a member-specific static descriptor into r8, tail-jump the cloned forwarder 00684080. PROVED BY FORM - 5 members, all 21 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton. CONTROL: 00684080 x5 shared; member identity is the lea'd descriptor. NOT dispositioned: the shared forwarder and the member descriptors. Selector: members/select_optptr_dispatch_siblings_3.py"
  - "optional-pointer member-call + cloned-forward, 103-byte form | C | members/nativeadapter-optptrmembercallvcallforward.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 103 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: call a member lookup on arg1; vcall [this+8] slot on the result; if  non-null forward via cloned forwarder 00684090 with a member rip  descriptor; else shared 0080F420 + 00810620 fallback; return 1. CONTROL: 7 external target(s): 2 shared across all 4 members (0080F420, 00810620), 5 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 0080F420/00810620. Selector: members/select_optptr_dispatch_siblings_4.py"
  - "optional-pointer alloc + record install, 104-byte form | C | members/nativeadapter-optptrallocrecordinstall.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 104 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: push arg1 onto the optptr stack via shared 0080F420; allocate a 0x10  record via shared 00810240; install member rip descriptor + arg3; call  shared 0080FA50 with a member tag; tail shared 00810F60 with edx=-2. CONTROL: 4 external target(s): 4 shared across all 4 members (0080F420, 0080FA50, 00810240, 00810F60). NOT dispositioned: the shared implementation(s) 0080F420/0080FA50/00810240/00810F60. Selector: members/select_optptr_dispatch_siblings_4.py"  # <- corrected 2026-10-02, OPUS - 0080F420 is lua_checkstack (0080F42E-0080F457, limit 0xF4240) and pushes nothing
  - "optional-pointer member-offset vcall, 120-byte form | C | members/nativeadapter-optptrmemberoffsetvcall.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 120 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: call member ops 005BCD20 + 005BC4D0-shape on arg1; if non-null vcall  [this+8] at member offset +[this+0x10]; then shared 0080F420 + 00810580  pop/store; return 1. CONTROL: 8 external target(s): 2 shared across all 4 members (0080F420, 00810580), 6 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 0080F420/00810580. Selector: members/select_optptr_dispatch_siblings_4.py"
  - "optional-pointer member-call cloned forward, 80-byte form | C | members/nativeadapter-optptrmembercallclonedforward.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 80 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: call a member lookup on arg1; if non-null vcall [this+8]; forward via  cloned forwarder 00684080 with a member rip descriptor; return 1. CONTROL: 4 external target(s): 1 shared across all 4 members (00684080), 3 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00684080. Selector: members/select_optptr_dispatch_siblings_4.py"
  - "optional-pointer float-pipeline lookup, 171-byte form | C | members/nativeadapter-optptrfloatpipelinelookup.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 171 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: run shared 00811470 + 0080F420 + 00810620 on arg1; if non-null vcall  [this+8] slot on it; if still non-null forward via cloned 00684080 +  shared 00811130; return 1 else shared fallback path. CONTROL: 8 external target(s): 5 shared across all 4 members (00684080, 0080F420, 00810620, 00811130, 00811470), 3 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 00684080/0080F420/00810620/00811130/00811470. Selector: members/select_optptr_dispatch_siblings_4.py"
  - "optional-pointer member-call vcall result, 116-byte form | C | members/nativeadapter-optptrmembercallvcallresult.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 116 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: call member ops on arg1; if non-null vcall [this+8] on the second  result; then shared 0080F420 + 00810580; return 1. CONTROL: 9 external target(s): 2 shared across all 4 members (0080F420, 00810580), 7 member-specific or subset-shared. NOT dispositioned: the member-specific targets; the shared implementation(s) 0080F420/00810580. Selector: members/select_optptr_dispatch_siblings_4.py"
  - "tagged out-record vptr store, 103-byte form | C | members/nativeleaf-taggedoutrecordvptrstore.tsv | 4 | not this game's code: compiler- or template-generated. PROVED BY FORM - 4 members, all 103 bytes, 4 byte image(s) collapsing to ONE instruction-form skeleton: if arg1 non-null vcall [this+8] at member offset +[this+0x10] on  arg1-8+index; if arg3 matches a member rip|1 tag, store the result into  the out record and return 1 else 0. CONTROL: 0 external target(s). NOT dispositioned: nothing beyond the members themselves. Selector: members/select_optptr_dispatch_siblings_4.py"
  - "float-pipeline member vcall adapters, 121-byte form | C | members/nativeadapter-floatpipelinevcalladapter.tsv | 5 | not this game's code: compiler- or template-generated - the float-valued sibling of the object-accessor adapters: run shared float helpers 00811640 (or edx,-1) and 00811130 on arg1 keeping xmm6, look the object up via shared 00683BF0; if non-null vcall [this+8] slot 1 with xmm1=saved float, then call a member-specific op and return 1. PROVED BY FORM - 5 members, all 121 bytes, 5 byte image(s) collapsing to ONE instruction-form skeleton. CONTROL: 00811640 x5, 00811130 x5 and 00683BF0 x5 shared, plus ONE member-specific op each (00684280, 00684300, 00684360, 006843D0, 00684450). NOT dispositioned: the shared implementations and the member-specific ops. Selector: members/select_optptr_dispatch_siblings_3.py"
---

# Phyre script object accessors

**747 functions identified by name, from one header, in one pass.** Each one is a generated
`PObjectAccessor<T>::Get` that takes an object handed over by a Lua script and checks it really is a
`T` before the engine touches it.

## 1. What the player sees

Nothing, when it works — which is the point.

A zone script says *give me this camera*, *give me this light*, *give me that animation clip*. Between
the script asking and the engine acting sits a small generated function whose only job is to answer
**"is the thing the script handed me actually the type I need?"** If yes, the engine proceeds. If no,
**it refuses and says exactly what it got instead**:

```
Object obtained from script was of type "%s" when an object of type "%s" was required.
Object obtained from script was not a Phyre Object when an object of type "%s" was required.
Unable to obtain object pointer from script - found another type of data instead (Lua type %d)
```

**This is the guard rail that keeps a mistyped script from corrupting the engine rather than crashing
it.** A script that asks for a light and is handed a mesh does not produce a garbage render or a
silent wrong result; it produces a refusal naming both types. For a player, the difference is between
a scripted event that visibly fails and one that quietly corrupts the scene it was meant to set up.

**412 distinct engine types are reachable from script this way** — cameras, lights, mesh instances,
animation clips, physics bodies, render passes, serialization clusters.

## 2. Native mechanism

Each accessor is a template instantiation of `Phyre::PScripting::PScriptAccessors::PObjectAccessor<T>`
from a single header. **They come in exactly two shapes**, and the shape is visible three independent
ways (the type name, the diagnostic text, and the source line).

```asm
00599770  PObjectAccessor<Phyre::PSerialization::PBinary::PClusterHeader &>::Get
00599780  call FUN_00682980          ; luaL_testudata(L, idx, "PhyreObject") - corrected 2026-09-13, was "fetch the script value"
00599790  call FUN_00811130          ; lua_settop - corrected 2026-09-13, was "resolve it"
00599798  je   0x599810              ; nothing there at all -> second assert site
0059979A  mov  r8,  [rbx]            ; the object's class descriptor
0059979D  mov  rbx, [rbx + 8]
005997A9  lea  rdx, [rip + ...]      ; the REQUIRED class descriptor
005997B0  cmp  rcx, rdx              ; walk the base-class chain
005997B3  je   0x59985b              ;   match -> accept
005997B9  mov  rcx, [rcx + 0x78]     ;   else follow ->base
005997C0  jne  0x5997b0
      ; --- fell off the chain: it is not a T ---
005997C9  lea  rax, [rip + ...]      ; __FILE__
005997D0  mov  [rip + ...], rax      ;   -> 02E41000
005997E5  mov  dword [rip + ...], 0x8f   ; __LINE__ = 143   -> 02E41008
005997EF  mov  [rip + ...], rax      ; __FUNCTION__          -> 02E41010
005997FD  call FUN_00812960          ; report
```

**The type check is a base-class chain walk**, not an equality test: `[descriptor + 0x78]` is the
pointer to the base descriptor, followed until it matches the required one or runs out. So a
**derived** object is accepted where a base is required, which is the correct C++ semantic.

### Why the function names are recoverable at all

**Every one of these functions writes its own fully-qualified C++ name into a global before
reporting.** That is what makes this a naming pass rather than a structural one — the binary states
each function's identity in its own body:

```
'Phyre::PScripting::PScriptAccessors::PObjectAccessor<class Phyre::PSerialization::PBinary::PClusterHeader &>::Get'
```

The mapping is a **clean bijection**, over the wider `Phyre::`-prefixed string set the extraction
used: **751 functions, 751 strings**, each function referencing exactly one string and each string
referenced by exactly one function, twice. **747 of those 751 are `PObjectAccessor`** — the other
four are a different mechanism (§7, AZ-3). An independent scan of the authorized EXE for
NUL-terminated ASCII containing `PObjectAccessor` returns exactly **747**, so the accessor population
is 747 and the bijection population is 751; every count below states which.

## 3. Key addresses

**The assert record** — one 24-byte global triple, written by **747 of 751** functions at **1,494
sites**, exactly two per function:

| address | width | field |
|---|---|---|
| `0x02E41000` | qword | `__FILE__` pointer |
| `0x02E41008` | dword | `__LINE__` |
| `0x02E41010` | qword | `__FUNCTION__` pointer |

**The single source file**, for all 747:

```
e:\jenkins\workspace\c11019p16003\middleware\phyreengine\include\Scripting/PhyreScripting.inl
```

**Representative accessors** (full list: `Tools/work/rtti/phyre_xrefs.tsv`, 1,498 rows):

| address | bound type |
|---|---|
| `00599770` | `Phyre::PSerialization::PBinary::PClusterHeader &` |
| `00599870` | `Phyre::PSerialization::PBinary::PClusterHeaderBase &` |
| `005B98D0` | `Phyre::PAnimation::PAnimationClip &` |
| `005BCE50` | `Phyre::PAnimation::PAnimationClipBinding *` |
| `005B9180` | `Phyre::PSharray<Phyre::PAnimation::PAnimationClip *> &` |
| `005F0E90` | `Phyre::PArray<Phyre::PRendering::PSceneRenderPass *, 8> &` |
| `005F10B0` | `Phyre::PArray<Phyre::PRendering::PLightType const *, 8> &` |
| `005F1710` | `Phyre::PArray<Phyre::PRendering::PNodeContext, 8> &` |

## 4. Data structures and formulas

**The two variants, and three independent features that agree on the split:**

| | pointer accessor | reference accessor |
|---|---|---|
| type name ends | `<T *>::Get` | `<T &>::Get` |
| **count by type name** | **402** | **345** |
| assert lines in `PhyreScripting.inl` | **106 and 118** | **141 and 143** |
| first message | `Unable to obtain object pointer from script - found another type of data instead (Lua type %d)` | `Object obtained from script was not a Phyre Object when an object of type "%s" was required.` |
| second message | `Object pointer obtained from script was of type "%s" when an object of type "%s" was required.` | `Object obtained from script was of type "%s" when an object of type "%s" was required.` |
| **count by message** | **402** | **345** |

**402 + 345 = 747, and the type-name split and the message split agree exactly.** These are separate
features of the binary — one is a mangled RTTI-style string, the other a printf format — so their
agreement is a real cross-check rather than one measurement restated.

**All 747 are `::Get`.** There is no `Set` in this set: the script side reads engine objects through
this path and does not write them through it *(answered: see below - `Get` hands out writable access, and AZ-2's "script cannot write" reading is refuted, 2026-09-14; 2026-10-02, OPUS)*.

**412 distinct bound types** across 747 accessors — most types that are reachable at all are reachable
both by pointer and by reference.

## 5. Call chain

```
Lua script asks for an object
   -> PObjectAccessor<T>::Get                     (one of the 747)
        -> FUN_00682980   luaL_testudata(L, idx, "PhyreObject")   (was: fetch the script value)
        -> FUN_00811130   lua_settop                              (was: resolve to a Phyre object)
        -> walk [descriptor + 0x78] base chain against the required descriptor
             match    -> return the object
             no match -> write __FILE__/__LINE__/__FUNCTION__ to 0x02E41000
                      -> FUN_00812960   report and refuse
```

The Lua side of this seam, and the 1,219 generated binding functions it belongs to, are documented in
[`../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md).
**`Lua type %d` in the pointer variant's message is independent confirmation of the VM's identity**
from a different string set than that document used.

## 6. Modding notes

- **The refusal path is a diagnostic, not a crash.** A mistyped script object produces a report and a
  rejection; the engine does not proceed on a wrong type. Anything injecting objects into the script
  environment must satisfy the base-chain walk, not merely look like a pointer.
- **Derived types are accepted where a base is required** — the check follows `+0x78` up the chain, so
  handing a `PMeshInstance` where a `PNode` is wanted is legal by design.
- **The global at `0x02E41000` is overwritten by every failing accessor**, so it holds only the most
  recent failure. It is a "current assert location" scratch record, not a log.
- **XIIOnline:** these are ~~read-side~~ accessors for Phyre's own object graph *(answered: see below - `Get` hands out writable access, 2026-09-14; 2026-10-02, OPUS)*. They are not a seam for
  gameplay state, and nothing here is worth detouring — the useful consequence is that **747 formerly
  anonymous functions now have exact names**, which makes call graphs through Phyre readable.

## 7. What is not known

- [x] ~~What `FUN_00682980` and `FUN_00811130` do in detail — the fetch and resolve steps are named by
      position in this chain, not read.~~ **AZ-1 ANSWERED 2026-09-13 (FABLE), from the bodies — and the position-based names were wrong.** **`00682980` is Lua 5.2's `luaL_testudata` with the type name fixed to `PhyreObject`**: `lua_touserdata` (`00811950`, `00682994`); if non-null, `lua_getmetatable` (`0080FBA0`, `006829A6`); then `lua_getfield(L, LUA_REGISTRYINDEX = −1001000, "PhyreObject")` (`0080FA50`, `006829AF`–`006829BE`, the name at `00D6FDE0`); `lua_rawequal(L, −1, −2)` (`00810810`, `006829CF`); `lua_settop(L, −3)` — pop 2 (`006829E1`); and the userdata pointer is returned only when the metatables were equal (`006829E6`–`006829FC`), else 0. **`00811130` is `lua_settop`** (`L->top` reset from `ci->func` and nil-tagged up to the new top, `00811130`–`00811177`). The four helpers each open with Lua's index-to-address step (`L->ci->func + idx`, the nil sentinel `01CCB510`, the registry index `0xFFF0B9D8`) and lie inside the Lua library row ([inventory](../../23-Third-Party-Libraries/third-party-middleware-inventory.md), *Lua 5.2.1*). So an accessor's chain is: test that the argument is a `PhyreObject` userdata, pop the two metatables, then walk the descriptor chain.
- [x] ~~Whether a `Set` counterpart exists elsewhere under a different template, or whether script
      genuinely cannot write engine objects through this mechanism.~~ **AZ-2.**
      *Narrowed 2026-09-14 (FABLE), not answered:*
      - **There is no `Set` sibling under this template family.** A whole-image search for `PScriptAccessors::`
        finds no member other than `PObjectAccessor<…>::Get`: all 747 signature strings, and zero other names.
      - **But `Get` hands out writable access.** Classifying the 747 template arguments: **395 are non-const pointers
        (`T *`), 328 non-const references (`T &`)**, 17 const references and 7 const pointers. What is pushed is the
        `{descriptor, object}` userdata over the live object
        ([Lua bindings, R-2](../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)), not a copy.
      - **So the remaining question** is whether any *other* binding family (field setters or methods on the pushed
        object) writes through that pointer. The accessor family neither proves nor rules out a write path.

      **ANSWERED 2026-09-14 (FABLE): yes, script writes engine objects, and it does so through method bindings, not a
      `Set` accessor.** The image carries **156 `PMethodCallerConcrete<Class, Return, Args…>` bindings** (RTTI).
      Each one takes the object from a `PObjectAccessor<Class *>::Get` and calls a member function on it.

      **One worked end to end: `PAnimatableComponent::setSpeed(float)`.**
      1. **Registration.** The class registrar `005AD8F0` registers the name `setSpeed` (`00D31A50`, `005ADBC7`). In
         the same guarded block it installs a caller object at `02CB0C60`. The caller's vtable is `00D34968`, whose
         RTTI is `PMethodCallerConcrete<PAnimatableComponent, void, float>`. Its member-function pointer is
         `005C9FF0` (`005ADC41`–`005ADC61`).
      2. **The script call.** The caller's slot 1 `005C1A60` does three things in order:
         - reads the float argument (`00811640`, a Lua 5.2 value helper);
         - gets the object through `PObjectAccessor<class Phyre::PAnimation::PAnimatableComponent *>::Get`
           (`005BC4D0`, bound by its own name string, see
           [the adapter family](../../24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md)
           `UQ-316`);
         - calls the member function with the object plus the caller's stored adjustment and the float
           (`005C1AA0`–`005C1AAA`).
      3. **The write.** `005C9FF0` walks the component's `[+0x28]`-long array of `0x80`-byte entries at `[+0x30]`.
         For each entry it stores the float at `+0x0C` and `+0x50` and adjusts `+0x54` (`005CA030`–`005CA076`).

      So a script value reaches live engine state in three steps: an accessor `Get`, a non-const pointer, and a bound
      mutator. `AZ-2`'s "script cannot write" reading is refuted. How many of the 156 bindings mutate, as opposed to
      query, is not counted here.
- [x] The 4 functions in the reference set that are not `PObjectAccessor` — `Phyre::PResult`, two
      `PSamplerStateBase` enums, `PPhysicsRigidBodyBase::PCollisionGroup`. They match the string
      pattern but are a different mechanism. **AZ-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (AZ-3): they are lazy type-descriptor
      accessors for four enums, each registered as a 4-byte scalar.* All four are 206-byte (`0xCE`) thread-safe local
      statics. `005A6670` (`Phyre::PResult`, name `00D311F0`) is typical:
      - under `_Init_thread_header` it builds a `PType` record at `02CB07A0` with a self-linked node, size and alignment 4,
        and the name pointer (`005A66B8`–`005A6721`);
      - **the vtable it installs is `00D311B0`, `PTypeDefault<unsigned int>`** (its slot 0 is the `bswap` of
        [the byte-order walk](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) Q-4);
      - it registers a teardown with `atexit` and returns the record.

      The other three have the identical shape: `005D8CA0` (`PSamplerStateFilterFormatType`, `00D49810`), `005D8D70`
      (`PSamplerStateWrapFormatType`, `00D49860`) and `0068F0F0` (`PCollisionGroup`, `00D79AA8`). **So an enum is
      reflected as a named 4-byte unsigned type sharing `PUInt32`'s behaviour.** The records exist because the
      `PMethodCallerConcrete<…>` bindings name them as parameter and return types. The RTTI strings show, for example,
      `PMethodCallerConcrete<PSamplerStateBase, PResult, PSamplerStateFilterFormatType>` and physics-world callers taking
      a `PCollisionGroup`. They carry no `__FILE__` because they are not accessors.
- [x] **AZ-4 ANSWERED (falsification pass, 2026-09-02).** The 156 `Phyre.Middleware.NativeQualified`
      accessors are separated from the 588 correctly-tagged ones by a single feature of the bound
      type: **140 of the 156 bind a type that is itself a template instantiation** (`PArray<…>`,
      `PSharray<…>`), and **zero of the 588 do** — a perfect separation, 140/140. Of the remaining
      16: ten bind a non-Phyre `struct` (the D3D11 descriptors `CD3D11_BLEND_DESC`,
      `D3D11_RENDER_TARGET_BLEND_DESC` and siblings), two bind `Phyre::PTimer`, and four are
      cv-qualified. So the GFZ classifier awarded the accessor CodeDomain only for a **plain,
      non-template, Phyre-namespaced class**, and fell back to `NativeQualified` whenever the bound
      type carried a nested `<`, sat outside `Phyre::`, or was a `struct`. The 3
      `Phyre.ScriptVM.ReflectionBridge` are plain Phyre classes
      (`PClassDescriptorDynamic`, `PAssetReferenceImport` ×2) and look like a deliberate, different
      assignment rather than a fallback.

## 8. Evidence

**Tool run.** `string_xref.py --pattern "Phyre::"` over the shipping EXE against
`functions.tsv`: **751 distinct strings matched, 1,498 LEA references, 751 functions, 0
unattributed.** Output `Tools/work/rtti/phyre_xrefs.tsv`.

**The bijection was tested, not assumed.** 751 strings and 751 functions matching is exactly the kind
of coincidence that turns out to be an attribution artifact, so it was checked both ways:

```
functions referencing exactly ONE distinct string : 751 / 751
strings referenced by exactly ONE function        : 751 / 751
(function,string) pairs with exactly 2 references : 747 / 751
```

**Source provenance is single-valued.** Disassembling all 751 and resolving every RIP-relative LEA
into `.rdata`: **747 carry a `__FILE__`, and there is exactly one distinct file** — three distinct
`(file, line)` sites, at lines 106/118 and 141/143.

**The GFZ audit: sound where it speaks, incomplete.** Compared both directions against the
`CodeDomain` tags:

| | GFZ tag | string evidence | GFZ-only | evidence-only |
|---|---:|---:|---:|---:|
| pointer accessors | 323 | **402** | **0** | 79 |
| reference accessors | 265 | **345** | **0** | 80 |

**Zero GFZ over-reach** — every function the GFZ calls an accessor emits the matching string. But
**159 string-proven accessors carry a different tag**: 156 `Phyre.Middleware.NativeQualified` and 3
`Phyre.ScriptVM.ReflectionBridge`. **The GFZ's precision here is 100 % and its recall is 79 %.** The
string evidence is the stronger of the two, because a function stating its own name in its own body
is not an inference.

**Base rate, stated rather than implied.** All 751 are still named `FUN_*`, which sounds decisive and
is not: the `Phyre` namespace is **95.4 %** `FUN_*` and the binary **84.2 %**. Per
[`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md), a saturated figure is quoted
with its denominator or not at all. **The load-bearing evidence here is the bijection and the
single-file provenance, not the naming rate.**

**One instrument failure, recorded.** A format-string census first returned **zero** diagnostic
strings across all 751. The cause was the scan's own filter: it required every byte to be printable
(`32 <= c < 127`), and **every one of these messages ends with a literal `\n`**. The `__FILE__` scan
using the same code path succeeded because a path has no newline. The number was clean, plausible and
entirely produced by the filter.

## 9. Related

- [`../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
  — the 1,219 generated bindings; **591 of these 747 are among them, 156 are not.**
  *(Corrected 2026-09-02, was "588 … 159 are not" — see §10.)*
- [`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
  — the class descriptors whose `+0x78` base pointer this walk follows.
- [`../../18-Audio/sead-function-identification.md`](../../18-Audio/sead-function-identification.md)
  and [`../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`](../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md)
  — the same string-cross-reference technique, applied to audio and post-processing.

## 10. Falsification pass — 2026-09-02, by a session that did not write this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`, fresh import verified before
the pass. Claims were attacked **in provenance order — inherited and assumed first, body-derived
last** — rather than in importance order, because a pass run in importance order attacks what its
author found hard and leaves untouched exactly the claims that were picked up cheaply.

### Overturned

**§9: "588 of these 747 are among them, 159 are not."** The real intersection of the 747 accessors
with the 1,219 `Phyre.ScriptVM.*`-tagged functions is **591**, and the complement is **156**.

`588` is `323 + 265` — the two *accessor* sub-tag counts from §8's table. It was carried into a
sentence about a different population: membership in the 1,219, which is every function with **any**
`Phyre.ScriptVM.*` CodeDomain. That set includes `ReflectionBridge`, and §8 of this very document
records that **3 of the 747 carry `Phyre.ScriptVM.ReflectionBridge`**. Those three are inside the
1,219 and were counted as outside it. The document therefore contradicted itself between §8 and §9,
with the arithmetic `747 − 588 = 159` matching §8's `156 + 3` mis-tag count and making the wrong
figure look corroborated.

This is the failure mode the number was *most* likely to have: a count that was correct for the set
it was measured on and wrong for the sentence it was written into.

### Answered

**AZ-4**, by a feature test on the bound type — see §7. 140 of the 156 mis-tagged accessors bind a
template instantiation and none of the 588 correctly-tagged do.

### Attacked and survived

| Claim | How it was attacked | Result |
|---|---|---|
| 747 accessors, all `::Get`, no `Set` | independent scan of the authorized EXE for NUL-terminated ASCII containing `PObjectAccessor`, with a positive control | **747, 747 `::Get`, 0 `::Set`** — exact |
| 402 pointer / 345 reference by type name | same scan, split on the `*>::Get` / `&>::Get` suffix | **402 / 345** — exact |
| 412 distinct bound types | same scan, template argument extracted and de-duplicated | **412** — exact |
| assert lines 106/118 (pointer) and 141/143 (reference) | disassembled all 747 bodies, decoded every `mov dword [rip+d], imm32` resolving to `0x02E41008` | **1,494 sites, exactly 2 per function, 747/747.** Pointer accessors write only 106 and 118 (402 each); reference accessors only 141 and 143 (345 each). **Zero exceptions in either direction** |
| the message split, 402 / 345 | resolved every RIP-relative reference in all 747 bodies against the four diagnostic strings | pointer accessors reference `00D24BE0` and `00D24C40`, 402 each; reference accessors reference `00D24050` and `00D240B0`, 345 each. **Zero cross-contamination** |
| the 24-byte assert record at `0x02E41000` | counted writes to each field across all 747 | **1,494 writes to each** of `__FILE__`, `__LINE__`, `__FUNCTION__` |
| the §2 disassembly listing | re-disassembled `00599770` from the EXE with an independent decoder | matches **byte-for-byte at every quoted address**. The listing elides `test r8,r8` at `005997A1` and `test rcx,rcx` at `005997BD`; both are abridgements of an explicitly abridged listing, not errors |
| the base-class chain walk at `+0x78` | read the loop directly | confirmed: it walks the **provided** object's chain looking for the **required** descriptor, so a derived type is accepted where a base is required, as §6 states |

The three-way agreement §4 claims is therefore stronger than "agree": the type-name suffix, the
`__LINE__` constant and the diagnostic string partition the 747 into the **same** 402 / 345 split
with no element out of place on any of the three features.

### What I tried that failed to break it

- Looked for a `Set` counterpart under the same template — **with a positive control first**, because
  the document itself records an instrument that returned a clean zero for these strings due to its
  own printable-byte filter. My first message scan reproduced that class of error: filtering on
  `"obtained from script"` missed `"Unable to **obtain** object pointer from script…"` entirely. The
  re-run asserts a known-present string before reporting any absence.
- Tried to make the `__LINE__` and type-name features disagree by testing every function
  individually rather than in aggregate; no function writes a line constant belonging to the other
  variant.
- Checked whether the appendix's address→type table could be an attribution artifact by re-deriving
  the mapping from the EXE rather than from `phyre_xrefs.tsv`; the accessor count matches exactly.

### Defects found that are not claims

- **The frontmatter said `passes: 1` while `_index/AUDIT-LOG.md` listed this document as owing "a
  first named falsification pass".** One of the two was wrong and neither could be checked from the
  other. `last_pass_state`, `crossref_clean` and `reopened_count` were absent entirely, so there was
  no recorded program state for the claimed pass. Added, with `reopened_count: 1` for this pass.
- **§2's bijection sentence did not name its population.** The bijection is over the wider `Phyre::`
  string set (751); the accessor population is 747. Both numbers were correct and the sentence did
  not say which was which. Fixed in place.

## Appendix — all 747 accessors

Address to bound type. **`Phyre::` is stripped from every entry** (all 747 carry it) and
the trailing `*` or `&` is the pointer/reference variant. Full untruncated names, with the
`PObjectAccessor<...>::Get` wrapper, are in `Tools/work/rtti/phyre_xrefs.tsv`.

| address | bound type | address | bound type |
|---|---|---|---|
| `00599770` | `PSerialization::PBinary::PClusterHeader &` | `0064DFC0` | `PPostProcessing::PCelShadingD3D11 *` |
| `00599870` | `PSerialization::PBinary::PClusterHeaderBase &` | `0064E0F0` | `PPostProcessing::PDeferredLighting *` |
| `00599970` | `PSerialization::PBinary::PClusterHeaderD3D11 &` | `0064E220` | `PPostProcessing::PDeferredLightingBase *` |
| `00599A70` | `PSerialization::PBinary::PInternal::PInstanceListHeader &` | `0064E350` | `PPostProcessing::PDeferredLightingD3D11 *` |
| `00599B70` | `PSerialization::PBinary::PClusterHeader *` | `0064E480` | `PPostProcessing::PDepthOfField *` |
| `00599CA0` | `PSerialization::PBinary::PClusterHeaderBase *` | `0064E5B0` | `PPostProcessing::PDepthOfFieldBase *` |
| `00599DD0` | `PSerialization::PBinary::PClusterHeaderD3D11 *` | `0064E6E0` | `PPostProcessing::PDepthOfFieldD3D11 *` |
| `00599F00` | `PSerialization::PBinary::PInternal::PInstanceListHeader *` | `0064E810` | `PPostProcessing::PFXAA *` |
| `005A05D0` | `PTimer const &` | `0064E940` | `PPostProcessing::PFXAABase *` |
| `005A06E0` | `PTimer *` | `0064EA70` | `PPostProcessing::PFXAAD3D11 *` |
| `005B82A0` | `PArray<unsigned int,4> &` | `0064EBA0` | `PPostProcessing::PGlow *` |
| `005B83B0` | `PArray<float,4> &` | `0064ECD0` | `PPostProcessing::PGlowBase *` |
| `005B84C0` | `PArray<PAnimation::PAnimationChannel *,8> &` | `0064EE00` | `PPostProcessing::PGlowD3D11 *` |
| `005B85D0` | `PArray<PAnimation::PAnimationDataSource *,8> &` | `0064EF30` | `PPostProcessing::PGlowGPUBase *` |
| `005B86E0` | `PArray<PAnimation::PAnimationChannelTarget,8> &` | `0064F060` | `PPostProcessing::PLowResParticles *` |
| `005B87F0` | `PArray<PAnimation::PAnimationConstantChannel,8> &` | `0064F190` | `PPostProcessing::PMLAA *` |
| `005B8900` | `PArray<PAnimation::PAnimationDataSourceListEntry,8> &` | `0064F2C0` | `PPostProcessing::PMLAABase *` |
| `005B8A10` | `PArray<PAnimation::PAnimationEvent,4> &` | `0064F3F0` | `PPostProcessing::PMLAAD3D11 *` |
| `005B8B20` | `PArray<PAnimation::PAnimationNetworkInstanceTarget,8> &` | `0064F520` | `PPostProcessing::PMaterialPostEffect *` |
| `005B8C30` | `PArray<PAnimation::PAnimationSlotArray,8> &` | `0064F650` | `PPostProcessing::PMeshParticleSystemBase *` |
| `005B8D40` | `PArray<PAnimation::PAnimationSlotFilterDeferredLoad,8> &` | `0064F780` | `PPostProcessing::PMotionBlur *` |
| `005B8E50` | `PArray<PAnimation::PAnimationSlotListIndex,8> &` | `0064F8B0` | `PPostProcessing::PMotionBlurBase *` |
| `005B8F60` | `PArray<PAnimation::PBlendableAnimationSource,8> &` | `0064F9E0` | `PPostProcessing::PMotionBlurD3D11 *` |
| `005B9070` | `PArray<PQWord,16> &` | `0064FB10` | `PPostProcessing::PPostEffectBase *` |
| `005B9180` | `PSharray<PAnimation::PAnimationClip *> &` | `0064FC40` | `PPostProcessing::PPostEffectManager *` |
| `005B9290` | `PAnimation::PAnimatableComponent &` | `0064FD70` | `PPostProcessing::PScreenSpaceAmbientOcclusion *` |
| `005B93B0` | `PAnimation::PAnimationAdditiveBlenderController &` | `0064FEA0` | `PPostProcessing::PScreenSpaceAmbientOcclusionBase *` |
| `005B94D0` | `PAnimation::PAnimationChannel &` | `0064FFD0` | `PPostProcessing::PScreenSpaceAmbientOcclusionD3D11 *` |
| `005B95D0` | `PAnimation::PAnimationChannelBase &` | `00650100` | `PPostProcessing::PScreenSpaceReflection *` |
| `005B96D0` | `PAnimation::PAnimationChannelTarget &` | `00650230` | `PPostProcessing::PScreenSpaceReflectionBase *` |
| `005B97D0` | `PAnimation::PAnimationChannelTimes &` | `00650360` | `PPostProcessing::PScreenSpaceReflectionD3D11 *` |
| `005B98D0` | `PAnimation::PAnimationClip &` | `0066AE50` | `PArray<unsigned char,4> &` |
| `005B99D0` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap &` | `0066AF60` | `PArray<int,4> &` |
| `005B9AD0` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache &` | `0066B070` | `PArray<PGeometry::PDataBlockD3D11,8> &` |
| `005B9BD0` | `PAnimation::PAnimationConstantChannel &` | `0066B180` | `PArray<PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> &` |
| `005B9CD0` | `PAnimation::PAnimationController &` | `0066B290` | `PArray<PGeometry::PMeshSegment,8> &` |
| `005B9DF0` | `PAnimation::PAnimationDataSourceListEntry &` | `0066B3A0` | `PArray<PGeometry::PSkeletonJointBounds,4> &` |
| `005B9EF0` | `PAnimation::PAnimationEvent &` | `0066B4B0` | `PArray<PGeometry::PSkinBoneRemap,2> &` |
| `005B9FF0` | `PAnimation::PAnimationEventController &` | `0066B5C0` | `PArray<PGeometry::PVertexStream,8> &` |
| `005BA110` | `PAnimation::PAnimationEventList &` | `0066B6D0` | `PSharray<PRendering::PMaterial *> &` |
| `005BA210` | `PAnimation::PAnimationNetworkInstance &` | `0066B7E0` | `PSharray<PGeometry::PDataBlockBufferD3D11> &` |
| `005BA330` | `PAnimation::PAnimationNetworkInstanceTarget &` | `0066B8F0` | `PSharray<PGeometry::PIndexDataBlockBufferD3D11> &` |
| `005BA430` | `PAnimation::PAnimationSet &` | `0066BA00` | `PGeometry::PDataBlock &` |
| `005BA530` | `PAnimation::PAnimationSlotArray &` | `0066BB00` | `PGeometry::PDataBlockBase &` |
| `005BA630` | `PAnimation::PAnimationSlotFilter &` | `0066BC00` | `PGeometry::PDataBlockBufferD3D11 &` |
| `005BA750` | `PAnimation::PAnimationSlotFilterDeferredLoad &` | `0066BD00` | `PGeometry::PDataBlockD3D11 &` |
| `005BA850` | `PAnimation::PAnimationSlotListIndex &` | `0066BE00` | `PGeometry::PDynamicDataBlock &` |
| `005BA950` | `PAnimation::PAnimationSpuTargetBlenderController &` | `0066BF00` | `PGeometry::PDynamicMesh::PDynamicSegmentDesc &` |
| `005BAA70` | `PAnimation::PAnimationTargetBlenderController &` | `0066C000` | `PGeometry::PIndexDataBlock &` |
| `005BAB90` | `PAnimation::PAnimationWeightedBlenderController &` | `0066C100` | `PGeometry::PIndexDataBlockBase &` |
| `005BACB0` | `PAnimation::PBlendableAnimationSource &` | `0066C200` | `PGeometry::PIndexDataBlockBufferD3D11 &` |
| `005BADB0` | `PCluster &` | `0066C300` | `PGeometry::PIndexDataBlockD3D11 &` |
| `005BAEB0` | `PAnimation::PTimeController &` | `0066C400` | `PGeometry::PMaterialSet &` |
| `005BAFD0` | `PAnimation::PTimeIntervalController &` | `0066C500` | `PGeometry::PMesh &` |
| `005BB0F0` | `PAnimation::PTimeScaleOffsetController &` | `0066C600` | `PGeometry::PMeshSegment &` |
| `005BB210` | `PArray<unsigned int,4> *` | `0066C700` | `PGeometry::PMeshSegmentBase &` |
| `005BB350` | `PArray<float,4> *` | `0066C800` | `PGeometry::PMeshSegmentD3D11 &` |
| `005BB490` | `PArray<PAnimation::PAnimationChannel *,8> *` | `0066C900` | `PGeometry::PShape &` |
| `005BB5D0` | `PArray<PAnimation::PAnimationDataSource *,8> *` | `0066CA00` | `PGeometry::PSkeletonJointBounds &` |
| `005BB710` | `PArray<PAnimation::PAnimationChannelTarget,8> *` | `0066CB00` | `PGeometry::PSkinBoneRemap &` |
| `005BB850` | `PArray<PAnimation::PAnimationConstantChannel,8> *` | `0066CC00` | `PGeometry::PVertexStream &` |
| `005BB990` | `PArray<PAnimation::PAnimationDataSourceListEntry,8> *` | `0066CD00` | `PArray<unsigned char,4> *` |
| `005BBAD0` | `PArray<PAnimation::PAnimationEvent,4> *` | `0066CE40` | `PArray<int,4> *` |
| `005BBC10` | `PArray<PAnimation::PAnimationNetworkInstanceTarget,8> *` | `0066CF80` | `PArray<PGeometry::PDataBlockD3D11,8> *` |
| `005BBD50` | `PArray<PAnimation::PAnimationSlotArray,8> *` | `0066D0C0` | `PArray<PGeometry::PDynamicMesh::PDynamicSegmentDesc,4> *` |
| `005BBE90` | `PArray<PAnimation::PAnimationSlotFilterDeferredLoad,8> *` | `0066D200` | `PArray<PGeometry::PMeshSegment,8> *` |
| `005BBFD0` | `PArray<PAnimation::PAnimationSlotListIndex,8> *` | `0066D340` | `PArray<PGeometry::PSkeletonJointBounds,4> *` |
| `005BC110` | `PArray<PAnimation::PBlendableAnimationSource,8> *` | `0066D480` | `PArray<PGeometry::PSkinBoneRemap,2> *` |
| `005BC250` | `PArray<PQWord,16> *` | `0066D5C0` | `PArray<PGeometry::PVertexStream,8> *` |
| `005BC390` | `PSharray<PAnimation::PAnimationClip *> *` | `0066D700` | `PSharray<PRendering::PMaterial *> *` |
| `005BC4D0` | `PAnimation::PAnimatableComponent *` | `0066D840` | `PSharray<PGeometry::PDataBlockBufferD3D11> *` |
| `005BC600` | `PAnimation::PAnimationAdditiveBlenderController *` | `0066D980` | `PSharray<PGeometry::PIndexDataBlockBufferD3D11> *` |
| `005BC730` | `PAnimation::PAnimationBlenderController *` | `0066DAC0` | `PGeometry::PDataBlock *` |
| `005BC860` | `PAnimation::PAnimationChannel *` | `0066DBF0` | `PGeometry::PDataBlockBase *` |
| `005BC990` | `PAnimation::PAnimationChannelBase *` | `0066DD20` | `PGeometry::PDataBlockBufferD3D11 *` |
| `005BCAC0` | `PAnimation::PAnimationChannelTarget *` | `0066DE50` | `PGeometry::PDataBlockD3D11 *` |
| `005BCBF0` | `PAnimation::PAnimationChannelTimes *` | `0066DF80` | `PGeometry::PDynamicDataBlock *` |
| `005BCD20` | `PAnimation::PAnimationClip *` | `0066E0B0` | `PGeometry::PDynamicMesh *` |
| `005BCE50` | `PAnimation::PAnimationClipBinding *` | `0066E1E0` | `PGeometry::PDynamicMesh::PDynamicSegmentDesc *` |
| `005BCF80` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap *` | `0066E310` | `PGeometry::PIndexDataBlock *` |
| `005BD0B0` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache *` | `0066E440` | `PGeometry::PIndexDataBlockBase *` |
| `005BD1E0` | `PAnimation::PAnimationConstantChannel *` | `0066E570` | `PGeometry::PIndexDataBlockBufferD3D11 *` |
| `005BD310` | `PAnimation::PAnimationController *` | `0066E6A0` | `PGeometry::PIndexDataBlockD3D11 *` |
| `005BD440` | `PAnimation::PAnimationDataSource *` | `0066E7D0` | `PGeometry::PMaterialSet *` |
| `005BD570` | `PAnimation::PAnimationDataSourceListEntry *` | `0066E900` | `PGeometry::PMesh *` |
| `005BD6A0` | `PAnimation::PAnimationEvent *` | `0066EA30` | `PGeometry::PMeshSegment *` |
| `005BD7D0` | `PAnimation::PAnimationEventController *` | `0066EB60` | `PGeometry::PMeshSegmentBase *` |
| `005BD900` | `PAnimation::PAnimationEventList *` | `0066EC90` | `PGeometry::PMeshSegmentD3D11 *` |
| `005BDA30` | `PAnimation::PAnimationHierarchyNode *` | `0066EDC0` | `PGeometry::PShape *` |
| `005BDB60` | `PAnimation::PAnimationNetworkInstance *` | `0066EEF0` | `PGeometry::PSkeletonJointBounds *` |
| `005BDC90` | `PAnimation::PAnimationNetworkInstanceTarget *` | `0066F020` | `PGeometry::PSkinBoneRemap *` |
| `005BDDC0` | `PAnimation::PAnimationSet *` | `0066F150` | `PGeometry::PVertexStream *` |
| `005BDEF0` | `PAnimation::PAnimationSlotArray *` | `00676600` | `PAssetReferenceImport &` |
| `005BE020` | `PAnimation::PAnimationSlotFilter *` | `00676700` | `PBase const &` |
| `005BE150` | `PAnimation::PAnimationSlotFilterDeferredLoad *` | `00676810` | `PAssetReference *` |
| `005BE280` | `PAnimation::PAnimationSlotListIndex *` | `00676940` | `PAssetReferenceImport *` |
| `005BE3B0` | `PAnimation::PAnimationSpuTargetBlenderController *` | `00678BB0` | `PCamera &` |
| `005BE4E0` | `PAnimation::PAnimationTargetBlenderController *` | `00678CB0` | `PCamera *` |
| `005BE610` | `PAnimation::PAnimationWeightedBlenderController *` | `00678DE0` | `PCameraProjection *` |
| `005BE740` | `PAnimation::PBlendableAnimationSource *` | `0067DB40` | `PArray<PText::PBitmapFontCharInfo,4> &` |
| `005BE870` | `PCluster *` | `0067DC50` | `PText::PBitmapFontCharInfo &` |
| `005BE9A0` | `PAnimation::PTimeController *` | `0067DD50` | `PArray<PText::PBitmapFontCharInfo,4> *` |
| `005BEAD0` | `PAnimation::PTimeIntervalController *` | `0067DE90` | `PText::PBitmapFont *` |
| `005BEC00` | `PAnimation::PTimeScaleOffsetController *` | `0067DFC0` | `PText::PBitmapFontCharInfo *` |
| `005F0C70` | `PArray<PRendering::PEffectVariant *,8> &` | `0067EAC0` | `PWorldMatrix &` |
| `005F0D80` | `PArray<PDynamicGeometry::PModifierNetworkInstance *,8> &` | `0067EBC0` | `PMatrix4x3 const &` |
| `005F0E90` | `PArray<PRendering::PSceneRenderPass *,8> &` | `0067ECD0` | `PWorldMatrix const &` |
| `005F0FA0` | `PArray<PRendering::PContextSwitch const *,8> &` | `0067EDD0` | `PWorldMatrix *` |
| `005F10B0` | `PArray<PRendering::PLightType const *,8> &` | `00682F40` | `PScripting::PAsyncProcessHeader &` |
| `005F11C0` | `PArray<PRendering::PShadowCasterType const *,8> &` | `00683040` | `PBase &` |
| `005F12D0` | `PArray<PRendering::PContextVariantFoldingTable,4> &` | `00683150` | `PScripting::PScript &` |
| `005F13E0` | `PArray<PRendering::PMaterialSwitch,8> &` | `00683250` | `PScripting::PScriptCallbackHandler &` |
| `005F14F0` | `PArray<PMatrix4,4> &` | `00683350` | `PScripting::PScript const &` |
| `005F1600` | `PArray<PRendering::PMeshInstanceSegmentContext,8> &` | `00683450` | `PScripting::PAsyncProcessHeader *` |
| `005F1710` | `PArray<PRendering::PNodeContext,8> &` | `00683580` | `PScripting::PClassCallableMethodScript *` |
| `005F1820` | `PArray<PRendering::PSceneRenderPass,8> &` | `006836B0` | `PScripting::PScheduler *` |
| `005F1930` | `PArray<PRendering::PShader,8> &` | `006837E0` | `PScripting::PScript *` |
| `005F1A40` | `PArray<PRendering::PShaderParameterCaptureBufferLocation,2> &` | `00683910` | `PScripting::PScriptCallbackHandler *` |
| `005F1B50` | `PArray<PRendering::PShaderParameterCaptureBufferLocationType,2> &` | `00698D00` | `PSharray<PPhysics::PPhysicsShape *> &` |
| `005F1C60` | `PArray<PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> &` | `00698E10` | `PPhysics::PPhysicsBox &` |
| `005F1D70` | `PArray<PRendering::PShaderParameterDefinition,8> &` | `00698F30` | `PPhysics::PPhysicsBoxBase &` |
| `005F1E80` | `PArray<PRendering::PShaderPass,8> &` | `00699050` | `PPhysics::PPhysicsBoxBullet &` |
| `005F1F90` | `PArray<PRendering::PShaderPassInfo,8> &` | `00699170` | `PPhysics::PPhysicsCapsule &` |
| `005F20A0` | `PArray<PRendering::PShaderStreamDefinition,8> &` | `00699290` | `PPhysics::PPhysicsCapsuleBase &` |
| `005F21B0` | `PArray<PString,8> &` | `006993B0` | `PPhysics::PPhysicsCapsuleBullet &` |
| `005F22C0` | `PSharray<unsigned int> &` | `006994D0` | `PPhysics::PPhysicsCharacterCamera &` |
| `005F23D0` | `PSharray<PRendering::PMeshInstanceSegmentStreamBinding const *> &` | `006995F0` | `PPhysics::PPhysicsCharacterController &` |
| `005F24E0` | `PRendering::PConstantBuffer &` | `006996F0` | `PPhysics::PPhysicsCharacterControllerBase &` |
| `005F25E0` | `PRendering::PConstantBufferBase &` | `006997F0` | `PPhysics::PPhysicsCharacterControllerBullet &` |
| `005F26E0` | `PRendering::PContextVariantFoldingTable &` | `006998F0` | `PPhysics::PPhysicsCylinder &` |
| `005F27E0` | `PRendering::PEffect &` | `00699A10` | `PPhysics::PPhysicsCylinderBase &` |
| `005F28E0` | `PRendering::PForwardShadowRenderer &` | `00699B30` | `PPhysics::PPhysicsCylinderBullet &` |
| `005F29E0` | `PRendering::PIndirectArgsBuffer &` | `00699C50` | `PPhysics::PPhysicsInterfaceBase &` |
| `005F2AE0` | `PRendering::PIndirectArgsBufferBase &` | `00699D70` | `PPhysics::PPhysicsInterfaceBullet &` |
| `005F2BE0` | `PRendering::PMaterialSwitch &` | `00699E90` | `PPhysics::PPhysicsMaterial &` |
| `005F2CE0` | `PRendering::PMeshInstanceBounds &` | `00699F90` | `PPhysics::PPhysicsMesh &` |
| `005F2DE0` | `PRendering::PMeshInstanceSegmentContext &` | `0069A0B0` | `PPhysics::PPhysicsMeshBase &` |
| `005F2EE0` | `PRendering::PMeshInstanceSegmentStreamBinding &` | `0069A1D0` | `PPhysics::PPhysicsMeshBullet &` |
| `005F2FE0` | `PRendering::PNodeContext &` | `0069A2F0` | `PPhysics::PPhysicsModel &` |
| `005F30E0` | `PRendering::PSamplerState &` | `0069A3F0` | `PPhysics::PPhysicsPlane &` |
| `005F31E0` | `PRendering::PSamplerStateBase &` | `0069A510` | `PPhysics::PPhysicsPlaneBase &` |
| `005F32E0` | `PRendering::PSceneRenderPass &` | `0069A630` | `PPhysics::PPhysicsPlaneBullet &` |
| `005F33E0` | `PRendering::PSceneWideParameterBuffer &` | `0069A750` | `PPhysics::PPhysicsRigidBody &` |
| `005F34E0` | `PRendering::PShader &` | `0069A850` | `PPhysics::PPhysicsRigidBodyBase &` |
| `005F35E0` | `PRendering::PShaderParameterCaptureBufferByteAddressBuffer &` | `0069A950` | `PPhysics::PPhysicsRigidBodyBullet &` |
| `005F36E0` | `PRendering::PShaderParameterCaptureBufferDataBlock &` | `0069AA50` | `PPhysics::PPhysicsShape &` |
| `005F37E0` | `PRendering::PShaderParameterCaptureBufferIndexDataBlock &` | `0069AB70` | `PPhysics::PPhysicsShapeBullet &` |
| `005F38E0` | `PRendering::PShaderParameterCaptureBufferLocation &` | `0069AC90` | `PPhysics::PPhysicsSphere &` |
| `005F39E0` | `PRendering::PShaderParameterCaptureBufferLocationSize &` | `0069ADB0` | `PPhysics::PPhysicsSphereBase &` |
| `005F3AE0` | `PRendering::PShaderParameterCaptureBufferLocationType &` | `0069AED0` | `PPhysics::PPhysicsSphereBullet &` |
| `005F3BE0` | `PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer &` | `0069AFF0` | `PPhysics::PPhysicsTaperedCapsule &` |
| `005F3CE0` | `PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer &` | `0069B110` | `PPhysics::PPhysicsTaperedCylinder &` |
| `005F3DE0` | `PRendering::PShaderParameterCaptureBufferRWStructuredBuffer &` | `0069B230` | `PPhysics::PPhysicsWorld &` |
| `005F3EE0` | `PRendering::PShaderParameterCaptureBufferRWTexture2D &` | `0069B330` | `PPhysics::PPhysicsWorldBase &` |
| `005F3FE0` | `PRendering::PShaderParameterCaptureBufferRWTexture3D &` | `0069B430` | `PPhysics::PPhysicsWorldBullet &` |
| `005F40E0` | `PRendering::PShaderParameterCaptureBufferSampler &` | `0069B530` | `PPhysics::PRaycastResult &` |
| `005F41E0` | `PRendering::PShaderParameterCaptureBufferStream &` | `0069B630` | `PSharray<PPhysics::PPhysicsShape *> *` |
| `005F42E0` | `PRendering::PShaderParameterCaptureBufferStructuredBuffer &` | `0069B770` | `PPhysics::PPhysicsBox *` |
| `005F43E0` | `PRendering::PShaderParameterCaptureBufferTexture2D &` | `0069B8A0` | `PPhysics::PPhysicsBoxBase *` |
| `005F44E0` | `PRendering::PShaderParameterCaptureBufferTexture3D &` | `0069B9D0` | `PPhysics::PPhysicsBoxBullet *` |
| `005F45E0` | `PRendering::PShaderParameterCaptureBufferTextureCubeMap &` | `0069BB00` | `PPhysics::PPhysicsCallbackData *` |
| `005F46E0` | `PRendering::PShaderParameterCaptureConstantBuffer &` | `0069BC30` | `PPhysics::PPhysicsCapsule *` |
| `005F47E0` | `PRendering::PShaderParameterDefinition &` | `0069BD60` | `PPhysics::PPhysicsCapsuleBase *` |
| `005F48E0` | `PRendering::PShaderPass &` | `0069BE90` | `PPhysics::PPhysicsCapsuleBullet *` |
| `005F49E0` | `PRendering::PShaderPassBase &` | `0069BFC0` | `PPhysics::PPhysicsCharacterCamera *` |
| `005F4AE0` | `PRendering::PShaderPassInfo &` | `0069C0F0` | `PPhysics::PPhysicsCharacterController *` |
| `005F4BE0` | `PRendering::PShaderPassParameterLocationTypes &` | `0069C220` | `PPhysics::PPhysicsCharacterControllerBase *` |
| `005F4CE0` | `PRendering::PShaderPassParameterLocationTypesBase &` | `0069C350` | `PPhysics::PPhysicsCharacterControllerBullet *` |
| `005F4DE0` | `PRendering::PShaderPassParameterLocationTypesConstantBuffer &` | `0069C480` | `PPhysics::PPhysicsCylinder *` |
| `005F4EE0` | `PRendering::PShaderPassStateBase &` | `0069C5B0` | `PPhysics::PPhysicsCylinderBase *` |
| `005F4FE0` | `PRendering::PShaderProgramBase &` | `0069C6E0` | `PPhysics::PPhysicsCylinderBullet *` |
| `005F50E0` | `PRendering::PShaderProgramParamsAndStreams &` | `0069C810` | `PPhysics::PPhysicsInterface *` |
| `005F51E0` | `PRendering::PShaderStreamDefinition &` | `0069C940` | `PPhysics::PPhysicsInterfaceBase *` |
| `005F52E0` | `PRendering::PShadowRenderer &` | `0069CA70` | `PPhysics::PPhysicsInterfaceBullet *` |
| `005F53E0` | `PRendering::PStructuredBuffer &` | `0069CBA0` | `PPhysics::PPhysicsMaterial *` |
| `005F54E0` | `PRendering::PStructuredBufferBase &` | `0069CCD0` | `PPhysics::PPhysicsMesh *` |
| `005F55E0` | `PRendering::PTexture2D &` | `0069CE00` | `PPhysics::PPhysicsMeshBase *` |
| `005F56E0` | `PRendering::PTexture2DBase &` | `0069CF30` | `PPhysics::PPhysicsMeshBullet *` |
| `005F57E0` | `PRendering::PTexture3D &` | `0069D060` | `PPhysics::PPhysicsModel *` |
| `005F58E0` | `PRendering::PTexture3DBase &` | `0069D190` | `PPhysics::PPhysicsPlane *` |
| `005F59E0` | `PRendering::PTextureCommonBase &` | `0069D2C0` | `PPhysics::PPhysicsPlaneBase *` |
| `005F5AE0` | `PRendering::PTextureCubeMap &` | `0069D3F0` | `PPhysics::PPhysicsPlaneBullet *` |
| `005F5BE0` | `PRendering::PTextureCubeMapBase &` | `0069D520` | `PPhysics::PPhysicsRigidBody *` |
| `005F5CE0` | `PArray<PRendering::PEffectVariant *,8> *` | `0069D650` | `PPhysics::PPhysicsRigidBodyBase *` |
| `005F5E20` | `PArray<PDynamicGeometry::PModifierNetworkInstance *,8> *` | `0069D780` | `PPhysics::PPhysicsRigidBodyBullet *` |
| `005F5F60` | `PArray<PRendering::PSceneRenderPass *,8> *` | `0069D8B0` | `PPhysics::PPhysicsShape *` |
| `005F60A0` | `PArray<PRendering::PContextSwitch const *,8> *` | `0069D9E0` | `PPhysics::PPhysicsShapeBase *` |
| `005F61E0` | `PArray<PRendering::PLightType const *,8> *` | `0069DB10` | `PPhysics::PPhysicsShapeBullet *` |
| `005F6320` | `PArray<PRendering::PShadowCasterType const *,8> *` | `0069DC40` | `PPhysics::PPhysicsSphere *` |
| `005F6460` | `PArray<PRendering::PContextVariantFoldingTable,4> *` | `0069DD70` | `PPhysics::PPhysicsSphereBase *` |
| `005F65A0` | `PArray<PRendering::PMaterialSwitch,8> *` | `0069DEA0` | `PPhysics::PPhysicsSphereBullet *` |
| `005F66E0` | `PArray<PMatrix4,4> *` | `0069DFD0` | `PPhysics::PPhysicsTaperedCapsule *` |
| `005F6820` | `PArray<PRendering::PMeshInstanceSegmentContext,8> *` | `0069E100` | `PPhysics::PPhysicsTaperedCylinder *` |
| `005F6960` | `PArray<PRendering::PNodeContext,8> *` | `0069E230` | `PPhysics::PPhysicsWorld *` |
| `005F6AA0` | `PArray<PRendering::PSceneRenderPass,8> *` | `0069E360` | `PPhysics::PPhysicsWorldBase *` |
| `005F6BE0` | `PArray<PRendering::PShader,8> *` | `0069E490` | `PPhysics::PPhysicsWorldBullet *` |
| `005F6D20` | `PArray<PRendering::PShaderParameterCaptureBufferLocation,2> *` | `0069E5C0` | `PPhysics::PRaycastResult *` |
| `005F6E60` | `PArray<PRendering::PShaderParameterCaptureBufferLocationType,2> *` | `006A74B0` | `PString &` |
| `005F6FA0` | `PArray<PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer,4> *` | `006A75B0` | `PString *` |
| `005F70E0` | `PArray<PRendering::PShaderParameterDefinition,8> *` | `006A8810` | `PSharray<PGameplay::PTriggerReceiverComponent *> &` |
| `005F7220` | `PArray<PRendering::PShaderPass,8> *` | `006A8920` | `PGameplay::PTrigger &` |
| `005F7360` | `PArray<PRendering::PShaderPassInfo,8> *` | `006A8A20` | `PSharray<PGameplay::PTriggerReceiverComponent *> *` |
| `005F74A0` | `PArray<PRendering::PShaderStreamDefinition,8> *` | `006A8B60` | `PGameplay::PTrigger *` |
| `005F75E0` | `PArray<PString,8> *` | `006A99E0` | `PGameplay::PQuarryComponent &` |
| `005F7720` | `PSharray<unsigned int> *` | `006A9AE0` | `PGameplay::PQuarryComponent *` |
| `005F7860` | `PSharray<PRendering::PMeshInstanceSegmentStreamBinding const *> *` | `006AA050` | `PTypedObject *` |
| `005F79A0` | `PRendering::PConstantBuffer *` | `006AAE00` | `PComponent &` |
| `005F7AD0` | `PRendering::PConstantBufferBase *` | `006AAF00` | `PComponent *` |
| `005F7C00` | `PRendering::PContextVariantFoldingTable *` | `006AC0D0` | `PEntity &` |
| `005F7D30` | `PRendering::PDynamicMeshInstance *` | `006AC1D0` | `PEntity *` |
| `005F7E60` | `PRendering::PEffect *` | `006AD250` | `PCameraOrthographic &` |
| `005F7F90` | `PRendering::PEffectVariant *` | `006AD370` | `PCameraOrthographic *` |
| `005F80C0` | `PRendering::PForwardShadowRenderer *` | `006AD9D0` | `PCameraPerspective &` |
| `005F81F0` | `PRendering::PIndirectArgsBuffer *` | `006ADAF0` | `PCameraPerspective *` |
| `005F8320` | `PRendering::PIndirectArgsBufferBase *` | `006AEAB0` | `PArray<PTypedObject,8> &` |
| `005F8450` | `PRendering::PMaterial *` | `006AEBC0` | `PInstancesComponent &` |
| `005F8580` | `PRendering::PMaterialSwitch *` | `006AECC0` | `PArray<PTypedObject,8> *` |
| `005F86B0` | `PRendering::PMeshInstance *` | `006AEE00` | `PInstancesComponent *` |
| `005F87E0` | `PRendering::PMeshInstanceAttachPoint *` | `006AEF30` | `PClassDescriptor const *` |
| `005F8910` | `PRendering::PMeshInstanceBounds *` | `006AFF70` | `PNameComponent *` |
| `005F8A40` | `PRendering::PMeshInstanceSegmentContext *` | `006B0630` | `PRandom::PRandomGenerator *` |
| `005F8B70` | `PRendering::PMeshInstanceSegmentStreamBinding *` | `006B3780` | `PMatrix4x3 *` |
| `005F8CA0` | `PRendering::PModifierNetworkDynamicMeshInstance *` | `006B5050` | `PScene::PNode &` |
| `005F8DD0` | `PRendering::PNodeContext *` | `006B5170` | `PScene::PNode *` |
| `005F8F00` | `PRendering::PParameterBuffer *` | `006B8AE0` | `PRendering::PMeshSegmentContext &` |
| `005F9030` | `PRendering::PParameterBufferBase *` | `006B8BE0` | `PRendering::PMeshSegmentContext *` |
| `005F9160` | `PRendering::PRenderTarget *` | `006BD5E0` | `PArray<unsigned char const *,8> &` |
| `005F9290` | `PRendering::PRenderTargetBase *` | `006BD6F0` | `PArray<PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> &` |
| `005F93C0` | `PRendering::PSamplerState *` | `006BD800` | `PArray<PDynamicGeometry::PRenderStream,8> &` |
| `005F94F0` | `PRendering::PSamplerStateBase *` | `006BD910` | `PDynamicGeometry::PModifierNetworkDynamicMesh &` |
| `005F9620` | `PRendering::PSceneRenderPass *` | `006BDA30` | `PDynamicGeometry::PModifierNetworkDynamicMeshSegment &` |
| `005F9750` | `PRendering::PSceneWideParameterBuffer *` | `006BDB30` | `PArray<unsigned char const *,8> *` |
| `005F9880` | `PRendering::PShader *` | `006BDC70` | `PArray<PDynamicGeometry::PModifierNetworkDynamicMeshSegment,8> *` |
| `005F99B0` | `PRendering::PShaderComputeProgram *` | `006BDDB0` | `PArray<PDynamicGeometry::PRenderStream,8> *` |
| `005F9AE0` | `PRendering::PShaderFragmentProgram *` | `006BDEF0` | `PDynamicGeometry::PModifierNetworkDynamicMesh *` |
| `005F9C10` | `PRendering::PShaderGeometryProgram *` | `006BE020` | `PDynamicGeometry::PModifierNetworkDynamicMeshSegment *` |
| `005F9D40` | `PRendering::PShaderParameterCaptureBufferByteAddressBuffer *` | `006BFA10` | `PRendering::PLight &` |
| `005F9E70` | `PRendering::PShaderParameterCaptureBufferDataBlock *` | `006BFB10` | `PRendering::PLight *` |
| `005F9FA0` | `PRendering::PShaderParameterCaptureBufferIndexDataBlock *` | `006C1C50` | `PArray<PRendering::PShadowCaster::PShadowSplit,8> &` |
| `005FA0D0` | `PRendering::PShaderParameterCaptureBufferLocation *` | `006C1D60` | `PRendering::PShadowCaster &` |
| `005FA200` | `PRendering::PShaderParameterCaptureBufferLocationSize *` | `006C1E60` | `PRendering::PShadowCaster::PShadowSplit &` |
| `005FA330` | `PRendering::PShaderParameterCaptureBufferLocationType *` | `006C1F60` | `PArray<PRendering::PShadowCaster::PShadowSplit,8> *` |
| `005FA460` | `PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer *` | `006C20A0` | `PRendering::PShadowCaster *` |
| `005FA590` | `PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer *` | `006C21D0` | `PRendering::PShadowCaster::PShadowSplit *` |
| `005FA6C0` | `PRendering::PShaderParameterCaptureBufferRWStructuredBuffer *` | `006C3B40` | `PArray<PBase const *,8> &` |
| `005FA7F0` | `PRendering::PShaderParameterCaptureBufferRWTexture2D *` | `006C3C50` | `PDynamicGeometry::PModifierNetworkInstance &` |
| `005FA920` | `PRendering::PShaderParameterCaptureBufferRWTexture3D *` | `006C3D50` | `PDynamicGeometry::PModifierNetworkInstanceInput &` |
| `005FAA50` | `PRendering::PShaderParameterCaptureBufferSampler *` | `006C3E50` | `PDynamicGeometry::PModifierNetworkInstancePacketInput &` |
| `005FAB80` | `PRendering::PShaderParameterCaptureBufferStream *` | `006C3F50` | `PArray<PBase const *,8> *` |
| `005FACB0` | `PRendering::PShaderParameterCaptureBufferStructuredBuffer *` | `006C4090` | `PDynamicGeometry::PModifierNetworkInstance *` |
| `005FADE0` | `PRendering::PShaderParameterCaptureBufferTexture2D *` | `006C41C0` | `PDynamicGeometry::PModifierNetworkInstanceInput *` |
| `005FAF10` | `PRendering::PShaderParameterCaptureBufferTexture3D *` | `006C42F0` | `PDynamicGeometry::PModifierNetworkInstancePacketInput *` |
| `005FB040` | `PRendering::PShaderParameterCaptureBufferTextureBase *` | `006C6A40` | `PArray<PLOD::PLODLevel,8> &` |
| `005FB170` | `PRendering::PShaderParameterCaptureBufferTextureCubeMap *` | `006C6B50` | `PSharray<PRendering::PMeshInstance *> &` |
| `005FB2A0` | `PRendering::PShaderParameterCaptureConstantBuffer *` | `006C6C60` | `PLOD::PLODGroup &` |
| `005FB3D0` | `PRendering::PShaderParameterDefinition *` | `006C6D60` | `PLOD::PLODLevel &` |
| `005FB500` | `PRendering::PShaderPass *` | `006C6E60` | `PArray<PLOD::PLODLevel,8> *` |
| `005FB630` | `PRendering::PShaderPassBase *` | `006C6FA0` | `PSharray<PRendering::PMeshInstance *> *` |
| `005FB760` | `PRendering::PShaderPassInfo *` | `006C70E0` | `PLOD::PLODGroup *` |
| `005FB890` | `PRendering::PShaderPassParameterLocationTypes *` | `006C7210` | `PLOD::PLODLevel *` |
| `005FB9C0` | `PRendering::PShaderPassParameterLocationTypesBase *` | `006C8520` | `POccluderGeometry::POccluderGeometryInstance *` |
| `005FBAF0` | `PRendering::PShaderPassParameterLocationTypesConstantBuffer *` | `006CD140` | `PGameplay::PScriptableComponent *` |
| `005FBC20` | `PRendering::PShaderPassStateBase *` | `006CDC00` | `PGameplay::PTriggerReceiverTypeCallbackData *` |
| `005FBD50` | `PRendering::PShaderProgramBase *` | `006CE340` | `PGameplay::PTriggerReceiverComponent &` |
| `005FBE80` | `PRendering::PShaderProgramParamsAndStreams *` | `006CE440` | `PGameplay::PTriggerReceiverComponent *` |
| `005FBFB0` | `PRendering::PShaderSource *` | `006D3350` | `PArray<PDynamicGeometry::PModifierAndInputs,8> &` |
| `005FC0E0` | `PRendering::PShaderStreamDefinition *` | `006D3460` | `PArray<PDynamicGeometry::PModifierNetworkBuffer,8> &` |
| `005FC210` | `PRendering::PShaderVertexProgram *` | `006D3570` | `PArray<PDynamicGeometry::PRenderStreamInput,4> &` |
| `005FC340` | `PRendering::PShadowRenderer *` | `006D3680` | `PDynamicGeometry::PModifierAndInputs &` |
| `005FC470` | `PRendering::PStructuredBuffer *` | `006D3780` | `PDynamicGeometry::PModifierNetwork &` |
| `005FC5A0` | `PRendering::PStructuredBufferBase *` | `006D3880` | `PDynamicGeometry::PModifierNetworkBuffer &` |
| `005FC6D0` | `PRendering::PTexture2D *` | `006D3980` | `PDynamicGeometry::PModifierNetworkInfoPacket_Buffer &` |
| `005FC800` | `PRendering::PTexture2DBase *` | `006D3A80` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode &` |
| `005FC930` | `PRendering::PTexture3D *` | `006D3B80` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance &` |
| `005FCA60` | `PRendering::PTexture3DBase *` | `006D3C80` | `PDynamicGeometry::PRenderStream &` |
| `005FCB90` | `PRendering::PTextureCommonBase *` | `006D3D80` | `PDynamicGeometry::PRenderStreamInput &` |
| `005FCCC0` | `PRendering::PTextureCubeMap *` | `006D3E80` | `PArray<PDynamicGeometry::PModifierAndInputs,8> *` |
| `005FCDF0` | `PRendering::PTextureCubeMapBase *` | `006D3FC0` | `PArray<PDynamicGeometry::PModifierNetworkBuffer,8> *` |
| `006190E0` | `PArray<unsigned char,1> &` | `006D4100` | `PArray<PDynamicGeometry::PRenderStreamInput,4> *` |
| `006191F0` | `PArray<PRendering::PStreamInputDescD3D11,8> &` | `006D4240` | `PDynamicGeometry::PModifierAndInputs *` |
| `00619300` | `PRendering::PConstantBufferD3D11 &` | `006D4370` | `PDynamicGeometry::PModifierNetwork *` |
| `00619400` | `PRendering::PIndirectArgsBufferD3D11 &` | `006D44A0` | `PDynamicGeometry::PModifierNetworkBuffer *` |
| `00619500` | `PRendering::PSamplerStateD3D11 &` | `006D45D0` | `PDynamicGeometry::PModifierNetworkInfoPacket *` |
| `00619600` | `PRendering::PShaderPassD3D11 &` | `006D4700` | `PDynamicGeometry::PModifierNetworkInfoPacket_Buffer *` |
| `00619700` | `PRendering::PShaderPassStateD3D11 &` | `006D4830` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode *` |
| `00619800` | `PRendering::PStreamInputDescD3D11 &` | `006D4960` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance *` |
| `00619900` | `PRendering::PStructuredBufferD3D11 &` | `006D4A90` | `PDynamicGeometry::PRenderStream *` |
| `00619A00` | `PRendering::PTexture2DD3D11 &` | `006D4BC0` | `PDynamicGeometry::PRenderStreamInput *` |
| `00619B00` | `PRendering::PTexture3DD3D11 &` | `006D8FD0` | `PDynamicGeometry::PMorphModifierWeightsUserDataObject &` |
| `00619C00` | `PRendering::PTextureCubeMapD3D11 &` | `006D90D0` | `PDynamicGeometry::PMorphModifierWeightsUserDataObject *` |
| `00619D00` | `CD3D11_BLEND_DESC const &` | `006DA250` | `POccluderGeometry::POccluderGeometryObject *` |
| `00619E10` | `CD3D11_DEPTH_STENCIL_DESC const &` | `00796640` | `PCameraProjection &` |
| `00619F20` | `CD3D11_RASTERIZER_DESC const &` | `00796760` | `PFramework::PDebugUtils &` |
| `0061A030` | `D3D11_DEPTH_STENCILOP_DESC const &` | `00796860` | `PFramework::PInputMapper &` |
| `0061A140` | `D3D11_RENDER_TARGET_BLEND_DESC const &` | `00796960` | `PFramework::PApplication *` |
| `0061A250` | `CD3D11_BLEND_DESC *` | `00796A90` | `PFramework::PApplicationViewport *` |
| `0061A390` | `CD3D11_DEPTH_STENCIL_DESC *` | `00796BC0` | `PFramework::PDebugUtils *` |
| `0061A4D0` | `CD3D11_RASTERIZER_DESC *` | `00796CF0` | `PFramework::PInputMapper *` |
| `0061A610` | `D3D11_DEPTH_STENCILOP_DESC *` | `0086EAF0` | `PArray<PInputs::PInputAction *,8> &` |
| `0061A750` | `D3D11_RENDER_TARGET_BLEND_DESC *` | `0086EC00` | `PArray<PInputs::PInputSource *,8> &` |
| `0061A890` | `PArray<unsigned char,1> *` | `0086ED10` | `PInputs::PInputAction &` |
| `0061A9D0` | `PArray<PRendering::PStreamInputDescD3D11,8> *` | `0086EE30` | `PInputs::PInputMap &` |
| `0061AB10` | `PRendering::PConstantBufferD3D11 *` | `0086EF30` | `PInputs::PInputSourceJoypadAxis &` |
| `0061AC40` | `PRendering::PIndirectArgsBufferD3D11 *` | `0086F050` | `PInputs::PInputSourceJoypadButton &` |
| `0061AD70` | `PRendering::PRenderTargetD3D11 *` | `0086F170` | `PInputs::PInputSourceKey &` |
| `0061AEA0` | `PRendering::PSamplerStateD3D11 *` | `0086F290` | `PInputs::PInputSourceMotionAngularVelocityX &` |
| `0061AFD0` | `PRendering::PShaderComputeProgramD3D11 *` | `0086F3B0` | `PInputs::PInputSourceMotionAngularVelocityY &` |
| `0061B100` | `PRendering::PShaderFragmentProgramD3D11 *` | `0086F4D0` | `PInputs::PInputSourceMotionAngularVelocityZ &` |
| `0061B230` | `PRendering::PShaderGeometryProgramD3D11 *` | `0086F5F0` | `PInputs::PInputSourceMotionLinearAccelerationX &` |
| `0061B360` | `PRendering::PShaderPassD3D11 *` | `0086F710` | `PInputs::PInputSourceMotionLinearAccelerationY &` |
| `0061B490` | `PRendering::PShaderPassStateD3D11 *` | `0086F830` | `PInputs::PInputSourceMotionLinearAccelerationZ &` |
| `0061B5C0` | `PRendering::PShaderProgramD3D11 *` | `0086F950` | `PInputs::PInputSourceMotionQuatW &` |
| `0061B6F0` | `PRendering::PShaderVertexProgramD3D11 *` | `0086FA70` | `PInputs::PInputSourceMotionQuatX &` |
| `0061B820` | `PRendering::PStreamInputDescD3D11 *` | `0086FB90` | `PInputs::PInputSourceMotionQuatY &` |
| `0061B950` | `PRendering::PStreamInputLayoutD3D11 *` | `0086FCB0` | `PInputs::PInputSourceMotionQuatZ &` |
| `0061BA80` | `PRendering::PStructuredBufferD3D11 *` | `0086FDD0` | `PInputs::PInputSourceMouseButton &` |
| `0061BBB0` | `PRendering::PTexture2DD3D11 *` | `0086FEF0` | `PInputs::PInputSourceMouseDeltaX &` |
| `0061BCE0` | `PRendering::PTexture3DD3D11 *` | `00870010` | `PInputs::PInputSourceMouseDeltaY &` |
| `0061BE10` | `PRendering::PTextureCubeMapD3D11 *` | `00870130` | `PInputs::PInputSourceTouchDragX &` |
| `006364B0` | `PSharray<PString> &` | `00870250` | `PInputs::PInputSourceTouchDragY &` |
| `006365C0` | `PClusterDependencyList &` | `00870370` | `PInputs::PInputSourceTouchPinch &` |
| `006366C0` | `PClassDescriptor const &` | `00870490` | `PInputs::PInputSourceTouchRotate &` |
| `006367E0` | `PSharray<PString> *` | `008705B0` | `PInputs::PInputSourceTouchTwoFingerDragX &` |
| `00636920` | `PBase *` | `008706D0` | `PInputs::PInputSourceTouchTwoFingerDragY &` |
| `00636A50` | `PClassDataMemberDynamic *` | `008707F0` | `PInputs::PInputSourceVisionTrackerX &` |
| `00636B80` | `PClassDescriptor *` | `00870910` | `PInputs::PInputSourceVisionTrackerY &` |
| `00636CB0` | `PClassDescriptorDynamic *` | `00870A30` | `PInputs::PInputSourceVisionTrackerZ &` |
| `00636DE0` | `PClassMember *` | `00870B50` | `PArray<PInputs::PInputAction *,8> *` |
| `00636F10` | `PClusterDependencyList *` | `00870C90` | `PArray<PInputs::PInputSource *,8> *` |
| `00637040` | `PNamespace *` | `00870DD0` | `PInputs::PInputAction *` |
| `00637170` | `PWorld *` | `00870F00` | `PInputs::PInputMap *` |
| `0064AF20` | `PArray<PPostProcessing::PPostEffectBase *,8> &` | `00871030` | `PInputs::PInputSource *` |
| `0064B030` | `PPostProcessing::PAtmospherics &` | `00871160` | `PInputs::PInputSourceJoypadAxis *` |
| `0064B150` | `PPostProcessing::PAtmosphericsBase &` | `00871290` | `PInputs::PInputSourceJoypadButton *` |
| `0064B270` | `PPostProcessing::PAtmosphericsD3D11 &` | `008713C0` | `PInputs::PInputSourceKey *` |
| `0064B390` | `PPostProcessing::PCelShading &` | `008714F0` | `PInputs::PInputSourceMotionAngularVelocityX *` |
| `0064B4B0` | `PPostProcessing::PCelShadingBase &` | `00871620` | `PInputs::PInputSourceMotionAngularVelocityY *` |
| `0064B5D0` | `PPostProcessing::PCelShadingD3D11 &` | `00871750` | `PInputs::PInputSourceMotionAngularVelocityZ *` |
| `0064B6F0` | `PPostProcessing::PDeferredLighting &` | `00871880` | `PInputs::PInputSourceMotionLinearAccelerationX *` |
| `0064B810` | `PPostProcessing::PDeferredLightingBase &` | `008719B0` | `PInputs::PInputSourceMotionLinearAccelerationY *` |
| `0064B930` | `PPostProcessing::PDeferredLightingD3D11 &` | `00871AE0` | `PInputs::PInputSourceMotionLinearAccelerationZ *` |
| `0064BA50` | `PPostProcessing::PDepthOfField &` | `00871C10` | `PInputs::PInputSourceMotionQuatW *` |
| `0064BB70` | `PPostProcessing::PDepthOfFieldBase &` | `00871D40` | `PInputs::PInputSourceMotionQuatX *` |
| `0064BC90` | `PPostProcessing::PDepthOfFieldD3D11 &` | `00871E70` | `PInputs::PInputSourceMotionQuatY *` |
| `0064BDB0` | `PPostProcessing::PFXAA &` | `00871FA0` | `PInputs::PInputSourceMotionQuatZ *` |
| `0064BED0` | `PPostProcessing::PFXAABase &` | `008720D0` | `PInputs::PInputSourceMouseButton *` |
| `0064BFF0` | `PPostProcessing::PFXAAD3D11 &` | `00872200` | `PInputs::PInputSourceMouseDeltaX *` |
| `0064C110` | `PPostProcessing::PGlow &` | `00872330` | `PInputs::PInputSourceMouseDeltaY *` |
| `0064C230` | `PPostProcessing::PGlowBase &` | `00872460` | `PInputs::PInputSourceTouchDragX *` |
| `0064C350` | `PPostProcessing::PGlowD3D11 &` | `00872590` | `PInputs::PInputSourceTouchDragY *` |
| `0064C470` | `PPostProcessing::PGlowGPUBase &` | `008726C0` | `PInputs::PInputSourceTouchPinch *` |
| `0064C590` | `PPostProcessing::PLowResParticles &` | `008727F0` | `PInputs::PInputSourceTouchRotate *` |
| `0064C6B0` | `PPostProcessing::PMLAA &` | `00872920` | `PInputs::PInputSourceTouchTwoFingerDragX *` |
| `0064C7D0` | `PPostProcessing::PMLAABase &` | `00872A50` | `PInputs::PInputSourceTouchTwoFingerDragY *` |
| `0064C8F0` | `PPostProcessing::PMLAAD3D11 &` | `00872B80` | `PInputs::PInputSourceVisionTrackerX *` |
| `0064CA10` | `PPostProcessing::PMaterialPostEffect &` | `00872CB0` | `PInputs::PInputSourceVisionTrackerY *` |
| `0064CB30` | `PPostProcessing::PMeshParticleSystemBase &` | `00872DE0` | `PInputs::PInputSourceVisionTrackerZ *` |
| `0064CC50` | `PPostProcessing::PMotionBlur &` | `00874DA0` | `PVision::PVisionMoveTracker &` |
| `0064CD70` | `PPostProcessing::PMotionBlurBase &` | `00874EA0` | `PVision::PVisionMoveTracker *` |
| `0064CE90` | `PPostProcessing::PMotionBlurD3D11 &` | `00874FD0` | `PVision::PVisionMoveTrackerBase *` |
| `0064CFB0` | `PPostProcessing::PPostEffectBase &` | `00875100` | `PVision::PVisionMoveTrackerWin32 *` |
| `0064D0D0` | `PPostProcessing::PPostEffectManager &` | `00875980` | `PVision::PVisionTracker &` |
| `0064D1D0` | `PPostProcessing::PScreenSpaceAmbientOcclusion &` | `00875A80` | `PVision::PVisionTracker *` |
| `0064D2F0` | `PPostProcessing::PScreenSpaceAmbientOcclusionBase &` | `00875BB0` | `PVision::PVisionTrackerBase *` |
| `0064D410` | `PPostProcessing::PScreenSpaceAmbientOcclusionD3D11 &` | `00875CE0` | `PVision::PVisionTrackerWin32 *` |
| `0064D530` | `PPostProcessing::PScreenSpaceReflection &` | `00878C70` | `PHierarchy::POctree *` |
| `0064D650` | `PPostProcessing::PScreenSpaceReflectionBase &` | `00878DA0` | `PHierarchy::POctreeChildren *` |
| `0064D770` | `PPostProcessing::PScreenSpaceReflectionD3D11 &` | `00878ED0` | `PHierarchy::POctreeData *` |
| `0064D890` | `PArray<PPostProcessing::PPostEffectBase *,8> *` | `00879000` | `PHierarchy::POctreeWorld *` |
| `0064D9D0` | `PPostProcessing::PAtmospherics *` | `0087A200` | `PArray<PInputs::PInputMap *,8> &` |
| `0064DB00` | `PPostProcessing::PAtmosphericsBase *` | `0087A310` | `PGame::PGameConfig &` |
| `0064DC30` | `PPostProcessing::PAtmosphericsD3D11 *` | `0087A410` | `PArray<PInputs::PInputMap *,8> *` |
| `0064DD60` | `PPostProcessing::PCelShading *` | `0087A550` | `PGame::PGameConfig *` |
| `0064DE90` | `PPostProcessing::PCelShadingBase *` | | |

## Audit pass 1 - 2026-09-13 (OPUS): two adapter families declared, and this page's own two are NOT provable

*(Static only - masked byte comparison over every member of each tag group. Nothing executed.)*

### Declared

| family | members | excluded | shape |
|---|---:|---:|---|
| script-VM object push adapters | **304** | 1 | 188 at 21 B push directly; 116 at 31 B add a constant member offset under a null guard. **All 304 tail-jump to one target, `00684080`.** |
| script-VM nullable object push adapters | **295** | 4 | load, branch to a null push when null, else add the offset and push. **All 295 reach `00684080`, `0080F420` and `00810620` exactly 295 times each - one per member.** |

**The sub-shapes are an artefact of the instrument, not of the code.** Within each family the
variants differ **only in an offset immediate** (8, 1, 0x30, 0x10), and a mask over call and `lea`
operands cannot see an immediate. That is
[`family_prover.py`](../../../Tools/analysis-kit/gfz-scripts/family_prover.py)'s documented blind
spot, and it is why the members were chosen by **body size plus inspection** rather than by taking
the mask's shape count at face value.

**The excluded members are the control.** Each tag group contained a small number of bodies that
are a genuinely different idiom - a virtual call through `[rcx+8]`, or a **dynamic** offset read
from the class descriptor at `[rcx+0xF4]` instead of a constant. They are named by address in the
members files. **A family that excludes nothing has usually not been looked at.**

### ⚠ The two families this page is named for cannot be proved by this instrument

`owner_layer` names `Phyre.ScriptVM.ObjectPointerAccessor` and `ObjectReferenceAccessor`. Under the
same test:

| group | members | sizes | distinct masked shapes |
|---|---:|---:|---:|
| `ObjectPointerAccessor` | 323 | **2** | **323** |
| `ObjectReferenceAccessor` | 264 | **2** | **264** |

**Two body sizes and one distinct image per member** - the bodies are structurally identical and
differ by their **field-offset immediates**, exactly the blind spot above. So these two are
**unproved, not disproved**, and they are deliberately **left undeclared**: the honest reading is
that this instrument cannot settle them, and declaring 587 functions on an instrument that cannot
see what distinguishes them would be asserting the bar rather than meeting it.

**What would settle them:** a mask that blanks immediates as well as displacements, or a decode
that compares instruction *forms* rather than bytes. Either is a small change to the prover and
neither has been made yet.

## Audit pass 2 - 2026-09-13 (OPUS): the two families this page is named for, settled

*(Static only. Nothing executed.)*

Audit pass 1 left these **deliberately undeclared**, saying the instrument could not settle them and
that *"what would settle them is a mask that blanks immediates, or a decode that compares instruction
forms."* That decode now exists (`family_prover.py --forms`) and they are settled.

| group | members | body sizes | byte images | **form images** |
|---|---:|---|---:|---:|
| `ObjectPointerAccessor` | 323 | 301 B (203), 302 B (120) | 323 | **2** |
| `ObjectReferenceAccessor` | 264 | 249 B (160), 282 B (104) | 264 | **2** |

**Two forms each, matching the two body sizes exactly.** The 323 byte images were never 323
functions; they were one generator emitting one field offset per member.

### The control, after an instrument error of my own

External call and jump targets, **with intra-body branches excluded**:

```
ObjectPointerAccessor    00811130 x646   00812960 x646   008119F0 x646   00682980 x323
ObjectReferenceAccessor  00812960 x528   00682980 x264   00811130 x264   0063BC00 x264
```

**Every count is an exact multiple of the member count**, and three of the four targets are shared
between the two groups.

> **My first census of this reported 108 targets for `ObjectReferenceAccessor` and I nearly wrote
> that each member calls its own per-type handler.** The 104 "member-specific targets" were
> **intra-body `jmp`s** - local branches over an else-arm, landing six bytes further into the same
> function. I had counted a jump target without asking whether it left the body. Excluding
> intra-body branches leaves **four**. *The family is cleaner than the error made it look, which is
> the direction that makes an error easy to keep.*

### What a form match does and does not prove

`--forms` drops constants. So it proves *these bodies are the same instruction sequence*, **not**
*the differing constants are irrelevant*. For these accessors the constant **is** the payload - the
field offset each one reaches - and the note says so.

**That distinction is not academic in this database.** A single immediate is the difference between
a unit dying at 0 HP and dying at 1000
([the HP contract](../../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md) §6). A form
prover that reported "same family, constants irrelevant" would be the same error wearing a tool's
authority.

**Not claimed.** The four shared implementations (`00682980`, `00811130`, `00812960`, `008119F0`,
`0063BC00`) are ~~**all still in the frontier**~~ *not in these rows — updated 2026-09-13: `00811130`, `00812960` and `008119F0` are Lua API bodies declared on the Lua library row, and `00682980` is `luaL_testudata` for `PhyreObject` (AZ-1)*, and what field any accessor reaches is untouched.
Nothing executed.

**The remaining 160 are dispositioned — by the module families, 2026-09-16 (SWE2-EC7).**
FABLE's `pobjectaccessor_undeclared_160.txt` — the `PObjectAccessor::Get` bodies the two accessor
rows above do not cover (140 binding `PArray`/`PSharray` container types, 20 binding other types) —
is now fully declared, just under a different home than this page. The per-module provenance
selector (`../members/select_phyre_module.py`, the `PHYRE-MODULES-AFTER-PILOT` package at
`4729fa0e`) absorbed every one: each body's only inbound references come from module-bound template
records, so it joined the family of the module its bound type names — PRendering 46, PhyreCore 44,
PAnimation 24, PGeometry 16, PDynamicGeometry 12, PInputs 6, PPostProcessing 2, PText 2, PPhysics 2,
PGameplay 2, PLOD 2, PScripting 1; one is A-measured. That is the same provenance claim this page
makes for the 587 — Phyre-generated code parameterized on a bound type — with the module that owns
the type stated. **747 of 747 are now dispositioned** (587 here, 160 under the module rows); the
four shared implementations named above remain not dispositioned.

## The class each generated adapter belongs to, from the descriptor vtable

**2026-09-19 (OPUS).** Four of the families on this page carry the same open question in their
own words — *"NOT dispositioned: the shared implementations they delegate to, and **whatever
object or member each adapter names**."* For the members that sit in a Phyre class descriptor's
vtable, that is now answered, and the answer is a table rather than a paragraph:
[`../Reflection-And-Class-Metadata/members/phyre-class-descriptor-vtable.tsv`](../Reflection-And-Class-Metadata/members/phyre-class-descriptor-vtable.tsv),
315 classes.

Every Phyre class's `PClassDescriptorConcrete<T>` object has a vtable installed by its own
constructor, and four of its slots hold one function per class:

| slot | family on this page | members named |
|---|---|--:|
| `+0x20` | `object-push-adapters` (304) | **297** |
| `+0x28` | the object-pointer accessor getter | **314 of 315** |
| `+0x30` | `nullable-object-push-adapters` (295) | **287** |
| `+0x38` | — the descriptor's own deleting destructor, not an adapter | 315 |

The remainder are not unexplained: `+0x20`'s other 18 are 5 in
`nativeadapter-descriptorforwardtailcall`, 4 in `nativeadapter-optptrallocrecordinstall` and 9 in
no family (eight at the same 21/31 B, one an 11-byte stub); `+0x30`'s other 28 are 16 in
`optptr-static-descriptor-dispatch-adapters`, 7 in `optptr-offsetadd-dispatch-adapters` and 5
stubs.

**`+0x28` is the control that makes the rest credible, and it is a name agreement.** Its body is
26 bytes on all 315 — `mov rcx,rdx ; mov rbx,r8 ; call <X> ; mov [rbx],rax ; ret` — and resolving
`X` in this page's own 747-entry address-to-bound-type table gives **314 hits whose bound type's
leaf name equals the class name, with 0 mismatches**. That table was built from RTTI xrefs; the
class name came from the string the descriptor constructor `lea`s into `r8`. Neither derives from
the other, and a wrong vtable would not land on the right name 314 times.

**What this does not do.** It names the class an adapter belongs to. It does not disposition the
shared implementations they delegate to — `00684080`, `0080F420`, `00810620`, `00682980` — which
remain exactly as open as this page already records, and it says nothing about the 400-odd
adapters in these families that no descriptor vtable references.

## SWE2-EC7-68 update (2026-09-19) - `00683BF0` two-key member getter

`00683BF0` (62 B) is the two-key member getter the accessor vtable
rows share: `00682A10(rcx, -1)` first, then `00811130(rcx, -2)`; a
non-null result is returned verbatim, otherwise the body returns
`&02E41580`, the shared empty-member object. Interior anchor
`00683C10` (the `00811130` call).

## SWE2-EC7-78 update (2026-09-20) - `00682A10` validate-and-decorate chain measured

`00682A10` (143 B) is the accessor's guarded fetch:
`00811950(rcx, edx)` produces `rsi`; both it and a `0080FBA0` probe
must succeed, then `0080FA50(rcx, 0xFFF0B9D8, "Vector")` decorates
and `00810810(rcx, -1, -2)` runs; a nonzero there sets `bl` and
`00811130(rcx, -3)` finishes. `rsi` returns only when `bl` stood -
else 0.
Interior anchor `00682A3F` (the `"Vector"` lea).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Presentation - CLIENT (1 edge).** `005AD8F0` is called by bodies filed to Presentation: `005C5C80` - shared machinery across the layer boundary, no shared ownership.

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-phyre-script-object-accessors-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00584910` | 63 B | calls `00599870(rdx)` and copies 0x48 bytes from the result P to `r8`: four 16-byte blocks at `+0x0` to `+0x30` and the qword at `+0x40` | `0058491C`, `00584924`, `0058493B`, `00584944` |
| `00584B70` | 67 B | calls `00599970(rdx)` and copies 0x54 bytes from the result P to `r8`: five 16-byte blocks at `+0x0` to `+0x40` and the dword at `+0x50` | `00584B7C`, `00584B84`, `00584BA3`, `00584BAA` |
| `00585060` | 43 B | calls `00599A70(rdx)` and copies 0x24 bytes from the result P to `r8`: 16-byte blocks at `+0x0` and `+0x10` and the dword at `+0x20` | `0058506C`, `00585074`, `0058507B`, `00585082` |
| `005A0B60` | 28 B | calls `005A05D0(rdx)` and copies the byte at the result pointer to byte `[r8]` | `005A0B6C`, `005A0B71`, `005A0B74` |
| `005A0D30` | 45 B | calls `005BA950(rdx)` and copies from the result P to `r8` at the same offsets the dword `+0x8` and the qwords `+0x10` and `+0x18` | `005A0D3C`, `005A0D44`, `005A0D4B`, `005A0D53` |
| `005A0FB0` | 112 B | calls `005B96D0(rdx)` and does nothing more when the result P equals `r8`; otherwise copies the dword `+0x20` and the qwords `+0x0`, `+0x8`, `+0x10` and `+0x18` from P to `r8`, then, when `r8+0x28` differs from `P+0x28`, calls `001EAD40(r8+0x28, Q)` where Q is qword `P+0x28` minus (byte `P+0x28` AND 1), and finally copies the dword `+0x30` | `005A0FC0`, `005A0FC8`, `005A0FD4`, `005A100A`, `005A1012` |
| `005A1260` | 53 B | calls `005B9CD0(rdx)` and copies from the result P to `r8` at the same offsets the dword `+0x8` and the qwords `+0x10`, `+0x18` and `+0x20` | `005A126C`, `005A1274`, `005A127B`, `005A128B` |
| `005A1820` | 45 B | calls `005BAA70(rdx)` and copies from the result P to `r8` at the same offsets the dword `+0x8` and the qwords `+0x10` and `+0x18` | `005A182C`, `005A1834`, `005A183B`, `005A1843` |
| `005A1BF0` | 33 B | calls `005B98D0(rdx)` and tail-jumps to `005AA8C0(r8, result)` | `005A1BFC`, `005A1C01`, `005A1C04`, `005A1C0C` |
| `005A1DD0` | 64 B | calls `005BA750(rdx)` and copies the qword `+0x0` of the result P to `[r8]`; then, when `r8+8` differs from `P+8`, tail-jumps to `001EAD40(r8+8, Q)` where Q is qword `P+8` minus (byte `P+8` AND 1), else returns | `005A1DDC`, `005A1DE8`, `005A1DEF`, `005A1E05` |
| `005A1EF0` | 29 B | calls `005BAEB0(rdx)` and copies the dword `+0x8` of the result to dword `r8+0x8` | `005A1EFC`, `005A1F01`, `005A1F04` |
| `005A20B0` | 33 B | calls `005B95D0(rdx)` and tail-jumps to `005AA840(r8, result)` | `005A20BC`, `005A20C1`, `005A20CC` |
| `005A2430` | 55 B | calls `005BAFD0(rdx)` and copies from the result P to `r8` at the same offsets the dword `+0x8`, the qword `+0x10` and the dwords `+0x18`, `+0x1C` and `+0x20` | `005A243C`, `005A2444`, `005A244B`, `005A2452`, `005A245E` |
| `005A2770` | 73 B | calls `005B94D0(rdx)`, then with the result P calls `005AA840(r8, P)`, copies the qword `+0x48` from P to `r8`, calls `005AA3C0(r8+0x50, P+0x50)` and copies the dword `+0x60` | `005A2780`, `005A278E`, `005A279B`, `005A27A3`, `005A27B0` |
| `005A3260` | 67 B | calls `005B9BD0(rdx)` and does nothing more when the result P equals `r8`; otherwise calls `005AA840(r8, P)` and copies the qword `+0x38` and the 16 bytes at `+0x48` from P to `r8` | `005A3270`, `005A3278`, `005A3283`, `005A328C`, `005A3294` |
| `005A4390` | 58 B | calls `005BAB90(rdx)`, then with the result P calls `005AA7D0(r8, P)` and tail-jumps to `005AA3C0(r8+0x28, P+0x28)` | `005A43A0`, `005A43AE`, `005A43C5` |
| `005A5050` | 58 B | calls `005B93B0(rdx)`, then with the result P calls `005AA7D0(r8, P)` and tail-jumps to `005AA3C0(r8+0x28, P+0x28)` | `005A5060`, `005A506E`, `005A5085` |
| `005A50B0` | 39 B | calls `005B97D0(rdx)`, copies the dword `+0x0` of the result P to `[r8]` and tail-jumps to `005AA3C0(r8+8, P+8)` | `005A50BC`, `005A50C7`, `005A50D2` |
| `005C1390` | 91 B | calls `005BC4D0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`, then calls `0080F420(rdx, 1)` and `00810580(rdx, eax result)` and returns 1 | `005C13A3`, `005C13AB`, `005C13B4`, `005C13C1`, `005C13CB` |
| `005C13F0` | 103 B | calls `005BC4D0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`, then calls `0080F420(rdx, 1)` and `00810640(rdx)` with the call's `xmm0` result passed in `xmm1`, and returns 1 | `005C1403`, `005C140B`, `005C1419`, `005C1427`, `005C1432` |
| `005C15B0` | 123 B | calls `005BC4D0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`; a non-null result R goes to `00684080(rdx, R, 02CAE660)`, a null result to `0080F420(rdx, 1)` then `00810620(rdx)`, and both paths return 1 | `005C15C3`, `005C15D4`, `005C15DD`, `005C15E9`, `005C160B` |
| `005C1A30` | 40 B | calls `005BC4D0(rdx)` and, when the result P is non-null, calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`; returns 0 on both paths | `005C1A3C`, `005C1A44`, `005C1A4D`, `005C1A50` |
| `005C1AC0` | 92 B | calls `005BC4D0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`, zero-extends the low byte of its result, then calls `0080F420(rdx, 1)` and `00810450(rdx, that byte)` and returns 1 | `005C1AD3`, `005C1ADB`, `005C1AEF`, `005C1AF2`, `005C1AFC` |
| `005C1BB0` | 89 B | calls `005BCAC0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P; its result R becomes `R+0x30` when non-null (null stays 0) and goes to `00684080(rdx, that, 02CF8470)`, returning 1 | `005C1BC3`, `005C1BCB`, `005C1BD0`, `005C1BD8`, `005C1BE9` |
| `005C1C70` | 89 B | calls `005BCAC0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, then calls `0080F420(rdx, 1)` and `00810660(rdx, 64-bit result)` and returns 1 | `005C1C83`, `005C1C8B`, `005C1C90`, `005C1C9E`, `005C1CA9` |
| `005C1CD0` | 120 B | calls `005BCAC0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P; a non-null result R goes to `00684080(rdx, R+0x30, 02CF8470)`, a null result to `0080F420(rdx, 1)` then `00810620(rdx)`, and both paths return 1 | `005C1CE3`, `005C1CF0`, `005C1CF9`, `005C1D06`, `005C1D28` |
| `005C1E00` | 99 B | calls `005BCD20(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, then calls `0080F420(rdx, 1)` and `00810640(rdx)` with the call's `xmm0` result passed in `xmm1`, and returns 1 | `005C1E13`, `005C1E1B`, `005C1E25`, `005C1E33`, `005C1E3E` |
| `005CF610` | 73 B | calls `005F2DE0(rdx)` and copies from the result P to `r8` the 16-byte blocks `+0x0` and `+0x10`, the qword `+0x20`, the dword `+0x28` and the qword `+0x30`, then tail-jumps to `00646C00(r8+0x38, P+0x38)` | `005CF61C`, `005CF628`, `005CF638`, `005CF640`, `005CF654` |
| `005CFA40` | 99 B | calls `005F47E0(rdx)` and copies from the result P to `r8` the word `+0x0` and the bytes `+0x2` and `+0x3`; when `r8+8` differs from `P+8`, calls `001EAD40(r8+8, Q)` where Q is qword `P+8` minus (byte `P+8` AND 1); then copies the dwords `+0x10` and `+0x14` | `005CFA50`, `005CFA5F`, `005CFA74`, `005CFA87`, `005CFA8F` |
| `005D0710` | 107 B | calls `005F4BE0(rdx)`, copies the 16 bytes `+0x0` of the result P to `r8`, clears the top bit (bit index 31) of dword `P+0x10` and calls `005E2F20(that value, qword P+0x18)`; when the old qword `r8+0x18` differs from that result, the top bit of the old dword `r8+0x10` is clear and the old qword is non-null, it calls `00584730(old qword)`; then stores the result to qword `r8+0x18` and the cleared value to dword `r8+0x10` | `005D0725`, `005D0737`, `005D073D`, `005D075F`, `005D076D` |
| `005D09F0` | 101 B | calls `005F51E0(rdx)` and copies the qword `+0x0` of the result P to `r8`; when `r8+8` differs from `P+8`, calls `001EAD40(r8+8, Q)` where Q is qword `P+8` minus (byte `P+8` AND 1); then copies the dword `+0x10`, the word `+0x14` and the bytes `+0x16` and `+0x17` | `005D0A00`, `005D0A0F`, `005D0A29`, `005D0A31`, `005D0A47` |
| `005D1990` | 58 B | calls `005F50E0(rdx)`, then with the result P calls `005DE830(r8, P)` and tail-jumps to `005DE680(r8+0x10, P+0x10)` | `005D19A0`, `005D19AE`, `005D19C5` |
| `005D24C0` | 107 B | calls `005F4DE0(rdx)`, copies the 16 bytes `+0x0` of the result P to `r8`, clears the top bit (bit index 31) of dword `P+0x10` and calls `005E2FB0(that value, qword P+0x18)`; when the old qword `r8+0x18` differs from that result, the top bit of the old dword `r8+0x10` is clear and the old qword is non-null, it calls `00584730(old qword)`; then stores the result to qword `r8+0x18` and the cleared value to dword `r8+0x10` | `005D24D5`, `005D24E7`, `005D24ED`, `005D250F`, `005D251D` |
| `005D2C80` | 90 B | calls `005F2BE0(rdx)`; when the result P differs from `r8`, calls `001EAD40(r8, Q)` where Q is qword `[P]` minus (byte `[P]` AND 1); then, when `r8+8` differs from `P+8`, calls `001EAD40(r8+8, Q)` where Q is qword `P+8` minus (byte `P+8` AND 1) | `005D2C90`, `005D2C98`, `005D2CAC`, `005D2CB9`, `005D2CCA` |
| `005D3D10` | 84 B | calls `005F34E0(rdx)`, copies the dword `+0x0` of the result P to `[r8]`, calls `005DE710(r8+8, P+8)`, `005DE680(r8+0x18, P+0x18)` and `005DE830(r8+0x28, P+0x28)`, and copies the dword `+0x38` | `005D3D20`, `005D3D34`, `005D3D41`, `005D3D4E`, `005D3D5B` |
| `005D7990` | 95 B | calls `005F2EE0(rdx)` and copies the qword `+0x0` of the result P to `r8`; when `r8+8` differs from `P+8`, calls `001EAD40(r8+8, Q)` where Q is qword `P+8` minus (byte `P+8` AND 1); then copies the word `+0x10` and the bytes `+0x12` and `+0x13` | `005D79A0`, `005D79AF`, `005D79C9`, `005D79D2`, `005D79E1` |
| `005FF6D0` | 115 B | calls `00811470(rdx, -1, 0)`, `00811130(rdx, -2)`, `00683B50(rdx)` and `005F8450(rdx)`; when the last is non-null it calls the function pointer at qword `rcx+8` with that result, the `00683B50` result and the `00811470` result as a dword; returns 0 on both paths | `005FF6F3`, `005FF703`, `005FF70B`, `005FF716`, `005FF729` |
| `005FF750` | 115 B | calls `00811640(rdx, -1, 0)`, `00811130(rdx, -2)`, `00683B50(rdx)` and `005F8450(rdx)`; when the last is non-null it calls the function pointer at qword `rcx+8` with that result, the `00683B50` result and the `00811640` `xmm0` result in `xmm2`; returns 0 on both paths | `005FF773`, `005FF783`, `005FF78B`, `005FF796`, `005FF7A9` |
| `005FF880` | 104 B | calls `00683BF0(rdx)` and loads 16 bytes from its result, then calls `00683B50(rdx)` and `005F8450(rdx)`; when the last is non-null it stores the 16 bytes to a stack slot and calls the function pointer at qword `rcx+8` with that result, the `00683B50` result and the slot's address; returns 0 on both paths | `005FF89D`, `005FF8A5`, `005FF8B3`, `005FF8C2`, `005FF8CE` |
| `005FF990` | 120 B | calls `00811470(rdx, -1, 0)`, `00811130(rdx, -2)` and `005F86B0(rdx)`, returning 0 when the last is null; otherwise calls the function pointer at qword `rcx+8` with that result and the `00811470` result as a dword, passes its result to `00684130(rdx, result)` and returns 1 | `005FF9AE`, `005FF9BE`, `005FF9C6`, `005FF9D5`, `005FF9DE` |
| `005FFCC0` | 134 B | calls `00811470(rdx, -1, 0)`, `00811130(rdx, -2)` and `005F94F0(rdx)`, returning 0 when the last is null; otherwise calls the function pointer at qword `rcx+8` with that result and the `00811470` result as a dword, then calls `0080F420(rdx, 1)` and `00810580(rdx, eax result)` and returns 1 | `005FFCDE`, `005FFCEE`, `005FFCF6`, `005FFD05`, `005FFD1C` |
| `005FFDE0` | 89 B | calls `005FCB90(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, then calls `0080F420(rdx, 1)` and `00810660(rdx, 64-bit result)` and returns 1 | `005FFDF3`, `005FFDFB`, `005FFE00`, `005FFE0E`, `005FFE19` |
| `00604220` | 127 B | reads the dword at `+4` of the thread-local block indexed by dword `02EAED3C` (via `gs:[0x58]`) and, unless dword `02CED0B8` is greater (signed) than that dword, returns the address `02CED0A0`; otherwise calls `008092FC` with the address `02CED0B8` and, only when dword `02CED0B8` is then -1, stores the address `02CB77A0` OR 1 to qword `02CED0A0`, calls `005D8CA0()` and stores its result to qword `02CED0A8`, zeroes qword `02CED0B0` and calls `0080929C` with the address `02CED0B8`; both paths return `02CED0A0` | `0060423F`, `0060425F`, `00604273`, `0060427A`, `00604298` |
| `006042A0` | 127 B | reads the dword at `+4` of the thread-local block indexed by dword `02EAED3C` (via `gs:[0x58]`) and, unless dword `02CED098` is greater (signed) than that dword, returns the address `02CED080`; otherwise calls `008092FC` with the address `02CED098` and, only when dword `02CED098` is then -1, stores the address `02CB77A0` OR 1 to qword `02CED080`, calls `005D8D70()` and stores its result to qword `02CED088`, zeroes qword `02CED090` and calls `0080929C` with the address `02CED098`; both paths return `02CED080` | `006042BF`, `006042DF`, `006042F3`, `006042FA`, `00604318` |
| `00611460` | 117 B | calls `00619700(rdx)` and copies 0x190 bytes from the result to `r8`: a loop of 3 passes each moving 0x80 bytes as eight 16-byte blocks, then one final 16-byte block at `+0x180` | `0061146C`, `00611471`, `00611487`, `006114C7`, `006114CC` |
| `00612A60` | 86 B | calls `00619800(rdx)`; when the result P differs from `r8`, calls `001EAD40(r8, Q)` where Q is qword `[P]` minus (byte `[P]` AND 1); then on both paths copies the qword `+0x8` and the dwords `+0x10`, `+0x14` and `+0x18` from P to `r8` | `00612A70`, `00612A78`, `00612A8C`, `00612A95`, `00612AAD` |
| `00624820` | 117 B | calls `00619D00(rdx)` and copies 0x108 bytes from the result to `r8`: a loop of 2 passes each moving 0x80 bytes as eight 16-byte blocks, then the qword at `+0x100` | `0062482C`, `00624831`, `00624847`, `00624887`, `0062488C` |
| `0063A150` | 121 B | calls `006366C0(rdx)` and `00636B80(rdx)`, returning 0 when the latter's result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10` and the `006366C0` result, zero-extends the low byte of its result, calls `0080F420(rdx, 1)` and `00810450(rdx, that byte)` and returns 1 | `0063A168`, `0063A173`, `0063A187`, `0063A192`, `0063A19F` |
| `0063C310` | 71 B | calls `00811640(rdx, -1, 0)`, keeps its `xmm0` result, calls `00811130(rdx, -2)` and stores the kept value as a 4-byte float to `[r8]` | `0063C32E`, `0063C33E`, `0063C348` |
| `0063C360` | 75 B | calls `00811640(rdx, -1, 0)`, converts its `xmm0` result from single to double precision, calls `00811130(rdx, -2)` and stores the double to qword `[r8]` | `0063C37E`, `0063C38E`, `0063C392`, `0063C39C` |
| `0065F390` | 71 B | calls `0066C800(rdx)`, then with the result P calls `006638A0(r8, P)` and `006632F0(r8+0x30, P+0x30)` and tail-jumps to `006636B0(r8+0x40, P+0x40)` | `0065F3A0`, `0065F3AE`, `0065F3BB`, `0065F3D2` |
| `0065FB70` | 71 B | calls `0066C600(rdx)`, then with the result P calls `006638A0(r8, P)` and `006632F0(r8+0x30, P+0x30)` and tail-jumps to `006636B0(r8+0x40, P+0x40)` | `0065FB80`, `0065FB8E`, `0065FB9B`, `0065FBB2` |
| `00660510` | 91 B | calls `0066BD00(rdx)`, then with the result P calls `00663560(r8, P)` and `00663400(r8+0x20, P+0x20)` and copies the dwords `+0x70`, `+0x74` and `+0x78` and the qword `+0x80` from P to `r8` | `00660520`, `0066052E`, `0066053B`, `00660543`, `0066055E` |
| `006613B0` | 91 B | calls `0066BA00(rdx)`, then with the result P calls `00663560(r8, P)` and `00663400(r8+0x20, P+0x20)` and copies the dwords `+0x70`, `+0x74` and `+0x78` and the qword `+0x80` from P to `r8` | `006613C0`, `006613CE`, `006613DB`, `006613E3`, `006613FE` |
| `0066FD90` | 118 B | calls `00683B50(rdx)` and `0066E900(rdx)`, returning 0 when the latter is null; otherwise calls the function pointer at qword `rcx+8` with that result and the `00683B50` result, sign-extends its `eax` result to 64 bits, calls `0080F420(rdx, 1)` and `00810580(rdx, that value)` and returns 1 | `0066FDA8`, `0066FDB3`, `0066FDC3`, `0066FDCE`, `0066FDDC` |
| `00674E90` | 100 B | calls `00676600(rdx)` and copies the qword `+0x0` of the result P to `r8`; when `r8+8` differs from `P+8`, calls `001EAD40(r8+8, Q)` where Q is qword `P+8` minus (byte `P+8` AND 1); both paths then copy the qword `+0x10` | `00674EA0`, `00674EAF`, `00674EC9`, `00674ED2`, `00674EE5` |
| `00677680` | 93 B | calls `00676810(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`; its result R becomes `R+0x30` when non-null (null stays 0) and goes to `00684080(rdx, that, 02CF8470)`, returning 1 | `00677693`, `0067769B`, `006776A4`, `006776AC`, `006776BD` |
| `006776E0` | 84 B | calls `00676810(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`, passes its result R to `00684080(rdx, R, 02E4D630)` and returns 1 | `006776F3`, `006776FB`, `00677704`, `00677714` |
| `00678F90` | 95 B | calls `00811640(rdx, -1, 0)`, keeps its `xmm0` result, calls `00811130(rdx, -2)` and `00678DE0(rdx)`; when the result P is non-null it calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10` and the kept value in `xmm1`; returns 0 on both paths | `00678FAE`, `00678FBE`, `00678FC6`, `00678FD7`, `00678FDA` |
| `0067EF00` | 73 B | calls `0067EDD0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, passes its result to `006B3610(rdx, result)` and returns 1 | `0067EF13`, `0067EF1B`, `0067EF20`, `0067EF29`, `0067EF2E` |
| `00680D20` | 76 B | calls `00683250(rdx)`; when the result P differs from `r8`, calls `001EAD40(r8, Q)` where Q is qword `[P]` minus (byte `[P]` AND 1); then on both paths copies the qwords `+0x8` and `+0x10` from P to `r8` | `00680D30`, `00680D38`, `00680D4C`, `00680D55`, `00680D62` |
| `0068A850` | 74 B | calls `0069A950(rdx)`, then with the result P calls `006928B0(r8, P)` and copies the qwords `+0x118` and `+0x120` from P to `r8` | `0068A860`, `0068A86E`, `0068A87A`, `0068A88D` |
| `0068BCC0` | 74 B | calls `0069A750(rdx)`, then with the result P calls `006928B0(r8, P)` and copies the qwords `+0x118` and `+0x120` from P to `r8` | `0068BCD0`, `0068BCDE`, `0068BCEA`, `0068BCFD` |
| `006A0EE0` | 77 B | calls `0069BFC0(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P plus the sign-extended dword `rcx+0x10`, passes its result to `006843D0(rdx, result)` and returns 1 | `006A0EF3`, `006A0EFB`, `006A0F04`, `006A0F0D` |
| `006A0FE0` | 99 B | calls `0069C220(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, then calls `0080F420(rdx, 1)` and `00810640(rdx)` with the call's `xmm0` result passed in `xmm1`, and returns 1 | `006A0FF3`, `006A0FFB`, `006A1005`, `006A1013`, `006A101E` |
| `006A1050` | 88 B | calls `0069C220(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, zero-extends the low byte of its result, then calls `0080F420(rdx, 1)` and `00810450(rdx, that byte)` and returns 1 | `006A1063`, `006A106B`, `006A107B`, `006A107E`, `006A1088` |
| `006A10B0` | 88 B | calls `0069D520(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P and the address of a 16-byte stack slot, copies the 16 bytes at its returned pointer to a second stack slot, calls `006843D0(rdx, address of that copy)` and returns 1 | `006A10C3`, `006A10CB`, `006A10D5`, `006A10E3`, `006A10E8` |
| `006A11C0` | 99 B | calls `0069D650(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, then calls `0080F420(rdx, 1)` and `00810640(rdx)` with the call's `xmm0` result passed in `xmm1`, and returns 1 | `006A11D3`, `006A11DB`, `006A11E5`, `006A11F3`, `006A11FE` |
| `006A1230` | 120 B | calls `0069D650(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P; a non-null result R goes to `00684080(rdx, R+8, 02E518D0)`, a null result to `0080F420(rdx, 1)` then `00810620(rdx)`, and both paths return 1 | `006A1243`, `006A1250`, `006A1259`, `006A1266`, `006A1288` |
| `006A1330` | 36 B | calls `0069D650(rdx)` and, when the result P is non-null, calls the function pointer at qword `rcx+8` with P; returns 0 on both paths | `006A133C`, `006A1344`, `006A1349`, `006A134C` |
| `006A13B0` | 88 B | calls `0069D650(rdx)` and returns 0 when the result P is null; otherwise calls the function pointer at qword `rcx+8` with P, zero-extends the low byte of its result, then calls `0080F420(rdx, 1)` and `00810450(rdx, that byte)` and returns 1 | `006A13C3`, `006A13CB`, `006A13DB`, `006A13DE`, `006A13E8` |

## Per-member rows: the class descriptor each object push adapters pushes (OPUS, 2026-10-03)

The family `script-VM object push adapters` (frontmatter: 304 members; 297 get a row here) shares the forms in the census table above (all reach the push target `00684080`), not repeated per row. What differs from member to member is the class descriptor X its one `lea r8, [X]` hands to the push. Each row anchors that `lea` (the member's distinguishing instruction) and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-object-push-adapters-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-object-push-adapters-1003/rows.tsv). A member without exactly one `lea r8`, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-object-push-adapters-1003/excluded.tsv).

### All 297 adapters (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 005A0E80 | `005A0E89` `lea` | `02CAD640` | PAnimationChannelTarget |
| 005A10F0 | `005A10FC` `lea` | `02CADD50` | PAnimationController |
| 005A1420 | `005A1429` `lea` | `02CAD040` | PBlendableAnimationSource |
| 005A1630 | `005A163C` `lea` | `02CAECE0` | PAnimationTargetBlenderController |
| 005A1A40 | `005A1A49` `lea` | `02CAD840` | PAnimationClip |
| 005A1BD0 | `005A1BD9` `lea` | `02CAE960` | PAnimationSlotFilterDeferredLoad |
| 005A1C90 | `005A1C9C` `lea` | `02CAEEE0` | PTimeController |
| 005A1FE0 | `005A1FE9` `lea` | `02CAD540` | PAnimationChannelBase |
| 005A2260 | `005A226C` `lea` | `02CAEFE0` | PTimeIntervalController |
| 005A25F0 | `005A25F9` `lea` | `02CAD440` | PAnimationChannel |
| 005A2AF0 | `005A2AFC` `lea` | `02CAEA60` | PAnimationSlotFilter |
| 005A2B60 | `005A2B69` `lea` | `02CAE350` | PAnimationDataSourceListEntry |
| 005A2FC0 | `005A2FCC` `lea` | `02CAF0E0` | PTimeScaleOffsetController |
| 005A3120 | `005A3129` `lea` | `02CADC50` | PAnimationConstantChannel |
| 005A3470 | `005A3479` `lea` | `02CAE450` | PAnimationNetworkInstanceTarget |
| 005A3670 | `005A3679` `lea` | `02CAE660` | PAnimationSet |
| 005A3950 | `005A395C` `lea` | `02CAD340` | PAnimationBlenderController |
| 005A3B60 | `005A3B69` `lea` | `02CAE760` | PAnimationSlotListIndex |
| 005A3D10 | `005A3D19` `lea` | `02CAE050` | PAnimationEvent |
| 005A3EE0 | `005A3EE9` `lea` | `02CADB40` | PAnimationClipBinding |
| 005A41C0 | `005A41CC` `lea` | `02CAEDE0` | PAnimationWeightedBlenderController |
| 005A43E0 | `005A43E9` `lea` | `02CAE860` | PAnimationSlotArray |
| 005A4460 | `005A4469` `lea` | `02CAD940` | PAnimationClipBindingChannelMap |
| 005A4810 | `005A481C` `lea` | `02CADE50` | PAnimationDataSource |
| 005A4A80 | `005A4A89` `lea` | `02CADA40` | PAnimationClipBindingDataBlockCache |
| 005A4D00 | `005A4D09` `lea` | `02CAE150` | PAnimationEventList |
| 005A4E50 | `005A4E5C` `lea` | `02CAD240` | PAnimationAdditiveBlenderController |
| 005A4E70 | `005A4E79` `lea` | `02CAD740` | PAnimationChannelTimes |
| 005A52C0 | `005A52CC` `lea` | `02CADF50` | PAnimationEventController |
| 005A5690 | `005A569C` `lea` | `02CAE550` | PAnimationNetworkInstance |
| 005A5880 | `005A588C` `lea` | `02CAE250` | PAnimationHierarchyNode |
| 005A58D0 | `005A58DC` `lea` | `02CAEBE0` | PAnimationSpuTargetBlenderController |
| 005CDE00 | `005CDE09` `lea` | `02CBA900` | PShaderParameterCaptureBufferRWTexture2D |
| 005CDE50 | `005CDE59` `lea` | `02CB6F80` | PMeshInstanceAttachPoint |
| 005CE540 | `005CE549` `lea` | `02CB6380` | PConstantBufferBase |
| 005CE5A0 | `005CE5AC` `lea` | `02CB7180` | PModifierNetworkDynamicMeshInstance |
| 005CE640 | `005CE649` `lea` | `02CB9600` | PShaderPassParameterLocationTypesBase |
| 005CE950 | `005CE959` `lea` | `02CB78A0` | PSamplerState |
| 005CE9F0 | `005CE9F9` `lea` | `02CBAB00` | PShaderSource |
| 005CEB00 | `005CEB09` `lea` | `02CB7BA0` | PContextVariantFoldingTable |
| 005CF010 | `005CF019` `lea` | `02CBB800` | PTexture2DBase |
| 005CF1B0 | `005CF1B9` `lea` | `02CBAA00` | PShaderParameterCaptureBufferRWTexture3D |
| 005CF300 | `005CF309` `lea` | `02CB6D80` | PMeshInstanceSegmentContext |
| 005CF790 | `005CF799` `lea` | `02CB9500` | PShaderParameterDefinition |
| 005CF7B0 | `005CF7B9` `lea` | `02CB6780` | PEffectVariant |
| 005CFD60 | `005CFD69` `lea` | `02CBBB00` | PTexture3D |
| 005CFE20 | `005CFE29` `lea` | `02CBB500` | PStructuredBufferBase |
| 005D0070 | `005D0079` `lea` | `02CB75A0` | PRenderTargetBase |
| 005D01C0 | `005D01C9` `lea` | `02CBA200` | PShaderParameterCaptureBufferSampler |
| 005D03A0 | `005D03A9` `lea` | `02CB7380` | PParameterBufferBase |
| 005D0600 | `005D0609` `lea` | `02CB9700` | PShaderPassParameterLocationTypes |
| 005D0780 | `005D0789` `lea` | `02CBAE00` | PShaderStreamDefinition |
| 005D0BA0 | `005D0BA9` `lea` | `02CB7280` | PNodeContext |
| 005D0BC0 | `005D0BC9` `lea` | `02CBA300` | PShaderParameterCaptureBufferStructuredBuffer |
| 005D13A0 | `005D13A9` `lea` | `02CBBC00` | PTextureCubeMapBase |
| 005D1400 | `005D1409` `lea` | `02CB7480` | PParameterBuffer |
| 005D1420 | `005D1429` `lea` | `02CB9A00` | PShaderPass |
| 005D14A0 | `005D14A9` `lea` | `02CBAC00` | PShaderProgramParamsAndStreams |
| 005D1880 | `005D1889` `lea` | `02CB9C00` | PShaderParameterCaptureBufferStream |
| 005D1A70 | `005D1A79` `lea` | `02CB7080` | PMeshInstanceBounds |
| 005D1E80 | `005D1E89` `lea` | `02CB6480` | PConstantBuffer |
| 005D1F30 | `005D1F39` `lea` | `02CBA400` | PShaderParameterCaptureBufferRWStructuredBuffer |
| 005D2230 | `005D2239` `lea` | `02CB9800` | PShaderPassParameterLocationTypesConstantBuffer |
| 005D25B0 | `005D25B9` `lea` | `02CB79A0` | PSceneRenderPass |
| 005D2880 | `005D2889` `lea` | `02CBAD00` | PShaderProgramBase |
| 005D2A30 | `005D2A39` `lea` | `02CB6A80` | PMaterialSwitch |
| 005D2A50 | `005D2A59` `lea` | `02CB9D00` | PShaderParameterCaptureBufferTextureBase |
| 005D2E90 | `005D2E99` `lea` | `02CBA500` | PShaderParameterCaptureBufferByteAddressBuffer |
| 005D3230 | `005D3239` `lea` | `02CB9B00` | PShaderPassStateBase |
| 005D33E0 | `005D33E9` `lea` | `02CBAF00` | PShaderVertexProgram |
| 005D3590 | `005D3599` `lea` | `02CB76A0` | PRenderTarget |
| 005D3600 | `005D3609` `lea` | `02CBB900` | PTexture2D |
| 005D3940 | `005D3949` `lea` | `02CB9000` | PShader |
| 005D3F10 | `005D3F19` `lea` | `02CBB600` | PStructuredBuffer |
| 005D4000 | `005D4009` `lea` | `02CB9100` | PShaderParameterCaptureBufferLocation |
| 005D4020 | `005D4029` `lea` | `02CBA600` | PShaderParameterCaptureBufferRWByteAddressBuffer |
| 005D4140 | `005D4149` `lea` | `02CBB300` | PShadowRenderer |
| 005D45B0 | `005D45B9` `lea` | `02CBB000` | PShaderFragmentProgram |
| 005D4940 | `005D4949` `lea` | `02CB6B80` | PMaterial |
| 005D4C50 | `005D4C59` `lea` | `02CB9F00` | PShaderParameterCaptureBufferTexture2D |
| 005D4D50 | `005D4D59` `lea` | `02CB6E80` | PMeshInstance |
| 005D4D70 | `005D4D79` `lea` | `02CB6680` | PEffect |
| 005D54A0 | `005D54A9` `lea` | `02CB9E00` | PShaderParameterCaptureConstantBuffer |
| 005D54F0 | `005D54F9` `lea` | `02CB9200` | PShaderParameterCaptureBufferLocationSize |
| 005D5530 | `005D5539` `lea` | `02CB6880` | PIndirectArgsBufferBase |
| 005D5AA0 | `005D5AA9` `lea` | `02CBBA00` | PTexture3DBase |
| 005D5AC0 | `005D5AC9` `lea` | `02CBB400` | PForwardShadowRenderer |
| 005D5AE0 | `005D5AE9` `lea` | `02CB9900` | PShaderPassBase |
| 005D5C20 | `005D5C29` `lea` | `02CB77A0` | PSamplerStateBase |
| 005D5CA0 | `005D5CA9` `lea` | `02CBB100` | PShaderGeometryProgram |
| 005D6430 | `005D6439` `lea` | `02CBA000` | PShaderParameterCaptureBufferTexture3D |
| 005D6620 | `005D6629` `lea` | `02CBBD00` | PTextureCubeMap |
| 005D68C0 | `005D68C9` `lea` | `02CBA700` | PShaderParameterCaptureBufferDataBlock |
| 005D68E0 | `005D68E9` `lea` | `02CB9300` | PShaderParameterCaptureBufferLocationType |
| 005D6B90 | `005D6B9C` `lea` | `02CB6580` | PDynamicMeshInstance |
| 005D6EC0 | `005D6EC9` `lea` | `02CBB200` | PShaderComputeProgram |
| 005D7280 | `005D7289` `lea` | `02CB7CA0` | PSceneWideParameterBuffer |
| 005D74B0 | `005D74B9` `lea` | `02CBA100` | PShaderParameterCaptureBufferTextureCubeMap |
| 005D7610 | `005D7619` `lea` | `02CB6C80` | PMeshInstanceSegmentStreamBinding |
| 005D7930 | `005D7939` `lea` | `02CBB700` | PTextureCommonBase |
| 005D7A70 | `005D7A79` `lea` | `02CBA800` | PShaderParameterCaptureBufferIndexDataBlock |
| 005D7AC0 | `005D7AC9` `lea` | `02CB9400` | PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 005D7F20 | `005D7F29` `lea` | `02CB6980` | PIndirectArgsBuffer |
| 005D8070 | `005D8079` `lea` | `02CB7AA0` | PShaderPassInfo |
| 00611230 | `00611239` `lea` | `02CF1E40` | PTexture3DD3D11 |
| 00611250 | `00611259` `lea` | `02CF1540` | PShaderPassStateD3D11 |
| 00611440 | `00611449` `lea` | `02CF1940` | PShaderVertexProgramD3D11 |
| 00611830 | `00611839` `lea` | `02CF1A40` | PShaderFragmentProgramD3D11 |
| 00611930 | `00611939` `lea` | `02CF1440` | PShaderPassD3D11 |
| 00611CA0 | `00611CA9` `lea` | `02CF2440` | PConstantBufferD3D11 |
| 00611EA0 | `00611EA9` `lea` | `02CF1B40` | PShaderGeometryProgramD3D11 |
| 006121F0 | `006121F9` `lea` | `02CF1D40` | PTexture2DD3D11 |
| 006123D0 | `006123D9` `lea` | `02CF1C40` | PShaderComputeProgramD3D11 |
| 00612660 | `00612669` `lea` | `02CF2040` | PRenderTargetD3D11 |
| 006126E0 | `006126E9` `lea` | `02CF2240` | PStructuredBufferD3D11 |
| 006129C0 | `006129C9` `lea` | `02CF1640` | PStreamInputDescD3D11 |
| 00612C80 | `00612C89` `lea` | `02CF1F40` | PTextureCubeMapD3D11 |
| 00612EE0 | `00612EE9` `lea` | `02CF1740` | PStreamInputLayoutD3D11 |
| 006130F0 | `006130F9` `lea` | `02CF2340` | PIndirectArgsBufferD3D11 |
| 00613490 | `00613499` `lea` | `02CF1840` | PShaderProgramD3D11 |
| 00613510 | `00613519` `lea` | `02CF2140` | PSamplerStateD3D11 |
| 0063E8B0 | `0063E8BC` `lea` | `02D34E40` | PMotionBlurBase |
| 0063E940 | `0063E94C` `lea` | `02D367A0` | PAtmosphericsBase |
| 0063ED90 | `0063ED9C` `lea` | `02D34C40` | PDepthOfField |
| 0063F0E0 | `0063F0EC` `lea` | `02D369A0` | PAtmosphericsD3D11 |
| 0063F220 | `0063F22C` `lea` | `02D364A0` | PScreenSpaceReflectionBase |
| 0063F370 | `0063F37C` `lea` | `02D35040` | PMotionBlurD3D11 |
| 0063F540 | `0063F54C` `lea` | `02D356A0` | PMLAABase |
| 0063F870 | `0063F87C` `lea` | `02D34840` | PDeferredLightingBase |
| 0063FB60 | `0063FB6C` `lea` | `02D35AA0` | PGlowBase |
| 0063FD10 | `0063FD1C` `lea` | `02D366A0` | PScreenSpaceReflectionD3D11 |
| 00640160 | `0064016C` `lea` | `02D368A0` | PAtmospherics |
| 00640180 | `0064018C` `lea` | `02D358A0` | PMLAAD3D11 |
| 00640380 | `0064038C` `lea` | `02D34F40` | PMotionBlur |
| 00640770 | `0064077C` `lea` | `02D35BA0` | PGlowGPUBase |
| 00640AD0 | `00640ADC` `lea` | `02D365A0` | PScreenSpaceReflection |
| 00640CC0 | `00640CCC` `lea` | `02D36AA0` | PLowResParticles |
| 00640DC0 | `00640DCC` `lea` | `02D357A0` | PMLAA |
| 00641020 | `0064102C` `lea` | `02D35300` | PScreenSpaceAmbientOcclusionBase |
| 00641450 | `0064145C` `lea` | `02D34A40` | PDeferredLightingD3D11 |
| 006414D0 | `006414DC` `lea` | `02D35DA0` | PGlowD3D11 |
| 006419D0 | `006419DC` `lea` | `02D36BA0` | PMaterialPostEffect |
| 006419F0 | `006419FC` `lea` | `02D361A0` | PCelShadingBase |
| 00641C00 | `00641C0C` `lea` | `02D35500` | PScreenSpaceAmbientOcclusionD3D11 |
| 00642070 | `0064207C` `lea` | `02D35CA0` | PGlow |
| 00642270 | `0064227C` `lea` | `02D34940` | PDeferredLighting |
| 00642360 | `0064236C` `lea` | `02D363A0` | PCelShadingD3D11 |
| 00642610 | `0064261C` `lea` | `02D35400` | PScreenSpaceAmbientOcclusion |
| 00642B10 | `00642B1C` `lea` | `02D35EA0` | PFXAABase |
| 00642D50 | `00642D5C` `lea` | `02D34B40` | PDepthOfFieldBase |
| 00642D70 | `00642D79` `lea` | `02D36CA0` | PPostEffectManager |
| 00642D90 | `00642D9C` `lea` | `02D362A0` | PCelShading |
| 00643430 | `0064343C` `lea` | `02D359A0` | PMeshParticleSystemBase |
| 00643470 | `0064347C` `lea` | `02D360A0` | PFXAAD3D11 |
| 00643760 | `0064376C` `lea` | `02D34740` | PPostEffectBase |
| 00643A80 | `00643A8C` `lea` | `02D34D40` | PDepthOfFieldD3D11 |
| 00643D30 | `00643D3C` `lea` | `02D35FA0` | PFXAA |
| 0065E740 | `0065E749` `lea` | `02D39F40` | PDynamicDataBlock |
| 0065E9B0 | `0065E9B9` `lea` | `02D3A840` | PMeshSegmentBase |
| 0065EC00 | `0065EC09` `lea` | `02D3A240` | PIndexDataBlockBase |
| 0065EE70 | `0065EE79` `lea` | `02D3A640` | PMesh |
| 0065F1E0 | `0065F1E9` `lea` | `02D39840` | PMeshSegmentD3D11 |
| 0065F200 | `0065F209` `lea` | `02D39940` | PIndexDataBlockBufferD3D11 |
| 0065F5C0 | `0065F5C9` `lea` | `02D39B40` | PDataBlockBufferD3D11 |
| 0065F8A0 | `0065F8A9` `lea` | `02D3ADE0` | PVertexStream |
| 0065FAA0 | `0065FAA9` `lea` | `02D3A940` | PMeshSegment |
| 0065FEA0 | `0065FEAC` `lea` | `02D3A140` | PDynamicMesh |
| 0065FEC0 | `0065FEC9` `lea` | `02D39A40` | PIndexDataBlockD3D11 |
| 006602E0 | `006602E9` `lea` | `02D39C40` | PDataBlockD3D11 |
| 006604E0 | `006604E9` `lea` | `02D3A040` | PDynamicSegmentDesc |
| 00660640 | `00660649` `lea` | `02D3A440` | PMaterialSet |
| 00660910 | `00660919` `lea` | `02D39D40` | PDataBlockBase |
| 00660BF0 | `00660BF9` `lea` | `02D3A540` | PSkeletonJointBounds |
| 00660DF0 | `00660DF9` `lea` | `02D3A340` | PIndexDataBlock |
| 00661090 | `00661099` `lea` | `02D3ACE0` | PShape |
| 00661250 | `00661259` `lea` | `02D39E40` | PDataBlock |
| 00661570 | `00661579` `lea` | `02D3A740` | PSkinBoneRemap |
| 00674B60 | `00674B69` `lea` | `02D3E680` | PAssetReference |
| 006780A0 | `006780A9` `lea` | `02D3F210` | PCamera |
| 006782F0 | `006782FC` `lea` | `02D3F310` | PCameraProjection |
| 0067C5E0 | `0067C5E9` `lea` | `02E3F960` | PBitmapFontCharInfo |
| 0067C840 | `0067C849` `lea` | `02E3FA60` | PBitmapFont |
| 0067E450 | `0067E459` `lea` | `02E404B0` | PWorldMatrix |
| 006883B0 | `006883B9` `lea` | `02E49FD0` | PPhysicsCharacterControllerBullet |
| 00688470 | `00688479` `lea` | `02E494D0` | PPhysicsWorld |
| 006884B0 | `006884B9` `lea` | `02E489D0` | PPhysicsRigidBodyBase |
| 00688A50 | `00688A5C` `lea` | `02E495D0` | PPhysicsShapeBullet |
| 00688BC0 | `00688BCC` `lea` | `02E499D0` | PPhysicsMeshBullet |
| 00688C60 | `00688C6C` `lea` | `02E490D0` | PPhysicsTaperedCapsule |
| 006893A0 | `006893A9` `lea` | `02E47ED0` | PPhysicsCharacterController |
| 00689560 | `0068956C` `lea` | `02E481D0` | PPhysicsInterfaceBase |
| 00689970 | `0068997C` `lea` | `02E48DD0` | PPhysicsShape |
| 00689990 | `0068999C` `lea` | `02E485D0` | PPhysicsMesh |
| 00689A10 | `00689A1C` `lea` | `02E487D0` | PPhysicsPlaneBase |
| 0068A3C0 | `0068A3C9` `lea` | `02E493D0` | PRaycastResult |
| 0068A3E0 | `0068A3E9` `lea` | `02E49CD0` | PPhysicsRigidBodyBullet |
| 0068AB80 | `0068AB8C` `lea` | `02E48ED0` | PPhysicsSphereBase |
| 0068ABA0 | `0068ABAC` `lea` | `02E47FD0` | PPhysicsCylinderBase |
| 0068ABC0 | `0068ABCC` `lea` | `02E49ED0` | PPhysicsInterfaceBullet |
| 0068ABE0 | `0068ABEC` `lea` | `02E49AD0` | PPhysicsPlaneBullet |
| 0068B7C0 | `0068B7C9` `lea` | `02E492D0` | PPhysicsWorldBase |
| 0068B8A0 | `0068B8A9` `lea` | `02E48BD0` | PPhysicsRigidBody |
| 0068BD10 | `0068BD1C` `lea` | `02E49BD0` | PPhysicsSphereBullet |
| 0068BD30 | `0068BD3C` `lea` | `02E482D0` | PPhysicsInterface |
| 0068BDB0 | `0068BDBC` `lea` | `02E498D0` | PPhysicsCylinderBullet |
| 0068BDD0 | `0068BDDC` `lea` | `02E488D0` | PPhysicsPlane |
| 0068C810 | `0068C81C` `lea` | `02E48FD0` | PPhysicsSphere |
| 0068C830 | `0068C839` `lea` | `02E486D0` | PPhysicsModel |
| 0068C850 | `0068C85C` `lea` | `02E480D0` | PPhysicsCylinder |
| 0068D000 | `0068D00C` `lea` | `02E478D0` | PPhysicsBoxBase |
| 0068D020 | `0068D02C` `lea` | `02E47AD0` | PPhysicsCapsuleBase |
| 0068D610 | `0068D619` `lea` | `02E48AD0` | PPhysicsCallbackData |
| 0068D750 | `0068D75C` `lea` | `02E47CD0` | PPhysicsCharacterCamera |
| 0068DB40 | `0068DB4C` `lea` | `02E496D0` | PPhysicsBoxBullet |
| 0068DB60 | `0068DB6C` `lea` | `02E497D0` | PPhysicsCapsuleBullet |
| 0068E2C0 | `0068E2C9` `lea` | `02E483D0` | PPhysicsMaterial |
| 0068E2E0 | `0068E2E9` `lea` | `02E49DD0` | PPhysicsWorldBullet |
| 0068E550 | `0068E55C` `lea` | `02E479D0` | PPhysicsBox |
| 0068E570 | `0068E57C` `lea` | `02E47BD0` | PPhysicsCapsule |
| 0068EBA0 | `0068EBA9` `lea` | `02E47DD0` | PPhysicsCharacterControllerBase |
| 0068F090 | `0068F09C` `lea` | `02E484D0` | PPhysicsMeshBase |
| 0068F0B0 | `0068F0BC` `lea` | `02E491D0` | PPhysicsTaperedCylinder |
| 0068F0D0 | `0068F0DC` `lea` | `02E48CD0` | PPhysicsShapeBase |
| 006A7010 | `006A7019` `lea` | `02E4D630` | PString |
| 006A7A90 | `006A7A99` `lea` | `02E4D940` | PTrigger |
| 006AB420 | `006AB429` `lea` | `02E4EAF0` | PEntity |
| 006ACE60 | `006ACE6C` `lea` | `02E4F290` | PCameraOrthographic |
| 006AD6D0 | `006AD6DC` `lea` | `02E4F710` | PCameraPerspective |
| 006B0310 | `006B0319` `lea` | `02E50160` | PRandomGenerator |
| 006B3CE0 | `006B3CEC` `lea` | `02E518D0` | PNode |
| 006B6A30 | `006B6A39` `lea` | `02E522F0` | PMeshSegmentContext |
| 006BB550 | `006BB559` `lea` | `02E57F60` | PModifierNetworkDynamicMeshSegment |
| 006BBAB0 | `006BBABC` `lea` | `02E58060` | PModifierNetworkDynamicMesh |
| 006BE910 | `006BE919` `lea` | `02E58DB0` | PLight |
| 006C07E0 | `006C07E9` `lea` | `02E59DC0` | PShadowCaster |
| 006C0A00 | `006C0A09` `lea` | `02E59CC0` | PShadowSplit |
| 006C28E0 | `006C28E9` `lea` | `02E5A4C0` | PModifierNetworkInstanceInput |
| 006C2B10 | `006C2B19` `lea` | `02E5A5C0` | PModifierNetworkInstancePacketInput |
| 006C2D30 | `006C2D39` `lea` | `02E5A6C0` | PModifierNetworkInstance |
| 006C49E0 | `006C49E9` `lea` | `02E5AD00` | PLODLevel |
| 006C4CE0 | `006C4CE9` `lea` | `02E5AE00` | PLODGroup |
| 006C8130 | `006C8139` `lea` | `02E5BBB0` | POccluderGeometryInstance |
| 006CD7B0 | `006CD7B9` `lea` | `02E5C370` | PTriggerReceiverTypeCallbackData |
| 006CE740 | `006CE749` `lea` | `02E5E230` | PModifierNetworkInfoPacket_ModifierInstance |
| 006CE9D0 | `006CE9D9` `lea` | `02E5E330` | PModifierNetworkInfoPacket_Buffer |
| 006CEBE0 | `006CEBE9` `lea` | `02E5DD30` | PRenderStreamInput |
| 006CEEA0 | `006CEEA9` `lea` | `02E5E430` | PModifierNetworkInfoPacket |
| 006CF020 | `006CF029` `lea` | `02E5DE30` | PRenderStream |
| 006CF220 | `006CF229` `lea` | `02E5DF30` | PModifierNetworkBuffer |
| 006CF470 | `006CF479` `lea` | `02E5E030` | PModifierAndInputs |
| 006CF6A0 | `006CF6A9` `lea` | `02E5E130` | PModifierNetworkInfoPacket_ModifierCode |
| 006CF960 | `006CF969` `lea` | `02E5E540` | PModifierNetwork |
| 006D7270 | `006D7279` `lea` | `02E9FDF0` | PMorphModifierWeightsUserDataObject |
| 006D9DB0 | `006D9DB9` `lea` | `02EA0850` | POccluderGeometryObject |
| 00791330 | `00791339` `lea` | `02EA9400` | PDebugUtils |
| 00791590 | `0079159C` `lea` | `02EA5660` | PApplication |
| 00791730 | `0079173C` `lea` | `02EA5380` | PApplicationViewport |
| 00791920 | `00791929` `lea` | `02EA5560` | PInputMapper |
| 00866ED0 | `00866EDC` `lea` | `02EB6AF0` | PInputSourceVisionTrackerY |
| 00866F00 | `00866F0C` `lea` | `02EB61F0` | PInputSourceMotionQuatZ |
| 00866F80 | `00866F8C` `lea` | `02EB58F0` | PInputSourceMouseDeltaY |
| 00867640 | `0086764C` `lea` | `02EB6BF0` | PInputSourceVisionTrackerZ |
| 00867680 | `0086768C` `lea` | `02EB62F0` | PInputSourceMotionQuatW |
| 00867700 | `0086770C` `lea` | `02EB59F0` | PInputSourceTouchRotate |
| 00867CC0 | `00867CCC` `lea` | `02EB63F0` | PInputSourceMotionAngularVelocityX |
| 00867CE0 | `00867CEC` `lea` | `02EB5AF0` | PInputSourceTouchPinch |
| 008682C0 | `008682CC` `lea` | `02EB6CF0` | PInputAction |
| 00868400 | `0086840C` `lea` | `02EB52F0` | PInputSource |
| 00868570 | `0086857C` `lea` | `02EB64F0` | PInputSourceMotionAngularVelocityY |
| 008685F0 | `008685FC` `lea` | `02EB5DF0` | PInputSourceTouchTwoFingerDragX |
| 00868AD0 | `00868ADC` `lea` | `02EB53F0` | PInputSourceKey |
| 00868D20 | `00868D2C` `lea` | `02EB65F0` | PInputSourceMotionAngularVelocityZ |
| 00868DA0 | `00868DAC` `lea` | `02EB5EF0` | PInputSourceTouchTwoFingerDragY |
| 00869210 | `00869219` `lea` | `02EB6DF0` | PInputMap |
| 008694F0 | `008694FC` `lea` | `02EB54F0` | PInputSourceJoypadButton |
| 00869650 | `0086965C` `lea` | `02EB66F0` | PInputSourceMotionLinearAccelerationX |
| 00869700 | `0086970C` `lea` | `02EB5BF0` | PInputSourceTouchDragX |
| 00869D00 | `00869D0C` `lea` | `02EB55F0` | PInputSourceJoypadAxis |
| 00869DA0 | `00869DAC` `lea` | `02EB67F0` | PInputSourceMotionLinearAccelerationY |
| 00869E80 | `00869E8C` `lea` | `02EB5CF0` | PInputSourceTouchDragY |
| 0086A510 | `0086A51C` `lea` | `02EB56F0` | PInputSourceMouseButton |
| 0086A530 | `0086A53C` `lea` | `02EB68F0` | PInputSourceMotionLinearAccelerationZ |
| 0086A5B0 | `0086A5BC` `lea` | `02EB5FF0` | PInputSourceMotionQuatX |
| 0086AC70 | `0086AC7C` `lea` | `02EB69F0` | PInputSourceVisionTrackerX |
| 0086AC90 | `0086AC9C` `lea` | `02EB57F0` | PInputSourceMouseDeltaX |
| 0086ACB0 | `0086ACBC` `lea` | `02EB60F0` | PInputSourceMotionQuatY |
| 00874640 | `00874649` `lea` | `02EB7CD0` | PVisionMoveTracker |
| 00874850 | `00874859` `lea` | `02EB7BD0` | PVisionMoveTrackerBase |
| 008749E0 | `008749E9` `lea` | `02EB7DD0` | PVisionMoveTrackerWin32 |
| 008752B0 | `008752B9` `lea` | `02EB8060` | PVisionTracker |
| 008754C0 | `008754C9` `lea` | `02EB7F60` | PVisionTrackerBase |
| 00875650 | `00875659` `lea` | `02EB8160` | PVisionTrackerWin32 |
| 008774E0 | `008774E9` `lea` | `02EB9270` | POctreeWorld |
| 00877710 | `00877719` `lea` | `02EB9170` | POctreeData |
| 00877960 | `00877969` `lea` | `02EB9070` | POctree |
| 00877BC0 | `00877BC9` `lea` | `02EB9370` | POctreeChildren |
| 00879900 | `00879909` `lea` | `02EB9E60` | PGameConfig |

## Per-member rows: the class descriptor each nullable object push adapters pushes (OPUS, 2026-10-03)

The family `script-VM nullable object push adapters` (frontmatter: 295 members; 287 get a row here) shares the forms in the census table above (all reach the push target `00684080`), not repeated per row. What differs from member to member is the class descriptor X its one `lea r8, [X]` hands to the push. Each row anchors that `lea` (the member's distinguishing instruction) and states X and the class X describes. The class is read from the certified image: the static initialiser that does `lea rcx, [X]` and calls a descriptor-constructor wrapper, and that wrapper's `lea r8, [name]` before its one call to `00632D80`; every such initialiser must agree. [`fam_rows.py`](../../_index/candidates/opus-ee-nullable-push-adapters-1003/fam_rows.py) re-derives every row and compares it with the committed [`rows.tsv`](../../_index/candidates/opus-ee-nullable-push-adapters-1003/rows.tsv). A member without exactly one `lea r8`, a descriptor not named by exactly one class, or a value that differs fails it. Two controls are refused: a swapped value and a moved anchor. Members that do not derive are listed in [`excluded.tsv`](../../_index/candidates/opus-ee-nullable-push-adapters-1003/excluded.tsv).

### All 287 adapters (OPUS)

| member | distinguishing instruction | class descriptor X | class X describes |
|---|---|---|---|
| 005A2BA0 | `005A2BB8` `lea` | `02CAF0E0` | PTimeScaleOffsetController |
| 005A2F20 | `005A2F34` `lea` | `02CADC50` | PAnimationConstantChannel |
| 005A3360 | `005A3374` `lea` | `02CAE450` | PAnimationNetworkInstanceTarget |
| 005A34B0 | `005A34C4` `lea` | `02CAE660` | PAnimationSet |
| 005A3810 | `005A3828` `lea` | `02CAD340` | PAnimationBlenderController |
| 005A3910 | `005A3924` `lea` | `02CAE760` | PAnimationSlotListIndex |
| 005A3AC0 | `005A3AD4` `lea` | `02CADB40` | PAnimationClipBinding |
| 005A3B20 | `005A3B34` `lea` | `02CAE050` | PAnimationEvent |
| 005A3FD0 | `005A3FE8` `lea` | `02CAEDE0` | PAnimationWeightedBlenderController |
| 005A4130 | `005A4144` `lea` | `02CAE860` | PAnimationSlotArray |
| 005A41E0 | `005A41F4` `lea` | `02CAD940` | PAnimationClipBindingChannelMap |
| 005A46D0 | `005A46E8` `lea` | `02CADE50` | PAnimationDataSource |
| 005A47D0 | `005A47E4` `lea` | `02CADA40` | PAnimationClipBindingDataBlockCache |
| 005A4990 | `005A49A4` `lea` | `02CAE150` | PAnimationEventList |
| 005A4AD0 | `005A4AE8` `lea` | `02CAD240` | PAnimationAdditiveBlenderController |
| 005A4B90 | `005A4BA4` `lea` | `02CAD740` | PAnimationChannelTimes |
| 005A5210 | `005A5228` `lea` | `02CADF50` | PAnimationEventController |
| 005A5350 | `005A5368` `lea` | `02CAE550` | PAnimationNetworkInstance |
| 005A55F0 | `005A5608` `lea` | `02CAE250` | PAnimationHierarchyNode |
| 005A5650 | `005A5668` `lea` | `02CAEBE0` | PAnimationSpuTargetBlenderController |
| 005A5A80 | `005A5A94` `lea` | `02CAD640` | PAnimationChannelTarget |
| 005CDBC0 | `005CDBD4` `lea` | `02CB6F80` | PMeshInstanceAttachPoint |
| 005CDF40 | `005CDF54` `lea` | `02CB6380` | PConstantBufferBase |
| 005CDFD0 | `005CDFE8` `lea` | `02CB7180` | PModifierNetworkDynamicMeshInstance |
| 005CE0E0 | `005CE0F4` `lea` | `02CB9600` | PShaderPassParameterLocationTypesBase |
| 005CE350 | `005CE364` `lea` | `02CB78A0` | PSamplerState |
| 005CE500 | `005CE514` `lea` | `02CBAB00` | PShaderSource |
| 005CE560 | `005CE574` `lea` | `02CB7BA0` | PContextVariantFoldingTable |
| 005CE990 | `005CE9A4` `lea` | `02CBB800` | PTexture2DBase |
| 005CEC40 | `005CEC54` `lea` | `02CBAA00` | PShaderParameterCaptureBufferRWTexture3D |
| 005CEE00 | `005CEE14` `lea` | `02CB6D80` | PMeshInstanceSegmentContext |
| 005CF320 | `005CF334` `lea` | `02CB9500` | PShaderParameterDefinition |
| 005CF370 | `005CF384` `lea` | `02CB6780` | PEffectVariant |
| 005CF820 | `005CF834` `lea` | `02CBBB00` | PTexture3D |
| 005CFA00 | `005CFA14` `lea` | `02CBB500` | PStructuredBufferBase |
| 005CFC60 | `005CFC74` `lea` | `02CB75A0` | PRenderTargetBase |
| 005CFD80 | `005CFD94` `lea` | `02CBA200` | PShaderParameterCaptureBufferSampler |
| 005CFF50 | `005CFF64` `lea` | `02CB7380` | PParameterBufferBase |
| 005D02A0 | `005D02B4` `lea` | `02CB9700` | PShaderPassParameterLocationTypes |
| 005D05C0 | `005D05D4` `lea` | `02CBAE00` | PShaderStreamDefinition |
| 005D0950 | `005D0964` `lea` | `02CB7280` | PNodeContext |
| 005D0990 | `005D09A4` `lea` | `02CBA300` | PShaderParameterCaptureBufferStructuredBuffer |
| 005D0EC0 | `005D0ED4` `lea` | `02CBBC00` | PTextureCubeMapBase |
| 005D0F60 | `005D0F74` `lea` | `02CB7480` | PParameterBuffer |
| 005D0FA0 | `005D0FB4` `lea` | `02CB9A00` | PShaderPass |
| 005D10A0 | `005D10B4` `lea` | `02CBAC00` | PShaderProgramParamsAndStreams |
| 005D12F0 | `005D1304` `lea` | `02CB9C00` | PShaderParameterCaptureBufferStream |
| 005D13C0 | `005D13D4` `lea` | `02CB7080` | PMeshInstanceBounds |
| 005D1790 | `005D17A4` `lea` | `02CB6480` | PConstantBuffer |
| 005D19D0 | `005D19E4` `lea` | `02CBA400` | PShaderParameterCaptureBufferRWStructuredBuffer |
| 005D1E40 | `005D1E54` `lea` | `02CB9800` | PShaderPassParameterLocationTypesConstantBuffer |
| 005D21A0 | `005D21B4` `lea` | `02CB79A0` | PSceneRenderPass |
| 005D2430 | `005D2444` `lea` | `02CBAD00` | PShaderProgramBase |
| 005D25F0 | `005D2604` `lea` | `02CB6A80` | PMaterialSwitch |
| 005D2690 | `005D26A4` `lea` | `02CB9D00` | PShaderParameterCaptureBufferTextureBase |
| 005D2A70 | `005D2A84` `lea` | `02CBA500` | PShaderParameterCaptureBufferByteAddressBuffer |
| 005D2D40 | `005D2D54` `lea` | `02CB9B00` | PShaderPassStateBase |
| 005D2ED0 | `005D2EE4` `lea` | `02CBAF00` | PShaderVertexProgram |
| 005D31B0 | `005D31C4` `lea` | `02CB76A0` | PRenderTarget |
| 005D31F0 | `005D3204` `lea` | `02CBB900` | PTexture2D |
| 005D34D0 | `005D34E4` `lea` | `02CB9000` | PShader |
| 005D3970 | `005D3984` `lea` | `02CBB600` | PStructuredBuffer |
| 005D3A50 | `005D3A64` `lea` | `02CB9100` | PShaderParameterCaptureBufferLocation |
| 005D3AF0 | `005D3B04` `lea` | `02CBA600` | PShaderParameterCaptureBufferRWByteAddressBuffer |
| 005D3D70 | `005D3D84` `lea` | `02CBB300` | PShadowRenderer |
| 005D40C0 | `005D40D4` `lea` | `02CBB000` | PShaderFragmentProgram |
| 005D4440 | `005D4454` `lea` | `02CB6B80` | PMaterial |
| 005D47C0 | `005D47D4` `lea` | `02CB9F00` | PShaderParameterCaptureBufferTexture2D |
| 005D48C0 | `005D48D4` `lea` | `02CB6E80` | PMeshInstance |
| 005D4900 | `005D4914` `lea` | `02CB6680` | PEffect |
| 005D4C90 | `005D4CA4` `lea` | `02CB9E00` | PShaderParameterCaptureConstantBuffer |
| 005D4CD0 | `005D4CE4` `lea` | `02CB9200` | PShaderParameterCaptureBufferLocationSize |
| 005D4D10 | `005D4D24` `lea` | `02CB6880` | PIndirectArgsBufferBase |
| 005D5330 | `005D5344` `lea` | `02CBBA00` | PTexture3DBase |
| 005D5370 | `005D5384` `lea` | `02CBB400` | PForwardShadowRenderer |
| 005D53B0 | `005D53C4` `lea` | `02CB9900` | PShaderPassBase |
| 005D5630 | `005D5644` `lea` | `02CB77A0` | PSamplerStateBase |
| 005D5670 | `005D5684` `lea` | `02CBB100` | PShaderGeometryProgram |
| 005D5F40 | `005D5F54` `lea` | `02CBA000` | PShaderParameterCaptureBufferTexture3D |
| 005D6280 | `005D6294` `lea` | `02CBBD00` | PTextureCubeMap |
| 005D64B0 | `005D64C4` `lea` | `02CBA700` | PShaderParameterCaptureBufferDataBlock |
| 005D64F0 | `005D6504` `lea` | `02CB9300` | PShaderParameterCaptureBufferLocationType |
| 005D6760 | `005D6778` `lea` | `02CB6580` | PDynamicMeshInstance |
| 005D6A50 | `005D6A64` `lea` | `02CBB200` | PShaderComputeProgram |
| 005D6E50 | `005D6E64` `lea` | `02CB7CA0` | PSceneWideParameterBuffer |
| 005D6F00 | `005D6F14` `lea` | `02CBA100` | PShaderParameterCaptureBufferTextureCubeMap |
| 005D7160 | `005D7174` `lea` | `02CB6C80` | PMeshInstanceSegmentStreamBinding |
| 005D72C0 | `005D72D4` `lea` | `02CBB700` | PTextureCommonBase |
| 005D74F0 | `005D7504` `lea` | `02CBA800` | PShaderParameterCaptureBufferIndexDataBlock |
| 005D7540 | `005D7554` `lea` | `02CB9400` | PShaderParameterCaptureBufferLocationTypeConstantBuffer |
| 005D7950 | `005D7964` `lea` | `02CB6980` | PIndirectArgsBuffer |
| 005D7B90 | `005D7BA4` `lea` | `02CB7AA0` | PShaderPassInfo |
| 005D8170 | `005D8184` `lea` | `02CBA900` | PShaderParameterCaptureBufferRWTexture2D |
| 00610F80 | `00610F94` `lea` | `02CF1E40` | PTexture3DD3D11 |
| 00611010 | `00611024` `lea` | `02CF1540` | PShaderPassStateD3D11 |
| 006111E0 | `006111F4` `lea` | `02CF1940` | PShaderVertexProgramD3D11 |
| 006116E0 | `006116F4` `lea` | `02CF1A40` | PShaderFragmentProgramD3D11 |
| 006117F0 | `00611804` `lea` | `02CF1440` | PShaderPassD3D11 |
| 00611B90 | `00611BA4` `lea` | `02CF2440` | PConstantBufferD3D11 |
| 00611CC0 | `00611CD4` `lea` | `02CF1B40` | PShaderGeometryProgramD3D11 |
| 00612040 | `00612054` `lea` | `02CF1D40` | PTexture2DD3D11 |
| 006120F0 | `00612104` `lea` | `02CF1C40` | PShaderComputeProgramD3D11 |
| 00612290 | `006122A4` `lea` | `02CF2040` | PRenderTargetD3D11 |
| 00612450 | `00612464` `lea` | `02CF2240` | PStructuredBufferD3D11 |
| 00612910 | `00612924` `lea` | `02CF1640` | PStreamInputDescD3D11 |
| 00612BE0 | `00612BF4` `lea` | `02CF1F40` | PTextureCubeMapD3D11 |
| 00612E30 | `00612E44` `lea` | `02CF1740` | PStreamInputLayoutD3D11 |
| 00612FD0 | `00612FE4` `lea` | `02CF2340` | PIndirectArgsBufferD3D11 |
| 006132A0 | `006132B4` `lea` | `02CF1840` | PShaderProgramD3D11 |
| 00613380 | `00613394` `lea` | `02CF2140` | PSamplerStateD3D11 |
| 0063EBD0 | `0063EBE8` `lea` | `02D34C40` | PDepthOfField |
| 0063ED00 | `0063ED18` `lea` | `02D369A0` | PAtmosphericsD3D11 |
| 0063EDD0 | `0063EDE8` `lea` | `02D364A0` | PScreenSpaceReflectionBase |
| 0063EFB0 | `0063EFC8` `lea` | `02D35040` | PMotionBlurD3D11 |
| 0063F100 | `0063F118` `lea` | `02D356A0` | PMLAABase |
| 0063F5D0 | `0063F5E8` `lea` | `02D34840` | PDeferredLightingBase |
| 0063F900 | `0063F918` `lea` | `02D35AA0` | PGlowBase |
| 0063FAC0 | `0063FAD8` `lea` | `02D366A0` | PScreenSpaceReflectionD3D11 |
| 0063FD50 | `0063FD68` `lea` | `02D368A0` | PAtmospherics |
| 0063FE60 | `0063FE78` `lea` | `02D358A0` | PMLAAD3D11 |
| 006400C0 | `006400D8` `lea` | `02D34F40` | PMotionBlur |
| 00640600 | `00640618` `lea` | `02D35BA0` | PGlowGPUBase |
| 00640730 | `00640748` `lea` | `02D365A0` | PScreenSpaceReflection |
| 00640800 | `00640818` `lea` | `02D36AA0` | PLowResParticles |
| 00640A10 | `00640A28` `lea` | `02D357A0` | PMLAA |
| 00640C20 | `00640C38` `lea` | `02D35300` | PScreenSpaceAmbientOcclusionBase |
| 006410D0 | `006410E8` `lea` | `02D34A40` | PDeferredLightingD3D11 |
| 00641240 | `00641258` `lea` | `02D35DA0` | PGlowD3D11 |
| 00641750 | `00641768` `lea` | `02D36BA0` | PMaterialPostEffect |
| 006417F0 | `00641808` `lea` | `02D361A0` | PCelShadingBase |
| 00641990 | `006419A8` `lea` | `02D35500` | PScreenSpaceAmbientOcclusionD3D11 |
| 00641E80 | `00641E98` `lea` | `02D35CA0` | PGlow |
| 00641FB0 | `00641FC8` `lea` | `02D34940` | PDeferredLighting |
| 00642090 | `006420A8` `lea` | `02D363A0` | PCelShadingD3D11 |
| 00642380 | `00642398` `lea` | `02D35400` | PScreenSpaceAmbientOcclusion |
| 00642840 | `00642858` `lea` | `02D35EA0` | PFXAABase |
| 006429C0 | `006429D8` `lea` | `02D34B40` | PDepthOfFieldBase |
| 00642A70 | `00642A84` `lea` | `02D36CA0` | PPostEffectManager |
| 00642AD0 | `00642AE8` `lea` | `02D362A0` | PCelShading |
| 00643240 | `00643258` `lea` | `02D359A0` | PMeshParticleSystemBase |
| 006432A0 | `006432B8` `lea` | `02D360A0` | PFXAAD3D11 |
| 00643490 | `006434A8` `lea` | `02D34740` | PPostEffectBase |
| 00643910 | `00643928` `lea` | `02D34D40` | PDepthOfFieldD3D11 |
| 00643A40 | `00643A58` `lea` | `02D35FA0` | PFXAA |
| 00643BD0 | `00643BE8` `lea` | `02D34E40` | PMotionBlurBase |
| 00643CF0 | `00643D08` `lea` | `02D367A0` | PAtmosphericsBase |
| 0065E900 | `0065E914` `lea` | `02D3A840` | PMeshSegmentBase |
| 0065EB50 | `0065EB64` `lea` | `02D3A240` | PIndexDataBlockBase |
| 0065EDC0 | `0065EDD4` `lea` | `02D3A640` | PMesh |
| 0065F090 | `0065F0A4` `lea` | `02D39840` | PMeshSegmentD3D11 |
| 0065F0D0 | `0065F0E4` `lea` | `02D39940` | PIndexDataBlockBufferD3D11 |
| 0065F440 | `0065F454` `lea` | `02D39B40` | PDataBlockBufferD3D11 |
| 0065F6C0 | `0065F6D4` `lea` | `02D3ADE0` | PVertexStream |
| 0065F8C0 | `0065F8D4` `lea` | `02D3A940` | PMeshSegment |
| 0065FD40 | `0065FD58` `lea` | `02D3A140` | PDynamicMesh |
| 0065FD80 | `0065FD94` `lea` | `02D39A40` | PIndexDataBlockD3D11 |
| 006600A0 | `006600B4` `lea` | `02D39C40` | PDataBlockD3D11 |
| 006601F0 | `00660204` `lea` | `02D3A040` | PDynamicSegmentDesc |
| 00660300 | `00660314` `lea` | `02D3A440` | PMaterialSet |
| 00660860 | `00660874` `lea` | `02D39D40` | PDataBlockBase |
| 006609E0 | `006609F4` `lea` | `02D3A540` | PSkeletonJointBounds |
| 00660BB0 | `00660BC4` `lea` | `02D3A340` | PIndexDataBlock |
| 00660DB0 | `00660DC4` `lea` | `02D3ACE0` | PShape |
| 00661050 | `00661064` `lea` | `02D39E40` | PDataBlock |
| 006614C0 | `006614D4` `lea` | `02D3A740` | PSkinBoneRemap |
| 006616E0 | `006616F4` `lea` | `02D39F40` | PDynamicDataBlock |
| 00674AA0 | `00674AB4` `lea` | `02D3E680` | PAssetReference |
| 00677FF0 | `00678004` `lea` | `02D3F210` | PCamera |
| 00678240 | `00678258` `lea` | `02D3F310` | PCameraProjection |
| 0067C790 | `0067C7A4` `lea` | `02E3FA60` | PBitmapFont |
| 0067C9C0 | `0067C9D4` `lea` | `02E3F960` | PBitmapFontCharInfo |
| 0067E3A0 | `0067E3B4` `lea` | `02E404B0` | PWorldMatrix |
| 00688090 | `006880A4` `lea` | `02E49FD0` | PPhysicsCharacterControllerBullet |
| 006881A0 | `006881B4` `lea` | `02E494D0` | PPhysicsWorld |
| 00688200 | `00688214` `lea` | `02E489D0` | PPhysicsRigidBodyBase |
| 006884D0 | `006884E8` `lea` | `02E495D0` | PPhysicsShapeBullet |
| 006887D0 | `006887E8` `lea` | `02E499D0` | PPhysicsMeshBullet |
| 006888A0 | `006888B8` `lea` | `02E490D0` | PPhysicsTaperedCapsule |
| 006891D0 | `006891E4` `lea` | `02E47ED0` | PPhysicsCharacterController |
| 00689280 | `00689297` `lea` | `02E481D0` | PPhysicsInterfaceBase |
| 006894C0 | `006894D8` `lea` | `02E48DD0` | PPhysicsShape |
| 00689580 | `00689598` `lea` | `02E485D0` | PPhysicsMesh |
| 006896B0 | `006896C8` `lea` | `02E487D0` | PPhysicsPlaneBase |
| 0068A090 | `0068A0A4` `lea` | `02E493D0` | PRaycastResult |
| 0068A120 | `0068A134` `lea` | `02E49CD0` | PPhysicsRigidBodyBullet |
| 0068A5F0 | `0068A608` `lea` | `02E48ED0` | PPhysicsSphereBase |
| 0068A7D0 | `0068A7E8` `lea` | `02E47FD0` | PPhysicsCylinderBase |
| 0068A810 | `0068A827` `lea` | `02E49ED0` | PPhysicsInterfaceBullet |
| 0068A8A0 | `0068A8B8` `lea` | `02E49AD0` | PPhysicsPlaneBullet |
| 0068B310 | `0068B324` `lea` | `02E492D0` | PPhysicsWorldBase |
| 0068B3C0 | `0068B3D4` `lea` | `02E48BD0` | PPhysicsRigidBody |
| 0068B6F0 | `0068B708` `lea` | `02E49BD0` | PPhysicsSphereBullet |
| 0068B730 | `0068B747` `lea` | `02E482D0` | PPhysicsInterface |
| 0068B820 | `0068B838` `lea` | `02E498D0` | PPhysicsCylinderBullet |
| 0068B860 | `0068B878` `lea` | `02E488D0` | PPhysicsPlane |
| 0068C5A0 | `0068C5B8` `lea` | `02E48FD0` | PPhysicsSphere |
| 0068C620 | `0068C634` `lea` | `02E486D0` | PPhysicsModel |
| 0068C660 | `0068C678` `lea` | `02E480D0` | PPhysicsCylinder |
| 0068CEA0 | `0068CEB8` `lea` | `02E478D0` | PPhysicsBoxBase |
| 0068CEE0 | `0068CEF8` `lea` | `02E47AD0` | PPhysicsCapsuleBase |
| 0068D090 | `0068D0A4` `lea` | `02E48AD0` | PPhysicsCallbackData |
| 0068D500 | `0068D518` `lea` | `02E47CD0` | PPhysicsCharacterCamera |
| 0068D9C0 | `0068D9D8` `lea` | `02E496D0` | PPhysicsBoxBullet |
| 0068DA00 | `0068DA18` `lea` | `02E497D0` | PPhysicsCapsuleBullet |
| 0068DFF0 | `0068E004` `lea` | `02E483D0` | PPhysicsMaterial |
| 0068E030 | `0068E044` `lea` | `02E49DD0` | PPhysicsWorldBullet |
| 0068E240 | `0068E258` `lea` | `02E479D0` | PPhysicsBox |
| 0068E280 | `0068E298` `lea` | `02E47BD0` | PPhysicsCapsule |
| 0068E900 | `0068E914` `lea` | `02E47DD0` | PPhysicsCharacterControllerBase |
| 0068EDA0 | `0068EDB8` `lea` | `02E484D0` | PPhysicsMeshBase |
| 0068EEC0 | `0068EED8` `lea` | `02E491D0` | PPhysicsTaperedCylinder |
| 0068EF00 | `0068EF18` `lea` | `02E48CD0` | PPhysicsShapeBase |
| 006A6F60 | `006A6F74` `lea` | `02E4D630` | PString |
| 006A79E0 | `006A79F4` `lea` | `02E4D940` | PTrigger |
| 006A9C60 | `006A9C74` `lea` | `02E4E430` | PTypedObject |
| 006AB340 | `006AB354` `lea` | `02E4EAF0` | PEntity |
| 006ACDB0 | `006ACDC8` `lea` | `02E4F290` | PCameraOrthographic |
| 006AD620 | `006AD638` `lea` | `02E4F710` | PCameraPerspective |
| 006B0260 | `006B0274` `lea` | `02E50160` | PRandomGenerator |
| 006B3C30 | `006B3C48` `lea` | `02E518D0` | PNode |
| 006B6990 | `006B69A4` `lea` | `02E522F0` | PMeshSegmentContext |
| 006BB4A0 | `006BB4B4` `lea` | `02E57F60` | PModifierNetworkDynamicMeshSegment |
| 006BBA00 | `006BBA18` `lea` | `02E58060` | PModifierNetworkDynamicMesh |
| 006BE860 | `006BE874` `lea` | `02E58DB0` | PLight |
| 006C0730 | `006C0744` `lea` | `02E59DC0` | PShadowCaster |
| 006C0950 | `006C0964` `lea` | `02E59CC0` | PShadowSplit |
| 006C2830 | `006C2844` `lea` | `02E5A4C0` | PModifierNetworkInstanceInput |
| 006C2A60 | `006C2A74` `lea` | `02E5A5C0` | PModifierNetworkInstancePacketInput |
| 006C2C80 | `006C2C94` `lea` | `02E5A6C0` | PModifierNetworkInstance |
| 006C4920 | `006C4934` `lea` | `02E5AD00` | PLODLevel |
| 006C4C20 | `006C4C34` `lea` | `02E5AE00` | PLODGroup |
| 006C8080 | `006C8094` `lea` | `02E5BBB0` | POccluderGeometryInstance |
| 006CD700 | `006CD714` `lea` | `02E5C370` | PTriggerReceiverTypeCallbackData |
| 006CE920 | `006CE934` `lea` | `02E5E330` | PModifierNetworkInfoPacket_Buffer |
| 006CEB30 | `006CEB44` `lea` | `02E5DD30` | PRenderStreamInput |
| 006CEC50 | `006CEC64` `lea` | `02E5E430` | PModifierNetworkInfoPacket |
| 006CEF10 | `006CEF24` `lea` | `02E5DE30` | PRenderStream |
| 006CF170 | `006CF184` `lea` | `02E5DF30` | PModifierNetworkBuffer |
| 006CF3C0 | `006CF3D4` `lea` | `02E5E030` | PModifierAndInputs |
| 006CF5F0 | `006CF604` `lea` | `02E5E130` | PModifierNetworkInfoPacket_ModifierCode |
| 006CF820 | `006CF834` `lea` | `02E5E540` | PModifierNetwork |
| 006CF920 | `006CF934` `lea` | `02E5E230` | PModifierNetworkInfoPacket_ModifierInstance |
| 006D71C0 | `006D71D4` `lea` | `02E9FDF0` | PMorphModifierWeightsUserDataObject |
| 006D9D00 | `006D9D14` `lea` | `02EA0850` | POccluderGeometryObject |
| 00791280 | `00791294` `lea` | `02EA9400` | PDebugUtils |
| 007914E0 | `007914F8` `lea` | `02EA5660` | PApplication |
| 00791680 | `00791698` `lea` | `02EA5380` | PApplicationViewport |
| 00791870 | `00791884` `lea` | `02EA5560` | PInputMapper |
| 00867380 | `00867398` `lea` | `02EB6BF0` | PInputSourceVisionTrackerZ |
| 00867430 | `00867448` `lea` | `02EB62F0` | PInputSourceMotionQuatW |
| 008674E0 | `008674F8` `lea` | `02EB59F0` | PInputSourceTouchRotate |
| 00867AF0 | `00867B08` `lea` | `02EB63F0` | PInputSourceMotionAngularVelocityX |
| 00867BA0 | `00867BB8` `lea` | `02EB5AF0` | PInputSourceTouchPinch |
| 00867FF0 | `00868008` `lea` | `02EB6CF0` | PInputAction |
| 008680A0 | `008680B8` `lea` | `02EB52F0` | PInputSource |
| 00868220 | `00868238` `lea` | `02EB64F0` | PInputSourceMotionAngularVelocityY |
| 00868300 | `00868318` `lea` | `02EB5DF0` | PInputSourceTouchTwoFingerDragX |
| 00868900 | `00868918` `lea` | `02EB53F0` | PInputSourceKey |
| 00868A20 | `00868A38` `lea` | `02EB65F0` | PInputSourceMotionAngularVelocityZ |
| 00868AF0 | `00868B08` `lea` | `02EB5EF0` | PInputSourceTouchTwoFingerDragY |
| 008690B0 | `008690C4` `lea` | `02EB6DF0` | PInputMap |
| 008691D0 | `008691E8` `lea` | `02EB54F0` | PInputSourceJoypadButton |
| 00869300 | `00869318` `lea` | `02EB66F0` | PInputSourceMotionLinearAccelerationX |
| 00869420 | `00869438` `lea` | `02EB5BF0` | PInputSourceTouchDragX |
| 00869A70 | `00869A88` `lea` | `02EB55F0` | PInputSourceJoypadAxis |
| 00869B20 | `00869B38` `lea` | `02EB67F0` | PInputSourceMotionLinearAccelerationY |
| 00869C30 | `00869C48` `lea` | `02EB5CF0` | PInputSourceTouchDragY |
| 0086A290 | `0086A2A8` `lea` | `02EB56F0` | PInputSourceMouseButton |
| 0086A2F0 | `0086A308` `lea` | `02EB68F0` | PInputSourceMotionLinearAccelerationZ |
| 0086A3A0 | `0086A3B8` `lea` | `02EB5FF0` | PInputSourceMotionQuatX |
| 0086A9F0 | `0086AA08` `lea` | `02EB69F0` | PInputSourceVisionTrackerX |
| 0086AAC0 | `0086AAD8` `lea` | `02EB57F0` | PInputSourceMouseDeltaX |
| 0086AB00 | `0086AB18` `lea` | `02EB60F0` | PInputSourceMotionQuatY |
| 0086B110 | `0086B128` `lea` | `02EB6AF0` | PInputSourceVisionTrackerY |
| 0086B1C0 | `0086B1D8` `lea` | `02EB61F0` | PInputSourceMotionQuatZ |
| 0086B270 | `0086B288` `lea` | `02EB58F0` | PInputSourceMouseDeltaY |
| 00874790 | `008747A4` `lea` | `02EB7BD0` | PVisionMoveTrackerBase |
| 00874920 | `00874934` `lea` | `02EB7DD0` | PVisionMoveTrackerWin32 |
| 00874AB0 | `00874AC4` `lea` | `02EB7CD0` | PVisionMoveTracker |
| 00875400 | `00875414` `lea` | `02EB7F60` | PVisionTrackerBase |
| 00875590 | `008755A4` `lea` | `02EB8160` | PVisionTrackerWin32 |
| 00875720 | `00875734` `lea` | `02EB8060` | PVisionTracker |
| 00877430 | `00877444` `lea` | `02EB9270` | POctreeWorld |
| 00877660 | `00877674` `lea` | `02EB9170` | POctreeData |
| 008778B0 | `008778C4` `lea` | `02EB9070` | POctree |
| 00877B10 | `00877B24` `lea` | `02EB9370` | POctreeChildren |
| 00879850 | `00879864` `lea` | `02EB9E60` | PGameConfig |

## Required class descriptor of each accessor (FABLE, 2026-10-03)

*FABLE, under SWE2-AUDIT-SPEC's ruling on template-family members and OPUS's adopted family sentence (record `opus-ee-rulings-1003`); page lead OPUS said yes (`FABLE-REQ-OPUS-ACCESSOR-DESCRIPTOR-ROWS-1003`); SWE2-AUDIT-SPEC reviewed the package. Checker: [`fable-accessor-descriptors-1003`](../../_index/candidates/fable-accessor-descriptors-1003/README.md) (`desc_check.py`, FAILS 0, with its self-test).*

**The shared shape, stated once.** A compare-form `PObjectAccessor<T>::Get` loads the descriptor its argument must derive from with one `lea rdx,[rip+X]`, then walks the object's base chain (`[descriptor + 0x78]`) comparing against X: `cmp rcx,rdx` in the reference form (`T &`), `cmp rax,rdx` in the pointer form (`T *`). A class that never matches reports a diagnostic line, with the class name read from `[descriptor + 0x30]`, and returns 0 (section 2). The diagnostic `__LINE__` immediates are the same in every member of a form (pointer form 106, 118; reference form 143, 141), so no row repeats them. **What differs between members is X**, and that is what each row states: the anchor is the member's `lea`, and the class name is the string X's own constructor stores at `[X + 0x30]`, read from the image. Most classes reach `00632D80` / `00632C90` through a per-class wrapper that loads the name into `r8`, and the static initialiser passes X in `rcx`. Nine core classes (PBase, PClassDescriptor, PCluster and six more) have their own constructors that store a literal name with `lea rax` / `mov [rbx+0x30],rax`. Every row was checked against the appendix type: 591 of 591 agree, 0 disagree, 0 unresolved. Which class each generated adapter belongs to, from the descriptor vtable, is the earlier section [The class each generated adapter belongs to](#the-class-each-generated-adapter-belongs-to-from-the-descriptor-vtable); its 315 `+0x28` accessors agree with this table on all 315.

**Coverage of the 747.** 591 members have a row. The other 156 stay entry-only: they have no compare `lea`, because the required descriptor comes back from a call (`call G ; mov r9,rax`). For 58 of them G's own descriptor is named in the image, and for the container types among them (`PArray<E>` / `PSharray<E>`) it is E's. SWE2-AUDIT-SPEC's ruling gives this shape no row; a row would need its own distinguishing instruction and value.

| Get body | T (appendix) | required descriptor X | interior anchor |
|---|---|---|---|
| `00599770` | `PSerialization::PBinary::PClusterHeader &` | requires class descriptor `02CAA0A0` (`PClusterHeader`); template member: distinguishing operand | Interior anchor `005997A9` (`lea`, entry + 0x39) |
| `00599870` | `PSerialization::PBinary::PClusterHeaderBase &` | requires class descriptor `02CA9FA0` (`PClusterHeaderBase`); template member: distinguishing operand | Interior anchor `005998A9` (`lea`, entry + 0x39) |
| `00599970` | `PSerialization::PBinary::PClusterHeaderD3D11 &` | requires class descriptor `02CA9DA0` (`PClusterHeaderD3D11`); template member: distinguishing operand | Interior anchor `005999A9` (`lea`, entry + 0x39) |
| `00599A70` | `PSerialization::PBinary::PInternal::PInstanceListHeader &` | requires class descriptor `02CA9EA0` (`PInstanceListHeader`); template member: distinguishing operand | Interior anchor `00599AA9` (`lea`, entry + 0x39) |
| `00599B70` | `PSerialization::PBinary::PClusterHeader *` | requires class descriptor `02CAA0A0` (`PClusterHeader`); template member: distinguishing operand | Interior anchor `00599BB2` (`lea`, entry + 0x42) |
| `00599CA0` | `PSerialization::PBinary::PClusterHeaderBase *` | requires class descriptor `02CA9FA0` (`PClusterHeaderBase`); template member: distinguishing operand | Interior anchor `00599CE2` (`lea`, entry + 0x42) |
| `00599DD0` | `PSerialization::PBinary::PClusterHeaderD3D11 *` | requires class descriptor `02CA9DA0` (`PClusterHeaderD3D11`); template member: distinguishing operand | Interior anchor `00599E12` (`lea`, entry + 0x42) |
| `00599F00` | `PSerialization::PBinary::PInternal::PInstanceListHeader *` | requires class descriptor `02CA9EA0` (`PInstanceListHeader`); template member: distinguishing operand | Interior anchor `00599F42` (`lea`, entry + 0x42) |
| `005B9290` | `PAnimation::PAnimatableComponent &` | requires class descriptor `02CAD140` (`PAnimatableComponent`); template member: distinguishing operand | Interior anchor `005B92DE` (`lea`, entry + 0x4E) |
| `005B93B0` | `PAnimation::PAnimationAdditiveBlenderController &` | requires class descriptor `02CAD240` (`PAnimationAdditiveBlenderController`); template member: distinguishing operand | Interior anchor `005B93FE` (`lea`, entry + 0x4E) |
| `005B94D0` | `PAnimation::PAnimationChannel &` | requires class descriptor `02CAD440` (`PAnimationChannel`); template member: distinguishing operand | Interior anchor `005B9509` (`lea`, entry + 0x39) |
| `005B95D0` | `PAnimation::PAnimationChannelBase &` | requires class descriptor `02CAD540` (`PAnimationChannelBase`); template member: distinguishing operand | Interior anchor `005B9609` (`lea`, entry + 0x39) |
| `005B96D0` | `PAnimation::PAnimationChannelTarget &` | requires class descriptor `02CAD640` (`PAnimationChannelTarget`); template member: distinguishing operand | Interior anchor `005B9709` (`lea`, entry + 0x39) |
| `005B97D0` | `PAnimation::PAnimationChannelTimes &` | requires class descriptor `02CAD740` (`PAnimationChannelTimes`); template member: distinguishing operand | Interior anchor `005B9809` (`lea`, entry + 0x39) |
| `005B98D0` | `PAnimation::PAnimationClip &` | requires class descriptor `02CAD840` (`PAnimationClip`); template member: distinguishing operand | Interior anchor `005B9909` (`lea`, entry + 0x39) |
| `005B99D0` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap &` | requires class descriptor `02CAD940` (`PAnimationClipBindingChannelMap`); template member: distinguishing operand | Interior anchor `005B9A09` (`lea`, entry + 0x39) |
| `005B9AD0` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache &` | requires class descriptor `02CADA40` (`PAnimationClipBindingDataBlockCache`); template member: distinguishing operand | Interior anchor `005B9B09` (`lea`, entry + 0x39) |
| `005B9BD0` | `PAnimation::PAnimationConstantChannel &` | requires class descriptor `02CADC50` (`PAnimationConstantChannel`); template member: distinguishing operand | Interior anchor `005B9C09` (`lea`, entry + 0x39) |
| `005B9CD0` | `PAnimation::PAnimationController &` | requires class descriptor `02CADD50` (`PAnimationController`); template member: distinguishing operand | Interior anchor `005B9D1E` (`lea`, entry + 0x4E) |
| `005B9DF0` | `PAnimation::PAnimationDataSourceListEntry &` | requires class descriptor `02CAE350` (`PAnimationDataSourceListEntry`); template member: distinguishing operand | Interior anchor `005B9E29` (`lea`, entry + 0x39) |
| `005B9EF0` | `PAnimation::PAnimationEvent &` | requires class descriptor `02CAE050` (`PAnimationEvent`); template member: distinguishing operand | Interior anchor `005B9F29` (`lea`, entry + 0x39) |
| `005B9FF0` | `PAnimation::PAnimationEventController &` | requires class descriptor `02CADF50` (`PAnimationEventController`); template member: distinguishing operand | Interior anchor `005BA03E` (`lea`, entry + 0x4E) |
| `005BA110` | `PAnimation::PAnimationEventList &` | requires class descriptor `02CAE150` (`PAnimationEventList`); template member: distinguishing operand | Interior anchor `005BA149` (`lea`, entry + 0x39) |
| `005BA210` | `PAnimation::PAnimationNetworkInstance &` | requires class descriptor `02CAE550` (`PAnimationNetworkInstance`); template member: distinguishing operand | Interior anchor `005BA25E` (`lea`, entry + 0x4E) |
| `005BA330` | `PAnimation::PAnimationNetworkInstanceTarget &` | requires class descriptor `02CAE450` (`PAnimationNetworkInstanceTarget`); template member: distinguishing operand | Interior anchor `005BA369` (`lea`, entry + 0x39) |
| `005BA430` | `PAnimation::PAnimationSet &` | requires class descriptor `02CAE660` (`PAnimationSet`); template member: distinguishing operand | Interior anchor `005BA469` (`lea`, entry + 0x39) |
| `005BA530` | `PAnimation::PAnimationSlotArray &` | requires class descriptor `02CAE860` (`PAnimationSlotArray`); template member: distinguishing operand | Interior anchor `005BA569` (`lea`, entry + 0x39) |
| `005BA630` | `PAnimation::PAnimationSlotFilter &` | requires class descriptor `02CAEA60` (`PAnimationSlotFilter`); template member: distinguishing operand | Interior anchor `005BA67E` (`lea`, entry + 0x4E) |
| `005BA750` | `PAnimation::PAnimationSlotFilterDeferredLoad &` | requires class descriptor `02CAE960` (`PAnimationSlotFilterDeferredLoad`); template member: distinguishing operand | Interior anchor `005BA789` (`lea`, entry + 0x39) |
| `005BA850` | `PAnimation::PAnimationSlotListIndex &` | requires class descriptor `02CAE760` (`PAnimationSlotListIndex`); template member: distinguishing operand | Interior anchor `005BA889` (`lea`, entry + 0x39) |
| `005BA950` | `PAnimation::PAnimationSpuTargetBlenderController &` | requires class descriptor `02CAEBE0` (`PAnimationSpuTargetBlenderController`); template member: distinguishing operand | Interior anchor `005BA99E` (`lea`, entry + 0x4E) |
| `005BAA70` | `PAnimation::PAnimationTargetBlenderController &` | requires class descriptor `02CAECE0` (`PAnimationTargetBlenderController`); template member: distinguishing operand | Interior anchor `005BAABE` (`lea`, entry + 0x4E) |
| `005BAB90` | `PAnimation::PAnimationWeightedBlenderController &` | requires class descriptor `02CAEDE0` (`PAnimationWeightedBlenderController`); template member: distinguishing operand | Interior anchor `005BABDE` (`lea`, entry + 0x4E) |
| `005BACB0` | `PAnimation::PBlendableAnimationSource &` | requires class descriptor `02CAD040` (`PBlendableAnimationSource`); template member: distinguishing operand | Interior anchor `005BACE9` (`lea`, entry + 0x39) |
| `005BADB0` | `PCluster &` | requires class descriptor `02CF8780` (`PCluster`); template member: distinguishing operand | Interior anchor `005BADE9` (`lea`, entry + 0x39) |
| `005BAEB0` | `PAnimation::PTimeController &` | requires class descriptor `02CAEEE0` (`PTimeController`); template member: distinguishing operand | Interior anchor `005BAEFE` (`lea`, entry + 0x4E) |
| `005BAFD0` | `PAnimation::PTimeIntervalController &` | requires class descriptor `02CAEFE0` (`PTimeIntervalController`); template member: distinguishing operand | Interior anchor `005BB01E` (`lea`, entry + 0x4E) |
| `005BB0F0` | `PAnimation::PTimeScaleOffsetController &` | requires class descriptor `02CAF0E0` (`PTimeScaleOffsetController`); template member: distinguishing operand | Interior anchor `005BB13E` (`lea`, entry + 0x4E) |
| `005BC4D0` | `PAnimation::PAnimatableComponent *` | requires class descriptor `02CAD140` (`PAnimatableComponent`); template member: distinguishing operand | Interior anchor `005BC516` (`lea`, entry + 0x46) |
| `005BC600` | `PAnimation::PAnimationAdditiveBlenderController *` | requires class descriptor `02CAD240` (`PAnimationAdditiveBlenderController`); template member: distinguishing operand | Interior anchor `005BC646` (`lea`, entry + 0x46) |
| `005BC730` | `PAnimation::PAnimationBlenderController *` | requires class descriptor `02CAD340` (`PAnimationBlenderController`); template member: distinguishing operand | Interior anchor `005BC776` (`lea`, entry + 0x46) |
| `005BC860` | `PAnimation::PAnimationChannel *` | requires class descriptor `02CAD440` (`PAnimationChannel`); template member: distinguishing operand | Interior anchor `005BC8A2` (`lea`, entry + 0x42) |
| `005BC990` | `PAnimation::PAnimationChannelBase *` | requires class descriptor `02CAD540` (`PAnimationChannelBase`); template member: distinguishing operand | Interior anchor `005BC9D2` (`lea`, entry + 0x42) |
| `005BCAC0` | `PAnimation::PAnimationChannelTarget *` | requires class descriptor `02CAD640` (`PAnimationChannelTarget`); template member: distinguishing operand | Interior anchor `005BCB02` (`lea`, entry + 0x42) |
| `005BCBF0` | `PAnimation::PAnimationChannelTimes *` | requires class descriptor `02CAD740` (`PAnimationChannelTimes`); template member: distinguishing operand | Interior anchor `005BCC32` (`lea`, entry + 0x42) |
| `005BCD20` | `PAnimation::PAnimationClip *` | requires class descriptor `02CAD840` (`PAnimationClip`); template member: distinguishing operand | Interior anchor `005BCD62` (`lea`, entry + 0x42) |
| `005BCE50` | `PAnimation::PAnimationClipBinding *` | requires class descriptor `02CADB40` (`PAnimationClipBinding`); template member: distinguishing operand | Interior anchor `005BCE92` (`lea`, entry + 0x42) |
| `005BCF80` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingChannelMap *` | requires class descriptor `02CAD940` (`PAnimationClipBindingChannelMap`); template member: distinguishing operand | Interior anchor `005BCFC2` (`lea`, entry + 0x42) |
| `005BD0B0` | `PAnimation::PAnimationClipBinding::PAnimationClipBindingDataBlockCache *` | requires class descriptor `02CADA40` (`PAnimationClipBindingDataBlockCache`); template member: distinguishing operand | Interior anchor `005BD0F2` (`lea`, entry + 0x42) |
| `005BD1E0` | `PAnimation::PAnimationConstantChannel *` | requires class descriptor `02CADC50` (`PAnimationConstantChannel`); template member: distinguishing operand | Interior anchor `005BD222` (`lea`, entry + 0x42) |
| `005BD310` | `PAnimation::PAnimationController *` | requires class descriptor `02CADD50` (`PAnimationController`); template member: distinguishing operand | Interior anchor `005BD356` (`lea`, entry + 0x46) |
| `005BD440` | `PAnimation::PAnimationDataSource *` | requires class descriptor `02CADE50` (`PAnimationDataSource`); template member: distinguishing operand | Interior anchor `005BD486` (`lea`, entry + 0x46) |
| `005BD570` | `PAnimation::PAnimationDataSourceListEntry *` | requires class descriptor `02CAE350` (`PAnimationDataSourceListEntry`); template member: distinguishing operand | Interior anchor `005BD5B2` (`lea`, entry + 0x42) |
| `005BD6A0` | `PAnimation::PAnimationEvent *` | requires class descriptor `02CAE050` (`PAnimationEvent`); template member: distinguishing operand | Interior anchor `005BD6E2` (`lea`, entry + 0x42) |
| `005BD7D0` | `PAnimation::PAnimationEventController *` | requires class descriptor `02CADF50` (`PAnimationEventController`); template member: distinguishing operand | Interior anchor `005BD816` (`lea`, entry + 0x46) |
| `005BD900` | `PAnimation::PAnimationEventList *` | requires class descriptor `02CAE150` (`PAnimationEventList`); template member: distinguishing operand | Interior anchor `005BD942` (`lea`, entry + 0x42) |
| `005BDA30` | `PAnimation::PAnimationHierarchyNode *` | requires class descriptor `02CAE250` (`PAnimationHierarchyNode`); template member: distinguishing operand | Interior anchor `005BDA76` (`lea`, entry + 0x46) |
| `005BDB60` | `PAnimation::PAnimationNetworkInstance *` | requires class descriptor `02CAE550` (`PAnimationNetworkInstance`); template member: distinguishing operand | Interior anchor `005BDBA6` (`lea`, entry + 0x46) |
| `005BDC90` | `PAnimation::PAnimationNetworkInstanceTarget *` | requires class descriptor `02CAE450` (`PAnimationNetworkInstanceTarget`); template member: distinguishing operand | Interior anchor `005BDCD2` (`lea`, entry + 0x42) |
| `005BDDC0` | `PAnimation::PAnimationSet *` | requires class descriptor `02CAE660` (`PAnimationSet`); template member: distinguishing operand | Interior anchor `005BDE02` (`lea`, entry + 0x42) |
| `005BDEF0` | `PAnimation::PAnimationSlotArray *` | requires class descriptor `02CAE860` (`PAnimationSlotArray`); template member: distinguishing operand | Interior anchor `005BDF32` (`lea`, entry + 0x42) |
| `005BE020` | `PAnimation::PAnimationSlotFilter *` | requires class descriptor `02CAEA60` (`PAnimationSlotFilter`); template member: distinguishing operand | Interior anchor `005BE066` (`lea`, entry + 0x46) |
| `005BE150` | `PAnimation::PAnimationSlotFilterDeferredLoad *` | requires class descriptor `02CAE960` (`PAnimationSlotFilterDeferredLoad`); template member: distinguishing operand | Interior anchor `005BE192` (`lea`, entry + 0x42) |
| `005BE280` | `PAnimation::PAnimationSlotListIndex *` | requires class descriptor `02CAE760` (`PAnimationSlotListIndex`); template member: distinguishing operand | Interior anchor `005BE2C2` (`lea`, entry + 0x42) |
| `005BE3B0` | `PAnimation::PAnimationSpuTargetBlenderController *` | requires class descriptor `02CAEBE0` (`PAnimationSpuTargetBlenderController`); template member: distinguishing operand | Interior anchor `005BE3F6` (`lea`, entry + 0x46) |
| `005BE4E0` | `PAnimation::PAnimationTargetBlenderController *` | requires class descriptor `02CAECE0` (`PAnimationTargetBlenderController`); template member: distinguishing operand | Interior anchor `005BE526` (`lea`, entry + 0x46) |
| `005BE610` | `PAnimation::PAnimationWeightedBlenderController *` | requires class descriptor `02CAEDE0` (`PAnimationWeightedBlenderController`); template member: distinguishing operand | Interior anchor `005BE656` (`lea`, entry + 0x46) |
| `005BE740` | `PAnimation::PBlendableAnimationSource *` | requires class descriptor `02CAD040` (`PBlendableAnimationSource`); template member: distinguishing operand | Interior anchor `005BE782` (`lea`, entry + 0x42) |
| `005BE870` | `PCluster *` | requires class descriptor `02CF8780` (`PCluster`); template member: distinguishing operand | Interior anchor `005BE8B2` (`lea`, entry + 0x42) |
| `005BE9A0` | `PAnimation::PTimeController *` | requires class descriptor `02CAEEE0` (`PTimeController`); template member: distinguishing operand | Interior anchor `005BE9E6` (`lea`, entry + 0x46) |
| `005BEAD0` | `PAnimation::PTimeIntervalController *` | requires class descriptor `02CAEFE0` (`PTimeIntervalController`); template member: distinguishing operand | Interior anchor `005BEB16` (`lea`, entry + 0x46) |
| `005BEC00` | `PAnimation::PTimeScaleOffsetController *` | requires class descriptor `02CAF0E0` (`PTimeScaleOffsetController`); template member: distinguishing operand | Interior anchor `005BEC46` (`lea`, entry + 0x46) |
| `005F24E0` | `PRendering::PConstantBuffer &` | requires class descriptor `02CB6480` (`PConstantBuffer`); template member: distinguishing operand | Interior anchor `005F2519` (`lea`, entry + 0x39) |
| `005F25E0` | `PRendering::PConstantBufferBase &` | requires class descriptor `02CB6380` (`PConstantBufferBase`); template member: distinguishing operand | Interior anchor `005F2619` (`lea`, entry + 0x39) |
| `005F26E0` | `PRendering::PContextVariantFoldingTable &` | requires class descriptor `02CB7BA0` (`PContextVariantFoldingTable`); template member: distinguishing operand | Interior anchor `005F2719` (`lea`, entry + 0x39) |
| `005F27E0` | `PRendering::PEffect &` | requires class descriptor `02CB6680` (`PEffect`); template member: distinguishing operand | Interior anchor `005F2819` (`lea`, entry + 0x39) |
| `005F28E0` | `PRendering::PForwardShadowRenderer &` | requires class descriptor `02CBB400` (`PForwardShadowRenderer`); template member: distinguishing operand | Interior anchor `005F2919` (`lea`, entry + 0x39) |
| `005F29E0` | `PRendering::PIndirectArgsBuffer &` | requires class descriptor `02CB6980` (`PIndirectArgsBuffer`); template member: distinguishing operand | Interior anchor `005F2A19` (`lea`, entry + 0x39) |
| `005F2AE0` | `PRendering::PIndirectArgsBufferBase &` | requires class descriptor `02CB6880` (`PIndirectArgsBufferBase`); template member: distinguishing operand | Interior anchor `005F2B19` (`lea`, entry + 0x39) |
| `005F2BE0` | `PRendering::PMaterialSwitch &` | requires class descriptor `02CB6A80` (`PMaterialSwitch`); template member: distinguishing operand | Interior anchor `005F2C19` (`lea`, entry + 0x39) |
| `005F2CE0` | `PRendering::PMeshInstanceBounds &` | requires class descriptor `02CB7080` (`PMeshInstanceBounds`); template member: distinguishing operand | Interior anchor `005F2D19` (`lea`, entry + 0x39) |
| `005F2DE0` | `PRendering::PMeshInstanceSegmentContext &` | requires class descriptor `02CB6D80` (`PMeshInstanceSegmentContext`); template member: distinguishing operand | Interior anchor `005F2E19` (`lea`, entry + 0x39) |
| `005F2EE0` | `PRendering::PMeshInstanceSegmentStreamBinding &` | requires class descriptor `02CB6C80` (`PMeshInstanceSegmentStreamBinding`); template member: distinguishing operand | Interior anchor `005F2F19` (`lea`, entry + 0x39) |
| `005F2FE0` | `PRendering::PNodeContext &` | requires class descriptor `02CB7280` (`PNodeContext`); template member: distinguishing operand | Interior anchor `005F3019` (`lea`, entry + 0x39) |
| `005F30E0` | `PRendering::PSamplerState &` | requires class descriptor `02CB78A0` (`PSamplerState`); template member: distinguishing operand | Interior anchor `005F3119` (`lea`, entry + 0x39) |
| `005F31E0` | `PRendering::PSamplerStateBase &` | requires class descriptor `02CB77A0` (`PSamplerStateBase`); template member: distinguishing operand | Interior anchor `005F3219` (`lea`, entry + 0x39) |
| `005F32E0` | `PRendering::PSceneRenderPass &` | requires class descriptor `02CB79A0` (`PSceneRenderPass`); template member: distinguishing operand | Interior anchor `005F3319` (`lea`, entry + 0x39) |
| `005F33E0` | `PRendering::PSceneWideParameterBuffer &` | requires class descriptor `02CB7CA0` (`PSceneWideParameterBuffer`); template member: distinguishing operand | Interior anchor `005F3419` (`lea`, entry + 0x39) |
| `005F34E0` | `PRendering::PShader &` | requires class descriptor `02CB9000` (`PShader`); template member: distinguishing operand | Interior anchor `005F3519` (`lea`, entry + 0x39) |
| `005F35E0` | `PRendering::PShaderParameterCaptureBufferByteAddressBuffer &` | requires class descriptor `02CBA500` (`PShaderParameterCaptureBufferByteAddressBuffer`); template member: distinguishing operand | Interior anchor `005F3619` (`lea`, entry + 0x39) |
| `005F36E0` | `PRendering::PShaderParameterCaptureBufferDataBlock &` | requires class descriptor `02CBA700` (`PShaderParameterCaptureBufferDataBlock`); template member: distinguishing operand | Interior anchor `005F3719` (`lea`, entry + 0x39) |
| `005F37E0` | `PRendering::PShaderParameterCaptureBufferIndexDataBlock &` | requires class descriptor `02CBA800` (`PShaderParameterCaptureBufferIndexDataBlock`); template member: distinguishing operand | Interior anchor `005F3819` (`lea`, entry + 0x39) |
| `005F38E0` | `PRendering::PShaderParameterCaptureBufferLocation &` | requires class descriptor `02CB9100` (`PShaderParameterCaptureBufferLocation`); template member: distinguishing operand | Interior anchor `005F3919` (`lea`, entry + 0x39) |
| `005F39E0` | `PRendering::PShaderParameterCaptureBufferLocationSize &` | requires class descriptor `02CB9200` (`PShaderParameterCaptureBufferLocationSize`); template member: distinguishing operand | Interior anchor `005F3A19` (`lea`, entry + 0x39) |
| `005F3AE0` | `PRendering::PShaderParameterCaptureBufferLocationType &` | requires class descriptor `02CB9300` (`PShaderParameterCaptureBufferLocationType`); template member: distinguishing operand | Interior anchor `005F3B19` (`lea`, entry + 0x39) |
| `005F3BE0` | `PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer &` | requires class descriptor `02CB9400` (`PShaderParameterCaptureBufferLocationTypeConstantBuffer`); template member: distinguishing operand | Interior anchor `005F3C19` (`lea`, entry + 0x39) |
| `005F3CE0` | `PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer &` | requires class descriptor `02CBA600` (`PShaderParameterCaptureBufferRWByteAddressBuffer`); template member: distinguishing operand | Interior anchor `005F3D19` (`lea`, entry + 0x39) |
| `005F3DE0` | `PRendering::PShaderParameterCaptureBufferRWStructuredBuffer &` | requires class descriptor `02CBA400` (`PShaderParameterCaptureBufferRWStructuredBuffer`); template member: distinguishing operand | Interior anchor `005F3E19` (`lea`, entry + 0x39) |
| `005F3EE0` | `PRendering::PShaderParameterCaptureBufferRWTexture2D &` | requires class descriptor `02CBA900` (`PShaderParameterCaptureBufferRWTexture2D`); template member: distinguishing operand | Interior anchor `005F3F19` (`lea`, entry + 0x39) |
| `005F3FE0` | `PRendering::PShaderParameterCaptureBufferRWTexture3D &` | requires class descriptor `02CBAA00` (`PShaderParameterCaptureBufferRWTexture3D`); template member: distinguishing operand | Interior anchor `005F4019` (`lea`, entry + 0x39) |
| `005F40E0` | `PRendering::PShaderParameterCaptureBufferSampler &` | requires class descriptor `02CBA200` (`PShaderParameterCaptureBufferSampler`); template member: distinguishing operand | Interior anchor `005F4119` (`lea`, entry + 0x39) |
| `005F41E0` | `PRendering::PShaderParameterCaptureBufferStream &` | requires class descriptor `02CB9C00` (`PShaderParameterCaptureBufferStream`); template member: distinguishing operand | Interior anchor `005F4219` (`lea`, entry + 0x39) |
| `005F42E0` | `PRendering::PShaderParameterCaptureBufferStructuredBuffer &` | requires class descriptor `02CBA300` (`PShaderParameterCaptureBufferStructuredBuffer`); template member: distinguishing operand | Interior anchor `005F4319` (`lea`, entry + 0x39) |
| `005F43E0` | `PRendering::PShaderParameterCaptureBufferTexture2D &` | requires class descriptor `02CB9F00` (`PShaderParameterCaptureBufferTexture2D`); template member: distinguishing operand | Interior anchor `005F4419` (`lea`, entry + 0x39) |
| `005F44E0` | `PRendering::PShaderParameterCaptureBufferTexture3D &` | requires class descriptor `02CBA000` (`PShaderParameterCaptureBufferTexture3D`); template member: distinguishing operand | Interior anchor `005F4519` (`lea`, entry + 0x39) |
| `005F45E0` | `PRendering::PShaderParameterCaptureBufferTextureCubeMap &` | requires class descriptor `02CBA100` (`PShaderParameterCaptureBufferTextureCubeMap`); template member: distinguishing operand | Interior anchor `005F4619` (`lea`, entry + 0x39) |
| `005F46E0` | `PRendering::PShaderParameterCaptureConstantBuffer &` | requires class descriptor `02CB9E00` (`PShaderParameterCaptureConstantBuffer`); template member: distinguishing operand | Interior anchor `005F4719` (`lea`, entry + 0x39) |
| `005F47E0` | `PRendering::PShaderParameterDefinition &` | requires class descriptor `02CB9500` (`PShaderParameterDefinition`); template member: distinguishing operand | Interior anchor `005F4819` (`lea`, entry + 0x39) |
| `005F48E0` | `PRendering::PShaderPass &` | requires class descriptor `02CB9A00` (`PShaderPass`); template member: distinguishing operand | Interior anchor `005F4919` (`lea`, entry + 0x39) |
| `005F49E0` | `PRendering::PShaderPassBase &` | requires class descriptor `02CB9900` (`PShaderPassBase`); template member: distinguishing operand | Interior anchor `005F4A19` (`lea`, entry + 0x39) |
| `005F4AE0` | `PRendering::PShaderPassInfo &` | requires class descriptor `02CB7AA0` (`PShaderPassInfo`); template member: distinguishing operand | Interior anchor `005F4B19` (`lea`, entry + 0x39) |
| `005F4BE0` | `PRendering::PShaderPassParameterLocationTypes &` | requires class descriptor `02CB9700` (`PShaderPassParameterLocationTypes`); template member: distinguishing operand | Interior anchor `005F4C19` (`lea`, entry + 0x39) |
| `005F4CE0` | `PRendering::PShaderPassParameterLocationTypesBase &` | requires class descriptor `02CB9600` (`PShaderPassParameterLocationTypesBase`); template member: distinguishing operand | Interior anchor `005F4D19` (`lea`, entry + 0x39) |
| `005F4DE0` | `PRendering::PShaderPassParameterLocationTypesConstantBuffer &` | requires class descriptor `02CB9800` (`PShaderPassParameterLocationTypesConstantBuffer`); template member: distinguishing operand | Interior anchor `005F4E19` (`lea`, entry + 0x39) |
| `005F4EE0` | `PRendering::PShaderPassStateBase &` | requires class descriptor `02CB9B00` (`PShaderPassStateBase`); template member: distinguishing operand | Interior anchor `005F4F19` (`lea`, entry + 0x39) |
| `005F4FE0` | `PRendering::PShaderProgramBase &` | requires class descriptor `02CBAD00` (`PShaderProgramBase`); template member: distinguishing operand | Interior anchor `005F5019` (`lea`, entry + 0x39) |
| `005F50E0` | `PRendering::PShaderProgramParamsAndStreams &` | requires class descriptor `02CBAC00` (`PShaderProgramParamsAndStreams`); template member: distinguishing operand | Interior anchor `005F5119` (`lea`, entry + 0x39) |
| `005F51E0` | `PRendering::PShaderStreamDefinition &` | requires class descriptor `02CBAE00` (`PShaderStreamDefinition`); template member: distinguishing operand | Interior anchor `005F5219` (`lea`, entry + 0x39) |
| `005F52E0` | `PRendering::PShadowRenderer &` | requires class descriptor `02CBB300` (`PShadowRenderer`); template member: distinguishing operand | Interior anchor `005F5319` (`lea`, entry + 0x39) |
| `005F53E0` | `PRendering::PStructuredBuffer &` | requires class descriptor `02CBB600` (`PStructuredBuffer`); template member: distinguishing operand | Interior anchor `005F5419` (`lea`, entry + 0x39) |
| `005F54E0` | `PRendering::PStructuredBufferBase &` | requires class descriptor `02CBB500` (`PStructuredBufferBase`); template member: distinguishing operand | Interior anchor `005F5519` (`lea`, entry + 0x39) |
| `005F55E0` | `PRendering::PTexture2D &` | requires class descriptor `02CBB900` (`PTexture2D`); template member: distinguishing operand | Interior anchor `005F5619` (`lea`, entry + 0x39) |
| `005F56E0` | `PRendering::PTexture2DBase &` | requires class descriptor `02CBB800` (`PTexture2DBase`); template member: distinguishing operand | Interior anchor `005F5719` (`lea`, entry + 0x39) |
| `005F57E0` | `PRendering::PTexture3D &` | requires class descriptor `02CBBB00` (`PTexture3D`); template member: distinguishing operand | Interior anchor `005F5819` (`lea`, entry + 0x39) |
| `005F58E0` | `PRendering::PTexture3DBase &` | requires class descriptor `02CBBA00` (`PTexture3DBase`); template member: distinguishing operand | Interior anchor `005F5919` (`lea`, entry + 0x39) |
| `005F59E0` | `PRendering::PTextureCommonBase &` | requires class descriptor `02CBB700` (`PTextureCommonBase`); template member: distinguishing operand | Interior anchor `005F5A19` (`lea`, entry + 0x39) |
| `005F5AE0` | `PRendering::PTextureCubeMap &` | requires class descriptor `02CBBD00` (`PTextureCubeMap`); template member: distinguishing operand | Interior anchor `005F5B19` (`lea`, entry + 0x39) |
| `005F5BE0` | `PRendering::PTextureCubeMapBase &` | requires class descriptor `02CBBC00` (`PTextureCubeMapBase`); template member: distinguishing operand | Interior anchor `005F5C19` (`lea`, entry + 0x39) |
| `005F79A0` | `PRendering::PConstantBuffer *` | requires class descriptor `02CB6480` (`PConstantBuffer`); template member: distinguishing operand | Interior anchor `005F79E2` (`lea`, entry + 0x42) |
| `005F7AD0` | `PRendering::PConstantBufferBase *` | requires class descriptor `02CB6380` (`PConstantBufferBase`); template member: distinguishing operand | Interior anchor `005F7B12` (`lea`, entry + 0x42) |
| `005F7C00` | `PRendering::PContextVariantFoldingTable *` | requires class descriptor `02CB7BA0` (`PContextVariantFoldingTable`); template member: distinguishing operand | Interior anchor `005F7C42` (`lea`, entry + 0x42) |
| `005F7D30` | `PRendering::PDynamicMeshInstance *` | requires class descriptor `02CB6580` (`PDynamicMeshInstance`); template member: distinguishing operand | Interior anchor `005F7D76` (`lea`, entry + 0x46) |
| `005F7E60` | `PRendering::PEffect *` | requires class descriptor `02CB6680` (`PEffect`); template member: distinguishing operand | Interior anchor `005F7EA2` (`lea`, entry + 0x42) |
| `005F7F90` | `PRendering::PEffectVariant *` | requires class descriptor `02CB6780` (`PEffectVariant`); template member: distinguishing operand | Interior anchor `005F7FD2` (`lea`, entry + 0x42) |
| `005F80C0` | `PRendering::PForwardShadowRenderer *` | requires class descriptor `02CBB400` (`PForwardShadowRenderer`); template member: distinguishing operand | Interior anchor `005F8102` (`lea`, entry + 0x42) |
| `005F81F0` | `PRendering::PIndirectArgsBuffer *` | requires class descriptor `02CB6980` (`PIndirectArgsBuffer`); template member: distinguishing operand | Interior anchor `005F8232` (`lea`, entry + 0x42) |
| `005F8320` | `PRendering::PIndirectArgsBufferBase *` | requires class descriptor `02CB6880` (`PIndirectArgsBufferBase`); template member: distinguishing operand | Interior anchor `005F8362` (`lea`, entry + 0x42) |
| `005F8450` | `PRendering::PMaterial *` | requires class descriptor `02CB6B80` (`PMaterial`); template member: distinguishing operand | Interior anchor `005F8492` (`lea`, entry + 0x42) |
| `005F8580` | `PRendering::PMaterialSwitch *` | requires class descriptor `02CB6A80` (`PMaterialSwitch`); template member: distinguishing operand | Interior anchor `005F85C2` (`lea`, entry + 0x42) |
| `005F86B0` | `PRendering::PMeshInstance *` | requires class descriptor `02CB6E80` (`PMeshInstance`); template member: distinguishing operand | Interior anchor `005F86F2` (`lea`, entry + 0x42) |
| `005F87E0` | `PRendering::PMeshInstanceAttachPoint *` | requires class descriptor `02CB6F80` (`PMeshInstanceAttachPoint`); template member: distinguishing operand | Interior anchor `005F8822` (`lea`, entry + 0x42) |
| `005F8910` | `PRendering::PMeshInstanceBounds *` | requires class descriptor `02CB7080` (`PMeshInstanceBounds`); template member: distinguishing operand | Interior anchor `005F8952` (`lea`, entry + 0x42) |
| `005F8A40` | `PRendering::PMeshInstanceSegmentContext *` | requires class descriptor `02CB6D80` (`PMeshInstanceSegmentContext`); template member: distinguishing operand | Interior anchor `005F8A82` (`lea`, entry + 0x42) |
| `005F8B70` | `PRendering::PMeshInstanceSegmentStreamBinding *` | requires class descriptor `02CB6C80` (`PMeshInstanceSegmentStreamBinding`); template member: distinguishing operand | Interior anchor `005F8BB2` (`lea`, entry + 0x42) |
| `005F8CA0` | `PRendering::PModifierNetworkDynamicMeshInstance *` | requires class descriptor `02CB7180` (`PModifierNetworkDynamicMeshInstance`); template member: distinguishing operand | Interior anchor `005F8CE6` (`lea`, entry + 0x46) |
| `005F8DD0` | `PRendering::PNodeContext *` | requires class descriptor `02CB7280` (`PNodeContext`); template member: distinguishing operand | Interior anchor `005F8E12` (`lea`, entry + 0x42) |
| `005F8F00` | `PRendering::PParameterBuffer *` | requires class descriptor `02CB7480` (`PParameterBuffer`); template member: distinguishing operand | Interior anchor `005F8F42` (`lea`, entry + 0x42) |
| `005F9030` | `PRendering::PParameterBufferBase *` | requires class descriptor `02CB7380` (`PParameterBufferBase`); template member: distinguishing operand | Interior anchor `005F9072` (`lea`, entry + 0x42) |
| `005F9160` | `PRendering::PRenderTarget *` | requires class descriptor `02CB76A0` (`PRenderTarget`); template member: distinguishing operand | Interior anchor `005F91A2` (`lea`, entry + 0x42) |
| `005F9290` | `PRendering::PRenderTargetBase *` | requires class descriptor `02CB75A0` (`PRenderTargetBase`); template member: distinguishing operand | Interior anchor `005F92D2` (`lea`, entry + 0x42) |
| `005F93C0` | `PRendering::PSamplerState *` | requires class descriptor `02CB78A0` (`PSamplerState`); template member: distinguishing operand | Interior anchor `005F9402` (`lea`, entry + 0x42) |
| `005F94F0` | `PRendering::PSamplerStateBase *` | requires class descriptor `02CB77A0` (`PSamplerStateBase`); template member: distinguishing operand | Interior anchor `005F9532` (`lea`, entry + 0x42) |
| `005F9620` | `PRendering::PSceneRenderPass *` | requires class descriptor `02CB79A0` (`PSceneRenderPass`); template member: distinguishing operand | Interior anchor `005F9662` (`lea`, entry + 0x42) |
| `005F9750` | `PRendering::PSceneWideParameterBuffer *` | requires class descriptor `02CB7CA0` (`PSceneWideParameterBuffer`); template member: distinguishing operand | Interior anchor `005F9792` (`lea`, entry + 0x42) |
| `005F9880` | `PRendering::PShader *` | requires class descriptor `02CB9000` (`PShader`); template member: distinguishing operand | Interior anchor `005F98C2` (`lea`, entry + 0x42) |
| `005F99B0` | `PRendering::PShaderComputeProgram *` | requires class descriptor `02CBB200` (`PShaderComputeProgram`); template member: distinguishing operand | Interior anchor `005F99F2` (`lea`, entry + 0x42) |
| `005F9AE0` | `PRendering::PShaderFragmentProgram *` | requires class descriptor `02CBB000` (`PShaderFragmentProgram`); template member: distinguishing operand | Interior anchor `005F9B22` (`lea`, entry + 0x42) |
| `005F9C10` | `PRendering::PShaderGeometryProgram *` | requires class descriptor `02CBB100` (`PShaderGeometryProgram`); template member: distinguishing operand | Interior anchor `005F9C52` (`lea`, entry + 0x42) |
| `005F9D40` | `PRendering::PShaderParameterCaptureBufferByteAddressBuffer *` | requires class descriptor `02CBA500` (`PShaderParameterCaptureBufferByteAddressBuffer`); template member: distinguishing operand | Interior anchor `005F9D82` (`lea`, entry + 0x42) |
| `005F9E70` | `PRendering::PShaderParameterCaptureBufferDataBlock *` | requires class descriptor `02CBA700` (`PShaderParameterCaptureBufferDataBlock`); template member: distinguishing operand | Interior anchor `005F9EB2` (`lea`, entry + 0x42) |
| `005F9FA0` | `PRendering::PShaderParameterCaptureBufferIndexDataBlock *` | requires class descriptor `02CBA800` (`PShaderParameterCaptureBufferIndexDataBlock`); template member: distinguishing operand | Interior anchor `005F9FE2` (`lea`, entry + 0x42) |
| `005FA0D0` | `PRendering::PShaderParameterCaptureBufferLocation *` | requires class descriptor `02CB9100` (`PShaderParameterCaptureBufferLocation`); template member: distinguishing operand | Interior anchor `005FA112` (`lea`, entry + 0x42) |
| `005FA200` | `PRendering::PShaderParameterCaptureBufferLocationSize *` | requires class descriptor `02CB9200` (`PShaderParameterCaptureBufferLocationSize`); template member: distinguishing operand | Interior anchor `005FA242` (`lea`, entry + 0x42) |
| `005FA330` | `PRendering::PShaderParameterCaptureBufferLocationType *` | requires class descriptor `02CB9300` (`PShaderParameterCaptureBufferLocationType`); template member: distinguishing operand | Interior anchor `005FA372` (`lea`, entry + 0x42) |
| `005FA460` | `PRendering::PShaderParameterCaptureBufferLocationTypeConstantBuffer *` | requires class descriptor `02CB9400` (`PShaderParameterCaptureBufferLocationTypeConstantBuffer`); template member: distinguishing operand | Interior anchor `005FA4A2` (`lea`, entry + 0x42) |
| `005FA590` | `PRendering::PShaderParameterCaptureBufferRWByteAddressBuffer *` | requires class descriptor `02CBA600` (`PShaderParameterCaptureBufferRWByteAddressBuffer`); template member: distinguishing operand | Interior anchor `005FA5D2` (`lea`, entry + 0x42) |
| `005FA6C0` | `PRendering::PShaderParameterCaptureBufferRWStructuredBuffer *` | requires class descriptor `02CBA400` (`PShaderParameterCaptureBufferRWStructuredBuffer`); template member: distinguishing operand | Interior anchor `005FA702` (`lea`, entry + 0x42) |
| `005FA7F0` | `PRendering::PShaderParameterCaptureBufferRWTexture2D *` | requires class descriptor `02CBA900` (`PShaderParameterCaptureBufferRWTexture2D`); template member: distinguishing operand | Interior anchor `005FA832` (`lea`, entry + 0x42) |
| `005FA920` | `PRendering::PShaderParameterCaptureBufferRWTexture3D *` | requires class descriptor `02CBAA00` (`PShaderParameterCaptureBufferRWTexture3D`); template member: distinguishing operand | Interior anchor `005FA962` (`lea`, entry + 0x42) |
| `005FAA50` | `PRendering::PShaderParameterCaptureBufferSampler *` | requires class descriptor `02CBA200` (`PShaderParameterCaptureBufferSampler`); template member: distinguishing operand | Interior anchor `005FAA92` (`lea`, entry + 0x42) |
| `005FAB80` | `PRendering::PShaderParameterCaptureBufferStream *` | requires class descriptor `02CB9C00` (`PShaderParameterCaptureBufferStream`); template member: distinguishing operand | Interior anchor `005FABC2` (`lea`, entry + 0x42) |
| `005FACB0` | `PRendering::PShaderParameterCaptureBufferStructuredBuffer *` | requires class descriptor `02CBA300` (`PShaderParameterCaptureBufferStructuredBuffer`); template member: distinguishing operand | Interior anchor `005FACF2` (`lea`, entry + 0x42) |
| `005FADE0` | `PRendering::PShaderParameterCaptureBufferTexture2D *` | requires class descriptor `02CB9F00` (`PShaderParameterCaptureBufferTexture2D`); template member: distinguishing operand | Interior anchor `005FAE22` (`lea`, entry + 0x42) |
| `005FAF10` | `PRendering::PShaderParameterCaptureBufferTexture3D *` | requires class descriptor `02CBA000` (`PShaderParameterCaptureBufferTexture3D`); template member: distinguishing operand | Interior anchor `005FAF52` (`lea`, entry + 0x42) |
| `005FB040` | `PRendering::PShaderParameterCaptureBufferTextureBase *` | requires class descriptor `02CB9D00` (`PShaderParameterCaptureBufferTextureBase`); template member: distinguishing operand | Interior anchor `005FB082` (`lea`, entry + 0x42) |
| `005FB170` | `PRendering::PShaderParameterCaptureBufferTextureCubeMap *` | requires class descriptor `02CBA100` (`PShaderParameterCaptureBufferTextureCubeMap`); template member: distinguishing operand | Interior anchor `005FB1B2` (`lea`, entry + 0x42) |
| `005FB2A0` | `PRendering::PShaderParameterCaptureConstantBuffer *` | requires class descriptor `02CB9E00` (`PShaderParameterCaptureConstantBuffer`); template member: distinguishing operand | Interior anchor `005FB2E2` (`lea`, entry + 0x42) |
| `005FB3D0` | `PRendering::PShaderParameterDefinition *` | requires class descriptor `02CB9500` (`PShaderParameterDefinition`); template member: distinguishing operand | Interior anchor `005FB412` (`lea`, entry + 0x42) |
| `005FB500` | `PRendering::PShaderPass *` | requires class descriptor `02CB9A00` (`PShaderPass`); template member: distinguishing operand | Interior anchor `005FB542` (`lea`, entry + 0x42) |
| `005FB630` | `PRendering::PShaderPassBase *` | requires class descriptor `02CB9900` (`PShaderPassBase`); template member: distinguishing operand | Interior anchor `005FB672` (`lea`, entry + 0x42) |
| `005FB760` | `PRendering::PShaderPassInfo *` | requires class descriptor `02CB7AA0` (`PShaderPassInfo`); template member: distinguishing operand | Interior anchor `005FB7A2` (`lea`, entry + 0x42) |
| `005FB890` | `PRendering::PShaderPassParameterLocationTypes *` | requires class descriptor `02CB9700` (`PShaderPassParameterLocationTypes`); template member: distinguishing operand | Interior anchor `005FB8D2` (`lea`, entry + 0x42) |
| `005FB9C0` | `PRendering::PShaderPassParameterLocationTypesBase *` | requires class descriptor `02CB9600` (`PShaderPassParameterLocationTypesBase`); template member: distinguishing operand | Interior anchor `005FBA02` (`lea`, entry + 0x42) |
| `005FBAF0` | `PRendering::PShaderPassParameterLocationTypesConstantBuffer *` | requires class descriptor `02CB9800` (`PShaderPassParameterLocationTypesConstantBuffer`); template member: distinguishing operand | Interior anchor `005FBB32` (`lea`, entry + 0x42) |
| `005FBC20` | `PRendering::PShaderPassStateBase *` | requires class descriptor `02CB9B00` (`PShaderPassStateBase`); template member: distinguishing operand | Interior anchor `005FBC62` (`lea`, entry + 0x42) |
| `005FBD50` | `PRendering::PShaderProgramBase *` | requires class descriptor `02CBAD00` (`PShaderProgramBase`); template member: distinguishing operand | Interior anchor `005FBD92` (`lea`, entry + 0x42) |
| `005FBE80` | `PRendering::PShaderProgramParamsAndStreams *` | requires class descriptor `02CBAC00` (`PShaderProgramParamsAndStreams`); template member: distinguishing operand | Interior anchor `005FBEC2` (`lea`, entry + 0x42) |
| `005FBFB0` | `PRendering::PShaderSource *` | requires class descriptor `02CBAB00` (`PShaderSource`); template member: distinguishing operand | Interior anchor `005FBFF2` (`lea`, entry + 0x42) |
| `005FC0E0` | `PRendering::PShaderStreamDefinition *` | requires class descriptor `02CBAE00` (`PShaderStreamDefinition`); template member: distinguishing operand | Interior anchor `005FC122` (`lea`, entry + 0x42) |
| `005FC210` | `PRendering::PShaderVertexProgram *` | requires class descriptor `02CBAF00` (`PShaderVertexProgram`); template member: distinguishing operand | Interior anchor `005FC252` (`lea`, entry + 0x42) |
| `005FC340` | `PRendering::PShadowRenderer *` | requires class descriptor `02CBB300` (`PShadowRenderer`); template member: distinguishing operand | Interior anchor `005FC382` (`lea`, entry + 0x42) |
| `005FC470` | `PRendering::PStructuredBuffer *` | requires class descriptor `02CBB600` (`PStructuredBuffer`); template member: distinguishing operand | Interior anchor `005FC4B2` (`lea`, entry + 0x42) |
| `005FC5A0` | `PRendering::PStructuredBufferBase *` | requires class descriptor `02CBB500` (`PStructuredBufferBase`); template member: distinguishing operand | Interior anchor `005FC5E2` (`lea`, entry + 0x42) |
| `005FC6D0` | `PRendering::PTexture2D *` | requires class descriptor `02CBB900` (`PTexture2D`); template member: distinguishing operand | Interior anchor `005FC712` (`lea`, entry + 0x42) |
| `005FC800` | `PRendering::PTexture2DBase *` | requires class descriptor `02CBB800` (`PTexture2DBase`); template member: distinguishing operand | Interior anchor `005FC842` (`lea`, entry + 0x42) |
| `005FC930` | `PRendering::PTexture3D *` | requires class descriptor `02CBBB00` (`PTexture3D`); template member: distinguishing operand | Interior anchor `005FC972` (`lea`, entry + 0x42) |
| `005FCA60` | `PRendering::PTexture3DBase *` | requires class descriptor `02CBBA00` (`PTexture3DBase`); template member: distinguishing operand | Interior anchor `005FCAA2` (`lea`, entry + 0x42) |
| `005FCB90` | `PRendering::PTextureCommonBase *` | requires class descriptor `02CBB700` (`PTextureCommonBase`); template member: distinguishing operand | Interior anchor `005FCBD2` (`lea`, entry + 0x42) |
| `005FCCC0` | `PRendering::PTextureCubeMap *` | requires class descriptor `02CBBD00` (`PTextureCubeMap`); template member: distinguishing operand | Interior anchor `005FCD02` (`lea`, entry + 0x42) |
| `005FCDF0` | `PRendering::PTextureCubeMapBase *` | requires class descriptor `02CBBC00` (`PTextureCubeMapBase`); template member: distinguishing operand | Interior anchor `005FCE32` (`lea`, entry + 0x42) |
| `00619300` | `PRendering::PConstantBufferD3D11 &` | requires class descriptor `02CF2440` (`PConstantBufferD3D11`); template member: distinguishing operand | Interior anchor `00619339` (`lea`, entry + 0x39) |
| `00619400` | `PRendering::PIndirectArgsBufferD3D11 &` | requires class descriptor `02CF2340` (`PIndirectArgsBufferD3D11`); template member: distinguishing operand | Interior anchor `00619439` (`lea`, entry + 0x39) |
| `00619500` | `PRendering::PSamplerStateD3D11 &` | requires class descriptor `02CF2140` (`PSamplerStateD3D11`); template member: distinguishing operand | Interior anchor `00619539` (`lea`, entry + 0x39) |
| `00619600` | `PRendering::PShaderPassD3D11 &` | requires class descriptor `02CF1440` (`PShaderPassD3D11`); template member: distinguishing operand | Interior anchor `00619639` (`lea`, entry + 0x39) |
| `00619700` | `PRendering::PShaderPassStateD3D11 &` | requires class descriptor `02CF1540` (`PShaderPassStateD3D11`); template member: distinguishing operand | Interior anchor `00619739` (`lea`, entry + 0x39) |
| `00619800` | `PRendering::PStreamInputDescD3D11 &` | requires class descriptor `02CF1640` (`PStreamInputDescD3D11`); template member: distinguishing operand | Interior anchor `00619839` (`lea`, entry + 0x39) |
| `00619900` | `PRendering::PStructuredBufferD3D11 &` | requires class descriptor `02CF2240` (`PStructuredBufferD3D11`); template member: distinguishing operand | Interior anchor `00619939` (`lea`, entry + 0x39) |
| `00619A00` | `PRendering::PTexture2DD3D11 &` | requires class descriptor `02CF1D40` (`PTexture2DD3D11`); template member: distinguishing operand | Interior anchor `00619A39` (`lea`, entry + 0x39) |
| `00619B00` | `PRendering::PTexture3DD3D11 &` | requires class descriptor `02CF1E40` (`PTexture3DD3D11`); template member: distinguishing operand | Interior anchor `00619B39` (`lea`, entry + 0x39) |
| `00619C00` | `PRendering::PTextureCubeMapD3D11 &` | requires class descriptor `02CF1F40` (`PTextureCubeMapD3D11`); template member: distinguishing operand | Interior anchor `00619C39` (`lea`, entry + 0x39) |
| `0061AB10` | `PRendering::PConstantBufferD3D11 *` | requires class descriptor `02CF2440` (`PConstantBufferD3D11`); template member: distinguishing operand | Interior anchor `0061AB52` (`lea`, entry + 0x42) |
| `0061AC40` | `PRendering::PIndirectArgsBufferD3D11 *` | requires class descriptor `02CF2340` (`PIndirectArgsBufferD3D11`); template member: distinguishing operand | Interior anchor `0061AC82` (`lea`, entry + 0x42) |
| `0061AD70` | `PRendering::PRenderTargetD3D11 *` | requires class descriptor `02CF2040` (`PRenderTargetD3D11`); template member: distinguishing operand | Interior anchor `0061ADB2` (`lea`, entry + 0x42) |
| `0061AEA0` | `PRendering::PSamplerStateD3D11 *` | requires class descriptor `02CF2140` (`PSamplerStateD3D11`); template member: distinguishing operand | Interior anchor `0061AEE2` (`lea`, entry + 0x42) |
| `0061AFD0` | `PRendering::PShaderComputeProgramD3D11 *` | requires class descriptor `02CF1C40` (`PShaderComputeProgramD3D11`); template member: distinguishing operand | Interior anchor `0061B012` (`lea`, entry + 0x42) |
| `0061B100` | `PRendering::PShaderFragmentProgramD3D11 *` | requires class descriptor `02CF1A40` (`PShaderFragmentProgramD3D11`); template member: distinguishing operand | Interior anchor `0061B142` (`lea`, entry + 0x42) |
| `0061B230` | `PRendering::PShaderGeometryProgramD3D11 *` | requires class descriptor `02CF1B40` (`PShaderGeometryProgramD3D11`); template member: distinguishing operand | Interior anchor `0061B272` (`lea`, entry + 0x42) |
| `0061B360` | `PRendering::PShaderPassD3D11 *` | requires class descriptor `02CF1440` (`PShaderPassD3D11`); template member: distinguishing operand | Interior anchor `0061B3A2` (`lea`, entry + 0x42) |
| `0061B490` | `PRendering::PShaderPassStateD3D11 *` | requires class descriptor `02CF1540` (`PShaderPassStateD3D11`); template member: distinguishing operand | Interior anchor `0061B4D2` (`lea`, entry + 0x42) |
| `0061B5C0` | `PRendering::PShaderProgramD3D11 *` | requires class descriptor `02CF1840` (`PShaderProgramD3D11`); template member: distinguishing operand | Interior anchor `0061B602` (`lea`, entry + 0x42) |
| `0061B6F0` | `PRendering::PShaderVertexProgramD3D11 *` | requires class descriptor `02CF1940` (`PShaderVertexProgramD3D11`); template member: distinguishing operand | Interior anchor `0061B732` (`lea`, entry + 0x42) |
| `0061B820` | `PRendering::PStreamInputDescD3D11 *` | requires class descriptor `02CF1640` (`PStreamInputDescD3D11`); template member: distinguishing operand | Interior anchor `0061B862` (`lea`, entry + 0x42) |
| `0061B950` | `PRendering::PStreamInputLayoutD3D11 *` | requires class descriptor `02CF1740` (`PStreamInputLayoutD3D11`); template member: distinguishing operand | Interior anchor `0061B992` (`lea`, entry + 0x42) |
| `0061BA80` | `PRendering::PStructuredBufferD3D11 *` | requires class descriptor `02CF2240` (`PStructuredBufferD3D11`); template member: distinguishing operand | Interior anchor `0061BAC2` (`lea`, entry + 0x42) |
| `0061BBB0` | `PRendering::PTexture2DD3D11 *` | requires class descriptor `02CF1D40` (`PTexture2DD3D11`); template member: distinguishing operand | Interior anchor `0061BBF2` (`lea`, entry + 0x42) |
| `0061BCE0` | `PRendering::PTexture3DD3D11 *` | requires class descriptor `02CF1E40` (`PTexture3DD3D11`); template member: distinguishing operand | Interior anchor `0061BD22` (`lea`, entry + 0x42) |
| `0061BE10` | `PRendering::PTextureCubeMapD3D11 *` | requires class descriptor `02CF1F40` (`PTextureCubeMapD3D11`); template member: distinguishing operand | Interior anchor `0061BE52` (`lea`, entry + 0x42) |
| `006365C0` | `PClusterDependencyList &` | requires class descriptor `02CF8880` (`PClusterDependencyList`); template member: distinguishing operand | Interior anchor `006365F9` (`lea`, entry + 0x39) |
| `006366C0` | `PClassDescriptor const &` | requires class descriptor `02CF8470` (`PClassDescriptor`); template member: distinguishing operand | Interior anchor `0063670E` (`lea`, entry + 0x4E) |
| `00636920` | `PBase *` | requires class descriptor `02CF8270` (`PBase`); template member: distinguishing operand | Interior anchor `00636962` (`lea`, entry + 0x42) |
| `00636A50` | `PClassDataMemberDynamic *` | requires class descriptor `02CF8370` (`PClassDataMemberDynamic`); template member: distinguishing operand | Interior anchor `00636A96` (`lea`, entry + 0x46) |
| `00636B80` | `PClassDescriptor *` | requires class descriptor `02CF8470` (`PClassDescriptor`); template member: distinguishing operand | Interior anchor `00636BC6` (`lea`, entry + 0x46) |
| `00636CB0` | `PClassDescriptorDynamic *` | requires class descriptor `02CF8580` (`PClassDescriptorDynamic`); template member: distinguishing operand | Interior anchor `00636CF6` (`lea`, entry + 0x46) |
| `00636DE0` | `PClassMember *` | requires class descriptor `02CF8680` (`PClassMember`); template member: distinguishing operand | Interior anchor `00636E22` (`lea`, entry + 0x42) |
| `00636F10` | `PClusterDependencyList *` | requires class descriptor `02CF8880` (`PClusterDependencyList`); template member: distinguishing operand | Interior anchor `00636F52` (`lea`, entry + 0x42) |
| `00637040` | `PNamespace *` | requires class descriptor `02CF8980` (`PNamespace`); template member: distinguishing operand | Interior anchor `00637086` (`lea`, entry + 0x46) |
| `00637170` | `PWorld *` | requires class descriptor `02CF8A80` (`PWorld`); template member: distinguishing operand | Interior anchor `006371B2` (`lea`, entry + 0x42) |
| `0064B030` | `PPostProcessing::PAtmospherics &` | requires class descriptor `02D368A0` (`PAtmospherics`); template member: distinguishing operand | Interior anchor `0064B07E` (`lea`, entry + 0x4E) |
| `0064B150` | `PPostProcessing::PAtmosphericsBase &` | requires class descriptor `02D367A0` (`PAtmosphericsBase`); template member: distinguishing operand | Interior anchor `0064B19E` (`lea`, entry + 0x4E) |
| `0064B270` | `PPostProcessing::PAtmosphericsD3D11 &` | requires class descriptor `02D369A0` (`PAtmosphericsD3D11`); template member: distinguishing operand | Interior anchor `0064B2BE` (`lea`, entry + 0x4E) |
| `0064B390` | `PPostProcessing::PCelShading &` | requires class descriptor `02D362A0` (`PCelShading`); template member: distinguishing operand | Interior anchor `0064B3DE` (`lea`, entry + 0x4E) |
| `0064B4B0` | `PPostProcessing::PCelShadingBase &` | requires class descriptor `02D361A0` (`PCelShadingBase`); template member: distinguishing operand | Interior anchor `0064B4FE` (`lea`, entry + 0x4E) |
| `0064B5D0` | `PPostProcessing::PCelShadingD3D11 &` | requires class descriptor `02D363A0` (`PCelShadingD3D11`); template member: distinguishing operand | Interior anchor `0064B61E` (`lea`, entry + 0x4E) |
| `0064B6F0` | `PPostProcessing::PDeferredLighting &` | requires class descriptor `02D34940` (`PDeferredLighting`); template member: distinguishing operand | Interior anchor `0064B73E` (`lea`, entry + 0x4E) |
| `0064B810` | `PPostProcessing::PDeferredLightingBase &` | requires class descriptor `02D34840` (`PDeferredLightingBase`); template member: distinguishing operand | Interior anchor `0064B85E` (`lea`, entry + 0x4E) |
| `0064B930` | `PPostProcessing::PDeferredLightingD3D11 &` | requires class descriptor `02D34A40` (`PDeferredLightingD3D11`); template member: distinguishing operand | Interior anchor `0064B97E` (`lea`, entry + 0x4E) |
| `0064BA50` | `PPostProcessing::PDepthOfField &` | requires class descriptor `02D34C40` (`PDepthOfField`); template member: distinguishing operand | Interior anchor `0064BA9E` (`lea`, entry + 0x4E) |
| `0064BB70` | `PPostProcessing::PDepthOfFieldBase &` | requires class descriptor `02D34B40` (`PDepthOfFieldBase`); template member: distinguishing operand | Interior anchor `0064BBBE` (`lea`, entry + 0x4E) |
| `0064BC90` | `PPostProcessing::PDepthOfFieldD3D11 &` | requires class descriptor `02D34D40` (`PDepthOfFieldD3D11`); template member: distinguishing operand | Interior anchor `0064BCDE` (`lea`, entry + 0x4E) |
| `0064BDB0` | `PPostProcessing::PFXAA &` | requires class descriptor `02D35FA0` (`PFXAA`); template member: distinguishing operand | Interior anchor `0064BDFE` (`lea`, entry + 0x4E) |
| `0064BED0` | `PPostProcessing::PFXAABase &` | requires class descriptor `02D35EA0` (`PFXAABase`); template member: distinguishing operand | Interior anchor `0064BF1E` (`lea`, entry + 0x4E) |
| `0064BFF0` | `PPostProcessing::PFXAAD3D11 &` | requires class descriptor `02D360A0` (`PFXAAD3D11`); template member: distinguishing operand | Interior anchor `0064C03E` (`lea`, entry + 0x4E) |
| `0064C110` | `PPostProcessing::PGlow &` | requires class descriptor `02D35CA0` (`PGlow`); template member: distinguishing operand | Interior anchor `0064C15E` (`lea`, entry + 0x4E) |
| `0064C230` | `PPostProcessing::PGlowBase &` | requires class descriptor `02D35AA0` (`PGlowBase`); template member: distinguishing operand | Interior anchor `0064C27E` (`lea`, entry + 0x4E) |
| `0064C350` | `PPostProcessing::PGlowD3D11 &` | requires class descriptor `02D35DA0` (`PGlowD3D11`); template member: distinguishing operand | Interior anchor `0064C39E` (`lea`, entry + 0x4E) |
| `0064C470` | `PPostProcessing::PGlowGPUBase &` | requires class descriptor `02D35BA0` (`PGlowGPUBase`); template member: distinguishing operand | Interior anchor `0064C4BE` (`lea`, entry + 0x4E) |
| `0064C590` | `PPostProcessing::PLowResParticles &` | requires class descriptor `02D36AA0` (`PLowResParticles`); template member: distinguishing operand | Interior anchor `0064C5DE` (`lea`, entry + 0x4E) |
| `0064C6B0` | `PPostProcessing::PMLAA &` | requires class descriptor `02D357A0` (`PMLAA`); template member: distinguishing operand | Interior anchor `0064C6FE` (`lea`, entry + 0x4E) |
| `0064C7D0` | `PPostProcessing::PMLAABase &` | requires class descriptor `02D356A0` (`PMLAABase`); template member: distinguishing operand | Interior anchor `0064C81E` (`lea`, entry + 0x4E) |
| `0064C8F0` | `PPostProcessing::PMLAAD3D11 &` | requires class descriptor `02D358A0` (`PMLAAD3D11`); template member: distinguishing operand | Interior anchor `0064C93E` (`lea`, entry + 0x4E) |
| `0064CA10` | `PPostProcessing::PMaterialPostEffect &` | requires class descriptor `02D36BA0` (`PMaterialPostEffect`); template member: distinguishing operand | Interior anchor `0064CA5E` (`lea`, entry + 0x4E) |
| `0064CB30` | `PPostProcessing::PMeshParticleSystemBase &` | requires class descriptor `02D359A0` (`PMeshParticleSystemBase`); template member: distinguishing operand | Interior anchor `0064CB7E` (`lea`, entry + 0x4E) |
| `0064CC50` | `PPostProcessing::PMotionBlur &` | requires class descriptor `02D34F40` (`PMotionBlur`); template member: distinguishing operand | Interior anchor `0064CC9E` (`lea`, entry + 0x4E) |
| `0064CD70` | `PPostProcessing::PMotionBlurBase &` | requires class descriptor `02D34E40` (`PMotionBlurBase`); template member: distinguishing operand | Interior anchor `0064CDBE` (`lea`, entry + 0x4E) |
| `0064CE90` | `PPostProcessing::PMotionBlurD3D11 &` | requires class descriptor `02D35040` (`PMotionBlurD3D11`); template member: distinguishing operand | Interior anchor `0064CEDE` (`lea`, entry + 0x4E) |
| `0064CFB0` | `PPostProcessing::PPostEffectBase &` | requires class descriptor `02D34740` (`PPostEffectBase`); template member: distinguishing operand | Interior anchor `0064CFFE` (`lea`, entry + 0x4E) |
| `0064D0D0` | `PPostProcessing::PPostEffectManager &` | requires class descriptor `02D36CA0` (`PPostEffectManager`); template member: distinguishing operand | Interior anchor `0064D109` (`lea`, entry + 0x39) |
| `0064D1D0` | `PPostProcessing::PScreenSpaceAmbientOcclusion &` | requires class descriptor `02D35400` (`PScreenSpaceAmbientOcclusion`); template member: distinguishing operand | Interior anchor `0064D21E` (`lea`, entry + 0x4E) |
| `0064D2F0` | `PPostProcessing::PScreenSpaceAmbientOcclusionBase &` | requires class descriptor `02D35300` (`PScreenSpaceAmbientOcclusionBase`); template member: distinguishing operand | Interior anchor `0064D33E` (`lea`, entry + 0x4E) |
| `0064D410` | `PPostProcessing::PScreenSpaceAmbientOcclusionD3D11 &` | requires class descriptor `02D35500` (`PScreenSpaceAmbientOcclusionD3D11`); template member: distinguishing operand | Interior anchor `0064D45E` (`lea`, entry + 0x4E) |
| `0064D530` | `PPostProcessing::PScreenSpaceReflection &` | requires class descriptor `02D365A0` (`PScreenSpaceReflection`); template member: distinguishing operand | Interior anchor `0064D57E` (`lea`, entry + 0x4E) |
| `0064D650` | `PPostProcessing::PScreenSpaceReflectionBase &` | requires class descriptor `02D364A0` (`PScreenSpaceReflectionBase`); template member: distinguishing operand | Interior anchor `0064D69E` (`lea`, entry + 0x4E) |
| `0064D770` | `PPostProcessing::PScreenSpaceReflectionD3D11 &` | requires class descriptor `02D366A0` (`PScreenSpaceReflectionD3D11`); template member: distinguishing operand | Interior anchor `0064D7BE` (`lea`, entry + 0x4E) |
| `0064D9D0` | `PPostProcessing::PAtmospherics *` | requires class descriptor `02D368A0` (`PAtmospherics`); template member: distinguishing operand | Interior anchor `0064DA16` (`lea`, entry + 0x46) |
| `0064DB00` | `PPostProcessing::PAtmosphericsBase *` | requires class descriptor `02D367A0` (`PAtmosphericsBase`); template member: distinguishing operand | Interior anchor `0064DB46` (`lea`, entry + 0x46) |
| `0064DC30` | `PPostProcessing::PAtmosphericsD3D11 *` | requires class descriptor `02D369A0` (`PAtmosphericsD3D11`); template member: distinguishing operand | Interior anchor `0064DC76` (`lea`, entry + 0x46) |
| `0064DD60` | `PPostProcessing::PCelShading *` | requires class descriptor `02D362A0` (`PCelShading`); template member: distinguishing operand | Interior anchor `0064DDA6` (`lea`, entry + 0x46) |
| `0064DE90` | `PPostProcessing::PCelShadingBase *` | requires class descriptor `02D361A0` (`PCelShadingBase`); template member: distinguishing operand | Interior anchor `0064DED6` (`lea`, entry + 0x46) |
| `0064DFC0` | `PPostProcessing::PCelShadingD3D11 *` | requires class descriptor `02D363A0` (`PCelShadingD3D11`); template member: distinguishing operand | Interior anchor `0064E006` (`lea`, entry + 0x46) |
| `0064E0F0` | `PPostProcessing::PDeferredLighting *` | requires class descriptor `02D34940` (`PDeferredLighting`); template member: distinguishing operand | Interior anchor `0064E136` (`lea`, entry + 0x46) |
| `0064E220` | `PPostProcessing::PDeferredLightingBase *` | requires class descriptor `02D34840` (`PDeferredLightingBase`); template member: distinguishing operand | Interior anchor `0064E266` (`lea`, entry + 0x46) |
| `0064E350` | `PPostProcessing::PDeferredLightingD3D11 *` | requires class descriptor `02D34A40` (`PDeferredLightingD3D11`); template member: distinguishing operand | Interior anchor `0064E396` (`lea`, entry + 0x46) |
| `0064E480` | `PPostProcessing::PDepthOfField *` | requires class descriptor `02D34C40` (`PDepthOfField`); template member: distinguishing operand | Interior anchor `0064E4C6` (`lea`, entry + 0x46) |
| `0064E5B0` | `PPostProcessing::PDepthOfFieldBase *` | requires class descriptor `02D34B40` (`PDepthOfFieldBase`); template member: distinguishing operand | Interior anchor `0064E5F6` (`lea`, entry + 0x46) |
| `0064E6E0` | `PPostProcessing::PDepthOfFieldD3D11 *` | requires class descriptor `02D34D40` (`PDepthOfFieldD3D11`); template member: distinguishing operand | Interior anchor `0064E726` (`lea`, entry + 0x46) |
| `0064E810` | `PPostProcessing::PFXAA *` | requires class descriptor `02D35FA0` (`PFXAA`); template member: distinguishing operand | Interior anchor `0064E856` (`lea`, entry + 0x46) |
| `0064E940` | `PPostProcessing::PFXAABase *` | requires class descriptor `02D35EA0` (`PFXAABase`); template member: distinguishing operand | Interior anchor `0064E986` (`lea`, entry + 0x46) |
| `0064EA70` | `PPostProcessing::PFXAAD3D11 *` | requires class descriptor `02D360A0` (`PFXAAD3D11`); template member: distinguishing operand | Interior anchor `0064EAB6` (`lea`, entry + 0x46) |
| `0064EBA0` | `PPostProcessing::PGlow *` | requires class descriptor `02D35CA0` (`PGlow`); template member: distinguishing operand | Interior anchor `0064EBE6` (`lea`, entry + 0x46) |
| `0064ECD0` | `PPostProcessing::PGlowBase *` | requires class descriptor `02D35AA0` (`PGlowBase`); template member: distinguishing operand | Interior anchor `0064ED16` (`lea`, entry + 0x46) |
| `0064EE00` | `PPostProcessing::PGlowD3D11 *` | requires class descriptor `02D35DA0` (`PGlowD3D11`); template member: distinguishing operand | Interior anchor `0064EE46` (`lea`, entry + 0x46) |
| `0064EF30` | `PPostProcessing::PGlowGPUBase *` | requires class descriptor `02D35BA0` (`PGlowGPUBase`); template member: distinguishing operand | Interior anchor `0064EF76` (`lea`, entry + 0x46) |
| `0064F060` | `PPostProcessing::PLowResParticles *` | requires class descriptor `02D36AA0` (`PLowResParticles`); template member: distinguishing operand | Interior anchor `0064F0A6` (`lea`, entry + 0x46) |
| `0064F190` | `PPostProcessing::PMLAA *` | requires class descriptor `02D357A0` (`PMLAA`); template member: distinguishing operand | Interior anchor `0064F1D6` (`lea`, entry + 0x46) |
| `0064F2C0` | `PPostProcessing::PMLAABase *` | requires class descriptor `02D356A0` (`PMLAABase`); template member: distinguishing operand | Interior anchor `0064F306` (`lea`, entry + 0x46) |
| `0064F3F0` | `PPostProcessing::PMLAAD3D11 *` | requires class descriptor `02D358A0` (`PMLAAD3D11`); template member: distinguishing operand | Interior anchor `0064F436` (`lea`, entry + 0x46) |
| `0064F520` | `PPostProcessing::PMaterialPostEffect *` | requires class descriptor `02D36BA0` (`PMaterialPostEffect`); template member: distinguishing operand | Interior anchor `0064F566` (`lea`, entry + 0x46) |
| `0064F650` | `PPostProcessing::PMeshParticleSystemBase *` | requires class descriptor `02D359A0` (`PMeshParticleSystemBase`); template member: distinguishing operand | Interior anchor `0064F696` (`lea`, entry + 0x46) |
| `0064F780` | `PPostProcessing::PMotionBlur *` | requires class descriptor `02D34F40` (`PMotionBlur`); template member: distinguishing operand | Interior anchor `0064F7C6` (`lea`, entry + 0x46) |
| `0064F8B0` | `PPostProcessing::PMotionBlurBase *` | requires class descriptor `02D34E40` (`PMotionBlurBase`); template member: distinguishing operand | Interior anchor `0064F8F6` (`lea`, entry + 0x46) |
| `0064F9E0` | `PPostProcessing::PMotionBlurD3D11 *` | requires class descriptor `02D35040` (`PMotionBlurD3D11`); template member: distinguishing operand | Interior anchor `0064FA26` (`lea`, entry + 0x46) |
| `0064FB10` | `PPostProcessing::PPostEffectBase *` | requires class descriptor `02D34740` (`PPostEffectBase`); template member: distinguishing operand | Interior anchor `0064FB56` (`lea`, entry + 0x46) |
| `0064FC40` | `PPostProcessing::PPostEffectManager *` | requires class descriptor `02D36CA0` (`PPostEffectManager`); template member: distinguishing operand | Interior anchor `0064FC82` (`lea`, entry + 0x42) |
| `0064FD70` | `PPostProcessing::PScreenSpaceAmbientOcclusion *` | requires class descriptor `02D35400` (`PScreenSpaceAmbientOcclusion`); template member: distinguishing operand | Interior anchor `0064FDB6` (`lea`, entry + 0x46) |
| `0064FEA0` | `PPostProcessing::PScreenSpaceAmbientOcclusionBase *` | requires class descriptor `02D35300` (`PScreenSpaceAmbientOcclusionBase`); template member: distinguishing operand | Interior anchor `0064FEE6` (`lea`, entry + 0x46) |
| `0064FFD0` | `PPostProcessing::PScreenSpaceAmbientOcclusionD3D11 *` | requires class descriptor `02D35500` (`PScreenSpaceAmbientOcclusionD3D11`); template member: distinguishing operand | Interior anchor `00650016` (`lea`, entry + 0x46) |
| `00650100` | `PPostProcessing::PScreenSpaceReflection *` | requires class descriptor `02D365A0` (`PScreenSpaceReflection`); template member: distinguishing operand | Interior anchor `00650146` (`lea`, entry + 0x46) |
| `00650230` | `PPostProcessing::PScreenSpaceReflectionBase *` | requires class descriptor `02D364A0` (`PScreenSpaceReflectionBase`); template member: distinguishing operand | Interior anchor `00650276` (`lea`, entry + 0x46) |
| `00650360` | `PPostProcessing::PScreenSpaceReflectionD3D11 *` | requires class descriptor `02D366A0` (`PScreenSpaceReflectionD3D11`); template member: distinguishing operand | Interior anchor `006503A6` (`lea`, entry + 0x46) |
| `0066BA00` | `PGeometry::PDataBlock &` | requires class descriptor `02D39E40` (`PDataBlock`); template member: distinguishing operand | Interior anchor `0066BA39` (`lea`, entry + 0x39) |
| `0066BB00` | `PGeometry::PDataBlockBase &` | requires class descriptor `02D39D40` (`PDataBlockBase`); template member: distinguishing operand | Interior anchor `0066BB39` (`lea`, entry + 0x39) |
| `0066BC00` | `PGeometry::PDataBlockBufferD3D11 &` | requires class descriptor `02D39B40` (`PDataBlockBufferD3D11`); template member: distinguishing operand | Interior anchor `0066BC39` (`lea`, entry + 0x39) |
| `0066BD00` | `PGeometry::PDataBlockD3D11 &` | requires class descriptor `02D39C40` (`PDataBlockD3D11`); template member: distinguishing operand | Interior anchor `0066BD39` (`lea`, entry + 0x39) |
| `0066BE00` | `PGeometry::PDynamicDataBlock &` | requires class descriptor `02D39F40` (`PDynamicDataBlock`); template member: distinguishing operand | Interior anchor `0066BE39` (`lea`, entry + 0x39) |
| `0066BF00` | `PGeometry::PDynamicMesh::PDynamicSegmentDesc &` | requires class descriptor `02D3A040` (`PDynamicSegmentDesc`); template member: distinguishing operand | Interior anchor `0066BF39` (`lea`, entry + 0x39) |
| `0066C000` | `PGeometry::PIndexDataBlock &` | requires class descriptor `02D3A340` (`PIndexDataBlock`); template member: distinguishing operand | Interior anchor `0066C039` (`lea`, entry + 0x39) |
| `0066C100` | `PGeometry::PIndexDataBlockBase &` | requires class descriptor `02D3A240` (`PIndexDataBlockBase`); template member: distinguishing operand | Interior anchor `0066C139` (`lea`, entry + 0x39) |
| `0066C200` | `PGeometry::PIndexDataBlockBufferD3D11 &` | requires class descriptor `02D39940` (`PIndexDataBlockBufferD3D11`); template member: distinguishing operand | Interior anchor `0066C239` (`lea`, entry + 0x39) |
| `0066C300` | `PGeometry::PIndexDataBlockD3D11 &` | requires class descriptor `02D39A40` (`PIndexDataBlockD3D11`); template member: distinguishing operand | Interior anchor `0066C339` (`lea`, entry + 0x39) |
| `0066C400` | `PGeometry::PMaterialSet &` | requires class descriptor `02D3A440` (`PMaterialSet`); template member: distinguishing operand | Interior anchor `0066C439` (`lea`, entry + 0x39) |
| `0066C500` | `PGeometry::PMesh &` | requires class descriptor `02D3A640` (`PMesh`); template member: distinguishing operand | Interior anchor `0066C539` (`lea`, entry + 0x39) |
| `0066C600` | `PGeometry::PMeshSegment &` | requires class descriptor `02D3A940` (`PMeshSegment`); template member: distinguishing operand | Interior anchor `0066C639` (`lea`, entry + 0x39) |
| `0066C700` | `PGeometry::PMeshSegmentBase &` | requires class descriptor `02D3A840` (`PMeshSegmentBase`); template member: distinguishing operand | Interior anchor `0066C739` (`lea`, entry + 0x39) |
| `0066C800` | `PGeometry::PMeshSegmentD3D11 &` | requires class descriptor `02D39840` (`PMeshSegmentD3D11`); template member: distinguishing operand | Interior anchor `0066C839` (`lea`, entry + 0x39) |
| `0066C900` | `PGeometry::PShape &` | requires class descriptor `02D3ACE0` (`PShape`); template member: distinguishing operand | Interior anchor `0066C939` (`lea`, entry + 0x39) |
| `0066CA00` | `PGeometry::PSkeletonJointBounds &` | requires class descriptor `02D3A540` (`PSkeletonJointBounds`); template member: distinguishing operand | Interior anchor `0066CA39` (`lea`, entry + 0x39) |
| `0066CB00` | `PGeometry::PSkinBoneRemap &` | requires class descriptor `02D3A740` (`PSkinBoneRemap`); template member: distinguishing operand | Interior anchor `0066CB39` (`lea`, entry + 0x39) |
| `0066CC00` | `PGeometry::PVertexStream &` | requires class descriptor `02D3ADE0` (`PVertexStream`); template member: distinguishing operand | Interior anchor `0066CC39` (`lea`, entry + 0x39) |
| `0066DAC0` | `PGeometry::PDataBlock *` | requires class descriptor `02D39E40` (`PDataBlock`); template member: distinguishing operand | Interior anchor `0066DB02` (`lea`, entry + 0x42) |
| `0066DBF0` | `PGeometry::PDataBlockBase *` | requires class descriptor `02D39D40` (`PDataBlockBase`); template member: distinguishing operand | Interior anchor `0066DC32` (`lea`, entry + 0x42) |
| `0066DD20` | `PGeometry::PDataBlockBufferD3D11 *` | requires class descriptor `02D39B40` (`PDataBlockBufferD3D11`); template member: distinguishing operand | Interior anchor `0066DD62` (`lea`, entry + 0x42) |
| `0066DE50` | `PGeometry::PDataBlockD3D11 *` | requires class descriptor `02D39C40` (`PDataBlockD3D11`); template member: distinguishing operand | Interior anchor `0066DE92` (`lea`, entry + 0x42) |
| `0066DF80` | `PGeometry::PDynamicDataBlock *` | requires class descriptor `02D39F40` (`PDynamicDataBlock`); template member: distinguishing operand | Interior anchor `0066DFC2` (`lea`, entry + 0x42) |
| `0066E0B0` | `PGeometry::PDynamicMesh *` | requires class descriptor `02D3A140` (`PDynamicMesh`); template member: distinguishing operand | Interior anchor `0066E0F6` (`lea`, entry + 0x46) |
| `0066E1E0` | `PGeometry::PDynamicMesh::PDynamicSegmentDesc *` | requires class descriptor `02D3A040` (`PDynamicSegmentDesc`); template member: distinguishing operand | Interior anchor `0066E222` (`lea`, entry + 0x42) |
| `0066E310` | `PGeometry::PIndexDataBlock *` | requires class descriptor `02D3A340` (`PIndexDataBlock`); template member: distinguishing operand | Interior anchor `0066E352` (`lea`, entry + 0x42) |
| `0066E440` | `PGeometry::PIndexDataBlockBase *` | requires class descriptor `02D3A240` (`PIndexDataBlockBase`); template member: distinguishing operand | Interior anchor `0066E482` (`lea`, entry + 0x42) |
| `0066E570` | `PGeometry::PIndexDataBlockBufferD3D11 *` | requires class descriptor `02D39940` (`PIndexDataBlockBufferD3D11`); template member: distinguishing operand | Interior anchor `0066E5B2` (`lea`, entry + 0x42) |
| `0066E6A0` | `PGeometry::PIndexDataBlockD3D11 *` | requires class descriptor `02D39A40` (`PIndexDataBlockD3D11`); template member: distinguishing operand | Interior anchor `0066E6E2` (`lea`, entry + 0x42) |
| `0066E7D0` | `PGeometry::PMaterialSet *` | requires class descriptor `02D3A440` (`PMaterialSet`); template member: distinguishing operand | Interior anchor `0066E812` (`lea`, entry + 0x42) |
| `0066E900` | `PGeometry::PMesh *` | requires class descriptor `02D3A640` (`PMesh`); template member: distinguishing operand | Interior anchor `0066E942` (`lea`, entry + 0x42) |
| `0066EA30` | `PGeometry::PMeshSegment *` | requires class descriptor `02D3A940` (`PMeshSegment`); template member: distinguishing operand | Interior anchor `0066EA72` (`lea`, entry + 0x42) |
| `0066EB60` | `PGeometry::PMeshSegmentBase *` | requires class descriptor `02D3A840` (`PMeshSegmentBase`); template member: distinguishing operand | Interior anchor `0066EBA2` (`lea`, entry + 0x42) |
| `0066EC90` | `PGeometry::PMeshSegmentD3D11 *` | requires class descriptor `02D39840` (`PMeshSegmentD3D11`); template member: distinguishing operand | Interior anchor `0066ECD2` (`lea`, entry + 0x42) |
| `0066EDC0` | `PGeometry::PShape *` | requires class descriptor `02D3ACE0` (`PShape`); template member: distinguishing operand | Interior anchor `0066EE02` (`lea`, entry + 0x42) |
| `0066EEF0` | `PGeometry::PSkeletonJointBounds *` | requires class descriptor `02D3A540` (`PSkeletonJointBounds`); template member: distinguishing operand | Interior anchor `0066EF32` (`lea`, entry + 0x42) |
| `0066F020` | `PGeometry::PSkinBoneRemap *` | requires class descriptor `02D3A740` (`PSkinBoneRemap`); template member: distinguishing operand | Interior anchor `0066F062` (`lea`, entry + 0x42) |
| `0066F150` | `PGeometry::PVertexStream *` | requires class descriptor `02D3ADE0` (`PVertexStream`); template member: distinguishing operand | Interior anchor `0066F192` (`lea`, entry + 0x42) |
| `00676600` | `PAssetReferenceImport &` | requires class descriptor `02D3E780` (`PAssetReferenceImport`); template member: distinguishing operand | Interior anchor `00676639` (`lea`, entry + 0x39) |
| `00676810` | `PAssetReference *` | requires class descriptor `02D3E680` (`PAssetReference`); template member: distinguishing operand | Interior anchor `00676852` (`lea`, entry + 0x42) |
| `00676940` | `PAssetReferenceImport *` | requires class descriptor `02D3E780` (`PAssetReferenceImport`); template member: distinguishing operand | Interior anchor `00676982` (`lea`, entry + 0x42) |
| `00678BB0` | `PCamera &` | requires class descriptor `02D3F210` (`PCamera`); template member: distinguishing operand | Interior anchor `00678BE9` (`lea`, entry + 0x39) |
| `00678CB0` | `PCamera *` | requires class descriptor `02D3F210` (`PCamera`); template member: distinguishing operand | Interior anchor `00678CF2` (`lea`, entry + 0x42) |
| `00678DE0` | `PCameraProjection *` | requires class descriptor `02D3F310` (`PCameraProjection`); template member: distinguishing operand | Interior anchor `00678E26` (`lea`, entry + 0x46) |
| `0067DC50` | `PText::PBitmapFontCharInfo &` | requires class descriptor `02E3F960` (`PBitmapFontCharInfo`); template member: distinguishing operand | Interior anchor `0067DC89` (`lea`, entry + 0x39) |
| `0067DE90` | `PText::PBitmapFont *` | requires class descriptor `02E3FA60` (`PBitmapFont`); template member: distinguishing operand | Interior anchor `0067DED2` (`lea`, entry + 0x42) |
| `0067DFC0` | `PText::PBitmapFontCharInfo *` | requires class descriptor `02E3F960` (`PBitmapFontCharInfo`); template member: distinguishing operand | Interior anchor `0067E002` (`lea`, entry + 0x42) |
| `0067EAC0` | `PWorldMatrix &` | requires class descriptor `02E404B0` (`PWorldMatrix`); template member: distinguishing operand | Interior anchor `0067EAF9` (`lea`, entry + 0x39) |
| `0067ECD0` | `PWorldMatrix const &` | requires class descriptor `02E404B0` (`PWorldMatrix`); template member: distinguishing operand | Interior anchor `0067ED09` (`lea`, entry + 0x39) |
| `0067EDD0` | `PWorldMatrix *` | requires class descriptor `02E404B0` (`PWorldMatrix`); template member: distinguishing operand | Interior anchor `0067EE12` (`lea`, entry + 0x42) |
| `00682F40` | `PScripting::PAsyncProcessHeader &` | requires class descriptor `02E41270` (`PAsyncProcessHeader`); template member: distinguishing operand | Interior anchor `00682F79` (`lea`, entry + 0x39) |
| `00683150` | `PScripting::PScript &` | requires class descriptor `02E41470` (`PScript`); template member: distinguishing operand | Interior anchor `00683189` (`lea`, entry + 0x39) |
| `00683250` | `PScripting::PScriptCallbackHandler &` | requires class descriptor `02E41170` (`PScriptCallbackHandler`); template member: distinguishing operand | Interior anchor `00683289` (`lea`, entry + 0x39) |
| `00683350` | `PScripting::PScript const &` | requires class descriptor `02E41470` (`PScript`); template member: distinguishing operand | Interior anchor `00683389` (`lea`, entry + 0x39) |
| `00683450` | `PScripting::PAsyncProcessHeader *` | requires class descriptor `02E41270` (`PAsyncProcessHeader`); template member: distinguishing operand | Interior anchor `00683492` (`lea`, entry + 0x42) |
| `00683580` | `PScripting::PClassCallableMethodScript *` | requires class descriptor `02E41070` (`PClassCallableMethodScript`); template member: distinguishing operand | Interior anchor `006835C2` (`lea`, entry + 0x42) |
| `006836B0` | `PScripting::PScheduler *` | requires class descriptor `02E41370` (`PScheduler`); template member: distinguishing operand | Interior anchor `006836F6` (`lea`, entry + 0x46) |
| `006837E0` | `PScripting::PScript *` | requires class descriptor `02E41470` (`PScript`); template member: distinguishing operand | Interior anchor `00683822` (`lea`, entry + 0x42) |
| `00683910` | `PScripting::PScriptCallbackHandler *` | requires class descriptor `02E41170` (`PScriptCallbackHandler`); template member: distinguishing operand | Interior anchor `00683952` (`lea`, entry + 0x42) |
| `00698E10` | `PPhysics::PPhysicsBox &` | requires class descriptor `02E479D0` (`PPhysicsBox`); template member: distinguishing operand | Interior anchor `00698E5E` (`lea`, entry + 0x4E) |
| `00698F30` | `PPhysics::PPhysicsBoxBase &` | requires class descriptor `02E478D0` (`PPhysicsBoxBase`); template member: distinguishing operand | Interior anchor `00698F7E` (`lea`, entry + 0x4E) |
| `00699050` | `PPhysics::PPhysicsBoxBullet &` | requires class descriptor `02E496D0` (`PPhysicsBoxBullet`); template member: distinguishing operand | Interior anchor `0069909E` (`lea`, entry + 0x4E) |
| `00699170` | `PPhysics::PPhysicsCapsule &` | requires class descriptor `02E47BD0` (`PPhysicsCapsule`); template member: distinguishing operand | Interior anchor `006991BE` (`lea`, entry + 0x4E) |
| `00699290` | `PPhysics::PPhysicsCapsuleBase &` | requires class descriptor `02E47AD0` (`PPhysicsCapsuleBase`); template member: distinguishing operand | Interior anchor `006992DE` (`lea`, entry + 0x4E) |
| `006993B0` | `PPhysics::PPhysicsCapsuleBullet &` | requires class descriptor `02E497D0` (`PPhysicsCapsuleBullet`); template member: distinguishing operand | Interior anchor `006993FE` (`lea`, entry + 0x4E) |
| `006994D0` | `PPhysics::PPhysicsCharacterCamera &` | requires class descriptor `02E47CD0` (`PPhysicsCharacterCamera`); template member: distinguishing operand | Interior anchor `0069951E` (`lea`, entry + 0x4E) |
| `006995F0` | `PPhysics::PPhysicsCharacterController &` | requires class descriptor `02E47ED0` (`PPhysicsCharacterController`); template member: distinguishing operand | Interior anchor `00699629` (`lea`, entry + 0x39) |
| `006996F0` | `PPhysics::PPhysicsCharacterControllerBase &` | requires class descriptor `02E47DD0` (`PPhysicsCharacterControllerBase`); template member: distinguishing operand | Interior anchor `00699729` (`lea`, entry + 0x39) |
| `006997F0` | `PPhysics::PPhysicsCharacterControllerBullet &` | requires class descriptor `02E49FD0` (`PPhysicsCharacterControllerBullet`); template member: distinguishing operand | Interior anchor `00699829` (`lea`, entry + 0x39) |
| `006998F0` | `PPhysics::PPhysicsCylinder &` | requires class descriptor `02E480D0` (`PPhysicsCylinder`); template member: distinguishing operand | Interior anchor `0069993E` (`lea`, entry + 0x4E) |
| `00699A10` | `PPhysics::PPhysicsCylinderBase &` | requires class descriptor `02E47FD0` (`PPhysicsCylinderBase`); template member: distinguishing operand | Interior anchor `00699A5E` (`lea`, entry + 0x4E) |
| `00699B30` | `PPhysics::PPhysicsCylinderBullet &` | requires class descriptor `02E498D0` (`PPhysicsCylinderBullet`); template member: distinguishing operand | Interior anchor `00699B7E` (`lea`, entry + 0x4E) |
| `00699C50` | `PPhysics::PPhysicsInterfaceBase &` | requires class descriptor `02E481D0` (`PPhysicsInterfaceBase`); template member: distinguishing operand | Interior anchor `00699C9E` (`lea`, entry + 0x4E) |
| `00699D70` | `PPhysics::PPhysicsInterfaceBullet &` | requires class descriptor `02E49ED0` (`PPhysicsInterfaceBullet`); template member: distinguishing operand | Interior anchor `00699DBE` (`lea`, entry + 0x4E) |
| `00699E90` | `PPhysics::PPhysicsMaterial &` | requires class descriptor `02E483D0` (`PPhysicsMaterial`); template member: distinguishing operand | Interior anchor `00699EC9` (`lea`, entry + 0x39) |
| `00699F90` | `PPhysics::PPhysicsMesh &` | requires class descriptor `02E485D0` (`PPhysicsMesh`); template member: distinguishing operand | Interior anchor `00699FDE` (`lea`, entry + 0x4E) |
| `0069A0B0` | `PPhysics::PPhysicsMeshBase &` | requires class descriptor `02E484D0` (`PPhysicsMeshBase`); template member: distinguishing operand | Interior anchor `0069A0FE` (`lea`, entry + 0x4E) |
| `0069A1D0` | `PPhysics::PPhysicsMeshBullet &` | requires class descriptor `02E499D0` (`PPhysicsMeshBullet`); template member: distinguishing operand | Interior anchor `0069A21E` (`lea`, entry + 0x4E) |
| `0069A2F0` | `PPhysics::PPhysicsModel &` | requires class descriptor `02E486D0` (`PPhysicsModel`); template member: distinguishing operand | Interior anchor `0069A329` (`lea`, entry + 0x39) |
| `0069A3F0` | `PPhysics::PPhysicsPlane &` | requires class descriptor `02E488D0` (`PPhysicsPlane`); template member: distinguishing operand | Interior anchor `0069A43E` (`lea`, entry + 0x4E) |
| `0069A510` | `PPhysics::PPhysicsPlaneBase &` | requires class descriptor `02E487D0` (`PPhysicsPlaneBase`); template member: distinguishing operand | Interior anchor `0069A55E` (`lea`, entry + 0x4E) |
| `0069A630` | `PPhysics::PPhysicsPlaneBullet &` | requires class descriptor `02E49AD0` (`PPhysicsPlaneBullet`); template member: distinguishing operand | Interior anchor `0069A67E` (`lea`, entry + 0x4E) |
| `0069A750` | `PPhysics::PPhysicsRigidBody &` | requires class descriptor `02E48BD0` (`PPhysicsRigidBody`); template member: distinguishing operand | Interior anchor `0069A789` (`lea`, entry + 0x39) |
| `0069A850` | `PPhysics::PPhysicsRigidBodyBase &` | requires class descriptor `02E489D0` (`PPhysicsRigidBodyBase`); template member: distinguishing operand | Interior anchor `0069A889` (`lea`, entry + 0x39) |
| `0069A950` | `PPhysics::PPhysicsRigidBodyBullet &` | requires class descriptor `02E49CD0` (`PPhysicsRigidBodyBullet`); template member: distinguishing operand | Interior anchor `0069A989` (`lea`, entry + 0x39) |
| `0069AA50` | `PPhysics::PPhysicsShape &` | requires class descriptor `02E48DD0` (`PPhysicsShape`); template member: distinguishing operand | Interior anchor `0069AA9E` (`lea`, entry + 0x4E) |
| `0069AB70` | `PPhysics::PPhysicsShapeBullet &` | requires class descriptor `02E495D0` (`PPhysicsShapeBullet`); template member: distinguishing operand | Interior anchor `0069ABBE` (`lea`, entry + 0x4E) |
| `0069AC90` | `PPhysics::PPhysicsSphere &` | requires class descriptor `02E48FD0` (`PPhysicsSphere`); template member: distinguishing operand | Interior anchor `0069ACDE` (`lea`, entry + 0x4E) |
| `0069ADB0` | `PPhysics::PPhysicsSphereBase &` | requires class descriptor `02E48ED0` (`PPhysicsSphereBase`); template member: distinguishing operand | Interior anchor `0069ADFE` (`lea`, entry + 0x4E) |
| `0069AED0` | `PPhysics::PPhysicsSphereBullet &` | requires class descriptor `02E49BD0` (`PPhysicsSphereBullet`); template member: distinguishing operand | Interior anchor `0069AF1E` (`lea`, entry + 0x4E) |
| `0069AFF0` | `PPhysics::PPhysicsTaperedCapsule &` | requires class descriptor `02E490D0` (`PPhysicsTaperedCapsule`); template member: distinguishing operand | Interior anchor `0069B03E` (`lea`, entry + 0x4E) |
| `0069B110` | `PPhysics::PPhysicsTaperedCylinder &` | requires class descriptor `02E491D0` (`PPhysicsTaperedCylinder`); template member: distinguishing operand | Interior anchor `0069B15E` (`lea`, entry + 0x4E) |
| `0069B230` | `PPhysics::PPhysicsWorld &` | requires class descriptor `02E494D0` (`PPhysicsWorld`); template member: distinguishing operand | Interior anchor `0069B269` (`lea`, entry + 0x39) |
| `0069B330` | `PPhysics::PPhysicsWorldBase &` | requires class descriptor `02E492D0` (`PPhysicsWorldBase`); template member: distinguishing operand | Interior anchor `0069B369` (`lea`, entry + 0x39) |
| `0069B430` | `PPhysics::PPhysicsWorldBullet &` | requires class descriptor `02E49DD0` (`PPhysicsWorldBullet`); template member: distinguishing operand | Interior anchor `0069B469` (`lea`, entry + 0x39) |
| `0069B530` | `PPhysics::PRaycastResult &` | requires class descriptor `02E493D0` (`PRaycastResult`); template member: distinguishing operand | Interior anchor `0069B569` (`lea`, entry + 0x39) |
| `0069B770` | `PPhysics::PPhysicsBox *` | requires class descriptor `02E479D0` (`PPhysicsBox`); template member: distinguishing operand | Interior anchor `0069B7B6` (`lea`, entry + 0x46) |
| `0069B8A0` | `PPhysics::PPhysicsBoxBase *` | requires class descriptor `02E478D0` (`PPhysicsBoxBase`); template member: distinguishing operand | Interior anchor `0069B8E6` (`lea`, entry + 0x46) |
| `0069B9D0` | `PPhysics::PPhysicsBoxBullet *` | requires class descriptor `02E496D0` (`PPhysicsBoxBullet`); template member: distinguishing operand | Interior anchor `0069BA16` (`lea`, entry + 0x46) |
| `0069BB00` | `PPhysics::PPhysicsCallbackData *` | requires class descriptor `02E48AD0` (`PPhysicsCallbackData`); template member: distinguishing operand | Interior anchor `0069BB42` (`lea`, entry + 0x42) |
| `0069BC30` | `PPhysics::PPhysicsCapsule *` | requires class descriptor `02E47BD0` (`PPhysicsCapsule`); template member: distinguishing operand | Interior anchor `0069BC76` (`lea`, entry + 0x46) |
| `0069BD60` | `PPhysics::PPhysicsCapsuleBase *` | requires class descriptor `02E47AD0` (`PPhysicsCapsuleBase`); template member: distinguishing operand | Interior anchor `0069BDA6` (`lea`, entry + 0x46) |
| `0069BE90` | `PPhysics::PPhysicsCapsuleBullet *` | requires class descriptor `02E497D0` (`PPhysicsCapsuleBullet`); template member: distinguishing operand | Interior anchor `0069BED6` (`lea`, entry + 0x46) |
| `0069BFC0` | `PPhysics::PPhysicsCharacterCamera *` | requires class descriptor `02E47CD0` (`PPhysicsCharacterCamera`); template member: distinguishing operand | Interior anchor `0069C006` (`lea`, entry + 0x46) |
| `0069C0F0` | `PPhysics::PPhysicsCharacterController *` | requires class descriptor `02E47ED0` (`PPhysicsCharacterController`); template member: distinguishing operand | Interior anchor `0069C132` (`lea`, entry + 0x42) |
| `0069C220` | `PPhysics::PPhysicsCharacterControllerBase *` | requires class descriptor `02E47DD0` (`PPhysicsCharacterControllerBase`); template member: distinguishing operand | Interior anchor `0069C262` (`lea`, entry + 0x42) |
| `0069C350` | `PPhysics::PPhysicsCharacterControllerBullet *` | requires class descriptor `02E49FD0` (`PPhysicsCharacterControllerBullet`); template member: distinguishing operand | Interior anchor `0069C392` (`lea`, entry + 0x42) |
| `0069C480` | `PPhysics::PPhysicsCylinder *` | requires class descriptor `02E480D0` (`PPhysicsCylinder`); template member: distinguishing operand | Interior anchor `0069C4C6` (`lea`, entry + 0x46) |
| `0069C5B0` | `PPhysics::PPhysicsCylinderBase *` | requires class descriptor `02E47FD0` (`PPhysicsCylinderBase`); template member: distinguishing operand | Interior anchor `0069C5F6` (`lea`, entry + 0x46) |
| `0069C6E0` | `PPhysics::PPhysicsCylinderBullet *` | requires class descriptor `02E498D0` (`PPhysicsCylinderBullet`); template member: distinguishing operand | Interior anchor `0069C726` (`lea`, entry + 0x46) |
| `0069C810` | `PPhysics::PPhysicsInterface *` | requires class descriptor `02E482D0` (`PPhysicsInterface`); template member: distinguishing operand | Interior anchor `0069C856` (`lea`, entry + 0x46) |
| `0069C940` | `PPhysics::PPhysicsInterfaceBase *` | requires class descriptor `02E481D0` (`PPhysicsInterfaceBase`); template member: distinguishing operand | Interior anchor `0069C986` (`lea`, entry + 0x46) |
| `0069CA70` | `PPhysics::PPhysicsInterfaceBullet *` | requires class descriptor `02E49ED0` (`PPhysicsInterfaceBullet`); template member: distinguishing operand | Interior anchor `0069CAB6` (`lea`, entry + 0x46) |
| `0069CBA0` | `PPhysics::PPhysicsMaterial *` | requires class descriptor `02E483D0` (`PPhysicsMaterial`); template member: distinguishing operand | Interior anchor `0069CBE2` (`lea`, entry + 0x42) |
| `0069CCD0` | `PPhysics::PPhysicsMesh *` | requires class descriptor `02E485D0` (`PPhysicsMesh`); template member: distinguishing operand | Interior anchor `0069CD16` (`lea`, entry + 0x46) |
| `0069CE00` | `PPhysics::PPhysicsMeshBase *` | requires class descriptor `02E484D0` (`PPhysicsMeshBase`); template member: distinguishing operand | Interior anchor `0069CE46` (`lea`, entry + 0x46) |
| `0069CF30` | `PPhysics::PPhysicsMeshBullet *` | requires class descriptor `02E499D0` (`PPhysicsMeshBullet`); template member: distinguishing operand | Interior anchor `0069CF76` (`lea`, entry + 0x46) |
| `0069D060` | `PPhysics::PPhysicsModel *` | requires class descriptor `02E486D0` (`PPhysicsModel`); template member: distinguishing operand | Interior anchor `0069D0A2` (`lea`, entry + 0x42) |
| `0069D190` | `PPhysics::PPhysicsPlane *` | requires class descriptor `02E488D0` (`PPhysicsPlane`); template member: distinguishing operand | Interior anchor `0069D1D6` (`lea`, entry + 0x46) |
| `0069D2C0` | `PPhysics::PPhysicsPlaneBase *` | requires class descriptor `02E487D0` (`PPhysicsPlaneBase`); template member: distinguishing operand | Interior anchor `0069D306` (`lea`, entry + 0x46) |
| `0069D3F0` | `PPhysics::PPhysicsPlaneBullet *` | requires class descriptor `02E49AD0` (`PPhysicsPlaneBullet`); template member: distinguishing operand | Interior anchor `0069D436` (`lea`, entry + 0x46) |
| `0069D520` | `PPhysics::PPhysicsRigidBody *` | requires class descriptor `02E48BD0` (`PPhysicsRigidBody`); template member: distinguishing operand | Interior anchor `0069D562` (`lea`, entry + 0x42) |
| `0069D650` | `PPhysics::PPhysicsRigidBodyBase *` | requires class descriptor `02E489D0` (`PPhysicsRigidBodyBase`); template member: distinguishing operand | Interior anchor `0069D692` (`lea`, entry + 0x42) |
| `0069D780` | `PPhysics::PPhysicsRigidBodyBullet *` | requires class descriptor `02E49CD0` (`PPhysicsRigidBodyBullet`); template member: distinguishing operand | Interior anchor `0069D7C2` (`lea`, entry + 0x42) |
| `0069D8B0` | `PPhysics::PPhysicsShape *` | requires class descriptor `02E48DD0` (`PPhysicsShape`); template member: distinguishing operand | Interior anchor `0069D8F6` (`lea`, entry + 0x46) |
| `0069D9E0` | `PPhysics::PPhysicsShapeBase *` | requires class descriptor `02E48CD0` (`PPhysicsShapeBase`); template member: distinguishing operand | Interior anchor `0069DA26` (`lea`, entry + 0x46) |
| `0069DB10` | `PPhysics::PPhysicsShapeBullet *` | requires class descriptor `02E495D0` (`PPhysicsShapeBullet`); template member: distinguishing operand | Interior anchor `0069DB56` (`lea`, entry + 0x46) |
| `0069DC40` | `PPhysics::PPhysicsSphere *` | requires class descriptor `02E48FD0` (`PPhysicsSphere`); template member: distinguishing operand | Interior anchor `0069DC86` (`lea`, entry + 0x46) |
| `0069DD70` | `PPhysics::PPhysicsSphereBase *` | requires class descriptor `02E48ED0` (`PPhysicsSphereBase`); template member: distinguishing operand | Interior anchor `0069DDB6` (`lea`, entry + 0x46) |
| `0069DEA0` | `PPhysics::PPhysicsSphereBullet *` | requires class descriptor `02E49BD0` (`PPhysicsSphereBullet`); template member: distinguishing operand | Interior anchor `0069DEE6` (`lea`, entry + 0x46) |
| `0069DFD0` | `PPhysics::PPhysicsTaperedCapsule *` | requires class descriptor `02E490D0` (`PPhysicsTaperedCapsule`); template member: distinguishing operand | Interior anchor `0069E016` (`lea`, entry + 0x46) |
| `0069E100` | `PPhysics::PPhysicsTaperedCylinder *` | requires class descriptor `02E491D0` (`PPhysicsTaperedCylinder`); template member: distinguishing operand | Interior anchor `0069E146` (`lea`, entry + 0x46) |
| `0069E230` | `PPhysics::PPhysicsWorld *` | requires class descriptor `02E494D0` (`PPhysicsWorld`); template member: distinguishing operand | Interior anchor `0069E272` (`lea`, entry + 0x42) |
| `0069E360` | `PPhysics::PPhysicsWorldBase *` | requires class descriptor `02E492D0` (`PPhysicsWorldBase`); template member: distinguishing operand | Interior anchor `0069E3A2` (`lea`, entry + 0x42) |
| `0069E490` | `PPhysics::PPhysicsWorldBullet *` | requires class descriptor `02E49DD0` (`PPhysicsWorldBullet`); template member: distinguishing operand | Interior anchor `0069E4D2` (`lea`, entry + 0x42) |
| `0069E5C0` | `PPhysics::PRaycastResult *` | requires class descriptor `02E493D0` (`PRaycastResult`); template member: distinguishing operand | Interior anchor `0069E602` (`lea`, entry + 0x42) |
| `006A74B0` | `PString &` | requires class descriptor `02E4D630` (`PString`); template member: distinguishing operand | Interior anchor `006A74E9` (`lea`, entry + 0x39) |
| `006A75B0` | `PString *` | requires class descriptor `02E4D630` (`PString`); template member: distinguishing operand | Interior anchor `006A75F2` (`lea`, entry + 0x42) |
| `006A8920` | `PGameplay::PTrigger &` | requires class descriptor `02E4D940` (`PTrigger`); template member: distinguishing operand | Interior anchor `006A8959` (`lea`, entry + 0x39) |
| `006A8B60` | `PGameplay::PTrigger *` | requires class descriptor `02E4D940` (`PTrigger`); template member: distinguishing operand | Interior anchor `006A8BA2` (`lea`, entry + 0x42) |
| `006A99E0` | `PGameplay::PQuarryComponent &` | requires class descriptor `02E4E1E0` (`PQuarryComponent`); template member: distinguishing operand | Interior anchor `006A9A19` (`lea`, entry + 0x39) |
| `006A9AE0` | `PGameplay::PQuarryComponent *` | requires class descriptor `02E4E1E0` (`PQuarryComponent`); template member: distinguishing operand | Interior anchor `006A9B22` (`lea`, entry + 0x42) |
| `006AA050` | `PTypedObject *` | requires class descriptor `02E4E430` (`PTypedObject`); template member: distinguishing operand | Interior anchor `006AA092` (`lea`, entry + 0x42) |
| `006AAE00` | `PComponent &` | requires class descriptor `02E4E720` (`PComponent`); template member: distinguishing operand | Interior anchor `006AAE39` (`lea`, entry + 0x39) |
| `006AAF00` | `PComponent *` | requires class descriptor `02E4E720` (`PComponent`); template member: distinguishing operand | Interior anchor `006AAF42` (`lea`, entry + 0x42) |
| `006AC0D0` | `PEntity &` | requires class descriptor `02E4EAF0` (`PEntity`); template member: distinguishing operand | Interior anchor `006AC109` (`lea`, entry + 0x39) |
| `006AC1D0` | `PEntity *` | requires class descriptor `02E4EAF0` (`PEntity`); template member: distinguishing operand | Interior anchor `006AC212` (`lea`, entry + 0x42) |
| `006AD250` | `PCameraOrthographic &` | requires class descriptor `02E4F290` (`PCameraOrthographic`); template member: distinguishing operand | Interior anchor `006AD29E` (`lea`, entry + 0x4E) |
| `006AD370` | `PCameraOrthographic *` | requires class descriptor `02E4F290` (`PCameraOrthographic`); template member: distinguishing operand | Interior anchor `006AD3B6` (`lea`, entry + 0x46) |
| `006AD9D0` | `PCameraPerspective &` | requires class descriptor `02E4F710` (`PCameraPerspective`); template member: distinguishing operand | Interior anchor `006ADA1E` (`lea`, entry + 0x4E) |
| `006ADAF0` | `PCameraPerspective *` | requires class descriptor `02E4F710` (`PCameraPerspective`); template member: distinguishing operand | Interior anchor `006ADB36` (`lea`, entry + 0x46) |
| `006AEBC0` | `PInstancesComponent &` | requires class descriptor `02E4F900` (`PInstancesComponent`); template member: distinguishing operand | Interior anchor `006AEBF9` (`lea`, entry + 0x39) |
| `006AEE00` | `PInstancesComponent *` | requires class descriptor `02E4F900` (`PInstancesComponent`); template member: distinguishing operand | Interior anchor `006AEE42` (`lea`, entry + 0x42) |
| `006AEF30` | `PClassDescriptor const *` | requires class descriptor `02CF8470` (`PClassDescriptor`); template member: distinguishing operand | Interior anchor `006AEF76` (`lea`, entry + 0x46) |
| `006AFF70` | `PNameComponent *` | requires class descriptor `02E4FF60` (`PNameComponent`); template member: distinguishing operand | Interior anchor `006AFFB2` (`lea`, entry + 0x42) |
| `006B0630` | `PRandom::PRandomGenerator *` | requires class descriptor `02E50160` (`PRandomGenerator`); template member: distinguishing operand | Interior anchor `006B0672` (`lea`, entry + 0x42) |
| `006B5050` | `PScene::PNode &` | requires class descriptor `02E518D0` (`PNode`); template member: distinguishing operand | Interior anchor `006B509E` (`lea`, entry + 0x4E) |
| `006B5170` | `PScene::PNode *` | requires class descriptor `02E518D0` (`PNode`); template member: distinguishing operand | Interior anchor `006B51B6` (`lea`, entry + 0x46) |
| `006B8AE0` | `PRendering::PMeshSegmentContext &` | requires class descriptor `02E522F0` (`PMeshSegmentContext`); template member: distinguishing operand | Interior anchor `006B8B19` (`lea`, entry + 0x39) |
| `006B8BE0` | `PRendering::PMeshSegmentContext *` | requires class descriptor `02E522F0` (`PMeshSegmentContext`); template member: distinguishing operand | Interior anchor `006B8C22` (`lea`, entry + 0x42) |
| `006BD910` | `PDynamicGeometry::PModifierNetworkDynamicMesh &` | requires class descriptor `02E58060` (`PModifierNetworkDynamicMesh`); template member: distinguishing operand | Interior anchor `006BD95E` (`lea`, entry + 0x4E) |
| `006BDA30` | `PDynamicGeometry::PModifierNetworkDynamicMeshSegment &` | requires class descriptor `02E57F60` (`PModifierNetworkDynamicMeshSegment`); template member: distinguishing operand | Interior anchor `006BDA69` (`lea`, entry + 0x39) |
| `006BDEF0` | `PDynamicGeometry::PModifierNetworkDynamicMesh *` | requires class descriptor `02E58060` (`PModifierNetworkDynamicMesh`); template member: distinguishing operand | Interior anchor `006BDF36` (`lea`, entry + 0x46) |
| `006BE020` | `PDynamicGeometry::PModifierNetworkDynamicMeshSegment *` | requires class descriptor `02E57F60` (`PModifierNetworkDynamicMeshSegment`); template member: distinguishing operand | Interior anchor `006BE062` (`lea`, entry + 0x42) |
| `006BFA10` | `PRendering::PLight &` | requires class descriptor `02E58DB0` (`PLight`); template member: distinguishing operand | Interior anchor `006BFA49` (`lea`, entry + 0x39) |
| `006BFB10` | `PRendering::PLight *` | requires class descriptor `02E58DB0` (`PLight`); template member: distinguishing operand | Interior anchor `006BFB52` (`lea`, entry + 0x42) |
| `006C1D60` | `PRendering::PShadowCaster &` | requires class descriptor `02E59DC0` (`PShadowCaster`); template member: distinguishing operand | Interior anchor `006C1D99` (`lea`, entry + 0x39) |
| `006C1E60` | `PRendering::PShadowCaster::PShadowSplit &` | requires class descriptor `02E59CC0` (`PShadowSplit`); template member: distinguishing operand | Interior anchor `006C1E99` (`lea`, entry + 0x39) |
| `006C20A0` | `PRendering::PShadowCaster *` | requires class descriptor `02E59DC0` (`PShadowCaster`); template member: distinguishing operand | Interior anchor `006C20E2` (`lea`, entry + 0x42) |
| `006C21D0` | `PRendering::PShadowCaster::PShadowSplit *` | requires class descriptor `02E59CC0` (`PShadowSplit`); template member: distinguishing operand | Interior anchor `006C2212` (`lea`, entry + 0x42) |
| `006C3C50` | `PDynamicGeometry::PModifierNetworkInstance &` | requires class descriptor `02E5A6C0` (`PModifierNetworkInstance`); template member: distinguishing operand | Interior anchor `006C3C89` (`lea`, entry + 0x39) |
| `006C3D50` | `PDynamicGeometry::PModifierNetworkInstanceInput &` | requires class descriptor `02E5A4C0` (`PModifierNetworkInstanceInput`); template member: distinguishing operand | Interior anchor `006C3D89` (`lea`, entry + 0x39) |
| `006C3E50` | `PDynamicGeometry::PModifierNetworkInstancePacketInput &` | requires class descriptor `02E5A5C0` (`PModifierNetworkInstancePacketInput`); template member: distinguishing operand | Interior anchor `006C3E89` (`lea`, entry + 0x39) |
| `006C4090` | `PDynamicGeometry::PModifierNetworkInstance *` | requires class descriptor `02E5A6C0` (`PModifierNetworkInstance`); template member: distinguishing operand | Interior anchor `006C40D2` (`lea`, entry + 0x42) |
| `006C41C0` | `PDynamicGeometry::PModifierNetworkInstanceInput *` | requires class descriptor `02E5A4C0` (`PModifierNetworkInstanceInput`); template member: distinguishing operand | Interior anchor `006C4202` (`lea`, entry + 0x42) |
| `006C42F0` | `PDynamicGeometry::PModifierNetworkInstancePacketInput *` | requires class descriptor `02E5A5C0` (`PModifierNetworkInstancePacketInput`); template member: distinguishing operand | Interior anchor `006C4332` (`lea`, entry + 0x42) |
| `006C6C60` | `PLOD::PLODGroup &` | requires class descriptor `02E5AE00` (`PLODGroup`); template member: distinguishing operand | Interior anchor `006C6C99` (`lea`, entry + 0x39) |
| `006C6D60` | `PLOD::PLODLevel &` | requires class descriptor `02E5AD00` (`PLODLevel`); template member: distinguishing operand | Interior anchor `006C6D99` (`lea`, entry + 0x39) |
| `006C70E0` | `PLOD::PLODGroup *` | requires class descriptor `02E5AE00` (`PLODGroup`); template member: distinguishing operand | Interior anchor `006C7122` (`lea`, entry + 0x42) |
| `006C7210` | `PLOD::PLODLevel *` | requires class descriptor `02E5AD00` (`PLODLevel`); template member: distinguishing operand | Interior anchor `006C7252` (`lea`, entry + 0x42) |
| `006C8520` | `POccluderGeometry::POccluderGeometryInstance *` | requires class descriptor `02E5BBB0` (`POccluderGeometryInstance`); template member: distinguishing operand | Interior anchor `006C8562` (`lea`, entry + 0x42) |
| `006CD140` | `PGameplay::PScriptableComponent *` | requires class descriptor `02E5C050` (`PScriptableComponent`); template member: distinguishing operand | Interior anchor `006CD186` (`lea`, entry + 0x46) |
| `006CDC00` | `PGameplay::PTriggerReceiverTypeCallbackData *` | requires class descriptor `02E5C370` (`PTriggerReceiverTypeCallbackData`); template member: distinguishing operand | Interior anchor `006CDC42` (`lea`, entry + 0x42) |
| `006CE340` | `PGameplay::PTriggerReceiverComponent &` | requires class descriptor `02E5C710` (`PTriggerReceiverComponent`); template member: distinguishing operand | Interior anchor `006CE379` (`lea`, entry + 0x39) |
| `006CE440` | `PGameplay::PTriggerReceiverComponent *` | requires class descriptor `02E5C710` (`PTriggerReceiverComponent`); template member: distinguishing operand | Interior anchor `006CE482` (`lea`, entry + 0x42) |
| `006D3680` | `PDynamicGeometry::PModifierAndInputs &` | requires class descriptor `02E5E030` (`PModifierAndInputs`); template member: distinguishing operand | Interior anchor `006D36B9` (`lea`, entry + 0x39) |
| `006D3780` | `PDynamicGeometry::PModifierNetwork &` | requires class descriptor `02E5E540` (`PModifierNetwork`); template member: distinguishing operand | Interior anchor `006D37B9` (`lea`, entry + 0x39) |
| `006D3880` | `PDynamicGeometry::PModifierNetworkBuffer &` | requires class descriptor `02E5DF30` (`PModifierNetworkBuffer`); template member: distinguishing operand | Interior anchor `006D38B9` (`lea`, entry + 0x39) |
| `006D3980` | `PDynamicGeometry::PModifierNetworkInfoPacket_Buffer &` | requires class descriptor `02E5E330` (`PModifierNetworkInfoPacket_Buffer`); template member: distinguishing operand | Interior anchor `006D39B9` (`lea`, entry + 0x39) |
| `006D3A80` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode &` | requires class descriptor `02E5E130` (`PModifierNetworkInfoPacket_ModifierCode`); template member: distinguishing operand | Interior anchor `006D3AB9` (`lea`, entry + 0x39) |
| `006D3B80` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance &` | requires class descriptor `02E5E230` (`PModifierNetworkInfoPacket_ModifierInstance`); template member: distinguishing operand | Interior anchor `006D3BB9` (`lea`, entry + 0x39) |
| `006D3C80` | `PDynamicGeometry::PRenderStream &` | requires class descriptor `02E5DE30` (`PRenderStream`); template member: distinguishing operand | Interior anchor `006D3CB9` (`lea`, entry + 0x39) |
| `006D3D80` | `PDynamicGeometry::PRenderStreamInput &` | requires class descriptor `02E5DD30` (`PRenderStreamInput`); template member: distinguishing operand | Interior anchor `006D3DB9` (`lea`, entry + 0x39) |
| `006D4240` | `PDynamicGeometry::PModifierAndInputs *` | requires class descriptor `02E5E030` (`PModifierAndInputs`); template member: distinguishing operand | Interior anchor `006D4282` (`lea`, entry + 0x42) |
| `006D4370` | `PDynamicGeometry::PModifierNetwork *` | requires class descriptor `02E5E540` (`PModifierNetwork`); template member: distinguishing operand | Interior anchor `006D43B2` (`lea`, entry + 0x42) |
| `006D44A0` | `PDynamicGeometry::PModifierNetworkBuffer *` | requires class descriptor `02E5DF30` (`PModifierNetworkBuffer`); template member: distinguishing operand | Interior anchor `006D44E2` (`lea`, entry + 0x42) |
| `006D45D0` | `PDynamicGeometry::PModifierNetworkInfoPacket *` | requires class descriptor `02E5E430` (`PModifierNetworkInfoPacket`); template member: distinguishing operand | Interior anchor `006D4612` (`lea`, entry + 0x42) |
| `006D4700` | `PDynamicGeometry::PModifierNetworkInfoPacket_Buffer *` | requires class descriptor `02E5E330` (`PModifierNetworkInfoPacket_Buffer`); template member: distinguishing operand | Interior anchor `006D4742` (`lea`, entry + 0x42) |
| `006D4830` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierCode *` | requires class descriptor `02E5E130` (`PModifierNetworkInfoPacket_ModifierCode`); template member: distinguishing operand | Interior anchor `006D4872` (`lea`, entry + 0x42) |
| `006D4960` | `PDynamicGeometry::PModifierNetworkInfoPacket_ModifierInstance *` | requires class descriptor `02E5E230` (`PModifierNetworkInfoPacket_ModifierInstance`); template member: distinguishing operand | Interior anchor `006D49A2` (`lea`, entry + 0x42) |
| `006D4A90` | `PDynamicGeometry::PRenderStream *` | requires class descriptor `02E5DE30` (`PRenderStream`); template member: distinguishing operand | Interior anchor `006D4AD2` (`lea`, entry + 0x42) |
| `006D4BC0` | `PDynamicGeometry::PRenderStreamInput *` | requires class descriptor `02E5DD30` (`PRenderStreamInput`); template member: distinguishing operand | Interior anchor `006D4C02` (`lea`, entry + 0x42) |
| `006D8FD0` | `PDynamicGeometry::PMorphModifierWeightsUserDataObject &` | requires class descriptor `02E9FDF0` (`PMorphModifierWeightsUserDataObject`); template member: distinguishing operand | Interior anchor `006D9009` (`lea`, entry + 0x39) |
| `006D90D0` | `PDynamicGeometry::PMorphModifierWeightsUserDataObject *` | requires class descriptor `02E9FDF0` (`PMorphModifierWeightsUserDataObject`); template member: distinguishing operand | Interior anchor `006D9112` (`lea`, entry + 0x42) |
| `006DA250` | `POccluderGeometry::POccluderGeometryObject *` | requires class descriptor `02EA0850` (`POccluderGeometryObject`); template member: distinguishing operand | Interior anchor `006DA292` (`lea`, entry + 0x42) |
| `00796640` | `PCameraProjection &` | requires class descriptor `02D3F310` (`PCameraProjection`); template member: distinguishing operand | Interior anchor `0079668E` (`lea`, entry + 0x4E) |
| `00796760` | `PFramework::PDebugUtils &` | requires class descriptor `02EA9400` (`PDebugUtils`); template member: distinguishing operand | Interior anchor `00796799` (`lea`, entry + 0x39) |
| `00796860` | `PFramework::PInputMapper &` | requires class descriptor `02EA5560` (`PInputMapper`); template member: distinguishing operand | Interior anchor `00796899` (`lea`, entry + 0x39) |
| `00796960` | `PFramework::PApplication *` | requires class descriptor `02EA5660` (`PApplication`); template member: distinguishing operand | Interior anchor `007969A6` (`lea`, entry + 0x46) |
| `00796A90` | `PFramework::PApplicationViewport *` | requires class descriptor `02EA5380` (`PApplicationViewport`); template member: distinguishing operand | Interior anchor `00796AD6` (`lea`, entry + 0x46) |
| `00796BC0` | `PFramework::PDebugUtils *` | requires class descriptor `02EA9400` (`PDebugUtils`); template member: distinguishing operand | Interior anchor `00796C02` (`lea`, entry + 0x42) |
| `00796CF0` | `PFramework::PInputMapper *` | requires class descriptor `02EA5560` (`PInputMapper`); template member: distinguishing operand | Interior anchor `00796D32` (`lea`, entry + 0x42) |
| `0086ED10` | `PInputs::PInputAction &` | requires class descriptor `02EB6CF0` (`PInputAction`); template member: distinguishing operand | Interior anchor `0086ED5E` (`lea`, entry + 0x4E) |
| `0086EE30` | `PInputs::PInputMap &` | requires class descriptor `02EB6DF0` (`PInputMap`); template member: distinguishing operand | Interior anchor `0086EE69` (`lea`, entry + 0x39) |
| `0086EF30` | `PInputs::PInputSourceJoypadAxis &` | requires class descriptor `02EB55F0` (`PInputSourceJoypadAxis`); template member: distinguishing operand | Interior anchor `0086EF7E` (`lea`, entry + 0x4E) |
| `0086F050` | `PInputs::PInputSourceJoypadButton &` | requires class descriptor `02EB54F0` (`PInputSourceJoypadButton`); template member: distinguishing operand | Interior anchor `0086F09E` (`lea`, entry + 0x4E) |
| `0086F170` | `PInputs::PInputSourceKey &` | requires class descriptor `02EB53F0` (`PInputSourceKey`); template member: distinguishing operand | Interior anchor `0086F1BE` (`lea`, entry + 0x4E) |
| `0086F290` | `PInputs::PInputSourceMotionAngularVelocityX &` | requires class descriptor `02EB63F0` (`PInputSourceMotionAngularVelocityX`); template member: distinguishing operand | Interior anchor `0086F2DE` (`lea`, entry + 0x4E) |
| `0086F3B0` | `PInputs::PInputSourceMotionAngularVelocityY &` | requires class descriptor `02EB64F0` (`PInputSourceMotionAngularVelocityY`); template member: distinguishing operand | Interior anchor `0086F3FE` (`lea`, entry + 0x4E) |
| `0086F4D0` | `PInputs::PInputSourceMotionAngularVelocityZ &` | requires class descriptor `02EB65F0` (`PInputSourceMotionAngularVelocityZ`); template member: distinguishing operand | Interior anchor `0086F51E` (`lea`, entry + 0x4E) |
| `0086F5F0` | `PInputs::PInputSourceMotionLinearAccelerationX &` | requires class descriptor `02EB66F0` (`PInputSourceMotionLinearAccelerationX`); template member: distinguishing operand | Interior anchor `0086F63E` (`lea`, entry + 0x4E) |
| `0086F710` | `PInputs::PInputSourceMotionLinearAccelerationY &` | requires class descriptor `02EB67F0` (`PInputSourceMotionLinearAccelerationY`); template member: distinguishing operand | Interior anchor `0086F75E` (`lea`, entry + 0x4E) |
| `0086F830` | `PInputs::PInputSourceMotionLinearAccelerationZ &` | requires class descriptor `02EB68F0` (`PInputSourceMotionLinearAccelerationZ`); template member: distinguishing operand | Interior anchor `0086F87E` (`lea`, entry + 0x4E) |
| `0086F950` | `PInputs::PInputSourceMotionQuatW &` | requires class descriptor `02EB62F0` (`PInputSourceMotionQuatW`); template member: distinguishing operand | Interior anchor `0086F99E` (`lea`, entry + 0x4E) |
| `0086FA70` | `PInputs::PInputSourceMotionQuatX &` | requires class descriptor `02EB5FF0` (`PInputSourceMotionQuatX`); template member: distinguishing operand | Interior anchor `0086FABE` (`lea`, entry + 0x4E) |
| `0086FB90` | `PInputs::PInputSourceMotionQuatY &` | requires class descriptor `02EB60F0` (`PInputSourceMotionQuatY`); template member: distinguishing operand | Interior anchor `0086FBDE` (`lea`, entry + 0x4E) |
| `0086FCB0` | `PInputs::PInputSourceMotionQuatZ &` | requires class descriptor `02EB61F0` (`PInputSourceMotionQuatZ`); template member: distinguishing operand | Interior anchor `0086FCFE` (`lea`, entry + 0x4E) |
| `0086FDD0` | `PInputs::PInputSourceMouseButton &` | requires class descriptor `02EB56F0` (`PInputSourceMouseButton`); template member: distinguishing operand | Interior anchor `0086FE1E` (`lea`, entry + 0x4E) |
| `0086FEF0` | `PInputs::PInputSourceMouseDeltaX &` | requires class descriptor `02EB57F0` (`PInputSourceMouseDeltaX`); template member: distinguishing operand | Interior anchor `0086FF3E` (`lea`, entry + 0x4E) |
| `00870010` | `PInputs::PInputSourceMouseDeltaY &` | requires class descriptor `02EB58F0` (`PInputSourceMouseDeltaY`); template member: distinguishing operand | Interior anchor `0087005E` (`lea`, entry + 0x4E) |
| `00870130` | `PInputs::PInputSourceTouchDragX &` | requires class descriptor `02EB5BF0` (`PInputSourceTouchDragX`); template member: distinguishing operand | Interior anchor `0087017E` (`lea`, entry + 0x4E) |
| `00870250` | `PInputs::PInputSourceTouchDragY &` | requires class descriptor `02EB5CF0` (`PInputSourceTouchDragY`); template member: distinguishing operand | Interior anchor `0087029E` (`lea`, entry + 0x4E) |
| `00870370` | `PInputs::PInputSourceTouchPinch &` | requires class descriptor `02EB5AF0` (`PInputSourceTouchPinch`); template member: distinguishing operand | Interior anchor `008703BE` (`lea`, entry + 0x4E) |
| `00870490` | `PInputs::PInputSourceTouchRotate &` | requires class descriptor `02EB59F0` (`PInputSourceTouchRotate`); template member: distinguishing operand | Interior anchor `008704DE` (`lea`, entry + 0x4E) |
| `008705B0` | `PInputs::PInputSourceTouchTwoFingerDragX &` | requires class descriptor `02EB5DF0` (`PInputSourceTouchTwoFingerDragX`); template member: distinguishing operand | Interior anchor `008705FE` (`lea`, entry + 0x4E) |
| `008706D0` | `PInputs::PInputSourceTouchTwoFingerDragY &` | requires class descriptor `02EB5EF0` (`PInputSourceTouchTwoFingerDragY`); template member: distinguishing operand | Interior anchor `0087071E` (`lea`, entry + 0x4E) |
| `008707F0` | `PInputs::PInputSourceVisionTrackerX &` | requires class descriptor `02EB69F0` (`PInputSourceVisionTrackerX`); template member: distinguishing operand | Interior anchor `0087083E` (`lea`, entry + 0x4E) |
| `00870910` | `PInputs::PInputSourceVisionTrackerY &` | requires class descriptor `02EB6AF0` (`PInputSourceVisionTrackerY`); template member: distinguishing operand | Interior anchor `0087095E` (`lea`, entry + 0x4E) |
| `00870A30` | `PInputs::PInputSourceVisionTrackerZ &` | requires class descriptor `02EB6BF0` (`PInputSourceVisionTrackerZ`); template member: distinguishing operand | Interior anchor `00870A7E` (`lea`, entry + 0x4E) |
| `00870DD0` | `PInputs::PInputAction *` | requires class descriptor `02EB6CF0` (`PInputAction`); template member: distinguishing operand | Interior anchor `00870E16` (`lea`, entry + 0x46) |
| `00870F00` | `PInputs::PInputMap *` | requires class descriptor `02EB6DF0` (`PInputMap`); template member: distinguishing operand | Interior anchor `00870F42` (`lea`, entry + 0x42) |
| `00871030` | `PInputs::PInputSource *` | requires class descriptor `02EB52F0` (`PInputSource`); template member: distinguishing operand | Interior anchor `00871076` (`lea`, entry + 0x46) |
| `00871160` | `PInputs::PInputSourceJoypadAxis *` | requires class descriptor `02EB55F0` (`PInputSourceJoypadAxis`); template member: distinguishing operand | Interior anchor `008711A6` (`lea`, entry + 0x46) |
| `00871290` | `PInputs::PInputSourceJoypadButton *` | requires class descriptor `02EB54F0` (`PInputSourceJoypadButton`); template member: distinguishing operand | Interior anchor `008712D6` (`lea`, entry + 0x46) |
| `008713C0` | `PInputs::PInputSourceKey *` | requires class descriptor `02EB53F0` (`PInputSourceKey`); template member: distinguishing operand | Interior anchor `00871406` (`lea`, entry + 0x46) |
| `008714F0` | `PInputs::PInputSourceMotionAngularVelocityX *` | requires class descriptor `02EB63F0` (`PInputSourceMotionAngularVelocityX`); template member: distinguishing operand | Interior anchor `00871536` (`lea`, entry + 0x46) |
| `00871620` | `PInputs::PInputSourceMotionAngularVelocityY *` | requires class descriptor `02EB64F0` (`PInputSourceMotionAngularVelocityY`); template member: distinguishing operand | Interior anchor `00871666` (`lea`, entry + 0x46) |
| `00871750` | `PInputs::PInputSourceMotionAngularVelocityZ *` | requires class descriptor `02EB65F0` (`PInputSourceMotionAngularVelocityZ`); template member: distinguishing operand | Interior anchor `00871796` (`lea`, entry + 0x46) |
| `00871880` | `PInputs::PInputSourceMotionLinearAccelerationX *` | requires class descriptor `02EB66F0` (`PInputSourceMotionLinearAccelerationX`); template member: distinguishing operand | Interior anchor `008718C6` (`lea`, entry + 0x46) |
| `008719B0` | `PInputs::PInputSourceMotionLinearAccelerationY *` | requires class descriptor `02EB67F0` (`PInputSourceMotionLinearAccelerationY`); template member: distinguishing operand | Interior anchor `008719F6` (`lea`, entry + 0x46) |
| `00871AE0` | `PInputs::PInputSourceMotionLinearAccelerationZ *` | requires class descriptor `02EB68F0` (`PInputSourceMotionLinearAccelerationZ`); template member: distinguishing operand | Interior anchor `00871B26` (`lea`, entry + 0x46) |
| `00871C10` | `PInputs::PInputSourceMotionQuatW *` | requires class descriptor `02EB62F0` (`PInputSourceMotionQuatW`); template member: distinguishing operand | Interior anchor `00871C56` (`lea`, entry + 0x46) |
| `00871D40` | `PInputs::PInputSourceMotionQuatX *` | requires class descriptor `02EB5FF0` (`PInputSourceMotionQuatX`); template member: distinguishing operand | Interior anchor `00871D86` (`lea`, entry + 0x46) |
| `00871E70` | `PInputs::PInputSourceMotionQuatY *` | requires class descriptor `02EB60F0` (`PInputSourceMotionQuatY`); template member: distinguishing operand | Interior anchor `00871EB6` (`lea`, entry + 0x46) |
| `00871FA0` | `PInputs::PInputSourceMotionQuatZ *` | requires class descriptor `02EB61F0` (`PInputSourceMotionQuatZ`); template member: distinguishing operand | Interior anchor `00871FE6` (`lea`, entry + 0x46) |
| `008720D0` | `PInputs::PInputSourceMouseButton *` | requires class descriptor `02EB56F0` (`PInputSourceMouseButton`); template member: distinguishing operand | Interior anchor `00872116` (`lea`, entry + 0x46) |
| `00872200` | `PInputs::PInputSourceMouseDeltaX *` | requires class descriptor `02EB57F0` (`PInputSourceMouseDeltaX`); template member: distinguishing operand | Interior anchor `00872246` (`lea`, entry + 0x46) |
| `00872330` | `PInputs::PInputSourceMouseDeltaY *` | requires class descriptor `02EB58F0` (`PInputSourceMouseDeltaY`); template member: distinguishing operand | Interior anchor `00872376` (`lea`, entry + 0x46) |
| `00872460` | `PInputs::PInputSourceTouchDragX *` | requires class descriptor `02EB5BF0` (`PInputSourceTouchDragX`); template member: distinguishing operand | Interior anchor `008724A6` (`lea`, entry + 0x46) |
| `00872590` | `PInputs::PInputSourceTouchDragY *` | requires class descriptor `02EB5CF0` (`PInputSourceTouchDragY`); template member: distinguishing operand | Interior anchor `008725D6` (`lea`, entry + 0x46) |
| `008726C0` | `PInputs::PInputSourceTouchPinch *` | requires class descriptor `02EB5AF0` (`PInputSourceTouchPinch`); template member: distinguishing operand | Interior anchor `00872706` (`lea`, entry + 0x46) |
| `008727F0` | `PInputs::PInputSourceTouchRotate *` | requires class descriptor `02EB59F0` (`PInputSourceTouchRotate`); template member: distinguishing operand | Interior anchor `00872836` (`lea`, entry + 0x46) |
| `00872920` | `PInputs::PInputSourceTouchTwoFingerDragX *` | requires class descriptor `02EB5DF0` (`PInputSourceTouchTwoFingerDragX`); template member: distinguishing operand | Interior anchor `00872966` (`lea`, entry + 0x46) |
| `00872A50` | `PInputs::PInputSourceTouchTwoFingerDragY *` | requires class descriptor `02EB5EF0` (`PInputSourceTouchTwoFingerDragY`); template member: distinguishing operand | Interior anchor `00872A96` (`lea`, entry + 0x46) |
| `00872B80` | `PInputs::PInputSourceVisionTrackerX *` | requires class descriptor `02EB69F0` (`PInputSourceVisionTrackerX`); template member: distinguishing operand | Interior anchor `00872BC6` (`lea`, entry + 0x46) |
| `00872CB0` | `PInputs::PInputSourceVisionTrackerY *` | requires class descriptor `02EB6AF0` (`PInputSourceVisionTrackerY`); template member: distinguishing operand | Interior anchor `00872CF6` (`lea`, entry + 0x46) |
| `00872DE0` | `PInputs::PInputSourceVisionTrackerZ *` | requires class descriptor `02EB6BF0` (`PInputSourceVisionTrackerZ`); template member: distinguishing operand | Interior anchor `00872E26` (`lea`, entry + 0x46) |
| `00874DA0` | `PVision::PVisionMoveTracker &` | requires class descriptor `02EB7CD0` (`PVisionMoveTracker`); template member: distinguishing operand | Interior anchor `00874DD9` (`lea`, entry + 0x39) |
| `00874EA0` | `PVision::PVisionMoveTracker *` | requires class descriptor `02EB7CD0` (`PVisionMoveTracker`); template member: distinguishing operand | Interior anchor `00874EE2` (`lea`, entry + 0x42) |
| `00874FD0` | `PVision::PVisionMoveTrackerBase *` | requires class descriptor `02EB7BD0` (`PVisionMoveTrackerBase`); template member: distinguishing operand | Interior anchor `00875012` (`lea`, entry + 0x42) |
| `00875100` | `PVision::PVisionMoveTrackerWin32 *` | requires class descriptor `02EB7DD0` (`PVisionMoveTrackerWin32`); template member: distinguishing operand | Interior anchor `00875142` (`lea`, entry + 0x42) |
| `00875980` | `PVision::PVisionTracker &` | requires class descriptor `02EB8060` (`PVisionTracker`); template member: distinguishing operand | Interior anchor `008759B9` (`lea`, entry + 0x39) |
| `00875A80` | `PVision::PVisionTracker *` | requires class descriptor `02EB8060` (`PVisionTracker`); template member: distinguishing operand | Interior anchor `00875AC2` (`lea`, entry + 0x42) |
| `00875BB0` | `PVision::PVisionTrackerBase *` | requires class descriptor `02EB7F60` (`PVisionTrackerBase`); template member: distinguishing operand | Interior anchor `00875BF2` (`lea`, entry + 0x42) |
| `00875CE0` | `PVision::PVisionTrackerWin32 *` | requires class descriptor `02EB8160` (`PVisionTrackerWin32`); template member: distinguishing operand | Interior anchor `00875D22` (`lea`, entry + 0x42) |
| `00878C70` | `PHierarchy::POctree *` | requires class descriptor `02EB9070` (`POctree`); template member: distinguishing operand | Interior anchor `00878CB2` (`lea`, entry + 0x42) |
| `00878DA0` | `PHierarchy::POctreeChildren *` | requires class descriptor `02EB9370` (`POctreeChildren`); template member: distinguishing operand | Interior anchor `00878DE2` (`lea`, entry + 0x42) |
| `00878ED0` | `PHierarchy::POctreeData *` | requires class descriptor `02EB9170` (`POctreeData`); template member: distinguishing operand | Interior anchor `00878F12` (`lea`, entry + 0x42) |
| `00879000` | `PHierarchy::POctreeWorld *` | requires class descriptor `02EB9270` (`POctreeWorld`); template member: distinguishing operand | Interior anchor `00879042` (`lea`, entry + 0x42) |
| `0087A310` | `PGame::PGameConfig &` | requires class descriptor `02EB9E60` (`PGameConfig`); template member: distinguishing operand | Interior anchor `0087A349` (`lea`, entry + 0x39) |
| `0087A550` | `PGame::PGameConfig *` | requires class descriptor `02EB9E60` (`PGameConfig`); template member: distinguishing operand | Interior anchor `0087A592` (`lea`, entry + 0x42) |
