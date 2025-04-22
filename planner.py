import sys
import heapq # Priority queue for uniform-cost search

# successors function to generate possible actions
def successors(state: tuple[any, any, frozenset], grid: list[list]) -> list:
    row, col, dirty = state
    actions = []
    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }

    for action, (dr, dc) in directions.items():
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '#':
            actions.append((action, (nr, nc, dirty)))

    # Vacuum
    if (row, col) in dirty:
        new_dirty = dirty - {(row, col)}
        actions.append(('V', (row, col, new_dirty)))

    return actions

# uniform-cost search algorithm
# function uses a priority queue to explore the least costly path first
def uniform_cost_search(grid: list[list], start_pos: tuple[int, int], dirty_cells: set) -> list:
    start_state = (start_pos[0], start_pos[1], frozenset(dirty_cells)) #frozenset to make it hashable
    frontier = [(0, [], start_state)]  # (cost, path, state)
    visited = set()
    
    nodes_generated = 1
    nodes_expanded = 0

    while frontier:
        cost, path, state = heapq.heappop(frontier)

        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if not state[2]:  # No more dirty cells
            return [path, nodes_generated, nodes_expanded]

        for action, next_state in successors(state, grid):
            heapq.heappush(frontier, (cost + 1, path + [action], next_state))
            nodes_generated += 1

    return [None, nodes_generated, nodes_expanded]

# depth-first search algorithm  
# function uses a stack to explore the deepest nodes first then backtracks
def depth_first_search(grid: list[list], start_pos: tuple[int, int], dirty_cells: set) -> list:
    start_state = (start_pos[0], start_pos[1], frozenset(dirty_cells)) #frozenset to make it hashable
    stack = [(start_state, [])]
    visited = set()

    nodes_generated = 1
    nodes_expanded = 0

    while stack:
        state, path = stack.pop()

        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        if not state[2]:
            return [path, nodes_generated, nodes_expanded]

        for action, next_state in reversed(successors(state, grid)):
            stack.append((next_state, path + [action]))
            nodes_generated += 1

    return [None, nodes_generated, nodes_expanded]

# Function to initialize the world
def initialize_world(world: str) -> list:
    with open(world, 'r') as file:
        vaccuum_world = file.readlines()
    vaccuum_world = [line.strip() for line in vaccuum_world] # [0] = width, [1] = height
    return vaccuum_world

# Main function to execute the vacuum robot planner
def main(algo: str, world: str):
    if algo not in ["depth-first", "uniform-cost"]:
        print("Invalid algorithm. Please use 'depth-first' or 'uniform-cost'.")
        return
    
    vacuum_world = initialize_world(world)
    cols = int(vacuum_world[0])
    rows = int(vacuum_world[1])
    vacuum_world = vacuum_world[2:] # remove the first two lines

    vacuum_world = [list(line) for line in vacuum_world] # convert to matrix
    dirty_cells = set()

    for r in range(rows):
        for c in range(cols):
            char = vacuum_world[r][c]
            if char == '@':
                r_pos = (r, c) # robot position
            elif char == '*':
                dirty_cells.add((r, c))
    
    if algo == "depth-first":
         # depth-first search algorithm
        search = depth_first_search(vacuum_world, r_pos, dirty_cells)
    elif algo == "uniform-cost":
        # uniform-cost search algorithm
        search = uniform_cost_search(vacuum_world, r_pos, dirty_cells)
    
    path = search[0] # path to the solution
    generated = search[1] # number of nodes generated
    expanded = search[2] # number of nodes expanded
    if path is None:
        print("No solution found.")
        return

    for move in path:
        print(move)
    print(f"{generated} nodes generated")
    print(f"{expanded} nodes expanded") 


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [ algorithm ] [ world-file ]")
        sys.exit(1)
    algorithm = sys.argv[1]
    world = sys.argv[2]
    main(algorithm, world)