"""Prepare additive referents for the three relocated review documents.

Does not write the database. Published payload and manifest remain unchanged.
Default generation validates every local link against its projected destination.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
DB = 'Database/FFXII TZA'
OLD = DB+'/_experiments/evidence/render-review-phase-qualification'
MANIFEST = '5b647504198d614ff8f507eef6efbaf89875d9142853703f65854ec7980d8823'
KINDS = ('clear-callee-footprints', 'removal-phase-contracts', 'slot-identity-publication')
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
sha = lambda b: hashlib.sha256(b).hexdigest()

def identity(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=sha(data))

def prepare(source, output):
    if output.exists():
        raise ValueError('existing output: reconcile, never replace')
    old = source/OLD
    if sha((old/'manifest.json').read_bytes()) != MANIFEST:
        raise ValueError('old manifest identity changed')
    manifest = json.loads((old/'manifest.json').read_bytes())
    if len(manifest['members']) != 76:
        raise ValueError('old manifest population changed')
    for row in manifest['members']:
        if identity(old/row['path']) != dict(bytes=row['bytes'], sha256=row['sha256']):
            raise ValueError('old published member changed: '+row['path'])
    additions, origins, reviews = {}, {}, []
    for kind in KINDS:
        directory = source/(DB+'/_index/candidates/fable-review-astra-render-'+kind+'-1002')
        copied = old/('fable-render-'+kind+'-REVIEW.md')
        primary = directory/'REVIEW.md'
        # Two checkout copies differ only in line endings. Keep both byte identities.
        if copied.read_text(encoding='utf-8') != primary.read_text(encoding='utf-8'):
            raise ValueError('review text differs beyond newline translation: '+kind)
        reviews.append(dict(kind=kind, copied=identity(copied), primary=identity(primary),
                            equality='decoded UTF-8 with universal newline translation only'))
        for match in LINK.finditer(copied.read_text(encoding='utf-8')):
            target = ''.join(match.group(1).split())
            if '/' in target or target.startswith('#'):
                continue
            origin = directory/target
            if not origin.is_file():
                raise ValueError('missing local review referent: '+target)
            destination = OLD+'/'+target
            data = origin.read_bytes()
            if destination in additions and additions[destination] != data:
                raise ValueError('conflicting same-name review referent: '+target)
            additions[destination] = data
            origins.setdefault(destination, []).append(dict(path=origin.relative_to(source).as_posix(), **identity(origin)))
    alias = DB+'/_experiments/evidence/fable-review-astra-render-clear-callee-footprints-1002/REVIEW.md'
    alias_data = ('# Navigation to the canonical independent review\n\n'
                  'This file is a navigation alias, not another review or experiment.\n\n'
                  '[FABLE\'s original review](../../../_index/candidates/fable-review-astra-render-clear-callee-footprints-1002/REVIEW.md).\n').encode()
    additions[alias] = alias_data
    observations = []
    for document in [old/('fable-render-'+k+'-REVIEW.md') for k in KINDS] + [source/alias]:
        document_rel = document.relative_to(source).as_posix()
        text = (additions[document_rel].decode() if document_rel in additions else document.read_text(encoding='utf-8'))
        for match in LINK.finditer(text):
            target = ''.join(match.group(1).split())
            if '://' in target or target.startswith('#'):
                continue
            destination = (document.parent/target).resolve()
            if not destination.is_relative_to(source.resolve()):
                raise ValueError('link outside source root')
            relative = destination.relative_to(source.resolve()).as_posix()
            if relative not in additions and not destination.is_file():
                raise ValueError('unresolved projected review link: '+target)
            observations.append(dict(document=document_rel, target=target, resolved=relative,
                                     added=relative in additions))
    if len(additions) != 8 or sum(r['added'] for r in observations) != 10:
        raise ValueError('unexpected additive population or original broken-link coverage')
    # All checks precede output creation. No partial successful-looking receipt.
    output.mkdir(parents=True)
    for rel, data in additions.items():
        path = output/'additions'/rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    result = dict(status='PREPARED_ADDENDUM', evidence_method='offline publication closure, no scientific rerun',
                  old_manifest_sha256=MANIFEST, original_members_checked=76, review_identities=reviews,
                  additions=[dict(path=rel, bytes=len(data), sha256=sha(data), origins=origins.get(rel, [])) for rel,data in additions.items()],
                  links=observations, original_broken_links_resolved=10,
                  limitations=['Projected closure only until explicit guarded commit and HEAD check.',
                               'Reviewer scripts/outputs are retained evidence; not new ASTRA runs.',
                               'No semantic changes or extra independent acceptance.'])
    result['cases'] = [dict(id='old-manifest-76')] + [dict(id='link:'+r['document']+' -> '+r['target']) for r in observations]
    result['driver_sha256'] = sha(Path(__file__).read_bytes())
    (output/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PREPARED: original76 unchanged, additive8, broken10 projected resolved')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=ROOT)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    prepare(args.source.resolve(), args.output.resolve())
