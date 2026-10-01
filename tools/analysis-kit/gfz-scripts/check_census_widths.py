"""Cross-check every declared field width against its own access census.

Three artefact classes make a census say a width it does not mean, and all three were
found the hard way while populating the store:

  * multi-byte NOPs -- `nop dword ptr [rax + rax]` pads with a ModRM memory operand and
    touches nothing, but reads as a 4-byte access. 48 rows across the eight censuses.
  * unrolled SIMD block copies -- a function moving a region emits a run of `movups
    xmmword`, none of which is a 16-byte field. This one corrupted a published layout
    twice before it was recognised.
  * indexed accesses with no displacement -- `[rcx + rax*8]` is filed at +0x000 though
    it is an array element reached through the base.

This excludes all three and reports every declared row whose size no longer matches.
A row declared as an ARRAY or a whole SPAN is expected to disagree with its element
width, so those are listed separately rather than as findings.

WHY THERE IS A COVERAGE VERDICT AS WELL AS A MISMATCH COUNT
-----------------------------------------------------------
ASTRA ran five isolated fixtures against a byte-stable snapshot of this checker and found
that three of them print "0 disagreements" and exit 0 without performing a single
comparison: a declaration whose census is missing, a malformed-only census, and no
declarations at all. The defect was one line - a row with no applicable census access was
`continue`d, indistinguishably from a row that had been checked and agreed.

That is the same fault the store hit from the other side the same day. OPUS-CONTRA-SAVENEST
found twelve offsets carrying two different widths in two types while this tool reported
zero disagreements, because it compares each type against its OWN census and is silent
about everything it never compared. A green light that means "nothing was compared" is
worse than a red one, and it was being read as a gate.

So the mismatch count is no longer the whole verdict. Every declared row is now accounted
for as CHECKED or as unchecked with a reason, malformed input is counted rather than
skipped, and the exit code separates the three outcomes:

    0  at least one comparison was performed and none disagreed
    1  a declared width disagrees with its cleaned census   (unchanged)
    2  nothing was proved: zero comparisons were performed

Partial coverage is NOT an error and must not be, or the check stays permanently red and
nobody reads it: eleven types have a census and the store has 223. Partial coverage is
reported as a number, which is the honest form.

THREE CENSUS SHAPES, BECAUSE A RECORD CAN BE REACHED THREE WAYS
---------------------------------------------------------------
Ten censuses are keyed by DISPLACEMENT, which is what a type reached through a pointer
gives you. A static block is reached by absolute address - `mov dword ptr [rip + 0x27695f6],
eax` names 02AEDFB8 outright - so its catalogue is keyed by address and carries a different
header. Every displacement-keyed checker skipped it for that reason and said nothing, so
BattleFormulaScratch had 912 rows of access evidence and 44 declared widths that had never
been compared to anything - in the type this store had already called its most completely
recovered. The address minus the base IS the displacement; once computed, the same
comparison applies. Its header is validated rather than assumed, and the rejection is
exercised by a fixture: this is the third schema in the kit and two earlier tools mis-parsed
a census by trusting column positions.

The third shape is a SUB-OBJECT that lives inside another type's census. `ImageBackedStateBlock`
is `SaveImage_GetActiveBuffer() + 0x8200` and the save-payload census is keyed to buffer+0x200,
so every one of its field offsets appears in that file at offset + 0x8000 - verified on six
independent sites on 2026-09-13 (+0x28 -> 0x8028, +0x30 -> 0x8030, +0x90 -> 0x8090,
+0x224 -> 0x8224, +0x3244 -> 0xB244, +0x32C4 -> 0xB2C4) and confirmed against the pointer's only
writer at 00253990, which stores getActiveBuffer() + 0x8200. Its twenty declared rows had never
been compared to anything, and registering it naively - same file, no shift - made all twenty
read as `census has no access at that displacement`, which is how the relationship was found.

    check_census_widths.py [--self-test]
"""
import collections
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

NOP = re.compile(r"^\s*nop\b", re.I)
INDEXED = re.compile(r"\[\s*\w+\s*\+\s*\w+\s*\*\s*[1248]\s*\]")
FORMS = (("xmmword", 16), ("qword ptr", 8), ("dword ptr", 4), ("byte ptr", 1))

CENSUS = {
    "SaveImageHeader": "save-header-accesses.tsv",
    "SpawnRecord": "spawn-record-accesses.tsv",
    "CharacterRenderRecord": "character-render-record-accesses.tsv",
    # Added 2026-09-13. The first census in this table that was GENERATED rather than
    # hand-built: record_field_scan.py --chain 0xB8,0xF0 with a mandatory control, emitting
    # the per-access format directly. SteeringRecord is reached only through a pointer
    # chain, so no displacement scan could see it and it had no census at all.
    "SteeringRecord": "steering-record-accesses.tsv",
    # Added 2026-09-13, the second generated census and the first STATIC one:
    # gen_static_census.py --base 0x02AEDFB8 --size 0xA8, controlled on six per-offset
    # access counts the field store had already recorded by hand (77, 43, 9, 6, 11, 7).
    "BattleFormulaScratch": "battle-formula-scratch-accesses.tsv",
    "CharacterRenderObject": "character-render-object-accesses.tsv",
    # Built 2026-09-11 by seeding the pool pointer at 022C6F28 with a NEGATIVE base offset
    # (--gptr 022C6F28:-48800), so a load of the pool yields "tail - 0x48800" and only accesses
    # at or above +0x48800 land in range; every record access falls out as a negative hit. The
    # control was the allocator's own capacity test, 004279B0 +0x0C.
    "CharacterRenderSystemTail": "character-render-system-tail-accesses.tsv",
    "SavePayload": "save-payload-accesses.tsv",
    "BattleUnit": "battle-unit-accesses.tsv",
    "ActorStorageRecord": "actor-storage-record-accesses.tsv",
    "ActorManagerSlot": "actor-manager-record-accesses.tsv",
    "BattleStatsRecord": "battle-stats-record-accesses.tsv",
    "BattleSystemState": "battle-state-block-accesses.tsv",
    "BattleResultRecord": "result-record-accesses.tsv",
    # RE-SEEDED 2026-09-19 (OPUS), and the caution that stood here for an afternoon is
    # withdrawn rather than left to rot. It read: 719 of 1,029 rows came from route
    # `chain:0xB8`, produced by a scan whose first hop matched ANY `mov RD, [RB+0xB8]` with no
    # constraint on RB - 410 functions in the image perform that load, 181 were admitted, only
    # 68 were Actor- or Movement-owned, and two PRESENTATION functions were why four declared
    # floats appeared to hold byte-level bitfield inserts.
    # THE REPAIR IS A COMPOSITION, not a new guess: the actor census already names functions
    # that take an ActorStorageRecord in arg0..arg3, WITH THE CALLER THAT PROVES IT, so the
    # context is taken as `[proven actor + 0xB8]` and the base is exactly as proven as that
    # claim and no more. 309 argument-proven rows kept verbatim, 719 chain rows replaced by 237
    # from 55 functions - Movement 42, unowned 9, ActorEntity 4, AND NOTHING FOREIGN.
    # IT COST COVERAGE AND THE COST IS STATED: of 101 displacements the old chain rows reached
    # from Actor- or Movement-owned functions, 56 survive and 45 do not, because those
    # functions are not in the actor census's argument-proven set. Those rows are now UNCHECKED
    # rather than wrongly checked, which is the trade this kit prefers. Total 1,028 -> 546 rows
    # and this gate's CHECKED count 1,393 -> 1,379.
    # THE PROOF THE REPAIR WORKED is not the row count: check_interior_offsets.py went from 16
    # leads to 12, and the four that vanished are exactly MovementContext's declared floats.
    # Regenerate with gen_movement_context_census.py, which carries both controls.
    "MovementContext": "movement-context-accesses.tsv",
    "SecondaryContext": "secondary-context-accesses.tsv",
    # Built 2026-09-11 from the 43 functions that load the block pointer at 01F82D20, with the
    # ROUTE tracked rather than assumed: a register is tainted by `mov reg,[01F82D20]`, cleared
    # the moment anything else writes it or a call intervenes, and only accesses through a
    # tainted register are recorded. Matching displacements without that tracking was measured
    # at roughly half background, so the route column here is a real claim, not decoration.
    "GameSettingConfig": "game-setting-config-accesses.tsv",
    # Wired 2026-09-13 (OPUS). This census FILE already existed and was the only one in the
    # tree that no map entry named, so its rows sat unread for the same reason the static
    # catalogue above did: not because the evidence was missing, but because nothing pointed
    # at it. Found by comparing the declared maps against the *-accesses.tsv files on disk.
    "EvaluationContext": "evaluation-context-accesses.tsv",
    # Built 2026-09-17 by work/SWE2-STRUCT/uq233_census.py: the 41 bodies that call the
    # lazy allocator 00193D50 or load the 01F7F5F0/01F81300 globals, PLUS every callee that
    # receives the context in an argument register or stack-argument slot (the blind spot
    # FABLE named in the handoff), PLUS the ctor 0018CD90 chain seeded at arg0. lea-formed
    # subobject pointers carry a base delta so +0x378/+0x3F0/+0x418 interiors attribute
    # correctly. Control: 00194250's five DOF writes (+0x110..+0x120) must appear.
    "PostProcessParamContext": "postprocess-context-accesses.tsv",
    # Built 2026-09-18 by work/SWE2-STRUCT/ts208_census.py: the four initialisers,
    # four dispatchers, five drawers and the draw helpers that receive the 0xD0
    # block in an argument register (rcx or r9), PLUS the three owner functions
    # that embed it (+0xC0/+0xD0/+0xE0), PLUS bodies that build it on their own
    # stack and copy it out (auto-detected memset destinations). Tags carry a
    # base delta so owner-relative and subobject-pointer accesses attribute
    # correctly; call-site backtracing is allowed only into the seed set or
    # through a proven embed-offset lea, which is what keeps memset and the
    # generic string utilities from contaminating the census. Control:
    # 002AE610's DOF-adjacent writes (+0x10..+0x1C) and the +0x98 digit-count
    # clamp must appear.
    "TextDrawState": "text-draw-state-accesses.tsv",
    # Added 2026-09-19 (OPUS). Ten types that had no census in this map, generated by
    # gen_ptr_census.py (the `*(void**)0xADDR` class the route grammar named and nothing
    # consumed) and gen_array_census.py (static ARRAYs reached through a register or a
    # folded-base RIP operand). Each is controlled differently and the provenance is in
    # `_types/README.md`; the route column of every row records which scan produced it.
    "ManagerSingleton0209BE80": "manager-singleton-0209be80-accesses.tsv",
    # Generated 2026-09-30 (SWE2-STRUCT) by gen_route_seeded_census.py on the declared route
    # `STATIC 0x0209AC60 | PTR 0x0209AC30`: 964 accesses at 146 offsets across 426 functions,
    # every base resolving to a declared row. The two shared-callee exposures the generator
    # flagged (002470D0 +0x308, 00280120 +0xC0, both 50+-caller helpers) land on declared
    # rows, not gaps, and carry `exposed` in their note column.
    "Manager0209AC60": "manager-0209ac60-accesses.tsv",
    # UNMEASURED-debt batch, same day, same tool (SWE2-STRUCT): every entry seeded from the
    # type's own declared `route` column; populations and exposure fractions are in each
    # file's header. Two PTR-seeded types produced EMPTY censuses (DeveloperConsoleSettings
    # - the cell is only loaded by the getter that publishes it - and TextPainter - the
    # static's fields are all reached through registers) and are deliberately NOT
    # registered: an empty file reads as a measured zero and these types are unmeasured,
    # not empty. Vp8DecoderInstance/Vp8MacroblockDecoder stay UNMEASURED - their CHAIN/
    # EMBED routes bottom out in VpxVp8DecoderContext, which has no seedable route.
    "ManagerSub0209AC60_02F8_00C0": "manager-sub-0209ac60-02f8-00c0-accesses.tsv",
    "ManagerSub8FA0SlotRecord02B8": "manager-sub-8fa0-slot-record-02b8-accesses.tsv",
    "ShadowSettings01F82EA8": "shadow-settings-01f82ea8-accesses.tsv",
    "CPostEffect": "cposteffect-accesses.tsv",
    "Vu1RegisterBank02064B00": "vu1-register-bank-02064b00-accesses.tsv",
    "BattleMenuChildRecord1E0": "battle-menu-child-record-1e0-accesses.tsv",
    "WidgetSingleton0208E6C0": "widget-singleton-0208e6c0-accesses.tsv",
    "WidgetSingleton0208E6D0": "widget-singleton-0208e6d0-accesses.tsv",
    "WidgetSingleton0208E6D8": "widget-singleton-0208e6d8-accesses.tsv",
    "WidgetSingleton0209C498": "widget-singleton-0209c498-accesses.tsv",
    "WidgetSingleton02CA99C0": "widget-singleton-02ca99c0-accesses.tsv",
    "Widget02CA6C80": "widget-02ca6c80-accesses.tsv",
    "Widget02CA9790": "widget-02ca9790-accesses.tsv",
    # Second route-seeded batch, same day, same tool (SWE2-STRUCT): the sweep showed zero
    # refuted gap rows across all 422 routed types, so these are registrations of measured
    # presence - every file's header carries its route and population.
    "AchievementState": "achievement-state-accesses.tsv",
    "ActiveLogWidget40C8": "active-log-widget-40c8-accesses.tsv",
    "ActorResourceEntry": "actor-resource-entry-accesses.tsv",
    "ActorWaitSlot": "actor-wait-slot-accesses.tsv",
    "AiOrderSet": "ai-order-set-accesses.tsv",
    "AudioParameterRamp": "audio-parameter-ramp-accesses.tsv",
    "AuthoredTableHeader": "authored-table-header-accesses.tsv",
    "AuthoredTableRegistrySlot": "authored-table-registry-slot-accesses.tsv",
    "AuthoredTriggerLiveEntry": "authored-trigger-live-entry-accesses.tsv",
    "AuthoredTriggerLiveSet": "authored-trigger-live-set-accesses.tsv",
    "BattleMenuChildBase4C0": "battle-menu-child-base-4c0-accesses.tsv",
    "BattleMenuPanelWidget3010Block": "battle-menu-panel-widget-3010b-lock-accesses.tsv",
    "BgmStream": "bgm-stream-accesses.tsv",
    "Category": "category-accesses.tsv",
    "DynGeoFontTextSpecialFinalInstance": "dyn-geo-font-text-special-final-instance-accesses.tsv",
    "DynGeoFontTextSpecialInstance": "dyn-geo-font-text-special-instance-accesses.tsv",
    "DynGeoFontTextSpecialShadowInstance": "dyn-geo-font-text-special-shadow-instance-accesses.tsv",
    "EastlPointerVector": "eastl-pointer-vector-accesses.tsv",
    "EeVu0RegisterBank": "ee-vu-0-register-bank-accesses.tsv",
    "EfxCallerTemplate": "efx-caller-template-accesses.tsv",
    "EncodedIdQueryRecord": "encoded-id-query-record-accesses.tsv",
    "FieldPendingRequestCells022C8030": "field-pending-request-cells-022c8030-accesses.tsv",
    "GameSettingKeyName": "game-setting-key-name-accesses.tsv",
    "GameSettingValueNameRow": "game-setting-value-name-row-accesses.tsv",
    "GlyphRunRecord14": "glyph-run-record-14-accesses.tsv",
    "GlyphRunWidget1498": "glyph-run-widget-1498-accesses.tsv",
    "GroupPersistentBank": "group-persistent-bank-accesses.tsv",
    "HandleSlotRecord": "handle-slot-record-accesses.tsv",
    "IndexedExternalSourceRequest": "indexed-external-source-request-accesses.tsv",
    "InputManager": "input-manager-accesses.tsv",
    "InputNameRegistryHeadCell": "input-name-registry-head-cell-accesses.tsv",
    "InputReservedBindingIds": "input-reserved-binding-ids-accesses.tsv",
    "LegacyPs2GsDerivedSlotRecord": "legacy-ps-2-gs-derived-slot-record-accesses.tsv",
    "LegacyPs2GsReferenceDescriptor": "legacy-ps-2-gs-reference-descriptor-accesses.tsv",
    "LegacyPs2GsSourceTextureRecord": "legacy-ps-2-gs-source-texture-record-accesses.tsv",
    "ManagerSub00A0Entry": "manager-sub-00a0e-ntry-accesses.tsv",
    "ManagerSub0209AC60_02F8": "manager-sub-0209ac60-02f8-accesses.tsv",
    "ManagerSub0209BE80_5380": "manager-sub-0209be80-5380-accesses.tsv",
    "ManagerSub0209BE80_57E0PairRecord": "manager-sub-0209be80-57e0-pair-record-accesses.tsv",
    "ManagerSub5380PoolAEntry": "manager-sub-5380-pool-a-entry-accesses.tsv",
    "ManagerSub5380PoolBEntry": "manager-sub-5380-pool-b-entry-accesses.tsv",
    "ManagerSub5380PoolCEntry": "manager-sub-5380-pool-c-entry-accesses.tsv",
    "ManagerSub7EA0Entry": "manager-sub-7ea0e-ntry-accesses.tsv",
    "ManagerSub7FB0Record": "manager-sub-7fb0-record-accesses.tsv",
    "ManagerSubA0D0Record": "manager-sub-0d0-record-accesses.tsv",
    "MapLightingTuning02CB7FD0": "map-lighting-tuning-02cb7fd0-accesses.tsv",
    "MapRefFieldRow": "map-ref-field-row-accesses.tsv",
    "MapRefImageHeader": "map-ref-image-header-accesses.tsv",
    "MapRefWeatherBlock": "map-ref-weather-block-accesses.tsv",
    "MapRefWeatherLane": "map-ref-weather-lane-accesses.tsv",
    "MapScreenContainer": "map-screen-container-accesses.tsv",
    "MapScreenPage": "map-screen-page-accesses.tsv",
    "MapScreenPageSlot": "map-screen-page-slot-accesses.tsv",
    "MovementBody": "movement-body-accesses.tsv",
    "NativeCommandFamilyTables": "native-command-family-tables-accesses.tsv",
    "NavBroadPhaseHeader": "nav-broad-phase-header-accesses.tsv",
    "NavMeshTriangle": "nav-mesh-triangle-accesses.tsv",
    "NavMeshVertex": "nav-mesh-vertex-accesses.tsv",
    "NavPortalRecord": "nav-portal-record-accesses.tsv",
    "NavRegionRecord": "nav-region-record-accesses.tsv",
    "NavRunStateBlock": "nav-run-state-block-accesses.tsv",
    "NavSlotPointerArray": "nav-slot-pointer-array-accesses.tsv",
    "OrderedCommandList": "ordered-command-list-accesses.tsv",
    "OrderedObject": "ordered-object-accesses.tsv",
    "PApplication": "p-application-accesses.tsv",
    "PAssetReferenceRegistry01F2EA70": "p-asset-reference-registry-01f2ea70-accesses.tsv",
    "PDeferredLightingBase": "p-deferred-lighting-base-accesses.tsv",
    "PDeferredLightingSlot0080": "p-deferred-lighting-slot-0080-accesses.tsv",
    "PNamedSemanticDescriptor": "p-named-semantic-descriptor-accesses.tsv",
    "PTypeDefaultUInt": "p-type-default-u-int-accesses.tsv",
    "PartyFormationSlot": "party-formation-slot-accesses.tsv",
    "PartySelectionRegistryPtrs022C8388": "party-selection-registry-ptrs-022c8388-accesses.tsv",
    "PersistentFlagPayload": "persistent-flag-payload-accesses.tsv",
    "PhyreClassDescriptor": "phyre-class-descriptor-accesses.tsv",
    "PpfxInitDescriptor": "ppfx-init-descriptor-accesses.tsv",
    "RampChannelRecord": "ramp-channel-record-accesses.tsv",
    "RenderCommandBuffer": "render-command-buffer-accesses.tsv",
    "RenderCommandBufferPair": "render-command-buffer-pair-accesses.tsv",
    "RenderCommandOwnerList": "render-command-owner-list-accesses.tsv",
    "RenderResourceEntryBuffer": "render-resource-entry-buffer-accesses.tsv",
    "RenderStrideC0Element": "render-stride-0e-lement-accesses.tsv",
    "ResourceKindOverrideTable": "resource-kind-override-table-accesses.tsv",
    "ResourceReadStatus": "resource-read-status-accesses.tsv",
    "ResourceSectionNameScratch": "resource-section-name-scratch-accesses.tsv",
    "SaveImage": "save-image-accesses.tsv",
    "SeparationCandidateScratch": "separation-candidate-scratch-accesses.tsv",
    "SeparationCellMasks": "separation-cell-masks-accesses.tsv",
    "StatusDefinitionRecord": "status-definition-record-accesses.tsv",
    "StickBasis022C7FA0": "stick-basis-022c7fa0-accesses.tsv",
    "StickWorldVector022C7FD0": "stick-world-vector-022c7fd0-accesses.tsv",
    "StorageByteStreamVector01F44D40": "storage-byte-stream-vector-01f44d40-accesses.tsv",
    "SummonEffectState02B40508": "summon-effect-state-02b40508-accesses.tsv",
    "SystemStopRecord": "system-stop-record-accesses.tsv",
    "SystemStopRegistry": "system-stop-registry-accesses.tsv",
    "TransformWorkbenchSavedPointer": "transform-workbench-saved-pointer-accesses.tsv",
    "TransformWorkbenchSavedValue": "transform-workbench-saved-value-accesses.tsv",
    "UiRootTable": "ui-root-table-accesses.tsv",
    "VmValueStack": "vm-value-stack-accesses.tsv",
    "Vu1ConstantVector01E02830": "vu-1c-onstant-vector-01e02830-accesses.tsv",
    "Vu1DataMemory02064E30": "vu-1da-ta-memory-02064e30-accesses.tsv",
    "Widget0209CC18": "widget-0209cc18-accesses.tsv",
    "Widget02B5F1F8": "widget-02b5f1f8-accesses.tsv",
    "Widget02B5F200": "widget-02b5f200-accesses.tsv",
    "Widget02CA9718": "widget-02ca9718-accesses.tsv",
    "WidgetConsumer02AEE4C8": "widget-consumer-02aee4c8-accesses.tsv",
    "WidgetFocusStack": "widget-focus-stack-accesses.tsv",
    "WidgetSingleton01FD4940": "widget-singleton-01fd4940-accesses.tsv",
    "WidgetSingleton01FD4948": "widget-singleton-01fd4948-accesses.tsv",
    "WidgetSingleton0208E6C8": "widget-singleton-0208e6c8-accesses.tsv",
    "WidgetSingleton020927F0": "widget-singleton-020927f0-accesses.tsv",
    "WidgetSingleton0209AC18": "widget-singleton-0209ac18-accesses.tsv",
    "WidgetSingleton0209AC20": "widget-singleton-0209ac20-accesses.tsv",
    "WidgetSingleton0209C300": "widget-singleton-0209c300-accesses.tsv",
    "WidgetSingleton0209C318": "widget-singleton-0209c318-accesses.tsv",
    "WidgetSingleton0209C380": "widget-singleton-0209c380-accesses.tsv",
    "WidgetSingleton0209C4C8": "widget-singleton-0209c4c8-accesses.tsv",
    "WidgetSingleton0209E5F8": "widget-singleton-0209e5f8-accesses.tsv",
    "WidgetSingleton0209E600": "widget-singleton-0209e600-accesses.tsv",
    "WidgetSingleton022C83E0": "widget-singleton-022c83e0-accesses.tsv",
    "WidgetSingleton022CA428": "widget-singleton-022ca428-accesses.tsv",
    "WidgetSingleton022CBE20": "widget-singleton-022cbe20-accesses.tsv",
    "WidgetSingleton02AED490": "widget-singleton-02aed490-accesses.tsv",
    "WidgetSingleton02AED490EntryA": "widget-singleton-02aed490e-ntry-a-accesses.tsv",
    "WidgetSingleton02AED490EntryB": "widget-singleton-02aed490e-ntry-b-accesses.tsv",
    "WidgetSingleton02AEE4C0": "widget-singleton-02aee4c0-accesses.tsv",
    "WidgetSingleton02B457E0": "widget-singleton-02b457e0-accesses.tsv",
    "WidgetSingleton02B457E0Record": "widget-singleton-02b457e0-record-accesses.tsv",
    "WidgetSingleton02B476B0": "widget-singleton-02b476b0-accesses.tsv",
    "WidgetSingleton02B47730": "widget-singleton-02b47730-accesses.tsv",
    "WidgetSingleton02B47740": "widget-singleton-02b47740-accesses.tsv",
    "WidgetSingleton02B62D78": "widget-singleton-02b62d78-accesses.tsv",
    "WidgetSingleton02B62D80": "widget-singleton-02b62d80-accesses.tsv",
    "WidgetSingleton02B62D88": "widget-singleton-02b62d88-accesses.tsv",
    "WidgetSingleton02CA8F38": "widget-singleton-02ca8f38-accesses.tsv",
    "WidgetSingleton02CA96D8": "widget-singleton-02ca96d8-accesses.tsv",
    "WidgetSingleton02CA9738": "widget-singleton-02ca9738-accesses.tsv",
    "WidgetSingleton02CA99C0QueueEntry": "widget-singleton-02ca99c0-queue-entry-accesses.tsv",
    "WidgetSingleton02CA99C8": "widget-singleton-02ca99c8-accesses.tsv",
    "WidgetSingleton02CA99D0": "widget-singleton-02ca99d0-accesses.tsv",
    "WidgetSingleton02CA99D8": "widget-singleton-02ca99d8-accesses.tsv",
    "WidgetSingleton02CA99E0": "widget-singleton-02ca99e0-accesses.tsv",
    "WorldLootDropEntry": "world-loot-drop-entry-accesses.tsv",
    "WorldLootPresenceRecord": "world-loot-presence-record-accesses.tsv",

    "ImageBackedStateBlock": "image-backed-state-block-accesses.tsv",
    # REPLACED 2026-09-19 (OPUS), and this is a FOURTH shape of the missing-artifact class: not an
    # absent census, but the WRONG ONE registered. The file here was the slot-seeded scan, 5
    # accesses at 3 offsets, while eight of this type's rows cite gen_ptr_census_ctor.py - the
    # ALLOCATION-seeded tool, which sees the constructor a slot-seeded scan structurally cannot,
    # because every field the ctor writes is written before the pointer ever reaches the slot.
    # That tool had no --out, so its result could not become the file; the flag was added in the
    # same package and the census is now 249 accesses at 182 offsets from 7 functions. This
    # gate's CHECKED count went 1,429 -> 1,474 on this one type.
    # IT IMMEDIATELY FOUND TWO DISAGREEMENTS, which is what a census this much stronger is for,
    # and both are adjudicated on the rows: +0xD00 and +0xD08 declare float against a single
    # 8-wide access each, and the 8-wide is 00186CD0's `mov qword ptr [rsi+0xd00], r12` /
    # `[rsi+0xd08], r12` with r12 zeroed at 00186CEE - a 16-byte CLEAR of the four floats, each
    # of which has its own `movss` store from its own register at 00185D01/0A/13/1B.
    # CONTAMINATION CHECKED BEFORE REGISTERING: every contributing function has between 1 and 9
    # callers, so no shared helper supplies any of this. That check is not decoration - it is why
    # ManagerSingleton0209BE80's much larger route-seeded census was NOT registered the same day.
    "BootSingleton01F7F598": "boot-singleton-01f7f598-accesses.tsv",
    "WorldLootPickupNode": "world-loot-pickup-node-accesses.tsv",
    "PartyRosterSlots": "party-roster-slots-accesses.tsv",
    "AchievementDescriptor": "achievement-descriptor-accesses.tsv",
    "SpawnGroupLedger": "spawn-group-ledger-accesses.tsv",
    "InputBindingProfile": "input-binding-profile-accesses.tsv",
    "ActorSequenceDescriptor": "actor-sequence-descriptor-accesses.tsv",
    "ImageAddressArenaRecord": "image-address-arena-record-accesses.tsv",
    # Added 2026-09-20 (OPUS). The first ARRAY type censused after `parse_route` was wired to
    # `Census.stride` - 252 accesses at 45 offsets in 60 functions, where this type had no
    # artifact at all. It is in this map because two of its rows were CTYPE-WRONG in a way only
    # a width comparison catches: recordCountByKind and recordBaseByKind were single 8-byte rows
    # and are four 2-byte elements each, which 002679F0's cursor loop settles outright.
    "ActorManagerSlot": "actor-manager-slot-accesses.tsv",
    # Added 2026-09-20 (OPUS). Both censused ZERO until the walk learned to follow a pointer
    # passed as the FIFTH or SIXTH argument - on the stack. 00477EE0 hands both tables to the
    # generic 0051F9F0 that way, and every access to them happens inside that callee. Neither
    # gains a field here: the rows were already read by hand and cite the same init sites the
    # census now finds. What they gain is a checkable artifact where there was none.
    "ChunkedSlotBankEntry": "chunked-slot-bank-entry-accesses.tsv",
    "ChunkedSlotEntry": "chunked-slot-entry-accesses.tsv",
    # Added 2026-09-20 (OPUS) with the type itself. It was documented in game-application.md and
    # had no type row at all; it surfaced as the OWNER of every CharacterRenderObject. Its census
    # comes almost entirely from the constructor - the PTR route's only host is the getter
    # 001BDAB0, which touches no field - so this row is also the check that the `ctor` column
    # stays parseable.
    "PendingCompletionQueue01F81248": "pending-completion-queue-01f81248-accesses.tsv",
    # Added 2026-09-19 (OPUS), second pass: three more ARRAY types with no census in this map.
    # ItemClassDescriptor's census is the one that settled the rebase reading - 0030B6A0 tests an
    # authored offset, loads it as a dword and stores it as a qword into the slot beside it, three
    # times, which is the (offsetA/pointerA, offsetB/pointerB, offsetC/pointerC) shape the other
    # type declared over this same table.
    "ItemClassDescriptor": "item-class-descriptor-accesses.tsv",
    "InputBindingRecord": "input-binding-record-accesses.tsv",
    # Added 2026-09-19 (OPUS), third pass: thirteen EMBED children, PROJECTED from their parents'
    # censuses by project_embed_census.py rather than scanned. Every row is a parent row with the
    # embed offset subtracted; nothing is decoded and nothing is inferred, and each projection was
    # checked to land inside the child's declared size (13 of 13, 0 past the end).
    #
    # THESE ARE NOT INDEPENDENT EVIDENCE. If a parent census is wrong at a displacement, the child's
    # is wrong at the same one, and a width check passing on both has checked one fact twice. The
    # route column of every row records `embed <Parent>+0xOFF` so that can never be mistaken.
    "ActorManagerSlotEntry": "actor-manager-slot-entry-accesses.tsv",
    "BattleTargetBuffer": "battle-target-buffer-accesses.tsv",
    "BattleTargetResultEntry": "battle-target-result-entry-accesses.tsv",
    "GambitConfig": "gambit-config-accesses.tsv",
    "NavigationPathState": "navigation-path-state-accesses.tsv",
    "SecondaryContextElement": "secondary-context-element-accesses.tsv",
    "SpawnKeepImage": "spawn-keep-image-accesses.tsv",
    "ManagerSub0209BE80_00A0": "manager-sub-0209be80-00a0-accesses.tsv",
    "ManagerSub0209BE80_57E0": "manager-sub-0209be80-57e0-accesses.tsv",
    "ManagerSub0209BE80_7EA0": "manager-sub-0209be80-7ea0-accesses.tsv",
    "ManagerSub0209BE80_7FB0": "manager-sub-0209be80-7fb0-accesses.tsv",
    "ManagerSub0209BE80_8FA0": "manager-sub-0209be80-8fa0-accesses.tsv",
    "ManagerSub0209BE80_A0D0": "manager-sub-0209be80-a0d0-accesses.tsv",
    # Added 2026-09-19 (OPUS). The ninth sibling, and the only one project_embed_census.py could
    # not produce, because ITS ROUTE COLUMN WAS BLANK while its field rows recorded the
    # containment in prose ("RE-BASED from ManagerSingleton0209BE80 +0xAB30"). A fact the store
    # holds only as prose is one no instrument can act on. The route is now filled in, and it was
    # PROVEN before it was written rather than copied from the siblings: 00290CF0 holds the
    # parent in rbx, does `lea rcx,[rbx+0xAB30]` at 00290D96 and passes that to 00276650 at
    # 00290DC0 - the function the store already cites as defining this extent with
    # memset(obj, 0, 0x61F0). Two rows project, which is the same order as its siblings.
    # Same EMBED caution as the block below: this is the parent's evidence rebased, not
    # independent evidence, and the route column of each row says so.
    "ManagerSub0209BE80_AB30": "manager-sub-0209be80-ab30-accesses.tsv",
    # Added 2026-09-19 (OPUS). Its route was proven and blank (Resume 101) and even once filled
    # in the projection was EMPTY, because the thirteen-slot claim array is written entirely
    # inside a SWITCH ARM: 0028F000 loads the singleton, dispatches through a jump table at
    # `jmp rcx`, and only the arm at 0028F034 forms `parent + 0x57E0` and tail-calls the loop.
    # A block walk that follows direct branches never entered it, so 0x2220 bytes of the
    # store's largest type censused as zero. jump_table.py resolves the arms; the parent went
    # 326 -> 358 offsets and this type went 0 -> 18.
    "ManagerSub0209BE80_57E0ArrayRecord": "manager-sub-57e0-array-record-accesses.tsv",
    # NOT MAPPED, deliberately. gen_array_census.py produces 9 accesses for this type and all
    # nine land on record 1495, the last of 1,496, at 4-byte widths against slots the store
    # declares as 8-byte callback pointers. Record 1495 is real - its +0x00 holds the code
    # pointer 00342560 - but its +0x08/+0x10/+0x18 hold 0xFFFFFFFF in the LOW DWORD only, and
    # three unrelated functions read and write them as 32-bit values (001EDC40 does
    # `cmp dword [01EF9218], 8`). Whether that is the final record's unused slots being reused
    # as globals, or the count overrunning by one, is not decidable from the scan. Mapping it
    # would add three unexplained MISMATCH rows to this gate; the observation is recorded on
    # OPUS-CON-DISPATCH-TABLE-RECORD-0-AT-PLUS-8 instead.
    # NOT ADDED, and the reason matters. `ActorManagerSlot` already maps to
    # actor-manager-record-accesses.tsv, and actor-manager-record-rip-accesses.tsv is a SECOND
    # census of the same type by a different route: 0 of its 113 accesses appear in the first,
    # because one follows a base register and the other resolves folded-base RIP operands. This
    # map is one file per type and cannot hold both. A type can have more than one census and
    # the map should say so; recorded rather than forced.
    #
    # Added 2026-09-19 (OPUS), fourth pass. WIDGET IS THE TYPE THIS STORE REUSES MOST - 50
    # construction sites, 40 registered handlers, 27 distinct sizes - AND IT HAD NO CENSUS AT
    # ALL, so this gate's zero had never said anything about any of its eighteen rows. That is
    # the exact "nothing was compared" failure this file's own header describes, found from the
    # other side: a same-day split of +0x98 and +0x9C into four uint16 rows went in with this
    # gate green, and the green meant only that Widget was absent from this map.
    # gen_widget_census.py supplies it. The seed is the 40 handlers - registration IS the proof
    # that RCX holds a widget - plus nine core functions each admitted with a named caller that
    # passes one in RCX; nothing is followed into callees. The taint is offset-0 MAY over the
    # instruction graph, killed by a load through the pointer EXCEPT at +0x10/+0x18/+0x20, which
    # the store declares `Widget*`, so the tree walkers' traversals are admissible and are read
    # from the declarations rather than hard-coded. The census STOPS AT +0xC0 because the
    # smallest widget the image constructs is exactly 0xC0 - below that line every widget has
    # the offset, at or above it the bytes belong to 27 different derived types (289 accesses at
    # 72 offsets excluded on that ground). CONTROL, and the generator refuses without it: all 18
    # declared rows must have a cited address the census reaches with a span containing the
    # row's own offset. 18 of 18.
    "Widget": "widget-accesses.tsv",
    # Added 2026-09-19 (OPUS). This type went uncensused because gen_static_census.py accepted
    # only a COUNT control and nobody had counted it - and a count taken from the scan it is
    # meant to check cannot fail. A SITE control fixes that: the two instruction addresses this
    # type's own rows cite, 00866D60 (writes mt[0]) and 00866D98 (sets index = 0x270), both
    # reproduce, and neither is the scan's to invent.
    # IT BELONGS IN THIS MAP AND NOT STATIC_CENSUS, which was my first mistake
    # and the tally caught it: `static catalogue header rejected 1`.
    # STATIC_CENSUS parses the HAND-BUILT address-keyed schema
    # (word/site/kind/instruction/function/name); gen_static_census.py emits the
    # ordinary displacement schema this map reads, which is also why
    # BattleFormulaScratch appears in BOTH maps with two DIFFERENT files.
    # THE RESULT CORROBORATES THE DECLARATION AGAINST AN EXTERNAL SPECIFICATION. The eight
    # offsets the scan finds are mt[0], mt[1], mt[227], mt[396], mt[397], mt[621], mt[623] and
    # +0x9C0 - and those are exactly MT19937's boundary indices: 227 is 624-397, the wrap the
    # twist uses, and 397 is M. The index lands at 624*4 = 0x9C0, immediately past the vector,
    # which is what the `mt[624]` + `index` declaration says. A published algorithm predicting
    # the offsets is the non-circular control a count could never have been.
    "Mt19937State": "mt19937-state-accesses.tsv",
    # Added 2026-09-19 (OPUS), the last two STATIC-routed types with no census. Both were
    # reachable only once --control-sites existed, for the reason Mt19937State was: nobody had
    # counted them, so no count control could be written that was not drawn from the scan it
    # checks. Controlled on the addresses their own rows cite - 003185E4/00318641 for the LCG,
    # 0037C39C/0037C319 for the machine record - all four reproduce.
    # PartyReadMachineRecord HAS TWO INSTANCES, `STATIC 0x02EBF3D0 | STATIC 0x02EBF3F0`, and
    # this census covers the FIRST. The second is a separate scan against the same declared
    # rows and is NOT folded in here: two instances of one type are two populations, and
    # merging them would attribute an access to whichever base happened to explain it.
    "SharedGameplayLcgState": "shared-gameplay-lcg-state-accesses.tsv",
    "PartyReadMachineRecord": "party-read-machine-record-accesses.tsv",
    # THE SECOND INSTANCE IS ON DISK AND NOT IN THIS MAP, deliberately and with the reason
    # recorded rather than left to be rediscovered. `party-read-machine-record-second-instance-
    # accesses.tsv` censuses 0x02EBF3F0 - 47 accesses, 9 offsets, 7 functions - and this map
    # holds one file per type, the same limit already recorded for ActorManagerSlot's two
    # censuses. It is WRITTEN rather than left in a console, because a census that exists only
    # as a printed number is the defect three packages were spent on today.
    # WHAT THE SECOND CENSUS IS FOR, and it earned its keep immediately: the two instances agree
    # on EVERY offset and width except +0x10, and NO FUNCTION TOUCHES BOTH (6 functions against
    # 7, disjoint). See the +0x10 row's per-path union note.
    # Added 2026-09-19 (OPUS), fifth pass, and this one is a DURABILITY repair rather than a new
    # scan. Twenty-seven LegacyPs2GsTextureContext rows already cite, verbatim, "gen_ptr_census_
    # depth1.py over PTR 0209A670, 36 accesses at 15 offsets in 11 functions" - a census that was
    # run to a CONSOLE and never written. No file existed, so nothing pointed at it and this gate
    # had never compared a single one of those rows; the type looked worked-over from its evidence
    # column and was invisible here. Re-running the generator with --out reproduces 36/15/11
    # exactly, which is the self-control: the artifact now on disk is the one the rows were
    # written from, not a near-miss.
    # WHAT THIS CHECK IS AND IS NOT WORTH. The rows were AUTHORED FROM these accesses, so the gate
    # passing today confirms the transcription and nothing more - the same "one fact checked twice"
    # caution the EMBED projections above carry. Its value is prospective: a later edit to any of
    # these rows, or a regeneration that moves, is now caught instead of silently accepted.
    # The depth-1 route matters to a reader: 16 of the 36 are same-function, and the other 20 come
    # from three callee/argument pairs one level down, which is why `gen_ptr_census.py` alone finds
    # 16 at 10 offsets for a 0x240 object. Every row's route column says `ptr-depth1 0209A670+0x0`.
    "LegacyPs2GsTextureContext": "legacy-ps2gs-texture-context-accesses.tsv",
    # Added 2026-09-19 (OPUS), the SECOND instance of the same durability defect and the first
    # one found by a check rather than by accident. 11 rows cite `gen_ptr_census_depth1.py`, no
    # file existed, and this type was in no census map - exactly LegacyPs2GsTextureContext an hour
    # earlier. `check_cited_artifacts.py` now finds the class; this is what it found.
    # PRODUCED BY A DIFFERENT TOOL THAN THE ROWS CITE, and the reason is stated because it matters
    # to what this census is worth. The rows' own evidence names FOUR bodies reached from the slot
    # load - 001D6040, 001D5650, 001D6170 and 001D58F0, the last of them at DEPTH 2 via 001D6170 -
    # and `gen_ptr_census_depth1.py` is one level by construction, so re-running it reproduced 9
    # accesses at 6 offsets from 2 functions: an artifact NARROWER than the reading the rows rest
    # on, which would have registered 20 rows as "no access at that displacement" when their real
    # support is a body the file does not contain. `gen_route_seeded_census.py` follows the store's
    # own route to depth 6 and carries the displacement through lea/add/argument slots: 86 accesses
    # at 41 offsets from 6 functions, and its own control holds - EVERY base the accesses were
    # reached through resolves to a declared row (+0x0, +0xC30, +0x607C, +0x2E3C, +0x2438, +0x47).
    # That tool had no --out either, which is why the richer census had never been a file; the flag
    # was added in the same package.
    "FrameMarkerSingleton01F82C80": "frame-marker-singleton-accesses.tsv",
    # Added 2026-09-19 (OPUS) to settle the LAST standing case of the bulk-clear-read-as-a-field
    # -list class. Resume 91 named RenderModelInstance's five `qwordSlot*` rows as a ctor's
    # forty-byte clear read as five fields and LEFT them, because the signature was argued
    # rather than measured. It is measured now: all five stores carry `zeroclear`, and four of
    # them - +0xC, +0x14, +0x1C, +0x24 - have NO OTHER ACCESS OF ANY KIND in the census.
    # The census needed the constructor, and the route could not reach it: RenderModelInstance
    # is `FN 0x003E55B0+0x0`, a getter's return, so the walk sees every body that USES the object
    # and never the one that builds it. gen_route_seeded_census.py --with-ctor seeds the
    # constructor the store already names in its own `ctor` column; 33 offsets became 64.
    "RenderModelInstance": "render-model-instance-accesses.tsv",
    # Added 2026-09-19 (OPUS), and it was UNCENSUSABLE until two defects in the same tool were
    # fixed in one afternoon. Its route is `STATIC 0x022C7020 | PTR 0x022C7CD0` and
    # gen_route_seeded_census.py matched the WHOLE route string, so it answered "not one this
    # tool models" for a route both of whose alternatives it models - gen_ptr_census.py has
    # always split on `|`. With that fixed, both alternatives still find zero seed hosts (the
    # static block is addressed RIP-absolutely and nothing loads the pointer slot), and the
    # census comes entirely from --with-ctor seeding 00478040, the constructor the store names:
    # 0 offsets -> 15 across 25 declared rows.
    "RenderModelInstanceContainer": "render-model-instance-container-accesses.tsv",
    # THE RENDER-ROOT FAMILY, added 2026-09-19 (OPUS). All five were declared the same day and
    # NONE had an artifact, so project_embed_census.py reported `parent has no census` for
    # every child and the whole family was unprojectable. The root's is route-seeded
    # (`STATIC 0x022C6F30 | PTR 0x022C6F20`, 31 accesses at 7 offsets); note that route needs
    # BOTH alternatives - a STATIC-only walk finds 4 offsets and none of the cited control
    # sites, because the six lea sites cache the root into 022C6F20 and reload it.
    "RenderResourceRoot": "render-resource-root-accesses.tsv",
    # The other three are NOT route-seeded and could not be: two are EMBED, and
    # RenderResourceEntry's declared `FN 0x002ED570+0x0` is SHARED with RenderStrideC0Element
    # because that resolver serves three banks - seeding from it bare gives 43 offsets against
    # the restricted 26, seventeen of them another bank's. These three come from
    # emit_seeded_census.py, which seeds only functions proved to take the object as argument
    # 0 and records those seeds in the file's own header.
    "RenderStrideC0Bank": "render-stride-c0-bank-accesses.tsv",
    "RenderResourceEntryBank": "render-resource-entry-bank-accesses.tsv",
    "RenderResourceEntry": "render-resource-entry-accesses.tsv",
    # The fourth render-root child, added the same way: its route is EMBED too, and its
    # four seeds are all called on [root +0xDA8]. Registering it makes
    # PresentationEntryReferenceNode projectable, which was one of the three EMBED types
    # still stranded.
    "PresentationEntryReferenceContainer":
        "presentation-entry-reference-container-accesses.tsv",
    # Added 2026-09-19 (OPUS) and NOT a render type. Its route is SLOTPTR, which no
    # census tool models, and its 8-slot registry at 0209C4D0 is reached by `lea` - 18
    # address-takings in 16 functions - not by indexed load, so a displacement scan sees
    # nothing and it had no artifact. Seeded instead from the four record-taking
    # functions its own rows cite most heavily; 74 offsets, control 3/3 on the three the
    # declared ctor clears. Registering it also unstrands TextDrawState, which embeds at
    # +0xD0.
    "MessageWindowRecord": "message-window-record-accesses.tsv",
    # ADDED 2026-09-20 (OPUS) with the type itself. Declared from a SCRATCH census of 23
    # offsets, then the real artifact was emitted by emit_seeded_census and found 44 -
    # seven of them inside rows the declaration had just called unobserved, six being
    # Widget header fields. Registering it here is the point: without the map entry this
    # checker reports "0 disagreements" for a type it never looked at, which is the green
    # light this file's own header warns is worse than a red one.
    "BattleMenuWidget2DC0": "battle-menu-widget-2dc0-accesses.tsv",
    # ADDED 2026-09-20 (OPUS). Its 95 rows were BUILT FROM this artifact after
    # clean() had removed the eight unrolled SIMD block copies in 00276D30, so the
    # comparison here is the same filter applied twice - which is the point: if the
    # rows were built from the cleaned census, the gate should find nothing, and a
    # disagreement would mean the build and the gate disagree about the filter.
    "BattleMenuPanelWidget3010": "battle-menu-panel-widget-3010-accesses.tsv",
    # ADDED 2026-09-20 (OPUS), the fourth level of this widget hierarchy. Its artifact is
    # the first here emitted by receiver_flow_census.py rather than emit_seeded_census.py,
    # and the difference is not cosmetic: nine of this type's fifteen offsets are reached
    # ONLY through the parent's `imul <reg>, <reg>, 0x1620` walk, where the object is the
    # INDEX register and a multiple of the stride is the base. A base-only harvest cannot
    # see those at all, which is how the type was first declared with five rows reading
    # "no access reaches it" over bytes that are demonstrably read.
    "BattleMenuChildWidget1620": "battle-menu-child-widget-1620-accesses.tsv",
    "PaneListWidget0B68": "pane-list-widget-0b68-accesses.tsv",
    "PaneSlotWidget0160": "pane-slot-widget-0160-accesses.tsv",
    "WidgetSingleton02B47758": "widget-singleton-02b47758-accesses.tsv",
    "WidgetSingleton02B47758_02A0": "widget-singleton-02b47758-02a0-accesses.tsv",
    "WidgetSingleton02B47758_0460": "widget-singleton-02b47758-0460-accesses.tsv",
    "WidgetSingleton02B47758_05F0": "widget-singleton-02b47758-05f0-accesses.tsv",
    "ResourceRequestSlot": "resource-request-slot-accesses.tsv",
    # RenderContext02CC0410 subtree, unlocked by the parent's STATIC route
    # (0x02CC0410, its ctor 005FD050 builds it in place). Children ride the
    # parent's EMBED/CHAIN routes; PPostEffectBase chains through
    # PDeferredLightingBase's VTABLE routes.
    "RenderContext02CC0410": "render-context-02cc0410-accesses.tsv",
    "RenderPrimitivePass1E8": "render-primitive-pass-1e8-accesses.tsv",
    "RenderContextPassStateBlock": "render-context-pass-state-block-accesses.tsv",
    "PrimitiveRendererD3D11": "primitive-renderer-d3d11-accesses.tsv",
    "PShaderPassStateD3D11": "p-shader-pass-state-d3d11-accesses.tsv",
    "PPostEffectBase": "p-post-effect-base-accesses.tsv",
}


# A STATIC block is censused by ABSOLUTE ADDRESS, not by displacement, because it has no base
# register to take a displacement from: `mov dword ptr [rip + 0x27695f6], eax` is an access to
# 02AEDFB8, full stop. That catalogue therefore has a different schema - word/site/kind/
# instruction/function/name - and every displacement-keyed checker skipped it silently for that
# reason alone. 912 rows of evidence were sitting unread behind a column name, for the type this
# store had already called its most completely recovered. The address minus the base IS the
# displacement, so the same comparison applies once it is computed.
# The third shape: a sub-object inside another type's census file, at a fixed displacement.
# The value is (census file, the sub-object's offset within that census's key space).
SUBOBJECT_CENSUS = {
    "ImageBackedStateBlock": ("save-payload-accesses.tsv", 0x8000),
    # BattleStatsRecord is the first type with TWO censuses: its own file reaches the kind-0
    # (party) home through the BattleUnit +0x698 chain, and this entry rebases the kind-1 home
    # out of the spawn record's census. A type in both maps is two independent work items -
    # each census is compared against the declared rows separately, so both homes' evidence
    # is checked and neither can mask a disagreement in the other.
    "BattleStatsRecord": ("spawn-record-accesses.tsv", 0x80),
}

STATIC_CENSUS = {
    "BattleFormulaScratch": ("formula-scratch-block-accesses.tsv", 0x02AEDFB8),
}
STATIC_HEADER = ["word", "site", "kind", "instruction", "function", "name"]
LEA = re.compile(r"^\s*lea\b", re.I)


EMIT_CHECKED = []   # (type, offset) actually compared -- for the union-coverage measurement
MARKER = "WIDTH DELIBERATE"


def reason_after(ev, minimum=40):
    """The exemption is earned by the REASON, not by the phrase.

    Granting it on a bare substring means a row could take the exemption by merely mentioning the
    rule - and the form is already inconsistent in the store (one row writes "WIDTH DELIBERATE,"
    with a comma rather than a colon), so the test cannot require punctuation either. It requires
    prose: at least `minimum` characters after the marker. Audited 2026-09-13 (OPUS): all ten rows
    carrying the marker give between 216 and 2,087 characters, so nothing is excluded by this and
    a future empty one will not pass silently."""
    i = ev.find(MARKER)
    if i < 0:
        return ""
    tail = ev[i + len(MARKER):].lstrip(":, ").strip()
    return tail if len(tail) >= minimum else ""


MARKER_WIDTH = re.compile(r"declared(?: at)? (\d+)")


def marker_contradicts(ev, size):
    """The exemption's own sentence names a width this row does not declare -> it was INHERITED.

    A marker is an EARNED exemption and `reason_after` already checks that a reason is present.
    It cannot check that the reason is about THIS row, and that is the failure this catches.

    WHERE IT CAME FROM, on 2026-09-19 (OPUS), found by hand and only afterwards made a check.
    The split scripts in this kit copy a parent row's evidence onto both children, which is right
    for provenance and WRONG FOR A MARKER: the sentence that earned the exemption was written
    about the parent's width. Four rows came out of the day's splits carrying one -
    `GameSettingConfig +0x2C/+0x2E`, declared 2, each saying "the declared 4 is the packed dword";
    `TextDrawState +0x9C/+0x9D`, declared 1, each saying "declared at 2 because the 0x1E
    initialiser", and the census quoted in that copied sentence was never even +0x9D's. Every one
    of them was silently exempt at an offset nobody was comparing.

    The test is deliberately narrow: only a NUMBER the marker states about itself, only within the
    sentence that opens it, and it fires only when that number is not the declared size. A marker
    that names no width is not accused of anything. Store-wide at the time of writing: 31 rows
    carry a marker, 4 contradicted, all 4 from that day's splits - so this is not a rule the
    existing corpus was bent to fit.

    A NOTE FOR WHOEVER WRITES THE NEXT WITHDRAWAL. `MARKER` is matched as a bare substring, so
    evidence prose that merely MENTIONS the phrase takes the exemption. Write it hyphenated when
    you mean to talk about it rather than claim it.
    """
    i = ev.find(MARKER)
    if i < 0:
        return None
    named = [int(n) for n in MARKER_WIDTH.findall(ev[i:i + 260])]
    return named if named and size not in named else None


def width_of(ins):
    if NOP.match(ins) or LEA.match(ins):
        return None
    i = ins.lower()
    for tok, w in FORMS:
        if tok in i:
            return w
    if "word ptr" in i:
        return 2
    return None


def censused_types(root="."):
    """(type, census file, static base or None, sub-object shift, EXTENT) for EVERY census shape.

    One definition of "which types have a census", because there are now three shapes and three
    consumers. Before this existed, `gen_recoverable_gaps` and `check_float_typed_as_int` each
    iterated CENSUS alone and silently skipped the static and sub-object shapes - so a type could be
    censused, width-checked and still produce no gap candidates and no float findings, which looks
    exactly like a type with nothing wrong in it.

    THE FIFTH ELEMENT IS THE REPAIR OF THIS HELPER'S OWN DEFECT, found 2026-09-13. `main` below has
    always clipped a sub-object's rebased offsets to the sub-object's extent, and its comment names
    the hazard exactly: "so a 20-row sub-object is not compared against its parent's other 60 KB".
    The helper extracted from that loop did NOT carry the extent, so every instrument written
    afterwards re-implemented the rebase as a bare `if off >= shift: off -= shift` - unbounded.
    `ImageBackedStateBlock` is declared out to 0x47E8 and the parent census runs to 0xE2D0, so a
    SavePayload access at 0xE2D0 was being presented to four instruments as a field of a type that
    ends 0x9AE8 earlier.

    The tuple is FIVE-WIDE deliberately. A consumer still unpacking four will fail loudly at import
    rather than silently keep the unbounded behaviour, which is the whole point: this is the same
    failure shape as a rule living in a comment beside the code that honours it, where the next thing
    built next to it does not.
    """
    sizes = type_sizes(os.path.join(root, "Database", "FFXII TZA", "_types", "types.tsv"))
    out = [(t, f, None, 0, 0) for t, f in CENSUS.items()]
    out += [(t, f, b, 0, sizes.get(t, 0)) for t, (f, b) in STATIC_CENSUS.items()]
    out += [(t, f, None, sh, sizes.get(t, 0)) for t, (f, sh) in SUBOBJECT_CENSUS.items()]
    return sorted(out)


def rebase(off, shift, extent):
    """A census displacement in the PARENT's frame -> this type's own frame, or None.

    None means the access is outside this type and belongs to nobody here. Both bounds matter and
    only the lower one was ever applied by the consumers:

        off <  shift           the access is before the sub-object starts
        off >= shift + extent  the access is past its end - the case that was missing

    An extent of 0 means the type declares no size, and then only the lower bound can be applied;
    that is a weaker answer, not a licence to drop the bound where one exists.
    """
    if shift:
        if off < shift:
            return None
        off -= shift
        if extent and off >= extent:
            return None
    return off


def clean(path, tally):
    """Displacement -> width counter, with the three artefact classes excluded.

    `tally` accumulates malformed input instead of discarding it: a census that parses to
    nothing must not look like a census that agrees."""
    per = collections.defaultdict(collections.Counter)
    xmm = collections.Counter()
    raw = []
    for n, line in enumerate(io.open(path, encoding="utf-8")):
        if n == 0:
            continue
        if not line.strip():
            continue
        # A `#` HEADER IS NOT A MALFORMED ROW, and counting it as one cost a detour on
        # 2026-09-20: a sweep of every accesses.tsv reported 1,279 `census_malformed` lines, and
        # in eleven of the thirteen files the number was EXACTLY that file's own comment-header
        # count. The tally exists so that a census parsing to nothing cannot look like a census
        # that agrees - which only works while the number means BROKEN ROWS. (The other two
        # files were the address-keyed schema this reader is not meant to parse at all, and
        # clean_static reads them correctly; the sweep was wrong, not the store.)
        if line.startswith("#"):
            tally["census_comment"] += 1
            continue
        c = line.rstrip("\n").split("\t")
        # NOR IS THE COLUMN HEADER, WHEREVER IT SITS. This reader skips line 0 as the header,
        # which is right for a file that opens with one - and wrong for the census files that
        # open with a `#` preamble, where the real header is further down and was landing in
        # `census_malformed` with everything else. Same 2026-09-20 detour, same remedy: the
        # number has to mean broken rows.
        if c[0] == "function" and len(c) > 3 and c[3] == "disp":
            tally["census_header"] += 1
            continue
        if len(c) < 6:
            tally["census_malformed"] += 1
            continue
        try:
            off = int(c[3], 16)
        except ValueError:
            tally["census_malformed"] += 1
            continue
        if off == 0 and INDEXED.search(c[5]):
            tally["census_indexed"] += 1
            continue
        # A CENSUS ROW MAY DECLARE ITSELF UNUSABLE AS WIDTH EVIDENCE. `gen_route_seeded_census.py`
        # follows the object's displacement into callees, which is what makes it see 326 offsets
        # on ManagerSingleton0209BE80 where a slot-seeded scan sees 42 - and also means a helper
        # the whole image calls gets credited with this type's layout. That generator now marks
        # such rows `exposed` in the route column, propagated along its own descent edges,
        # because the subtree below a shared helper is not private either: 00217060 has ONE
        # caller and that caller is the 103-caller 00202B70.
        # THE ROW IS KEPT IN THE FILE AND EXCLUDED HERE, deliberately. It is evidence about
        # SOMETHING - a real access at a real address - and discarding it would lose the
        # distinction a later reader needs to decide whether that subsystem's view of these
        # bytes is a second view of one field or a different object entirely.
        if len(c) > 6 and "exposed" in c[6]:
            tally["census_shared_helper"] += 1
            continue
        # A CONTIGUOUS RUN OF STORES OF A PROVABLY-ZERO REGISTER IS A CLEAR, and its stride is
        # the width the compiler chose to zero with, not a field boundary. This store has now
        # met it three times - RenderModelInstance's five `qwordSlot*` rows (Resume 91),
        # BootSingleton01F7F598 +0xD00/+0xD08, and ManagerSub0209BE80_7EA0's four `void*` rows,
        # which turned out to be two float4s - and each was read by hand, because nothing here
        # can see that `rax` was zeroed two instructions earlier. The producer can, and marks
        # it. A SINGLE zero store is NOT marked: initialising one genuine field to zero looks
        # identical, and only the run is incompatible with a field list.
        if len(c) > 6 and "zeroclear" in c[6]:
            tally["census_zero_clear"] += 1
            continue
        w = width_of(c[5])
        if w is None:
            tally["census_no_width"] += 1
            continue
        if w == 16:
            xmm[c[0]] += 1
        raw.append((off, w, c[0]))
    bulk = {fn for fn, n in xmm.items() if n >= 4}
    # The bulk rule is sound in intent and COSTS SOMETHING, so the cost is recorded rather than
    # absorbed. At an offset where a declared 16-byte field and an unrolled block copy look
    # identical, dropping the run also drops the field's only 16-wide evidence - and a zero
    # disagreement count partly bought that way is not the same as a zero that was earned.
    # Measured 2026-09-13 (OPUS): 10 declared rows are touched, 4 of them materially.
    dropped_at = collections.Counter()
    for off, w, fn in raw:
        if w == 16 and fn in bulk:
            tally["census_bulk_xmm"] += 1
            dropped_at[off] += 1
            continue
        per[off][w] += 1
        tally["census_used"] += 1
    return per, dropped_at


def clean_static(path, base, size, tally):
    """Displacement -> width counter for an absolute-address catalogue.

    The header is validated rather than assumed: this is the third schema in the kit and two
    earlier tools mis-parsed a census by trusting column positions."""
    per = collections.defaultdict(collections.Counter)
    first = True
    for n, line in enumerate(io.open(path, encoding="utf-8")):
        c = line.rstrip("\n").split("\t")
        if first:
            first = False
            if [x.strip().lower() for x in c[:6]] != STATIC_HEADER:
                tally["static_bad_header"] += 1
                return per
            continue
        if len(c) < 4:
            tally["census_malformed"] += 1
            continue
        try:
            addr = int(c[0], 16)
        except ValueError:
            tally["census_malformed"] += 1
            continue
        if not (base <= addr < base + size):
            tally["static_outside_extent"] += 1
            continue
        w = width_of(c[3])
        if w is None:
            tally["census_no_width"] += 1
            continue
        per[addr - base][w] += 1
        tally["census_used"] += 1
    return per


def type_sizes(types_path):
    """Declared type sizes, used to bound a static catalogue to its own extent. A fixture that
    declares no types is a valid input, not an error."""
    sizes = {}
    if not os.path.exists(types_path):
        return sizes
    for n, line in enumerate(io.open(types_path, encoding="utf-8")):
        if not n:
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) > 1:
            try:
                sizes[c[0]] = int(c[1], 16) if c[1].lower().startswith("0x") else int(c[1])
            except ValueError:
                pass
    return sizes


def load_declared(fields_path, tally):
    declared = collections.defaultdict(dict)
    for line in io.open(fields_path, encoding="utf-8"):
        c = line.rstrip("\n").split("\t")
        if len(c) < 3 or c[0] == "type":
            continue
        if c[0] not in CENSUS and c[0] not in STATIC_CENSUS and c[0] not in SUBOBJECT_CENSUS:
            continue
        try:
            declared[c[0]][int(c[1], 16)] = (int(c[2]), c[3], c[4] if len(c) > 4 else "",
                                             c[8] if len(c) > 8 else "")
        except ValueError:
            tally["declared_malformed"] += 1
    return declared


def run(root, verbose=True):
    fields_path = os.path.join(root, "Database", "FFXII TZA", "_types", "fields.tsv")
    paths = {os.path.basename(p): p
             for p in glob.glob(os.path.join(root, "Database", "FFXII TZA", "**",
                                             "*-accesses.tsv"), recursive=True)}
    tally = collections.Counter()
    declared = load_declared(fields_path, tally)
    sizes = type_sizes(os.path.join(root, "Database", "FFXII TZA", "_types", "types.tsv"))

    bad, spans, deliberate = 0, [], []
    checked = 0
    no_census_file, no_access, bulk_cost = [], [], []
    marker_no_reason, marker_unused = [], []

    # OVER THE WHOLE STORE, not the censused part. Every other check here needs a census to have
    # something to compare against, so it runs inside the per-type loop below and says nothing
    # about the 383 types that have none. This one needs only the row: an exemption whose own
    # sentence names a width the row does not declare is wrong whether or not anybody ever
    # censused the type, and on an uncensused type it is the more dangerous, because nothing
    # else here will ever look at that offset again.
    marker_contra = []
    for line in io.open(fields_path, encoding="utf-8"):
        c = line.rstrip("\n").split("\t")
        if len(c) < 9 or c[0] == "type" or MARKER not in c[8]:
            continue
        try:
            named = marker_contradicts(c[8], int(c[2]))
        except ValueError:
            continue
        if named:
            marker_contra.append((c[0], c[1], c[2], c[3], named))

    work = [(t, f, None, 0) for t, f in CENSUS.items()]
    work += [(t, f, b, 0) for t, (f, b) in STATIC_CENSUS.items()]
    work += [(t, f, None, sh) for t, (f, sh) in SUBOBJECT_CENSUS.items()]
    for tname, fname, sbase, shift in work:
        rows = declared.get(tname, {})
        if fname not in paths:
            if rows:
                no_census_file.append((tname, fname, len(rows)))
            continue
        if sbase is None:
            per, dropped_at = clean(paths[fname], tally)
        else:
            per = clean_static(paths[fname], sbase, sizes.get(tname, 0), tally)
            dropped_at = {}
        if shift:
            # A sub-object's field offsets are its own; the parent's census records them shifted by
            # the sub-object's position inside the parent. Rebase, and drop everything outside this
            # type's extent so a 20-row sub-object is not compared against its parent's other 60 KB.
            ext = sizes.get(tname, 0)
            per = dict((rebase(d, shift, ext), w) for d, w in per.items()
                       if rebase(d, shift, ext) is not None)
            dropped_at = dict((rebase(d, shift, ext), n) for d, n in dropped_at.items()
                              if rebase(d, shift, ext) is not None)
        for off, n in dropped_at.items():
            row = rows.get(off)
            if row is None:
                continue
            kept = per.get(off)
            if not kept:
                bulk_cost.append((tname, off, row[0], row[2], n, "ALL evidence dropped"))
            elif row[0] == 16 and 16 not in kept:
                bulk_cost.append((tname, off, row[0], row[2], n,
                                  "only 16-wide evidence dropped; kept %s" % dict(kept)))
        for off, (size, name, ct, ev) in sorted(rows.items()):
            c = per.get(off)
            if not c:
                # NOT a pass. Nothing at this displacement was ever compared.
                no_access.append((tname, off, size, name))
                continue
            checked += 1
            EMIT_CHECKED.append((tname, off))
            best = c.most_common(1)[0][0]
            if MARKER in ev and not reason_after(ev):
                marker_no_reason.append((tname, off, size, name))
            if size == best:
                if MARKER in ev:
                    marker_unused.append((tname, off, size, name, dict(c)))
                continue
            if "WIDTH DELIBERATE" in ev and reason_after(ev):
                # A row may declare a width the census disagrees with, PROVIDED it says
                # why in its own evidence. A union span and a field whose writers and
                # readers use different widths are both legitimate; a check that stays
                # permanently red is one nobody reads, so the exception is explicit,
                # carried by the row itself, and listed here rather than hidden.
                deliberate.append((tname, off, size, name, dict(c)))
                continue
            if size > 16 or ct.endswith("]") or size in (10, 16) and ct.endswith("]"):
                spans.append((tname, off, size, name, dict(c)))
                continue
            widths = sorted(c)
            if best != min(widths) and c[min(widths)] >= c[best]:
                best = min(widths)
            if size != best:
                bad += 1
                if verbose:
                    print("  MISMATCH %-20s +0x%04X declared %-4d name=%-24s clean evidence %s"
                          % (tname, off, size, name[:24], dict(c)))

    if verbose:
        print()
        print("declared whole (array or span) - disagreement expected: %d" % len(spans))
        for tname, off, size, name, c in spans:
            print("  span     %-20s +0x%04X declared %-5d %-24s elements %s"
                  % (tname, off, size, name[:24], c))
        print()
        if marker_no_reason:
            print("DEFECT -- rows taking the WIDTH DELIBERATE exemption with no reason after it: %d"
                  % len(marker_no_reason))
            for tname, off, size, name in marker_no_reason:
                print("      %-22s +0x%04X declared %-4s %s" % (tname, off, size, name[:24]))
        if marker_contra:
            print("DEFECT -- exemptions whose own sentence names a width the row does NOT"
                  " declare: %d" % len(marker_contra))
            print("      An INHERITED marker: the reason was written about a superseded"
                  " declaration, usually a parent row that was later split, and it exempts this")
            print("      row from comparison on the strength of a sentence that is about a"
                  " different field. Rewrite it for this row or withdraw it.")
            for tname, off, size, name, named in marker_contra:
                print("      %-22s %-8s declared %-4s %-22s marker says %s"
                      % (tname, off, size, name[:22], named))
        if marker_unused:
            print("WIDTH DELIBERATE markers that are no longer needed -- the census now AGREES: %d"
                  % len(marker_unused))
            print("      Retiring one is its owner's call; a stale exemption hides the next real"
                  " disagreement at that offset.")
            for tname, off, size, name, c in marker_unused:
                print("      %-22s +0x%04X declared %-4s %-22s census %s"
                      % (tname, off, size, name[:22], c))
        print("declared deliberately against the census, with a reason in the row: %d"
              % len(deliberate))
        for tname, off, size, name, c in deliberate:
            print("  stated   %-20s +0x%04X declared %-5d %-24s census %s"
                  % (tname, off, size, name[:24], c))

        print()
        print("COVERAGE -- what was actually compared, not what stayed quiet")
        total = checked + len(no_access) + sum(n for _, _, n in no_census_file)
        # The denominator a gate would otherwise assume. This checker can only ever see the
        # types in CENSUS; every other row in the store is outside its reach, and saying so
        # is the difference between "the store's widths agree" and what this actually proves.
        store_rows = store_types = 0
        seen = set()
        for line in io.open(fields_path, encoding="utf-8"):
            c = line.split("\t")
            if len(c) > 2 and c[0] != "type" and c[0].strip():
                store_rows += 1
                seen.add(c[0])
        store_types = len(seen)
        print("  declared rows in the store:                                  %d in %d types"
              % (store_rows, store_types))
        print("  OUTSIDE THIS CHECKER'S REACH (no census mapping):            %d in %d types"
              % (store_rows - total, store_types - len(CENSUS) - len(STATIC_CENSUS)
                                - len(SUBOBJECT_CENSUS)))
        print("  declared rows in scope (the %d types with a census mapping): %d"
              % (len(CENSUS) + len(STATIC_CENSUS) + len(SUBOBJECT_CENSUS), total))
        print("    CHECKED, a comparison was performed:                      %d" % checked)
        print("    unchecked, census file absent:                            %d"
              % sum(n for _, _, n in no_census_file))
        for tname, fname, n in no_census_file:
            print("        %-22s %-36s %d row(s)" % (tname, fname, n))
        print("    unchecked, census has no access at that displacement:     %d" % len(no_access))
        by_type = collections.Counter(t for t, _, _, _ in no_access)
        for tname, n in sorted(by_type.items()):
            print("        %-22s %d row(s)" % (tname, n))
        print("  census lines read but not usable as width evidence:")
        for k, label in (("static_bad_header", "static catalogue header rejected"),
                         ("static_outside_extent", "address outside the type's extent"),
                         ("census_malformed", "malformed or short"),
                         ("census_no_width", "no operand width"),
                         ("census_indexed", "indexed at zero displacement"),
                         ("census_bulk_xmm", "unrolled SIMD block copy"),
                         ("census_shared_helper", "reached via a shared helper"),
                         ("census_zero_clear", "a zeroed-register clear run")):
            print("      %-32s %d" % (label, tally[k]))
        print("      %-32s %d" % ("usable width observations", tally["census_used"]))
        print("  WHAT THE SIMD RULE COST -- declared rows whose evidence it removed: %d" % len(bulk_cost))
        print("      Every one is an ARRAY. Where the array is accessed per element the rule costs")
        print("      nothing; where its natural access IS a block move, the rule removes exactly the")
        print("      evidence that would have confirmed it, and that row is UNCHECKED, not passing.")
        for tname, off, size, ct, n, why in sorted(bulk_cost):
            print("      %-22s +0x%04X %-12s declared %-4s  %d line(s)  %s"
                  % (tname, off, ct[:12], size, n, why))
        if tally["declared_malformed"]:
            print("  declared rows that would not parse: %d" % tally["declared_malformed"])
        print()
        print("ROWS WHOSE DECLARED SIZE DISAGREES WITH THE CLEANED CENSUS: %d" % bad)
        if not checked:
            print("NO COMPARISON WAS PERFORMED. This result proves nothing about any width.")

    return bad, checked, len(no_access), sum(n for _, _, n in no_census_file), tally


FIXTURES = {
    # ASTRA's five EXP036 cases, restated so the verdict can be seen to distinguish them.
    "matching": (
        [("BattleUnit", "0x0010", "4", "f", "uint32", "", "", "", "")],
        "function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n"
        "00100000\tf\t00100000\t0x10\tr\tmov eax, dword ptr [rcx + 0x10]\tseed\t\n",
        (0, 1)),
    "mismatch": (
        [("BattleUnit", "0x0010", "1", "f", "uint8", "", "", "", "")],
        "function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n"
        "00100000\tf\t00100000\t0x10\tr\tmov eax, dword ptr [rcx + 0x10]\tseed\t\n",
        (1, 1)),
    "census_missing_displacement": (
        [("BattleUnit", "0x0010", "4", "f", "uint32", "", "", "", "")],
        "function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n"
        "00100000\tf\t00100000\t0x20\tr\tmov eax, dword ptr [rcx + 0x20]\tseed\t\n",
        (0, 0)),
    "malformed_only": (
        [("BattleUnit", "0x0010", "4", "f", "uint32", "", "", "", "")],
        "function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n"
        "garbage\n",
        (0, 0)),
    "no_declarations": (
        [],
        "function\tname\tsite\tdisp\tkind\tinstruction\troute\tnote\n"
        "00100000\tf\t00100000\t0x10\tr\tmov eax, dword ptr [rcx + 0x10]\tseed\t\n",
        (0, 0)),
}


# The absolute-address path gets its own fixtures. A header check that is never exercised is
# not a header check, and this is the third schema in the kit: two earlier tools mis-parsed a
# census by trusting column positions, so the rejection must be demonstrable.
STATIC_FIXTURES = {
    "static_matching": (
        [("BattleFormulaScratch", "0x0004", "4", "f", "uint32", "", "", "", "")],
        "word\tsite\tkind\tinstruction\tfunction\tname\n"
        "02AEDFBC\t00100000\tr\tmov eax, dword ptr [rip + 0x1]\t00100000\tf\n",
        (0, 1)),
    "static_mismatch": (
        [("BattleFormulaScratch", "0x0004", "1", "f", "uint8", "", "", "", "")],
        "word\tsite\tkind\tinstruction\tfunction\tname\n"
        "02AEDFBC\t00100000\tr\tmov eax, dword ptr [rip + 0x1]\t00100000\tf\n",
        (1, 1)),
    "static_wrong_header": (
        [("BattleFormulaScratch", "0x0004", "4", "f", "uint32", "", "", "", "")],
        "address\tsite\tkind\tinstruction\tfunction\tname\n"
        "02AEDFBC\t00100000\tr\tmov eax, dword ptr [rip + 0x1]\t00100000\tf\n",
        (0, 0)),
    "static_outside_extent": (
        [("BattleFormulaScratch", "0x0004", "4", "f", "uint32", "", "", "", "")],
        "word\tsite\tkind\tinstruction\tfunction\tname\n"
        "02AEE400\t00100000\tr\tmov eax, dword ptr [rip + 0x1]\t00100000\tf\n",
        (0, 0)),
}


def self_test():
    import shutil
    import tempfile
    root = tempfile.mkdtemp(prefix="ccw-fixture-")
    ok = True
    try:
        cases = [(k, v, False) for k, v in FIXTURES.items()]
        cases += [(k, v, True) for k, v in STATIC_FIXTURES.items()]
        for name, (rows, census, (want_bad, want_checked)), static in sorted(cases):
            tdir = os.path.join(root, name, "Database", "FFXII TZA", "_types")
            cdir = os.path.join(root, name, "Database", "FFXII TZA", "11-Party")
            os.makedirs(tdir)
            os.makedirs(cdir)
            with io.open(os.path.join(tdir, "fields.tsv"), "w", encoding="utf-8") as fh:
                fh.write("type\toffset\tsize\tname\tctype\tmeaning\treadiness\tconfidence\tevidence\n")
                for r in rows:
                    fh.write("\t".join(r) + "\n")
            if static:
                with io.open(os.path.join(tdir, "types.tsv"), "w", encoding="utf-8") as fh:
                    fh.write("type\tsize\n")
                    fh.write("BattleFormulaScratch\t0xA8\n")
                target = "formula-scratch-block-accesses.tsv"
            else:
                target = "battle-unit-accesses.tsv"
            with io.open(os.path.join(cdir, target), "w", encoding="utf-8") as fh:
                fh.write(census)
            bad, checked, _, _, _ = run(os.path.join(root, name), verbose=False)
            good = (bad, checked) == (want_bad, want_checked)
            ok &= good
            print("  %-28s mismatches=%d comparisons=%d  expected (%d,%d)  %s"
                  % (name, bad, checked, want_bad, want_checked, "ok" if good else "FAILED"))
            print("        exit would be %d (%s)"
                  % (1 if bad else (0 if checked else 2),
                     "mismatch" if bad else ("checked and clean" if checked else
                                            "NOTHING PROVED")))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print()
    print("fixtures: %s" % ("all distinguish correctly" if ok else "A FIXTURE FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    bad, checked, _, _, _ = run(KP.ROOT)
    raise SystemExit(1 if bad else (0 if checked else 2))
