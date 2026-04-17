import random
import heapq
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from collections import deque

# =========================================================
# 1. RANDOM MAZE GENERATION
# =========================================================

def generate_maze(rows, cols):
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if random.random() < 0.2:
                grid[i][j] = "#"
    grid[0][0] = "S"
    for _ in range(5):
        x = random.randint(1, rows-1)
        y = random.randint(1, cols-1)
        grid[x][y] = "F"
    return grid

# =========================================================
# 2. LOAD IMAGES 
# =========================================================

def load_image(path):
    if os.path.exists(path):
        return mpimg.imread(path)
    return None

pacman_img = load_image("pacman.png")
food_img = load_image("food.png")
wall_img = load_image("wall.png")

# =========================================================
# 3. BUILD ENVIRONMENT
# =========================================================

grid = generate_maze(10, 12)
rows, cols = len(grid), len(grid[0])
walls = set()
food = set()
start = (0, 0)

for i in range(rows):
    for j in range(cols):
        if grid[i][j] == "#":
            walls.add((i, j))
        elif grid[i][j] == "F":
            food.add((i, j))
        elif grid[i][j] == "S":
            start = (i, j)

# =========================================================
# 4. STATE + SUCCESSORS + HEURISTIC
# =========================================================

def get_successors(state):
    x, y, food_left = state
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    out = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in walls:
            new_food = set(food_left)
            if (nx, ny) in new_food:
                new_food.remove((nx, ny))
            out.append(((nx, ny, frozenset(new_food)), 1))
    return out

def heuristic(state):
    x, y, food_left = state
    if not food_left:
        return 0
    # Manhattan distance to the closest food
    return min(abs(x - fx) + abs(y - fy) for fx, fy in food_left)

# =========================================================
# 5. UNIFIED SEARCH ALGORITHM
# =========================================================

def run_search(start_state, method="astar"):
    method = method.lower()
    
    # frontier stores: (priority, current_g_score, current_state, path_history)
    # Note: BFS/DFS don't strictly need priority, but we use a unified structure.
    
    if method == "bfs":
        frontier = deque([(start_state, [])]) # Queue
    elif method == "dfs":
        frontier = [(start_state, [])] # Stack
    else:
        # Priority Queue for A* and Greedy
        frontier = []
        priority = heuristic(start_state)
        heapq.heappush(frontier, (priority, 0, start_state, []))

    visited = set()

    while frontier:
        # Pop based on method
        if method == "bfs":
            state, path = frontier.popleft()
        elif method == "dfs":
            state, path = frontier.pop()
        else:
            _, g, state, path = heapq.heappop(frontier)

        if len(state[2]) == 0: # Goal: All food eaten
            return path + [state]

        if state in visited:
            continue
        visited.add(state)

        for nxt, cost in get_successors(state):
            if nxt not in visited:
                new_path = path + [state]
                if method == "bfs":
                    frontier.append((nxt, new_path))
                elif method == "dfs":
                    frontier.append((nxt, new_path))
                elif method == "greedy":
                    heapq.heappush(frontier, (heuristic(nxt), 0, nxt, new_path))
                elif method == "astar":
                    new_g = g + cost
                    heapq.heappush(frontier, (new_g + heuristic(nxt), new_g, nxt, new_path))
    return []

# =========================================================
# 6. RUN SEARCH BASED ON INPUT
# =========================================================

print("Choose algorithm: bfs, dfs, greedy, astar")
choice = input("Enter choice: ").strip()

start_state = (start[0], start[1], frozenset(food))
solution = run_search(start_state, method=choice)

if not solution:
    print("No solution found!")
    exit()

# =========================================================
# 7. DRAW & ANIMATE
# =========================================================

def draw(ax, grid, agent_pos, food_left):
    ax.clear()
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks([])
    ax.set_yticks([])

    for i in range(rows):
        for j in range(cols):
            x, y = j, rows - i - 1
            if grid[i][j] == "#":
                if wall_img is not None:
                    ax.imshow(wall_img, extent=(x, x+1, y, y+1), zorder=1)
                else:
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color="black"))
            else:
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color="white", ec="gray", zorder=0))

    for (fx, fy) in food_left:
        x, y = fy, rows - fx - 1
        if food_img is not None:
            ax.imshow(food_img, extent=(x, x+1, y, y+1), zorder=2)
        else:
            ax.text(x+0.5, y+0.5, "🍒", ha="center", va="center")

    px, py = agent_pos
    x, y = py, rows - px - 1
    if pacman_img is not None:
        ax.imshow(pacman_img, extent=(x, x+1, y, y+1), zorder=3)
    else:
        ax.text(x+0.5, y+0.5, "😋", ha="center", va="center", fontsize=18)

fig, ax = plt.subplots()
def animate(i):
    if i < len(solution):
        x, y, food_left = solution[i]
        draw(ax, grid, (x, y), food_left)

ani = animation.FuncAnimation(fig, animate, frames=len(solution), interval=200, repeat=False)
plt.show()