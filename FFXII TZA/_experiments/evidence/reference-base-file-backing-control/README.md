# The quoted base-cell bytes are not a file-backed cell sample

Player view: the game image reserves this cell in a region that starts zero-filled. An unchecked address-to-file calculation finds nonzero bytes from somewhere else in the executable. Those bytes cannot establish that this cell starts nonzero or currently holds that value in the running game.

**Method A.** Original certified PE header and section table, existing guarded shipping-reader positive/negative controls, a labelled unsafe-file-offset control, and the primary PE specification. No original/native/emulator/live execution or loaded-state sample. Existing load-zero/writer findings are reused, not recounted or newly discovered.

The primary SPEC42 review says `Cell contents 90 FB 05 00 nonzero`. Its codec width/modular proof is independently valid; this specific byte witness needs provenance. Exact reference73461d section identity:

| .data field | original value |
|---|---|
| RVA | 0x1CD0000 |
| VirtualSize | 0x11A7530 |
| SizeOfRawData | 0x18E400 |
| PointerToRawData | 0x1CCE600 |
| raw-backed VA end, base0x120000 | 0x1F7E400 |
| virtual VA end | 0x2F97530 |
| questioned cell | **0x1F83530**, past raw end, inside virtual span |

The [Microsoft PE section specification](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#section-table-section-headers) distinguishes initialized disk bytes from the zero-filled remainder of a larger virtual section. The known owner contract already states this cell is zero at image load and an undriven computed writer exists. No process-lifetime-zero or no-writer claim follows.

Actual existing `img_rd` accepts the file-backed1.0 constant, the already-retained9-byte encoder and the last8 serialized `.data` bytes. It rejects both4-byte and8-byte cell reads, the first unbacked8 bytes and a read straddling the raw end. The guarded reader is correct; no canonical index or central-reader regression is alleged. Raw refusal is not an observation of zero memory.

A deliberately unsafe formula, `raw_offset + (targetVA − preferred_base − sectionRVA)`, accepts the address using VirtualSize while ignoring SizeOfRawData. It reaches file offset0x1E61B30 and reproduces **90FB0500BAFB0500**, matching the quoted low4 bytes. Those bytes belong to the separate raw section and legitimate mapped address recorded in `result.json`; the guarded reader confirms that other address, not the questioned cell.

This is a discriminating **failure hypothesis**, not proof of SPEC's actual producer or cause. The witness could instead refer to intentionally injected or live state, but neither provenance is supplied in that sentence. SPEC must identify the actual invocation/input/mapping method, then preserve the original plus an additive correction or explicit intervention/live label. If an unchecked raw translation was used, fix that exact producer/procedure and inventory only its dependent claims, with positive raw-backed and negative virtual-tail/straddle controls. Do not build a new loader or broadly invalidate accepted reviews.

OPUS independently reviews this narrow structural evidence. The stable-base modular inverse proof42 stays valid; no actual nonzero/high runtime base, portable default, mapped-address validity, ownership or lifetime is established here. Raw/code/header/reader/context/review preimages and tools are retained. Readonly `check.py` verifies them against the original image and the existing reader; own checks and integrity are not independent acceptance.

No game process was listed by the bounded FF12 process inventory. PC control remains off; no game/input/instrument/save/config/reference/peer writes. Parked menu budget remains consumed/unapproved. Full L1+L2 goal remains NOT_MET. Consumer/procedure correction and independent agreement stay pending until the actual witness path is identified.
