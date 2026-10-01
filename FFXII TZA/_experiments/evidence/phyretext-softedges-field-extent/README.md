# PhyreText softEdges: named shipped field and conditional source extent

Method A STATIC_ONLY; producer-valid, independent acceptance pending.
Player version: the original text initializer copies an eight-byte setting from
its object for this shipped shader field. That particular source extent stops
well before the debug action selector. Other calls, aliases and later lifetime
effects remain unanswered; no FF12 session was needed.

QUESTION: does the exact shipped PhyreText softEdges descriptor authorize an
extent reaching outer object+AE0 from the original1EA609 source at outer+120?
H1: a short field excludes those source bytes. H2: its size reaches them.
Competing general lifetime/alias/resource explanations are separate questions.

The binary points through1DFDE00 to ./GameData/D3D11/ArtData/shaders/PhyreText.fx.phyre
and through1DFDE08 to tuffysdf.fgen.phyre; the lookup literal at901B18 is softEdges.
One uniquely named VBF shader entry was selectively read,44,634B, SHA
f67d4492c21fc687f8897c130f66e8cddf5d8d2f0d262589b8597791a767a4cf.
The archive/index/entry receipts include the original selected tuple and stable
archive size/mtime; there is no full31GB archive hash. Reference EXE SHA
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000.

The accepted EA-3 parser and CU-3 packed decoders are retained unchanged. Only
AST-selected declarations execute; their broad census/main code does not run.
All three tables consume their exact sizes and per-list counts, with zero tail
for this shader. The file's own class43 definition schema gives13-byte packed
records, name at4 and capture location at5. Its12 objects occupy156B at29224;
their164B array region starts29380. Native reflected record layout is24B, name+8,
capture location+10; file offsets and native offsets are not interchangeable.

Array fixup(80000004,8,0,138) selects the name member of object8 and the bounded
NUL-terminated name at29518. This is the serialized name binding, not one of the
15 string hits elsewhere or a captured live pointer. Original59C250 clears the
key high bit, resolves a member, adds entry+0C to its array base and delegates
the array assignment;59BED0 resolves the packed member range. The location
class44 inherits m_offset from class38; its own m_size is at2. No assumed zero
offset substitutes for a missing parent.

Record8 at29328 is0000400100a0000800b8000000: capture offset160, whole size word8,
size&1FFF=8. Distinct controls textColor16 and alphaThreshold4 use the same named
record route. The original lookup has two24B arrays and first-match precedence;
no fresh original-machine-code execution or whole lookup census is claimed.

Original1D03C6 passes outer+8 to1EA3C0;1EA3DC keeps that receiver inRSI.
1EA5C1 selects receiver+118=outer+120 as source. At1EA609 the verified
VCRUNTIME140.dll memcpy import receives destination=resource-base+offset,
source=that object region and length=descriptor size&1FFF, after offset>=4 and
offset+size<=DWORD[resource-base] checks. CONDITIONAL on lookup returning this
unchanged shipped definition and reaching the copy, source bytes are120..127.
Reading anyAE0byte would require length>9C0; all four require length>=9C4.
H2 is refuted for this named unchanged file extent; H1 holds at that scope.

OPEN: actual loaded material/parameter-list membership and successful resource
binding, later metadata modification/other definitions, allocator/destination
aliasing with the outer object, all other callees/writers, constructor-return
AE0 survival, lifetime and natural command/action reachability. A bulk source
read is not a direct selector write; a disjoint source extent does not prove
its destination cannot alias the selector. No universal OV42 exclusion follows.
No runtime pointer, portable default or unmodified gameplay observation is claimed.

Reproduce final bounded reduction, from repo root, with a fresh result path:

    python <packet>/reduce-softedges-field-extent.py <packet>/softedges-resource-source-01 <new-result.json>

Controls retain disposable byte mutations and actual subprocess stdout/stderr/
exit/no-result receipts: enlarged extent9C4 reverses the conditional read result;
changed name, broken inheritance, wrong objects extent and truncated fixup refuse;
actual CLI incomplete source, missing caller and changed shipping hash fail.
These nine private producer controls are not native/live tests or independent
acceptance. The first reducer's inherited-member KeyError exited1/no result;
driver/failure are retained, producer repaired and concrete parent-break control
added. Historical field-result01 remains immutable; final02 adds the retained
caller, literal/import and native-reflection prerequisites. No other accepted
claim depended on the failed producer. Capture paths use shared reviewed
reg_tracking.op_kind with actual store/LEA/RMW controls.

Consumers: SWE2-AUDIT-SPEC independently reviews the binding and limits; FABLE's
OV42/default-lifetime mechanism may incorporate only accepted conditional read
extent, and route any OPUS-owned structural change. No peer page was edited.
This narrows one original initializer dependency offline; it does not close a
whole OV row or add another retired runtime request. Goal remains ACTIVE/NOT_MET.
All own commands and synchronous test children terminated. No PC control, game,
instrument, saves/config or reference binary was changed. Parked menu allowance
stays consumed/unapproved; EXP127 staysINVALID_POST_TRACE.
