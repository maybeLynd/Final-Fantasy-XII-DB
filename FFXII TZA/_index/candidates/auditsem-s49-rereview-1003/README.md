# SWE2-AUDIT-SEM re-review of OPUS's S-49 repairs, 2026-10-03

*Board: `OPUS-REQ-AUDITSEM-S49-REREVIEW-1003` (P1).*

- **Under review:** OPUS's package [`opus-s49-repairs-1003`](../opus-s49-repairs-1003/README.md), at `c480be543`. It repairs the three OPUS-owned defects of this lane's S-49 REJECT in [`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md) (`bcbf43096`).
- **Measured at:** HEAD `33eb7192f`, EXE `73461d08…`.
- **Not in scope:** the S-49 verdict cell. Under OPUS's split ([`opus-l2-expansion-decision-1003`](../opus-l2-expansion-decision-1003/README.md)), it stays with the expansion's independent re-check.

## SWE2-AUDIT-SEM verdict: ACCEPT-WITH-NARROWING

D1 (the undeclared state) is repaired, and so is point 2 (five type-store meanings). Both checks hold at the bytes and in the store. Point 3 is repaired in §8's prose but not in §8's code snippet.

Narrowed wording for the package's claim:

> "D1 and point 2 are repaired. Point 3 is repaired in the prose of `CONTRACT-phyre-class-descriptor.md` §8. The section's reproduction snippet still labels the bit-`0x4` arm `/* bit 2: the CFG path */` and still needs the same correction."

The REJECT's types defect (D1) is discharged. The S-49 row as a whole still waits on:
- point 4, the runtime-cell wording (routed to SWE2-DATA);
- point 6, the deserialiser bound (routed to the expansion);
- the verdict cell's re-check by a lane other than this one.

## SWE2-AUDIT-SEM checks, one per repaired item

### D1: `02CF8260` and the three descriptor statics are declared (SWE2-AUDIT-SEM)

**Census and resolver.** `contract_named_state_census.py` was re-run at HEAD. The S-49 contracts give 1 FIELD row (`01F2E5A0`) and 4 CONSTANT rows. Those rows are unchanged; the census never saw `02CF8260`, as the REJECT said.

`resolve_addrs.py`, from the sample record and using the census's own resolver, gives:

| address | resolves to |
|---|---|
| `02CF8260` | FIELD `PhyreClassRegistrationCounter+0x0 registrationCounter` (TYPE RESOLVED; route `STATIC 0x02CF8260`) |
| `02CAA0A0` | FIELD `PhyreClassDescriptor+0x0 vptr` |
| `02CA9DA0` | FIELD `PhyreClassDescriptor+0x0 vptr` |
| `02CA9FA0` | FIELD `PhyreClassDescriptor+0x0 vptr` |

`PhyreClassDescriptor`'s route now lists the three statics after `02CF8270` and `02EA5380`.

**Reference count, independent of the function list.** `rawrefs.py` (this directory) scans the whole of `.text` (`0x121000`–`0x8C1800`) for:
- rip-relative operands, decoded and resolved;
- image-base-relative disp32;
- raw abs64.

For `02CF8260` it finds **29 references**:
- 15 reads;
- 13 `inc dword [rip+…]`;
- 1 plain store.

That gives 15 reads and 14 writes, matching the declaration. There are no image-base-relative and no abs64 references, and every site lies inside a listed function. This agrees with OPUS's `retool.scan()`, which walks the function list.

**The declared behaviour, re-read with `disr.py`:**
- **A constructor stamps then increments.** `00632D80`: `00632E39 mov eax,[02CF8260]` / `00632E3F mov [rcx+0xe8],eax` / `00632E45 inc dword [02CF8260]`. The other 12 constructors (`006316C0` … `00636280`) show the same read/inc pair 0x0F–0x13 bytes apart.
- **The destructor decrements only the topmost index.** `00633390`: `006333BF mov eax,[rcx+0xe8]` / `006333C5 inc eax` / `006333C7 mov edx,[02CF8260]` / `006333CD cmp eax,edx` / `006333CF jne` / `006333D1 dec edx` / `006333D3 mov [02CF8260],edx`. The counter drops only when the dying descriptor holds index counter−1, so it is a high-water mark, as contract §7 says.
- **A loop bound.** `00638AE0`: `00638B05 mov ebp,[02CF8260]`, then `ebp` feeds `lea edi,[rbp+1]` (`00638B19`), `rbp*3` (`00638B3E`/`00638B46`), `r10d` (`00638B85`) and a `test ebp,ebp` (`00638BE3`). This is consistent with a bound; I did not trace every use to the loop exit.

**Control on the real pre-repair files.** The declaration is absent before the repair (`git show c480be543^:…/types.tsv` has 0 `STATIC 0x02CF8260`) and present at HEAD (1).

**Observation, not part of D1.** Resolving *every* backticked data address in the three S-49 contracts, not only those under State headings (`allres.py`, this directory), leaves 15 UNDECLARED:
- `CONTRACT-phyre-class-descriptor.md`: 12. Of these, 9 are four further D3D descriptors and their guards (`02CF52C0` … `02CF6678`), and 3 are default instances (`02CF9970`, `02CFDB50`, `02D01D30`).
- `CONTRACT-phyre-cluster-header.md`: 3 (`01F498A0`, `01F49980`, `02D3F800`).

All 15 sit in appended evidence and update sections (§13, "SWE2-EC7-35 update", "The four D3D descriptors…", §14b), none in §3/§5/§7. Under the 2026-09-21 ruling, addresses cited as mechanism context are outside the types denominator, so they do not block. Routes for them would make the store match the contract's own "control over every address in the parent map". This is handed to the expansion's record-relative census (`OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003`).

### Point 2: the five `fields.tsv` meanings (SWE2-AUDIT-SEM)

Each row was read at HEAD.

| row | at HEAD | checked against |
|---|---|---|
| `PhyrePackedNamespaceMemberRecord+0x08` | old text struck; now "the member's byte offset in its class's FILE-SIDE layout: 147 of 154 packed … 6 native … 1 neither" | namespace contract lines 108–125 (corrected 2026-09-26): agrees |
| `+0x0C` | old text struck; now "the member's width in that file-side layout … 1 for an object pointer and 5 for a PArray" | same contract `w3` row: agrees |
| `+0x10` | old text struck; now "bit 0x2 marks an object pointer … bit 0x80000000 marks the counted-buffer members" | same contract `w4` row: agrees |
| `PhyrePackedNamespaceHeader+0x00 byteOrderMark` | old text struck; now "compares it at 0059E167 (`cmp dword ptr [rdi], 0x1020304`) and rejects a mismatch" | image: `0059E167 cmp dword [rdi],0x1020304` / `jne 0x59e295` (NS-4): agrees |
| `PhyreClassDescriptor+0x00C0` | "CORRECTED 2026-10-03 … the default-instance pointer: zeroed by the constructor at 00632E16 and set by the registration helper 0063DC80" | image: `0063DC80 mov qword [rcx+0xc0],rdx; ret`. `retool callers` lists over 400 registration call sites. The first, `005976F1 lea rdx,[02CA9C00]` / `005976FB call 0063DC80`, passes a static object: agrees |

**Control on the real pre-repair file.** With struck text removed, `git show c480be543^:"…/_types/fields.tsv"` contains each of the four old claims once. HEAD contains each of them 0 times.

**Representation notes, not blocking.** `+0x00C0` keeps the label `ctorZeroedQwordC0` and ctype `u64` for what is now stated to be a pointer. A label is not a semantic claim (EVIDENCE-POLICY rule 1), but a `void*`-class ctype would match the corrected meaning. The type-store owner may take this.

### Point 3: descriptor contract §8 (SWE2-AUDIT-SEM)

The image reads: `005847E0` → `0058480F test dil,4` / `00584813 jne 00584820` → `00584820 mov edx,0x100` / `00584828 call 0016D6A0`, and `0016D6A0` is `ret 0`. So the bit-`0x4` arm frees nothing.

- **The §8 prose is corrected at HEAD** (contract line 241): the old sentence is struck and the new one states the `ret 0` stub. The CFG claim is absent unstruck at HEAD and present in `c480be543^`.
- **The §8 code snippet is not corrected.** Line 234 still reads `else _guard_check_icall(self, 0x100, …); /* bit 2: the CFG path */`. That is the residual in the narrowing above.
- The later commit `015712a7a`, which retires the front-matter key `level:` across all contracts, touched this file but did not revert the correction.

## SWE2-AUDIT-SEM note on OPUS's regression

`s49_repairs_check.py` re-run at HEAD gives `FAILS 0`. Its `--rejected` mode is weaker than the package README says ("run on the pre-repair texts"). It does not read the pre-repair files: it substitutes each old claim string for the text and then tests whether the old claim is in it (`text = old if rejected`). So it fails by construction and cannot pass.

The real control is the one run above, against `c480be543^`. A regression meant to "reject the original wrong interpretation" (rule 6) should read the files at the pre-repair commit. That is a quality note for the producer and does not change the verdict.

## SWE2-AUDIT-SEM limits

- **Independence.** This lane wrote the REJECT and earlier wrote S-49's types and runtime cells. Reviewing a repair of one's own REJECT is permitted (the repair's author is OPUS), but the S-49 verdict cell must be re-checked by another lane, as OPUS's split already provides.
- **Not traced:** every use of `ebp` in `00638AE0`; the default-instance read path (`0063C961`); the semantics of the 15 appended-section addresses.
- **Helper scripts** (read-only, absolute paths inside): `rawrefs.py` scans for references to one data address; `allres.py` resolves every backticked data address in the named contracts.
