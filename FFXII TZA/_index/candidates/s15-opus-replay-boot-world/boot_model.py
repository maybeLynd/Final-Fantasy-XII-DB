"""Process-start OS answers for the boot world (OPUS, 2026-09-26), disclosed; every call is logged.
 _set_app_type: recorded (console/GUI type), no effect in the image; SetUnhandledExceptionFilter: no previous filter (0);
 _time64: a FIXED wall clock, 1,758,844,800 (2025-09-26 00:00:00 UTC), written through the pointer when non-null - the
 process's only non-deterministic input at start, pinned so the world is reproducible."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX

T0 = 1758844800


def install(W, uc, log, extra=None):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    for _slot, _nm in W.import_slots():            # ordinal imports (OLEAUT32 ord 2/4/6) by the world's names
        if _nm.startswith("ord"):
            IAT[_nm] = _slot
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]

    def _set_app_type(u):
        log.append(("_set_app_type", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
        return 0

    def SetUnhandledExceptionFilter(u):
        log.append(("SetUnhandledExceptionFilter", "%X" % u.reg_read(UC_X86_REG_RCX)))
        return 0

    def _time64(u):
        p = u.reg_read(UC_X86_REG_RCX)
        if p:
            u.mem_write(p, struct.pack("<q", T0))
        log.append(("_time64",))
        return T0

    def _set_fmode(u):                             # default file translation mode: success
        log.append(("_set_fmode", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
        return 0

    def _set_new_mode(u):                          # operator new's failure handling mode: the previous mode was 0
        log.append(("_set_new_mode", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
        return 0

    def clock(u):                                  # processor time since start, pinned at 0 ticks
        log.append(("clock",))
        return 0

    threads = []

    def CreateThread(u):                           # (attrs, stack, start, param, flags, &tid): recorded, NOT run
        from unicorn.x86_const import UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP
        start, param = u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9)
        rsp = u.reg_read(UC_X86_REG_RSP)
        flags, ptid = struct.unpack("<I", bytes(u.mem_read(rsp + 0x28, 4)))[0], q(rsp + 0x30)
        h = 0x5000 + 0x10 * len(threads)
        if ptid:
            u.mem_write(ptid, struct.pack("<I", 0x100 + len(threads)))
        threads.append({"start": "%X" % start, "param": "%X" % param, "flags": flags, "handle": "%X" % h})
        log.append(("CreateThread", "%X" % start, "%X" % param, flags))
        return h

    COMMODE = 0x7B7F0000
    uc.mem_map(COMMODE, 0x1000)
    uc.mem_write(COMMODE, bytes(0x1000))

    def __p__commode(u):                           # the CRT's _commode cell (0 = no commit-on-flush)
        return COMMODE

    def SetThreadAffinityMask(u):                  # a 4-processor machine: the previous mask was all four
        log.append(("SetThreadAffinityMask", "%X" % u.reg_read(UC_X86_REG_RCX), "%X" % u.reg_read(__import__("unicorn").x86_const.UC_X86_REG_RDX)))
        return 0xF

    def SetThreadPriority(u):
        log.append(("SetThreadPriority",))
        return 1

    def ResumeThread(u):                           # the thread was suspended once; it is recorded, not run
        log.append(("ResumeThread", "%X" % u.reg_read(UC_X86_REG_RCX)))
        return 1

    def GetCurrentProcess(u):
        return 0xFFFFFFFFFFFFFFFF

    def Sleep(u):
        log.append(("Sleep", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
        return 0

    def GetSystemInfo(u):                          # SYSTEM_INFO: x64, 4 KiB pages, 4 processors, 64 KiB granularity
        p = u.reg_read(UC_X86_REG_RCX)
        u.mem_write(p, struct.pack("<HHIQQQIIIHH", 9, 0, 0x1000, 0x10000, 0x7FFFFFFEFFFF, 0xF, 4, 8664, 0x10000, 6, 0x5E03))
        return 0

    def RaiseException(u):                         # only the MSVC thread-naming exception 0x406D1388 is modelled: with no
        from unicorn.x86_const import UC_X86_REG_R9   # debugger its own __except swallows it and control reaches the same
        code = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF  # continuation, so returning is equivalent; any other code stops
        if code != 0x406D1388:
            log.append(("RaiseException UNMODELLED", "%X" % code))
            u.emu_stop()
            return 0
        info = u.reg_read(UC_X86_REG_R9)
        name_p = q(info + 8)
        log.append(("thread name", bytes(u.mem_read(name_p, 64)).split(bytes(1))[0].decode("latin1"),
                    struct.unpack("<I", bytes(u.mem_read(info + 0x10, 4)))[0]))
        return 0

    def InitializeSListHead(u):                    # an empty interlocked list: 16 zero bytes
        u.mem_write(u.reg_read(UC_X86_REG_RCX), bytes(16))
        return 0

    def _configure_narrow_argv(u):                 # argv parsing mode: success
        return 0

    LAST = {"err": 0}                              # the thread's last-error value, set by the calls modelled here

    def GetLastError(u):
        return LAST["err"]

    def CreateDirectoryW(u):                       # the folder already exists
        LAST["err"] = 183
        return 0

    def CreateMutexW(u):                           # the single-instance mutex: created, no other instance
        LAST["err"] = 0
        log.append(("CreateMutexW",))
        return 0x6000

    def _configthreadlocale(u):                    # per-thread locale mode: the previous mode was global (2)
        return 2

    def ImmDisableIME(u):
        return 1

    def CoInitializeEx(u):
        return 0

    STEAMCTX = 0x7B7E0000
    uc.mem_map(STEAMCTX, 0x1000)
    uc.mem_write(STEAMCTX, bytes(0x1000))

    def SteamInternal_ContextInit(u):              # the Steam client is not running: a context with no interfaces
        log.append(("SteamInternal_ContextInit",))
        return STEAMCTX

    def SteamAPI_Init(u):
        log.append(("SteamAPI_Init", 0))
        return 0

    def SteamAPI_RestartAppIfNecessary(u):         # no relaunch through Steam is required
        log.append(("SteamAPI_RestartAppIfNecessary", "%X" % (u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF)))
        return 0

    def exit_(u):
        log.append(("exit", u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF))
        u.emu_stop()
        return 0

    from unicorn.x86_const import UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP
    STR = 0x7B7D0000
    uc.mem_map(STR, 0x10000)
    uc.mem_write(STR, bytes(0x10000))
    CMDLINE = STR + 0x100
    uc.mem_write(CMDLINE, ('"' + W.EXE + '"\0').encode("utf-16-le"))
    bump = {"p": STR + 0x2000}

    def salloc(n):
        p = bump["p"]; bump["p"] += (n + 0x1F) & ~0xF
        return p

    def wstr(u, a, n=None):
        b = bytes(u.mem_read(a, 0x800))
        s = b.decode("utf-16-le", "replace")
        s = s.split("\0")[0]
        return s if n is None else s[:n]

    def SteamAPI_RegisterCallback(u):              # recorded; no callback is ever delivered in this model
        log.append(("SteamAPI_RegisterCallback", "%X" % u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF))
        return 0

    def _initialize_narrow_environment(u):
        return 0

    def IsDebuggerPresent(u):
        return 0

    def GetCommandLineW(u):                        # the executable alone, no arguments
        return CMDLINE

    def CommandLineToArgvW(u):                     # argv = [exe]; *pNumArgs = 1
        pn = u.reg_read(UC_X86_REG_RDX)
        s = W.EXE
        sp = salloc(2 * len(s) + 2); u.mem_write(sp, (s + "\0").encode("utf-16-le"))
        arr = salloc(16); u.mem_write(arr, struct.pack("<QQ", sp, 0))
        if pn:
            u.mem_write(pn, struct.pack("<i", 1))
        return arr

    def LocalFree(u):
        return 0

    def WideCharToMultiByte(u):                    # (cp, flags, wide, cch, out, cb, def, used): ANSI (latin-1 range)
        wp, cch = u.reg_read(UC_X86_REG_R8), u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF
        rsp = u.reg_read(UC_X86_REG_RSP)
        out, cb = q(rsp + 0x28), struct.unpack("<i", bytes(u.mem_read(rsp + 0x30, 4)))[0]
        s = wstr(u, wp) + ("\0" if cch == 0xFFFFFFFF else "")
        if cch != 0xFFFFFFFF:
            s = bytes(u.mem_read(wp, 2 * cch)).decode("utf-16-le", "replace")
        b = s.encode("latin-1", "replace")
        if cb == 0:
            return len(b)
        u.mem_write(out, b[:cb])
        return min(len(b), cb)

    def SysAllocStringLen(u):                      # BSTR: length prefix, copy, terminator
        src, n = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
        p = salloc(4 + 2 * n + 2) + 4
        u.mem_write(p - 4, struct.pack("<I", 2 * n))
        u.mem_write(p, (bytes(u.mem_read(src, 2 * n)) if src else bytes(2 * n)) + bytes(2))
        return p

    def SysAllocString(u):                         # OLEAUT32 ord 2
        src = u.reg_read(UC_X86_REG_RCX)
        if not src:
            return 0
        t = wz(u, src)
        p = salloc(4 + 2 * len(t) + 2) + 4
        u.mem_write(p - 4, struct.pack("<I", 2 * len(t)))
        wput(u, p, t)
        return p

    def SysFreeString(u):
        return 0

    def SetThreadExecutionState(u):
        return 0x80000000

    METRICS = {0: 1920, 1: 1080, 16: 1920, 17: 1040, 78: 1920, 79: 1080, 80: 1}   # SM_CX/CYSCREEN, full-screen, virtual, monitors

    def GetSystemMetrics(u):                       # one 1920 x 1080 primary display
        i = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
        log.append(("GetSystemMetrics", i))
        return METRICS.get(i, 0)

    def GetUserDefaultLangID(u):                   # en-US
        return 0x0409

    def GetUserDefaultUILanguage(u):
        return 0x0409

    def wz(u, a, cap=0x4000):                      # a NUL-terminated UTF-16 string, read to its terminator
        out = []
        while True:
            b = bytes(u.mem_read(a, 0x200))
            for i in range(0, len(b), 2):
                c = b[i] | (b[i + 1] << 8)
                if c == 0:
                    return "".join(out)
                out.append(chr(c))
            a += 0x200
            if len(out) > cap:
                return "".join(out)

    def wput(u, a, s):
        u.mem_write(a, (s + "\0").encode("utf-16-le"))

    def wcscpy_s(u):                               # (dst, count, src) -> 0 or ERANGE (34)
        d, n, s = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        t = wz(u, s)
        if len(t) + 1 > n:
            return 34
        wput(u, d, t)
        return 0

    def wcscat_s(u):
        d, n, s = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        a, t = wz(u, d), wz(u, s)
        if len(a) + len(t) + 1 > n:
            return 34
        wput(u, d, a + t)
        return 0

    def wcsncpy_s(u):                              # (dst, count, src, max): _TRUNCATE (-1) truncates
        d, n, s, m = (u.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))
        t = wz(u, s)
        if m != 0xFFFFFFFFFFFFFFFF:
            t = t[:m]
        if len(t) + 1 > n:
            if m == 0xFFFFFFFFFFFFFFFF:
                wput(u, d, t[:n - 1]); return 80
            return 34
        wput(u, d, t)
        return 0

    def wcslen(u):
        return len(wz(u, u.reg_read(UC_X86_REG_RCX)))

    def wcscmp(u):
        a, b = wz(u, u.reg_read(UC_X86_REG_RCX)), wz(u, u.reg_read(UC_X86_REG_RDX))
        return 0 if a == b else (0xFFFFFFFF if a < b else 1)

    def _wcsicmp(u):
        a, b = wz(u, u.reg_read(UC_X86_REG_RCX)).lower(), wz(u, u.reg_read(UC_X86_REG_RDX)).lower()
        return 0 if a == b else (0xFFFFFFFF if a < b else 1)

    def wcsrchr(u):
        s, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFFFF
        t = wz(u, s)
        i = len(t) if c == 0 else t.rfind(chr(c))
        return s + 2 * i if i >= 0 else 0

    def wcschr(u):
        s, c = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFFFF
        t = wz(u, s)
        i = len(t) if c == 0 else t.find(chr(c))
        return s + 2 * i if i >= 0 else 0

    def SetThreadUILanguage(u):                    # returns the language set
        return u.reg_read(UC_X86_REG_RCX) & 0xFFFF

    # the executable's own resources, from its resource directory (the image is mapped, so data is read in place)
    pe_r = pefile.PE(W.EXE)
    RES = {}
    for t in (pe_r.DIRECTORY_ENTRY_RESOURCE.entries if hasattr(pe_r, "DIRECTORY_ENTRY_RESOURCE") else []):
        tkey = t.id if t.name is None else str(t.name)
        for n in t.directory.entries:
            nkey = n.id if n.name is None else str(n.name)
            for lang in n.directory.entries:
                RES.setdefault((tkey, nkey), (lang.data.struct.OffsetToData, lang.data.struct.Size))
    RESH = 0x7B7C0000
    uc.mem_map(RESH, 0x1000)
    handles = {}

    def reskey(u, v):
        return v if v < 0x10000 else wz(u, v).upper()

    def FindResourceW(u):                          # (module, name, type): a handle to the entry, or 0
        name, typ = reskey(u, u.reg_read(UC_X86_REG_RDX)), reskey(u, u.reg_read(UC_X86_REG_R8))
        e = RES.get((typ, name))
        log.append(("FindResourceW", typ, name, bool(e)))
        if not e:
            return 0
        h = RESH + 0x10 * (len(handles) + 1)
        handles[h] = e
        return h

    def LoadResource(u):
        return u.reg_read(UC_X86_REG_RDX)

    def LockResource(u):
        e = handles.get(u.reg_read(UC_X86_REG_RCX))
        return 0x120000 + e[0] if e else 0

    def SizeofResource(u):
        e = handles.get(u.reg_read(UC_X86_REG_RDX))
        return e[1] if e else 0

    FN = {"FindResourceW": FindResourceW, "LoadResource": LoadResource, "LockResource": LockResource,
          "SizeofResource": SizeofResource, "SetThreadUILanguage": SetThreadUILanguage, "wcscpy_s": wcscpy_s, "wcscat_s": wcscat_s, "wcsncpy_s": wcsncpy_s, "wcslen": wcslen, "wcscmp": wcscmp,
          "_wcsicmp": _wcsicmp, "wcsrchr": wcsrchr, "wcschr": wcschr,
          "GetUserDefaultLangID": GetUserDefaultLangID, "GetUserDefaultUILanguage": GetUserDefaultUILanguage, "GetSystemMetrics": GetSystemMetrics, "SteamAPI_RegisterCallback": SteamAPI_RegisterCallback, "_initialize_narrow_environment": _initialize_narrow_environment,
          "IsDebuggerPresent": IsDebuggerPresent, "GetCommandLineW": GetCommandLineW, "CommandLineToArgvW": CommandLineToArgvW,
          "LocalFree": LocalFree, "WideCharToMultiByte": WideCharToMultiByte, "SysAllocStringLen": SysAllocStringLen,
          "SysFreeString": SysFreeString, "SetThreadExecutionState": SetThreadExecutionState,
          "ord4": SysAllocStringLen, "ord6": SysFreeString, "ord2": SysAllocString,
          "GetLastError": GetLastError, "CreateDirectoryW": CreateDirectoryW, "CreateMutexW": CreateMutexW,
          "_configthreadlocale": _configthreadlocale, "ImmDisableIME": ImmDisableIME, "CoInitializeEx": CoInitializeEx,
          "SteamInternal_ContextInit": SteamInternal_ContextInit, "SteamAPI_Init": SteamAPI_Init,
          "SteamAPI_RestartAppIfNecessary": SteamAPI_RestartAppIfNecessary, "exit": exit_,
          "InitializeSListHead": InitializeSListHead, "RaiseException": RaiseException, "_configure_narrow_argv": _configure_narrow_argv, "__p__commode": __p__commode, "SetThreadAffinityMask": SetThreadAffinityMask, "SetThreadPriority": SetThreadPriority,
          "ResumeThread": ResumeThread, "GetCurrentProcess": GetCurrentProcess, "Sleep": Sleep, "GetSystemInfo": GetSystemInfo,
          "_set_app_type": _set_app_type, "SetUnhandledExceptionFilter": SetUnhandledExceptionFilter, "_time64": _time64,
          "_set_fmode": _set_fmode, "_set_new_mode": _set_new_mode, "clock": clock, "CreateThread": CreateThread, "_beginthreadex": CreateThread}
    FN.update(extra or {})
    for nm, f in FN.items():
        if nm not in IAT:
            continue
        W.OSRET[nm] = 0
        W.BRIDGED.add(nm)
        uc.hook_add(UC_HOOK_CODE, (lambda f: lambda u, a, n, _: u.reg_write(UC_X86_REG_RAX, f(u) & 0xFFFFFFFFFFFFFFFF))(f),
                    begin=q(IAT[nm]), end=q(IAT[nm]))
    install.LAST = LAST
    return IAT, threads
