# GIF replay mode boundary

With the shared gate enabled and **positive NLOOP**, a REGLIST tag (FLG1) ends
00210320's local walk through the completion call, even when EOP is0. It does
not take the local PACKED payload-handler path. This is exact original static
control flow, not an observation of rendered output or authored packet frequency.

`primary.json` retains424 original bytes, complete disassembly, reference/tool
identity and the three contiguous PE fragments with CHAININFO parent bytes. The
entry RuntimeFunction alone is only28 bytes; truncating there would miss this
behavior. `check.py` checks full source/extents/branches and reduces the observations.
No emulator, native or live game executed for this question; A is sufficient.

## The discriminating branches

Header read00210390 is16 bytes. NLOOP is masked to15 bits; mode comes from bits58–59.
With positive NLOOP, either PRE path reaches00210473 for non-PACKED mode; its
FLG1 equality branch at00210476 goes to002104A0 (call0020EC80), followed only by
register restoration and return. Normal EOP comparison is00210489, which this
path bypasses. Native completion effects are not proved or assumed empty.

Zero NLOOP is the important boundary:002103BE skips mode parsing and00210426
skips handling, then EOP0 loops to the next header after advancing16 bytes. Thus
"every REGLIST tag stops" would overstate the result. PACKED reaches0020F3E0;
if that handler returns, its returned cursor feeds the EOP loop. IMAGE2/3 advance
over NLOOP*16 bytes and reach the EOP check without local payload dispatch.
The shared gate0 skips all input reads and the completion call.

The already-correct0020F310 sizing rules include REGLIST sizes. Measurement and
replay are separate operations: a sized/copied REGLIST span does not demonstrate
that the replay routine processes it as a supported register stream.

## Limits and propagation

Branch witnesses cover positive/zero NLOOP, EOP0/1, PACKED, IMAGE2/3 and gate0;
they are symbolic consequences of the original instructions, not executed tests.
Native completion may submit earlier pending work. No claim of no rendering,
unused/dead authored REGLIST, ignored state everywhere or a crash is made.
Handler effects, actual packet mode population, initialization, normal reachability
and presentation remain open. FABLE mode/traversal prose and OPUS exact input-domain
preconditions are named consumers; independent review and incorporation are pending.
No family exclusion, contract or type is manufactured to close a counter.

Player version: the game can measure and copy a packet format that this replay
routine does not walk like the usual drawing format. A nonempty REGLIST tag ends
this routine's walk; an empty one follows the end-marker rule instead. This does
not yet tell us what the player sees or how often real game data uses the format.

PC off; reference read-only. No process/instrument/input/save/config changes and
no new live restoration receipt. L1+L2 database/final review goal remains NOT_MET.
