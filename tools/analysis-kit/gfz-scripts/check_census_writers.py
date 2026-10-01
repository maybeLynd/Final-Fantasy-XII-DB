#!/usr/bin/env python3
"""Can each access census see the type's own constructor?

A census seeded on record-RETURNING accessors reaches consumers and structurally
cannot reach producers: a constructor never receives the record from a getter, it is
upstream of one. So such a census is excellent at readers and blind to the very
functions that establish field meanings.

That is not a hypothesis. Every type in `_types/` that declares a `ctor` has that
constructor ABSENT from its own census - three of three when this was written -
and the effect is visible in the data: `ActorStorageRecord +0x03` shows 89 reads and
zero writes although the carver stamps it twice.

Why it matters enough to have a checker. Two claims were published from these censuses
and withdrawn: "no writer found" on `ActorManagerSlot +0x48` and `+0x60`, and a phantom
`ActorStorageRecord +0x044` split off a real qword pointer. Both were the same error -
treating good READ coverage as coverage. This makes the limit measurable per census so
nobody has to rediscover it by being wrong.

The ctor/alloc test is definitive where the store declares one. Where it does not, the
read/write split is printed as an advisory signal only: a census with few writes from
few functions is suspect, but a type that genuinely is mostly read looks the same, so
the number is never reported as a verdict.

    check_census_writers.py
"""
import collections
import glob
import io
import re
import os
import sys

FIELD_HEADER = "function	name	site	disp	kind	instruction	route	note"

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
DB = os.path.join(ROOT, "Database", "FFXII TZA")

# A census file names its type only by convention, so the mapping is explicit.
# An unmapped census is REPORTED, never silently skipped - a new one appearing
# unnoticed is how a blind spot stays hidden.
ADDR = re.compile(r"\b(00[0-9A-Fa-f]{6})\b")

CENSUS_TYPE = {
    "actor-storage-record-accesses.tsv": "ActorStorageRecord",
    "actor-manager-record-accesses.tsv": "ActorManagerSlot",
    "character-render-record-accesses.tsv": "CharacterRenderRecord",
    "character-render-system-tail-accesses.tsv": "CharacterRenderSystemTail",
    "spawn-record-accesses.tsv": "SpawnRecord",
    "character-render-object-accesses.tsv": "CharacterRenderObject",
    "game-setting-config-accesses.tsv": "GameSettingConfig",
    "battle-unit-accesses.tsv": "BattleUnit",
    "battle-stats-record-accesses.tsv": "BattleStatsRecord",
    "battle-state-block-accesses.tsv": "BattleSystemState",
    "result-record-accesses.tsv": "BattleResultRecord",
    "save-header-accesses.tsv": "SaveImageHeader",
    "save-payload-accesses.tsv": "SavePayload",
    "movement-context-accesses.tsv": "MovementContext",
    "secondary-context-accesses.tsv": "SecondaryContext",
    "evaluation-context-accesses.tsv": "EvaluationContext",
    "formula-scratch-block-accesses.tsv": None,
    # MAPPED 2026-09-14 (OPUS). Both were listed under "UNMAPPED censuses (add them to
    # CENSUS_TYPE)" every run, which is a to-do printed by a gate rather than a finding:
    # two censuses were not scored AT ALL, so their write coverage was neither good nor
    # bad but absent. Both types exist in `_types/types.tsv` with a declared site -
    # SteeringRecord allocation_site 00269FA3, BattleFormulaScratch ctor 003849B0 - so
    # mapping them makes them testable, and the outcome was not known when this was
    # written. SteeringRecord's ctor is PROSE ("its owning context's initialisation"),
    # so it falls to the NOT TESTABLE list on that half by the rule already here.
    "steering-record-accesses.tsv": "SteeringRecord",
    "battle-formula-scratch-accesses.tsv": "BattleFormulaScratch",
    # MAPPED 2026-09-24 (SWE2-STRUCT). Both censuses name their type by the same
    # convention the map already encodes: the slot file is route-seeded to the
    # declared IMAGE array (02098E10 stride 0x288 count 5) and now carries the
    # ctor's rows, the entry file is the 0x18 sub-record's census. ActorManager-
    # SlotEntry's ctor cell names FUN_003DA400/FUN_003DD230 in prose, so it lands
    # on the NOT TESTABLE half by the rule already here.
    "actor-manager-slot-accesses.tsv": "ActorManagerSlot",
    "actor-manager-slot-entry-accesses.tsv": "ActorManagerSlotEntry",
    # MAPPED 2026-09-24 (SWE2-STRUCT). Every filename names its store type by the
    # same convention the existing entries encode; each census's displacement
    # range was checked against the declared extent before mapping. The cells
    # they expose were read from the shipping bytes: real constructors got their
    # rows appended, alloc-only and orchestrator sites are filed under
    # EXPECTED_ABSENCE with a body-read reason, and ctor cells that cite a
    # non-field-writing function were reworded to prose in types.tsv.
    "boot-singleton-01f7f598-accesses.tsv": "BootSingleton01F7F598",
    "manager-singleton-0209be80-accesses.tsv": "ManagerSingleton0209BE80",
    "manager-sub-0209be80-00a0-accesses.tsv": "ManagerSub0209BE80_00A0",
    "manager-sub-0209be80-57e0-accesses.tsv": "ManagerSub0209BE80_57E0",
    "manager-sub-0209be80-7ea0-accesses.tsv": "ManagerSub0209BE80_7EA0",
    "manager-sub-0209be80-7fb0-accesses.tsv": "ManagerSub0209BE80_7FB0",
    "manager-sub-0209be80-8fa0-accesses.tsv": "ManagerSub0209BE80_8FA0",
    "manager-sub-0209be80-a0d0-accesses.tsv": "ManagerSub0209BE80_A0D0",
    "manager-sub-0209be80-ab30-accesses.tsv": "ManagerSub0209BE80_AB30",
    "manager-sub-57e0-array-record-accesses.tsv": "ManagerSub0209BE80_57E0ArrayRecord",
    "party-read-machine-record-accesses.tsv": "PartyReadMachineRecord",
    "party-read-machine-record-second-instance-accesses.tsv": "PartyReadMachineRecord",
    "image-address-arena-record-accesses.tsv": "ImageAddressArenaRecord",
    "secondary-context-element-accesses.tsv": "SecondaryContextElement",
    # "record-rip" is the rip-absolute sibling of the canonical slot census.
    "actor-manager-record-rip-accesses.tsv": "ActorManagerSlot",
    "actor-sequence-descriptor-accesses.tsv": "ActorSequenceDescriptor",
    "battle-target-buffer-accesses.tsv": "BattleTargetBuffer",
    "battle-target-result-entry-accesses.tsv": "BattleTargetResultEntry",
    "navigation-path-state-accesses.tsv": "NavigationPathState",
    "spawn-group-ledger-accesses.tsv": "SpawnGroupLedger",
    # No store type exists for the locomotion angle context - the census's disp
    # column is "ctx+0xN" and predates any declaration. Mapping it to None keeps
    # it unscoreable rather than guessed.
    "locomotion-angle-accesses.tsv": None,
    "gambit-config-accesses.tsv": "GambitConfig",
    "party-roster-slots-accesses.tsv": "PartyRosterSlots",
    "item-class-descriptor-accesses.tsv": "ItemClassDescriptor",
    "world-loot-pickup-node-accesses.tsv": "WorldLootPickupNode",
    "input-binding-profile-accesses.tsv": "InputBindingProfile",
    "input-binding-record-accesses.tsv": "InputBindingRecord",
    "text-draw-state-accesses.tsv": "TextDrawState",
    # Several widget types exist; this census is the base Widget - its routes
    # read "widget rcx proc-abi" and it contains ctor 002465F0.
    "widget-accesses.tsv": "Widget",
    "render-model-instance-accesses.tsv": "RenderModelInstance",
    "render-model-instance-container-accesses.tsv": "RenderModelInstanceContainer",
    "legacy-ps2gs-texture-context-accesses.tsv": "LegacyPs2GsTextureContext",
    "frame-marker-singleton-accesses.tsv": "FrameMarkerSingleton01F82C80",
    "postprocess-context-accesses.tsv": "PostProcessParamContext",
    "chunked-slot-bank-entry-accesses.tsv": "ChunkedSlotBankEntry",
    "chunked-slot-entry-accesses.tsv": "ChunkedSlotEntry",
    "pending-completion-queue-01f81248-accesses.tsv": "PendingCompletionQueue01F81248",
    "render-resource-root-accesses.tsv": "RenderResourceRoot",
    "spawn-keep-image-accesses.tsv": "SpawnKeepImage",
    "achievement-descriptor-accesses.tsv": "AchievementDescriptor",
    "image-backed-state-block-accesses.tsv": "ImageBackedStateBlock",
    "mt19937-state-accesses.tsv": "Mt19937State",
    "shared-gameplay-lcg-state-accesses.tsv": "SharedGameplayLcgState",
}


FUNCS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "work", "graph", "functions.tsv")
_RANGES = None


def containing(va):
    """The entry address of the function containing `va`, uppercase hex, or None."""
    global _RANGES
    if _RANGES is None:
        _RANGES = []
        try:
            for n, l in enumerate(io.open(FUNCS, encoding="utf-8")):
                if not n:
                    continue
                c = l.rstrip("\n").split("\t")
                try:
                    _RANGES.append((int(c[0], 16), int(c[2]), c[0].upper()))
                except (ValueError, IndexError):
                    pass
        except OSError:
            _RANGES = []
    for e, sz, txt in _RANGES:
        if e <= va < e + max(sz, 1):
            return txt
    return None


# THE FIVE ALLOC-ONLY ROWS, READ FROM THE SHIPPING BYTES 2026-09-14 (OPUS), before the split above
# was made. A row is only filed as an expected absence because somebody read the function and found
# it does not address a field of the type - not because of its label.
EXPECTED_ABSENCE = {
    "003325E7": "CharacterRenderSystem_AllocateAndInitialize: mov ecx,0x48930 / call 0036A100, "
                "then stores the pointer into 022C6F20 and 022C6F28 and hands it on. Never "
                "addresses a field. Covers both rows that share this site.",
    "00269FA3": "FUN_00269f90: reads the OWNING context's +0xDC, shl 7 (the record's declared 0x80 "
                "size), add 0x120, and writes the slot pointer to [rcx+0xF0] - a field of the "
                "CONTEXT, not of the record.",
    "001BD527": "FUN_001bd4a0: mov ecx,0x668 / call 00210EC0, then call 001F4DA0(rax) - allocates "
                "and DELEGATES initialisation.",
    "0030E5D3": "BattleStats_ChangeStatusAndProcessSideEffects: lea rcx,[rsp+0x80] / xor edx,edx / "
                "mov r8d,0x148 / call 00861EC0 - a memset of a STACK buffer. The 'allocation site' "
                "is a stack frame and a bulk zero is not a field access.",
    "00236957": "BattleStorage_InitializeWorkArrays (body read 2026-09-24, SWE2-STRUCT): allocates "
                "0x9400 = 64 * 0x250 through tagged allocator 00384510, publishes to 0208E690 and "
                "memsets the pool - alloc-only, no per-record field write. Pool-side initial "
                "values come from the memset, not a constructor.",
    # READ 2026-09-24 (SWE2-STRUCT) for the manager-singleton mapping batch.
    "0028F8CF": "FUN_0028f8b0: mov ecx,0x10FD0 / call 00271420 (tagged alloc), publishes the "
                "pointer to 0209BE80 and calls ctor 00291750. Its only field writes land at "
                "parent +0xAA44/+0x10F68 - inside other sub-records' spans, not this one's.",
    "00189034": "FUN_00189000: mov ecx,0xDD8 / call allocator, then publishes the pointer and "
                "calls the object's constructor - alloc+publish+delegate, no field write.",
    "001BDA80": "FUN_001bda50: mov ecx,0x108 / call allocator, then call 001BC9D0 - allocates "
                "and DELEGATES initialisation; the body writes no field itself.",
    "0026E79E": "FUN_0026e760: mov ecx,0x240 / call 003EC8D0, then call ctor 002F6AB0 - "
                "allocates and delegates; no field write.",
    "00477EE0": "FUN_00477ee0 (body read 2026-09-24, SWE2-STRUCT): supplies the static .data "
                "index arrays as arguments to 0051F9F0 - argument plumbing; writes nothing "
                "inside the container.",
    "00210EC0": "FUN_00210ec0: malloc thunk - allocates and returns the block; never touches "
                "a field of what it produced.",
    "00D10460": "Not code - the .rdata AchievementDescriptor table itself; IMAGE storage, "
                "read-only by section, so no function can own it.",
}


def scan(db=DB, emit=None):
    """The whole measurement, with printing factored out.

    EXTRACTED 2026-09-14 (OPUS) so `check_nowriter_claims` can DERIVE the blind set instead of
    carrying a hand-copied list of it. That list had been seven types since September while the
    measured set grew to eleven, so a clean result there was a statement about seven elevenths of
    its own subject. `main()` prints from this function, so the two cannot diverge again.

    `emit` is called with each census's table row; passing None measures silently.
    -> (blind, unmapped, other, prose, tested)
    """
    meta = {}
    for n, line in enumerate(io.open(os.path.join(db, "_types", "types.tsv"),
                                     encoding="utf-8")):
        if not n:
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) > 6:
            meta[c[0]] = (c[4], c[5])          # allocation site, ctor

    blind, unmapped, other, prose, tested = [], [], [], [], 0
    expected = []
    for path in sorted(glob.glob(os.path.join(db, "**", "*-accesses.tsv"), recursive=True)):
        base = os.path.basename(path)
        head = io.open(path, encoding="utf-8").readline().rstrip("\n")
        if head != FIELD_HEADER:
            other.append((base, head))
            continue
        fns, reads, writes, wfns = set(), 0, 0, set()
        for n, line in enumerate(io.open(path, encoding="utf-8")):
            if not n:
                continue
            c = line.rstrip("\n").split("\t")
            if len(c) < 6:
                continue
            fns.add(c[0])
            if c[4] in ("w", "rw"):
                writes += 1
                wfns.add(c[0])
            elif c[4] == "r":
                reads += 1
        if emit:
            emit("  %-36s %5d %6d %6d %6d"
                 % (base[:36], len(fns), reads, writes, len(wfns)))
        fns_upper = set(x.upper() for x in fns)

        if base not in CENSUS_TYPE:
            unmapped.append(base)
            continue
        tname = CENSUS_TYPE[base]
        if not tname:
            continue
        alloc, ctor = meta.get(tname, ("UNRESOLVED", "UNRESOLVED"))
        for label, site in (("ctor", ctor), ("alloc", alloc)):
            if not site or site in ("UNRESOLVED", ""):
                continue
            # THE COLUMN IS NOT ALWAYS AN ADDRESS. "image storage at 02098E10", "the owning
            # record's initialisation", "the caller that builds the result" - a set of function
            # entry addresses can never contain any of those, so comparing the raw text reported
            # every one of them as a blind census. Six of ten findings were that. Extract an
            # address; test only when there is one; report the rest as what they are.
            addrs = ADDR.findall(site)
            if not addrs:
                prose.append((base, tname, label, site))
                continue
            # A CITED ADDRESS IS USUALLY AN INSTRUCTION, NOT AN ENTRY. The store cites the site of
            # the interesting instruction - "003325E7 mov ecx, 0x48930" - while a census's function
            # column holds function entries. Comparing them directly never matches even when the
            # function is present, so each address is mapped to its containing function first.
            want = set()
            for a in addrs:
                want.add(a.upper())
                owner = containing(int(a, 16))
                if owner:
                    want.add(owner)
            tested += 1
            if not (want & fns_upper):
                # AN ALLOCATION SITE IS NOT A CONSTRUCTOR. This file's claim is about a census that
                # cannot see its CONSTRUCTOR; an allocator produces storage and need not touch a
                # field of what it allocated, so its absence from a FIELD census is expected rather
                # than blind. All five alloc-only rows were read from the shipping bytes on
                # 2026-09-14 before this split was made - see expected_absence() below.
                # A ROW REACHES `expected` ONLY IF SOMEBODY READ IT. The first version of
                # this split routed every non-ctor row there and then printed "NOT READ -
                # filed on its label alone, which this file does not accept as a reason"
                # against two of them. If the reason is not accepted, the row does not
                # belong in the bucket: `BattleUnit` and `SpawnRecord` declare the SAME
                # address as ctor and allocator, and their allocator half is unread, so it
                # stays a finding until it is read.
                if label != "ctor" and addrs[0].upper() in EXPECTED_ABSENCE:
                    expected.append((base, tname, label, addrs[0]))
                else:
                    blind.append((base, tname, label, addrs[0]))
    return blind, unmapped, other, prose, tested, expected


def blind_types(db=DB):
    """The distinct TYPE NAMES whose census cannot see their constructor or allocator.

    Distinct types, not rows: `BattleUnit` and `SpawnRecord` are each blind on both their ctor and
    their allocator, so the row count is thirteen where the type count is eleven. A claim is about
    a type, so the type count is the one a claim checker wants.
    """
    return sorted({t for _base, t, _label, _site in scan(db)[0]})


def main():
    print("CENSUS WRITE COVERAGE")
    print("  %-36s %5s %6s %6s %6s" % ("census", "fns", "reads", "writes", "wrFns"))
    blind, unmapped, other, prose, tested, expected = scan(DB, emit=print)

    print()
    if other:
        print("  NOT FIELD CENSUSES - different schema, not scored:")
        for base, head in other:
            print("    %-36s header: %s" % (base, head))
        print("    Scoring these with the field-census columns reads addresses as function")
        print("    names and function names as access kinds, and reports a plausible zero.")
        print()
    if unmapped:
        print("  UNMAPPED censuses (add them to CENSUS_TYPE): %s" % ", ".join(unmapped))
        print()
    if prose:
        print("  NOT TESTABLE - the store names the constructor or allocation in prose rather than")
        print("  as an address, so there is no function to look for. A type whose storage is in the")
        print("  image, or whose producer is described rather than located, cannot fail this test:")
        for base, tname, label, site in prose:
            print("    %-36s %-22s %-5s %s" % (base[:36], tname[:22], label, site[:52]))
        print()
    print("  definitive tests possible: %d (a type must declare a ctor or allocation site)"
          % tested)
    if not blind:
        print("  every declared constructor appears in its own census.")
        return 0
    if expected:
        print("  EXPECTED ABSENCES - an ALLOCATION SITE is not a constructor: %d" % len(expected))
        print("  A field census records FIELD ACCESSES. An allocator produces storage and need not")
        print("  touch a field of what it allocated, so its absence is the census doing its job.")
        print("  Each of these was READ from the shipping bytes before it was filed here:")
        for base, tname, label, site in expected:
            why = EXPECTED_ABSENCE[site.upper()]
            print("    %-36s %s %s %s" % (base[:36], tname[:20], label, site))
            print("        %s" % why[:150])
        print()

    print("  CONSTRUCTORS ABSENT FROM THEIR OWN CENSUS: %d" % len(blind))
    for base, tname, label, site in blind:
        print("    %-36s %s %s %s is not among its functions" % (base, tname, label, site))
    print()
    print("  A census that cannot see its constructor cannot support ANY 'no writer found'")
    print("  claim about that type. Reads are covered; writes are not.")
    print()
    print("  MEASURED 2026-09-14 (OPUS): THE GAP IS REAL AND CURRENTLY UNEXERCISED.")
    print("  Searching all 589 documents for an absence claim - 'no writer', 'never written',")
    print("  'read-only', 'nothing initialises' - on a line naming one of these types found four")
    print("  matches and NOT ONE of them rests on a census:")
    print("    * character-render-object.md states a negative and BOUNDS IT in the next sentence")
    print("      - 'it rules out a direct, statically visible reference in either direction' -")
    print("      and names the constructor it read rather than inferring from absence;")
    print("    * battle-record-kind-byte.md's '+0xE68 is not written' is scoped to the kind-1")
    print("      path and cites the reset that leaves 0 (00236AC2);")
    print("    * the remaining match is a working note in an agent inbox, not a publication.")
    print("  So nothing is retracted. What follows is that these censuses must be completed")
    print("  BEFORE such a claim is made, not that an existing one is wrong. Re-run")
    print("  check_nowriter_claims.py to re-test that - and the gate runner now runs it every")
    print("  suite, so the clean result is re-established rather than remembered. It was named")
    print("  Tools/work/OPUS/nowriter_claims_blind_census.py until 2026-09-14, in a directory")
    print("  .gitignore excludes, so this line told every reader to run a file they did not have.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
