"""rv_slot.py - FABLE independent re-derivation for ASTRA packet render-slot-identity-publication (aac0489ac).

Own reader (rvlib.py: struct + capstone 5). Does not import ASTRA's prove.py or the shared role adapter.
Every claim is a function of the image so the controls can rerun it on a privately patched copy.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rvlib import check_manifest, Img, Body, Report, expect, run_control, fam  # noqa: E402

POOL = 0x022C6F28
BODIES = {0x0041F730: 0x0041FBE8, 0x00420480: 0x00420851, 0x004269A0: 0x00426C85, 0x004279B0: 0x00427AF9}


def bodies(img):
    return {s: Body(img, s, e) for s, e in BODIES.items()}


def c_bodies(img, R):
    tot = 0
    for s, e in BODIES.items():
        B = Body(img, s, e)
        ents, pok = img.pdata_cover(s, e)
        rets, tails, outs = B.exits()
        R.check("body %08X..%08X decodes exactly (%d B)" % (s, e, e - s), B.exact)
        R.check("body %08X .pdata tiles it as one function (%d record(s), later ones chained to the root)" % (s, len(ents)), pok,
                " ".join("%08X..%08X%s" % (b, en, "~chain" if fl & 4 else "") for b, en, fl, root in ents))
        R.check("body %08X local CFG closed (no jcc/jmp leaves, last insn ret)" % s,
                not outs and not tails and B.order and B[B.order[-1]].mnemonic == "ret",
                "rets=%s tails=%s outs=%s" % ([hex(r) for r in rets], tails, outs))
        tot += e - s
    R.check("total bytes = 3255", tot == 3255, str(tot))


def c_clear(img, R):
    B = Body(img, 0x0041F730, 0x0041FBE8)
    expect(R, B, 0x0041F744, "xor edx, edx")
    expect(R, B, 0x0041F74B, "mov r8d, 0x740")
    expect(R, B, 0x0041F751, "mov rbx, rcx")
    expect(R, B, 0x0041F754, "call 0x861ec0")
    R.check("00861EC0 is the IAT thunk for memset", img.import_name_of_thunk(0x00861EC0) == "memset",
            str(img.import_name_of_thunk(0x00861EC0)))
    # no write to rcx/rdx/r8 families between entry and the call except the three setters
    bad = [a for a in B.order if a < 0x0041F754 and ({"rcx", "rdx", "r8"} & B[a].reg_writes)
           and a not in (0x0041F744, 0x0041F74B)]
    R.check("memset args rcx=arg0, edx=0, r8d=0x740 unchanged before call", not bad, str(bad))
    expect(R, B, 0x0041F768, "or ebp, 0xffffffff")
    expect(R, B, 0x0041F795, "mov word ptr [rbx], bp")
    I = B[0x0041F795]
    R.check("0041F795 store is WORD write at disp 0", I.mems and I.mems[0]["size"] == 2 and I.mems[0]["write"]
            and I.mems[0]["disp"] == 0)
    wr = [a for a in B.order if a > 0x0041F768 and a < 0x0041F795 and ("rbp" in B[a].reg_writes or "rbx" in B[a].reg_writes)]
    R.check("rbp/rbx not rewritten between 0041F768 and 0041F795", not wr, str(wr))
    R.check("0041F768 dominates 0041F795", B.dominates(0x0041F768, 0x0041F795))
    w0 = [(hex(a), m["size"]) for a, m in B.mem_writes(lambda m: m["base"] == "rbx" and m["index"] is None and m["disp"] < 2)]
    R.note("41F730 direct rbx-based writes overlapping +0: %s" % w0)
    w284 = [(hex(a), B[a].text) for a, m in B.mem_writes(lambda m: m["base"] != "rsp" and m["index"] is None and
                                                       m["disp"] < 0x288 and m["disp"] + m["size"] > 0x284)]
    R.note("41F730 direct writes overlapping +284..+287 after the memset: %s" % w284)


def c_reset(img, R):
    B = Body(img, 0x004269A0, 0x00426C85)
    expect(R, B, 0x004269AF, "mov rsi, qword ptr [rip + 0x1ea0572]")
    R.check("004269AF loads global 022C6F28", 0x004269AF + 7 + 0x1ea0572 == POOL)
    expect(R, B, 0x004269B6, "mov edi, 0xa0")
    expect(R, B, 0x004269BB, "mov rbx, rsi")
    expect(R, B, 0x004269C0, "mov rcx, rbx")
    expect(R, B, 0x004269C3, "call 0x41f730")
    expect(R, B, 0x004269C8, "add rbx, 0x740")
    expect(R, B, 0x004269CF, "sub rdi, 1")
    expect(R, B, 0x004269D3, "jne 0x4269c0")
    # loop model: count iterations and byte offsets from the decoded constants
    offs = []
    rdi = 0xA0
    rbx = 0
    while True:
        offs.append(rbx)
        rbx += 0x740
        rdi -= 1
        if rdi == 0:
            break
    R.check("clear loop runs 160 times at stride 740h, offsets 0..%Xh" % offs[-1],
            len(offs) == 160 and offs[-1] == 159 * 0x740)
    expect(R, B, 0x004269DF, "xor ebx, ebx")
    expect(R, B, 0x004269ED, "mov qword ptr [rsi + 0x48808], rbx")
    I = B[0x004269ED]
    R.check("004269ED is a QWORD write (covers 48808 cursor and 4880C count)", I.mems[0]["size"] == 8 and I.mems[0]["write"])
    wr = [a for a in B.order if 0x004269DF < a < 0x004269ED and ({"rbx", "rsi"} & B[a].reg_writes)]
    R.check("rbx/rsi not rewritten between 004269DF and 004269ED", not wr, str(wr))
    R.check("004269ED is reached straight-line after the loop (no branch in 004269D5..004269ED)",
            all(not B[a].mnemonic.startswith("j") for a in B.order if 0x004269D5 <= a < 0x004269ED))


def c_alloc(img, R):
    B = Body(img, 0x004279B0, 0x00427AF9)
    expect(R, B, 0x004279C4, "mov rbx, qword ptr [rip + 0x1e9f55d]")
    R.check("004279C4 loads global 022C6F28", 0x004279C4 + 7 + 0x1e9f55d == POOL)
    expect(R, B, 0x004279D7, "call 0x4278e0")
    expect(R, B, 0x004279DC, "cmp ax, -1")
    expect(R, B, 0x004279E0, "je 0x4279e9")
    expect(R, B, 0x004279E9, "cmp dword ptr [rbx + 0x4880c], 0xa0")
    expect(R, B, 0x004279F3, "jge 0x4279e2")
    expect(R, B, 0x004279E2, "xor eax, eax")
    expect(R, B, 0x004279FA, "movsxd rsi, dword ptr [rbx + 0x48808]")
    expect(R, B, 0x00427A06, "imul rdi, rsi, 0x740")
    expect(R, B, 0x00427A0D, "add rdi, rbx")
    expect(R, B, 0x00427A10, "mov rcx, rdi")
    expect(R, B, 0x00427A13, "call 0x41f730")
    # every compare/test on any path entry -> 00427A13
    pre = B.reach(B.start) & B.reach(B.start)  # all reachable
    region = [a for a in B.order if a < 0x00427A13 and a in B.reach(B.start)]
    cmps = [a for a in region if B[a].mnemonic in ("cmp", "test", "bt")]
    R.check("only compares before the first clear are 004279DC (name lookup) and 004279E9 (count<160)",
            cmps == [0x004279DC, 0x004279E9], str([hex(a) for a in cmps]))
    R.check("004279E9 count compare is signed (jge)", B[0x004279F3].mnemonic == "jge")
    R.check("cursor load 004279FA is a signed DWORD read (movsxd, size 4)",
            B[0x004279FA].mnemonic == "movsxd" and B[0x004279FA].mems[0]["size"] == 4)
    # self-index store and dominance chain
    expect(R, B, 0x00427A4D, "mov word ptr [rdi], si")
    m = B[0x00427A4D].mems[0]
    R.check("00427A4D is a WORD write at [rdi+0]", m["size"] == 2 and m["write"] and m["disp"] == 0 and m["base"] == "rdi")
    wr = [a for a in B.order if 0x00427A0D < a < 0x00427A4D and ({"rsi", "rdi"} & B[a].reg_writes)
          and B[a].mnemonic != "call"]
    R.check("rsi/rdi have no in-body writer between 00427A0D and 00427A4D (calls rely on nonvolatile ABI)", not wr,
            str([hex(a) for a in wr]))
    expect(R, B, 0x00427A6E, "mov rcx, rdi")
    expect(R, B, 0x00427A71, "call 0x420480")
    expect(R, B, 0x00427A76, "or dword ptr [rdi + 0x290], 1")
    expect(R, B, 0x00427A7F, "inc dword ptr [rbx + 0x4880c]")
    # list-link publication that the packet's ID -> flag -> count order does not mention
    expect(R, B, 0x00427A18, "cmp dword ptr [rbx + 0x48810], -1")
    expect(R, B, 0x00427A21, "mov dword ptr [rbx + 0x48810], esi")
    expect(R, B, 0x00427A37, "mov word ptr [rcx + rbx + 4], si")
    expect(R, B, 0x00427A43, "mov word ptr [rdi + 2], ax")
    expect(R, B, 0x00427A47, "mov dword ptr [rbx + 0x48814], esi")
    R.check("list tail write 00427A47 dominates the self-index store 00427A4D", B.dominates(0x00427A47, 0x00427A4D))
    R.check("each path to 00427A4D first writes list head 48810 (00427A21) or the old tail row's WORD +4 (00427A37)",
            0x00427A4D not in B.reach(B.start, avoid=[0x00427A21, 0x00427A37]))
    R.note("so the new index (SI) is published into pool list state (48810/48814, predecessor +4) BEFORE WORD [record+0]")
    chain = [0x00427A13, 0x00427A4D, 0x00427A71, 0x00427A76, 0x00427A7F]
    for x, y in zip(chain, chain[1:]):
        R.check("%08X dominates %08X" % (x, y), B.dominates(x, y))
    R.check("00427A4D is not reached again after 00427A71 (no back edge into the publish region)",
            0x00427A4D not in B.reach(0x00427A76))
    # next-free scan
    expect(R, B, 0x00427A7D, "xor eax, eax")
    expect(R, B, 0x00427A85, "cmp dword ptr [rbx + 0x4880c], 0xa0")
    expect(R, B, 0x00427A94, "jl 0x427a9e")
    expect(R, B, 0x00427A96, "mov dword ptr [rbx + 0x48808], eax")
    expect(R, B, 0x00427AB0, "inc ecx")
    expect(R, B, 0x00427AB2, "mov dword ptr [rbx + 0x48808], ecx")
    expect(R, B, 0x00427AB8, "cmp ecx, 0xa0")
    expect(R, B, 0x00427ABE, "jl 0x427ac8")
    expect(R, B, 0x00427AC0, "mov ecx, eax")
    expect(R, B, 0x00427AC8, "movsxd rdx, ecx")
    expect(R, B, 0x00427ACB, "imul r8, rdx, 0x740")
    expect(R, B, 0x00427AD2, "cmp dword ptr [r8 + rbx + 0x284], eax")
    expect(R, B, 0x00427ADA, "jne 0x427ab0")
    loop = [a for a in B.order if 0x00427A7D < a <= 0x00427ADA]
    R.check("eax (=0) has no writer between 00427A7D and the loop exit", not [a for a in loop if "rax" in B[a].reg_writes])
    R.check("scan loop has no other exit than 00427ADA fall-through",
            [a for a in B.order if 0x00427AB0 <= a <= 0x00427ADA and B[a].mnemonic.startswith("j")] == [0x00427ABE, 0x00427ADA])


def c_meta(img, R):
    B = Body(img, 0x00420480, 0x00420851)
    first_non_prologue = [a for a in B.order if a >= 0x0042049A][0]
    expect(R, B, 0x0042049A, "or dword ptr [rcx + 0x284], 0x2010f9")
    R.check("0042049A is the first non-stack memory access", all(
        all(m["base"] == "rsp" for m in B[a].mems) for a in B.order if a < 0x0042049A) and first_non_prologue == 0x0042049A)
    R.check("rcx not written before 0042049A", not [a for a in B.order if a < 0x0042049A and "rcx" in B[a].reg_writes])
    calls = B.calls()
    R.check("first call in 420480 (%08X) is after 0042049A" % calls[0][0], calls[0][0] > 0x0042049A)
    R.check("0042049A dominates every call in 420480", all(B.dominates(0x0042049A, a) for a, _ in calls))
    m = B[0x0042049A].mems[0]
    R.check("0042049A is a DWORD read-modify-write", m["size"] == 4 and m["read"] and m["write"])
    hits = []
    for a, m in B.mem_writes(lambda m: m["base"] not in ("rsp",)):
        lo, hi = m["disp"], m["disp"] + m["size"]
        if m["index"] is None and (lo < 2 and hi > 0 or lo < 0x288 and hi > 0x284):
            hits.append((a, B[a].text))
    R.note("420480 direct writes overlapping +0..+1 or +284..+287 (any base): %s" % [("%08X" % a, t) for a, t in hits])
    R.check("those writes are only ORs (no clear of +0 or +284)", all(t.startswith("or ") for a, t in hits))
    idx = B.mem_writes(lambda m: m["base"] != "rsp" and m["index"] is not None)
    R.check("420480 has no indexed non-stack writes (so the scan above is not missing one)", not idx, str(idx))
    rs = [a for a in B.order if "rsi" in B[a].reg_writes]
    R.note("420480 writers of rsi: %s (rsi = record from 004204B8 to the epilogue)" % ["%08X %s" % (a, B[a].text) for a in rs])


def c_forward(img, R):
    F = Body(img, 0x0041F340, 0x0041F72E)
    expect(R, F, 0x0041F608, "movsx edx, word ptr [r14]")
    expect(R, F, 0x0041F60F, "call 0x372350")
    r14w = [a for a in F.order if "r14" in F[a].reg_writes and F[a].mnemonic != "call"]
    R.check("factory r14 = its arg0 (0041F361 mov r14, rcx; only other writer is the epilogue pop)",
            r14w == [0x0041F361, 0x0041F726] and F.dominates(0x0041F361, 0x0041F608), str(["%08X" % a for a in r14w]))
    S = Body(img, 0x00372350, 0x003723A4)
    expect(R, S, 0x00372383, "mov dword ptr [rax + 0x68], edi")
    G = Body(img, 0x004215A0, 0x00421892)
    expect(R, G, 0x004216D3, "movsx ebx, word ptr [rsi]")
    expect(R, G, 0x004216DB, "mov dword ptr [rax + 0x6c], ebx")


def c_scan_math(R):
    """Fixed-width model of 00427A9E..00427ADA. Not machine-code execution."""
    N = 160

    def scan(cur, flags, limit=1000):
        visited = []
        ecx = cur
        for _ in range(limit):
            ecx = (ecx + 1) & 0xFFFFFFFF
            if (ecx ^ 0x80000000) - 0x80000000 >= N:  # jl is signed
                ecx = 0
            idx = (ecx ^ 0x80000000) - 0x80000000
            visited.append(idx)
            if not (0 <= idx < N):
                return "OOB", visited
            if flags[idx] == 0:
                return "STOP", visited
        return "NOSTOP", visited

    ok_bounds = True
    ok_cycle = True
    ok_term = True
    for cur in range(N):
        st, v = scan(cur, [1] * N, limit=N)
        ok_bounds &= all(0 <= i < N for i in v)
        ok_cycle &= sorted(v) == list(range(N)) and v[-1] == cur
        for z in range(N):
            fl = [1] * N
            fl[z] = 0
            st, v = scan(cur, fl)
            ok_term &= st == "STOP" and len(v) <= N
    R.check("model: from any cursor 0..159 every visited index is 0..159", ok_bounds)
    R.check("model: 160 visits cover all 160 rows exactly once, ending at the start cursor", ok_cycle)
    R.check("model: with one stable zero +284 anywhere, the scan stops within 160 visits (160x160 cases)", ok_term)
    st, v = scan(5, [1] * N, limit=10 * N)
    R.check("countermodel: all 160 flags nonzero -> no stop within 1600 visits (cycles)", st == "NOSTOP")
    # count gate vs cursor: livecount 0 passes `cmp count,0xa0 / jge`, cursor -1 or 160 still selects a record
    for cur in (-1, 160):
        passes_gate = not (0 >= 0xA0)
        off = cur * 0x740
        R.check("countermodel: count 0 passes gate, cursor %d -> record offset %d outside [0, %d)" % (cur, off, N * 0x740),
                passes_gate and not (0 <= off < N * 0x740))
    # count after increment
    R.check("countermodel premise: count 0 -> 1 after 00427A7F, 1 < 160 so the scan at 00427A9E is entered", 1 < 0xA0)


def run_all(img, R):
    c_bodies(img, R)
    c_clear(img, R)
    c_reset(img, R)
    c_alloc(img, R)
    c_meta(img, R)
    c_forward(img, R)


def main():
    img = Img.load()
    R = Report("render-slot")
    print("== image sha256 verified, base %X" % img.base)
    check_manifest(R, "render-slot-identity-publication", "a2bcea12693de55748686a2cef48402c0189666974a8af9a8c0720b2717c73ee")
    run_all(img, R)
    c_scan_math(R)
    print("== controls (each mutation/wrong expectation must be REJECTED)")
    ctl = [
        ("count cap 0xA0 -> 0x9F at 004279EF", lambda: img.patched(0x004279EF, bytes([0x9F])), c_alloc),
        ("self-index WORD store -> DWORD (66 89 37 -> 89 37 90)", lambda: img.patched(0x00427A4D, bytes([0x89, 0x37, 0x90])), c_alloc),
        ("insert cursor compare before clear (movsxd -> cmp esi,0 ; nops)",
         lambda: img.patched(0x004279FA, bytes([0x83, 0xFE, 0x00, 0x90, 0x90, 0x90, 0x90])), c_alloc),
        ("OR 2010F9 -> AND at 0042049A", lambda: img.patched(0x0042049A, bytes([0x81, 0xA1])), c_meta),
        ("clear size 740h -> 73Fh at 0041F74D", lambda: img.patched(0x0041F74D, bytes([0x3F])), c_clear),
        ("reset loop count 0xA0 -> 0x9F at 004269B7", lambda: img.patched(0x004269B7, bytes([0x9F])), c_reset),
        ("body end shifted: wrong .pdata expectation", lambda: img, None),
    ]
    allok = True
    for label, fac, fn in ctl:
        if fn is None:
            def fn2(im, RR):
                RR.check("x", im.pdata_cover(0x004279B0, 0x00427AF8)[1])
            res = run_control(label, fac, fn2)
        else:
            res = run_control(label, fac, fn)
        allok &= res
        R.check("CONTROL rejects: " + label, res)
    # known-answer: the reader sees WORD vs DWORD widths
    from rvlib import Insn
    ci = next(img.cs.disasm(bytes([0x66, 0x89, 0x37]), 0))
    ci2 = next(img.cs.disasm(bytes([0x0F, 0x11, 0x01]), 0))
    a1, a2 = Insn(img.cs, ci).mems[0], Insn(img.cs, ci2).mems[0]
    R.check("CONTROL known-answer: 66 89 37 = WORD write; 0F 11 01 = 16-byte write (corrected reader)",
            a1["size"] == 2 and a1["write"] and a2["size"] == 16 and a2["write"])
    R.note("instrument defect recorded: capstone's own access flag for 0F 11 01 says write=%s; rvlib treats a "
           "destination memory operand as written" % a2["cs_write"])
    print("== %d FAIL" % R.fails)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
