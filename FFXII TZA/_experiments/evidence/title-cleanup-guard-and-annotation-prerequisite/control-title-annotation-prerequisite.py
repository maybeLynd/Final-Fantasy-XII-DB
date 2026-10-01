"""Bounded controls of the actual title publication/read prerequisite.

Retained inputs stay immutable. Changed records are labelled synthetic fixtures.
No board, canonical, native, live or peer writes. Every child exits before return.
"""
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

W = pathlib.Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_driver():
    spec = importlib.util.spec_from_file_location("actual_publication", W / "prepare-residue-packet-publication.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_new(p, value):
    with p.open("x", encoding="utf8") as f:
        json.dump(value, f, indent=2)


def worker():
    folder, result_name, out = pathlib.Path(sys.argv[2]), sys.argv[3], pathlib.Path(sys.argv[4])
    if out.exists():
        raise ValueError("immutable result exists")
    result = load_driver().verify_packet_annotations(folder, result_name)
    write_new(out, result)


def main():
    if len(sys.argv) != 2:
        raise ValueError("fresh output directory")
    out = pathlib.Path(sys.argv[1])
    out.mkdir()
    driver = load_driver()
    checks = []

    def run_case(name, argv, target, expected_exit):
        prefix = out / name
        r = subprocess.run(argv, capture_output=True, timeout=45, cwd=driver.ROOT)
        for suffix, data in [(".stdout", r.stdout), (".stderr", r.stderr)]:
            with pathlib.Path(str(prefix)+suffix).open("xb") as f:
                f.write(data)
        write_new(pathlib.Path(str(prefix)+".status.json"), dict(argv=argv, exit=r.returncode))
        if (r.returncode == 0) != (expected_exit == 0) or target.exists() != (expected_exit == 0):
            raise AssertionError("wrong terminal/output result: " + name)
        checks.append(dict(case=name, exit=r.returncode, result_exists=target.exists(),
                           status="PASS_POSITIVE" if expected_exit == 0 else "PASS_REFUSED_NO_RESULT"))

    for task, name in driver.ANNOTATION_RESULTS.items():
        folder = W / driver.JOBS[task]["pairs"][0][0]
        target = out / (driver.JOBS[task]["slug"] + "-qualified.json")
        run_case(driver.JOBS[task]["slug"], [sys.executable, str(pathlib.Path(__file__)), "--worker",
                  str(folder), name, str(target)], target, 0)
        value = json.loads(target.read_text())
        if value["status"] != "VERIFIED_PREREQUISITE" or not value["source_checks"]:
            raise ValueError("missing/zero qualification")

    task = "ASTRA-PUBLISH-TITLE-TRACKER-CALLBACK-0930"
    name = driver.ANNOTATION_RESULTS[task]
    frozen = W / driver.JOBS[task]["pairs"][0][0]
    for case_name in ["false-annotation-with-current-pin", "false-access-role-with-current-pin", "zero-source-map", "missing-source"]:
        fixture = out / case_name
        fixture.mkdir()
        result = json.loads((frozen / name).read_text())
        for pin in result["source_pins"]:
            dest = fixture / pin["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(frozen / pin["path"], dest)
        pin = result["source_pins"][0]
        src = fixture / pin["path"]
        source = json.loads(src.read_text())
        if case_name == "false-annotation-with-current-pin":
            record = source["ranges"][0]["instructions"][0]
            record["mnemonic"], record["args"] = "je", "0x1fb6b7"
            src.write_text(json.dumps(source, indent=2), encoding="utf8")
            pin["sha256"] = sha(src)
        elif case_name == "false-access-role-with-current-pin":
            records = [i for q in source["ranges"] for i in q["instructions"] if i["memory"]]
            if not records:
                raise ValueError("missing real memory control")
            memory = records[0]["memory"][0]
            memory["role"] = "w" if memory["role"] != "w" else "r"
            src.write_text(json.dumps(source, indent=2), encoding="utf8")
            pin["sha256"] = sha(src)
        elif case_name == "zero-source-map":
            result["source_pins"] = []
        else:
            src.unlink()
        write_new(fixture / name, result)
        target = fixture / "must-not-exist.json"
        run_case(case_name, [sys.executable, str(pathlib.Path(__file__)), "--worker",
                  str(fixture), name, str(target)], target, 1)

    for case_name in ["cleanup-missing-continuation", "cleanup-wrong-unwind-parent"]:
        fixture = out / case_name
        fixture.mkdir()
        result = json.loads((W / "title-cleanup-guard-scope-result-02.json").read_text())
        for pin in result["source_pins"]:
            shutil.copyfile(W / pin["path"], fixture / pin["path"])
        src = fixture / "title-cleanup-callees-source-01.json"
        source = json.loads(src.read_text())
        if case_name == "cleanup-missing-continuation":
            source["ranges"] = [q for q in source["ranges"] if q["start"] != "0x62bf2b"]
        else:
            source["verified_unwind_chains"][0]["steps"][0]["parent"][0] += 1
        src.write_text(json.dumps(source, indent=2), encoding="utf8")
        target = fixture / "must-not-exist.json"
        run_case(case_name, [sys.executable, str(W / "prove-title-cleanup-guard-scope-02.py"),
                  str(target), str(fixture)], target, 1)

    write_new(out / "result.json", dict(
        status="PASS_PRODUCER_PREREQUISITE_CONTROLS_INDEPENDENT_PENDING", checks=checks,
        driver_sha256=sha(pathlib.Path(__file__)), publication_driver_sha256=sha(W / "prepare-residue-packet-publication.py"),
        validator_sha256=sha(W / "validate-title-source-annotations.py"),
        guard_checker_sha256=sha(W / "prove-title-cleanup-guard-scope-02.py"),
        limits="Actual prerequisite function and reader CLI tested; full guarded prepare/publish requires a real current claim. Four retained positives, six labelled defect/missing controls; no new native/live experiments or independent acceptance.",
        cleanup="All subprocesses terminal; owned disposable fixture files only; retained/canonical/reference/peer bytes unchanged",
    ))
    print("Four retained prerequisites verified; six actual malformed/missing cases refused. No game execution.")


if __name__ == "__main__":
    if sys.argv[1] == "--worker":
        worker()
    else:
        main()
