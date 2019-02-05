import time

def fib_R(n):
    if n == 1 or n == 2:
        result = 1
    else:
        result = fib_RM(n-1) + fib_RM(n-2) # , memo = memo
        
    return result

def fib_RM(n, memo = {}):
    if n in memo:
        return memo[n]
    if n == 1 or n == 2:
        memo[n] = 1 # result = 1
    else:
        # result = fib_RM(n-1, memo = memo) + fib_RM(n-2, memo = memo) # , memo = memo
        memo[n] = fib_RM(n-1, memo = memo) + fib_RM(n-2, memo = memo)
        
    # memo[n] = result
    # return result
    return memo[n]

def fib_BU(n):
    if n == 1 or n == 2:
        return 1
    BU = [None] * (n+1)
    BU[1] = 1
    BU[2] = 1
    for i in range(3,n+1):
        BU[i] = BU[i-1] + BU[i-2]
    return BU[n]


val = 1000
t1 = time.time()
print (fib_R(val))
t2 = time.time()
print ('\t',t2-t1)
print ('')

print (fib_RM(val))
t3 = time.time()
print ('\t',t3-t2, (t2-t1)/(t3-t2))
print ('')

t4 = time.time()
print (fib_BU(val))
print ('\t',t4-t3, (t2-t1)/(t4-t3), (t3-t2)/(t4-t3))
print ('')

