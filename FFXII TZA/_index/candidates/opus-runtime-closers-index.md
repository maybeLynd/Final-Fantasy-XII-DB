# OPUS runtime closers: one index for adjudication (OPUS, 2026-09-25, block 329)

**Purpose.** Every L2 runtime cell below is MIXED / NOT MET / PARTIAL, and each one is waiting on per-invariant adjudication (the S-01 precedent: every invariant either live, or executed where no substitution can reach it). This index lists, for each gate row, the OPUS replay closers that exist, the contract items each one executes, and what stands in for anything not run. **It scores nothing.** Generated from the closers' own README tables and result.json by `Tools/work/OPUS/runtime_index.py`; open the closer for the evidence.

**Reading the columns.**
- *stubs*: `none` means the closer's README states that no application stub is used. Imports are bridged by name, and fixtures are planted data.
- *boundaries*: `yes` means the run ends at a recorded stop boundary somewhere. The boundary's arguments are recorded and nothing is substituted. The README names each one, and every contract item a boundary cuts off is listed under 'Not covered'.
- *cases*: passed / total from result.json, or `all (ok)` where the harness records one overall verdict. Every closer listed was run three times with identical result.json. Where passed is below total, the closer's README says why (for example, s02's five request ids that leave `00227680` and read a then-unbuilt singleton).

## S-02 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s02-opus-replay-26a5f0-and-reach` | 287 | `cd48d9875` | EXP-191's scripted leaves (disclosed); 0026A5F0 and 00227680 real | no | 61 / 66 |
| `s02-opus-replay-stop-reach-executed` | 331 | `5bde53415` | none | yes | all (ok) / 2 |
| `s02-opus-replay-world-tick-stub-free` | 318 | `3b6546f1c` | none | no | all (ok) / 7 |

`s02-opus-replay-26a5f0-and-reach`, contract items executed:
- **PASS**, no fault, no scripted `s26a5f0` call: `wt-latch-store-real`

`s02-opus-replay-stop-reach-executed`, contract items executed:
- SS-7: `SS7_reach_executed_all_28_slots`
- —: `slot0_record_depends_on_flag_bit3`

`s02-opus-replay-world-tick-stub-free`, contract items executed:
- the binding gap: `stub_free_all_modes`
- WT-1: `WT1_mode_consulted_at_five_sites`
- WT-2: `WT2_drain_before_mode`
- WT-3: `WT3_active_word_set_and_cleared`
- WT-4: `WT4_sentinels_and_unstaged_writes`
- WT-5: `WT5_loop_bounds_observed`

## S-04 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s04-opus-replay-validator-shipped` | 328 | `af48eb0a0` | none | yes | all (ok) / 4 |

`s04-opus-replay-validator-shipped`, contract items executed:
- —: `bind_every_shipped_slot`
- I2, §2: `arms_2_to_32_at_their_edges`
- I2: `class1_redispatch_every_family`
- I2: `I2_validator_vs_inventory_count`

## S-06 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s06-opus-replay-console-arms` | 315 | `b4382c11e` | none | no | all (ok) / 7 |
| `s06-opus-replay-dispatcher` | 291 | `8f8d676ed` | none | no | 62 / 62 |

`s06-opus-replay-console-arms`, contract items executed:
- I-1, I-3: `I1_I3_table_static`
- I-2: `I2_out_of_range_is_a_noop`
- I-3: `I3_shared_arm_does_nothing`
- I-1: `dispatch_selects_the_table_arm`
- I-4: `I4_float_steps_observed`
- postcondition: `postcondition_observed`

## S-08 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s08-opus-replay-queue-static-invariants` | 330 | `d90034fed` | none | yes | all (ok) / 4 |

`s08-opus-replay-queue-static-invariants`, contract items executed:
- I1: `I1_constructor_field_list`
- I4: `I4_counter_wrap_signed`
- I6: `I6_offset_truncates_toward_zero`
- I7: `I7_recycle_does_not_sanitize`

## S-11 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s11-opus-replay-environment-variant` | 352 | `c50c8cbaf` | none | yes | 4 / 4 |
| `s11-opus-replay-field-record-accessors` | 304 | `88d70591b` | none | no | 9 / 9 |
| `s11-opus-replay-trigger-points` | 317 | `f54ee4436` | none | no | all (ok) / 8 |

`s11-opus-replay-environment-variant`, contract items executed:
- EV-1: `EV1_tail_call_with_zero_arguments`
- EV-6: `EV6_only_DBC_is_pre_cleared`
- EV-6: `EV6_unloaded_table_keeps_stale_values`
- EV-5: `EV5_band_from_the_preset`

`s11-opus-replay-trigger-points`, contract items executed:
- TP-1: `TP1_threshold`
- **TP-2 — contradicted**: `TP2_height_is_ignored`
- TP-3: `TP3_75_25_from_the_draw`
- TP-4: `TP4_one_point_flag_and_bit`
- TP-4: `TP4_flag_FF_sets_none`
- TP-5: `TP5_32_point_ceiling`
- TP-6: `TP6_eligibility`
- not in the contract: `field_not_in_live_table`

## S-12 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s12-opus-replay-weather-apply` | 303 | `b1581cbac` | none | yes | 5 / 5 |
| `s12-opus-replay-weather-roll` | 339 | `966599ad6` | none | yes | all (ok) / 2 |

`s12-opus-replay-weather-apply`, contract items executed:
- the commit and the postcondition: `ungated-commit`
- **I-2**: `i2-saturation`
- the debug `+0xAAC` override (§3 table): `debug-override-forces-slot`
- **I-4 / I-5**: `i5-selector-bound-slot-unchecked`

`s12-opus-replay-weather-roll`, contract items executed:
- §12 roll / resolve / probability, I-1, I-2: `roll_matches_the_contract_model`
- §12: `override_and_unloaded_script`

## S-14 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s14-opus-replay-enemy-install` | 343 | `b5fbc51cd` | none | yes | all (ok) / 5 |
| `s14-opus-replay-installer-stub-free` | 333 | `646c16a9a` | none | yes | all (ok) / 5 |

`s14-opus-replay-enemy-install`, contract items executed:
- `41ac8746…bcd992`: `rsn_b.ard`
- `c778e09a…eeabbd`: `bhm_c.ard`
- I1, I4, §3: `I1_I4_enemy_install_every_definition`
- I8: `I8_class1_float_from_byte_27`
- I5: `I5_row_bound_is_the_shipped_count`
- I6: `I6_freshness_gate`
- I7: `I7_tracked_registration_needs_a_code`
- spawn initializer: `byte[spawn]`

`s14-opus-replay-installer-stub-free`, contract items executed:
- I4, I8, §2: `I4_I8_party_install`
- I2: `I2_reset_then_master_reject`
- I1, I3: `I1_other_class_clears_bit26`
- I3: `I3_rekey_selection`
- I7: `I7_party_path_registers_nothing`

## S-18 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s18-opus-replay-delta-and-position` | 307 | `c7aa7c097` | none | no | 5 / 5 |
| `s18-opus-replay-facing-and-steering` | 308 | `8b01d6499` | none | yes | 9 / 9 |
| `s18-opus-replay-turn-limiter` | 307 | `c7aa7c097` | none | no | 2 / 2 |

`s18-opus-replay-delta-and-position`, contract items executed:
- LD-1, LD-3, LD-5: `delta_class_gate_LD1_LD3_LD5`
- LD-4, LD-6, the `+0xF8` repair: `delta_spherical_LD4_LD6_grid`
- LD-4's scope (page §4): `delta_planar_branch`
- not in the contract (page §8): `delta_vector_arm_r8_nonzero`
- LD-2: `getpos_LD2`

`s18-opus-replay-facing-and-steering`, contract items executed:
- 256 selector values: `select_slot_00269F90`
- 8 kinds × 3 headings × 4 entries: `facing_kind_dispatch`
- 4,103 headings in [−8, 8] plus crossings: `rewrap_idempotent`
- 4: `kind3_steering_record_write`
- 10: `ED2_commit_block_003EC260`
- 8 kinds × 7 modes × 3 enables: `set_steering_mode_0026AE90`
- 31: `set_movement_mode_0026C120`
- 18: `push_pop_002EAB80_002EAAA0`
- 5: `normalise_loop_003A1C50`

## S-19 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s19-opus-replay-separation-pass` | 337 | `086170ce3` | none | yes | all (ok) / 8 |

`s19-opus-replay-separation-pass`, contract items executed:
- P-2: `P2_each_pair_once`
- P-5: `P5_order_dependent`
- P-1: `P1_unregistered_not_active`
- P-3: `P3_remembered_pairs_visited_only_under_candidates`
- P-4: `P4_mode_selects_active_test`
- P-4: `P4_layer_and_owner_refusals`
- P-7: `P7_three_weight_outcomes`
- P-6: `P6_clear_extent`

## S-20 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s20-opus-replay-combo-roll` | 346 | `8137f350d` | none | yes | all (ok) / 4 |
| `s20-opus-replay-command-seam` | 351 | `2d4796ba5` | see README | yes | all (ok) / 4 |
| `s20-opus-replay-handler-table` | 350 | `42b704ca4` | see README | yes | all (ok) / 4 |

`s20-opus-replay-combo-roll`, contract items executed:
- CB-3, §12: `CB3_first_hit_draws_twelve_not_two`
- CB-3 (new detail): `CB3_count_rises_as_hp_falls`
- CB-4, §12: `CB4_progress_against_the_nibble`
- CB-5: `CB5_foe_record_table_and_cap`

`s20-opus-replay-command-seam`, contract items executed:
- CS-1: `CS1_seam_records_pending_not_commit`
- CS-1: `CS1_seam_refusals`
- CS-2: `CS2_commit_writes_the_three_fields`
- CS-5: `CS5_dispatch_reads_the_committed_id`

`s20-opus-replay-handler-table`, contract items executed:
- HT-1, HT-2: `HT1_HT2_table_shape`
- HT-3, HT-5: `HT3_HT5_tail_call_and_minus_one`
- HT-6: `HT6_event_before_dispatch`
- HT-4: `HT4_one_table_one_bound`

## S-21 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s21-opus-replay-385ba0` | 288 | `6f1c17e98` | EXP-149's stub table with per-case real bodies; 0031B860 scripted (disclosed) | no | all (ok) / 39 |
| `s21-opus-replay-applier-stub-free` | 332 | `5a18dee69` | none | yes | all (ok) / 4 |

`s21-opus-replay-385ba0`, contract items executed:
- **real**: `ap-steal-meta-real`
- scripted: `ap-steal-empty-meta-scripted`
- **real**: `ap-steal-empty-meta-real`

`s21-opus-replay-applier-stub-free`, contract items executed:
- I2: `I2_copy_through_without_masks`
- I1, I3: `I1_I3_apply_bit_mode3_and_outer_recompute`
- I1: `I1_remove_bit_mode0`
- I5, I6, I7: `I5_I6_I7_numeric_dispatch`

## S-22 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s22-opus-replay-recipe-resolver` | 316 | `4dd18c437` | none | no | all (ok) / 5 |
| `s22-opus-replay-steps-and-element-scaling` | 311 | `03456103d` | none | no | 9 / 9 |

`s22-opus-replay-recipe-resolver`, contract items executed:
- RW-1: `RW1_table_extent_static`
- RW-2, RW-4 (§12): `RW2_RW4_static`
- RW-2: `RW2_committed_list_only`
- not in the contract: `loop_early_exit_observed`

`s22-opus-replay-steps-and-element-scaling`, contract items executed:
- §12 (read from the mapped image): `ST1_ST2_ST3_ST5_table_static`
- ST-3: `ST3_noops_execute_and_write_nothing`
- ST-4, ST-7: `ST4_ST7_recipe_65_113`
- ST-4: `ST4_finalize_reads_only_the_scratch`
- ST-4: `ST4_order_is_the_semantics`
- ST-5: `ST5_double_finalize`
- (observed): `finalize_arms_observed`
- WE-4, WE-5, §12: `WE4_WE5_bit16_skips_the_stage`
- WE-2, WE-6: `WE2_WE6_rule_table`

## S-23 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s23-opus-replay-hp-second-store` | 334 | `2d28b72fd` | none | yes | all (ok) / 3 |

`s23-opus-replay-hp-second-store`, contract items executed:
- §4 postcondition / invariant (corrected): `second_store_on_the_lethal_path`
- §4: `single_store_without_a_status_transition`
- §4 invariant: `bound_holds_after_every_store`

## S-24 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s24-opus-replay-stat-derivation` | 342 | `74696a97f` | none | yes | all (ok) / 7 |

`s24-opus-replay-stat-derivation`, contract items executed:
- `41ac8746…bcd992`: `rsn_b.ard`
- `7957c1b9…003e34`: `rwf_d.ard`
- D-1: `D1_two_disjoint_sources`
- D-2, §10, §12: `D2_every_output_inside_its_cap`
- D-3, §11: `D3_one_cmove_picks_the_cap`
- D-4, §12: `D4_second_write_of_the_same_slot`
- D-2, §10: `growth_input_wraps_to_the_floor`
- D-5, §12: `D5_either_layer_pays_the_bonus`
- D-7: `D7_tail_behind_three_guards`

## S-25 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s25-opus-replay-enmity` | 345 | `8769914e9` | none | yes | all (ok) / 8 |

`s25-opus-replay-enmity`, contract items executed:
- E-4: `E4_three_parameters_third_negated`
- E-2: `E2_threat_is_stored_on_the_target`
- E-5: `E5_grudge_alone_does_not_propagate`
- E-5: `E5_propagation_needs_grudge_and_perception`
- (new): `first_grudge_seeds_the_vector`
- E-3: `E3_class_gates`
- E-8: `E8_suppression_gates_the_write`
- E-1, E-6, E-7: `E6_E7_decay_interval_and_step`

## S-26 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s26-opus-replay-effect-layers` | 341 | `49954e0c1` | none | yes | all (ok) / 9 |

`s26-opus-replay-effect-layers`, contract items executed:
- L-3: `L3_merge_is_the_or_of_both_layers`
- L-4: `L4_alias_bit_16`
- L-5: `L5_id15_revocation`
- §3, §5, §10: `L5_owner_global_written_by_the_merge`
- L-2: `L2_mutate_takes_the_layer_as_a_parameter`
- L-2, §10: `mutate_side_effects_key_on_the_merged_presence`
- L-1: `L1_rebuild_never_writes_the_mutable_layer`
- L-6, §12: `L6_rebuild_reconciles`
- L-6, §8: `foe_derived_layer_is_the_unit_E80_bitmap`

## S-27 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s27-opus-replay-periodic-builder` | 310 | `d7bd335d8` | none | no | 6 / 6 |
| `s27-opus-replay-periodic-tick-entry` | 320 | `19fc4b8e7` | none | no | all (ok) / 4 |

`s27-opus-replay-periodic-builder`, contract items executed:
- I-2, I-5, §12 "no stage wrote the unit": `A_order_and_empty_ownership`
- §3 effect-slot family, I-6, §10: `B_stage3_effect_slots`
- (observed): `C_five_expiries_list_bound`
- §3 status-word family, §9, I-7: `D_stage2_beat_and_regen`
- §9 phase, §10 fallback, I-7: `F_stage4_drain_modes`
- I-5: `E_I5_no_stage_calls_another`

`s27-opus-replay-periodic-tick-entry`, contract items executed:
- §2, §7: `full_tick_stub_free`
- I-1: `I1_deadline_between_gate1_and_gate2`
- §4 gates: `gates_refuse_the_builder`
- block 310's finding: `sink_commits_the_beat`

## S-28 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s28-opus-replay-five-slot-maps` | 338 | `72d6d5146` | none | yes | all (ok) / 3 |
| `s28-opus-replay-slot-map-writers` | 340 | `cb7dbbc88` | none | yes | all (ok) / 2 |

`s28-opus-replay-five-slot-maps`, contract items executed:
- SM-4, SM-8: `SM4_SM8_born_identical`
- SM-5: `SM5_refresh_order`
- SM-1, SM-2, SM-3: `SM1_SM2_SM3_resolver`
- BS-1, BS-2: `BS1_BS2_binder_arms`
- BS-3, BS-5: `BS3_BS5_reset_leaves`
- the invariant, §4: `writer_keeps_its_own_side_only`
- §4 exception, §7: `bulk_clears_break_it`
- §2: `readers`
- §2: `leader_derived`
- PF-3: `PF3_deferred_until_commit`
- PF-4: `PF4_redundant_commit_still_pushes`
- PF-5, PF-6: `PF5_PF6_order_and_the_summon_call`
- PF-7: `PF7_bit14_raises_0_and_2_only`
- PF-8: `PF8_null_stats_faults_mid_function`

`s28-opus-replay-slot-map-writers`, contract items executed:
- SM-7, SM-6: `SM7_removal_refreshes_all_five`
- SM-7's range check: `SM7_range_and_absence_refused`

## S-29 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s29-opus-replay-equipment-eligibility` | 323 | `4ac0ac73b` | none | yes | all (ok) / 9 |

`s29-opus-replay-equipment-eligibility`, contract items executed:
- EQ-1, §12: `EQ1_partner_test_asymmetric`
- EQ-2: `EQ2_shield_exempt_only_inline`
- EQ-3: `EQ3_packed_slot_and_exemption`
- EQ-5, §12: `EQ5_forbidden_mask`
- EQ-6, §12: `EQ6_selector_and_index_bypass`
- EQ-7: `EQ7_two_classes_one_range`
- §16a: `wrapper_owned_test_always_on`
- EQ-8, EQ-4: `EQ8_EQ4_recommender_order`
- EQ-8: `EQ8b_empty_main_forced_then_offhand_dropped`

## S-30 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s30-opus-replay-shop-ladders` | 324 | `3766a546b` | none | yes | all (ok) / 10 |

`s30-opus-replay-shop-ladders`, contract items executed:
- §3, the page's corpus: `bind_shipped_table`
- SG-2: `SG2_every_row_gate_matches_model`
- SG-1: `SG1_one_gate_then_pointer_walk`
- SG-6, §14: `SG6_rank_floor_row2_not_all_gated`
- §10: `S10_negative_operand_fails_threshold_0`
- SG-4: `SG4_kind1_kind2_one_argument`
- SG-5: `SG5_unknown_kind_skipped`
- SG-5, §12: `SG5b_unknown_kind_listed_when_above`
- SG-7: `SG7_bound_not_snapshotted`
- SG-2, SG-3: `SG2b_SG3_null_section_and_null_data`

## S-31 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s31-opus-replay-licence-check-shipped` | 326 | `ae05328ab` | none | yes | all (ok) / 6 |

`s31-opus-replay-licence-check-shipped`, contract items executed:
- §3, §15: `bind_shipped_tables`
- §13's builder: `builder_every_ability_matches_model`
- I3: `I3_escape_bit_census`
- I4: `I4_any_single_square`
- I5, §10, §14: `I5_quickenings_counted_over_shipped_rows`
- §14: `licence_records_0_17`

## S-32 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s32-opus-replay-defeat-rewards` | 344 | `ff77d13d2` | see README | yes | all (ok) / 6 |
| `s32-opus-replay-gil-storage` | 347 | `e7a1ef7e2` | none | yes | all (ok) / 8 |
| `s32-opus-replay-level-advance` | 348 | `50f15d044` | see README | yes | all (ok) / 5 |
| `s32-opus-replay-loot-rolls` | 349 | `572e349b9` | none | yes | all (ok) / 6 |

`s32-opus-replay-defeat-rewards`, contract items executed:
- `f52f5dd2…ac9b5d`: `bds_a.ard`
- `41ac8746…bcd992`: `rsn_b.ard`
- DR-1: `DR1_order_to_the_return`
- DR-2: `DR2_null_recipient_calls`
- DR-3: `DR3_level_walk_is_a_search`
- DR-4: `DR4_gil_reads_the_defeated_units_span`
- DR-5: `DR5_status12_converts_lp_to_gil`
- DR-6: `DR6_report_exceeds_stored_gain`

`s32-opus-replay-gil-storage`, contract items executed:
- GL-1: `GL1_clamp_in_the_setter`
- GL-2, GL-4: `GL2_GL4_meter_kind_and_zero_delta`
- GL-3: `GL3_delta_before_clamp`
- GL-2: `GL2_console_writer_is_metered`
- GL-5: `GL5_two_getter_entries`
- GL-2, GL-4 (new edge): `delta_wraps_to_a_metered_gain`
- (the meter): `meter_counters_accumulate_and_saturate`
- (the meter): `meter_counters_observed`

`s32-opus-replay-level-advance`, contract items executed:
- LU-3: `LU3_three_cadences`
- LU-8: `LU8_growth_is_rolled`
- LU-4: `LU4_nonzero_kind_bare_increment`
- LU-1, LU-2: `LU1_LU2_cap_and_monotonic`
- LU-7: `LU7_poster_runs_without_an_owner`

`s32-opus-replay-loot-rolls`, contract items executed:
- LC-1, LC-2, LC-3: `LC1_LC3_one_stream_three_steps`
- LC-4: `LC4_variable_draws`
- LC-7: `LC7_prefill_and_bucket_plus_one`
- (new): `merge_duplicate_slots`
- LC-6: `LC6_rank_is_the_default_profile`
- LC-4 (extras): `extras_not_reached`

## S-34 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s34-opus-replay-six-entries` | 306 | `c3292bbba` | none | no | 6 / 6 |

## S-36 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s36-opus-replay-request-router` | 327 | `5b427aace` | none | yes | all (ok) / 8 |
| `s36-opus-replay-widget-ctor` | 298 | `2bd7e6560` | none on 002465F0's path; memset bridged | no | 5 / 5 |

`s36-opus-replay-request-router`, contract items executed:
- R-a, §4: `Ra_latch_before_policy`
- R-b, §4: `Rb_policy_bit_table`
- R-c, R-3, R-6: `Rc_R3_busy_root_refuses_after_dispatch`
- R-3, R-6, §3: `R3_R6_accepted_request`
- R-6: `R6_prelude_audio_split`
- R-1, §5: `R1_single_slot_silent_replace`
- R-2: `R2_post_policy_narrower`
- §5: `R1b_blocked_byte_refuses`

`s36-opus-replay-widget-ctor`, contract items executed:
- a null handler becomes the default; `self[0] != NULL`: `null-handler-default`
- precondition: `memset`s all `size` bytes: `null-handler-default`
- "both left zero when the argument is NULL": `handler-null-locals-zero-payload`
- the stack flag's bit 0 → `+0x40` bit 14: `flag-bit14`
- (measurement): `small-size-measurement`

## S-37 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s37-opus-replay-text-interpreter` | 313 | `957305e5f` | none | no | 6 / 6 |

`s37-opus-replay-text-interpreter`, contract items executed:
- I-1, I-7: `A_ordinary_bytes_I1_I7`
- §2 return semantics: `B_end_of_run`
- I-1: `C_lead_tokens_observed`
- I-3, I-6: `D_escape_selectors_I3_I6`
- I-2: `E_parsers_I2`
- §3 DynGeo layout: `F_dyngeo_draw_layout`

## S-38 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s38-opus-replay-render-object` | 353 | `` | none | yes | all (ok) / 6 |

`s38-opus-replay-render-object`, contract items executed:
- R-2, R-3: `R2_R3_construct`
- R-7: `R7_clear_latch_publishes_nothing`
- R-5: `R5_selector_picks_one_bank`
- R-6: `R6_publish_has_no_loops`
- R-1: `R1_one_size_both_ends`
- R-2: `R2_teardown_vtable_chain`

## S-39 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s39-opus-replay-command-lists` | 312 | `e8b57cf11` | none | no | 7 / 7 |

`s39-opus-replay-command-lists`, contract items executed:
- §3, I-3: `A_construction`
- I-1, I-9: `B_enqueue_both_lists`
- I-4, I-5, I-7, §2: `C_walks_I4_I5_I7`
- I-8, I-1: `D_marks_and_clear_I8_I1`
- I-1: `E_owner_destroys_I1`
- I-6: `F_flush_I6`
- I-10: `G_handshake_I10`

## S-42 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s42-opus-replay-music-control` | 325 | `96c76b21d` | none | yes | all (ok) / 9 |

`s42-opus-replay-music-control`, contract items executed:
- MC-4, MC-5: `MC4_MC5_trampoline_then_rebase`
- the field-music reader, after MC-5: `reader_over_rebased_shipped_file`
- MC-5: `MC5_zero_stays_zero_twice_doubles`
- MC-5: `MC5_address_limits`
- MC-4: `MC4_sign_extended_target`
- MC-6: `MC6_checker_bounded_to_one`
- MC-7: `MC7_ring_clamped_to_file`
- MC-7: `MC7_pieces_and_ring_cursor`
- MC-8: `MC8_play_pair`

## S-43 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s43-opus-replay-save-image-pipeline` | 335 | `66b750fb7` | none | yes | all (ok) / 5 |

`s43-opus-replay-save-image-pipeline`, contract items executed:
- SV-1: `SV1_getters_and_spacing`
- SV-2: `SV2_copies_complete_with_tail`
- SV-6: `SV6_selector_first_then_copy_then_writer`
- SV-4: `SV4_backup_unread_by_the_family`
- SV-5: `SV5_two_clears`

## S-46 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s46-opus-replay-area-seed` | 336 | `68f4b9e25` | none | yes | all (ok) / 2 |

`s46-opus-replay-area-seed`, contract items executed:
- I4, §7: `I4_area_count_seeding`
- I4, §9: `I4_same_count_same_stream`

## S-47 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s47-opus-replay-24ed80` | 289 | `86c611a64` | none on the 0024ED80 path; EXP-084's other cases as they were | no | 53 / 53 |

## S-48 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s48-opus-replay-ramp-channels` | 321 | `1a11429d6` | none | no | all (ok) / 8 |

`s48-opus-replay-ramp-channels`, contract items executed:
- entry: `reset_003B6890`
- §4.1: `P1_identity_guard_writes_nothing`
- §4.2: `P2_steps_zero_is_immediate`
- §4.4: `P4_paused_does_not_accumulate`
- §4.5: `P5_byte_counter`
- §2, §3: `S2_S3_channel_layout`

## S-50 - OPUS closers

| closer | block | commit | stubs | boundaries | cases |
|---|---|---|---|---|---|
| `s50-opus-replay-lua-loader` | 322 | `7946042f2` | none | yes | all (ok) / 3 |

`s50-opus-replay-lua-loader`, contract items executed:
- §4 PRE, §3.2, §12: `PRE_and_marshalling_00683C30`
- §4 I1, I2; §7: `I1_I2_fork_and_mode_guards`
- §4 I3, §3.1, §10: `I3_header_18_compared_17_read`
