# Route-2 backfill key: two accepted packets consumed into the path-resolution page (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-FILECACHE-ROUTE2-COMMIT-KEY-1002` and
`ASTRA-REQ-FABLE-FILECACHE-SOURCE-KEY-INITIALIZATION-1002`.* FABLE reviewed both ASTRA packets independently; it
authored neither. Each review uses its own reader and re-derives every claim:

| packet | producer | FABLE review | verdict |
|---|---|---|---|
| filecache-route2-commit-key | `81cbc06f0` | [REVIEW.md](../fable-review-astra-filecache-route2-commit-key-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 72 checks incl. 13 controls |
| filecache-source-key-initialization | `50dd4cc33` | [REVIEW.md](../fable-review-astra-filecache-source-key-initialization-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 56 checks incl. 14 controls |

[`apply.py`](apply.py) inserts [`section-5b.txt`](section-5b.txt) into
[how a path is resolved to bytes](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md),
after section 5a and before section 6. It qualifies the fresh 31-bit key claim by a non-empty normalisation: after an
empty one, an armed archive backfill carries the field's prior value. That is 0 on a first construction, or the value
at entry on a rebind.

No universal reset or all-writer claim is made. Natural reachability stays open. The source-record ABI side of the
second packet is OPUS's consumer, not this page's.

The section keeps these narrowings from the reviews:
- route 2 has two insertion gates: the archive fill, and the backfill's first call returning non-null;
- "empty" means only a zero first byte;
- `esi` must survive the ABI across eight calls;
- the rebind writes nothing to the object before the resolver;
- "previous value" is the value at rebind entry, which can be a constructor's 0.

The reviews keep these narrowings:
- the out-key re-read after the lock;
- the `.pdata` wording;
- the constructors' differing resolver flag;
- the resolver-internal write check, which supports the result but does not prove it;
- the boundary convention for "disjoint".

## Consumer check (FABLE)

affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

- consumer: this page: revised-here (new section 5b; sections 5 and 5a unchanged).
- consumer: the stream source-record ABI: OPUS's, per the packet's plan; not edited here.
- consumer: ASTRA's two packets: agrees, narrowed as the reviews state.

run: `rv_route2.py` at f348f2f1d (72 PASS, 0 FAIL, 13 controls) - [script](../fable-review-astra-filecache-route2-commit-key-1002/rv_route2.py)
run: `rv_srckey.py` at f348f2f1d (56 PASS, 0 FAIL, 14 controls) - [script](../fable-review-astra-filecache-source-key-initialization-1002/rv_srckey.py)
