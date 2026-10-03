# SWE2-AUDIT-SPEC review: ASTRA OV42 prescribed registration event-zero path

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-OV42-REGISTER-EVENT0-1003` (reviews `ASTRA-PUBLISH-REGISTER-EVENT0-1003`) · commit reviewed `0d55f84172d1d16dc9fa1de13177b4c5a5b2ec92`, at HEAD `a19ddeadd`
Package: `_experiments/evidence/ov42-register-event0/` (unchanged since `0d55f8417`). Image pin `73461d08…21f8`, base `0x120000`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The claim holds at the shipping bytes for both prescribed handlers at event 0:

- both read QWORD `[view+48h]` before the event guard;
- neither dereferences that context or the payload;
- there is no call and no explicit non-stack write;
- `EAX=0`, and the entry-relative RSP is restored before `RET`;
- `0029B7D0` leaves `EDX=0`, and `0029B810` leaves `EDX=FFFFFFFF`.

The package says registration is **not** effect-free: `3F89C0` memsets the view and stores `+26/+38/+40/+48` before the conditional call. It keeps OPEN:

- the callback retained by an existing row;
- the transitive effects of event 1;
- initialization, natural reachability, lifetime, scheduling, first draw and presentation.

This is a static path interpretation, not an execution. It grants no whole-OV42 closure.

## SWE2-AUDIT-SPEC identity and integrity

- `manifest.json` hashes to `153a65ee9386436e5e69962241be8adcddc2314b3629fdd5d2fcd6c6b8e1e683`, as named. It lists 98 members, and all match size and sha256 (0 mismatches). The only unlisted file is the manifest itself.
- The drivers are:
  - `prove.py` `251090bba6867a1c99ee7ce84204f9c1c1079ed15c3d0c6b422313787f61d38d`, the repaired producer named on the board;
  - `control.py` `9433f6e3747a3ffb3502c4906d524754c3d078de3b4d1f26be07a3695bebf630`;
  - the retained failed driver `failed-prove-01.py` `8e202981…adcc` and the intermediate `prove-02.py` `bb871aee…af76`.
- `proof-03.status.json` (`0c9ec194…892c`) records the driver `251090bb…`, `terminal: true`, `exit: 0` and `exception: null`. Its stdout is `PROVED: prescribed event0 context-read-only, EAX0; event1 call/event2 store controls detected`, and stderr is empty.
- `control-01.status.json` records the driver `9433f6e3…`, exit 0 and stdout `VALIDATED: five real CLI refusals; old-stack regression; call/write mutations; unknown-predicate refusal`.
- `result-03.json` is `eff5d150…7d84` and `normalized-result-03.json` is `c157f7ff…c456`.

## SWE2-AUDIT-SPEC reproduction

Venv python 3.14.6 with capstone 5.0.7. Outputs went to a scratch directory, and nothing was written into the package.

- `prove.py <scratch>/result-03.json`: exit 0, with the same stdout. Both `result-03.json` and `normalized-result-03.json` are **byte-identical** to the retained files.
- `control.py <scratch>/controls-rerun`: exit 0, with the same stdout.
  - All five CLI children exited 1 with `expected_refusal: true` and no output. Their final stderr lines, in order:
    - `upstream-failed`: `ValueError: required physical producer failed or incomplete`;
    - `extent-incomplete`: `ValueError: physical extent prerequisite incomplete`;
    - `unwind-header-changed`: `ValueError: unsupported or altered physical unwind identity`;
    - `registration-incomplete`: `ValueError: retained registration source prerequisite incomplete`;
    - `coherent-guard-change`: `ValueError: retained original body differs`.
  - The four `path_controls` compare **equal** to the retained `controls-01/result.json`.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (`disr.py`, raw bytes and `.pdata` read independently)

- **Bodies and roots.**
  - `d[29B7D0..+50]` hashes to `f8768931…af1b` and `d[29B810..+82]` to `8ab5f631…603c`, both as stated, and the total is 132 B.
  - `.pdata` (exception directory RVA `0x2E78000`, 35713 rows) has single roots `29B7D0-29B802` and `29B810-29B862`. Both share unwind info `01D52BC8`, header `01 04 01 00`: version 1, flags 0, prolog 4, one code, which is `sub rsp,28h` (a 40-byte private frame).
  - Both ends are followed by `CC` padding.
- **`0029B7D0`, event 0.** `sub rsp,28h` / `mov rax,r8` / **`mov r8,[rcx+48h]`** / `cmp edx,1` / `jne 29B7FB` → `xor eax,eax` / `add rsp,28h` / `ret`.
  - The `+48h` read precedes the guard.
  - `rax` takes the payload but is never dereferenced.
  - `EDX` is unchanged at 0.
- **`0029B810`, event 0.** `sub rsp,28h` / **`mov r9,[rcx+48h]`** / `mov r10,r8` / `sub edx,1` (EDX becomes `FFFFFFFF`, ZF=0) / `je` not taken / `cmp edx,1` / `jne 29B82F` → `xor eax,eax` / `add rsp,28h` / `ret`.
  - The read again precedes the guard, and there is no dereference of `r9` or `r10`.
- **Positive detector sites.**
  - Event 1 in `29B7D0` falls into `29B7E0…29B7EA call 2973E0`.
  - Event 2 in `29B810` gives `sub edx,1` = 1 and `cmp edx,1` equal, which leads to `29B825 mov eax,[r9+2Ch]` / `shl eax,4` / **`29B82C mov [rcx+4],eax`**.
  - Both boundaries exist exactly where the controls stop.
- **Registration call `003F89C0`.**
  - `memset(view,0,58h)` at `3F89E5`, then `or word [rsi+26h],1`, `mov [rsi+38h],rax` (the fifth-argument callback), `mov [rsi+40h],ebx` and `mov [rsi+48h],rdi` (context = incoming `r9`).
  - Then `test rax,rax / je 3F8A0E`. On the non-NULL path, `mov r8,rbp` / `xor edx,edx` / `mov rcx,rsi` / `call rax`.
  - So `RCX=view`, `EDX=0` and `R8` = the payload. Because `3F89D4` is `mov ebp,edx`, that payload is the **zero-extended 32-bit second argument** of `3F89C0`.
  - Under non-interference, the `+48h` the handler reads is the context just stored at `3F89FB`. "Not whole-registration-effect-free" is correct.

## SWE2-AUDIT-SPEC control sensitivity

- **Old vs. new relative-stack control.**
  - The defect is the unsigned masking of the relative RSP. The retained failed tracer returns `pre_ret_rsp_delta = 18446744073709551616` (2^64), and the corrected tracer returns 0, on the same `29B7D0` bytes.
  - The producer requires a delta of 0, so the old model would have refused a correct body. **Sensitive.**
  - My extra mutation `29B7FD add rsp,28h`→`add rsp,20h` gives delta `-8`, which the producer refuses.
- **Event-0 discriminators.**
  - `83fa01`→`83fa00` makes primary event 0 reach the `CALL 0x2973e0` boundary.
  - `83ea01`→`83c201` makes secondary event 0 reach `OBJECT_WRITE 0x29b82c`.
  - Both show that a guard change is visible to the path result. **Sensitive.**
- **Unknown predicate.** `83fa01`→`83f801` (`cmp eax,1`, with `rax` symbolic) is refused with `unknown predicate: no path claim`. So no claim is made from an unknown flag. **Sensitive.**
- **CLI refusals.** `coherent-guard-change` recomputes the extent's body sha. It is refused because the producer compares the retained body with the **image** (`original(a,len(z))!=z`), not just with a stored hash. This is a real image-bound check. The other four exercise distinct prerequisite fields.
- **Extra reviewer mutations** (`scratch/ov42e0/mutate.py`):
  - `29B7FB xor eax,eax`→`xor ecx,ecx` returns `eax='payload'`, which the producer refuses.
  - An `rbp`-based store on the path is refused (`unhandled memory destination`). The tracer refuses every memory-destination instruction, so its `rbp` exclusion from `OBJECT_WRITE` has no effect.
  - One gap, which does not touch the facts: `29B7D4 mov rax,r8`→`mov rcx,r8` makes the `+48h` read follow the **payload**. The tracer still reports the identical footprint `('rcx',0x48,8,'r')` and **accepts**. The footprint check keys on the base register's *name*, not its symbolic value.
  - On the shipping bytes, `rcx` is not written before `29B7D7`/`29B814` on either path, so "reads view+48, does not follow context/payload" stands, on this review's reading of the bytes.

## SWE2-AUDIT-SPEC claims audit

- Both handlers read QWORD `view+48` before the event guard, and neither follows context/payload: **holds**, at the bytes.
- No call or non-stack write, `EAX=0`, entry-relative RSP restored, primary `EDX=0` and secondary `EDX=FFFFFFFF`: **holds**.
- Volatile flags and registers may change, the implicit `RET` access is a premise, and an invalid receiver can fault: **stated correctly**.
- The README and result `limitations` keep an existing row's callback, event-1 transitive effects, native fill, lifetime, scheduling, actual reach and presentation OPEN. No new-experiment credit is taken, and the failed `proof-01` is kept as history and not counted. **No overclaim.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Wording precision for consumers.** "R8 = the supplied payload" at the registration call is the zero-extended 32-bit second argument of `3F89C0` (`mov ebp,edx` / `mov r8,rbp`), not a pointer-width parameter. Neither event-0 path uses it.
- **Tracer.** Record the symbolic value of each memory base (`registers[base]`) in the footprint, and require `'view'` for the `+48h` read. Then a base-register reassignment cannot pass as a receiver read. Add the `mov rcx,r8` mutation above as a FAILS control.
