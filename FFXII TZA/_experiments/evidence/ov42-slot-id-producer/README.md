# Presentation-slot capacity and action-word admission

**Question.** Does the local presentation-slot allocator exclude action IDs 511–534, or does it only admit free capacity and store the caller's word? This is the next static discriminator from FABLE's accepted OV-42 model. It does not determine which normal AI/script commands actually supply those IDs.

**Player view.** A free presentation slot can hold the suspect action IDs. The slot allocator does not filter them by action range. Whether normal game actions ever choose those IDs still depends on upstream producers.

## Evidence method and original identity

Method A: reuse the exact committed original 229-byte allocator and 166-byte acquire-wrapper prefix from `spattack-native-word-remap` (`1f6569546`). Capture only the missing **19-byte suffix** to close the wrapper CFG. There is no FF12/emulator/native execution and no repeated original-code experiment. Retained Git exit/output and manifest/member identities are checked; the reviewed shared adapter is actually used in the suffix capture and annotation checks, including store/LEA/read-modify/write controls.

EXE SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base `120000`. The original allocator is `30D070..30D155`; acquire wrapper is now closed `30CFB0..30D069`. The action-word store **`30D14F` belongs to `30D070`**, called by the acquire wrapper at `30D051`; it is not an instruction inside `30CFB0`. This makes the exact helper/ABI relationship explicit for consumers.

## Established result

The complete `30D070` body contains no native call. It zero-extends incoming `DX` into `R10D`, and the only other use of that carrier is the final WORD store at `slot+1C`. There is no action-range or category test on the input value.

The scan starts at slot 0, increments by 1 through slot 31 and stops at 32. Slot `i` is `22C17B0 + 48*i`; WORD `slot+1C == FFFF` selects the first free slot. This source-bound induction also rules out the scan's apparent null-record branch under the valid 32-slot array and stable-state premises. It is not an absence sample.

For a valid first free slot `k` in 0–31, normal execution writes the supplied action WORD unchanged, identity DWORD at `+20`, and DWORD 1 at `+10/+14/+18`, then returns the index. Thus **511–534 are not excluded by this local allocator**. Queue linkage is an intervening effect; valid, disjoint, backed list/pool/frame storage is required. This is a conditional original-code implication, not observed runtime allocation or lifetime.

If all 32 markers are occupied, the original branch returns `AL=FF` with no own nonframe write. That is capacity exhaustion, not action-ID refusal. Consumers should use the actual return width/preconditions; the package does not turn every wrapper early exit into an allocation-result certificate.

The acquire wrapper receives the action WORD in `R8W`, saves it as `BX`, forwards zero-extended `BX` in `EDX` and the saved identity in `ECX`, and stores the helper's returned `AL` into `unit+4` after the call. An existing non-FF `unit+4` skips acquisition. The bit-30 action-row arm has a separate `22C2158` bit-1 gate; the D0–F1 special-state exception is separate. Candidate IDs 511–534 have WORD differences 303–326 from D0, so reach the flag gate rather than the D0–F1 exception. Readable stable resolved rows and unchanged carriers remain premises.

**Sentinel boundary.** A supplied WORD FFFF is also copied. The occupancy marker would therefore remain FFFF even though other slot fields/list links are initialized. This helper has no special input-sentinel refusal. No natural FFFF submission, actual repeat allocation or resulting queue corruption is asserted here.

## Controls, limits and required consumption

`prove-01` / `result-01.json` and `control-01` / `control-result-01.json` are producer-valid. The control runs three real CLI prerequisite refusals and seven labelled source mutations for scan direction/stride/sentinel/bound, action-versus-identity store, wrapper forwarding and post-call unit binding. Missing suffix status, failed upstream exit and missing retained source cannot produce a result. Full versus first-free CFG controls are connected to the capacity claim. No malformed or zero-case run receives PASS.

Assume valid stable backed slot/list/frame storage, disjointness needed by linkage, normal native ABI/returns and valid resolved action data. This does not prove current resource identity, initialized pool ownership/reuse, upstream command/AI/authored VM input domains, action execution, actual rejection, or whole OV-42. Retained prior independent acceptance does not automatically accept this new proof.

FABLE owns the local-gate update and upstream producer frontier in its action-availability page. OPUS owns exact acquire-versus-allocate ABI, input/return widths, occupancy marker and valid-state qualifications. SPEC must independently review the original scan invariant, complete wrapper CFG, carrier-only reasoning and concrete prerequisite paths. No peer consumer is edited here. All tools are finite, handles close, and no PC/game/save/config/reference state changes.
