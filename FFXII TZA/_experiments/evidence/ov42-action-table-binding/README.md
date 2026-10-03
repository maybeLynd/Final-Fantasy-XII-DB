# Action-table binding: pointer identity is insufficient

Player version: an action number is converted into an address in the loaded action
table, then back into a number when a special sequence is queued. The earlier
arithmetic proof requires both steps to use the same row base and stride. This
packet identifies what loading changes; it does not claim a reload occurs during
an ordinary attack.

Question: can unchanged descriptor-pointer identity substitute for unchanged
decoded rows-base/stride across `304934 -> 304F4D -> 3068A7/3068B2`? Competing
explanations were an immutable initialized binding versus in-place rebinding or
alias writes. Method A suffices to refute that substitution and correct the
binder specification. Actual call-window writer exclusion remains unresolved.

Original image SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred base00120000. Four complete physical bodies total1870 bytes:
`236C30`1037, `237FC0`404, `3845F0`252, `3846F0`177. Exception metadata,
chained extents, raw bytes and actual reviewed access roles are retained and
checked against the original image. These are previously named native functions,
not four new experiments. Entry-only lookup found no covering maps in the named
corpus for these bodies; that is not global absence of prior disassembly.
The complete10-byte decoder20E600 and9-byte encoder20E620 are reused from exact
committed source maps. Existing K14 arena evidence is consumed, not reopened.

The actual action binding passes through an argument-specific wrapper:

- `236D7B` loads directory QWORD0208E680; `236D82` reads DWORD+3C intoECX;
  `236D85` calls237FC0.
- `237FCF` signextendsECX intoRDX, `237FD5` takes address02EBF138,
  and `237FDE` calls3845F0.
- `3845F4` stores the descriptor QWORD into the slot before the null check
  and field rewrites. This order is not atomic initialization or concurrent
  visibility proof. The wrapper subsequently constructs another lookup;
  allocator/initialization success is outside this packet's acceptance.

For nonzero descriptor fields+C/+10/+18/+1C, the binder adds low32(D) and stores
the low32 result. There is no initialized/rebased flag check before the+C update.
Zero fields remain zero. With valid separate slot/storage, arena0, D=00100000
and initial+C=20, two supplied binds store00100020 then00200020 while publishing
the same descriptor pointer. This is a mathematical countermodel tied to original
instructions, not a native call, stock resource sample or proof of natural
double binding. It disproves general idempotence and the pointer-equality shortcut.

For nonzero+14, let M=low32(old+14+low32(D)). The binder calls20E620 and stores
E=low32(M-low32(A)). If M!=0, it then calls20E600 to visit the nested directory.
20E620 is the encoder, with a DWORD arena read;20E600 is the decoder, with a
QWORD arena read. Both are complete leaves with no calls or memory writes.
The stored+14 is an encodedDWORD, not a resolved pointer. Decoder output is
low64(A64+zeroextend32(E)); an unchanged arena gives a low32 roundtrip, not
universal full64 identity. The original registryAG12 wording at its+14 row must
be corrected by the owner. Other published captures/results stay immutable.

Direct fixed-displacement stores in3845F0 do not target descriptor+4/+8. That
does not by itself prove whole-call preservation: nested directory and child
entry writes can alias header storage without a validated layout/disjointness
premise. A supplied count-zero directory atD+4 has its last DWORD atD+8;
original3846B9 addsD+4 there, changing stride60 to64 in the chosen model.
This is a deliberately overlapping generic descriptor, not a stock action
table or naturally reached malformed resource. Preserve that distinction.

For the first outer-count directory entries,3845F0 calls3846F0 withR8D=0.
The child encodes its supplied pointer into the entry, decodes its directory,
and follows the zero-depth branch that adds the child base to each of its
count+1 entries. This branch does not recursively call itself. Storage validity,
separation, ordinary ABI and arena consistency remain explicit preconditions.

Producer01 rejected an overly strong dominance assertion before writing any
result: zero+C skips its write while nonzero+14 still reaches the encoder.
Producer02 checks order under the named nonnull/nonzero+C prefix. The failed
driver/raw status and a focused zero-row CFG regression control are retained.
An earlier direct-slot-LEA inspection also failed before output; the wrapper
chain above replaces that mistaken search assumption, not an absence claim.

Reproduce `prove.py FRESH_RESULT.json` from repository root. Result02 validates
exact Git inputs, original bytes, reviewed roles, complete leaves, operation
widths and conditional order before emitting facts. Control01 reuses that
actual positive and exercises four actual CLI refusals: failed extent exit,
capture exception, empty successful capture stdout, and missing encoder input.
Each refusal leaves no result. Six source/CFG controls check changed widths,
encoder direction, sign extension, slot identity, zero ranges and the conditional
order defect. Case receipts retain exact input hashes and changed files;
reconstruct each negative from the base package plus its declared mutations.
Controls are producer verification, not independent acceptance or native runs.

Consumers: FABLE corrects registryAG12 and records the narrower OV42 binding
frontier; OPUS incorporates widths, slot-before-rebase order and layout premises;
SPEC independently reviews the exact final packet. No peer-owned page is edited
here. Required closure remains pending until consumers agree.

Next discriminator: actual resource registration/reset/reuse paths and whether
any reachable callback/writer can alter+C/+8/arena during the named combat window.
A direct-reference census, binder pointer identity, or an empty live trace cannot
replace that proof. The previous current-row quotient result remains conditional;
wholeOV42, ownership/lifetime and natural command reachability remain OPEN.
Historical accepted formerly-runtime eliminations remain4; no new whole item is
credited before review/incorporation. FullL1+L2 and deployedM0-M5 goal ACTIVE.

No game, native/emulated execution, PC control, instrumentation or save/config/
reference/peer change. All own finite children completed. Parked menu allowance
remains spent/unapproved; EXP127 invalid; K14 closed. Continue independent source
work while review waits.
