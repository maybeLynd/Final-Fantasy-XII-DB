"""gen_voice_cue_arg_census.py — voice-verb argument census over shipped event scripts.

SWE2-DATA, for FABLE-REQ-SWE2-DATA-VOICE-CUE-TO-SCRIPT-LINE-MAP.

For every `ps2data/plan_master/us/event/**/<name>.ebp` whose section-0 image
carries the 0x8000000B magic, decode every voice-verb call site and record all
resolved literal arguments plus the joined VSP1 cue counts of the same-named
.vpc pack.

Operand roles are native-proven (wrappers push constants via 00267F90 then
forward to 003581B0 / 00351020; 00267E10 pops; 003E9C10 does the bound check
`[VSP1+4] <= index -> no-op`):

    voiceplay      0x0087 arg0 = cue word (slot<<24 | index)
    voiceplay_b5   0x00B5 arg0 = cue word                    (FIRST arg)
    voiceplay_28b  0x028B arg1 = cue word, arg0 -> record +0x14 annotation
    voiceplay_28c  0x028C arg1 = cue word, arg0 -> +0x14, arg2/arg3 = params
    voiceread      0x0085 arg0 = runtime slot
    voiceread_20a  0x020A arg0 = runtime slot, arg1 = pack selector (always 0)
    voicereadsync  0x0086 arg0 = runtime slot
    voicestop      0x0088 arg0 = runtime slot
    voicedispose   0x008C arg0 = runtime slot
    voicestandby   0x028D arg0 = runtime slot
    voicepan       0x00B1 arg0 = runtime slot, arg1 = pan

The previous census (members/voice-cue-census.tsv) took the LAST argument of
every play verb as the cue index, which is wrong for voiceplay_b5 (arg0) and
voiceplay_28c (arg1).  This file supersedes it for argument semantics.

Columns:
    script, verb, sites, resolved_sites, dynamic_sites,
    cue_slot_bytes, cue_indices_sorted, in_range_n, out_of_range_n,
    out_of_range_values, pack_vsp1_counts, other_arg_values
"""
import collections
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "..", "agent_flow", "tools")))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "25-EBP-Script-Container",
    "Bytecode-And-Opcodes", "members")))

import vbfextract as V  # noqa: E402
import gen_req_channel_census as G  # noqa: E402

VBF = os.environ.get(
    "FFXII_VBF", r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf")
OUT = os.path.join(HERE, "voice-cue-arg-census.tsv")

CALLOPS = (0x58, 0x59, 0x5D, 0x5E)
# verb -> index of the cue-word argument (native-proven)
CUEPOS = {0x0087: 0, 0x00B5: 0, 0x028B: 1, 0x028C: 1}
READ_VERBS = {0x0085, 0x020A, 0x0086, 0x0088, 0x008C, 0x028D, 0x00B1}


def vsp1_counts(pack_bytes):
    out = []
    for i in range(0, 0x40, 4):
        off = struct.unpack_from("<I", pack_bytes, 8 + i)[0]
        if off and off + 8 < len(pack_bytes) \
                and pack_bytes[off:off + 4] == b"VSP1":
            out.append(struct.unpack_from("<I", pack_bytes, off + 4)[0])
    return out


def script_sites(section0):
    diroff = struct.unpack_from("<I", section0, 0x18)[0]
    count = struct.unpack_from("<I", section0, diroff)[0]
    starts = []
    for si in range(count):
        o = diroff + 4 + si * 0x30 + 8
        if o + 4 <= len(section0):
            v = struct.unpack_from("<I", section0, o)[0]
            if v < len(section0):
                starts.append(v)
    bounds = sorted(set(starts) | {diroff, len(section0)})
    for start in sorted(starts):
        end = min((x for x in bounds if x > start), default=len(section0))
        if end <= start:
            continue
        ins, _ = G.decode(section0[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op in CALLOPS and (imm in CUEPOS or imm in READ_VERBS):
                yield start + pc, imm, ins, j


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    verbs = G.load_verbs()

    rows = []
    for ep in sorted(p for p in names
                     if "/us/event/" in p and p.lower().endswith(".ebp")):
        sname = ep.rsplit("/", 1)[-1][:-4]
        try:
            b = V.read_entry(f, names, blocks, ep)
        except Exception:
            continue
        if len(b) < 0x88 or struct.unpack_from("<I", b, 0x80)[0] != 0x8000000B:
            continue
        sec = b[0x80:0x80 + struct.unpack_from("<I", b, 0x84)[0]]
        vp = ep[:-4] + ".vpc"
        counts = vsp1_counts(V.read_entry(f, names, blocks, vp)) \
            if vp in names else []
        slot0 = counts[0] if counts else None

        per_verb = collections.defaultdict(
            lambda: {"sites": 0, "resolved": 0, "dyn": 0,
                     "idx": set(), "slots": set(), "in": 0, "oor": 0,
                     "oorvals": set(), "other": set()})
        reads = set()
        for pc, imm, ins, j in script_sites(sec):
            v = verbs[imm]
            need = v[0] or 0
            args, st = G.resolve_args(ins, j, need, verbs)
            if imm in READ_VERBS:
                vals = [a[1] for a in args if a[1] is not None]
                if vals:
                    reads.add((v[2], tuple(vals)))
                continue
            d = per_verb[v[2]]
            d["sites"] += 1
            if st != "ok" or not args:
                d["dyn"] += 1
                continue
            pos = CUEPOS[imm]
            if pos >= len(args) or args[pos][1] is None:
                d["dyn"] += 1
                continue
            d["resolved"] += 1
            w = args[pos][1]
            d["slots"].add(w >> 24)
            idx = w & 0xFFFFFF
            d["idx"].add(idx)
            for k, a in enumerate(args):
                if k != pos and a[1] is not None:
                    d["other"].add(a[1])
            if slot0 is not None and idx < slot0:
                d["in"] += 1
            else:
                d["oor"] += 1
                d["oorvals"].add(idx)

        for vn, d in sorted(per_verb.items()):
            rows.append("\t".join([
                sname, vn, str(d["sites"]), str(d["resolved"]),
                str(d["dyn"]),
                ",".join(str(x) for x in sorted(d["slots"])) or "-",
                ",".join(str(x) for x in sorted(d["idx"])) or "-",
                str(d["in"]), str(d["oor"]),
                ",".join(str(x) for x in sorted(d["oorvals"])) or "-",
                ",".join(str(x) for x in counts) or "-",
                ",".join(str(x) for x in sorted(d["other"])) or "-",
            ]))
        for rd, vals in sorted(reads):
            rows.append("\t".join([
                sname, rd, "1", "1", "0", "-",
                ",".join(str(x) for x in vals), "0", "0", "-",
                ",".join(str(x) for x in counts) or "-", "-",
            ]))

    hdr = ("script\tverb\tsites\tresolved_sites\tdynamic_sites\t"
           "cue_slot_bytes\tcue_indices\tin_range_n\tout_of_range_n\t"
           "out_of_range_values\tpack_vsp1_counts\tother_arg_values")
    with open(OUT, "w", encoding="utf-8", newline="\n") as o:
        o.write(hdr + "\n" + "\n".join(rows) + "\n")
    print("wrote %s: %d rows" % (OUT, len(rows)))


if __name__ == "__main__":
    main()
