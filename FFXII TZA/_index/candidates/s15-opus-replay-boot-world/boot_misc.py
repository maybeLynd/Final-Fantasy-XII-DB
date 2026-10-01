"""Further process-start OS answers for the boot world (OPUS, 2026-09-26), disclosed; every call is logged.
CryptAcquireContextW: a verify-only CSP context (handle written through the pointer, TRUE); CryptReleaseContext: TRUE.
MD5 hashing (CryptCreateHash CALG_MD5 / CryptHashData / CryptGetHashParam / CryptDestroyHash) with standard
semantics (hashlib); any other algorithm refuses. SystemParametersInfoW: sticky keys only (get answers the Windows default
flags 0x7E, hot key active; set is recorded); any other action refuses. GlobalMemoryStatusEx: a 16 GiB machine.
timeGetDevCaps: 1 ms .. 1000 s; timeBegin/EndPeriod succeed. strcspn: the C library's. CoCreateInstance: the audio endpoint
layer (MMDeviceEnumerator) is NOT modelled - every creation answers REGDB_E_CLASSNOTREG with a null interface, so the game's
own failure path runs. OutputDebugStringA: logged. toupper / tolower: the C locale. GetCurrentThread: the pseudo-handle -2. The key / cipher calls are NOT modelled: reaching one stops the run by name (the import fence)."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP


def install(W, uc, log):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
    d4s = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
    st = {"csp": 0}

    def CryptAcquireContextW(u):                  # (&hProv, container, provider, type, flags)
        st["csp"] += 1
        h = 0xC5900000 + st["csp"]
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), struct.pack("<Q", h))
        log.append(("CryptAcquireContextW", u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF, "%X" % d4s(u.reg_read(UC_X86_REG_RSP) + 0x28)))
        return 1

    def CryptReleaseContext(u):
        return 1

    import hashlib
    hashes = {}

    def CryptCreateHash(u):                       # (hProv, algid, key, flags, &hHash): CALG_MD5 (0x8003) only
        alg = u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
        if alg != 0x8003 or u.reg_read(UC_X86_REG_R8):
            raise RuntimeError("CryptCreateHash algid %X / keyed: not modelled" % alg)
        h = 0xC5A00000 + len(hashes) + 1
        hashes[h] = hashlib.md5()
        uc.mem_write(q(u.reg_read(UC_X86_REG_RSP) + 0x28), struct.pack("<Q", h))
        return 1

    def CryptHashData(u):                         # (hHash, data, len, flags)
        h, p, n = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
        hashes[h].update(bytes(uc.mem_read(p, n)) if n else b"")
        log.append(("CryptHashData", n))
        return 1

    def CryptGetHashParam(u):                     # (hHash, param, buf, &len, flags): HP_HASHVAL 2, HP_HASHSIZE 4
        h, prm, buf, pl = (u.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))
        prm &= 0xFFFFFFFF
        val = hashes[h].digest() if prm == 2 else struct.pack("<I", 16) if prm == 4 else None
        if val is None:
            raise RuntimeError("CryptGetHashParam %d: not modelled" % prm)
        cap = d4s(pl)
        uc.mem_write(pl, struct.pack("<I", len(val)))
        if buf:
            if cap < len(val):
                return 0
            uc.mem_write(buf, val)
            log.append(("CryptGetHashParam", prm, val.hex()))
        return 1

    def CryptDestroyHash(u):
        hashes.pop(u.reg_read(UC_X86_REG_RCX), None)
        return 1

    SK = {"flags": 0x7E}

    def SystemParametersInfoW(u):                 # (action, uiParam, pv, winIni): the sticky-keys pair only (0x3A get / 0x3B set)
        act, pv = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_R8)
        if act == 0x3A:                           # STICKYKEYS {cbSize, dwFlags}: the Windows default, hot key active (bit 2)
            uc.mem_write(pv + 4, struct.pack("<I", SK["flags"]))
        elif act == 0x3B:
            SK["flags"] = d4s(pv + 4)
        else:
            raise RuntimeError("SystemParametersInfoW action %X: not modelled" % act)
        log.append(("SystemParametersInfoW", "%X" % act, "%X" % SK["flags"]))
        return 1

    def GlobalMemoryStatusEx(u):                  # MEMORYSTATUSEX: 16 GiB physical, 8 GiB free, 128 TiB virtual
        p = u.reg_read(UC_X86_REG_RCX)
        G = 1 << 30
        uc.mem_write(p + 4, struct.pack("<IQQQQQQQ", 50, 16 * G, 8 * G, 32 * G, 24 * G, 128 << 40, (128 << 40) - 4 * G, 0))
        return 1

    def timeGetDevCaps(u):                        # TIMECAPS {wPeriodMin 1, wPeriodMax 1000000}: MMSYSERR_NOERROR
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), struct.pack("<II", 1, 1000000))
        return 0

    def strcspn(u):                               # C strcspn: length of the leading run not in the reject set
        a, r = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX)
        def cz(p):
            b = bytearray()
            while True:
                c = uc.mem_read(p + len(b), 1)[0]
                if c == 0:
                    return bytes(b)
                b.append(c)
        s_, rej = cz(a), set(cz(r))
        n = 0
        while n < len(s_) and s_[n] not in rej:
            n += 1
        return n

    def CoCreateInstance(u):                      # the audio endpoint layer is not modelled: REGDB_E_CLASSNOTREG, *ppv = NULL
        import uuid
        clsid = uuid.UUID(bytes_le=bytes(uc.mem_read(u.reg_read(UC_X86_REG_RCX), 16)))
        pp = q(u.reg_read(UC_X86_REG_RSP) + 0x28)
        if pp:
            uc.mem_write(pp, bytes(8))
        log.append(("CoCreateInstance", str(clsid), "REGDB_E_CLASSNOTREG"))
        return 0x80040154

    def OutputDebugStringA(u):
        a = u.reg_read(UC_X86_REG_RCX)
        log.append(("OutputDebugStringA", bytes(uc.mem_read(a, 200)).split(b"\0")[0].decode("latin1")))
        return 0

    def toupper(u):                               # C locale
        c = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
        return c - 32 if 97 <= c <= 122 else c

    def tolower(u):
        c = u.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
        return c + 32 if 65 <= c <= 90 else c

    FN = {"toupper": toupper, "tolower": tolower, "GetCurrentThread": lambda u: 0xFFFFFFFFFFFFFFFE,
          "GlobalMemoryStatusEx": GlobalMemoryStatusEx, "timeGetDevCaps": timeGetDevCaps, "timeBeginPeriod": lambda u: 0,
          "timeEndPeriod": lambda u: 0, "strcspn": strcspn, "CoCreateInstance": CoCreateInstance, "CoTaskMemFree": lambda u: 0,
          "OutputDebugStringA": OutputDebugStringA, "SystemParametersInfoW": SystemParametersInfoW, "CryptAcquireContextW": CryptAcquireContextW, "CryptReleaseContext": CryptReleaseContext, "CryptCreateHash": CryptCreateHash,
          "CryptHashData": CryptHashData, "CryptGetHashParam": CryptGetHashParam, "CryptDestroyHash": CryptDestroyHash}
    install.FN = FN
    for nm, f in FN.items():
        if nm not in IAT:
            continue
        W.BRIDGED.add(nm)
        W.OSRET.setdefault(nm, 0)

        def hook(u, a, n, _, f=f, nm=nm):
            r = f(u)
            if r is not None:
                u.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
        uc.hook_add(UC_HOOK_CODE, hook, begin=q(IAT[nm]), end=q(IAT[nm]))
