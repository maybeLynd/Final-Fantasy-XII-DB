"""FCP section 3, parsed the way the attach routine 0041EDE0 reads it, over every @FCP block in the extract.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract).
Layout read from code (0041EDE0, mode 0; slot index s, section base S = payload + u16[payload + 6]):
    S + 0x000 + 2*s    u16     bone id for slot s, 0xFFFF = slot unused          (0041EF22)
    S + 0x040 + 12*s   f32[3]  offset for slot s                                 (0041EF99 / 0041EFC0 / 0041EFE7)
    S + 0x1C0 + 4*s    f32     uniform scale for slot s                          (0041EED0)
    S + 0x240 + 12*s   f32[3]  rotation for slot s                               (0041EF55 / 0041EF5F / 0041EF69)
The four arrays abut exactly if there are 32 slots: 0x40 / 2 = 32, (0x1C0 - 0x40) / 12 = 32, (0x240 - 0x1C0) / 4 = 32,
and a fourth array of 32 x 12 ends at 0x3C0.  THAT IS A PREDICTION, not something the code states - tested here:
  P1  every section 3 has at least 0x3C0 bytes before the next section or the end of the payload
  P2  bone words are 0xFFFF or small; the floats of USED slots are finite, scales positive
  P3  the floats of UNUSED slots are defaults (scale 1.0 or 0, offsets 0) - i.e. the arrays really are slot-parallel
Control: the FCP page found 1,066 @FCP blocks with payload version byte +0x32 = 0x0A in all of them.
Section 8 (added the same day): 003E6D10 returns u16[section8] x 0x1D0 + 0x10 as a byte size, so
  P4  every section 8 is exactly 0x10 + n x 0x1D0 bytes long, n being its first word
Section 4 (added the same day): 003E6770 reads a u32 count, caps it at 4, and walks 0x50-byte descriptors from +0x10, so
  P5  every section 4 is exactly 0x10 + n x 0x50 bytes long with n <= 4
FABLE, 2026-09-19.
"""
import os, struct, glob, math, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
files = glob.glob(os.path.join(ROOT, "**", "*.cm"), recursive=True)
blocks = 0; ver_ok = 0; have3 = 0
p1_ok = p1_bad = 0; gaps = collections.Counter()
used_slots = collections.Counter(); bone_max = 0
bad_float = 0; scale_used = collections.Counter(); unused_scale = collections.Counter(); unused_off_nonzero = 0
used_per_block = collections.Counter()
s8 = collections.Counter(); s8n = collections.Counter()
s4 = collections.Counter(); s4n = collections.Counter(); s4dir = collections.Counter()
for path in files:
    d = open(path, "rb").read()
    i = d.find(b"@FCP")
    if i < 0:
        continue
    size = struct.unpack_from("<I", d, i + 8)[0]
    pay = d[i + 0x30: i + size]
    if len(pay) < 0x40:
        continue
    blocks += 1
    ver_ok += (pay[0x32] == 0x0A)
    offs = struct.unpack_from("<18H", pay, 0)          # sectionOffset[0..17]
    o8 = offs[8]
    if o8:
        later8 = sorted(o for k, o in enumerate(list(offs) + [struct.unpack_from('<H', pay, 0x24)[0]]) if k not in (0, 8) and o > o8)
        end8 = later8[0] if later8 else len(pay)
        n8 = struct.unpack_from('<H', pay, o8)[0]
        s8n[n8] += 1
        s8['exact' if end8 - o8 == 0x10 + n8 * 0x1D0 else 'differs'] += 1
    o4 = offs[4]
    if o4:
        later4 = sorted(o for k, o in enumerate(list(offs) + [struct.unpack_from('<H', pay, 0x24)[0]]) if k not in (0, 4) and o > o4)
        end4 = later4[0] if later4 else len(pay)
        n4 = struct.unpack_from('<I', pay, o4)[0]
        s4n[n4] += 1
        s4['exact' if (end4 - o4 == 0x10 + n4 * 0x50 and n4 <= 4) else 'differs'] += 1
        s4dir[os.path.relpath(path, ROOT).replace(os.sep, '/').split('/')[3]] += 1
    o3 = offs[3]
    if not o3:
        continue
    have3 += 1
    later = sorted(o for k, o in enumerate(offs) if k not in (0, 3) and o > o3)
    more = struct.unpack_from("<H", pay, 0x24)[0]      # sectionOffset[18] is a real section start too
    if more > o3:
        later.append(more)
    end = min(later) if later else len(pay)
    gap = end - o3
    gaps[gap] += 1
    if gap >= 0x3C0 and o3 + 0x3C0 <= len(pay):
        p1_ok += 1
    else:
        p1_bad += 1
        continue
    S = o3
    bones = struct.unpack_from("<32H", pay, S)
    n_used = 0
    for s, b in enumerate(bones):
        off = struct.unpack_from("<3f", pay, S + 0x40 + 12 * s)
        sc = struct.unpack_from("<f", pay, S + 0x1C0 + 4 * s)[0]
        rot = struct.unpack_from("<3f", pay, S + 0x240 + 12 * s)
        if b != 0xFFFF:
            n_used += 1
            used_slots[s] += 1
            bone_max = max(bone_max, b)
            if not all(math.isfinite(v) and abs(v) < 1e4 for v in off + rot + (sc,)) or sc <= 0:
                bad_float += 1
            scale_used[round(sc, 3)] += 1
        else:
            unused_scale[round(sc, 3)] += 1
            unused_off_nonzero += any(abs(v) > 1e-6 for v in off)
    used_per_block[n_used] += 1

print("control: .cm files with an @FCP block:", blocks, "(published 1,066); version byte 0x0A in", ver_ok)
print("blocks with a section 3:", have3)
print("P1  section 3 has >= 0x3C0 bytes before the next section:", p1_ok, "pass,", p1_bad, "fail")
print("    gap to the next section (bytes -> blocks):", sorted(gaps.items(), key=lambda kv: -kv[1])[:6])
print("P2  largest bone id in a used slot:", bone_max, "; used slots with a non-finite float or a scale <= 0:", bad_float)
print("    scale of USED slots (value -> count):", sorted(scale_used.items(), key=lambda kv: -kv[1])[:8])
print("P3  scale of UNUSED slots:", sorted(unused_scale.items(), key=lambda kv: -kv[1])[:5], "; unused slots with a non-zero offset:", unused_off_nonzero)
print("slots used per block (count -> blocks):", sorted(used_per_block.items()))
print("which slots are used (slot -> blocks):", sorted(used_slots.items()))
print("P4  section 8 present in", sum(s8.values()), "blocks; length == 0x10 + n x 0x1D0:", dict(s8), "; n ->", sorted(s8n.items()))
print("P5  section 4 present in", sum(s4.values()), "blocks; length == 0x10 + n x 0x50 and n <= 4:", dict(s4), "; n ->", sorted(s4n.items()), "; by folder:", sorted(s4dir.items(), key=lambda kv: -kv[1]))
