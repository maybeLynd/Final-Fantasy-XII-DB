"""uc1_band.py — the UC-1 applied B bands, applied to the function population.

2026-09-28 series break, two applications the same day.  FRONTIER's GO
(6ba4b6a91) under FABLE's band ruling §5/§6/§7 admitted
`uc1-applied-population-1-64.tsv`: 694 admit-frontier + 2 split-part = 696
bodies join the measured population AS FRONTIER (never A/B/C by default,
never D); 5 listed extents grow (007C23C0's is the instruction extent — the
native extent runs to 007C2A58); 4 rows are HELD (declared uncertainty —
reported every run, never counted, never dropped); 1 listed row (`007EE7F0`,
adjudicated a false entry) is removed.  OPUS's follow-up
(`uc1-applied-population-65-256.tsv`, OPUS-UC1-POPULATION-CHANGE under
FRONTIER GO d50e87938) admits 99 more frontier bodies in the 65-256 band and
holds 21 more rows.  Three admitted rows carry tail transfers in their note
column (`002E4C90→004232D0`, `002E5B00→002ED6A0`, `00708270→0071BB70`).

Population: **34,269 listed + 795 frontier = 35,064** (before the 65-256
application: 34,965).  Figures dated before 2026-09-28 keep the 34,270
population identity — they are a different series, annotated, not restated.

`apply(sizes)` is the single switch every population reader shares.  Band
rows carry no name/tags, so a reader that needs function-list metadata
synthesizes it via `meta_rows()`.
"""
import io

HERE = os.path.dirname(os.path.abspath(__file__))
_UC1_DIR = os.path.join(HERE, "..", "..", "..", "FFXII TZA",
                        "99-Unresolved-Residual", "Unlisted-Code")
BAND_TSVS = (os.path.join(_UC1_DIR, "uc1-applied-population-1-64.tsv"),
             os.path.join(_UC1_DIR, "uc1-applied-population-65-256.tsv"))
BAND_TSV = BAND_TSVS[0]
SERIES_BREAK = "2026-09-28"


def _parse(path):
    band = {"frontier": {}, "held": [], "extend": {}, "removed": set()}
    with open(path, encoding="utf-8", errors="replace") as f:
        head = f.readline().rstrip("\n").split("\t")
        while head and head[0].startswith("#"):          # comment preamble
            head = f.readline().rstrip("\n").split("\t")
        ik, is_, ie = head.index("kind"), head.index("start"), head.index("end")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) <= max(ik, is_, ie) or p[ik].startswith("#"):
                continue
            kind = p[ik]
            try:
                st, en = int(p[is_], 16), int(p[ie], 16)
            except ValueError:
                continue
            if kind in ("admit-frontier", "split-part"):
                band["frontier"][st] = en - st
            elif kind == "held":
                band["held"].append((st, en))
            elif kind == "extend-listed":
                band["extend"][st] = en
            elif kind == "remove-listed":
                band["removed"].add(st)
    return band


def load(path=None):
    """Parse the applied-band TSVs.  Returns a dict:

      frontier : {start: size}   the 795 new bodies (admit-frontier + split-part)
      held     : [(start, end)]  declared uncertainty — never in the population
      extend   : {entry: end}    listed bodies whose instruction extent grows
      removed  : {entry}         listed bodies adjudicated false
    """
    if path is not None:
        return _parse(path)
    band = {"frontier": {}, "held": [], "extend": {}, "removed": set()}
    for p in BAND_TSVS:
        part = _parse(p)
        for st in part["frontier"]:
            if st in band["frontier"]:
                raise ValueError("UC-1 band frontier %08X admitted twice" % st)
            band["frontier"][st] = part["frontier"][st]
        band["held"] += part["held"]
        for e, en in part["extend"].items():
            if e in band["extend"] and band["extend"][e] != en:
                raise ValueError("UC-1 band extends %08X inconsistently" % e)
            band["extend"][e] = en
        band["removed"] |= part["removed"]
    return band


def apply(sizes, band=None):
    """The coordinated switch: 34,270 -> 34,269 listed + 795 frontier = 35,064.

    `sizes` is the {entry: body_bytes} map a reader built from functions.tsv.
    Returns (new_sizes, info).  Fails LOUD on a band row that disagrees with
    the list it patches — a stale band TSV is corruption, not a variant.
    """
    band = band or load()
    sizes = dict(sizes)
    info = {"listed_before": len(sizes)}
    for e in band["removed"]:
        if e not in sizes:
            raise ValueError("UC-1 band removes %08X, which the loaded "
                             "population does not contain" % e)
        del sizes[e]
    for e, en in band["extend"].items():
        if e not in sizes:
            raise ValueError("UC-1 band extends %08X, absent from the loaded "
                             "population" % e)
        sizes[e] = en - e
    for st in band["frontier"]:
        if st in sizes:
            raise ValueError("UC-1 band frontier %08X collides with a listed "
                             "entry" % st)
        sizes[st] = band["frontier"][st]
    info.update({"listed": info["listed_before"] - len(band["removed"]),
                 "frontier": len(band["frontier"]), "held": len(band["held"]),
                 "extended": len(band["extend"]),
                 "removed": len(band["removed"]),
                 "total": len(sizes)})
    return sizes, info


def maybe_apply(sizes, path, default_path, band=None):
    """apply() iff `path` IS the shared census (`default_path`).

    The band is a property of the shipped functions.tsv, not of a map shape.
    Every own-loader applies it through here so a fixture path loads exactly
    what it names - this is the same guard check_dispositions.load_functions
    uses.
    """
    if os.path.realpath(path) == os.path.realpath(default_path):
        sizes, _ = apply(sizes, band)
    return sizes


def frontier_starts():
    """Set of UC-1 frontier body entries — never A/B/C by default, never D."""
    return set(load()["frontier"])


def held():
    """The held rows — declared uncertainty, reported every run, never counted.
    25 rows: 4 from the 1-64 band + 21 from the 65-256 band."""
    return list(load()["held"])


def meta_rows(band=None):
    """{start: (size, name, is_thunk)} for the frontier bodies, for readers
    that keep a metadata table beside `sizes` (check_frontier_shape)."""
    band = band or load()
    return {st: (sz, "UC1-FRONTIER-%08X" % st, False)
            for st, sz in band["frontier"].items()}


def describe(info):
    return ("%d listed + %d frontier = %d (series break %s; %d held, "
            "%d extended, %d removed)"
            % (info["listed"], info["frontier"], info["total"],
               SERIES_BREAK, info["held"], info["extended"], info["removed"]))
