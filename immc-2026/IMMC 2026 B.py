import sys
import statistics

# limit
sys.setrecursionlimit(10**9)

# input
R, C, B = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(R)]

# dfs
assigned = [[False]*C for _ in range(R)]
best_cost = float('inf')
best_labels = None
DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def in_bounds(r, c):
    return 0 <= r < R and 0 <= c < C

def find_unassigned():
    for r in range(R):
        for c in range(C):
            if grid[r][c] != 0 and not assigned[r][c]:
                return r, c
    return None

def explore_region(r, c, visited_local, cells, current_sum):
    yield (list(cells), current_sum)

    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if not in_bounds(nr, nc):
            continue
        if assigned[nr][nc] or (nr, nc) in visited_local:
            continue

        visited_local.add((nr, nc))
        cells.append((nr, nc))

        yield from explore_region(nr, nc, visited_local, cells, current_sum + grid[nr][nc])

        cells.pop()
        visited_local.remove((nr, nc))

labels = [[0]*C for _ in range(R)]
def backtrack(current_cost, region_id):
    global best_cost, best_labels

    # prune
    if current_cost >= best_cost:
        return

    start = find_unassigned()
    if start is None:
        # all assigned
        if current_cost < best_cost:
            best_cost = current_cost
            best_labels = [row[:] for row in labels]
        return

    r, c = start

    # try all connected regions
    visited_local = {(r, c)}
    cells = [(r, c)]

    for region_cells, region_sum in explore_region(r, c, visited_local, cells, grid[r][c]):
        cost = abs(region_sum - B)

        # assign
        for rr, cc in region_cells:
            assigned[rr][cc] = True
            labels[rr][cc] = region_id

        backtrack(current_cost + cost, region_id + 1)

        # undo
        for rr, cc in region_cells:
            assigned[rr][cc] = False
            labels[rr][cc] = 0

backtrack(0, 1)

# sum regions
region_sums = []
max_label = max(max(row) for row in best_labels)
for label in range(1, max_label + 1):
    s = 0
    for r in range(R):
        for c in range(C):
            if best_labels[r][c] == label:
                s += grid[r][c]
    region_sums.append(s)

# output
print("\nDrone assignments:")
for row in best_labels:
    print(" ".join(map(str, row)))

total_sum = sum(region_sums)
mean = total_sum / len(region_sums)
std_dev = statistics.stdev(region_sums)
print()
print(f'μ = {mean:.3f}')
print(f'σ = {std_dev:.3f}')