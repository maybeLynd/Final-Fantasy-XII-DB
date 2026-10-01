"""test_ff12_content.py - the Player-progression content catalogue (ff12_content.py) over the installed archive.

  C1  the extractor runs into a temp file, exits 0, and finishes in under 60 s
  C2  the document is format ff12-content-1 with every top-level, world and family key the schema names
  C3  every source carries path / sha256 / size; every archive member and the enemy catalog are hashed
  C4  every control the extractor stores passed, and the required ones are present (region 60000 = Dalmasca, area
      60100 = Rabanastre, 11 regions, 38 areas, each bank's count, 40 party rows with the main six, espers, catalog
      unit count against its own counts block)
  C5  world shapes: 11 regions and 38 areas; region.areas and area.region agree; every area link is an area id; every
      location's area is an area id or null; area.locations and location.area agree
  C6  map placement is only what the joins give: location.maps equals the maps whose location is that id; a map is in
      unplaced_maps exactly when it has neither location nor area; placed + area-only + unplaced = all maps
  C7  families: keys are unique and prefixed as the schema says (party:<row>, licence:<i>, enemy:<ard>:<unit>); the
      party table has 40 rows, rows 0-5 main, 13 espers; every map enemy is an enemy key and every enemy's maps
      are map codes that list it
  C8  names are kept, not dropped: blank / duplicate entries are present and flagged; every family has its bank count
  C9  --self-test exits 0; the same self-test with a missing enemy catalog exits non-zero (sensitivity)
  C10 groups schema: every family entry has group ([top, sub] codes, [] or null) and a group_basis; every code is
      declared in groups[family]; a null group carries group_raw
  C11 every group.* control is stored and passed (action kinds, magick school, equipment class, licence groups and
      grants, gambit relation mode, key-item sub-tables, bazaar grants, enemy genus / class)
  C12 spot checks from the game's fields: Cure = Magicks / White Magicks; Broadsword = Sword (1H); the Zodiark licence
      is Quickenings and Espers and grants the Zodiark action; the NOT USED gambit row is grouped by its relation
      mode (Foe), not by its name; Blue Bottle is a key-item object; every loot entry is []; a unit named Wolf has
      genus_name Wolf; the 235 kind-7 actions are null with group_raw, not guessed
  C13 entry pages: every entry of every family and every world object has sections [{title, entries[{label, value,
      link?}]}], no empty section, values are text or numbers, and no label, value or about text carries hex, an
      offset or an undecoded <XX> code
  C14 dev blocks: {table, row, fields, undecoded} on every entry that has sections, and every table is explained
      once in notes.dev_basis
  C15 recovered: per family {numerator <= denominator, scope}; an augments family exists; every licence grant and
      every section link resolves to a catalogue key (checked here independently of the extractor's own control)
  C16 known values and the font: the value.* / pin.* / charset.font / text.groups / links.resolve controls are stored
      and pass; the gambit named with <C4> displays with its font glyph; "Fly, Enkidu" displays with "!";
      notes.ungrounded_codes is present
"""
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, 'ff12_content.py')
fails = 0


def check(tag, ok, text=''):
    global fails
    fails += not ok
    print('%s  %s %s' % ('PASS' if ok else 'FAIL', tag, text))


T = tempfile.mkdtemp(prefix='ff12content_')
out = os.path.join(T, 'content.json')
t0 = time.time()
p = subprocess.run([sys.executable, TOOL, '--out', out], capture_output=True, text=True, encoding='utf-8')
dt = time.time() - t0
check('C1', p.returncode == 0 and os.path.exists(out) and dt < 60,
      'exit %d in %.1f s%s' % (p.returncode, dt, '' if p.returncode == 0 else ('\n' + p.stdout[-2000:] + p.stderr[-2000:])))
if not os.path.exists(out):
    print('FAILS %d' % fails)
    sys.exit(1)
d = json.load(open(out, encoding='utf-8'))

# C2 schema keys
top = {'format', 'generated_at', 'sources', 'world', 'families', 'controls'}
wkeys = {'regions', 'areas', 'locations', 'maps', 'unplaced_maps'}
fkeys = {'party', 'licences', 'abilities', 'commands', 'gambits', 'statuses', 'equipment', 'key_items', 'bazaar',
         'enemies', 'genera'}
w = d.get('world', {})
fam = d.get('families', {})
shape_bad = []
for r in w.get('regions', []):
    if not (isinstance(r.get('id'), int) and isinstance(r.get('name'), str) and isinstance(r.get('areas'), list)):
        shape_bad.append(('region', r.get('id')))
for a in w.get('areas', []):
    if not (isinstance(a.get('id'), int) and isinstance(a.get('name'), str) and isinstance(a.get('region'), int)
            and isinstance(a.get('links'), list) and isinstance(a.get('strahl'), bool) and isinstance(a.get('locations'), list)):
        shape_bad.append(('area', a.get('id')))
for l in w.get('locations', []):
    if not (isinstance(l.get('id'), int) and isinstance(l.get('name'), str) and (l.get('area') is None or isinstance(l['area'], int))
            and isinstance(l.get('maps'), list)):
        shape_bad.append(('location', l.get('id')))
for m in w.get('maps', []):
    if not (isinstance(m.get('areaId'), int) and isinstance(m.get('mapCode'), str)
            and (m.get('location') is None or isinstance(m['location'], int)) and isinstance(m.get('enemies'), list)):
        shape_bad.append(('map', m.get('mapCode')))
for k, v in fam.items():
    for e in v:
        if not (isinstance(e.get('key'), str) and isinstance(e.get('name'), str)):
            shape_bad.append((k, e.get('key')))
check('C2', d.get('format') == 'ff12-content-1' and top <= set(d) and wkeys <= set(w) and fkeys <= set(fam)
      and not shape_bad,
      'missing top %s world %s families %s; bad shapes %s' % (sorted(top - set(d)), sorted(wkeys - set(w)),
                                                              sorted(fkeys - set(fam)), shape_bad[:5]))

# C3 sources
src = d.get('sources', {})
want_src = {'battle_pack', 'menu_mapname', 'wmap', 'amap', 'lmap', 'cmap', 'map_ref', 'enemy_catalog'}
src_bad = [k for k in want_src if not (k in src and src[k].get('path') and isinstance(src[k].get('sha256'), str)
                                       and len(src[k]['sha256']) == 64 and isinstance(src[k].get('size'), int))]
check('C3', not src_bad and all({'path', 'sha256', 'size'} <= set(v) for v in src.values()), 'unhashed/missing %s' % src_bad)

# C4 controls
ctl = {c['id']: c for c in d.get('controls', [])}
required = ['world.region60000', 'world.area60100', 'world.regions11', 'world.areas38', 'party.rows', 'party.main6',
            'party.espers', 'catalog.units'] + ['bank.%d.count' % i for i in range(15)]
check('C4', all(c['ok'] for c in ctl.values()) and all(r in ctl for r in required),
      'failed %s; absent %s' % ([k for k, c in ctl.items() if not c['ok']], [r for r in required if r not in ctl]))

# C5 world shapes
areas = {a['id']: a for a in w['areas']}
regions = {r['id']: r for r in w['regions']}
locs = {l['id']: l for l in w['locations']}
c5 = []
if len(regions) != 11 or len(areas) != 38:
    c5.append('counts %d/%d' % (len(regions), len(areas)))
for r in regions.values():
    for aid in r['areas']:
        if aid not in areas or areas[aid]['region'] != r['id']:
            c5.append('region %d lists area %s' % (r['id'], aid))
for a in areas.values():
    if a['region'] not in regions or a['id'] not in regions[a['region']]['areas']:
        c5.append('area %d region %s' % (a['id'], a['region']))
    if any(x not in areas for x in a['links']):
        c5.append('area %d links %s' % (a['id'], a['links']))
    if sorted(a['locations']) != sorted(l['id'] for l in locs.values() if l['area'] == a['id']):
        c5.append('area %d locations' % a['id'])
for l in locs.values():
    if l['area'] is not None and l['area'] not in areas:
        c5.append('location %d area %s' % (l['id'], l['area']))
check('C5', not c5, '; '.join(c5[:6]) or 'regions %d, areas %d, locations %d' % (len(regions), len(areas), len(locs)))

# C6 placement
maps = w['maps']
c6 = []
for l in locs.values():
    if sorted(l['maps']) != sorted(m['mapCode'] for m in maps if m['location'] == l['id']):
        c6.append('location %d maps' % l['id'])
unpl = sorted(m['mapCode'] for m in maps if m['location'] is None and m.get('area') is None)
if sorted(w['unplaced_maps']) != unpl:
    c6.append('unplaced_maps != maps with neither join')
if any(m['location'] is not None and m['location'] not in locs for m in maps):
    c6.append('dangling location')
on_loc = sum(m['location'] is not None for m in maps)
area_only = sum(m['location'] is None and m.get('area') is not None for m in maps)
if on_loc + area_only + len(w['unplaced_maps']) != len(maps):
    c6.append('partition')
check('C6', not c6, '; '.join(c6) or 'maps %d: on location %d, area only %d, unplaced %d'
      % (len(maps), on_loc, area_only, len(w['unplaced_maps'])))

# C7 families
c7 = []
for k, v in fam.items():
    keys = [e['key'] for e in v]
    if len(keys) != len(set(keys)):
        c7.append('%s keys not unique' % k)
if not all(e['key'] == 'party:%d' % i for i, e in enumerate(fam['party'])):
    c7.append('party keys')
if not all(e['key'] == 'licence:%d' % i for i, e in enumerate(fam['licences'])):
    c7.append('licence keys')
if not all(e['key'].startswith('enemy:') and e['key'].count(':') == 2 for e in fam['enemies']):
    c7.append('enemy keys')
kinds = [e['kind'] for e in fam['party']]
if len(kinds) != 40 or kinds[:6] != ['main'] * 6 or kinds.count('esper') != 13 or kinds.count('main') != 6:
    c7.append('party kinds %s' % kinds)
if [e['name'] for e in fam['party'][:6]] != ['Vaan', 'Ashe', 'Fran', 'Balthier', 'Basch', 'Penelo']:
    c7.append('main names')
ekeys = {e['key']: e for e in fam['enemies']}
map_codes = {m['mapCode']: m for m in maps}
for m in maps:
    for k in m['enemies']:
        if k not in ekeys or m['mapCode'] not in ekeys[k]['maps']:
            c7.append('map %s enemy %s' % (m['mapCode'], k))
for e in fam['enemies']:
    for mc in e['maps']:
        if mc not in map_codes or e['key'] not in map_codes[mc]['enemies']:
            c7.append('enemy %s map %s' % (e['key'], mc))
check('C7', not c7, '; '.join(c7[:6]) or 'party kinds %s' % {k: kinds.count(k) for k in sorted(set(kinds))})

# C8 names kept
want = {'abilities': 545, 'equipment': 544, 'licences': 362, 'commands': 63, 'statuses': 32, 'gambits': 284,
        'bazaar': 128, 'key_items': 512, 'genera': 64}
cnt_bad = {k: len(fam[k]) for k, n in want.items() if len(fam[k]) != n}
everything = [e for v in fam.values() for e in v] + w['regions'] + w['areas'] + w['locations']
flag_bad = [e.get('key', e.get('id')) for e in everything
            if bool(e.get('blank')) != (e.get('display', e['name']).strip() == '')]
blank = sum(bool(e.get('blank')) for e in everything)
dup = sum(e.get('duplicate', False) for v in fam.values() for e in v)
dup_ok = all(fam[k][[x['key'] for x in fam[k]].index(e['duplicate_of'])]['name'] == e['name']
             for k, v in fam.items() for e in v if e.get('duplicate'))
check('C8', not cnt_bad and not flag_bad and blank > 0 and dup > 0 and dup_ok,
      'count mismatches %s; blank flags wrong %s; blank %d, duplicate %d, duplicate_of consistent %s'
      % (cnt_bad, flag_bad[:5], blank, dup, dup_ok))

# C9 self-test and its sensitivity
s1 = subprocess.run([sys.executable, TOOL, '--self-test'], capture_output=True, text=True, encoding='utf-8')
s2 = subprocess.run([sys.executable, TOOL, '--self-test', '--catalog', os.path.join(T, 'no-such-catalog.json')],
                    capture_output=True, text=True, encoding='utf-8')
check('C9', s1.returncode == 0 and 'FAILS 0' in s1.stdout and s2.returncode != 0 and 'FAIL  catalog.present' in s2.stdout,
      'self-test exit %d; missing-catalog self-test exit %d' % (s1.returncode, s2.returncode))

# C10 groups schema
groups = d.get('groups', {})
c10 = []
for k, v in fam.items():
    if k not in groups:
        c10.append('groups lacks %s' % k)
        continue
    for e in v:
        gp = e.get('group', 'MISSING')
        if gp == 'MISSING' or not isinstance(e.get('group_basis'), str) or not e['group_basis']:
            c10.append('%s no group/basis' % e['key'])
        elif gp is None:
            if 'group_raw' not in e:
                c10.append('%s null without group_raw' % e['key'])
        elif not (isinstance(gp, list) and len(gp) <= 2 and all(c in groups[k] for c in gp)):
            c10.append('%s group %s' % (e['key'], gp))
check('C10', not c10, '; '.join(c10[:6]) or 'grouped %d, null %d, none %d' % (
    sum(1 for v in fam.values() for e in v if e.get('group')),
    sum(1 for v in fam.values() for e in v if e.get('group') is None),
    sum(1 for v in fam.values() for e in v if e.get('group') == [])))

# C11 group controls
greq = ['group.action.summon', 'group.action.quickening', 'group.action.trap', 'group.action.idspace',
        'group.action.school', 'group.equip.class', 'group.licence.groups', 'group.licence.qe',
        'group.licence.grants', 'group.gambit.mode', 'group.keyitem.subtables', 'group.bazaar.gives',
        'group.enemy.genus', 'group.enemy.class']
check('C11', all(r in ctl and ctl[r]['ok'] for r in greq), 'absent/failed %s' % [r for r in greq if not (r in ctl and ctl[r]['ok'])])

# C12 spot checks
def by_name(family, name):
    return [e for e in fam[family] if e['name'] == name]
def labels(family, e):
    return [groups[family][c] for c in e['group']] if e.get('group') else e.get('group')
c12 = []
cure = by_name('abilities', 'Cure')
if not cure or labels('abilities', cure[0]) != ['Magicks', 'White Magicks']:
    c12.append('Cure %s' % (labels('abilities', cure[0]) if cure else None))
bs = by_name('equipment', 'Broadsword')
if not bs or labels('equipment', bs[0])[1:] != ['Sword (1H)']:
    c12.append('Broadsword %s' % (labels('equipment', bs[0]) if bs else None))
zl = by_name('licences', 'Zodiark')
zk = {e['key'] for e in by_name('abilities', 'Zodiark')}
if not zl or labels('licences', zl[0])[0] != 'Quickenings and Espers' or not (set(zl[0].get('grants', [])) & zk):
    c12.append('Zodiark licence %s' % (zl[0] if zl else None))
nu = [e for e in fam['gambits'] if e.get('gambit_rows') and e['name'].startswith('NOT USED')]
if not nu or any(e['group'] != ['rel:1'] for e in nu):
    c12.append('NOT USED gambit %s' % [(e['key'], e['group']) for e in nu])
bb = by_name('key_items', 'Blue Bottle')
if not bb or bb[0]['group'] != ['sub:objects']:
    c12.append('Blue Bottle %s' % (bb[0]['group'] if bb else None))
if any(e['group'] != [] for e in fam['loot']):
    c12.append('loot grouped')
wolves = by_name('enemies', 'Wolf')
if not wolves or any(e.get('genus_name') != 'Wolf' for e in wolves):
    c12.append('Wolf %s' % [e.get('genus_name') for e in wolves])
k7 = [e for e in fam['abilities'] if e.get('group_raw', {}).get('action_kind') == 7] if fam['abilities'] else []
if len(k7) != 235 or any(e['group'] is not None for e in k7):
    c12.append('kind-7 actions %d' % len(k7))
check('C12', not c12, '; '.join(c12) or 'all spot checks hold')

# C13 entry pages
import re
HEXRE = re.compile(r'0x[0-9A-Fa-f]+|\+0x|<[0-9A-F]{2}>')
objs = [(k, e) for k, v in fam.items() for e in v] + \
       [(part, o) for part in ('regions', 'areas', 'locations', 'maps') for o in w.get(part, [])]
c13 = []
for k, o in objs:
    secs = o.get('sections')
    if not isinstance(secs, list):
        c13.append('%s no sections' % o.get('key'))
        continue
    for s in secs:
        if not (isinstance(s.get('title'), str) and s.get('entries')):
            c13.append('%s empty/untitled section' % o.get('key'))
            continue
        for x in s['entries']:
            if not (isinstance(x.get('label'), str) and isinstance(x.get('value'), (str, int, float))):
                c13.append('%s bad entry %s' % (o.get('key'), x))
            for f in ('label', 'value'):
                if isinstance(x.get(f), str) and HEXRE.search(x[f]):
                    c13.append('%s hex/code %r' % (o.get('key'), x[f]))
    if isinstance(o.get('about'), str) and HEXRE.search(o['about']):
        c13.append('%s about %r' % (o.get('key'), o['about'][:40]))
check('C13', not c13, '; '.join(c13[:6]) or '%d objects, %d sections' % (len(objs), sum(len(o.get('sections') or []) for _, o in objs)))

# C14 dev blocks
basis = d.get('notes', {}).get('dev_basis', {})
c14 = []
for k, e in [(k, e) for k, v in fam.items() for e in v]:
    dv = e.get('dev')
    if e.get('sections') and k not in ('commands', 'genera', 'enemy_classes'):
        if not (isinstance(dv, dict) and {'table', 'row', 'fields', 'undecoded'} <= set(dv)):
            c14.append('%s dev %s' % (e['key'], sorted(dv) if isinstance(dv, dict) else dv))
    if isinstance(dv, dict) and dv.get('table') not in basis:
        c14.append('%s table %r not in dev_basis' % (e['key'], dv.get('table')))
check('C14', not c14, '; '.join(c14[:5]) or '%d tables explained in notes.dev_basis' % len(basis))

# C15 recovered, augments, links
rec = d.get('recovered', {})
keys = {e['key'] for v in fam.values() for e in v} | {o['key'] for part in ('regions', 'areas', 'locations', 'maps')
                                                       for o in w.get(part, [])}
c15 = []
for k in fam:
    r = rec.get(k)
    if not (isinstance(r, dict) and 0 <= r.get('numerator', -1) <= r.get('denominator', -1) == len(fam[k])
            and r.get('scope')):
        c15.append('recovered %s %s' % (k, r))
if 'augments' not in fam or not fam['augments']:
    c15.append('no augments family')
dang = [(e['key'], g) for e in fam.get('licences', []) for g in e.get('grants', []) if g not in keys]
dang += [(o.get('key'), x['link']) for _, o in objs for s in o.get('sections') or [] for x in s['entries']
         if x.get('link') and x['link'] not in keys]
if dang:
    c15.append('dangling %d %s' % (len(dang), dang[:4]))
check('C15', not c15, '; '.join(c15[:5]) or 'recovered %s' % {k: '%d/%d' % (r['numerator'], r['denominator'])
                                                            for k, r in rec.items()})

# C16 known values, font glyphs
vreq = ['value.potion.price', 'value.phoenix.price', 'value.cure.mp', 'value.cure.price', 'value.fire.element',
        'value.holy.element', 'value.dark.element', 'value.zodiark.lp', 'value.teleport.price', 'value.ko.about',
        'value.deathgaze.hp', 'pin.broadsword.attack', 'charset.font', 'text.groups', 'links.resolve',
        'augments.warmage', 'licence.boards']
c16 = ['control %s absent/failed' % r for r in vreq if not (r in ctl and ctl[r]['ok'])]
c4 = [e for e in fam['gambits'] if '<C4>' in e['name']]
if not c4 or any('<' in e.get('display', e['name']) or '≧' not in e.get('display', '') for e in c4):
    c16.append('<C4> gambits %s' % [(e['name'], e.get('display')) for e in c4[:2]])
enk = [e for e in fam['abilities'] if e['name'].startswith('Fly, Enkidu')]
if not enk or enk[0].get('display') != 'Fly, Enkidu!':
    c16.append('Enkidu %s' % [(e['name'], e.get('display')) for e in enk])
if 'ungrounded_codes' not in d.get('notes', {}):
    c16.append('no notes.ungrounded_codes')
check('C16', not c16, '; '.join(c16) or 'all known-value, font and link controls hold')

print('FAILS %d' % fails)
sys.exit(1 if fails else 0)
