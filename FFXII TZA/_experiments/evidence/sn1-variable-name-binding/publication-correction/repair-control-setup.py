import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;p=W/'prepare-default-controls.py';old=p.read_bytes();(W/'retained/control-setup-before-location-fix.py').write_bytes(old);assert not (W/'producer-default-controls.json').exists()
(W/'control-setup-failure.json').write_text(json.dumps(dict(status='INVALID_COPY_CONTROL_SETUP',cause='Constructed AST Expr statement lacked lineno; original selected copy call already had locations. Execution did not reach copy, no control receipt or package freeze.',old_source_sha256=hashlib.sha256(old).hexdigest(),repair='Fix missing locations on wrapper statement; reconcile already-installed publisher and owned existing fixture, no overwrite of source/input/package.'),indent=2)+'\n')
s=old.decode();s=s.replace("assert 'validate_manifest_pins' not in s;s=s.replace", "already='validate_manifest_pins' in s;s=s.replace")
s=s.replace("assert s.count(needle)==1;s=s.replace(needle,needle+", "assert s.count(needle)==1;s=s if already else s.replace(needle,needle+")
s=s.replace("from verify import git,normalized,verify','from verify import git,normalized,verify\\nfrom manifest_closure import validate_manifest_pins'", "from verify import git,normalized,verify','from verify import git,normalized,verify\\nfrom manifest_closure import validate_manifest_pins' if not already else 'from verify import git,normalized,verify'")
s=s.replace("tmp.mkdir();(tmp/'w/retained/__pycache__').mkdir(parents=True);(tmp/'p').mkdir()", "tmp.mkdir(exist_ok=True);(tmp/'w/retained/__pycache__').mkdir(parents=True,exist_ok=True);(tmp/'p').mkdir(exist_ok=True)")
s=s.replace("compile(ast.Module(body=[ast.Expr(value=calls[0])],type_ignores=[])","compile(ast.fix_missing_locations(ast.Module(body=[ast.Expr(value=calls[0])],type_ignores=[]))")
p.write_text(s)
