#!/usr/bin/env python3
# Generate pass-22 crossing-section bullets for SWE2-DATA's routed pages.
# Reads C:/tmp/p22-mine.json (produced by _swe2_p22_edges.py) and inserts one
# bullet per unaccounted (doc, subsystem) pair - at the end of an existing
# crossing section, else a new trailing section.
import io, os, re, sys, json, collections

DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
SEC = re.compile(
    r"^#{2,3} +(?:Cross-subsystem neighbours|Crossings into other layers)"
    r"[^\n]*\n.*?(?=^#{1,3} |\Z)", re.M | re.S)

READABLE = {
    "ActorEntity": "actor entity", "Audio": "audio", "CombatAI": "combat AI",
    "CombatAction": "combat action", "CombatFormula": "combat formula",
    "CoreRuntimeScheduling": "core runtime scheduling",
    "Gameplay": "gameplay", "Input": "input",
    "Items_Equipment_Shops_License": "items/equipment",
    "Movement": "movement", "Party": "party",
    "Platform": "platform",
    "PlatformOnlineAchievements": "platform/online achievements",
    "Presentation": "presentation/rendering",
    "Resource": "resource",
    "Rewards_Progression_Economy": "rewards/progression",
    "RNG_Random_Selection": "random selection",
    "Save_Load_Settings": "save/load/settings", "SaveLoad": "save/load",
    "Script_VM_Native_Bridge": "script VM / native bridge",
    "Spawn_Encounter_Lifecycle": "spawn/encounter",
    "Status_Periodic_Terminal": "status/periodic terminal",
    "Story_Event_Quest_Hunt": "story/event/quest", "StoryEvent": "story event",
    "UI": "UI", "World": "world", "WorldAreaField": "world area",
    "Application": "application", "Developer": "developer",
    "Combat": "combat", "Actor": "actor",
}

def top(edges, idx, n):
    c = collections.Counter(e[idx] for e in edges)
    return [a for a, _ in c.most_common(n)]

def bullet(sub, hits):
    rd = READABLE.get(sub, sub.replace("_", " ").lower())
    inc = [h for h in hits if h[1] == "caller"]   # neighbour calls subject
    out = [h for h in hits if h[1] == "callee"]   # subject calls neighbour
    cls = " and ".join(x for x, g in (("CLIENT", inc), ("SERVICE", out)) if g)
    parts = []
    if inc:
        sj = top(inc, 0, 3)
        ot = top(inc, 2, 3)
        parts.append("%s %s also called by bodies filed to %s: %s"
                     % ("`%s`" % "`, `".join(sj) if len(sj) > 1 else "`%s`" % sj[0],
                        "are" if len(sj) > 1 else "is",
                        rd, ", ".join("`%s`" % o for o in ot)
                        + (" (+%d more)" % (len({h[2] for h in inc}) - len(ot))
                           if len({h[2] for h in inc}) > len(ot) else "")))
    if out:
        sj = top(out, 0, 3)
        ot = top(out, 2, 3)
        parts.append("%s %s bodies filed to %s: %s"
                     % ("`%s`" % "`, `".join(sj) if len(sj) > 1 else "`%s`" % sj[0],
                        "reach" if len(sj) > 1 else "reaches",
                        rd, ", ".join("`%s`" % o for o in ot)
                        + (" (+%d more)" % (len({h[2] for h in out}) - len(ot))
                           if len({h[2] for h in out}) > len(ot) else "")))
    return ("- **%s - %s (%d edge%s).** %s - shared machinery across the layer "
            "boundary, no shared ownership."
            % (sub, cls, len(hits), "" if len(hits) == 1 else "s",
               "; ".join(parts)))

mine = json.load(open("C:/tmp/p22-mine.json", encoding="utf-8"))
apply = "--apply" in sys.argv
for doc, subs in sorted(mine.items()):
    if not subs:
        continue
    path = os.path.join(DB, *doc.split("/"))
    text = io.open(path, encoding="utf-8").read()
    bullets = [bullet(s, hits) for s, hits in sorted(subs.items())]
    ms = list(SEC.finditer(text))
    if ms:
        m = ms[-1]
        end = m.end()
        newtext = text[:end].rstrip("\n") + "\n" + "\n".join(bullets) + "\n" + text[end:]
        where = "extended"
    else:
        newtext = text.rstrip("\n") + (
            "\n\n## Cross-subsystem neighbours - SWE2-DATA (pass-22 dispositions, 2026-10-02)\n\n"
            + "\n".join(bullets) + "\n")
        where = "new section"
    if apply:
        io.open(path, "w", encoding="utf-8", newline="\n").write(newtext)
        print("PATCHED  %-72s %s (%d bullets)" % (doc, where, len(bullets)))
    else:
        print("WOULD    %-72s %s (%d bullets)" % (doc, where, len(bullets)))
        if len(sys.argv) > 1 and sys.argv[1] == "--show":
            for b in bullets:
                print("   ", b[:180])
