from functools import reduce

def my_square(lst):
    return list(map(lambda x: x ** 2, lst))

def square(num):
    return num ** 2

def my_square2(lst):
    return list(map(square, lst))

def my_filter(lst):
    return list(filter(lambda x: x > 3, lst))

def mult(lst):
    prod = lst[0]
    for i in range(1, len(lst)):
        prod *= lst[i]
    return prod

def my_mult(list):
    return reduce(lambda x,y: x * y, n)

if __name__ == '__main__':
    n = [2, 3, 4, 8, 9]
    print(my_square(n))
    #other way
    print(my_square2(n))

    #filter
    print(my_filter(n))

    #reducer
    print(my_mult(n))