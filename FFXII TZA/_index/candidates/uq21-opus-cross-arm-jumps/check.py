"""UQ-21 (OPUS, 2026-09-26): are the console's cross-arm jumps shared tails by design, or the compiler folding identical
code? STATIC over the shipped image: the dispatcher 001D1660, whose table 001D4C1C holds 282 dword RVAs, ids 12-293.
  X1 the population reproduces: 21 unconditional jumps from 14 arms into another arm's interior. A jump to an arm's
     START is a normal exit and is not counted.
  X2 every target is an instruction boundary of its host arm.
  X3 every jump lands at the MAXIMAL common suffix. The instruction before the jmp differs from the instruction before
     the target, so the shared code begins exactly where the two instruction streams become identical. rip-relative
     operands are compared by their resolved addresses. That is the placement cross-jumping (tail merging) produces.
     Control: the same comparison run on an arm against itself counts every instruction as agreeing.
  X4 8 of the 21 enter in the middle of an expression, where no source-level label can sit:
       6 carry a call argument across the jump: the jumping arm sets xmm0, or edx / r8d, and the host's next call
         reads it;
       2 (ids 276 and 280) carry the CPU flags: the host's first instruction is `setne`, reading flags the jumping
         arm computed.
     The other 13 enter at statement boundaries, and the maximal-suffix placement of X3 holds for them too.
Exit 1 on any FAIL; writes result.json."""
import struct, re, collections, json, sys
from pathlib import Path
import pefile, capstone
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[4]
pe = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"), fast_load=True); img = pe.get_memory_mapped_image(); IB = 0x120000
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64); md.detail = True
TABLE, BODY_HI, NOP = 0x1D4C1C, 0x1D4C19, 0x1D4BFA
ids = {12 + i: IB + struct.unpack_from("<I", img, TABLE - IB + 4 * i)[0] for i in range(282)}
starts = sorted(set(ids.values()))
end_of = {t: (starts[n + 1] if n + 1 < len(starts) else BODY_HI) for n, t in enumerate(starts)}
owner = collections.defaultdict(list)
for c, t in ids.items(): owner[t].append(c)
def dec(t, hi=None): return list(md.disasm(img[t - IB:(hi or end_of[t]) - IB], t))
def arm_of(a): return next((t for t in starts if t <= a < end_of[t]), None)
def norm(i):
    s = i.op_str; m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", s)
    if m: s = s.replace(m.group(0), "[%#x]" % (i.address + i.size + int(m.group(1), 16)))
    return i.mnemonic + " " + s
def agree(xs, a, ys, b):
    n = 0
    while a >= 0 and b >= 0 and norm(xs[a]) == norm(ys[b]): n += 1; a -= 1; b -= 1
    return n
BASE = {"ecx": "rcx", "cl": "rcx", "edx": "rdx", "dl": "rdx", "r8d": "r8", "r8b": "r8", "r9d": "r9", "r9b": "r9"}
ARGS = {"rcx", "rdx", "r8", "r9", "xmm0", "xmm1", "xmm2", "xmm3"}
FLAGREAD = re.compile(r"^(set|j(?!mp)|cmov|adc|sbb)")
rows = []; ctrl_ok = True
for t in starts:
    if t == NOP: continue
    ins = dec(t)
    for k, x in enumerate(ins):
        if not (x.mnemonic == "jmp" and x.op_str.startswith("0x")): continue
        tgt = int(x.op_str, 16)
        if t <= tgt < end_of[t]: continue
        h = arm_of(tgt)
        if h is None or h == t or tgt in starts: continue
        hins = dec(h); idx = next((j for j, y in enumerate(hins) if y.address == tgt), None)
        ag = agree(ins, k - 1, hins, idx - 1) if idx is not None else None
        ctrl_ok &= agree(ins, k - 1, ins, k - 1) == k
        suf = dec(tgt, end_of[h])
        written = set()
        for y in suf:
            if y.mnemonic == "call": break
            written |= {BASE.get(y.reg_name(r), y.reg_name(r)) for r in y.regs_access()[1]}
        set_before = set()
        for y in ins[max(0, k - 4):k]: set_before |= {BASE.get(y.reg_name(r), y.reg_name(r)) for r in y.regs_access()[1]}
        flags = bool(suf) and bool(FLAGREAD.match(suf[0].mnemonic))
        cross = sorted((set_before & ARGS) - written)
        has_call = any(y.mnemonic == "call" for y in suf)
        kind = "flags-live" if flags else ("argument-live" if cross and has_call else "statement-boundary")
        rows.append({"arm": "%08X" % t, "ids": owner[t], "site": "%08X" % x.address, "target": "%08X" % tgt, "host": "%08X" % h,
                     "host_ids": owner[h], "boundary": idx is not None, "agree_before": ag,
                     "jump_prev": norm(ins[k - 1]), "host_prev": norm(hins[idx - 1]) if idx else None, "kind": kind, "crossing": cross,
                     "host_suffix": [norm(y) for y in suf[:6]]})
kinds = collections.Counter(r["kind"] for r in rows)
cases = {
    "X1_21_jumps_from_14_arms_into_another_arms_interior": len(rows) == 21 and len({r["arm"] for r in rows}) == 14,
    "X2_every_target_is_an_instruction_boundary_of_its_host": all(r["boundary"] for r in rows),
    "X3_every_jump_lands_at_the_maximal_common_suffix": all(r["agree_before"] == 0 for r in rows) and ctrl_ok,
    "X4_8_enter_mid_expression_6_argument_2_flags": kinds == {"statement-boundary": 13, "argument-live": 6, "flags-live": 2},
}
out = {"evidence": ["STATIC"], "live_game": False, "kinds": dict(kinds), "jumps": rows, "cases": cases, "ok": all(cases.values())}
json.dump(out, open(HERE / "result.json", "w"), indent=1, sort_keys=True)
for r in rows:
    print("%s ids %-6s -> %s (host ids %s) %-18s jmp-side: %-34s host-side: %-34s %s" % (r["site"], r["ids"], r["target"], r["host_ids"][:3],
          r["kind"], r["jump_prev"][:34], (r["host_prev"] or "")[:34], r["crossing"]))
print(dict(kinds))
for k, v in cases.items(): print("%-64s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
sys.exit(0 if out["ok"] else 1)
