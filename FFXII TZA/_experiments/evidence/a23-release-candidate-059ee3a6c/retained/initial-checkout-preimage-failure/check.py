"""Exact historical release-candidate verification; never compare moving CURRENT."""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CANDIDATE = '059ee3a6ccf9f4d5b49ef52deb61d1be75bde1e9'
GEN = 'g20260929T213407Z-9c7238'
MAN_SHA = '865299843d417576c56167c3375db3f3a17e5a2abde61f128b5fdd24b9adc66e'
ZIP_SHA = '23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7'
FOLDER = Path('Database/Tools/work/dashboard') / GEN
ARCHIVE = Path('Database/Tools/work/dashboard-exports') / (GEN + '.zip')
OWNER = Path('Database/FFXII TZA/_index/candidates/a23-release-0929')
VERIFIER = Path('Database/Tools/analysis-kit/gfz-scripts/generation.py')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


git_receipts = []


def git_blob(path):
    argv = ['git', 'show', CANDIDATE + ':' + path]
    p = subprocess.run(argv, capture_output=True)
    git_receipts.append({'argv': argv, 'exit': p.returncode,
                         'stdout_bytes': len(p.stdout), 'stdout_sha256': sha(p.stdout),
                         'stderr': p.stderr.decode('utf-8', errors='replace')})
    require(p.returncode == 0 and p.stdout, 'Git prerequisite failed or empty source')
    return p.stdout


zip_bytes = ARCHIVE.read_bytes()
require(sha(zip_bytes) == ZIP_SHA, 'named archive identity changed')
sidecar = Path(str(ARCHIVE) + '.sha256').read_text().split()
require(sidecar == [ZIP_SHA, ARCHIVE.name], 'sidecar hash/name mismatch')
with zipfile.ZipFile(ARCHIVE) as z:
    names = z.namelist()
    require(len(names) == len(set(names)) == 35 and all(not n.endswith('/') for n in names),
            'duplicate/incorrect member population')
    require(all('..' not in Path(n).parts and not Path(n).is_absolute() for n in names),
            'invalid member path')
    manifest_bytes = z.read('MANIFEST.json')
    require(sha(manifest_bytes) == MAN_SHA, 'manifest identity changed')
    manifest = json.loads(manifest_bytes)
    require(manifest['generation'] == GEN and manifest['format'] == 'ff12-generation-2',
            'wrong generation/format')
    member_rows = []
    for name in names:
        data = z.read(name)
        require(data == (FOLDER / name).read_bytes(), 'ZIP/store member differs: '+name)
        member_rows.append({'path': name, 'bytes': len(data), 'sha256': sha(data)})
    for name, rec in manifest['inputs'].items():
        require(rec['state'] == 'present', 'unexpected input state: '+name)
        if name == 'exe':
            data = Path(rec['path']).read_bytes()
        else:
            data = z.read('inputs/' + name)
        require(sha(data) == rec['sha256'] and len(data) == rec['size'],
                'declared input mismatch: '+name)
    for name, rec in manifest['outputs'].items():
        data = z.read('outputs/' + name)
        require(sha(data) == rec['sha256'] and len(data) == rec['size'],
                'declared output mismatch: '+name)
    require(sha(VERIFIER.read_bytes()) == manifest['verifier'], 'current verifier is not candidate verifier')
    argv = [sys.executable, str(VERIFIER), 'verify-zip', str(ARCHIVE)]
    native = subprocess.run(argv, capture_output=True, text=True)
    require(native.returncode == 0 and native.stdout.startswith('VERIFIED '),
            'supported verifier failed/incomplete')
    verified = json.loads(native.stdout[len('VERIFIED '):])
    require(verified == {'generation': GEN, 'members': 35}, 'wrong verifier result')

    original_receipt_bytes = git_blob((OWNER / 'release-result.json').as_posix())
    require(original_receipt_bytes == (OWNER / 'release-result.json').read_bytes(),
            'producer receipt differs from candidate commit')
    producer = json.loads(original_receipt_bytes)
    views = []
    for name in ('progress', 'overview', 'systems', 'vbf', 'executable', 'types', 'evidence', 'fleet'):
        path = OWNER / ('view-'+name+'.body')
        raw = git_blob(path.as_posix())
        require(raw == path.read_bytes(), 'retained served body changed')
        body = json.loads(raw)
        require(body['meta']['generation'] == GEN
                and body['view'] == json.loads(z.read('outputs/view-'+name+'.json')),
                'producer observed view/ZIP mismatch: '+name)
        step = next(s for s in producer['steps'] if s['step'] == 'view-'+name)
        require(step['status'] == 200 and step['bytes'] == len(raw) and step['sha256'] == sha(raw),
                'producer HTTP receipt mismatch')
        views.append({'view': name, 'retained_http_sha256': sha(raw), 'matches_zip': True,
                      'observer': 'FRONTIER, not an ASTRA live capture'})
    sources = []
    for name, rel in (('build_views.py','Database/Tools/dashboard/build_views.py'),
                      ('requirements.py','Database/Tools/dashboard/requirements.py'),
                      ('uc1_band.py','Database/Tools/analysis-kit/gfz-scripts/uc1_band.py')):
        blob = git_blob(rel)
        snapshot = z.read('inputs/'+name)
        direct = blob == snapshot
        crlf = name == 'uc1_band.py' and blob.replace(b'\r\n',b'\n') == snapshot.replace(b'\r\n',b'\n')
        require(direct or crlf, 'candidate source differs: '+name)
        sources.append({'input': name, 'git_bytes_sha256': sha(blob),
                        'snapshot_bytes_sha256': sha(snapshot), 'exact': direct,
                        'CRLF_equivalence_only_for_uc1': crlf and not direct})
    require(sha(git_blob(VERIFIER.as_posix())) == manifest['verifier'], 'verifier source binding failed')
    # Same-size/population private control; no archive rewrite or second export.
    chosen = z.read('outputs/view-progress.json')
    changed = bytes([chosen[0] ^ 1]) + chosen[1:]
    require(len(changed) == len(chosen) and sha(changed) != manifest['outputs']['view-progress.json']['sha256']
            and changed != (FOLDER/'outputs/view-progress.json').read_bytes(),
            'private member-change detection control failed')

require(sha(ARCHIVE.read_bytes()) == ZIP_SHA, 'archive changed during check')
out = {'status': 'SCOPED_RELEASE_SNAPSHOT_SOURCE_CHECKED_NOT_FULL_A23_ACCEPTANCE',
       'candidate_commit': CANDIDATE, 'generation': GEN,
       'zip_sha256': ZIP_SHA, 'manifest_sha256': MAN_SHA,
       'driver_sha256': sha(Path(__file__).read_bytes()), 'python': sys.version,
       'members': member_rows, 'producer_observed_views': views, 'sources': sources,
       'git_receipts': git_receipts,
       'actual_verify_zip': {'argv': argv, 'exit': native.returncode,
                             'stdout': native.stdout, 'stderr': native.stderr},
       'private_same_count_member_control': {'member': 'outputs/view-progress.json',
                                             'before_sha256': sha(chosen), 'after_sha256': sha(changed),
                                             'hash_and_store_equality_rejected': True},
       'limits': ['Retained HTTP observations are the deployment owner\'s, not new ASTRA live observations.',
                  'CURRENT movement is expected and not compared to this historical candidate.',
                  'No loaded-module attestation, launcher/restart or dashboard suite execution performed.',
                  'Rollback and process receipts require their own scope review; they are not ASTRA runs.',
                  'Full A23/M0-M5 and L1/L2 acceptance remain unawarded.'],
       'cleanup': 'Read-only; no export, rebuild, server/process control or peer/reference write'}
print(json.dumps(out, indent=2))
