"""EXP-010 read-only observation window; no focus, input, debug or process-write actions."""
import argparse
import ctypes
from ctypes import wintypes as w
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

kit = Path(__file__).resolve().parents[5] / "Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, str(kit))
import runtime_probe as rp
import ffxii_runtime as runtime
import process_liveness as live

p = argparse.ArgumentParser()
p.add_argument("--pid", required=True, type=int)
p.add_argument("--seconds", default=8.0, type=float)
p.add_argument("--out", required=True, type=Path)
a = p.parse_args()
record = {"command": sys.argv, "start_unix": time.time(), "pid": a.pid,
          "observer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "samples": [], "status": "INVALID"}
h = None
exit_code = 1
try:
    found = rp.find_process("FFXII_TZA.exe")
    assert len(found) == 1 and found[0][0] == a.pid, "require exactly the intended process"
    exe = Path(found[0][1])
    raw = exe.read_bytes()
    record["exe"] = str(exe)
    record["exe_sha256"] = hashlib.sha256(raw).hexdigest()
    assert record["exe_sha256"] == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
    verdict, hits, modules = runtime.classify(a.pid)
    record.update(module_verdict=verdict, watched_modules=hits, modules=modules)
    assert verdict == "clean" and modules, "module control failed"
    h = rp.k32.OpenProcess(rp.PROCESS_QUERY_INFORMATION | rp.PROCESS_VM_READ, False, a.pid)
    assert h, "read-only OpenProcess failed"
    reader = rp.Probe(h)
    base = rp.module_base(h)
    record["image_base"] = base
    assert base == rp.IMAGE_BASE, "module base mismatch"
    assert reader.read(rp.CONTROL_ADDR, len(rp.CONTROL_BYTES)) == rp.CONTROL_BYTES, "read control failed"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    count = struct.unpack_from("<H", raw, pe + 6)[0]
    table = pe + 24 + struct.unpack_from("<H", raw, pe + 20)[0]
    texts = []
    for n in range(count):
        off = table + n * 40
        if raw[off:off + 8].rstrip(b"\0") != b".text":
            continue
        virtual_size, rva, size, raw_off = struct.unpack_from("<4I", raw, off + 8)
        length = min(size, virtual_size)
        expected = raw[raw_off:raw_off + length]
        actual = reader.read(base + rva, length)
        assert actual is not None, "live text unreadable"
        texts.append({"rva": rva, "bytes": length,
                      "disk_sha256": hashlib.sha256(expected).hexdigest(),
                      "live_sha256": hashlib.sha256(actual).hexdigest(), "matches": actual == expected})
    record["code_identity"] = texts
    assert len(texts) == 1 and texts[0]["matches"], "live code identity mismatch"
    def q(addr):
        b = reader.read(addr, 8)
        assert b is not None, "pointer unreadable"
        value = struct.unpack("<Q", b)[0]
        assert value, "null input pointer"
        return value
    array = q(q(q(0x02EA5368) + 0xDF8) + 0x118) + 0x30
    record["input_array"] = array
    user = ctypes.WinDLL("user32", use_last_error=True)
    user.GetForegroundWindow.restype = w.HWND
    user.GetWindowThreadProcessId.argtypes = [w.HWND, ctypes.POINTER(w.DWORD)]
    rp.k32.CheckRemoteDebuggerPresent.argtypes = [w.HANDLE, ctypes.POINTER(w.BOOL)]
    start = time.perf_counter()
    cpu = live.times(h)
    record["window_start_unix"] = time.time()
    print("OBSERVING", a.pid, "for", a.seconds, "seconds", "window_start_unix", record["window_start_unix"], flush=True)
    while time.perf_counter() - start < a.seconds:
        elapsed = time.perf_counter() - start
        data = reader.read(array, 256)
        assert data is not None, "input read failed"
        fgpid = w.DWORD()
        user.GetWindowThreadProcessId(user.GetForegroundWindow(), ctypes.byref(fgpid))
        debug = w.BOOL()
        assert rp.k32.CheckRemoteDebuggerPresent(h, ctypes.byref(debug)), 'debugger presence unreadable'
        record["samples"].append({"seconds": elapsed, "cpu_seconds": live.times(h) - cpu,
                                  "foreground_pid": fgpid.value,
                                  "debugger_present": bool(debug.value),
                                  "held": [i for i, v in enumerate(data) if v]})
        time.sleep(0.01)
    record["status"] = "OBSERVED"
    exit_code = 0
except Exception as e:
    record["error"] = repr(e)
finally:
    if h:
        rp.k32.CloseHandle(h)
    record["end_unix"] = time.time()
    a.out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(record["status"], record.get("error", ""), a.out, flush=True)
raise SystemExit(exit_code)
