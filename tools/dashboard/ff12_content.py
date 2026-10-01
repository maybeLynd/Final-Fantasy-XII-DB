"""FF12 content catalogue for the dashboard's "Player progression" tab.

Usage:
    python ff12_content.py --out <path.json> [--vbf <archive>] [--catalog <enemy_catalog.json>]
    python ff12_content.py --self-test [--vbf <archive>]

Everything is decoded from the game's own files, read straight out of the installed
FFXII_TZA.vbf (in memory; nothing is written next to the archive or into the repo). Standard
library only, no network.

What comes from where (the format pages under Database/FFXII TZA/02-Resource-And-Asset-Pipeline):
  world.regions    wmap (worldmap/menumap_world.bin) region table, slots 1..11 -> menu_mapname ids
  world.areas      wmap area table (28-byte records 1..38): region byte, link[4], name id;
                   strahl = the area appears in the wmap Strahl table; locations = the sub-location
                   records whose persistence group amap Q maps to this area
  world.locations  the 48 sub-location records (lmap records == cmap directory entries, the
                   menumap_world.h sub-location enumeration); area = amap Q[cmap group]
  world.maps       the hub enemy catalog's zones (areaId = field id). A map is placed on a location
                   only by the engine's own field->sub-location walk (003C0380): map_ref.bin group,
                   the cmap entries of that group, lmap array D (member field -> node field), lmap
                   array A +12 (node field). Its area comes from amap Q[map_ref group]. A map joined
                   to neither goes to world.unplaced_maps. Map codes are never parsed for placement.
  families         battle_pack.bin text banks (blob +0xF8) and the party table (blob +0x44);
                   enemies from the hub enemy catalog.

Bank ids follow battle-text-banks.md section 5.1 (corrected 2026-09-11): bank 11 is the LOOT names
(class 7) and bank 12 the KEY ITEMS (class 13: area maps, area names, objects) -- not "11 key items,
12 locations". Both are emitted: key_items = bank 12, loot = bank 11.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import struct
import sys
import time
import zlib

DEFAULT_VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
DEFAULT_CATALOG = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
    'XIIOnlineHub', 'XIIOnlineHub', 'Assets', 'enemies', 'enemy_catalog.json'))

P_BATTLE = 'ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin'
P_MAPNAME = 'ps2data/image/ff12/test_battle/us/binaryfile/menu_mapname.bin'
P_WMAP = 'ps2data/image/ff12/myoshiok/us/worldmap/menumap_world.bin'
P_AMAP = 'ps2data/image/ff12/myoshiok/us/worldmap/menumap_area.bin'
P_LMAP = 'ps2data/image/ff12/myoshiok/us/worldmap/menumap_location.bin'
P_CMAP = 'ps2data/image/ff12/myoshiok/us/worldmap/menumap_common.bin'
P_WHDR = 'ps2data/image/ff12/myoshiok/us/worldmap/menumap_world.h'
P_MAPREF = 'ps2data/image/ff12/ch/common/map_ref.bin'   # ch and in copies are byte-identical
P_FONT = 'gamedata/d3d11/artdata/font/us/font00.dat'
P_TEXTDIR = 'ps2data/image/ff12/test_battle/us/binaryfile/'

# ---------------------------------------------------------------------------------------------
# VBF reader (copied from agent_flow/tools/vbfextract.py: load_index / read_entry)
# ---------------------------------------------------------------------------------------------
BLOCK = 0x10000


def vbf_load_index(f):
    magic, headerLen = struct.unpack("<4sI", f.read(8))
    if magic != b"SRYK":
        raise ValueError('not a VBF archive (magic %r)' % magic)
    (numFiles,) = struct.unpack("<Q", f.read(8))
    entries_off = 0x10 + numFiles * 16
    f.seek(entries_off)
    raw = f.read(0x20 * numFiles)
    entries = []
    for i in range(numFiles):
        sb, sb2, size, off, noff = struct.unpack_from("<IIQQQ", raw, i * 0x20)
        entries.append((sb, size, off, noff))
    strtab_off = entries_off + 0x20 * numFiles
    f.seek(strtab_off)
    (strLen,) = struct.unpack("<I", f.read(4))
    strtab = f.read(strLen)
    blocklist_off = strtab_off + strLen
    f.seek(blocklist_off)
    bl_raw = f.read(headerLen - blocklist_off)
    blocks = struct.unpack("<%dH" % (len(bl_raw) // 2), bl_raw)
    names = {}
    for sb, size, off, noff in entries:
        end = strtab.index(b"\0", noff)
        names[strtab[noff:end].decode()] = (sb, size, off)
    return names, blocks


def vbf_read_entry(f, names, blocks, path):
    sb, size, off = names[path]
    nblocks = (size + BLOCK - 1) // BLOCK
    out = bytearray()
    pos = off
    for i in range(nblocks):
        csize = blocks[sb + i]
        expected = BLOCK if i < nblocks - 1 else (size - BLOCK * (nblocks - 1))
        if csize == 0:
            csize = BLOCK
        f.seek(pos)
        data = f.read(csize)
        if csize == expected:
            out += data
        else:
            try:
                out += zlib.decompress(data)
            except zlib.error:
                out += data
        pos += csize
    if len(out) != size:
        raise ValueError('%s: decompressed %d bytes, index says %d' % (path, len(out), size))
    return bytes(out)


# ---------------------------------------------------------------------------------------------
# Text decoder (from Database/Tools/work/repos-2d/ff12text.py dec(), with the characters the
# database has since decoded: 0xA0 '&', 0xAA ':' (battle-text-banks.md 2.3), 0xA4 '+', 0xA6 '=',
# 0xAE '(' / 0xAF ')' (the-thirty-two-statuses.md GA-2, which corrects ff12text's '"' reading),
# 0x81 'u-acute' (bank 0 0x10A "Cuchulainn", battle-text-banks.md 5). Every other byte is kept as
# <XX> so nothing is dropped silently; 0x0F inline escapes are kept verbatim.
# ---------------------------------------------------------------------------------------------
_CH = {0x04: ' ', 0x02: '\n', 0xA3: '_', 0xA5: '-', 0xA7: ',', 0xA8: '.', 0xAC: "'",
       0xA0: '&', 0xAA: ':', 0xA4: '+', 0xA6: '=', 0xAE: '(', 0xAF: ')', 0x81: '\u00fa'}


def dec(b):
    """Lossless decode. A 0x0F escape and the three bytes after it are printed as <XX> and never
    read as characters (the map-name escapes are 0F xx 81 yy, e.g. 0F 20 81 94 around Leviathan;
    the amap page's template is 0F 3F 81 80). Longer escapes leave their remaining bytes as <XX>
    too, since those bytes are not in the charset."""
    out = []
    esc = 0
    for c in b:
        if c == 0:
            break
        if esc:
            out.append('<%02X>' % c)
            esc -= 1
        elif c == 0x0F:
            out.append('<0F>')
            esc = 3
        elif c in _CH:
            out.append(_CH[c])
        elif 0x20 <= c <= 0x39:
            out.append(chr(ord('A') + c - 0x20))
        elif 0x3A <= c <= 0x53:
            out.append(chr(ord('a') + c - 0x3A))
        elif 0x85 <= c <= 0x8E:
            out.append(chr(ord('0') + c - 0x85))
        else:
            out.append('<%02X>' % c)
    return ''.join(out)


def u8(b, o):
    return b[o]


def u16(b, o):
    return struct.unpack_from('<H', b, o)[0]


def i16(b, o):
    return struct.unpack_from('<h', b, o)[0]


def u32(b, o):
    return struct.unpack_from('<I', b, o)[0]


# ---------------------------------------------------------------------------------------------
# Decoders
# ---------------------------------------------------------------------------------------------
BANK_EXPECT = [545, 544, 1, 362, 63, 32, 284, 16, 629, 128, 129, 512, 512, 16, 64]


def decode_banks(bp):
    """battle_pack.bin text banks: {bank: [raw bytes per block]}."""
    base = u32(bp, 0xF8)
    cnt = u16(bp, base)
    banks = []
    for bi in range(cnt):
        bk = base + u32(bp, base + 4 + 4 * bi)
        bc = u16(bp, bk)
        lst = []
        for i in range(bc):
            s = bk + u32(bp, bk + 4 + 4 * i)
            raw = bp[s:]
            if raw[:2] == b'\0\0':
                raw = raw[2:]
            e = raw.index(b'\0')
            lst.append(raw[:e])
        banks.append(lst)
    return banks


def decode_st2e(b, off):
    if b[off:off + 4] != b'st2e':
        raise ValueError('no st2e at %#x' % off)
    return dict(count=u32(b, off + 4), rec=u32(b, off + 8), hdr=u32(b, off + 0xC))


def decode_party(bp, banks):
    sec = u32(bp, 0x44)
    h = decode_st2e(bp, sec)
    rows = []
    for r in range(h['count']):
        o = sec + h['hdr'] + h['rec'] * r
        ref = u16(bp, o + 0x30)
        bank, idx = ref >> 11, ref & 0x7FF
        raw = banks[bank][idx] if bank < len(banks) and idx < len(banks[bank]) else None
        rows.append(dict(row=r, ref=ref, bank=bank, index=idx, cls=bp[o + 0x2B],
                         raw=raw, name=dec(raw) if raw is not None else None))
    return h, rows


def decode_mapname(d):
    cnt = u32(d, 4)
    hdr = u32(d, 0xC)
    ids = [u32(d, hdr + 4 * i) for i in range(cnt)]
    hb = u32(d, 0x14)
    base = u32(d, hb + 4)
    n2 = u32(d, hb + 12)
    offs = [u32(d, hb + 16 + 4 * i) for i in range(n2 + 1)]
    out = {}
    for i, x in enumerate(ids):
        out[x] = d[hb + base + offs[i]:hb + base + offs[i + 1]].split(b'\0')[0]
    return out


def decode_wmap(d):
    if d[:4] != b'wmap':
        raise ValueError('wmap magic')
    ro, ao, qo, so = u16(d, 8), u16(d, 0xA), u16(d, 0xC), u16(d, 0x10)
    regions = [u32(d, ro + 4 + 4 * i) for i in range(u32(d, ro))]
    areas = []
    for i in range(u32(d, ao)):
        o = ao + 4 + 28 * i
        areas.append(dict(rec=i, links=[x for x in d[o + 4:o + 8]], region=d[o + 10], self=d[o + 11],
                          nameId=u32(d, o + 16), nameId2=u32(d, o + 24)))
    routes = []
    for i in range(u32(d, qo)):
        o = qo + 4 + 8 * i
        routes.append((d[o], d[o + 1], u16(d, o + 2)))
    strahl = []
    for i in range(u32(d, so)):
        o = so + 4 + 4 * i
        strahl.append(dict(pos=u16(d, o), area=d[o + 2]))
    closes = so + 4 + 4 * len(strahl) == len(d)
    return dict(regions=regions, areas=areas, routes=routes, strahl=strahl, closes=closes)


def decode_amap(d):
    if d[:4] != b'amap':
        raise ValueError('amap magic')
    oP, oQ, oR, oS = u16(d, 8), u16(d, 0xA), u16(d, 0xC), u16(d, 0xE)
    P = list(d[oP + 1:oP + 1 + d[oP]])
    Q = list(d[oQ + 1:oQ + 1 + d[oQ]])
    R = [u16(d, oR + 2 + 2 * i) for i in range(u16(d, oR))]
    S = [u32(d, oS + 4 + 4 * i) for i in range(u32(d, oS))]
    closes = oS + 4 + 4 * len(S) == len(d)
    return dict(P=P, Q=Q, R=R, S=S, closes=closes)


def decode_cmap(d):
    if d[:4] != b'cmap':
        raise ValueError('cmap magic')
    o = u16(d, 8)
    ents = []
    for i in range(u32(d, o)):
        e = o + 4 + 8 * i
        ents.append(dict(group=d[e], page=d[e + 1], aux=i16(d, e + 2), nameId=u32(d, e + 4)))
    return ents


def decode_lmap(d):
    """Native layout (lmap page section 10): counts(4) | A 24*nA | B 24*nB | C 20*nC | block 8 | D 4*nD."""
    if d[:4] != b'lmap':
        raise ValueError('lmap magic')
    cnt = d[9]
    offs = [u16(d, 0xA + 2 * i) for i in range(cnt)]
    recs = []
    for i, r in enumerate(offs):
        nA, nB, nC, nD = d[r:r + 4]
        a0 = r + 4
        c0 = a0 + 24 * (nA + nB)
        d0 = c0 + 20 * nC + 8
        end = offs[i + 1] if i + 1 < cnt else len(d)
        A = [u16(d, a0 + 24 * e + 12) for e in range(nA)]
        D = [(u16(d, d0 + 4 * e), u16(d, d0 + 4 * e + 2)) for e in range(nD)]   # (node, member)
        recs.append(dict(A=A, D=D, nB=nB, nC=nC, closes=(d0 + 4 * nD == end)))
    return recs


def decode_mapref(d):
    if d[:4] != b'MRF\x02':
        raise ValueError('map_ref magic')
    base = struct.unpack_from('<i', d, 4)[0]
    n = (len(d) - base) // 8
    return [u16(d, base + 8 * i + 6) for i in range(n)]


def decode_world_h(txt):
    subs = {}
    areas = {}
    for line in txt.splitlines():
        m = re.match(r'#define\s+menumap_sublocation_(\w+?)\s+(\d+)\s*(?://\s*(.*))?$', line.strip())
        if m and not m.group(1).endswith(('MAX', 'ALL')):
            subs[int(m.group(2))] = (m.group(1), (m.group(3) or '').strip())
        m = re.match(r'#define\s+menumap_world_area_(\w+?)\s+(\d+)\s*(?://\s*(.*))?$', line.strip())
        if m and m.group(1) not in ('MAX', 'none'):
            areas[int(m.group(2))] = (m.group(1), (m.group(3) or '').strip())
    return subs, areas


def locate_field(field, mapref, cmap, lmap):
    """003C0380: field id -> sub-location record index, or None."""
    if field >= len(mapref):
        return None
    group = mapref[field]
    for n in range(min(len(cmap), len(lmap))):
        if cmap[n]['group'] != group:
            continue
        node = field
        for nd, mem in lmap[n]['D']:
            if mem == field:
                node = nd
                break
        if node in lmap[n]['A']:
            return n
    return None


# ---------------------------------------------------------------------------------------------
# Authored groups (the Player-progression nesting). Every group comes from a table field whose
# meaning a database page states, or whose label is an authored name bank row; a value whose
# meaning is not documented leaves group None and carries group_raw. [] = the family has no
# category field at all.
# ---------------------------------------------------------------------------------------------
P_ACTION = '07-Combat-Action/Action-Definition-Row/the-action-definition-row.md'
P_IDSPACE = '00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md'
P_EQUIP = '12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md'
P_AUTOSTAT = '08-Combat-Formula/the-auto-status-rebuild.md'
P_LICCHK = '12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md'
P_GAMBIT = '09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md'
P_BANKS = '02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md'

# action row +0x1E values whose meaning a page states (the action row page, section 2.2, and the
# facts it links): 1 magick, 2 technick, 3 item, 255 NOT USED / Reserve rows; 5 = exactly the
# thirteen rows whose +0x26 is an Esper party row; 6 = exactly action ids 0xD0-0xE1, the 18
# Quickenings; 8 = exactly rows 246-261, the trap actions. 5, 6 and 8 are checked by control.
ACTION_KIND = {
    1: ('magick', 'Magicks', P_ACTION + ' 2.2: +0x1E 1 -> +0x22 is a magick id'),
    2: ('technick', 'Technicks', P_ACTION + ' 2.2: +0x1E 2 -> +0x22 is a technick id'),
    3: ('item', 'Items', P_ACTION + ' 2.2: +0x1E 3 -> +0x22 is an item id'),
    5: ('summon', 'Summons', P_ACTION + ' 2.2: +0x1E 5 rows are exactly the 13 rows whose +0x26 is the Esper party row'),
    6: ('quickening', 'Quickenings', P_ACTION + ' 2.2 (+0x28): +0x1E 6 rows are exactly ids 0xD0-0xE1, the 18 Quickenings'),
    8: ('trap', 'Traps', P_ACTION + ' 2.2: +0x1E 8 rows are exactly rows 246-261, the trap actions'),
    255: ('unused', 'Unused / Reserve rows', P_ACTION + ' 2.3: +0x1E 255 = the NOT USED and Reserve rows'),
}

# equipment +0x09 class -> 0031E9F0 runtime category (the FC-4 table, the auto-status page)
EQUIP_RUNTIME = {0: 1, 1: 2, 10: 2, 11: 2, 12: 2, 15: 2, 16: 2, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 13: 3, 14: 3,
                 7: 4, 8: 4, 9: 4, 17: 4, 23: 5, 24: 5, 25: 5, 26: 5, 18: 6, 19: 7, 20: 8, 21: 9, 22: 9}

# licence node byte +5 -> 003241D0 group, and the FC-4 table's words for each (auto-status page)
LIC_GROUP = {1: 0x15, 2: 0x15, 3: 0x15, 4: 0x16, 5: 0x16, 6: 0x16, 7: 0x17, 8: 0x18, 9: 0x19, 10: 0x19,
             11: 0x19, 12: 0x19, 13: 0x19, 14: 0x1A, 15: 0x1B, 16: 0x1B, 17: 0x1B, 18: 0x1C, 19: 0x1D,
             20: 0x1D, 30: 0x1E}
LIC_GROUP_LABEL = {0x15: 'Weapons', 0x16: 'Armour', 0x17: 'Shields', 0x18: 'Accessories', 0x19: 'Magicks',
                   0x1A: 'Technicks', 0x1B: 'Augments', 0x1C: 'Gambit Slots and Essentials',
                   0x1D: 'Quickenings and Espers', 0x1E: 'Second Board'}
LIC_GROUP_NODES = {0x15: 104, 0x16: 39, 0x17: 10, 0x18: 23, 0x19: 42, 0x1A: 24, 0x1B: 76, 0x1C: 11, 0x1D: 31, 0x1E: 1}
LIC_SUB_LABEL = {1: 'Swords, Greatswords, Katana, Spears, Bows, Axes & Hammers', 2: 'Rods, Staves, Maces, Measures',
                 3: 'Daggers, Ninja Swords, Poles, Guns, Crossbows, Hand-bombs', 4: 'Heavy', 5: 'Mystic',
                 6: 'Light', 7: 'Shields', 8: 'Accessories', 9: 'White', 10: 'Black', 11: 'Time',
                 12: 'Mixed tier (White / Green / Black)', 13: 'Mixed tier (Arcane / Black / Time)',
                 14: 'Technicks', 15: 'Single named augments', 16: 'Three-node lores and passives',
                 17: 'Battle Lore, Magick Lore and HP', 18: 'Gambit Slot and Essentials', 19: 'Quickening',
                 20: 'Espers', 30: 'Second Board'}

# gambit condition row +0x10 = the relation mode of BattleTarget_MatchesRelationMode (section 8i)
GAMBIT_MODE = {1: 'Foe', 2: 'Ally', 4: 'Self'}

KEYITEM_SUB = [(0x88, 'maps', 'Area maps'), (0x8C, 'areanames', 'Area names'), (0x90, 'objects', 'Objects')]


def st2e_rows(bp, dirofs):
    sec = u32(bp, dirofs)
    h = decode_st2e(bp, sec)
    base = sec + h['hdr']
    return [bp[base + h['rec'] * r: base + h['rec'] * (r + 1)] for r in range(h['count'])]


def _rows_by_name(rows, off, bank):
    """bank entry index -> [row indices] whose name word at +off names bank:index."""
    out = {}
    for i, r in enumerate(rows):
        w = u16(r, off)
        if w >> 11 == bank:
            out.setdefault(w & 0x7FF, []).append(i)
    return out


def _clean(label):
    return display_of(label) if label is not None else label


def _set(e, group, basis, raw=None):
    e['group'] = group
    e['group_basis'] = basis
    if raw is not None:
        e['group_raw'] = raw


def apply_groups(bp, banks, families, ctl, notes):
    groups = {}

    def bname(bank, i):
        return _clean(dec(banks[bank][i]))

    # ---------------- abilities (bank 0) <- action table +0x3C
    act = st2e_rows(bp, 0x3C)
    schools = [bname(u16(r, 2) >> 11, u16(r, 2) & 0x7FF) for r in st2e_rows(bp, 0x30)]
    cmds = [bname(u16(r, 2) >> 11, u16(r, 2) & 0x7FF) for r in st2e_rows(bp, 0x48)]
    kinds = [r[0x1E] for r in act]
    ctl('group.action.summon', [i for i, k in enumerate(kinds) if k == 5] == [i for i, r in enumerate(act) if r[0x26]],
        'action +0x1E 5 rows = the rows with an Esper party row at +0x26 (%d)' % kinds.count(5))
    ctl('group.action.quickening', [i for i, k in enumerate(kinds) if k == 6] == list(range(0xD0, 0xE2)),
        'action +0x1E 6 rows = ids 0xD0-0xE1, the 18 Quickenings')
    ctl('group.action.trap', [i for i, k in enumerate(kinds) if k == 8] == list(range(246, 262)),
        'action +0x1E 8 rows = rows 246-261, the trap actions')
    nib = {1: 3, 2: 4, 3: 0}
    ctl('group.action.idspace', all(u16(act[i], 0x22) >> 12 == nib[k] for i, k in enumerate(kinds) if k in nib),
        'action +0x1E 1/2/3 rows carry +0x22 ids of nibble 3 (magick) / 4 (technick) / 0 (item)')
    mag = {dec(banks[0][u16(r, 0x34) & 0x7FF]): r[0x2C] & 7 for r in act if r[0x1E] == 1}
    ctl('group.action.school', len(schools) == 5 and schools[mag.get('Cure', 9)] == 'White Magicks'
        and schools[mag.get('Fire', 9)] == 'Black Magicks' and schools[mag.get('Haste', 9)] == 'Time Magicks'
        and all(v < 5 for v in mag.values()),
        'magick school = action +0x2C & 7 into the school table (+0x30): Cure White, Fire Black, Haste Time')
    ctl('group.action.cmdlist', [cmds[k] for k in (1, 2, 3, 5, 6)] == ['Magicks', 'Technicks', 'Items', 'Summon', 'Quickening'],
        'the command list (class 21, +0x48) names rows 1/2/3/5/6 Magicks/Technicks/Items/Summon/Quickening')
    g = groups['abilities'] = {}
    by = _rows_by_name(act, 0x34, 0)
    for e in families['abilities']:
        rows = by.get(e['index'], [])
        e['action_rows'] = rows
        if not rows:
            _set(e, [], 'no action-table row names this bank-0 entry (+0x34)')
            continue
        ks = sorted({act[r][0x1E] for r in rows})
        if len(ks) != 1 or ks[0] not in ACTION_KIND:
            _set(e, None, P_ACTION + ' 2.2: +0x1E value(s) %s not documented' % ks,
                 {'action_kind': ks[0] if len(ks) == 1 else ks})
            continue
        code, label, basis = ACTION_KIND[ks[0]]
        g['kind:' + code] = label
        grp = ['kind:' + code]
        if code == 'magick':
            sc = sorted({act[r][0x2C] & 7 for r in rows})
            if len(sc) == 1 and sc[0] < len(schools):
                g['school:%d' % sc[0]] = schools[sc[0]]
                grp.append('school:%d' % sc[0])
                basis += '; school = +0x2C & 7 into the magick school table (' + P_IDSPACE + ' 2.9, 2.5 class 24)'
        _set(e, grp, basis)
    und = {}
    for k in sorted(set(kinds) - set(ACTION_KIND)):
        und[str(k)] = {'rows': kinds.count(k),
                       'command_list_row_name': cmds[k] if k < len(cmds) else None}
    notes['abilities_undocumented_kinds'] = {
        'what': 'action +0x1E values with no documented meaning; group is null on their entries. The command '
                'list (class 21) row of the same index is shown as an UNVERIFIED lead only: the row index '
                'agrees with every documented kind (1, 2, 3, 5, 6 and 8 = "NOT USED trap"), but no page states '
                'that +0x1E indexes the command list.',
        'values': und}

    # ---------------- equipment (bank 1) <- equipment table +0x38
    eq = st2e_rows(bp, 0x38)
    cats = [bname(u16(r, 2) >> 11, u16(r, 2) & 0x7FF) for r in st2e_rows(bp, 0x18)]
    enames = {bname(1, u16(r, 2) & 0x7FF): r[9] for r in eq if u16(r, 2) >> 11 == 1}
    pairs = [('Broadsword', 'Sword (1H)'), ('Gendarme', 'Shield'), ('Leather Cap', 'Helm'),
             ('Leather Clothing', 'Chest'), ('Opal Ring', 'Accessory'), ('Onion Arrows', 'Arrows')]
    ctl('group.equip.class', all(r[9] <= 26 for r in eq) and all(cats[enames[a]] == b for a, b in pairs if a in enames)
        and all(a in enames for a, _ in pairs),
        'equipment +0x09 is 0-26 on all rows and names the category table (+0x18) row: '
        + ', '.join('%s -> %s' % p for p in pairs))
    g = groups['equipment'] = {}
    rc_members = {}
    for c, rc in EQUIP_RUNTIME.items():
        rc_members.setdefault(rc, []).append(c)
    by = _rows_by_name(eq, 2, 1)
    for e in families['equipment']:
        rows = by.get(e['index'], [])
        e['equipment_rows'] = rows
        if not rows:
            _set(e, [], 'no equipment row names this bank-1 entry (+0x02)')
            continue
        cs = sorted({eq[r][9] for r in rows})
        if len(cs) != 1:
            _set(e, None, 'rows naming this entry disagree on +0x09', {'equipment_class': cs})
            continue
        c = cs[0]
        rc = EQUIP_RUNTIME[c]
        g['rc:%d' % rc] = ' / '.join(cats[m] for m in sorted(rc_members[rc]))
        g['class:%d' % c] = cats[c]
        _set(e, ['rc:%d' % rc, 'class:%d' % c],
             P_EQUIP + ' 11: +0x09 equipment class, named by the category table (' + P_IDSPACE + ' 2.5 class 28); '
             'top = its 0031E9F0 runtime category (' + P_AUTOSTAT + ' FC-4)')

    # ---------------- licences (bank 3) <- licence node table +0x34
    lic = st2e_rows(bp, 0x34)
    b5 = [r[5] for r in lic]
    per_group = {}
    for v in b5:
        per_group[LIC_GROUP.get(v)] = per_group.get(LIC_GROUP.get(v), 0) + 1
    ctl('group.licence.groups', None not in per_group and per_group == LIC_GROUP_NODES,
        'licence node byte +5 folds into the ten 003241D0 groups with the FC-4 node counts %s' %
        {hex(k) if k else k: v for k, v in sorted(per_group.items(), key=lambda x: (x[0] is None, x[0] or 0))})
    ctl('group.licence.qe', b5.count(19) == 18 and b5.count(20) == 13,
        'licence byte +5 19 = 18 nodes (Quickening x18), 20 = 13 nodes (the thirteen espers)')
    eq_by_id = {0x1000 + i: u16(r, 2) for i, r in enumerate(eq)}
    grant_bad = []
    g = groups['licences'] = {}
    by = _rows_by_name(lic, 0, 3)
    for e in families['licences']:
        rows = by.get(e['index'], [])
        e['licence_rows'] = rows
        if not rows:
            _set(e, [], 'no licence node names this bank-3 entry (+0x00)')
            continue
        vs = sorted({lic[r][5] for r in rows})
        grants = []
        for r in rows:
            grp = LIC_GROUP.get(lic[r][5])
            for k in range(8):
                x = u16(lic[r], 8 + 2 * k)
                if x == 0xFFFF:
                    continue
                if x >> 12 == 1 and x in eq_by_id and eq_by_id[x] >> 11 == 1:
                    key = 'equipment:%d' % (eq_by_id[x] & 0x7FF)
                elif grp in (0x1B, 0x1C, 0x1E):
                    key = 'augment:%d' % x
                elif grp in (0x19, 0x1A, 0x1D) and x < len(act):
                    key = 'ability:%d' % (u16(act[x], 0x34) & 0x7FF)
                    want = {0x19: 1, 0x1A: 2, 0x1D: 5}[grp]
                    if act[x][0x1E] != want:
                        grant_bad.append((e['key'], hex(x)))
                else:
                    key = 'raw:0x%04X' % x
                    grant_bad.append((e['key'], hex(x)))
                if key not in grants:
                    grants.append(key)
        e['grants'] = grants
        e['lp'] = [lic[r][4] for r in rows]
        if len(vs) != 1 or vs[0] not in LIC_GROUP:
            _set(e, None, 'licence node byte +5 value(s) %s not in the FC-4 table' % vs, {'node_kind': vs})
            continue
        v = vs[0]
        top = LIC_GROUP[v]
        g['lg:0x%02X' % top] = LIC_GROUP_LABEL[top]
        g['b5:%d' % v] = LIC_SUB_LABEL[v]
        _set(e, ['lg:0x%02X' % top, 'b5:%d' % v],
             'licence node byte +5 -> 003241D0 group (' + P_AUTOSTAT + ' FC-4; ' + P_LICCHK + ' 6)')
    ctl('group.licence.grants', not grant_bad,
        'every licence grant id resolves: 0x1nnn -> an equipment row; groups 0x19/0x1A/0x1D -> an action row of '
        'kind magick/technick/summon; groups 0x1B/0x1C/0x1E -> an augment id (%d unresolved %s)' %
        (len(grant_bad), grant_bad[:3]))

    # ---------------- gambits (bank 6) <- gambit condition table +0x20
    gam = st2e_rows(bp, 0x20)
    agree = sum(1 for r in gam if GAMBIT_MODE.get(r[0x10]) and
                dec(banks[6][u16(r, 0x14) & 0x7FF]).startswith(GAMBIT_MODE[r[0x10]]))
    ctl('group.gambit.mode', all(r[0x10] in GAMBIT_MODE for r in gam) and agree >= len(gam) - 1,
        'gambit row +0x10 is relation mode 1/2/4 on all %d rows and agrees with the name prefix on %d '
        '(the other is a NOT USED row)' % (len(gam), agree))
    g = groups['gambits'] = {}
    by = _rows_by_name(gam, 0x14, 6)
    for e in families['gambits']:
        rows = by.get(e['index'], [])
        e['gambit_rows'] = rows
        if not rows:
            _set(e, [], 'no gambit condition row names this bank-6 entry (+0x14)')
            continue
        ms = sorted({gam[r][0x10] for r in rows})
        if len(ms) != 1 or ms[0] not in GAMBIT_MODE:
            _set(e, None, 'relation mode(s) %s not documented' % ms, {'relation_mode': ms})
            continue
        g['rel:%d' % ms[0]] = GAMBIT_MODE[ms[0]]
        _set(e, ['rel:%d' % ms[0]],
             'gambit condition row +0x10 = the relation mode BattleTarget_MatchesRelationMode tests (' + P_GAMBIT +
             ' 8i / Z-15: 1 Foe, 2 Ally, 4 Self) - the game\'s own target class, not the name prefix')

    # ---------------- key items (bank 12) <- the three class-13 sub-tables
    g = groups['key_items'] = {}
    owner = {}
    for off, code, label in KEYITEM_SUB:
        for r in st2e_rows(bp, off):
            w = u16(r, 8)
            if w >> 11 == 12:
                owner.setdefault(w & 0x7FF, set()).add((code, label))
    for e in families['key_items']:
        o = owner.get(e['index'])
        if not o:
            _set(e, [], 'no key-item sub-table row names this bank-12 entry (+0x08)')
        elif len(o) != 1:
            _set(e, None, 'named by several key-item sub-tables', {'subtables': sorted(c for c, _ in o)})
        else:
            code, label = next(iter(o))
            g['sub:' + code] = label
            _set(e, ['sub:' + code], 'class-13 sub-table (' + P_IDSPACE + ' 2.5: directory +0x88 / +0x8C / +0x90)')
    ctl('group.keyitem.subtables', sum(1 for e in families['key_items'] if e['group']) == 512,
        'every bank-12 entry is named by exactly one key-item sub-table (64 + 32 + 416)')

    # ---------------- bazaar (bank 9): no category field; its documented facts ride along
    baz = st2e_rows(bp, 0xE8)
    items = st2e_rows(bp, 0x4C)
    loot = st2e_rows(bp, 0x84)
    kisub = [st2e_rows(bp, off) for off, _, _ in KEYITEM_SUB]

    def resolve(x):
        """An encoded id -> (family key, name) through its nibble's table (P_IDSPACE 2.1 / 2.5)."""
        n, i = x >> 12, x & 0xFFF
        w, prefix = None, None
        if n == 0 and i < len(items):
            w, prefix = u16(items[i], 8), 'item-action'
        elif n == 1 and i < len(eq):
            w, prefix = u16(eq[i], 2), 'equipment'
        elif n == 2 and i < len(loot):
            w, prefix = u16(loot[i], 6), 'loot'
        elif n == 8:
            for base, t in zip((0, 0x40, 0x60), kisub):
                if base <= i < base + len(t):
                    w, prefix = u16(t[i - base], 8), 'keyitem'
        if w is None:
            return None, None
        key = {'item-action': 'ability', 'equipment': 'equipment', 'loot': 'loot', 'keyitem': 'keyitem'}[prefix]
        return '%s:%d' % (key, w & 0x7FF), _clean(dec(banks[w >> 11][w & 0x7FF]))

    by = _rows_by_name(baz, 0, 9)
    unresolved = 0
    for e in families['bazaar']:
        rows = by.get(e['index'], [])
        _set(e, [], 'the bazaar row (+0xE8, 36 B) has no category field; the-bazaar-recipe-unlock-and-purchase.md')
        if rows:
            r = baz[rows[0]]
            e['repeatable'] = bool(u16(r, 0x14) & 1)
            e['gives'] = []
            for o in (4, 8, 0xC):
                if r[o + 2]:
                    k, n = resolve(u16(r, o))
                    unresolved += k is None
                    e['gives'].append({'id': '0x%04X' % u16(r, o), 'count': r[o + 2], 'key': k, 'name': n})
    ctl('group.bazaar.gives', unresolved == 0,
        'every bazaar grant id resolves through its nibble table (items +0x4C, equipment +0x38, loot +0x84, '
        'key items) to a named family entry (%d unresolved)' % unresolved)
    groups['bazaar'] = {}

    # ---------------- families with no category field
    for fam, why in (('loot', 'the loot row (+0x84, 10 B) has no documented category field'),
                     ('statuses', 'not grouped: bank 5 is in status-id order'),
                     ('commands', 'not grouped'), ('enemy_classes', 'not grouped'), ('genera', 'not grouped')):
        for e in families.get(fam, []):
            _set(e, [], why)
        groups[fam] = {}

    # ---------------- party
    g = groups['party'] = {}
    for e in families['party']:
        g['kind:' + e['kind']] = e['kind'].capitalize()
        _set(e, ['kind:' + e['kind']], 'party_kind_rule (notes): class byte +0x2B and the checked row bands')

    # ---------------- enemies: genus -> bank 14, classification -> bank 13
    b14 = [dec(x) for x in banks[14]]
    b13 = [dec(x) for x in banks[13]]
    ens = families['enemies']
    if ens:
        tests = {}
        for sh in (0, 1, -1):
            hit = tot = 0
            for e in ens:
                if e['name'] in b14:
                    tot += 1
                    v = e.get('genus')
                    hit += v is not None and 0 <= v + sh < len(b14) and b14[v + sh] == e['name']
            tests[sh] = (hit, tot)
        genus_ok = tests[0][1] > 0 and tests[0][0] >= 0.8 * tests[0][1] and max(tests[1][0], tests[-1][0]) <= 0.05 * tests[0][1]
        ctl('group.enemy.genus', genus_ok,
            'catalog genus indexes bank 14: units named like a genus carry its index %d/%d; shifted +1 %d, -1 %d'
            % (tests[0][0], tests[0][1], tests[1][0], tests[-1][0]))
        el = [e for e in ens if e.get('genus') is not None and 0 <= e['genus'] < len(b14) and b14[e['genus']] == 'Elemental']
        cl = {sh: sum(1 for e in el if e.get('classification') is not None and 0 <= e['classification'] + sh < len(b13)
                      and b13[e['classification'] + sh] == 'Elemental') for sh in (0, 1, -1)}
        cls_ok = genus_ok and el and cl[0] == len(el) and cl[1] == cl[-1] == 0
        ctl('group.enemy.class', cls_ok,
            'catalog classification indexes bank 13: the one name both banks carry (Elemental) agrees on %d/%d '
            'genus-Elemental units; shifted +1 %d, -1 %d' % (cl[0], len(el), cl[1], cl[-1]))
        g = groups['enemies'] = {}
        for e in ens:
            gv, cv = e.get('genus'), e.get('classification')
            grp = []
            basis = []
            raw = {}
            if cls_ok and cv is not None and 0 <= cv < len(b13):
                g['class:%d' % cv] = _clean(b13[cv]) or 'class %d (blank name)' % cv
                grp.append('class:%d' % cv)
                basis.append('classification -> bank 13 (control group.enemy.class: one shared-name pair, 55 units)')
            else:
                raw['classification'] = cv
            if genus_ok and gv is not None and 0 <= gv < len(b14):
                e['genus_name'] = _clean(b14[gv])
                g['genus:%d' % gv] = _clean(b14[gv]) or 'genus %d (blank name)' % gv
                grp.append('genus:%d' % gv)
                basis.append('genus -> bank 14 (control group.enemy.genus)')
            else:
                raw['genus'] = gv
            if len(grp) == 2:
                _set(e, grp, '; '.join(basis))
            else:
                _set(e, None, '; '.join(basis) or 'genus / classification outside the banks', raw)
    else:
        groups['enemies'] = {}
    return groups


# ---------------------------------------------------------------------------------------------
# Entry pages: sections / about / dev (the Player-progression reader). Every value comes from a field a
# database page documents; the page is named in dev.basis. Values are in player words and units.
# ---------------------------------------------------------------------------------------------
P_MP = '10-Status-Periodic-Terminal/where-mp-comes-from.md'
P_TARGETS = '07-Combat-Action/how-an-action-gathers-its-targets.md'
P_WEATHER = '08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md'
P_SHOP = '12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md'
P_FILL = ('00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md 4 (the former per-class fill '
          'table, retained in _experiments/evidence/continuation-section05-encoded-query/canonical_changes.diff)')
P_STATSRC = '08-Combat-Formula/where-a-stat-number-comes-from.md (Equipment: five slots)'
P_BAZAAR = '12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md'
P_STATUS = '_types/fields.tsv StatusDefinitionRecord; 10-Status-Periodic-Terminal/the-thirty-two-statuses.md'
P_TEXTGRP = ('text id g*1000+k = row k of text group g (10-Status-Periodic-Terminal/the-thirty-two-statuses.md GE-1; '
             '22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md; group g = the st2e text file '
             'whose ids start at g*10000, 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/'
             'vbf-archive-and-st2e-tables.md 9)')
P_BOARDS = '12-Items-Equipment-Shops-License/license-board-grid-format.md'
P_PARTYSTATS = ('04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md (kind 0: base '
                'stats); 08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md')
P_AUG = P_BANKS + ' 5 (the augment table); 08-Combat-Formula/the-auto-status-rebuild.md (licences, equipment)'
P_CATALOG = 'XIIOnlineHub Assets/enemies/enemy_catalog.json (sources: Vanilla ARD Map.xlsx, enemy-action-groups.csv, ai/*.json)'

AFF_LABEL = [('Weak', 'Weak to'), ('Absorb', 'Absorbs'), ('Half-Damage', 'Takes half damage from'),
             ('Immune', 'Immune to'), ('Potency', 'Strengthens')]
ENEMY_STATS = [('Max HP', 'HP'), ('Max MP', 'MP'), ('Strength', 'Strength'), ('Magick Power', 'Magick Power'),
               ('Vitality', 'Vitality'), ('Speed', 'Speed'), ('Attack Power', 'Attack'), ('Defense', 'Defense'),
               ('Magick Resist', 'Magick Resist'), ('Evade (Parry)', 'Evade (parry)'),
               ('Evade (Weapon)', 'Evade (weapon)'), ('Evade (Shield)', 'Evade (shield)'),
               ('Magick Evade (Shield)', 'Magick evade')]
ENEMY_REWARDS = [('Experience', 'EXP'), ('License Points', 'LP'), ('Clan Points', 'CP'), ('Gil', 'Gil')]
LOOT_SLOTS = [('Guaranteed Drop', 'Drops', 'always'), ('Common Drop', 'Drops', 'common'),
              ('Uncommon Drop', 'Drops', 'uncommon'), ('Rare Drop', 'Drops', 'rare'),
              ('Very Rare Drop', 'Drops', 'very rare'), ('Monograph Drop', 'Drops', 'with a Monograph'),
              ('Canopic Jar Drop', 'Drops', 'with a Canopic Jar'), ('Common Steal', 'Steal', 'common'),
              ('Uncommon Steal', 'Steal', 'uncommon'), ('Rare Steal', 'Steal', 'rare'),
              ('Common Poach', 'Poach', 'common'), ('Uncommon Poach', 'Poach', 'uncommon')]
LOOT_VERB = {'Drops': 'Dropped by', 'Steal': 'Stolen from', 'Poach': 'Poached from'}
REVERSE_CAP = 120


def _e(label, value, link=None):
    if value is None or value == '' or value == []:
        return None
    d = {'label': label, 'value': value}
    if link:
        d['link'] = link
    return d


def _s(title, entries):
    ent = [x for x in entries if x]
    return {'title': title, 'entries': ent} if ent else None


def _capped(label_of, items, what):
    """Reverse-link list, capped; the rest is counted, never dropped silently."""
    out = [label_of(x) for x in items[:REVERSE_CAP]]
    if len(items) > REVERSE_CAP:
        out.append(_e('More', '%d more %s' % (len(items) - REVERSE_CAP, what)))
    return out


def st2e_strings(b):
    """An st2e text file -> the raw string of each record, in record order."""
    cnt = u32(b, 4)
    hb = u32(b, 0x14)
    base = u32(b, hb + 4)
    n2 = u32(b, hb + 12)
    offs = [u32(b, hb + 16 + 4 * i) for i in range(n2 + 1)]
    return [b[hb + base + offs[i]:hb + base + offs[i + 1]].split(b'\0')[0] for i in range(min(cnt, n2))]


def text_groups(text_files):
    groups = {}
    files = {}
    for p, b in text_files.items():
        first = u32(b, u32(b, 0xC))
        if first % 10000 == 0:
            g = first // 10000
            groups[g] = st2e_strings(b)
            files[g] = p.rsplit('/', 1)[1]
    return groups, files


def enrich(bp, banks, families, groups, world, units, zones, ai_dir, action_packages, text_files, boards,
           ctl, notes, sources):
    R = lambda off: st2e_rows(bp, off)
    tg, tg_files = text_groups(text_files)
    ctl('text.groups', tg_files.get(2) == 'menu_message.bin' and tg_files.get(12) == 'listhelp_status.bin'
        and tg_files.get(18) == 'menu_command_template.bin',
        'text group g = the file whose ids start at g*10000 reproduces the three size-matched groups: '
        '2 menu_message, 12 listhelp_status, 18 menu_command_template (%s)' %
        {g: tg_files.get(g) for g in (2, 12, 18)})

    def text(tid):
        if not tid:
            return None
        g, k = divmod(tid, 1000)
        rows = tg.get(g)
        if rows is None or k >= len(rows):
            return None
        s = display_of(dec(rows[k])).replace('\n', ' ').strip()
        return s or None

    def nm(w):
        b, i = w >> 11, w & 0x7FF
        return display_of(dec(banks[b][i])) if b < len(banks) and i < len(banks[b]) else None

    act, eq, lic, gam = R(0x3C), R(0x38), R(0x34), R(0x20)
    items, loot, baz, aug, sts = R(0x4C), R(0x84), R(0xE8), R(0xEC), R(0x40)
    mags, tecs, elems, cmdt = R(0x78), R(0x7C), R(0xA8), R(0x48)
    kisub = [(off, code, R(off)) for off, code, _ in KEYITEM_SUB]
    party_rows = st2e_rows(bp, 0x44)
    el_names = [nm(u16(r, 0)) for r in elems]
    st_names = [e['name'] for e in families['statuses']]

    def act_key(i):
        return 'ability:%d' % (u16(act[i], 0x34) & 0x7FF)

    def eq_key(i):
        return 'equipment:%d' % (u16(eq[i], 2) & 0x7FF)

    def resolve(x):
        n, i = x >> 12, x & 0xFFF
        if n == 0 and i < len(items):
            w = u16(items[i], 8)
            return 'ability:%d' % (w & 0x7FF)
        if n == 1 and i < len(eq):
            return eq_key(i)
        if n == 2 and i < len(loot):
            return 'loot:%d' % (u16(loot[i], 6) & 0x7FF)
        if n == 8:
            for base, (_, _, t) in zip((0, 0x40, 0x60), kisub):
                if base <= i < base + len(t):
                    return 'keyitem:%d' % (u16(t[i - base], 8) & 0x7FF)
        return None

    by_key = {e['key']: e for fam in families.values() for e in fam}

    def title(key):
        e = by_key.get(key)
        return (e.get('display') or e['name']) if e else key

    def link(label, key, value=None):
        return _e(label, value if value is not None else title(key), key)

    # ---- augments family (the licence and equipment grants resolve here)
    seen = {}
    fam_aug = []
    for i, r in enumerate(aug):
        w = u16(r, 2)
        raw = banks[w >> 11][w & 0x7FF] if (w >> 11) < len(banks) and (w & 0x7FF) < len(banks[w >> 11]) else None
        e = text_entry('augment:%d' % i, raw, seen, {'index': i})
        _set(e, [], 'the augment table (+0xEC) has no category field')
        fam_aug.append(e)
    families['augments'] = fam_aug
    groups['augments'] = {}
    for e in fam_aug:
        by_key[e['key']] = e

    # ---- reverse indices
    rev = {}

    def add(key, kind, val):
        rev.setdefault(key, {}).setdefault(kind, []).append(val)

    for e in families['licences']:
        for g in e.get('grants', []):
            add(g, 'licence', e['key'])
    for i, r in enumerate(baz):
        bk = 'bazaar:%d' % (u16(r, 0) & 0x7FF)
        for o in (4, 8, 0xC):
            if r[o + 2]:
                k = resolve(u16(r, o))
                if k:
                    add(k, 'bazaar_gives', (bk, r[o + 2]))
        for o in (0x16, 0x1A, 0x1E):
            if r[o + 2]:
                k = resolve(u16(r, o))
                if k:
                    add(k, 'bazaar_needs', (bk, r[o + 2]))
    for i, r in enumerate(act):
        m = u32(r, 0x18)
        for s in range(32):
            if m >> s & 1:
                add('status:%d' % s, 'actions', act_key(i))
    for i, r in enumerate(eq):
        c = r[9]
        if c <= 26 and EQUIP_RUNTIME[c] >= 7 and r[0x1A] != 0xFF:
            add('augment:%d' % r[0x1A], 'equipment', eq_key(i))
    for i, r in enumerate(party_rows):
        m = u32(r, 0x50) | (u32(r, 0x54) << 32)
        for s in range(64):
            if m >> s & 1:
                add('augment:%d' % s, 'party', 'party:%d' % i)

    # enemy actions (catalog AI scripts: bit 15 = a weighted action package, else a literal action id)
    ai_cache = {}
    enemy_actions = {}
    for e in families['enemies']:
        u = units.get(e['key'][len('enemy:'):]) or {}
        acts = []
        for k in dict.fromkeys(u.get('aiKeys') or []):
            ard = k.split(':')[0]
            if ard not in ai_cache:
                p = os.path.join(ai_dir, ard + '.json')
                try:
                    ai_cache[ard] = json.load(open(p, encoding='utf-8')).get('scripts', {})
                except (OSError, ValueError):
                    ai_cache[ard] = {}
            sc = ai_cache[ard].get(k) or {}
            for grp in (sc.get('groups') or {}).values():
                for ent in grp:
                    aid = ent.get('actionId')
                    if aid is None:
                        continue
                    ids = []
                    if aid & 0x8000:
                        pk = action_packages.get(str(aid - 0x8000)) or {}
                        ids = [a.get('id') for a in pk.get('actions') or []]
                    elif aid < len(act):
                        ids = [aid]
                    for x in ids:
                        if x is not None and x < len(act) and act_key(x) not in acts:
                            acts.append(act_key(x))
        enemy_actions[e['key']] = acts
        for a in acts:
            add(a, 'enemies', e['key'])
        for slot, verb, rate in LOOT_SLOTS:
            it = ((u.get('loot') or {}).get(slot) or {})
            x = it.get('id')
            if x is not None and x != 0xFFFF:
                k = resolve(x)
                if k:
                    add(k, 'loot_' + verb, (e['key'], rate))
    sources['enemy_ai'] = {'path': ai_dir, 'sha256': None, 'size': len(ai_cache),
                           'note': 'the %d AI script files the catalog names were read (not hashed)' % len(ai_cache)}

    def rev_sections(key):
        out = []
        r = rev.get(key, {})
        if r.get('licence'):
            out.append(_s('Learned from licence', [link('Licence', k) for k in r['licence']]))
        if r.get('bazaar_gives'):
            out.append(_s('Sold in the bazaar as', [link('Bazaar good', k, '%s (x%d)' % (title(k), n))
                                                    for k, n in r['bazaar_gives']]))
        if r.get('bazaar_needs'):
            out.append(_s('Used in bazaar goods', [link('Bazaar good', k, '%s (needs %d)' % (title(k), n))
                                                   for k, n in r['bazaar_needs']]))
        for verb in ('Drops', 'Steal', 'Poach'):
            lst = r.get('loot_' + verb)
            if lst:
                out.append(_s(LOOT_VERB[verb], _capped(lambda x: link('Enemy', x[0], '%s (%s)' % (title(x[0]), x[1])),
                                                       lst, 'enemies')))
        return out

    dev_basis = notes.setdefault('dev_basis', {})

    def dev(table, row, fields, undecoded, basis, rawrow=None, rows=None):
        d = {'table': table, 'row': row, 'fields': fields, 'undecoded': undecoded}
        dev_basis.setdefault(table, basis)
        if rawrow is not None:
            d['raw'] = rawrow.hex(' ')
        if rows and len(rows) > 1:
            d['rows'] = rows
        return d

    def finish(e, secs, about=None):
        e['sections'] = [s for s in secs if s]
        if about:
            e['about'] = about

    # ---------------- abilities
    mag_by = {r[2]: r for r in mags}
    tec_by = {r[2]: r for r in tecs}
    for e in families['abilities']:
        rows = e.get('action_rows') or []
        if not rows:
            finish(e, rev_sections(e['key']))
            e['dev'] = dev('battle_pack.bin text bank 0', e['index'], {}, 'no action-table row names this entry',
                           P_BANKS)
            continue
        i = rows[0]
        r = act[i]
        kind = r[0x1E]
        secs = []
        ov = [_e('Type', groups['abilities'].get(e['group'][0]) if e.get('group') else None)]
        if e.get('group') and len(e['group']) > 1:
            ov.append(_e('School', groups['abilities'][e['group'][1]]))
        if kind == 5 and r[0x26]:
            ov.append(link('Summons', 'party:%d' % r[0x26]))
        secs.append(_s('Overview', ov))
        cost = []
        if r[0x0A]:
            cost.append(_e('Mist charges' if kind in (5, 6) else 'MP cost', r[0x0A]))
        shop = None
        if kind == 3:
            x = u16(r, 0x22)
            if x >> 12 == 0 and (x & 0xFFF) < len(items):
                shop = u16(items[x & 0xFFF], 0x0A)
        elif kind == 1 and i in mag_by:
            shop = u16(mag_by[i], 0)
        elif kind == 2 and i in tec_by:
            shop = u16(tec_by[i], 0)
        if shop:
            cost.append(_e('Price', '%d gil' % shop))
            if kind == 3:
                cost.append(_e('Sells for', '%d gil' % (shop // 2)))
        secs.append(_s('Cost', cost))
        eff = [_e('Power', r[0x10] or None)]
        els = [el_names[b] for b in range(8) if r[0x13] >> b & 1 and b < len(el_names)]
        eff.append(_e('Element', ', '.join(els) if els else None))
        if r[0x14]:
            eff.append(_e('Status chance', '%d%%' % r[0x14]))
        secs.append(_s('Effect', eff))
        m = u32(r, 0x18)
        secs.append(_s('Statuses it applies or removes', [link('Status', 'status:%d' % s) for s in range(32) if m >> s & 1]))
        flags = u32(r, 0x0C)
        tgt = []
        if r[6] == 0:
            area = 'whole party' if flags & 2 else 'single target'
        elif flags >> 24 & 1:
            area = 'cone from the user'
        elif flags >> 25 & 1:
            area = 'line from the user'
        elif flags >> 21 & 1:
            area = 'area around the user'
        else:
            area = 'area around the target'
        tgt.append(_e('Area', area))
        if r[6]:
            side = u16(r, 0x36)
            tgt.append(_e('Hits', 'everyone in the area' if side & 8 else
                          ('the side opposite the target' if side & 4 else "everyone on the target's side")))
        if flags >> 26 & 1:
            tgt.append(_e('Reach', "the weapon's reach"))
        elif r[5] and r[5] != 255:
            tgt.append(_e('Reach', '%.1f' % (r[5] / 10.0)))
        secs.append(_s('Targeting', tgt))
        secs += rev_sections(e['key'])
        en = rev.get(e['key'], {}).get('enemies')
        if en:
            secs.append(_s('Used by enemies', _capped(lambda k: link('Enemy', k), en, 'enemies')))
        about = text(u16(r, 0x2E)) or (text(u16(r, 0)) if u16(r, 0) != 4000 else None)
        finish(e, secs, about)
        e['dev'] = dev('battle_pack.bin directory +0x3C (action table, 60 B)', i, {
            '+0x00 helpTextId': u16(r, 0), '+0x05 reach': r[5], '+0x06 radius': r[6], '+0x07 angleOrWidth': r[7],
            '+0x08 recipe': r[8], '+0x09 chargeClass': r[9], '+0x0A mpCostOrCharges': r[0x0A],
            '+0x0C flags': flags, '+0x10 power': r[0x10], '+0x11 power2': r[0x11], '+0x12 hitThreshold': r[0x12],
            '+0x13 elementMask': r[0x13], '+0x14 statusChance': r[0x14], '+0x18 statusMask': m,
            '+0x1E kind': kind, '+0x22 linkedId': u16(r, 0x22), '+0x26 esperRow': r[0x26],
            '+0x2C school/element': r[0x2C] & 7, '+0x2E descriptionId': u16(r, 0x2E), '+0x34 nameWord': u16(r, 0x34),
            '+0x36 side': u16(r, 0x36)},
            'Not shown: +0x09 charge-time class (no seconds conversion is documented); +0x12 hit threshold (no player '
            'unit documented); +0x08 recipe (formula id). Whether +0x18 statuses are added or removed depends on the '
            'recipe, which is not decoded per recipe. Which side the player may pick as the first target is not in '
            'the row. Shape-only bytes: +0x02-+0x04, +0x1C, +0x1D, +0x1F-+0x21, +0x24, +0x28, +0x30, +0x38, +0x3A.',
            '%s 2.2; MP cost: %s; area and side: %s; element bits: %s (0x01 Fire .. 0x20 Wind) and the element '
            'table order for 0x40 / 0x80; prices: %s and %s; texts: %s' % (P_ACTION, P_MP, P_TARGETS, P_WEATHER,
                                                                         P_SHOP, P_FILL, P_TEXTGRP), r, rows)

    # ---------------- equipment
    for e in families['equipment']:
        rows = e.get('equipment_rows') or []
        if not rows:
            finish(e, rev_sections(e['key']))
            e['dev'] = dev('battle_pack.bin text bank 1', e['index'], {}, 'no equipment row names this entry', P_BANKS)
            continue
        i = rows[0]
        r = eq[i]
        c = r[9]
        rc = EQUIP_RUNTIME.get(c)
        kind = None if rc is None else (1 if rc <= 5 else (2 if rc == 6 else 3))
        secs = [_s('Overview', [_e('Category', groups['equipment'].get('class:%d' % c))])]
        st = []
        if kind == 1:
            st += [_e('Attack', r[0x1A]), _e('Evade', r[0x1D])]
        elif kind == 2:
            st += [_e('Evade', r[0x18]), _e('Magick evade', r[0x19])]
        elif kind == 3 and (r[0x18] or r[0x19]):
            st += [_e('Defense', r[0x18]), _e('Magick resist', r[0x19])]
        secs.append(_s('Stats', st))
        if kind == 3 and r[0x1A] != 0xFF:
            secs.append(_s('Effect while equipped', [link('Effect', 'augment:%d' % r[0x1A])]))
        price = u16(r, 0x12)
        secs.append(_s('Shop', [_e('Price', '%d gil' % price if price else None),
                                _e('Sells for', '%d gil' % (price // 2) if price else None)]))
        if r[7] & 0x10:
            secs.append(_s('Licence', [_e('Licence needed', 'no')]))
        secs += rev_sections(e['key'])
        finish(e, secs, text(u16(r, 0x0E)))
        e['dev'] = dev('battle_pack.bin directory +0x38 (equipment table, 52 B)', i, {
            '+0x07 flags': r[7], '+0x09 equipmentClass': c, '+0x0E descriptionId': u16(r, 0x0E),
            '+0x11 secondaryCompatKey': r[0x11], '+0x12 price': price, '+0x18': r[0x18], '+0x19': r[0x19],
            '+0x1A': r[0x1A], '+0x1D': r[0x1D], '+0x28 subRecord': u16(r, 0x28), 'itemKind(0031E9A0)': kind},
            'No description: the description word +0x0E of the row is 0 on every row in this build, and no other '
            'equipment help-text source is located. Not decoded: the +0x28 sub-record (two words, four bytes and five flag fields every item adds - the stat '
            'bonuses, element, on-hit status and immunities are expected there, but no page names its fields); '
            '+0x19 on a weapon is its damage recipe (a formula id, not a player value); combo and critical rates '
            'are not located.',
            '%s (kind 1 weapons: +0x1A attack, +0x1D evade; kind 2 shields: +0x18 evade, +0x19 magick evade; kind 3 '
            'armour: +0x18 defense, +0x19 magick resist); kind from the runtime category (%s FC-4); +0x1A effect: '
            '_types/fields.tsv EquipmentDefinitionRecord; +0x07 bit 0x10 no licence: %s 5b; price +0x12: %s; '
            'description +0x0E: %s; texts: %s' % (P_STATSRC, P_AUTOSTAT, P_LICCHK, P_SHOP, P_FILL, P_TEXTGRP),
            r, rows)

    # ---------------- licences
    board_of = {}
    for n, b in sorted(boards.items()):
        w, h = u16(b, 4), u16(b, 6)
        for c in range(w * h):
            node = u16(b, 8 + 2 * c)
            if node != 0xFFFF:
                board_of.setdefault(node, []).append(n)
    ctl('licence.boards', len(boards) == 12 and max(board_of) == len(lic) - 1 if board_of else False,
        'the 12 job boards read, their node numbers run 0-%d = the licence table rows' %
        (max(board_of) if board_of else -1))
    for e in families['licences']:
        rows = e.get('licence_rows') or []
        if not rows:
            finish(e, rev_sections(e['key']))
            e['dev'] = dev('battle_pack.bin text bank 3', e['index'], {}, 'no licence node names this entry', P_BANKS)
            continue
        r = lic[rows[0]]
        lps = sorted({lic[x][4] for x in rows})
        secs = [_s('Licence', [_e('Group', groups['licences'].get(e['group'][0]) if e.get('group') else None),
                               _e('Kind', groups['licences'].get(e['group'][1]) if e.get('group') else None),
                               _e('LP cost', lps[0] if len(lps) == 1 else '%d-%d' % (lps[0], lps[-1])),
                               _e('Squares', len(rows) if len(rows) > 1 else None)])]
        secs.append(_s('Grants', [link('Grants', k) for k in e.get('grants', [])]))
        bs = sorted({n for x in rows for n in board_of.get(x, [])})
        secs.append(_s('Job boards', [_e('Board', 'Board %d' % n) for n in bs]))
        finish(e, secs, text(u16(r, 2)))
        e['dev'] = dev('battle_pack.bin directory +0x34 (licence nodes, 24 B)', rows[0], {
            '+0x02 descriptionId': u16(r, 2), '+0x04 lp': r[4], '+0x05 nodeKind': r[5],
            '+0x08 grants': [u16(r, 8 + 2 * k) for k in range(8)]},
            'Which job each board_N.bin is is not documented (listed by number); license_board.bin, the 13th board, '
            'is not identified; +0x06 / +0x07 are not documented.',
            'LP +0x04: %s 6 / the query-record page (licence +0x20 <- row+4); node kind +0x05 and grants +0x08: %s 6, '
            '%s FC-4; boards: %s; description +0x02: %s; texts: %s' % (P_LICCHK, P_LICCHK, P_AUTOSTAT, P_BOARDS,
                                                                        P_FILL, P_TEXTGRP), r, rows)

    # ---------------- gambits
    for e in families['gambits']:
        rows = e.get('gambit_rows') or []
        if not rows:
            finish(e, [])
            e['dev'] = dev('battle_pack.bin text bank 6', e['index'], {}, 'no gambit condition row names this entry',
                           P_BANKS)
            continue
        r = gam[rows[0]]
        price = u16(r, 6)
        finish(e, [_s('Gambit', [_e('Targets', groups['gambits'].get(e['group'][0]) if e.get('group') else None),
                                 _e('Price', '%d gil' % price if price else None)])], text(u16(r, 4)))
        e['dev'] = dev('battle_pack.bin directory +0x20 (gambit conditions, 32 B)', rows[0], {
            '+0x04 descriptionId': u16(r, 4), '+0x06 price': price, '+0x08 opcode': u16(r, 8),
            '+0x10 relationMode': r[0x10], '+0x14 nameWord': u16(r, 0x14)},
            'The condition opcode (+0x08/+0x0A/+0x0C) and its parameters (+0x18..+0x1C) are not named per value.',
            'relation mode +0x10: %s 8i; price +0x06 and description +0x04: %s (+0x28 is the price: %s); texts: %s'
            % (P_GAMBIT, P_FILL, P_SHOP, P_TEXTGRP), r, rows)

    # ---------------- statuses
    for i, e in enumerate(families['statuses']):
        r = sts[i]
        clr = u32(r, 0x0C)
        blk = u32(r, 0x20)
        secs = [_s('Duration', [_e('Wears off', 'never' if r[8] == 0xFF else None)]),
                _s('Removes', [link('Status', 'status:%d' % s) for s in range(32) if clr >> s & 1 and s != i]),
                _s('Blocked by', [link('Status', 'status:%d' % s) for s in range(32) if blk >> s & 1])]
        acts = rev.get(e['key'], {}).get('actions') or []
        secs.append(_s('Actions that apply or remove it', _capped(lambda k: link('Action', k), acts, 'actions')))
        finish(e, secs, text(u16(r, 0x0A)))
        e['dev'] = dev('battle_pack.bin directory +0x40 (status table, 40 B)', i, {
            '+0x08 baseDuration': r[8], '+0x09 durationUnit': r[9], '+0x0A descriptionId': u16(r, 0x0A),
            '+0x0C clearMask': clr, '+0x20 blockingMask': blk},
            'The duration is in engine units scaled by Vitality (no seconds conversion documented); the twelve '
            'ranking bytes +0x11..+0x1D are unexplained.', P_STATUS + '; texts: ' + P_TEXTGRP, r)

    # ---------------- loot
    lrow = {u16(r, 6) & 0x7FF: (i, r) for i, r in enumerate(loot) if u16(r, 6) >> 11 == 11}
    for e in families['loot']:
        ir = lrow.get(e['index'])
        if not ir:
            finish(e, rev_sections(e['key']))
            e['dev'] = dev('battle_pack.bin text bank 11', e['index'], {}, 'no loot row names this entry', P_BANKS)
            continue
        i, r = ir
        price = u16(r, 0)
        secs = [_s('Value', [_e('Price', '%d gil' % price if price else None),
                             _e('Sells for', '%d gil' % (price // 2) if price else None)])]
        secs += rev_sections(e['key'])
        finish(e, secs, text(u16(r, 2)))
        e['dev'] = dev('battle_pack.bin directory +0x84 (loot, 10 B)', i, {
            '+0x00 price': price, '+0x02 descriptionId': u16(r, 2), '+0x04': r[4], '+0x06 nameWord': u16(r, 6),
            '+0x08': u16(r, 8)}, '+0x04 and +0x08 are copied into the query record but not named.',
            'price +0x00 (sell list halves it): %s; description +0x02: %s; texts: %s' % (P_SHOP, P_FILL, P_TEXTGRP),
            r)

    # ---------------- bazaar
    brow = {u16(r, 0) & 0x7FF: (i, r) for i, r in enumerate(baz)}
    for e in families['bazaar']:
        i, r = brow.get(e['index'], (None, None))
        if r is None:
            finish(e, [])
            continue
        gives = [link('Gives', resolve(u16(r, o)), '%s (x%d)' % (title(resolve(u16(r, o))), r[o + 2]))
                 for o in (4, 8, 0xC) if r[o + 2] and resolve(u16(r, o))]
        needs = [link('Needs', resolve(u16(r, o)), '%s (x%d)' % (title(resolve(u16(r, o))), r[o + 2]))
                 for o in (0x16, 0x1A, 0x1E) if r[o + 2] and resolve(u16(r, o))]
        fl = u16(r, 0x14)
        finish(e, [_s('Gives', gives), _s('Needs (loot sold)', needs),
                   _s('Purchase', [_e('Price', '%d gil' % u32(r, 0x10)), _e('Repeatable', 'yes' if fl & 1 else 'no'),
                                   _e('Made available by the story', 'yes' if fl & 2 else None)])],
               text(u16(r, 2)))
        e['dev'] = dev('battle_pack.bin directory +0xE8 (bazaar, 36 B)', i, {
            '+0x02 descriptionId': u16(r, 2), '+0x10 price': u32(r, 0x10), '+0x14 flags': fl, '+0x22 icon': u16(r, 0x22)},
            'none beyond the icon frame (+0x22, 120 on every row).', P_BAZAAR + '; texts: ' + P_TEXTGRP, r)

    # ---------------- key items
    krow = {}
    for off, code, t in kisub:
        for i, r in enumerate(t):
            krow.setdefault(u16(r, 8) & 0x7FF, (off, i, r))
    for e in families['key_items']:
        ir = krow.get(e['index'])
        secs = [_s('Kind', [_e('Kind', groups['key_items'].get(e['group'][0]) if e.get('group') else None)])]
        secs += rev_sections(e['key'])
        if not ir:
            finish(e, secs)
            continue
        off, i, r = ir
        finish(e, secs, text(u16(r, 6)))
        e['dev'] = dev('battle_pack.bin directory +0x%02X (key items, 10 B)' % off, i, {
            '+0x02': u16(r, 2), '+0x04': r[4], '+0x06 descriptionId': u16(r, 6), '+0x08 nameWord': u16(r, 8)},
            '+0x02 and +0x04 are copied into the query record but not named.',
            'description +0x06: %s; texts: %s' % (P_FILL, P_TEXTGRP), r)

    # ---------------- augments
    for i, e in enumerate(fam_aug):
        r = aug[i]
        par = u16(r, 4)
        secs = [_s('Effect', [_e('Amount', par if par else None)])]
        rv = rev.get(e['key'], {})
        secs.append(_s('On the License Board as', [link('Licence', k) for k in rv.get('licence', [])]))
        secs.append(_s('Granted by equipment', _capped(lambda k: link('Equipment', k), rv.get('equipment', []), 'items')))
        secs.append(_s('Innate for', [link('Character', k) for k in rv.get('party', [])]))
        finish(e, secs, text(u16(r, 0)))
        e['dev'] = dev('battle_pack.bin directory +0xEC (augments, 8 B)', i, {
            '+0x00 descriptionId': u16(r, 0), '+0x02 nameWord': u16(r, 2), '+0x04 parameter': par, '+0x06': u16(r, 6)},
            '+0x06 is 0xFF on every row; the parameter unit differs per augment (HP, percent, count).',
            P_AUG + '; texts: ' + P_TEXTGRP, r)

    # ---------------- party
    for e in families['party']:
        i = int(e['key'].split(':')[1])
        r = party_rows[i]
        m = u32(r, 0x50) | (u32(r, 0x54) << 32)
        secs = [_s('Base stats', [_e('HP', u16(r, 0x16)), _e('MP', u16(r, 0x1A)), _e('Strength', r[0x1E]),
                                  _e('Magick Power', r[0x21]), _e('Vitality', r[0x24]), _e('Speed', r[0x27]),
                                  _e('Evade', r[0x2A])]),
                _s('Always-on effects', [link('Effect', 'augment:%d' % s) for s in range(64) if m >> s & 1])]
        if r[0x47]:
            secs.append(_s('Battle start', [_e('Starts with MP', '%d%%' % r[0x47])]))
        finish(e, secs)
        e['dev'] = dev('battle_pack.bin directory +0x44 (party table, 128 B)', i, {
            '+0x16 baseHP': u16(r, 0x16), '+0x1A baseMP': u16(r, 0x1A), '+0x1E str': r[0x1E], '+0x1F strGrowth': r[0x1F],
            '+0x21 mag': r[0x21], '+0x22 magGrowth': r[0x22], '+0x24 vit': r[0x24], '+0x25 vitGrowth': r[0x25],
            '+0x27 spd': r[0x27], '+0x28 spdGrowth': r[0x28], '+0x2A evade': r[0x2A], '+0x2B class': r[0x2B],
            '+0x46 licenceRankFloor': r[0x46], '+0x47 startMpPercent': r[0x47], '+0x50/+0x54 innateMask': m},
            'Growth bytes (+0x1F, +0x22, +0x25, +0x28) have no per-level unit documented; the starting level and '
            'starting equipment are not located in this row.',
            P_PARTYSTATS + '; innate mask: ' + P_AUTOSTAT + ' (kind 0: the party row\'s two masks); '
            'start MP: ' + P_MP, r)

    # ---------------- enemies
    maps_by_code = {m['mapCode']: m for m in world['maps']}
    area_name = {a['id']: a.get('display') or a['name'] for a in world['areas']}
    lanes_level = {}
    for z in zones.values():
        for c in z.get('controllers') or []:
            for ln in c.get('lanes') or []:
                uk = ln.get('unitKey')
                lv = ((ln.get('recipe') or {}).get('level') or [None])[0]
                if uk and lv is not None:
                    lanes_level.setdefault('enemy:' + uk, set()).add(lv)
    for e in families['enemies']:
        u = units.get(e['key'][len('enemy:'):]) or {}
        ds = u.get('defaultStats') or {}
        cls = u.get('class') or {}
        prof = [_e('Class', groups['enemies'].get(e['group'][0]) if e.get('group') else None),
                _e('Genus', e.get('genus_name')),
                _e('Hunt target', 'yes' if u.get('isHunt') else None), _e('Boss', 'yes' if u.get('isBoss') else None)]
        lv = sorted(lanes_level.get(e['key'], []))
        if lv:
            prof.append(_e('Level', lv[0] if len(lv) == 1 else '%d-%d' % (lv[0], lv[-1])))
        secs = [_s('Profile', prof),
                _s('Stats', [_e(lab, ds.get(k)) for k, lab in ENEMY_STATS if ds.get(k)]),
                _s('Rewards', [_e(lab, ds.get(k)) for k, lab in ENEMY_REWARDS if ds.get(k)])]
        aff = cls.get('affinities') or {}
        secs.append(_s('Elements', [_e(lab, ', '.join(x.strip().capitalize() for x in str(aff.get(k)).split(',')))
                                    for k, lab in AFF_LABEL if aff.get(k) and str(aff.get(k)).lower() != 'none']))
        for verb, title_ in (('Drops', 'Drops'), ('Steal', 'Steal'), ('Poach', 'Poach')):
            ent = []
            for slot, v, rate in LOOT_SLOTS:
                if v != verb:
                    continue
                x = ((u.get('loot') or {}).get(slot) or {}).get('id')
                if x is not None and x != 0xFFFF:
                    k = resolve(x)
                    ent.append(link(rate.capitalize(), k) if k else _e(rate.capitalize(), (u['loot'][slot] or {}).get('name')))
            secs.append(_s(title_, ent))
        wid = (u.get('weapon') or {}).get('id')
        wk = resolve(wid) if wid is not None and wid != 0x1000 else None
        wname = (u.get('weapon') or {}).get('name')
        if wk and by_key.get(wk) and (by_key[wk].get('placeholder') or title(wk).startswith('NOT USED')) and wname:
            secs.append(_s('Equipment', [link('Weapon', wk, wname)]))
        else:
            secs.append(_s('Equipment', [link('Weapon', wk) if wk else None]))
        secs.append(_s('Actions', [link('Action', k) for k in enemy_actions.get(e['key'], [])]))
        det = cls.get('detection') or {}
        mv = cls.get('movement') or {}
        secs.append(_s('Behaviour', [_e('Notices sound and magick', 'yes' if det.get('soundAndMagick') else None),
                                     _e('Notices by life', 'yes' if det.get('life') else None),
                                     _e('Flies', 'yes' if mv.get('Is Flying') else None),
                                     _e('Floats', 'yes' if mv.get('Is Floating') else None)]))
        areas_ = []
        for mc in e.get('maps', []):
            m = maps_by_code.get(mc) or {}
            a = m.get('area')
            if a is not None and 'area:%d' % a not in areas_:
                areas_.append('area:%d' % a)
        secs.append(_s('Found in', [{'label': 'Area', 'value': area_name.get(int(a.split(':')[1])), 'link': a}
                                    for a in areas_] +
                       [{'label': 'Map', 'value': mc, 'link': 'map:' + mc} for mc in e.get('maps', [])]))
        finish(e, secs)
        e['dev'] = {'table': 'enemy_catalog.json units', 'row': e['key'][len('enemy:'):],
                    'fields': {'additiveStats': {k: v for k, v in (u.get('additiveStats') or {}).items() if v},
                               'lootRates': u.get('lootRates'), 'class': {k: cls.get(k) for k in
                                                                         ('classification', 'genus', 'affinities',
                                                                          'detection', 'movement')},
                               'aiKeys': u.get('aiKeys'), 'levels': lv},
                    'undecoded': 'Values come from the hub catalog (its own sources), not decoded here from the .ard. '
                                 'additiveStats is shown raw: its per-level meaning is not documented. The lane level '
                                 'pair\'s second value is not documented; Level shows the first.',
                    }
        dev_basis.setdefault('enemy_catalog.json units', P_CATALOG + '; action package ids (bit 15): ' + P_GAMBIT + ' Z-16')

    # ---------------- commands / genera / enemy classes: reverse links and texts
    crow = {u16(r, 2) & 0x7FF: r for r in cmdt if u16(r, 2) >> 11 == 4}
    for e in families['commands']:
        r = crow.get(e['index'])
        finish(e, [], text(u16(r, 0)) if r else None)
        if r:
            e['dev'] = dev('battle_pack.bin directory +0x48 (command list, 4 B)', None,
                           {'+0x00 descriptionId': u16(r, 0), '+0x02 nameWord': u16(r, 2)}, 'none',
                           P_FILL + '; texts: ' + P_TEXTGRP, r)
    for fam, key in (('genera', 'genus'), ('enemy_classes', 'class')):
        members = {}
        for en in families['enemies']:
            for c in en.get('group') or []:
                members.setdefault(c, []).append(en['key'])
        for e in families[fam]:
            lst = members.get('%s:%d' % (key, e['index']), [])
            finish(e, [_s('Enemies', _capped(lambda k: link('Enemy', k), lst, 'enemies'))])

    # ---------------- world
    loc_by = {l['id']: l for l in world['locations']}
    for r_ in world['regions']:
        r_['key'] = 'region:%d' % r_['id']
    for a in world['areas']:
        a['key'] = 'area:%d' % a['id']
    for l in world['locations']:
        l['key'] = 'location:%d' % l['id']
    for m in world['maps']:
        m['key'] = 'map:' + m['mapCode']
    for r_ in world['regions']:
        r_['sections'] = [s for s in [_s('Areas', [{'label': 'Area', 'value': area_name.get(x), 'link': 'area:%d' % x}
                                                   for x in r_['areas']])] if s]
    for a in world['areas']:
        maps_ = [m for m in world['maps'] if m.get('area') == a['id']]
        en = []
        for m in maps_:
            for k in m['enemies']:
                if k not in en:
                    en.append(k)
        a['sections'] = [s for s in [
            _s('Travel', [_e('Strahl can land here', 'yes' if a['strahl'] else None)]),
            _s('Connects to', [{'label': 'Area', 'value': area_name.get(x), 'link': 'area:%d' % x}
                               for x in dict.fromkeys(a['links'])]),
            _s('Locations', [{'label': 'Location', 'value': loc_by[x].get('code') or str(x), 'link': 'location:%d' % x}
                             for x in a['locations']]),
            _s('Maps', [{'label': 'Map', 'value': m['mapCode'], 'link': m['key']} for m in maps_]),
            _s('Enemies found here', _capped(lambda k: link('Enemy', k), en, 'enemies'))] if s]
    for l in world['locations']:
        en = []
        for mc in l['maps']:
            for k in (maps_by_code.get(mc) or {}).get('enemies', []):
                if k not in en:
                    en.append(k)
        l['sections'] = [s for s in [
            _s('Area', [{'label': 'Area', 'value': area_name.get(l['area']), 'link': 'area:%d' % l['area']}
                        if l['area'] is not None else None]),
            _s('Maps', [{'label': 'Map', 'value': mc, 'link': 'map:' + mc} for mc in l['maps']]),
            _s('Enemies found here', _capped(lambda k: link('Enemy', k), en, 'enemies'))] if s]
    for m in world['maps']:
        m['sections'] = [s for s in [
            _s('Where', [{'label': 'Location', 'value': str(m['location']), 'link': 'location:%d' % m['location']}
                         if m['location'] is not None else None,
                         {'label': 'Area', 'value': area_name.get(m['area']), 'link': 'area:%d' % m['area']}
                         if m.get('area') is not None else None]),
            _s('Enemies', [link('Enemy', k) for k in m['enemies']])] if s]

    # ---------------- controls: every link resolves; known values
    keys = set(by_key) | {x['key'] for part in ('regions', 'areas', 'locations', 'maps') for x in world[part]}
    bad = []
    for fam in families.values():
        for e in fam:
            for g in e.get('grants', []):
                if g not in keys:
                    bad.append((e['key'], g))
            for s in e.get('sections', []):
                for x in s['entries']:
                    if x.get('link') and x['link'] not in keys:
                        bad.append((e['key'], x['link']))
    for part in ('regions', 'areas', 'locations', 'maps'):
        for o in world[part]:
            for s in o.get('sections', []):
                for x in s['entries']:
                    if x.get('link') and x['link'] not in keys:
                        bad.append((o['key'], x['link']))
    ctl('links.resolve', not bad, 'every section link and every licence grant resolves to a catalogue entry '
                                  '(%d dangling %s)' % (len(bad), bad[:4]))

    def val(fam, name, sec, label):
        for e in families[fam]:
            if (e.get('display') or e['name']) == name:
                for s in e.get('sections', []):
                    if s['title'] == sec:
                        for x in s['entries']:
                            if x['label'] == label:
                                return x['value']
        return None

    checks = [
        ('value.potion.price', val('abilities', 'Potion', 'Cost', 'Price'), '60 gil', 'Potion costs 60 gil'),
        ('value.phoenix.price', val('abilities', 'Phoenix Down', 'Cost', 'Price'), '200 gil', 'Phoenix Down costs 200 gil'),
        ('value.cure.mp', val('abilities', 'Cure', 'Cost', 'MP cost'), 8, 'Cure costs 8 MP'),
        ('value.cure.price', val('abilities', 'Cure', 'Cost', 'Price'), '200 gil', 'the Cure magick sells for 200 gil in shops'),
        ('value.fire.element', val('abilities', 'Fire', 'Effect', 'Element'), 'Fire', "Fire's element is Fire"),
        ('value.holy.element', val('abilities', 'Holy', 'Effect', 'Element'), 'Holy', "Holy's element is Holy (bit 0x40)"),
        ('value.dark.element', val('abilities', 'Dark', 'Effect', 'Element'), 'Dark', "Dark's element is Dark (bit 0x80)"),
        ('value.zodiark.lp', val('licences', 'Zodiark', 'Licence', 'LP cost'), 200, 'the Zodiark licence costs 200 LP'),
        ('value.teleport.price', val('loot', 'Teleport Stone', 'Value', 'Price'), '200 gil', 'Teleport Stone is worth 200 gil'),
        ('pin.broadsword.attack', val('equipment', 'Broadsword', 'Stats', 'Attack'), 14,
         'PIN (the shipped table, no independent source on this machine): Broadsword Attack 14'),
        ('pin.broadsword.evade', val('equipment', 'Broadsword', 'Stats', 'Evade'), 5,
         'PIN (the shipped table): Broadsword Evade 5'),
        ('pin.broadsword.price', val('equipment', 'Broadsword', 'Shop', 'Price'), '390 gil',
         'PIN (the shipped table): Broadsword price 390 gil'),
    ]
    for cid, got, want, what in checks:
        ctl(cid, got == want, '%s (got %r)' % (what, got))
    ko = next((e.get('about') for e in families['statuses'] if e['name'] == 'KO'), None)
    ctl('value.ko.about', bool(ko) and ko.startswith('The character has lost consciousness'),
        'KO help text from the status text group (%r)' % (ko or '')[:50])
    dg = next((e for e in families['enemies'] if e['name'] == 'Deathgaze'), None)
    hp = None
    if dg:
        for s in dg.get('sections', []):
            for x in s['entries']:
                if s['title'] == 'Stats' and x['label'] == 'HP':
                    hp = x['value']
    want = ((units.get(dg['key'][len('enemy:'):]) or {}).get('defaultStats') or {}).get('Max HP') if dg else None
    ctl('value.deathgaze.hp', dg is not None and hp == want and hp, 'Deathgaze HP on its page = the catalog\'s Max HP (%r)' % hp)
    w20 = [x['link'] for s in by_key['augment:20'].get('sections', []) for x in s['entries'] if s['title'] == 'On the License Board as']
    ctl('augments.warmage', any(title(k) == 'Warmage' for k in w20),
        'augment 20 ("Gain MP after dealing magick damage.") lists the Warmage licence')

    return {fam: {'numerator': sum(1 for e in lst if e.get('sections')), 'denominator': len(lst),
                  'scope': 'entries with at least one decoded section'} for fam, lst in families.items()}


# ---------------------------------------------------------------------------------------------
# Building the catalogue
# ---------------------------------------------------------------------------------------------
def sha(b):
    return hashlib.sha256(b).hexdigest()


_TOKEN = re.compile(r'<[0-9A-F]{2}>')
_ESCAPE_RUN = re.compile(r'<0F>(?:<[0-9A-F]{2}>)*')


# The PC font's own character table (16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md,
# "Glyph record ... {u32 key; u32 utf8; ...}": utf8 is the glyph's UTF-8 bytes, the record's human-readable
# name). The game's single-byte text code c draws glyph key c - 0x20 of us/font00.dat: the reading is
# accepted only because it reproduces every code the decoder already maps (control charset.font).
_FONT = {}            # text code -> character
_UNGROUNDED = set()   # text codes met in names that the font table cannot ground


def load_font(dat):
    """us/font00.dat -> {text code: character}; 0x28 header + 0x24-byte {key, utf8, ...} records."""
    out = {}
    n = (len(dat) - 0x28) // 0x24
    for i in range(n):
        o = 0x28 + 0x24 * i
        key, u8 = u32(dat, o), u32(dat, o + 4)
        try:
            ch = u8.to_bytes(4, 'little').rstrip(b'\0').decode('utf-8')
        except UnicodeDecodeError:
            continue
        if ch and key + 0x20 < 0x100:
            out[key + 0x20] = ch
    return out


def _font_token(m):
    code = int(m.group(0)[1:3], 16)
    ch = _FONT.get(code) if code >= 0x20 else None
    if ch is None:
        _UNGROUNDED.add(code)
        return m.group(0)
    return ch


def display_of(name):
    """The player-readable form of a lossless name: each 0x0F escape run (<0F> and the <XX> tokens directly
    after it) removed, then every remaining <XX> code drawn through the font table. A code the font cannot
    ground stays <XX> and is listed in notes.ungrounded_codes."""
    s = _ESCAPE_RUN.sub('', name)
    return _TOKEN.sub(_font_token, s).strip()


def text_entry(key, raw, seen, extra=None, name=None):
    if name is None:
        name = dec(raw) if raw is not None else ''
    e = {'key': key, 'name': name}
    if extra:
        e.update(extra)
    if name.strip() == '':
        e['blank'] = True
    if raw is not None and raw[:1] == b'\x0f':
        e['placeholder'] = True          # 0x0F-escape-prefixed "No name" / "Reserve" slots
    if _TOKEN.search(name):
        e['undecoded_bytes'] = True
        if display_of(name) != name:
            e['display'] = display_of(name)
            if not e['display']:
                e['blank'] = True
    if name in seen:
        e['duplicate'] = True
        e['duplicate_of'] = seen[name]
    else:
        seen[name] = key
    return e


BANK_FAMILIES = [
    # family, bank, key prefix
    ('abilities', 0, 'ability'),
    ('equipment', 1, 'equipment'),
    ('licences', 3, 'licence'),
    ('commands', 4, 'command'),
    ('statuses', 5, 'status'),
    ('gambits', 6, 'gambit'),
    ('bazaar', 9, 'bazaar'),
    ('loot', 11, 'loot'),
    ('key_items', 12, 'keyitem'),
    ('enemy_classes', 13, 'enemyclass'),
    ('genera', 14, 'genus'),
]

MAIN_NAMES = ['Vaan', 'Ashe', 'Fran', 'Balthier', 'Basch', 'Penelo']


def build(vbf_path, catalog_path):
    t0 = time.time()
    sources = {}
    controls = []

    def ctl(cid, ok, what):
        controls.append({'id': cid, 'ok': bool(ok), 'what': what})

    st = os.stat(vbf_path)
    sources['vbf'] = {'path': vbf_path, 'sha256': None, 'size': st.st_size,
                      'note': 'archive not hashed (size); each member read from it is hashed below'}
    with open(vbf_path, 'rb') as f:
        names, blocks = vbf_load_index(f)
        raw = {}
        for key, p in (('battle_pack', P_BATTLE), ('menu_mapname', P_MAPNAME), ('wmap', P_WMAP),
                       ('amap', P_AMAP), ('lmap', P_LMAP), ('cmap', P_CMAP),
                       ('menumap_world_h', P_WHDR), ('map_ref', P_MAPREF)):
            raw[key] = vbf_read_entry(f, names, blocks, p)
            sources[key] = {'path': 'vbf:' + p, 'sha256': sha(raw[key]), 'size': len(raw[key])}
        # the PC font's character table, the text-group files and the job boards
        raw['font00'] = vbf_read_entry(f, names, blocks, P_FONT)
        sources['font00'] = {'path': 'vbf:' + P_FONT, 'sha256': sha(raw['font00']), 'size': len(raw['font00'])}
        text_files = {}
        for p in sorted(n for n in names if n.startswith(P_TEXTDIR) and n.endswith('.bin')):
            b = vbf_read_entry(f, names, blocks, p)
            if b[:4] == b'st2e' and u32(b, 8) == 4 and u32(b, 4):
                text_files[p] = b
                sources['text:' + p.rsplit('/', 1)[1]] = {'path': 'vbf:' + p, 'sha256': sha(b), 'size': len(b)}
        boards = {}
        for loc in ('ch', 'in', 'kr', 'cn'):
            ps = ['ps2data/image/ff12/test_battle/%s/binaryfile/board_%d.bin' % (loc, n) for n in range(1, 13)]
            if all(p in names for p in ps):
                for n, p in enumerate(ps, 1):
                    boards[n] = vbf_read_entry(f, names, blocks, p)
                    sources['board_%d' % n] = {'path': 'vbf:' + p, 'sha256': sha(boards[n]), 'size': len(boards[n])}
                break
    _FONT.clear()
    _FONT.update(load_font(raw['font00']))
    _UNGROUNDED.clear()

    # ---- decoder self-control
    ctl('dec.vaan', dec(bytes([0x35, 0x3A, 0x3A, 0x47])) == 'Vaan', 'charset: 35 3A 3A 47 decodes to "Vaan"')
    ctl('dec.escape', dec(bytes([0x0F, 0x20, 0x81, 0x94, 0x35])) == '<0F><20><81><94>V',
        'charset: a 0x0F escape and its 3 parameter bytes stay <XX> (0x81 is not read as a letter there)')

    # ---- text banks
    bp = raw['battle_pack']
    banks = decode_banks(bp)
    ctl('banks.count', len(banks) == 15, 'battle_pack has 15 text banks (got %d)' % len(banks))
    for bi, want in enumerate(BANK_EXPECT):
        got = len(banks[bi]) if bi < len(banks) else None
        ctl('bank.%d.count' % bi, got == want, 'bank %d has %s blocks (expected %d)' % (bi, got, want))

    families = {}
    for fam, bank, prefix in BANK_FAMILIES:
        seen = {}
        families[fam] = [text_entry('%s:%d' % (prefix, i), r, seen, {'index': i, 'bank': bank})
                         for i, r in enumerate(banks[bank])]
    ctl('bank.status.order', [e['name'] for e in families['statuses'][:3]] == ['KO', 'Stone', 'Petrify'],
        'bank 5 opens KO, Stone, Petrify (status id order)')
    ctl('bank.espers.actions', [dec(banks[0][i]) for i in (0x106, 0x112)] == ['Belias', 'Zodiark'],
        'bank 0 0x106 / 0x112 are Belias / Zodiark')

    # ---- party table
    ph, prow = decode_party(bp, banks)
    ctl('party.rows', ph['count'] == 40 and ph['rec'] == 128,
        'party table (blob +0x44) is st2e 40 x 128 B (got %d x %d)' % (ph['count'], ph['rec']))
    ctl('party.main6', [r['name'] for r in prow[:6]] == MAIN_NAMES,
        'party rows 0-5 are %s (got %s)' % (', '.join(MAIN_NAMES), [r['name'] for r in prow[:6]]))
    # Espers: the 13-row band whose class byte is 20 (battle-text-banks.md 5); proven by name
    # against the thirteen Esper summon actions, bank 0 0x106-0x112.
    esper_rows = [r['row'] for r in prow if r['cls'] == 20]
    esper_names = [prow[i]['name'] for i in esper_rows]
    esper_actions = [dec(banks[0][i]) for i in range(0x106, 0x113)]
    band_ok = (len(esper_rows) == 13 and esper_rows == list(range(esper_rows[0], esper_rows[0] + 13))
               and esper_names == esper_actions)
    ctl('party.espers', band_ok,
        'party rows with class byte 20 are one contiguous 13-row band (%s) whose names equal bank 0 '
        '0x106-0x112 (the Esper actions)' % (('%d-%d' % (esper_rows[0], esper_rows[-1])) if esper_rows else 'none'))
    party = []
    seen = {}
    for r in prow:
        if r['row'] < 6:
            kind = 'main'
        elif band_ok and r['row'] in esper_rows:
            kind = 'esper'
        elif r['cls'] == 13 and r['raw'] is not None and r['raw'][:1] != b'\x0f' and r['name'].strip():
            kind = 'guest'
        else:
            kind = 'other'
        party.append(text_entry('party:%d' % r['row'], r['raw'], seen,
                                {'kind': kind, 'class': r['cls'], 'nameRef': '%d:%d' % (r['bank'], r['index'])}))
    families['party'] = party

    # ---- world
    mn = decode_mapname(raw['menu_mapname'])
    wm = decode_wmap(raw['wmap'])
    am = decode_amap(raw['amap'])
    cm = decode_cmap(raw['cmap'])
    lm = decode_lmap(raw['lmap'])
    mr = decode_mapref(raw['map_ref'])
    subs_h, areas_h = decode_world_h(raw['menumap_world_h'].decode('utf-8', 'replace'))

    def mname(i):
        r = mn.get(i)
        return dec(r) if r is not None else None

    region_slots = [(slot, nid) for slot, nid in enumerate(wm['regions']) if nid != 0xFFFFFFFF]
    area_recs = [a for a in wm['areas'] if a['nameId'] != 0xFFFFFFFF]
    ctl('world.region60000', mname(60000) == 'Dalmasca', 'menu_mapname 60000 = "Dalmasca" (got %r)' % mname(60000))
    ctl('world.area60100', mname(60100) == 'Rabanastre', 'menu_mapname 60100 = "Rabanastre" (got %r)' % mname(60100))
    ctl('world.region_slot1', region_slots and region_slots[0] == (1, 60000),
        'wmap region slot 1 holds name id 60000')
    ctl('world.regions11', len(region_slots) == 11, 'wmap has 11 region names (got %d)' % len(region_slots))
    ctl('world.areas38', len(area_recs) == 38, 'wmap has 38 named areas (got %d)' % len(area_recs))
    ctl('world.area_names', all(a['nameId'] == 60099 + a['self'] == a['nameId2'] and a['nameId'] in mn
                                for a in area_recs),
        'every area record: +16 name id = 60099 + self index = +24 name id, and is in menu_mapname')
    ctl('world.wmap.closes', wm['closes'] and len(wm['strahl']) == 18 and len(wm['routes']) == 60,
        'wmap Strahl table closes to EOF; 18 Strahl points, 60 routes (menumap_world.h)')
    ctl('world.amap.S', am['closes'] and am['S'][1:] == [a['nameId'] for a in wm['areas'][1:]],
        'amap closes to EOF and S[i] equals the wmap area name id for all 38 areas')
    ctl('world.amap.S.shift', am['S'][1:-1] != [a['nameId'] for a in wm['areas'][2:]],
        'negative control: amap S shifted by one does not match wmap')
    ctl('world.lmap.closes', len(lm) == 48 and all(r['closes'] for r in lm),
        'lmap: 48 records, each walks to its exact end under the native layout')
    ctl('world.cmap48', len(cm) == 48 and all(e['nameId'] in mn for e in cm),
        'cmap: 48 sub-location entries, every name id in menu_mapname')
    same = sum(mr[f] == cm[n]['group'] for n in range(48) for f in lm[n]['A'] if f < len(mr))
    tot = sum(len(lm[n]['A']) for n in range(48))
    nxt = sum(mr[f] == cm[(n + 1) % 48]['group'] for n in range(48) for f in lm[n]['A'] if f < len(mr))
    ctl('world.join.lmapA_group', same == tot == 384 and nxt == 0,
        'map_ref group of every lmap A field = its cmap entry group (%d/%d); next-record control %d' % (same, tot, nxt))
    ctl('world.maxQ', len(am['Q']) == 59 and max(am['Q']) <= 38,
        'amap Q: 59 persistence groups, each mapping to an area index <= 38')

    # regions
    regions = []
    for slot, nid in region_slots:
        seenr = {}
        e = text_entry('region:%d' % slot, mn.get(nid, b''), seenr, {'id': slot, 'nameId': nid})
        e.pop('key')
        e['areas'] = [a['self'] for a in area_recs if a['region'] == slot]
        regions.append(e)
    # locations (sub-locations)
    locations = []
    for n in range(len(cm)):
        g = cm[n]['group']
        area = am['Q'][g] if g < len(am['Q']) and am['Q'][g] != 0 else None
        e = {'id': n, 'name': mname(cm[n]['nameId']) or '', 'nameId': cm[n]['nameId'],
             'area': area, 'group': g}
        if n in subs_h:
            e['code'] = subs_h[n][0]
            if subs_h[n][1]:
                e['authored_jp'] = subs_h[n][1]
        if not e['name'].strip():
            e['blank'] = True
            if area is not None:
                # the area name; the cmap page (section 4) reads empty sub-location names as falling
                # back to the parent's name. Given as a separate field, never as 'name'.
                e['fallback_name'] = display_of(mname(60099 + area) or '')
        e['fields'] = list(lm[n]['A']) + [mem for _, mem in lm[n]['D']] if n < len(lm) else []
        e['maps'] = []
        locations.append(e)
    # areas
    strahl_areas = {s['area'] for s in wm['strahl']}
    areas = []
    for a in area_recs:
        e = {'id': a['self'], 'name': mname(a['nameId']) or '', 'nameId': a['nameId'], 'region': a['region'],
             'links': [x for x in a['links'] if x != 0xFF], 'strahl': a['self'] in strahl_areas,
             'locations': [l['id'] for l in locations if l['area'] == a['self']]}
        if a['self'] in areas_h:
            e['code'] = areas_h[a['self']][0]
            e['authored_jp'] = areas_h[a['self']][1]
        if not e['name'].strip():
            e['blank'] = True
        if _TOKEN.search(e['name']):
            e['undecoded_bytes'] = True
            if display_of(e['name']) != e['name']:
                e['display'] = display_of(e['name'])
        areas.append(e)

    # ---- enemy catalog -> maps and enemies
    maps = []
    units, zones, action_packages = {}, {}, {}
    unplaced = []
    enemies = []
    if catalog_path and os.path.exists(catalog_path):
        cb = open(catalog_path, 'rb').read()
        sources['enemy_catalog'] = {'path': catalog_path, 'sha256': sha(cb), 'size': len(cb)}
        cat = json.loads(cb.decode('utf-8'))
        action_packages = cat.get('actionPackages', {})
        units = cat.get('units', {})
        counts = cat.get('counts', {})
        zones = cat.get('zones', {})
        ctl('catalog.units', len(units) == counts.get('units'),
            'enemy catalog: %d units, counts block says %s' % (len(units), counts.get('units')))
        ctl('catalog.zones', len(zones) == counts.get('decodedZones'),
            'enemy catalog: %d zones, counts block says decodedZones %s' % (len(zones), counts.get('decodedZones')))
        ctl('catalog.areaId_is_field', all(zones[k]['areaId'] == int(k, 16) for k in zones)
            and any(z['areaId'] in lm[0]['A'] for z in zones.values()),
            'catalog zone keys are hex areaIds, and catalog areaIds meet lmap A field ids')
        unit_maps = {}
        for zk, z in zones.items():
            fid = z['areaId']
            ens = []
            for c in z.get('controllers') or []:
                for ln in c.get('lanes') or []:
                    uk = ln.get('unitKey')
                    if uk and ('enemy:' + uk) not in ens:
                        ens.append('enemy:' + uk)
            loc = locate_field(fid, mr, cm, lm)
            grp = mr[fid] if fid < len(mr) else None
            area = am['Q'][grp] if grp is not None and grp < len(am['Q']) and am['Q'][grp] != 0 else None
            m = {'areaId': fid, 'mapCode': z['mapCode'], 'ard': z.get('ard'), 'location': loc,
                 'area': area, 'group': grp, 'enemies': ens}
            maps.append(m)
            if loc is not None:
                locations[loc]['maps'].append(z['mapCode'])
            if loc is None and area is None:
                unplaced.append(z['mapCode'])
            for uk in ens:
                unit_maps.setdefault(uk, [])
                if z['mapCode'] not in unit_maps[uk]:
                    unit_maps[uk].append(z['mapCode'])
        seen = {}
        for uk, u in units.items():
            key = 'enemy:%s:%s' % (u.get('ard'), u.get('unitId'))
            e = text_entry(key, None, seen, None, name=u.get('name') or '')
            cls = u.get('class') or {}
            e['genus'] = cls.get('genus')
            e['classification'] = cls.get('classification')
            e['isHunt'] = u.get('isHunt')
            e['isBoss'] = u.get('isBoss')
            e['maps'] = unit_maps.get(key, [])
            enemies.append(e)
        ctl('catalog.lane_units', all(k in {e['key'] for e in enemies} for k in unit_maps),
            'every unit a controller lane names is a catalog unit')
    else:
        sources['enemy_catalog'] = {'path': catalog_path, 'sha256': None, 'size': None, 'note': 'not found'}
        ctl('catalog.present', False, 'enemy catalog not found at %s' % catalog_path)
    families['enemies'] = enemies
    group_notes = {}
    groups = apply_groups(bp, banks, families, ctl, group_notes)
    placed_loc = sum(1 for m in maps if m['location'] is not None)
    placed_area_only = sum(1 for m in maps if m['location'] is None and m['area'] is not None)
    world = {'regions': regions, 'areas': areas, 'locations': locations, 'maps': maps,
             'unplaced_maps': unplaced,
             'placement': {'maps': len(maps), 'on_location': placed_loc, 'on_area_only': placed_area_only,
                           'unplaced': len(unplaced),
                           'rule': 'location = engine walk 003C0380 (map_ref group -> cmap entries of that '
                                   'group -> lmap D member->node -> lmap A +12 node); area = amap Q[map_ref '
                                   'group]; unplaced = neither join exists. Map codes are never parsed.'}}
    party_rule = ('main = rows 0-5 (names checked); esper = the contiguous 13-row class-byte-20 band whose names '
                  'equal the Esper actions bank 0 0x106-0x112; guest = other class-13 rows with a real name; '
                  'other = the rest (No name placeholders, Chocobo)')

    # ---- the font reading of the text codes, checked against every code the decoder maps by page
    documented = {c: dec(bytes([c])) for c in list(range(0x20, 0x54)) + list(range(0x85, 0x8F)) + list(_CH)
                  if c >= 0x20}
    agree = sum(1 for c, ch in documented.items() if _FONT.get(c) == ch)
    shifted = {sh: sum(1 for c, ch in documented.items() if load_font(raw['font00']).get(c + sh) == ch) for sh in (-1, 1)}
    ctl('charset.font', agree == len(documented) and max(shifted.values()) < len(documented) // 4,
        'font00 glyph key = text code - 0x20 reproduces every documented code (%d/%d); shifted by +-1: %s'
        % (agree, len(documented), shifted))

    # ---- entry pages
    ai_dir = os.path.join(os.path.dirname(catalog_path or ''), 'ai')
    recovered = enrich(bp, banks, families, groups, world, units, zones, ai_dir, action_packages, text_files, boards,
                       ctl, group_notes, sources)
    world['recovered'] = {part: {'numerator': sum(1 for o in world[part] if o.get('sections')),
                                 'denominator': len(world[part]), 'scope': 'objects with at least one section'}
                          for part in ('regions', 'areas', 'locations', 'maps')}
    group_notes['ungrounded_codes'] = {
        'what': 'text codes the font table cannot ground; they stay <XX> in display',
        'codes': ['0x%02X' % c for c in sorted(_UNGROUNDED)]}
    doc = {'format': 'ff12-content-1',
           'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
           'sources': sources, 'world': world, 'families': families, 'groups': groups, 'recovered': recovered,
           'notes': {'party_kind_rule': party_rule,
                     'banks': 'bank 11 = loot and bank 12 = key items per battle-text-banks.md 5.1',
                     'names': 'name is the lossless decode (<XX> = a byte the charset does not map, or a 0x0F '
                              'escape and its parameters); display = the player-readable form: 0x0F escape runs '
                              'removed and every other code drawn through the PC font\'s own character table '
                              '(us/font00.dat, glyph key = code - 0x20; control charset.font), present only when it '
                              'differs. blank = empty (or empty once the '
                              'escapes are removed); duplicate = '
                              'the same name as an earlier entry of the family (duplicate_of); placeholder = '
                              'a 0x0F-prefixed No name / Reserve slot. Nothing is dropped.',
                     'locations': 'the 48 sub-location records (lmap/cmap/menumap_world.h order); names are '
                                  'mostly empty in menu_mapname (fallback_name = the area name)',
                     'group': 'group = [top, sub] codes into groups[family]; group_basis names the field and page. '
                              'null = the field exists but the meaning of this value is not documented (see group_raw); '
                              '[] = no category field / no row. Never derived from names.',
                     **group_notes},
           'controls': controls,
           'elapsed_s': round(time.time() - t0, 2)}
    return doc


def print_controls(doc):
    for c in doc['controls']:
        print('%s  %-26s %s' % ('PASS' if c['ok'] else 'FAIL', c['id'], c['what']))
    fails = sum(not c['ok'] for c in doc['controls'])
    print('CONTROLS %d, FAILS %d' % (len(doc['controls']), fails))
    return fails


def summary(doc):
    w = doc['world']
    print('regions %d, areas %d, locations %d, maps %d (on location %d, on area only %d, unplaced %d)' % (
        len(w['regions']), len(w['areas']), len(w['locations']), len(w['maps']),
        w['placement']['on_location'], w['placement']['on_area_only'], w['placement']['unplaced']))
    print('families: ' + ', '.join('%s %d' % (k, len(v)) for k, v in doc['families'].items()))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--out')
    ap.add_argument('--vbf', default=os.environ.get('FFXII_VBF', DEFAULT_VBF))
    ap.add_argument('--catalog', default=DEFAULT_CATALOG)
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args(argv)
    if not a.out and not a.self_test:
        ap.error('--out or --self-test is required')
    doc = build(a.vbf, a.catalog)
    fails = print_controls(doc)
    summary(doc)
    if a.out:
        tmp = a.out + '.tmp'
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(doc, f, ensure_ascii=False, separators=(',', ':'))
        os.replace(tmp, a.out)
        print('wrote', a.out, os.path.getsize(a.out), 'bytes in %.2f s' % doc['elapsed_s'])
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
