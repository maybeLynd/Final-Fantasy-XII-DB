"""S-50 DA-1, bounded statically (OPUS, 2026-09-26): the shipping image contains no code that can create a lua_State.

Lua 5.2 creates a state in lua_newstate, whose protected body f_luaopen calls luaT_init (ltm.c: interns the tag-method names
"__index" ... "__call" from luaT_eventname) and luaX_init (llex.c: interns the reserved words from luaX_tokens), and stores
MEMERRMSG "not enough memory" (lstate.c). luaL_newstate (lauxlib.c) wraps it and installs a panic function whose message is
"PANIC: unprotected error in call to Lua API (%s)". If any of these is linked, its marker is referenced by code.

Census over the whole .text (every 4-byte window read as a rip-relative displacement ending the instruction, AND every 4-byte
window equal to the image-base-relative displacement target - 0x120000, the form `lea rax, [rip -> 00120000]` + [rax + disp]
that 00824386 uses), plus every qword in the image equal to the target (pointer tables). Domain: this image only.
Markers expected ABSENT if no constructor is linked:
 M1  the string "not enough memory" (MEMERRMSG);
 M2  the string "PANIC: unprotected error in call to Lua API";
 M3  a code reference to the tag-method name table (luaT_init's only use of it);
 M4  a code reference to luaX_tokens from anything other than luaX_token2str (luaX_init).
Positive controls, expected PRESENT (they prove the Lua core is linked and the scanner finds both reference forms):
 P1  "C stack overflow" and "error in error handling" referenced by code (ldo.c);
 P2  "_ENV" referenced by luaX_setinput 008242A0 (llex.c is linked);
 P3  luaX_tokens referenced image-base-relative by luaX_token2str 00824340 (the second reference form is detected);
 P4  "_LOADED" referenced by code (lauxlib.c is linked, so luaL_newstate's absence is not lauxlib's absence).
Static. Writes result.json.
"""
import hashlib
import json
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
FUNCS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "graph", "functions.tsv"))

raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
pe = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe + 6)[0]
optsz = struct.unpack_from("<H", raw, pe + 20)[0]
BASE = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
secs = []
o = pe + 24 + optsz
for _ in range(nsec):
    name = raw[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ra = struct.unpack_from("<IIII", raw, o + 8)
    secs.append((name, BASE + va, vs, ra, rs))
    o += 40
img = {}
for name, va, vs, ra, rs in secs:
    img[va] = raw[ra:ra + min(vs, rs)] + bytes(max(0, vs - rs))
text = [s for s in secs if s[0] == ".text"][0]
code, code_va = img[text[1]], text[1]
starts = sorted(int(l.split("\t")[0], 16) for l in open(FUNCS, encoding="utf-8", errors="replace") if l[:1] in "0123456789ABCDEF")


def func(a):
    lo, hi = 0, len(starts)
    while lo < hi:
        mid = (lo + hi) // 2
        if starts[mid] <= a:
            lo = mid + 1
        else:
            hi = mid
    return "%08X" % starts[lo - 1]


def find_strings(s):
    out = []
    for va, blob in img.items():
        for m in re.finditer(re.escape(s), blob):
            out.append(va + m.start())
    return sorted(out)


def code_refs(target):
    """functions whose code references target, rip-relative or image-base-relative"""
    hits = set()
    ib = struct.pack("<I", (target - BASE) & 0xFFFFFFFF)
    for i in range(len(code) - 4):
        d = struct.unpack_from("<i", code, i)[0]
        if code_va + i + 4 + d == target:
            hits.add(func(code_va + i))
    i = code.find(ib)
    while i != -1:
        hits.add(func(code_va + i))
        i = code.find(ib, i + 1)
    return sorted(hits)


def ptr_refs(target):
    p = struct.pack("<Q", target)
    out = []
    for va, blob in img.items():
        j = blob.find(p)
        while j != -1:
            out.append("%08X" % (va + j))
            j = blob.find(p, j + 1)
    return out


def table_of(first, second):
    """a pointer table whose entry 0 points at string `first` and entry 1 at `second`"""
    for a in find_strings(b"\x00" + first + b"\x00"):
        s = a + 1
        for t in ptr_refs(s):
            t = int(t, 16)
            nxt = struct.unpack_from("<Q", img[[va for va in img if va <= t < va + len(img[va])][0]], t - [va for va in img if va <= t < va + len(img[va])][0] + 8)[0]
            for va, blob in img.items():
                if va <= nxt < va + len(blob) and blob[nxt - va:nxt - va + len(second) + 1] == second + b"\0":
                    return t
    return None


R = {}
R["M1_not_enough_memory"] = [{"at": "%08X" % a, "code_refs": code_refs(a)} for a in find_strings(b"not enough memory")]
R["M2_panic"] = [{"at": "%08X" % a, "code_refs": code_refs(a)} for a in find_strings(b"PANIC: unprotected error in call to Lua API")]
events = table_of(b"__index", b"__newindex")
R["M3_event_table"] = {"at": "%08X" % events if events else None, "code_refs": code_refs(events) if events else None,
                       "newindex_string_code_refs": [code_refs(a + 1) for a in find_strings(b"\x00__newindex\x00")]}
tokens = table_of(b"and", b"break")
R["M4_tokens_table"] = {"at": "%08X" % tokens if tokens else None, "code_refs": code_refs(tokens) if tokens else None}
R["P1"] = {s.decode(): [code_refs(a) for a in find_strings(s)] for s in (b"C stack overflow", b"error in error handling")}
R["P2_ENV"] = [code_refs(a + 1) for a in find_strings(b"\x00_ENV\x00")]
R["P4_LOADED"] = [code_refs(a + 1) for a in find_strings(b"\x00_LOADED\x00")]
cases = {
    "M1_no_MEMERRMSG_literal": R["M1_not_enough_memory"] == [],
    "M2_no_luaL_newstate_panic_message": R["M2_panic"] == [],
    "M3_tag_method_names_never_interned": events is not None and R["M3_event_table"]["code_refs"] == [] and all(r == [] for r in R["M3_event_table"]["newindex_string_code_refs"]),
    "M4_reserved_words_read_only_by_token2str": tokens is not None and R["M4_tokens_table"]["code_refs"] == ["00824340"],
    "P1_ldo_messages_referenced": all(any(r) for r in R["P1"].values()),
    "P2_luaX_setinput_references_ENV": any("008242A0" in r for r in R["P2_ENV"]),
    "P3_image_base_form_detected_via_token2str": tokens is not None and "00824340" in R["M4_tokens_table"]["code_refs"],
    "P4_lauxlib_linked": any(r for r in R["P4_LOADED"]),
}
res = {"static": True, "domain": "the shipping image only (sha256 %s)" % SHA[:16], "census": R, "cases": cases, "ok": all(cases.values())}
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1, sort_keys=True)
for k, v in cases.items():
    print("%-60s %s" % (k, "PASS" if v else "FAIL"))
print(json.dumps(R)[:1500])
print("ALL PASS" if res["ok"] else "FAILED")
raise SystemExit(0 if res["ok"] else 1)
