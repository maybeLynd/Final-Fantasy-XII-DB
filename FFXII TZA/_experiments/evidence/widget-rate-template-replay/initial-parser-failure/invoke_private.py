import sys
from pathlib import Path
w=Path(__file__).resolve().parent
spec=__import__('json').loads((w/'invocation.json').read_text())
source=(w/'retained/producer.py').read_text()
needle='FI = os.path.join(DB, "_types", "fields.tsv")'
assert source.count(needle)==1
fixture=Path(sys.argv[1]).resolve()
assert fixture.parent==w/'disposable' and fixture.name in ('legacy.tsv','current.tsv')
transformed=source.replace(needle,'FI = '+repr(str(fixture)))
sys.argv=[spec['original_file'],*sys.argv[2:]]
exec(compile(transformed,spec['original_file'],'exec'),{'__file__':spec['original_file'],'__name__':'__main__'})
