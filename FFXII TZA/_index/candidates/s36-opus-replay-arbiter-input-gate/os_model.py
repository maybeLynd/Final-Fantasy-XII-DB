"""A disclosed OS model for the S-36 input run (OPUS, 2026-09-26): a fresh install on a machine with one XInput pad.
Installed by name at each import's trap; every call is logged; an import not listed stays unbridged, and a call the model does
not cover (an unmodelled printf conversion) stops the run by name.
 - folders: SHGetFolderPathW -> C:\\Users\\model\\Documents; _waccess / GetFileAttributesW -> absent; _wmkdir -> created;
   CreateDirectoryW -> FALSE (already exists); no configuration file opens (_wfopen*, fopen*, CreateFileW fail).
 - strings: the UCRT wide printf (__stdio_common_vswprintf[_s], honouring the legacy-wide-specifiers option bit), user32
   wsprintfW, lstrcatW / lstrcpyW / lstrlenW, with their library semantics.
 - platform: GetVersionExA -> 6.2.9200 (what an unmanifested process sees on Windows 8/10/11; the poll only tests for 6.1);
   GetForegroundWindow -> the game's own window handle [02EA5248] (the game has the focus); GetCursorPos (0, 0),
   ScreenToClient, GetClientRect 1920x1080; no key down (GetAsyncKeyState / GetKeyState / GetKeyboardState).
 - libraries: LoadLibraryW loads (its exports are then not found: the world's GetProcAddress answers 0); XInputSetState
   (rumble) is accepted; Steam: SteamInternal_ContextInit returns a context holding no interfaces, SteamAPI_RunCallbacks has
   nothing pending."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP

DOCS = "C:\\Users\\model\\Documents"


def install(W, uc, log):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]

    def wstr(u, a, n=520):
        b = bytes(u.mem_read(a, n))
        out = []
        for i in range(0, len(b) - 1, 2):
            c = b[i] | (b[i + 1] << 8)
            if c == 0:
                break
            out.append(chr(c))
        return "".join(out)

    def cstr(u, a, n=520):
        return bytes(u.mem_read(a, n)).split(b"\0")[0].decode("latin1")

    def SHGetFolderPathW(u):                       # (hwnd, csidl, token, flags, path out): S_OK, the Documents path
        rsp = u.reg_read(UC_X86_REG_RSP)
        out = q(rsp + 0x28)
        u.mem_write(out, (DOCS + "\0").encode("utf-16-le"))
        log.append(("SHGetFolderPathW", "%X" % (u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)))
        return 0

    def CreateDirectoryW(u):                       # the folder exists: FALSE with ERROR_ALREADY_EXISTS is what a caller sees
        log.append(("CreateDirectoryW", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0

    def GetFileAttributesW(u):                     # no configuration file present
        log.append(("GetFileAttributesW", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0xFFFFFFFF

    def CreateFileW(u):
        log.append(("CreateFileW", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0xFFFFFFFFFFFFFFFF                  # INVALID_HANDLE_VALUE

    def _wfopen(u):
        log.append(("_wfopen", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0

    def _wfopen_s(u):                              # (FILE **, name, mode): ENOENT
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), bytes(8))
        log.append(("_wfopen_s", wstr(u, u.reg_read(UC_X86_REG_RDX))))
        return 2

    def _wfsopen(u):
        log.append(("_wfsopen", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0

    def fopen(u):
        log.append(("fopen", cstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0

    def fopen_s(u):
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), bytes(8))
        log.append(("fopen_s", cstr(u, u.reg_read(UC_X86_REG_RDX))))
        return 2

    def GetLastError(u):
        return 183                                 # ERROR_ALREADY_EXISTS (after the directory call)

    def _waccess(u):                               # no configuration file present: -1 (ENOENT)
        log.append(("_waccess", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0xFFFFFFFF

    def _wmkdir(u):                                # a fresh install: the folder is created
        log.append(("_wmkdir", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0

    def _access(u):
        log.append(("_access", cstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0xFFFFFFFF

    import re
    SPEC = re.compile(r"%([-+ 0#]*)(\*|\d+)?(?:\.(\*|\d+))?(hh|h|ll|l|w|I64|I32|z|j|t|L)?([diouxXcCsSfFeEgGp%])")

    def wfmt(u, fmt, va, legacy):                  # the UCRT wide printf over an emulated va_list (8-byte slots)
        out, pos, i = "", 0, 0

        def nxt():
            nonlocal i
            v = q(va + 8 * i)
            i += 1
            return v
        for m in SPEC.finditer(fmt):
            out += fmt[pos:m.start()]
            pos = m.end()
            flags, width, prec, length, conv = m.groups()
            if conv == "%":
                out += "%"
                continue
            w = nxt() & 0xFFFFFFFF if width == "*" else (int(width) if width else None)
            p = nxt() & 0xFFFFFFFF if prec == "*" else (int(prec) if prec is not None else None)
            fl = flags or ""
            if conv in "di":
                v = nxt()
                bits = 64 if length in ("ll", "I64", "z", "j", "t") else 32
                v &= (1 << bits) - 1
                if v >> (bits - 1):
                    v -= 1 << bits
                s = ("%" + fl + (str(w) if w else "") + ("." + str(p) if p is not None else "") + "d") % v
            elif conv in "uxXo":
                v = nxt() & ((1 << (64 if length in ("ll", "I64", "z", "j", "t") else 32)) - 1)
                s = ("%" + fl + (str(w) if w else "") + ("." + str(p) if p is not None else "") + {"u": "d"}.get(conv, conv)) % v
            elif conv in "sS":
                a = nxt()
                wide = (length in ("l", "w")) or (conv == "s" and legacy and length != "h") or (conv == "S" and not legacy and length != "h")
                t = ("(null)" if not a else (wstr(u, a, 4096) if wide else cstr(u, a, 4096)))
                if p is not None:
                    t = t[:p]
                s = t.rjust(w) if w and "-" not in fl else (t.ljust(w) if w else t)
            elif conv in "cC":
                s = chr(nxt() & 0xFFFF)
            else:
                raise ValueError("wide printf conversion %s not modelled" % conv)
            out += s
        return out + fmt[pos:]

    def __stdio_common_vswprintf(u):               # (options, buf, count, fmt, locale, va) -> chars written or -1
        rsp = u.reg_read(UC_X86_REG_RSP)
        opts, buf, cnt, fmt = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9)
        va = q(rsp + 0x30)
        txt = wfmt(u, wstr(u, fmt, 2048), va, bool(opts & 4))
        if cnt and len(txt) + 1 > cnt:
            u.mem_write(buf, (txt[:cnt - 1] + "\0").encode("utf-16-le"))
            log.append(("vswprintf", txt[:80], "truncated"))
            return 0xFFFFFFFF
        u.mem_write(buf, (txt + "\0").encode("utf-16-le"))
        log.append(("vswprintf", txt[:80]))
        return len(txt)

    def __stdio_common_vswprintf_s(u):             # same arguments; truncation is an error (-1)
        return __stdio_common_vswprintf(u)

    def lstrcatW(u):                               # Win32: append src to dst, return dst
        d, s = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        a, b = wstr(u, d, 4096), wstr(u, s, 4096)
        u.mem_write(d, (a + b + "\0").encode("utf-16-le"))
        log.append(("lstrcatW", b[:40]))
        return d

    def lstrcpyW(u):
        d, s = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        u.mem_write(d, (wstr(u, s, 4096) + "\0").encode("utf-16-le"))
        return d

    def lstrlenW(u):
        return len(wstr(u, u.reg_read(UC_X86_REG_RCX), 4096))

    VA = 0x7B6F0000
    uc.mem_map(VA, 0x1000)

    def wsprintfW(u):                              # user32, variadic (buf, fmt, ...): %s is wide; result capped at 1024 chars
        rsp = u.reg_read(UC_X86_REG_RSP)
        slots = [u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9)] + [q(rsp + 0x28 + 8 * k) for k in range(8)]
        u.mem_write(VA, b"".join(struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF) for v in slots))
        txt = wfmt(u, wstr(u, u.reg_read(UC_X86_REG_RDX), 2048), VA, True)[:1023]
        u.mem_write(u.reg_read(UC_X86_REG_RCX), (txt + "\0").encode("utf-16-le"))
        log.append(("wsprintfW", txt[:80]))
        return len(txt)

    def GetVersionExA(u):                          # OSVERSIONINFOA for 6.2 build 9200 (what an unmanifested process sees on 8/10/11)
        p = u.reg_read(UC_X86_REG_RCX)
        u.mem_write(p + 4, struct.pack("<IIII", 6, 2, 9200, 2))
        log.append(("GetVersionExA", "6.2.9200"))
        return 1

    def XInputSetState(u):                         # rumble accepted
        log.append(("XInputSetState", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
        return 0

    def GetForegroundWindow(u):                    # the game's own window has the focus (the handle in [02EA5248])
        return q(0x2EA5248)

    def GetCursorPos(u):                           # the cursor rests at (0, 0)
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), struct.pack("<ii", 0, 0))
        return 1

    def ScreenToClient(u):                         # the client area starts at the screen origin
        return 1

    def GetClientRect(u):                          # a 1920 x 1080 client area
        uc.mem_write(u.reg_read(UC_X86_REG_RDX), struct.pack("<iiii", 0, 0, 1920, 1080))
        return 1

    def GetAsyncKeyState(u):                       # no key is down
        return 0

    def GetKeyState(u):
        return 0

    def GetKeyboardState(u):                       # 256 bytes, no key down
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), bytes(256))
        return 1

    def SteamAPI_RunCallbacks(u):                  # the pump: no Steam callback is pending in this model
        log.append(("SteamAPI_RunCallbacks",))
        return 0

    STEAMCTX = 0x7B600000
    uc.mem_map(STEAMCTX, 0x1000)
    uc.mem_write(STEAMCTX, bytes(0x1000))

    def SteamInternal_ContextInit(u):              # a Steam context holding no interfaces: every Steam step is skipped
        log.append(("SteamInternal_ContextInit",))
        return STEAMCTX

    def LoadLibraryW(u):                           # the library loads; its exports are not found (the world's GetProcAddress = 0)
        log.append(("LoadLibraryW", wstr(u, u.reg_read(UC_X86_REG_RCX))))
        return 0x7FFB0000

    FN = {f.__name__: f for f in (GetCursorPos, ScreenToClient, GetClientRect, GetAsyncKeyState, GetKeyState, GetKeyboardState, SteamAPI_RunCallbacks, GetVersionExA, XInputSetState, GetForegroundWindow, wsprintfW, SteamInternal_ContextInit, LoadLibraryW, __stdio_common_vswprintf_s, lstrcatW, lstrcpyW, lstrlenW, SHGetFolderPathW, CreateDirectoryW, GetFileAttributesW, CreateFileW, _wfopen, _wfopen_s, _wfsopen, fopen,
                                  fopen_s, GetLastError, _waccess, _wmkdir, _access, __stdio_common_vswprintf)}
    for nm, f in FN.items():
        if nm not in IAT:
            continue
        W.OSRET[nm] = 0
        W.BRIDGED.add(nm)

        def hook(u, a, n, _, f=f, nm=nm):
            try:
                r = f(u)
            except Exception as e:                  # anything the model does not cover stops the run, by name
                log.append(("UNSUPPORTED", nm, str(e)))
                u.emu_stop()
                return
            u.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
        uc.hook_add(UC_HOOK_CODE, hook, begin=q(IAT[nm]), end=q(IAT[nm]))
    return IAT
