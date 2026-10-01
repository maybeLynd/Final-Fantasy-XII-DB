# EXP-128 body spans: sha256 over shipped bytes for each real body.
# Real bodies executed: the queue/task poll pump (E070 0032E070, six-arm
# jump-table state machine via JTAB 0032E2D0), the tick pacer (EB70
# 0035EB70) + its EA30 thunk, the retire twins (E330/E370), the progress
# wrapper (E3B0), the active->idle list splice (EC40), the tick getter
# (E810), three leaves (G8C70/GE0E0/G6A0), the yield tail (G20C0 ->
# 16D6A0) and the PREL thunk (G97F0 -> EXP-126's 00369860, whose free
# path executes for real inside the pump's retire arms).
# Re-executed from EXP-126: PREL 00369860, FLAG 0046DFE0 (the pump's S3/S4
# poll gate calls it directly; residual rdx/r8 visible at entry).
# Scripted boundaries (entry-intercepted, NOT executed):
#   XADD0 003EADD0 init gate         X46E0 0046E030 submit-A shim
#   X2DF6 002DF6C0 submit-B          XDD50 0046DD50 teardown pump
#   X9780 003E9780 teardown pump     XFD50 0036FD50 teardown gate
#   XBB79 003BB790 cond. tail        X2090 00862090 tick source
#   X17D3 0017D3E0 resync gate       X91B0 003691B0 resync helper
#   X9190 00369190 resync helper     X5E7A 0035E7A0 resync value
#   CB40/CB48/CB50 0x6301/2/30000 planted ret-stub task callbacks
import hashlib, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import check

# (name, va, disasm-window hi). Trailing int3/nop padding is trimmed.
BODIES = [
    ("e070", check.E070, 0x32E2D0),
    ("ea30", check.EA30, 0x35EA37),
    ("eb70", check.EB70, 0x35EC80),
    ("e330", check.E330, 0x32E370),
    ("e370", check.E370, 0x32E3B0),
    ("e3b0", check.E3B0, 0x32E3F0),
    ("ec40", check.EC40, 0x32ECE0),
    ("e810", check.E810, 0x35E818),
    ("g8c70", check.G8C70, 0x368C77),
    ("ge0e0", check.GE0E0, 0x46E0E7),
    ("g6a0", check.G6A0, 0x16D6A3),
    ("g20c0", check.G20C0, 0x8620CE),
    ("g97f0", check.G97F0, 0x3697FD),
    ("prel", check.PREL, 0x369C60),
    ("flag", check.FLAG, 0x46DFF2),
]
SCRIPTED = [check.XADD0, check.X46E0, check.X2DF6, check.XDD50,
            check.X9780, check.XFD50, check.XBB79, check.X2090,
            check.X17D3, check.X91B0, check.X9190, check.X5E7A,
            check.CB40, check.CB48, check.CB50]
INDIRECT = {
    "e070": [{"site": "0x32e0bb",
              "form": "jmp rcx (six-arm JTAB dispatch)",
              "src": "d[rdi+rax*4+0x20e2d0] offsets BD/49/63/63/AB/AB "
                     "+image base",
              "planted": "shipped table (rdata-in-text, verified)"},
             {"site": "0x32e189",
              "form": "call rax",
              "src": "task S4 progress callback q[+0x48]",
              "planted": "0x63020000 fixture trampoline"}],
    "e330": [{"site": "0x32e34f",
              "form": "call rax",
              "src": "task retire callback q[+0x40]",
              "planted": "0x63010000 fixture trampoline"}],
    "e370": [{"site": "0x32e392",
              "form": "call rax",
              "src": "task retire callback q[+0x40] (d28==-1 gated)",
              "planted": "0x63010000 fixture trampoline"}],
    "e3b0": [{"site": "0x32e3c2",
              "form": "call rax",
              "src": "task progress callback q[+0x50]",
              "planted": "0x63030000 fixture trampoline"}],
    "ec40": [{"site": "0x32ecce",
              "form": "jmp 0x16d6a0",
              "src": "direct tail into the ret-0 leaf",
              "planted": "shipped target"}],
    "g20c0": [{"site": "0x8620c9",
               "form": "jmp 0x16d6a0",
               "src": "yield tail (rdx=0x1ccf998 residual)",
               "planted": "shipped target"}],
    "g97f0": [{"site": "0x3697f7",
               "form": "jmp 0x369860",
               "src": "free-if-nonnull tail into PREL",
               "planted": "shipped target"}],
    "prel": [{"site": "0x369a79",
              "form": "call qword [rip+disp]",
              "src": "q[0x8c2d80] (ships rdata ptr 0x1ccf02c)",
              "planted": "0x46dfe0"},
             {"site": "0x369ab7",
              "form": "call qword [rip+disp]",
              "src": "q[0x8c2d80] (ships rdata ptr 0x1ccf02c)",
              "planted": "0x46dfe0"}],
}


def body(raw, secs, va, hi):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = list(md.disasm(check.img_rd(raw, secs, va, hi - va), va))
    end = len(insns)
    while end > 0 and insns[end - 1].mnemonic in ("int3", "nop"):
        end -= 1
    insns = insns[:end]
    hi2 = insns[-1].address + insns[-1].size
    blob = check.img_rd(raw, secs, va, hi2 - va)
    return {"va": "0x%x" % va, "lo": "0x%x" % va, "hi": "0x%x" % hi2,
            "span": hi2 - va, "insns": len(insns), "cov": 1.0,
            "sha256": hashlib.sha256(blob).hexdigest(), "indirect": []}


def main():
    raw, secs = check.load_image()
    real = []
    for name, va, hi in BODIES:
        b = body(raw, secs, va, hi)
        b["name"] = name
        if name in INDIRECT:
            b["indirect"] = INDIRECT[name]
        print("%s 0x%x span=%d insns=%d" % (name, va, b["span"], b["insns"]))
        real.append(b)
    json.dump({"real": real,
               "scripted": ["0x%x" % v for v in SCRIPTED]},
              open("bodies.json", "w"), indent=1)
    print("scripted:", ["0x%x" % v for v in SCRIPTED])


if __name__ == "__main__":
    main()
