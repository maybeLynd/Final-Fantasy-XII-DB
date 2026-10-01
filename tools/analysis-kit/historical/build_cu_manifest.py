from pathlib import Path
rows={
'001E7D30':('EASTL.ContainerRuntime.VectorInsertFillReallocate','Complete body performs vector-style capacity growth, allocator-backed relocation, fill insertion, and old-buffer release; three established EASTL container routines call it.'),
'0024D770':('Presentation.RuntimeEligibilityAndInstanceResolution','Complete body evaluates typed presentation-instance eligibility/state and resolves Presentation-owned records through 003B0BF0/003B2CA0.'),
'0024E2F0':('Presentation.RuntimeEligibilityAndInstanceResolution','Complete body searches typed presentation instance chains and validates IDs through Presentation-owned resolver 003B0BF0; also directly called by two Presentation owners.'),
'002561C0':('Presentation.Camera.CAM7ResourceLoader','Complete body validates magic 0x374D4143 (little-endian CAM7), allocates parsed record arrays, and builds pointer tables from the resource image.'),
'0028D460':('Presentation.EffectGeometry.NativeImplementation','Complete body constructs/updates effect geometry from indexed coordinates and repeatedly acquires Presentation-owned runtime objects via 003F0040/003F1290.'),
'002D81D0':('Presentation.ResourceHandleTable.NativeImplementation','Complete body allocates a slot in a bounded global handle table, updates resource-handle bitfields/records, and is directly called by three Presentation owners.'),
'0035D0E0':('UI.RuntimeTreeTraversalCleanup','Complete body selects UI-state predicates, walks a global tree recursively through 0035D280, conditionally releases nodes, and is directly invoked by two UI owners.'),
'0035D280':('UI.RuntimeTreeTraversalCleanup','Complete body recursively traverses child links, applies a predicate, conditionally releases a node, and is the recursive worker of UI-driven 0035D0E0.'),
'0036B980':('Runtime.ImageAddressStructuredRelocation','Complete body validates/relocates a packed structure and repeatedly uses runtime image-address encode/decode primitives; semantics are relocation/fixup rather than generic scheduling.'),
'0036F550':('Presentation.VFXRuntimeInitialization','Complete body initializes a large VFX/presentation global state block and is directly entered by VFXSystem_RenderLayerPass before Presentation-owned processing.'),
'00374FD0':('CoreRuntimeScheduling.TableStateMaintenance','Complete body scans up to 32 runtime table entries, evaluates per-type flags, and invokes a state-maintenance primitive; directly called by three CoreRuntimeScheduling owners including MainLoop_UpdateAndRenderFrame.'),
'00394B70':('Presentation.Geometry.IndexedCoordinateExpansion','Complete body expands ushort indexed 2D coordinates into float output positions using presentation-scale constants; called by multiple Presentation owners.'),
'00395780':('Presentation.Geometry.TransformNormalizeKernel','Complete body applies matrix/vector transforms and repeated normalization via sqrtf over geometry arrays; directly called by five Presentation owners.'),
'00395CF0':('Presentation.Geometry.TransformNormalizeKernel','Complete body applies matrix/vector transforms and repeated normalization via sqrtf over geometry arrays; directly called by five Presentation owners.'),
'00396560':('Presentation.Geometry.TransformNormalizeKernel','Complete body applies matrix/vector transforms and repeated normalization via sqrtf over geometry arrays; directly called by five Presentation owners.'),
'00396A30':('Presentation.Geometry.TransformNormalizeKernel','Complete body applies matrix/vector transforms and repeated normalization via sqrtf over geometry arrays; directly called by five Presentation owners.'),
'0039BB60':('Runtime.ImageAddressRecordFixup','Complete body walks packed records, converts pointers through RuntimePointer_EncodeImageAddress/ImageAddress_ResolveRuntimePointer, and marks fixed-up fields.'),
'003AE9C0':('Runtime.Sort.FloatKeyPointerArray','Complete body is an in-place quicksort/insertion-sort hybrid over pointer arrays ordered by float field +0x1c; classified from algorithm body, not Presentation caller proximity.'),
'003F1E90':('ActorEntity.StateInterpolation.NativeImplementation','Complete body advances actor state/timers and interpolates multiple actor transform/state fields using ActorEntity-owned helpers 00271380/002713E0.'),
'00400AC0':('ActorEntity.RuntimeListMaintenance','Complete body resolves packed actor handles, finds/reorders linked-list records, and updates per-actor state flags using ActorEntity-owned helpers.'),
'0046BAC0':('ActorEntity.ManagerPopulationFiltering','Complete body iterates actor-manager record ranges, filters actors by class/state flags, and builds packed actor record selections using ActorEntity-owned manager helpers.'),
'0059A3B0':('Phyre.Middleware.SerializationRenderingIntegration','Complete body allocates/copies middleware state and invokes established Phyre reflection object traversal from a Phyre post-processing caller.'),
'0059E300':('Phyre.Middleware.SerializationRenderingIntegration','Complete body orchestrates numerous established Phyre serialization/reflection/rendering routines with CFG-safe indirect calls and middleware memory management.'),
'0059F500':('Phyre.Middleware.SerializationRenderingIntegration','Complete body is an internal worker called from the Phyre serialization/rendering orchestration at 0059E300 and operates on the same middleware-managed structure.'),
'00629AA0':('Presentation.EffectFont.BindingAndMaterialization','Complete body validates four Presentation effect/font resources via established materialization consumers and updates their bound runtime handles through callback slots.'),
'007FFEE0':('Media.Video.WebM_MKV.ObjectCleanup','Complete body destroys a dynamic list of polymorphic media/parser objects and frees its storage; called by established WebM/MKV implementation functions.'),
'008001B0':('Media.Video.WebM_MKV.ObjectCleanup','Complete body recursively frees WebM/MKV parser-owned object arrays/substructures and calls 007FFEE0; directly called by established WebM/MKV implementation.'),
'00808D78':('Microsoft.MSVCCRT.ExecutableStartup','Complete body is the MSVC CRT executable startup sequence: initialize CRT, startup lock, initterm, TLS atexit registration, WinMain command line, exit/cexit, and CRT uninitialize.'),
}
out=Path('/tmp/gfz_v121_evidence/V121_CU_SEMANTIC_CLOSURE_PRE_ENRICH.tsv')
with out.open('w') as f:
 f.write('entry\tdomain\tevidence\n')
 for a,(d,e) in rows.items(): f.write(f'{a}\t{d}\t{e}\n')
print(out, len(rows))
