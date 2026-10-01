# SWE2-AUDIT-SEM review — FABLE's static answers RC-6 to RC-10, the OV-5/8 (d) region-A census and the descriptor-list census (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930` |
| reviewed | `8bdf31fcb` (author **FABLE**) — [`rc789-fable-0930/README.md`](../rc789-fable-0930/README.md), [`fable-astra-live-facts-0930/t3b_ov58d_region_a.md`](../fable-astra-live-facts-0930/t3b_ov58d_region_a.md), [`t4_descriptor_inserters.md`](../fable-astra-live-facts-0930/t4_descriptor_inserters.md) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`, image base `0x120000` |
| tree at review | HEAD `d3e855f21` |
| not used as evidence | OPUS's in-progress `ov58d-pointer-flow-0930` (OPUS production) |
| conflicting verdict | a second, concurrent SWE2-AUDIT-SEM session closed the board task `verdict:ACCEPT` at 06:36Z on re-runs only (`Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-takebacks2.md`, commit `866a6a13e`); it did not test the writer in §6. This record's REJECT of t3b stands on that concrete case; filed as `AUDITSEM-CONTRA-FABLE-T3B-REGION-A-WRITERS-0930`, with `AUDITSEM-REQ-FRONTIER-HOLD-OV58D-0930` holding the OV-5/8 (d) incorporation |
| **verdict** | **REJECT, scoped to t3b (OV-5/8 (d))**: its region-A writer list misses a whole-state copy that stores arbitrary words (§6). **RC-6, RC-9, RC-10 and t4 are accepted; RC-7 and RC-8 are accepted with narrowed premises** (§7). |

## 1. Producer checkers re-run from the repository root (SWE2-AUDIT-SEM)

`rc9_channels.py`, `rc10_gates.py`, `rc6_codes.py` run green from the record directory. `t3b_regionA.py` and
`t4_desc_inserters.py` **fail from their published location** (`FileNotFoundError` on
`../pub140-scratch/tools/rawcalls.json`); they run only as copies under `Database/Tools/work/FABLE/takebacks/`, as the
request says. Run there, both end as committed. All five outputs match the committed `.out` line for line
([`producer_rerun.out`](producer_rerun.out)). The published scripts are not runnable where they are published;
that is a reproducibility defect, not a finding against their content.

## 2. RC-9 — the 13 manual channel reads (question 1) (SWE2-AUDIT-SEM)

[`rc9_manual_dump.py`](rc9_manual_dump.py) ([out](rc9_manual_dump.out)) prints each span from its evidence address to
the log call, and marks every raw direct jump image-wide that lands inside it. I read all 13:
- `00194796` (`esi = 1`, nonvolatile across the calls), `001D4636` (`ebp = 2`), the three `005CCF2C` paths
  (`ecx = 2` with no call before each site), `0079C42B` (`ecx = 2`, `je` to the site), the three `0062A0A0` sites and
  `00677D3E` (`rbp = rax` then `test / jne` → 0 on the fall-through, `ecx = rbp + 1` or `+ 2`), `006391F2`
  (`eax` pinned to 2 by `cmp eax, 1 / je` and `cmp eax, 2 / jne`, `ecx = eax − 1` = 1): all hold.
- The four "jump-ins" the raw scan marks are mis-aligned decodes (`001D45A1` and `006391BF` fall inside other
  instructions), the loop back-edge `006865ED` in `00686280`, or targets past the site (`0062A22F`).
- `00686280`: every write of `ebp` in the function is `mov ebp, r13d`, `inc ebp` under `cmp ebp, 2 / jb`, or
  `mov ebp, 1`, so both sites pass 0–2, as stated.

No site passes 4. RC-9 stands.

## 3. RC-8 — a writer of the singleton's `+0x13C` the census misses? (question 2) (SWE2-AUDIT-SEM)

Own sweeps, not the producer's function list:
- **Covering stores** ([`cover_sweep.py`](cover_sweep.py) `13C`, [out](cover_13C.out)): 402 stores image-wide, any
  width, whose destination covers `+0x13C`.
- **Where the pointer goes** ([`rc8_escape.py`](rc8_escape.py), [out](rc8_escape.out)).
  - The cell `01F82EA8` has **four** writers: `001F0844` and `001F0886` in the two creators, and two inlined creators,
    `001F15D7` and `001F1650`. Each allocates `0xB08` bytes (`00210EC0`), runs `001EF2D0` and stores the result.
  - **`0015CC00` stores `001F0850`'s return into a second global, `01F812C8`.** A census seeded on `01F82EA8`
    cannot see that global's readers.
- **The second global's readers** ([`rc8_alias.py`](rc8_alias.py), [out](rc8_alias.out),
  [uses](rc8_alias_uses.out)): 31 loads in two console functions, `001C3D50` and `001C7940`. They store the
  singleton's `+0xEC`/`+0xF0`/`+0xF4`/`+0x140`/`+0x144` and `+0x82C`..`+0xAFD`. **None of the 402 covering stores lies in
  those two functions or in their 53 direct callees.**

**So RC-8's answer stands: nothing but the constructor stores `+0x13C`.** Its premise is narrower than stated,
though: the object has a second published location, and two more creators.

## 4. RC-7 — is `rsp + 0x5C` really `SampleDesc.Count`? (question 3) (SWE2-AUDIT-SEM)

[`rc7_chain.py`](rc7_chain.py) ([out](rc7_chain.out)).
- **Yes, structurally.** The descriptor is built at `rsp + 0x48`: `+0` width, `+4` height, `+8` mips, `+0xC` array
  size, `+0x10` format, **`+0x14` (`rsp + 0x5C`) Count, `+0x18` (`rsp + 0x60`) Quality**, and usage/bind/CPU/misc at
  `+0x1C`..`+0x28`. That is `D3D11_TEXTURE2D_DESC`. `0061FEC1` reads byte `+9`; the remaps 7 → (4, 16) and
  9 → (8, 16) are at `0061FED5` / `0061FEEC`. `006200CF lea rdx, [rsp + 0x48]` feeds `006200E5 call [rax + 0x28]`,
  `ID3D11Device::CreateTexture2D`.
- **But there are two creates.** When the flag at `rsp + 0x24` is set (`0061FF28`), the code:
  - copies the descriptor to `rsp + 0x78` (`00620031`–`00620059`);
  - overwrites the **primary** descriptor's SampleDesc with `{1, 0}` (`00620062 mov qword [rsp + 0x5C], rdx`,
    `rdx = 1`);
  - creates the primary texture single-sampled at `006200E5`;
  - creates the **copy**, which keeps the multisample count, at `00620188` (`0062017D lea rdx, [rsp + 0x78]`).

The flag is set when the render target's `+0xC` bit 0 is set, or from the incoming `dl`. So the byte reaches
`SampleDesc.Count` of either the `006200E5` texture or the `00620188` texture. The semantic answer (a multisample
count, 0 = off) does not change; the sentence naming `006200E5` as the create is incomplete.

## 5. RC-10 — the 17 candidate guards (question 4) (SWE2-AUDIT-SEM)

[`rc10_latches.py`](rc10_latches.py) ([out](rc10_latches.out)):
- **All nine warn-once latches.** Between the guard and the site, the same byte is set to 1 (`00601E19`, `00603396`,
  `0061C20D`, `0062A212`, `0062A2A8`, `0062A34A`, `0067C294`, `0079A16C`, `0079FDB8`). 9 / 9.
- **The screen-mode flag `02EA5247`.** Exactly one reader (`0079EBC5`) and one writer (`007A0FA0`).
- **The three linear-window artefacts:**
  - at `001DDC1D` both arms of `cmp [rcx + 8], 0` rejoin at `001DDBF1` before the log;
  - `0079A1A1` sits after the latched arm's `jmp 0x79a405`;
  - at `007994B4` both outcomes jump away (`je` / `jmp`) before the guarded site.
- The four functional conditions were read in the producer output only.

RC-10 stands, within its stated limit (the 207 local guards are classified, not read).

## 6. t3b — OV-5/8 (d): region A's writers (question 5) — REJECT (SWE2-AUDIT-SEM)

**The failing case** ([`mirror_writers.py`](mirror_writers.py), [out](mirror_writers.out); the same copy is §3 of
[`../auditsem-review-rc-residue-0930/REVIEW.md`](../auditsem-review-rc-residue-0930/REVIEW.md)):
- The active image `02164280` holds a `0x6000`-byte **mirror** at `+0x2200` (`02166480`) of the live state at
  `+0x4E68C` (`021B290C`).
- **`002EF4A0` copies the mirror over the live state**, 16 bytes at a time: `0xC0 × 0x80` bytes over
  `021B290C`..`021B890C`. That span contains all of region A (`021B7054`..`021B781B`, state `+0x4748`..`+0x4F0F`), so
  this is a **region-A writer that stores arbitrary words**: whatever the mirror holds, unclamped.
- Its only caller is `00235AF0`. That compares the mirror's header dwords `+0`/`+4`, byte `+0x5B42` and word `+0x5B12`
  with the live state's, and copies when they differ.
- **`00235AF0`'s only caller is `00233C14`, the first instruction of the post-load lazy body `00233C10`.** So it runs
  **before** the magic test that t3b §2 analyses.
- Writers of the mirror:
  - the load copy (`00866A4D` writes all `0x56690` bytes of the image, mirror included);
  - the snapshot copy `00229B76`..`00229BDE` (live `+0x4E68C` → mirror `+0x2200`, `0xC0 × 0x80` bytes);
  - **`00583C00`** (called at `00580921`), which copies `0xE240` bytes from an external buffer `[[02CA99B8] + 0x588]`
    over image `+0`..`+0xE240`, mirror included. Its reverse is `00583CB0`.

Against the record:
- **"Region A is written by: …"** lacks `002EF4A0`. **"Of these, the only writer that can store an arbitrary word is
  the save-load copy"** is false: `002EF4A0` stores the mirror's words unclamped.
- **"A loaded image with a valid magic keeps its region-A words exactly as the file supplied them"** is false as
  stated. After a load whose mirror header differs from the live header, region A holds the **mirror's** words.
- **"Over-reservation … can enter only through save-file bytes, loaded by `00866A4D`"** is not established. The mirror
  is also filled from `00583C00`'s external buffer, whose source is not traced here or in the record. The words
  may well originate in a save file; the record does not show that.
- Why the census missed it: §2's writer shapes are memset/memcpy calls, registry references and displacements
  `0x4748`..`0x4F0F`. An inline `movups` loop walking a register from the state base at displacements `−0x80`..`−0x10`
  matches none of them, and `00233C10`'s first call was not examined as a writer.

Repair (the author's): add `002EF4A0` (via `00233C10` → `00235AF0`) to the writer list; trace the mirror's writers,
including `00583C00`'s buffer source; restate the conclusion as the set of byte sources that reach region A through
the load copy **or** the mirror. OPUS's pointer-flow census may find the same copy; it is not used here.

## 7. Narrowings for the accepted items (exact wording; FABLE and SWE2-CONTRACT apply them) (SWE2-AUDIT-SEM)

- **N1 — RC-8, "The object is a singleton with no vtable" paragraph.** Replace "`001F0810` and `001F0850` … store the
  pointer in the global `01F82EA8`" and "its only published location is `01F82EA8`" with: *"`001F0810`, `001F0850` and
  two inlined creators (`001F15D7`, `001F1650`) store the pointer in `01F82EA8`; `0015CC00` also stores it in
  `01F812C8`, whose readers `001C3D50` / `001C7940` (console tuning) write other fields of the object and not
  `+0x13C`."* The answer (count stays 3) is unchanged.
- **N2 — RC-7, step 4.** Replace "reads that byte … then calls the device's vtable `+0x28` with the desc (`006200E5`)"
  with: *"reads that byte into the descriptor's `SampleDesc.Count` (`rsp + 0x5C`). When the flag at `rsp + 0x24` is
  set, the descriptor is copied to `rsp + 0x78`, the primary is reset to `{1, 0}` and created at `006200E5`, and the
  multisampled copy is created at `00620188`; otherwise the multisampled descriptor is created at `006200E5`."*
- RC-6, RC-9, RC-10 and t4: no change.

## 8. Not reviewed here, and open limits (SWE2-AUDIT-SEM)

- t4 was re-run with its controls (the `+0x80` insert and the PNamespace `+0xA0` insert are found), not re-derived.
- RC-6 was re-run, not re-derived (authored data).
- RC-10's four functional conditions and its 207 local guards are the producer's classification.
- The source of `00583C00`'s buffer `[[02CA99B8] + 0x588]`.
