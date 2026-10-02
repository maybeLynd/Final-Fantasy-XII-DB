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
  - "optional-pointer offset-add dispatch adapters, 64-byte form | C | members/optptr-offsetadd-dispatch-adapters.tsv | 8 | not this game's code: compiler- or template-generated - sibling spelling of the static-descriptor optional-pointer row above: rdx=[r8]+member displacement and r8=a member-specific record; non-null tail-jumps shared 00810620, else calls 0080F420 with edx=0x19 and tail-jumps a cloned forwarder (00684080 x6, 00684090 x2). PROVED BY FORM - 8 members, all 64 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x8 and 00810620 x8 shared, plus 00684080/00684090 shared - every member reaches exactly one of the two cloned thunks. NOT dispositioned: the shared implementations and the member records - this row disposes of the adapter, not the adapted. Selector: members/select_optptr_dispatch_siblings_2.py"
  - "optional-pointer member-call dispatch adapters, 75-byte form | C | members/optptr-membercall-dispatch-adapters.tsv | 8 | not this game's code: compiler- or template-generated - sibling spelling: rdi=[r8] saved, a member-specific op is called, and the non-null path tail-jumps shared 00810620 with rdx=rdi while the null path calls 0080F420 (edx=0x19) and tail-jumps a member-specific op. PROVED BY FORM - 8 members, all 75 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x8 and 00810620 x8 shared, plus member-specific ops (00684130 x2 subset-shared, 6 distinct others). NOT dispositioned: the shared implementations and the member-specific ops - this row disposes of the adapter, not the adapted. Selector: members/select_optptr_dispatch_siblings_2.py"
  - "optional-pointer member-call result-dispatch adapters, 78-byte form | C | members/optptr-membercall-resultdispatch-adapters.tsv | 6 | not this game's code: compiler- or template-generated - the 75-byte sibling plus one more move: the member call's result is forwarded in r8 to the true-path tail 00810620; the null path calls 0080F420 (edx=0x19) and tail-jumps the cloned forwarder 00684080. PROVED BY FORM - 6 members, all 78 bytes, ONE operand-aware byte image and ONE instruction-form skeleton. CONTROL: 0080F420 x6, 00810620 x6 and 00684080 x6 shared, plus member-specific ops (5 distinct). NOT dispositioned: the shared implementations and the member-specific ops. Selector: members/select_optptr_dispatch_siblings_2.py"
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
