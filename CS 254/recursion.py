# Dashiell Coyier HW D08

## Meta functions

# Recursive meta function


def recursive(x):
    if criterion(x):
        return base(x)
    else:
        prex = pre(x)
        recx = recursive(prex)
        return post(x, prex, recx)


# Iterative meta function


def iterative(x):
    stack = []
    while not criterion(x):  # storing all x and pre x until base case is found
        stack.append([x, pre(x)])
        x = pre(x)
    recx = base(x)  # compute base case, set this to the changing recx value
    while len(stack) > 0:
        val = stack.pop()
        recx = post(
            val[0], val[1], recx
        )  # iteratively call post() with changing values of recx to build up
    return recx


# Iterative-tail meta function


def iterativeTail(x):
    stack = []
    while not criterion(x):
        stack.append([x, pre(x)])
        x = pre(x)
    return base(x)
    # immediately return the base case (x value that met criterion and was not placed on stack)


# Twice recursive meta function


def recursive2(x):
    if criterion(x):
        return base(x)
    else:
        prex = pre(x)
        recx = recursive2(prex)
        midx = mid(x, prex, recx)
        recx2 = recursive2(midx)
        return post(x, prex, recx, midx, recx2)


## Factorial


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def criterion(x):
    if x == 0:
        return True
    return False


def base(x):
    return 1


def pre(x):
    return x - 1


def post(x, prex, recx):
    return x * recx


print(recursive(10))
print(factorial(10))
print(recursive(0))
print(factorial(0))
print(recursive(1))
print(factorial(1))
print(recursive(99))
print(factorial(99))


print(iterative(10))
print(factorial(10))
print(iterative(0))
print(factorial(0))
print(iterative(1))
print(factorial(1))
print(iterative(99))
print(factorial(99))


## Euclidean


def euclidean(ab):
    if ab[0] == 0:
        return ab[1]
    elif ab[1] == 0:
        return ab[0]
    else:
        return euclidean([ab[1], ab[0] % ab[1]])


def criterion(x):
    if (x[0] == 0) or (x[1] == 0):
        return True
    return False


def base(x):
    if x[0] == 0:
        return x[1]
    return x[0]


def pre(x):
    return [x[1], x[0] % x[1]]


def post(x, prex, recx):
    return recx


print(recursive([1, 1]))
print(euclidean([1, 1]))
print(recursive([5, 9]))
print(euclidean([5, 9]))
print(recursive([99, 914]))
print(euclidean([99, 914]))
print(recursive([100, 250]))
print(euclidean([100, 250]))

print(iterative([1, 1]))
print(euclidean([1, 1]))
print(iterative([5, 9]))
print(euclidean([5, 9]))
print(iterative([99, 914]))
print(euclidean([99, 914]))
print(iterative([100, 250]))
print(euclidean([100, 250]))


print(iterativeTail([1, 1]))
print(euclidean([1, 1]))
print(iterativeTail([5, 9]))
print(euclidean([5, 9]))
print(iterativeTail([99, 914]))
print(euclidean([99, 914]))
print(iterativeTail([100, 250]))
print(euclidean([100, 250]))


## Fibonacci


def fibonacci(n):
    # print(n)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def criterion(x):
    if x == 0 or x == 1:
        return True
    return False


def base(x):
    if x == 0:
        return 0
    return 1


def pre(x):
    return x - 1


def mid(x, prex, recx):
    return x - 2


def post(x, prex, recx, midx, recx2):
    return recx + recx2


print(recursive2(10))
print(fibonacci(10))
print(recursive2(0))
print(fibonacci(0))
print(recursive2(1))
print(fibonacci(1))
print(recursive2(26))
print(fibonacci(26))


## N choose k


def choose(nk):
    if nk[0] == 0 or nk[1] == 0 or nk[0] == nk[1]:
        return 1
    else:
        return choose([nk[0] - 1, nk[1]]) + choose([nk[0] - 1, nk[1] - 1])


def criterion(x):
    if x[0] == 0 or x[1] == 0 or x[0] == x[1]:
        return True
    return False


def base(x):
    return 1


def pre(x):
    return [x[0] - 1, x[1]]


def mid(x, prex, recx):
    return [x[0] - 1, x[1] - 1]


def post(x, prex, recx, midx, recx2):
    return recx + recx2


print(recursive2([1, 1]))
print(choose([1, 1]))
print(recursive2([9, 5]))
print(choose([9, 5]))
print(recursive2([10, 6]))
print(choose([10, 6]))
print(recursive2([15, 8]))
print(choose([15, 8]))
