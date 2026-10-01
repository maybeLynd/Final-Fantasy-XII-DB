#!/usr/bin/env python3
"""Nine bounded controls for the read-only overlay preflight; uses temporary files only."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from verify_overlay import classify


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    checks=[]
    with tempfile.TemporaryDirectory(prefix='ff12-overlay-controls-') as td:
        base=Path(td); target=(base/'target'); target.mkdir(); target=target.resolve()
        item={'path':'file.txt','before_sha256':sha(b'before'),'after_sha256':sha(b'after')}
        def check(name: str, actual, expected) -> None:
            if actual!=expected:
                raise AssertionError((name,actual,expected))
            checks.append({'name':name,'pass':True})
        (target/'file.txt').write_bytes(b'before')
        check('expected_preimage',classify(target,item)['state'],'expected_preimage')
        check('new_absent',classify(target,dict(item,path='new.txt',before_sha256=None))['state'],'new_file')
        (target/'file.txt').write_bytes(b'after')
        check('already_applied',classify(target,item)['state'],'already_applied')
        (target/'file.txt').write_bytes(b'newer-local-edit')
        check('edited_conflict',classify(target,item)['state'],'conflict')
        check('missing_replacement',classify(target,dict(item,path='missing.txt'))['state'],'conflict')
        (target/'directory').mkdir()
        check('nonfile_conflict',classify(target,dict(item,path='directory'))['state'],'conflict_nonfile')
        for name,path in [('parent_escape','../outside'),('symlink_escape','external/file')]:
            if name=='symlink_escape':
                (base/'outside').mkdir(); (target/'external').symlink_to(base/'outside',target_is_directory=True)
            try:
                classify(target,dict(item,path=path))
            except ValueError:
                check(name,True,True)
            else:
                raise AssertionError('Unsafe path admitted: '+name)
        manifest=base/'manifest.json'; manifest.write_text(json.dumps({'section':'TEST','files':[item,item]}))
        before=(target/'file.txt').read_bytes()
        result=subprocess.run([sys.executable,str(Path(__file__).with_name('verify_overlay.py')),
                               '--target',str(target),'--manifest',str(manifest)],capture_output=True,text=True)
        check('duplicate_manifest_rejected',result.returncode,2)
        if (target/'file.txt').read_bytes()!=before:
            raise AssertionError('Preflight modified a target file')
    print(json.dumps({'section':'SECTION-09','tests':len(checks),'passed':len(checks),
                      'checks':checks,'target_unchanged':True,'temporary_fixtures_removed':True},indent=2))

if __name__=='__main__':
    main()
