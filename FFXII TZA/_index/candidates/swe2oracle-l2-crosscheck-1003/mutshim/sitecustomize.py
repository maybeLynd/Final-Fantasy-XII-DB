"""sitecustomize for the SWE2-ORACLE mutation shim (L2 cross-check, copied from execcov/sitecustomize.py).

PYTHONPATH entries are scanned for `sitecustomize` at interpreter start, so a
`check.py` run with PYTHONPATH=<execcov> installs this meta-path finder before
any suite code runs. The finder intercepts the top-level `import unicorn` even
when the suite prepends its own vendored unicorn to sys.path (ASTRA harnesses
do `sys.path.insert(0, work/ASTRA/python-libs)`).

The intercepted module executes execcov/unicorn/__init__.py, whose inner
`import unicorn` bypasses this finder via _loading and then resolves whatever
real unicorn the suite would have used — preserving each harness's intended
engine build. Inert when XC_MUT is unset.
"""
import importlib.abc, importlib.util, os, sys

_here = os.path.dirname(os.path.abspath(__file__))
_shim = os.path.join(_here, "unicorn", "__init__.py")
_loading = [False]


class _UnicornShimFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if (fullname != "unicorn" or path is not None or _loading[0]
                or not os.environ.get("XC_MUT")
                or not os.path.exists(_shim)):
            return None
        # The shim's own inner `import unicorn` sees _loading and falls through
        # to the real package; afterwards sys.modules caches the shim, so this
        # finder is consulted at most once per process.
        _loading[0] = True
        return importlib.util.spec_from_file_location(
            "unicorn", _shim,
            submodule_search_locations=[os.path.dirname(_shim)])


sys.meta_path.insert(0, _UnicornShimFinder())
