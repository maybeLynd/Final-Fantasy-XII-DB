"""sd20_voice_callback.py - which class is a CoreSourceVoice's callback object? (OPUS, 2026-09-30; register SD-20)

Re-reads each fact from the certified image through Database/Tools/analysis-kit/gfz-scripts/retool.py (its RTTI
complete-object-locator reader included) and asserts it. Prints PASS/FAIL per fact and `FAILS n` last.
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, c, SZ = T.R, T.scan(), T.sizes()
fails = 0
BASE_CB = 0x01CB5218     # SQEX::Sd::Driver::Core::ICoreSourceVoiceCallback (RTTI)


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def body(f, upto=None):
    return [i for i in R.md.disasm(R.at(f, SZ[f]), f) if upto is None or i.address <= upto]


def fields(f, reg, upto=None):
    s = collections.Counter()
    for i in body(f, upto):
        for m in re.finditer(r"\[%s \+ (0x[0-9a-f]+|\d+)\]" % reg, i.op_str):
            s[int(m.group(1), 0)] += 1
    return set(s)


# F1 - the base interface vtable and the three classes that install it, each at a fixed sub-object offset
check("F1", T.rtti_class(BASE_CB) == "SQEX::Sd::Driver::Core::ICoreSourceVoiceCallback", "01CB5218 is ICoreSourceVoiceCallback")
inst = sorted((f, a) for f, a, k in c["refs"].get(BASE_CB, ()) if k == "lea")
where = {}
for f, a in inst:
    nxt = ins(a + 7) if ins(a).op_str.startswith("rax") else None
    for j in body(f)[[i.address for i in body(f)].index(a):][:4]:
        # capstone prints small displacements in decimal ([rdi + 8]) and larger ones in hex
        m = re.match(r"qword ptr \[(r\w+)(?: \+ (0x[0-9a-f]+|\d+))?\], rax", j.op_str) if j.mnemonic == "mov" else None
        if m:
            where[f] = int(m.group(2), 0) if m.group(2) else 0
            break
check("F2", where == {0x007B8E50: 0x10, 0x007DC730: 8, 0x007EA050: 8, 0x007B8F70: 0} or
      {k: v for k, v in where.items() if k != 0x007B8F70} == {0x007B8E50: 0x10, 0x007DC730: 8, 0x007EA050: 8},
      "installers of the interface vtable and the sub-object offset each writes: %s" % {("%08X" % k): hex(v) for k, v in where.items()})
cls = {0x007B8E50: T.rtti_class(0x01CB5238), 0x007DC730: T.rtti_class(0x01CB7B20), 0x007EA050: T.rtti_class(0x01CB92A8)}
check("F3", cls == {0x007B8E50: "SQEX::Sd::Driver::ExternalSourceVoice", 0x007DC730: "SQEX::Sd::Driver::CRI::HCAMixerVoice",
                    0x007EA050: "SQEX::Sd::Driver::Voice"},
      "the classes those constructors build (primary vtable RTTI): %s" % {("%08X" % k): v for k, v in cls.items()})
# F4 - the voice factory 007AEA20 has three callers; each passes (5th argument, [rsp+0x20]) its object + that offset
cs = sorted(c["calls"].get(0x007AEA20, ()))
arg = {0x007B91E7: ("lea rax, [rbp + 0x10]", 0x007B91B8), 0x007DCF92: ("lea rax, [rdi + 8]", 0x007DCF69)}
ok4 = [a for _, a in cs] == [0x007B91E7, 0x007DCF92, 0x007ED332]
for site, (text, at) in arg.items():
    ok4 = ok4 and ("%s %s" % (ins(at).mnemonic, ins(at).op_str)) == text
ok4 = ok4 and ins(0x007ED2EE).op_str == "rdi, [rbx + 8]" and ins(0x007ED30F).op_str == "rdi, r13" \
    and ins(0x007ED32D).op_str == "qword ptr [rsp + 0x20], rdi" and ins(0x007B91E2).op_str == "qword ptr [rsp + 0x20], rax" \
    and ins(0x007DCF87).op_str == "qword ptr [rsp + 0x20], rax"
check("F4", ok4, "factory callers 007B9050 (passes this+0x10), 007DCE20 (this+8), 007EBAD0 (lea rdi, [rbx + 8] at 007ED2EE; null when rbx is null) as the 5th argument")
# F5 - each caller's object is its class, by layout: the fields it touches before the call are fields the class's
#      constructor sets (a consistency test, not a proof of type)
e = fields(0x007B8E50, "rcx") | fields(0x007B8E50, "rsi")
h, v = fields(0x007DC730, "rbx"), fields(0x007EA050, "rdi")
ue, uh, uv = fields(0x007B9050, "rbp", 0x007B91E7), fields(0x007DCE20, "rdi", 0x007DCF92), fields(0x007EBAD0, "rbx", 0x007ED332)
check("F5", 0x508 in e and 0x500 in ue and uh & h >= {0x38, 0x48, 0x50, 0x90, 0xA4} and {0x448, 0x450, 0x190, 0x1B0} <= (uv & v),
      "shared fields - ExternalSourceVoice/007B9050: +0x500 used, +0x508 constructed; HCAMixerVoice/007DCE20: %s; Voice/007EBAD0: %s"
      % (sorted(hex(x) for x in uh & h), sorted(hex(x) for x in uv & v)[:8]))
print("FAILS %d" % fails)
