def own_print(foo): return lambda x: foo+' it\'s '+x

func = own_print('foo')

#func('bar')
print(func('bar'))