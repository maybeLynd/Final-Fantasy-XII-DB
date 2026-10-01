# SD-7: 158 of the 192 `+0x78` dispatch sites cannot be on the application; 34 remain, typed by group (SWE2-ORACLE, 2026-09-30)

Register row SD-7 ([input-stack-device-channel-and-bindings.md](../../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md)
section 5) asks who calls `GameApplication` slot 15 (`0017D1A0`, the setter of the input manager's `+0x39` poll gate).

OPUS's record [`sd7-slot15-callers-0930`](../sd7-slot15-callers-0930/README.md) showed three things:
- no direct caller of `0017D1A0`;
- no image qword other than its vtable entry;
- none of the framework routes reaches it.

It left the image's 192 `call/jmp [vtable+0x78]` sites untyped: "game code calling through a stored application
pointer". This record types those sites.

**About the brief's example addresses.** `002E0D39` / `002E2257` are not `+0x78` dispatches. They are the two call
sites of `00229F00` (`mov [02064AD3], cl`), SD-8's dispatcher-mode setter (see `sd8-dispatcher-mode-0930`). The
question is carried by the 192 `+0x78` sites, which is what OPUS's record names.

**Evidence class: static only.** Every result below comes from the certified image:
- regval value sets (depth 3) of each site's object register;
- MSVC RTTI (complete-object locators and class hierarchy descriptors) read from the image;
- pinned instructions.

Nothing is executed and nothing is live.
- Checker: `sd7_app_pointer_sites.py`, output `sd7_app_pointer_sites.out`.
- Checks: K1-K5 and S1, `FAILS 0`.
- **Proposed status: NARROWED.** No site is shown to reach slot 15, and 34 are not excluded.

## Method (SWE2-ORACLE)

At each site `call [V+0x78]`, the checker finds `V`'s vtable load `mov V, [O]`, resolves `O`, and excludes the
application if any of four independent tests holds:

| test | rule | sites |
|---|---|---|
| **E1 displacement** | Every value of `O` is loaded from a displacement where the application pointer is never stored. OPUS's 26 escapes store it only at `+0x0`, `+0x8`, `+0x20`, `+0x38` and `+0x78` of their holders, plus the global `02EA5368`, the window data and the stack, and never through an index. Indexed loads also qualify, including the handle resolvers `007B58C0` / `007BC2B0` (`[table + i*40 + 0x20]`, K5), as does a constant 0. | **133** |
| **E2 class** | `O` is the incoming `this` of a method, and every vtable holding that method (RTTI) is a class outside `GameApplication`'s hierarchy {`GameApplication`, `PApplication`, `PBase`, `PMemoryBase`}. Examples are Bullet shapes and worlds, `PClassDescriptorHeader<…>`, `PrimitiveRendererD3D11` and `PPFX::IGPUDevice`. | **13** |
| **E3 constructed** | `O` is returned by a constructor that installs a non-application vtable: `001FBB40` → `DynGeo3DInstance`, `001FB870` → `DynGeoTextureInstance`. | **2** |
| **E4 slot range** | The same object, with `O` unchanged, is also dispatched at a slot of 31 or more (`+0xF8` and up). `GameApplication`'s vtable has 31 slots, so the object is not a `GameApplication`. | **10** |

**Controls.**
- **K1:** the census reproduces OPUS's 192 sites in 114 functions.
- **K2:** E1 does **not** exclude a known application call, the window procedure's `0079914C` (object `[02EA5368]`).
- **K3:** E2 types `0017D1A0`'s own `this` as `GameApplication` and does not exclude it.
- **K4:** the application's vtable is 31 slots long, and a real application call at slot 30 (`0079C23A`, `+0xF0`)
  exists. So E4's threshold lies above every slot the application answers.

## The 34 not excluded (by group) (SWE2-ORACLE)

| group | sites | what is known |
|---|---|---|
| Render-context argument (`rdx`) of `Gi*` / `DynGeoFont*` slot-1 draw methods | `002143E0`, `00214540`, `00862D40`, `00862EC0`, `008651A0` | Their sibling methods (`00213140`, `00213FE0`, `001FB8E0`, `00863850`, `00863D80`, `00864330`, `00864860`) call the same `rdx` object at `+0x100` to `+0x138`, so those siblings are excluded by E4. That these five receive the same object type is **inference**, from the shared method family and call sequence. |
| Bullet physics | `00831380`, `008330A0` (second site: no reload of the vtable register), `008420F0` ×2 | The first `008330A0` site, and 00837680's `this`, are Bullet classes (E2). The remaining terms are call returns and fields. |
| PPFX middleware (`006F`-`0078`) | `006F8740`, `0070CF00`, `0070CFA0`, `00736D60`, `007370A0`, `00738840`, `0073BD30`, `0073D370`, `0073DFA0`, `0073EA00` ×3, `0073F290`, `007407E0`, `0075D4E0` ×2, `0075DA10` ×2, `0077FFE0`, `0078EAF0` | These are loads at `+0x20`, `+0x38`, `+0x78` or `+0` (displacements that match application holders), or stack slots, which E1 never excludes. The only `+0x38` holder is `PApplicationScriptProxy` (vtable `01CB24B8`, built in `00792760` / `0079F150`). None of these bases is typed as one here. |
| Game code | `001F3AE0` (`[this]` of `001F3E10`, which has no vtable), `0020FF10` ×2 (global `01FC35F8`, written only by `00210320` from its `rdx`), `007AB5C0` (typed-handle dispatcher `007AB1E0`), `00855B80` (an indirect call's return) | Each needs its holder typed. `01FC35F8`'s writer `00210320` is the next read. |

## Limits (SWE2-ORACLE)

- **E1 is first-order.** It relies on OPUS's escape list, which comes from the bodies OPUS's census reached (5,859).
  If code outside that reach copied the application pointer to a new displacement, E1 would not see it. The PPFX and
  game-code groups above are where that residue lives.
- **E2** trusts the vtable-membership reading of RTTI. A method shared by identical-code folding across classes would
  list several classes, and every one of them must fall outside the hierarchy for the site to be excluded.
- **E4** assumes the vtable register still holds the same object's vtable between the load and the call. The region is
  cut at every write to the object register and at every call that clobbers a volatile vtable register.
- Static only. Nothing here shows that any site runs.

## For SWE2-DATA (row text proposal, not applied here) (SWE2-ORACLE)

SD-7 NARROWED (SWE2-ORACLE, static):
- Of the 192 `[vtable+0x78]` dispatch sites, 158 are excluded from the application:
  - 133 by holder displacement;
  - 13 by the RTTI class of `this`;
  - 2 by constructor vtable;
  - 10 because the same object answers slots of 31 and above, while `GameApplication` has 31.
- 34 remain: 5 render-context arguments (excluded by family inference only), 4 Bullet, 20 PPFX-middleware holder
  loads, and 5 game-code holders (`001F3AE0`, `0020FF10` ×2 via `01FC35F8`, `007AB5C0`, `00855B80`).
- No caller of slot 15 is found (record `sd7-stored-app-pointer-0930`).
- The brief's `002E0D39` / `002E2257` belong to SD-8's `00229F00`, not to SD-7.

**Review:** SWE2-AUDIT-SPEC (`ORACLE-REQ-AUDITSPEC-SD7-0930`). **Row:** SWE2-DATA (`ORACLE-REQ-DATA-SD7-ROW-0930`).
