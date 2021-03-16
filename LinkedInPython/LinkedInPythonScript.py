# Computing greatest common denominator of two number

def gcd(a, b):
    if a % b == 0:
        return b
    else:
        return gcd(b, (a % b))


print(gcd(100, 60))
print(gcd(20, 8))


# Lists in python are defined like: list = [] and they are equivalent to stack in java
# Queues in Python are named deque and can be imported from collections.
# Hashtable in Python is called dict e.g. items = dict({"key1" : 1, "key2" : 2}) or items = {}, items["key2"] = 2
# for key, value in items.items(): | for i in range(len(dataset) -1 , 0, 1)
#Sorting data: bubble Sort(not so good not efficient), merge sort(uses recursion), the quicksort
# floor divisor e.g. 5 // 2 = 2
