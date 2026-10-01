"""Minimal COFF (.obj) reader: sections, symbols, relocations. Also exe loader for FFXII_TZA.exe."""
import struct
from pathlib import Path

EXE = Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe")
BASE = 0x120000


class Exe:
    def __init__(self):
        d = self.d = EXE.read_bytes()
        pe = struct.unpack_from("<I", d, 0x3C)[0]
        n = struct.unpack_from("<H", d, pe + 6)[0]
        opt = struct.unpack_from("<H", d, pe + 20)[0]
        self.secs = []
        for i in range(n):
            o = pe + 24 + opt + i * 40
            name = d[o:o + 8].rstrip(b"\0").decode("latin-1")
            vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
            self.secs.append((name, vs, va, rs, ro))

    def off(self, v):
        for name, vs, va, rs, ro in self.secs:
            if BASE + va <= v < BASE + va + rs:
                return v - BASE - va + ro
        return None

    def read(self, v, n):
        # section-aware; virtual tail past raw size reads as zero
        for name, vs, va, rs, ro in self.secs:
            if BASE + va <= v < BASE + va + max(vs, rs):
                out = bytearray()
                for k in range(n):
                    r = v + k - BASE - va
                    out.append(self.d[ro + r] if r < rs else 0)
                return bytes(out)
        return None

    def sec_of(self, v):
        for name, vs, va, rs, ro in self.secs:
            if BASE + va <= v < BASE + va + max(vs, rs):
                return name
        return None


class Obj:
    def __init__(self, path):
        d = self.d = Path(path).read_bytes()
        self.path = str(path)
        mach, nsec, ts, symptr, nsym, optsz, ch = struct.unpack_from("<HHIIIHH", d, 0)
        self.sections = []
        for i in range(nsec):
            o = 20 + optsz + i * 40
            name = d[o:o + 8].rstrip(b"\0").decode("latin-1")
            vs, va, sz, rawptr, relptr, lnptr, nrel, nln, chars = struct.unpack_from("<IIIIIIHHI", d, o + 8)
            raw = d[rawptr:rawptr + sz] if rawptr else b"\0" * sz
            rels = []
            for r in range(nrel):
                ra, si, ty = struct.unpack_from("<IIH", d, relptr + r * 10)
                rels.append((ra, si, ty))
            self.sections.append(dict(name=name, raw=raw, rels=rels, chars=chars))
        strtab = symptr + nsym * 18
        self.syms = {}
        i = 0
        while i < nsym:
            o = symptr + i * 18
            nm = d[o:o + 8]
            if nm[:4] == b"\0\0\0\0":
                so = struct.unpack_from("<I", nm, 4)[0]
                e = d.index(b"\0", strtab + so)
                name = d[strtab + so:e].decode("latin-1")
            else:
                name = nm.rstrip(b"\0").decode("latin-1")
            val, secn, typ, sc, naux = struct.unpack_from("<IhHBB", d, o + 8)
            self.syms[i] = dict(name=name, value=val, sec=secn, type=typ, sc=sc)
            i += 1 + naux

    def functions(self):
        """(name, section_index, start, end) for external/static labels in code sections."""
        out = []
        for si, s in enumerate(self.sections):
            if not (s["chars"] & 0x20):  # CNT_CODE
                continue
            labs = sorted({(v["value"], v["name"], v["sc"]) for v in self.syms.values()
                           if v["sec"] == si + 1 and v["sc"] in (2, 3, 6) and not v["name"].startswith(".") and v["name"] != s["name"]})
            for k, (val, name, sc) in enumerate(labs):
                end = labs[k + 1][0] if k + 1 < len(labs) else len(s["raw"])
                out.append((name, sc, si, val, end))
        return out
