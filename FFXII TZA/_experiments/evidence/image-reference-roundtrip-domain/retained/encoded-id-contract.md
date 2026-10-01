---
contract: decode a 16-bit encoded id into its class and row, validate it against that class's registry descriptor, and fill a query record with the row's name, description and per-class copies
category: 00-Engine-Core-Runtime
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md
entries: ["0031C5D0", "0035D330", "0035D380", "00322C50", "0030B6A0", "0031E9A0", "002F9860"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-05 original-code static derivation and bounded native execution, plus independent retained EXP-143 review. Historical per-caller and authored-corpus surveys are carried, not recertified."
last_reviewed: 2026-09-22
production_review: "SECTION-05; locally validated, independent acceptance pending; prior audit metadata is historical"
audit:
  by: OPUS
  date: 2026-09-21
---

# Contract — encoded IDs, registry initialization and reusable query records

**Current specification: SECTION-05 (2026-09-22), local production complete; independent acceptance
pending.** Historical audit metadata does not accept this rewrite. Evidence tags: **N05** means
original instructions run with synthetic state; **S05** means selected original-code/data inspection;
**R143** means independent review of retained EXP-143 records, not a new emulator/live run;
**HIST** means explicitly carried older page/consumer research.

Evidence: [section review](../_experiments/evidence/continuation-section05-encoded-query/REVIEW.md),
[original instructions](../_experiments/evidence/continuation-section05-encoded-query/original_disassembly.txt),
[case results](../_experiments/evidence/continuation-section05-encoded-query/results/native_baseline.json),
and [current mechanism](the-query-record-from-initialization-to-reuse.md).

## 1. Purpose

This shared interface derives inventory classes from 16-bit encoded IDs, validates class-specific
requests, resolves names/descriptions, and selectively writes a reusable 0x98-byte result for menu
and other consumers. It is not a uniform serialization of an item and is not a pure function of ID.
Class tags, low-nibble row indices, decoded pointers and relative offsets are different quantities.

## 2. Interface

| Entry | Interface and bounded guarantee |
|---|---|
| `00309440` | Reads low 16 input bits; nibble 0..E selects `01EEBCC0+n*0x58+0x38`; shipped value is n+5. Nibble F returns -1. |
| `00322C50` | ECX class, EDX 32-bit ID/row; classes 1..32. Returns 0/1 from signed-inclusive bounds, with class1 redispatch. |
| `0030B6A0` | RCX state base; updates fifteen registry rows AND clears/masks derived state. |
| `0031C5D0` | RCX caller-supplied writable 0x98-byte query; clears name+18 then dispatches; partial writes on success. Returns 0, -2, or class19 valid-case -1. |
| `0035D330` | ECX tag, EDX DWORD value; writes static `022CA520` request+0/+4. |
| `0035D380` | ECX tag, DX WORD value; writes static `022CA480` request+0/+6. |

Both wrappers always return their own record address. A negative fill calls the original three-byte
`ret 0` at `0016D6A0`, then zeros all 0x98 bytes. That stub is not an error-state proof. A nonnegative
return does not scrub the record. No status value is returned separately by the wrapper. **N05/S05**

## 3. Types and representations

**`ItemClassDescriptor`, 0x58**, static table at `01EEBCC0`, fifteen rows:

| Offset | Representation |
|---|---|
| 00/18/28 | QWORD-tested offset slots, low DWORD used for addition |
| 08/20/30 | Resulting pointer/storage lanes, QWORD stores of zero-extended 32-bit sums |
| 10 | Number of WORD storage elements; differs from the ID count for bitset classes |
| 14/44 | Four-byte declared interiors; no meaning promoted here |
| 38 | Registry class; shipped 5..19, equal to nibble+5, not nibble |
| 3C | Inventory-dispatch count; not the universal validator's bound source |
| 40 | Exclusive prefix sum of preceding +3C counts, computed by rebase with 32-bit wrap |
| 48/50 | Mutate/query function pointers; class14/15/18/19 have mutate but no query |

Lane08 is WORD-packed counts for classes5..7 and a WORD-indexed bitset for other supported classes;
lane20 is interpreted by the selected handler, not a universal bit array. These are conditional
views, not three identical arrays. Shipped counts sum to 6892. **N05/S05; other mutation semantics HIST**

**`EncodedIdQueryRecord`, 0x98**: class DWORD at0; row DWORD+4 overlaps ID WORD+6; optional borrowed
text pointers at08/10/18; tagged scalar/byte/word views thereafter. Class10 initializes twelve
DWORDs at `+38+8*k`, k=0..11, through +90..93. The tail is NOT universally unwritten.
Equipment updates bit0 of byte+54; action/command/school classes can write pointer+08.
A sized, physically tiled record is not evidence that every output has a known semantic meaning.

## 4. Preconditions · postconditions · invariants

**I1 — tag selects the input lane.** WORD+6: classes1,5..11,13..18,30,31. DWORD+4:2..4,19..29,32.
Class12 reads neither input lane and immediately returns -2. The old 16/16 partition is false.
Selecting a wrapper does not change what the class arm reads. **S05, one N05 baseline per class**

**I2 — three validation domains must not be collapsed.** `00309440` maps the low16 nibble;
`00322C50` uses class-dependent runtime descriptors/constant ranges; inventory queries use the
fifteen-row registry's counts and handlers. Validator class19 is E000..EFFE inclusive. Class13 sums
four descriptor counts; missing entries contribute zero. Class1 retains the full32 input for the
redispatched validator. **S05/R143/N05 bounded controls**

**I3 — rebase width is observable.** Each offset's full QWORD decides whether to write, but the
stored pointer is `u32(low32(offset)+low32(state))`. Zero offsets preserve destination pointers.
High-half-only offsets still select the write. No universal high-half-zero precondition is silently
assumed; shipped high halves are zero, synthetic variants demonstrate other behavior. **N05**

**I4 — rebase also resets state using the full pointer.** It zeros exactly state+57C8..59C7 and
ANDs the 128 bytes state+59C8..5A47 with F8. Above-4GiB state fixtures distinguish these full64
writes from truncated registry pointers. Repetition recomputes pointers/prefixes and resets derived
state again; it is not merely adding a base once to existing pointers. **N05**

**I5 — direct fill and wrapper failure differ.** Direct fill clears only name+18 at entry. An early
refusal can preserve all other bytes; class1 may first replace the tag. Wrappers clear the whole
record on negative return. Success preserves any lane that its reached arm does not assign. **N05**

**I6 — borrowed results have two lifetimes.** A wrapper address is static and aliases later calls to
that wrapper; the other wrapper has a distinct record. Returned text pointers refer to separately
resolved storage, not copied/owned strings. Allocation/free or resource-reload lifetime is not proved
by their sampled pointer values. Concurrent/reentrant safety remains unestablished. **N05/S05**

## 5. State

| Object | Address |
|---|---|
| Fifteen registry descriptors | `01EEBCC0` |
| Row/DWORD wrapper record | `022CA520` |
| ID/WORD wrapper record | `022CA480` |
| Query 32-arm table | `0031E598`, image-relative DWORD targets |
| Validator 32-arm table | `00323054`, distinct from the query table |
| Text-bank root slots | `02EBF170` and indexed neighbors |
| Universal relative-reference base | `01F83530` |
| Description ready/root arrays | `02EC3D80`, `02F973C0` |

Dynamic row descriptors in `02EBF0xx..02EBF1xx` are not the inventory descriptors at `01EEBCC0`.
State contents, resource bindings and existing result bytes are inputs to this mechanism.

## 6. Relationships

`0020E600` returns zero-extended DWORD argument plus the FULL QWORD relocation base. Individual
query arms then perform row stride multiply/add in 32-bit registers, so a decoded high half can be
lost before row dereference; that is distinct from full-width text-pointer resolution. **S05/N05**

`002F9860` resolves description IDs using its pool/root state. `00309EC0` and `0030AE30` dispatch
inventory modes0/1; their original packed and bitset handlers are executed by this fixture.
Packed available quantity is low10 count minus high6 reserved count; total is low10. With synthetic
reserved>total the available result is negative. Missing query handler returns zero, not proof that
the corresponding mutation is inert. `FFFF` and invalid nibble are rejected separately. **N05**

**Restored by the owner (OPUS, 2026-09-25)** — the handler table and the validator tail the rewrite dropped,
re-read from the image. **The handlers are not always a pair.** In the registry at `01EEBCC0` (stride `0x58`,
row = class − 5), classes **14, 15, 18 and 19** carry a mutate handler at `+0x48` and a **null** query handler
at `+0x50`: `002FD530`, `002FD640`, `002FD780`, `002FD880`. Classes **10, 12 and 16** have both handlers null.
The universal validator dispatches classes 1–32 through the 32-entry table at `00323054`, and all arms converge
on one tail: `0032302E cmp ebx, edx` / `jl` → 0 (below LOW), `00323036 lea eax, [rcx-1]` / `00323039 cmp ebx,
eax` / `jg` → 0 (above HIGH), `00323041 mov eax, 1`. **[page, OPUS re-read]**

`0031E9A0`/`0031E9F0` select equipment views; `00323890`/`003241D0` select licence category values.
The existing caller census identifies consumer routes, but its absent-read findings are limited by
pointer handoff/spill coverage and cannot prove that a producer never writes a lane. **HIST/S05**

## 7. State transitions

1. Authored registry offset/count/handler values exist in the image; pointer lanes and prefix cells
   are initially zero in these fifteen rows. This is an on-disk observation, not proof of live order.
2. Rebase converts nonzero offsets, computes prefixes, and resets derived state as I3/I4 specify.
3. A caller supplies a class and the lane that class reads. Class1 may rewrite the class in place.
4. Validator admission does not guarantee row/text pointer availability. The filler writes its
   selected outputs from row data, text services and current inventory state.
5. Direct fill returns its status; wrappers erase negative results and always return the static pointer.
6. Further calls can replace assigned fields while retaining other prior bytes. Real reload and
   call-order/lifetime obligations are outside this synthetic-state proof.

## 8. Script · resource · event interactions

Names and class-specific data depend on loaded row and text descriptors; inventory values depend on
runtime state. The historical authored-table/name survey is retained on the mechanism page, not
rerun here. This packet runs no VBF extraction, script, menu renderer, asset loader or event loop.
No string lifetime guarantee across resource replacement is inferred.

## 9. Determinism

No RNG or clock is invoked on the tested query/rebase paths. Outcomes are reproducible given the
same request bytes, existing output bytes, registry, row/text data and inventory state. This is not
purity with respect to ID alone, and it is not a proof of thread-safe or reentrant wrapper usage.

## 10. Failure paths and edge conditions

- Out-of-domain tag or class12: direct -2, name cleared; wrapper zeroes all bytes.
- Class19: correctly formed DWORD E000..EFFE returns -1; outside-range -2.
- Class1 does not repack WORD+6 as DWORD+4 when it derives class19. The tested id-form E000 therefore
  fails validation, after rewriting its tag, rather than automatically taking the -1 path.
- Classes4/22/23 validate and can return0 having only performed the common name clear.
- Class10 writes its strided tail but preserves intervening four-byte gaps and final +94..97.
- Class13 validator's fourth descriptor can admit IDs beyond the filler’s three fixed row ranges;
  synthetic8200 returns0 with stale row outputs. Normal-game reachability is not established.
- Class2 can return0/nullname with decoded row base0; classes5/6 fault at row+0A/+12 when valid
  counts coexist with base0. These are isolated-child controls, not crashes induced in FF12.
- Missing text bank can yield nullname despite successful validation; owning nothing is not the
  universal cause of a missing name.

## 11. Observable behaviour

The interface supplies names and tagged values used by menus and other readers (historical caller
survey). This section proves selected original call results and memory effects, not a newly rendered
menu, audible event, fresh loaded asset or complete gameplay session.

## 12. Reproduction formula

```text
rebase(state):
    prefix = 0
    for each of the 15 rows:
        for off,pointer in [(00,08),(18,20),(28,30)]:
            if QWORD(row+off) != 0:
                QWORD(row+pointer) = zero_extend(u32(DWORD(row+off)+low32(state)))
        DWORD(row+40) = prefix
        prefix = u32(prefix + DWORD(row+3C))
    zero(state+57C8, 0x200)              # full state pointer, not low32 alias
    for k in 0..127: BYTE(state+59C8+k) &= F8

wrapper(class, value, selected_buffer, lane_width):
    write class and exactly the selected input lane
    rc = original_fill(selected_buffer) # tagged partial writes; not a whole-record initializer
    if rc < 0: original_ret_stub(0x800); zero(selected_buffer, 0x98)
    return selected_buffer
```

This pseudocode specifies two reproduced interfaces; the complete filler remains the class table,
original instructions and named test evidence—not an invented uniform row-copy formula.

## 13. Runtime validation

**Restored by the owner (OPUS, 2026-09-25): `EXP-100`** (auto-status-gates-exec, method B, 40/40 cases,
13/13 mutants, stable across two processes) executes the validator `00322C50` **for real, arm 6 of 32 only**
(the equipment-id range), inside another contract's experiment. **[EXP-100]**

**N05: 200 assertions**, identical repeat, seven targeted private-image mutants rejected. Original
filler/validator/wrappers/rebase and their reached application callees execute without application
substitutions; only imported memset is bridged. Synthetic states include one baseline per query
class, conflicts in preserved bytes, two distinct record buffers, high-address base tests, packed
inventory modes, text chains, special class outputs and isolated-child pointer failures.

**R143:** 246 retained traced records and four summary-only returns reconcile, including all validator
classes and 32 jump-table entries. The producer's reported173 is a mixed outer-container count, not
173 uniform executions. This is retained-evidence review, not a full historical Unicorn rerun.

No initialized-game timing, live mutation, all authored records, allocation lifetime, or formal L2
acceptance is claimed. Detailed reproduction and limits are in the section review.

## 14. Unresolved

- [ ] Exact downstream meaning of all tagged output slots and strided class10 elements; physical
  stores and preservation rules do not assign semantic names by themselves.
- [ ] Exhaustive caller validity/reentrancy and pointer lifetime across resource replacement.
- [x] ~~Shipped-state reachability of synthetic descriptor/count/mask anomalies, especially class13’s
  fourth-range mismatch and high-address truncation.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT): both
  named anomalies are unreachable on shipped data; the residual is one runtime property.**
  - *Class13 fourth range.* The validator arm `00322E28` sums `[desc+4]` over four slots —
    `02EBF090`, `02EBF088`, `02EBF080`, `02EBF078`, each null-safe (`test rcx,rcx` → contributes
    0) — admitting `[0x8000, 0x8000+sum)`. The installer fills the four slots from master-record
    fields `+0x88`/`+0x8C`/`+0x90`/`+0x94` via `003845F0` at `00236E8C`/`00236EA6`/`00236EC0`/
    `00236EDA`. **The fourth slot resolves a table that ships empty** (`02EBF078` = `+0x94`,
    `0 × 10`, per the mechanism page's authored census). Shipped sum = 64+32+416+0 = **512**,
    matching the registry row's `+3C = 0x200`, so the admitted range `[0x8000, 0x8200)` is exactly
    the three populated sub-tables the filler serves — ids ≥ `0x8200` can never validate on
    shipped data, and the "synthetic 8200" anomaly requires a nonzero fourth count no shipped
    pack supplies.
  - *High-address truncation.* ~~All 45 registry offset qwords (`+00`/`+18`/`+28` × 15 rows) ship
    with **zero high dwords** (direct table dump) — the "decoded high half lost before row
    dereference" path has no shipped operand.~~ *Corrected 2026-09-25 (FABLE, Claude Opus 5.5;
    `overlay-publication-plan.md` ruling 5).* The 45 offset qwords do ship with zero high dwords.
    That is what the image initialises, and **they are not operands of that path**. No code writes them.
    The only functions that address the table are the rebase `0030B6A0` and `0030B270`. The rebase reads
    each offset and writes `+08`/`+20`/`+30`/`+40`; `0030B270` reads `+3C` and calls through `+50`.
    Domain: rip-relative and `lea` references across `01EEBCC0`–`01EEC1E8`, plus a whole-file scan
    for stored 8-byte pointers into that range, which found none. Its control finds the one stored
    handler pointer `002FD530`. The rebase tests each whole qword for non-zero but adds only its low
    dword (`0030B6C5`–`0030B6CB`), so a high half could not reach a pointer even if one were present.
    The query arms take their row operand elsewhere: `0020E600(dword [table directory + 0xC])`,
    for example `[02EBF100]` in the class-5 arm (`0031C723`–`0031C75F`). So the high half that
    could be lost is that return value's, which is `qword[01F83530]` plus a zero-extended dword.
    The rebase's own zero-extended sums are exact while the state block sits below 4 GiB. That block is
    `02164280 + 0x4E68C`, passed by both callers (`00233C2A`, `00238A89`), and the PE sets no
    `DYNAMIC_BASE` (`DllCharacteristics 0x8120`, preferred base `0x120000`). The remaining surface is the state base itself:
    `0020E600` = `arg + qword[01F83530]`; that global is BSS with exactly two image-wide
    rip-references (`0020E602` add, `0020E626` inverse sub) ~~and no static store site — it is
    never written by any static store the census found — the image zero-initialises it~~ and no rip-relative store.
    **It is zero at image load**, past `.data`'s file-backed end `01F7E400`.
    - **One in-image store route reaches it, through a computed address.** The texture-id table writer `00210570`
      (reached from GiSetTexture's execute `00863040`) bounds the id only from above: `cmp cx, 0x4000` / `jge` is a
      signed 16-bit test. It then stores `qword [01F83580 + movsx(id)·16]`, so id `0xFFFB` (−5) writes its pointer
      argument into `01F83530`.
    - *Re-derived from the bytes 2026-09-26 (OPUS, owner), and replayed by FABLE:*
      `02-Resource-And-Asset-Pipeline/members/image_address_base_writer_bounds.py` R6.
    - The shipped id producers keep ids below `0x4000`, so the route is **undriven, not absent**. "Zero for the
      process life" is **supported, not proven**.
    - Every consequence drawn here from a zero base holds on the load-time value, and on every state the undriven
      route leaves untouched.
    - So how it acquires its value, and whether it can hold an address ≥ 4 GiB, are runtime questions, not decidable
      statically. *(For one consumer's behaviour with a base ≥ 4 GiB, see the S-32 `lu6.py` observation: `0030C71D`
      `add ebp, eax` keeps the low half.)* *Restated 2026-09-26 (OPUS), per
      `FABLE-REQ-OPUS-PROPAGATE-01F83530-SCOPE-INTO-THREE-CONTRACTS`.* *Corrected by the owner (OPUS, 2026-09-25), per FABLE's defect note (overlay-publication-plan.md ruling 5): the overlay's "populated through a computed pointer" asserted a writer with no evidence; `ImageRelativeReferenceBase` records exactly two references, both reads (`0020E602`, `0020E626`).* *Residual:* narrowed to exactly that.
- [x] ~~Whole-engine absence of external readers/writers of preserved gaps; the older consumer census
  cannot establish that. +08, +54 and the class10 tail now have concrete writer evidence.~~
  **CLOSED 2026-09-23 (SWE2-CONTRACT), static side proven, pointer side bounded with one named
  exception.** Raw disp32 scan over all `.text` for `[022CA480, +0x98)` and `[022CA520, +0x98)`:
  **17 candidate sites, of which 5 are immediates inside a bit-mixing body (`004B20xx`–`004B21xx`,
  not memory operands) and 12 verified** — the two wrappers writing `+0`/`+4`/`+6` and consumer
  `0035E2xx` touching `+0`/`+18`. **No static access touches any preserved gap.** For the
  pointer-handed side, all 191 wrapper/filler call sites were scanned forward tracking the
  returned record register: 71 record-based accesses, and the only gap-offset reads are
  **`[rax+0x5C]` in the diff loop `002CFF45`–`002CFFBE`** — which reads `+0x50`/`+0x5C`/`+0x60`
  of consecutive fills whose *class is data-derived* (`edi+1` from `+0x50` of a class-1 fill).
  `+0x5C` is unwritten only for class10 — so a class10 fill's stale `+5C` is observable iff
  that derived tag is 10, a runtime-data property. *Residual:* pointer chains that spill the
  record to memory beyond the forward window, and whole-`0x98` copies (`00273BA0`) that move
  gap bytes opaquely — which preserves rather than observes them.
- [ ] Formal independent acceptance and required major-system empirical obligations.

## 15. Evidence

SECTION-05 pins 19 original bodies, nine data spans and unchanged EXP-143 inputs. The shipped
registry table, full selected disassembly, 32 retained query snapshots, named native assertions,
negative controls, before/after rows and exact file diff are included. Historical authored data and
external consumer surveys remain explicitly historical. Canonical types and sibling pages carry the
same current corrections; TEAM, L2 verdicts, global dashboards and old raw captures are unchanged.

**2026-09-23 SWE2-CONTRACT additions** — shipped registry table dumped in full (all 45 offset
qwords' high halves zero); class-13 validator arm `00322E28` decoded (four null-safe descriptor
sums over `02EBF078`/`080`/`088`/`090`); installer `00236C80`–`00236Fxx` decoded (`003845F0`
installs each slot from master-record fields, class-13 = `+0x88`/`+0x8C`/`+0x90`/`+0x94`);
raw disp32 census over `.text` for both static records (17 candidates, 5 immediate false
positives verified non-memory, 12 real — none at a preserved-gap offset); forward
record-register tracking over all 191 wrapper/filler call sites (71 record accesses, sole
gap-offset read `[rax+0x5C]` in the `002CFF45` diff loop, class data-derived).

## 16. Parity plan

Compare all 0x98 bytes, not a truncated prefix. Supply sentinel-filled records and run the two wrappers
separately with compatible class/input lanes; include failure-then-success and success-then-success
reuse, peer-buffer isolation, tag1 redispatch, class10 tail gaps, masked-byte updates, and class19’s
last-valid/first-invalid boundary. Rebase tests need distinct full64 and low32 state mappings, zero
and high-half offsets, prefix overflow and repeated invocation. These are database falsifiers;
L3 reconstruction and integrated game parity are later work, not completion prerequisites here.

`00309EC0` (102 B) is the encoded-id class dispatcher: `cx == 0xFFFF` returns `-1`, `(cx & 0xF000) > 0xE000` returns `-1`; the top nibble selects `01EEBCC0 + class*0x58`, `cx & 0xFFF` bounds-checks against `dword[+0x3C]-1`, and `qword[+0x50]` non-null tail-dispatches `jmp rax` ~~with `(0, cx)`~~ **as `handler(id, 0)`**: `ecx` = the zero-extended encoded id (`00309F1C movzx ecx, r8w`) and `edx` = 0 (`00309F1A xor edx, edx`) - the class registry's second-level resolve.

*Corrected 2026-09-26 (OPUS, contract owner).* **The changed assumption is the argument order.** The earlier `(0, cx)` put the 0 first. The bytes load the id into `ecx`, the first argument, and 0 into `edx`, the second.
- **The base stays `01EEBCC0`.** It is `00309EF4 lea rax, [rip + 0x1BE1DC5]` with the next instruction at `00309EFB`. `00309440`'s `01EEBCF8` is the same table + `0x38`.
- **`01EC81F0` is refuted** (see `FRONTIER-REQ-OPUS-VERIFY-01EC81F0-VS-01EEBCC0-S05-MERGE`). No instruction references it. Read as fifteen `0x58` rows, every `+0x3C` count is 0.
- **Regression:** [`s05-opus-dispatch-abi-controls`](../_index/candidates/s05-opus-dispatch-abi-controls/README.md).
  - Executed with a decoy table at `01EC81F0` and argument capture at both query handlers: the shipped image passes `(01EEBCC0, handler(id, 0))` and fails both wrong readings.
  - A retargeted-`lea` mutant and a swapped-argument mutant each fail the valid reading.
  - A text check rejects either wrong reading in this paragraph and its consumers.
- *These controls prove the dispatch and its ABI, not what any callback means.*

Interior anchor `00309F20` (function `00309EC0`).

`002F9920` (314 B) is the bucketed sub-table search over `02EC3D80`/`02F973C0`: `ecx/10000` (magic `0x68DB8BAD`) picks a bucket `< 0x1C`; `dword[entry+4]`-counted records walk `word[+8]*i + 0020E600(+0xC)` comparing `dword[ecx]` to `esi`; on match `+0x14` -> `dword[+4]` -> `dword[resolved + i*4 + 4]` -> `0020E600` returns - the class registry's keyed second-level lookup.

Interior anchor `002F99EF` (function `002F9920`).

`0029FF60` (247 B) is the encoded-id description-entry filler the shop and bazaar listings call: a nonzero arg5 wins, else `dword[[rcx]+0x14]` biased `+0x186A0`; with `rdx` live, ids `>= 0x186A0` resolve through `002F9920(id - 0x186A0)` and lower ids through `002F9860(id)`, the resolved row feeding `00365B30` / `0029CC70` / `002B4090` by the `([rsi+8] & 0xC0) << 0x10` count and the `r14d > 0x20` split, while a null `rdx` routes to `0029CC00` / `0029CB80`; the result lands `[rsi+0x18]` and `0020E620` stamps `[rsi+0x20]` - the class-split entry fill.

Interior anchor `0029FFB8` (function `0029FF60`).

`0029CB80` (113 B) is the encoded-id name ring-buffer `0029FF60` and the save/blinking-icon callers share: ids `>= 0x186A0` resolve through `002F9920(id - 0x186A0)` and lower ids through `002F9860(id)`, then `dword[01E0C560]` increments mod 8 to pick one of eight 0x20-byte slots at `0209C390`, `002B4090(0x20, slot, name, edx)` copies the resolved string, and the slot pointer returns - the small rotating scratch that keeps id-to-name answers alive for the caller's immediate use.

Interior anchor `0029CBA6` (function `0029CB80`).

`003C02B0` (129 B) is the `02B457E0`-table description-entry fill: `qword[02B457E0 + 0xE8]` locates the table record, `base + word[+8]` holds the bound dword that caps `ebx`, and the matching 8-byte row at `bound + ebx*8 + 4` yields `bx` to `[rdx]`, a byte to `[rdx + 2]`, and its `dword[+4]` resolves through `002F9920` unless `-1` - the resolved pointer lands `[rdi + 8]`, `003C05F0(ebx)` supplies `[rdi + 0x10]`, and the body returns 1 - the quest-list / accessor-hub entry builder.

Interior anchor `003C02E2` (function `003C02B0`).

`0024DE70` (60 B) is the top-nibble class dispatcher the screen-fade and status-write callers hit: `((ecx >> 0x1C) & 0xF) - 1` bounds-checks `<= 8` and tail-jumps through the `0024DEAC` jump table - cases reaching `002FCA00`, `003B0AD0`, `00375AE0` or `003B2510`, with `0` returned for classes outside the table - the record-class router over the tagged-entry families.

Interior anchor `0024DE88` (function `0024DE70`).

`003B2510` (146 B) is the class-router case `0024DE70` dispatches to: it scans the `0x30`-stride `02EBE5E0`..`02EBEBE0` table for the `+0x00` key, then shape-dispatches on `+0x1C` - 0 returns 0, <=4 returns 1, 5 returns 2, 7 returns 5, and otherwise the `+0x10` child decides: `word[+0x378] & 0x100` set falls into 1, else `byte[+0x370]` indexes the `002925A4` jump table - the per-class shape answer the registry callers consume.

Interior anchor `003B2520` (function `003B2510`).
