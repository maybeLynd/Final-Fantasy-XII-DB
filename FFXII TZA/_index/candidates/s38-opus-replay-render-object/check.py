"""S-38: execute the character render object's constructor 001F4DA0, transform publish 001FB120 and teardown 001F51E0
(CONTRACT-character-render-object.md R-1..R-3, R-5..R-7) as shipped code (OPUS, 2026-09-25, block 353).

Evidence class: NATIVE-REPLAY (unicorn), live_game false. world.py (block 318/319's builder, Session; UCRT rand bridge from block
332) supplies the image, the IAT traps and the named bridges. No application stub and no stop boundary.
Fixtures: six idle objects at 0x76300000 plus the frame singleton [01F7F598] (a zeroed block whose +0x1C byte selects the bank),
a 0x668-byte object buffer filled 0xCC before construction, a record-array element vector (+0x58) of one 0x318-byte element whose
first qword points at a zeroed object, three 64-byte source matrices; the ready latch +0x4B4 is set to 1 by fixture for the
publish cases (the setter, the 2,328-byte finish-setup method 001F6E70, is not executed).
Writes result.json next to this file.
"""
import json
import os
import struct

import pefile
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RIP
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

import world as W
import shipped_pack as SP

HERE = os.path.dirname(os.path.abspath(__file__))
FX = json.load(open(os.path.join(HERE, "world.json")))
CTOR, PUBLISH, DTOR, VTABLE = 0x1F4DA0, 0x1FB120, 0x1F51E0, 0x903B68
W.ALLOWED |= ({0x16D6A0} | SP.allowed(W) | set().union(*(W.closure(f) for f in (CTOR, PUBLISH, DTOR))))
S = W.Session(FX["fixes"], FX["inits"])
uc = S.uc
made, skipped = SP.bind(W, S)
IDLE = 0x76300000
for i, cell in enumerate((0x209BE80, 0x1F7FFE0, 0x215E6E0, 0x209CC40, 0x2092758, 0x20927C0, 0x1F7F598)):
    uc.mem_write(IDLE + i * 0x20000, bytes(0x20000))
    uc.mem_write(cell, struct.pack("<Q", IDLE + i * 0x20000))
FRAME = IDLE + 6 * 0x20000
OBJ, ELEMS, ELEMOBJ, MATS = 0x76280000, 0x76290000, 0x762A0000, 0x762B0000
pe = pefile.PE(W.EXE, fast_load=True)


def w(a, fmt, *v):
    uc.mem_write(a, struct.pack(fmt, *v))


def r(a, n):
    return bytes(uc.mem_read(a, n))


writes = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: writes.append((a - OBJ, n, "%08X" % u.reg_read(UC_X86_REG_RIP))),
            begin=OBJ, end=OBJ + 0x667)
elem_writes = []
uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: elem_writes.append((a - ELEMS, n)), begin=ELEMS, end=ELEMS + 0x317)

results, allok = {}, True


def record(name, ok, **kw):
    global allok
    allok &= bool(ok)
    results[name] = dict(pass_=bool(ok), **kw)
    print("%-34s %s  %s" % (name, "PASS" if ok else "FAIL", kw.get("note", "")))


# ---- R-2 / R-3: construction ----
uc.mem_write(OBJ, b"\xCC" * 0x668)
del writes[:]
ok = S.call(CTOR, OBJ)
vt = struct.unpack("<Q", r(OBJ, 8))[0]
latch = r(OBJ + 0x4B4, 1)[0]
latch_writes = [x for x in writes if x[0] <= 0x4B4 < x[0] + x[1]]
record("R2_R3_construct", ok and vt == VTABLE and latch == 0 and [x[2] for x in latch_writes] == ["001F4EC9"],
       vtable="%X" % vt, latch=latch, latch_writers=latch_writes,
       note="001F4DA0 over a 0xCC-filled 0x668 buffer installs vtable 00903B68 and clears the ready latch +0x4B4 with one byte store "
            "at 001F4EC9")


# ---- R-7 / R-5: the publish ----
def setup_publish(latch_value, selector):
    uc.mem_write(OBJ + 0x4C4, b"\x11" * 0x180)              # both banks hold a recognisable previous content
    w(OBJ + 0x4B4, "<B", latch_value)
    w(OBJ + 0x58, "<QQQ", ELEMS, ELEMS + 0x318, ELEMS + 0x318)
    uc.mem_write(ELEMS, bytes(0x318))
    uc.mem_write(ELEMOBJ, bytes(0x100))
    w(ELEMS, "<Q", ELEMOBJ)
    for k in range(3):
        uc.mem_write(MATS + 0x40 * k, bytes(range(0x40 * k, 0x40 * k + 0x40)))
    w(FRAME + 0x1C, "<B", selector)


def publish():
    del writes[:], elem_writes[:]
    return S.call(PUBLISH, OBJ, 0, 0, 0, stack=(0, MATS, MATS + 0x40, MATS + 0x80))


setup_publish(0, 0)
ok = publish()
record("R7_clear_latch_publishes_nothing", ok and writes == [] and elem_writes == [] and r(OBJ + 0x4C4, 0x180) == b"\x11" * 0x180,
       note="latch 0: 001FB120 returns at 001FB13A with no store to the object or the element - both banks keep their previous bytes")

banks = {}
for sel in (0, 1):
    setup_publish(1, sel)
    ok = publish()
    a, b = r(OBJ + 0x4C4, 0xC0), r(OBJ + 0x584, 0xC0)
    src = r(MATS, 0xC0)
    banks[sel] = {"ok": ok, "bank_A_is_source": a == src, "bank_B_is_source": b == src,
                  "bank_A_untouched": a == b"\x11" * 0xC0, "bank_B_untouched": b == b"\x11" * 0xC0,
                  "object_write_span": ["+%X" % min(x[0] for x in writes), "+%X" % max(x[0] + x[1] for x in writes)] if writes else None,
                  "element_writes": sorted({"+%X" % x[0] for x in elem_writes})}
record("R5_selector_picks_one_bank", banks[0]["ok"] and banks[0]["bank_A_is_source"] and banks[0]["bank_B_untouched"]
       and banks[1]["ok"] and banks[1]["bank_B_is_source"] and banks[1]["bank_A_untouched"], banks=banks,
       note="latch 1: with [01F7F598]+0x1C = 0 the three source matrices land in bank A (+0x4C4) and bank B is untouched; with 1 they "
            "land in bank B (+0x584) and bank A is untouched - the bank is chosen outside the object")

# ---- R-6: no loops in the publish (static, from the instructions) ----
code = pe.get_data(PUBLISH - 0x120000, 496)
ins = list(Cs(CS_ARCH_X86, CS_MODE_64).disasm(code, PUBLISH))
back = [i for i in ins if i.mnemonic.startswith("j") and i.op_str.startswith("0x") and int(i.op_str, 16) < i.address]
record("R6_publish_has_no_loops", len(ins) == 105 and sum(1 for i in ins if i.mnemonic == "movups") == 48 and back == [],
       instructions=len(ins), movups=sum(1 for i in ins if i.mnemonic == "movups"), backward_jumps=len(back),
       note="001FB120: 105 instructions, 48 movups, no backward jump (static)")

# ---- R-1: allocation and sized delete agree ----
imm = {a: pe.get_data(a - 0x120000, 5) for a in (0x1BD527, 0x1F5309)}
record("R1_one_size_both_ends", all(v[:1] in (b"\xB9", b"\xBA") and struct.unpack("<I", v[1:5])[0] == 0x668 for v in imm.values()),
       sites={"%08X" % a: v.hex() for a, v in imm.items()},
       note="the allocation at 001BD527 and the sized delete at 001F5309 both load 0x668 (static)")

# ---- teardown ----
setup_publish(1, 0)
vt_stores = []
hv = uc.hook_add(UC_HOOK_MEM_WRITE, lambda u, acc, a, n, v, _: vt_stores.append(["%08X" % u.reg_read(UC_X86_REG_RIP), "%X" % v]),
                 begin=OBJ, end=OBJ + 7)
ok = S.call(DTOR, OBJ)
uc.hook_del(hv)
record("R2_teardown_vtable_chain", ok and vt_stores and vt_stores[0] == ["001F51F9", "%X" % VTABLE] and len(vt_stores) >= 2
       and vt_stores[-1][1] != "%X" % VTABLE, vtable_stores=vt_stores, latch_after=r(OBJ + 0x4B4, 1)[0],
       note="001F51E0 first stores the class vtable 00903B68 (001F51F9 - the class's second and last reference), runs its member "
            "teardown, and the base destructor then installs the base vtable; the latch is not cleared by it")

json.dump({"ok": allok, "bound": made, "allowed_functions": len(W.ALLOWED), "results": results},
          open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
print("ok" if allok else "NOT ok")


# EXIT STATUS FOLLOWS THE RECORDED VERDICT (OPUS, 2026-10-03, the user's root-cause directive item 4): this package
# recorded "ok" in result.json but always exited 0, so no automated re-run could see it fail.
import json as _ej, os as _eo, sys as _es
_es.exit(0 if _ej.load(open(_eo.path.join(_eo.path.dirname(_eo.path.abspath(__file__)), "result.json"),
                            encoding="utf-8")).get("ok") is True else 1)
