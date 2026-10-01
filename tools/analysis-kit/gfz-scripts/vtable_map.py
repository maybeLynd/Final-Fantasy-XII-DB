#!/usr/bin/env python3
"""vtable_map.py - recover MSVC vtables from .rdata and name them via RTTI.

Written 2026-09-02 for AR-3. Pass 52 measured that 7,185 unowned functions have no call
edge and are reachable only through a pointer stored in data - 65.8 % of the apparently
uncalled code. A call-graph tool can never attribute them. This one can, because MSVC
stores a Complete Object Locator at vtable[-1] and the locator names the class.

    vtable[-1] -> _RTTICompleteObjectLocator {
        DWORD signature;         // 1 on x64
        DWORD offset;            // offset of this vftable in the object
        DWORD cdOffset;
        DWORD pTypeDescriptor;   // RVA
        DWORD pClassDescriptor;  // RVA
        DWORD pSelf;             // RVA of this locator  (x64 only; the check that matters)
    }
    TypeDescriptor { void *pVFTable; void *spare; char name[]; }   // ".?AVFoo@Bar@@"

The `pSelf` field is what makes this safe: a false positive would have to contain its own
address. That is the difference between this and a heuristic pointer scan.

WHAT THIS TOOL CANNOT SEE - read before treating an unnamed table as anonymous
-----------------------------------------------------------------------------
  * A class compiled without RTTI (/GR-) has vtables with no locator. They are reported
    as UNNAMED runs, not as "not vtables".
  * A run of function pointers is not necessarily a vtable. Jump tables, callback arrays
    and static dispatch tables have the same shape. Only the named ones are certain.
  * Slot count is the length of the pointer run, which merges adjacent tables when one
    ends and another begins with no locator between them.

An UNNAMED run is a candidate, not a vtable.
"""
import argparse, collections, io, re, struct, sys
import kit_paths as KP  # noqa: E402
import os

EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
FUNCS = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")


def load_image(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from('<I', d, 0x3C)[0]
    n = struct.unpack_from('<H', d, pe + 6)[0]
    optsz = struct.unpack_from('<H', d, pe + 20)[0]
    base = struct.unpack_from('<Q', d, pe + 24 + 24)[0]
    off = pe + 24 + optsz
    secs = []
    for i in range(n):
        o = off + i * 40
        secs.append((d[o:o+8].rstrip(b'\0').decode(), struct.unpack_from('<I', d, o+12)[0],
                     struct.unpack_from('<I', d, o+8)[0], struct.unpack_from('<I', d, o+20)[0],
                     struct.unpack_from('<I', d, o+16)[0]))
    return d, base, secs


_UNDNAME = None


def _load_undname():
    """dbghelp!UnDecorateSymbolName, or None when unavailable (non-Windows)."""
    global _UNDNAME
    if _UNDNAME is None:
        try:
            import ctypes, ctypes.wintypes as w
            fn = ctypes.WinDLL("dbghelp.dll").UnDecorateSymbolName
            fn.argtypes = [ctypes.c_char_p, ctypes.c_char_p, w.DWORD, w.DWORD]
            fn.restype = w.DWORD

            def call(sym):
                buf = ctypes.create_string_buffer(8192)
                n = fn(sym.encode("ascii", "replace"), buf, 8192, 0)
                return buf.value.decode("ascii", "replace") if n else None
            _UNDNAME = call
        except Exception:
            _UNDNAME = False
    return _UNDNAME or None


_RTTI_SUFFIX = re.compile(r"\s*`RTTI Type Descriptor'\s*$")
_TYPE_PREFIX = re.compile(r"^\s*(class|struct|union|enum)\s+")


def demangle_naive(m):
    """The '@'-reversing splitter. Correct for non-template names ONLY - kept as the
    fallback when dbghelp is unavailable. See demangle()."""
    if not m.startswith(".?A"):
        return m
    body = m[4:] if len(m) > 4 and m[3] in "VU" else m[3:]
    body = body.rstrip("@")
    parts = [p for p in body.split("@") if p]
    return "::".join(reversed(parts)) if parts else m


def demangle(m):
    """'.?AVFoo@Bar@@' -> 'Bar::Foo', correct for template classes too.

    AS-9 FIXED 2026-09-02. The previous implementation reversed the mangled name on '@',
    which is right for a plain qualified name but wrong for a TEMPLATE: the mangled form
    nests a second qualified name inside the first, so splitting on '@' emitted the outer
    namespace twice and flattened the template arguments into the namespace path -

        naive  : SQEX::Sd::SQEX::Sd::Driver::Core::$00PEAVCoreSourceVoice::?$FixedList::NODE
        correct: SQEX::Sd::FixedList<1,class SQEX::Sd::Driver::Core::CoreSourceVoice *>::NODE

    Rather than hand-roll an MSVC demangler this asks Windows to do it: the real symbol for
    a type descriptor is '??_R0' + <name after the dot> + '@8', which dbghelp decodes.

    MEASURED over the 2,335 NUL-terminated '.?A...' names in FFXII_TZA.exe:
        2,335 / 2,335 decoded by dbghelp, none fell through;
        all   621 non-template names -> byte-identical to demangle_naive();
        all 1,714 template names     -> differ, and only the template ones differ.
    So this changes exactly the names that were wrong and nothing that was already right.

    WHAT THE FIX DOES NOT DO - measured by diffing the --out TSV before and after:
        (vtable, slot, target) triples : byte-identical, in the same order
        rows whose class name changed  : 21,895 / 25,798  (84.9 %)
        distinct class strings         : 2,248 before, 2,248 after  (NO reduction)
        distinct (vtable, class) pairs : 2,286 before, 2,286 after
    The old splitter was injective - each distinct mangled name produced its own distinct
    wrong string - so correcting the names moves no counts at all. The 25,798-vs-25,603
    triple discrepancy against rtti_recover.py that the old docstring blamed on this defect
    is therefore NOT caused by it and is still unexplained. Do not treat AS-9 as having
    closed that gap.

    HARVESTING NOTE for anyone scanning for these strings: a type name is NUL-terminated and
    contains '@@' internally (a template argument list is itself '@@'-terminated). A regex
    that stops at the first '@@' truncates every template name - read to the NUL instead.

    Falls back to demangle_naive() when dbghelp is unavailable or cannot decode a name, so
    the tool still runs off-Windows with the old, template-incorrect behaviour.
    """
    if not m.startswith(".?A"):
        return m
    und = _load_undname()
    if und is not None:
        s = und("??_R0" + m[1:] + "@8")
        if s:
            s = _TYPE_PREFIX.sub("", _RTTI_SUFFIX.sub("", s)).strip()
            if s:
                return s
    return demangle_naive(m)


def top_namespace(cls):
    """Enclosing namespace of a demangled class name, for the summary tally.

    Must not split on a '::' that sits inside template arguments: correct names contain
    them ('TAsyncUpdate<class Phyre::PFoo>::Bar' has no top-level namespace), and a plain
    split() on '::' reports 'TAsyncUpdate<class Phyre'. A name beginning with a backtick is
    a function-local class, whose enclosing scope is a function rather than a namespace.
    """
    if cls.startswith("`"):
        return "(function-local)"
    depth = 0
    i = 0
    while i < len(cls) - 1:
        c = cls[i]
        if c == "<":
            depth += 1
        elif c == ">":
            depth -= 1
        elif c == ":" and cls[i + 1] == ":" and depth == 0:
            return cls[:i]
        i += 1
    return "(global)"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--functions", default=FUNCS)
    ap.add_argument("--out", help="TSV of vtable,class,slot,target")
    ap.add_argument("--min-run", type=int, default=1)
    a = ap.parse_args(argv)

    d, imb, secs = load_image(a.exe)

    def rva2raw(r):
        for nm, vo, vs, ro, rsz in secs:
            if vo <= r < vo + vs:
                o = ro + (r - vo)
                return o if o < len(d) else None
        return None

    def va2raw(v):
        return rva2raw(v - imb)

    ents = set()
    for i, l in enumerate(io.open(a.functions, encoding="utf-8", errors="replace")):
        if i == 0:
            continue
        p = l.rstrip("\n").split("\t")
        if len(p) > 1 and not p[1].startswith(("Unwind@", "Catch_All@")):
            try:
                ents.add(int(p[0], 16))
            except ValueError:
                pass

    text = [s for s in secs if s[0] == '.text'][0]
    TLO, THI = text[1] + imb, text[1] + imb + text[2]

    def is_fn(v):
        return TLO <= v < THI

    def read_col(va):
        """Return the class name if va is a valid x64 Complete Object Locator."""
        o = va2raw(va)
        if o is None or o + 24 > len(d):
            return None
        sig, offs, cd, ptd, pcd, pself = struct.unpack_from('<6I', d, o)
        if sig != 1 or pself != va - imb:
            return None
        to = rva2raw(ptd)
        if to is None:
            return None
        e = d.find(b'\0', to + 16, to + 16 + 512)
        if e < 0:
            return None
        try:
            return d[to + 16:e].decode('ascii')
        except UnicodeDecodeError:
            return None

    named, unnamed, rows = {}, [], []
    for nm, vo, vs, ro, rsz in secs:
        if nm in ('.text', '.pdata', '.reloc'):
            continue
        lo, hi = ro, ro + min(rsz, vs)
        i = lo
        while i + 8 <= hi:
            v = struct.unpack_from('<Q', d, i)[0]
            if not (is_fn(v) and v in ents):
                i += 8
                continue
            j = i
            run = []
            while j + 8 <= hi:
                w = struct.unpack_from('<Q', d, j)[0]
                if is_fn(w) and w in ents:
                    run.append(w)
                    j += 8
                else:
                    break
            va = imb + vo + (i - ro)
            cls = None
            if i - 8 >= lo:
                p = struct.unpack_from('<Q', d, i - 8)[0]
                if p:
                    mangled = read_col(p)
                    if mangled:
                        cls = demangle(mangled)
            if len(run) >= a.min_run:
                if cls:
                    named[va] = (cls, run)
                    for k, t in enumerate(run):
                        rows.append((va, cls, k, t))
                else:
                    unnamed.append((va, run))
            i = j

    nf = sum(len(v[1]) for v in named.values())
    uf = sum(len(r[1]) for r in unnamed)
    print("NAMED vtables (RTTI locator verified via pSelf): %d" % len(named))
    print("   slots: %d   distinct functions: %d" % (nf, len({t for _, v in named.items() for t in v[1]})))
    print("UNNAMED pointer runs (candidates, NOT confirmed vtables): %d" % len(unnamed))
    print("   slots: %d   distinct functions: %d" % (uf, len({t for _, r in unnamed for t in r})))
    allfn = {t for _, v in named.items() for t in v[1]} | {t for _, r in unnamed for t in r}
    print("union of function pointers found in data: %d" % len(allfn))

    ns = collections.Counter()
    for cls, _ in named.values():
        ns[top_namespace(cls)] += 1
    print("\ntop namespaces by named vtable count:")
    for k, v in ns.most_common(12):
        print("   %-34s %5d" % (k[:34], v))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("vtable\tclass\tslot\ttarget\n")
            for va, cls, k, t in rows:
                f.write("%08X\t%s\t%d\t%08X\n" % (va, cls, k, t))
        print("\nwrote %s (%d rows)" % (a.out, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
