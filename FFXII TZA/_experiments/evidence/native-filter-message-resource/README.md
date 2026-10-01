# Native fatal-error resource and lookup preconditions — ASTRA (SOL)

The original filter's `0x7837` request names a counted Windows string resource.
Method A resolves the embedded data and lookup mechanics; no game or native API
was executed. The verified shipping image SHA256 is
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The committed81 filter bytes establish the input and call to `0019A510`.

Original lookup `0019A510` requests type **6**, block
`((uint32(id) >> 4) + 1) & 0xFFFF`. It visits module candidates obtained through
`0080C51C` from registry `02EAF320`, and stops after finding a nonnull selected
string or exhausting candidates. Source calls for finding, loading, locking and
sizing the resource are resolved against the original import lookup bytes.
Module initialization, module order and successful API effects are unobserved.

The selector `0019A5B0` uses `id & 15`, skips earlier strings by their leading
u16 lengths and returns the **length-prefix pointer** for a nonempty selected
string; empty, unavailable or out-of-end selections return null on the normal
paths read here. It does not return `text+2` or create an owned string itself.
This connects to81's leading-u16/pointer+2 call. The current-pointer checks do
**not** establish complete malformed-resource or lifetime safety.

The original executable's RT_STRING block **0x784**, entry **7** contains nine
language variants. The English entry (`0409`) is **“Fatal error encountered.”**:
24 UTF-16 code units, prefix offset346 within its682-byte block. Its counted
bytes do not include a nul terminator. German, Spanish, French, Italian, Japanese,
Korean and two Chinese variants are retained individually; the raw language IDs,
lengths and bytes are authoritative. The neighboring entries and all16 prefix
boundaries distinguish this entry from an adjacent string. A block's codepage
field is recorded independently of the counted UTF-16 representation.

This establishes embedded candidate text, not the initialized registry's selected
module, Windows's selected language, a successful loaded resource, a captured
displayed message, callback effects, pointer lifetime or EXP-127's failure cause.
`FindResourceW` can search another module from the registry. No universal default
language, normal-game reachability or termination claim is made.

Exact lookup148B, selector159B and module-getter124B source windows have local
branches validated through instruction targets. The getter uses signed index
bounds, the field at `+0x58`, an indexed pointer at `+0x50`, and a special pointer
at `+0x10` when the index equals the bound. These are source mechanisms, not a
captured registry layout/lifetime guarantee. A trap at `0080C597` terminates the
local graph. An initial console preparation wrongly followed that trap into an
adjacent routine; actual capture/checker now treat `RET`, `INT3` and `UD2` as
boundaries. No accepted package depended on that preparation.

Raw original code/resource-directory/data/import bytes, tools and driver identity
are retained; normalized observations live in `result.json`. The reviewed shared
access-role adapter is called on actual decoded instructions, with store/LEA/RMW
controls. Current Python/Capstone module/DLL hashes are required by the reducer.
This is82's tool measurement, not a retroactive claim about81's original DLL hash.

Default capture validates retained data without recapture. Focused alternatives
reject neighboring-index binding, invented nul termination and trap fallthrough.
A private wrong-provider receipt is exercised through the actual default capture
and must fail before producing a result. These producer controls and source
calculations are separate from independent project acceptance.

FABLE owns CV-3 prose; OPUS owns resource/ABI contracts. DATA incorporation and
SPEC independent review are separately queued. Published81 remains immutable.
PC OFF, saves/config/reference binaries unchanged; S19 allowance stays spent and
extension unapproved. Full L1+L2 remains NOT_MET.
