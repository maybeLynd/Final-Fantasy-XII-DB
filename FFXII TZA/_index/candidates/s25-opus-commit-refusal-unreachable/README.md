# S-25: a matched gambit line is never refused by the commit, over the shipped action table (OPUS, 2026-09-26)

**Evidence classes: STATIC (T1–T3) and NATIVE-REPLAY (D1–D3), `live_game: false`.**

**The question.** `CONTRACT-gambit-walk.md` §7 (FABLE's qualification, 2026-09-25) left one thing open: *"Whether the unit
arm or the slot combiner can still make a real commit refuse is open"*. AUDIT-SEM's in-progress S-25 cell names it as the
runtime residual (*"real commit refusal reachability (§7 open)"*).

**The commit refuses only outside its two bands,** `0`–`0x21E` and `0x4000`–`0x4166`. `check.py` shows that every action id
the evaluator lets through lies inside one of them. It runs over block 332's world (`../s21-opus-replay-applier-stub-free/`),
where `battle_pack` is bound by shipped code; that world's `result.json` keeps md5 `baf273ee…`.

**6 / 6 pass; `result.json` is byte-identical over two runs (md5 `23f16575…`).**

| case | observed |
|---|---|
| `T1_one_success_exit_one_out_writer_walk_slot_only_to_the_evaluator` | the evaluator `003014C0` has **one** success exit (`003017E9`), and its action slot has **one** writer, the decode at `00301500`. The walk writes its slot `[rsp+0x70]` only at `00305CD6` (the `0xFFFF` init). It passes the slot only to the evaluator (`00305DCA`) and reads it for the commit (`00305DE3`) and the third call (`00305E44`) |
| `T2_two_arms_condition_band_and_availability` | the success exit is reached through one of two arms. The **condition arm** is `003015CE`/`003015D2`, taken when `id − 0x4000 ≤ 0x166`, and leads to `00301830`. The **unit arm** calls `002FFCF0`, which must return 0 (`00301604` / `00301606`) |
| `T3_commit_returns_0_only_from_the_band_test` | the commit `0030F760` has one return-0 site, `0030F981`, and its one branch source is `0030F7EC`, the band test |
| `D1_class20_is_exactly_0_to_21E` | `00322C50(20, id)` accepts exactly **`0`–`0x21E`** over `0`–`0x7FFF`. The action table `[02EBF138]` has **543 rows** |
| `D2_availability_refuses_ids_outside_class20_with_reason_4` | on an eligible unit, `002FFCF0` returns **4** for `0x21F`, `0x3FFF`, `0x4167` and `0x7FFF`, before any target selector. It returns 0 for `0x96` (Attack) |
| `D3_the_commit_band_is_real` | control: the commit called directly refuses `0x21F` and `0x4167` (returns 0) and accepts `0x21E` and `0x4166` |

**Reading.** The unit arm admits exactly the commit's first band, because class 20's range is the table's row count. The
condition arm admits exactly its second band. The action id the commit receives is the one the evaluator decoded. So a
satisfied condition always commits.

**The bound is the table's.** A `battle_pack` whose action table had more than `0x21F` rows would let the unit arm pass
ids the commit refuses. The shipped one does not. The contract's §7 records the answer.
