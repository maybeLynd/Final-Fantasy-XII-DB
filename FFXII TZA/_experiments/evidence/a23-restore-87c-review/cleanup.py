"""Remove only this driver's explicitly named disposable restore trees."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
W = (P / 'run-01').resolve(strict=True)
if W.parent != P or (W / 'cleanup.json').exists():
    raise RuntimeError('refuse unexpected root/repeated cleanup')
pre = json.loads((W / 'preconditions.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
inputs = []
for label, record in pre['retained_inputs'].items():
    archive = Path(record['path'])
    if sha(archive) != record['sha256']:
        raise RuntimeError('retained input moved: ' + label)
    with zipfile.ZipFile(archive) as z:
        members = [{'path': n, 'bytes': len(z.read(n)), 'sha256': hashlib.sha256(z.read(n)).hexdigest()} for n in z.namelist()]
    inputs.append({'label': label, **record, 'zip_bytes': archive.stat().st_size, 'members': members, 'external_required': True})
derived = W / 'derived-trailing-output.zip'
with zipfile.ZipFile(derived) as z:
    members = [{'path': n, 'bytes': len(z.read(n)), 'sha256': hashlib.sha256(z.read(n)).hexdigest()} for n in z.namelist()]
inputs.append({'label': 'trailing-output', 'path': str(derived), 'sha256': sha(derived), 'zip_bytes': derived.stat().st_size, 'members': members, 'external_required': True})
(W / 'input-qualification.json').write_text(json.dumps({'inputs': inputs, 'limits': 'ZIP bodies stay at immutable retained paths; missing bodies make replay INCOMPLETE. Member indexes are not substitute bodies.'}, indent=2) + '\n')
records = []
for label in ('original', 'percent-distinct', 'case-pair', 'unverified', 'trailing-period', 'trailing-output'):
    target = W / ('disposable-' + label)
    resolved = target.resolve()
    if resolved.parent != W or resolved.name != 'disposable-' + label or target.is_symlink():
        raise RuntimeError('disposable path verification failed')
    existed = target.exists()
    tree = {p.relative_to(target).as_posix(): sha(p) for p in target.rglob('*') if p.is_file()} if existed else {}
    if existed:
        if not target.is_dir():
            raise RuntimeError('unexpected non-directory disposable')
        shutil.rmtree(target)
    records.append({'absolute_target': str(resolved), 'existed_before': existed, 'tree_before': tree, 'absent_after': not target.exists()})
unchanged = all(sha(Path(x['path'])) == x['sha256'] for x in inputs)
source_unchanged = sha(P / 'generation.py') == pre['source_sha256']
out = {'cleanup_driver_sha256': sha(Path(__file__)), 'records': records, 'all_disposables_absent': all(x['absent_after'] for x in records), 'all_input_archives_unchanged': unchanged, 'exact_source_unchanged': source_unchanged, 'no_game_save_config_reference_or_peer_process_changes': True}
(W / 'cleanup.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'records'}))
raise SystemExit(0 if unchanged and source_unchanged and out['all_disposables_absent'] else 1)
