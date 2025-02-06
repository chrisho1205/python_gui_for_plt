import numpy as np 
list1=[1,2,3]
list2=np.array(list1)
magnitude = np.linalg.norm(list1)
list3= list2 / magnitude
print(list3)