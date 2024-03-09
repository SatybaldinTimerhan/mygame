lst = ['a', 1, 2, '3', '4', 'r']
new_lst = []    
for element in lst:
    if isinstance(element, int):
        new_lst.append(element)
lst = new_lst
print(lst)  