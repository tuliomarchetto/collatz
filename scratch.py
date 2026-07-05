import sys
import os
sys.path.append(os.getcwd())
from collatz.tree import inverse_tree

def max_depth_to_cover(X: int, max_allowed_depth: int = 1000):
    reached = {1, 2}
    frontier = [2]
    uncovered = set(range(1, X + 1)) - reached
    
    depth = 0
    while uncovered and depth < max_allowed_depth:
        depth += 1
        nxt = []
        for m in frontier:
            kids = [2 * m]
            q, r = divmod(2 * m - 1, 3)
            if r == 0 and q % 2 == 1 and q > 0:
                kids.append(q)
            for c in kids:
                if c not in reached:
                    reached.add(c)
                    nxt.append(c)
                    uncovered.discard(c)
        frontier = nxt
        if not frontier:
            break
    
    return depth

for x in [10, 100, 1000, 10000]:
    print(f"X={x}, depth={max_depth_to_cover(x)}")
