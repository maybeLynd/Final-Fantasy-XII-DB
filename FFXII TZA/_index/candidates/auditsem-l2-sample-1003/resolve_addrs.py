import sys
sys.path.insert(0, r'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts')
import contract_named_state_census as C
spans, fields, sizes = C.load_store()
for a in sys.argv[1:]:
    print(a, C.resolve(int(a, 16), spans, fields, sizes))
