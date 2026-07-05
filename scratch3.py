import sys
import os
sys.path.append(os.getcwd())
from collatz.tree import inverse_tree

def empirical_bounds(depth):
    reached = {1, 2}
    frontier = [2]
    
    for d in range(1, depth + 1):
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
        frontier = nxt
        if frontier:
            print(f"Depth {d}: min={min(frontier)}, max={max(frontier)}")

empirical_bounds(30)
