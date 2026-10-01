#!/usr/bin/env python3
"""runtime_input_probe.py - press a real key and watch which byte of the game's input state moves.

The question this exists to settle
----------------------------------
`EXP-005` wrote bytes into the array the game's own input query reads, watched them persist
untouched, and found **nothing consumed them**. Three explanations survived; the cheapest
discriminator was written down as *"the operator holds a key while the harness polls"* -- an
irreducible manual step.

**It is not irreducible.** The operating system can hold the key, the harness can hold the
foreground, and the harness can poll. This tool does all three, so the operator does none of it.

What it produces
----------------
A map from a physical key to the array index that moves when it is pressed -- **derived, not
inferred**. `EXP-005` inferred `index = keymap_value - 28` from the fact that the smallest
`GameSetting.ini` code is 28 and the query subtracts `0x1C`. That is a good argument and it is
not a measurement. This is the measurement.

Three outcomes, all informative
-------------------------------
1. **Some index moves.** The array IS the live keyboard state, the mapping is now measured, and
   the open question narrows to why a written byte behaves differently from a game-written one.
2. **No index moves, for any key.** The array is not what the title screen reads -- and
   `EXP-005`'s remaining two explanations become one.
3. **The whole array is rewritten every frame.** Then the earlier "the value survives" reading
   was taken from a device block the poll had already abandoned.

Why the foreground check is not optional
----------------------------------------
Windows delivers keyboard input to the foreground window. A probe that does not **verify** it
holds the foreground is measuring its own terminal, and would produce a confident negative for
every key. `window_focus.py` verifies with `GetForegroundWindow`; this tool re-checks after
every key and reports any poll where focus was lost, rather than averaging it away.

**Read-only on the game.** It opens the process for READ only -- there is no write path in this
file at all. The only thing it changes is the operating system's idea of which key is down,
which is the same thing a keyboard does.
"""
import argparse
import ctypes
import ctypes.wintypes as w
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP
import runtime_poke as PK
import window_focus as WF

u32 = ctypes.WinDLL("user32", use_last_error=True)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)

# The keys a title screen plausibly answers, plus enough spread to catch a mapping that is not
# what anyone expects. Names are what a person would call them, codes are Windows virtual keys.
KEYS = [
    ("Enter", 0x0D), ("Space", 0x20), ("Escape", 0x1B), ("Z", 0x5A), ("X", 0x58),
    ("A", 0x41), ("S", 0x53), ("D", 0x44), ("Q", 0x51), ("E", 0x45),
    ("Up", 0x26), ("Down", 0x28), ("Left", 0x25), ("Right", 0x27),
    ("F1", 0x70), ("Tab", 0x09), ("LShift", 0xA0), ("LControl", 0xA2),
]

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
INPUT_KEYBOARD = 1


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", w.WORD), ("wScan", w.WORD), ("dwFlags", w.DWORD),
                ("time", w.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class _U(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT), ("pad", ctypes.c_ubyte * 32)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", w.DWORD), ("u", _U)]


def send_key(vk, up):
    """Send BOTH forms. EXP-004 tested virtual-key and scan-code separately and got two
    negatives; sending both together removes the chance that the one form tested was the wrong
    one, at the cost of not knowing which form worked. Which form worked is a later question
    than whether anything works at all."""
    scan = u32.MapVirtualKeyW(vk, 0)
    n = 2
    arr = (INPUT * n)()
    arr[0].type = INPUT_KEYBOARD
    arr[0].u.ki = KEYBDINPUT(vk, scan, KEYEVENTF_KEYUP if up else 0, 0, None)
    arr[1].type = INPUT_KEYBOARD
    arr[1].u.ki = KEYBDINPUT(0, scan,
                             KEYEVENTF_SCANCODE | (KEYEVENTF_KEYUP if up else 0), 0, None)
    return u32.SendInput(n, arr, ctypes.sizeof(INPUT))


def nonzero(b):
    return [i for i, v in enumerate(b) if v]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--hold", type=float, default=0.35, help="seconds to hold each key")
    ap.add_argument("--poll", type=float, default=0.01)
    ap.add_argument("--keys", help="comma-separated subset of the key names")
    a = ap.parse_args()

    hits = RP.find_process(a.process)
    if not hits:
        sys.stderr.write("runtime_input_probe: no %r process running\n" % a.process)
        return 2
    pid = hits[0][0]
    rw = PK.RW(pid)
    va, base = PK.resolve_array(rw)
    print("pid %d   held-array at 0x%016X, %d bytes" % (pid, va, len(base)))
    if nonzero(base):
        print("REFUSING: %d byte(s) already non-zero at rest -- a baseline that is not clean "
              "would make every result ambiguous: %s" % (len(nonzero(base)), nonzero(base)))
        return 3
    print("baseline: all %d bytes zero" % len(base))

    wins = WF.windows_of(pid)
    if not wins:
        print("the game has no visible window; input cannot be delivered")
        return 3
    hwnd = max(wins, key=lambda t: t[2] * t[3])[0]
    ok, fg = WF.focus(hwnd)
    if not ok:
        print("REFUSING: could not take the foreground (it is %#x). Every negative below would "
              "be a measurement of this terminal, not of the game." % fg)
        return 3
    print("foreground: the game (hwnd %#x), verified" % hwnd)
    print()

    keys = KEYS
    if a.keys:
        want = {k.strip().lower() for k in a.keys.split(",")}
        keys = [k for k in KEYS if k[0].lower() in want]

    # CONTROL for the whole instrument: poll the array for the same duration with NO key down.
    # Any index that moves here is noise and disqualifies itself from every result below.
    noise = set()
    t0 = time.time()
    while time.time() - t0 < a.hold:
        cur = rw.read(va, len(base))
        if cur:
            noise |= set(nonzero(cur))
        time.sleep(a.poll)
    print("CONTROL, no key held for %.2f s : %s"
          % (a.hold, "clean" if not noise else "NOISE at %s" % sorted(noise)))
    print()

    hits = {}
    lost_focus = 0
    for name, vk in keys:
        send_key(vk, False)
        seen = set()
        t0 = time.time()
        while time.time() - t0 < a.hold:
            cur = rw.read(va, len(base))
            if cur:
                seen |= set(nonzero(cur))
            if u32.GetForegroundWindow() != hwnd:
                lost_focus += 1
            time.sleep(a.poll)
        send_key(vk, True)
        time.sleep(0.05)
        seen -= noise
        after = rw.read(va, len(base))
        stuck = sorted(set(nonzero(after)) - noise) if after else []
        hits[name] = (sorted(seen), stuck)
        print("  %-9s vk %#04x  ->  indices while held: %-22s  still set after release: %s"
              % (name, vk, sorted(seen) or "none", stuck or "none"))

    print()
    moved = {k: v for k, v in hits.items() if v[0]}
    print("keys tried            : %d" % len(keys))
    print("keys that moved a byte: %d" % len(moved))
    print("polls that lost focus : %d" % lost_focus)
    if moved:
        print()
        print("MEASURED MAPPING  (index -> the game's own code, index + %d)" % PK.CODE_BIAS)
        rev = {v: k for k, v in PK.KEYMAP.items()}
        for name, (idx, _s) in sorted(moved.items()):
            for i in idx:
                code = i + PK.CODE_BIAS
                print("  %-9s index %3d  code %3d  %s"
                      % (name, i, code, rev.get(code, "(no GameSetting.ini name)")))
    else:
        print()
        print("NO KEY MOVED ANY BYTE, with the game verifiably in the foreground.")
        print("That is a real negative for this instrument: the control was clean and focus held.")
    rw.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
