#!/usr/bin/env python3
"""Bounded regression checks for the read-only file-overlay classifier."""
from __future__ import annotations
import hashlib,json,tempfile
from pathlib import Path
from verify_overlay import classify

def tests()->list[dict]:
    h=lambda b:hashlib.sha256(b).hexdigest();res=[]
    with tempfile.TemporaryDirectory(prefix='ff12-overlay-') as name:
        root=Path(name).resolve();p=root/'x';r={'path':'x','before_sha256':h(b'old'),'after_sha256':h(b'new')}
        def check(name,want):
            actual=classify(root,r)['state'];assert actual==want,(name,actual);res.append({'name':name,'pass':True})
        check('missing_replacement','conflict');p.write_bytes(b'old');check('expected_preimage','expected_preimage')
        p.write_bytes(b'new');check('already_applied','already_applied');p.write_bytes(b'peer edit');check('peer_edit_preserved','conflict');assert p.read_bytes()==b'peer edit'
        p.unlink();r['before_sha256']=None;check('new_file','new_file');p.mkdir();check('directory_collision','conflict_nonfile');p.rmdir()
        for n,path in [('parent_escape','../escape'),('absolute_path','/tmp/escape'),('backslash_path','x\\escape')]:
            r['path']=path
            try:classify(root,r)
            except ValueError:res.append({'name':n,'pass':True})
            else:raise AssertionError(n)
    return res
if __name__=='__main__':print(json.dumps({'read_only':True,'controls':tests()},indent=2))
