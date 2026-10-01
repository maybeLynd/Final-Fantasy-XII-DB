# S-50 runtime: per-invariant stub exposure for EXP-110 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-50, Lua core loader.
- **Runtime verdict:** MIXED. The cell reads *"EXP-110 executes the three loader callers
  (`00684D10`/`00684F60`/`00686280`) under isolated original-code replay … isolated original-code execution under
  disclosed stubs — no per-invariant stub-exposure analysis yet"*.
- **Binding gap:** it opens *"types NOT MET -> PARTIAL 2026-09-21 (OPUS) …"* and says *"Runtime stays NOT MET -
  nothing here executed"*.
- **Contract:** one, `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md`. Its §4 has three stated
  invariants, labelled I1–I3 here, plus a precondition and a postcondition, labelled PRE and POST.

This note scores nothing.

**The headline: EXP-110 scripts the contract's subject.** The chunk loader `00683C30` is an entry-intercepted
application stub with a planted `al` return:
- `bodies.json` `scripted[0]` = `load` `0x683c30`;
- `check.py` line 109 is `LOAD = 0x00683C30`;
- the hook at lines 382–388 records `(rcx,rdx)` and writes `rax = load_ret` (default 1).

Nothing downstream of `00683C30` runs: `00812F70`, `00810180`, `0081DF50`, the fork `0081D790`, `0082BE30`,
`0082E910`, the header check `0082E490`. The contract's own §13 addendum (2026-09-25, OPUS) already says *"the
callers have since run, the loader has not"*.

## Substitutions per record

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-110** `phyre-script-callers-exec` (frontmatter: this contract) | the three callers D10 `00684D10`, F60 `00684F60`, C280 `00686280`; the leaves GETTOP `0080FD00`, SETTOP `00811130`, PUSHB `00810450`, PUSHI `00810580`, PUSHN `00810640`, PUSHP `008105A0`, TOBOOL `008113D0`, TYPE `008119F0`, SING `006372A0` | **application stubs:** **LOAD `00683C30`** (the contract's entry), PCALL `00810340`, ERRSTR `00811530`, LOG `005CDAA0`, PUSHLS `0080FB20`, IDXOP `00810730`, SETFLD `00810ED0`, COPY `00682AA0`, MARSH `00682D20`, ITER `006811B0`, DISP `00681010`, GROW `0080F420`, GETA `006810B0`, GETB `00681130`, TONUM `00811470`, MSHL `00636920`. **TLS stubs:** twelve singleton getters `SENTS[0..11]` (`00630490`, `0062FF50`, `0062FFC0`, `00630030`, `006300A0`, `00630110`, `00630180`, `00630420`, `006303B0`, `006301F0`, `00630260`, `006302D0`), which read `gs:[0x58]` and cannot run under Unicorn. **Import bridge:** CPY86 `00861EBA` → IAT `008C2A68` = `VCRUNTIME140!memcpy`, implemented as a real copy (hook at `check.py` lines 389–393). **Fixtures:** pool headers `02E41020`/`02E41050`, Lua state/stack images, and buffers |

## Per invariant

| invariant | where it lives | executed by EXP-110? | can a substitution reach it? |
|---|---|---|---|
| **PRE** `00683C30` dereferences `rdx` before any buffer null check; only `data` is checked | `00683C30` body | **no**: LOAD is scripted at entry | **not executed: coverage, not exposure** |
| **POST** `true` only when `luaL_loadbufferx` returned 0; stack restored on failure | `00683C30` body with `00812F70`, `00811530`, `00811130` | **no**. LOAD's `al` is planted. The callers' reaction to it is executed, but that is not this claim | **not executed**. The planted `al` stands in for the claim's output; it does not test it |
| **I1** the fork is on the first byte only (`cmp esi, 0x1B` at `0081D7DD`, confirmed by disassembly) | `0081D790` | **no** | **not executed** |
| **I2** both mode guards are `if (mode && …)`; Phyre passes `mode = NULL` (`00683C5A`) | `0081D790`; the `strchr` calls go through IAT `008C2A10` (`0081D7ED`) | **no** | **not executed**. If run, `strchr` would be an import bridge |
| **I3** the header compare, with its read of `0x11` = 17 bytes (`mov r8d, 0x11` at `0082E4CC`) | `0082E490` | **no** | **not executed by EXP-110**. See finding 1 |

**Exposure: empty, for coverage reasons.** No substitution in EXP-110 can reach a loader invariant because no
loader body runs. **EXP-110 belongs to this contract only by adjacency:** it is this contract's callers' record.
Its measured claims are about the callers:
- the result-store widths 1/2/4/8;
- the 9-sentinel result dispatch;
- the marshal pushes;
- the pool checkout;
- TValue pop byte-preservation.

None of those appears in this contract's §4.

## Findings

1. **One execution of an I3 body exists outside the cell.** Contract §13 cites `diff_lua_header.py`
   (`Reconstruction/Tests/Differential/`, 2026-09-12). It is not an EXP record and not named in the cell. It runs
   `0082E490` at its real VA. Its hooks (source lines 103–106 and 187–207):
   - `0081C6A0`, the ZIO read. **Application stub:** it copies `n = r8` bytes from a planted stream and returns 0.
   - `0081BFF0`, the message formatter. **Application stub:** its `r9` is read as the verdict and the frame is
     abandoned.
   - `00808C40`, `__security_check_cookie`. A statically linked CRT helper, **not an IAT import**.

   **Reach on I3:**
   - The 17 is an immediate loaded before the call (`0082E4CC`). The read stub only **observes** it (`lastlen`).
   - The comparisons are inline and real:
     - `cmp rcx,rdx` at `0082E503`, qword `[rsp+0x20]` vs `[rsp+0x38]`;
     - `0082E50D`, qword `+0x28` vs `+0x40`;
     - `cmp di,[rsp+0x48]` at `0082E514`.
   - The stub supplies the bytes compared, which is the intended input. It cannot change the length or the compare
     extent.
   - The formatter stub sits after the verdict is chosen.

   So no substitution in that harness reaches I3. Read from source only; **not re-run here**.
2. **I3's §4 wording conflates two lengths.** §4 says *"the header comparison is over `0x11` = 17 bytes"*. The
   shipped body **reads** 17 (`r8d = 0x11`) and **compares 18**:
   - The three compares above cover 8 + 8 + 2 bytes from `[rsp+0x38]`.
   - Byte 0 is planted `0x1B` by the check itself (`mov byte [rsp+0x38],0x1b` at `0082E4EA`).

   The contract's §2 row ("builds 18 bytes, **reads 17**, compares **18**") matches the bytes; §4's sentence does
   not. This is intra-contract, noted for the scorer, not for this exposure question.
3. **EB-4 is executed by the callers, under a planted loader return.** In `d10-loadfail`, `f60-loadfail` and
   `c280-loadfail` (`check.py` lines 1039, 1069, 1098), LOAD returns 0. None of the three callers then reaches
   ERRSTR or LOG: the model returns right after the `L…` trace token (`check.py` lines 660–663, 732–733, 820–823).
   The native trace matched in all 48 cases.
   - Contract §10 and §14 still list `EB-4` ("whether any caller reports a compile failure") as unread.
   - The source page `the-lua-loader-and-what-it-accepts.md` line 437 marks it ANSWERED "no" statically
     (FABLE, 2026-09-12).
   - The execution supports the source page. Its input (`al = 0`) is the stub's planted value, so it shows the
     callers' reaction to a false return, not that a compile error yields one.
4. **The binding gap is stale against the row's own cells.**
   - It says *"types NOT MET -> PARTIAL"*; the types cell reads **MET** (re-scored 2026-09-25).
   - It says *"Runtime stays NOT MET - nothing here executed"*; the runtime cell reads **MIXED** (EXP-110).

   Its substance, that the loader body is unexecuted by any EXP record, still holds. `0082E490` runs only in the
   non-EXP differential harness.

## For the scorer

- **Stub exposure on PRE, POST and I1–I3: empty. Every claim is unexecuted by EXP-110.** The contract's entry
  `00683C30` is an application stub there, with planted `al`. No body downstream of it runs:
  `00812F70`/`00810180`/`0081DF50`/`0081D790`/`0082BE30`/`0082E910`/`0082E490`.
- **The cell's only record is a caller-side record.** Its frontmatter names this contract. Its measured claims are
  about `00684D10`/`00684F60`/`00686280` and are not §4 invariants.
- **Substitution classes in EXP-110:**
  - 17 application stubs, including LOAD;
  - 12 TLS getter stubs, which cannot be emulated;
  - 1 import bridge (`memcpy`, IAT `008C2A68`);
  - fixture pools and state.
- **The only execution of an invariant body found is `diff_lua_header.py`** (`0082E490`, I3). It is not an EXP
  record and not in the cell. Its stubs (`0081C6A0` read, `0081BFF0` formatter, `00808C40` cookie) cannot reach
  I3's read length or compare extent. Not re-run here.
- **Intra-contract:** §4's "comparison over 17 bytes" disagrees with §2 and the bytes (read 17, compare 18).
  `EB-4` is still listed as unread in the contract but is answered on the source page. EXP-110's load-fail cases
  agree with that answer, under a planted return.
- **The binding-gap text is stale** against the types cell (MET) and the runtime cell (MIXED).
- **Evidence class:** original-code replay (NATIVE-REPLAY) and static. `live_game: false`. `DA-1` (whether
  `00683C30` is ever entered in a running game) is untouched. Nothing live.
