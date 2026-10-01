# S-49 runtime: per-invariant stub exposure for EXP-094 / EXP-097 (OPUS, 2026-09-25)

**Row:** S-49 Phyre asset and class-descriptor surface. The runtime cell is MIXED, *"no per-invariant
stub-exposure analysis yet"*. The three contracts are cluster header, packed namespace and class descriptor. The
records are:
- **EXP-094:** the cluster header load `0059A3B0` and the namespace block;
- **EXP-097:** the class descriptor destructor `00633390`;
- **EXP-124:** live, title menu; registered defaults and parent links.

This note scores nothing.

## Substitutions, as disclosed

| record | substituted | kind |
|---|---|---|
| EXP-094 | `0019C580` / `0019C570` heap alloc/free sinks; `00808B90` CRT `atexit`; `008092FC` / `0080929C` lazy-init acquire/release (not taken) | CRT / heap boundary |
| EXP-094 | stream object `+0x10` ready / `+0x28` read leaves (`min(len, remaining)` copy) | I/O fixture: *"no shipped memory-stream class exists to run instead"* |
| EXP-094 | **member-node graph spliced into `desc+0x80`** (`00160210` leaves it self-linked; the engine's member registration was not replayed) | **reflection fixture** |
| EXP-094 | **member-type objects**: vtable slot `+0` is a fixture swap leaf that does a real `bswap` and logs `(addr, flag)` | **reflection fixture** |
| EXP-094 | `memcpy` IAT → fixture routine | import |
| EXP-097 | `00584730` `_aligned_free`, scripted at entry | CRT heap boundary |

Everything else runs as shipped bytes:
- EXP-094: the loader, the descriptor walker `0063E2E0`, descriptor construction, the namespace block swap and the
  stream accounting;
- EXP-097: the destructor, the `+0x70` detach `0063D640`, the `+0x60` drain `006B6700` and the TLS getter `006373D0`.

## Per invariant

| contract / inv. | claim | can a substitution reach it? | owner reading |
|---|---|---|---|
| header **I1** | a big-endian file is accepted by flipping the whole header and re-testing the same constant | **The accept / re-test:** loader body, real. **"The whole header is flipped":** the walk is real, but it walks a **fixture member graph** and calls **fixture swap leaves**. The engine's own member registration and member-type swap functions did not run. | **accept path not reachable; the extent and manner of the flip are exposed to the reflection fixture** |
| header **I2** | `bytesConsumed` advances by what was read (`0059A3DA` adds `eax`) | the addition is loader code; `eax` is the fixture read's return | **not reachable** (the claim is the addition) |
| header **I3** | a different header length is tolerated | loader control flow | **not reachable** |
| header **I4** | nothing validates contents | loader code | **not reachable** |
| namespace **I1**, **I2** | the size formula closes; `sum(w3) == nMembers`, contiguous | **archive census** (35,984 / 35,984 files), not an execution claim | **no execution exposure**; the evidence class is data census |
| namespace **I3** | the reader validates nothing | reader code, real | **not reachable** |
| namespace **I4** | a short read still advances and still swaps | the advance is real; the swap of the namespace block is the real block swap | **not reachable** |
| descriptor **I1** | name `char*` at `+0x30` | layout, confirmed by EXP-124 live reads of registered descriptors | **no exposure** (live) |
| descriptor **I2** | aligned storage: the deleting destructor calls `_aligned_free` | the **call target** is the claim, and it is recorded at the scripted entry | **not reachable** (the heap internals are not claimed) |
| descriptor **I3** | six circular lists, self-linked when empty | the drain `006B6700` is real | **not reachable** |
| descriptor **I4** | `+0x70` released before any list; two vtable identities | destructor body and `0063D640` real | **not reachable** |

## For the scorer

- **Eleven of twelve claims are out of every substitution's reach.** Their substitutions are CRT/heap or I/O
  boundaries, not application stubs.
- **The exposure is header I1's flip.** It was executed through a fixture member graph and fixture swap leaves. It
  closes when a run uses the engine's own member registration (the deferred finalize machinery `00160210` leaves
  pending) and the real member-type swap functions. EXP-094 calls that registration *"too deep to replay"*.
- **A static reading of which member-type vtables the real `PClusterHeader` members carry would bound it** without
  execution. That is FABLE/ORACLE territory, routed as a question rather than claimed here.
