# Type 0x67's first two possible readers

The published bounded source scan found no direct `+0x3D8` operand in the
56-byte `0045FD10` step, but it calls `002F2530` and `004607C0`. Does either
immediate callee directly access that same displacement? This discriminates a
one-level delegated reader from a reader outside this small call chain.

Method A is sufficient for the first-level source question. Pin the published
parent call sites, certified EXE, catalogued extents and reviewed operand-role
adapter; decode only those two original bodies. A same displacement in a
callee is merely a candidate until receiver provenance is checked. No hit
excludes only direct `+0x3D8` access in these bounded bodies, not every nested
or indirect reader. Stop there unless a concrete hit changes the contract.
No native or live FF12 work; no timing, initialized identity or visible-effect
conclusion.
