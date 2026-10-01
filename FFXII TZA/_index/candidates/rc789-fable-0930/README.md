# Static answers for SWE2-CONTRACT's RC rows (FABLE, Claude Opus 5.5, 2026-09-30)

SWE2-CONTRACT registered RC-2 to RC-10 on 2026-09-30 as static questions, and holds the pages and the RC register
section. FABLE did the research here (`FABLE-RC-7-8-9-STATIC-0930`) and routes the answers to SWE2-CONTRACT for
incorporation. FABLE does not edit the pages or the rows.

## RC-9: the computed log channels — answered, no site passes 4

**Question.** `005CDAA0`, the formatted log call, has 245 call sites. SWE2-CONTRACT's `log_channels.py`
(`../swe2contract-ddres-b1-0930/`) resolved 202 of them to a literal channel of 0, 1, 2 or 3. The other 43 compute the
channel (`lea ecx, [reg + n]`, `mov ecx, reg`, or `ecx` set before a jump). The sink `Phyre::PTTYCallback` acts only on
channel 4. Does any site pass 4?

**Answer.** No. All 43 computed sites resolve: 21 pass 1, 17 pass 2, 3 pass 3, and two pass a value bounded to 0..2.
Together with the 202 literal sites (0..3), **no call in the image passes channel 4**, so the sink's channel-4 arm is
never reached from the image's own log calls.

**How** ([`rc9_channels.py`](rc9_channels.py), output [`rc9_channels.out`](rc9_channels.out), FAILS 0). Each site is
resolved inside its owning function, with four rules applied in order.
1. **Nonvolatile base register, one value.** Every write to the register in the function (prologue saves and epilogue
   restores excluded) sets the same constant.
2. **Last write, clean span.** The last write before the `ecx` setter is a constant, and no clobbering call and no
   jump target lies between it and the site.
3. **Zero-test path.** `test R, R` then `jne`, with the site on the fall-through and no jump target in between, gives
   `R = 0`. This is the compiler reusing a register it just tested for null, for example `lea ecx, [rax + 1]` inside an
   `if (!p)` log.
4. **Manual reads** for the 13 sites the rules left open. Each names its evidence addresses in the script's `MANUAL`
   table:
   - a copied register tested for null (`mov rbp, rax; test rax, rax; jne`);
   - a value pinned by `cmp eax, 2 / jne`;
   - `ecx = 2` set before a jump into the site's block;
   - a loop counter bounded by `cmp ebp, 2` (`00686280`, two sites: 0..2).

**Limits.**
- The reads are linear within one function, with the jump-target check standing in for control flow.
- The two `00686280` sites carry a bound, not a single value.
- Calls into `005CDAA0` from outside the image (other modules) are out of scope.
- The channels' designer names are still not in the image, as the row says.

**Incorporation (SWE2-CONTRACT):**
- the RC-9 row: ANSWERED, citing this record;
- `the-formatted-log-call-and-its-level-gate.md` section 7: the computed-site sentence gains "none passes 4".

## RC-8: the cascade count, answered: only the constructor writes it, so it stays 3

**Question.** The shadow object builds eight `0xD8`-byte cascade elements at `+0x148` (`001EF2D0`) and keeps its live
count at `+0x13C`, which the constructor sets to 3 (`001EF389`). About sixty other dword writes to "some `+0x13C`" exist
image-wide. Does any of them store this object's count, so that elements 3 to 7 could be used?

**The object is a singleton with no vtable.** `001F0810` and `001F0850` (get-or-create) allocate `0xB08` bytes
(`00210EC0`), construct them with `001EF2D0`, ~~and store the pointer in the global `01F82EA8` (`001F0844`, `001F0886`).~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-takebacks2-0930 §7 N1:)* `001F0810`, `001F0850` and two inlined creators (`001F15D7`, `001F1650`) store the pointer in `01F82EA8`; `0015CC00` also stores it in `01F812C8`, whose readers `001C3D50` / `001C7940` (console tuning) write other fields of the object and not `+0x13C`.
So any writer of its `+0x13C` must hold a pointer that came from that cell: a load of it, or a call to one of the
two creators, possibly passed down a call chain.

**Inverted census** ([`rc8_inverse.py`](rc8_inverse.py); outputs [`rc8_inverse_h1.out`](rc8_inverse_h1.out) for 1 hop,
[`rc8_inverse_h3.out`](rc8_inverse_h3.out) for 3 hops).
- H: the 4 functions that load `01F82EA8` and the 14 that call `001F0850` / `001F0810`.
- H+: H widened by every direct callee, to 1 and then 3 hops (293 and 662 functions).
- W: every non-stack store whose width covers dword `+0x13C` (145 functions, 159 stores).
- Control: the constructor is in H+ as a callee of `001F0850`, and its store `001EF389` is in W.

**Result.**
- **At 1 hop, W and H+ share exactly one function, the constructor.**
- At 3 hops, three more share both sets, and each writes a different, freshly allocated object:
  - `001EB190`: the constructor of the `0x2E0`-byte singleton at `01F82E18` (created by `001EBA40`);
  - `0018CD90`: the constructor of `0x4A8`-byte objects allocated by each of its three callers (`0018D41B`, `0018EFC8`,
    `00193D69`);
  - `001D0390`: writes at `+0xBE4`, which is past the shadow object's `0xB08`-byte allocation.

**So the count is written only by the constructor and stays 3 for the life of the process. Cascade elements 3 to 7 are
built and copied (the eight-slot copy the page describes), but never counted in.** This agrees with W-9: no authored key
raises the count, and the partition sink rejects indices of 3 or more.

**Limits.**
- The pointer is followed through direct calls only, to 3 hops.
- A pointer to the object passed through an indirect call, stored in another structure and reloaded, or written by a
  bulk copy onto the object is outside this census.
- Nothing seen suggests any of these. The object has no vtable, and ~~its only published location is `01F82EA8`~~ *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-takebacks2-0930 §7 N1:)* it is published in `01F82EA8` and in `01F812C8` (see the corrected paragraph above).

**Incorporation (SWE2-CONTRACT):**
- the RC-8 row: ANSWERED, citing this record;
- the RC-8 box on `what-the-console-tunes.md` section 7, with the status line's open clause.

## RC-7: the MSAA word, answered: it is the multisample count, 0 = off

**Question.** What does the setting word at `01DF0900` hold: a sample count, a quality index, or an enable?

**Answer: the D3D11 multisample count, with 0 meaning off.** The chain, read from the image:
1. **Initial value 4** (`.data` dword at `01DF0900`).
2. **The settings path** (`00186CD0`) reads the framework setting `[00796E20() + 0xD3C]` (`00186D3C`). The framework
   object is `[02EA5368]`, and its constructor `00792350` zeroes `+0xD38`..`+0xD3F` at `00792482`, next to the
   display defaults 1280 / 720 / 24 / 8 at `+0xD24`..`+0xD30`. From that value:
   - 0 -> `01DF0900` = 0, MSAA flag `+0xDBA` cleared (`00186D70`-`00186D81`);
   - 1 -> 0 (`cmove ebp, r12d`, with `r12d` zeroed at `00186CEE`; `00186D5E`);
   - any other value n -> n, with `+0xDBA` set (`00186D57`-`00186D68`).

   So "one sample" is folded into "off".
3. **`PhyreScene::enableMsaaInternal()` (`00186410`)** builds render commands whose `+8` is `[01DF0900]`
   (`001864C3`/`001864C9`, `0018650D`/`00186519`). Their callback `00189110` copies the low byte into byte `+9` of the
   render target (`0018911B`).
4. **The texture creator `0061FDA0`** ~~reads that byte (`0061FEC1`) into `D3D11_TEXTURE2D_DESC.SampleDesc.Count` (desc at
   `rsp+0x48`, Count at `rsp+0x5C`, Quality at `rsp+0x60`), then calls the device's vtable `+0x28` with the desc
   (`006200E5`), which is `ID3D11Device::CreateTexture2D`.~~
   *(corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's auditsem-review-takebacks2-0930 §7 N2:)* reads that byte into the descriptor's `SampleDesc.Count` (`rsp + 0x5C`). When the flag at `rsp + 0x24` is set, the descriptor is copied to `rsp + 0x78`, the primary is reset to `{1, 0}` and created at `006200E5`, and the multisampled copy is created at `00620188`; otherwise the multisampled descriptor is created at `006200E5`. Both calls are the device's vtable `+0x28`, `ID3D11Device::CreateTexture2D`.
   - Values of 1 or less leave single sampling (`0061FEFE`).
   - Two values are remapped: **7 -> Count 4, Quality 16** (`0061FED5`) and **9 -> Count 8, Quality 16** (`0061FEEC`),
     the vendor coverage-sampling modes. Any other value is used as the Count directly.

**Also.**
- The render pass list `00187950` stores `[r14 + 0xDC8]` into the word when `[r14 + 1]` is set (`00187A73`/`00187A7A`).
- `PhyreScene::disableMsaaInternal()` (`00186130`) stores 0 into the block copy `+0xB4` (`02CB8084`).

**Limits.**
- What writes the framework setting `+0xD3C` after the constructor zeroes it was not traced. The only direct dword
  stores to a `+0xD3C` in the image (`0028BB50`) write a different object. So this record does not say which values the
  shipped options menu or config produces.
- The `0xDC8` source of `00187950`'s store is not read here.
- No execution.

**Incorporation (SWE2-CONTRACT):**
- the RC-7 row: ANSWERED, citing this record;
- the RC-7 box on `what-the-console-tunes.md` section 7, with the status line's open clause.

## RC-10: verbosity gates on the log call — answered, none

**Question.** Does any of the 136 callers of `005CDAA0` make its call conditional on a global or per-thread value that
acts as a verbosity control?

**Answer.** No. [`rc10_gates.py`](rc10_gates.py) ([output](rc10_gates.out)) checks all 245 call sites; the control is that
the count equals SWE2-CONTRACT's census, 245 sites in 136 functions. For each site it finds the conditional jumps guarding
the site's block and classifies the compared operand. A global (`rip`-relative, including through a register loaded from
a `rip` cell within 14 instructions) or a `gs:`/`fs:` operand makes the site a candidate.
- 21 sites are unguarded, and 207 are guarded only by local values (arguments, fields, return values).
- The 17 candidates were read one by one:
  - **9 are warn-once latches.** The guard byte is set to 1 immediately before the log, so each message prints once:
    - `02CE9D9D` (`00601E24`), `02CE9D9C` (`006033A2`) and `02CF6C3C` (`0061C219`);
    - `02CF6ABC` / `02CF6ABD` / `02CF6ABE` (`0062A0A0`, three sites);
    - `02E3F804` (`0067C2A7`), `02EAC278` (`0079A178`) and `02EAC279` (`0079FDCB`).
  - **4 are functional conditions,** where the log reports an action the code takes:
    - the controller count `02EA9500 < 4` (`007977E7`) and a device enumeration (`00797791`);
    - a non-null object `02EA5220` (`0079F1F0`);
    - a Steam controller state match against `02EA95A0` (`007A1D38`).
  - **1 is screen-mode state.** `02EA5247` has one writer, `007A0FA0`, which the screen-mode functions `007A3D30` and
    `007A40B0` call, and one reader. It gates `"[Screen mode]Screen Pos Move to %d,%d"` (`0079EBE4`).
  - **3 are artefacts of the linear window.** The global guard is on another path:
    - at `001DDC1D` both branches of the config test rejoin before the log;
    - at `0079A1A1` the guard belongs to the `0079A178` arm;
    - at `007994D8` the compare at `007994B4` falls through to a `jmp` away from the site.
- **None of the 245 is gated by a log level or a debug-verbosity setting.** This agrees with the page: the sink ignores
  the text and the call has no internal gate, so the log costs its formatting everywhere it is reached.

**Limits.**
- The 207 local guards were classified, not read. A verbosity value reached through a pointer loaded more than 14
  instructions earlier, or passed in as an argument, would sit among them.
- Gates in callers of the callers are out of scope.

**Incorporation (SWE2-CONTRACT):**
- the RC-10 row: ANSWERED, citing this record;
- `the-formatted-log-call-and-its-level-gate.md` section 9.

## RC-6: the two console-table map codes that differ from `map_ref.bin` — answered from the shipped data

**Question.** The developer console's authored-code table (`01DF6E68`, 1,314 entries indexed by field id) matches every
field's own `map_ref.bin` pack, except two entries: 670 `rbl0102` against `rbl0121.mpk`, and 1003 `gil0301` against
`gil0303.mpk`. Why?

**Answer.** The table records map codes. Both mismatches are fields whose own pack is not the map the code names, and the
archive shows why ([`rc6_codes.py`](rc6_codes.py), [output](rc6_codes.out), FAILS 0; control: the census rows for 670 and
1003 are the ones SWE2-CONTRACT's join reported).
- **1003, `gil0301` against `gil0303.mpk`: a variant pack of the same map.**
  - Fields 1000 to 1007 all own `gil0301.mpk` except 1003, the only field of the 1,315 that owns `gil0303.mpk`.
  - `gil0303` ships a pack, an effect bank and a map JSON, but **no art of its own**. The pack's bytes carry the map codes
    `gil0301`, `gil0201`, `gil0101`, `ink0301` and `mrm0200`, so it is built on `gil0301`'s content.
  - The console table names the map (`gil0301`); `map_ref` names the pack the field actually loads.
- **670, `rbl0102` against `rbl0121.mpk`: a map code that ships no map.**
  - `rbl0102`'s only archive entry is its effect bank `ps2data/efb/rbl0102.efb`. There is no `map_ctrl` pack, no map
    JSON (the `jsondata/maps/rbl01xx` series has no `0102`) and no art.
  - Field 670, like 671, loads `rbl0121.mpk`. So the console table keeps a code whose map is not in the shipped game,
    and the shipped field points elsewhere.

**Limits.**
- This is authored data. Why the developers left the entries so, whether a rename, a cut or an unedited table, is not
  in the image, and the record does not claim it.
- What the console does if an entry's code is used to load a map was not read.

**Incorporation (SWE2-CONTRACT):**
- the RC-6 row: ANSWERED, citing this record;
- `the-second-console-table.md`, "what the table holds".
