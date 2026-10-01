"""test_access_policy_producers.py - the four census producers use the shared access policy, not capstone's raw flags.

FRONTIER-REQ-OPUS-ACCESS-FLAG-PRODUCER-REPAIR (OPUS, 2026-09-27). Three parts, all required:
  STATIC   arg_extent_scan, census_receiver_fixpoint, disp_image_census and singleton_field_scan read no `op.access` /
           CS_AC_* and route memory labels through reg_tracking.op_kind (and register kills, where they track registers,
           through reg_tracking.written)
  POLICY   hand-encoded instructions give the labels the SDM gives them - the cases capstone 5.0.7 gets wrong included:
           store / load / lea / nop / prefetch / lock cmpxchg / test (both forms) / cmp / setcc / plain read-modify-write
  KILLS    a sub-register write kills its parent; cmpxchg writes rax; cdq writes rdx only; test writes no GPR
Run: python test_access_policy_producers.py  (exit 0 on success)
"""
import os, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reg_tracking as RT

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

PRODUCERS = {"arg_extent_scan.py": True, "census_receiver_fixpoint.py": True, "disp_image_census.py": False,
             "singleton_field_scan.py": True}
for f, tracks in PRODUCERS.items():
    s = open(os.path.join(HERE, f), encoding="utf-8").read()
    raw = re.findall(r"\bop\.access\b|CS_AC_(?:READ|WRITE)", s)
    check("STATIC %s: no raw flags; op_kind%s" % (f, " and written" if tracks else ""),
          not raw and "RT.op_kind(" in s and (not tracks or "RT.written(" in s), str(raw[:3]))

md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def one(hexbytes):
    return next(md.disasm(bytes.fromhex(hexbytes), 0x1000))
def mem_kind(hexbytes):
    x = one(hexbytes)
    for oi, op in enumerate(x.operands):
        if op.type == X86_OP_MEM:
            return RT.op_kind(x, op, oi), x
CASES = [("0f114310", "w", "movups [rbx+0x10], xmm0 (store; capstone says read)"),
         ("0f104310", "r", "movups xmm0, [rbx+0x10] (load)"),
         ("894308", "w", "mov [rbx+8], eax"),
         ("8b4308", "r", "mov eax, [rbx+8]"),
         ("488d4308", "addr", "lea rax, [rbx+8] (address, not an access)"),
         ("0f1f00", "addr", "nop dword ptr [rax] (padding; capstone says read)"),
         ("0f181b", "addr", "prefetcht2 [rbx] (capstone says read)"),
         ("f00fb10b", "rw", "lock cmpxchg [rbx], ecx (capstone says read only)"),
         ("854304", "r", "test [rbx+4], eax (capstone gives no flag)"),
         ("f60301", "r", "test byte ptr [rbx], 1"),
         ("833b00", "r", "cmp dword ptr [rbx], 0 (memory first, still a read)"),
         ("0f9303", "w", "setae byte ptr [rbx] (capstone says read)"),
         ("830301", "rw", "add dword ptr [rbx], 1")]
for hx, want, why in CASES:
    k, x = mem_kind(hx)
    check("POLICY %-38s -> %s" % (x.mnemonic + " " + x.op_str, want), k == want, "%s; got %s" % (why, k))
KILLS = [("b901000000", {"rcx"}, set(), "mov ecx, 1 kills rcx"),
         ("f00fb10b", {"rax"}, set(), "lock cmpxchg writes rax on failure"),
         ("99", {"rdx"}, {"rax"}, "cdq writes rdx only"),
         ("a901000000", set(), {"rax"}, "test eax, 1 writes flags only")]
for hx, must, mustnot, why in KILLS:
    w = RT.written(one(hx))
    check("KILLS %s" % why, must <= w and not (mustnot & w), str(sorted(r for r in w if r.startswith("r"))))
# EMIT (OPUS, 2026-09-28): census_receiver_fixpoint's EMIT_JSON per-site [read, write] flags come from the same op_kind
# label. From 6b6a423db the label and the per-site key shared one name, so every flag was [0, 0] while the printed
# totals were right. RampChannelRecord (cell 02B40528, extent 0xE0) has a known load and a known store at +0x08.
import json, subprocess, tempfile
_tmp = os.path.join(tempfile.mkdtemp(), "emit.json")
subprocess.run([sys.executable, os.path.join(HERE, "census_receiver_fixpoint.py"), "02B40528", "0", "0xE0"],
               env=dict(os.environ, SEED="cell", EMIT_JSON=_tmp), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
_s = json.load(open(_tmp, encoding="utf-8"))["sites"] if os.path.exists(_tmp) else {}
_f = _s.get("8:4", {})
check("EMIT census_receiver_fixpoint per-site flags", _f.get("003B64D7") == [1, 0] and _f.get("003B573D") == [0, 1],
      "mulss xmm0,[rbx+8] -> %s (want [1, 0]); mov dword [rbx+8], imm -> %s (want [0, 1])"
      % (_f.get("003B64D7"), _f.get("003B573D")))
print("FAILS", fails)
sys.exit(1 if fails else 0)
