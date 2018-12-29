a=[]
print a
print id(a)

a.extend([1,2,3,1,])
print a
print id(a)
del a
a=[]
print a
print id(a)
a.extend([1,2,3,1,])
print a
print id(a)