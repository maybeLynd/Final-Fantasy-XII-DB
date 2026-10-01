"""Local teardown branches and named free import; Method A, fresh result only.

This proves the original call/import boundary, not actual CRT/heap effects.
"""
import hashlib, importlib.util, json, pathlib, sys

W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("source_checks", W / "prove-title-queue-consumption.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)


def main():
    if len(sys.argv) not in (2, 3):
        raise ValueError("fresh result [disposable source directory]")
    out = pathlib.Path(sys.argv[1])
    source = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    if out.exists():
        raise ValueError("immutable output exists")
    pins = []
    raw, x = P.load(source, "title-cleanup-import-boundary-source-02.json", pins)
    callback, c = P.load(source, "title-cleanup-callback-queue-source-01.json", pins)
    if raw.get("pdata_entries") != [[0x5DE250, 0x5DE282, 0x1D9FF38]]:
        raise ValueError("wrong teardown pdata")
    expected = {
        "0x5de250": ("0x5de282", "6b2681abecb85b9a3ec34068909ae6f6eb9b00da7d3fc64ab8c5df27bd71a2c0"),
        "0x19c590": ("0x19c597", "b15d06e9f05badc31af760cf0820c11e11edb991d8ae644a8280aa9b9da9e78d"),
    }
    if len(raw["ranges"]) != 2 or any(
        q["start"] not in expected or (q["end_exclusive"], q["sha256"]) != expected[q["start"]]
        for q in raw["ranges"]
    ):
        raise ValueError("wrong local source identity")
    for pc, mnemonic, args in [
        (0x5DE25F, "mov", "rbx, rcx"),
        (0x5DE262, "call", "0x625f00"),
        (0x5DE268, "test", "al, al"),
        (0x5DE26A, "je", "0x5de275"),
        (0x5DE26C, "mov", "rcx, rbx"),
        (0x5DE26F, "call", "0x62bcb0"),
        (0x5DE275, "mov", "rcx, rbx"),
        (0x5DE27D, "jmp", "0x616c60"),
        (0x19C590, "jmp", "qword ptr [rip + 0x7265b1]"),
    ]:
        P.need(x, pc, mnemonic, args)
    for pc, mnemonic, args in [
        (0x17ECC6, "mov", "rbx, rcx"),
        (0x17ECC9, "call", "0x5de250"),
        (0x17ECCE, "mov", "rcx, rbx"),
        (0x17ECD6, "jmp", "0x19c590"),
    ]:
        P.need(c, pc, mnemonic, args)
    memory = x[0x19C590]["memory"]
    if len(memory) != 1 or memory[0]["rip_target"] != "0x8c2b48" or memory[0]["role"] != "r":
        raise ValueError("wrong actual import pointer read")
    entry = raw.get("import_boundary", {})
    if entry != dict(
        dll="api-ms-win-crt-heap-l1-1-0.dll", name="free", hint=24,
        descriptor_rva="0x1ccad08", lookup_table_rva="0x1ccb8b0", slot=1,
        iat="0x8c2b48", descriptor_bytes="b0b8cc010000000000000000e6f5cc01402b7a00",
        lookup_bytes="80eecc0100000000", name_bytes="18006672656500",
    ):
        raise ValueError("wrong named original import binding")
    todo, seen, calls = [0x5DE250], set(), []
    while todo:
        pc = todo.pop()
        if pc in seen:
            continue
        if pc not in x or not 0x5DE250 <= pc < 0x5DE282:
            raise ValueError("unclosed normal teardown CFG")
        seen.add(pc)
        i = x[pc]
        if i["mnemonic"] == "jmp":
            if pc != 0x5DE27D or i["args"] != "0x616c60":
                raise ValueError("unexpected external tail")
            continue
        if i["mnemonic"].startswith("j"):
            todo.append(int(i["args"], 16))
        if i["mnemonic"] == "call":
            calls.append((pc, i["args"]))
        todo.append(pc + len(bytes.fromhex(i["bytes"])))
    if seen != {pc for pc in x if 0x5DE250 <= pc < 0x5DE282} or sorted(calls) != [
        (0x5DE262, "0x625f00"), (0x5DE26F, "0x62bcb0"),
    ]:
        raise ValueError("unchecked local teardown instructions/calls")
    result = dict(
        status="PRODUCER_CHECKED_IMPORT_BOUNDARY_INDEPENDENT_PENDING",
        producer_complete=True, method="A STATIC_ONLY", exe_sha256=P.SHA,
        source_pins=pins, normal_cfg_instructions=len(seen),
        helper_sha256=P.sha(W / "prove-title-queue-consumption.py"),
        checker_sha256=P.sha(pathlib.Path(__file__)),
        question="What explicit cleanup/import boundary does the queued callback reach on normal return?",
        established=[
            "5DE250 preserves its incoming pointer, calls625F00, optionally calls62BCB0 when returned AL is nonzero, then tails616C60 with that pointer. These three callee effects remain separate, not an invented full resource teardown.",
            "17ECC0 preserves its input in RBX, calls5DE250, restores RCX from that preserved input on normal return, then tails19C590. Normal ABI-preserving callee return is required.",
            "Exact7B19C590 jumps through original IAT8C2B48. The shipping PE lookup and descriptor bind that slot to free in api-ms-win-crt-heap-l1-1-0.dll; it is not an object vtable dispatch.",
            "Thus, IF the established queue consumer invokes17ECC0 with its stored data and the teardown returns normally, that same pointer is handed to the named free import. No normal gameplay occurrence, loaded module identity, successful heap effect or valid ownership is established by this source composition.",
        ],
        assumptions=[
            "Normally returning ABI-preserving625F00/62BCB0/616C60 and callback entry",
            "Loaded IAT follows the unmodified shipping import binding for a native free effect; this was not observed",
            "Pointer/heap validity and correct resource ownership require separate evidence",
        ],
        limitations=[
            "No execution or live process read; named import is not proof of native effects under a stub or modified IAT",
            "No all-child resource cleanup, cancellation/drain, initialization, alias/reuse or title lifetime guarantee",
            "Optional pefile unavailable and malformed generated source refused before reduction; only corrected02 source is used",
        ],
        next_discriminators=[
            "Bound625F00/62BCB0/616C60 where their effects are necessary for title lifecycle; check existing peer evidence first",
            "Retained/static ownership/constructor/writer evidence before fresh process observation",
        ],
        affected_claims=["FABLE title deferred resource release boundary", "OPUS callback ABI/heap ownership contracts"],
        native_runs=0, live_runs=0, new_whole_runtime_rows_closed=0,
        cleanup="Read-only original source/import data; own synchronous scripts; no PC/game/save/config/reference write",
    )
    with out.open("x", encoding="utf8") as f:
        json.dump(result, f, indent=2)
    print("Original teardown/free import boundary proved; callee effects and lifetime remain OPEN")


if __name__ == "__main__":
    main()
