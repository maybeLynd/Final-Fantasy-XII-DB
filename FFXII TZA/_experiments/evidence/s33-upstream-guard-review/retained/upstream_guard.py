"""upstream_guard.py - refuse a downstream replay unless the upstream check it imports actually passed
(OPUS, 2026-10-01, on ASTRA-REQ-OPUS-S33-UPSTREAM-VERDICT-GUARD-1001).

check.py imports block 332's check (s21-opus-replay-applier-stub-free) under redirect_stdout and then used its
world (C.W, C.uc, C.S) without looking at its verdict, so an upstream that printed FAIL still let this replay
report PASS. verdict(mod) is the one gate: the upstream must expose allok exactly True and a non-empty results
dict whose every entry is a dict with pass_ exactly True. Anything else - False, missing, malformed, empty - is a
refusal with its reason. The import itself is wrapped by the caller; an exception there is also a refusal.
"""


def verdict(mod):
    """(True, "") when the imported upstream passed, else (False, why)."""
    allok = getattr(mod, "allok", None)
    results = getattr(mod, "results", None)
    if allok is not True:
        return False, "upstream allok is %r, not True" % (allok,)
    if not isinstance(results, dict) or not results:
        return False, "upstream results missing or empty (%s)" % type(results).__name__
    bad = sorted(k for k, v in results.items() if not (isinstance(v, dict) and v.get("pass_") is True))
    if bad:
        return False, "upstream case(s) not passing: %s" % ", ".join(bad)
    return True, ""
