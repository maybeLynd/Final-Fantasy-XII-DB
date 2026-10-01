# Original licence builder clear boundary — scoped A/B falsification

Question: qualify the current contract's “n <= 0 builds an all-zero mask” as
logical empty-mask/caller-preclear behavior versus a physical output-clear
guarantee. Do not label the logical empty mask wrong merely because its extent
is zero. Separate the standalone builder from PREREQ's precleared 46-byte mask.

H1: nonpositive loop count suppresses/fully clears caller output. H2: clear-size
calculation and callback occur first; zero clears zero bytes, and raw counts
whose high bit is set can pass a large unsigned clear argument before the signed
loop test. Neither hypothesis establishes normal game reachability of malformed
counts. Consumer OPUS licence contract/ABI and FABLE integration.

Existing A: shipping002F8FA0 stores count in eax, lea r8d,[rax+7] (32-bit wrap/
zero extension), shr r8,3, calls00861EC0 before reloading/test r14d/jle. PREREQ
00323BB0 preclears its own46-byte temporary. EXP140 runs real bodies but its
published positive builder cases do not settle warm zero-count output or this
clear boundary. Preserve its completed request and original57/35 controls;
do not replay them or take ORACLE's production.

Chosen B: reuse the immutable existing World/loader/fixture, with a scoped local
callback observer and correct Windows x64 entry-stack alignment. Four fixtures:
0,8,FFFFFFF9 andFFFFFFF8 row counts, warm46-byte output with canaries. Allow the
existing disclosed scripted memset bridge ONLY for sizes <=46. Stop BEFORE it
on larger sizes, record original argument/order and mark BOUNDARY_STOP, never
claim completed operation/large write/fault. No Python model counterpart needed
to infer agreement with itself; compare exact expected observed boundary/bytes.

Controls: full original executable and driver identity; verified code bytes;
ABI entry/callback RSP%16=8; positive count8 reaches bridge length1 and changes
exactly one output byte; zero-count outcomes preserve expected physical bytes;
no unmapped/trap/timeout; all terminal points justified; raw input/events/memory
before-after/returns and source kept. Each run2s/6000 instructions maximum; stop
the package if controls fail. No oversized allocation or clear is attempted.

Limits: guest state/descriptor rows supplied; memset is scripted, not native CRT
effects; negative clear has only entry-argument evidence. Original arithmetic,
branches/caller writes/call order execute unchanged shipping instructions. No
live game/init/resource binding, no native OS process/input API, saves/config/
reference writes or reconstruction phase. Independent review and owner
propagation remain required; no unconditional semantic closure from PASS.
