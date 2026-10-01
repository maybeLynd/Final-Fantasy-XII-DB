"""Single-thread Win32 synchronisation for the boot world (OPUS, 2026-09-26), disclosed and STRICT.
Semaphores and events are tracked objects. A wait on a signalled object consumes it (semaphore count - 1, auto-reset event
cleared) and answers WAIT_OBJECT_0; a zero-timeout wait on an unsignalled object answers WAIT_TIMEOUT; a blocking wait on an
unsignalled object would need another thread (no other thread runs in this world), so it STOPS the run by name
("WOULD_BLOCK"). Critical sections and SRW locks are uncontended in one thread: acquire and try-acquire succeed.
Overrides block 332's always-signalled WaitForSingleObject for objects this model created; a handle it did not create is
left to the model installed before it."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP

HBASE = 0x9000


def install(W, uc, log):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
    objs = {}                                     # handle -> {"kind", "count"/"set", "max"/"manual"}
    stop = {"why": None}

    def new(o):
        h = HBASE + 4 * (len(objs) + 1)
        objs[h] = o
        return h

    def CreateSemaphoreW(u):                      # (attrs, initial, maximum, name)
        o = {"kind": "sem", "count": u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF, "max": u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF}
        h = new(o)
        log.append(("CreateSemaphore", "%X" % h, o["count"], o["max"]))
        return h

    def CreateEventW(u):                          # (attrs, manualReset, initialState, name)
        o = {"kind": "event", "manual": u.reg_read(UC_X86_REG_RDX) & 0xFF, "set": u.reg_read(UC_X86_REG_R8) & 0xFF}
        h = new(o)
        log.append(("CreateEvent", "%X" % h, o["manual"], o["set"]))
        return h

    def CreateEventExW(u):                        # (attrs, name, flags, access): flags 1 = manual reset, 2 = initially set
        fl = u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
        o = {"kind": "event", "manual": fl & 1, "set": (fl >> 1) & 1}
        h = new(o)
        log.append(("CreateEventEx", "%X" % h, o["manual"], o["set"]))
        return h

    def ReleaseSemaphore(u):                      # (h, n, &prev)
        h = u.reg_read(UC_X86_REG_RCX)
        if h not in objs:
            return None
        o, n, pp = objs[h], u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_R8)
        if pp:
            uc.mem_write(pp, struct.pack("<I", o["count"]))
        if o["count"] + n > o["max"]:
            return 0
        o["count"] += n
        return 1

    def SetEvent(u):
        h = u.reg_read(UC_X86_REG_RCX)
        if h not in objs:
            return None
        objs[h]["set"] = 1
        return 1

    def ResetEvent(u):
        h = u.reg_read(UC_X86_REG_RCX)
        if h not in objs:
            return None
        objs[h]["set"] = 0
        return 1

    def signalled(o):
        return o["count"] > 0 if o["kind"] == "sem" else bool(o["set"])

    def consume(o):
        if o["kind"] == "sem":
            o["count"] -= 1
        elif not o["manual"]:
            o["set"] = 0

    def wait_one(u, h, ms):
        o = objs[h]
        if signalled(o):
            consume(o)
            return 0
        if ms == 0:
            return 0x102
        stop["why"] = "WOULD_BLOCK on %s %X (timeout %X)" % (o["kind"], h, ms)
        log.append(("WOULD_BLOCK", o["kind"], "%X" % h, "%X" % ms))
        u.emu_stop()
        return 0x102

    def WaitForSingleObject(u):
        h = u.reg_read(UC_X86_REG_RCX)
        if h not in objs:
            return None
        return wait_one(u, h, u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)

    def WaitForMultipleObjectsEx(u):              # (count, handles, waitAll, ms, alertable)
        n, arr, wall, ms = (u.reg_read(r) & 0xFFFFFFFFFFFFFFFF for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))
        n, ms, wall = n & 0xFFFFFFFF, ms & 0xFFFFFFFF, wall & 0xFFFFFFFF
        hs = [q(arr + 8 * i) for i in range(n)]
        if any(h not in objs for h in hs):
            raise RuntimeError("wait on a handle this model did not create")
        if wall:
            if all(signalled(objs[h]) for h in hs):
                for h in hs:
                    consume(objs[h])
                return 0
        else:
            for i, h in enumerate(hs):
                if signalled(objs[h]):
                    consume(objs[h])
                    return i
        if ms == 0:
            return 0x102
        stop["why"] = "WOULD_BLOCK on %d objects" % n
        log.append(("WOULD_BLOCK", n, wall, "%X" % ms))
        u.emu_stop()
        return 0x102

    FN = {"CreateSemaphoreW": CreateSemaphoreW, "CreateSemaphoreA": CreateSemaphoreW, "CreateEventW": CreateEventW,
          "CreateEventA": CreateEventW, "CreateEventExW": CreateEventExW, "ReleaseSemaphore": ReleaseSemaphore,
          "SetEvent": SetEvent, "ResetEvent": ResetEvent, "WaitForSingleObject": WaitForSingleObject,
          "WaitForSingleObjectEx": WaitForSingleObject, "WaitForMultipleObjectsEx": WaitForMultipleObjectsEx,
          "TryEnterCriticalSection": lambda u: 1, "AcquireSRWLockShared": lambda u: 0, "ReleaseSRWLockShared": lambda u: 0}
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
    return objs, stop
