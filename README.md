# `BackTrack Maze`

To create a 2D maze game in Ursina where the player moves using the A, S, W, D keys, and the blocks change colors to indicate paths taken and backtracking, you can follow these steps:

1. Set up the Ursina environment.
2. Create a grid representing the maze.
3. Implement player movement and color-changing logic for marking paths and backtracking.

Here's a basic implementation:

```python
from ursina import *

app = Ursina()

# Define maze dimensions
maze_width = 10
maze_height = 10

# Create a grid to represent the maze
maze = [[0 for x in range(maze_width)] for y in range(maze_height)]

# Initialize player position
player_pos = [0, 0]

# Create a list to keep track of the path taken
path = []

# Create a function to draw the maze
def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            block = Entity(model='quad', color=color.white, position=(x, y, 0), scale=(0.9, 0.9, 0.9))
            block.original_color = color.white
            maze[y][x] = block

# Draw the initial maze
draw_maze()

# Function to update the player's position
def update():
    global player_pos, path
    
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

    # Check if new position is within maze bounds
    if 0 <= new_pos[0] < maze_width and 0 <= new_pos[1] < maze_height:
        # Check if the new position is not the same as the last position (backtracking)
        if new_pos in path:
            maze[player_pos[1]][player_pos[0]].color = maze[player_pos[1]][player_pos[0]].original_color
            path.pop()
        else:
            path.append(player_pos[:])
            maze[player_pos[1]][player_pos[0]].color = color.red

        player_pos = new_pos
        maze[player_pos[1]][player_pos[0]].color = color.green

# Initial player position
maze[player_pos[1]][player_pos[0]].color = color.green

app.run()
```

### Explanation:
1. **Setup**: Import Ursina, define the maze dimensions, and initialize the player's position and path tracking list.
2. **Drawing the Maze**: The `draw_maze` function creates a grid of blocks to represent the maze.
3. **Player Movement**: The `update` function checks for key presses (W, A, S, D) to move the player. It updates the player's position, marks the current block as red if it's a new path, and reverts the block to its original color if the player backtracks.

### Running the Game:
1. Install Ursina: `pip install ursina`
2. Save the script to a file, e.g., `maze_game.py`.
3. Run the script: `python maze_game.py`.

You can expand this basic example by adding more features, such as walls, a start and end point, and more complex maze generation algorithms.
