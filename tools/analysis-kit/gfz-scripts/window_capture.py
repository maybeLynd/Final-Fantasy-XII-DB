#!/usr/bin/env python3
"""window_capture.py - photograph the game's window, so the harness can SEE what it did.

Why this exists
---------------
`EXP-006` drove the game off the title screen with real input -- area id went `12` -> `306` and a
save buffer filled -- and the harness still printed `TITLE`, because its verdict keys on the
entity free list and a menu spawns no entities. **The harness could change the screen and not
know which screen it had changed to.**

Every runtime experiment so far has inferred the game's state from numbers chosen in advance.
That works until the game reaches a state nobody predicted, which is exactly when it matters.
A picture is the one observable that does not have to be anticipated.

What it captures, and the trap it avoids
----------------------------------------
`PrintWindow` with `PW_RENDERFULLCONTENT` (flag 2) asks the window to draw itself into a bitmap.
For a Direct3D swap-chain that often comes back **entirely black**, because the presented frame
never passes through GDI. So this tool tries `PrintWindow` first and, when the result is blank,
falls back to a **screen-region grab** of the window's rectangle via `BitBlt` from the screen DC.

**It reports which path produced the image and whether the result was blank**, rather than
writing a black PNG and letting the caller believe it photographed something. A capture tool that
cannot distinguish "the screen is black" from "the capture failed" is worse than none: it
manufactures confident negatives, which is the failure this project keeps rebuilding tools to
avoid.

The screen grab needs the window to be visible and unobscured, so `--focus` foregrounds it first
(verified, via `window_focus.py`) and the result records whether focus was actually held.

**Read-only.** It opens no process handle, reads no process memory and writes nothing to the
game. The only thing it touches is the desktop's own pixels.
"""
import argparse
import ctypes
import ctypes.wintypes as w
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP
import window_focus as WF

u32 = ctypes.WinDLL("user32", use_last_error=True)
gdi = ctypes.WinDLL("gdi32", use_last_error=True)

# DPI FIRST, before any window rectangle is asked for. A DPI-unaware process is handed LOGICAL
# coordinates by GetWindowRect while the screen DC is in PHYSICAL pixels, so a BitBlt at the
# reported rectangle grabs the wrong part of the desktop -- which is exactly what the first run
# of this tool did: it photographed a neighbouring window and the game's title bar.
try:                                   # Windows 10 1703+
    u32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))   # PER_MONITOR_AWARE_V2
except AttributeError:
    try:
        u32.SetProcessDPIAware()
    except AttributeError:
        pass

SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0
PW_RENDERFULLCONTENT = 2


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", w.DWORD), ("biWidth", ctypes.c_long),
                ("biHeight", ctypes.c_long), ("biPlanes", w.WORD),
                ("biBitCount", w.WORD), ("biCompression", w.DWORD),
                ("biSizeImage", w.DWORD), ("biXPelsPerMeter", ctypes.c_long),
                ("biYPelsPerMeter", ctypes.c_long), ("biClrUsed", w.DWORD),
                ("biClrImportant", w.DWORD)]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", w.DWORD * 3)]


def _grab(hwnd, cx, cy, use_printwindow):
    """-> BGRA bytes, top-down, or None."""
    src = u32.GetWindowDC(hwnd) if use_printwindow else u32.GetDC(0)
    if not src:
        return None
    mem = gdi.CreateCompatibleDC(src)
    bmp = gdi.CreateCompatibleBitmap(src, cx, cy)
    gdi.SelectObject(mem, bmp)
    if use_printwindow:
        ok = u32.PrintWindow(hwnd, mem, PW_RENDERFULLCONTENT)
    else:
        r = w.RECT()
        u32.GetWindowRect(hwnd, ctypes.byref(r))
        ok = gdi.BitBlt(mem, 0, 0, cx, cy, src, r.left, r.top, SRCCOPY)
    data = None
    if ok:
        bi = BITMAPINFO()
        bi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bi.bmiHeader.biWidth = cx
        bi.bmiHeader.biHeight = -cy          # negative: top-down, so no row flip later
        bi.bmiHeader.biPlanes = 1
        bi.bmiHeader.biBitCount = 32
        buf = ctypes.create_string_buffer(cx * cy * 4)
        got = gdi.GetDIBits(mem, bmp, 0, cy, buf, ctypes.byref(bi), DIB_RGB_COLORS)
        if got:
            data = buf.raw
    gdi.DeleteObject(bmp)
    gdi.DeleteDC(mem)
    if use_printwindow:
        u32.ReleaseDC(hwnd, src)
    else:
        u32.ReleaseDC(0, src)
    return data


def blankness(bgra):
    """How close to a single flat colour the image is, and what that colour is.

    Returned as a fraction so the caller can judge rather than trust a boolean: a real title
    screen is dark but not uniform, and a failed capture is uniform."""
    if not bgra:
        return (1.0, (0, 0, 0))
    n = len(bgra) // 4
    step = max(1, n // 20000)                # sample, do not walk 3.7 M pixels
    counts = {}
    total = 0
    for i in range(0, n, step):
        px = bgra[i * 4:i * 4 + 3]
        counts[px] = counts.get(px, 0) + 1
        total += 1
    top, hits = max(counts.items(), key=lambda kv: kv[1])
    return (hits / float(total), (top[2], top[1], top[0]))


def write_png(path, bgra, cx, cy):
    """A minimal PNG writer -- no third-party imaging dependency for a 3-line format."""
    rows = bytearray()
    for y in range(cy):
        rows.append(0)                                    # filter type 0
        row = bgra[y * cx * 4:(y + 1) * cx * 4]
        rows += bytes(row[i + 2] for i in range(0, len(row), 4)) if False else b""
        # interleave RGB from BGRA without a per-pixel Python loop over three appends
        mv = memoryview(row)
        rows += bytes(b"".join(bytes((mv[i + 2], mv[i + 1], mv[i]))
                               for i in range(0, len(row), 4)))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    hdr = struct.pack(">IIBBBBB", cx, cy, 8, 2, 0, 0, 0)   # 8-bit RGB
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", hdr))
        f.write(chunk(b"IDAT", zlib.compress(bytes(rows), 6)))
        f.write(chunk(b"IEND", b""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--focus", action="store_true",
                    help="foreground the window first (verified) -- required for the screen path")
    ap.add_argument("--scale", type=int, default=1,
                    help="keep every Nth pixel, to hand a smaller image to a reader")
    a = ap.parse_args()

    hits = RP.find_process(a.process)
    if not hits:
        sys.stderr.write("window_capture: no %r process running\n" % a.process)
        return 2
    pid = hits[0][0]
    wins = WF.windows_of(pid)
    if not wins:
        sys.stderr.write("window_capture: pid %d has no visible top-level window\n" % pid)
        return 3
    hwnd, title, cx, cy = max(wins, key=lambda t: t[2] * t[3])
    print("pid %d  hwnd %#x  %d x %d  %s" % (pid, hwnd, cx, cy, title))

    if a.focus:
        ok, fg = WF.focus(hwnd)
        print("foreground: %s" % ("the game, verified" if ok else "REFUSED (is %#x)" % fg))

    best = None
    for label, use_pw in (("PrintWindow", True), ("screen BitBlt", False)):
        data = _grab(hwnd, cx, cy, use_pw)
        frac, colour = blankness(data)
        print("  %-14s -> %s, %.1f %% one colour rgb%s"
              % (label, "no image" if data is None else "%d bytes" % len(data),
                 100.0 * frac, colour))
        if data is not None and (best is None or frac < best[1]):
            best = (data, frac, label)
        if data is not None and frac < 0.5:
            break

    if best is None:
        print("CAPTURE FAILED: neither path produced an image")
        return 4
    data, frac, label = best
    if frac >= 0.98:
        print("CAPTURE IS BLANK (%.1f %% one colour) -- writing it anyway, and saying so, "
              "because a blank PNG reported as a photograph is how a tool lies" % (100.0 * frac))

    if a.scale > 1:
        s = a.scale
        nx, ny = cx // s, cy // s
        out = bytearray(nx * ny * 4)
        for y in range(ny):
            srow = (y * s) * cx * 4
            drow = y * nx * 4
            for x in range(nx):
                si = srow + (x * s) * 4
                out[drow + x * 4:drow + x * 4 + 4] = data[si:si + 4]
        data, cx, cy = bytes(out), nx, ny

    write_png(a.out, data, cx, cy)
    print("wrote %s  (%d x %d, via %s)" % (a.out, cx, cy, label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
