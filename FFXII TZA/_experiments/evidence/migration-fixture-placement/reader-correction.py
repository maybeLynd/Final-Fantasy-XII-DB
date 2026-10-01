"""Rerun only affected reader observation; preserve original overall invalid status."""
import hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;ROOT=W.parents[4];old=W/'run-01';D=W/'reader-02';assert not D.exists();D.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
prior=json.loads((old/'raw.json').read_text());assert prior['finished'] is False and prior['fatal']['type']=='TypeError'
assert prior['driver_sha256']==sha((old/'driver.py').read_bytes())
assert len(prior['cases'])==4,'Missing retained producer controls'
source=old/'reader-source.py';assert source.read_bytes()==(ROOT/'Database/Tools/analysis-kit/gfz-scripts/check_questions.py').read_bytes()
raw={'method':'A affected original reader rerun only; no freezer control repetition','driver_sha256':sha(Path(__file__).read_bytes()),
     'prior_raw_sha256':sha((old/'raw.json').read_bytes()),'prior_overall_status':'INVALID_TYPEERROR_RETAINED',
     'source_sha256':sha(source.read_bytes()),'finished':False}
try:
 spec=importlib.util.spec_from_file_location('retained_original_reader',source)
 Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q)
 boxes=Q.read_boxes(str(old/'reader-root'))
 (D/'original-return-repr.txt').write_text(repr(boxes)+'\n')
 assert isinstance(boxes,list) and len(boxes)==1 and isinstance(boxes[0],tuple) and len(boxes[0])==5
 p,line,ticked,ids,label=boxes[0]
 assert isinstance(p,str) and isinstance(line,int) and isinstance(ticked,bool) and isinstance(ids,set) and isinstance(label,str)
 assert p=='04-Actor-Entity/control.md' and ids=={'W-999'} and not ticked
 raw['observation']={'file':p,'line':line,'ticked':ticked,'ids':sorted(ids),'label':label}
 E=ROOT/'Database/FFXII TZA/_experiments/evidence/migration-my-progress-independent'
 m=json.loads((E/'manifest.json').read_text())
 for x in m['members']:
  b=(E/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes']
 raw['all_published_members_unchanged']=True;raw['finished']=True
 (W/'freeze-after.py').write_bytes((ROOT/'Database/Tools/work/ASTRA/migration-my-progress-independent/freeze.py').read_bytes())
except BaseException as e:raw['fatal']={'type':type(e).__name__,'detail':str(e)};raise
finally:(D/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('READER_CORRECTION_ONE_OBSERVATION','W-999 retained; nested fixture absent; previous overall INVALID retained')
