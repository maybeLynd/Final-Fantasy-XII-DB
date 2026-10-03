# Consumption draft: ov42-interpreter-transfer (FABLE, 2026-10-02)

*Paths are plain backticked text; the applier turns the packet and record paths into page-relative links.*

Drafted against the availability page at `1c4c5820f`. It appends one subsection after the other OV-42 subsections of
the same package. The new text cites `00309C00`, `00267E10`, `0030EEA0`, `0030CFB0` and `0031B7E0`, all already cited
on the page, and the data cell `022C2170`. The script bridge, the reference getter, the interpreter's push (PUSHV) and
the decoder's native are named by role; none is cited on the page by entry.

## Edit 1 (FABLE page): new subsection at the end of the page

```
### FABLE 2026-10-02: how the queued word survives the script round trip, and when it does not (OV-42)

*From ASTRA's packet `ov42-interpreter-transfer` (`_experiments/evidence/ov42-interpreter-transfer/README.md`,
`76dfc5dc6`), reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-interpreter-transfer-1002/REVIEW.md`, 77 checks, 0 FAIL, 9 controls).
Static, plus an emulation of the original push, pop and decoder.*

- **The store is raw.** The queue reader `00309C00` writes the queue DWORD through the bridge's first-resolved
  out-reference with a plain 4-byte store, not the interpreter's typed store. The reference getter picks a base from
  bits 24..26 of the reference word and adds its low 24 bits; it never reads the width or float bits, so the
  variable's declared width does not narrow this store. Scopes 6 and 7 take base 0.
- **Reading it back separates width from kind.** The interpreter's push loads the variable at one of six widths
  (u8, s8, u16, s16, s32, f32, from bits 28..31 of the resolved record) and tags the payload by the record's kind:
  kind 1 integer, kind 2 float (the same 32 bits). The pop `00267E10` returns a tag-1 payload exactly and converts a
  tag-2 payload with CVTTSS2SI. Pushes need depth below 63.
- **The decoder needs only the low 16 bits.** The decoder's native passes the first pop in EDX and the second in ECX
  to `0030EEA0`, which turns −1 into FFFF and otherwise adds 0xD0 in BX (16 bits). So any integer-tagged value with
  the queued word's low 16 bits, other than −1, decodes back to that word. Emulated through the original bytes for
  all 65,534 available words with u16, s16 and s32 integer loads.
- **What breaks it.** Through a u8 or s8 load, words 511..534 decode to 255..278. Through a float tag, the raw
  encoded value (303 for 511) is a positive subnormal, CVTTSS2SI gives 0 and the decoder gives 208 (emulated with
  exceptions masked).
- **The decoder is gated.** It stores the decoded word at unit `+0x758` and calls `0030CFB0` only when `0031B7E0`
  returns a unit for the second pop and DWORD `022C2170` is 4. Otherwise it returns −1 or −2, and the native discards
  that result.

**Limits kept.**

- Which variable a real script uses, at which declared width and kind, is not read. 511..534 survive the round trip
  only through a 16- or 32-bit integer variable.
- A valid four-byte destination, nonaliasing, lifetime, valid stack state and the error handler's effects are
  premises. The reader's second direct consumer (above) takes the queue without any script store.
- Whole OV-42 stays OPEN.
```

## Route to OPUS

- The script-variable representation contract: a native out-reference store is a raw DWORD regardless of the
  variable's declared width; PUSHV's width (bits 28..31) and kind (record WORD) are independent; scopes 6..7 of the
  reference word resolve to base 0.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edit 1)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_xfer.py` at HEAD (77 checks, 77 PASS, 0 FAIL, 9 controls)
