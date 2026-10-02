# FABLE review: ASTRA ov42-actor-predicate-domain

- **Packet:** [ov42-actor-predicate-domain README](../../../_experiments/evidence/ov42-actor-predicate-domain/README.md)
- **Producer commit:** `2b341ca3a` (ASTRA). The manifest sha256 begins `ca8a35ee40fa75f9` and equals the manifest
  committed in `2b341ca3a`. All 61 members hash as listed. The six retained source ranges (two retained raw files)
  equal the certified image's bytes. They include every body reviewed here.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes. They cover the 479-byte body, its two
  returns, the class query's dominance and its refusal arm, the zero-extended id, R8D = 1 at the class query, and the
  RDI record carrier into `00306480`. The narrowings fix the class name, keep the count as a runtime premise, and name
  the callees that the record-stability premise covers. None contradicts the packet.

## Method

[rv_avail.py](rv_avail.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the filecache-route2 review (sha256 `69f9bc40be32abcc32b189539c35a6738d829306c19d61a0bccc41723c6e33ca`).
It does not import or run ASTRA's `prove.py`, `run.py`, `control.py`, `metadata.py`, the capture drivers, or the
shared role adapter `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes five bodies completely:
  - `002FFCF0`, against its own `.pdata` chain;
  - `00322C50` with its jump table;
  - `00306480`, and the two helpers that read byte +5 (`003060E0`, `00323EC0`).
- It builds a local CFG from direct branches for each body.
- It runs a reverse reaching-definition walk for EAX at the shared return. A call counts as a definition.
- It runs edge-removal reachability, dominance, and path-restricted register-write censuses. These follow
  predecessor paths, not address intervals.
- It runs its own small concrete evaluator. The evaluator executes the image's own class-query instructions for all
  65,536 u16 ids, with an injected descriptor (count 543, count 511, or NULL), and poisons R8 to record every read.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is rechecked
  after all controls.

Raw output: [rv_avail.out](rv_avail.out).

## Re-derived (64 checks, 64 PASS, 0 FAIL; 14 controls among them)

### Bodies

| Claim | Result |
|---|---|
| Complete local body `002FFCF0` + 0x1DF, 479 B | PASS: it decodes exactly, with int3 on both sides. Six `.pdata` records tile it. The first (+0x8B, flags 0) is unchained. The other five are CHAININFO records rooted at `002FFCF0`. The first record alone is 139 B, so a reader that stops at the first record truncates the body. |
| Only a shared reason return and an early constant-2 return | PASS: the local CFG is closed, with no tail jump and no out-of-body branch. Its two rets are `002FFCF0` + 0xBD (shared) and + 0x1DE (early, the last instruction). |
| Class query `00322C50` | PASS: 1025 B of code. Its single `.pdata` record runs on to `00322C50` + 0x484. It covers a 3-byte pad and the 32-entry image-relative jump table at `00322C50` + 0x404. All 32 targets are instruction boundaries. |
| Downstream | PASS: `00306480` (99 B, one record), `003060E0` (595 B, five chained) and `00323EC0` (338 B, five chained) decode exactly. |

### Claim 1: a normal zero return passed class 0x14

| Claim | Result |
|---|---|
| The class-query call dominates the shared return | PASS: `002FFCF0` + 0x9B dominates + 0xBD. The early return is not reachable from the call. |
| The early return is constant 2 and comes before the class query | PASS: + 0x1CF `mov eax, 2`. It is entered only from the five gates at + 0x1F, + 0x28, + 0x42, + 0x64 and + 0x7F. |
| A failed class returns 4 with no later call | PASS: + 0xA0 `test eax, eax` / + 0xA2 `jne`. The fall-through + 0xA4 `mov eax, 4` reaches only the epilogue and ret, with no call and no further EAX write. |
| Return provenance, not "a constant somewhere" | PASS: EAX at + 0xBD has exactly seven reaching definitions: the constants 4, 0x24 and 0x2C, plus four calls. The calls to `0030E9C0` (+ 0x17F), `0031A7B0` (+ 0x197) and `00306480` (+ 0x1AD) reach the ret only through `test eax, eax; jne`, so only when nonzero. **The only zero-capable definition is `00303BD0` at + 0x1C0.** With the class-success edge + 0xA2 -> + 0xBE removed, that call is unreachable. |
| The id is the zero-extended low 16 of entry CX | PASS: + 0x1C `movzx ebx, cx` has no earlier rcx/rbx write. rbx's only other writers are the two restores. + 0x90 `movzx r14d, bx` and + 0x94 `mov edx, r14d` give EDX at the call. |

**Inside the class query.** `00322C50` checks `class - 1 <= 0x1F` (unsigned) and dispatches through the table. ECX =
0x14 selects entry 19, which is `00322C50` + 0x322. That arm loads descriptor `02EBF138` and its count `[+4]`. A NULL
descriptor gives count 0. The shared tail at + 0x3DC accepts `0 <= id <= count - 1`, using signed `jl`/`jg`.

The own evaluator gives these results over all 65,536 ids:

- count 543: exactly 0..542 are accepted, including all of 511..534;
- NULL descriptor: nothing is accepted;
- count 511: exactly 0..510 are accepted.

### Claim 2: R8D = 1 is not read on the class-0x14 path

| Claim | Result |
|---|---|
| R8D = 1 at the class query | PASS: `002FFCF0` + 0x85 `mov r8d, 1`, then + 0x97 `lea ecx, [r8 + 0x13]` (ECX = 0x14), then the call. r8 is written only at + 0x85 and + 0x1A4. |
| The class-0x14 slices do not read R8 | PASS: the static slice has 36 instructions: the entry, the arm, the shared tail and the 0 return. None of them reads R8, and none is a call. Across all 65,536 evaluated ids, the poisoned R8 is never read. |

### Claim 3: the `00306480` RDX is the record loaded at entry, held in RDI

| Claim | Result |
|---|---|
| RDX = q[incoming RDX + 0x698] | PASS: + 0x12 `mov rsi, rdx` and + 0x15 `mov rdi, qword ptr [rdx + 0x698]` (8 B). rdi is written only there and at the two epilogue pops. + 0x15 dominates the call at + 0x1AD. No rdi writer lies on any of the 96 path instructions between them. |
| Later reloads do not replace it | PASS: the only unit+698 reloads are + 0x48 (into rcx) and + 0xC4 (into rax). |
| ECX = the same low-16 id, R8D = 0 | PASS: + 0x1A4 `xor r8d, r8d`, + 0x1A7 `mov rdx, rdi`, + 0x1AA `movzx ecx, bx`. No rbx writer lies on any path from + 0x1C. |
| The byte-5 premise belongs to this record | PASS. `00306480` writes neither rdx nor r8 before calling `003060E0` (+ 0x26). `003060E0` takes the record from RDX (+ 0x21 `mov rdi, rdx`) and reads `byte [rdi + 5]` at + 0x49; + 0x21 dominates that read, with no rdi writer on any path between. `00306480` also passes rbx = the same RDX to `00323EC0` (+ 0x45), which reads `byte [rsi + 5]` at + 0x33. The `pop rsi` at `00323EC0` + 0x28 lies on its class-refusal return, not on that path. A nonzero `003060E0` result becomes 0xF (`00306480` + 0x2F), and `003060E0` returns 5 at + 0x220. |

### Packet integrity

| Claim | Result |
|---|---|
| Manifest and members | PASS: 61 of 61 members match, and the manifest equals the one committed in `2b341ca3a`. |
| Stated facts | PASS: result-02's 479 B, normal returns `0x2ffdad`/`0x2ffece`, call `0x2ffe9d` -> `0x306480` and R8D 0 equal this review. |
| Retained bytes | PASS: the six retained ranges hash to the image. |

## Controls (14, each must FAIL a named check on a privately patched image; all did)

A null control runs first. An unchanged private copy, with the sha check off, passes all 43 image checks. The control
runs use a 17-id boundary set for the evaluator. The packet-side checks are kept out of the control set.

1. `movzx ebx, cx` -> `movsx` (+ 0x1C). Fails the low-16 check.
2. `lea ecx, [r8+0x13]` -> `+0x14`. Fails the class-argument check.
3. `mov r8d, 1` -> `2`. Fails the class-argument check.
4. The class-success `jne` -> `je`. Fails the failed-class check.
5. `mov eax, 4` -> `xor eax, eax`. Fails the failed-class check and "the constants are nonzero".
6. Carrier `[rdx+0x698]` -> `[rdx+0x6A0]`. Fails the carrier check.
7. Reload + 0xC4 rewritten to `mov rdi, [rsi+0x698]`, so a later reload replaces RDI. Fails the rdi census, the path
   check and the reload check.
8. `mov rdx, rdi` -> `mov rdx, rsi` (the outer unit is passed). Fails the `00306480`-argument check.
9. `xor r8d, r8d` -> `mov r8d, ebx`. Fails the same check.
10. `movzx ecx, bx` -> `movsx`. Fails the same check.
11. Arm `mov ecx, [rcx+4]` -> `mov ecx, r8d`, so the class-0x14 arm reads R8. Fails the arm check, the static no-R8
    slice and the evaluator.
12. Tail `jg` -> `jge`. Fails the tail check, and the evaluator now gives an upper bound of 541.
13. The descriptor displacement + 8, another registry slot. Fails the arm check, and the evaluator refuses.
14. `003060E0` `mov rdi, rdx` -> `mov rdi, rcx`. Fails the byte-5 carrier check.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's three CLI refusals and its
three synthetic decoded-record controls were not repeated. These 14 replace them for this review.

## Narrowings

1. **"class20" is decimal 20, ECX `0x14`.** It is table entry 19 (`00322C50` + 0x322), not class `0x20`. Consumers
   should write `0x14`.
2. **543 is a runtime premise, not an image fact.** `02EBF138` lies in `.data`'s virtual tail, so it is 0 at load.
   With a NULL descriptor every id is refused, so the reason is 4, never 0. The bound follows whatever count is
   bound there (511 gives 0..510). "Zero return => 0..542" holds only under the initialized-count-543 premise, which
   the packet states.
3. **Record stability names two callees.** RDI and RBX survive seven callees only by the Win64 ABI: `00377C20`,
   `00322C50`, `00253B90`, `0030D9A0`, `0020E600`, `0030E9C0` and `0031A7B0`. Two of them receive the record pointer
   itself in RCX: `0030E9C0` (+ 0x17F) and `0031A7B0` (+ 0x197). The premise that byte +5 is the same at the
   `00306480` leg as at entry therefore includes "neither writes the record".
4. **A zero return needs more than class 0x14.** It also requires `0030E9C0`, `0031A7B0`, `00306480` and `00303BD0` to
   each return 0. Class 0x14 is one necessary condition, as the packet says, not the whole condition.

**Additions (not narrowings):**

- No instruction anywhere in `00322C50` reads the incoming R8. The one R8 read, `00322C50` + 0x22D, follows its own
  arm's writes. The class-1 arm's call to `00309440` (+ 0x31) would pass the incoming R8 on unchanged. This agrees
  with OPUS's license contract.
- `00323EC0` asks class 0x14 with R8D = 0, and `003060E0` asks it with R8D = 1.
- R8D = 0 at the `00306480` call is not dead. It reaches `003060E0` as its third argument (+ 0x18 `mov ebp, r8d`).

## Limits (kept as the packet states them)

This review supports conditional static facts only. These are premises:

- valid readable unit and parsed records and a private frame;
- an initialized, stable descriptor count of 543;
- the original class-0x14 contract;
- normal nonvolatile ABI behaviour, normal returns, and no interference.

The following remain open and are not awarded:

- any caller, any natural state, and the feasibility of a zero result for 511..534;
- the remaining state, category, licence and cost gates;
- committed producers and override writers;
- loader, I/O, owner and lifetime effects;
- whole OV-42 and OV-21.

No pointer stability or mutation was observed in a running game.

run: `rv_avail.py` at c0bf8acd5 (64 checks, 64 PASS, 0 FAIL, 14 controls; output identical to [`rv_avail.out`](rv_avail.out))
