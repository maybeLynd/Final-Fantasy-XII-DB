"""Labelled test-only catalogue reader substitution; unchanged producer Python."""
import argparse,io,runpy
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--catalog',required=True);a=p.parse_args()
source=Path(a.source).resolve();catalog=Path(a.catalog).resolve()
original=io.open;expected=(source.parents[3]/'Tools/work/graph/functions.tsv').resolve()
text=catalog.read_text('utf-8');lines=text.splitlines(keepends=True)
matched=[i for i,x in enumerate(lines) if x.startswith('002E45E0\t')];assert len(matched)==1
k=matched[0];parts=lines[k].rstrip('\r\n').split('\t');assert parts[:3]==['002E45E0','Movement_UpdateSteeringTowardTarget','963']
ending=lines[k][len(lines[k].rstrip('\r\n')):];parts[2]='40';lines[k]='\t'.join(parts)+ending
mutated=''.join(lines)
def controlled_open(file,*args,**kwargs):
 if Path(file).resolve()==expected:
  assert not args or args[0] in ('r','rt');return io.StringIO(mutated)
 return original(file,*args,**kwargs)
io.open=controlled_open
runpy.run_path(str(source),run_name='__main__')
