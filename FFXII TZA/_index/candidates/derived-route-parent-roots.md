# The nine derived-route parents: an honest root, or the reason there is none (OPUS, 2026-09-25)

Answers `FRONTIER-REQ-OPUS-NINE-DERIVED-ROUTES-NEED-PARENT-ROOTS`. **Rule applied, from the goal:
no FN or route is added merely to make a census runnable.** A route here must state where the
object provably IS; a parent whose only root is a form the grammar cannot express is recorded as
such. **Nothing is written to `_types/types.tsv`**: the worktree copy reverts 23 committed F-6
routes (`worktree-drift-2026-09-25/`), so no route edit can be published from it safely. These are
the determinations, for application once it is clean. Evidence class NATIVE/STATIC.

## Expressible now with an existing route kind

| parent | root | evidence |
|---|---|---|
| **PDeferredLightingBase** (0x41D8) | `VTABLE 0x00D61EA0` | the class's own RTTI vtable, from its Complete Object Locator (`.?AVPDeferredLightingBase@PPostProcessing@Phyre@@`); VTABLE's seed rule — `this` in `rcx` at every method entry — is exactly what a vtable slot guarantees. The derived `PDeferredLighting` vtable `00D61F40` is a second honest alternative for the base's extent. |
| **AuthoredTableHeader** (0x20) | `PTR` for each registrar-proven slot | `003845F0(slot, header)` stores `rdx` into `[rcx]` at `003845F4` and relocates the pointee's `+0x0C/+0x10/+0x18/+0x1C` as this shape, so **every slot passed to it holds an AuthoredTableHeader**. 42 call sites; 41 resolve `rcx` to a rip `lea` — **41 distinct slots, `02EBF008..02EBF150` (every qword in that run except `02EBF0D0`)**, 33 of them from `00236C30`. The 42nd (`0023864E`, in the forwarder `00238640`) takes the slot as an argument. Membership by the REGISTRAR, not by position in the band — which is what the row's "a positional scan mixes types" rightly refuses. 41 is a floor (rcx resolved within 12 instructions); the row's own figure is 47/35 and the difference is not adjudicated here. |

## A real root the grammar cannot state: an argument register at a named entry

| parent | root | evidence already on the row |
|---|---|---|
| **ActorDefinitionPayload** (≥0x4C) | `rdx` at `0026C8C0` (`ActorManager_BindLoadedDefinitionPayload`) | `0026C8F7 mov r15, rdx` keeps it, `0026C95A mov [rdi], rdx` stores it to ActorManagerSlot +0x00 (row's 2026-09-18 correction) |
| **AuthoredExpressionBlock** | `rcx` at `0042FDB0` | `0042FDC1 movzx ecx, byte ptr [rcx+0x40]`, four `call 004314E0` on `rcx+0x00..0x30` |
| **PaneListWidget0B68** (0xB68) | `rcx` at its handler `0029BE50` | the pool allocator's handler argument (`00296502`, handler in `rdx` at `002964F6`) — the kit's widget-admissibility rule; the census row reaches 376/376 instructions of it |

**Proposed grammar form (FRONTIER's to accept or refuse): `ARG <reg> 0xFUNC`** — "the object is
in `<reg>` at the entry of FUNC" — seeded exactly like one entry of `VTABLE`. Each use must cite
the instruction that proves the register, as the three rows above already do. Until it exists,
these three are **UNROUTABLE IN THE CURRENT GRAMMAR, root known**.

## Genuinely no single root: the Lua 5.2.1 heap objects

**LuaState, LuaProto, LuaTable** (and LuaGlobalState, reached as `lua_State+0x18`) are GC-heap
objects of a statically linked **Lua 5.2.1** (`members/lua.tsv`: 600 bodies `0080F2E0..00830760`,
unnamed in `functions.tsv`). Their root is "`lua_State*` is the first argument of the Lua API" —
spread over an unidentified subset of 600 bodies, not one entry. An `FN 0081ED30` (luaF_newproto)
or similar would be true provenance but would census only a constructor's callers: **that is the
route-to-make-a-census-run the goal forbids.** And for reconstruction the layouts come from the
pinned upstream headers (`lstate.h`, `lobject.h`), not from a census. **Disposition: UNROUTABLE BY
DESIGN — argument-rooted across a third-party API; layout authority is upstream Lua 5.2.1.**

## Result, if applied

2 parents gain a parseable root now (unblocking PDeferredLightingSlot0080 and AuthoredBlobFixupTable),
3 wait on one grammar form, 3 (+LuaGlobalState) are recorded as unroutable with the reason.
