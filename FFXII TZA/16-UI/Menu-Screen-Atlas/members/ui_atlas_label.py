"""ui_atlas_label.py IN.tsv OUT.tsv: relabel an atlas TSV (from ui_atlas.py) with the full key-family -> screen map, keeping the
menu-screen labels; child propagation is re-run on the relabelled rows (installer inside a labelled procedure's subtree)."""
import sys, collections
FAM = [
    ({"BattleCommand", "BtlCommand", "BattleMist", "BattleMenu", "CPCWindow", "BattleNum", "GambitPosition"}, "battle command menu"),
    ({"HpGauge"}, "party HP gauge"), ({"BossGauge"}, "boss gauge"),
    ({"NumEffect", "ExpLp", "LpNum", "ExpNum", "ExpEffect", "EXPLPNumOffsetX", "EXPLPNumOffsetY"}, "damage / EXP / LP numbers"),
    ({"MsgWin", "MessageWin", "NobuMessage", "NobuMsg", "TalkingMessage", "SystemWindow", "MessageLine"}, "message window"),
    ({"OverHead", "NAOverHeadTextOffsetY"}, "overhead name text"), ({"PauseMenu"}, "pause menu"), ({"TargetInfo"}, "target info"),
    ({"ActiveLog"}, "battle log"), ({"TrackMap", "ExtraTrack"}, "track map"), ({"LocaMap", "ExtraLoca", "BaseMap"}, "location map"),
    ({"ScrollBar", "ScrollTable", "ScrollUp", "ScrollDown", "ScrollMark", "ScrollList"}, "scroll bar / list"),
    ({"MenuList", "CommandMenu", "ListHelp", "ListItem"}, "menu list"), ({"StatusAlone"}, "status window"),
    ({"MaskTop", "MaskBottom", "MaskGradation"}, "screen mask"), ({"NgSignal"}, "NG signal"), ({"LevelupBlink"}, "level-up blink"),
    ({"AutoWindow"}, "auto window"), ({"HelpMessage", "TriangleHelp"}, "help message"), ({"ActionList"}, "action list"),
    ({"SilhouettePos", "SilhouetteWidth"}, "silhouette"), ({"2DSideCursorCenterX", "2DSideCursorCenterY"}, "2D side cursor"),
]
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1], encoding="utf-8")]
head, body = rows[0], rows[1:]
for r in body:
    if r[3] != "-" and "child" not in r[3]: continue
    ks = set(r[6].split(",")) if r[6] != "-" else set()
    labs = [name for fams, name in FAM if ks & fams]
    if labs: r[3] = " + ".join(labs[:2])
    elif "child" in r[3]: r[3] = "-"
with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
    f.write("\t".join(head) + "\n")
    for r in body: f.write("\t".join(r) + "\n")
print(collections.Counter(r[3] for r in body).most_common())
