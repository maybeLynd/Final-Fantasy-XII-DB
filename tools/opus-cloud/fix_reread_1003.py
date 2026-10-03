"""fix_reread_1003.py - OPUS's re-read corrections to the drafted ee rows of 2026-10-03 (sead-win-config, the Lua loader
and later packs). Each entry replaces one clause the bytes contradict or overstate; the reason is recorded in the
record's rows.json 'corrections'. Idempotent: an entry whose OLD text is gone is skipped (each NEW differs from OLD in a
way that does not contain OLD)."""
import io
import json
import os

C = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates"

FIXES = {
    "opus-sead-win-config-ee-1003": [
        ("00220DE0", "and finally stores 1 to byte `[rcx+0x90]`",
         "and finally re-reads byte `[rcx+0x90]` and stores 1 there when it is zero, 0 otherwise",
         "the final store is `sete` of the re-read byte (00220E5B..00220E65), not a constant 1"),
        ("007AA110", "builds `count` 0x30-byte elements after it (qword `+0` = `01CB44A0`, every other field 0)",
         "builds `count` 0x30-byte elements after it (qword `+0` = `01CB44A0`, qwords `+8`/`+0x10`, dwords `+0x1C`/`+0x24` and byte `+0x20` = 0)",
         "the build loop writes only those fields (007AA1C0..007AA1D2); dword +0x18 and qword +0x28 are not written"),
        ("007B4A70", "(moving on to qword node `+0x10` when that succeeds)",
         "(moving on to qword node `+0x10` when that succeeds and visiting the same node again when it fails)",
         "the state-3 path jumps back to the loop test with rbx unchanged on failure (007B4B4E cmovns, 007B4BAA)"),
        ("007B4A70", "&qword s+0x10, qword o+0x38",
         "the address of a stack copy of qword `s+0x10`, qword o+0x38",
         "r9 = rsp+0x40, which holds a copy of qword [s+0x10] (007B4BF4, 007B4C06, 007B4C3B)"),
        ("007D85E0", "with qword `+0` = `01CB7068` and their fields zeroed",
         "with qword `+0` = `01CB7068` and bytes `+8`..`+0x17`, dwords `+0x1C`/`+0x24` and byte `+0x20` zeroed",
         "the record build writes only those fields (007D860D..007D86E4); dword +0x18 and qword +0x28 are not written"),
        ("007D9530", "with `r` = `007AED00()` it stores",
         "calling `007AED00()` twice (each result `r`) it stores",
         "007AED00 is called at 007D9584 and again at 007D95A4"),
        ("007D99E0", "and their other fields zeroed, except",
         "and bytes `+8`..`+0x17`, dwords `+0x1C`/`+0x24` and byte `+0x20` zeroed, except",
         "the record build writes only those fields (007D9A0A..007D9AAE); dword +0x18 and qword +0x28 are not written"),
        ("007DA0A0", "and the other fields zeroed",
         "and dwords `+8`/`+0x14`/`+0x1C`/`+0x24` and byte `+0x20` zeroed",
         "the record build writes only those fields besides qword +0xC (007DA0DA..007DA10B); dword +0x18 and qword +0x28 are not written"),
        ("007DAAB0", "qword `+0x24` = 0x3F800000, other fields 0",
         "qword `+0x24` = 0x3F800000, dwords `+0x20`/`+0x2C`/`+0x34`/`+0x3C` and byte `+0x38` = 0",
         "the record build writes only those fields (007DAAE4..007DAB00); dwords +0x30 and +0x40 are not written"),
        ("007DDED0", "a block passed to `007DD2B0` and qword `02EAE0C0`",
         "the zeroed block passed through `007DD2B0`, whose return is stored to qword `02EAE0C0`",
         "02EAE0C0 receives 007DD2B0's return (007DE0BB, 007DE0CA), not the block pointer directly"),
        ("007E9E60", "&qword s+0x10",
         "the address of a stack copy of qword `s+0x10`",
         "rdx = rsp+0x50, which holds a copy of qword [s+0x10] (007E9EA2..007E9ECE)"),
    ],
    "opus-the-lua-loader-and-what-it-accepts-ee-1003": [
        ("00682E30", "when that bit was set, links the record before the list head at qword `+0x10` + 0x90",
         "when that value is non-null, appends the record to the circular list whose sentinel is at qword `+0x10` + 0x90",
         "the branch at 00682E9A tests ZF from `sub rbx, rax` (the cleared pointer), not the bit; the insert at 00682EE9..00682EF7 links before the sentinel, i.e. at the tail"),
        ("0081E5A0", "to `0081DC10`; both then",
         "to `0081DC10` (when it is null, `0081DC10` gets the incoming `rdx`); both then",
         "a null qword c+0x38 skips the call but still reaches 0081DC10 with rdi = the incoming rdx (0081E6E0 -> 0081E6FE)"),
        ("008233F0", "qword `c+0x38` is above qword `[rcx+0x28]`",
         "qword `c+0x38` is not above qword `[rcx+0x28]`",
         "`jbe 008234C7` at 008234AD calls the line hook when the position is at or below the saved one; the line comparison runs only when it is above"),
        ("00828D30", "registers `01CCC970` with the registry's index 2 as upvalue (`008109F0`, `00810730`, `008135B0(.., 1)`)",
         "registers the functions at `01CCC970` into the registry's index-2 table with the package table as their one upvalue (`008109F0`, `00810730(rcx, -2)`, `008135B0(.., 1)`)",
         "008135B0 sets each closure into the table at -(nup+2) (the index-2 table pushed by 008109F0) with nup copies of the top value (the package table copy from 00810730) as upvalues"),
        ("0082F000", "for list `+0xC` and list `+8` with the current pc and `r8d`",
         "for list `+0xC` and list `+8` with the current pc, `r8d` and the position of the emitted false and true load respectively (-1 when none was emitted)",
         "the fifth argument of the two 00830540 calls is r15d / r12d, the 0082F360 results or -1 (0082F182, 0082F195)"),
        ("008113D0", "below: the closure qword `[qword [rcx+0x20]]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when that closure's dword `+8` is 0x16 or the index exceeds its byte `+0xA`",
         'below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`',
         "the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)"),
        ("00811470", "below: the closure qword `[qword [rcx+0x20]]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when that closure's dword `+8` is 0x16 or the index exceeds its byte `+0xA`",
         'below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`',
         "the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)"),
        ("00811530", "below: the closure qword `[qword [rcx+0x20]]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when that closure's dword `+8` is 0x16 or the index exceeds its byte `+0xA`",
         'below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`',
         "the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)"),
        ("00811640", "below: the closure qword `[qword [rcx+0x20]]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when that closure's dword `+8` is 0x16 or the index exceeds its byte `+0xA`",
         'below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`',
         "the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)"),
    ],
    "opus-sound-variant-selection-ee-1003": [
        ('007CF780', 'writes to the output pair at `rdx` the qword `01CB6E80` followed by',
         'writes to the output pair at `rdx` the address `01CB6E80` followed by',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-sound-variant-selection-ee-1003), incorporated verbatim: each body stores the lea result, the address itself'),
        ('007CFE60', 'writes the qword `01CB6E10` to `[rdx]`',
         'writes the address `01CB6E10` to `[rdx]`',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-sound-variant-selection-ee-1003), incorporated verbatim: each body stores the lea result, the address itself'),
        ('007D0710', 'writes the qword `01CB6E10` to `[rdx]`',
         'writes the address `01CB6E10` to `[rdx]`',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-sound-variant-selection-ee-1003), incorporated verbatim: each body stores the lea result, the address itself'),
    ],
    "opus-referenced-code-the-list-never-had-uc1-1002": [
        ('00125743', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00125753', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('008824F0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('008832D0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00884090', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('008858B0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00888650', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00888690', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00888700', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00888780', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('008888C0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00889330', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('0088D4E0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('0088DB60', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('008922A0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00892990', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00893A80', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00893AC0', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
        ('00895570', 'no direct reference was found (call/jump, rip-reference and table scans)',
         'no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)',
         'SWE2-AUDIT-SPEC narrowing (auditspec-review-opus-uc1-entry-rereview-1003), incorporated verbatim: the row names the census R1 test 1 now requires'),
    ],
}


def main():
    for rec, fixes in FIXES.items():
        p = os.path.join(C, rec, "rows.json")
        d = json.load(io.open(p, encoding="utf-8"))
        rows = {r["fn"]: r for r in d["rows"]}
        done = []
        for fn, old, new, why in fixes:
            r = rows[fn]
            if old in r["text"]:
                assert r["text"].count(old) == 1, (fn, old)
                r["text"] = r["text"].replace(old, new)
                d.setdefault("corrections", []).append({"fn": fn, "why": why if why.startswith("SWE2-AUDIT-SPEC") else "OPUS re-read: " + why})
                done.append(fn)
            elif new not in r["text"]:
                print("WARN %s %s: neither the old nor the new clause is present" % (rec, fn))
        if done:
            json.dump(d, io.open(p, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
        print(rec, "applied", done)


if __name__ == "__main__":
    main()
