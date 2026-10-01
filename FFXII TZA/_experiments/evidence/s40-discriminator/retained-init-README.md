# S-40: the post-processing frame and its creation route, run as shipped up to the Direct3D device (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), against a one-method device-context model. `live_game: false`.**

**The gap.** S-40's runtime cell was `—`: *"the row gates on runtime for the licensed-library layer; no live capture
exists"*. Every S-40 invariant was byte-verified statically (`CONTRACT-post-processing-subsystem.md`, block 238), and none
had been executed.

## What was run

`check.py` runs over block 332's world (`../s21-opus-replay-applier-stub-free/check.py`, whose cases run first; its
`result.json` is unchanged). It calls the game's own frame function `00193DA0` with a render command
`{+0 render context, +0x10 cfg}`.

**Built, not planted:**
- **The library's allocator object** `02E5BDE0` is built by its shipped C++ static initialiser `00167990`. That function
  is an entry of the CRT initialiser table (pointer at `008C44D8`), which block 332's CRT start does not run.
- **The wrapper chain is built by the frame itself.** That covers the wrapper `[02D38540]`, its adapter object
  (`0065E530` / `006CBAA0`) and the library handle (`006DA990`).
- **`CPostEffect` (`0xD40`) is built by the library itself.** `006DAA70` allocates it, and its constructor `006FF5D0` runs.
- **The licence is the shipped string** at `00D86C00`, validated by the library's own reader: `006DFF40` → `0071CD10`,
  which parses with `0071D170` and checks with `0071D9E0`.

**Fence.** The frame's closure, plus the targets `edges.tsv` cannot see because they are reached indirectly:
- the allocator vtable `00D86BD8`, read from the image up to its null slot;
- the handle vtable slot `006DAF50`;
- `006DA990`, behind the tail-jump thunk `006DEF20`;
- the `free` thunk `0019C590`.

**Bridges** (`crt_bridge.py`, by name, fail-closed):
- **C runtime:** `strtok_s`, `sscanf`, `strcpy_s`, `atoi`, `memcmp` and `strncmp`, with the C library's semantics.
  `sscanf` supports `d`/`u`/`x`/`X` only; any other conversion stops the run.
- **msvcp140:** the six `basic_streambuf<char>` / `basic_istream<char>` members the licence reader uses, with standard
  semantics over the MSVC x64 layout. The image's inline `setg` writes `_IGfirst`, `_IGnext` and `_IGcount` at the offsets
  the bridge uses (`0071DB6B`–`0071DB84`). `read` refuses unless the buffer's `xsgetn`/`uflow`/`underflow` slots resolve to
  the base-class imports. The DLL's vtables and locale sit on a non-executable page.
- **Counts from the run:** `sscanf` ×5,664, `memcmp` ×110, `strtok_s` ×28, `istream::read` ×5.

**The device is not emulated.** The render context is a zero block. Its only populated field is `+0x110`, the D3D11
device context `Initialize` takes. That context is a **disclosed one-method model**:
- slot 112 (`+0x380`, `ID3D11DeviceContext::GetType`) returns 1, `D3D11_DEVICE_CONTEXT_DEFERRED`;
- every other slot points into a non-executable page.

In the shipped game the context is the immediate one. The model makes `Initialize` take its own refusal branch instead of
the device work behind it.

**8 / 8 pass; `result.json` is byte-identical over two runs (md5 `5d726159…`).**

| case | contract claim | observed |
|---|---|---|
| `static_initialiser_builds_the_library_allocator` | (world) | `00167990` returns; `02E5BDE0` gets the vtable `00D86BD8` |
| `P1_teardown_without_object_runs_nothing_behind_the_gate` | §4 step 1–2, **I-1** "none without a library object" | `cfg+0x99` set and no library object: `0065E6C0` → `006CC2F0` runs and null-guards both members. The frame returns through `00193DFC`. No creation link, no setter forwarder and no run forwarder is entered |
| `P2_creation_route_once_per_link_with_constant_flags` | §3 route, **I-2** | `cfg+0x99` clear: `0065E5A0` → `006CBD20` → `006DAA70` → `006FF900`, each entered once. `006DAA70` receives `3`, `5` and fifth argument **`0x20001`** |
| `P2_shipped_licence_validates` | §3 licence registration | `0071CD10` returns 0 on the shipped licence (feature `YEBIS_D3D11`, no dates, MAC `00-…-00`) |
| `P2_Initialize_stores_0x20001_at_208_and_20C` | **I-2**, the I-3 bits | `CPostEffect` allocated at `[02EA0B70]`, constructor run once. `Initialize` stores `0x20001` at `+0x208` and `+0x20C`, read back. `0x800`, `0x40000`, `0x4000000` and `0x8000000` are all clear |
| `P3_refused_init_is_logged_and_creation_continues` | §3 failure clause, **I-5** | `GetType` called once. The library logs *"CPostEffect::Initialize(): Device context must be immediate context."* and returns `0x80070057`, as does `006DAA70`. `006CBD20` logs *"Failed to initialize PPFX context."* through `005CDAA0(2, …)` and continues into `006DB4C0` → `00708110` |
| `P3_continuation_faults_on_the_unbuilt_plus_108` | **I-5 bounded** | `00708110` faults at **`00708186`** reading `0x68`: `CPostEffect+0x108` = 0 and `+0x147` = 0. Nothing behind `00193DFC` runs |
| `S1_plus_147_and_plus_108_written_only_past_the_device_check` | why P3 generalises | Byte-verified: the constructor zeroes `+0x108` (`006FF68E`). `Initialize`'s own body writes `+0x108` only at `007009BB`, and writes `+0x147` only at `00700083`, under flag `0x800` (`00700077`), after `00700056` zeroes it. `00708110` returns early only on `+0x147` (`00708152`/`0070815F`), otherwise it reads `[+0x108]+0x68`. The context-type test is `006FFC50`–`006FFC5E`, and the frame gate is `00193DFC` |

## What this settles

- **The creation route runs as the contract says, with the library's own code.** Every link is single, the
  arguments are constant, the licence is accepted and `0x20001` is stored (I-2).
- **I-1's "none without a library object" half runs.** The `cfg+0x99` teardown on an empty wrapper null-guards and
  returns, and nothing behind the gate runs.
- **I-5 is bounded, and the contract now says so (§3, §5).** The claim *"a failed initialisation is logged and creation
  continues"* is true, but the continuation's next library call faults unless `Initialize` passed `007009BB`. That
  point lies behind the immediate-context test.
- **The frame's setters and its run are device-gated.** They sit behind `00193DFC`. They run only after a creation that
  returned, and by S1 that needs an `Initialize` that passed `007009BB`, which takes a real immediate D3D11 context.
  So I-1's "at most one run per frame", I-3's pass exclusion, I-4 and I-5's `ApplyEffects` half stay static-only
  (byte-verified in the contract cell). They cannot be executed without the device. This is the same render-layer
  boundary AUDIT-SEM ruled on for S-37 (`AUDITSEM-REQ-OPUS-409`).

## Not covered

- Everything `Initialize` does with a real device, and the frame after creation: the §4 setters, `ApplyEffects` and
  its HRESULT.
- A live capture.
