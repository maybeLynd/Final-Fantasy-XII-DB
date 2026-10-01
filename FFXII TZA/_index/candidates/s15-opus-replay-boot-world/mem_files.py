"""Memory-only writable files for the boot world (OPUS, 2026-09-26), disclosed; nothing is written to disk.
A fresh install has no user configuration: a read open of a name never written answers ENOENT (last error 2). A write open
("w"/"wb") creates the file in memory and answers success, and the thread's last error becomes 0 - what CreateFileW with
CREATE_ALWAYS reports for a file that did not exist. fwrite appends, fclose closes; a later read open of the same name reads
back what was written (fseek / ftell / fread over it). Installed after os_model / boot_model / file_bridge: a call on a
handle this model did not open is left to the model installed before it."""
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9

FBASE = 0x7BA00000


def install(W, uc, log, last):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
    uc.mem_map(FBASE, 0x10000)
    store, open_ = {}, {}                           # name -> bytearray; handle -> [name, pos, writable]

    def wz(a):
        b = bytearray()
        while len(b) < 1040:
            c = bytes(uc.mem_read(a + len(b), 2))
            if c == b"\0\0":
                break
            b += c
        return b.decode("utf-16-le")

    def _wfopen_s(u):                               # (FILE **, name, mode) -> errno
        pp, name, mode = u.reg_read(UC_X86_REG_RCX), wz(u.reg_read(UC_X86_REG_RDX)), wz(u.reg_read(UC_X86_REG_R8))
        key = name.lower()
        if "w" in mode or "a" in mode:
            if "w" in mode or key not in store:
                store[key] = bytearray()
            h = FBASE + 0x100 * (len(open_) + 1)
            open_[h] = [key, len(store[key]) if "a" in mode else 0, True]
            uc.mem_write(pp, struct.pack("<Q", h))
            last["err"] = 0
            log.append(("mem_wfopen_s", name, mode, "created"))
            return 0
        if key in store:
            h = FBASE + 0x100 * (len(open_) + 1)
            open_[h] = [key, 0, False]
            uc.mem_write(pp, struct.pack("<Q", h))
            log.append(("mem_wfopen_s", name, mode, "read-back", len(store[key])))
            return 0
        uc.mem_write(pp, bytes(8))
        last["err"] = 2                             # ERROR_FILE_NOT_FOUND
        log.append(("mem_wfopen_s", name, mode, "ENOENT"))
        return 2

    def mine(r):
        return r in open_

    def fwrite(u):                                  # (buf, size, count, FILE *) -> items written
        fp = u.reg_read(UC_X86_REG_R9)
        if not mine(fp):
            return None
        size, count = u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        data = bytes(uc.mem_read(u.reg_read(UC_X86_REG_RCX), size * count)) if size * count else b""
        f = open_[fp]
        buf = store[f[0]]
        buf[f[1]:f[1] + len(data)] = data
        f[1] += len(data)
        log.append(("mem_fwrite", f[0], len(data)))
        return count

    def fread(u):                                   # (buf, size, count, FILE *) -> items read
        fp = u.reg_read(UC_X86_REG_R9)
        if not mine(fp):
            return None
        size, count = u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        f = open_[fp]
        data = bytes(store[f[0]][f[1]:f[1] + size * count])
        n = len(data) // size if size else 0
        uc.mem_write(u.reg_read(UC_X86_REG_RCX), data[:n * size])
        f[1] += n * size
        return n

    def fseek(u):                                   # (FILE *, offset, origin) -> 0
        fp = u.reg_read(UC_X86_REG_RCX)
        if not mine(fp):
            return None
        off = u.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
        off = off - (1 << 32) if off >> 31 else off
        org = u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
        f = open_[fp]
        f[1] = (0, f[1], len(store[f[0]]))[org] + off
        return 0

    def ftell(u):
        fp = u.reg_read(UC_X86_REG_RCX)
        return open_[fp][1] if mine(fp) else None

    def fclose(u):
        fp = u.reg_read(UC_X86_REG_RCX)
        if not mine(fp):
            return None
        log.append(("mem_fclose", open_[fp][0], len(store[open_[fp][0]])))
        del open_[fp]
        return 0

    for nm, f in (("_wfopen_s", _wfopen_s), ("fwrite", fwrite), ("fread", fread), ("fseek", fseek), ("ftell", ftell), ("fclose", fclose)):
        if nm not in IAT:
            continue
        W.BRIDGED.add(nm)
        W.OSRET.setdefault(nm, 0)

        def hook(u, a, n, _, f=f):
            r = f(u)
            if r is not None:
                u.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
        uc.hook_add(UC_HOOK_CODE, hook, begin=q(IAT[nm]), end=q(IAT[nm]))
    return store
