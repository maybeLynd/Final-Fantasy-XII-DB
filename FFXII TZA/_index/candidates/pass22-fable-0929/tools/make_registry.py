"""Write registry_rows.tsv (neighbour-dispositions.tsv's 7-column format) for the pairs FABLE routes to the
registry, then prove the instrument's own loader accepts every row (control: audit_crossrefs.load_dispositions
over a scratch copy that holds only these rows)."""
import io, json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rebuild_edges  # noqa: F401  (puts the kit on sys.path)
import audit_crossrefs as ac

pairs = json.load(io.open(r"C:/x/p22/fable_pairs.json", encoding="utf-8"))
det = {(p[1], p[2]): p[3] for p in pairs}

BP = "01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md"
RIG = "17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md"
SLC = "17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md"
POSE = "17-Presentation-Rendering/Model-And-Motion-Formats/the-pose-sequencer.md"
PHY = "22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md"

BUSY = ("003601B0 (14 B: mov eax,1; shl eax,cl; or [022CB720],eax; ret) and 003601C0 (16 B, the same with not/and) "
        "set and clear one bit of the busy dword 022CB720, which the per-frame check 00360120 tests as a whole "
        "(00360129); each caller owns its own bit. This page's verbs use bit 0x13 (its row B1).")
OWN_BUSY = ("Reading of the helper: 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md "
            "(Interior citation - frontier hub 003601B0; EX-8 item 1).")
rows = [
 (BP, "ActorEntity",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (bodies and call sites read). " + BUSY +
  " ActorEntity's area unload 002628B0 sets bit 0xB (00262BA3/00262BA8). A shared one-hot flag helper, no actor "
  "relationship of the party verbs. " + OWN_BUSY),
 (BP, "Audio",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (bodies and call sites read). " + BUSY +
  " Audio's music-change body 003614E0 sets bit 6 after storing [022CBA58] (003615EC/003615F1); 00361460 clears "
  "bit 6 and zeroes [022CBA58] (00361464-0036146E). Another owner's bit of the same word, no audio relationship "
  "of the party verbs. " + OWN_BUSY),
 (BP, "WorldAreaField",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (bodies and call sites read). " + BUSY +
  " WorldTransition_StageFieldTransition 003145E0 sets bit 0xC (00314639/0031463E). Another owner's bit of the "
  "same word, no world relationship of the party verbs. " + OWN_BUSY),
 (RIG, "UI",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (bodies read). 7 edges: UI bodies 00247AE0, 002D2600, "
  "002D28E0, 00368010, 003C5500, 003F26F0, 003F2A70 call 00203170 (44 B, 84 callers), four movups stores of the "
  "identity rows (1,0,0,0)..(0,0,0,1) from 008C5F80/008C5F90/008C5FB0/008C5FD0 to [rcx] - an identity-matrix "
  "initialiser the rig's 005188C0 also calls. 1 edge: UI 0035DCC0 calls 0036DD80 (15 B, 47 callers), which "
  "stores (0,0,0,1) from 008C5FD0 into the software vf00 cell 01EF93F0 "
  "(00-Engine-Core-Runtime/CONTRACT-transform-primitives.md lists it among that lane's three writers). Shared "
  "transform-workbench leaves; no UI relationship of the rig."),
 (SLC, "Input",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (body and call site read). "
  "InputGameplay_ArbitrateDigitalInputAndModalState 00253C70 calls 001EDE70 (7 B, 22 callers: mov eax,[01F82E38]; "
  "ret - the raw 60-fps gate) at 00253D8F, the second of two tests before it clears 0209E5B4. The page cites the "
  "same getter as the angle setters' one-way read; one more reader of a process-wide frame-rate flag. The gate is "
  "decoded in 16-UI/Widget-Object-Model/CONTRACT-widget-object.md (The two globals); the rig page records the "
  "same edge as Input - MECHANICAL (SWE2-EC7-156)."),
 (POSE, "Movement",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (body and call site read). "
  "WorldActor_UpdateRuntimeAndScriptExecutionState 0025DF00 calls 001EDE80 (61 B, 7 callers) at 0025DFA9 and "
  "branches forward to 0025E12B on 0. 001EDE80 returns 1 unless half-rate holds ([01F82E38]!=0, [01DFE0C0]==0), "
  "else 0022A080()+0022A030() (001EDE84-001EDEA7): the step count the page's step routine also reads (its "
  "Core runtime scheduling paragraph, row Q5). Group 2 of 00-Engine-Core-Runtime/Per-Frame-Update-Gate/"
  "one-word-decides-which-fifteen-subsystems-tick.md owns the reading. No movement relationship of the sequencer."),
 (POSE, "UI",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (body and call site read). 003FA790 calls 001EDE80 at "
  "003FA7F8 and skips its call to 003FC170 on 0. Same shared step-count getter as the Movement row: 1 unless "
  "half-rate, else the sum of two frame counters; owned by group 2 of 00-Engine-Core-Runtime/Per-Frame-Update-Gate/"
  "one-word-decides-which-fifteen-subsystems-tick.md. No UI relationship of the sequencer."),
 (PHY, "CoreRuntimeScheduling",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (body and call sites read). The render pass list 00187950 "
  "calls 001A1470 (93 B, 35 callers) three times with the heap singleton [01F7F4C0] and size 0x10 (00187AB5, "
  "00187AFE, 00187B4F). The body rounds the size to 16, bumps the cursor [rcx+8] and wraps to the base [rcx] past "
  "[rcx+0x10] (001A147A-001A14CC): the ring/bump allocator the textbook new sequences in "
  "00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md call. Allocation only; no scheduling "
  "relationship of the post-effect family."),
 (PHY, "Platform",
  "FABLE 2026-09-29 (pass-22 debt): MECHANICAL, tier 1 (body and call sites read). D3D11 backend bodies 0061F200, "
  "0061F710, 006209C0, 006239C0 call 005FD050 (129 B, 55 callers), the magic-static getter returning the object "
  "at 02CC0410 (005FD065-005FD0CB), and take [+0x108] or [+0x110] off it (0061F289/0061F299, 0061F74B, 006209F6, "
  "00623A25). The same singleton this page's CON-197 row reads; the backend's buffer and view creation is not "
  "part of the post-effect family. Reading of the getter: 00-Engine-Core-Runtime/Object-Model/"
  "vtable-method-index.md (Interior citation - frontier hub 005FD050)."),
]

out = r"C:/x/p22/drafts/registry_rows.tsv"
lines = []
for doc, sub, note in rows:
    d = det[(doc, sub)]
    n = int(d.split(" ", 1)[0])
    detail = d.split("never mentioned: ", 1)[1]
    assert "\t" not in note and "|" not in note
    lines.append("\t".join([doc, sub, str(n), "unaccounted", detail, "GENUINELY-IRRELEVANT", note]))
with io.open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
print("wrote %d rows to %s" % (len(lines), out))

# control: the instrument's loader must accept each row as a disposition
tmp = tempfile.mkdtemp(prefix="p22reg_", dir=os.environ.get("TEMP"))
os.makedirs(os.path.join(tmp, "_index", "candidates"))
with io.open(os.path.join(tmp, ac.DISPOSITION_FILE), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")
ok, unknown = ac.load_dispositions(tmp)
want = {(doc, sub) for doc, sub, _ in rows}
print("loader accepted %d of %d; unknown verdicts %d; all keys match: %s"
      % (len(ok), len(rows), len(unknown), set(ok) == want))
