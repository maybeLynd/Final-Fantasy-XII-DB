#!/usr/bin/env python3
"""gen_settings_commands.py - rebuild the in-game settings command table.

Emits members/settings_command_table.tsv. All facts are re-derived from the
shipping image and the extracted text pools; nothing is hand-copied.

Sources:
  * Database/Tools/work/exe/FFXII_TZA.exe           (dispatchers, setters/getters,
                                                     descriptor table 0x01E0BF60,
                                                     BSS-pane builder stores)
  * .../test_battle/us/binaryfile/menu_command.bin  (bank 1 labels/choices)
  * .../test_battle/us/binaryfile/menu_message.bin  (bank 2 labels)
  * .../test_battle/us/binaryfile/help_menu.bin     (bank 3 help strings)

Address basis: canonical VA, image base 0x00120000 included.
"""
import os
import struct
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'Database', 'Tools', 'analysis-kit', 'gfz-scripts'))
from disasm_fn import Image, DEFAULT_EXE  # noqa: E402

POOL_ROOT = 'D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/'
OUT = os.path.join(os.path.dirname(__file__), 'settings_command_table.tsv')

# ---------------------------------------------------------------- pools ----
GLYPH = {0x20 + i: c for i, c in enumerate(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')}


def decode(s):
    r = ''
    for b in s:
        if b == 0:
            break
        if b in GLYPH:
            r += GLYPH[b]
        elif b == 4:
            r += ' '
        elif b < 0x20:
            r += '<%02X>' % b
        else:
            r += '[%02X]' % b
    return r


def load_pool(path):
    f = open(path, 'rb').read()
    heap = struct.unpack('<I', f[0x14:0x18])[0]
    _one, base, _size, hcnt = struct.unpack('<IIII', f[heap:heap + 16])
    offs = struct.unpack('<%dI' % (hcnt + 1), f[heap + 16:heap + 16 + 4 * (hcnt + 1)])
    out = []
    for i in range(hcnt):
        o = heap + base + offs[i]
        end = f.index(b'\x00', o)
        out.append(f[o:end])
    return out


POOLS = {1: load_pool(POOL_ROOT + 'menu_command.bin'),
         2: load_pool(POOL_ROOT + 'menu_message.bin'),
         3: load_pool(POOL_ROOT + 'help_menu.bin')}


def text(tid):
    if tid in (0xFFFF, 0x0000):
        return ''
    bank, pos = divmod(tid, 1000)
    if bank in POOLS and 0 <= pos < len(POOLS[bank]):
        return decode(POOLS[bank][pos])
    return '<unresolved %04X>' % tid


# ------------------------------------------------------------ image data ----
img = Image(DEFAULT_EXE)


def u16(va):
    return struct.unpack('<H', img.read(va, 2))[0]


def u32(va):
    return struct.unpack('<I', img.read(va, 4))[0]


# descriptor table: 45 slots at 0x01E0BF60 -> {u8 style, u8 id, u16 count, items[count*6]}
DESCS = []
for i in range(45):
    p = img.qword(0x01E0BF60 + i * 8)
    if not p:
        DESCS.append(None)
        continue
    h = img.read(p, 4)
    style, bid, cnt = h[0], h[1], struct.unpack('<H', h[2:4])[0]
    items = []
    d = img.read(p + 4, cnt * 6)
    for j in range(cnt):
        items.append((d[j * 6], u16(p + 4 + j * 6 + 2), u16(p + 4 + j * 6 + 4)))
    DESCS.append((p, style, bid, items))


def desc(i):
    return DESCS[i] if i < len(DESCS) else None


def choices(cid):
    d = desc(cid)
    if not d or not d[3]:
        return ''
    return ' / '.join('%s(0x%04X)' % (text(t), t) for _c, t, _r in d[3])


# dispatch tables (entries are offsets from 0x120000, 35 slots = cmds 4..38)
def arm(tab, cmd):
    return 0x120000 + struct.unpack('<i', img.read(tab + (cmd - 4) * 4, 4))[0]


GET_TAB, SET_TAB = 0x240518, 0x240968
DEFAULT_GET, DEFAULT_SET = 0x240512, 0x24095E

# selector table shared by 00240750 (set-normalise) and 00240330 (get-normalise)
SEL = img.read(0x2403CC, 35)
SEL_NAME = {0: 'v!=0', 1: 'v++ / v--', 2: 'v==0 (invert)', 3: 'pass', 4: 'v!=1', 5: 'pass'}


def sel(cmd):
    return SEL_NAME[SEL[cmd - 4]]


# ------------------------------------------------------------- per-command --
# cmd: (setter, extra-callee, store field, getter, read field, pane rows,
#       reachability note)
ROWS = {
    4:  ('002DE060', None,      'opt+0 bit 3',                      '002DDC30', 'opt+0 bit 3',
         'desc0[4] desc1-- desc2[4]', 'in-game Config'),
    5:  ('002DE0F0', None,      'opt+0 bits 4-11 (s8)',             '002DDC90', 'opt+0 bits 4-11 (s8)',
         'desc0[5] desc1-- desc2[5]', 'in-game Config'),
    6:  ('002DE2D0', None,      'opt+4 bit 22',                     '002DDE00', 'opt+4 bit 22',
         'desc0[6] desc1-- desc2[6]', 'in-game Config'),
    8:  ('002DE1E0', '002DE1C0', 'opt+0 bit 15 + bit 16',           '002DDD50', 'opt+0 bit 15',
         'desc0[7] desc1-- desc2[7]', 'in-game Config'),
    9:  ('002DE080', '0035FF30', 'opt+0 bit 13 -> 0035FF30',        '002DDC40', 'opt+0 bit 13',
         'desc0[9] desc1[8] desc2[9]', 'all Config variants'),
    10: ('002DE200', '0037DDC0', 'opt+0 bit 14 -> 0037DDC0',        '002DDD60', 'opt+0 bit 14',
         'desc0[10] desc1[9] desc2[10]', 'all Config variants'),
    11: ('002DE230', None,      'opt+0 bit 12 (set = !normalised)', '002DDD70', 'u16[0215E6DC] bit 0 if non-zero, else NOT opt+0 bit 12 (CON-194)',
         'desc0[11] desc1[10] desc2[11]', 'all Config variants'),
    12: ('002DE190', '001E1020', 'opt+4 bit 8 -> 001E1020',         '002DDD20', 'opt+4 bit 8',
         'desc0[12] desc1[11] desc2[12]', 'all Config variants'),
    13: ('002DE160', '001E0FF0', 'opt+4 bit 9 -> 001E0FF0',         '002DDD00', 'opt+4 bit 9',
         'desc0[13] desc1[12] desc2[13]', 'all Config variants'),
    14: ('002DE250', '0023B2E0', 'opt+4 bits 23-26 -> 0023B2E0',    '002DDDA0', 'opt+4 bits 23-26',
         'desc0[14] desc1[13] desc2[14]', 'all Config variants'),
    16: ('002DE2F0', None,      'opt+4 bit 10',                     '002DDE20', 'opt+4 bit 10',
         'desc0[15] desc1[14] desc2[15]', 'all Config variants'),
    17: ('002DE110', '002DF530', 'opt+0xE u16 (OST-gated) -> 002DF530', '002DDCA0', 'opt+0xE u16',
         'desc0[16] desc1[15] desc2[16]', 'all Config variants'),
    19: ('002DE0B0', '002DF2B0', 'opt+8 u16 (<=100) -> 002DF2B0',   '002DDC70', 'opt+8 u16 (clamped)',
         'desc0[19] desc1[18] desc2[19]', 'all Config variants'),
    20: ('002DE290', '002DF2B0', 'opt+0xA u16 (<=100) -> 002DF2B0', '002DDDE0', 'opt+0xA u16 (clamped)',
         'desc0[20] desc1[19] desc2[20]', 'all Config variants'),
    21: ('002DE310', '002DF2B0', 'opt+0xC u16 (<=100) -> 002DF2B0', '002DDE40', 'opt+0xC u16 (clamped)',
         'desc0[21] desc1[20] desc2[21]', 'all Config variants'),
    28: ('0017E740', None,      'cfg setting[22] CameraRevise',     '0017E260', 'cfg+0x58',
         'BSS-pane rec36 (kind4)', 'Controls screen'),
    29: ('0032E020', '0017E760', 'cfg setting[24] MouseSensityY (1-6)', '0017E420', 'cfg+0x60',
         'BSS-pane rec34 (kind3)', 'Controls screen'),
    30: ('0032E030', '0017E780', 'cfg setting[23] MouseSensityX (1-6)', '0017E430', 'cfg+0x5C',
         'BSS-pane rec35 (kind3)', 'Controls screen'),
    38: ('0017E6E0', '00198960', 'cfg setting[25] DecideButton -> 00198960', '0017E210', 'cfg+0x64',
         'BSS-pane rec38 (kind4)', 'Controls screen'),
}

# pane-descriptor rows that send a command: (desc_id, item_index, child, label tid, req tid)
PANE_ITEMS = []
for did in (0, 1, 2):
    d = desc(did)
    for j, (c, t, r) in enumerate(d[3]):
        PANE_ITEMS.append((did, j, c, t, r))

# BSS pane rows (reconstructed from the static-initializer stores at 002414B0..)
BSS_ROWS = [(34, 3, 0x562, 0xD3A, 29), (35, 3, 0x563, 0xD3B, 30),
            (36, 4, 0x564, 0xD3C, 28), (38, 4, 0x565, 0xD3F, 38)]

# -------------------------------------------------------------- emission ----
def label_of(cid):
    """First pane item that names this command id."""
    for did, j, c, t, r in PANE_ITEMS:
        if c == cid and t != 0xFFFF:
            return t, r
    for _i, _k, t, r, cmd in BSS_ROWS:
        if cmd == cid:
            return t, r
    return 0xFFFF, 0xFFFF


w = open(OUT, 'w', encoding='utf-8')
w.write('cmd\tlabel_tid\tlabel\tchoices\tsetter\textra_call\tstores\tgetter\treads\t'
        'sel\tset_arm\tget_arm\trow_style\tpane_row\treachability\n')
for cmd in sorted(ROWS):
    setter, extra, store, getter, read, pane, reach = ROWS[cmd]
    tid, rid = label_of(cmd)
    d = desc(cmd)
    style = d[1] if d else -1
    w.write('%d\t0x%04X\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%08X\t%08X\t%d\t%s\t%s\n' % (
        cmd, tid, text(tid), choices(cmd), setter, extra or '-', store, getter, read,
        sel(cmd), arm(SET_TAB, cmd), arm(GET_TAB, cmd), style, pane, reach))

# unhandled ids (default arm)
w.write('\n# ids with no handler (default arm 00240512/0024095E):\n')
for cmd in range(4, 39):
    if cmd in ROWS:
        continue
    w.write('# cmd %d set->%08X get->%08X\n' % (cmd, arm(SET_TAB, cmd), arm(GET_TAB, cmd)))

# unexported option fields (accessor pairs with no command)
w.write('\n# option-record fields with accessors but no command id:\n')
w.write('# opt+0 bits0-1: get 002DDCF0 (caller 004742A0) / set 002DE150 (no callers)\n')
w.write('# opt+0 bit2:    get 002DDCE0 (no callers)\n')
w.write('# opt+0 bit16:   written by cmd8 compound arm; get 002DDD40 (callers 002778C0 00290CF0)\n')
w.write('# opt+0 bits17-24: byte field; bit17 = (005C5230()==2) set by defaults installer 002DDE60\n')
w.write('# opt+4 bit21:   get 002DDDC0 (caller 00251F40) / set 002DE270 (caller 0034D440)\n')
w.write('# opt+0x18 dword&3 -> 002DF360 (re-applied by 002DDA30); opt+0x1C dword read by 002DDA30\n')
w.close()
print('wrote', OUT)
