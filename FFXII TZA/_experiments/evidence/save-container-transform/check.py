# EXP-088 - save-container transform, isolated original-code execution.
#
# CONTRACT-save-container-transform.md is the last contract in gate26's
# nothing-executed bucket. Its §13 names a SWE2-ORACLE-shaped experiment: "the
# container is a pure function of the file and the title" - round-trip a real
# save through deflate(9) -> RC4(MD5(rotated title)) and invert. This harness
# executes the writer, encrypt, decrypt, reader-inner and reader bodies plus
# the ENTIRE shipped zlib 1.2.11 subtree as shipped bytes at canonical VAs.
#
#   REAL (executed as shipped):
#     00866200  container writer (mode-0 arm: header, rand->n, deflate, encrypt,
#               fwrite, temp-file/CopyFileW commit protocol, frees its ctx)
#     00865AE0  encrypt: CryptAcquireContext (NEWKEYSET retry), rotate title,
#               B[31]=0, strlen, CryptHashData, CryptDeriveKey(RC4,0x800000),
#               CryptEncrypt in 1000-byte chunks
#     00865840  decrypt: same key pipeline, CryptDecrypt in 1000-byte chunks
#     00865D90  reader-inner: _aligned_malloc(declared), decrypt, uncompress
#     008666B0  reader: fopen/fseek/ftell/fread, gates SAFH / size>4 / size>12 /
#               n<=31 / declared<=1MiB, reserve, push_back loop into the global
#               byte vector at 01F44D40, exact-length + positive checks
#     0087AF40  deflate wrapper (deflateInit_ level=[rsp+0x20], deflate loop,
#               deflateEnd) + the whole zlib deflate/inflate subtree as shipped
#     00866150 / 00865720 / 0019xxxx  real vector reserve/grow + wstring helpers
#     00808C40  __security_check_cookie
#
#   HLE (IAT stubs - disclosed fixtures, all calls logged with args):
#     CryptoAPI x9 - RC4 model: key bytes = MD5 digest of the hashed material
#       (matches the documented MS derive for a 16-byte RC4 key from an MD5
#       hash; writer and reader share the model so round-trip is consistent).
#       CryptDeriveKey semantics live in advapi32, OUTSIDE the EXE - the model
#       is a fixture, not executed code.
#     stdio: _wfopen_s/_wfopen/fread/fwrite/fseek/ftell/fclose/_wremove over an
#       in-memory filesystem keyed on the wide path string.
#     rand (scripted), GetTempPathW, SetFileAttributesW, CopyFileW, heap funcs
#       (_aligned_malloc/_aligned_free/malloc/calloc/free), CRT mem/string funcs,
#       std exception throws + _invalid_parameter_noinfo_noreturn (loud if hit).
#     Game allocator vtable on the vector at 01F44D40 (+0x10 alloc, +0x18 free).
#
# The whole image is mapped as the loader maps it (sections at canonical VAs,
# file bytes where raw exists). All fixture I/O goes through ctypes host
# buffers via mem_map_ptr (see EXP-087: the host's unicorn DLLs intermittently
# report UNMAPPED from uc_mem_write/read on mapped pages).
#
# Unresolved by construction: CryptDeriveKey's exact internal expansion is
# modelled, so byte-exact ciphertext parity against a REAL save file awaits a
# real file; what is executed here is the shipped container pipeline itself.

import ctypes, hashlib, json, os, struct, sys, zlib

sys.path.insert(0, r"Database/Tools/work/ASTRA/python-libs")
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000

IMG_LO = BASE                 # whole image mapped 0x120000 .. IMG_HI
IMG_HI = 0x2F800000           # covers .reloc end 0x2F73360
STUBS  = 0x50000000           # HLE stub page: each stub 0x10 bytes, byte 0 = 0xC3
TRAP   = 0x50010000           # unhandled-IAT trap page (index-encoded stubs)
HEAP   = 0x40000000           # guest heap arena (16 MiB)
STACK  = 0x61000000
RETQ   = 0x62000000
CTX    = 0x60004000           # writer ctx: +4 mode, +8 inline wchar path
PATHW  = 0x60006000           # reader path argument (wide string)
VTAB   = 0x60007000           # allocator vtable for the global vector

G_VEC   = 0x1F44D40           # global byte vector {+0 begin, +8 end, +0x10 cap, +0x18 vtbl}
G_N     = 0x2EB3868           # rotation amount global (movsxd)
G_N2    = 0x2EB386C           # writer-tail bookkeeping global
G_D4    = 0x2B40E04           # writer-tail flag global
G_COOKIE= 0x1F44830           # __security_cookie image

# IAT slot -> stub index (stub VA = STUBS + idx*0x10)
IAT = {
    "rand":                        0x8C3098,
    "GetTempPathW":                0x8C23F0,
    "SetFileAttributesW":          0x8C23F8,
    "CopyFileW":                   0x8C23E8,
    "_wremove":                    0x8C2B08,
    "_wfopen_s":                   0x8C2E00,
    "_wfopen":                     0x8C2E08,
    "fseek":                       0x8C2EE8,
    "ftell":                       0x8C2EE0,
    "fread":                       0x8C2EF0,
    "fwrite":                      0x8C2F40,
    "fclose":                      0x8C2F00,
    "memcpy":                      0x8C2A68,
    "memmove":                     0x8C2A40,
    "memset":                      0x8C2A60,
    "strncpy":                     0x8C2F70,
    "strlen":                      0x8C2F60,
    "_aligned_malloc":             0x8C2B60,
    "_aligned_free":               0x8C2B70,
    "malloc":                      0x8C2B40,
    "calloc":                      0x8C2B58,
    "free":                        0x8C2B48,
    "_invalid_parameter_noinfo_noreturn": 0x8C2DA8,
    "_Xout_of_range":              0x8C2CF0,
    "_Xlength_error":              0x8C2CE8,
    "CryptAcquireContextW":        0x8C2000,
    "CryptCreateHash":             0x8C2048,
    "CryptHashData":               0x8C2040,
    "CryptDeriveKey":              0x8C2030,
    "CryptEncrypt":                0x8C2020,
    "CryptDecrypt":                0x8C2018,
    "CryptDestroyKey":             0x8C2028,
    "CryptDestroyHash":            0x8C2038,
    "CryptReleaseContext":         0x8C2008,
}
STUB_NAMES = list(IAT.keys()) + ["alloc_v", "free_v"]     # vtable stubs last
STUB_VA = {name: STUBS + i * 0x10 for i, name in enumerate(STUB_NAMES)}
VA_STUB = {STUB_VA[n]: n for n in STUB_NAMES}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)

def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    def rva2off(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                return ra + rva - sva
        return None
    # import directory -> every IAT slot VA (name table for the trap report)
    iat_names = {}
    imp_dir = pe + 24 + (112 if struct.unpack_from("<H", raw, pe + 24)[0] == 0x20B else 96) + 8
    imp_rva, _ = struct.unpack_from("<2I", raw, imp_dir)
    off2 = rva2off(imp_rva)
    i = 0
    while True:
        ilt, ts, fwd, name_rva, iat_rva = struct.unpack_from("<5I", raw, off2 + 20 * i)
        if name_rva == 0:
            break
        dll = raw[rva2off(name_rva):].split(b"\0")[0].decode()
        ilt = ilt or iat_rva
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt) + 8 * j)[0]
            if e == 0:
                break
            if e >> 63:
                nm = f"#{e & 0xffff}"
            else:
                no = rva2off(e & 0x7FFFFFFF)
                nm = raw[no + 2:].split(b"\0")[0].decode()
            iat_names[BASE + iat_rva + 8 * j] = f"{dll}!{nm}"
            j += 1
        i += 1
    return raw, secs, iat_names

class GuestMem:
    """Host-backed guest memory via mem_map_ptr (EXP-087 workaround: the host's
    unicorn DLLs intermittently fail uc_mem_write/read on mapped pages)."""
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        ptr = ctypes.addressof(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ptr)
        self.regions.append((addr, size, ptr))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), data, len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def wstr(self, addr):
        out = b""
        while True:
            c = self.r(addr, 2)
            if c == b"\0\0": break
            out += c; addr += 2
        return out.decode("utf-16-le")

# ---- HLE helpers -------------------------------------------------------------
def rc4(key, data):
    S = list(range(256)); j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    i = j = 0; out = bytearray()
    for c in data:
        i = (i + 1) & 0xFF; j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        out.append(c ^ S[(S[i] + S[j]) & 0xFF])
    return bytes(out)

def ref_container(payload, n, title):
    """Python reference for the documented transform (zlib.compress level 9)."""
    B = list(title[:32])
    B = B[n:] + B[:n]; B[31] = 0
    key = hashlib.md5(bytes(B[:31])).digest()
    ct = rc4(key, zlib.compress(payload, 9))
    return b"SAFH" + dw(len(payload)) + dw(n) + ct

class World:
    def __init__(self, case, raw, secs, iat_names):
        self.case = case
        self.iat_names = iat_names
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x1000000), (STACK, 0x100000), (RETQ, 0x1000),
                     (STUBS & ~0xFFF, 0x20000), (0x60000000, 0x20000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        for va in range(STUBS, TRAP, 0x10):
            gm.w(va, b"\xc3")
        for va in range(TRAP, TRAP + 0x10000, 0x10):
            gm.w(va, b"\xc3")
        # every IAT slot -> an index-encoded trap stub; known slots -> their HLE stub
        self.trap_of_slot = {}
        self.slot_of_trap = {}
        for i, slot in enumerate(sorted(iat_names)):
            tv = TRAP + (i % 0x1000) * 0x10
            self.trap_of_slot[slot] = tv
            self.slot_of_trap[tv] = slot
            gm.w(slot, qw(tv))
        for name, slot in IAT.items():
            gm.w(slot, qw(STUB_VA[name]))
        # cookie + globals
        gm.w(G_COOKIE, qw(0x0000ABCD12340000))
        gm.w(G_N, dw(case.get("n", -1) & 0xFFFFFFFF))
        gm.w(G_N2, dw(case.get("g_n2", 0)))
        gm.w(G_D4, dw(case.get("g_d4", 0)))
        # global byte vector + allocator vtable
        self.heap_ptr = HEAP
        self.allocs = {}
        vec = case.get("vec", None)
        if vec is None:
            gm.w(G_VEC + 0x00, qw(0)); gm.w(G_VEC + 0x08, qw(0))
            gm.w(G_VEC + 0x10, qw(0))
        else:
            buf = self.galloc(len(vec), init=vec)
            gm.w(G_VEC + 0x00, qw(buf)); gm.w(G_VEC + 0x08, qw(buf + len(vec)))
            gm.w(G_VEC + 0x10, qw(buf + len(vec)))
        gm.w(G_VEC + 0x18, qw(VTAB))
        for i in range(8):
            gm.w(VTAB + i * 8, qw(TRAP + 0x8000 + i * 0x10))
        gm.w(VTAB + 0x10, qw(STUB_VA["alloc_v"]))
        gm.w(VTAB + 0x18, qw(STUB_VA["free_v"]))
        # writer ctx: {+0 ?, +4 mode, +8 wchar path[]}
        gm.w(CTX, b"\0" * 0x400)
        gm.w(CTX + 4, dw(case.get("mode", 0)))
        gm.w(CTX + 8, self.tgt_path().encode("utf-16-le") + b"\0\0")
        # reader path argument
        gm.w(PATHW, case.get("path", "slot01.sav").encode("utf-16-le") + b"\0\0")
        # preset guest memory (unit-call buffers etc.)
        for va, data in case.get("fill", []):
            gm.w(va, data)
        # per-case byte patches (mutants)
        for va, data in case.get("patch", []):
            gm.w(va, data)
        # HLE state
        self.files = dict(case.get("files", {}))   # path -> bytearray
        self.handles = {}
        self.next_fd = 0x100
        self.rand_seq = list(case.get("rand", [7]))
        self.rand_i = 0
        self.trace = []
        self.faults = []
        self.hist = []
        self.crypto = {"prov": 1, "hashes": {}, "keys": {}, "next": 0x500}
        self.control = case.get("ctl", {})        # e.g. fail_acquire: 2
        self.calls = {n: 0 for n in STUB_NAMES}
        self.trapped = []
        uc = self.uc
        uc.hook_add(UC_HOOK_CODE, self.on_code, begin=STUBS, end=TRAP + 0xFFFF)
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def tgt_path(self):
        return self.case.get("target", "slot01.sav")

    def galloc(self, n, init=b""):
        a = self.heap_ptr
        self.heap_ptr += max(1, (n + 0xF) & ~0xF)
        if init:
            self.gm.w(a, init)
        self.allocs[a] = n
        return a

    # ---- stub dispatch -------------------------------------------------------
    def pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        return ret

    def on_code(self, uc, addr, size, _):
        if addr >= TRAP:
            slot = self.slot_of_trap.get(addr, 0)
            self.trapped.append(addr)
            self.faults.append(("TRAP", self.iat_names.get(slot, hex(addr)),
                                uc.reg_read(UC_X86_REG_RIP)))
            uc.emu_stop()
            return
        name = VA_STUB.get(addr)
        if name is None:
            return
        self.calls[name] += 1
        fn = getattr(self, "h_" + name.replace("-", "_"), self.h_unhandled)
        fn(name)
        uc.reg_write(UC_X86_REG_RIP, self.pop_ret())

    def h_unhandled(self, name):
        self.trace.append((name, "UNHANDLED"))
        self.uc.reg_write(UC_X86_REG_RAX, 0)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, uc.reg_read(UC_X86_REG_RIP)))
        return False

    # ---- register/stack args -------------------------------------------------
    def args(self):
        uc = self.uc
        return (uc.reg_read(UC_X86_REG_RCX), uc.reg_read(UC_X86_REG_RDX),
                uc.reg_read(UC_X86_REG_R8), uc.reg_read(UC_X86_REG_R9))
    def sarg(self, i):
        sp = self.uc.reg_read(UC_X86_REG_RSP)
        return struct.unpack("<Q", self.gm.r(sp + 0x28 + i * 8, 8))[0]
    def ret(self, v):
        self.uc.reg_write(UC_X86_REG_RAX, v & 0xFFFFFFFFFFFFFFFF)

    # ---- CRT -----------------------------------------------------------------
    def h_rand(self, name):
        v = self.rand_seq[min(self.rand_i, len(self.rand_seq) - 1)]
        self.rand_i += 1
        self.trace.append((name, hex(v & 0xFFFFFFFF)))
        self.ret(v & 0xFFFFFFFF)
    def h__aligned_malloc(self, name):
        n, align = self.args()[:2]
        self.heap_ptr = (self.heap_ptr + align - 1) & ~(align - 1)
        a = self.galloc(int(n))
        self.trace.append((name, n, align, hex(a)))
        self.ret(a)
    def h_malloc(self, name):
        n = self.args()[0]
        a = self.galloc(int(n))
        self.trace.append((name, n, hex(a)))
        self.ret(a)
    def h_calloc(self, name):
        n, sz = self.args()[:2]
        a = self.galloc(int(n) * int(sz))
        self.trace.append((name, n, sz, hex(a)))
        self.ret(a)
    def h__aligned_free(self, name):
        p = self.args()[0]
        self.allocs.pop(p, None)
        self.trace.append((name, hex(p)))
    def h_free(self, name):
        p = self.args()[0]
        self.allocs.pop(p, None)
        self.trace.append((name, hex(p)))
    def h_memcpy(self, name):
        d, s, n = self.args()[:3]
        if n:
            self.gm.w(d, self.gm.r(s, n))
        self.trace.append((name, hex(d), hex(s), n))
        self.ret(d)
    def h_memmove(self, name):
        self.h_memcpy(name)
    def h_memset(self, name):
        d, c, n = self.args()[:3]
        self.gm.w(d, bytes([c & 0xFF]) * n)
        self.trace.append((name, hex(d), c & 0xFF, n))
        self.ret(d)
    def h_strncpy(self, name):
        d, s, n = self.args()[:3]
        src = self.gm.r(s, n)
        z = src.find(b"\0")
        if z >= 0:
            src = src[:z] + b"\0" * (n - z)
        self.gm.w(d, src)
        self.trace.append((name, hex(d), hex(s), n))
        self.ret(d)
    def h_strlen(self, name):
        s = self.args()[0]
        n = self.gm.r(s, 0x10000).find(b"\0")
        self.trace.append((name, hex(s), n))
        self.ret(n)
    def h__invalid_parameter_noinfo_noreturn(self, name):
        self.faults.append(("INVALID_PARAM", 0, self.uc.reg_read(UC_X86_REG_RIP)))
        self.uc.emu_stop()
    def h__Xout_of_range(self, name):
        self.faults.append(("XOUT_OF_RANGE", 0, self.uc.reg_read(UC_X86_REG_RIP)))
        self.uc.emu_stop()
    def h__Xlength_error(self, name):
        self.faults.append(("XLENGTH", 0, self.uc.reg_read(UC_X86_REG_RIP)))
        self.uc.emu_stop()

    # ---- game allocator vtable ----------------------------------------------
    def h_alloc_v(self, name):
        this, n, fl = self.args()[:3]
        a = self.galloc(int(n))
        self.trace.append((name, n, hex(a)))
        self.ret(a)
    def h_free_v(self, name):
        this, p, n = self.args()[:3]
        self.allocs.pop(p, None)
        self.trace.append((name, hex(p), n))

    # ---- stdio model ---------------------------------------------------------
    def _open(self, path, mode):
        for h, f in self.handles.items():
            if f["path"] == path and not f["closed"]:
                pass
        writing = any(c in mode for c in "wax")
        if writing:
            self.files[path] = bytearray()
        if path not in self.files:
            return None
        fd = self.next_fd; self.next_fd += 1
        self.handles[fd] = {"path": path, "pos": 0, "closed": False,
                            "write": writing}
        return fd
    def h__wfopen_s(self, name):
        pfp, pathp, modep = self.args()[:3]
        path = self.gm.wstr(pathp) if pathp else ""
        mode = self.gm.wstr(modep) if modep else ""
        fd = self._open(path, mode)
        deny = self.control.get("deny_open")          # substring -> forced ENOENT
        if deny and deny in path:
            fd = None
        self.trace.append((name, path, mode, "ok" if fd else "ENOENT"))
        if fd is None:
            self.gm.w(pfp, qw(0)); self.ret(2)
        else:
            self.gm.w(pfp, qw(fd)); self.ret(0)
    def h__wfopen(self, name):
        pathp, modep = self.args()[:2]
        path = self.gm.wstr(pathp) if pathp else ""
        mode = self.gm.wstr(modep) if modep else ""
        fd = self._open(path, mode)
        self.trace.append((name, path, mode, fd or 0))
        self.ret(fd or 0)
    def h_fseek(self, name):
        fd, off, wh = self.args()[:3]
        f = self.handles.get(fd)
        if not f: self.ret(-1); return
        data = self.files[f["path"]]
        f["pos"] = off if wh == 0 else f["pos"] + off if wh == 1 else len(data) + off
        self.trace.append((name, fd, off, wh, f["pos"]))
        self.ret(0)
    def h_ftell(self, name):
        fd = self.args()[0]
        f = self.handles.get(fd)
        self.ret(f["pos"] if f else -1)
    def h_fread(self, name):
        buf, sz, cnt, fd = self.args()[:4]
        f = self.handles.get(fd)
        if not f: self.ret(0); return
        data = self.files[f["path"]]
        got = min(sz * cnt, len(data) - f["pos"])
        self.gm.w(buf, bytes(data[f["pos"]:f["pos"] + got]))
        f["pos"] += got
        items = got // sz if sz else 0
        self.trace.append((name, fd, sz, cnt, items))
        self.ret(items)
    def h_fwrite(self, name):
        buf, sz, cnt, fd = self.args()[:4]
        f = self.handles.get(fd)
        if not f: self.ret(0); return
        data = self.files[f["path"]]
        blob = self.gm.r(buf, sz * cnt)
        end = f["pos"] + len(blob)
        if end > len(data):
            data += b"\0" * (end - len(data))
        data[f["pos"]:end] = blob
        f["pos"] = end
        self.trace.append((name, fd, sz, cnt, len(blob)))
        self.ret(cnt)
    def h_fclose(self, name):
        fd = self.args()[0]
        if fd in self.handles:
            self.handles[fd]["closed"] = True
        self.trace.append((name, fd))
        self.ret(0)
    def h__wremove(self, name):
        path = self.gm.wstr(self.args()[0])
        self.files.pop(path, None)
        self.trace.append((name, path))
        self.ret(0)
    def h_GetTempPathW(self, name):
        n, buf = self.args()[:2]
        s = "C:\\TMP\\".encode("utf-16-le")
        self.gm.w(buf, s)
        self.trace.append((name, n))
        self.ret(len(s) // 2)
    def h_SetFileAttributesW(self, name):
        pathp, attr = self.args()[:2]
        self.trace.append((name, self.gm.wstr(pathp) if pathp else "", attr))
        self.ret(1)
    def h_CopyFileW(self, name):
        sp, dp, fe = self.args()[:3]
        s = self.gm.wstr(sp) if sp else ""
        d = self.gm.wstr(dp) if dp else ""
        ok = s in self.files and not (fe and d in self.files)
        if ok:
            self.files[d] = bytearray(self.files[s])
        self.trace.append((name, s, d, fe, ok))
        self.ret(1 if ok else 0)

    # ---- CryptoAPI model -----------------------------------------------------
    def h_CryptAcquireContextW(self, name):
        pph, cont, prov, typ, fl = (*self.args(), self.sarg(0))
        n = self.calls[name]
        failn = self.control.get("fail_acquire", 0)
        if n <= failn:
            self.trace.append((name, "FAIL", fl))
            self.gm.w(pph, qw(0)); self.ret(0); return
        self.gm.w(pph, qw(self.crypto["prov"]))
        self.trace.append((name, "ok", "type=%d" % typ, "flags=0x%x" % fl))
        self.ret(1)
    def h_CryptCreateHash(self, name):
        prov, alg, key, fl, ph = (*self.args(), self.sarg(0))
        if self.control.get("fail_createhash"):
            self.trace.append((name, "FAIL")); self.ret(0); return
        h = self.crypto["next"]; self.crypto["next"] += 1
        self.crypto["hashes"][h] = bytearray()
        self.gm.w(ph, qw(h))
        self.trace.append((name, "alg=0x%x" % alg, "h=%x" % h))
        self.ret(1)
    def h_CryptHashData(self, name):
        h, data, n, fl = self.args()[:4]
        if self.control.get("fail_hashdata"):
            self.trace.append((name, "FAIL")); self.ret(0); return
        blob = self.gm.r(data, n)
        self.crypto["hashes"][h] += blob
        self.trace.append((name, "h=%x" % h, "len=%d" % n, "data=" + blob.hex()))
        self.ret(1)
    def h_CryptDeriveKey(self, name):
        prov, alg, h, fl, pk = (*self.args(), self.sarg(0))
        if self.control.get("fail_derive"):
            self.trace.append((name, "FAIL")); self.ret(0); return
        digest = hashlib.md5(bytes(self.crypto["hashes"][h])).digest()
        k = self.crypto["next"]; self.crypto["next"] += 1
        S = list(range(256)); j = 0
        for i in range(256):
            j = (j + S[i] + digest[i % len(digest)]) & 0xFF
            S[i], S[j] = S[j], S[i]
        self.crypto["keys"][k] = {"S": S, "i": 0, "j": 0}
        self.gm.w(pk, qw(k))
        self.trace.append((name, "alg=0x%x" % alg, "flags=0x%x" % fl,
                           "key=%x" % k, "md5=" + digest.hex()))
        self.ret(1)
    def _rc4_step(self, k, buf, n):
        st = self.crypto["keys"][k]
        S, i, j = st["S"], st["i"], st["j"]
        data = bytearray(self.gm.r(buf, n))
        for x in range(n):
            i = (i + 1) & 0xFF; j = (j + S[i]) & 0xFF
            S[i], S[j] = S[j], S[i]
            data[x] ^= S[(S[i] + S[j]) & 0xFF]
        st["i"], st["j"] = i, j
        self.gm.w(buf, bytes(data))
    def h_CryptEncrypt(self, name):
        key, h, final, fl = self.args()[:4]
        buf, plen, buflen = self.sarg(0), self.sarg(1), self.sarg(2)
        n = struct.unpack("<I", self.gm.r(plen, 4))[0]
        if self.control.get("fail_encrypt"):
            self.trace.append((name, "FAIL")); self.ret(0); return
        self._rc4_step(key, buf, n)
        self.trace.append((name, "key=%x" % key, "final=%d" % final,
                           "len=%d" % n, "bufcap=%d" % buflen))
        self.ret(1)
    def h_CryptDecrypt(self, name):
        key, h, final, fl = self.args()[:4]
        buf, plen = self.sarg(0), self.sarg(1)
        n = struct.unpack("<I", self.gm.r(plen, 4))[0]
        if self.control.get("fail_decrypt"):
            self.trace.append((name, "FAIL")); self.ret(0); return
        self._rc4_step(key, buf, n)
        self.trace.append((name, "key=%x" % key, "final=%d" % final, "len=%d" % n))
        self.ret(1)
    def h_CryptDestroyKey(self, name):
        k = self.args()[0]
        self.crypto["keys"].pop(k, None)
        self.trace.append((name, "key=%x" % k))
        self.ret(1)
    def h_CryptDestroyHash(self, name):
        h = self.args()[0]
        self.crypto["hashes"].pop(h, None)
        self.trace.append((name, "h=%x" % h))
        self.ret(1)
    def h_CryptReleaseContext(self, name):
        p, fl = self.args()[:2]
        self.trace.append((name, "prov=%x" % p, "flags=%x" % fl))
        self.ret(1)

TITLE_VA = 0x1CCFCF8    # image .rdata: the 32-char title string

def build(case, raw, secs, iat_names):
    return World(case, raw, secs, iat_names)

def invoke(w, va, rcx=0, rdx=0, r8=0, r9=0, stack_args=()):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    for i, a in enumerate(stack_args):
        gm.w(sp - 0x100 + i * 8, qw(a))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    try:
        uc.emu_start(va, RETQ, count=4_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

# ---- case layer --------------------------------------------------------------
def img_read(raw, secs, va, n):
    r = va - BASE
    for sva, vs, ra, rs in secs:
        if sva <= r < sva + rs:
            return raw[ra + (r - sva):ra + (r - sva) + n]
    raise AssertionError("VA not in image: %x" % va)

W_ENTRY, R_ENTRY, ENC, DEC = 0x866200, 0x8666B0, 0x865AE0, 0x865840
TPATH = "slot01.sav"

def det_bytes(n, seed=0):
    out = bytearray()
    while len(out) < n:
        out += hashlib.sha256(b"payload%d" % seed).digest()
        seed += 1
    return bytes(out[:n])

def patterned(n):
    return bytes((i * 7 + (i >> 5)) & 0xFF for i in range(n))

def vec_bytes(w):
    b = struct.unpack("<Q", w.gm.r(G_VEC, 8))[0]
    e = struct.unpack("<Q", w.gm.r(G_VEC + 8, 8))[0]
    return w.gm.r(b, e - b) if b and e >= b else b""

def out_struct(w, rax):
    if not rax or rax < IMG_LO and not (0x40000000 <= rax < 0x50000000):
        return None
    try:
        f0 = struct.unpack("<I", w.gm.r(rax, 4))[0]
        f4 = struct.unpack("<I", w.gm.r(rax + 4, 4))[0]
        return (f0, f4)
    except Exception:
        return None

def run_case(case, raw, secs, iat_names):
    w = build(case, raw, secs, iat_names)
    rets = []
    for ph in case.get("phases", [{}]):
        rets.append(invoke(w, ph.get("entry", case.get("entry", W_ENTRY)),
                           rcx=ph.get("rcx", case.get("rcx", CTX)),
                           rdx=ph.get("rdx", case.get("rdx", 0)),
                           r8=ph.get("r8", case.get("r8", 0)),
                           r9=ph.get("r9", case.get("r9", 0))))
    snap = {
        "rets": [hex(r) for r in rets],
        "vec": vec_bytes(w).hex(),
        "vec_len": len(vec_bytes(w)),
        "g_n": struct.unpack("<i", w.gm.r(G_N, 4))[0],
        "g_n2": struct.unpack("<i", w.gm.r(G_N2, 4))[0],
        "files": {p: bytes(v).hex() for p, v in w.files.items()},
        "trace": [list(t) if isinstance(t, tuple) else t for t in w.trace],
        "faults": [list(f) if isinstance(f, tuple) else f for f in w.faults],
        "trapped": [hex(t) for t in w.trapped],
        "out": out_struct(w, rets[-1]) if rets else None,
    }
    return snap, w

def rotb(title, n):
    B = list(title[:32])
    B = B[n:] + B[:n]; B[31] = 0
    return bytes(B[:31])

def cases(title):
    C = lambda **k: k
    PAYLOAD = patterned(0x400)
    ref = ref_container(PAYLOAD, 7, title)          # python-side valid container, n=7
    SRC = patterned(0x200)
    ENC_DST, ENC_LEN, ENC_SRC = HEAP + 0x800000, HEAP + 0x900000, HEAP + 0x700000
    def enc_case(nm, n, src, cap=None, **kw):
        cap = cap if cap is not None else max(len(src), 0x40)
        return C(name=nm, entry=ENC, n=n,
                 fill=[(ENC_SRC, src), (ENC_LEN, dw(cap))],
                 phases=[{"entry": ENC, "rcx": ENC_DST, "rdx": ENC_LEN,
                          "r8": ENC_SRC, "r9": len(src)}],
                 **kw)
    def dec_case(nm, n, ct, **kw):
        return C(name=nm, entry=DEC, n=n,
                 fill=[(ENC_SRC, ct), (ENC_LEN, dw(len(ct)))],
                 phases=[{"entry": DEC, "rcx": ENC_DST, "rdx": ENC_LEN,
                          "r8": ENC_SRC, "r9": len(ct)}],
                 **kw)
    def fin_bytes(snap, path=TPATH):
        return bytes.fromhex(snap["files"].get(path, ""))
    out = []
    # ---------- writer (entry 00866200, rcx=ctx; payload = global vector) ----
    out += [
        C(name="w-write", entry=W_ENTRY, vec=PAYLOAD, rand=[7], target=TPATH,
          check=lambda s, w: (fin_bytes(s) == ref
                              and s["g_n"] == 7
                              and not s["trapped"] and not s["faults"]),
          why="writer mode0: shipped zlib deflate + shipped encrypt produce the "
              "container; compared BYTE-EXACT vs the python reference (SAFH + "
              "declared + n + RC4(MD5(rotl(title)))) - single CryptEncrypt final=1"),
        C(name="w-roundtrip", entry=W_ENTRY, vec=PAYLOAD, rand=[7], target=TPATH,
          path=TPATH,
          phases=[{"entry": W_ENTRY, "rcx": CTX},
                  {"entry": R_ENTRY, "rcx": PATHW, "rdx": 1}],
          check=lambda s, w: (s["vec"] == PAYLOAD.hex() and not s["faults"]
                              and not s["trapped"]),
          why="writer -> reader through shipped code both directions: 008666B0 "
              "re-reads the committed file, shipped decrypt + shipped zlib inflate "
              "reproduce the payload in the global vector"),
        C(name="w-fopen-fail", entry=W_ENTRY, vec=PAYLOAD, rand=[7],
          target=TPATH, ctl={"deny_open": "sav_tmp"},
          check=lambda s, w: (TPATH not in s["files"]
                              and not any(t[0] == "rand" for t in s["trace"])
                              and not any(t[0] == "fwrite" for t in s["trace"])
                              and not s["faults"]),
          why="tmp _wfopen_s fails -> frees ctx and returns before rand/header"),
        C(name="w-incompressible", entry=W_ENTRY, vec=det_bytes(64), rand=[3],
          target=TPATH,
          check=lambda s, w: (TPATH not in s["files"]
                              and len(s["files"].get("C:\\TMP\\sav_tmp", "")) == 24
                              and not any(t[0] == "CryptEncrypt" for t in s["trace"])
                              and any(t[0] == "fwrite" and t[2] == 12
                                      for t in s["trace"])),
          why="deflate(9) output > dst capacity (payload-size buffer): wrapper "
              "returns nonzero -> NO encrypt, NO commit: the 12-byte header-only "
              "temp file is abandoned in the temp dir and eax is still 0 - a "
              "silent save abort the return value cannot distinguish"),
        C(name="w-mode1", entry=W_ENTRY, vec=PAYLOAD, rand=[7], mode=1,
          check=lambda s, w: (s["vec_len"] == 0
                              and not any(t[0] == "rand" for t in s["trace"])
                              and TPATH not in s["files"]),
          why="ctx+4 != 0: skips everything, frees ctx, truncates the vector"),
        C(name="w-null-ctx", entry=W_ENTRY, rcx=0, vec=PAYLOAD, rand=[7],
          check=lambda s, w: any(isinstance(f[1], int) and f[1] == 4
                                 for f in s["faults"]),
          why="rcx=0 -> [rcx+4] mode read faults at VA 4"),
        C(name="w-rand-intmin", entry=W_ENTRY, vec=PAYLOAD, rand=[0x80000000],
          target=TPATH,
          check=lambda s, w: (len(fin_bytes(s)) > 12
                              and struct.unpack("<I", fin_bytes(s)[8:12])[0] == 0
                              and s["g_n"] == 0),
          why="rand()=INT_MIN: abs(INT_MIN)=INT_MIN (still negative) -> signed "
              "%32 fixup -> 0, exactly the contract pass-1 claim, executed"),
        C(name="w-rand-neg3", entry=W_ENTRY, vec=PAYLOAD, rand=[0xFFFFFFFD],
          target=TPATH,
          check=lambda s, w: (struct.unpack("<I", fin_bytes(s)[8:12])[0] == 3
                              and s["g_n"] == 3),
          why="rand()=-3 -> branchless abs -> n=3"),
        C(name="w-n31", entry=W_ENTRY, vec=PAYLOAD, rand=[31], target=TPATH,
          check=lambda s, w: (struct.unpack("<I", fin_bytes(s)[8:12])[0] == 31
                              and s["g_n"] == 31),
          why="n=31: rotation leaves 1 char then NUL - maximum in-range amount"),
        C(name="w-existing-target", entry=W_ENTRY, vec=PAYLOAD, rand=[7],
          target=TPATH, files={TPATH: bytearray(b"OLDSAVE" + b"\0" * 5)},
          check=lambda s, w: (fin_bytes(s) == ref
                              and sum(1 for t in s["trace"] if t[0] == "CopyFileW") == 1),
          why="pre-existing target with backup flag CLEAR: the verify-open finds "
              "it but 02B40E04==0 skips the sav_org backup - a single "
              "tmp->target CopyFileW overwrites it"),
        C(name="w-backup-flag", entry=W_ENTRY, vec=PAYLOAD, rand=[7],
          target=TPATH, files={TPATH: bytearray(b"OLDSAVE" + b"\0" * 5)},
          g_d4=1,
          check=lambda s, w: (fin_bytes(s) == ref
                              and [t[1] + "->" + t[2] for t in s["trace"]
                                   if t[0] == "CopyFileW"]
                                  == ["slot01.sav->C:\\TMP\\sav_org",
                                      "C:\\TMP\\sav_tmp->slot01.sav"]),
          why="backup flag 02B40E04 set + existing target: CopyFileW first backs "
              "the target up to sav_org, then commits tmp->target"),
        C(name="w-cipher-not-plain", entry=W_ENTRY, vec=PAYLOAD, rand=[7],
          target=TPATH,
          check=lambda s, w: (fin_bytes(s)[12:] != zlib.compress(PAYLOAD, 9)[:len(fin_bytes(s)) - 12]
                              and len(fin_bytes(s)) > 12),
          why="control: ciphertext on disk is NOT the raw zlib stream - the RC4 "
              "layer is actually applied (guards against a no-op-encrypt false pass)"),
    ]
    # ---------- unit encrypt (rcx=dst, rdx=&cap->len, r8=src, r9d=len) -------
    out += [
        enc_case("enc-basic", 7, SRC,
          check=lambda s, w: (s["rets"][0] == "0x1"
                              and w.gm.r(ENC_DST, len(SRC)) == rc4(
                                  hashlib.md5(rotb(title, 7)).digest(), SRC)
                              and struct.unpack("<I", w.gm.r(ENC_LEN, 4))[0] == len(SRC)
                              and [t[2] for t in s["trace"] if t[0] == "CryptHashData"][0] == "len=31"),
          why="encrypt unit: out = RC4(MD5(rotl(title,7)[:31]),src); hashdata len=31"),
        enc_case("enc-chunk-2000", 7, patterned(2000),
          check=lambda s, w: ([t[2] for t in s["trace"] if t[0] == "CryptEncrypt"]
                              == ["final=0", "final=0"]),
          why="len 2000 = 2x1000: BOTH chunks Final=0 - the loop only sets Final "
              "for a chunk <1000, so a multiple-of-1000 length never sets it"),
        enc_case("enc-chunk-1500", 7, patterned(1500),
          check=lambda s, w: ([t[2] for t in s["trace"] if t[0] == "CryptEncrypt"]
                              == ["final=0", "final=1"]),
          why="1500 -> chunks 1000(f=0) + 500(f=1)"),
        enc_case("enc-chunk-999", 7, patterned(999),
          check=lambda s, w: ([t[2] for t in s["trace"] if t[0] == "CryptEncrypt"]
                              == ["final=1"]),
          why="999 -> single partial chunk, Final=1"),
        enc_case("enc-len0", 7, b"",
          check=lambda s, w: (s["rets"][0] == "0x1"
                              and not any(t[0] == "CryptEncrypt" for t in s["trace"])
                              and struct.unpack("<I", w.gm.r(ENC_LEN, 4))[0] == 0),
          why="len 0: zero CryptEncrypt calls, success, out len 0"),
        enc_case("enc-acquire-retry", 7, SRC, ctl={"fail_acquire": 1},
          check=lambda s, w: (s["rets"][0] == "0x1"
                              and [t[-1] for t in s["trace"]
                                   if t[0] == "CryptAcquireContextW"]
                                  == [0, "flags=0x8"]),
          why="first CryptAcquireContextW(flags=0) fails -> retried with "
              "flags=8 (CRYPT_NEWKEYSET) then succeeds"),
        enc_case("enc-acquire-fail2", 7, SRC, ctl={"fail_acquire": 2},
          check=lambda s, w: (s["rets"][0] == "0x0"
                              and len([t for t in s["trace"] if t[0] == "CryptAcquireContextW"]) == 2
                              and not any(t[0] == "CryptCreateHash" for t in s["trace"])),
          why="both acquires fail -> return 0 before hashing"),
        enc_case("enc-hashdata-fail", 7, SRC, ctl={"fail_hashdata": 1},
          check=lambda s, w: (s["rets"][0] == "0x0"
                              and not any(t[0] == "CryptDeriveKey" for t in s["trace"])
                              and any(t[0] == "CryptDestroyHash" for t in s["trace"])),
          why="CryptHashData fails -> 0, hash still destroyed"),
        enc_case("enc-derive-fail", 7, SRC, ctl={"fail_derive": 1},
          check=lambda s, w: (s["rets"][0] == "0x0"
                              and not any(t[0] == "CryptEncrypt" for t in s["trace"])
                              and any(t[0] == "CryptDestroyHash" for t in s["trace"])),
          why="CryptDeriveKey fails -> 0"),
        enc_case("enc-n0", 0, SRC,
          check=lambda s, w: (w.gm.r(ENC_DST, len(SRC)) == rc4(
                                  hashlib.md5(rotb(title, 0)).digest(), SRC)),
          why="n=0: B = title verbatim with B[31]=0 -> strlen 31"),
        enc_case("enc-n31", 31, SRC,
          check=lambda s, w: (w.gm.r(ENC_DST, len(SRC)) == rc4(
                                  hashlib.md5(rotb(title, 31)).digest(), SRC)),
          why="n=31: hash material is title[31]+title[0:30]"),
    ]
    # ---------- unit decrypt --------------------------------------------------
    CT = rc4(hashlib.md5(rotb(title, 7)).digest(), SRC)
    out += [
        dec_case("dec-roundtrip", 7, CT,
          check=lambda s, w: (s["rets"][0] == "0x1"
                              and w.gm.r(ENC_DST, len(SRC)) == SRC),
          why="decrypt(encrypt(x)) == x through the shipped chunk loop"),
        dec_case("dec-chunk-2000", 7, rc4(hashlib.md5(rotb(title, 7)).digest(), patterned(2000)),
          check=lambda s, w: ([t[2] for t in s["trace"] if t[0] == "CryptDecrypt"]
                              == ["final=0", "final=0"]),
          why="decrypt mirrors the 1000-byte chunking with the same Final edge"),
        dec_case("dec-hashdata-fail", 7, CT, ctl={"fail_hashdata": 1},
          check=lambda s, w: s["rets"][0] == "0x0",
          why="decrypt fails the same way when hashing fails"),
    ]
    # ---------- reader gates --------------------------------------------------
    out += [
        C(name="r-valid", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(ref)}, path=TPATH,
          check=lambda s, w: (s["vec"] == PAYLOAD.hex() and s["g_n"] == 7
                              and not s["faults"] and not s["trapped"]),
          why="valid container (python-built): reader fills the global vector "
              "with the payload; n published to 02EB3868"),
        C(name="r-gate-size4", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(b"SAFH")}, path=TPATH,
          check=lambda s, w: s["vec"] == b"SAFH".hex() and s["g_n"] == -1,
          why="size<=4 reject path does NOT just return: it pushes the raw file "
              "bytes into the output vector (a fallback fill the contract does "
              "not describe)"),
        C(name="r-gate-magic", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(b"XAFH" + ref[4:])}, path=TPATH,
          check=lambda s, w: (s["vec"] == (b"XAFH" + ref[4:]).hex()
                              and s["g_n"] == -1),
          why="bad magic -> same raw-fill fallback: the WHOLE file lands in the "
              "vector verbatim"),
        C(name="r-gate-size12", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(b"SAFH" + dw(len(PAYLOAD)) + dw(7))}, path=TPATH,
          vec=b"PREEXISTING",
          check=lambda s, w: (s["vec"] == "" and s["g_n"] == -1),
          why="size<=12 after magic: vector TRUNCATED to empty (end=begin) - a "
              "different failure shape than the raw-fill gates"),
        C(name="r-gate-n32", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(ref[:8] + dw(0x20) + ref[12:])}, path=TPATH,
          vec=b"PREEXISTING",
          check=lambda s, w: (s["vec_len"] == 0 and s["g_n"] == -1),
          why="n>31 unsigned reject happens BEFORE [02EB3868] is stored - global "
              "keeps its sentinel - but the vector IS truncated to empty"),
        C(name="r-gate-decl-over", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(ref[:4] + dw(0x100001) + ref[8:])}, path=TPATH,
          check=lambda s, w: (s["vec_len"] == 0 and s["g_n"] == 7),
          why="declared>1MiB rejected AFTER the n store - [02EB3868]=7 even "
              "though the file was refused (ordering detail)"),
        C(name="r-gate-decl0", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(ref[:4] + dw(0) + ref[8:])}, path=TPATH,
          check=lambda s, w: s["vec_len"] == 0 and s["g_n"] == 7,
          why="declared=0 reaches decrypt+inflate then the positive check jle "
              "rejects - vector reserved but empty"),
        C(name="r-gate-mismatch", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(ref[:4] + dw(len(PAYLOAD) + 1) + ref[8:])}, path=TPATH,
          check=lambda s, w: s["vec_len"] == 0 and s["g_n"] == 7,
          why="declared != actual decompressed -> exact-length jne rejects after "
              "a fully successful decrypt+inflate"),
        C(name="r-gate-trunc", entry=R_ENTRY, rcx=PATHW, rdx=1,
          files={TPATH: bytearray(ref[:-17])}, path=TPATH,
          check=lambda s, w: s["vec_len"] == 0 and s["g_n"] == 7,
          why="truncated ciphertext -> shipped zlib inflate != Z_OK -> reject"),
        C(name="r-mode0-nofile", entry=R_ENTRY, rcx=PATHW, rdx=0, files={},
          path=TPATH,
          check=lambda s, w: (s["rets"][0] != "0x0" and s["out"] is not None
                              and s["out"][1] == 0 and s["vec_len"] == 0),
          why="mode 0 + open fail: returns the 0x210 result object {0,mode,path} "
              "rather than 0 - 'no file' is distinguishable from 'reject'"),
        C(name="r-mode1-nofile", entry=R_ENTRY, rcx=PATHW, rdx=1, files={},
          path=TPATH,
          check=lambda s, w: s["rets"][0] == "0x0" and s["vec_len"] == 0,
          why="mode 1 + open fail: returns 0 immediately, no result object"),
    ]
    # ---------- mutants -------------------------------------------------------
    M = []
    def mut(nm, patch, base, check, why):
        d = dict(base); d["name"] = nm; d["patch"] = patch
        d["check"] = check; d["why"] = why
        M.append(d)
    base_w = dict(entry=W_ENTRY, vec=PAYLOAD, rand=[7], target=TPATH)
    base_r = dict(entry=R_ENTRY, rcx=PATHW, rdx=1,
                  files={TPATH: bytearray(ref)}, path=TPATH)
    mut("m-magic0", [(0x8667C4, b"\x54")], base_r,
        lambda s, w: s["vec"] != PAYLOAD.hex(),
        "cmp byte[rsi],0x53 -> 0x54 at 008667C2+6: the valid file is rejected")
    mut("m-nbound", [(0x866807, b"\x3f")], dict(base_r,
        files={TPATH: bytearray(ref[:8] + dw(0x20) + ref[12:])}),
        lambda s, w: (s["g_n"] == 0x20
                      and any(t[0] == "CryptDecrypt" for t in s["trace"])),
        "cmp eax,0x1F -> 0x3F at 00866805: n=0x20 now passes the gate - n IS "
        "stored to 02EB3868 and decryption runs (fails downstream: wrong key)")
    mut("m-declbound", [(0x866819, b"\x10\x00\x00\x00")], base_r,
        lambda s, w: s["vec_len"] == 0,
        "cmp edx,0x100000 -> 0x10 at 00866817: declared 0x400 now rejected")
    mut("m-exact", [(0x86686D, b"\x90\x90")], dict(base_r,
        files={TPATH: bytearray(ref[:4] + dw(len(PAYLOAD) + 1) + ref[8:])}),
        lambda s, w: s["vec_len"] == len(PAYLOAD) + 1,
        "nop the exact-length jne at 0086686D: declared=actual+1 now accepted - "
        "the vector is filled to the DECLARED size (1025) not the inflated size")
    mut("m-positive", [(0x866871, b"\xeb")], base_r,
        lambda s, w: s["vec_len"] == 0,
        "jle -> jmp at 00866871: EVERY file now fails the positive check")
    mut("m-chunk", [(0x865C67, b"\xe7\x03")], dict(entry=ENC, n=7,
        fill=[(ENC_SRC, patterned(2000)), (ENC_LEN, dw(4096))],
        phases=[{"entry": ENC, "rcx": ENC_DST, "rdx": ENC_LEN,
                 "r8": ENC_SRC, "r9": 2000}]),
        lambda s, w: [t[2] for t in s["trace"] if t[0] == "CryptEncrypt"] == ["final=1"],
        "mov ecx,0x3E8 -> 0x3E7 at 00865C66: chunk bound becomes 999 but the "
        "Final test still compares against literal 0x3E8 at 00865CA0 - so the "
        "first 999-byte chunk is already 'final' and the loop drops the tail")
    mut("m-strlen-null", [(0x865C04, b"\x01")], dict(entry=ENC, n=7,
        fill=[(ENC_SRC, SRC), (ENC_LEN, dw(0x40))],
        phases=[{"entry": ENC, "rcx": ENC_DST, "rdx": ENC_LEN,
                 "r8": ENC_SRC, "r9": len(SRC)}]),
        lambda s, w: any(t[0] == "CryptHashData" and t[2] != "len=31"
                         for t in s["trace"]),
        "mov byte[rbp-0x12],0 -> 1 at 00865C08: B[31] not NUL'd -> strlen(B) "
        "runs past 31 -> hashdata length changes")
    mut("m-abs", [(0x8663D1, b"\x1f\x00\x00\x00")], dict(base_w, rand=[0xFFFFFFDD]),
        lambda s, w: (len(fin_bytes(s)) >= 12
                      and struct.unpack("<I", fin_bytes(s)[8:12])[0] == 3),
        "and eax,0x8000001F -> and eax,0x0000001F at 008663D1: rand=-35: signed "
        "%32 gives -3 in the original; without the sign bit the mutant emits "
        "35&0x1F=3")
    mut("m-acq-retry", [(0x865B57, b"\x74")], dict(entry=ENC, n=7,
        fill=[(ENC_SRC, SRC), (ENC_LEN, dw(0x40))],
        phases=[{"entry": ENC, "rcx": ENC_DST, "rdx": ENC_LEN,
                 "r8": ENC_SRC, "r9": len(SRC)}]),
        lambda s, w: ("flags=0x8" in [t[3] for t in s["trace"]
                                      if t[0] == "CryptAcquireContextW" and len(t) > 3]),
        "jne -> je at 00865B57: a successful first acquire is treated as failure "
        "-> the NEWKEYSET retry always runs")
    out += M
    return out
def main():
    raw, secs, iat_names = load_image()
    title = img_read(raw, secs, TITLE_VA, 32)
    print("title:", title)
    results = {}
    npass = nfail = 0
    only = sys.argv[1:] or None
    for case in cases(title):
        if only and case["name"] not in only:
            continue
        snap, w = run_case(case, raw, secs, iat_names)
        ok = bool(case["check"](snap, w)) and not snap["trapped"]
        results[case["name"]] = snap
        print(("PASS " if ok else "FAIL ") + case["name"])
        if not ok:
            nfail += 1
            print("   why:", case["why"])
            print("   faults:", snap["faults"][:4], "trapped:", snap["trapped"][:4])
            print("   trace:", snap["trace"][-8:])
        else:
            npass += 1
    print(f"{npass}/{npass + nfail} pass")
    with open(os.path.join(os.path.dirname(__file__), "result.json"), "w") as f:
        json.dump(results, f, indent=1)

if __name__ == "__main__":
    main()
