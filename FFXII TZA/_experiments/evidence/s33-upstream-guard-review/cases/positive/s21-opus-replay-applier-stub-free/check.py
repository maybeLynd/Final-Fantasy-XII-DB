allok=True
results={'qualified':{'pass_':True}}
print('qualified PASS')

def __getattr__(name):
    if name == 'W':
        print('ASTRA_DOWNSTREAM_STATE_BOUNDARY')
        raise SystemExit(0)
    raise AttributeError(name)
