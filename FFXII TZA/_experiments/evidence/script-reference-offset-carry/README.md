# PUSHP class/width preservation needs an offset domain — 76

Method **A / STATIC_ONLY**. Exact shipping PUSHP entry268100 through its normal
RET2681A3 (164 bytes), adjacent six-entry scale table24, and reviewed access
adapter retained. EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
No original instruction, guest, native or live execution.

Question: does the handler unconditionally preserve the packed class and force
width exactly7, or can computed-offset bits contribute to those fields?
Source distinguishes these hypotheses without another runtime setup:

```
scaled = low32(index * stride)          # widths0/1:1, 2/3:2, 4/5:4
sum    = low32((descriptor & 0xffffff) + scaled)
packed = sum | (descriptor & 0x07000000) | 0x70000000
```

The source masks **before** the ADD268166, not after. OR268169 puts back saved
class bits without clearing carried bits; OR26816C sets bits28–30 without
clearing bit31. There is no intervening mask/rejection before the dword payload
write268194. The capacity branch drops a full-stack push; it does not validate
the computed offset. Resolver CALL262440 is inspected but neither executed nor
stubbed. The local scale-table branches reach the single normal epilogue.

These are **conditional calculations**, not observed references:

| descriptor | index | stride | packed result | class | width | float bit |
|---|---:|---:|---|---:|---:|---:|
| 02FFFFFE | 1 | 1 | 72FFFFFF | 2 | 7 | 0 |
| 02FFFFFF | 1 | 1 | 73000000 | 3 | 7 | 0 |
| 02000000 | −1 | 1 | FFFFFFFF | 7 | 15 | 1 |
| 42000000 | −1 | 4 | FFFFFFFC | 7 | 15 | 1 |

Within24-bit computed sums preserve the original class and yield width7.
Positive carry can set another class bit; negative low32 sums can also set the
float bit and bit31, yielding width15. Saved class bits are retained by OR;
that is different from guaranteeing the resulting class is identical. The
original auxiliary width-byte write and tag1 path are separate from decoding
the resulting packed dword. Do not silently insert a final offset mask or exact
width replacement in an executable specification.

Controls distinguish a final24-bit mask (positive carry would yield72000000)
and exact width7 replacement (negative width4 would yield7FFFFFFC). Actual source
operands/table/branches/writes and shared adapter payload-store/read/LEA-address
classifications are checked. Three fault assertions fail; the actual producer
default reduces unchanged raw. Published primary preimage is an immutable
git-show view at its recorded commit, not an assumed identity for peer dirty
bytes. Preparation failures are retained additively: helper inspect.py shadowed
stdlib before image read, then a dirty consumer preimage stopped capture before
raw/result. Producer/import path and read procedure were corrected; no accepted
conclusion depended on either failure.

Consumers FABLE/OPUS/DATA: qualify unconditional class-preserved/width7 prose and
models with arithmetic domain; preserve literal low32 ADD/OR effects and original
width versus packed-width distinction. Incorporation and independent SPEC
acceptance are separate from these producer controls. Do not exclude required
out-of-domain DB questions simply to reach zero.

Not proved: actual shipped offset/index combinations, reference occurrence,
upstream validity/caller/frame/depth, bank initialization/lifetime, consequences
of consuming these hypothetical references, native faults or malformed-input
safety. Package74's conditional flattening is not evidence of a shipped large
array. No PC/process/instrument/host-native allocation/save/config/reference
change. S19 spent/unapproved extension persists; full L1+L2 DB_GOAL=NOT_MET.
