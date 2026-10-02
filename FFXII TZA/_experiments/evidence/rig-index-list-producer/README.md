# Rig index list, borrowed core and relocation cache

## Result and method

Method A resolves the original producers for the skeleton reset's `+78` bone
core and `+88` configured-index-list reference. It also identifies rig `+84` as
a raw low-address cache, distinct from the render element's encoded `+84`.
No live game or isolated machine-code execution was necessary.

The local fixup distinguishes fresh binding, relocation and a repeated call
at the same low address. The reset reader uses an unsigned count and unsigned
indices without its own bone-count check. A separate nullable-lookup boundary
requires an explicit initialized-owner precondition. Actual lifetime, extent,
natural entry and native controller effects remain open.

For the player: the rig remembers where its copied data lives so it can adjust
references after a move. Its bone storage comes from another render record.
Correct initialization of that connection matters before a reset can run.

## Three fields, three meanings

`003E1C50` uses RDI as the rig pointer. When its initial decoded `+70` is
non-NULL, it uses signed WORD `+68` to locate a CharacterRenderRecord through
global `022C6F28`, stride `740h` and that record's `+284` gate. It rewrites rig
`+70`, calls `00421D20`, then stores the encoded result into rig `+78`.
If the initial decoded `+70` is zero, this `+78` assignment is skipped; there
is no implicit clear on that path.

`00421D20` reads the input record's index `+18`, resolves its root through
encoded `+10`, looks up the root's `+D98` pool, and returns the decoded found
row's `+84`. That row is the RenderStrideC0Element whose `+84` holds encoded
resolved workspace in the retained producer package. Rig `+78` therefore
borrows that core through the lookup; this does not prove its usable extent,
ownership or later lifetime.

Rig `+84` has a different purpose. At `003E1D49` the routine loads its DWORD,
compares it with EDI (the rig pointer's low 32 bits), and returns from the
rebasing section when equal. On a completed fresh/relocation path,
`003E27EA` stores EDI directly into rig `+84`, without an encoder.

If the cached value is zero, the fresh path rebases `+88` using the rig's low
address. Otherwise the relocation path computes `ESI=low32(current-oldSelf)`
and rebases by that delta. With a stable decoder base, exact instruction
arithmetic gives:

- Fresh: `new88=low32(old88+low32(rig))`.
- Relocated: `new88=low32(old88+low32(currentRig-oldRawSelf84))`.
- Same cached low address: no `+88` rewrite.

The conditional `+70`/`+78` refresh occurs before this cache check. Thus a
repeat skips list rebasing while still allowing its borrowed-core link to be
refreshed. This is a local guard fact, not proof that every native controller
initializer is idempotent. Pointers differing by 4 GiB collide in the cache;
a nonzero pointer with low DWORD zero collides with the cold zero value. Actual
allocator address-domain guarantees are not established here.

The raw authored-offset interpretation is not portable to arbitrary decoder
bases. Keep the original 32-bit operations and final full-width decode;
mathematical examples are not runtime samples or proof that the base is always
zero.

## Reset count and indices

`003E3C30` decodes rig `+88` before checking unsigned DWORD `+8C`. Count zero
skips list dereferences and calls to `00203170`. For a positive count it reads
each unsigned DWORD index, decodes rig `+78`, and passes:

`Decode(rig78) + 230h + index*290h`

to `00203170`, using 64-bit address arithmetic. The list advances four bytes
per iteration; EDI is compared unsigned against `+8C`. This body has no
per-index bone-count/range check. Native reset effects, list/core readability,
alignment, extent and stability need their own evidence/preconditions.

The supplied fixup body has no direct RDI-relative `+8C` access. This does not
prove a constructor default, count preservation against indirect aliases, or
the contents of the original copy call. Existing accepted UQ220 evidence
identifies the rig as FCP section 2; that census is not repeated here.

## Nullable lookup precondition

When initial decoded rig `+70` is nonzero, a WORD `+68 == FFFF` or an inactive
indexed record makes the rebinding logic encode zero into `+70`. At stable
base zero its next decode gives RCX=0, which is passed to `00421D20`.
That helper starts with PUSH/SUB and then reads DWORD `[RCX+18h]`; it has no
input-NULL check before this read. The conditional effective address is 18h.

This is a source-path result, not an observed fault, a naturally reachable
invalid state, or an explanation of EXP127's unknown crash cause. At a nonzero
base the address is `low64(Decode(Encode(0))+18h)`, not universally 18h.
The helper's -1/missing-row returns require a valid input object; they are not
a NULL-input guarantee. Normal completion of the borrowed-core/rebase path
requires valid active owner metadata when that rebinding branch is taken.

Producer 1's scoped normal-return facts are retained unchanged. Producer 2
adds this boundary and precondition, rather than falsely invalidating those
facts or overwriting their original driver/result/receipt.

## Provenance and controls

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
New source contains complete 2,992/109/70-byte bodies (3,171 bytes). The binder,
decoder and encoder source is retained from published parent evidence with its
original manifests and capture receipts, without recapture/execution credit.

The actual capture uses the shared reviewed role adapter. Producer checks cover
all upstream terminal/exit/exception and invocation identity gates before
output, exact original bytes, complete local CFG/named lookup tail, argument
and field operations, carriers, cache-load dominance and memory widths/roles.
Four actual CLI refusals cover failed capture, incomplete wrapper, missing
source and a coherent mutation of the lookup's first read. They validate the
producer, not native effects or independent project acceptance.

No PC/game/native harness/instrument/save/config/reference/peer file or peer
process changed. All scientific children are terminal. Independent review and
canonical owner consumption are required. All-writer, initialization, runtime
entry, scheduling, address-domain, extent and lifetime obligations remain open.
EXP127 stays invalid; the parked menu allowance stays spent and unapproved.
