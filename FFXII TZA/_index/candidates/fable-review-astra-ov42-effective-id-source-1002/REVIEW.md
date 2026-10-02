# FABLE review: ASTRA ov42-effective-id-source

- **Packet:** [ov42-effective-id-source README](../../../_experiments/evidence/ov42-effective-id-source/README.md)
- **Producer commit:** `2cce275ad`. The manifest sha256 begins `d548df12a842f390` and equals the committed manifest.
  All 49 members hash as listed. The packet's range hashes equal the certified image's bytes: the getter
  `00387090` .. + 0x95, the resolver `0031B860` .. + 0x53, and the retained caller ranges `00304850` + 0x520 .. + 0x5D9
  and `0030EEA0` .. + 0x65. `retained-callers-01.json` is byte-identical to `0ada5145`'s
  `retained/slot-acquisition-callers-raw-01.json`.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes: the carriers, load widths, the `0x9F`
  compare, the table-pointer test, the two separate resolver calls, both NULL paths and the AX → R8D transfer.
  A concrete emulation of the original getter and resolver, and of the caller's straight line through them, agrees
  on every case tried. The narrowings place the caller fragment inside a phase case, state when the table pointer
  can be zero, and add two side facts and the getter's other direct callers. None of them contradicts the packet.

## Method

[rv_effid.py](rv_effid.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It does not import or run
ASTRA's `prove.py`, `prove_owner_reload_order.py`, `feasibility.py`, `control.py`, capture drivers, freeze or
publication scripts, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes both bodies completely. Each is bound by the
  image's own `.pdata` and by int3 padding up to the next root record. Their local CFGs are checked closed.
- It takes register-write censuses for the query (RDI), the table pointer (RBX) and the owner returns (RAX). It also
  takes a compare census and lists every memory write.
- It follows `00304850`'s `.pdata` chain to its end and decodes the whole chained body. It reads the body's one
  indirect jump (a phase switch) and its table. It then checks every direct and table branch target against the
  straight line that carries the query into the getter and the getter's AX into R8D.
- It emulates the **original** getter and resolver (unicorn) over synthetic query records, units and tables, with
  a scripted unit registry. The registry's count and by-index helpers `00236850` / `00236820` are stubbed by a code
  hook, and they are the only code not run from the image. It also runs the caller's straight line
  `00304850` + 0x5AD .. + 0x5D4 through both bodies.
- It runs a raw `E8`/`E9` rel32 and `0F 8x` census over `.text` for direct references to both bodies.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_effid.out](rv_effid.out).

## Re-derived (62 checks, 62 PASS, 0 FAIL; 16 controls among them)

### Bodies

| Claim | Result |
|---|---|
| Getter `00387090`, 149 B | PASS: it decodes exactly. Three `.pdata` records tile it: the root `00387090` .. + 0x6 and two CHAININFO records + 0x6 .. + 0x6B and + 0x6B .. + 0x95, both rooted at `00387090`. int3 padding follows to the next root `00387130`. It has two rets (+ 0x87, + 0x94), no tail and no indirect jump. Its only calls are `0031B860` at + 0x2F and + 0x5C. |
| Resolver `0031B860`, 83 B | PASS: one `.pdata` record, int3 padding to the root `0031B8C0`. It has two rets (+ 0x15 and + 0x52). Its only calls are `00236850` (+ 0x1D, + 0x3D) and `00236820` (+ 0x28). |

### The getter

| Claim | Result |
|---|---|
| The query is the incoming RCX, kept in RDI | PASS: the RDI home save is at + 0x6 and `mov rdi, rcx` at + 0xB. RDI is written only there and at the reload + 0x61. There is no RCX write before the first call, and the second call takes `mov rcx, rdi` (+ 0x59), the instruction before it. |
| Query leg: `+5` == 0 selects `0208D480` + BYTE `+4` * 64, with no first call | PASS: there is `test rcx` / `je` and a BYTE `+5` `test` / `jne`, both to the first call. Then `movzx ebx, byte [rcx+4]`, `lea 0208D480`, `shl 6`, `add`, and a `jmp` to + 0x59 past the first call. Emulated: one resolver call, and `02EBF188` is untouched. |
| Otherwise O1 → `02EBF188`; non-null O1 selects `0208DE80` + BYTE `O1+0xEA9` * 64; null O1 gives RBX = 0 | PASS: the QWORD store is at + 0x34, then `test rax` / `je` to `xor ebx, ebx` (+ 0x57). Emulated: `02EBF188` = O1, or 0 for a null O1. |
| RBX is the table pointer at the test | PASS: RBX is written only on the two legs and by the two `pop rbx`. Nothing writes it between the second call and `test rbx, rbx`. |
| Valid O2: zero-extended WORD `O2+0x714`, except `0x9F` with RBX != 0 → WORD `RBX+0x10` | PASS: `test rbx` / `je` + 0x88, then `mov ecx, 0x9f` and `cmp word ptr [rax+0x714], cx` (2 bytes) / `jne` + 0x88. Else `movzx eax, word ptr [rbx+0x10]` (2 bytes) and ret. + 0x88 is `movzx eax, word ptr [rax+0x714]` (2 bytes) and ret. It is the target of all three branches. No RAX write comes between the second return and a result load. Emulated: table word `8123` comes back as RAX = `8123`, not sign-extended. |
| RBX = 0 returns `0x9F` directly | PASS (emulated): with O1 null and O2's word `0x9F`, the result is `0x9F`. |
| No local candidate bound | PASS: there are six tests, on the query, BYTE `+5`, O1, O2 and RBX, plus the one WORD compare with `0x9F`. The `+0x714` word is touched only by that compare and the + 0x88 load. Emulated on both table legs: each of 511..534 is returned unchanged with RAX's upper half zero. So are 0, 9E, A0, 19F, 7FFF, 8000 and FFFF. |
| O1 and O2 are separate | PASS (emulated): the registry changes between the calls (O1 = unit A in slot 5, O2 = unit B in slot 9, B's word `0x9F`). The getter returns A's slot record `+0x10` (`555`), not B's (`999`). The table follows O1 and the word follows O2. |
| No safe NULL return | PASS: `je` + 0x88 at + 0x69 goes straight to the load through RAX. Emulated: `getter(NULL)` makes both resolver calls with no registry callback, writes 0 to `02EBF188`, and then reads address `0x714` (an unmapped-read fault in the emulator). A non-null query with no matching owner also reads `0x714`, even with a nonzero table pointer. |
| Writes | PASS: the getter writes only the RDI home slot, the `push rbx` and the QWORD `02EBF188`. Both rets restore RBX and RSP. |

### The resolver

| Claim | Result |
|---|---|
| NULL query returns 0 before any registry call | PASS: `test rcx` / `jne` (+ 0x9 / + 0xC). NULL falls to `xor eax, eax` and ret, and no call is reachable from there. |
| Otherwise a unit whose QWORD `+0x698` equals the query, or 0; count re-read | PASS: EBX = 0, then the count call, `jle` → 0. The loop does ECX = EBX, the by-index call, skips a null entry, and compares `cmp qword ptr [rax+0x698], rdi` (8 bytes) / `je` to the return of that RAX. Else `inc ebx`, the count is re-read (+ 0x3D), and a signed `cmp ebx, eax` / `jl` closes the loop. Emulated: with entries [NULL, key 77, key 99 (A), key 99 (B)] it returns A, the first match, after three count calls. No match, or an empty registry, returns 0. Its only write is the RBX home slot. |

### The caller

| Claim | Result |
|---|---|
| The getter call sits in an interior fragment of `00304850` | PASS: the `.pdata` chain has seven records, `00304850` .. + 0x828 (root + 0xA6, then six CHAININFO records rooted at `00304850`). The call (+ 0x5C2) lies in the chained record + 0x520 .. + 0x741, and + 0x520 is not a root record. See narrowing 1 for where in the routine it sits. |
| + 0x5AD loads the query from unit `+0x698` | PASS: `mov rcx, qword ptr [rdi+0x698]` (8 bytes). Neither of the two instructions before the call (`or dword [rdi+4], 0x80`, `movzx ebx, byte [rdi+0xea9]`) writes RCX. |
| + 0x5CA zero-extends AX into R8D, then + 0x5D4 calls `0030CFB0`, with no call between | PASS: the line is `call 00387090`, `mov edx, [rdi+8]`, `movzx r8d, ax`, `mov r9d, ebx`, `mov rcx, r12`, `call 0030CFB0`. Its only calls are at the two ends. RAX is not written before + 0x5CA, and R8 is written only there. Emulated from + 0x5AD: the run reaches `0030CFB0` with R8 = the getter's result (upper bits zero), RCX = R12, EDX = unit DWORD `+8` and R9D = unit BYTE `+0xEA9`. Each of 511..534 arrives as R8 unchanged. |

### Manifest

PASS. The manifest sha256 begins `d548df12a842f390`, it equals the manifest at `2cce275ad`, and all 49 members match.

## Controls (16, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy, with the sha check off, passes all 37 image checks.

1. `mov ecx, 0x9f` → `0xA0` (`00387090` + 0x70). Fails the substitution check and the emulated `0x9F` cases.
2. The + 0x88 WORD read → BYTE read. Fails the direct-leg check and the emulated candidate checks.
3. The table word `+0x10` → `+0x12`. Fails the substitution check and the emulated `0x9F` cases.
4. The table load `movzx` → `movsx`. Fails the substitution check and the zero-extension case (`8123`).
5. The table-pointer `je` → nops. Fails the substitution and direct-leg checks and the emulated null-O1 case.
6. The O2-null `je` + 0x88 → `je` + 0x82, a safe return of 0 that the code does not have. Fails the O2, direct-leg
   and no-sentinel checks and the emulated NULL faults.
7. The second resolver input `mov rcx, rdi` → `mov rcx, rax` (O1 passed as the query). Fails the query-carrier
   check and the emulated checks.
8. The table index BYTE `+4` → `+5`. Fails the query-leg check and the emulated table cases.
9. The query bank `0208D480` → `0208D4C0`. Fails the query-leg check and the emulated table cases.
10. The O1 cell `02EBF188` → `02EBF190`. Fails the O1-leg and write-census checks and the emulated O1 cases.
11. The resolver's null-query `jne` → `jmp`. Fails the resolver NULL check and the emulated `getter(NULL)` case.
12. The resolver's key `+0x698` → `+0x6A0`. Fails the scan check and every emulated owner case.
13. The resolver's match `je` + 0x48 → + 0x46 (a match returns 0). Fails the scan check and the emulated cases.
14. The caller's `movzx r8d, ax` → `movzx r8d, bx`. Fails the line check and both emulated caller checks.
15. The caller's `mov r9d, ebx` → `mov r8d, ebx` (an R8 write after the transfer). Fails the line and
    "R8 written only at + 0x5CA" checks and the emulated caller check.
16. The caller's query `+0x698` → `+0x6A0`. Fails the line check and the emulated caller checks.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's four CLI refusals and seven
source mutations were not repeated; these 16 replace them for this review.

## Narrowings

1. **The caller fragment is phase case 6 of a 13-way switch.** `00304850`'s one indirect jump (+ 0x10A) dispatches on
   BYTE `[rsi+4]`, bounded by `cmp eax, 0xc` / `ja`. Its table is 13 DWORD RVAs at image base + 0x1E5044 =
   `00304850` + 0x7F4, and the table ends exactly at the chain end + 0x828. Those last 0x34 bytes are data, not code.
   Entry 6 is + 0x555. No other table entry, and no direct jump or jcc in the body, lands in + 0x555 .. + 0x5D4,
   except the case's own `jne` + 0x55E → + 0x56D. Case 5 (+ 0x523) also falls through into + 0x555 after
   `inc byte ptr [rsi+4]`. The packet's retained prefix starts at + 0x520, the instruction just before case 5's entry. This places
   the line; it does not prove a natural caller. RDI, RSI, R12 and the phase byte remain premises.
2. **The table pointer is zero only when the first resolver returned NULL.** The query leg forms `0208D480` + 64*k
   (k <= 255) and the O1 leg forms `0208DE80` + 64*k. Neither can be 0. So for a non-null query with BYTE `+5` = 0,
   a valid O2 word `0x9F` is always substituted. `0x9F` comes back unchanged only on the resolver leg with a null O1.
   The index is a raw byte in both legs, with no bound in the getter. The type store's 40 / 32 record counts for the
   two banks are not enforced here.
3. **Two reads, one write.** The `0x9F` compare (+ 0x75) and the returned direct word (+ 0x88) are separate WORD
   reads of `O2+0x714`; they agree only under the stable-owner premise. The getter writes `02EBF188` on every
   resolver-leg call, including 0 for a null O1, and never on the query leg.
4. **The getter has three raw direct callers.** They are `00304850` + 0x5C2 (the packet's), `00304850` + 0x67C (the
   later case, whose AX goes to EDX through `movzx edx, ax`) and the unit display-record builder `00329220` + 0x738.
   Only the first is read for the transfer. Indirect callers are not covered. `0031B860` has 136 raw direct
   references, two of them the getter's. `00304850` has one raw direct caller, `00307BE0` + 0x39. The getter never
   calls it: its only calls are the two resolver calls. So the handler-table page's "`00304850` both calls and is
   called by" the getter is wrong in its second half for direct calls (see the consumption draft).
5. **Which unit O2 is.** The caller's query is its unit's own QWORD `+0x698`, and O2 is the *first* registry unit
   with that `+0x698`. O2 is the caller's own unit only if that unit is registered and no earlier entry shares the
   key. That is not established.

## Limits (kept as the packet states them)

This review supports conditional static facts, plus emulation of the original bytes on synthetic state. The following
remain open and are not awarded:

- a safe NULL return: there is none, and no natural NULL caller or observed fault is claimed;
- table initialization, contents and usable extent, and the meaning of record `+0x10`;
- natural action-id values at `+0x714`, and that field's writers and their admission (the next frontier);
- stable owner identity: O1 and O2 are separate call results, and owner lifetime, reuse and registry order are not
  read;
- a complete caller: the retained prefix is an interior fragment, and narrowing 1 places it without proving its entry
  state;
- command acceptance, execution or rejection, and whole OV-42.

Valid, readable, stable query, owner, table and frame accesses, the normal native ABI and preserved nonvolatile
registers are premises.

run: `rv_effid.py` at HEAD a7cb39140 (62 checks, 62 PASS, 0 FAIL, 16 controls; output identical to [`rv_effid.out`](rv_effid.out))
