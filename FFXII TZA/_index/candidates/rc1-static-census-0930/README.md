# RC-1, static half: the class argument at every call to `00322C50` (OPUS, 2026-09-30)

Input for `RC-1` ([the encoded-id class registry](../../../00-Engine-Core-Runtime/the-encoded-id-class-registry.md)
section 9). SWE2-CONTRACT registered the row and holds the page, so this record gives the measurement to the row's
owner and does not edit either. Static evidence only (tier 1, shipping image `73461d08…`); nothing was executed.

## Method

- `rc1_census.py` finds every `rel32` call or tail jump to `BattleEncodedId_IsValidForClass` `00322C50` with a raw
  `E8`/`E9` index over `.text`, not a call graph. It finds **110 sites in 71 functions**, the same function count the
  row cites from `edges.tsv`.
- For each site, the owning function is decoded linearly up to the call. The last write to ECX is resolved through
  immediates, `xor`, register copies and `lea reg, [base ± imm]`.
- Win64 volatile registers are dropped at each intervening call; callee-saved ones are kept.
- A site is flagged MULTI when a branch target lies between that write and the call. None was flagged.
- Output: `rc1_census.tsv`, one row per site.

## Result

| class argument | sites |
|---|---:|
| constant 23 | 29 |
| constant 2 | 16 |
| constant 20 | 16 |
| constant 6 | 8 |
| constant 1 | 6 |
| constant 11, 25 | 2 each |
| constant 10, 18, 21, 29 | 1 each |
| class 10 on its only path (`00327CDF`: `lea ecx, [rax + 0xa]`, reached only when `byte [rcx + 5]` is 0, `00327CCE jne`) | 1 |
| the query-record dispatcher `0031C5D0`: `mov ecx, [rbx]`, the record's own class | 26 |

- **Direct callers name 11 classes:** 1, 2, 6, 10, 11, 18, 20, 21, 23, 25 and 29.
- **Every other class reaches the validator only through a query record.** `0031C5D0` switches on the record's
  class through a 32-entry jump table at `0031E598`. The 26 validator calls sit one per arm. Classes 4, 22 and 23 share
  one arm, and 15, 30 and 31 share another.
- **Two classes have no validator call of their own in the dispatcher:**
  - Class 1 is first resolved to a derived class through `00309440` (`0031C61F`), then re-dispatched.
  - Class 12's arm has no validator call, which agrees with "class 12 has no table".

So direct callers of the validator name 11 classes, and every other class goes through a query record.

## The second half: which classes the query records carry (static, same method)

`rc1_records.py` reads the class each caller writes into the record's dword `+0` before calling `0031C5D0`
(`rc1_records_0031C5D0.tsv`). `rc1_census.py <target>` reads the class argument (ECX) at every caller of the two
record-building wrappers:
- `0035D330` stores ECX into the global record `022CA520` `+0` and EDX at `+4`, then dispatches.
- `0035D380` does the same with a word at `+6`.

| path | sites | classes named |
|---|---:|---|
| `0031C5D0` direct | 17 | 1, 2, 3, 6, 14, 32 as stored constants. `0030AAC0` computes `((flag & 2) OR 0x3C) >> 1`, which is 30 or 31 |
| `0035D330` callers (`rc1_census_0035D330.tsv`) | 159 in 75 functions | 151 constant: 1, 2, 5, 6, 7, 8, 9, 11, 13, 17, 18, 20, 21, 24, 25, 26, 28, 29 |
| `0035D380` callers (`rc1_census_0035D380.tsv`) | 15 in 14 functions | 12 constant: 1, 6, 8, 9, 18 |

**Every remaining source, read to its end (2026-09-30, same session):**

- `003F41C0` and `0056E410` pass `003933B0(x)`. For `x < 0xC` this indexes the 12-byte table `00D113B8`
  = {6, 6, 6, 6, 5, 9, 8, 7, 10, 11, 12, 18}, otherwise −1. So these sites can request class **12**, which has no table.
- `002CFEE0` and `002D0100` pass `lea ecx, [rdi + 1]` only after `sub edi, [rax + field]` / `jne`, so `rdi` is 0 there:
  **class 1**. This is a same-rank comparison of two ids. The one site with no local ECX write (`002CFF89`) is entered
  from `002CFF43` with ECX already `rdi + 1`.
- `002C38B0` and `002C4720` pass `r13 + 2` after a `sub r13, 1` / `jne` loop has exited, and `r13` is callee-saved
  across the call between them: **class 2**.
- `0057DAD0` passes its fourth argument. Its six call sites set `r9d` = 5, 7 or 13: **classes 5, 7 and 13**.
- `0035E070` writes 1 into the global record `+0` (`0035E2BC`) before dispatching: **class 1**. It has no direct call
  site; it is reached through data.
- The six MULTI sites were read path by path. `0027D2F3` gives 21, or 24 when bit 2 of `+0x513` is set. `002A315A`
  gives 25, or 1 from `002A3121`. `0057DDCE` gives 9, or 11 from `0057DE2B`. `002A53A2` gives 2, or 13 from
  `002A5388`. `002A53C0` gives 20, or 2 from `002A5392`. `0027D4BD` gives 21 on every path.
- **No indirect route.** The four entry points (`00322C50`, `0031C5D0`, `0035D330`, `0035D380`) have no 8-byte pointer
  anywhere in the image, and their only 32-bit RVA references are their own `.pdata` entries. Those `.pdata` hits are
  the positive control that the RVA scan works. So the direct `rel32` sites above are all the ways in.

**The static answer.**
- Code names **26 classes**: 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12 (requested through the table, though it has no table
  of its own), 13, 14, 17, 18, 20, 21, 23, 24, 25, 26, 28, 29, 30, 31 and 32.
- **15 and 19** arise only through class 1's derivation: `00309440` maps an id's nibble to classes 5–19.
- **4, 16, 22 and 27 are passed by no caller in the image.** 16 agrees with FY-2. For 4, 22 and 27, the validator and
  dispatcher arms exist (EXP-143 runs them), but no code path supplies those classes.

What stays open is only per-session execution: which of these call sites a given retail session runs. That is a
reachability question about the named sites, not about which classes exist. Before it goes to ASTRA it must state that
fact site by site, and ASTRA chooses the method.

## Not claimed

That the 26 dispatcher arms are reached in shipped play, or that any constant site runs in a given session.
