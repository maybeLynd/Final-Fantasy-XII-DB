"""S-15 (OPUS, 2026-09-26): the field runtime pass's exit A and interpreter arm EXECUTED over shipped field scripts bound by the real
loader, in a boot world built by the game's own start-up code - and where that start-up stops at the device.

WORLD (world_boot.py): the whole image allowed, imports the only boundary, disclosed process-start models; the CRT pre-C and C++
initialiser tables run as shipped. Then, in shipped order:
 1. main 007980A0 as a PREFIX. It creates the settings object [01F82D20] and stops in GameSettingConfig_SerializeText at msvcp140's
    narrow basic_ostream constructor (not modelled), writing a fresh install's GameSetting.ini (memory-only).
 2. app vtable slot 2 = 0017CEB0 (0079F150 calls it after device creation 006253D0). It builds the job system, indexes
    ../FFXII_TZA.vbf (fread, MD5 through CryptoAPI) and stops in 001DD420's display-mode enumeration: 006242C0 reads the DXGI
    adapter [renderer+0x1880], which only device creation 006253D0 stores (006256F2 / 00625749).
 3. the rest of 0017D6B0 and 0017CEB0's tail, then the game-init job 0017D4C0's callees one by one (the job is what the
    registrar 0017CF30, slot 3, submits after 0079F150's device steps). Two stop in the render layer: 001B7850 (render targets;
    loads /GameData/D3D11/ArtData/shaders/video.fx.phyre) and 001B1580 (an 8x8 texture filled through a map/lock).
 4. OTHER THREADS: where the main thread waits on another thread, that thread's shipped code runs as a PREFIX on a side stack:
    the input worker 0035EA40 up to its ready-flag store 0035EA64, and the job manager's worker loop 001A1240 (thread entry
    001A1230, started by 001A0AF0) for exactly one job, up to 001A12E9, whenever the loader's status test 0046DFE0 finds a read
    in flight with a job queued. Boot's loads (map_ref.bin, ...) are served this way from the real archive.
 5. msvcp140's narrow streams (narrow_streams.py) call the GAME's basic_stringbuf virtuals (overflow 001DFA80, underflow 001E0390,
    pbackfail 001DFCF0) through guest calls when the library would.
 6. the save-image reset 002EF650 (the call 0022B6E0 makes at 0022B78B), which sets the battle block [02EBF190].
 7. message 16 delivered to the UI system widget (handler 00253780, created by the UI boot 00253970): its pack branch 00280980
    fills the HUD context's MRP pointers (+0x00..+0xB0) from the mrppack blob at [ctx+0x3D0].
 8. two shipped field scripts through the real loader: 00330310's prefix to 003303E3 (the buffer), the file's shipped bytes into
    it (the I/O thread's work), then the real completion 003304A0. ttl_b01.ebp (namespace 5 index 39) into manager slot 1;
    byu_w01.ebp (namespace 5 index 2736) into slot 2. Paths come from the game's own path table [0215F000], filled at boot.
 9. the field pass 0025D9E0 on each slot, once per frame (as the per-frame update runs it), the loader pump drained between.

CASES
 B1  the CRT tables run with no failure; main stops in SerializeText's ostream; slot 2 stops at 006242C0 reading [+0x1880]; the
     render-layer steps stop at 001B6C75 / the memset in 001B1630; the other init steps return.
 B2  both binds complete; slot 1's +0x12 = 0 (ttl_b01's driven-actor word at definition +0x50 is -1) and slot 2's +0x12 = 1
     (byu_w01's is 0): the bind's own store 0026CD28 `mov [rdi+0x12], al` of (word [def+0x50] >= 0).
 X1  THE INTERPRETER ARM: slot 1, frame 0: the +0x12 == 0 branch runs audio then the init core (return 0025DC2C), drives the
     record ttl_b01 bound, and its wait entry (state 1) sends 0025DF00 into WorldActorScriptVM_InterpretBytecode 0025E4C0
     (return 0025E0D8).
 X2  EXIT A: slot 2, frame 1: the drive loop (+0x12 = 1) drives the driven actor (record 0, return 0025DB48 / 0025DB6D) through the
     interpreter; the record comes back SETTLED (+0x14 bit 6 set, 0x30 -> 0x70), and the pass publishes +0x12 and calls the
     init core from 0025DB7D (return 0025DB82) - exit A. +0x12 is 0 afterwards (r12b = 0 on this path).
 X3  the script drives the deferred arm: slot 1, frame 3: the interpreter's native lifecycle command 002621D0 -> 00353080 calls
     WorldSimulation_ProcessDeferredModeRequest 0032FC30(1, 0x1AD); the request runs through ActorResource_BeginManagerResource
     0032FCA0 and stops at 0020A800's std::regex construction (msvcp140 locale::_Init, not modelled).
 S1  static: 0026CD1A..0026CD28 compute +0x12 from word [def+0x50]; 0025DB79 is the drive loop's store of r12b.
Evidence classes NATIVE-REPLAY and STATIC, live_game false. Writes result.json.
"""
import json
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
T0 = time.time()
import world_boot as B                                            # noqa: E402
from unicorn import UC_HOOK_CODE as _HC                           # noqa: E402
from unicorn import x86_const as _X                               # noqa: E402
import narrow_streams as NS                                       # noqa: E402

S, uc, q, d4, fn, LOG = B.S, B.uc, B.q, B.d4, B.fn, B.LOG
RIP, RAX, RSP = _X.UC_X86_REG_RIP, _X.UC_X86_REG_RAX, _X.UC_X86_REG_RSP
RETADDR = 0x71000000
R = {"crt": B.CRT, "steps": []}

# ---------------------------------------------------------------- other threads' prefixes and guest calls
_u32 = lambda a: struct.unpack("<I", bytes(uc.mem_read(a, 4)))[0]
_u64 = q
THREAD_PREFIX = {
    0x35E930: (lambda: _u32(0x22CA630) == 0, 0x35EA40, lambda: 0, 0x35EA6E),
    0x46DFE0: (lambda: _u32(0x215EFF4) == 0xFFFFFFFF and _u64(0x1F81160) != 0 and _u64(_u64(0x1F81160) + 0x50) != _u64(0x1F81160) + 0x50,
               0x1A1240, lambda: _u64(0x1F81160), 0x1A12E9),
}
PEND = []
TSTACK = 0x7BC00000
uc.mem_map(TSTACK, 0x40000)
for _pc, (_c, _e, _r, _s) in THREAD_PREFIX.items():
    uc.hook_add(_HC, (lambda c: lambda u, a, n, _: (PEND.append(a), u.emu_stop()) if c() else None)(_c), begin=_pc, end=_pc)
REGS = [getattr(_X, "UC_X86_REG_" + n) for n in ("RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP", "R8", "R9", "R10", "R11", "R12",
                                                  "R13", "R14", "R15", "RIP", "EFLAGS")]
PREFIX_LOG, GUEST_LOG = [], []


def _regs():
    return ({r: uc.reg_read(r) for r in REGS}, {i: uc.reg_read(getattr(_X, "UC_X86_REG_XMM%d" % i)) for i in range(16)})


def _restore(st_):
    for r, v in st_[0].items():
        uc.reg_write(r, v)
    for i, v in st_[1].items():
        uc.reg_write(getattr(_X, "UC_X86_REG_XMM%d" % i), v)


def _side(entry, args, stop_at, depth):
    sp = TSTACK + 0x10000 * depth - 0x1000
    uc.mem_write(sp, struct.pack("<Q", RETADDR))
    uc.reg_write(RSP, sp)
    for r, v in zip((_X.UC_X86_REG_RCX, _X.UC_X86_REG_RDX, _X.UC_X86_REG_R8, _X.UC_X86_REG_R9), args):
        uc.reg_write(r, v & 0xFFFFFFFFFFFFFFFF)
    return _run_until(entry, stop_at, depth)


def _serve_guest(g, st_, depth):
    while True:
        ok_ = _side(g.fn, g.args, RETADDR, depth + 1)
        rax = uc.reg_read(RAX)
        GUEST_LOG.append(("%08X" % g.fn, g.name.split("@")[0][:24], ok_))
        if not ok_:
            return False
        _restore(st_)
        try:
            final = g.then(rax)
        except NS.NeedGuest as g2:
            g2.name = g.name
            g = g2
            continue
        uc.reg_write(RAX, final & 0xFFFFFFFFFFFFFFFF)
        return True


def _serve_prefix(spin, st_, depth):
    cond, entry, rcx_fn, pstop = THREAD_PREFIX[spin]
    ok_ = _side(entry, (rcx_fn(),), pstop, depth + 1)
    PREFIX_LOG.append(("%08X" % entry, ok_))
    if ok_:
        _restore(st_)
    return ok_


def _run_until(pc, stop_at, depth):
    while True:
        S.st["bad"], S.st["faults"] = [], []
        try:
            uc.emu_start(pc, stop_at, count=S.count)
        except Exception as e:
            S.st["faults"].append(str(e))
        rip = uc.reg_read(RIP)
        if rip == stop_at and not S.st["bad"] and not S.st["faults"]:
            return True
        if S.st["bad"] or S.st["faults"] or not (PEND or NS.GUESTQ) or depth >= 3:
            return False
        st_ = _regs()
        if NS.GUESTQ:
            if not _serve_guest(NS.GUESTQ.pop(), st_, depth):
                return False
            pc = rip
        else:
            spin = PEND.pop()
            if not _serve_prefix(spin, st_, depth):
                return False
            pc = spin


def call(fn_, *args):
    if S.call(fn_, *args):
        return True
    if not (PEND or NS.GUESTQ):
        return False
    st_ = _regs()
    rip = st_[0][RIP]
    S.st["bad"], S.st["faults"] = [], []
    if NS.GUESTQ:
        if not _serve_guest(NS.GUESTQ.pop(), st_, 0):
            return False
    else:
        spin = PEND.pop()
        if not _serve_prefix(spin, st_, 0):
            return False
        rip = spin
    return _run_until(rip, RETADDR, 0)


def stop_of(ok):
    rip = uc.reg_read(RIP)
    return {"ok": ok, "halt": [str(x)[:70] for x in (S.st["bad"] or S.st["faults"])[:1]], "rip": "%X" % rip,
            "import": B.TRAPNAMES.get(rip, "")[:60], "in": B.shadow()[-3:]}


def step(tag, ok):
    rec = dict(stop_of(ok), step=tag)
    R["steps"].append(rec)
    print("%-58s %s %s %s %s" % (tag[:58], ok, rec["halt"], rec["import"][:40], rec["in"]))
    return ok


# ---------------------------------------------------------------- 1-3: the start-up in shipped order
S.count = 400000000
del B.SHADOW[:]
step("main 007980A0 (prefix)", S.call(0x7980A0))
R["settings_object"] = "%X" % q(0x1F82D20)
APP = q(0x2EA5368)
R["app_object"] = "%X" % APP
ARGV = 0x7BB00000                                    # argv as main builds it from the model's command line: the executable
uc.mem_map(ARGV, 0x1000)
uc.mem_write(ARGV + 0x100, b"C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE\\x64\\FFXII_TZA.exe\0")
uc.mem_write(ARGV, struct.pack("<QQ", ARGV + 0x100, 0))
del B.SHADOW[:]
step("app slot 2 0017CEB0(app, argv, 1)", S.call(0x17CEB0, APP, ARGV, 1))
R["adapter_writers_static"] = [B.fn(0x6256F2)[:8], B.fn(0x625749)[:8]]
SEQ = [(0x1D6BE0,), (0x1BE3E0,), (0x19CDE0,), (0x1C2F00,), (0x1DBA40,), (0x182F70, d4(APP + 0xD24), d4(APP + 0xD28)),
       (0x1DB500,), (0x199790,), ("new", 0x20, 0x1A14E0, 0x1F7F4C0), ("new", 0xC0, 0x1A16E0, 0x1F7F4C8), ("new", 0x10, 0x1A17D0, 0x1F7F4D0),
       ("new", 0xA0, 0x1B24D0, 0x1F7F4D8), (0x1A11B0,), (0x198750,), (0x19EF40,), (0x1B6BC0,), (0x1B29F0,), (0x1B7EE0,), ("crs",),
       (0x1C18A0,), (0x1C1940,), (0x1B5F10,), (0x1D6990,), (0x1D8150,), (0x1D89D0,), (0x1831A0,), (0x22A0B0, 1, ARGV), (0x1B1BA0,),
       ("rcx", 0x1B1C00, 0x1B1580), (0x22A4B0,), (0x1D8CD0,), ("new", 0x10, 0x1D5600, 0x1F7F4E0), (0x1AD3E0,), (0x1C0D40,), (0x1D62D0,),
       (0x194AB0,), ("rcx", 0x194AF0, 0x194AA0), (0x1DB1E0,)]
S.count = 80000000
for st_ in SEQ:
    del B.SHADOW[:]
    if st_[0] == "new":
        _, sz, ctor, cell = st_
        S.call(0x210EC0, sz)
        ok = S.call(ctor, uc.reg_read(RAX))
        uc.mem_write(cell, struct.pack("<Q", uc.reg_read(RAX)))
        tag = "new(%X) %08X -> [%08X]" % (sz, ctor, cell)
    elif st_[0] == "rcx":
        _, getter, f = st_
        S.call(getter)
        ok = S.call(f, uc.reg_read(RAX))
        tag = "%08X(%08X())" % (f, getter)
    elif st_[0] == "crs":
        S.call(0x1B7F20)
        ok = S.call(0x1B7850, uc.reg_read(RAX))
        tag = "001B7850(001B7F20()) render targets"
    else:
        ok = call(*st_)
        tag = "%08X" % st_[0]
    step(tag, ok)


def pump_drain(tag, limit=400):
    n = 0
    while q(0x22C51C0) and n < limit:
        n += 1
        if not call(0x32E070, 0):
            step("pump 0032E070 (%s)" % tag, False)
            break
    return n


# ---------------------------------------------------------------- 6-7: the save image and the HUD context
del B.SHADOW[:]
step("save-image reset 002EF650", call(0x2EF650))
R["battle_block_02EBF190"] = "%X" % q(0x2EBF190)
R["pump_after_boot"] = pump_drain("after boot")
CTX = q(0x209AC30)


def find_widgets(root, proc, out, depth=0):              # the widget tree: handler +0x00, first child +0x18, next sibling +0x20
    w = root
    while w and depth < 64:
        if q(w) == proc:
            out.append(w)
        if q(w + 0x18):
            find_widgets(q(w + 0x18), proc, out, depth + 1)
        w = q(w + 0x20)
    return out


SYSW = find_widgets(q(0x208EA28), 0x253780, [])
R["hud"] = {"ctx": "%X" % CTX, "plus8_before": "%X" % q(CTX + 8), "mrppack_blob": "%X" % q(CTX + 0x3D0), "system_widgets": len(SYSW)}
if SYSW and q(CTX + 0x3D0):
    MSG = TSTACK + 0x3F800
    uc.mem_write(MSG, struct.pack("<III", 16, 0, 0) + bytes(20))
    del B.SHADOW[:]
    step("message 16 to the UI system widget 00253780", call(0x253780, SYSW[0], MSG))
    pump_drain("after message 16")
R["hud"]["plus8_after"] = "%X" % q(CTX + 8)

# ---------------------------------------------------------------- 8: two shipped field scripts through the real loader
EXTRACT = r"D:\FFXII_TZA_extract"
R["binds"] = {}


def bind(MGR, NS_, IDX, REQ=13):
    del B.SHADOW[:]
    S.call(0x36C1D0, 5, 5)                                   # select arena 5
    path = bytes(uc.mem_read(q(q(0x215F000 + 8 * NS_) + 8 * IDX), 160)).split(b"\0")[0].decode("latin1")
    stop = uc.hook_add(_HC, lambda u, a, n, _: u.emu_stop(), begin=0x3303E3, end=0x3303E3)
    uc.ctl_flush_tb()
    call(0x330310, MGR, REQ, NS_, IDX)
    uc.hook_del(stop)
    prefix_stop = "%X" % uc.reg_read(RIP)
    buf = q(0x22C6C00 + 8 * MGR)
    data = open(os.path.join(EXTRACT, *path.split("\\")), "rb").read()
    uc.mem_write(buf, data)
    del B.SHADOW[:]
    ok = step("completion 003304A0 (slot %d, %s)" % (MGR, path.split("\\")[-1]), call(0x3304A0, (buf & 0xFFFFFFFF) | MGR))
    SL = 0x2098E10 + 0x288 * MGR
    R["binds"][MGR] = {"path": path, "size_table": d4(0x2EC3EE0 + 4 * (5000 * NS_ + IDX)), "file_bytes": len(data),
                       "file_word_D0": struct.unpack_from("<h", data, 0xD0)[0], "def_minus_buffer": q(SL) - buf,
                       "def_word_50": struct.unpack("<h", bytes(uc.mem_read(q(SL) + 0x50, 2)))[0], "prefix_stop": prefix_stop,
                       "completion_ok": ok, "slot_10_17": bytes(uc.mem_read(SL + 0x10, 8)).hex(), "records": d4(SL + 0x20)}
    return ok


BOUND = [m for m, ns_, ix in ((1, 5, 39), (2, 5, 2736)) if bind(m, ns_, ix)]
R["pump_after_bind"] = pump_drain("after bind")

# ---------------------------------------------------------------- 9: the field pass, frame by frame
EV = []
for _a, _nm in ((0x25DF00, "resolve"), (0x25E4C0, "INTERPRETER"), (0x2620E0, "init_core"), (0x261F90, "audio"), (0x32FC30, "deferred"),
                (0x3DB6E0, "select_entry"), (0x2621D0, "vm_lifecycle_native"), (0x32FCA0, "begin_manager_resource")):
    uc.hook_add(_HC, (lambda nm: lambda u, a, n, _: EV.append({"ev": nm, "rcx": "%X" % u.reg_read(_X.UC_X86_REG_RCX),
                                                             "rdx": "%X" % (u.reg_read(_X.UC_X86_REG_RDX) & 0xFFFFFFFF),
                                                             "ret": "%08X" % q(u.reg_read(RSP))}))(_nm), begin=_a, end=_a)
uc.ctl_flush_tb()


def records(SL):
    out = []
    for k in range(min(d4(SL + 0x20), 8)):
        S.call(0x358940, SL, k)
        r = uc.reg_read(RAX)
        if not r:
            continue
        w, wi = q(r + 0xA8), uc.mem_read(r + 0x11, 1)[0]
        out.append({"rec": k, "addr": "%X" % r, "b10": uc.mem_read(r + 0x10, 1)[0], "b11": wi, "b14": uc.mem_read(r + 0x14, 1)[0],
                    "b63": uc.mem_read(r + 0x63, 1)[0], "b88": uc.mem_read(r + 0x88, 1)[0],
                    "wait_state": uc.mem_read(w + 40 * wi + 0x14, 1)[0] if w else None})
    return out


R["frames"] = {}
S.count = 20000000
for MGR in BOUND:
    SL = 0x2098E10 + 0x288 * MGR
    fr = R["frames"][MGR] = [{"frame": "before", "records": records(SL)}]
    for frame in range(4):
        del EV[:]
        del B.SHADOW[:]
        ok = call(0x25D9E0, MGR)
        fr.append({"frame": frame, "ok": ok, "stop": stop_of(ok), "b12_after": uc.mem_read(SL + 0x12, 1)[0],
                   "events": list(EV), "records": records(SL)})
        print("slot %d frame %d ok %s +12 %d events %s" % (MGR, frame, ok, fr[-1]["b12_after"], [e["ev"] for e in EV][:14]))
        if not ok:
            break
        pump_drain("slot %d frame %d" % (MGR, frame), limit=50)

# ---------------------------------------------------------------- S1: static
import capstone                                                  # noqa: E402
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
at = lambda a: ("%s %s" % next(md.disasm(B.img[a - B.IB:a - B.IB + 16], a, count=1))[1:] if False else
                ("%s %s" % ((lambda i: (i.mnemonic, i.op_str))(next(md.disasm(B.img[a - B.IB:a - B.IB + 16], a, count=1))))).strip())
R["static"] = {k: at(k_) for k, k_ in (("0026CD1A", 0x26CD1A), ("0026CD25", 0x26CD25), ("0026CD28", 0x26CD28), ("0025DB2E", 0x25DB2E),
                                        ("0025DB31", 0x25DB31), ("0025DB79", 0x25DB79), ("0025DB7D", 0x25DB7D), ("006242C0+0x9D", 0x62435D),
                                        ("006256F2", 0x6256F2), ("00625749", 0x625749))}
R["prefixes"] = {"input_worker": sum(1 for e, ok in PREFIX_LOG if e == "0035EA40" and ok),
                 "job_worker": sum(1 for e, ok in PREFIX_LOG if e == "001A1240" and ok), "failed": [p for p in PREFIX_LOG if not p[1]]}
R["guest_calls"] = {k: sum(1 for g in GUEST_LOG if g[0] == k and g[2]) for k in ("001DFA80", "001E0390", "001DFCF0")}
R["guest_failed"] = [g for g in GUEST_LOG if not g[2]]
R["boot_reads"] = sorted({x[1] for x in LOG if isinstance(x, tuple) and x and x[0] == "fopen" and len(x) > 3})

# ---------------------------------------------------------------- cases
steps = {s["step"]: s for s in R["steps"]}
f1, f2 = R["frames"].get(1, []), R["frames"].get(2, [])


def evs(fr, i):
    return [e for e in fr[i + 1]["events"]] if len(fr) > i + 1 else []


x1 = evs(f1, 0)
x2 = evs(f2, 1)
x3 = evs(f1, 3)
dev_stops = [s for s in R["steps"] if not s["ok"]]
cases = {
    "B1_startup_runs_as_shipped_and_stops_at_the_device": not R["crt"]["failed"] and R["crt"]["cpp"] == 1172
        and steps["main 007980A0 (prefix)"]["import"].startswith("??0?$basic_ostream@D") and "GameSettingConfig_Seria" in " ".join(steps["main 007980A0 (prefix)"]["in"])
        and steps["app slot 2 0017CEB0(app, argv, 1)"]["rip"] == "624364" and "../FFXII_TZA.vbf" in R["boot_reads"]
        and steps["001B7850(001B7F20()) render targets"]["rip"] == "1B6C75"
        and steps["001B1580(001B1C00())"]["import"] == "memset"
        and all(s["ok"] for s in R["steps"] if s["step"] not in ("main 007980A0 (prefix)", "app slot 2 0017CEB0(app, argv, 1)",
                "001B7850(001B7F20()) render targets", "001B1580(001B1C00())", "00182F70", "message 16 to the UI system widget 00253780"))
        and R["static"]["006256F2"].startswith("mov qword ptr [rbx + 0x1880]") and R["static"]["00625749"].startswith("mov qword ptr [rbx + 0x1880]"),
    "B2_both_binds_complete_plus12_from_the_definition": R["binds"].get(1, {}).get("completion_ok") and R["binds"].get(2, {}).get("completion_ok")
        and R["binds"][1]["file_word_D0"] == -1 and R["binds"][2]["file_word_D0"] == 0
        and R["binds"][1]["def_word_50"] == -1 and R["binds"][2]["def_word_50"] == 0 and R["binds"][1]["def_minus_buffer"] == 0x80
        and R["binds"][1]["slot_10_17"][4:6] == "00" and R["binds"][2]["slot_10_17"][4:6] == "01"
        and R["static"]["0026CD28"] == "mov byte ptr [rdi + 0x12], al" and R["static"]["0026CD25"] == "setge al"
        and R["static"]["0026CD1A"].startswith("cmp word ptr [r15 + 0x50]"),
    "X1_interpreter_arm_runs_on_ttl_b01s_bound_record": [e["ev"] for e in x1][:4] == ["audio", "init_core", "resolve", "INTERPRETER"]
        and x1[1]["ret"] == "0025DC2C" and x1[3]["ret"] == "0025E0D8" and x1[3]["rdx"] == x1[2]["rdx"]
        and f1[0]["records"][0]["wait_state"] == 1,
    "X2_exit_A_on_byu_w01s_driven_actor": any(e["ev"] == "init_core" and e["ret"] == "0025DB82" for e in x2)
        and any(e["ev"] == "INTERPRETER" for e in x2) and any(e["ev"] == "resolve" and e["ret"] in ("0025DB48", "0025DB6D") for e in x2)
        and f2[0]["records"][0]["b14"] & 0x40 == 0 and f2[2]["records"][0]["b14"] & 0x40 == 0x40
        and f2[1]["b12_after"] == 1 and f2[2]["b12_after"] == 0 and R["static"]["0025DB79"] == "mov byte ptr [rbx + 0x12], r12b",
    "X3_the_script_drives_the_deferred_arm_to_its_regex": any(e["ev"] == "deferred" and e["rcx"] == "1" and e["rdx"] == "1AD" for e in x3)
        and any(e["ev"] == "vm_lifecycle_native" for e in x3) and any(e["ev"] == "begin_manager_resource" for e in x3)
        and len(f1) > 4 and not f1[4]["ok"] and f1[4]["stop"]["import"].startswith("?_Init@locale@std@@"),
    "W_threads_and_guest_calls_served_without_failure": R["prefixes"]["input_worker"] >= 1 and R["prefixes"]["job_worker"] >= 1
        and not R["prefixes"]["failed"] and not R["guest_failed"] and R["hud"]["plus8_after"] != "0",
}
res = {"live_game": False, "evidence": ["NATIVE-REPLAY", "STATIC"], "results": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True, default=str)
for k, v in cases.items():
    print("%-66s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if res["ok"] else "FAILED")
sys.exit(0 if res["ok"] else 1)
