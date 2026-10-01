"""awn_a_checks.py - SWE2-CONTRACT for OPUS, 2026-10-01: wave A of SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS.

For every correction this record applies, it asserts on the target file that
  (a) the review's new wording is present (whitespace-normalised, so a line wrap does not matter),
  (b) the replaced original is kept struck (~~original~~) and does not survive anywhere unstruck,
  (c) the dated note naming the review is beside it.
Negative and structural checks:
  T*  every table row this record edited still has its header's column count (no pipe leaked into a cell);
  L*  every review link the notes add resolves to the review file;
  B1  the blocked `_types` cell is untouched (its replacement is proposed in the README, not applied);
  X1  each review's original wording is genuinely gone from the unstruck text of its target, checked against the
      git HEAD copy (the original was present at HEAD, so the check can fail).
Static, text-only; reads the working tree and `git show HEAD:<path>`. Prints PASS/FAIL lines and `FAILS <n>`.
"""
import io
import os
import re
import subprocess
import sys

DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
C = "_index/candidates/"
FAILS = 0


def check(label, ok, msg):
    global FAILS
    print("%s  %s %s" % ("PASS" if ok else "FAIL", label, msg))
    if not ok:
        FAILS += 1


def read(rel):
    return io.open(os.path.join(DB, rel), encoding="utf-8", newline="").read()


def head(rel):
    r = subprocess.run(["git", "show", "HEAD:./" + rel], cwd=DB, capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def unstruck(s):
    return re.sub(r"~~.*?~~", " ", norm(s))


NOTE = "narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review]("

# (label, file, original replaced (or None when the wording only adds), new wording, review id)
A = [
    ("SD1-1", C + "sd1-force-fight-enemy-consumers-0930/README.md", "(a kind-1-only branch at `00305BA5`)",
     "(`00305BA5`, reached by both kinds; the test at `00305B7D` diverts only a kind-1 unit whose status word has bit 27 set)", "sd1"),
    ("SD1-2", C + "sd1-force-fight-enemy-consumers-0930/README.md", "The flag has two readers (UQ-152)",
     "The flag has two consumer readers (UQ-152); the second writer `00252C80` also reads its old value at `00252C94`", "sd1"),
    ("P6-1", C + "text-gap-append-0930/README.md",
     "**Four addresses are interior to real `.pdata` extents of bodies the list cuts short:** `00808ED9`, `00121E11`, `0015AE4A`, and `0036F22E` (a chained fragment).",
     "**Four addresses decode as code inside bodies the list cuts short:** `00121E11` is the second byte of `jmp $` at `00121E10` after the `ret` at "
     "`00121E0E`, `0036F22E` is `mov eax, edi` in the epilogue ending `ret` at `0036F23A`, `00808ED9` and `0015AE4A` are epilogue instructions.",
     "pass6-opus-rows"),
    ("GR1-1", C + "gr1-wait-slot-settled-0930/README.md",
     "**Every read has a covering write in its command's begin handler or earlier in the same handler.**",
     "**Every read is preceded by the same command's own write.** For 24 of the 38 command-reads the write is on every path (in the reading "
     "function, or in a begin that writes on every path). For the other 14 (0/512, 0/1051-0/1053, def/43, 44, 87, 93 and 94), the begin writes "
     "on one path only and records it in a guard: `[r8+5]` for `00343A30`, `[r8+8]` for `00343B00`, the sign of `[r8]` for `0050CA40`. The "
     "reader tests the guard first.", "gr1"),
    ("GR1-2", C + "gr1-wait-slot-settled-0930/README.md", None,
     "The phase byte `+0x15` is written only by the interpreter (wait arming / clears), the slot reset `0025D460`, `002621D0` and the VMResult "
     "writers. The handlers never write it. So a command starts at phase 0 unless an opcode is abandoned mid-execution, which is not traced here.",
     "gr1"),
    ("GR1-3", C + "gr1-wait-slot-settled-0930/README.md", None,
     "(one, `00342910`, is a loop-widening artefact: its byte stores reach slot `+0x1C..+0x1F`)", "gr1"),
    ("GR7-1", C + "gr7-kind10-reader-0930/README.md",
     "The other `+0xB90` accesses in the image, in `00172750`, `001728C0`, `00177A70`, `00186800`, `004B8F20` and `0070A7F0`, are outside the "
     "battle layer. The battle-unit census does not type them as battle units, and they were not re-typed here.",
     "The other `+0xB90` accesses in the image are in `00172750`, `001728C0`, `00177A70` (fragment `00177B71`), `00186800`, `00186CD0`, "
     "`004B8F20`, `0052D1E7`, `0054FE00`, `0070A7F0` (fragments `0070A83C` / `0070A894`), `00791E70` and `007D44BC`. The raw disp32 census "
     "covers every width and form, and none of these bases is a BattleUnit (the review record types each one). A reader through a biased base "
     "(a unit pointer plus a folded offset) or a bulk copy of a unit is outside any displacement census.", "gr7"),
    ("GR7-2", C + "gr7-kind10-reader-0930/README.md", None,
     "and the full 0xF50 clear of the slot on allocate (`002344D2`, `memset(slot, 0, 0xF50)` in `00234480`), which has no displacement.", "gr7"),
    ("GR7-3", C + "gr7-kind10-reader-0930/README.md", None,
     "The gambit rebuild `00328140` writes row word `+8+2e` into entry e's {mode, opcode} word, so K6 reads the evaluator's opcode byte. The 256 "
     "rows are identical in all nine language packs.", "gr7"),
    ("GR45-1", C + "gr4-gr5-action-row-readers-0930/README.md", "There are 722 qword loads of `02EBF138` by rip, in 129 functions.",
     "There are 719 distinct qword loads of `02EBF138` by rip (retool counts 722 because `00305133`, `0030514F` and `0030515E` lie in both of "
     "the overlapping extents `00305080` and `00305110`)", "gr45"),
    ("GR45-2", C + "gr4-gr5-action-row-readers-0930/README.md", None,
     "This control exercises the call-argument hand-off (11 of the 232 sites need a call hop). No site depends on the return route or on outgoing "
     "stack arguments, so those two routes have no positive control in this image.", "gr45"),
    ("GR45-3", C + "gr4-gr5-action-row-readers-0930/README.md", "`00328360` to `002FCBF0`",
     "`0030CBE0` passes it through ~~`00328360` to `002FCBF0`~~ `00328360` → `0042FCE0` → `002FCBF0` (two tail jumps)", "gr45"),
    ("GR45-4", C + "gr4-gr5-action-row-readers-0930/README.md", None,
     "Conditional tail calls (a jcc to another function) are not handed tags. There is one in the walked set, `002E809A` → `00426FA0`, and it "
     "carries only the header in r8, which is not read.", "gr45"),
    ("GR1315-1", C + "gr13-15-shop-list-widget-0930/README.md", "They call the target's own procedure.",
     "They call the list control's procedure (`002D2DB0`, `002D279E` / `002D2B5C`), which forwards message 26 to the procedure of the control's "
     "`+0xC8` (`002D2E11`–`002D2E29`). For the shop's list control, that is the driver `0056D370`: it is set at creation from the layout "
     "loader's owner argument (`0056D776` → `002432CB` → `0029F9AC` → `002D16B0`). The driver sends message 26 to the stub (`0056D3B8`).",
     "gr13-15"),
    ("GR17-1", C + "gr17-reward-table-lifetime-0930/README.md", "135 of the 383 functions that can reach `00312280` are address-taken",
     "135 of the 382 functions that can reach `00312280` (383 counting `00312280` itself, which is not address-taken) are address-taken", "gr17"),
    ("GR17-2", C + "gr17-reward-table-lifetime-0930/README.md", None,
     "Conditional tail jumps (jcc) were also checked: none leaves a framed function, and the jcc edges from frameless leaves add only the "
     "address-taken leaves `002E7090` / `002E70C0` (a review finding, `auditspec-review-gr17-0930/gr17_jccfix.out`)", "gr17"),
    ("CRT-1", C + "opus-dd-crt-0930/README.md", "constructs two empty MSVC strings at `+0x20` and `+0x40`",
     "initialises two MSVC strings and fills the one at `+0x20` from the caller's key string (`001A4C90`, source `[r8]`, `0071E39F`; the call "
     "is `0071E3A2 call 0x1a4c90`); the one at `+0x40` is left empty (capacity 15, size 0): key copied, default mapped value", "dd-crt"),
    ("ANIM-1", "22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md",
     "The shipped data uses it four times, all for node visibility (`BM-4`, the section below), so no shipped light, camera, face or material "
     "is animated this way.",
     "The shipped Phyre cluster data uses it four times, all for node visibility (`BM-4`, the section below), so no light, camera, face or "
     "material is animated through the authored channel-target route. A binding built natively at run time would not appear in that census.",
     "dd-anim"),
    ("ANIM-2", C + "opus-dd-crt-0930/batch2-animation.md", None,
     "binding built natively at run time would not appear in that census", "dd-anim"),
    ("W1599-1", "16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md", "203 functions at 240 sites",
     "the factory `00244F50`: ~~203 functions at 240 sites~~ 247 call/jmp sites in 206 functions at HEAD (UQ-190 counted 240 in 203 on the "
     "2026-09-17 function list)", "dd-1599-a"),
    ("SD100-1", C + "sd100-reveal-modes-0930/README.md",
     "`+0x9B += +0x9C`; each 30 steps `+0x90` by `+0xA0`. When a line is full, it pages through `002ABB20`: automatically when the step `+0xA0` "
     "> 1, otherwise only when `00248F20` answers 1. It then restores the `0x7D00` budget.",
     "`+0x9B += +0x9C`. When the speed `+0x9C` is 30, it scrolls through `002ABB20`, which advances the head `+0x8C` to the next line or `#` "
     "page wait, and snaps `+0x90` to the head with no lag. It does this when `+0xA0` > 1, or when `00248F20` answers 1 (the mode query "
     "`00229EA0` is not 2). Otherwise, each time `+0x9B` reaches 30, the head `+0x8C` advances by `+0xA0`, the lag `+0x9D` moves by `+0xA0` "
     "toward `+0x9E`, and `+0x90` steps by `+0xA0` while it is at most `+0x8C - +0x9D`. `0x7D00` is an upper clamp on `+0x8C`.", "sd100"),
    ("SD100-2a", C + "sd100-reveal-modes-0930/README.md", "a timed stretch that types a step per tick, then normal typing",
     "it exits at once if `+0x88` is already 0", "sd100"),
    ("SD100-2b", C + "sd100-reveal-modes-0930/README.md", "typing at the authored rate, with no paging",
     "catches the reveal up to the head at the rate", "sd100"),
    ("SD100-2c", C + "sd100-reveal-modes-0930/README.md", None,
     "catches the reveal up to the head at a step per tick", "sd100"),
    ("SD100-3a", C + "sd100-reveal-modes-0930/README.md", None,
     "the pager `002A9980` (`002A9A27`, `dil` = 0 after `002A9A00 xor edi, edi`), the setter `002B3950` (`002B3963`, `al` = 0 after "
     "`002B395A xor eax, eax`) and `002A6F80` (`002A6FB3`, through window `+0x180`)", "sd100"),
    ("SD100-3b", C + "sd100-reveal-modes-0930/README.md", None,
     "the message-window procedure `002A6190` (`002A6606`, through window `+0x180`, the old mode saved at `+0x181`)", "sd100"),
    ("SD100-3c", C + "sd100-reveal-modes-0930/README.md", None,
     "`002AC5F0` on its stack copy of the element (`002ADBC2`, `(dword & 0xFFF7FF04) or 4`)", "sd100"),
    ("SD100-3d", C + "sd100-reveal-modes-0930/README.md",
     "the pager `002A9980` (`002A9A27`, from `dil`) and the setter `002B3950` (`002B3963`, from `al`)",
     "| restore | `002A5F40` (`002A5FE8`) swaps the byte saved at `+0x181` back in, unless the mode is 2 or 4", "sd100"),
    ("SD100-4", C + "sd100-reveal-modes-0930/README.md",
     "**`002B3950` and the pager's variable store** set the mode from a value their callers supply. The callers are not traced.",
     "The writers are complete for stores addressed as `[element + 0xB0]` (any width or base, image-wide) and through the window's `+0xD0` "
     "element and the stack elements of `002A5460`, `002B3050`, `002B5390`, `002A1B00` and `002AC5F0` (SWE2-AUDIT-SPEC review). Elements "
     "reached through shifted pointers, `memcpy` copies, and the elements handed to `002A8C50` / `002A9980` by pointer are not swept.", "sd100"),
    ("SD105-1", C + "sd105-reveal-inputs-0930/README.md",
     "`002B32D0` writes it: 0.125 with the default bound, one lag unit per fade step. The message-window run builder `002A4830` copies `+0x50` "
     "wholesale from its source record.",
     "Two code paths compute it: the wrapper `002B32D0` (`002B33F0`, after the base fill's `+0x9E` = 8, so 0.125), and the markup parser's `\"` "
     "tag (`0F 22`) in `002A8C50`. That tag first sets `+0x9E` to its second payload byte & 0x1F (`003FFEE0` at `002A9456`), then stores "
     "`+0x50` (`002A947A`). At text position 0 it also sets `+0x90` = −(s8)`+0x9E` and `+0x9D` = 0 (`002A94B4`..`002A94C1`). Element copies "
     "(`002A4830` and others) carry `+0x50` across unchanged.", "sd105"),
    ("SD105-2a", C + "sd105-reveal-inputs-0930/README.md",
     "In the control-code engine `002AC5F0`, `[rbp−0x70]` is a text element built on the frame for a nested run (the argument insertion), so "
     "`[rbp+0x1C]` is that element's `+0x8C` (−0x70 + 0x8C = +0x1C).",
     "`[rbp−0x70]` is a 0xD0-byte copy of the current element `r14` (`002AD495`..`002AD52E`), made for a nested run (the argument insertion). "
     "So `[rbp+0x1C]` is the copy's `+0x8C`.", "sd105"),
    ("SD105-2b", C + "sd105-reveal-inputs-0930/README.md",
     "`002AD569` stores `002B43C0`'s result on the nested element there. Reading that result as the nested run's count is an interpretation.",
     "`002AD569` stores `002B43C0`'s result there. `002B43C0` lays the text out on a copy whose head `+0x8C` is `strlen(text)`, and returns "
     "`002AF340`'s character count (the SWE2-DATA page §4 reading).", "sd105"),
    ("SD105-3a", C + "sd105-reveal-inputs-0930/README.md",
     "**Authored overrides.** Whether any authored data sets `+0x9E` to something other than 8 is not checked.",
     "**Authored overrides.** The `\"` tag (`0F 22`) sets `+0x9E` per text (0-31). Whether shipped text uses it is not checked.", "sd105"),
    ("SD105-3b", C + "sd105-reveal-inputs-0930/README.md", None,
     "`002A1B00`'s element is a copy of the element at `r14` (`002A1B34`..`002A1BCB`), so it carries that element's `+0x50`. `002A3250`'s is "
     "not traced.", "sd105"),
    ("SD106-1", C + "sd106-measure-sites-0930/README.md",
     "**`002B3280` builds a kind-0 element on a text and hands back its measured width and height.**",
     "**`002B3280` builds a kind-0 element on a text and, called with `r9d` ≠ 0 (as all five sites call it), hands back its measured width "
     "(`+0x94` + 8) and height (`+0x96`). With `r9d` = 0 it builds through `002B3D50` and takes the element's size from the same two pointers "
     "instead.**", "sd106"),
    ("SD106-2a", C + "sd106-measure-sites-0930/README.md",
     "**the confirm caption** again (`+0x1B0`, element `+0xE0`), on two paths: after `002B3400` initialises the element on it, and after a "
     "0x400-byte clear",
     "**the confirm caption** again (`+0x1B0`, element `+0xE0`), on two of the message arm's three paths. `0057C58B` measures the caption "
     "copied from the argument when `+0x630` bit 0x20 is clear (with the bit set the caption goes through `002B3400` / `002B3050` and "
     "`002B3280` is not called). `0057C5DB` runs when the argument has no caption: the buffer is cleared by `memset` (`00861EC0`, 0x400 "
     "bytes), and the measured size is discarded for height 0 and width 2 x `[01E0CDC0]`. On every path the width is then raised to 0x60.",
     "sd106"),
    ("SD106-2b", C + "sd106-measure-sites-0930/README.md", "the size read back at `[rbp+0x58]` / `[rbp+0x50]` (M5)",
     "the dialog's caption width and height, `[rbp+0x58]` / `[rbp+0x50]` (M5)", "sd106"),
    ("SD106-3", C + "sd106-measure-sites-0930/README.md", "centred on screen",
     "centred on the UI canvas `[01E0C1D8]` x `[01E0C1DC]` (512 x 448, or 1920 x 1080 when `0024B120` selects it)", "sd106"),
]

print("== A: each applied wording is on its target, the original kept struck, the dated note beside it")
for label, rel, old, new, rev in A:
    txt = read(rel)
    n = norm(txt)
    ok_new = norm(new) in n
    ok_note = (NOTE in txt) and ("auditspec-review-%s-0930/REVIEW.md" % rev) in txt
    if old is None:
        check(label, ok_new and ok_note, "%s: wording added%s" % (rel.split("/")[-2] if rel.startswith(C) else rel, "" if ok_new else " - MISSING"))
    else:
        struck = ("~~" + norm(old) + "~~") in n
        # exactly one unstruck copy fewer than at HEAD (a dated historical copy elsewhere may stay, e.g. the widget page's UQ-190 note)
        gone = unstruck(txt).count(norm(old)) == unstruck(head(rel)).count(norm(old)) - 1
        check(label, ok_new and ok_note and struck and gone,
              "%s: new wording %s, original %s, %s" % (rel.split("/")[-2] if rel.startswith(C) else rel,
                                                       "present" if ok_new else "MISSING", "struck" if struck else "NOT STRUCK",
                                                       "one unstruck copy fewer than HEAD" if gone else "UNSTRUCK COPY REMAINS"))

print("== X: the struck originals were really there at HEAD (the struck checks can fail)")
seen = set()
for label, rel, old, new, rev in A:
    if old is None or label in seen:
        continue
    seen.add(label)
    h = head(rel)
    check("X1-" + label, bool(h) and norm(old) in norm(h) and norm(new) not in norm(h), "original present and new wording absent at HEAD")

print("== Checker texts")
o = read(C + "gr13-15-shop-list-widget-0930/gr13_15_shop_list_check.out")
check("K1", "the shop list control forwards it to the driver, which routes it to the stub" in o
      and "whatever target, the shop widget and the driver route it to the stub" not in o and o.rstrip().endswith("FAILS 0"),
      "gr13_15_shop_list_check.out: B6 re-issued with the review's check text, FAILS 0")
p = read(C + "gr13-15-shop-list-widget-0930/gr13_15_shop_list_check.py")
check("K2", "the shop list control forwards it to the driver, which routes it to the stub" in p
      and "whatever target, the shop widget" not in p, "gr13_15_shop_list_check.py: B6 message text")
s = read(C + "sd106-measure-sites-0930/sd106_sites.py")
check("K3", "after the element is initialised by" not in s and "auditspec-review-sd106-0930 item 4" in s,
      "sd106_sites.py: the M5 comment drops the 002B3400 path (the check itself is unchanged)")

print("== T: every edited table row keeps its header's column count")


def cells(line):
    # split on pipes outside backticks
    out, cur, tick = [], "", False
    for ch in line.strip():
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return len(out) - 2


for rel in sorted({a[1] for a in A}):
    lines = read(rel).replace("\r\n", "\n").split("\n")
    hdr = None
    bad = []
    for i, ln in enumerate(lines):
        if ln.startswith("|"):
            if hdr is None:
                hdr = cells(ln)
            elif "SWE2-CONTRACT for OPUS" in ln and cells(ln) != hdr:
                bad.append(i + 1)
        else:
            hdr = None
    check("T-" + "/".join(rel.split("/")[-2:]), not bad, "edited rows off-width: %s" % (bad or "none"))

print("== L: every review link the notes add resolves")
for rel in sorted({a[1] for a in A}):
    txt = read(rel)
    links = re.findall(r"\[review\]\(([^)]+auditspec-review-[^)]+-0930/REVIEW\.md)\)", txt)
    base = os.path.dirname(os.path.join(DB, rel))
    missing = [l for l in links if not os.path.isfile(os.path.normpath(os.path.join(base, l)))]
    check("L-" + "/".join(rel.split("/")[-2:]), links and not missing,
          "%d note link(s), unresolved %s" % (len(links), missing or "none"))

print("== B: blocked items are untouched")
t = read("_types/types.tsv")
check("B1", "constructs two empty MSVC strings at +0x20 and +0x40 (capacity 15, size 0)" in t
      and "key copied, default mapped value" not in t,
      "_types/types.tsv MsvcTreeNodeHeader ctor cell carries the original (SWE2-STRUCT holds the file); replacement proposed in README")

print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
