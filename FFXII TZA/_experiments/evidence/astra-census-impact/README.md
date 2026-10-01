# ASTRA — census instrument impact, 2026-09-21

**Result: a retained scanner fails five of ten discriminating instrument controls.**
This is a tool falsification package, not a new FF12 experiment. The original
scanner remains unchanged for reproducibility and its owner receives the defect.

## Question and method

OPUS asked whether ASTRA's evidence tools mishandle volatile registers at calls,
partial-register writes, or `add index, base`. Competing explanations: the notices
do not affect a given instrument; the instrument safely loses information; or it
invents an exact target by retaining stale register state.

Method A source review plus synthetic instrument controls is sufficient. Live
FF12 and isolated shipping-code execution cannot improve this tool-level test.
`check.py` runs the **unchanged retained scanner**, replacing only its executable
and function catalog with ten disposable byte sequences. It independently executes
those same synthetic bytes in Unicorn to observe their write addresses. Synthetic
calls use a stated test callee that clears RAX and returns. No FF12 instructions,
initialization, state, scheduling or reachability are being executed or inferred.

## Identity and raw evidence

The tested source is `sources/aq18_span_write_census.py`, copied byte-for-byte from
`../katano-savedata/aq18_span_write_census.py`. SHA-256:
`0a1e25dcd6326e39b01e419a38854bf40a8eab1f2e710c87949619d4510e02d6`.
OPUS introduced it in `56e1d3ba469000106276e79709d869480e5d92f8`.
`observation.json` retains every fixture's bytes/disassembly, actual write,
reported addresses, source stdout, checker/source hashes and tool versions.
`reviewed-sources.json` identifies the bounded source review. `manifest.json`
and `validation.txt` seal the package and its reproduction receipt.

This scanner's game target is the reference executable SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, but **no new
whole-image run occurred**. Synthetic writes were confined to emulator memory.

## Observations and implication

| Control | Actual effect | Retained scanner |
|---|---|---|
| Direct address; immediate add | Correct span byte written | Correct exact target |
| Call with volatile RAX; `xor eax,eax` | RAX changes to zero | Correctly drops the old address |
| Call with nonvolatile RBX | Address survives the legal test callee | Correct exact target |
| `xor al,al` after LEA of `02165176` | Writes `02165100`, outside span | Falsely reports `02165176` |
| `xor ax,ax` after that LEA | Writes `02160000`, outside span | Falsely reports `02165176` |
| `mov al,90h` after that LEA | Writes `02165190` | Reports wrong exact address `02165176` |
| Zero index, `add index,base` | Writes `02165176` | Misses the write |
| Zero index, `add base,index` | Writes `02165176` | Misses the write |

The script already clears Win64 volatile registers at calls and normalizes
32-bit names. Its map omits 8/16-bit aliases. Its register-register ADD case
falls through to destination invalidation in **both** orientations; this is
not the same algorithm as OPUS's newer receiver-provenance census. Merely keeping
an unknown-index base as an *exact address* would be an unsound fix. The owner
should conservatively invalidate partial-register aliases, and either preserve
sound constant/affine information or explicitly count unresolved computed bases.

The source's unconditional **“A HIT is decisive”** claim is unsafe. Until repaired
and affected evidence rerun, ASTRA does not accept its exact address attributions
without independent instruction/path validation. Its historical image-wide
counts and absence argument require owner revalidation. This package does **not**
show that one of these synthetic patterns occurs in the historical FF12 scan,
or that its reported zero-span result is false.

## ASTRA impact and boundaries

The reviewed manager-mark and actor-pool checkers do not use a general propagated
receiver map. They enumerate all aliases of the selected nonvolatile registers,
pin the individual instructions and make explicit returning-callee/Win64-ABI
assumptions. The manager mark's table calculation verifies base, index and byte
width at the actual store. These controls do not invalidate those packages.

The reviewed pointer collector resolves **RIP operands only** and preserves the
indexed-reader counterexample; it does not claim a propagated all-writer census.
The spawn-manager checker replays retained read/write events and checks explicit
callback boundaries, rather than following a Capstone register-provenance map.
The grep candidates containing “tracked” in input navigation or contradiction
index prose are not register trackers. This is a bounded source assessment,
not certification of every historical tool, imported helper or database claim.

Affected canonical consumer: OPUS, `PersistentFlagPayload` field
`scriptGlobalSpaceUndeclaredTail` at `+0xCF6`, whose history cites the scanner's
121,843 resolved operands and twelve indexed sites. Preserve independent evidence:
the direct `002EF390` getter interpretation, whole-object clear and shipped-save
samples do not depend on this scanner. Do not infer runtime padding/dead space,
resurrect a nondiscriminating live read, or erase the field solely on this defect.
OPUS owns repair, affected census rerun and claim propagation; closure remains
pending its acceptance. No canonical peer file was changed here.

## Reproduce and cleanup

From the repository root:

```text
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/astra-census-impact/check.py"
```

All ten cases must execute and match the retained observations; a zero/partial
run cannot produce the receipt. A successful checker means **the defects were
reproduced**, not that the old scanner passed. No game, PC-control session,
instrumentation, save or configuration was opened or modified. Cleanup consists
of discarding local emulator objects; no native detach/restoration is needed.
