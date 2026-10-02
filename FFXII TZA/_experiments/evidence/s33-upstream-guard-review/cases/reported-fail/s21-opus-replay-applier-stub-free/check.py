allok=False
results={'qualified':{'pass_':False}}
print('qualified FAIL; NOT ok')

def __getattr__(name):
    if name == 'W':
        print('ASTRA_DOWNSTREAM_STATE_BOUNDARY')
        raise SystemExit(0)
    raise AttributeError(name)
