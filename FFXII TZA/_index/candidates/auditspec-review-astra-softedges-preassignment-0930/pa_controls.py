"""SWE2-AUDIT-SPEC: ASTRA's three CLI refusal controls reproduced in THIS directory on copies of result-02's source_pins,
plus a positive twin on the SAME copy (ASTRA's positive run used the canonical packet, not a copy) and sensitivity
mutations of instructions the conclusions rest on:
  jns->js at 0060EFFB (negative-count boundary), movsxd->mov at 0059CC84 (sext32 of the slot offset),
  cmp rax, r9 -> cmp rax, r8 at 0063E430 (root exclusion), xor r13d->mov r13d,1 at 0059CC38 (preclear value)."""
import hashlib, json, pathlib, shutil, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
W = HERE.parents[2] / "_experiments" / "evidence" / "phyretext-preassignment-cleanup"
REPO = HERE.parents[4]
r = json.loads((W / "softedges-preassignment-cleanup-result-02.json").read_text())
driver = W / "reduce-softedges-preassignment-cleanup.py"
print("reducer sha matches result02:", r["checker_sha256"] == hashlib.sha256(driver.read_bytes()).hexdigest())
out = HERE / "controls"
if out.exists(): shutil.rmtree(out)   # created by this script only
out.mkdir()
CASES = [("baseline", None, None, None, None),
         ("missing-parent-getter", "softedges-array-parent-getter-code-01.json", None, None, None),
         ("false-parent-store", "softedges-array-descriptor-offset-code-01.json", 0x632dda, "args", "qword ptr [rcx + 0x78], rdx"),
         ("false-borrowed-flag", "softedges-member-assignment-code-01.json", 0x60f01f, "args", "eax, 0x1e"),
         ("jns-to-js", "softedges-member-assignment-code-01.json", 0x60effb, "mnemonic", "js"),
         ("movsxd-to-mov", "softedges-header-membership-code-01.json", 0x59cc84, "mnemonic", "mov"),
         ("root-cmp-r8", "softedges-array-descriptor-offset-code-01.json", 0x63e430, "args", "rax, r8"),
         ("preclear-r13-one", "softedges-header-membership-code-01.json", 0x59cc38, "mnemonic", "or")]
for name, fn, pc, field, val in CASES:
    c = out / name; s = c / "source"; s.mkdir(parents=True)
    for pin in r["source_pins"]:
        d = s / pin["path"]; d.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / pin["path"], d)
    hits = "-"
    if fn and pc is None:
        (s / fn).unlink()
    elif fn:
        p = s / fn; z = json.loads(p.read_text()); hits = 0
        for q in z["ranges"]:
            for i in q["instructions"]:
                if int(i["pc"], 16) == pc: i[field] = val; hits += 1
        p.write_text(json.dumps(z) + "\n")
    a = subprocess.run([sys.executable, str(driver), str(c / "result.json"), str(s)], cwd=REPO, capture_output=True, timeout=120)
    last = (a.stdout + a.stderr).decode(errors="replace").strip().splitlines()[-1:] or [""]
    print("%-22s hits=%-2s exit=%d result=%-5s | %s" % (name, hits, a.returncode, (c / "result.json").exists(), last[0][-120:]))
