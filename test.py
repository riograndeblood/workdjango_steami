# from itertools import groupby
# l = [1,2,4,4,3,4,0,5,5,4]
# new = [i for i, _ in groupby(sorted(l))]
# print(new)
#
#
# x = [1,2,4,4,3,4,0,5,5,4]
# y = sorted(set(x), key=lambda d: x.index(d))
# print(y)


# def f(l):
#     n = []
#     for i in l:
#         if i not in n:
#             n.append(i)
#     return n
# print(f([1,2,4,4,3,4,0,5,5,4]))
#
#
# l = [1,2,4,4,3,4,0,5,5,4]
# n = []
# for i in l:
#     if i not in n:
#         n.append(i)
# print(n)


# a = []
# for i in range(1, 15):
#     a.append(i)
#     print(''.join(map(str, a)))

# def num(arr):
#     return sorted(arr, key=lambda x: x == 0)
#
# x = [1, 4, 0, -4, 5, 0, -10, 4, 0, 8]
# print(x)
# print(num(x))
#
# print('-------------')
# def num2(arr):
#     zerro = arr.count(0)
#     arr = [i for i in arr if i != 0]
#     arr.extend([0] * zerro)
#     return arr
# arr = [1, 4, 0, -4, 5, 0, -10, 4, 0, 8]
# print(arr)
# result = num2(arr)
# print(result)
#


def remove_char(s):
    return s[1:-1]

print(remove_char('This world'))
