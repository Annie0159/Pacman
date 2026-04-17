# Pacman
<img width="626" height="462" alt="picture" src="https://github.com/user-attachments/assets/20229d2e-2d64-485e-9bfa-8d6294daa52a" />

This project simulates a Pacman-like agent navigating a randomly generated maze to collect food using different search algorithms.

The Goal: To demonstrate **AI search algorithms** in a visual and interactive environment.

## Algorithms Used

- **BFS**: Guarantees shortest path (in steps), but can be slower  
- **DFS**: Faster but not optimal  
- **Greedy**: Uses heuristic only (not always optimal)  
- **A\***: Optimal and efficient using cost + heuristic  

## Tech Stack

- **Language**: Python 3.x  
- **Libraries**:
  - matplotlib (visualization & animation)
  - numpy
  - heapq
  - collections (deque)
  - random, os

## Install Dependencies

```bash
pip install matplotlib numpy
```
## Run the Program
```bash
python main.py
```

## How it works
- A random maze is generated:<br>
  S → Start position (Pacman)<br>
  | → Walls<br>
  F → Food locations<br>
- Choose a search algorithm:bfs, dfs, greedy, astar<br>
- The agent:<br>
Finds a path<br>
Navigates the maze<br>
Collects all food<br>
Displays animated movement
