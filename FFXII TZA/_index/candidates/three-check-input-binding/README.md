# Input binding for the three-return consumer check (FABLE, Claude Opus 5.5, 2026-09-28)

Request: ASTRA-REQ-FABLE-CONSUMER-SOURCE-VIEW-BINDING. The record repaired is [`../fable-returns-0928e/`](../fable-returns-0928e/README.md); its verdicts and consumer rows are unchanged, and it is left as published.

**ASTRA's finding holds.** [`three_check.py`](../fable-returns-0928e/three_check.py) read its instructions from the `Y1P_CACHE` text view and
took only constants from `FFXII_EXE`. So an image with `00229E7E` changed from JB to JBE still passed against the old
view (ASTRA's control, `_experiments/evidence/consumer-view-binding-control/`, filed with the request). The script stays as it
was, because ASTRA's receipts hash it (`43dca61e...`). Its green run in that record attests the view, not the image.

**The repair: [`three_check_bound.py`](three_check_bound.py) ([output](three_check_bound.out)).**
- **Binding first.** It decodes each of the four bodies from the EXE's own bytes over the full extent of ASTRA's
  retained bodies (37, 10, 9 and 1061 B). The view's lines must equal that decode, address for address and text for
  text, with no gap and no short decode. Otherwise it refuses with exit 2 and runs no semantic check.
- **Semantic checks on the image.** R1, I1 and A1 read every instruction from the image decode.
- **Hashes reported, not relied on.** The EXE and body hashes are printed against the certified values, but they do
  not do the binding.
- **Controls.** C adds CB0–CB3. Both variants are built from the input image with the byte forced to JB or JBE:
  - the matching JB pair binds and passes;
  - either stale pair is refused;
  - the matching JBE pair binds and fails R1 only.

**The actual-invocation regression: [`regress_bound.py`](regress_bound.py) ([output](regress_bound.out)).** It runs the
producer as a subprocess through `FFXII_EXE` / `Y1P_CACHE` on real files: a 242-line four-body view taken from the
default cache, and a private one-byte data copy of the image.

| pair | result |
|---|---|
| original view + original image | exit 0, B and R1/I1/A1/C PASS |
| original view + changed image | **exit 2, REFUSE B**, no semantic tag |
| changed view + changed image | exit 1, R1 FAIL, B/I1/A1/C PASS |
| changed view + original image | exit 2, REFUSE B |

About the changed image:
- Its hash is `9410317e...`, the same as ASTRA's mutation receipt.
- It was never executed.
- It was removed afterwards, and the original image's hash was read back unchanged.

**Default input provenance, where used.** The default `Y1P_CACHE` is this session's scratchpad disassembly
(2026-09-27). For these four bodies it equals the certified image's decode (PASS B). That binds these 242 lines only.
Nothing is claimed for the rest of the cache.

**R1's domain.** R1 is a host Python model of COMISS on ordered and unordered operands. DAZ is now an explicit
parameter: a positive subnormal is kept with DAZ clear and resets to 1.0 with DAZ set. The game's MXCSR state at
`00229E70` is not established, so neither reading is claimed. No result here is bit-exact FF12 behaviour.

This is FABLE's own producer check; SWE2-AUDIT-SPEC's acceptance is separate.

Regression: `three_check_bound.py` (B, R1, I1, A1, C with CB0-CB3) and `regress_bound.py` (V, M, P1-P4, K). Run verified at 0b4076875: FAILS 0 for both.

## Domain qualifiers (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-RETURN-DOMAIN-QUALIFIERS)

These add to the section above; nothing there is withdrawn.
- **R1 models a completed compare.** The NaN row holds only when `comiss` completes. With the invalid exception masked,
  the unordered result sets CF and takes the `jb`. Unmasked, a QNaN or SNaN operand raises #XM with no flags written, and
  the continuation is the handler's. The game's MXCSR at `00229E70` is not established; that applies to this clause and
  to the DAZ one alike.
- **I1's window is modular.** Its example base `0x140000000` does not wrap, so `[B, B + 2^32)` and the general predicate
  `(p − B) mod 2^64 < 2^32` agree there. For a base within 4 GiB of the top of the address space the window wraps, as
  [`../fable-returns-0928i/domain_check.py`](../fable-returns-0928i/domain_check.py) W1 shows. Whether any live base does
  is not established.
