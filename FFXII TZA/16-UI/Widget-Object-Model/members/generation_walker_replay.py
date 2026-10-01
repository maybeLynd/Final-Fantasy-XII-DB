# generation_walker_replay.py - bounded ORIGINAL-CODE REPLAY of the widget generation walker 00248030.
#
# What it does: maps the shipping image at its virtual addresses, plants a synthetic widget tree in
# heap memory, points every node's obj+0 handler at an OBSERVATION STUB (a lone `ret` whose entry is
# hooked to record rcx, rdx and the 24-byte message record), stubs the release call 002482E0 the same
# way (records the node, does NOT unlink it), and executes the UNMODIFIED bytes of 00248030 together
# with its one callee 001EDDA0 (executed for real, reading the image's own 01DFE0C0 / 01F82E38).
#
# Controls: every case asserts its expected outcome; two byte-mutants of the walker must FAIL those
# assertions, which shows the observations are sensitive to the two disputed claims:
#   jb_to_jae  - 002480E5 `jb` -> `jae`  (bit-18 polarity)
#   no_reload  - 002480FB `mov edx,[0208ED5C]` -> nops (the parity reload after the callback)
#
# NOT claimed: this is not a live session, the tree is synthetic, the handler is an observer (not a
# real widget procedure such as 002284F0), and the release stub does not reproduce 002482E0's effects.
#
# Usage: python generation_walker_replay.py [--exe PATH] [--out JSON]
# Exit status 0 only when the original passes every case and each mutant is detected.
import sys, struct, json, hashlib, argparse, pathlib
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RIP

HERE = pathlib.Path(__file__).resolve()
DEFAULT_EXE = HERE.parents[4] / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
BASE = 0x120000
WALK, WALK_SIZE = 0x248030, 0x153
HALFRATE, HALFRATE_SIZE = 0x1EDDA0, 0x1B
RELEASE = 0x2482E0
PARITY = 0x208ED5C
MSG2 = 0x915108
STUB, SENTINEL = 0x7F000000, 0x7F000100
HEAP, STACK = 0x60000000, 0x70000000
B17, B18, B10 = 1 << 17, 1 << 18, 1 << 10


class Image:
    def __init__(self, path):
        self.d = open(path, "rb").read()
        d = self.d
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        nsec = struct.unpack_from("<H", d, pe + 6)[0]
        opt = struct.unpack_from("<H", d, pe + 20)[0]
        self.secs = []
        for i in range(nsec):
            vs, va, rs, ro = struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
            self.secs.append((va, vs, rs, ro))
        self.end = max(va + vs for va, vs, rs, ro in self.secs)

    def read(self, addr, n):
        r = addr - BASE
        for va, vs, rs, ro in self.secs:
            if va <= r < va + min(vs, rs):
                return self.d[ro + r - va: ro + r - va + n]
        raise ValueError(hex(addr))


def emulator(img, mutant):
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(BASE, (img.end + 0xFFFF) & ~0xFFFF)          # virtual tail stays zero
    for va, vs, rs, ro in img.secs:
        mu.mem_write(BASE + va, img.d[ro: ro + min(vs, rs)])
    mu.mem_map(HEAP, 0x100000)
    mu.mem_map(STACK - 0x100000, 0x100000)
    mu.mem_map(STUB, 0x1000)
    mu.mem_write(STUB, b"\xC3")
    mu.mem_write(SENTINEL, b"\xF4")
    if mutant == "jb_to_jae":
        assert bytes(mu.mem_read(0x2480E5, 1)) == b"\x72"
        mu.mem_write(0x2480E5, b"\x73")
    elif mutant == "no_reload":
        assert bytes(mu.mem_read(0x2480FB, 2)) == b"\x8B\x15"
        mu.mem_write(0x2480FB, b"\x90" * 6)
    return mu


def run(img, tree, parity, mutant=None, flip_in=None):
    mu = emulator(img, mutant)
    names = list(tree)
    addr = {n: HEAP + 0x1000 + i * 0x200 for i, n in enumerate(names)}
    rev = {v: k for k, v in addr.items()}
    for n, t in tree.items():
        a = addr[n]
        mu.mem_write(a, struct.pack("<Q", STUB))
        for off, key in ((0x10, "parent"), (0x18, "child"), (0x20, "sibling")):
            mu.mem_write(a + off, struct.pack("<Q", addr[t[key]] if t.get(key) else 0))
        mu.mem_write(a + 0x40, struct.pack("<I", t["flags"]))
        mu.mem_write(a + 0xB4, struct.pack("<I", 7))       # sentinel: untouched nodes keep 7
    mu.mem_write(PARITY, struct.pack("<I", parity))
    log = []

    def hook(uc, address, size, user):
        rcx = uc.reg_read(UC_X86_REG_RCX)
        if address == STUB:
            rdx = uc.reg_read(UC_X86_REG_RDX)
            rec = struct.unpack("<3Q", bytes(uc.mem_read(rdx, 24)))
            log.append(["msg", rev.get(rcx, hex(rcx)), f"{rdx:08X}", list(rec)])
            if rev.get(rcx) == flip_in:
                p = struct.unpack("<I", bytes(uc.mem_read(PARITY, 4)))[0]
                uc.mem_write(PARITY, struct.pack("<I", p ^ 1))
        else:
            log.append(["release", rev.get(rcx, hex(rcx))])
            rsp = uc.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", bytes(uc.mem_read(rsp, 8)))[0]
            uc.reg_write(UC_X86_REG_RSP, rsp + 8)
            uc.reg_write(UC_X86_REG_RIP, ret)
    mu.hook_add(UC_HOOK_CODE, hook, begin=STUB, end=STUB)
    mu.hook_add(UC_HOOK_CODE, hook, begin=RELEASE, end=RELEASE)
    rsp = STACK - 0x1000
    mu.mem_write(rsp, struct.pack("<Q", SENTINEL))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RCX, addr[names[0]])
    mu.emu_start(WALK, SENTINEL, count=100000)
    final = {}
    for n in names:
        fl = struct.unpack("<I", bytes(mu.mem_read(addr[n] + 0x40, 4)))[0]
        final[n] = {"bit2": fl >> 2 & 1, "bit10": fl >> 10 & 1, "bit17": fl >> 17 & 1,
                    "bit18": fl >> 18 & 1,
                    "visited": struct.unpack("<I", bytes(mu.mem_read(addr[n] + 0xB4, 4)))[0] != 7}
    return log, final


def messaged(log):
    return [e[1] for e in log if e[0] == "msg"]


def released(log):
    return [e[1] for e in log if e[0] == "release"]


# Trees. Parity global = 1 and bit 17 = 0 everywhere, so every node starts STALE.
STALE = {"R": dict(child="A", flags=0),
         "A": dict(parent="R", sibling="B", flags=B18),
         "B": dict(parent="R", sibling="C", flags=0),
         "C": dict(parent="R", flags=B10)}
CURRENT = {k: dict(v, flags=v["flags"] | B17) for k, v in STALE.items()}
SUBTREES = {"R": dict(child="A", flags=0),
            "A": dict(parent="R", child="A1", sibling="C", flags=B18),
            "A1": dict(parent="A", flags=0),
            "C": dict(parent="R", child="C1", flags=B10),
            "C1": dict(parent="C", flags=0)}


def case_checks(img, mutant):
    """Return {case: (passed, detail)} for one build (original or a mutant)."""
    out = {}
    log, fin = run(img, STALE, 1, mutant)
    ok = (messaged(log) == ["R", "B"] and released(log) == ["C"]
          and all(e[2] == f"{MSG2:08X}" and e[3] == [2, 0, 0] for e in log if e[0] == "msg")
          and fin["A"]["bit17"] == 1 and fin["A"]["bit2"] == 1 and fin["A"]["bit18"] == 1
          and fin["C"]["bit17"] == 0 and fin["C"]["bit2"] == 0)
    out["bit18_suppresses_own_message"] = (ok, {"log": log, "final": fin})
    log, fin = run(img, CURRENT, 1, mutant)
    ok = log == [] and not fin["A"]["visited"] and not fin["B"]["visited"]
    out["current_nodes_get_nothing"] = (ok, {"log": log, "final": fin})
    log, fin = run(img, SUBTREES, 1, mutant)
    ok = messaged(log) == ["R", "A1"] and released(log) == ["C"] and not fin["C1"]["visited"]
    out["bit18_does_not_prune_subtree"] = (ok, {"log": log, "final": fin})
    log, fin = run(img, STALE, 1, mutant, flip_in="B")
    ok = (messaged(log) == ["R", "B"] and fin["R"]["bit17"] == 1 and fin["A"]["bit17"] == 1
          and fin["B"]["bit17"] == 0 and released(log) == [])
    out["stamp_uses_parity_after_callback"] = (ok, {"log": log, "final": fin})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=str(DEFAULT_EXE))
    ap.add_argument("--out", default=str(HERE.with_suffix(".json")))
    a = ap.parse_args()
    img = Image(a.exe)
    result = {
        "scope": "original-code replay of 00248030 (+ callee 001EDDA0) over planted trees; "
                 "observation-stub handler; release stub records only. Not live, not a real widget tree.",
        "body_sha256": {"00248030": hashlib.sha256(img.read(WALK, WALK_SIZE)).hexdigest(),
                        "001EDDA0": hashlib.sha256(img.read(HALFRATE, HALFRATE_SIZE)).hexdigest()},
        "message_record_00915108": list(struct.unpack("<3Q", img.read(MSG2, 24))),
        "builds": {},
    }
    status = 0
    for build in (None, "jb_to_jae", "no_reload"):
        checks = case_checks(img, build)
        name = build or "original"
        result["builds"][name] = {k: {"passed": v[0], **v[1]} for k, v in checks.items()}
        failed = [k for k, v in checks.items() if not v[0]]
        if build is None:
            verdict = "PASS" if not failed else "FAIL " + ",".join(failed)
            status |= bool(failed)
        else:
            verdict = ("DETECTED by " + ",".join(failed)) if failed else "NOT DETECTED"
            status |= not failed
        result["builds"][name]["verdict"] = verdict
        print(f"{name:10s} {verdict}")
    json.dump(result, open(a.out, "w"), indent=1, sort_keys=True)
    print("00248030 sha256", result["body_sha256"]["00248030"])
    sys.exit(status)


if __name__ == "__main__":
    main()
