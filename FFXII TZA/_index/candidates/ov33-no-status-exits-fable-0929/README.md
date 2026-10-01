# OV-33 (ii)/(iii), static part: can a shipped request take an exit that writes no read status?

FABLE (Claude Opus 5.5), 2026-09-29, drafted by a FABLE static helper and checked by FABLE before publishing.

FABLE's spot re-reads:
- `0024AC30` requests kind `0x23` id `ecx + 7` and takes the size from `0032E400`. When `0037B330()` is 0, it hands that
  size to `0032E620` with no sign test (`0024AC47`-`0024AC9F`).
- The event loader `0032FCA0` skips a request on a negative size (`0032FE54 test ebx, ebx` / `0032FE5E js`;
  `0032FED2 jl`).

Independent review: SWE2-AUDIT-SEM (requested with this publish). Nothing here was run live.

**FABLE addendum: the E4-archive producers narrow to one.** The six archive-missing rows are kind 1, ids 127..132
(US 129-131, UK 131-132, CN 127). The E4 section below names three live producers of kind-1 requests:
1. `002EAD50`'s default arm;
2. `0032FCA0` with m = 4 (id = set + `0x6B`);
3. a debug verb.

FABLE read `m` at every `0032FC30` call site from the raw index. The eight sites are `0025DAED`, `00306C56`, `003140BA`,
`00352304`, `003530CF`, `003535A3`, `003CA07C` and `0050D115`, and `0032FCA0`'s only caller is `0032FC30` (`0032FC7B`,
with no address-take).
- **Sites that pass 3 or less, or a fixed small value:**
  - `003530CF` and `00352304` clamp m to at most 3 (`cmovg`);
  - `003CA07C` and `003535A3` pass 3;
  - `003140BA` (the world-tick drain) passes 0 (`xor ecx, ecx`);
  - `0050D115` diverts 4 to `00314410` (`0050D0DC`).
- **Sites that could carry 4:** only `0025DAED` (m = `r12d`, set `0xD4` fixed at `0025DAE8`) and `00306C56` (m = `ebx`,
  set = the action row's `+0x24`, whose shipped values are 0, 40..77, 210 and 355; `../rc5-operand-dataflow-fable-0929/`).
  Even with m = 4 their kind-1 ids would be 319 and {107, 147..184, 317, 462}. **None is in 127..132**, which would need
  sets 20..25.

So producer 2 cannot request an archive-missing row, whatever m those two sites carry. **The E4-archive fact narrows to**
whether `002EAD50`'s default arm receives a model id whose low 16 bits are 76..81 (id = low16 + `0x33`), or the debug
verb requests one of those ids.

This rests on the `m = 4 -> kind 1, id = set + 0x6B` mapping as this record states it; FABLE did not re-read that
mapping.

**Producer 1, from the shipped manifests** (FABLE, 2026-09-30): `002EAD50`'s only caller is `002E6700`, the model loader
walking the `0215FD78` list.
- **Guard.** `002E6700` skips a non-positive size (`002E678B jle`), but the six rows do have positive sizes; the archive
  lacks them, the table does not.
- **Mapping.** `002ED6F0` sends a model id `(letter << 16) + N` to kind 1 only for a letter outside
  `c n s m b g C N S M t w` (default arm `002ED840`), and the id becomes N + `0x33` (`002E676C` / `002EAD95`).
- **Census.** [`e4_manifest_models.py`](e4_manifest_models.py) -> [`.out`](e4_manifest_models.out) reads every shipped
  EBP's section-12 manifest (7,587 files; control: `dgl_g0102` holds `C:22`, PASS). **Every manifest model id uses one
  of those twelve letters** (C N S b c g m n s t w seen). None goes to kind 1, so none reaches the six rows.

**The E4-archive fact is therefore:** whether a model id from a source other than the script manifests, with an
unknown letter and N 76..81, reaches `002E6700`, or the debug verb requests one of the six rows.
Image `FFXII_TZA.exe` sha256 `73461d08…`, image base 0x120000 included in every address.
Data sources:
- the 12 install tables `D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables\*.fst` (US sha256 `3a03ea77…`, the same file as `ov42-selector-fst-bound/fst-inputs-01`);
- the archive `FFXII_TZA.vbf` in the same folder, read through `agent_flow/tools/vbfextract.py`: 89,414 entries, all names lower-case.

## Verdicts

| exit | verdict | one-line reason |
|---|---|---|
| **E1** `002DF7B9` | **REACHABLE** | Kind 35 has no FST entry in any language, and `0024AC30` requests it with no size check. It fires when a save-crystal menu opens (request 6), and for requests 16 and 22 (0x40/0x41). Two further routes depend on the language: UK at boot and KR/CN at the staff roll. |
| **E2** `002DF801` | **DEPENDS-ON** one fact, below | `001D6F20` returns null only when the path is absent from the archive **and** the loose-route gate still found its key in the RAM FileCache map. |
| **E3** `001D6DB9` / `001D6FD9` | **UNREACHABLE** in shipped play | The pointer has two writers. It is created at platform init before the game boots, and destroyed only in teardown, which cannot reach the pump. Sole premise: the 0x140228-byte allocation at `001A11CC` succeeds. |
| **E4** loose `-2` (`001A0ED2`) | **UNREACHABLE** | The record is the one `001D6F20` has just verified as set. The job then runs inline, and nothing in between writes the three fields. |
| **E4** archive `-2` (`001A0D80`) | **DEPENDS-ON** one fact, below | `-2` ⇔ the resolver cannot open the path ⇔ the archive lacks it. Among the FST-sized paths the pump can issue there are exactly **6** such rows, all kind 1. |

**E2 fact:** whether, while the FileCache "map jump pending" byte `+0x88` is set, a request is issued for a path that `FFXII_TZA.vbf` lacks and whose key (`00674A00` over the `0020C440`-normalised path) the FileCache map at `[01F83438]+0x28` holds.

**E4-archive fact:** whether shipped play issues a request for one of the six (language, kind 1, id) rows whose path the archive lacks: US 129/130/131, UK 131/132, CN 127.
The one other live source of an unchecked path is `00377DC0`'s run-time-built kind-0xFF path; it is listed below and was not resolved.

---

## E1: the FST entry is -1 at `002DF7B0`/`002DF7B9`

**Correction to the task premise.** The `-1` check exists only in `002DF780`. `002DF6C0`, the kind-0xFF raw-path issuer, has no FST check (`002DF6C0`–`002DF77E`, read whole). What it shares with `002DF780` is the `001D6F20`-null exit (`002DF717`).

### How the FST is filled (`e1_fst_writers.py`, FAILS 0)
- There are exactly three address forms of `[02EC3EE0, +0xC8320)`:
  - `002DF96D lea` in `002DF960`, which is the reader (`002DF977 mov eax,[rax+r8*4]`);
  - `002E0432 lea rcx` in `ResourcePath_Init` `002DF9A0`, which is the `fread(02EC3EE0, 0xC8320, 1, f)` destination at `002E0444`;
  - `002DF7B0 cmp [r15+rax*4+0x2da3ee0], -1`, the issuer, in image-base-relative form.
- There are 0 absolute memory operands and 0 DIR64 relocs into the table. The 720 absolute hits are arithmetic immediates, all in unlisted code.
- `002DF9A0` has one caller, `0022A159` in the boot function `0022A0B0`.
- So the table is the chosen language's shipped `.fst`, read once at boot and never written afterwards.
- The file name is `../FileSizeTables/FileSizeTable_<lang>.fst`, `lang` ∈ `01E88B00` = JP US FR DE IT ES UK KR CH ASIA IN CN. A failed `fopen` or short read takes the fatal arm at `002E044F`/`002E0478`.
- Controls: `002DF96D` and `002DF7B0` found.

### Census of `-1` entries (`e1_fst_census.py`, FAILS 0)
- Controls: dword 0 = 57 (system.cnf); US has 10,521 sized entries across 31 kinds, matching the FST page.
- No entry in any table is 0, and none is negative other than -1.
- Ten kinds have no sized entry in **any** language: **3, 6, 17, 18, 27, 29, 31, 35, 36, 40**.
- The ids whose sized/-1 status differs by language are listed per kind in the `.out` (kinds 1, 2, 5, 7, 8, 9, 12). Two examples:
  - kind 7, ids 218–223: -1 in KR and CN only;
  - kind 9, id 31: -1 in UK only.

### Producers of slot `+0x21` kind / `+0x24` index
- `e1_slot_writers.py` (FAILS 0): 13 functions address the queue storage `[022C31C0, 022C5200)`. Of them, only `0032E870` stores over `+0x21`/`+0x24` (controls `0032E943`, `0032E902`).
  - The pump's own stores (`0032E0FF`…`0032E28D`) touch only `+0x20`/`+0x23`/`+0x28`/`+0x2C`/`+0x38`/`[+0]`.
- `e1_producer_sites.py` (FAILS 0): `0032E870` is reached only from `0032E620` ×2, `0032E780` and `0032E7C0`. The index has 74 raw E8/E9 sites into the builders, all on instruction boundaries; there are 0 jcc sites and 0 address-takes. Controls `002492F3`, `0032E84D`, `0032EC01` pass.
  - `0032E620`: 51 sites. `0032E780`: 2 sites. `0032E7B0` → `0032E7C0`: 16 sites + 1 thunk jmp. Those 17 are kind 0xFF, so they are not E1.
- `0032E870` does not test the byte count. The pump issues whenever `+0x28 != 0` (`0032E0CE`), so a request with bytes = -1 is issued.
- `0032E400(k,i)` returns -1 for an FST `-1`, and returns it unrounded (`0032E43B`). The override array `022C51F0` is never filled (DG-6).

**Classification of the 53 `0032E620`/`0032E780` sites** (reading aid: `e1_site_summary.out`, `e1_producer_windows.txt`):

- **Gated.** Each request is skipped when `0032E400` for the *same* (kind, id) is ≤ 0 or < 0, so none of these can reach E1:
  - `00249210`; `00259DF0` (9,3); `0026883E` (9,2);
  - `002E60F0` (0x20, 0/1);
  - `002E6EB0`: the size comes from `002E9920`, which repeats the same `002ED6F0` arithmetic; `jle 002E7016`;
  - `002EA530`; `0032EB40` (`> 0x800`); `0032F430` (8,0x350);
  - `0032FCA0` ×4 and `00330310` (see the RC-5 lead below);
  - `00360C70` (9,6); `0036ED50` ×2; `00378030`; `00378540` ×7; `00379E90` (9,7); `00384420` (2,id, `jns`);
  - `003A13F0` ×3; `003B0660` (10,0); `003B2310` (12, 0x1FE/0x240); `003DCBC0` (9,5); `003EA820` (0x15,id).
- **Ungated with static ids**, checked against all 12 tables (`e1_static_ids.py`, FAILS 0; controls (0,0) = 57 and (35,9) = -1):
  - **`0024AC30` (35, p+7): -1 in all 12 → E1.** Details below.
  - **`003EAC40` NpcDictionary_Load → `0051ED10` (9, 0x1F): -1 in UK → E1 at boot in UK.** It is reached as `0022A433` → `00379D20` → `00379D24`. The boot function has no conditional branch before it except `0022A3E1`, which skips `0036FD70` and nothing else. The one step not read: `0036A1A0(-1)`, the allocation of a block of size -1, must return (both of its visible arms return).
  - **`00365810` via `0053EB90` msg 1 (7, 218..223): -1 in KR and CN → E1 when the staff-roll widget opens.** The widget is built by `0053ED10`, reached from the script thunk `00511540`. Which shipped script reaches it was not censused.
  - `002EF300` debug_loadjfdata (1, 117..132) has a constant size 0xE240 and is -1 in JP/CH/ASIA/IN. No shipped script uses the verb (`katano-debug-savedata.md`; not re-derived).
  - `003EADE0` BGM stream (kind 0x24) is -1 everywhere. No shipped script issues verbs `0448`–`044F` (`the-music-control-file-and-the-bgm-stream.md` §1; not re-derived).
  - All sized in all 12 languages: `00268809` (9,4), `00291C80` (7,152..161), `002C8EE0` (7,116..117), `003658F0` (7,210), `0039C3F0` (7,213), `003B53C0` (9,42), `003EAB60` (9,32), `00473D20` (9,33), and `002FC860`'s fallback ids (11/38 × 120, 138, 0).
- **Ungated with ids computed at run time** (site, and why):
  - `002EAD50` @`002EAE08`: (kind, id) comes from `002ED6F0(model id)`, whose default arm gives kind 1 and id = low16 + 0x33. The size is taken but not tested.
  - `002FC860` @`002FC96F`, when `02EC3D7D` ≠ 0: the size comes from the table `02EC19C0[id]`, not the FST, so the id is not FST-checked. The other branch always falls back to sized ids.
  - `0036ED50` @`0036EDF7`: gated. (Listed earlier; noted here because its id is `word [rec+0x14]`.)
  - `00324510` (26, i<301): the sizes come from `{id,size}` pairs at `022C27B8`, which have no rip writer. State 1 (`022C27A0 == 1`) has no writer either, so the producer is dormant.
  - `003DC5B0` @`003DC683`: kind, id and size come from `003DCA30`/`003DC8D0`.
  - `003DDA70` @`003DDAB9`: the indexed-source owner, kind 5/8, id 3k+1/4k+1, with the length taken from `.mot` metadata. This is the OV-42 selector domain.
  - `003DF550` @`003DF593`: the record's `+0x2C`/`+0x2E`/`+0x30`.
  - `003E9EF0` @`003E9F59`: the record's words `+0xC`/`+0x10` and the size at `+0x14`.
  - `0050DFE0` @`0050E039`: a script verb. Kind, id, dest and bytes all come from the VM stack.
- **Dead or not E1:**
  - `003306E0` and `003319D0` (kind 0xFF) sit behind the folded `005C5230` (returns 0), at `0032FCE8` and `0032FC67`.
  - `00377DC0` (kind 0xFF, bytes -1) goes to `002DF6C0`, which has no E1 check.

### E1 route 1: all languages (kind 35 `ff12menuoverlay_NN_debug.bin`, not in the archive)
1. A save-crystal menu is opened as request 6.
2. The router's generic widget `0027FB70`, built by `00280A00`, handles it.
   - Its open table `00280090` sends 6 to `0027FFD6`, which stores `+0xCC = 2`. Request 16 does the same at `0027FFCA`.
   - The tick then runs state 0 → 1 (`0027FD47`) → 2 (`0027FC0F`) → `0024AC10([+0xCC]=2)` at `0027FC2C`.
3. `0024AC10(2)` calls `0024AC30(2,0)`, and `0024AC30` calls `0032E400(0x23, 9)`, which returns -1 (`0024AC4C`).
4. If `0037B330() == 0` (the arena-11 mode, `0024AC53`), `0024AC30` calls `0032E620(0x23, 9, [01FD4A18], -1)` at `0024AC9F`, which builds the slot.
5. The pump calls `0046E030` → `002DF780`, and **`002DF7B9` is taken**.
6. Second route: the map screen, request 2 with parameter 0x40/0x41 → `002D7070` → proc `002D70F0`, state 11 → `0024ACE0` → `0024AC30(1,1)` → (35, 8), followed by a drain `0032E520(0)`.

- The mode condition is the only run-time condition.
  - `02ADD930`/`02ADD931` are zeroed at boot (`0037B390` at `0022A399`) and returned to 0 by `0024AB60`/`0035B8D0`.
  - They are set to 1 by `0035B840`, to 2 by `003DD6C0` (a slot with `+0x17 & 0x40`) and to 3 by the overlay itself.
  - The writer census is `e1_mode_writers.py` (FAILS 0; control `0037B458`): the bytes `0037B330` reads (`02ADD930`/`02ADD931`) are stored only by `0037B2F0` (copies the pending byte `02ADD932` unless it is 4; caller `002E66D3`), `0037B390` (boot, 0/0) and `0037B450` (callers `0024AB6F`, `0024AC7F`, `0035B877`, `0035B98B`, `003DD715`). `0037B3D0`, `0037B470` and `0037B490` write only `02ADD932`/`02ADD933`.
  - The skip arm `0024ACC1` is a folded assert (`0016D6A0(0x80000)`). If the mode is non-zero, no request is issued and the router waits at tick state 3. Only `0024ACF0` (the done callback) or `0024AC10(1)` set `02091094`.
- Consequence: `0024ACF0` sets `02091094 = 1` whether the stale status yields state 5 or 6, so the menu proceeds either way.

### Coordinator lead (RC-5, event sets 355/398/440): not an E1 route (`e1_kind8_sets.py`, FAILS 0)
- The FST side is confirmed. Kind 8 and kind 0x25 rows 1420..1423, 1592..1595 and 1760..1763 are -1 in **all 12** tables. Control: US rows 120..127 are positive.
- **The chain gates every request.** For `m` in 1..3, `0032FCA0` sets kind 8 and base = set·4 (`0032FD30`).
  - Each of its requests is preceded by `0032E400` of the same pair, and skipped on a negative result:
    - base+2 at `0032FE9E`, skipped by `js` `0032FE5E`;
    - base+1 at `0032FF0B`, skipped by `jl` `0032FED2`;
    - base+3 at `0032FF76`, skipped by `js` `0032FF38`;
    - (0x25, base+3) at `0032FFE2`, skipped by `jl` `0032FFA3`.
  - The primary base+0 request is at `00330444` in `ActorResource_BeginPrimaryPayloadLoad`, skipped by `jle` `00330378`. When set = 0xD4 and `022C6F10` is set, that arm copies memory instead of requesting.
  - The tail `0032EB40` is gated at `> 0x800` (`0032EBB3`).
  - `003306E0` is never taken (`r13d = setne(005C5230(5)) = 0`).
- So `0032FC30(m, 355)` builds no request for rows 1420..1423, and **E1 is not reached from that battle action**. The effect is that the set's resources are silently not loaded (the owner bits `0x1000/0x2000/0x4000/0x8000/0x20000` are not set).

## E2: `001D6F20(path, 1)` returns null at `002DF801` (and `002DF717`)

- Bodies were read to every return: `001D6F20`, `00597930`, `0059EE90`, `0059D900`, `001D6D20`, `0020C1B0`, `0020C300`, `0020BE50`, `001D6B20`/`0020C710`, `001D6B90`/`0020C720`.
- `001D6F20` returns null **only** from `001D6F7F`, after `0059D900` finds the record unset (`+8 == -1 && +0x10 == 0 && +0x20 == -1`).
  - If the 0x30 allocation `00210EC0` fails, `001D6F59` passes null to `0059D900`, which dereferences `[0+8]`. That is a crash, not a null return.
- The resolver `0059EE90` never sets `+8`. The record stays unset iff both of the following hold:
  - **route 1** (RAM FileCache, `001D6D20` → `0020C1B0`) is skipped or misses. A miss returns exactly -1 (`0020C2C7`); a hit returns the `0020C300` object or 0, which counts as set.
    - Route 1 is skipped when the extension filter `0059EF4B`–`0059EFA9` matches, when the length is ≤ 3, or when `01F83440` is 0.
  - **route 2** (package, `0019AEE0` on `lower(path.lstrip("./\\").replace("\\","/"))`, `0059F111`–`0059F192`) returns null (`0059F1C0`).
- On the loose route, the gate `001D6B40` = `0020BE50(cache, path)` looks up the **same map with the same key function** as route 1 (`0020C440` + `00674A00`, tree at `+0x28`).
  - For a path that passes the filter, route 1 therefore hits unless the entry is evicted between the two locked lookups. After a miss, route 2 still hits whenever the archive has the file.
  - **So E2 always requires a path the archive lacks.**
- `e2_path_census.py` (FAILS 0) runs `ResourcePath_Init` symbolically for each language and both values of its `edx` argument.
  - The kind-7 element patches apply only when edx = 0 (`002DFF86`). There were 0 unhandled writes.
  - Every FST-sized (kind, id) is resolved exactly as `002DF7CC` does. Controls: the system.cnf path is present; the kind-35 array names `ff12menuoverlay`; a fake key is reported absent.
  - Results:
    - every sized, non-NULL path is **in the archive** except **6 rows**: US (1,129), (1,130), (1,131); UK (1,131), (1,132); CN (1,127);
    - several sized ids resolve to a NULL pointer, e.g. US (1,1), (1,2);
    - by the code, a NULL path fails `0020BE50` (`rdx == 0`) and crashes at `001D6E20` on the archive route, so it is not E2.
  - Side finding: kind 1's array is shorter than the FST's kind-1 ids. US ids 109..132 resolve past the array's end into neighbouring `.ca` paths whose archive sizes differ from the FST value; ids 24 and 32 match.
- The cache map is filled by route-2 successes (PC-1 record `pc1-config-route`, not re-derived here). A key for an absent path can therefore enter the map only by a u32 key collision or by an insert path not read here (the map-jump prefetch).
- **DEPENDS-ON:** the fact stated at the top. The candidate paths are the six rows above (all kind 1; their live producers are `002EAD50`'s default arm, `0032FCA0` with m = 4, and the debug verb), plus `00377DC0`'s kind-0xFF paths.

## E3: `001A1220()` returns null (`001D6DB9` / `001D6FD9`)

- `001A1220` is `mov rax,[01F81160]; ret`. The cell is in `.data`'s virtual tail, so it is zero-initialised.
- `e3_readlayer_ptr.py` (FAILS 0) swept rip, image-base-relative, absolute and reloc forms over the cell ±0x10. The only stores covering the cell are:
  - `001A11E4` in `001A11B0`, the create. It stores the allocation `00584740(0x140228)` → `0019C580`, constructed by `0019F620`, or null if the allocation fails. Its only caller is `0017D56C` in the platform init `0017D4C0`, which runs unconditionally, before the game boot `0022A0B0` at `0017D5CC`.
  - `001A120A` in `001A11F0`, the destroy. Its only caller is `0017D679` in the teardown `0017D670`.
  - Image-base-relative: 0 verified. Absolute: 0. Relocs: 0.
- `e3_shutdown_reach.py` (FAILS 0; control: `0022B6E0` reaches the pump): the direct-call closure of everything `0017D670` runs after `0017D679` (55 functions) reaches no pump entry.
  - Its 22 functions with indirect calls are listed; they are CRT and Input code.
- Verdict: **UNREACHABLE**, except for the init-time allocation failure named above. In that case the loose route would crash earlier, at `001D6EF9` (an unchecked dereference of the same pointer).
- The null-out-pointer gates `001D6DC7`/`001D6FE7` are dead, as the probe notes say: all four call sites pass `lea 0215EFF4`.

## E4: a negative status other than -1

- The worker body is `001A07B0`: case 2 → `001A0CF0` (archive, from `001D6D90`); case 3 → `001A0E50` (loose, from `001D6FB0`).
- The completion `001D6D70` receives `ecx` = the low dword of job `+0x10` (`001A084F`).
- The result is stored as `mov eax,eax` (zero-extended). A read count therefore becomes a negative status only if it is ≥ 2^31. `002150E0`/`00215110` return counts clamped to the request, and `0020C150` returns 0 or `00217A70`'s value; `00217A70` was not read.
- **Loose `-2` (`001A0ED2`): UNREACHABLE.**
  - The record tested is job `+0x138`, which `001D6FB0` stored from its `rcx`. That is the object `001D6F20` returned after `0059D900` said "set" (`001D6F5C`).
  - `001D6FB0` passes `r8b = 1`, so `001A0BB0` runs `001A07B0` inline (`001A0BD9`–`001A0BDE`).
  - The only call between the check and `001A0EB5` that touches the record is `0059FBA0` (seek), which reads `+0x10`/`+8`/`+0x20` and writes none of them.
- **Archive `-2` (`001A0D80`): DEPENDS-ON.**
  - `00597970` runs the same resolver `0059EE90` on `rec+0x20` with selector 1. `0059D920` tests the same three fields at `+0x28`/`+0x30`/`+0x40`.
  - So `-2` ⇔ the path cannot be opened ⇔ it is absent from the archive, modulo a route-1 key collision.
  - The E2 census gives the complete list for FST-sized paths: the six kind-1 rows. NULL paths crash at `001D6E20` before the job exists.
  - Kind-0xFF paths come only from `00377DC0` (the other two raw-path producers are dead), which rewrites `ResourcePath_Get(kind, id)` (`002DF880`) and was not resolved.

## Limits
- The call-site, gate and branch classifications are hand reads of the per-site windows. The scripts supply the site census and the data checks; the reading aid `e1_site_summary.py` is not a verdict.
- The following were not censused:
  - which shipped scripts reach the staff roll (`00511540`);
  - the `m` values that reach `0032FC30` (m = 4 gives kind 1, id set+0x6B);
  - the model ids `002E6700` passes to `002EAD50`;
  - `00377DC0`'s path rewrite.
- The FileCache insert paths other than the route-2 commit were not read. E2 rests on that.
- Nothing was executed live.

## Scripts (all end with FAILS/STATUS)
| script | result | control |
|---|---|---|
| `e1_fst_writers.py` | 3 address forms; the only write is the boot fread | `002DF96D`, `002DF7B0` found |
| `e1_fst_census.py` | per-kind/per-language counts; 10 empty kinds; 0 zero or other-negative values | dword0 = 57; US 10,521 / 31 |
| `e1_slot_writers.py` | only `0032E870` writes `+0x21`/`+0x24` | `0032E943`, `0032E902` |
| `e1_producer_sites.py` (+ `e1_producer_windows.txt`) | 74 raw sites, 0 jcc, 0 address-takes | `002492F3`, `0032E84D`, `0032EC01` |
| `e1_site_summary.py` | reading aid for the 53 sites | size call `00249296` seen |
| `e1_static_ids.py` | static ids vs -1 set | (0,0) = 57; (35,9) = -1 |
| `e1_kind8_sets.py` | sets 355/398/440 are -1 in all 12; 5 gates verified | US rows 120..127 positive |
| `e2_path_census.py` | 6 sized non-NULL rows absent from the archive | system.cnf present; kind-35 array read; fake key absent |
| `e1_mode_writers.py` | stores to the arena-11 mode bytes | `0037B458` listed |
| `e3_readlayer_ptr.py` | 2 stores (create/destroy) | `001A1220` load found |
| `e3_shutdown_reach.py` | teardown closure reaches no pump entry | `0022B6E0` reaches the pump |
