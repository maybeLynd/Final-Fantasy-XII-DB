"""Read-only shipped-file bridge (OPUS, 2026-09-26): the C runtime's fopen / fread / fseek / _fseeki64 / ftell / fclose over the game's own install folder.
A path the game opens is resolved the way the process resolves it (relative to the executable's folder, x64\\); only mode "rb"
is served; a missing file answers NULL; every call is logged. Nothing is ever written."""
import os
import struct
import pefile
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9


def install(W, uc, log):
    IAT = {(imp.name or b"").decode(): imp.address for e in pefile.PE(W.EXE).DIRECTORY_ENTRY_IMPORT for imp in e.imports}
    q = lambda a: struct.unpack("<Q", bytes(uc.mem_read(a, 8)))[0]
    exe_dir = os.path.dirname(W.EXE)
    files = {}
    nxt = [0x7FC00010]

    def cstr(u, a):
        return bytes(u.mem_read(a, 520)).split(b"\0")[0].decode("latin1")

    def fopen(u):
        name, mode = cstr(u, u.reg_read(UC_X86_REG_RCX)), cstr(u, u.reg_read(UC_X86_REG_RDX))
        path = os.path.normpath(os.path.join(exe_dir, name.replace("/", os.sep)))
        if mode not in ("rb", "r") or not os.path.isfile(path):
            log.append(("fopen", name, mode, "NULL"))
            return 0
        h = nxt[0]; nxt[0] += 0x10
        files[h] = open(path, "rb")
        log.append(("fopen", name, mode, os.path.relpath(path, os.path.dirname(exe_dir)), os.path.getsize(path)))
        return h

    def fread(u):                                      # (buf, size, count, FILE *) -> items read
        buf, size, count, h = (u.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9))
        f = files.get(h)
        if f is None or size == 0:
            return 0
        data = f.read(size * count)
        u.mem_write(buf, data)
        log.append(("fread", size, count, len(data)))
        return len(data) // size

    def fclose(u):
        f = files.pop(u.reg_read(UC_X86_REG_RCX), None)
        if f:
            f.close()
        return 0

    def fseek(u):                                      # (FILE *, offset, origin) -> 0; fseek takes a 32-bit long, _fseeki64 64 bits
        h, off, org = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
        f = files.get(h)
        if f is None or org > 2:
            return 0xFFFFFFFF
        wide = fseek.wide
        off = off & (0xFFFFFFFFFFFFFFFF if wide else 0xFFFFFFFF)
        bits = 64 if wide else 32
        if off >> (bits - 1):
            off -= 1 << bits
        f.seek(off, org)
        log.append(("fseek", off, org))
        return 0

    def fseeki64(u):
        fseek.wide = True
        try:
            return fseek(u)
        finally:
            fseek.wide = False
    fseek.wide = False

    def ftell(u):
        f = files.get(u.reg_read(UC_X86_REG_RCX))
        return f.tell() if f else 0xFFFFFFFFFFFFFFFF

    def strncpy(u):                                    # C strncpy: copy up to n bytes, pad the rest with NULs; returns dst
        d, s, n = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8)
        b = bytes(u.mem_read(s, n)).split(b"\0")[0][:n] if n else b""
        u.mem_write(d, b + bytes(n - len(b)))
        return d

    for nm, f in (("fopen", fopen), ("fread", fread), ("fclose", fclose), ("strncpy", strncpy),
                  ("fseek", fseek), ("_fseeki64", fseeki64), ("ftell", ftell), ("_ftelli64", ftell)):
        if nm not in IAT:
            continue
        W.OSRET[nm] = 0
        W.BRIDGED.add(nm)
        uc.hook_add(UC_HOOK_CODE, (lambda f: lambda u, a, n, _: u.reg_write(UC_X86_REG_RAX, f(u) & 0xFFFFFFFFFFFFFFFF))(f),
                    begin=q(IAT[nm]), end=q(IAT[nm]))
    return IAT
