"""rv_controls.py - SWE2-AUDIT-SPEC reviewer controls for prove-title-tracker-callback-boundary.py (2026-09-30).

usage: python rv_controls.py SCRATCH_DIR     (fresh dir outside the packet; the packet is only read)

The checker takes an optional disposable SOURCE directory, so each case copies the two retained source captures there,
mutates one thing, and runs the packet's own checker unchanged against a fresh target:
  positive             unmodified copies
  missing-queue-source  the packet's own three refusal cases, re-created here (the packet's control script writes into
  wrong-global-getter   the packet and refuses an existing output dir, so it is not re-run in place)
  old-store-role
  consistent-index-op  185A94 movsxd displacement 0xCB8 -> 0xCC0 in bytes AND args, span sha rebuilt   (witnessed op)
  fast-path-call       185AD2 'add rsp,0x38' + 185AD6 'ret' (5 bytes) -> 'call 0x1858a0' (E8 rel32), span sha rebuilt
                       (an UNWITNESSED instruction on the fast arm: does the checker gate "no call on that branch"?)
"""
import hashlib, json, pathlib, shutil, struct, subprocess, sys

PKT = pathlib.Path(__file__).resolve().parents[3] / "_experiments/evidence/title-tracker-callback-boundary"
ROOT = PKT.parents[4]
CHK = PKT / "prove-title-tracker-callback-boundary.py"
SRC = ["title-tracker-cleanup-source-01.json", "title-cleanup-callback-queue-source-01.json"]
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=False)


def edit_queue(fn):
    def m(src):
        p = src / SRC[1]
        z = json.loads(p.read_text())
        fn(z)
        p.write_text(json.dumps(z, indent=2) + "\n")
    return m


def rehash(z):
    for q in z["ranges"]:
        q["sha256"] = hashlib.sha256(bytes.fromhex("".join(i["bytes"] for i in q["instructions"]))).hexdigest()


def find(z, pc):
    for q in z["ranges"]:
        for k, i in enumerate(q["instructions"]):
            if int(i["pc"], 16) == pc:
                return q, k, i
    raise KeyError(hex(pc))


def wrong_getter(z):
    find(z, 0x189120)[2]["memory"][0]["rip_target"] = "0x1f7f5a0"


def old_role(z):
    find(z, 0x185ACF)[2]["memory"][0]["role"] = "r"


def consistent_index(z):
    i = find(z, 0x185A94)[2]
    assert i["bytes"] == "486381b80c0000", i["bytes"]
    i["bytes"] = "486381c00c0000"
    i["args"] = "rax, dword ptr [rcx + 0xcc0]"
    i["memory"][0]["displacement"] = 0xCC0
    rehash(z)


def fast_call(z):
    q, k, i = find(z, 0x185AD2)
    assert q["instructions"][k + 1]["pc"] == "0x185ad6" and i["bytes"] + q["instructions"][k + 1]["bytes"] == "4883c438c3"
    rel = 0x1858A0 - (0x185AD2 + 5)
    q["instructions"][k:k + 2] = [dict(pc="0x185ad2", bytes="e8" + struct.pack("<i", rel).hex(), mnemonic="call",
                                       args="0x1858a0", memory=[])]
    rehash(z)


def run(case, mutate):
    c = out / case
    src = c / "source"
    src.mkdir(parents=True)
    for n in SRC:
        shutil.copyfile(PKT / n, src / n)
    mutate(src)
    tgt = c / "result.json"
    r = subprocess.run([sys.executable, "-B", str(CHK), str(tgt), str(src)], cwd=ROOT, capture_output=True, text=True,
                       timeout=60)
    last = (r.stderr.strip().splitlines() or [""])[-1]
    print("%-20s exit=%d result=%s  %s" % (case, r.returncode, tgt.exists(), last if r.returncode else r.stdout.strip()))


run("positive", lambda s: None)
run("missing-queue-source", lambda s: (s / SRC[1]).unlink())
run("wrong-global-getter", edit_queue(wrong_getter))
run("old-store-role", edit_queue(old_role))
run("consistent-index-op", edit_queue(consistent_index))
run("fast-path-call", edit_queue(fast_call))
