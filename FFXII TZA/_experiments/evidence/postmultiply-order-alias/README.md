# In-place matrix composer: operand order and right-buffer overlap

**PASS_STATIC_ONLY — method A. Zero new original-code executions or live runs.**
Complete shipping003977B0,349B, RET0039790C, body SHA
`69b03e9207174ab6f16e5d56817186ec446e5348ab0025255fc8a585d064b726`;
image SHA`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
base00120000. Source retains full raw bytes, complete decoded instructions,
tool/reader identity and exact current workbench preimage. The shipping reader
hash-gates the entire image. No game/setup/save/config/reference writes.

Question: the page's349B description says each output is
`sum_k stack[r][k]*rdx[k][i]`, C=A*B, and that the snapshot prevents write-back
aliasing the operand. Both claims need qualification from this body's own bytes;
00397910's separate alias campaign does not establish003977B0's semantics.

Let A be the original16 floats at RCX, B the16 floats at RDX, C the output at RCX.
The actual flat equation is:

`C[4*r+c] = sum_k B[4*r+k] * A[4*k+c]`.

This is **B*A for flat row-major matrices**, equivalently A*B under column-major
interpretation. It is a local flat-address equation, not an enginewide storage
convention or assertion about an application's intended composition order.
The page's explicit operand-index equation is reversed. FABLE owns its correction;
OPUS owns precise primitive preconditions. Other pages name calls, not this equation.

003977CD/D5/E6/F6 load the four16B rows at RCX+0/+10/+20/+30; stores
003977DD/EE/FD and00397805 copy those64B to the private frame. With destination
D and frame F, original LEA/SUB produce R8=F-D, R9=R10=F+10h-D,
RAX=D+20h. For loop column c, the four scalar source loads therefore select
**A[c],A[4+c],A[8+c],A[12+c]**. They multiply four contiguous words of each
row of B, then store C[c],C[4+c],C[8+c],C[12+c]. RAX advances4 bytes; R11
starts4 and decrements1; JNE003978E8 goes back00397810. The first three output
rows sum k1+k0, then k2, then k3; the fourth k0+k1, then k2, then k3.
Do not silently change this ordering for exceptional or cancellation-sensitive floats.

Conditional exact finite discriminator: A=diag(2,3,4,1), B=identity with
B[0,1]=1. Original source equation gives C[0,1]=**3**; the page's row-major
A*B gives**2**. Identity-only inputs agree and cannot distinguish them.
`check.py` decodes the retained raw body itself and symbolically reduces only
the original straight-line SSE loop into expression trees. It checks every
output's operand indices and retains sum ordering. This is source analysis;
the conditional values are not executions or a model agreeing with its fixture.

Only A is copied. All16 B words are read again in every column. With exact
RCX==RDX, column0 writes word0 at0039785E before column1 rereads word0 at
00397829. The copied A values remain stable, but later B values have changed.
For a matrix with leading2x2 block[[1,2],[3,4]] and identity on the other axes,
disjoint same-valued B gives square[[7,10],[15,22]]. Exact buffer alias gives
**[[7,22],[15,46]]** from that ordered dependency graph. All arithmetic here
is exactly representable in f32, so this finite example does not depend on
reassociation/rounding. The runtime buffer/caller occurrence is unobserved.

Reusable preconditions: normal ABI,16-byte-aligned valid64B A, stable valid64B B,
private stack frame unaliased by arguments. Keeping B disjoint from writable A
is sufficient to retain the flat equation. No arbitrary partial-overlap taxonomy
or global alias safety follows. A snapshot protects reads from A, not B's
loop-carried reads.003978F9 calls the cookie checker; this A package does not
execute that library/native boundary or establish its effects/return register.

Rejected hypotheses retained: row-major A*B, both operands staged, and identity
as a discriminating control. Published inputs/results immutable; frozen checker
compares the receipt instead of overwriting it. Named FABLE/OPUS incorporation
and independent SPEC review remain pending, not acceptance by routing.
No live caller, ownership, reuse, scheduling, camera presentation or integrated
parity claim. PC OFF; spent S19 setup allowance unchanged; L1+L2 goal NOT_MET.
