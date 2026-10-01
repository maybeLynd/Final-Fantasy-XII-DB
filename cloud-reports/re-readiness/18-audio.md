# Reconstruction readiness: 18-Audio

- **System folder:** `FFXII TZA/18-Audio/` (every `.md` page in the folder and its subfolders; member `.tsv` files consulted only to confirm layouts and counts)
- **Board task:** OPUS-CLOUD-RE-READINESS-INPUT-AUDIO-1001
- **Date:** 2026-10-01
- **Brief:** `docs/cloud-briefs/re-readiness.md` (stream R). This is a draft written from the text snapshot only. Nothing here was checked against the executable.

## Pages read, with the status each page states

Paths are relative to `FFXII TZA/`. The alias in the first column is used in every citation below, in the form `ALIAS §section-heading :line`.

| alias | page | status line, as the page states it |
|---|---|---|
| R0 | `18-Audio/README.md` | no status line (category README) |
| R1 | `18-Audio/Sound-Bank-And-Voice-Formats/README.md` | no status line (folder README) |
| C-SR | `18-Audio/Audio-Boundary/CONTRACT-sound-request.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN` (:5-7) |
| C-FM | `18-Audio/CONTRACT-field-music-selection.md` | `level: L2 # calculation parity only; INTEGRATION untested, so not L3`, `readiness: DIFFERENTIAL TESTED`, `confidence: PROVEN` (:5-7) |
| C-MC | `18-Audio/CONTRACT-music-control-file-and-bgm-stream.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN` (:5-7) |
| C-SP | `18-Audio/CONTRACT-spatial-source-objects.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN` (:5-7) |
| C-BK | `18-Audio/Audio-Bank-And-Controller-Family/CONTRACT-audio-bank-and-controller-family.md` | `level: L2`, `readiness: CONTRACT READY`, `confidence: PROVEN` (:5-7) |
| BK | `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md` | `status: DOCUMENTED`, `evidence_tier: 1` (:4-5) |
| REQ | `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` | `status: AUDITED`, `evidence_tier: 1` (:4-6) |
| ENG | `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md` | `status: AUDITED — every question this page asks is closed (the 0215EFxx command block, UQ-254, answered 2026-09-17); the remaining ~130 functions of the inbound API surface are tracked as UQ-245 on the request page (UQ-253 superseded); status re-derived 2026-09-18 (FABLE)` (:4) |
| FADE | `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md` | `status: AUDITED`, `level: L1`, `readiness: BEHAVIORALLY UNDERSTOOD`, `confidence: PROVEN` (:4-9) |
| SAB | `18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md` | `status: AUDITED — the container, its families and how every bank is addressed are read; the 4,097 six-digit se banks' route (the record factory's id-based path) closed 2026-09-18` (:4) |
| CFG | `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md` | `status: AUDITED` (:4) |
| SEB | `18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md` | `status: AUDITED` (:4) |
| SPP | `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md` | `status: AUDITED` (:4) |
| TRG | `18-Audio/Sound-Selection/sound-trigger.md` | `status: AUDITED — the trigger, its slots, the seven parameter operations and the state-2 consumer (answered 2026-09-17), … every section-7 box is ticked …` (:4) |
| VAR | `18-Audio/Sound-Selection/sound-variant-selection.md` | `status: DOCUMENTED — SD-23, SD-24, SD-25, G-1 and G-13 are ANSWERED and G-2 is SUPERSEDED (owner re-status 2026-09-30, OPUS …)` (:4) |
| ANIM | `18-Audio/how-an-animation-makes-a-sound.md` | `status: DOCUMENTED`, `evidence_tier: 1` (:4-6) |
| AREA | `18-Audio/how-the-music-changes-when-you-change-area.md` | `status: DOCUMENTED`, `evidence_tier: 1` (:4-6) |
| MCF | `18-Audio/the-music-control-file-and-the-bgm-stream.md` | `status: AUDITED`, `evidence_tier: 1` (:4-6) |
| VPK | `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md` | `status: AUDITED — the slot, the verbs and the .vpc pack's layout read; the mode byte, the slot word and the states (GA-4) answered 2026-09-17, the cue table and the cue-index rule (GA-3) 2026-09-18` (:4) |
| WVAR | `18-Audio/which-variation-of-a-sound-you-hear.md` | `status: AUDITED — every register row is closed (owner re-status 2026-09-30, OPUS) …` (:4) |
| LAY | `18-Audio/the-spatial-audio-object-model.md` | `status: AUDITED`, `evidence_tier: 4` (:4-6) |
| DRV | `18-Audio/sqex-sd-sound-driver-architecture.md` | `status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) …`, `evidence_tier: 4` (:4-6) |
| SDID | `18-Audio/sead-engine-identity-and-diagnostics.md` | `status: AUDITED`, `evidence_tier: 2` (:4-6) |
| SFID | `18-Audio/sead-function-identification.md` | `status: AUDITED`, `evidence_tier: 2` (:4-6) |
| FIVE | `18-Audio/the-five-slot-array-the-console-reads.md` | `status: AUDITED` (:4) |

Member files consulted: `Audio-Boundary/members/pan-speaker-tables.tsv` (the ring tables for 1, 2, 6 and 8 outputs), `Audio-Boundary/members/se-index-census.tsv` (212 sites, 162 immediate, `se000.seb` 123 filled), `Sound-Selection/members/sndclass-census.tsv` (13,150 rows: class byte `+4` is 0 ×1,985 and 1 ×11,165), and `Sound-Selection/members/cyclekey-census.tsv` (11,165 sequence records, all version 4, key 0). Each matches its page's figure.

---

## 1. Interface

The folder documents ten parts. Four are the game's own audio layer:
- the sound-effect request path;
- music selection and the music command block;
- the script BGM stream and the voice packs;
- the bank and controller classes.

Two are game-side producers: the animation emitter and the map sound list. The other four belong to the statically linked SQEX::Sd ("SEAD") driver:
- spatial sources;
- selection and trigger;
- the mix path;
- start-up configuration.

The tables below are grouped that way.

### 1.1 Entry points (functions, with their callers)

**A. Sound-effect request path (game side)**

| entry | role | callers, as stated | source |
|---|---|---|---|
| `00249C60` (51 B) | gated wrapper: gate `02091098` → resolver `003A1180` → tail-call `002DF220(id, 0x40, 0x7F)`; one argument in `ecx` (the bank-local index) | 100 distinct non-Audio callers: "68 unowned / 29 UI / 3 Save_Load_Settings = 100". Named examples: `0057FE80`; the UI cancel paths `002BAF80`, `002D3BA0` and `0027EA70` | REQ §10.1 "Overturned — the census" :1187-1200; REQ §7 UQ-239 :840; C-SR §2 :62 |
| `00249CA0` (51 B) | the same wrapper, but with the resolver `003A11F0` (no liveness test) | "6 external callers"; `002D3BA0` when flag `0x20000000` of `+0xE4` is set | ENG §3 :133; REQ §7 UQ-239 :840 |
| `00271500` (42 B) | the `00249C60` shape with no gate check | not stated | C-SR §2 :64-68; REQ §2 scope table :96 |
| `0024A1A0` (46 B) | gated **stop** by id: `002DEE80` then `002DF0F0(id, 0)` → `001DBE90` → `00210C50` | not stated | C-SR §14 SR-1 :698-714; REQ §7 :950-964 |
| inlined resolve-and-play | each calls a resolver then `002DF220` directly, with no gate | `0030C650` (level-up), `003112F0` (hit result), `00357040` (script), `0046CC70` (presentation), `00366870`, `003E8690` | C-SR §2 :85-91 |
| `00357040` | handler of `sebsoundplay_2c1` (`0x02C1`, arity 4): `(bankClass, localIndex, pan, volume)`; bank class 1 → `003A1100`, 2 → `003A1070`, else `003A1180` | script VM | C-SR §2 :97-102; C-SR §14 SR-3 :754 |
| `003A1070` / `003A1100` / `003A1180` / `003A11F0` / `003A1240` | the five resolvers: `entry[+8]*512 + localIndex` | the wrappers above. `003A1240`'s only caller is `002E9FB2`, in `002E9D90` | C-SR §3 "The five resolvers" :162-184; C-SR §14 SR-6 :847-851 |
| `002DF220` (92 B) | play: refuses id −1 and the second gate, then `001DBDB0(0, id & 0x7FFFFFFF, (u8)pan, vol & 0x7F)` | "9 callers"; "5 external + 4 internal" | C-SR §7 :345-354; C-SR interior hub :1063-1070; ENG §3 :134 |
| `002DEF40` / `002DF010` / `003A0E20` / `002DEFA0` | play variants: selector from bit 31; pan-only; bit-30 two-byte encoding; descriptor play | `002DEF40` ← `mapsoundplay_2bb`; `002DF010` ← `mapsoundplay`; `002DEFA0` ← SP1 emitters `003638B0`; `003A0E20`: not stated | REQ §4 "The play call" :518-531; SPP §3 :109-117 |
| `001DBDB0` → `00210C00` | dispatch, then the fork: selector 0 → registry `+8` Seb `0021B5B0`; otherwise `+0x10` Sep `00219EA0` | `002DF220`, `002DEF40`, `002DF010` | REQ §2 "The dispatcher and the bank split" :215-267 |
| `00224570` (763 B) / `00223190` (356 B) | voice start inside the matched bank (pan through `002256F0`, volume through `002257E0`, start through `007A78B0`) | `00224540` ← `0021B5B0`; `00223160` ← `00219EA0` | REQ §3 :375-378; REQ §7 :993-1005 |
| `00249FC0` (7 B) | the only writer of gate `02091098` | `00512080` (verb `fsmenu_sedisable`, `7013`), `0027F5D0` (writes 1), `002D6F90` (writes 0) | C-SR §8 :404-437; C-SR §14 SR-4 :770-782 |
| `003A13F0` (582 B) | boot bank-slot setup: sets up the 66-node pool, then loads kind-32 entries 0/1/3 (`se000`/`se007`/`se002`), whose completions `003A1390`/`003A1330`/`003A12D0` set handles A/B/C | "called only from `00266D10`" | C-SR §14 SR-2 :722-726; REQ §7 UQ-243 :942 |
| `003A1650` | SE block registration (registry claim, then `002DEF00` → `001DBD20` → `0021B430` → `00223AD0`) | the actor-resource step `002E60F0` (kind-32 `.seb` load) | SEB §3.1 :83-107, §3.2 :168-174 |

**B. Music (game side)**

| entry | role | callers, as stated | source |
|---|---|---|---|
| `003EAA70` (229 B) | `FieldMusic_Select(fieldId)` → track or −1; calls only `FieldData_GetVariable0` (`00265270`) | exactly four: `0025D9E0` (site `0025DBC1`), `00261F90` (`00262034`), `0026DE20` (`0026DE4C`), `0026DEF0` (`0026DEF6`) | C-FM §2 :44-54; C-FM §14.4 :307-309 |
| `00261F90` (335 B) | area-transition music handler: a done-latch, then save override, mapped track, mode overrides `0x5B`/`0x5A`, then a crossfade | called every frame by the field pass | AREA intro :32-35, §2 :43-56, §3 :58-94 |
| `003EAB60` | musicctrl binder: `0051ED10(9, 0x20, 003EAB90)`, stored to `02B5E0D0` | tail-jump from `00379D20` ← `0022A0B0` ← `0017D4C0` ← `0017D000` ← job queued by `0017CF30` (`GameApplication` vtable `008C5760` slot 3) | C-MC §4 MC-1 :71-77, MC-2 :79-81 |
| `003EAB90` (71 B) | completion callback: rebases the page words in place | `0032E330` → trampoline `0051EDB0` (`movsxd rax, ecx` / `jmp rax`) | C-MC §2 :46-49; MCF §2.1 :108-113 |
| `002DEC30`, `002DEC80`, `002DECE0`, `002DED30`, `002DED70`, `002DEDB0` | music switch family; each ends with `0215EF44 = newTrack` | not stated (forward to `001DBC70`/`001DBCA0` → registry `+0x00`) | REQ §2 "The music block" :293-331; REQ interior table :2431-2435 |
| `002DEE50` / `002DEE30` | set the music level byte `0215EF4D` and forward | `00261F90` (`002DEE50(current, 0x78, 0x7F)`) | AREA §4-§5 :110-127 |
| `002DEC00` (7 B) | read the current track `0215EF44` | 12 non-Audio callers | REQ §3 :395; ENG §3 :138 |
| `003614C0` → `003614E0` | start a track at full volume (`r9d = 0x7F`) | `00261F90` | AREA §4 :116, §5 :123 |
| `00360C20` / `00361630` | four-slot track table: find / find-or-reserve | verbs `musicplay`/`musicread` (`022B`/`0229`) | AREA "DG-2 answered" :585-592 |
| `00360C70` → `00360B40` | load `musicinfo.bin` (kind 9 index 6) to `022CBA50` | boot initialiser `00266D10` | AREA "DG-2 answered" :600-604 |
| `00361010` (30 B) | `musicinfo[id].flags & 1` | "5 callers" | AREA interior `00361010` :660-665 |
| `002DE360` | music command-block initialiser | not stated | REQ §2 :297-312; ENG §7 UQ-254 :286 |
| `002DF530` | `Audio_SetMode`, clamps to `[0,2]` | `002DE110` (Config "Music" row) | REQ SWE2-EC7-27 :1845-1850; DRV §7 G-5 :539 |

**C. Script BGM stream**

| entry | role | callers | source |
|---|---|---|---|
| `003557C0`, `00354690`→`003EB100`, `00354920`→`003EB0A0`, `003EB150`, `003EADC0`→`003EAD10`, `003EB010`, `00355FB0`, `0050C7F0` | handlers of verbs `044D` usebgmstream, `0448` read, `0449` readsync, `044A` play, `044C` stop, `044E` free, `044F` status, `201E` debug (`044B` has no handler) | script VM. "0 of 1,115 `us` `.ebp` files call any of the verb ids" | MCF §3.2 :231-243; MCF corpus block :52 |
| `003EADE0` | stream state machine | `003EADD0` ← request pump `0032E070` (state-1 arm `0032E0BD`, and the end of every pass `0032E29B`) | MCF §3.3 :245-268 |
| `003EB050` | descriptor init | `0032EA90` | MCF §3.1 :209 |
| `003EB0D0` | "is the stream active" checker (a loop bounded to one) | `0032E620` (`0032E656`); verb `044F` | MCF §3.5 :294-300; C-MC MC-6 :123-126 |

**D. Voice packs**

| entry | role | callers | source |
|---|---|---|---|
| `0034EE40` / `0034E8B0` → `003EA0D0` → `003E9F80` | `voiceread` / `voiceread_20a`: reset the slot, then load table 1 then table 0 | script VM (`0085`, `020A`) | VPK §2.2 :71-102 |
| `003515B0` → `00351020` → `003581B0` → `003EA180`, `003E9BF0` → `003E9C10` | `voiceplay` (`0087`) and `_b5`/`_28b`/`_28c`: record the speaker; check `sabf`; `002DF660` stream bind; set pending | script VM | VPK §2.3 :131-160; VPK §4 GA-3 correction :245-250 |
| `003E9780` | pump post-pass: refreshes `+0x30`; starts the pending cues through `002DF680` while frame mode `02064AD3 == 2` | only `0032E070` | VPK §2.3 :155-160; VPK §7 :352-358 |
| `00351EB0`→`003EA2C0`; `00352E80`→`003EA430`; `00354A20`→`003EA4B0`; `00352DB0`→`003E98B0`; `003EA200` | voicestop / voicepan / voicechangepan / voicedispose / set+remove expanded voice memory (`0395`/`0396`) | script VM | VPK §2.4 :162-175; VPK §2.2 :90-92 |
| `003E9970(manager)` | free every slot owned by a manager | manager teardown `002628B0`, `00360710` | VPK §2.4 :170-172 |
| `0032FCA0` | `ActorResource_BeginManagerResourceSetLoad`: loads the `.snd`/`.mot`/`.vpc`/`.vpcjp` PKFL directories into `022C6E98`/`022C6E70`/`022C6EE8`/`022C6EC0` | only `WorldSimulation_ProcessDeferredModeRequest` `0032FC30` | VPK §2.5 :104-119; VPK §4 GA-5 :304 |

**E. Bank and controller family**

| entry | role | callers | source |
|---|---|---|---|
| `00210B30` / `00210AF0` / `002105E0` | registry get / lazy create (64 B) / constructor of the five controllers (construction order 0, 8, 0x10, 0x20, 0x18) | `001DBDB0`, the music forwards, the stream wrappers | REQ §2 :217-231; BK §3 :154-169 |
| `00210980` / `00210B60` / `00210C40` | per-format entries → loaders `00222740` (`.win.mab`, `%s%03d%s`) / `00223AD0` (`%s/se%03d/se%03d%s`) / `00222DC0` (`%s/se%03d/se%06d%s`) | music track reserve `002DEC70`→`001DBB80`; `.seb` registration; the `SeSep` walk `002DF070`→`001DBE60` | BK §4 :173-184; AREA "DG-2 answered" :585-592; REQ subtree `002DF070` :1802-1821 |
| `001DC2E0` → `00211270`→`0021D770`; `00211230`→`0021D6B0`→`002252C0`; `00211260`→`0021D700`; `00211280`→`0021D840`/`0021C870` | stream controller: bind / start / poll / stop | `002DF660`, `002DF680`, `002DF630`, `002DF690` (BGM stream, voice cues, bootstrap coordinator `003B8670`) | MCF §3.3 :269-282; MCF `002DF630/002DF680` subtrees :469-517; BK §7 BD-1 :268-275 |
| `001DC130` → `0021C680` | ShoutAudioController intake | completions `0036EAB0` / `0036E9F0` of the party read-in voice-pack load | BK §7 BD-1 :252-266 |
| bank vtable slots 0, 2, 3-5, 6, 9, 10; controller slots 0-7 | broadcast, teardown, gated re-dispatch, arm (pause/resume), manager-gated replay; register / drain / erase | vtable dispatch (callers not enumerated per slot) | BK §2 "The vtable slots" :95-130; C-BK §2 :46-63, AC-6 :116-132 |

**F. Animation sound emitter (game side)**

| entry | role | callers | source |
|---|---|---|---|
| `00520C50` (cmd `0x05`, through `0046CBA0`) / `00520D00` (cmd `0x29`) | authored animation commands → `0046CC70(emitter, mode, type, volume)` | the presentation command stream | ANIM §1 :34-41 |
| `0046CC70` (1,069 B) → `0046C250` picker, `002E9D90` lookup, `0046C6E0` audibility, `0046C8F0` descriptor + play | emitter play routine | the two commands above | ANIM §2-§5 :65-149 |
| `0034B7C0`, `0034C210`, `0034CA40` | script verbs that call `002E9D90` | script VM | ANIM "Cross-subsystem neighbours" :192 |

**G. Map sound list and weather ambience (game side)**

| entry | role | callers | source |
|---|---|---|---|
| `003635E0(list, bank, handle)` / `00363750` | bind (walk `SeSep`, register chunks) / unbind (keep list) | map-pack bind bit 0 in `003775D0` | SPP §3 :98-136 |
| `00346260` (`0x02BA`) / `00346990` (`0x02BB`) | `mapsoundplay(i)` → `002DF010`; `mapsoundplay_2bb` → `002DEF40` | script VM | SPP §3 :109-112 |
| `003638B0` | SP1 positional emitter play through `002DEFA0` | `003631B0` (SP1 walk) | SPP §3 :114-117 |
| `00363B40` | weather ambience selection | `002620E0` | SPP §3 :119-131 |

**H. SEAD driver (library side)**

| entry | role | callers | source |
|---|---|---|---|
| `00210760` | game audio start-up: reads `sead.win.config`, calls `007A4D50` (init) and `007A5B50` (Lay init), frees the buffer | `001DBA40` | CFG §3 :88-93 |
| `007A5400` | audio tick: QPC `dt` → `007AB5C0` (action consumer), `007AAEA0` (category step), `007B52B0` (sequence pass) then `007B5AD0` (voice pass) | not stated (the audio driver thread body, per register SD-25 quoted in VAR §10 :537) | FADE §4 :146-149; TRG §7 G-18 :377-379, G-19 :330 |
| `007AF740` → `007B0000` | device-clock voice pass (six walks) | installed as a device callback by `007AEF30` | SFID "The CoreSourceVoice::Render anomaly narrowed" :528-546; DRV §5 :433-441 |
| `007BC4F0` | Lay batch: calls every source's slot 34 | `007A5E50` | LAY §5 CO-2 :291-303 |
| `007BAEC0` | Lay action consumer: listener setters `007EF630`/`007EF790` | the action queue | LAY §2 CO-10 :88-97 |
| `007BD120` → slot 43 → `007BD240` → `007E7300` | the sound-instance stepper, selection, trigger and sequence arm | `007BDFA0`, `007BF0A0` (slot 42) | VAR §5 :267-273; TRG §2 :45-174 |
| `007A78B0` | handle-level play request (posts `0xA` for type 2, `0x1C` for type 8) | `00223190`, `00224570`, `00224E40`, `00224F10`, `002252C0`; `007EEA00`, `007F0820` | TRG §7 G-18 :402-407; BK §7 BD-2 :310-322 |
| `007A81F0` (cmd `0xE`, SetVolume), `007A84A0` (`0xB` stop), `007A8590` (`0xC` pause), `007A7A20` (`0xD` resume), `007A7E00`/`007A7E90` (pan mode / pan), `007A9650` (`0x26`, `Music::SyncTo`), `00210ED0` (action type 3, category volume) | SEAD handle API (posts queued commands) | game-side bank code, `002256F0`, `002257E0`, `00222B70`, `00222AD0`, `002DE0B0`/`002DE290`/`002DE310` | BK §7 BD-2 :286-309; REQ §4 "Pan" :569-584; DRV §7 G-3 :508-512, G-5 :539 |
| `007AEA20` | `CoreSourceVoice` factory | `007B9050`, `007DCE20`, `007EBAD0` (`Voice::Initialize`) | DRV §2e :258-278 |

### 1.2 Inputs and outputs (data read and written, with record layouts)

**Request call (game → audio).** `PlaySound(int32_t localIndex)` (one argument, in `ecx`). The result is the play call's result, or −1 (C-SR §2 :72-74). The wrappers pass `edx = 0x40` (pan) and `r8d = 0x7F` (volume) (C-SR §2 :74). `002DF220` masks volume `& 0x7F`, truncates pan to a byte, clears id bit 31 and inserts selector 0: dispatcher signature `(0, id, pan, volume)` (C-SR §13a :578-592). The id is `globalSoundId = bankSlot*512 + localIndex`, with the slot 0..63, so the id space is "exactly fifteen bits" (C-SR §3 :144-150).

**Failure returns.** Gate → −1. Resolver failure → −1. Id −1 at the play call → 0. Second gate → 0. `00267310` mute (verb only) → 0. **No bank owns the id → a receipt is still issued** (C-SR §10 :446-462). The receipt comes from `00212950`: `(counter+1) & 0x7FFFFFFF`, and 0 is replaced by 1 (REQ §4 "The play handle" :557-567; C-SR SWE2-EC7-69 :1093-1100).

**Slot pool / SE block registry at `02AEEDC0`.** 66 nodes × 24 B: 64 pool slots plus two list heads (`02AEF3C0` used, `02AEF3D8` free), and a 9-byte bitmap at `02AEF3F0`. Init: `+0` next, `+2` prev, `+4` = −1 (empty id), `+8` = i (self-tag), `+0xA`/`+0xE` = 0 (C-SR §15a "Resolved 2026-09-23" :958-972). Other fields stated:
- `+0xC`: a state byte (`003A1290`);
- `+0xE`: refcount; `+0xA`: generation (`003A0F80`);
- `+0x10`/`+0x14`: cleared by the sweep `003A0EA0` (C-SR §15a :974-985).

SEB gives "id `+0x04`, handle `+0x14`, use count `+0x0E`" (SEB §4 Data addresses :215). REQ describes the same table from origin `02AEEDC8`, with the tag at `+0`/`+2` (REQ §10.3a :1364-1384).

**Voice record (game side).** REQ §4 "The voice record" :610-623:
- `+0x08` the SQEX::Sd sound object;
- `+0x10` state (2 after reset);
- `+0x14` u64 = −1;
- `+0x18` playHandle;
- `+0x1C` volume 0..127 (default `0x7F`);
- `+0x20` pan 0..255 (default `0x40`);
- `+0x24` key;
- `+0x28` = 0;
- `+0x2C` kind.

**Bank record.** REQ §4 "The bank record" :625-640:
- `+0x08`/`+0x10` entry list;
- `+0x30` load state (1 loading, 2 ready);
- `+0x34` kind (1 Music, 2 Seb, 4 Sep, 6 Stream, 8 Shout);
- `+0x38` whole-id key;
- `+0x3C` bank-block key.

Object sizes: bank 0x38/0x48/0x58/0x68/0x68/0xA0; controllers 0x20/0xB8/0xE0 (BK §3 :134-152). Seb keys on `id/512` at `+0x3C`; Sep keys on the raw id at `+0x38` (C-SR §13a "The two dispatches" :661-677). Sep record factory `00222DC0`:
- `+0x3C` = id/100 (REQ subtree :1816) or id/1000 (SAB §3 :309); the pages disagree, see §2.4;
- `+0x40..+0x49` = the payload `{u32, u8}` twice;
- `+0x38` = id; `+0x30` = 1.

**Pan and volume formulas.** REQ §4 "Pan" :569-596:
- `002256F0`: `offset = pan<0x80 ? pan−0x40 : 0xBF−pan`; axis ±1; then `Sd_SetPanVector(voice+8, offset/128, axis, 0, frames/60)`.
- `002257E0`: clamp 0..127, `/127.0`, fade `/60` (REQ §4 "Volume" :598-608).
- Driver geometry: `pan` × π is the azimuth; `frpan` is the distance (`gain = |frpan|·g + 0.5·cos(|frpan|·π/2)`); `udpan` is unused; constant-power pairing over the speaker ring; ring tables in `pan-speaker-tables.tsv` (REQ §7 UQ-242 :938).

**Ramp (SEAD).** `+0x08` start, `+0x0C` target, `+0x10` elapsed, `+0x14` duration (0 means snap), `+0x1C` curve 0..5, stride `0x30` (FADE §2 :41-50). Further fields from `007CA560`: `+0x20` active, `+0x24` mode, `+0x28/+0x2C` slew limits, `+0x38` curve element (CFG §6d :457-463). The six curves (FADE §3 :105-113, corrected §6 :213-240):
- 0: `t`
- 1: `1−(1−t²)³`
- 2: `1−(1−t)²`
- 3: `t²`
- 4: `2ᵗ−1`
- 5: `2−2¹⁻ᵗ`
- above 5: 0

The advancer clamps `elapsed` at `duration` (FADE §4 DQ-1 :152-168). The category parameter is the product of its ramps × master `+0x48`/`+0x4C` (FADE §2 :80-97, §5 DQ-2 :177-199).

**Music table `musicctrl.bin`** (kind 9 index 0x20; 1,615 B). C-FM §3 :58-82; MCF §2.3 :176-187, §8 :399-403:
- header `"MUS0"`, `u32 maxFieldId` (1311), `u32 pageOffset[11]`;
- run `{u16 start:11|span:5, u8 count, u8 defaultTrack, {u16 threshold, u8 track}[count]}`, stride `4+3·count`.

Algorithm: C-FM §12 :151-190. Census: 291 runs, 48 with a ladder (MCF §2.3 :189-198). Track id → `music<id>.win.mab` (AREA "DG-2 answered" :581-598).

**`musicinfo.bin`** (kind 9 index 6): 256 × `{u8 flags, u8 track}`. Only bit 0 is read: it exempts the track from the mode overrides (AREA "DG-2 answered" :600-612; AREA §7 UQ-263 :165-180).

**BgmStream descriptor `02B5E0E0`** (0x38 B; MCF §3.1 :213-229):
- `+0x00` requestId (−1 idle); `+0x08` buffer; `+0x10` bufferBytes; `+0x14` soundHandle; `+0x18` streamId;
- `+0x1C` kind `0x24`; `+0x20` index; `+0x24` fileBytes; `+0x28` bytesRead; `+0x2C` ringCursor;
- `+0x30` state 1…8; `+0x31` active; `+0x32` `0x40`; `+0x33` `0x7F`.

State table: MCF §3.3 :260-268. Piece size `0x10000`; ring floor `0x30000`, rounded to 64 KB (MCF §3.2 :235, §3.3 :269).

**Voice slot** (64 × 0x40 at `02B5D0B0`; VPK §2.1 :47-65):
- `+0x00` manager; `+0x04` state; `+0x05` manager; `+0x07` heap;
- `+0x0C`/`+0x0E` kinds 0x25 / 8; `+0x10` id; `+0x14`/`+0x18` sizes;
- `+0x20`/`+0x28` tables; `+0x30` current; `+0x38` speaker records.

Cue entry (16 B in a `VSP1` block): `+0x08` offset (bits 0-23) | volume (bits 24-30) | pending (bit 31); `+0x0C` size; `+0x0F` pan; `+0x10` stream id; `+0x14` load handle. The last two physically sit in the next record (VPK §2.3 :139-147; §4 GA-3 :211-226). The voice language is bit 10 of `[020BE6E0]+4` (VPK §2.1 :67-69).

**`.sab`/`.mab` container** (SAB §2 :141-162):
- header `{magic sabf/mabf, u8 version 2, u8 flag, u16 dirDelta, u8 chunkCount, u8 nameLength, u16 param, u32 totalSize}`;
- directory at `((0x10+nameLength)&0xF0)+dirDelta`;
- 16-B chunk records `{tag, flags, offset (file-relative), pad}`;
- chunks `snd `/`seq `/`trk `/`mtrl` (`.sab`) and `musc`/`inst`/`mtrl` (`.mab`) (SAB §5 :341-343).

The `snd ` record (`SabFile::Sound`, version 16) and the `seq ` record (`SabFile::Sequence`, version 4) are tabled by version (VAR §12 "The version vocabulary" :695-709). `snd ` fields: `+4` class, `+5` count, `+1` cursor, `+0x19` bit 5, entry table at `u16 +0x1A`. `seq ` fields: weight `+0x10`, group `+0x11`, ranges `+0x10`/`+0x14`, byte `+8`. Macro and category fields of the Sound record: `+0x06` category, `+0x07` flags, `+0x0A`/`+0x0B`/`+0x4F` macro slots (CFG §6d :465-480). Addressing: Seb banks are `se<n>/se<n>.win.sab`; per-sound banks are `se<id/1000>/se<id>.win.sab` (SAB §3 :306-309).

**`.seb`** (SEB §2 :66-77): `{char[8] 'SeBlock ', i16 blockId, i16 slotCount 128, u32 fileSize, i32 slotOffset[128]}`. Only slot `+0` u32 (dead) and `+4` u8 (flag) are read. The re-seed rule for node `+0x09`: SEB §7 UQ-255 :342-355.

**`SPP1`** (SPP §2 :69-89): `{magic, count, bankLength, bankOffset, u16 hasMapNo, u16 mapNo, zero, u16 reservedAt, u16 weatherAt, zero}`, then `u32 soundId[count]`, then a weather table `{u16 n, i16 entryIndex[7]}`.

**`sead.win.config`** (`scnf`, 10 chunks; CFG §2 :52-84). Element grammars for `bus `, `eps `, `epsp`, `curv`, `hcam`, `ctgr`, `ctgl`: CFG §6d :346-510. `mcr ` bytecode: CFG §6c :265-345. Categories: `dummy0`, `music` (cap 4), `se` (48), `voice` (8) (CFG §7 WC-1 :526-536).

**Sound object (SEAD `Driver::Sound`).** TRG §4 :218-234; TRG §7 G-14 :324, G-16 :331-348, G-18 :373-432:
- `+0x30` record; `+0x4C` slotCount; `+0x54` state 0-7; `+0x400` slots (8 B);
- `+0x500` start offset; `+0x51C` start delay;
- ramp blocks `+0x88` (volume ×4), `+0x188` (pitch), `+0x1B8`/`+0x1E8`/`+0x218` (pan), `+0x2A8` (lowpass).

Sequence object: `+0x9C` state, `+0xA9` arm flag, `+0xAC` offset, `+0xC0` delay, dirty bytes `+0xA1..+0xA5`.

**Lay source object** (C-SP §3 :62-69; LAY §5 :280-288, :392-398, :506-515):
- `+0xD0..+0xDC` effective position (w = 1); `+0xE0` audibility; `+0xE4` radius; `+0xE1`; `+0x100` (Direction) vector;
- Dynamic: `+0x110` position, `+0x138` time, `+0x13C` dirty;
- Polygon: `+0x104` mode 0-4, `+0x108` count, `+0x110` vertices (16 B), `+0x218..+0x220` face indices.

Listener (0xA0 B at `[02EADE08]`): `+0x30` position, `+0x40`/`+0x50` directions, `+0x60..+0x9C` matrix, identity at creation (LAY §2 CO-5 :204-220).

**CoreSourceVoice** (DRV §4 :403-420): state `+0x80` (0 constructed, 1 opened, 2 paused, 3 playing, 4 closed), rate `+0x94`, position `+0x98`, start offset `+0xA0`, two-slot buffer queue `+0xB0..+0xC0`, gain `+0x100/+0x104`, pitch `+0x108`, sends `+0x218/+0x268`. Mix: eight-channel interleaved float, a fixed number of frames per tick (SFID :520-529).

**Animation emitter** (render record `+0x5F0`): byte `+0` enabled, `+1..+3` last-choice nibbles, `+4` countdown, `+5` group, `+6` variant, `+0x18` playing handle, `+0x1C` type (ANIM §2 :67-71, §5 :138-149). Selection table: ANIM §2 :73-83. Point table: ANIM §3 :98-110.

### 1.3 State (globals and objects, with lifetime)

| state | contents | initial value | written by / lifetime | source |
|---|---|---|---|---|
| `02091098` (u32) | global request gate; non-zero refuses the three gated entries | not stated | one writer `00249FC0`; the script and a widget raise it (state 10 of `0027F5D0`); `002D6F90` clears it at the widget's teardown | C-SR §3 :108; REQ §7 UQ-239 :809-840 |
| `022CB726` (s8) | second gate, read by `003603C0` | zeroed at boot by `00360370` (with `022CB724 = 0x5A`) | set by the skip reset `003601D0`; cleared by `00360110` when a definition payload binds | REQ §2 "Where the two gates come from" :341-343; REQ §7 UQ-240 :842-846 |
| `02AEF3FC` / `02AEF400` / `02AEF404` | handles A/B/C (`se000`/`se007`/`se002` registry handles) | A and C are set to −1 before their loads; **B starts at its `.bss` zero** | set once by the load callbacks; release not stated | C-SR §10 row 4 note :454; C-SR §14 SR-2 :722-746 |
| `02AEEDC0` pool / `02AEF3F0` bitmap | the 64-slot registry | built by the `003A13F0` init loop | release `003A0F80` (refcount, generation) | C-SR §15a :958-985 |
| `01FD36A0` | audio registry singleton (five controllers) | lazily created (64 B) by `00210AF0` | lifetime and release not stated | REQ §3 data :436 |
| `01FD36B4` | receipt counter | not stated | `00212950` | REQ §3 data :437 |
| `01FD36C0` | 128-entry request table | not stated | `00212A70` clears; base teardown `00222000` | REQ SWE2-EC7-68 :2050-2056; BK §2 slot 2 :108 |
| `0215EF44` / `0215EF4D` / `0215EF50` / `0215EFD8` / `0215EFDC` | current track (−1), music level (0), 16×8 handle table (never filled), group-hold mask (0), request serial | set by `002DE360` | switch family; `002DF370`; `002DF660` | REQ §2 :297-312; ENG §7 UQ-254 :286 |
| `02B5E0D0` | musicctrl table pointer (heap 5, below 2 GB) | `.bss` zero; valid only after the delivery and rebase (MC-3) | one writer `003EAB78`; "How often the framework dispatches slot 3, and whether heap 5 is ever released or reset, are NOT established" | C-MC MC-1 :71-77, MC-3 :83-85; C-FM §15 :351 |
| `022CBA50` | `musicinfo.bin` pointer | not stated (the loader clears it) | the `00360B40` store | AREA §7 UQ-263 :171-176 |
| `022CB9F0` | four track slots × 24 B: `+0` state (0/3/4/5), `+1` key, `+2` flags, `+3` handle | not stated | `00361630`, `00360D70` | REQ §4 "The four-slot track table" :656-667 |
| `02B5E0E0` | BgmStream (one) | `003EB050` | the verbs and `003EADE0` | MCF §3.1 :209-229 |
| `02B5D0B0` | 64 voice slots | not stated | the verbs; manager teardown | VPK §2.1 :47-65 |
| `022CBAF8`, `022CBA88`, `022CBB58/64/70`, `022CBA7C` | bound map sound list, handle (−1 none), weather selections / keep list, current ambience | not stated (`022CBA88` is −1 when none) | `003635E0` / `00363750` / `00363B40` | SPP §4 Data addresses :170-176 |
| `01F832E8` / `01F832E9` / `01DFE40C` / `01F832F0` / `01F832B0` | flag A (`sum_…0001`), sticky flag B (`spc_`), the in-progress slot (−1 at rest), five 32-B slot names, per-slot release dwords | `01DFE40C` is −1 at rest; the others not stated | `0020AC30` | REQ §11 :1440-1510; FIVE :54-66 |
| `02EADE08` | the one `Lay::Listener` | origin and identity matrix | created once by `007BB620` from `007A5B50` | LAY §2 CO-5 :204-220 |
| `02EAD3E0` | SEAD's copy of `sead.win.config` | memcpy of the file | one writer `007B0FF7` | CFG §6 :200-221 |
| `02EAD000` / `02EAD008` | category count and table (0x88-B Category objects) | built by `007AAA40` | for the process (not stated beyond that) | CFG §7 WC-1 :526-539 |
| `02EAD34C` / `02EAD348` / `02EAD350` / `02EAD354` | channel count (= 8), device rate, buffer bytes, frames per tick | `007AEF30` | device init | CFG §3 :150-156; SFID :520-528 |
| `01FD4138` voice pool | 1,024 shared voice records | `002216B0(0x400, 0x400)` from `00210895` | not stated | REQ §7 UQ-244 :986-991 |
| `02EAD010` / `02EADD70` | Action (1,024 × 40 B) and LayAction (512 × 80 B) pools | `007AB390` / `007BAC80` | not stated | SDID §7 G-24 :293-320 |
| `02EAD57C` | the opcode-165 compare global | 0 (two writers, both zero) | — | TRG §7 G-18 :424-427 |
| `01F403E0..F8` / `01F40410..28` | process-wide volume and pitch ramps | not stated | action types 5 / 6 | DRV §7 G-3 :525-527 |
| `0215E6E0` options record | `+0x08`/`+0x0A`/`+0x0C` category volumes 0..100; `+0x0E` soundtrack mode | `002DDE60` resets them to 100 | `002DE0B0`/`002DE290`/`002DE310`, `002DE110` | DRV §7 G-3 :508-520, G-5 :539 |
| `0215E710` | the polygon/spatial descriptor global | not stated | filled by `002DE800` | LAY CO-7 :627-693 |
| emitter `+0x5F0` | per-character emitter bytes | not stated | `0046CC70`/`0046C250` | ANIM §1 :41, §2 :67-71 |

### 1.4 Order (what runs when, and what triggers it)

**Boot / start-up, in the order the pages give where they give one.** Relative order between the bullets is not stated unless noted.
- Game audio start-up `00210760` (from `001DBA40`): reads the config, `007A4D50` (pools: Action 0x400, LayAction 0x200; mixer `007AC4F0`; categories `007AAA40`; config copy `007B0F90`), then `007A5B50` (Lay init, listener `007BB620`), then frees the buffer (CFG §3 :88-93; SDID §7 G-24 :307-310; LAY §2 :209-210).
- Voice pool `002216B0` from `00210895` (REQ §7 UQ-244 :986-988).
- Registry: lazy, on the first `00210B30` (REQ §2 :217-218).
- Area/boot initialiser `00266D10`: `003A13F0` (bank slots A/B/C) and `00360C70` (musicinfo) (C-SR §14 SR-2 :722; AREA DG-2 :600-603).
- The application init job: `0022A0B0` → `00379D20` → npcdic, questbase, then tail-jump to the musicctrl binder (MCF §2.1 :70-80; C-MC MC-1 :75-76).
- `0032EA90` → `003EB050` (BGM descriptor) (MCF §3.1 :209); `0032F430` (voice directories, resident `pre_z0000`) (VPK §2.5 :121-129).
- `002DE360` (music block): not stated when.

**Per game frame** (the frame order between these is not stated):
- Field pass `0025D9E0` calls `00261F90` every frame. The latch `context+0x10` bit `0x40` makes it run once per transition (AREA §2 :54-56).
- Request pump `0032E070`: the BGM machine in the state-1 arm (a submit skips the queue that pass) and at the end of every pass; then the voice post-pass `003E9780`, which starts cues only in frame mode 2 (MCF §3.3 :247-253; VPK §2.3 :155-160; VPK §4 GA-4 :277-281).
- Per-frame skip check `00360120` (sets the second gate through `003601D0`) (REQ §7 UQ-240 :844; REQ SWE2-EC7-66 :2027-2029).
- Weather ambience `00363B40` from `002620E0` after `00379860`/`00379290`/`003DE920` (SPP §3 :119-120).
- Animation commands fire when their animation reaches them (ANIM §6 :153-155).

**SEAD audio tick `007A5400`** (its own thread per SD-25, quoted in VAR §10 :537): `dt` from QPC, then `007AB5C0` (commands), `007AAEA0` (categories), the sequence pass `007B52B0` → `007E7540`, then the voice pass `007B5AD0` → `007E8BB0` (TRG §7 G-19 :330; G-18 :377-393). Where `007A5E50` (the Lay batch) sits in this order: not stated.

**Device clock** `007AF740` → `007B0000`: reset master → reset submixes → render sources (twice) → finish submixes → finish master (SFID :531-546; DRV §2c :215-216). How the device clock and the `007A5400` tick are ordered relative to each other: not stated.

**Lifecycle of one SE request:** wrapper → gates → resolve → `002DF220` → fork → the receipt is minted → bank walk → `00224570`: spin while load state 1 (`Sleep(0)`), voice from the shared pool, pan, volume, `007A78B0` (posts `0xA`) → the tick arms the Sound (`007BDFA0`, state 1→2) → the stepper runs slot 43 → trigger → sequence arm → the sequence pass pushes dirty parameters to the voice → the voice's slot 1 decodes and submits (REQ §5 :671-698; TRG §7 G-16/G-19 :330-348; BK §7 BD-2 :310-323).

### 1.5 Dependencies (on other systems)

| system | what audio uses | source |
|---|---|---|
| Resource and Asset Pipeline | request builder `0032E620`, pump `0032E070`, size table `0032E400` (`.fst`), whole-file loader `0051ED10`, path arrays (kind 9 `01EBF740`, kind 32 `01E7FCF0`, kind 33/39 shout tables) | MCF §2.1 :91-119; SEB §3.1 :94-107; C-MC §16a :222-225 |
| Script VM bridge | `sebsoundplay_2c1`, `fsmenu_sedisable`, voice verbs, BGM verbs, `mapsoundplay`, `musicplay`/`musicread`; pop order "reverse push order" | C-SR §7 :392-395; MCF §3.2; VPK §2.2-2.4 |
| Actor / World | ActorManager slot flags `02098E20` (liveness for `00267330`, sub-step byte for `00267310`); `FieldData_GetVariable0`; field pass `0025D9E0`; manager pack loads | REQ §4 "The world-live precondition" :492-502; C-FM §8 :116-120; VPK §2.5 |
| Save / Settings | save payload `+0x1063` bit `0x40` / `+0x1534` (pinned track); options record `0215E6E0`; config word `020BE6E0` | AREA §3 :74-76; DRV §7 G-3 :508-520; VPK §2.1 :67-69 |
| UI / Input | `0027F5D0` widget and synthesised cancel; UI sound callers | REQ §7 UQ-239 :809-840 |
| Battle runtime | mode tests `0037C8F0` (mode 1 → `0x5B`) / `0037C860` (mode 2 → `0x5A`) | AREA §7 :154-158 |
| Presentation | animation commands; render-record emitter; FCP radius `0x9001D1E`; presentation PRNG `003A6E60` / `01EF93E8` | ANIM §2-§3, falsification :218 |
| World / map pack | `.mpk` slots 0, 10, 16; weather slot `00265920` | SPP §3 :98-131 |
| CHSE tables | which `.seb` blocks an actor asks for | SEB §7 UQ-257 :383-391 |
| Frame loop | frame mode `02064AD3` (`00229EA0`) | VPK §4 GA-4 :277-281; SPP §7 :199 |
| Third-party libraries | CRI HCA, Tremor/vorbisfile, libogg, MS ADPCM (`007F6FB0`) | SFID §13 :364-403 |
| Platform | WASAPI device (`007DE2F0`), QPC timer | SFID §7 G-26 :216-223; SDID §2 :75-85 |

---

## 2. Gaps

Each gap gives the page, section and line that show it. "Not stated" means the folder says nothing about it.

### 2.1 Open or partly open items the pages themselves list

**Request path and banks**
1. **No live capture of any request-path behaviour.** "Live capture: still absent, and that is the gate this contract fails" (C-SR §13 :520-521). The live checks are queued and not run: "One attach answers all three, and none has been performed" (C-SR §13 :647-651). `INTEGRATION`, `TIMING` and `PRESENTATION` are "Not constructible offline" (C-SR §16 :1002-1005).
2. **The voice-object claim is still a runtime obligation.** "The outstanding claim is that a voice object is initialised from these fields … live-only" (C-SR §4 correction :211-218).
3. **Why `003A1070` guards on handle B and reads handle C:** "NO ADMISSIBLE SOURCE for the *why*" (C-SR §14 SR-2 :716-717, :748-750).
4. **Unread `0024A1A0` stop branches:** "What the bank slot `+8` does for `−4`, and the Seb `−1` / `−2` branch, were not opened" (REQ §7 :963-964).
5. **Pool-exhaustion behaviour:** "*Not established:* what the other classes' slot 4 frees when a pool is empty … and what the game does when the retry also fails" (REQ §7 UQ-244 :992).
6. **`007A78B0`'s first float (4.8):** REQ says "What 4.8 is … and what the registry question in step 2 asks were not read" (REQ §7 :1005). TRG answers only part of this, calling the 4.8 a dead load that is zeroed (TRG §7 G-18 :405). The step-2 registry question stays not stated.
7. **Pan geometry residue:** kind 9's class and slot 9 are "not identified" (REQ §7 UQ-242 :885). "The one-output table points at zero-initialised memory filled at run time" (:938). The spread's "ordinary initialized value and permissible caller range stay open" (:919-921; C-SR §4 :259-262).

**Lay spatial sources**
8. **Slot 34's consumer:** "**Not established:** what slot 11 does with the `0.0`, what slot 1's states 2 and 3 are, and who reads the batch arrays" (LAY §5 CO-2 :304-306).
9. **Slot 7 bodies:** "What slot 7 does in any class was not read" (LAY §5 CO-4 :316).
10. **Two of the three call sites of the spatial builder `00221940` (`00223259`, `002247CB`):** "what those carry is not established here" (LAY CO-7 answer :688-692).
11. **What `+0x218` (face indices) is read by:** "Its reader was not traced" (LAY CO-8 :711).
12. **`DynamicSound` radius source:** "What `DynamicSound` computes its radius **from** (SA-4)", and whether `+0xE0` is a cull or a mix weight (C-SP §14 :188-190). The four large Dynamic and Polygon bodies are only partly transcribed: "whose line-by-line arithmetic is not transcribed here" (LAY UQ-267 :443-446).

**Banks and controllers**
13. "What the five commands of AC-6's mask mean to a player" and why Stream lacks the `+0x20` member (C-BK §14 :206-209). BK slot 3/4/5: "what the `+0x60`/`+0x70` map is keyed on" (BK §7 BD-3 :334-335).

**Music**
14. **Music table lifetime:** "**UNKNOWN / NOT EXERCISED.**" (C-FM §15 :351). Producer, binding and scheduling "need appropriate evidence" (C-FM §13 :224-228; C-FM §16 :412-416). `INTEGRATION` is NOT TESTED (C-FM §17 :477).
15. **BGM stream:** "What the stream's eight states mean individually" and whether any consumer reads the table before the rebase (C-MC §14 :198-200).
16. **Track start fade units:** `003614C0(id, 0x78, 1)` → "`003614E0`, whose conversion was not read" (AREA §7 :152-153). `0x78` = 2.0 s is shown only for the outgoing fade.
17. **Music meter bodies:** "`007F3570` and `007F3800` … and what populates a meter in the first place" are not read (SDID "The two halves interlock" :266-268).
18. **`fhmusicdata.bin`:** it has a layout and "no reader in this build" (MCF §2.1 :121-139).

**Driver, selection and trigger**
19. **SEAD action records:** "**Not established:** what an `ACTION` record holds, and how often either pool comes near exhaustion in play (live-only)" (SDID §7 G-24 :319-320).
20. **Opcode-165 data census:** "which shipped `.sab` records carry an opcode-165 entry with a non-zero step or base" (TRG §7 G-18 :430-432).
21. **Who dispatches the voice's slot 1:** "the site that dispatches it (the tick's voice pass or the render callback) is not enumerated here" (TRG §7 G-19 :330).
22. **The 37/38 assert strings:** G-20 is ticked with no answer text on the page (SDID §7 :272-273). The 25 assert-named functions are "NOT APPLIED AS NAMES" (SFID :697-700).

**Voice packs**
23. **Voice cue references out of range:** 1,236 of 2,531 play sites are out of range of the same-named pack. "Which block `voiceread(slot)` binds is the loader-side question the authored data leaves open" (VPK §4 GA-3 :251). Other verbs are unread: "`voicereadsync`, `voicesync`, `voicestandby`, `voicevolume`, … only the six above are read here" (VPK §2.4 :173-175).

**Formats and config**
24. **Map sound list:** "The units of `0xF` and `0xB4` are not established here" (SPP §3 :131). Whether `env99.spp` is ever requested: "no located producer; the residue is a computed-kind producer" (SPP §7 SQ-1 :205). Whether any `mapsoundplay(n)` indexes past `count` is untested (SPP §9 :270-271).
25. **`sead.win.config`:** "Filter type 6's and SimpleFilter mode 2's filter shapes are unclassified, four WC-1 roles are medium confidence, and the authored parameter *names* are unrecoverable" (CFG §7 :552-554).
26. **Seb slot `u8` bit meanings:** "The individual bit *meanings* are also unnamed" (SEB §7 UQ-255 :326-327). Bits 2 and 4 are dead-authored (:353-355).

**Animation emitter**
27. **Emitter residue:** "what that byte [`+0xB5`] classifies was not established" (ANIM §3 :105). The front matter says "NOT read - the spatial descriptor builders and the play call beyond their arguments, the bank resolvers, the ground table, the three non-positional bank getters" (ANIM front matter :22-23).

**Five-slot array**
28. **The console's view:** "what a slot's dword holds, what `0020A760` does with a non-zero entry, what the console's fallback value is" (FIVE "Falsification pass" :78-79).

### 2.2 Structural gaps a re-implementer would hit (callees named but not described; formats located but not parsed)

1. **Bank chunk contents beyond `snd `/`seq `.**
   - SAB: "**Nothing about chunk contents.** `snd `, `seq `, `trk `, `mtrl`, `musc` and `inst` are located, bounded and named; none is parsed" (SAB §7 :445-447).
   - VAR §12 later places the `snd `/`seq ` fields the selects read, and SPP shows the `SeSep` payload beyond 5 bytes is dead on PC (SPP update :365-373).
   - **No page in the folder decodes `trk `, `mtrl`, `musc` or `inst`.** DRV: "named chunk classes (`ChunkTableElement`, `Material`, `MaterialChunk` …) which imply a chunked layout, but no offsets or widths are established" (DRV §4 :424-427).
   - Without them, a re-implementer cannot locate a sample's encoded data, its codec or its loop points. Where each voice's buffers are filled is answered only in the register (SD-20/SD-21, see item 4).
2. **The sequence opcode stream.** Only opcodes 2 (loop marker), 3 (fixed wait) and 5 (random wait) and the script opcodes 161-166 (165 in detail) are described (TRG §7 G-18 :384-393, :413-428). The rest of `007E6DD0`'s opcode set and the event-script interpreter `007B31A0`'s full vocabulary (23 live `mcr` opcodes are listed in CFG §6c) are not described for sequences.
3. **`Magi::Music` playback.**
   - Only the meter converter `007F31F0`, `SetMode`, `SyncTo` and the section-transition request are identified (SDID "The Music meter" :220-268; SFID §7 G-26 :219-220; SFID :486-498).
   - How a `.mab` is played is not described: sections, loops, custom points, `UpdateTransition`, `UpdateRemainingLoopCount`, and the `+0x190`/`+0xD8`/`+0x638` start fields (BK §7 BD-2 :319-322).
   - The music controller's start body `002251B0` is only an anchor ("the music-bank start body", MCF :533-535).
4. **The mix-path remainder is answered only off-page.** DRV still says the decode kernels, the eleven other `CoreSourceVoice` slots, the pool take `007DF750` and "who calls start and queue" are "Registered as `SD-21`", and the callback class at `+0x88` is `SD-20` (DRV §2b :185-187, §2c :226-227, §2e :276-278). The status line says both were answered on 2026-09-30 (DRV :4). The answers are in register records outside this folder, not on the page.
5. **Callees named with one-line roles only** (an interior anchor and no behaviour). Examples:
   - the bodies of the `0020Axxx` name-registrar subtree (REQ :1749-1765, "object bookkeeping");
   - `00221D60` (REQ :1985-1987);
   - `003D7F30`, `00361200`, `00361630`, `00207E90` (REQ :1928-1945);
   - `00225030`, `0021D770`, `00221C70` (MCF :529-545);
   - `00222080`, `00223A20` (BK :572-583);
   - `003E5B30`, `00224E40`, `0021C760` (LAY :881-903).
6. **Voice-start internals.** `00224570`'s RB-tree lookup by `id % 512`, the reuse conditions ("Seb reuse needs all three of `state==1`, the `~s6d` flag and bit 7 of `sd+4`") and the callback-arm asymmetry are given as one-line findings, not as a layout (C-SR §13a "The fork, both dispatches and the workers, executed" :685-689). The `sd` record's layout: not stated.
7. **Initial values not given** for the global gate `02091098`, the receipt counter `01FD36B4`, the voice slot array `02B5D0B0`, the track slots `022CB9F0` and the map-sound state `022CBB58`… (§1.3 table). Teardown or release of the registry singleton, the shared voice pool and the Category table: not stated.
8. **Frame order.** Where the field pass, the request pump, the per-frame skip check and the weather ambience fall relative to each other in a frame is not stated (§1.4). Neither is how the SEAD tick `007A5400` relates to the device callback `007AF740`, or where `007A5E50` (the Lay batch) is called.
9. **Formula given only for some inputs.**
   - The `PolygonSound` modes are described for the `00224E40` route only (LAY :688-692).
   - The fallback meter grid is given (SDID :235-251), but meter population is not.
   - The pan setter's mapping above `0x7F` is given, but the stereo-voice side "cannot" be inferred from pan alone (C-SR §4 :226-248).
   - SwitchSound's `"distance"` and by-name switches "are never reached" on shipped data (VAR §7 G-11 :354-359).
10. **The game-facing upstream surface.** UQ-245 ("the remaining ~130 functions of the corrected 168-function inbound surface") was closed SUPERSEDED as a population statement, not answered (REQ §7 :1006-1007). The inbound surface is a floor: 182 functions and 325 callers by byte decode (REQ §10.1 :1206-1218).

### 2.3 Fields written by documented functions but left unexplained

- Bank record `+0x18`..`+0x2C` (allocator, `+0x20` u64 = 0, `+0x28` = −1, `+0x2C` = 0): meaning not stated (REQ §4 "The bank record" :629-635).
- Voice record `+0x28` (= 0 on reset) and `+0x2C` "kind tested by the pan setter's assert": the values of the kind are not stated (REQ §4 "The voice record" :621-622).
- `002E9D90`'s "two enable bytes" and "the actor's manager allows it": not identified (ANIM §4 :114).
- `hcam +0x01 = 16` → params `+8`: what it configures is not named (CFG §6d :365-369). The "16" is never given a meaning anywhere in the folder.
- `+0x294` on `CoreSourceVoice` is first "**not named here**" (DRV §2a :129) and later identified as the resampler fraction (DRV §2b :160-161).
- SPP `+0x10`/`+0x12` MapNo pair and `+0x18`: dead-authored on PC (SPP §7 SQ-1 :205).
- `musicinfo.bin` flag bits 1, 2 and 7 and the second byte have no reader (AREA §7 UQ-263 :165-180). They are safe to ignore.
- `.seb` slot `u32` is dead (SEB §7 :342-345); `SeSep` payload bytes 5+ are dead (SPP update :365-373); `dword0` of the Sep record: "no reader … found in the bank code" (SPP :382-398).

### 2.4 Contradictions between or within pages

A re-implementer has to resolve each of these before relying on the value.

1. **Second-gate polarity (`003603C0` at `002DF220`).** The page and contract say non-zero refuses:
   - REQ §2 :179-181 ("test eax, eax / jne return 0") and REQ §3 data :431;
   - C-SR §10 row 5 :455 and §12 :508;
   - C-SR §15 :883 ("`je` to the work, falling through to `xor eax,eax`").

   Two passages read the other way:
   - C-SR §13a :596-598: "`002DF23B call 003603C0` / `test eax, eax` / `je` both land on `002DF244 xor eax, eax`";
   - C-SR interior hub :1065-1066: "`ecx == -1` or **a zero from `003603C0`** returns 0".

   Both crossings sections call `022CB726` "the single global **enable** byte" (C-SR :1021-1024; ENG :673-675).
2. **Teardown of the three handles.**
   - C-SR §3 :119-121: "all three reset to `-1` by the 582-byte teardown `003A13F0`".
   - REQ §2 :107: "it first resets all three to `−1`".
   - Both contradict C-SR §15 correction :889 and §14 SR-2 :722-726 (B is never written; `003A13F0` is the boot loader).
   - REQ §3 still names `003A13F0` `Audio_ReleaseBankSlots`, "invalidates `02AEF3FC`" (:358). REQ §7 UQ-243 calls it "the boot routine" (:942).
3. **`002DF010`'s volume.** REQ §3 says "`Audio_PlayResolvedSound_PanOnly` … passes only `0x40`" (:364). REQ's interior table says it "tail-calls `001DBDB0(…, 0x40, 0x7F)`" (:2437).
4. **`00360C20`'s return.** REQ §4 table: `+0x03` handle "the value returned to callers" (:663). Interior table: "returns that slot's byte `+0`" (:2438).
5. **`003A0E20` argument order.** REQ §4 :529 has `002DF4D0((id >> 8) & 0xFF, id & 0xFF, …)`. LAY SWE2-EC7-73 :908-909 has `002DF4D0(cl, cl>>8, edx, r8d)`.
6. **Sep record `+0x3C`.** REQ subtree :1816 and :1820: "`id / 100` … round-toward-zero divide by 100". SAB §3 :309 and SPP update :310-311: the same `0x10624DD3`/`sar 6` sequence is a divide by 1,000.
7. **Who raises the gate at `0x42`.** ENG §7 :273-274: `0027F5D0` "closes it … in the sub-state entered when its parameter `+0xD4` is `0x42`". C-SR §14 SR-4 :773-778 and REQ §7 UQ-239 :816-826: raised in state 10; `+0xD4 == 0x42` gates the call to the teardown `002D6F90`, which clears it.
8. **Controller `+0x20`.** C-BK AC-3 :91-96 calls it "a SECOND BASE", and C-BK §14 :206-207 still asks what that base is. BK §7 BD-4 :336-359: "not a base at all — an embedded request queue", reworded the same day to the controller's **bank pool**. C-BK §7 :166 still says "drain the request queue (slot 7)".
9. **Broadcast vtable load.** BK §2 slot 0 :106 says `rax = [this]` is "loaded once before the loop". C-BK AC-4 :98-107 says it is inside the loop and that it "corrects the family page". The page text was not changed.
10. **AC-6 mask width.** "a FIVE-BIT COMMAND MASK" (C-BK :116; BK :113 "five-bit"), but six bits are listed: `1, 2, 4, 8, 0x10, 0x20` (C-BK :126-129).
11. **Base controller constructor.** `00212710` (REQ §3 :384, §8 :1029, :1115) against `002130E0`, "the base constructor `002130E0` zero-fills `+0x08`–`+0x38`" (BK §7 BD-4 :339; BK crossings :488).
12. **The lazy driver object's offset.** "The +0x50 field the Sep slot-8 bodies require … (lazy-created through `00221D10`…)" (BK §2 :128-129) against "`00221D10` … `[rcx+0x20]` is returned when live … the result is stored to `+0x20`" (BK SWE2-EC7-68 :614-618).
13. **The pool constants.** BK §7 BR-8 :241-243: "2 concurrent music voices, 96 environmental, 256 effect …". The correction box above it, BK §7 :223-230, says they are bank objects, not voices.
14. **The spatial contract is stale about the bank family.** C-SP :34-35 and §6 :142 say "the bank and controller family remains uncontracted". C-BK exists and claims it (C-BK :32-35).
15. **Lay slot tables.**
    - LAY §2 :114-120 ("`DirectionSound` **no**", "`AmbientSound` **no override at all**"), LAY §4 :262 and §6 :455 are superseded by the correction at :122-160 but still read as current.
    - LAY CO-6 :324 says Ambient "contributes five slots of its own (0, 1, 7, 34, 35), not three". UQ-267 :367 says "3 own bodies".
    - The object table :512 says mode byte "`0` selects nearest-vertex, non-zero selects plane-and-edges". The correction :488-498 has five modes.
    - DRV §7 G-4 :537 still calls `+0xE0` "the ready byte". C-SP SA-3 :88-103 says it is audibility.
16. **Pan axes.** SFID §2 :121-122 and §6 :198: "three panning axes … left/right, front/rear, and up/down". REQ §7 UQ-242 :938: `pan` is an azimuth, `frpan` a distance factor, and `udpan` "is carried all the way down and then not used".
17. **`SetVolume` ceiling.** SFID §3 :162-163 and §4 :182: "the volume ceiling is configurable rather than hardcoded" (`DAT_01cebba8`). REQ §3 data :449 and FADE :85 give `01CEBBA8` as the constant `+1.0f`. FADE §5 :192 gives the range as `0.0`–`1.0`.
18. **Output channel count.** `02EAD34C` is "the constant **8**" (SFID :522-523; CFG §3 :150-152). REQ §7 UQ-242 :938 reads the speaker ring "by the device's output-channel count (`007AECE0` returns `[02EAD34C]`)", with distinct tables for two, six and eight outputs (`pan-speaker-tables.tsv`).
19. **Device backend.** SDID §2 :75-85 says WASAPI, "Not XAudio2". MCF :514 calls `007A7010`/`007A78B0`/`007A7A20` "the XAudio-side calls".
20. **BGM stream start parameters.**
    - MCF §3.3 :277-278 and C-MC MC-8 :133-136: `0x40`/`0x7F` are centre pan / full volume.
    - The MCF `002DF630/002DF680` subtree :486-487 says `002252C0` calls "`002256F0(arg4 = 0x7F, the volume)`, `002257E0(arg3 = 0x40)`", which sends `0x7F` to the pan setter.
    - MCF §5 :327: "What `0x40` and `0x7F` set on the bank … is not named. `FZ-15`."
    - Also, MCF :450 says `002DF690` is the close "this page's state 6 names". State 6 calls `002DF680` (:265).
21. **musicctrl span maximum.** MCF §2.3 :191: "largest span 22 = 23 fields". MCF §8 :406: "`span` **0 in 169** (max 5)".
22. **Music-block gate bit.** AREA §3 :60: the music block runs when `context + 0x17` has **bit 7** set. AREA §7 UQ-264 :181: "the non-music path (`context + 0x17` **bit 2** clear)".
23. **musicinfo pointer.** AREA interior :663 reads `[022DBA50]`. Everywhere else it is `022CBA50` (AREA :84-86, :603).
24. **Mutant count.** C-FM §13a :233: "22/22 cases and 10/10 mutants killed". C-FM :272: "the 22 cases and 20 mutants stay as recorded".
25. **Producer question.** C-FM §14.1 :294-300 says `DG-1` is ANSWERED. C-FM §16 :412-416 says "Requires further original-game evidence: the table producer and lifetime (`DG-1`)". C-MC :2 says "Load the music-control table once per process", but its own MC-1 :71-77 withdraws "once per process".
26. **`dt` sign.** FADE §4 :146-149: "`dt` is traced … It cannot be negative". FADE :167-168: "`dt` itself (the `xmm1` argument) was not traced, so a negative step is not ruled out".
27. **Curve 0.** FADE §6 :213-240: curve 0 is linear, "a different arm from out-of-range". CFG §6d :450-453 lists five arms and "default `0`", which omits the linear arm.
28. **Trigger block offsets and stale statements.**
    - TRG §2 :115 and §4 :224-225 put the indexed block at `+0x254 + i*0x30`. TRG §7 G-14 :324 puts it at `+0x248 + i×0x30` (`+0x250` start, `+0x254` target, …).
    - TRG §8 :446-448 still says naming any parameter "volume" or "pitch" "would be a guess". G-14 names them.
    - TRG §5 :295 and :300 still say `007E7300` is "unread"; §2 :149-162 reads it.
29. **The byte at Sequence `+0x10`.** WVAR :176 says `007CF830` "asks whether a range is authored". VAR §10-§11 :500-505, :574 say the same accessor reads the per-candidate **weight**. TRG UQ-259 :585 says the field is shared ("read one field two ways").
30. **Weighted-pass fallback.** VAR §11 :613-615: "selection always falls through to the uniform second pass". VAR §12 :637-644: pass 1 plays every zero-weight set, then one weighted draw; there is no "uniform second pass".
31. **Animation RNG.** ANIM crossings :183-184 still say "**Gameplay - SHARED GENERATOR.** The picker draws from the gameplay random number generator". The page's CON-190 correction says it is the presentation PRNG (ANIM §2 :67-69; falsification :218).
32. **Voice-slot states.** VPK §2.1 :53 says "1 already resident · 2 requested · 3 loaded · 4 · 5 loaded, sized". VPK §4 GA-4 :288-299 says 1 = parked (no read issued; nothing promotes it), 4 = dispose pending, 5 = more to come.
33. **`.sab` `+0x0A` and addressing.**
    - SAB §5 :347 and §6b :405 report "350 distinct values in `.sab`". The SPP update :327-332 calls it "a strict ordinal … one slot per folder … 268 folders" (0..267).
    - SAB §7 :448-453 still says `+0x0A` is "undecided" and "How the 4,345 `se` banks are addressed is not established". SAB §3 :214-256 and :309 answer both.
34. **SR-1 stale.** C-SR §14 SR-1 :713-714: "`00210C50` remains unread". SR-7 :861-865 and REQ's interior table :2418 read it.
35. **"Any execution: none".** C-SR §15 :900: "any execution of this path, isolated or live | **none**; §13". C-SR §13 :520-529 records 326 isolated-execution comparisons, and §13a records EXP-096 and EXP-105.
36. **Status-line conflicts.**
    - DRV :4 says `DOCUMENTED`; DRV :33 says "**Status is PARTIAL**".
    - VAR :4 says `DOCUMENTED`; VAR :32 says "**PARTIAL.**".
    - R0 :29 lists the voice-pack page as "**PARTIAL, tier 1**"; VPK :4 says `AUDITED`.
    - R0 lists 4 of the folder's systems, then says "_None yet._ … entirely undocumented" (R0 :33).
    - R1 :3-5 still calls the formats "the largest undocumented hole".
    - DRV §7 G-3 :534-535 still says "**Still open:** which rows … send commands `0x13`–`0x15` — `SD-22`"; DRV :4 says SD-22 was answered on 2026-09-30.
    - CFG §1 :47-48: "Which game setting drives which category is not traced here". CFG §7 :540-542 traces it.
    - DRV :369 gives `CoreSourceVoice` 16 methods; DRV §2c :199 gives 17 slots.

---

## 3. Rating

**NOT YET** for `18-Audio` as a whole. The game-side layer on its own is **MOSTLY**.

**Why the game-side layer is MOSTLY.**
- It is documented at tier 1, mostly from static reads of the shipping image, with five L2 contracts that each passed one falsification pass.
- From the database alone, a re-implementer could write these parts with named gaps only:
  - the request path: the wrappers, five resolvers, both gates, the 66-node registry, the receipt rule, and the fork to Seb/Sep with their two keying rules (C-SR, REQ);
  - field music selection, which is differentially tested on shipped bytes (C-FM §17);
  - the musicctrl load/rebase and the BGM stream machine (C-MC, MCF);
  - the voice-pack slots and cue table (VPK);
  - the map sound list and weather ambience (SPP);
  - the animation emitter (ANIM);
  - the bank/controller object model (C-BK, BK);
  - every authored file header (`.sab`, `.seb`, `SPP1`, `scnf`, `musicctrl`, `musicinfo`).
- The named gaps that keep it below READY are §2.1 items 1-7, 13-16, 23-24 and 27, plus the uninitialised-state and frame-order gaps in §2.2 items 7-8.
- About thirty contradictions in §2.4 would have to be settled first. Several of them change values a port would hard-code:
  - the second-gate polarity (2.4.1);
  - the BGM/voice pan and volume order at `002252C0` (2.4.20);
  - `id/100` against `id/1000` (2.4.6);
  - `002DF010`'s volume (2.4.3).

**Why the system as a whole is NOT YET.** The gaps are structural, not field-level.
1. **Content formats.**
   - The playable content of a bank is undocumented: `trk `, `mtrl`, `musc` and `inst` are "located, bounded and named; none is parsed" (SAB §7 :445-447).
   - Only three sequence opcodes are described (TRG G-18).
   - So a re-implementer cannot get from a resolved sound id to samples, loops and track structure using this folder.
2. **Music playback.**
   - Music playback (`Magi::Music`, `.mab`) is identified by name and a few methods only (§2.2 item 3).
   - Area music depends on it (`music<id>.win.mab`, AREA DG-2).
3. **The SEAD mix and voice remainder.**
   - The SEAD mix and voice remainder that the pages call `SD-20`/`SD-21` is answered only in register records outside the folder (§2.2 item 4).
   - The decoders it relies on (CRI HCA, Tremor, MS ADPCM) are third-party and out of this folder's scope (SFID §13).
4. **No runtime evidence.**
   - No part of the request, bank or spatial chain has runtime-validated behaviour (C-SR §13 :520-521; C-SP §13 :181-184; C-BK §13 :199-202).
   - Field music has native-oracle evidence for two input conditions only (C-FM §13 :217-228).

**What would move the rating.**
- **To MOSTLY overall:**
  - a format sheet for `trk `/`mtrl` and `musc`/`inst`, plus the sequence opcode table;
  - a `Magi::Music` playback page;
  - the SD-20/SD-21 answers copied onto DRV;
  - the §2.4 contradictions resolved on the pages.
- **To READY:** the live checks C-SR already designed (§13 :647-651) and the `INTEGRATION` rows of the contracts.
