# S-38 runtime: per-invariant stub exposure for EXP-108/109/112/117–123/125/126/128 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-38 character rendering.
- **Runtime verdict:** MIXED, with the qualifier *"isolated original-code execution under disclosed stubs — no
  per-invariant stub-exposure analysis yet"*.
- **The cell's records:** 13, "the render family" — EXP-108, 109, 112, 117, 118, 119, 120, 121, 122, 123, 125, 126
  and 128.
- **Binding gap:** *"types PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap; the contract no longer binds
  it"*.
- **Contracts** (`important-subsystems.tsv` col 6):
  - `17-Presentation-Rendering/CONTRACT-character-transform-publish.md` (TP);
  - `CONTRACT-coast-down-latch.md` (CD);
  - `CONTRACT-render-record-pool-lifecycle.md` (RP, invariants 1–5);
  - `CONTRACT-character-render-object.md` (RO, R-1..R-7).

Evidence class throughout: NATIVE-REPLAY (Unicorn, shipped bytes at their real VAs). `live_game: false` on all 13
records. Nothing here is live. This note scores nothing.

## Which contract each record belongs to

Only **one** of the 13 records executes an S-38 contract's §4 invariant set.

| record | front-matter `contract:` | subject | S-38 §4 invariant executed? |
|---|---|---|---|
| EXP-109 | RP | the six lifecycle operations `004269A0` / `004278E0` / `004279B0` / `00428710` / `00427C90` / `00429140` | **yes: RP 1–5** |
| EXP-117 | RP | slot-handle algebra `003B56D0` + RES/MIDS/D6A over the `0xE0` pool `q[02B40528]` | no. It runs two of EXP-109's scripted callees (`003B56D0` HID, `002ED570` MIDS) real |
| EXP-118 | RP | vector writer `003E5B30` (RP §21, not §4) | no |
| EXP-119 | RP | `0051B9E0` → `0051F240` T51, `00370E20` E20 | no. It runs EXP-109's scripted T51 real |
| EXP-120 | RP | `003E56A0` F56, `00370F60` F60 | no. It runs EXP-109's scripted E56 real |
| EXP-108 | **`CONTRACT-authored-command-ramp-channels.md`**, which is **S-48**'s | ramp consumers `003B6020` / `003B62D0` | no, it is another row's contract |
| EXP-112 | **`04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`** | actor record ctor `00266530`. This is not the `0x740` render record | no, it is another category's contract |
| EXP-121, EXP-128 | **`02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md`** | queue tails / the `0032E070` pump | no |
| EXP-122, 123, 125, 126 | **none** ("the general allocator …") | allocator `0036A100` / `0036BC60` / move scan / free path | no |

No record in the cell executes **TP's `001FB120`**, **CD's `00424080`**, or **RO's `001F4DA0` / `001F51E0` /
`001F6E70`**. I grepped every `_experiments/EXP-*.md` and every `evidence/*/check.py` for those VAs and found no
hits. `001FB120` and `00424080` *are* executed, but by the differential pilots
`Reconstruction/Tests/Differential/diff_character_publish.py` and `diff_coast_down.py`. Those are not EXP records
and are not named in the cell (see the last section).

## Substitutions per record

Classes:
- **app** = application stub (a scripted game function);
- **imp** = import bridge (a CRT/OS import, resolved through the PE import directory);
- **fix** = fixture (planted data or a planted callback).

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-109** (`evidence/render-pool-lifecycle-exec`; bodies.json `real` 29 / `scripted` 18; the hooks in `World.__init__`) | CTOR `004269A0`, LKUP `004278E0`, ALOC `004279B0`, PROM `00428710`, RETI `00427C90`, RELE `00429140`. CLR `0041F730` (1208 B). DRAIN `00426EC0`. HC1 `003B6000`, HC2 `003AFBE0`. G68 `003E68E0`, L2D `00422D50`. BASE `0020E600`, BAS2 `0020E620`. T1W/T2W/T3W `0041D6C0/D0/E0`. F4W `006C0520`, CPY `0046D110` → `00202C70`, A8W `003E5D00`, Z50 `003E37E0`. Inits `003B6890`, `003AFCD0`, `004778A0`, `003AF2B0`, `0042F000`, `003B53C0`, `003E0720` | **app:** RINIT `00420480`, PTD `0041FCF0`, HID `003B56D0` (planted return), PHOOK `0042C410`, TDOWN `004200A0`, F4C0 `0042F4C0`, E56 `003E56A0`, MIDS `002ED570`, T51 `0051B9E0`, `00512EF0`, `0040DB70`, `0032E400` / `620` / `520`, and the allocator trio `0036C1D0` / `0036A100` / `0036C140`. **imp:** `00861EC0` = `jmp [008C2A60]` = `VCRUNTIME140!memset`. The harness hooks the thunk and performs the byte-fill itself. **fix:** the whole pool (the tail, and 160 records with `+0x284 = 1` by default, `default_rec`); PHOOK's planted write to tail `+0x18` (`prom-pinbit1`, `prom-bit0pin`); the planted returns of E56, MIDS, T51 and HID; the slot and handle tables |
| EXP-108 | `003B6020`, `003B62D0`, `0020E600`, `00264670`, `0036F360`, `003A1DB0`, `003B6BF0`, `003E6F70`, `00421FF0`, `0046FAE0` | **app:** `003E56A0`, `002ED570`, `00370F60` (all three are closed by EXP-117/120). **fix:** the planted `0xE0` slot table |
| EXP-112 | `00266530`, `00266AD0`, `00266BD0`, `003DB580`, `003DB280`, `003DB6E0`, `0020E600` | **app:** `00265FF0`, `00265B60`, `00268380`, `002681E0`, `003DBB60`, `00268EA0` (dead), `003DBDC0` (dead) |
| EXP-117 | `003B56D0`, `003E5AD0`, `003AB7F0`, `002ED570`, `003E6DA0`, `0020E600` | **app:** `0036B130` (real in EXP-084), `00370E20` (real in EXP-119). **fix:** the pool at `q[02B40528]` and the codec base |
| EXP-118 | `003E5B30`, `00422D50`, `0041C970`, `003E6DA0`, `002ED570`, `003AB7F0`, `0020E600` | **app:** `0051B9E0`, `0036B130`, `00370E20`. **fix:** the tables and objects |
| EXP-119 | `0051B9E0` → `0051F240`, `00370E20`, `003AB7F0`, `0020E600` | **app:** `0036B130`. **fix:** ctx and tables |
| EXP-120 | `003E56A0`, `00370F60`, `0020E600` | none. **fix:** the record, the table and the codec base |
| EXP-121 | `0036C140`, `0036C1D0`, `0036C1F0`, `0032E400`, `0046DE70`, `002DF960`, `00512EF0`, `0032E520`, `0046DFE0` | **app:** `0032E070`, `0035EA30` |
| EXP-122 | `0036A100`, `0036BFE0`, `0020E620` | **app:** `0036BC60`, `0036AAD0`, `0036ABE0`. **fix:** `q[desc+0xA0] = 0046DFE0`, dispatched through the real `call rax` at `0036C03B` |
| EXP-123 | the allocator core `0036BC60` + 12 real bodies | **app:** `0036A570`. The slot `q[008C2D80]` is planted to the FLAG leaf; the record calls it a "shared twin hook cell". **It is the `exit` IAT slot (imp)**, see below |
| EXP-125 | 25 real, incl. `0036AAD0`, `0036ABE0`, `0036A2A0`, `0036A570` and `00808C40` (`__security_check_cookie`) | **app:** `00369860`, `004746F0`. `q[008C2F70]` (the "output-hook cell") and `q[008C2D80]` are planted to FLAG: **the `strncpy` and `exit` IAT slots (imp)** |
| EXP-126 | 33 real, incl. `00369860`, `004746F0` and the thunk `00861EBA` | **imp:** `VCRUNTIME140!memcpy`. Its IAT cell `008C2A68` is planted to a trampoline at `0x63000000`. `008C2D80` is planted as in 125 (imp) |
| EXP-128 | 15 real, incl. `0032E070`, `0035EA30` | **app:** 12 bodies (`003EADD0`, `0046E030`, `002DF6C0`, `0046DD50`, `003E9780`, `0036FD50`, `003BB790`, `0017D3E0`, `003691B0`, `00369190`, `0035E7A0`, and `00862090`). **`00862090` is `jmp [008C21D0]` = `KERNEL32!GetCurrentThread` (imp)**, which the record names the "tick source". **fix:** the task callbacks at `0x63010000` / `20000` / `30000`; the `memcpy` (`008C2A68`), `vsprintf` (`008C2F08`), `strncpy` and `exit` slots planted |

Two things were read and not otherwise verified:
- **bodies.json:** read for every record.
- **`on_code` hooks:** read in full for EXP-109 only. For the other twelve I read the record tables and grepped each
  `check.py` for IAT-cell plants.

## Per invariant

The static reach method for RP:
- **Pointer references:** an image-wide census of the pool singleton pointer `022C6F28` (`data_xref_scan`, control
  `004279B0` present) found 636 instructions in 372 functions.
- **Closures:** I took each of EXP-109's 17 scripted callees and built its direct-call closure (`edges.tsv`).
- **Result:** 16 closure members reference the pool pointer. **Exactly one of them touches a tail index field
  (`+0x48800..+0x48814`): `00427B00`, in TDOWN's closure, and only as a read** (`00427B14 mov eax,[rbx+0x48800]`).
- **Record link fields:** I checked the scripted callees' **own** bodies for stores at record `+0x00` / `+0x02` /
  `+0x04` / `+0x290` (RINIT, PTD, PHOOK, TDOWN, F4C0, HID) and found none. TDOWN writes the links only through its
  tail jump to CLR (`004201E6 jmp 0041F730` → `0041F771`..`0041F795`), and that runs after RETI's unlink.
- **Not covered:** indirect calls, and stores inside the closures to record links.

Script: `scratchpad/s38_pool_reach.py`.

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| **RP-1** `headActive/headPending == -1` iff the list is empty | EXP-109 (`lkup-empty`, `prom-*`, `reti-*`, `rele-pending-*`, `ctor-fresh`) | **no.** Every head write is in a real body. No stub closure writes a tail index |
| **RP-2** `0 ≤ liveCount ≤ 160`, with the ceiling checked before the increment | EXP-109 `aloc-full`, `aloc-lastfree` (`004279E9` compare, `00427A7F` inc) | **no** |
| **RP-3** `liveCount == 0 → nextFree = 0`, in both release paths and the ctor | EXP-109 `reti-*`, `rele-pending*`, `ctor-fresh` | **no.** All three writes are real (`00427D50` via `ebp`, `00429288`, and CTOR's qword store) |
| **RP-4** promotion does not touch `liveCount` | EXP-109 `prom-*` | **no.** No `+0x4880C` store in the closures of PTD, HID, PHOOK or E56 |
| **RP-5a** the free-cursor scan tests exactly `d[rec+0x284] == 0` (`00427AD2`) | EXP-109 ALOC cases | the compare itself is real, **but where it stops is exposed**. See RP-5b |
| **RP-5b** the initializer sets `+0x284` non-zero (`0042049A or dword [rcx+0x284], 0x2010F9`, with `rcx` = the record, passed at `00427A6E mov rcx,rdi` → `00427A71 call 00420480`) | **not executed.** RINIT is scripted with no effect | **yes: app stub `00420480` reaches it**, through a skipped write, and it changes what the scan returns. See finding 1 |
| **RP-5c** every release clears `+0x284` (the termination argument) | the pending path of RELE → CLR is real. **The zeroing itself is done by the memset import bridge** (`0041F754 call 00861EC0`) | **import-class** on the RELE path. **app stub `004200A0` on the RETI path:** its tail call to `0041F730` is skipped, so the retire-path reset is **not executed** |
| RP termination: the scan is unbounded (`00427AB0`–`00427ADA`) and terminates because a free slot exists | EXP-109 | **exposed.** It terminates in the harness only because of RINIT's skipped write **plus** a fixture that violates the contract's own premise (finding 1) |
| **RO R-1..R-4** (three `0x668` sites; two vtable references; latch width; 17 byte reads) | static census claims by nature | n/a (static) |
| **RO R-5 / R-6 / R-7** (the banks; no loops; a clear latch publishes nothing) | **no record in the cell** | coverage, not exposure. See the last section |
| **TP** post/invariants: exactly one bank is written; it never writes both, never reads the bank it writes, never writes the parity byte | **no record in the cell** | coverage, not exposure |
| **CD** preconditions (sign-extended id, unchecked pointers); the four postconditions; the corrected invariant | **no record in the cell** | coverage, not exposure |

## Finding 1: EXP-109's free-cursor scan stops on a stub artifact in every case where it runs

What the fixture and the stub do:
- **The fixture:** `default_rec` gives **all 160 records `+0x284 = 1`**. No ALOC case plants a zero.
- **ALOC's sequence:** ALOC takes `i = nextFree`, and CLR (real, memset via the import bridge) zeroes record `i`.
  Scripted RINIT does **not** apply `0042049A`, so record `i`'s `+0x284` stays 0.
- **The scan:** it runs from `i+1`, wraps at `0xA0` (`00427AB8`/`00427ABE`), and stops on **record `i` itself**.

I ran the shipped harness read-only, importing `check.py` (`s38-probes/s38_probe109.py`). For all six scanning
cases, `nextFree` after the call equals the index just returned:

| case | allocated | nextFree |
|---|---|---|
| `aloc-first` | 0 | 0 |
| `aloc-second` | 1 | 1 |
| `aloc-mid` | 5 | 5 |
| `aloc-third` | 5 | 5 |
| `aloc-pendempty` | 5 | 5 |
| `aloc-scanwrap` | `0x9E` | `0x9E` |

**Counterfactual** (`s38-probes/s38_probe109b.py`): the scripted RINIT is given only its first store (`or [rcx+0x284],
0x2010F9`). In all six cases the scan then fails to return within the harness's 4,000,000-instruction cap, and
`nextFree` is left mid-scan (`0x80`, `0x7E`, …). *Return status confirmed at review (block 301, `s38-probes/s38_probe109c.py` → `.out.txt`): with the store applied, six cases end at the cap inside the scan loop (`00427AB2`..`00427AC8`) and do not return; `aloc-lastfree` returns. With the stub, all seven return.* This is expected, because the fixture has no free record while
`liveCount < 160`, which breaks RP §4's premise that "invariant 2 guarantees a free slot exists".

**Consequence:**
- EXP-109 establishes the scan's **mechanics**: the wrap, the field, the zero test, and the kills on
  `m-al-scanbound`, `m-al-scanfield`, `m-al-scancc` and `m-al-wrapcc`.
- Its **stopping point** comes from an application stub combined with a fixture outside the contract's reachable
  state.
- RP-5b is unexecuted, and the model mirrors the stub.

## Other contradictions found

1. **The binding gap is stale against the row's own cells.**
   - "types PARTIAL": the types cell reads **MET** (re-scored 2026-09-25).
   - "nothing executed": the runtime cell lists 13 records, and EXP-109 executes RP 1–5's bodies.
2. **The runtime cell's "render family" overstates what executes S-38.**
   - Of the 13, EXP-108 is S-48's contract, EXP-112 is 04-Actor-Entity's, EXP-121 and EXP-128 are the resource
     request queue's, and EXP-122, 123, 125 and 126 declare no contract.
   - EXP-117 to EXP-120 execute callees inside RP's scope but no §4 invariant.
   - **Overlap:** S-48's runtime cell cites EXP-108, 109, 117, 119 and 120 as well.
3. **RP §13a (FABLE 2026-09-22) cites EXP-120 "because it executes `002ED570`". EXP-120 does not execute it.**
   - EXP-120's bodies.json `real` list is `003E56A0` / `00370F60` / `0020E600`.
   - Its own text says "`002ED570` was closed by EXP-117".
   - EXP-120 does execute `003E56A0` (EXP-109's scripted E56), which *is* in RP's scope. So the citation stands and
     its stated reason is wrong.
4. **RP §13a is internally inconsistent in two ways.**
   - **The front-matter table is stale:** it says EXP-121/122/123/125/126/128 carry the RP `contract:` key, but they
     now read resource-request-queue (121, 128) or none (122, 123, 125, 126).
   - **Its two "the five are unexecuted" sentences contradict the same page:**
     - *"the five are unexecuted"* (in the FABLE subsection);
     - *"The five operations are still unexecuted — §13's pilot does not exist"* (in falsification pass 1);
     - but §13 (the differential `diff_render_pool.py`, 2026-09-12) and §20 (EXP-109, 2026-09-19) both execute all
       five.
5. **RO §13 says "No experiment executes these four bodies."** That is true of EXP records. But TP §13 records
   `001FB120`, one of the four, executed as shipped bytes by `diff_character_publish.py` (156 commands, 0
   mismatches). The sibling pages disagree on whether the publish has run.
6. **Import slots are misread as "hook cells" in four of the cell's records.** I resolved these through the PE import
   directory (`iat.py`) and cross-checked each against the hint/name string the on-disk slot points to:

   | slot | import | the records call it | records |
   |---|---|---|---|
   | `008C2D80` | `exit` | "shared twin hook cell" | 123, 125, 126, 128 |
   | `008C2F70` | `strncpy` | "output-hook cell" | 125, 126, 128 |
   | `008C2F08` | `__stdio_common_vsprintf` | "emit cell" | 126, 128 |
   | `008C21D0` | `GetCurrentThread`, behind the thunk `00862090` | "tick source" | 128 |

   - **Why they look like data pointers:** "ships rdata `0x1CCF02C` / `0x1CCEF16` / `0x1CCECB4`" are the unbound
     IAT's hint/name RVAs, not dormant data pointers.
   - **The FLAG plants are therefore import bridges, not fixtures.** None of this touches an S-38 invariant. It is
     recorded because these records sit in S-38's cell.

## Outside the cell (not analysed per invariant, stated for coverage)

- **`diff_character_publish.py`** runs TP's `001FB120` real. It answers one callee: the accessor `00189120` (`mov
  rax,[01F7F598]; ret`, app), whose planted return is the parity object (fix).
  - **What that return decides:** it selects *which* bank is written.
  - **What it does not decide:** TP's one-bank / no-parity-write claims and RO R-5..R-7 are properties of the real
    body.
- **`diff_coast_down.py`** runs CD's `00424080` real. It answers `0020E600` (address arithmetic, no stores) and
  `0051B9E0` → `0051F240`, both app.
  - **What those answers feed:** the §7a tail's selection. The real `0051F240` also makes a lazy write to
    `q[elem+0x18]` (RP §22), which the oracle skips.
  - **What they do not feed:** the latch's own invariants, which concern `*rdx`, `*r8` and the two motion blocks.
- I have not verified these two harnesses beyond their hook code.

## For the scorer

- **Exactly one record in the cell (EXP-109) executes an S-38 §4 invariant set, RP 1–5.** The other twelve are
  other contracts' evidence, or callee-level evidence without a §4 invariant.
- **RP-1..RP-4:** no substitution reaches them. This rests on the static direct-call census above: no scripted
  closure writes a tail index. Indirect calls are not covered.
- **RP-5 is exposed to application stub `00420480` (RINIT).**
  - Its skipped `0042049A` store changes where the unbounded scan stops, measured in all six scanning cases.
  - The fixture (160 × `+0x284 = 1`, with `liveCount < 160`) is outside the contract's reachable state.
  - RP-5's clearing half is import-class (memset) on the RELE path and unexecuted (app stub `004200A0`) on the
    RETI path.
- **Of EXP-109's other scripted callees, some run real elsewhere in the cell and some do not:**
  - **Real elsewhere:** HID and MIDS (117), T51 (119), E56 (120), `0036C1D0` / `0036C140` / `0032E400` /
    `0032E520` / `00512EF0` (121), and `0036A100` (122).
  - **Real nowhere in the cell:** RINIT, PTD, PHOOK, TDOWN, F4C0, `0040DB70`, `0032E620`.
- **Unexecuted by every record in the cell:** TP (`001FB120`), CD (`00424080`), and RO's four bodies. TP and CD have
  differential executions outside the cell. RO R-1..R-4 are static by nature.
- **Stale text:** the binding-gap text (types, "nothing executed"). RP §13a's EXP-120 reason, front-matter table and
  "unexecuted" sentences. RO §13 against TP §13.
- **`live_game`** is false on all 13 records. MEANING NOT CLAIMED for any stubbed callee's semantics.
