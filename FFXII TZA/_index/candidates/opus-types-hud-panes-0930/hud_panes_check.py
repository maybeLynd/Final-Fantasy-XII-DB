"""hud_panes_check.py - two battle-HUD blocks identified (OPUS, 2026-09-30): ManagerSub0209BE80_7FB0 is the level-up
blink controller (six 0x110 slot records, each a claim flag, a key and a three-entry queue feeding a 0xF0-byte blink
widget); ManagerSub0209BE80_8FA0 is the target-info window (a 0x1110-byte widget whose +0xAC0 sub-object owns the
TargetInfo layout widget).
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.

H1  the per-frame gate's group 0x0080 (0028E450: flag byte bit 7) calls 00296860(hud + 0x7FB0, 6) at 0028E459-0028E465.
H2  00296860 walks n records of 0x110 (rbx = obj + 0x104, `add rbx, 0x110`): when the record's claim flag (+0xF0) is set
    and its widget slot is free (00273A20), it builds a 0xF0-byte widget (00245000, then 00246AC0) with procedure
    00299D10 (lea r8 at 002968B5), passing the queue entry at the consumer cursor (+0xF8 + 4 * [+0x104]) and the key
    (+0xF4); it clears the entry, advances the cursor mod 3 and drops the claim when the next entry is empty.
H3  00299D10 is the widget whose layout key the layout-parameter page names LevelupBlinkSpeed (its timer-speed argument
    at 00299E7D) and whose per-row fade driver 00299FC0 resolves the entry through the actor getter 003588B0 - the
    queued value is an actor ordinal.
H4  the HUD constructor 00291750 builds ManagerSub0209BE80_8FA0 at hud + 0x8FA0 (002917AA-002917B1) through 002BE450: a
    0x1110-byte widget (00245000) with procedure 002BE490.
H5  the open / close router 002BE1A0(hud + 0x8FA0, mode, ..) is reached only through 0028FE40 / 0028FEA0 (each
    `add rcx, 0x8fa0` on [0209BE80]); mode 1 runs the teardown 002BEED0, any other mode 002BE300(hud + 0x8FA0 + 0xAC0),
    which tail-jumps to 002C0F30 when its record is live; 002C0F30 builds a 0x2B8-byte widget with procedure 002C0870 -
    the procedure the layout-parameter page binds to the TargetInfo* keys. 0028FEA0's caller is 0027B880, an arm of
    BattleMenu_UpdateCommandSelectionAndDispatch 002778C0.
Prints PASS/FAIL per check and FAILS n last.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


# H1
check("H1", txt(0x0028E450).startswith("test byte ptr [rip") and txt(0x0028E450).endswith(", 0x80")
      and txt(0x0028E459) == "lea rcx, [rbx + 0x7fb0]" and txt(0x0028E460) == "mov edx, 6" and txt(0x0028E465) == "call 0x296860"
      and sorted(set(c["calls"].get(0x00296860, ()))) == [(0x0028E290, 0x0028E465)],
      "group 0x0080 calls 00296860(hud + 0x7FB0, 6); its only caller")
# H2
proc = 0x002968BC + 0x3454
ok = txt(0x00296881) == "lea rbx, [rcx + 0x104]" and txt(0x00296897) == "cmp dword ptr [rbx - 0x14], ebp" \
    and txt(0x002968A3) == "call 0x273a20" and txt(0x002968C0) == "mov edx, 0xf0" and txt(0x002968B5) == "lea r8, [rip + 0x3454]" \
    and proc == 0x00299D10 and txt(0x002968C5) == "movsxd rcx, dword ptr [rbx + rax*4 - 0xc]" and txt(0x002968CA) == "mov eax, dword ptr [rbx - 0x10]" \
    and txt(0x002968DE) == "call 0x245000" and txt(0x002968E6) == "call 0x246ac0" \
    and txt(0x002968EF) == "mov dword ptr [rbx + rax*4 - 0xc], ebp" and txt(0x002968F3) == "inc word ptr [rbx]" \
    and txt(0x002968F6) == "cmp word ptr [rbx], 3" and txt(0x00296909) == "mov dword ptr [rbx - 0x14], ebp" \
    and txt(0x0029690C) == "add rbx, 0x110"
check("H2", ok, "records of 0x110: claim +0xF0, key +0xF4, queue +0xF8 (3 dwords), cursor +0x104 (mod 3); widget 0xF0 with procedure %08X" % proc)
# H3 - the procedure's layout key and its actor resolve, as the layout page reads them
doc = open(os.path.join(HERE, "..", "..", "..", "16-UI", "Layout-Parameter-System", "ui-layout-parameters-and-editor-schema.md"),
           encoding="utf-8").read()
hud = open(os.path.join(HERE, "..", "..", "..", "16-UI", "Battle-Hud", "the-battle-hud-layout-readers.md"), encoding="utf-8").read()
ok = "| `LevelupBlink…` | 1 | `00299D10` P |" in doc and "`00299D10` P (level-up blink) | `LevelupBlinkSpeed`" in hud \
    and "`00299FC0` (221 B) is the per-row fade driver `00299D10` ticks: `003588B0` resolves `dword[rcx+0xC4]`" in doc
check("H3", ok, "00299D10 = the LevelupBlink layout procedure (layout pages); its fade driver resolves the entry via 003588B0")
# H4
check("H4", txt(0x002917AA) == "lea rcx, [rdi + 0x8fa0]" and txt(0x002917B1) == "call 0x2be450"
      and txt(0x002BE459) == "lea r8, [rip + 0x30]" and 0x002BE460 + 0x30 == 0x002BE490 and txt(0x002BE460) == "mov edx, 0x1110"
      and txt(0x002BE465) == "call 0x245000" and sorted(set(c["calls"].get(0x002BE450, ()))) == [(0x00291750, 0x002917B1)],
      "00291750 builds hud + 0x8FA0 as a 0x1110-byte widget with procedure 002BE490")
# H5
ok = txt(0x0028FE7E) == "add rcx, 0x8fa0" and txt(0x0028FEDD) == "add rcx, 0x8fa0"     and sorted(set(c["calls"].get(0x002BE1A0, ()))) == [(0x0028FE40, 0x0028FE94), (0x0028FEA0, 0x0028FEF3)]     and txt(0x002BE1D3) == "cmp esi, 1" and txt(0x002BE1DB) == "call 0x2beed0" and txt(0x002BE1FF) == "lea rcx, [rbx + 0xac0]"     and txt(0x002BE431) == "jmp 0x2c0f30" and txt(0x002C0F5A) == "lea r8, [rip - 0x6f1]" and 0x002C0F61 - 0x6F1 == 0x002C0870     and txt(0x002C0F7D) == "mov edx, 0x2b8" and txt(0x002C0F8A) == "call 0x245000"     and "| `TargetInfo…` | 1 | `002C0870` P |" in doc     and sorted(set(c["calls"].get(0x0028FEA0, ()))) == [(0x0027B880, 0x0027BA8B)] and sorted({f for f, _ in c["calls"].get(0x0027B880, ())}) == [0x002778C0]
check("H5", ok, "002BE1A0 opens (002BE300 -> 002C0F30: TargetInfo widget, procedure 002C0870) or closes (mode 1: 002BEED0) the pane; "
      "reached from the battle menu (002778C0 -> 0027B880 -> 0028FEA0) and 0028FE40")
print("FAILS %d" % fails)
