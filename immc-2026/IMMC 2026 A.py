import heapq

# input
R, C, A = map(int, input().split())
T = [list(map(float, input().split())) for _ in range(R)]

# build count grid
count = [[0 for _ in range(C)] for _ in range(R)]

# build heap (negative values for max heap behaviour)
heap = []
for i in range(R):
    for j in range(C):
        heapq.heappush(heap, (-T[i][j], i, j))

# ranger function
def f(x):
    return 0.5 * x

# assignment
for _ in range(A):
    neg_val, i, j = heapq.heappop(heap)
    val = -neg_val

    new_val = f(val)
    T[i][j] = new_val
    count[i][j] += 1

    heapq.heappush(heap, (-new_val, i, j))

# output
print()
print('Ranger assignments:')
for row in count:
    print(*row)

print()
print('Updated T(x,y):')
for row in T:
    print(' '.join(f'{val:.3f}' for val in row))

