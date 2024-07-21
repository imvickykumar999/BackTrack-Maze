from ursina import *
import random
import time

app = Ursina()

# Define maze dimensions
maze_width = 15
maze_height = 11

# Create a grid to represent the maze
maze = [[0 for x in range(maze_width)] for y in range(maze_height)]

# Initialize player position
player_pos = [1, 1]

# Create a list to keep track of the path taken
path = []

# Function to create a perfect maze with DFS
def create_maze():
    stack = [(1, 1)]
    visited = set((1, 1))
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    
    while stack:
        current = stack[-1]
        y, x = current
        maze[y][x] = 1

        unvisited_neighbors = []
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 1 <= ny < maze_height-1 and 1 <= nx < maze_width-1 and (ny, nx) not in visited:
                unvisited_neighbors.append((ny, nx))

        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            ny, nx = next_cell
            visited.add((ny, nx))
            stack.append(next_cell)
            
            # Knock down wall between current and next
            wall_y, wall_x = (y + ny) // 2, (x + nx) // 2
            maze[wall_y][wall_x] = 1
        else:
            stack.pop()

# Draw the maze
def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 0:
                block = Entity(model='quad', color=color.black, position=(x, y, 0), scale=(0.9, 0.9, 0.9))
                block.original_color = color.black
            else:
                block = Entity(model='quad', color=color.white, position=(x, y, 0), scale=(0.9, 0.9, 0.9))
                block.original_color = color.white
            maze[y][x] = block

create_maze()
draw_maze()

# Set the camera to view the entire maze
camera.orthographic = True
camera.fov = max(maze_width, maze_height) * 0.6
camera.position = (maze_width / 2 - 0.5, maze_height / 2 - 0.5)

# Movement delay setup
move_delay = 0.2  # Time in seconds between movements
last_move_time = time.time()

# Function to update the player's position
def update():
    global player_pos, path, last_move_time
    
    current_time = time.time()
    if current_time - last_move_time < move_delay:
        return
    
    new_pos = player_pos[:]

    if held_keys['w']:
        new_pos = [player_pos[0], player_pos[1] + 1]
    elif held_keys['s']:
        new_pos = [player_pos[0], player_pos[1] - 1]
    elif held_keys['a']:
        new_pos = [player_pos[0] - 1, player_pos[1]]
    elif held_keys['d']:
        new_pos = [player_pos[0] + 1, player_pos[1]]
    else:
        return

    # Check if new position is within maze bounds and different from current position
    if new_pos != player_pos and 0 <= new_pos[0] < maze_width and 0 <= new_pos[1] < maze_height:
        # Check if the new position is not a wall
        if maze[new_pos[1]][new_pos[0]].original_color != color.black:
            # Check if the new position is not the same as the last position (backtracking)
            if new_pos in path:
                maze[player_pos[1]][player_pos[0]].color = maze[player_pos[1]][player_pos[0]].original_color
                path.pop()
            else:
                path.append(player_pos[:])
                maze[player_pos[1]][player_pos[0]].color = color.red

            player_pos = new_pos
            maze[player_pos[1]][player_pos[0]].color = color.green
            last_move_time = current_time

# Initial player position
maze[player_pos[1]][player_pos[0]].color = color.green

app.run()
