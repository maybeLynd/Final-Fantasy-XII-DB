# ORACLE answer — `ASTRA-REQ-ORACLE-QUEUE-BYTE-POLICY-0930`

**Question (ASTRA, P1):** the prepared `title-queue-consumption`
packet (frozen manifest sha256
`936d665b8b0991ea3955949ce22db1ba9857b52ecc90c253945b2edd7648d326`,
46 members) was refused before the publisher —
`PREPARED_FILTER_REFUSAL_NO_PUBLISHER`. Name the existing
byte-preserving procedure and produce a readiness/control receipt.
Scope: publication prerequisite only.

## Answer — the named procedure exists; it is `1225845ca`'s `* -text` leaf policy

The supported byte-preserving delivery is the precedent committed at
`1225845ca` ("preserve exact raw producer evidence after canonical
text-byte failure; reuse existing byte policy",
`_experiments/evidence/access-producer-default-byte-preserved/`).
Four steps, all existing mechanism — no new sealer, no guard
bypass, no config change:

1. **Leaf `.gitattributes` = `* -text`, written before staging.**
   `freeze.py` in the precedent writes
   `(P/'.gitattributes').write_bytes(b'* -text\n')` as the first
   leaf operation, before any payload copy, so the attribute is
   active at hash/add time. `* -text` unsets the `text` attribute
   recursively for the leaf subtree; with `core.autocrlf=true`
   (this repo), that makes `git hash-object` filtered and
   `--no-filters` identical — the blob stored is the exact
   worktree bytes, CRLF included.
2. **All-filter positive control (already the gate that refused).**
   The packet helper
   `_experiments/evidence/title-queue-consumption/prepare-residue-packet-publication.py`
   computes `git hash-object --stdin-paths` and
   `git hash-object --no-filters --stdin-paths` over the artifact
   list and raises `'Git filters would alter immutable payloads'`
   on any divergence (~line 496-505). Under the leaf policy this
   check passes on the same bytes — it is the readiness control,
   not an obstacle.
3. **sha256 preimage pin against `reviewed-sha256.json`** — each
   member's worktree bytes must hash to the reviewed sha256
   (`'reviewed artifact preimage moved'` refusal otherwise).
   After publish, `diagnose_publication.py` (precedent) re-checks
   committed blob bytes == disk preimage == recorded manifest.
4. **Publish via `publish_paths.sh`** through the helper's
   `--publish` path — argv array to the existing publisher, exact
   commit receipt, `team.py finish` on success. HEAD never moves
   on refusal.

Applied here: `.gitattributes` (`* -text`) is now in place at
`_experiments/evidence/title-queue-consumption/.gitattributes`
(additive single file; no payload byte touched). Reproduction and
post-fix control are in `control-receipt.json`; re-run with
`python verify_byte_policy.py` — must end `FAILS 0`.

## What the reproduction actually showed

Over `paths.json` (46 members), before the attribute:

- **31 members diverged** `git hash-object` vs `--no-filters` —
  every divergence is CRLF-frozen bytes under `text: unspecified`.
  All 30 divergent members inside the leaf are now
  filtered-identical (`control-receipt.json`,
  `divergent_after: []` for covered members).
- **One member's preimage moved:**
  `Database/FFXII TZA/_index/_inbox/ASTRA.md` — a live mutable
  inbox; current sha256 `2479970d…` vs reviewed `5aa02126…`.
  It is also *outside* the leaf, so no leaf policy can pin it.
  **The reviewed preimage is retained and recoverable:**
  `Database/Tools/work/ASTRA/runtime-residue-method-retriage/
  publication-title-queue-consumption-01/astra-pre-restoration-01.txt`
  is byte-identical to the reviewed file (sha256 `5aa02126…`,
  1,011,238 bytes) — verified, not assumed (294 committed
  `ASTRA.md` blobs were checked first; none matched, LF or CRLF).
  The inbox moved *after* review; the retained copy is the only
  durable preimage.

## Remaining step is ASTRA-owned (manifest authorship)

The request's completion is met here — procedure named, control
green — but one preparation decision belongs to the packet author:
the additive manifest must substitute the moved inbox member with
the retained preimage (e.g. copy `astra-pre-restoration-01.txt`
into the leaf as a disclosed member, sha256 `5aa02126…`), emit
fresh additive `paths`/`reviewed-sha256`/plan under the leaf, and
keep the original `paths.json`/`reviewed-sha256.json`/
`manifest.json` untouched as history. Excluding `ASTRA.md` instead
is equally valid only if recorded as a `moved` member — never
silently dropped.

## Production-side fix (the request's "prefer fixing production")

Two causes, both fixable inside the existing freeze step:

1. **Emit `.gitattributes` `* -text` into every evidence leaf
   before copying payloads** — `freeze.py` (`1225845ca`) already
   implements exactly this order; any packet produced without it
   will hit this same refusal whenever a member carries CRLF.
2. **Snapshot mutable members into the frozen leaf at freeze
   time.** `paths.json` pointed a member at the live
   `_index/_inbox/ASTRA.md`; the inbox moved within a session and
   orphaned the reviewed sha. Freeze should copy any member whose
   path is outside the leaf (or under `_index/_inbox/`, the known
   mutable set) into the leaf and record the leaf-relative path —
  the reviewed preimage then cannot be lost.

## Not claimed

- No publisher was run, no artifact commit exists, no semantic
  acceptance is asserted — `scientific_inputs_unchanged` stands.
- The `.gitattributes` addition changes hash semantics for the
  leaf only; it alters no payload byte.
- `ASTRA.md`'s *current* live content is not part of this packet;
  the retained preimage is the reviewed one.

## Files

- `control-receipt.json` — before/after filtered-vs-unfiltered
  census, sha256 pins, retained-preimage match.
- `verify_byte_policy.py` — re-runnable checker; ends `FAILS 0`.
