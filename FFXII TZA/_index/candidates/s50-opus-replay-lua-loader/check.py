"""S-50: execute CONTRACT-lua-chunk-loader.md's Phyre entry 00683C30, the fork 0081D790 (f_parser) and the header check
0082E490 as shipped code, and test PRE, the argument marshalling, I1 (the fork on the first byte), I2 (mode guards with a NULL
mode) and I3 (the 18-byte header, 17 read) (OPUS, 2026-09-25, block 322).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. No shipped asset carries a chunk and no lua_State constructor has
been located (the Lua pages' DA-1), so this does not load a chunk end to end. Instead each body runs as shipped code up to the
first call into machinery that needs a live lua_State, and that call is a STOP BOUNDARY (the run ends there and its arguments
are recorded; nothing is substituted):
  00812F70 luaL_loadbufferx (from 00683C30), 0082E910 luaU_undump and 0082BE30 luaY_parser (from the fork), 0081BFF0
  luaO_pushfstring (the error message on any refusal: the format and the 'why' string are recorded).
The chunk bytes and the ZIO / SParser / LoadState records are planted fixtures; the ZIO reader is the shipped
`xor eax, eax; ret` at 00122125 (EOF). strchr (the mode guard's import) is bridged by name. world.py (block 318/319's builder, Session)
supplies the image, the IAT traps and the named bridges; its world is built once and not otherwise used.
Writes result.json next to this file.
"""
import json
import os
import struct

from unicorn import UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RSP

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
PHYRE, LOADBUF, FORK, HEADER, UNDUMP, PARSER, PUSHF = 0x683C30, 0x812F70, 0x81D790, 0x82E490, 0x82E910, 0x82BE30, 0x81BFF0
EOF_READER = 0x122125                          # a shipped `xor eax, eax; ret`: the ZIO reader returns NULL (EOF)
STOPS = {LOADBUF: "luaL_loadbufferx", UNDUMP: "luaU_undump", PARSER: "luaY_parser", PUSHF: "luaO_pushfstring"}
W.ALLOWED |= {0x16D6A0, EOF_READER, PHYRE, FORK, HEADER, 0x81C6A0} | W.closure(0x81C6A0) | set(STOPS)   # boundaries are recorded by on_stop, never run
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
BASE = 0x76380000
L, BUF, DATA, ZIO, SP_, LS, STR = BASE, BASE + 0x1000, BASE + 0x2000, BASE + 0x3000, BASE + 0x3100, BASE + 0x3200, BASE + 0x4000
stop = {}


def on_stop(u, a, n, _):
    rsp = u.reg_read(UC_X86_REG_RSP)
    stop["at"] = STOPS[a]
    stop["args"] = [u.reg_read(r) for r in (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9)] + \
        [struct.unpack("<Q", bytes(u.mem_read(rsp + 0x28, 8)))[0]]
    u.emu_stop()


for a in STOPS:
    uc.hook_add(UC_HOOK_CODE, on_stop, begin=a, end=a)


def cstr(a):
    b = bytes(uc.mem_read(a, 128))
    return b[:b.index(b"\x00")].decode("latin-1") if b"\x00" in b else b.decode("latin-1")


def call(fn, *args):
    stop.clear()
    uc.mem_write(BASE, bytes(0x8000))
    return S.call(fn, *args)


def put_str(addr, s):
    uc.mem_write(addr, s + b"\x00")
    return addr


results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= ok
    results[name] = dict(pass_=ok, **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- 00683C30: PRE and the marshalling into luaL_loadbufferx ----
call(PHYRE, L, BUF)                                           # data NULL (the fixture buffer is zero)
null_data = dict(stop)
null_ret = S.st["faults"][:1]
call(PHYRE, L, BUF)
uc.mem_write(BUF + 0x10, struct.pack("<I", 0x80001234))
uc.mem_write(BUF + 0x18, struct.pack("<Q", DATA))
uc.mem_write(BUF + 0x48, struct.pack("<Q", 0x21))
uc.mem_write(DATA, b"return 1")
S.call(PHYRE, L, BUF)
marsh = dict(stop)
S.call(PHYRE, L, 0)
null_rdx_faults = list(S.st["faults"][:1])
pre_ok = (null_data.get("at") is None and marsh.get("at") == "luaL_loadbufferx" and marsh["args"][0] == L
          and marsh["args"][1] == DATA and bool(null_rdx_faults))
record("PRE_and_marshalling_00683C30", pre_ok, data_null_reached=null_data.get("at"),
       loadbufferx_args={"L": hex(marsh["args"][0]), "data": hex(marsh["args"][1]), "len": hex(marsh["args"][2]),
                         "name": hex(marsh["args"][3]), "mode": hex(marsh["args"][4])} if marsh else None,
       null_buffer_pointer=null_rdx_faults,
       note="a NULL data pointer is refused before any load; rdx itself is dereferenced first (a NULL buffer faults); the load "
            "receives L, data, length and name as the recorded values")


# ---- the fork 0081D790: f_parser(L, SParser*) over a pre-filled ZIO ----
def fork(first_bytes, mode=None):
    call(FORK, L, SP_)
    uc.mem_write(DATA, first_bytes)
    uc.mem_write(ZIO, struct.pack("<QQ", len(first_bytes), DATA))          # ZIO { size_t n; const char *p; ... }
    uc.mem_write(SP_, struct.pack("<Q", ZIO))                                # SParser { ZIO *z; Mbuffer; Dyndata; mode; name }
    m = put_str(STR, mode) if mode is not None else 0
    uc.mem_write(SP_ + 0x50, struct.pack("<QQ", m, put_str(STR + 0x100, b"=fixture")))   # SParser.mode / .name (0081D7D9, 0081D7FC)
    S.call(FORK, L, SP_)
    msg = cstr(stop["args"][3]) if stop.get("at") == "luaO_pushfstring" and stop["args"][3] else None
    return {"reached": stop.get("at"), "why": msg}


forks = {"binary_mode_NULL": fork(b"\x1bLuaR\x00"), "text_mode_NULL": fork(b"return 1"),
         "binary_mode_t": fork(b"\x1bLuaR\x00", b"t"), "text_mode_b": fork(b"return 1", b"b"),
         "binary_mode_bt": fork(b"\x1bLuaR\x00", b"bt")}
i1 = forks["binary_mode_NULL"]["reached"] == "luaU_undump" and forks["text_mode_NULL"]["reached"] == "luaY_parser"
i2 = forks["binary_mode_bt"]["reached"] == "luaU_undump" and forks["binary_mode_t"]["reached"] == "luaO_pushfstring" \
    and forks["text_mode_b"]["reached"] == "luaO_pushfstring"
record("I1_I2_fork_and_mode_guards", i1 and i2, cases=forks,
       note="first byte 0x1B -> luaU_undump, anything else -> luaY_parser; with mode NULL no guard fires; a mode that excludes the "
            "chunk's kind is refused (the message is formatted) before either path")


# ---- the header check 0082E490 over a planted LoadState { L, ZIO*, Mbuffer*, name } ----
GOOD = bytes.fromhex("4c75615200010408040400") + bytes.fromhex("19930d0a1a0a")      # the 17 bytes after the 0x1B


def header(rest):
    call(HEADER, LS)
    uc.mem_write(DATA, rest)
    uc.mem_write(ZIO, struct.pack("<QQQQQ", len(rest), DATA, EOF_READER, 0, L))  # ZIO {n, p, reader, data, L}
    uc.mem_write(LS, struct.pack("<QQQQ", L, ZIO, 0, put_str(STR + 0x200, b"=fixture")))
    ok = S.call(HEADER, LS)
    why = cstr(stop["args"][3]) if stop.get("at") == "luaO_pushfstring" and stop["args"][3] else None
    return {"accepted": ok and not stop, "why": why}


good = header(GOOD)
flips = {}
for i in range(17):
    b = bytearray(GOOD)
    b[i] ^= 0x01
    flips[i + 1] = header(bytes(b))
trunc = header(GOOD[:16])
i3 = good["accepted"] and all(not v["accepted"] for v in flips.values()) and trunc["why"] is not None
record("I3_header_18_compared_17_read", i3, shipped_header_accepted=good, per_byte_flip={str(k): v["why"] for k, v in flips.items()},
       truncated_16_bytes=trunc, note="the shipped 5.2 float header passes; a flip at ANY of header bytes 1..17 is refused (with the "
                                      "message recorded); 16 bytes is 'truncated': 17 are read after the dispatcher's 0x1B")
json.dump({"ok": allok, "results": results}, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")
