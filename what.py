from datetime import datetime
i=datetime.now() 
print str(i)
x= i.strftime('%Y/%m/%d %H:%M:%S')
print x

print type(x)
