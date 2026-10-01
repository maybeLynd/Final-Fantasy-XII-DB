"""Conditional original count-loop/selected-field dataflow; Method A only.

Fresh result [disposable source directory]. No native/service execution.
"""
import importlib.util
import json
import pathlib
import sys

W = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("source_records", W / "prove-title-queue-consumption.py")
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
spec = importlib.util.spec_from_file_location("decoded_annotations", W / "validate-title-source-annotations.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)


def main():
    if len(sys.argv) not in (2, 3):
        raise ValueError("fresh result [source directory]")
    out = pathlib.Path(sys.argv[1])
    source = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else W
    if out.exists():
        raise ValueError("immutable result exists")
    pins = []
    raw, x = P.load(source, "title-cleanup-count-selector-source-01.json", pins)
    annotations = S.validate(raw)
    spans = {
        "0x62b100": ("0x62b170", "6fadd69dd27b4ba1e27b6c8874af4005b5ef935ebb032957a70e7c6e9cc711b4"),
        "0x623df0": ("0x623e28", "b8e0d8db65e69c3595d7bab7b40ebea5a9738aa8676f0fff27a00539524b844a"),
    }
    if len(raw["ranges"]) != 2 or any(q["start"] not in spans or (q["end_exclusive"], q["sha256"]) != spans[q["start"]] for q in raw["ranges"]):
        raise ValueError("incomplete/wrong original span")
    if raw.get("pdata_entry") != [0x62B100, 0x62B170, 0x1D6B7C8] or raw.get("selector_leaf", {}).get("trailing_bytes") != "cc"*8:
        raise ValueError("named span/leaf prerequisite changed")
    loop = P.closed(x, 0x62B100, 0x62B170)
    leaf = P.closed(x, 0x623DF0, 0x623E28)
    if loop["calls"] != [dict(pc="0x62b129", target="0x623df0"),
                         dict(pc="0x62b139", target="0x5ccb80"),
                         dict(pc="0x62b143", target="0x623df0")]:
        raise ValueError("first-access/service order changed")
    if leaf["calls"] or leaf["returns"] != ["0x623e0d", "0x623e27"]:
        raise ValueError("selector not completely closed at both returns")
    for pc, mnemonic, args in [
        (0x62B10A, "mov", "edx, dword ptr [rcx + 0x30]"),
        (0x62B10D, "xor", "ebx, ebx"), (0x62B10F, "and", "edx, 0x7fffffff"),
        (0x62B115, "mov", "eax, 1"), (0x62B11A, "mov", "rdi, rcx"),
        (0x62B11D, "cmovne", "eax, edx"), (0x62B120, "test", "eax, eax"),
        (0x62B122, "je", "0x62b165"), (0x62B124, "mov", "edx, ebx"),
        (0x62B126, "mov", "rcx, rdi"), (0x62B129, "call", "0x623df0"),
        (0x62B12E, "mov", "ecx, dword ptr [rax]"), (0x62B130, "test", "ecx, ecx"),
        (0x62B132, "jle", "0x62b14e"), (0x62B134, "mov", "ecx, 1"),
        (0x62B139, "call", "0x5ccb80"), (0x62B13E, "mov", "edx, ebx"),
        (0x62B140, "mov", "rcx, rdi"), (0x62B143, "call", "0x623df0"),
        (0x62B148, "mov", "ecx, dword ptr [rax]"), (0x62B14A, "test", "ecx, ecx"),
        (0x62B14C, "jg", "0x62b134"), (0x62B14E, "mov", "ecx, dword ptr [rdi + 0x30]"),
        (0x62B151, "inc", "ebx"), (0x62B153, "and", "ecx, 0x7fffffff"),
        (0x62B159, "mov", "eax, 1"), (0x62B15E, "cmovne", "eax, ecx"),
        (0x62B161, "cmp", "ebx, eax"), (0x62B163, "jb", "0x62b124"),
        (0x623DF0, "mov", "eax, dword ptr [rcx + 0x30]"),
        (0x623DF3, "btr", "eax, 0x1f"), (0x623DF7, "cmp", "eax, 1"),
        (0x623DFA, "jbe", "0x623e0e"), (0x623DFC, "mov", "r8, qword ptr [rcx + 0x38]"),
        (0x623E00, "mov", "eax, edx"), (0x623E02, "imul", "rax, rax, 0x58"),
        (0x623E06, "add", "rax, 0x38"), (0x623E0A, "add", "rax, r8"),
        (0x623E0D, "ret", ""), (0x623E0E, "lea", "r8, [rcx + 0x38]"),
        (0x623E12, "xor", "ecx, ecx"), (0x623E14, "test", "eax, eax"),
        (0x623E16, "mov", "eax, edx"), (0x623E18, "cmove", "r8, rcx"),
        (0x623E1C, "imul", "rax, rax, 0x58"), (0x623E20, "add", "rax, 0x38"),
        (0x623E24, "add", "rax, r8"), (0x623E27, "ret", ""),
    ]:
        P.need(x, pc, mnemonic, args)
    if any(i["memory"] and any(m["role"] in ("w", "rw") for m in i["memory"]) for pc, i in x.items() if 0x623DF0 <= pc < 0x623E28):
        raise ValueError("selector has an unchecked write")
    if x[0x623E0E]["memory"][0]["role"] != "addr" or x[0x62B12E]["memory"][0]["role"] != "r":
        raise ValueError("selector address/first read role changed")
    result = dict(
        status="PRODUCER_CHECKED_CONDITIONAL_COUNT_SELECTOR_INDEPENDENT_PENDING", producer_complete=True,
        method="A STATIC_ONLY", exe_sha256=P.SHA, source_pins=pins, normal_cfgs=[loop, leaf],
        annotation_prerequisite=annotations, checker_sha256=P.sha(pathlib.Path(__file__)),
        helper_sha256=P.sha(W / "prove-title-queue-consumption.py"),
        question="Does62B100 sanitize zero count before processing, and what does623DF0 return?",
        established=[
            "623DF0 returns B+zeroextend32(EDX)*58+38 modulo2^64, with B=0 for n0, object+38 for n1, pointer[object+38] for n>1 and n=DWORD+30&7FFFFFFF. It selects a record's+38 field, not its base; bit31 does not change this local selection. Both normal branches/returns are verified.",
            "The selector has no local index-versus-count check, calls or memory writes. Masked count0 still returns38 for index0, not NULL. A nonzero input index also contributes its stride for count1; caller bounds are a separate requirement.",
            "62B100 initial bound is max(1,n), index0; its first selected DWORD read precedes5CCB80. With unchanged count0 across the two initial reads, that access is absolute38. No local count sanitizer, empty-state skip or native service call occurs before this read; backed-memory and valid-state prerequisites remain required.",
            "For selected DWORD signed-positive,62B100 passes ECX1 to5CCB80, selects the current field again, rereads it and repeats while signed-positive. It does not pass the selected pointer/object to that service in RCX. Service purpose, side effects and progress/termination are unproved.",
            "After a nonpositive selected value it increments index and reloads masked count, again choosing max(1,n), then uses unsigned index<bound. Under stable valid count/storage and terminating native service, n>0 visits indices0..n-1. Actual changing count/storage or service effects invalidate that fixed-extent/termination premise.",
            "Thus62B100 does not locally repair the zero-count state before the previously proved cleanup loop; this moves the valid-state obligation to constructors/writers/callers. It does not prove that the shipping game ever creates or reaches that invalid state.",
        ],
        partition_basis="All masked32-bit counts are exactly n0/n1/n>=2; both values of bit31 are ignored locally. MOV EAX,EDX zero-extends index; 58*(2^32-1)+38 fits64 bits before base addition. This is instruction/dataflow proof, not sampled/native cases.",
        assumptions=["ABI-correct normally returning code with backed object count field", "No conflicting count write across initial caller/selector reads for zero-count witness", "Stable valid selected storage/count and terminating opaque service for fixed loop extent"],
        limitations=["No native/emulated/game execution, actual zero-state or initialized pointer/ownership proof", "No inferred refcount/scheduler meaning, safe lifetime/idempotence/cancellation or5CCB80 effects", "No full constructor/count-writer census, concurrency safety or all malformed-input guarantee"],
        affected_claims=["FABLE queued cleanup valid count/storage preconditions", "OPUS selector return offset and caller-bounded index ABI"],
        next_discriminator="Use original constructor/count-writer/caller evidence to prove n>=1 at cleanup or identify a legitimate zero-state skip; do not force a native state and call it natural reachability",
        native_runs=0, live_runs=0, new_whole_runtime_rows_closed=0,
        cleanup="All source reads/synchronous helpers only; no PC/game/save/config/reference/peer writes",
    )
    with out.open("x", encoding="utf8") as f:
        json.dump(result, f, indent=2)
    print("Original selected-field offset and first-access zero-state precondition proved; initialization/service effects OPEN")


if __name__ == "__main__":
    main()
