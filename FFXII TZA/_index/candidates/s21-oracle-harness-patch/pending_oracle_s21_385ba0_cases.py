"""PENDING PATCH FOR ORACLE (prepared by OPUS 2026-09-25, block 264) - applied and run by OPUS on a scratch COPY only (block 288: 39/39 x3, all three predictions held); ORACLE's file untouched.

Target: _experiments/evidence/apply-result-whole-exec/check.py (EXP-149's harness).
Purpose: test the S-21 I8 divergence named in candidates/s21-runtime-per-invariant-exposure.md. The metadata step
00385BA0 (scripted in EXP-149, executed by no record) clears spawn+0x14 bit i whenever record byte +0x32+i is
non-zero; the applier's own btr (0031146C) additionally needs the steal id != 0xFFFF.

Changes, each with an exact preimage anchor (refuses if an anchor is missing or the patch is already present):
  1. on_code: a per-case `realbodies` escape checked BEFORE the SCR stub table, so 00385BA0 runs as shipped bytes.
     Its callees: 0031B860 (the harness's b860_map, the same owner resolution the applier uses) and 00469EC0
     (only when record +0x1C == 1; the new cases keep +0x1C = 0).
  2. plant_record: when a case sets rec['meta_real'], plant +0x138 = +0x13C = 0xFFFFFFFF, so 00385BA0 skips its
     battle-state writes (q[02EBF190]+0x5B0E / +0x5B00), which in this fixture would land outside the 0x40
     flag-object allocation. Existing cases are unaffected (they do not set the key).
  3. three cases cloned from 'ap-steal' after CASES:
       ap-steal-meta-real           = ap-steal with 00385BA0 real               -> predicted b14 0x02 (as before)
       ap-steal-empty-meta-scripted = b33=1 on the 0xFFFF slot, 00385BA0 stub   -> predicted b14 0x02
       ap-steal-empty-meta-real     = b33=1 on the 0xFFFF slot, 00385BA0 real   -> predicted b14 0x00
     (initial b14 0x07; stealtab [0x3001, 0xFFFF, 0x4002]; two real 003008A0 steals in every case)
  4. their checks, inserted before the 'ap-item' check.
Usage (ORACLE): python pending_oracle_s21_385ba0_cases.py <path-to-check.py>; run; record per ORACLE's process.
Running the harness rewrites its result.json - ORACLE's call. OPUS makes no claim about the outcome.
"""
import io
import sys

A1 = "        ent = self.SCR.get(addr)\n        if ent is not None:\n            tag, retkey = ent\n            self._args(tag)\n            if retkey:\n"
N1 = ("        if addr in self.case.get(\"realbodies\", ()):   # OPUS block 264 patch: run shipped bytes\n"
      "            self.trace.append(\"real_%x\" % addr)\n"
      "            return\n") + A1
A2 = "        gm.w(base + 0x140, dw(r.get(\"d140\", 0)))    # flag word 2\n"
N2 = A2 + ("        if r.get(\"meta_real\"):   # OPUS block 264 patch: keep 385BA0 off the battle-state block\n"
           "            gm.w(base + 0x138, dw(0xFFFFFFFF))\n"
           "            gm.w(base + 0x13C, dw(0xFFFFFFFF))\n")
A3 = "\n\ndef run_case(name, case, raw, secs):\n"
N3 = ("\n\n# OPUS block 264 patch: S-21 I8 divergence cases (00385BA0 real vs scripted, empty steal slot)\n"
      "CASES[\"ap-steal-meta-real\"] = dict(CASES[\"ap-steal\"], realbodies={X_85BA0},\n"
      "                                    rec=dict(CASES[\"ap-steal\"][\"rec\"], meta_real=1))\n"
      "CASES[\"ap-steal-empty-meta-scripted\"] = dict(CASES[\"ap-steal\"],\n"
      "                                              rec=dict(CASES[\"ap-steal\"][\"rec\"], b33=1))\n"
      "CASES[\"ap-steal-empty-meta-real\"] = dict(CASES[\"ap-steal\"], realbodies={X_85BA0},\n"
      "                                          rec=dict(CASES[\"ap-steal\"][\"rec\"], b33=1, meta_real=1))\n") + A3[2:]
A4 = "    elif name == \"ap-item\":\n"
N4 = ("    elif name in (\"ap-steal-meta-real\", \"ap-steal-empty-meta-scripted\", \"ap-steal-empty-meta-real\"):\n"
      "        # OPUS block 264 patch: static prediction, blocks 240/264\n"
      "        if tr.count(\"i08a0_real\") != 2:\n"
      "            f.append(\"08A0 count %d want 2 (slots 0,2)\" % tr.count(\"i08a0_real\"))\n"
      "        want = 0x00 if name == \"ap-steal-empty-meta-real\" else 0x02\n"
      "        eq(\"b14\", trec[\"b14\"], want)\n") + A4


def main(path):
    s = io.open(path, encoding="utf-8", newline="").read()
    if "OPUS block 264 patch" in s:
        print("already patched")
        return 0
    eol = "\r\n" if "\r\n" in s else "\n"

    def e(t):
        return t.replace("\n", eol)
    for a in (A1, A2, A3, A4):
        if s.count(e(a)) != 1:
            print("anchor not unique/missing:", a.strip()[:60])
            return 1
    for a, n in ((A1, N1), (A2, N2), (A3, N3), (A4, N4)):
        s = s.replace(e(a), e(n))
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print("patched")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
