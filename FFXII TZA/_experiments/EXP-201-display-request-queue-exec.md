# EXP-201 — display-request queue `003BBD00` / `003284D0` / `003EFD00` execution

**Status:** complete — **394/394 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`be5088bdbeac09d363985991df0f0f0c97ba55022f664eea40f939c18ebfc965`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..200; 360 inherited + 34 new `fa3b0-*`/`fmt-*`/`bd00-*`/`d4d0-*`
direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json` *[shared, mutable path: later EXPs of this harness rewrote it (407 cases at EXP-202, 556 at EXP-256). This record's result is sealed receipt `r-95260e713b7dba43`; see Receipts.]*
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-200's resume note pointed at `003BBD00`/`003284D0` as a suspected
"formatter family (CRT closure)". Disassembly reclassifies it: this is the
**battle display-request queue** — the ring of 64 0x50-byte slots that carries
damage numbers, reward text and gauge icons to the UI. Promoted from scripted
boundaries to shipped-byte execution:

- `003284D0` — type-2 wrapper (0x52 bytes): distance-gates `q[obj+0x10]`,
  builds `{q[+0]=subobj, d[+8]=movzx(dl), b[+0xC]=2}` on the stack, calls
  `003BBD00`.
- `002FA3B0` — distance gate (0xB8 bytes): `rcx==0` → 0; `003272A0()` gate
  refreshes the camera vec3 at `01EBBB00`/`+4`/`+8` from
  `q[gate+0x10]`'s position when `b[02089340]&0x10`; then `00265020` reads the
  arg object's vec3 (`q[obj+0xB8]`, only when `(b[obj+3]>>5)-1 ∈ {0,2}` —
  rejected classes leave the dst **zeroed**, dist 0 → in-range), forces
  component+4 to 0, `003A1920` computes squared distance tail-jumping to the
  `sqrtf` IAT thunk; returns `comiss 24.0f, dist` (`seta`) — **strictly less
  than 24.0** (`fa3b0-edge`: 24.0 exactly is out).
- `003BBD00` — queue slot allocator/registrar (0x288 bytes), below.
- `00506700` — slot initializer (0x1B0 bytes), below.
- `003EFD00` — decimal digit-writer (0xEC bytes), below.
- `0028FBE0` — type-0-only dispatcher (0xA9 bytes), below.
- `0035D330` — resource-block wrapper (real): writes `d[022CA520]=kind`,
  `d[022CA524]=id`, calls `0031C5D0(blk)`; `eax<0` → `0016D6A0(0x800)` stub,
  memset 0x98 of the block, returns `&blk`.

Already-real callees reused: `003272A0`, `00265020`, `003A1920`, `003589B0`,
`003590D0`, `003588B0`, `00263E30`, `0024A5A0`, `002DD7E0`, `002DD7B0`,
`002B58B0`.

New scripted boundaries (deliberate): `0031C5D0` (deep resource-table
resolver, jump-table switch into `0020E600` machinery — retkey
`s31c5d0_ret`), `002B3050` (string machinery), `00296280`→`296280` table scan
stays whatever it was; CRT `rand()` (IAT `0x1CCEF20` via cell `0x8C3098`) and
CRT `sqrtf()` (IAT `0x1CCED52` via `0x861F14`) get real-semantics stubs
(`randv` sequence-able, `randn` count; `sqrtf` computes `math.sqrt` on the
low f32 of XMM0).

## `003BBD00(req)` — the allocator

`req` layout: `q[+0]` object, `d[+8]` value/resource-id, `b[+0xC]` type,
`b[+0xD]` subtype.

- `qtab = q[02B457D0]`, `qidx = movsx b[02B443C0]` (signed byte). Null table
  or negative-index lookup miss → `al=0xFF` (`bd00-notab`, `bd00-neg`).
- Slot probe: `qtab[qidx*0x50]` occupied → `0xFF` (`bd00-occ`).
- **Type-2 pre-gate:** `b[req+0xC]==2` → `0035D330(0x1A, d[req+8])` →
  `b[blk+0x24]==0xFF` → `0xFF` (`bd00-t2ff`, `bd00-t2neg` — a `31C5D0`
  negative return memsets the block to zeros, `b24` becomes 0, gate passes).
- **Candidate scan** over all 64 entries: same-object live entries mark
  `d[rsp+0x20+cat*4]` by their `b[entry+0x3E]` (only when
  `w[entry+0x38]` under the type-2-or-`0x1E` threshold).
- **Category derive:** if `rsp+0x20` set → cat `r14` comes from which stack
  cells got marked (cat 2..4 chains: `cat2+no3→4`? — precise: `c0&&c1&&!c2→4`,
  `c0&&!c1&&c2→3`? implemented per the live chain — the derive prefers
  existing siblings' classes); when nothing derives → `rand()&1` →
  **cat = 2*(rand&1)+1** — only 1 or 3 are reachable that way
  (`bd00-rand1`/`bd00-rand3`, `randn==2` vs derive-path `randn==1` for
  `bd00-cat*`).
- `0028FBE0(req)` runs BEFORE the slot init.
- **Type-2 second scan:** every live type-2 entry gets `w[+0x3A] += 3`
  (`bd00-t2pri` proves both same-obj and other-obj bump); same-obj entries
  with `w[+0x38]<=0` feed `edi = max(d[entry+0x44]) + 3` → written to
  `d[newslot+0x44]`.
- `00506700(slot, req)` initializes; then `rand()&0x1F` →
  `S = (rand&0x1F)*K1*K2 + K3` (verified live: rand 0 → S=1.0, rand 1 →
  S=1.03125 — the scale `S` jitters the per-category corner pair
  `T[cat] = {(0,0),(-16,-16),(16,16),(16,-16),(-16,16)}` at `0xD11600`);
  `d[slot+0x14] = S*Tx`, `d[slot+0x18] = S*Ty`; `b[slot+0x3E] = cat`;
  `b[02B443C0]` advances mod 64 (`cmovge` — `bd00-wrap`: 0x3F→0); return
  `movzx(bl|0x20)` — **byte-width result; high rax bits are cookie garbage
  (`bd00-notab` showed `0x2b994cd85dff` for 0xFF — assert `al` only).**

## `00506700(slot, req)` — the initializer

`memset(slot,0,0x50)`; `w[+0x3A]=1`; `q[+0]=q[req]`; `d[+8]=003589B0(obj)`
packed id; `b[+0x3C]=b[req+0xC]`; then by type:

- **type 0** — `003EFD00(&slot+0x40, d[req+8], 0, 0)`; strlen scan →
  `b[+0x3F]`; `0024A5A0("battle_4_c")` → `q[+0x30]` name; subtype
  `b[req+0xD]` indexes `d[0xD227A8+i*4]` style ids → `002DD7E0` → `d[+0xC]`
  colour, `002DD7B0` → `b[+0x3D]` (`bd00-t0`: `"12345"` text, len 5,
  `0x80808080` default colour, `b3D=0`).
- **type 1** — `b[+0x3F]=b[req+8]`; `0024A5A0("battle_4_p")` → `q[+0x30]`;
  subtype indexes a **byte pair** at `0x120000+0xC02780+i*2`/`+1` → two
  `002DD7E0` → `d[+0xC]`,`d[+0x10]` (`bd00-t1`).
- **type 2** — `0035D330(0x1A, d[req+8])` (second `31C5D0` call);
  `w[+0x3A]=3`; `b[+0x3F]=b[req+8]`; `d[+0x44]=0`; `q[+0x30]=
  002B58B0(q[blk+0x18])` prefix-skip name; `b[+0x3D]=4`;
  `d[+0xC]=0x80808080`; `b[blk+0x25]` flags pick the `002DD7E0` index
  (`&2→1`, `&4→0x12`, `&8→0xB6`, `&0x10→0xF3` — `bd00-t2b25` with
  `b25=0x12` → `&2&&&0x10`: first match `&2` → index 1 … live result
  `d0C=0x1234` via `dd7` table) → `d[+0xC]`; `002B3050(0, name, &+0x40,
  &+0x42)` string copy (scripted).
- **other types** (`bd00-t3` with `rqt=3`): none of the arms — slot keeps
  `w3A=1`, `b3C=3`, rest zeroed.

## `003EFD00(dst, value, width, zpad)` — the decimal writer

Digit count via the `x*0x66666667>>34` signed `/5` loop over **signed**
edx — `edx<=0` skips it entirely, so **negative values format as an empty
string** (`fmt-neg`: edx=`0xFFFFFFD6` → `buf[0]=NUL`, len 0 — not `-42`,
not `4294967254`). `edx==0` → count forced 1 → `"0"`. `width` (r8d): pad
count = `width-count`, memset fill `' '` unless r9d≠0 → `'0'`; digits
written left→right through the divisor table `d[0xD11CE0+i*4]`
(1,10,…,10⁹), `idiv` per digit, NUL at `buf+pad+count`. **Returns the
total written width** (`fmt-pos` → 5, `fmt-pad` width 4 → 4).

## `0028FBE0(req)` — type-0 dispatch

Only when `b[req+0xC]==0 && d[req+8]!=0` (`bd00-t0v0`: value 0 → scan
skipped): `003589B0(q[req])` packed id → `00296280` table scan must resolve
→ `q[q[0209BE80]+0x10F78]` controller must exist → jump table on
`b[req+0xD]-1` (`0x28FC8C+idx*4`, 7 entries → `[0,4]`→`297040(id,0)`,
`[1,5]`→`296E90(id)`, `[2,6]`→`297040(id,1)`, `[3]`→no-op). `bd00-t0`
exercises scan+controller only (subtype 0 → `edx=-1` → `ja` → return).

## Corrections of record

- The family is **not** a CRT closure — `003BBD00` is the queue registrar;
  `003EFD00` is the actual formatter.
- `003BBD00`'s return is a **byte** (`al`); failure paths leave stale
  cookie bits in upper rax (`0x…ff`) — consumers test `al`.
- Category derive only runs when same-object siblings exist; otherwise
  `rand()&1` yields cat 1 or 3 — **cats 0/2/4 are derive-only**.
- `randn` counts proved: `bd00-cat*` = 1 rand (scale only), `bd00-rand*` =
  2 (cat + scale).
- `002FA3B0`'s `3272A0` gate controls only the **camera-cell refresh** —
  the distance check always runs; rejected object classes produce a zero
  vec → always "in range" (`fa3b0-b3` = 1 at pos 100).
- `0x2089340` is a shared dword: `0030B770` reads `d&0x3080` bits while
  `003272F0`/`003272A0` test `b&0x10` — fixture writes must preserve the
  dword (`b770-b7`/`n6500-ctxblk` regression).
- Harness memset hook now honours the `dl` fill byte (formatter padding);
  IAT stubs cover `rand`/`sqrtf` (Unicorn XMM regs are ints — low 32 bits).

## Validation

`python check.py` — 394/394, three independent runs, `result.json` SHA256
`be5088bdbeac09d363985991df0f0f0c97ba55022f664eea40f939c18ebfc965`
identical each time. New fixtures: `qt`/`qtptr`/`qidx` (queue ring +
index), `rblk` (022CA520 block bytes), `pos`/`cam`/`so3` (distance-gate
vec3s + class byte), `obj10`/`rqo`/`rqv`/`rqt`/`rqs` (request fields),
`dd7` (index table `0215E6B8`/`0215E6C8`), `randv`, `s31c5d0_ret`, string
`rcx`/`edx`/`r8`/`r9` attr resolution.

**Not claimed:** live-game reachability, initialized-state identity of
fixture rows, `00296280`-table population semantics under real gameplay,
or `0031C5D0`/`002B3050` internals (deliberately scripted — the resource
resolver's `0020E600` subtree and the string engine are their own
packages). The two wrappers' callers (`003283D0` type-0 posting with
`abs(edx)` + subtype style-table `0x1EED300`, `00328480` type-1) were
disassembled but are not yet executed entries — queued for the next
package.

## Receipts (SWE2-ORACLE, 2026-09-29)

**Bound 2026-09-29 by SWE2-ORACLE** (run by OPUS's Claude subagent under that identity), for
`FRONTIER-REQ-ORACLE-EXP201-RECEIPT-SEALING`. The text above is unchanged except for the marker on the Result line.

- **This record's run is receipt `r-95260e713b7dba43`** in `_experiments/evidence/receipts/store/`, sealed with
  `gfz-scripts/seal.py` (OPUS, `475456436`). It holds the exact committed `check.py` of `aa29615b7`, the 394-case
  `result` (SHA256 `be5088bdbeac09d363985991df0f0f0c97ba55022f664eea40f939c18ebfc965`, the hash cited above) and
  `inputs/image-identity.json` (the authority image by hash; the image itself is not stored).
- **The bytes are genuine, not rebuilt.** They are the commit's own: `git cat-file --filters aa29615b7:<path>` gives
  the working copy the run wrote, and it hashes to the cited value. Re-executed 2026-09-29 from the sealed driver
  against the authority image: 394/394, byte-identical. The original run's environment was not recorded.
- **The live path moved.** `member-block-chain-exec/result.json` is shared with the later EXPs of this harness. It held
  407 cases at EXP-202 (receipt `r-edb8403635767456`) and holds 556 at EXP-256 (receipt `r-5be60dc8ce879ae1`, the
  current run). Cite the receipt, not the path.
- **Regression:** `_experiments/evidence/receipts/exp201_receipts.py check`. It verifies the three receipts, their
  hashes and case maps, and that this record and contract section 13j cite `r-95260e713b7dba43`. It rejects this
  record as committed at `aa29615b7` (a path citation with no receipt, the original error). `rerun` re-executes the
  sealed drivers.
- ~~**Open:** `seal.py publishable` refuses all three receipts on the result's shape alone (a flat `{case_id: {...}}`
  object, which its case parser does not read). The shape is requested of seal.py's owner
  (`SWE2-ORACLE-REQ-OPUS-SEAL-FLATMAP-0929`); until then the check prints those rows as PEND, never PASS.~~
  *(Closed 2026-09-30, SWE2-ORACLE: OPUS `eae0ed3c7` reads flat case maps. All three `R-*-gate` rows print PASS at HEAD,
  `GATE-PENDING none`. A non-JSON stored result is now a FAIL row with a negative control, `N-non-json-result`.
  EXP-202 and EXP-256 now cite their own receipts. Answers `AUDITSPEC-REQ-ORACLE-EXP201-PRECISIONS-0929`.)*
