# V121 GN — INPUTGAMEPLAY UI REQUEST MAPPING — SUPERSEDING ADDENDUM — 2026-09-01

**Status:** READ_ONLY_ANALYSIS_ONLY / NOT_APPLIED / NOT_PERSISTENCE_CERTIFIED  
**Project:** For Xeavin — FFXII_TZA GFZ/GZF V121 full-executable reconstruction  
**Secondary use:** XIIOnline local menu/input policy research  
**Supersedes request-map portions of:**  
`V121_GN_INPUTGAMEPLAY_UI_REQUEST_MAPPING_ADDENDUM_2026-09-01.md`

**Intended physical parent:** GM160 recovery-transfer GZF contained in the uploaded handoff ZIP  
**Authorized EXE SHA-256:** `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

## 0. Accounting fence

No GM160 GZF mutation is claimed.

Persistence-certified GM160 remains:

- functions: **38,161**
- explicit: **38,001**
- unresolved: **160**
- coverage: **99.58072%**
- overlap: **0**

Current strong unresolved GN proposals remain:

1. `00313A00`  
   `InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

2. `002F7380`  
   `Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`

This addendum strengthens the six request identities projected by `00313A00` and records a complete direct-producer census for the still-unnamed request slots.

---

# 1. Exact `00313A00` projected request set

Existing complete-body evidence remains:

`00313A00`
→ row 2 of the shared gameplay capability/inhibition policy
→ `00254500`
→ native UI request inhibit mask.

The exact inhibited request IDs contributed by row 2 are:

**1, 2, 3, 5, 14, 21**

Previously closed:

- request 1 — Battle Menu open/request
- request 3 — field party-leader selection/change
- request 5 — field free-target actor cycle / target selection

This superseding pass closes request **2** strongly and distinguishes the evidence status of **14** from **21**.

---

# 2. Request 2 = Party Menu / Menu Screen

## 2.1 Exact Input trigger

Canonical:

`00253C70`
`InputGameplay_ArbitrateDigitalInputAndModalState`

The exact authorized body contains:

```text
CMP EBP, 0x1000
JNE ...
CMP R14D, EBP
JNE ...
TEST BL, R15B
JNE ...

XOR EDX, EDX
LEA ECX, [RDX + 2]
CALL 002E1B10
```

Therefore the exact native input path is:

**raw pad mask `0x1000`**
→ request ID **2**
→ parameter **0**
→ deferred UI request mailbox.

The same executable independently establishes the neighboring PS-style button masks:
- Circle/Cross in the configurable DecideButton pair;
- Square at `0x8000` in the Battle Menu path.

Thus `0x1000` is the Triangle position in this native pad-bit layout.

Independent published FFXII controls identify:

**Triangle = open/display Party Menu / Menu Screen.**

### Decision

**STRONG / PLAYER-FACING CLOSED**

Request:

**2 = Party Menu / Menu Screen open/request family**

Strong working name:

`UIRequest_PartyMenuOpen`

Do not yet assign friendly names to every request-2 parameter/submode.

---

# 3. Request-2 mailbox behavior

## `002E1B10`

Complete body:
- **85 bytes**
- SHA-256:
  `62a2fe4bf593914f631b602743053ee3ac6575a32cd864aba711fcd39da2a945`

Mechanism:
1. refuse if the deferred-request mailbox is unavailable/busy;
2. special-case request 2 against aggregate gameplay policy bit 0;
3. set deferred-request-present flag;
4. store request ID;
5. store parameter;
6. return success.

Request 2 therefore enters the same deferred native request system used by scripted/fullscreen-menu operations, while retaining one extra policy guard at mailbox insertion.

---

# 4. Request 2 is also the default fullscreen-menu request

## `002E0DA0`

Complete body:
- **104 bytes**
- SHA-256:
  `7869990c5a2e0d05e7e42bfe32346f41e338da19908cc9dc9f4aa8c781376a78`

It accepts a compact selector whose low 15 bits are interpreted as values `0..6`.

Exact translation:

| Compact fullscreen selector | Native request ID |
|---:|---:|
| 0 | 17 |
| 1 | 18 |
| 2 | 10 |
| 3 | 15 |
| 4 | 19 |
| 5 | 6 |
| 6 | 22 |
| other/default | **2** |

Bit `0x8000` is preserved into the returned request value.

This translator is called by:

## `002E1A60`

Complete body:
- **123 bytes**
- SHA-256:
  `d933ec03159ce46d2b0aa82bddf612b048408aa4b1d98ad51950c87f06a55f2d`

which:
- translates the fullscreen selector;
- derives a request parameter;
- writes the translated request to the same deferred mailbox.

---

# 5. Authored ScriptVM proof for the fullscreen-menu translator

The two-argument ScriptVM native:

**`0x048D openfullscreenmenu_48d`**

maps its BEGIN handler to:

## `003462D0`

- body: **81 bytes**
- SHA-256:
  `c03df66d175062ed135fb0b31a2dccd83b3177373a20178d2d376e52866fbae0`

The exact body:
1. obtains two VM operands;
2. passes them as selector + parameter to `002E1A60`;
3. continues native UI/script synchronization.

Thus the mapping:

`0..6 -> 17/18/10/15/19/6/22`
with default `2`

is specifically a:

**ScriptVM fullscreen-menu selector → native UI request ID**

translation.

This materially strengthens request 2 as the fullscreen/Party Menu root/default request.

The exact player-facing names of selector values 0..6 are not established by the current ff12-script catalog and remain numeric.

VM wrappers are authored-intent evidence only and are not recommended XIIOnline replay seams.

---

# 6. Parameterized request-2 family

Exact native request-2 producers observed include:

- Triangle input → parameter `0`;
- scripted/fullscreen translator default → parameter derived by caller;
- other native request-2 callsites use:
  - `0`
  - `0x21`
  - `0x40`
  - `0x41`
  - `0x42`
  - a dynamic value under field/story conditions.

The generic request callback has dedicated request-2 parameter branches.

Therefore:

**request 2 is a Party/Menu family, not one single immutable screen transition.**

Do not prematurely name:
- `0x21`
- `0x40`
- `0x41`
- `0x42`

as Status, Equip, License Board, Gambits, etc. without independent resource/state evidence.

---

# 7. Complete direct producer census

A complete direct CALL/JMP census against the exact authorized `.text` finds semantic transfers to the key request entry points.

## Direct `002E1B10` request-mailbox transfers

```text
00253D78
00253EE6
00253F44
00253F53
0035C81E
0035D750
0050DAC4  [tail-jump]
```

The first four and `0035D750` produce request 2 variants.

`0035C81E` produces request 11.

`0050DAC4` is the developer/debug arbitrary-ID bridge described below.

## Direct `002E1A60` fullscreen-selector transfers

```text
00346308
00347112
```

Both feed the exact `002E0DA0` selector→request translation above.

## Fixed deferred request

`002E1AE0` stores request **12** directly.

No ordinary hardcoded producer of request **14** or **21** appears in this direct request pipeline.

---

# 8. Developer arbitrary request hook — `debug_open_triangle_menu2`

## `0050DAB0`

Complete body:
- **25 bytes**
- SHA-256:
  `c26b8b8fff4b93dce875f6b4db00988d45ac52587a4a1b98c9bc479d5f109d25`

Exact body:
1. obtain one VM numeric value through `00267E10`;
2. zero the request parameter;
3. place the VM value in the request-ID argument;
4. tail-jump directly to `002E1B10`.

The bundled ff12-script call-map/crosswalk independently binds this function to native call:

**`0x2037 debug_open_triangle_menu2`**

Therefore the debug layer can submit an **arbitrary numeric Triangle-menu/UI request ID** through the ordinary deferred request mailbox.

This includes router-valid IDs 14 and 21.

The call-map metadata lists zero declared arguments for this debug verb, while the exact handler mechanically consumes a VM numeric value. The executable body is authoritative for the handler mechanics; the catalog name remains authored-intent evidence.

---

# 9. Related authored debug Triangle-menu namespace

The bundled ff12-script catalog independently includes:

- `0x202F debug_open_triangle_menu`
- `0x2030 debug_isopen_triangle_menu`
- `0x2037 debug_open_triangle_menu2`

This proves that the developer ScriptVM interface explicitly exposes a **Triangle-menu** namespace.

`0050DAB0` is the variant that mechanically injects a numeric request ID into the real native deferred request system.

This does **not** prove that every router ID is a normal retail Party Menu submenu.

It proves that the developer/debug layer can exercise those request slots through the Triangle-menu infrastructure.

---

# 10. Request 14 — valid persistent/fullscreen mode, but friendly identity unresolved

Request 14:
- is router-valid;
- uses generic scheduler `00280A00`;
- is inhibited by `00313A00` projection through policy bits 6 and/or 9;
- has no ordinary hardcoded request producer identified in the exact executable census;
- can be injected through `debug_open_triangle_menu2`.

There is one additional strong structural fact.

## Current fullscreen-mode translator — `002E0E30`

- body: **236 bytes**
- SHA-256:
  `467b1045946e400256c4e9069aacfe370736614355554d1a819b3aec087aa398`

It:
1. queries current fullscreen/UI mode through `0028F5F0`;
2. accepts current modes `0..19`;
3. maps them back into native request IDs.

For current mode **14**, it returns native request **14**.

Therefore request 14 is not merely a meaningless reserved number:

**it corresponds to a representable persistent/current fullscreen UI mode.**

However:
- no ordinary static retail producer was found;
- no authored screen/resource name has been recovered;
- the generic lifecycle has no request-14-specific branch.

### Decision

**KEEP NUMERIC, BUT STRUCTURALLY CLASSIFIED**

Strong description:

**request 14 = valid fullscreen UI mode/request slot 14; policy-controlled; no ordinary hardcoded producer identified; developer Triangle-menu injection supported.**

Do not guess its submenu name.

---

# 11. Request 21 — router-valid generic/transient slot, friendly identity unresolved

Request 21:
- is router-valid;
- uses generic scheduler `00280A00`;
- is inhibited by `00313A00` projection through policy bit 8;
- has no ordinary hardcoded producer identified in the exact executable census;
- can be injected through `debug_open_triangle_menu2`.

Unlike request 14:

`002E0E30`'s current-fullscreen-mode translator covers only current modes `0..19`.

There is no current fullscreen-mode 21 in that translator.

Therefore current evidence distinguishes request 21 from request 14:

**request 21 is a valid router request slot but is not represented as one of the current persistent fullscreen modes handled by `002E0E30`.**

It may represent:
- a transient UI operation;
- a special screen transition;
- a debug/data-driven operation;
- another non-persistent request type.

Current evidence does not choose among those possibilities.

### Decision

**KEEP NUMERIC**

Strong description:

**request 21 = policy-controlled generic UI request slot 21; no ordinary hardcoded producer identified; not represented in the current fullscreen-mode 0..19 translator; developer Triangle-menu injection supported.**

Do not invent a submenu name.

---

# 12. Updated six-request map

| Request ID | Strongest current identity | Confidence |
|---:|---|---|
| 1 | Battle Menu open/request | **PROVEN / STRONG** |
| 2 | Party Menu / Menu Screen open/request family | **STRONG / PLAYER-FACING CLOSED** |
| 3 | Field party-leader selection/change | **PROVEN / STRONG** |
| 5 | Field free-target actor cycle / target selection | **PROVEN / STRONG** |
| 14 | Fullscreen UI mode/request slot 14; no ordinary hardcoded producer found | **STRUCTURALLY PROVEN / NAME OPEN** |
| 21 | Generic/transient UI request slot 21; no ordinary hardcoded producer found | **STRUCTURALLY PROVEN / NAME OPEN** |

These are the exact six native requests inhibited by the `00313A00` row-2 contribution.

---

# 13. Revised semantic interpretation of `00313A00`

Current strong GN proposal remains:

`InputGameplay.FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation`

The row-2 policy is now known to suppress concrete player/UI capabilities including:

- Battle Menu;
- Party Menu / Menu Screen;
- party-leader change;
- free-target actor cycling;

plus two valid but still unnamed request slots:

- fullscreen mode/request 14;
- request 21.

This is stronger than an abstract control mask while still avoiding unsupported screen labels.

No V120 PrimaryOwner is inferred.

---

# 14. XIIOnline implications

## Party Menu

Request 2 itself is local UI policy, not shared-world authority.

Do not network:
- request-2 mailbox bits;
- request-2 generic UI object state;
- submode parameters as authoritative world state.

The underlying multiplayer-significant state inside Party Menu must be synchronized at its true owners:
- party composition;
- equipment;
- Gambits;
- licenses;
- inventory;
- settings policy where relevant.

Local UI should consume those authoritative states.

## Scripted fullscreen menus

Authored `openfullscreenmenu_48d` proves that scripts can request specific fullscreen menu modes through the same native request architecture.

For XIIOnline cutscene/event work:
- script intent may request a local screen;
- do not network the VM wrapper;
- reproduce higher semantic event state and allow the local UI transition through a verified native owner when synchronization is actually needed.

## Requests 14/21

Do not build multiplayer behavior around guessed identities.

Treat them as local UI capability slots until stronger authored/resource evidence names them.

---

# 15. GFZ mutation gate remains unchanged

This request-map closure strengthens `00313A00` but does not authorize a persistence claim without the physical GM160 parent being imported.

Required later:
1. fresh-import the GM160 recovery GZF from the user-supplied handoff package;
2. reproduce exact 38,001 / 160 / snapshot / overlap / embedded EXE;
3. regenerate current residual;
4. require `00313A00` still unresolved with exact body SHA;
5. apply exact-current enrichment only;
6. whole-project immutable diff;
7. closed-file `PACK_PASS`;
8. independent fresh reopen;
9. regenerate post-GN residual.

Until then:

**applied GN rows = 0**

and certified GM160 remains:

**38,001 explicit / 160 unresolved / 99.58072% / overlap 0.**
