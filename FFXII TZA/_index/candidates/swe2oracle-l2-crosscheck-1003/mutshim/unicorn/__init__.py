"""Single-byte mutation shim (SWE2-ORACLE, L2 cross-check 2026-10-03).

Loaded in place of `unicorn` by ../sitecustomize.py when XC_MUT is set (the loader is execcov's). It re-exports the
real unicorn and wraps `Uc` so that, at the start of every emu_start, the byte at XC_MUT's site is replaced when the
guest still holds the expected original byte. The suite under test is never edited. It also counts executions of the
instruction at the site (UC_HOOK_CODE, begin=end=site), so a mutation that never ran is reported as NOT-REACHED rather
than as a harness that cannot fail.

XC_MUT = "<site hex>:<patch-byte addr hex>:<orig hex>:<new hex>"   XC_OUT = json path: {applied, mismatched, hits}
"""
import atexit, json, os, sys, weakref

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

_site, _pa, _orig, _new = [int(x, 16) for x in os.environ["XC_MUT"].split(":")]
_STAT = {"applied": 0, "mismatched": 0, "unmapped": 0, "hits": 0}
_Uc = _real.Uc


def _count(uc, a, n, user):
    _STAT["hits"] += 1


class Uc(_Uc):
    def __new__(cls, *a, **kw):
        uc = _Uc.__new__(_Uc, *a, **kw)
        _Uc.__init__(uc, *a, **kw)
        uc.hook_add(_real.UC_HOOK_CODE, _count, begin=_site, end=_site)
        start_ref = weakref.WeakMethod(uc.emu_start)
        uc_ref = weakref.ref(uc)

        def wrapped(begin, until, timeout=0, count=0):
            u = uc_ref()
            try:
                b = bytes(u.mem_read(_pa, 1))[0]
                if b == _orig:
                    u.mem_write(_pa, bytes([_new]))
                    _STAT["applied"] += 1
                elif b != _new:
                    _STAT["mismatched"] += 1
            except Exception:
                _STAT["unmapped"] += 1
            return start_ref()(begin, until, timeout, count)

        uc.emu_start = wrapped
        uc._xc_keep = wrapped
        return uc


def _dump():
    out = os.environ.get("XC_OUT")
    if out:
        with open(out, "w") as f:
            json.dump(_STAT, f)


atexit.register(_dump)
