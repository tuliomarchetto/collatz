import sys
import os
import math
sys.path.append(os.getcwd())
from collatz.tree import inverse_tree

def analyze_tree(depth):
    reached, levels = inverse_tree(depth, cap=1_000_000)
    print("Depth:", depth)
    print("Nodes:", sum(levels))
    
def max_stopping_time(X):
    # This is equivalent to depth in inverse tree
    max_s = 0
    for n in range(1, X+1):
        s = 0
        curr = n
        while curr != 1:
            if curr % 2 == 0:
                curr //= 2
            else:
                curr = 3*curr + 1
            s += 1
        if s > max_s:
            max_s = s
    return max_s

print("Max depth for X=1000:", max_stopping_time(1000))
print("Max depth for X=10000:", max_stopping_time(10000))

from collatz.search import verify_range
r = verify_range(10000)
print(r.stopping_records[-1])
