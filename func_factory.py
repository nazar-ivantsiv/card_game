def own_print(foo): 
	return lambda x: foo+' its '+x

func = own_print('foo')

#func('bar')
print(func('bar'))

'''
def my_name(name1):
	def i_am(name2):
		print(name1)
return i_am

func = my_name('foo')
func('bar')
'''
