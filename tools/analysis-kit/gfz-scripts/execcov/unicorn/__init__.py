"""Unicorn execution-coverage shim (OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R).

Placed on PYTHONPATH ahead of site-packages so `import unicorn` inside a sealed
experiment `check.py` resolves here. The real unicorn package is loaded underneath
and re-exported; only `Uc` is wrapped.

For every constructed Uc the shim adds one UC_HOOK_BLOCK observer and maintains a
shadow call stack at basic-block granularity:

  * a block whose terminator is `call` marks the NEXT executed block as a callee;
    the callee's functions.tsv entry (exact entry-address match, else None) and the
    expected return address are pushed,
  * a `ret`-terminated block pops one frame; a popped catalogue entry counts
    ENTERED+RETURNED. The containing body of every executed ret also counts
    returned (covers harness entry calls and tail-call transfers),
  * the first block of each emu_start pushes an implicit frame so the
    harness-called subject function pairs with its terminating ret,
  * a catalogue entry reached as a jmp target is entered without a frame
    (tail call): its later ret pops the caller's frame, as real code does.

At process exit the executed catalogue entries are classified per entry:

  returned        frame popped by a ret, or a ret executed inside the body extent
  faulted         open frame when the run faulted, or the body holding fault RIP
  returned+faulted  both, in different emu_starts of the run
  open            frame still open at a clean emu_stop (cap / sentinel end)
  entered         entry executed, no return observed, not open, no fault
  body_only       body blocks executed but the entry itself never ran
                  (mid-body jump targets, fall-throughs)
  stubbed         NOT EXECUTED - the entry block's guest bytes differ from the
                  shipped bytes and end in a ret within 16 bytes (a harness
                  entry patch such as `gm.w(va, b"\xc3")`)
  scripted        NOT EXECUTED - the entry block was observed but control
                  reached the frame's return address without a ret (a
                  UC_HOOK_CODE at the entry wrote RIP = return address)

Only `returned`, `faulted` and `returned+faulted` mean the shipped body executed. An executed body
that also ran patched (mutant) bytes outside a stub is listed in `mutated`.
Stubs planted outside the image never match a catalogue entry; they are counted
only as non-image blocks. Dumped as JSON to $EXECCOV_OUT.

v2 (2026-10-03, SWE2-ORACLE): v1 had no patch or redirect detection - entry-
patched and hook-scripted bodies were recorded `returned` (commit-callees-exec
00512F30/0033C9B0; auto-status-gates-exec 0031B860/0030E130/0030E360/002FEF30/
0030E060), because every redirect left the shadow stack one frame deep.
"""
import atexit, bisect, gc, hashlib, json, os, struct, sys, weakref

_here = os.path.dirname(os.path.abspath(__file__))
_shim_dir = os.path.dirname(_here)

_saved = sys.modules.pop("unicorn", None)
_saved_path = list(sys.path)
try:
    sys.path = [p for p in sys.path if os.path.abspath(p or ".") != _shim_dir]
    import unicorn as _real
finally:
    sys.path = _saved_path
sys.modules["unicorn"] = _saved if _saved is not None else sys.modules.pop("unicorn")

globals().update({k: getattr(_real, k) for k in dir(_real) if not k.startswith("_")})
__version__ = getattr(_real, "__version__", None)
__path__ = list(_real.__path__)
__all__ = [k for k in globals() if not k.startswith("_")]

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

COV_OUT = os.environ.get("EXECCOV_OUT")
SCRIPTS = os.path.dirname(_shim_dir)
ROOT = os.path.abspath(os.path.join(SCRIPTS, "..", "..", "..", ".."))
CAT = os.environ.get("EXECCOV_FUNCTIONS", os.path.join(
    ROOT, "Database", "Tools", "work", "graph", "functions.tsv"))
EXE = os.environ.get("EXECCOV_EXE", os.path.join(
    "D:\\SteamLibrary\\steamapps\\common\\FINAL FANTASY XII THE ZODIAC AGE",
    "x64", "FFXII_TZA.exe"))

_entries = []      # sorted catalogue entry addresses
_bodies = []       # (entry, entry+body_bytes) parallel to _entries
_pe = []           # [(va0, va1, file_offset, raw_size)]
_md = Cs(CS_ARCH_X86, CS_MODE_64)
_md.detail = False


def _load_catalogue(path):
    lines = open(path, encoding="utf8").read().splitlines()
    for ln in lines[1:]:
        f = ln.split("\t")
        try:
            e, b = int(f[0], 16), int(f[2])
        except (ValueError, IndexError):
            continue
        _entries.append(e)
        _bodies.append((e, e + b))
    _entries.sort()
    _bodies.sort(key=lambda t: t[0])


IMAGEBASE = int(os.environ.get("EXECCOV_IMAGEBASE", "0x120000"), 0)


def _load_pe(path):
    d = open(path, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = pe + 0x18
    # SizeOfOptionalHeader is FileHeader+0x10 = pe+0x14. v1 read opt+0x14,
    # parsed a garbage section table and made [_img_lo, _img_hi) span
    # 0x120000..0x18C21471B, so blocks_outside_image was always 0.
    sec = opt + struct.unpack_from("<H", d, pe + 0x14)[0]
    for i in range(nsec):
        vs, va, rs, ro = struct.unpack_from("<IIII", d, sec + i * 40 + 8)
        span = max(vs, rs)
        if span:
            va0 = IMAGEBASE + va
            _pe.append((va0, va0 + span, ro, rs))
    return d


def _file_bytes(a, n):
    """shipped bytes at a (raw-backed part only; None outside the image)."""
    for va0, va1, ro, rs in _pe:
        if va0 <= a < va1:
            k = a - va0
            if k >= rs:
                return None
            return _IMG[ro + k:ro + min(k + n, rs)]
    return None


def _entry_of(a):
    """a is exactly a catalogue entry."""
    i = bisect.bisect_right(_entries, a) - 1
    return _entries[i] if i >= 0 and _entries[i] == a else None


def _body_of(a):
    """innermost catalogue body containing a (smallest containing span)."""
    i = bisect.bisect_right(_entries, a) - 1
    hit = None
    while i >= 0 and _entries[i] <= a:
        e, end = _bodies[i]
        if end > a:
            if hit is None or end - e < _bodies[hit][1] - _bodies[hit][0]:
                hit = i
        elif e <= a - 0x80000:
            break
        i -= 1
    return _entries[hit] if hit is not None else None


_RETS = ("ret", "retf")
EXECUTED = ("returned", "faulted", "returned+faulted")
_img_lo = _img_hi = 0


class _Cov(object):
    """One Uc's coverage state; classification sets are shared via _STATE."""

    def __init__(self, uc):
        self.uc_ref = weakref.ref(uc)
        self.stack = []
        self.pending_call = None
        self.first_block = True
        self.term = {}          # block start -> 'call' | 'ret' | 'jmp' | None
        self.pcache = {}        # (start, size) -> guest bytes differ from shipped
        self.prev = None        # (start, size, terminator) of the last block

    def _read(self, a, n):
        # guest memory, not the file image: harnesses patch code bytes for
        # mutant cases, and planted/stub regions live outside the image.
        uc = self.uc_ref()
        try:
            return bytes(uc.mem_read(a, n)) if uc is not None else b""
        except Exception:
            return b""

    def _termof(self, a, n):
        t = self.term.get(a, False)
        if t is not False:
            return t
        t = None
        for i in _md.disasm(self._read(a, n), a):
            # last token: capstone keeps prefixes in the mnemonic
            # ("bnd ret", "bnd jne", "notrack jmp"); v1 missed every bnd ret
            t = i.mnemonic.split()[-1]
        self.term[a] = t
        return t

    def _patched(self, a, n):
        k = (a, n)
        v = self.pcache.get(k)
        if v is None:
            v = False
            if _img_lo <= a < _img_hi:
                fb = _file_bytes(a, n)
                if fb:
                    v = self._read(a, len(fb)) != fb
            self.pcache[k] = v
        return v

    def on_block(self, uc, a, n, user):
        s = _STATE
        t = self._termof(a, n)
        p = self._patched(a, n)
        pv = self.prev
        self.prev = (a, n, t)
        # A frame's return address reached without a ret: the harness skipped
        # the callee (UC_HOOK_CODE wrote RIP). Pop the skipped frames so the
        # shadow stack stays aligned; the skipped entry is scripted.
        if pv is not None and pv[2] not in _RETS and self.stack:
            idx = None
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][1] == a:
                    idx = i
                    break
            if idx is not None:
                pe = _entry_of(pv[0])
                if pe is not None:
                    s.scripted.add(pe)
                del self.stack[idx:]
                self.pending_call = None
        if self.first_block:
            self.first_block = False
            self.stack.append((_entry_of(a), None))
        elif self.pending_call is not None:
            self.stack.append((_entry_of(a), self.pending_call))
            self.pending_call = None
        s.blocks.add((a, n))
        e = _entry_of(a)
        stub = p and e is not None and t in _RETS and n <= 16
        if p:
            s.patched_blocks.add((a, n))
            if stub:
                s.stubbed.add(e)
            else:
                b = _body_of(a)
                if b is not None:
                    s.mutated.add(b)
        if t == "call":
            self.pending_call = a + n
        elif t in _RETS:
            if self.stack:
                ent, _ra = self.stack.pop()
                if ent is not None and not (stub and ent == e):
                    s.returned.add(ent)
            if not stub:
                b = _body_of(a)
                if b is not None:
                    s.returned.add(b)
                else:
                    s.nonimage_rets += 1
        if e is not None and not stub:
            s.entered.add(e)

    def flush_open(self, faulted):
        s = _STATE
        for ent, _ra in self.stack:
            if ent is not None:
                s.open_entries.add(ent)
                if faulted:
                    s.faulted.add(ent)
        self.stack = []
        self.first_block = True


class _State(object):
    def __init__(self):
        self.blocks = set()         # unique (addr, size) executed blocks
        self.entered = set()
        self.body_only = set()
        self.returned = set()
        self.faulted = set()
        self.open_entries = set()
        self.stubbed = set()
        self.scripted = set()
        self.mutated = set()
        self.patched_blocks = set()
        self.fault_rips = []
        self.nonimage_rets = 0
        self.runs = 0

    def final(self):
        non_img = sum(1 for a, n in self.blocks if not (_img_lo <= a < _img_hi))
        for a, n in self.blocks:
            if not (_img_lo <= a < _img_hi) or (a, n) in self.patched_blocks:
                continue
            b = _body_of(a)
            if b is not None and b not in self.entered:
                self.body_only.add(b)
        for r in self.fault_rips:
            b = _body_of(r)
            if b is not None:
                self.faulted.add(b)
        self.open_entries -= self.faulted
        self.body_only -= self.entered
        out = {}
        for e in sorted(self.entered | self.body_only | self.stubbed
                        | self.scripted):
            if e in self.faulted and e in self.returned:
                cls = "returned+faulted"
            elif e in self.faulted:
                cls = "faulted"
            elif e in self.returned:
                cls = "returned"
            elif e in self.stubbed and e not in self.entered:
                cls = "stubbed"
            elif e in self.scripted:
                cls = "scripted"
            elif e in self.open_entries:
                cls = "open"
            elif e in self.entered:
                cls = "entered"
            else:
                cls = "body_only"
            out["%08x" % e] = cls
        rec = {
            "instrument": "execcov-shim v2",
            "catalogue": _cat_sha,
            "exe_sha256": _exe_sha,
            "emu_starts": self.runs,
            "unique_blocks": len(self.blocks),
            "blocks_in_image": len(self.blocks) - non_img,
            "blocks_outside_image": non_img,
            "entries_executed": len(self.entered),
            "entries": out,
            "mutated": ["%08x" % e for e in sorted(self.mutated)
                        if out.get("%08x" % e) in EXECUTED],
            "patched_blocks": len(self.patched_blocks),
        }
        if COV_OUT:
            with open(COV_OUT, "w") as f:
                json.dump(rec, f, indent=1, sort_keys=True)


_STATE = _State()

_Uc = _real.Uc


class Uc(_Uc):
    """Factory wrapper: __new__ returns a real (arch-dispatched) Uc whose
    emu_start is instrumented at the instance level. Real Uc.__new__ returns
    an arch subclass (e.g. UcIntel), so subclass init never runs — instrument
    inside __new__ instead."""

    def __new__(cls, *a, **kw):
        uc = _Uc.__new__(_Uc, *a, **kw)
        _Uc.__init__(uc, *a, **kw)
        if COV_OUT:
            cov = _Cov(uc)
            uc.hook_add(_real.UC_HOOK_BLOCK, cov.on_block)
            # Weak refs only: a uc -> wrapped -> orig -> uc cycle would keep
            # every case's engine (and its image-sized guest buffers) alive
            # until cyclic GC, which OOMs suites that build hundreds of Ucs.
            start_ref = weakref.WeakMethod(uc.emu_start)
            cov_ref = weakref.ref(cov)
            uc_ref = weakref.ref(uc)

            def wrapped(begin, until, timeout=0, count=0):
                if _STATE.runs % 25 == 24:
                    gc.collect()
                _STATE.runs += 1
                orig = start_ref()
                try:
                    r = orig(begin, until, timeout, count)
                except Exception:
                    cov_ref().flush_open(True)
                    try:
                        _STATE.fault_rips.append(
                            uc_ref().reg_read(_real.UC_X86_REG_RIP))
                    except Exception:
                        pass
                    raise
                cov_ref().flush_open(False)
                return r

            uc.emu_start = wrapped
            uc._execcov = cov
        return uc


_IMG = b""
_cat_sha = _exe_sha = None
if COV_OUT:
    _load_catalogue(os.path.abspath(CAT))
    _IMG = _load_pe(os.path.abspath(EXE))
    _img_lo = min(t[0] for t in _pe)
    _img_hi = max(t[1] for t in _pe)
    _cat_sha = hashlib.md5(open(os.path.abspath(CAT), "rb").read()).hexdigest()
    _exe_sha = hashlib.sha256(_IMG).hexdigest()
    atexit.register(_STATE.final)
