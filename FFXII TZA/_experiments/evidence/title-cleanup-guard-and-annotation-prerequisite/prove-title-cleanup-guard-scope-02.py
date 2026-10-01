"""Original BC guard scope and local cleanup/caller predicates; Method A only.

Fresh result [optional disposable source directory]. No native/emulated execution.
"""
import importlib.util, json, pathlib, struct, sys

W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("source_checks", W / "prove-title-queue-consumption.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
annotation_spec = importlib.util.spec_from_file_location("byte_annotations", W / "validate-title-source-annotations.py")
S = importlib.util.module_from_spec(annotation_spec)
annotation_spec.loader.exec_module(S)


def cfg(ix, start, end, tail=None):
    todo, seen, calls, returns = [start], set(), [], []
    while todo:
        pc = todo.pop()
        if pc in seen:
            continue
        if pc not in ix or not start <= pc < end:
            raise ValueError("normal CFG leaves proved fragments")
        seen.add(pc)
        i = ix[pc]
        if i["mnemonic"] == "ret":
            returns.append(hex(pc))
            continue
        if i["mnemonic"] == "jmp":
            target = int(i["args"], 16)
            if tail is not None and target == tail:
                continue
            todo.append(target)
            continue
        if i["mnemonic"].startswith("j"):
            todo.append(int(i["args"], 16))
        if i["mnemonic"] == "call":
            calls.append(dict(pc=hex(pc), target=i["args"]))
        todo.append(pc + len(bytes.fromhex(i["bytes"])))
    if seen != {pc for pc in ix if start <= pc < end}:
        raise ValueError("unchecked local instructions")
    return dict(entry=hex(start), end_exclusive=hex(end), instructions=len(seen),
                returns=sorted(returns), opaque_calls=sorted(calls, key=lambda x: int(x["pc"], 16)),
                tail=hex(tail) if tail is not None else None)


def main():
    if len(sys.argv) not in (2, 3):
        raise ValueError("fresh result [disposable source directory]")
    out = pathlib.Path(sys.argv[1])
    source = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    if out.exists():
        raise ValueError("immutable result exists")
    pins = []
    raw, x = P.load(source, "title-cleanup-callees-source-01.json", pins)
    caller, c = P.load(source, "title-cleanup-import-boundary-source-02.json", pins)
    annotation_checks = [S.validate(raw), S.validate(caller)]
    root = [0x62BCB0, 0x62BCF1, 0x1DA8B68]
    expected_entries = [
        root, [0x62BCF1, 0x62BD04, 0x1DA8510],
        [0x62BD04, 0x62BF24, 0x1DA8524], [0x62BF24, 0x62BF2B, 0x1DA853C],
        [0x62BF2B, 0x62BF37, 0x1DA854C], [0x616C60, 0x616CBD, 0x1DA8590],
    ]
    if raw.get("pdata_entries") != expected_entries or len(raw.get("verified_unwind_chains", [])) != 4:
        raise ValueError("incomplete original cleanup chain")
    for chain in raw["verified_unwind_chains"]:
        current = chain["fragment"]
        if chain["root"] != root or not chain["steps"]:
            raise ValueError("wrong original chain root")
        for step in chain["steps"]:
            z = bytes.fromhex(step["raw_unwind"])
            n = 4 + 2*((z[2] + 1) & ~1)
            parent = [v + 0x120000 for v in struct.unpack_from("<III", z, n)]
            if not z[0] >> 3 & 4 or len(z) != n+12 or step["entry"] != current or step["parent"] != parent:
                raise ValueError("raw unwind/preimage mismatch")
            current = parent
        if current != root:
            raise ValueError("unclosed original chain")
    spans = {
        "0x625f00": ("0x625f0b", "6d349b012688951b55484ac4d52f372b3b3cd9a1c1ecf45b58433c19485f0567"),
        "0x62bcb0": ("0x62bcf1", "5e3fb7d69a511147d10a8cb0e5ca6301d1739e9894d4d82b4f4bde2498dab8d7"),
        "0x62bcf1": ("0x62bd04", "4e1bb58a3b4a7bfe71a383eae4ea3f6a0fac855b0d1ba76f2c7faffd3130ae57"),
        "0x62bd04": ("0x62bf24", "24450e2df1d737c74a52dd9d76ae2607cc490473f9b2e54388abdecd8a6a8fd5"),
        "0x62bf24": ("0x62bf2b", "d0467028639ac68fe790545d4c5b78651e1109574efb5dc7cc486bec82d1efd7"),
        "0x62bf2b": ("0x62bf37", "4904e69f3fed77695c4378c265dd1e79785e072d2d0322341c048ec607ab2afa"),
        "0x616c60": ("0x616cbd", "6750a87d2d33d6e73f8e0a31fadf4b358d0fe043bec205d9fde807b16bdd1f16"),
    }
    if len(raw["ranges"]) != len(spans) or any(
        q["start"] not in spans or (q["end_exclusive"], q["sha256"]) != spans[q["start"]]
        for q in raw["ranges"]
    ):
        raise ValueError("missing/changed original span")
    guard_cfg = cfg(x, 0x625F00, 0x625F0B)
    cleanup_cfg = cfg(x, 0x62BCB0, 0x62BF37)
    common_cfg = cfg(x, 0x616C60, 0x616CBD, 0x5DE290)
    for pc, mnemonic, args in [
        (0x625F00, "cmp", "dword ptr [rcx + 0xbc], 0"),
        (0x625F07, "setne", "al"), (0x625F0A, "ret", ""),
        (0x62BCBE, "call", "0x62b100"), (0x62BCC3, "mov", "rcx, qword ptr [rbx + 0x20]"),
        (0x62BCC7, "xor", "r14d, r14d"), (0x62BCCA, "mov", "dword ptr [rbx + 0xbc], r14d"),
        (0x62BCD1, "test", "rcx, rcx"), (0x62BCD4, "je", "0x62bce3"),
        (0x62BCD6, "call", "0x62b870"), (0x62BCDB, "test", "eax, eax"),
        (0x62BCDD, "jne", "0x62bf2b"), (0x62BCE3, "mov", "ecx, dword ptr [rbx + 0x30]"),
        (0x62BCE6, "mov", "eax, 1"), (0x62BCEB, "and", "ecx, 0x7fffffff"),
        (0x62BCF9, "cmovne", "eax, ecx"), (0x62BCFC, "test", "eax, eax"),
        (0x62BCFE, "je", "0x62bf24"), (0x62BD13, "btr", "eax, 0x1f"),
        (0x62BD17, "cmp", "eax, 1"), (0x62BD1A, "jbe", "0x62bd22"),
        (0x62BD1C, "mov", "rcx, qword ptr [rbx + 0x38]"),
        (0x62BD22, "lea", "rcx, [rbx + 0x38]"), (0x62BD26, "test", "eax, eax"),
        (0x62BD28, "jne", "0x62bd2d"), (0x62BD2A, "mov", "rcx, r14"),
        (0x62BD2D, "mov", "eax, ebp"), (0x62BD2F, "imul", "rsi, rax, 0x58"),
        (0x62BD33, "cmp", "qword ptr [rsi + rcx + 0x28], r14"),
        (0x62BF29, "xor", "eax, eax"), (0x62BF36, "ret", ""),
        (0x616C72, "call", "0x62b100"), (0x616C78, "mov", "rcx, rbx"),
        (0x616C7B, "call", "0x62bcb0"), (0x616C81, "mov", "ecx, dword ptr [rbx + 0x30]"),
        (0x616C84, "mov", "eax, ecx"), (0x616C86, "shr", "eax, 0x1f"),
        (0x616C89, "not", "al"), (0x616C8B, "test", "al, 1"),
        (0x616C8D, "je", "0x616ca7"), (0x616C8F, "btr", "ecx, 0x1f"),
        (0x616C93, "cmp", "ecx, 1"), (0x616C96, "jbe", "0x616ca7"),
        (0x616C98, "mov", "rcx, qword ptr [rbx + 0x38]"),
        (0x616C9C, "test", "rcx, rcx"), (0x616C9F, "je", "0x616ca7"),
        (0x616CA1, "call", "0x584730"), (0x616CA7, "xor", "eax, eax"),
        (0x616CA9, "mov", "qword ptr [rbx + 0x38], rax"),
        (0x616CAD, "mov", "dword ptr [rbx + 0x30], eax"),
        (0x616CB0, "mov", "rcx, rbx"), (0x616CB8, "jmp", "0x5de290"),
    ]:
        P.need(x, pc, mnemonic, args)
    for pc, mnemonic, args in [
        (0x5DE262, "call", "0x625f00"), (0x5DE268, "test", "al, al"),
        (0x5DE26A, "je", "0x5de275"), (0x5DE26F, "call", "0x62bcb0"),
        (0x5DE275, "mov", "rcx, rbx"), (0x5DE27D, "jmp", "0x616c60"),
    ]:
        P.need(c, pc, mnemonic, args)
    for pc in [0x62BCCA, 0x616CA9, 0x616CAD]:
        if x[pc]["memory"][0]["role"] != "w":
            raise ValueError("actual local store role changed")
    if x[0x62BD22]["memory"][0]["role"] != "addr":
        raise ValueError("inline selector LEA is not a memory read")
    result = dict(
        status="PRODUCER_CHECKED_CONDITIONAL_GUARD_SCOPE_INDEPENDENT_PENDING",
        producer_complete=True, method="A STATIC_ONLY", exe_sha256=P.SHA,
        source_pins=pins, normal_cfgs=[guard_cfg, cleanup_cfg, common_cfg],
        annotation_prerequisites=annotation_checks,
        checker_sha256=P.sha(pathlib.Path(__file__)),
        helper_sha256=P.sha(W / "prove-title-queue-consumption.py"),
        question="Does BC zero prevent all queued cleanup, and what local release/empty-count premises apply?",
        established=[
            "625F00 writes AL=(DWORD[object+BC]!=0); it is an11B local read predicate, not an established ownership/refcount test or initialized object proof. Upper RAX bits are not established by SETNE AL.",
            "5DE250 gates its first62BCB0 call on that AL, then normally tails616C60, whose62BCB0 call is unconditional. Under normal ABI returns there is one reached direct cleanup call when sampled BC=0, two when nonzero; opaque callee reentry is outside that local count.",
            "62BCB0 first delegates62B100, then locally clears BC before optionally calling62B870 on object+20. A nonzero EAX from that delegate takes the early RET path preserving it, skipping the record loop. The ordinary loop completion writes EAX0. Neither caller tests62BCB0's result before continuing its common cleanup path.",
            "The local iteration bound uses n=DWORD+30 masked7FFFFFFF and max(1,n). Selector uses NULL for n0, inline object+38 for n1, pointer[object+38] for n>1, with58B record stride. If the post-delegate loop-entry count is0, the first member read is at absolute28; there is no local empty-zero sanitizer. This is a conditional malformed-state precondition, not observed gameplay or proof that native delegates permit that state.",
            "616C60 calls584730 on object+38 only when bit31 of current DWORD+30 is clear, masked count>1 and pointer+38 is nonNULL. It then zeros pointer+38 and DWORD+30 and tails5DE290 on every normal local branch. Bit31 semantics beyond this release predicate remain unassigned.",
            "Thus BC zero is not a guarantee of no cleanup calls; nonzero delegate returns are not propagated as a local abort by the outer teardown callers. No successful resource destruction, safe repetition, cancellation/drain or all-child release follows from these call/store facts.",
        ],
        assumptions=[
            "ABI-normal returning original callees; pointer/object fields and selected58B records backed for ordinary behavior",
            "Valid nonzero loop-entry count and stable count/storage where iteration safety/termination is required",
            "Native62B100/62B870/584730/5DE290, virtual callbacks and global62EC70 effects remain boundaries",
            "Local call multiplicity excludes reentry; no loaded-game state or pointer binding asserted",
        ],
        limitations=[
            "No native/emulated/game execution, live initialized BC/count, ownership/refcount or lifetime proof",
            "No all-branch native effect coverage or universal idempotence/leak/double-free/malformed-input safety",
            "Five unwind fragments and syntactic normal CFG closure are coverage evidence, not five experiments",
        ],
        next_discriminators=[
            "Use existing62B100/623DF0 selector and constructor/writer evidence to establish valid count/storage preconditions",
            "Bind62B870 early-return and virtual/deallocation effects only where required for title lifetime",
        ],
        affected_claims=["FABLE title/deferred release guard and status meaning", "OPUS field/count/ownership cleanup contracts"],
        native_runs=0, live_runs=0, new_whole_runtime_rows_closed=0,
        cleanup="Original file reads and checked synchronous scripts only; no PC/game/save/config/reference mutation",
    )
    with out.open("x", encoding="utf8") as f:
        json.dump(result, f, indent=2)
    print("Original BC guard scope and conditional cleanup predicates proved; native lifetime/ownership remains OPEN")


if __name__ == "__main__":
    main()
