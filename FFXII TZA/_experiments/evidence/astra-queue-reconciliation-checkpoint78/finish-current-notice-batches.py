"""Finish the exact prepared notice tail, stopping on any refused prerequisite.

Each child remains a five-operation, fresh-preimage, supported CLI batch.
This launcher neither retries nor mutates the board itself. It saves terminal
status and exception evidence instead of treating missing output as success.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent

def main():
    start, end = 77, 118
    run = HERE / "finish-current-notice-batches-01"
    run.mkdir()
    driver = HERE / "apply-current-bounded.py"
    for first in range(start, end + 1, 5):
        last = min(first + 4, end)
        tag = "current-%03d-%03d" % (first, last)
        command = [sys.executable, "-B", str(driver), str(first), str(last), tag]
        receipt = {"argv": command, "driver_sha256": hashlib.sha256(driver.read_bytes()).hexdigest()}
        try:
            child = subprocess.run(command, capture_output=True, text=True, timeout=540)
            receipt.update(exit=child.returncode, stdout=child.stdout, stderr=child.stderr)
            terminal = HERE / tag / "terminal.json"
            if terminal.is_file():
                receipt["terminal"] = json.loads(terminal.read_text())
            ok = (child.returncode == 0 and receipt.get("terminal", {}).get("status") == "CURRENT_BOUNDED_BATCH_COMPLETE"
                  and receipt["terminal"]["last"] == last)
        except Exception as error:
            receipt["exception"] = repr(error)
            ok = False
        receipt["status"] = "CHECKED_CHILD_TERMINAL" if ok else "STOPPED_NO_RETRY"
        (run / (tag + ".json")).write_text(json.dumps(receipt, indent=2))
        print(json.dumps({"batch": tag, "status": receipt["status"]}), flush=True)
        if not ok:
            raise SystemExit(1)
    (run / "terminal.json").write_text(json.dumps({"status": "PREPARED_NOTICE_TAIL_COMPLETE", "start": start, "last": end}, indent=2))

if __name__ == "__main__":
    main()
