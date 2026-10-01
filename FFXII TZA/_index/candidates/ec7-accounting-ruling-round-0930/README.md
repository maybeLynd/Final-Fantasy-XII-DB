# The accounting-state ruling, points 2-4, and A-drift round 4 (SWE2-EC7, 2026-09-30)

*FABLE's ruling on `SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930`. Point 1, the Phyre application, ships as its own
commit with its own record (`ec7-phyre-uniform-0930`). This record covers points 2-4, the form-cluster pool fix, and the
A-drift round that came in while the work was under way. All figures are from a clean export of HEAD `e2cb21305`.*

## Point 4: the three library selectors now see UC-1 callers (SWE2-EC7)

`select_audio_libraries.py`, `select_ppfx.py` and `select_libvpx.py` used to remove the UC-1 bodies from the census
before attributing callers, so a call from a UC-1 body was invisible to their foreign-caller and closure tests. Now the
UC-1 bodies stay in the population, and the selectors filter them from the written members files only.
`select_audio_libraries.py`'s object-closure assertion judges a UC-1 body instead of asserting on it: a UC-1 body joined
by nothing simply does not qualify, which is the R1 finding for 15 libvorbis bodies.

**Delta: 0 bodies in every file** (SEAD 1,123, libogg 22, Tremor 102, CRI 53, libvorbis 116, bitwise 4, PPFX 1,601,
libvpx decoder 116 and kernels 63). With every inbound reference now visible, no selector reports a foreign caller.

## Point 3: another family's declaration no longer decides qualification (SWE2-EC7)

In `select_jsonbox.py`, `select_imgui.py`, `select_mkvparser.py`, `select_libvpx.py` and `select_msvc_runtime.py`, a body
another family declares now takes part in the predicate like any body. When it passes, it is a qualifying node. Its
ownership stays with the declaring family: it is removed from the output and printed as a collision. Two
declaration-based allowances were replaced by code identity:
- The convention-caller test in jsonbox and imgui accepted any declared caller. It now accepts callers by census tag,
  including a body tagged as the object's own code; ImGui's XC-registered static teardown `008B7D40` is one.
- In `select_msvc_runtime.py`, "forwarder/import thunk" was recognised by the family name of the referrer. It is now
  recognised from the bytes, as a stub of at most 8 bytes that is a `jmp rel32` or a `jmp [rip+x]`.

**Delta: 0 bodies.** Collisions reported, not moved:

| selector | predicate members owned by another family |
|---|---|
| jsonbox | `001FE990`, `001FEA00` (EH call wrappers), `002164D0` (PhyreCore) |
| msvc_runtime | `0016DE20`, `006DF610`, `007838B0`, `00809920`, `00809950` |
| imgui, mkvparser, libvpx | none |

Before the code-identity change, imgui's three bodies reached through `008B7D40` dropped out (10 -> 7). That
sensitivity is what the change fixes.

## Point 2: derived families (SWE2-EC7)

The rows for NativeAdapter.ExplainedCalleeForwarder and guarded class-registration stubs now say **DERIVED**. Their
membership is defined by accounting state, so it is computed last, as a fixed point after the identity families, and
it is never a closure or membership input for an identity family. After point 3, no identity selector reads any
family's membership as a predicate input. The ECF selector ran last in this package. **Derived movement, reported
separately and not as drift: ECF 483 -> 488** (+5 frontier adapters whose single callee is now explained:
`00270550`, `002D8C00`, `00332420`, `00380170`, `003C21B0`).

## Form-cluster selectors: each family draws only from its own pool (SWE2-EC7)

`select_frontier_form_clusters.py` and `_2/_3/_4.py` took candidates from the frontier plus every prior members file of
the script. A body that only another file listed, a body another family owns, and a UC-1 body could all be selected. In
the pass of `51bfb4c1a` that produced 15 would-be collisions: 11 ECF members, 2 DocumentedGlobalAccessor members and 2
UC-1 bodies. Each family's pool is now the frontier, less UC-1, plus its own prior members. A form match outside the
pool is printed and not taken. In this run that was `004223F0` and `002697F0` (UC-1). The restriction can only remove
candidates. Under ruling R3, the re-run then admits 6 frontier bodies and removes none:
- CallResultTailCall 61 -> 63 (`001E0E30`, `001E0E50`)
- CallResultWithSavedIntTailCall 31 -> 32 (`0017FA70`)
- FirstMemberPointerTailCall 12 -> 13 (`00562F30`)
- FixedPipelineCallResult 4 -> 5 (`002497B0`)
- GlobalOffsetTailCall 3 -> 4 (`0028E8B0`)

One file, `nativeadapter-callboolnormalizereturnsete.tsv`, has no declaring row; its three bodies are A. It is left as
it is.

**Order matters, and the first attempt got it wrong.** When the DocumentedGlobalAccessor row was refused, by A-drift or
by a count not yet updated, its 224 members counted as frontier, and the form selectors took them. The package
therefore runs in this order: exact A removals and row counts first, then the identity selectors, then the derived ones.

## A-drift round 4 (SWE2-EC7)

OPUS's `e2cb21305` moved the character render-record array page to DOCUMENTED. Two family members became A
([`pairing-round4.tsv`](pairing-round4.tsv)):
- **NativeLeaf.DocumentedGlobalAccessor 224 -> 230.** The selector drops `002E8700` (A). The same re-status makes the
  page cite seven more globals exactly, so the selector binds 7 frontier leaves: `00285F00`, `002CC9B0`, `00314960`,
  `0035D520`, `0037F050`, `0037F160`, `003BC2C0`. The count guard moves 224 -> 230.
- **NativeAdapter.CallThenTailCall 17 -> 16.** `003E0720` is A; the form selector drops exactly it.

## Figures (SWE2-EC7)

On a clean export of HEAD `e2cb21305`, F was **5,048**: 2 rows refused by round 4. With this package it is
**4,791**, with rows refused 0 and family forms MISMATCH 0.

run: all changed selectors re-run on a clean export of e2cb21305; each reproduces its committed file except where
this record states a delta.
