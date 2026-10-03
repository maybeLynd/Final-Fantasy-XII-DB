"""apply_types.py [--apply] - OPUS's type-store share of SWE2-AUDIT-SPEC's L2 expansion (AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003
(a)), 2026-10-03. Without --apply it reports which declarations are present (exit 0 when all are).

Each declaration was re-read at the bytes before it was written here (README); three of SPEC's census notes were corrected
on the way: 01EF93FC is initialised (1.0f by 0036D990/0036D9E0), not a pure constant; 0208E680 is the battle_pack.bin
blob POINTER the licence contract names, not `licenceOwnedBits` (that is BattleStatsRecord +0x194, already declared);
AiOrderSet's static route at 02089378 already existed.

Refuses to write while types.tsv or fields.tsv carry uncommitted edits that are not its own (another lane's work)."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types"))
REC = "opus-l2exp-types-1003"
TAG = "DECLARED 2026-10-03 (OPUS, AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003 (a); %s)" % REC

# type, size, category, instance, allocation_site, ctor, dtor, readiness, confidence, level, evidence, documents, route
NEW_TYPES = [
    ("Vf00ConstantVector", "0x10", "00-Engine-Core-Runtime", "single static instance at 0x01EF93F0",
     "IMAGE 0x01EF93F0 - .data; no allocation call",
     "0036D990 and 0036D9E0 each store (0, 0, 0, 1.0f): qword +0x0 = 0, dword +0x8 = 0, f32 +0xC = 1.0f (01CEBBA8)",
     "none - static storage", "TYPE RESOLVED", "PROVEN", "L1",
     TAG + ": the emulated VU0 vf00 constant; +0xC is read by 174 rip-relative sites (e.g. 0024AEA4 movss) and written "
     "only by the two initialisers", "00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md", "STATIC 0x01EF93F0"),
    ("SpawnCounterRow", "0x80", "05-Spawn-Encounter-Lifecycle",
     "two rows (count 2) of the spawn-counter table at 0x0208D354 (= 02089340 + 0x4014), selected by the bank toggle byte 0208D454 (002339B5 load, 002339C1 xor 1, 002339C6 store); 002339CC lea rax,[0208D354], 002339D3 shl rdi,7",
     "IMAGE 0x0208D354 - BSS; no allocation call", "none recovered", "none - static storage", "TYPE RESOLVED", "PROVEN",
     "L1", TAG + ": the table the battle-unit construction contract names as the spawn-counter table; the row stride 0x80 "
     "is the shift at 002339D3; the index is the toggle byte (0 or 1), and the two rows end exactly at it (0208D354 + 2 * 0x80 = 0208D454); 002339E2 rep stosw fills the selected row with 0x40 words of 1", "04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md",
     "ARRAY 0x0208D354 stride=0x80 count=2"),
    ("SpawnArcDegrees", "0x4", "05-Spawn-Encounter-Lifecycle", "single static instance at 0x02089358",
     "IMAGE 0x02089358 - BSS", "0023A520 stores 0xB4 (180); 0023A1F0 stores a truncated float (script verb 0050F470)",
     "none - static storage", "TYPE RESOLVED", "PROVEN", "L1",
     TAG + ": the candidate-heading arc width arcDeg; read only by 00234AF0 (00234B27)",
     "05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md", "STATIC 0x02089358"),
    ("CapabilityRow12Cell", "0x8", "05-Spawn-Encounter-Lifecycle",
     "single static at 0x0215F1F0 (= 0215F1C0 + 0x30, capability row 12; the qword spans rows 12 and 13)",
     "IMAGE 0x0215F1F0 - BSS", "written whole by 002E069C and 002E158E (qword stores)", "none - static storage",
     "TYPE RESOLVED", "HIGH", "L1",
     TAG + ": capability row 12 as the group-completion contract names it; both writers store the qword",
     "05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md", "STATIC 0x0215F1F0"),
    ("GroupCompletionBytes0209A2C4", "0x4", "05-Spawn-Encounter-Lifecycle", "single static instance at 0x0209A2C4",
     "IMAGE 0x0209A2C4 - BSS", "002670D7 stores the dword, 002670DD stores word +0 = 0x100; byte stores at 0025AB15 and "
     "others", "none - static storage", "TYPE RESOLVED", "HIGH", "L1",
     TAG + ": the group-completion contract names byte 0209A2C4[2] (= 0209A2C6), read signed by 0026E02F",
     "05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md", "STATIC 0x0209A2C4"),
    ("CameraContext", "0x860", "17-Presentation-Rendering",
     "two contexts at 0x02097D20, stride 0x860 (0025A6BE lea rax,[02097D20]; 0025A6CB imul r15,rdi,0x860)",
     "IMAGE 0x02097D20 - BSS", "none recovered", "none - static storage", "STRIDE RESOLVED", "HIGH", "L1",
     TAG + ": camera context 0, which the party-focus contract's teardown writes (two 0xB0 blocks and the +0x850 float); "
     "the interior layout beyond that is not measured", "11-Party/CONTRACT-party-focus-and-control-suppression.md",
     "ARRAY 0x02097D20 stride=0x860 count=2"),
    ("GlobalFrameTick", "0x4", "00-Engine-Core-Runtime", "single static instance at 0x0208F570",
     "IMAGE 0x0208F570 - BSS", "stored by 0022819C (and five more dword stores)", "none - static storage", "TYPE RESOLVED",
     "PROVEN", "L1", TAG + ": the global tick the per-frame update gate reads; 149 rip-relative dword accesses (143 reads, "
     "6 writes), e.g. 00228738", "00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md", "STATIC 0x0208F570"),
    ("BootHandshakeWord", "0x4", "00-Engine-Core-Runtime", "single static instance at 0x02EBA3F8",
     "IMAGE 0x02EBA3F8 - BSS", "24 dword stores", "none - static storage", "TYPE RESOLVED", "PROVEN", "L1",
     TAG + ": the word the boot frame spin-waits on at 0022B720 (battle-runtime-mode contract, I-10); 62 dword accesses "
     "(38 reads, 24 writes), e.g. 0022A850", "00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md", "STATIC 0x02EBA3F8"),
    ("AchievementManager", "0x80", "20-Platform-Online-Achievements", "single heap instance at *(0x01F83450)",
     "HEAP 0x80 bytes, 0020CD30: 00210EC0(0x80) when *(01F83450) is null", "0020C730 (0020CD6B), pointer stored at 0020CD71",
     "0020CD80: 00809950 then *(01F83450) = 0 (0020CDED)", "TYPE RESOLVED", "PROVEN", "L1",
     TAG + ": the steam-integration contract's achievement manager",
     "20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md", "PTR 0x01F83450"),
    ("BattlePackBlobPointer", "0x8", "02-Resource-And-Asset-Pipeline", "single static instance at 0x0208E680",
     "IMAGE 0x0208E680 - BSS, the cell right after BattleRuntimeUnitRecord's second bank",
     "bound on delivery by 00238850", "the prior blob is released through 00384500 and the cell rewritten (002369A3..002369B4)",
     "TYPE RESOLVED", "PROVEN", "L1",
     TAG + ": the battle_pack.bin blob pointer the licence and authored-table contracts name; 45 qword accesses. "
     "Not licenceOwnedBits (that is BattleStatsRecord +0x194, already declared)",
     "12-Items-Equipment-Shops-License/CONTRACT-license-check.md", "STATIC 0x0208E680"),
    ("ResourceSectionHeader", "0x30", "02-Resource-And-Asset-Pipeline",
     "the header of each section in a loaded resource, matched by 00409C30", "INTERIOR - inside a loaded resource image",
     "none - read in place", "none", "TYPE RESOLVED", "PROVEN", "L1",
     TAG + ": 00409C30 compares dword +0x00 with the tag (0 and 0x4C4C4140 match any) and eight dwords +0x10..+0x2C with "
     "the 32-byte name key; the extent is the matched fields", "02-Resource-And-Asset-Pipeline/CONTRACT-resource-section-addressing.md",
     ""),
    ("ActionDefinition", "AUTHORED the st2e table's row stride (header word +0x08)", "07-Combat-Action",
     "rows of the st2e action table whose header is *(0x02EBF138): row = 0020E600(header +0x0C) + stride * id "
     "(0030D19B..0030D1E9)", "INTERIOR - the battle_pack.bin blob", "none - authored data", "none", "PARTIAL", "PROVEN", "L1",
     TAG + ": the action row the element-scaling contract names; only +0x13 is declared here",
     "08-Combat-Formula/CONTRACT-environmental-element-scaling.md", ""),
    ('StaticFloat02EBF000', '0x4', '17-Presentation-Rendering', 'single static instance at 0x02EBF000', 'IMAGE 0x02EBF000 - .data past raw data, so .bss, zero at load; no allocation call', '0039AF20 stores it (0039AF27 movss); its only caller 0039CD50 passes 512.0 (0039CD8C movss xmm0,[008C5B48]; call at 0039CD94), reached once from the boot init 00259180 (002591C3)', 'none - static storage', 'TYPE RESOLVED', 'HIGH', 'L1', TAG + ': a scalar float, not a registry slot. The one rip-relative access is the 4-byte movss store 0039AF27; no rip-relative reader, lea or image pointer reaches 02EBF000..02EBF007. Extent 4: 02EBF004 is unreferenced and 02EBF008 begins AuthoredTableRegistrySlot; 02EBEFF8/02EBEFFC are separate floats (0039AED0) after RenderCommandBufferPair 02EBEFC0+0x34 (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)', '02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md; 17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md', 'STATIC 0x02EBF000'),
    ('Record02EC19C0', '0x8', '00-Engine-Core-Runtime', '0x02EC19C0 + index * 8, 512 records (02EC19C0..02EC29C0); index = word +0x20 of a node on the list at qword 02EC3D60, or the loop counter of 002FCFF0/002FC200', 'IMAGE 0x02EC19C0 - .data past raw data, so .bss; zeroed whole by 002FC200 (002FC2C6 memset 0x1000)', '002FC200 (memset 0x1000 at 002FC2C6, then word +4 low 0x1F from byte table 01EEBB10 for indices 0..0x18F, 002FC2E4/002FC2EE); 002FCFF0 (dword +0 = 0032E400(0xB or 0x26, index) for all 0x200 indices, 002FD02F)', 'none - static storage', 'STRIDE RESOLVED', 'PROVEN', 'L1', TAG + ': extent 0x1000 from the memset 002FC2C0/002FC2C6, flush with the next object 02EC29C0 (memset 0x914 at 002FC564/002FC570); stride 8 from every indexed access (002FC2E4, 002FC4F3, 002FC8B4, 002FCB07, 002FC9E2, 002FCB4A, 002FCD68) and the 002FCFF0 walk (002FD031 +8, 0x200 iterations 002FD00D/002FD035). The group-completion contract names 02EC19C0 as the end of SpawnGroupLedger (64 x 0x18 from 02EC13C0) (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)', '05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md; 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md', 'ARRAY 0x02EC19C0 stride=0x8 count=512'),
]
# type, offset, size, name, ctype, meaning, readiness, confidence, evidence
NEW_FIELDS = [
    ("SpawnCounterRow", "0x000", "128", "counters", "uint16[64]", "64 word counters; the row the toggle selects is reset to 1 each (002339DA mov eax,1; 002339E2 rep stosw, ecx 0x40)", "TYPE RESOLVED", "PROVEN", TAG),
    ("Vf00ConstantVector", "0x000", "8", "xy", "f32[2]", "0.0, 0.0 (stored as a zero qword by 0036D9B0 / 0036D9F0)", "TYPE RESOLVED", "PROVEN", TAG),
    ("Vf00ConstantVector", "0x008", "4", "z", "f32", "0.0 (0036D9BB / 0036D9FB)", "TYPE RESOLVED", "PROVEN", TAG),
    ("Vf00ConstantVector", "0x00C", "4", "w", "f32", "1.0f, loaded from 01CEBBA8 (0036D9A8 / 0036D9E8); read by 174 sites", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("SpawnArcDegrees", "0x000", "4", "arcDeg", "int32", "candidate heading arc width in degrees; default 180 (0023A550)", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("CapabilityRow12Cell", "0x000", "8", "capabilityRows12And13", "u64", "capability rows 12 and 13 of the table at 0215F1C0, stored together (002E069C, 002E158E)", "TYPE RESOLVED", "HIGH", TAG),
    ("GroupCompletionBytes0209A2C4", "0x002", "1", "groupCompletionByte2", "int8", "the byte the group-completion contract names (0209A2C4[2]); read with movsx by 0026E02F", "TYPE RESOLVED", "HIGH", TAG),
    ("GlobalFrameTick", "0x000", "4", "tick", "uint32", "the global tick (per-frame update gate)", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("BootHandshakeWord", "0x000", "4", "handshake", "uint32", "the boot frame spin-waits on it (0022B720)", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("AchievementManager", "0x000", "8", "gameId", "u64", "compared with each callback's +0x00 (steam-integration contract)", "SEMANTICALLY IDENTIFIED", "HIGH", TAG),
    ("AchievementManager", "0x008", "8", "entries", "SteamAchievementRecord*", "the entry array, stride 0x198", "SEMANTICALLY IDENTIFIED", "HIGH", TAG),
    ("AchievementManager", "0x010", "4", "count", "uint32", "entry count (41)", "SEMANTICALLY IDENTIFIED", "HIGH", TAG),
    ("AchievementManager", "0x014", "4", "achievedCount", "uint32", "achieved count", "SEMANTICALLY IDENTIFIED", "HIGH", TAG),
    ("BattlePackBlobPointer", "0x000", "8", "blob", "u8*", "the loaded battle_pack.bin blob; released through 00384500", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("ResourceSectionHeader", "0x000", "4", "tag", "uint32", "section kind tag; 0 and 0x4C4C4140 in the query match any (00409C30..00409C3E)", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("ResourceSectionHeader", "0x010", "32", "nameKey", "u8[32]", "32-byte section name key, compared as eight dwords (00409C45..00409C8A)", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ("ActionDefinition", "0x013", "1", "elementMask", "uint8", "element bits: 0x01 Fire, 0x02 Lightning, 0x04 Ice, 0x08 Earth, 0x10 Water, 0x20 Wind (test byte [rcx+0x13],1 at 0038B295)", "SEMANTICALLY IDENTIFIED", "PROVEN", TAG),
    ('StaticFloat02EBF000', '0x000', '4', 'value000', 'float', '512.0 stored once at boot (0039AF27, from 0039CD50); no reader found; meaning not claimed (how-a-position-becomes-a-single-number.md calls it a screen distance in write-only globals)', 'TYPE RESOLVED', 'HIGH', TAG + ': 0039AF27 movss store; 0039CD8C loads 512.0 from 008C5B48; 0039CD94 call (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)'),
    ('Record02EC19C0', '0x000', '4', 'field00', 'int32', 'the per-index result of 0032E400(code, index), code 0xB or 0x26 by 002DEBB0(); 002FC860 copies it to node +0x1C and takes its positive path when it is above 0 (signed test). Meaning not claimed', 'TYPE RESOLVED', 'PROVEN', TAG + ': 002FD02F store; 002FC8B4 read, 002FC8B7 copy, 002FC8BA/002FC8BC test + jg; 002FC8BE element 0 (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)'),
    ('Record02EC19C0', '0x004', '2', 'field04', 'u16', 'low 0x1F = byte table 01EEBB10[index] & 0x1F for indices 0..0x18F, summed over the 02EC3D60 list by four readers; value 0x20 read as a flag by 002FCB40, no writer of it found; meaning not claimed', 'TYPE RESOLVED', 'HIGH', TAG + ': 002FC2E4 and 0xFFE0, 002FC2EE or; reads 002FC4F3, 002FCB07, 002FC9E2, 002FCD68 (each & 0x1F); 002FCB4A/002FCB4E/002FCB51 value 0x20 (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)'),
    ('Record02EC19C0', '0x006', '2', 'unobserved06', 'u8[2]', 'no access found; meaning not claimed', 'DISCOVERED', 'HIGH', TAG + ": no instruction among the seven 02EC19C0/02EC19C4 references' functions touches +6/+7 (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)"),
    ('GroupCompletionBytes0209A2C4', '0x000', '1', 'groupCompletionByte0', 'int8', 'a 0/1 flag: one of the four bytes the gate 0026DFB0 ANDs (passes only when each has 0x1); cleared by the init 00266D10 (dword 0x01010101 then word 0x100 leave +0 = 0); set by 0025AB15 (1), 0026BC62 and the indexed setter 0026BD20 (index 0); cleared by 0025D674 and 00268E41; meaning beyond the gate not claimed', 'TYPE RESOLVED', 'PROVEN', TAG + ': writers 0025AB15, 0025D674, 00268E41, 0026BC62, 0026BD2F (index 0), 002670D7/002670DD; reader 0026E026 movsx; gate 0026E01F..0026E044; 00262C60..00262C70 skips index 0 (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)'),
    ('GroupCompletionBytes0209A2C4', '0x001', '1', 'groupCompletionByte1', 'int8', 'a 0/1 flag ANDed by the same gate; set to 1 by the init word 0x100 (002670DD); meaning not claimed', 'TYPE RESOLVED', 'PROVEN', TAG + ': writers 0026BD42 setne, 002670DD, 0026BD2F (index 1), 00262C65 (loop); readers 00265460, 0026E038 (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)'),
    ('GroupCompletionBytes0209A2C4', '0x003', '1', 'groupCompletionByte3', 'int8', 'a 0/1 flag ANDed by the same gate; 1 after the init dword 0x01010101; meaning not claimed', 'TYPE RESOLVED', 'PROVEN', TAG + ': writers 002670D7, 0026BD2F (index 3), 00262C65 (loop); reader 0026E01F (second pass 2026-10-03: measured by repos-91, a local helper; anchors re-read by OPUS)'),
]


def foreign_edits():
    r = subprocess.run(["git", "-C", TYPES, "diff", "--name-only", "--", "types.tsv", "fields.tsv"], capture_output=True,
                       text=True)
    names = [n for n in r.stdout.split() if n]
    if not names:
        return []
    d = subprocess.run(["git", "-C", TYPES, "diff", "--", "types.tsv", "fields.tsv"], capture_output=True, text=True).stdout
    own = [l for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
    return [l for l in own if REC not in l]


def run(apply):
    tt = io.open(os.path.join(TYPES, "types.tsv"), encoding="utf-8", newline="").read()
    ft = io.open(os.path.join(TYPES, "fields.tsv"), encoding="utf-8", newline="").read()
    # 2026-10-03: compare whole rows, not just presence - a corrected tuple (SpawnCounterRow count=2) used to stay
    # stale on the store while the check printed FAILS 0. A differing row that is this record's (carries TAG) is
    # rewritten on --apply; one that is not is another lane's row and is reported, never touched.
    def sync(text, wanted, keylen):
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.rstrip("\r\n").split(nl)
        at = {tuple(l.split("\t")[:keylen]): i for i, l in enumerate(lines)}
        miss, stale, foreign = [], [], []
        for w in wanted:
            k, row = tuple(w[:keylen]), "\t".join(w)
            if k not in at:
                miss.append(w)
            elif lines[at[k]] != row:
                (stale if TAG in lines[at[k]] else foreign).append((at[k], row, " ".join(k)))
        if apply:
            for i, row, _k in stale:
                lines[i] = row
            lines += ["\t".join(w) for w in miss]
        return nl.join(lines) + nl, miss, stale, foreign

    tt2, miss_t, stale_t, foreign_t = sync(tt, NEW_TYPES, 1)
    ft2, miss_f, stale_f, foreign_f = sync(ft, NEW_FIELDS, 2)
    missing = [w[0] for w in miss_t] + ["%s (stale row)" % k for _i, _r, k in stale_t]
    missing_f = [w[0] + " " + w[1] for w in miss_f] + ["%s (stale row)" % k for _i, _r, k in stale_f]
    for _i, _r, k in foreign_t + foreign_f:
        print("CONFLICT %s: the store's row is another lane's and differs from this record" % k)
    if apply and (missing or missing_f):
        fe = foreign_edits()
        if fe:
            raise SystemExit("REFUSED: types.tsv/fields.tsv carry %d uncommitted lines that are not this record's "
                             "(another lane's work); publish or wait first" % len(fe))
        if tt2 != tt:
            io.open(os.path.join(TYPES, "types.tsv"), "w", encoding="utf-8", newline="").write(tt2)
        if ft2 != ft:
            io.open(os.path.join(TYPES, "fields.tsv"), "w", encoding="utf-8", newline="").write(ft2)
        missing, missing_f = [], []
    missing += ["CONFLICT " + k for _i, _r, k in foreign_t]
    missing_f += ["CONFLICT " + k for _i, _r, k in foreign_f]
    for m in missing:
        print("NOT DECLARED type", m)
    for m in missing_f:
        print("NOT DECLARED field", m)
    print("checks %d types + %d fields  FAILS %d" % (len(NEW_TYPES), len(NEW_FIELDS), len(missing) + len(missing_f)))
    return 1 if (missing or missing_f) else 0


if __name__ == "__main__":
    sys.exit(run("--apply" in sys.argv))
