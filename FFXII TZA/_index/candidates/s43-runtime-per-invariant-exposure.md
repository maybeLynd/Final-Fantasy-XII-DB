# S-43 runtime: per-invariant stub exposure for EXP-057 / EXP-088 (OPUS, 2026-09-25, block 299)

**Row:** S-43, the save image. The runtime cell is MIXED with the qualifier "no per-invariant stub-exposure analysis
yet". The binding gap reads "types PARTIAL and nothing executed …". This note scores nothing.

## S-43's four contracts, and what executes each

| contract | executed by | substitutions |
|---|---|---|
| `CONTRACT-save-image-buffers.md` | **EXP-057**: the original CRC helper and the active-buffer getter `002EF640`, "without stubs". Its §13 cites further isolated original-code records | **none.** Disclosed limit: the finalizer is **entered at `00583F81` with an injected destination and frame**. Its earlier effects (the whole-image clear, copy and submission) are not run by EXP-057 |
| `CONTRACT-save-container-transform.md` | **EXP-088**: 46 / 46 cases and 9 / 9 byte mutants. All five entry bodies plus every bounded real callee run, including the **entire shipped zlib deflate / inflate subtrees** (real code, real mallocs), the vector helpers, the CRT locked-IO wrapper and the cookie check. The `memcpy` / `memset` import thunks resolve through their real IAT slots | **imports only:** CryptoAPI (ADVAPI32) is a high-level model (the record: *"the derived key bytes themselves are not proven against real advapi32"*); file I/O is a synthetic filesystem; `rand` is scripted per case. **No application function is stubbed** |
| `CONTRACT-storage-read-completion.md` | its §13 cites `diff_storage_read.py` (SWE2-CONTRACT, `eab67079`), which drives all three entries under Unicorn. **Not named in S-43's runtime cell** | not examined in this note |
| `CONTRACT-save-image-pipeline.md` (SV-1..SV-6) | **none.** Its §13 says: "No experiment executes these seven bodies" | coverage gap |

## Per invariant, where a substitution exists

| contract item | can a substitution reach it? |
|---|---|
| save-image-buffers: the fill length `0x56690`, the copy loop's `0xACD` iterations × 8 | **no.** EXP-057 has no stubs. The whole-image clear and copy are the part EXP-057 does not run (a coverage limit, disclosed) |
| container transform: writer order, header layout, `rand` → `abs` → `%32` rotation, deflate level 9, chunking, capacity bookkeeping, failure returns | **import-class only.** Call order, constants, flags and failure returns are measured from shipped code |
| container transform: **the ciphertext bytes** | **import-class, and the model's fidelity is open.** RC4 key derivation from the MD5 digest is the HLE's assumption. EXP-088 bounds this itself: it needs a real `.sav` cross-check or live advapi32 |
| save-image-pipeline SV-1..SV-6 | not executed |

## For the scorer

- **No application stub reaches any S-43 invariant.** Every substitution is at an OS or CRT import boundary. The one
  with open fidelity (CryptoAPI key derivation) affects only the ciphertext bytes, and its record says so.
- **Coverage gaps, not exposures:**
  - `save-image-pipeline` has no execution;
  - EXP-057 enters the finalizer mid-segment;
  - `storage-read-completion`'s differential test is not cited in the cell.
- **Stale text:** "types PARTIAL … nothing executed", against a MET types cell and the executions above.
- `live_game` is false.
