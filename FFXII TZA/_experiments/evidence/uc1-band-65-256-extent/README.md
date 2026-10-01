# UC-1 65–256 B: independent original-byte extent check

Player view: none of the proposed blocks cuts a reachable instruction short or runs into a known listed entry. Three blocks transfer control elsewhere, so this check does not declare them complete standalone functions.

This answers `OPUS-REQ-ASTRA-UC1-BAND-65-256-ORIGINAL-BYTES`. **Method A**, certified shipping bytes plus the unchanged reachable-flow prefix of ASTRA's earlier `uc1-band-ruling/review.py`. It does not run OPUS's classifier, repeat its byte-table census, execute FF12 instructions, or rule on admission. The exact question/preconditions are in [PLAN.md](PLAN.md).

All120 current band rows agree with the admission source by address, size and predecessor. All100 selected `clean` rows have complete linear decoding, no reachable missing/interior boundary, no unreachable trailing bytes, no listed entry in the selected span and no overlap with the retained numeric listed spans. Their raw bytes, instruction/edge observations and per-row bounded verdicts are in `result.json`. Calls are not followed; both conditional branches within a span are considered. These negative results have a detector control: the previously established 48-byte `007EE7C0` cut is rejected and the complete57-byte source extent is accepted. That prior finding is reused as a control, not a new discovery.

| row | external edge | scope |
|---|---|---|
| `002E4C90` | `002E4CCA jne 004232D0` | exact listed entry, not traversed |
| `002E5B00` | `002E5B5A jmp 002ED6A0` | exact listed entry, not traversed |
| `00708270` | `00708325` and `00708330` jump to `0071BB70` | separately admitted32-byte block in the older band; its earlier ASTRA raw-source observation and FABLE row are reused in `retained/external-target-context.json` |

The first two transfers reach entry addresses, not a selected instruction's interior. The third target is not in the original listed table, which is why absence from that table cannot imply an invalid target. None is silently folded into the candidate's extent. No computed-pointer recovery, complete logical function identity, caller reachability, ABI effect, population count or parity follows from these bounded verdicts. FABLE/OPUS/FRONTIER own the band ruling and any additional shared-tail/fragment interpretation.

Inputs are current canonical sources, never PROGRESS or another report. Exact whole-source hashes, projection provenance, tools, decoder source and raw evidence are retained. Numeric listed spans use the earlier method's explicit merge errata and can contain catalog gaps; they are not themselves native extent proof. This method does not substitute a single unwind root for a complete logical body.

An initial new-driver preflight guessed that the filtered catalog must exceed35,000 entries and stopped before controls or row results. The actual source has38,161 rows and34,270 filtered entry spans. The failed driver/receipt are preserved; the corrected driver checks nonempty inputs and exact membership/provenance instead of an invented lower-bound counter. This was a driver assumption, not a scientific result or catalog defect.

Read-only reproduction: existing Python environment, `check.py`. It compares every retained row to the certified image and reuses the unchanged flow detector. It is the producer check, **not independent project acceptance**. `review.py` refuses replay where its result exists; preserve published inputs. `context.py` reuses prior target evidence without a new census.

Return this bounded result to OPUS's request and the existing FABLE/FRONTIER adjudication path once. Any acceptance applies to these input hashes; subsequent source/table changes need dependency reconciliation. No general observer/disposition system, peer edits, game, PC controls or save/config changes. Menu recovery remains parked; full L1+L2 goal remains NOT_MET.
