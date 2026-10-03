"""Run the immutable committed path controller with its explicit kit import path.

This supplies a dependency-resolution precondition; it does not repair/rewrite
the retained publisher or bypass the controller's private prerequisite checks.
"""
import hashlib,runpy,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
P=ROOT/'Database/FFXII TZA/_experiments/evidence/render-review-link-closure/drivers-v2'
pins={'control-publisher-path.py':'aae9e61c9cbe59097a3af5a897a361127404abc840d907899a8a18fb7d953699','publisher-driver.py':'5c1b458faeafcc4b206d30ba1ce660ceebd0e8dc54834f974931445490a6eb18'}
for name,pin in pins.items():
    if hashlib.sha256((P/name).read_bytes()).hexdigest()!=pin:raise ValueError('committed path-control dependency changed: '+name)
if len(sys.argv)!=2:raise ValueError('one fresh output path required')
sys.path.insert(0,str(ROOT/'Database/Tools/analysis-kit/gfz-scripts'))
sys.argv=[str(P/'control-publisher-path.py'),sys.argv[1]]
runpy.run_path(str(P/'control-publisher-path.py'),run_name='__main__')
