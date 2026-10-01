"""DD owner-read checks for the three 15-Input pages (SWE2-DATA, 2026-09-30). Static, the certified image.

CC  call chain (input-stack page, new 'Call chain' section): every edge is a raw rel32 call/jmp/jcc site found by a
    byte scan of .text (no function list), from the site to the target.
    Controls: CC+ the known edge 001950BA -> 00198000 (Initialize -> LoadKeymapIni) is found; CC- an edge that does not
    exist (0035F420 -> 00198000) is not.
IV  InputManager_Initialize (00195060): either validator returning 1 branches to 00198B60 (the defaults installer);
    only both returning 0 reach 00195DF0. The validators return 1 on failure: 00196550 on a duplicate code
    (001965CF mov al,1), 001965E0 when no profile has all 28 ids in range (0019667B sete al).
PC  r2 page: 020927C8 gates the play clock - its one reader 00254CC0 skips the clock update while it is non-zero.
    Control: the rip sweep over 020927C8 finds the known area-change setter store 00252DF5.
EV  capability page: event ids 0x2001 / 0x2009 / 0x2031 are ready / magic_ready / ability_ready in FABLE's event-slot
    census (bt4-event-motion-slots/event-slot-names.tsv); control: 0x2033 is steal (that record's own control).
B21 capability page: aggregate bit 21's two consumers test it (00228380 at 002283DA, 00229AF0 at 00229B03).
"""
import csv, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, secs, BASE, dis, raw_rip_refs, owner  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


t = [s for s in secs if s[0] == ".text"][0]
_, va, vs, ro, rs = t
blob = d[ro:ro + rs]
EDGES = {}
for p in range(len(blob) - 6):
    b0 = blob[p]
    if b0 in (0xE8, 0xE9):
        EDGES.setdefault(BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0], set()).add(BASE + va + p)
    elif b0 == 0x0F and 0x80 <= blob[p + 1] <= 0x8F:
        EDGES.setdefault(BASE + va + p + 6 + struct.unpack_from("<i", blob, p + 2)[0], set()).add(BASE + va + p)


def edge(site, target):
    return site in EDGES.get(target, ())


check("CC+ control: 001950BA -> 00198000 found", edge(0x001950BA, 0x00198000))
check("CC- control: no site of 0035F420 calls 00198000",
      not any(0x0035F420 <= s < 0x0035F420 + 0x168 for s in EDGES.get(0x00198000, ())))
CHAIN = [
    (0x0035ED2B, 0x0035FCA0, "UpdateFrame -> UpdateRegisteredChannels"),
    (0x0035FD85, 0x0035F420, "UpdateRegisteredChannels -> PollAndBuildChannelHistory"),
    (0x0035FD8D, 0x0035F690, "UpdateRegisteredChannels -> AdvanceChannelTimingState"),
    (0x0035F467, 0x00862670, "poll -> bridge"),
    (0x00862673, 0x001E09B0, "bridge -> InputAPI_PollControlState (jmp)"),
    (0x001E09D3, 0x00196FF0, "InputAPI -> InputManager_PollAndBuildControlState (jmp)"),
    (0x0019702D, 0x007999E0, "manager poll -> InputSystem_UpdateRegisteredDevices"),
    (0x0035F517, 0x0035FAC0, "poll -> ConvertButtonMaskToTransitions (first)"),
    (0x0035F529, 0x0035F760, "poll -> NormalizeAnalogAndComputeTransitions (second)"),
    (0x0035FBB8, 0x0035FBD0, "digital builder -> repeat filter"),
    (0x0035FA6B, 0x0035FBD0, "analog builder -> repeat filter"),
    (0x0035F548, 0x0035F590, "poll -> UpdateDeviceFeedbackOutput"),
    (0x0019877E, 0x00195060, "CreateSingleton -> Initialize"),
    (0x001950B2, 0x00197EE0, "Initialize -> BuildKeymapPath"),
    (0x001950C2, 0x00196550, "Initialize -> ValidateBindingUniqueness"),
    (0x001950CE, 0x001965E0, "Initialize -> ValidateBindingIdRanges"),
    (0x001950EB, 0x00198B60, "Initialize -> defaults installer (either validator failed)"),
    (0x001950DA, 0x00195DF0, "Initialize -> publisher (both passed)"),
]
for s, tg, what in CHAIN:
    check("CC %08X -> %08X %s" % (s, tg, what), edge(s, tg))

b = {x.address: x for x in dis(0x00195060)}
check("IV1 Initialize: uniqueness != 0 -> 001950E8 (defaults installer); ranges != 0 -> the same",
      b[0x001950C9].op_str == "0x1950e8" and b[0x001950D5].op_str == "0x1950e8" and b[0x001950EB].op_str == "0x198b60")
u = {x.address: x for x in dis(0x00196550)}
check("IV2 ValidateBindingUniqueness returns 1 on a duplicate (001965A6 je -> 001965D4 mov al, 1)",
      u[0x001965A6].op_str == "0x1965cf" and u[0x001965D4].op_str == "al, 1" and u[0x001965C7].op_str == "al, al")
r = {x.address: x for x in dis(0x001965E0)}
check("IV3 ValidateBindingIdRanges returns 1 when no profile reaches 28 in-range ids (cmp edx, 0x1c / sete al)",
      r[0x00196663].op_str == "edx, 0x1c" and r[0x0019667B].mnemonic == "sete")

refs = raw_rip_refs(0x020927C8, 0x020927CC)
sites = sorted((a, m) for a, m, o, tt in refs)
print("   020927C8 rip references: %s" % " ".join("%08X %s" % (a, m) for a, m in sites))
check("PC0 control: the sweep finds the area-change setter store 00252DF5", any(a == 0x00252DF5 for a, _ in sites))
readers = [a for a, m, o, tt in refs if m == "cmp"]
check("PC1 the only read is 00254CC4 (cmp) in 00254CC0", readers == [0x00254CC4] and owner(0x00254CC4) == 0x00254CC0)
c = {x.address: x for x in dis(0x00254CC0)}
check("PC2 00254CC0 skips the clock update while the word is non-zero (00254CCB jne 00254DC9 = the epilogue)",
      c[0x00254CCB].op_str == "0x254dc9" and c[0x00254CF8].op_str.startswith("qword ptr [rdi + 0x10]"))

TSV = os.path.join(HERE, "..", "bt4-event-motion-slots", "event-slot-names.tsv")
names = {row["kind2_event"]: row["name"] for row in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t")}
check("EV0 control: 0x2033 is steal in the census", names.get("0x2033") == "steal")
check("EV1 0x2001 ready, 0x2009 magic_ready, 0x2031 ability_ready",
      (names.get("0x2001"), names.get("0x2009"), names.get("0x2031")) == ("ready", "magic_ready", "ability_ready"),
      str((names.get("0x2001"), names.get("0x2009"), names.get("0x2031"))))

a = {x.address: x for x in dis(0x00228380)}
bb = {x.address: x for x in dis(0x00229AF0)}
check("B21 both consumers test bit 21 of the aggregate (002283DA bt esi, 0x15; 00229B03 bt eax, 0x15)",
      a[0x002283DA].op_str == "esi, 0x15" and bb[0x00229B03].op_str == "eax, 0x15")
print("FAILS %d" % FAILS)
