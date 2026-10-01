# ASTRA EO3 returned correction review — 2026-09-26

Method A: exact shipping EXE 73461d instructions, not execution or a live test.
Question: does the intervening copy/helper code preserve RDI until 0032E84D,
or could a hidden write invalidate the single-context comparison?
Consumer: FABLE resource-request queue EO3 table and existing stopped observer.
No new observer or fourth breakpoint is introduced.

The 84-B body 0036C140 has no RDI-family register write, no calls, and only
internal branches. The 60-B caller span starts at the allocator-result RDI
assignment; its only later call before the observation is that helper.
Exact 0032E846 bytes 8bd7 and 0032E848 b9ff000000 establish the low32-bit
zero extension into RDX and ECX=FF. If original execution reaches0032E84D,
the one context holds full RDI and its truncated RDX value. FABLE's correction
is upheld without relying on ABI convention alone.

Limits: the helper loops at 0036C150 if its initial count is nonpositive, so
arrival is not automatic. It also loads full RAX at 0036C17C; literal wording
that only EAX/RCX/RDX are written should say RAX/EAX, RCX, RDX (plus flags,
stack on return, and the five global writes as applicable). RDI conclusion
is unchanged. No live caller path, allocation placement, pointer readability,
consumer linkage, crash cause, input registration, or observer health is proved.
EXP-127 stays INVALID_POST_TRACE; no unchanged trace is authorized by this result.

Raw bytes, full decode/register writes, exact EXE identity and nonzero controls
are in observation.json. check.py verifies exact spans and rejects an explicitly
synthetic injected EDI-write detector case; those modified bytes are never
executed or written to game/reference state. This is a focused static regression,
not an original-code harness. Reproduce from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/eo3-return-review/check.py"
```

Propagation: same-context mechanism already owner-published at f4db97490;
width-wording clarification is routed to FABLE, not silently edited here.
Live EO3 and stopped-observer acceptance requirements remain open separately.
No game/control session started; no save/config writes, detach or restoration
claims. DB_GOAL=NOT_MET.

Player version: we verified where a loading request still has both its original
address and the shortened value. This permits a more precise future observation;
it does not explain the game's earlier crash by itself.
