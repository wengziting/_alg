def my_map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])

def my_filter(pred, lst):
    if not lst:
        return []
    head, *tail = lst
    return ([head] if pred(head) else []) + my_filter(pred, tail)

def my_reduce(func, lst, initializer=None):
    if initializer is None:
        if not lst:
            raise TypeError("my_reduce() of empty sequence with no initial value")
        return my_reduce(func, lst[1:], lst[0])
    if not lst:
        return initializer
    return my_reduce(func, lst[1:], func(initializer, lst[0]))

    def bubble_pass(lst):
    def step(acc, val):
        if not acc:
            return [val]
        prev = acc[:-1]
        last = acc[-1]
        if last > val:
            return prev + [val, last]
        else:
            return acc + [val]
            
    return my_reduce(step, lst, [])

def bubble_sort(lst, n=None):
    if n is None:
        n = len(lst)
    if n <= 1:
        return lst

    return bubble_sort(bubble_pass(lst), n - 1)


data = [64, 34, 25, 12, 22, 11, 90]

print("my_map (平方):", my_map(lambda x: x**2, [1, 2, 3, 4]))
print("my_filter (偶數):", my_filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
print("my_reduce (累加):", my_reduce(lambda x, y: x + y, [1, 2, 3, 4], 0))

print("\n原始陣列:", data)
print("泡沫排序後:", bubble_sort(data))
