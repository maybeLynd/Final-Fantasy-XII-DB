# Identified CRT classifier, not live FF12 binding

**STATIC_ONLY.** The installed `C:\Windows\System32\ucrtbase.dll`, SHA256
`5c52e3a303baaac0e0af8bd9b96134993da34bc9d834a31ef37e1d2cdc7fe192`, exports
`_fdclass` directly at RVA `0x5F410`. Its complete 65-byte, 21-instruction leaf
ends at `0x5F450` with five return sites; 15 bytes of INT3 padding follow.
This is an identified host dependency, not a DLL shipped beside FF12 and not a
capture of the running game's API-set resolution.

The body copies the low binary32 bits from XMM0 with `MOVD ECX,XMM0` and uses
integer exponent/mantissa masks. It derives these signed codes in EAX/low AX:

| Exponent | Mantissa | Code | Meaning |
|---|---|---:|---|
| all ones | nonzero | 2 | NaN, including quiet and signaling payloads |
| all ones | zero | 1 | infinity |
| neither zero nor all ones | any | -1 | normal |
| zero | nonzero | -2 | subnormal |
| zero | zero | 0 | zero |

Sign is irrelevant to this partition. The complete body contains no floating
arithmetic, memory operand, call, or MXCSR access. This source proof does not
observe FP exception flags or establish effects in an omitted caller.

The shipping-image import witness identifies IAT `0x008C2C10` as
`api-ms-win-crt-math-l1-1-0.dll!_fdclass`. Original GGRID's two calls compare
returned AX with 2 and exit early on equality. The retained EXP-131 fixture
already declares these five class codes, and explicitly scripts the import.
The new host body therefore supports that dependency model **conditionally on
binding this exact implementation**. It does not turn any old bridge into an
original native or live execution, or prove an actual game's CRT identity.

`source.json` retains exact host export/body bytes and disassembly, original
FF12 import bytes rechecked by the pinned existing image reader, and canonical
Git dependency blobs. `result.json` records the source partition, twenty
illustrative bit patterns, and three rejected source mutations. These examples
are conditional calculations, not native observations or exhaustive runs.
The checker verifies the complete decode, branch closure and five return sites.

The first capture stopped because an old EXP-131 checkout uses CRLF while its
canonical Git blob uses LF. No result was produced. Its producer and partial
capture are retained under `historical-canonical-byte-precondition`. The corrected
producer retains exact pinned Git blobs, records checkout hashes/lengths, and
accepts only newline-equivalent views; other differences still fail. No published
input changed. Reusable lesson: source text identity must name canonical bytes,
not silently equate a checkout with its Git blob.

No DLL was loaded or executed, and no FF12 process, PC control, save/config or
reference write was used. Owner incorporation and independent review are pending.
Actual live binding and initialization remain open. Do not repeat these source
controls after their intended claim is settled.

Player version: the tested assumption concerns how the game's maths library
labels unusual number values. This DLL's code agrees with the fixture's labels;
we have not observed that library being selected inside a running game.
