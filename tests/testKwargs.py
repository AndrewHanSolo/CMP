def table_things(track, **kwargs):
	for name, value in kwargs.items():
		print (track, name, value)
	if "pear" in kwargs:
		print("hit")

table_things('question', apple = 'fruit', cabbage = 'vegetable')


funcDict = {'table': table_things}

for key, func in funcDict.items():
	func('quiz', pear = 'a', asd = 'd')