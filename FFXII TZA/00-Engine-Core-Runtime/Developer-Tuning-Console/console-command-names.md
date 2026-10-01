---
system: Console command names
category: 00-Engine-Core-Runtime
status: AUDITED — the 3.9 falsification item resolved 2026-09-18: 02CB8130 is the diffuse-intensity float; id 28's toggle lives in the console object's +0xC72 and suspends that float
owner_layer: CodeDomain:DeveloperConsole; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: join-falsification-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Console command names — all 282, joined

**GENERATED — do not hand-edit.** Source: the label table recovered from the row renderer,
joined to the nine arm-catalogue slices. Regenerate rather than patch.

Every command the developer console exposes, with the name the engine itself prints for it.

## Where the names come from

The row renderer `001CD0E0` prints `"%s%s%f"` with the label fetched from
`[ctx + id*8 + 0x130]`, so

```
id = (displacement - 0x130) / 8
```

**293 labels, ids 1-294, zero collisions, all 282 action ids covered.** Id 294 —
*"Key Kana Test"* — is a **render row with no action entry**, listed below for completeness
with an empty slice cell, because a row the menu draws and the dispatcher cannot reach is
exactly the distinction the two tables exist to make. Alignment is proven
four ways — the dispatcher's own `add r9d,-0xC` / `cmp r9d,0x119`; command 103's label against
the behaviour slice C read from its arm; the clamped pairs in C and E; a stride-12 stat array —
plus a cross-source control against the config keys: **20 arm-bearing pairs, 0 contradictions.**

## What a label is NOT authority for

> **A label names the row. It does not describe the arm.**

Slice H holds three adjacent rows labelled *"Enable 100% successful steal / poach / drop"*
whose arms cycle **four, three and five** states over ranges including `-1`. **Where the label
and the disassembly disagree, the arm wins.** A label is evidence of what someone *called* a
field — which is why it names targets an arm cannot — and not of that field's type, range or
semantics. **"Enable" in a label does not make a row a toggle.**

**Use the label to name the target; read the arm for everything else.** A propagated label is
safe in a parameter column and unsafe as a reason to skip re-reading the arm.

## Counts

| | |
|---|---:|
| action ids | **282** |
| render rows with no action entry | **1** |
| carrying a printed name | **283** |
| with the target field identified | **121** |

**Slice coverage:** A 32 · B 32 · C 32 · D 32 · E 32 · F 32 · G 32 · H 32 · I 26

## The table

**Behaviour columns are deliberately absent, and their absence is the point.** The join this
was built from also carried `shape`, `step`, `direction` and `bound` — and those cells are the
**pre-correction** classification: its `FLOAT`/`CALL` split is the withdrawn **102 / 71**, and
its `DO-NOTHING` count is the retired **56 unimplemented**, a figure three separate findings
have since replaced with *226 live · 38 read-outs · 12 buttons with the action removed · 6
blank*. Copying them here would republish two retracted numbers as data, in a generated file
that looks more authoritative than the prose that corrected them.

> **A generated table inherits the errors of its source and launders them into fact.**

**The nine slice documents are the authority for behaviour and they carry the corrections.**
This file answers one question — *what does the engine call this row, and who read it* — which
is exactly what the label table adds and nothing more.

| id | name the engine prints | arm | slice | field |
|---:|---|---|:-:|---|
| 12 | Read Json Data: | `001D16B1` | [A](arm-catalogue-slice-A-ids-12-43.md) | `01DF6E48` |
| 13 | Reread Json Data: Press Circle to reread json data | `001D4BFA` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 14 | Invincible: | `001D16C4` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 15 | Load ps2 savedata from slot: | `001D17D8` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 16 | Convert PS2 Savedata | `001D4BFA` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 17 | Save autosave to common save data: | `001D4BFA` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 18 | Jump To: | `001D4BFA` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 19 | Load sample chr: | `001D1740` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 20 | Load chr: | `001D170E` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 21 | Variation: | `001D177E` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 22 | CLUT: | `001D17AB` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 23 | Set chr rotation: | `001D4BFA` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 24 | Change cast shadow object: | `001D1818` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 25 | Shadow Level: | `001D1830` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 26 | Debug high model skeleton: | `001D1867` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 27 | Force town face: | `001D1893` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 28 | Use PS2 lighting: | `001D18E0` | [A](arm-catalogue-slice-A-ids-12-43.md) | `02CB8130` |
| 29 | Use normal map: | `001D1B11` | [A](arm-catalogue-slice-A-ids-12-43.md) | `rdi+0xC71` |
| 30 | Display normal only: | `001D1B26` | [A](arm-catalogue-slice-A-ids-12-43.md) | `02CB8148` |
| 31 | Use vertex color: | `001D1B39` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 32 | Display texture density: | `001D1B50` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 33 | Switch diffuse texture: | `001D1BBA` | [A](arm-catalogue-slice-A-ids-12-43.md) | `rdi+0xCF0` |
| 34 | Enable Map Display: | `001D1BCF` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 35 | Enable Character Display: | `001D1C0B` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 36 | Character Skeletons: | `001D2ADE` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 37 | Enable UI Display: | `001D1C47` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 38 | Enable VFX Display: | `001D1C83` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 39 | Draw VFX when capturing: | `001D1CCE` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 40 | Enable Shadow Display: | `001D1CE9` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 41 | Enable AO: | `001D1D17` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 42 | Display AO Only: | `001D1D36` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 43 | HBAO NumSteps: | `001D1D5A` | [A](arm-catalogue-slice-A-ids-12-43.md) | - |
| 44 | HBAO NumDir: | `001D1DB4` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 45 | HBAO Full Resolution: | `001D4AC0` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 46 | HBAO Depth Full Res: | `001D4ADF` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 47 | early AO: | `001D1E0E` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 48 | Post AA enable: | `001D1E2A` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 49 | SMAA level | `001D1E68` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 50 | Mask Border | `001D1E49` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 51 | Draw Chr Names: | `001D18CA` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 52 | Draw UI WithOut Scale : | `001D1F46` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 53 | Debug Cubemap: | `001D3988` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 54 | Toggle event cubemap: | `001D39CD` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 55 | Toggle cube map probes mode: | `001D3A2A` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 56 | Capture cube map. (L/R to toggle SkyBox) | `001D4BFA` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 57 | Operate cube map | `001D3A4A` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 58 | Set cube map properties: | `001D4BFA` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 59 | Recapture cube maps: | `001D4BFA` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 60 | Capture panorama: | `001D1F5A` | [B](arm-catalogue-slice-B-ids-44-75.md) | - |
| 61 | Camera Light enable: | `001D213D` | [B](arm-catalogue-slice-B-ids-44-75.md) | `01DFE192` |
| 62 | After Water fix enable: | `001D2150` | [B](arm-catalogue-slice-B-ids-44-75.md) | `rdi+0x10D9` |
| 63 | Hair Camera Light Direction X Bias: | `001D2165` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80B0` |
| 64 | Hair Camera Light Direction Y Bias: | `001D219B` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80B4` |
| 65 | Hair Camera Light Direction Z Bias: | `001D21D1` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80B8` |
| 66 | Hair Specular Power Modifier: | `001D2207` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80BC` |
| 67 | Hair Specular Power Eye-Camera Distance Factor: | `001D223D` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80C0` |
| 68 | Hair Specular Intensity Before Clamp Modifier: | `001D2273` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80C4` |
| 69 | Hair Specular Intensity Before Clamp Eye-Camera Distance Factor: | `001D22A9` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80C8` |
| 70 | Hair Specular Intensity After Clamp Modifier: | `001D22DF` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80CC` |
| 71 | Hair Specular Intensity After Clamp Eye-Camera Distance Factor: | `001D2315` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80D0` |
| 72 | Eye Type A Camera Light Direction X Bias: | `001D234B` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80E8` |
| 73 | Eye Type A Camera Light Direction Y Bias: | `001D2381` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80EC` |
| 74 | Eye Type A Camera Light Direction Z Bias: | `001D23B7` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80F0` |
| 75 | Eye Type A Specular Power Modifier: | `001D23ED` | [B](arm-catalogue-slice-B-ids-44-75.md) | `02CB80F4` |
| 76 | Eye Type A Specular Power Eye-Camera Distance Factor: | `001D2423` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80F8` |
| 77 | Eye Type A Specular Intensity Before Clamp Modifier: | `001D2459` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80FC` |
| 78 | Eye Type A Specular Intensity Before Clamp Eye-Camera Distance Factor: | `001D248F` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8100` |
| 79 | Eye Type A Specular Intensity After Clamp Modifier: | `001D24C5` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8104` |
| 80 | Eye Type A Specular Intensity After Clamp Eye-Camera Distance Factor: | `001D24FB` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8108` |
| 81 | Eye Type B Camera Light Direction X Bias: | `001D2531` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB810C` |
| 82 | Eye Type B Camera Light Direction Y Bias: | `001D2567` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8110` |
| 83 | Eye Type B Camera Light Direction Z Bias: | `001D259D` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8114` |
| 84 | Eye Type B Specular Power Modifier: | `001D25D3` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8118` |
| 85 | Eye Type B Specular Power Eye-Camera Distance Factor: | `001D2609` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB811C` |
| 86 | Eye Type B Specular Intensity Before Clamp Modifier: | `001D263F` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8120` |
| 87 | Eye Type B Specular Intensity Before Clamp Eye-Camera Distance Factor: | `001D2675` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8124` |
| 88 | Eye Type B Specular Intensity After Clamp Modifier: | `001D26AB` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8128` |
| 89 | Eye Type B Specular Intensity After Clamp Eye-Camera Distance Factor: | `001D26E1` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB812C` |
| 90 | Eye A and B Cube Map Blend Factor: | `001D2717` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80D4` |
| 91 | Eye A and B Specular Blend Modifier: | `001D274D` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80D8` |
| 92 | Eye A and B Ambient Scale: | `001D2783` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80DC` |
| 93 | Eye A and B Ambient Bound: | `001D27CC` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80E0` |
| 94 | Eye A and B Specular Shadow Modifier | `001D2815` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80E4` |
| 95 | Fresnel Specular intensity: | `001D2065` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80A0` |
| 96 | Fresnel Specular power: | `001D209B` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80A4` |
| 97 | Fresnel Specular Clamp Value: | `001D20D1` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80A8` |
| 98 | Fresnel Specular Skin Intensity: | `001D2107` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB80AC` |
| 99 | Fresnel Reflection enable: | `001D2052` | [C](arm-catalogue-slice-C-ids-76-107.md) | `01DFE191` |
| 100 | Camera Pose: | `001D4BFA` | [C](arm-catalogue-slice-C-ids-76-107.md) | - |
| 101 | Advanced panorama: | `001D4BFA` | [C](arm-catalogue-slice-C-ids-76-107.md) | - |
| 102 | Current GPU Temperature: | `001D4BFA` | [C](arm-catalogue-slice-C-ids-76-107.md) | - |
| 103 | Camera Over Write (O to capture): | `001D2AFD` | [C](arm-catalogue-slice-C-ids-76-107.md) | - |
| 104 | FOV: | `001D2B4D` | [C](arm-catalogue-slice-C-ids-76-107.md) | `rdi+0xC10` |
| 105 | Aspect Ratio: | `001D2B83` | [C](arm-catalogue-slice-C-ids-76-107.md) | `rdi+0xC14` |
| 106 | Camera scale: | `001D2BB9` | [C](arm-catalogue-slice-C-ids-76-107.md) | `rdi+0xC18` |
| 107 | Cube map factor: | `001D1FB0` | [C](arm-catalogue-slice-C-ids-76-107.md) | `02CB8140` |
| 108 | Diffuse intensity: | `001D1FE6` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8130` |
| 109 | Specular intensity: | `001D201C` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8134` |
| 110 | Cube map intensity: | `001D284B` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8138` |
| 111 | IBL Diffuse/Classic Ambient factor: | `001D2881` | [D](arm-catalogue-slice-D-ids-108-139.md) | `01DFE194` |
| 112 | IBL Diffuse limit: | `001D28B7` | [D](arm-catalogue-slice-D-ids-108-139.md) | `01F82ED0` |
| 113 | IBL Diffuse intensity: | `001D28ED` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8144` |
| 114 | Map Specular Intensity: | `001D2E18` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2D0 (through the accessor called at 001D2E18)` |
| 115 | Map CubeMap Intensity: | `001D2E61` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2D4 (through the accessor called at 001D2E61)` |
| 116 | Map CubeMap Factor: | `001D2EAA` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2D8 (through the accessor called at 001D2EAA)` |
| 117 | Map IBL Diffuse Factor: | `001D38C8` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2DC (through the accessor called at 001D38C8)` |
| 118 | Map IBL Diffuse Limit: | `001D390D` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2E0 (through the accessor called at 001D390D)` |
| 119 | Map IBL Diffuse Intensity: | `001D3952` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB806C` |
| 120 | Water Refraction Factor: | `001D2EEF` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8044` |
| 121 | Water Specular Factor: | `001D2F25` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8048` |
| 122 | Water Extra Debug Factor Two | `001D2F91` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8050` |
| 123 | Water Extra Debug Cubemap Factor | `001D2FC7` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8054` |
| 124 | Water Extra Debug Roughness Factor | `001D2FFD` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8058` |
| 125 | Water Parallax Occlusion Debug Factor | `001D3033` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB805C` |
| 126 | Water Fresnel Factor | `001D3069` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB8060` |
| 127 | Water texture U Factor | `001D309F` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2E8 (through the accessor called at 001D309F)` |
| 128 | Water texture V Factor | `001D30E4` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2EC (through the accessor called at 001D30E4)` |
| 129 | Water Min Z | `001D3129` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2F0 (through the accessor called at 001D3129)` |
| 130 | Sample step size | `001D316E` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2F4 (through the accessor called at 001D316E)` |
| 131 | Total Num of Pixels | `001D31B3` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x2FC (through the accessor called at 001D31B3)` |
| 132 | Reflection blend | `001D31F8` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x300 (through the accessor called at 001D31F8)` |
| 133 | Reflection strength | `001D323D` | [D](arm-catalogue-slice-D-ids-108-139.md) | `rax+0x304 (through the accessor called at 001D323D)` |
| 134 | Water Quality | `001D3282` | [D](arm-catalogue-slice-D-ids-108-139.md) | - |
| 135 | Water Texture Reflection Factor | `001D2F5B` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB804C` |
| 136 | Map Eye Specular Power Modifier: | `001D32CA` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB7FE8` |
| 137 | Map Eye Specular Power Eye Camera Distance Factor: | `001D3300` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB7FEC` |
| 138 | Map Eye Specular Intensity Before Clamp Modifier: | `001D3336` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB7FF0` |
| 139 | Map Eye Specular Intensity Before Clamp Eye Camera Distance Factor: | `001D336C` | [D](arm-catalogue-slice-D-ids-108-139.md) | `02CB7FF4` |
| 140 | Map Eye Specular Intensity After Clamp Modifier: | `001D33A2` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FF8` |
| 141 | Map Eye Specular Intensity After Clamp Eye Camera Distance Factor: | `001D33D8` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FFC` |
| 142 | Map Eye CubeMap Intensity Modifier: | `001D340E` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8000` |
| 143 | Map Eye Specular Blend Modifier: | `001D3444` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8004` |
| 144 | Map Eye Diffuse Modifier: | `001D347A` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8014` |
| 145 | Map Eye Ambient Modifier: | `001D34B0` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8018` |
| 146 | Map Eye Ambient Bound: | `001D34F9` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB801C` |
| 147 | Map BGNPC Fresnel Enabled: | `001D3542` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FD0` |
| 148 | Map BGNPC Fresnel Intensity: | `001D3555` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FD4` |
| 149 | Map BGNPC Fresnel Power: | `001D358B` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FD8` |
| 150 | Map BGNPC Fresnel Clamp Value: | `001D35C1` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FDC` |
| 151 | Map BGNPC Fresnel Skin Intensity: | `001D35F7` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FE0` |
| 152 | Map Camera Light Enabled: | `001D362D` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB7FE4` |
| 153 | Map Eye Camera Light X Modifier: | `001D3640` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8008` |
| 154 | Map Eye Camera Light Y Modifier: | `001D3676` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB800C` |
| 155 | Map Eye Camera Light Z Modifier: | `001D36AC` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8010` |
| 156 | Map Hair Specular Power Modifier: | `001D36E2` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8020` |
| 157 | Map Hair Specular Power Eye Camera Distance Factor: | `001D3718` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8024` |
| 158 | Map Hair Specular Intensity Before Clamp Modifier: | `001D374E` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8028` |
| 159 | Map Hair Specular Intensity Before Clamp Eye Camera Distance Factor: | `001D3784` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB802C` |
| 160 | Map Hair Specular Intensity After Clamp Modifier: | `001D37BA` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8030` |
| 161 | Map Hair Specular Intensity After Clamp Eye Camera Distance Factor: | `001D37F0` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8034` |
| 162 | Map Hair Camera Light X Modifier: | `001D3826` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8038` |
| 163 | Map Hair Camera Light Y Modifier: | `001D385C` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB803C` |
| 164 | Map Hair Camera Light Z Modifier: | `001D3892` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8040` |
| 165 | Re-read soft particle config | `001D4BFA` | [E](arm-catalogue-slice-E-ids-140-171.md) | - |
| 166 | Use soft particle: | `001D2923` | [E](arm-catalogue-slice-E-ids-140-171.md) | - |
| 167 | SSS enable: | `001D2983` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8434` |
| 168 | SSS Width: | `001D2996` | [E](arm-catalogue-slice-E-ids-140-171.md) | `02CB8438` |
| 169 | SSS Diffuse a: | `001D29CC` | [E](arm-catalogue-slice-E-ids-140-171.md) | `01DFE1AC` |
| 170 | SSS Diffuse b: | `001D2A02` | [E](arm-catalogue-slice-E-ids-140-171.md) | `01F82EE4` |
| 171 | SSS Blur: | `001D2A38` | [E](arm-catalogue-slice-E-ids-140-171.md) | `rax+0x1EC (through the accessor called at 001D2A38)` |
| 172 | Gaussian Filter big kernel (15x15 or 7x7): | `001D1E9D` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 173 | Gaussian Filter factor: | `001D1ED4` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 174 | Gaussian Filter blend amount: | `001D1F0D` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 175 | Yebis enable: | `001D2A7D` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 176 | Show Map Hide Group: | `001D2BEF` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 177 | Particle Draw Type Range Start: | `001D2C25` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 178 | Particle Draw Type Range End: | `001D2C91` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 179 | Color Correction Position: | `001D2964` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 180 | Map render DisplayList Id Start: | `001D2CFC` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 181 | Map render DisplayList Id End: | `001D2D68` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 182 | Fusion Technique Select: | `001D2DD3` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 183 | Print Magic Info: | `001D2E04` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 184 | Set All Enemy HP One: | `001D4BFA` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 185 | Huge Damage: | `001D3A91` | [F](arm-catalogue-slice-F-ids-172-203.md) | `rdi+0xC34` |
| 186 | Camera speed: | `001D3AE5` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 187 | Enable mouse control camera: | `001D3AA6` | [F](arm-catalogue-slice-F-ids-172-203.md) | `rdi+0xC35` |
| 188 | Enable reading key mapping from file: | `001D3ABB` | [F](arm-catalogue-slice-F-ids-172-203.md) | `rdi+0xC3C` |
| 189 | Navi Map Scale : | `001D3C3C` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 190 | Adjust tracmap center x (L/R) | `001D3CBD` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 191 | Adjust tracmap center y (L/R): | `001D3D17` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 192 | Adjust tracmap Super Wide Mul (L/R) | `001D3D84` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 193 | Adjust tracmap Super Wide MidPoint (L/R): | `001D3DE5` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 194 | Procedural texture: Toggle Usage | `001D4BFA` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 195 | Procedural texture: Toggle Management | `001D4BFA` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 196 | Procedural texture rotation ratio | `001D454A` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 197 | 100% Spawn Rare Monster : | `001D3E7A` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 198 | Save My Memory Leak Table | `001D4BFA` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 199 | Set gill to max: | `001D3E9C` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 200 | Set LP to max: | `001D3EB6` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 201 | Set level to max: | `001D3ED0` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 202 | File Cache Enable : | `001D3C77` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 203 | File Cache Reset Memory | `001D4BFA` | [F](arm-catalogue-slice-F-ids-172-203.md) | - |
| 204 | File Cache Info : | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 205 | Music : | `001D3EEF` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 206 | Voice: | `001D3F1E` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 207 | Sound Effect: | `001D3F4D` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 208 | 60fps input : | `001D3C99` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 209 | Load Debug Menu Settings | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 210 | Save Debug Menu Settings | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 211 | Debug Menu Text Shadow UVOffset X: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 212 | Debug Menu Text Shadow UVOffset Y: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 213 | Debug Menu Text Soft Edges X: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 214 | Debug Menu Text Soft Edges Y: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 215 | Debug Menu Text Shadow Dimension Offset X: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 216 | Debug Menu Text Shadow Dimension Offset Y: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 217 | 3D Sound Behind Ratio: | `001D4006` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 218 | Scene Item Debug Text Offset X: | `001D3F7C` | [G](arm-catalogue-slice-G-ids-204-235.md) | `rax+0x4664 (through the accessor called at 001D3F7C)` |
| 219 | Scene Item Debug Text Offset Y: | `001D3FC1` | [G](arm-catalogue-slice-G-ids-204-235.md) | `rax+0x4668 (through the accessor called at 001D3FC1)` |
| 220 | Extra BGM status: | `001D4033` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 221 | PS2 Far Plane: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 222 | Control character position: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 223 | Unlock All license: Press Circle | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 224 | Unlock all item: Press Circle | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 225 | Set clan point: | `001D405C` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 226 | Set step count: | `001D4155` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 227 | Set play time: | `001D424E` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 228 | Enable infinite summon time: | `001D3B1C` | [G](arm-catalogue-slice-G-ids-204-235.md) | `rdi+0xE1C` |
| 229 | Enable infinite chocobo time: | `001D3B31` | [G](arm-catalogue-slice-G-ids-204-235.md) | `rdi+0xE1D` |
| 230 | Enable infinite chocobo turbo time: | `001D3B46` | [G](arm-catalogue-slice-G-ids-204-235.md) | `rdi+0xE1E` |
| 231 | Set scenario flag: | `001D4362` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 232 | Count of battle: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 233 | Count of magic: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 234 | Count of tech: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 235 | Count of steal: | `001D4BFA` | [G](arm-catalogue-slice-G-ids-204-235.md) | - |
| 236 | Count of killed monsters: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 237 | Current LP: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 238 | Set count of battle: | `001D43C9` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 239 | Set count of magic: | `001D4416` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 240 | Set count of tech: | `001D4463` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 241 | Set count of steal: | `001D44B0` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 242 | Set count of killed monsters: | `001D44FD` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 243 | Enable 100% successful steal: | `001D3B5B` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 244 | Enable 100% successful poach: | `001D3BA2` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 245 | Enable 100% successful drop: | `001D3BEE` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 246 | Chara Name: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 247 | Level: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 248 | HP: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 249 | MP: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 250 | ATPOW: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 251 | DFPOW: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 252 | WDFPOW: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 253 | EVPOW: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 254 | MEVPOW: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 255 | STR: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 256 | MGC: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 257 | WPR: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 258 | SPD: | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 259 | Reset Parameter: Press Circle | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 260 | Master Volume Ratio: | `001D4590` | [H](arm-catalogue-slice-H-ids-236-267.md) | `rdi+0x10B8` |
| 261 | Set Leather Count to 2: Press Circle | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 262 | Print Memory stats: Press Circle | `001D4BFA` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 263 | Game Window Mode: | `001D45E9` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 264 | Game Display Resolution: | `001D46DD` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 265 | Game Monitor : | `001D4712` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 266 | System Adapter: | `001D464B` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 267 | Mouse Control Vertical Camera Speed: | `001D4766` | [H](arm-catalogue-slice-H-ids-236-267.md) | - |
| 268 | Mouse Control Horizon Camera Speed: | `001D4731` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 269 | Mouse Wheel Control Scroll Table Frequency: | `001D47FD` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 270 | Mouse Wheel Control Scroll Table Buffer Size: | `001D4832` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 271 | Camera Revise Enable: | `001D47B5` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 272 | Brightness: | `001D4867` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 273 | Vsync : | `001D48AD` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 274 | Anisotropic filtering : | `001D4972` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 275 | Shadows Quality : | `001D49C1` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 276 | Character self-shadow : | `001D4A28` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 277 | Anti-aliasing : | `001D4A3D` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 278 | Post process AA : | `001D4A8A` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 279 | Ambient Occlusion : | `001D4B03` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 280 | Depth of Field : | `001D4B37` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 281 | Glare : | `001D4B49` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 282 | Save Config File : | `001D4BFA` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 283 | Apply Graphic Quality Default : | `001D4B7D` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 284 | BackBufferCount : | `001D4907` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 285 | Frame Limit (Apply save config file & restart game) : | `001D494F` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 286 | Clear Achievements : | `001D4BFA` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 287 | FrameSkip Enabled: | `001D47EA` | [I](arm-catalogue-slice-I-ids-268-293.md) | `01E02801` |
| 288 | Mouse Control Camera Max Move: | `001D479B` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 289 | Disable PauseMenu : | `001D4BFA` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 290 | Game Time Stop is | `001D4BFA` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 291 | Save Load Message Debug State : | `001D4BB7` | [I](arm-catalogue-slice-I-ids-268-293.md) | - |
| 292 | Super wide Mask Debug Enable : | `001D4BEA` | [I](arm-catalogue-slice-I-ids-268-293.md) | `rdi+0x10E0` |
| 293 | Key Board Debug For Japanese Keyboard: | `001D3AD0` | [I](arm-catalogue-slice-I-ids-268-293.md) | `rdi+0xC3D` |
| 294 | Key Kana Test Press ,Press Enter Button | (no action table entry) | - | - |

## Falsification pass - 2026-09-03, six attacks, one contradiction found

**Stamped by the generator because the pass is a property of the join it emits.** The attacks
below were run against the join and their results are printed rather than asserted; a bare
`passes: 1` on a generated file would be the status field asserting a check that never ran,
which this project has corrected in four separate fields already.

| attack | result |
|---|---|
| **A1** duplicate labels - a shifted index read would repeat or garble | **0 of 283** |
| **A2** two ids claiming one arm | **56 ids share `001D4BFA`** - the do-nothing tail |
| **A3** arms outside the dispatcher | none; all 282 lie in `001D16B1`-`001D4BFA` |
| **A4** gaps in the action id range | **none** - 12 to 293 continuous, exactly 282 |
| **A5** one field claimed by two ids | **1** - `02CB8130`, and it is a contradiction |
| **A6** arm address order vs id order | **29 inversions**, excluding the shared tail |

**A2 is where "56 unimplemented" came from, and the join shows exactly how it went wrong.**
Fifty-six ids really do point at the shared tail - **that number was right about the action
table.** It was wrong about the menu: 38 of them still draw a live value, 12 are labelled
buttons with the action removed, 6 draw blank. **A true statement about one table, restated
about the other.**

**A6 is a warning for anyone re-deriving arm extents.** Arms are **not** laid out in id order -
29 adjacent id pairs run backwards in address. **Bounding an arm at the next *id* is wrong 29
times; bounding it at the next *address* is right.** Every delivered slice used address order,
so nothing here is retracted - but the two orders are not interchangeable and the catalogue
never said so.

**A5 is the pass's one real finding, and only the join could see it.**

> **`02CB8130` is bound by two slices to two incompatible things** - id 28 *"Use PS2 lighting"*
> (a toggle) in slice A, and id 108 *"Diffuse intensity"* (a float) in slice D. **A boolean and
> a float cannot share an address.** One reading is wrong, or the field is narrower than one of
> them assumes.

The address sits at **`+0x160` inside the `02CB7FD0` static object**, whose analysis produced the
rule that catches exactly this: *width must come from the store, and a boolean that cannot be
3.9 is what catches it.* **Raised, not resolved** - resolving it means reading the two stores,
and the slice authors own those reads.

**Resolved 2026-09-18 (FABLE), by reading the two arms: `02CB8130` is a float, and id 28 does not own it.** Every reference to `02CB8130` in the image is a `movss` or an 8-byte zeroing — eleven sites, all in the console handler `001D1660` and the overlay `001CD0E0`. Arm 108 (*Diffuse intensity*, `001D1FE6`–`001D200F`) loads the float and steps it up or down by the constant at `009002BC`. Arm 28 (*Use PS2 lighting*, `001D18E0`–`001D1A6D`) keeps its **toggle in the console object's byte `+0xC72`** (`sete` / store at `001D18E7`–`001D18EA`); when the toggle turns *on* it **saves** the three diffuse floats `02CB8130` / `02CB8134` / `02CB8138` into `+0xC74` / `+0xC7C` / `+0xC78` and zeroes them (`001D18F8`–`001D195A`), together with the three bytes `01DFE190`–`01DFE192`, the device fields `+0x2D0` / `+0x2D4` / `+0x2E4` and the bytes `02CB7FD0` / `02CB7FE4`, and recomputes `02CB8080`; when it turns *off* it restores them (`001D1A55`–`001D1A6D`). So both slices were right about their arms and wrong about the join: the address in id 28's row is the field the toggle *suspends*, not the toggle's state, and no boolean lives at `02CB8130`. Static: the two arm bodies and a whole-image reference sweep. *Slice A had reached the same reading on 2026-09-03 (its “Correction” section) and slice D marks the field resolved; this page's status had not caught up with its own slices.*

## Provenance

The label table was recovered by one session from the row renderer; the arm columns come from
nine slice documents written by five sessions over one run. **The two were produced
independently and joined afterwards**, which is what makes their agreement worth anything —
including the six enumeration bounds that were read from arm instructions *before the label
table existed* and match their label counts exactly.

*(Pass 22 adjacency, 2026-09-14: the renderer `001CD0E0` this table feeds sits on the
**presentation** path — called by `001D5260`/`001D0190`, calling `001DCD30` — and reaches
**resource** `0020C700` and **audio** `002DEBA0` for its fetch legs (5 edges). The command names
are drawn by render-path code; the crossings are the renderer's, repeated here because this page
cites it.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **PlatformOnlineAchievements — SERVICE (1 edge).** 1 outbound (page-cited `001CD0E0` call PlatformOnlineAchievements bodies `003166F0`). Substantive edges include `001CD0E0` calls `003166F0`.
- **WorldAreaField — CLIENT and SERVICE (3 edges).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `002DEBA0`); 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270); `002DEBA0` is called by `World_UpdateSimulationTick` (00314020).
