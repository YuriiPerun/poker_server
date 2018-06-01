list1=[lambda x,y: 2*x**2-x, lambda x,y:x+y-1]
print(list1)
list1=[e(1,2) for e in list1]
print(list1)
list1.append(['bb',5])
print(list1)
list1.extend(['aa',1])
print(list1)
list1.remove(2)
print(list1)
list1.pop(2)
print(list1)
list1.index(1)
print(list1)
list1+='rr'
print(list1)
list1=list1[0:-1:1]
print(list1)