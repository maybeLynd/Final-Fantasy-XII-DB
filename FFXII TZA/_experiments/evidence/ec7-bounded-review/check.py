"""Two-case check of existing EC7 metadata validation, not FF12 execution."""
from pathlib import Path
import hashlib,importlib.util,json,sys,tempfile
source=Path('Database/Tools/analysis-kit/gfz-scripts/check_dispositions.py')
spec=importlib.util.spec_from_file_location('ec7_reviewed',source)
tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
rows=[]
with tempfile.TemporaryDirectory(prefix='astra_ec7_') as d:
 root=Path(d); page=root/'case.md'; members=root/'members.tsv'
 text='---\nstatus: DOCUMENTED\nfunction_families:\n  - "test | B | members.tsv | 2 | shared test shape; controlled metadata fixture only"\n---\n'
 page.write_text(text,encoding='utf-8')
 for label,values in [('unique-positive-control',[0x120010,0x120020]),('duplicate-member',[0x120010,0x120010])]:
  listing=''.join('%08X\n'%v for v in values)
  members.write_text(listing,encoding='utf-8')
  result=tool.evaluate(d,{0x120000:16,0x120010:16,0x120020:16},[str(page)])
  rows.append(dict(label=label,page=text,members=listing,result=result))
assert rows[0]['result']['B']==2 and rows[0]['result']['families_accepted']==1
defect=rows[1]['result']['families_accepted']==1 and rows[1]['result']['B']==1
record=dict(method='A: inspect and exercise existing metadata checker, not original FF12 instructions',checker_path=source.as_posix(),checker_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),reviewer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python=sys.version,fixture_census={'00120000':16,'00120010':16,'00120020':16},cases=rows,status='CONFIRMED_DUPLICATE_MEMBER_DEFECT' if defect else 'DUPLICATE_REFUSED',limits='No real family declared; no database census, game execution or weighted metric changed. This tests member cardinality, not semantic family validity or selector reproduction.')
out=Path(sys.argv[1]);assert not out.exists(),'Preserve original receipt'
out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(record['status'])
for r in rows:print(r['label'],r['result']['accepted'],'B=',r['result']['B'],'refused=',r['result']['families_refused'])
