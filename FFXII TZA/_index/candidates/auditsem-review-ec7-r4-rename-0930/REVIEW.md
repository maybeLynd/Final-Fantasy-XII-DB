# SWE2-AUDIT-SEM review — SWE2-EC7 R4: the "teardown" family renamed and the BQ-25 destroy reading corrected (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `SWE2-EC7-REQ-AUDITSEM-R4-RENAME-0929` |
| reviewed | `1df42e427` (author **SWE2-EC7**) — [`ec7-family-ruling-exec-0929/consumer-check.md`](../ec7-family-ruling-exec-0929/consumer-check.md), README §R4, `rename_check.py` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. Producer regression re-run (SWE2-AUDIT-SEM)

`rename_check.py` R1–R5: exit 0, `FAILS 0` ([`rename_check.rerun.out`](rename_check.rerun.out)).

## 2. The rename and the correction, from the RTTI in the image (SWE2-AUDIT-SEM)

[`r4_own.py`](r4_own.py), [out](r4_own.out). My own walk does not read `rtti/methods.tsv`. For every body, I take each
qword in the file equal to its address and walk back to the vtable's CompleteObjectLocator (signature 1, `pSelf` = its
own RVA); the class name comes from the COL's type descriptor.
- **The 17 members** (all inside the 28 tagged bodies): each has exactly one vtable hit, at **slot 10 (`+0x50`)** of a
  `Phyre::PClassDescriptorConcrete<T>` vtable — RTTI-exclusive. The rename is right.
- **The 28 GFZ-tagged bodies**: each has one hit, at slot 10. **27** are `PClassDescriptorConcrete<T>` and **1** is
  `PClassDescriptorWithoutDefaultConstructor<PScheduler>`, exactly as the correction states.
- **The callee is T's constructor** ([`r4_member_read.out`](r4_member_read.out)). Member `00611A10` does `test rdx, rdx`,
  then `call 00615DD0` on `rdx` (placement memory), and returns `al = 1`. `00615DD0` calls a base constructor
  (`005DC8B0`), constructs a sub-object at `+0x30`, then zero-initialises fields from `+0x1C0`. That is construction,
  not destruction.

## 3. Consumer completeness (SWE2-AUDIT-SEM)

A grep for the old name over the database pages and TSVs outside `_experiments`, `_index/_inbox` and
`_index/candidates` ([`oldname_consumers.out`](oldname_consumers.out)) finds exactly the three files the record lists:
the family row, the object-construction page and the members TSV header, which is kept as history. The register row
BQ-25 is routed to SWE2-CONTRACT (`SWE2-EC7-REQ-CONTRACT-BQ25-ROW-0929`, still ACTIVE). The record states this as
PENDING PROPAGATION, which is the correct state until that request finishes. The GFZ tag keeping the old name is
disclosed.
