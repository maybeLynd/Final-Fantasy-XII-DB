# SWE2-AUDIT-SPEC review — OPUS DD owner re-status batch 3 (`d46835689`)

Task: `OPUS-REQ-AUDITSPEC-DD-1599-C-0930`. Pages: `reflected-render-parameters-and-shader-assets.md`,
`frp-object-container.md` (PARTIAL → DOCUMENTED).

## Verdict: ACCEPT-WITH-NARROWING

The commit's action was procedurally correct against the records standing at commit time — sections
filled, claims tier-cited, dispositions fair. **However the batch's headline outcome no longer holds
on one page:** `reflected-render-parameters-and-shader-assets.md` is currently PARTIAL, not
DOCUMENTED. Its DOCUMENTED flip rested on SD-141's 2026-09-30 answer ("nothing reads the flying-fade
pair"), which this lane REJECTED and which was then corrected twice (`02ce73b03` reopened the page;
the current tree carries the corrected GPU-consumer answer from `sd141-gpu-consumers-1001`: the pair
is copied by `005DEC50` into a snapshot `00604750` writes through `006097B0`/`00626060` into the
SceneWideParameterConstantBuffer at `+0x5D4`/`+0x5DC`, and 517 `phyredefaultlitshader.fx` DXBC blobs
read it). The page's present PARTIAL status line is accurate — OV-42 (live, ASTRA) stays open and the
resolved SD-141 chain is stated. This is supersession by later evidence, not a defect in the batch
commit; recorded here so the verdict cannot be read as "the page currently stands DOCUMENTED".

## Verification

**frp-object-container.md** — ACCEPT, all claims verified:

- §7 "Nothing about entry contents" closed for this sheet: each entry tag is decoded on its own
  sheet (§9 census of all 4,230 files + per-format sheets fcp/ftr/fdm-for/fte-fct/fef/motion),
  residue stays there — correct disposition for a container sheet ✓
- §7 "Why variant 1 exists" declared a build-tooling limit, resting on §3's "The write path. None
  found." — **independently verified**: image-wide scan of the `@FRP` dword (`0x50524640`) found 11
  in-.text occurrences; every decoded site is a magic-validation `cmp dword [x], imm32` or a
  lookup-key `mov edx/r9d, imm32`. **Zero store forms** — nothing in the image writes an @FRP
  container, so the variant choice genuinely belongs to offline build tooling. The limit is a fair
  and honest disposition (same reasoning §7 already applies to the alignment policy) ✓
- `PROPOSED-repos-4b-14`/`-15` correctly left as history, not register ids ✓
- Status line: DOCUMENTED, no open register row ✓

**reflected-render-parameters-and-shader-assets.md** — action correct at commit time; outcome
superseded as detailed above. The current page correctly preserves the full correction chain with
strikes and dated attributions (line 147 / line ~400 checkbox), and `last_pass_state:
swe2auditspec-sd141-reject-corrected-pass-2` names the review that drove it.

## Scope note

No new measurement was claimed by the batch; the only load-bearing native claim under test (§3's
no-writer finding) was re-verified independently by magic-store census.
