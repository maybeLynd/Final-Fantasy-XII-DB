# Native relation reset versus pool release

Question: do 00512EE0's inline reset and 00512C80's linked clear have the same
ownership effects? Must a caller that resets a record first release its linked
rows? This changes the cache representation/lifetime contract, independently
of whether a natural summoner KO reaches either path.

Competing explanations: both release the fixed-pool rows; versus only 512C80
walks/releases them, and 512EE0 merely resets the owner's markers. Static bytes
can distinguish these. Method A: bounded entry-reachable leaf CFG, shared byte
roles, write/dataflow census. No emulator or process required for this claim.
Stop after that discriminator; actual caller order/reuse remains a new exact
question, not implied by these local effects.

Starting reference EXE73461d08/base120000; actual shared reviewed capture path.
Two no-covering-pdata entries: 512C80 bounded before proven512CD0 entry; 512EE0
bounded before physical512F30 entry. Check original bytes, all direct normal
successors, no calls and RET boundaries; do not invent physical function roots.

Controls planned: remove the pool flag write or add a pool write to simple
reset must invalidate the effect distinction. Changed final global-counter
write must invalidate decrement accounting. Preserve normal valid indices,
disjoint owner/pool and finite acyclic owned-list premises. Negative 'no pool
effect' must come from the complete qualified code, not absence sampling.

Downstream OPUS cache-type/ownership contracts; FABLE relation-lifetime/KO
composition. Existing DATA access census not duplicated. No whole UQ147/OV
row, natural initialization or reuse acceptance. No game/save/config/reference
or peer process writes; finite static capture only. Current parent owns work.
