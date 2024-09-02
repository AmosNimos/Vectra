import os

# Rectangular cuboid model with different lengths on each axis
vertices = [
    (0, 0, 0),  # Vertex 0
    (2, 0, 0),  # Vertex 1
    (2, 3, 0),  # Vertex 2
    (0, 3, 0),  # Vertex 3
    (0, 0, 4),  # Vertex 4
    (2, 0, 4),  # Vertex 5
    (2, 3, 4),  # Vertex 6
    (0, 3, 4)   # Vertex 7
]

# Edges defining the cube (pairs of vertex indices)
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom square
    (4, 5), (5, 6), (6, 7), (7, 4),  # Top square
    (0, 4), (1, 5), (2, 6), (3, 7)   # Vertical lines
]

# Global state
view_axis = 'Z'  # Default top-down view
scale = 1         # Grid scale
camera_x = 0      # Camera position on the x-axis
camera_y = 0      # Camera position on the y-axis
camera_z = 0      # Camera position on the z-axis
selected = 0

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def interpolate(p1, p2):
    """Generate points along a line between two vertices."""
    x1, y1 = p1
    x2, y2 = p2
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        return [(x1, y1)]

    x_step = dx / steps
    y_step = dy / steps

    x, y = x1, y1
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_step
        y += y_step

    return points

def render_grid(vertices, edges, axis, scale, camera_x, camera_y, camera_z, selected):
    """Render the ASCII grid based on current view axis and scale."""
    grid_size = 20
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    for edge in edges:
        v1, v2 = edge
        if axis == 'Z':
            p1 = ((vertices[v1][0] - camera_x) // scale, (vertices[v1][1] - camera_y) // scale)
            p2 = ((vertices[v2][0] - camera_x) // scale, (vertices[v2][1] - camera_y) // scale)
        elif axis == 'X':
            p1 = ((vertices[v1][1] - camera_y) // scale, (vertices[v1][2] - camera_z) // scale)
            p2 = ((vertices[v2][1] - camera_y) // scale, (vertices[v2][2] - camera_z) // scale)
        elif axis == 'Y':
            p1 = ((vertices[v1][0] - camera_x) // scale, (vertices[v1][2] - camera_z) // scale)
            p2 = ((vertices[v2][0] - camera_x) // scale, (vertices[v2][2] - camera_z) // scale)

        for x, y in interpolate(p1, p2):
            x, y = int(x), int(y)
            if 0 <= x < grid_size and 0 <= y < grid_size:
                if x == p1[0] and x == p2[0]: 
                    grid[y][x] = '│'  # Mark edge point with box-drawing char
                elif y == p1[1] and y == p2[1]:
                    grid[y][x] = '─'  # Mark edge point with box-drawing char
                else:
                    grid[y][x] = '.' 

    cursor_in_view = False
    for index, vertex in enumerate(vertices):
        if axis == 'Z':
            x, y = (vertex[0] - camera_x) // scale, (vertex[1] - camera_y) // scale
        elif axis == 'X':
            x, y = (vertex[1] - camera_y) // scale, (vertex[2] - camera_z) // scale
        elif axis == 'Y':
            x, y = (vertex[0] - camera_x) // scale, (vertex[2] - camera_z) // scale
        x, y = int(x), int(y)

        if 0 <= x < grid_size and 0 <= y < grid_size:
            if selected == index:
                cursor_in_view = True
                grid[y][x] = '★'  # Highlight the selected vertex
            else:
                grid[y][x] = '•'  # Mark vertex with a box-drawing character

    if not cursor_in_view:
        selected = 0  # Reset to the first vertex if no vertex is in view

    for row in grid:
        print(''.join(row))

def main():
    global view_axis, scale, camera_x, camera_y, camera_z, selected

    while True:
        clear_screen()
        print(f"View Axis: {view_axis}, Scale: {scale}, Camera: ({camera_x}, {camera_y}, {camera_z})")
        print("+----------------------+")
        render_grid(vertices, edges, view_axis, scale, camera_x, camera_y, camera_z, selected)
        print("+----------------------+")
        print("Commands: (v) View Axis, (s) Scale, (x,y,z) Camera Position, (b) Next Vertex, (q) Quit")
        command = input("> ").lower()

        # View Axis
        if command.startswith('v'):
            if len(command) > 1 and command[1] in ('x', 'y', 'z'):
                view_axis = command[1].upper()  # Set view axis from command
            else:
                view_axis = input("Enter new view axis (X/Y/Z): ").strip().upper()
                if view_axis not in ('X', 'Y', 'Z'):
                    view_axis = 'Z'  # Default to Z if input is invalid
        # Camera Axis Position
        elif command.startswith('c'):
            axis = command[1] if len(command) > 1 else None
            value = command[2:] if len(command) > 2 else None

            if axis in ('x', 'y', 'z'):
                if value:
                    try:
                        value = int(value)
                        if axis == 'x':
                            camera_x = value
                        elif axis == 'y':
                            camera_y = value
                        elif axis == 'z':
                            camera_z = value
                    except ValueError:
                        print("Invalid value. Position not set.")
                else:
                    # Prompt for the camera position if no value provided
                    pos = input(f"Enter new camera {axis.upper()} position (integer): ")
                    try:
                        if axis == 'x':
                            camera_x = int(pos)
                        elif axis == 'y':
                            camera_y = int(pos)
                        elif axis == 'z':
                            camera_z = int(pos)
                    except ValueError:
                        print("Invalid position. Setting to 0.")
                        if axis == 'x':
                            camera_x = 0
                        elif axis == 'y':
                            camera_y = 0
                        elif axis == 'z':
                            camera_z = 0
            else:
                print("Invalid axis. Use 'x', 'y', or 'z'.")

        # Scale
        elif command.startswith('s'):
            scale = int(command[1:]) if len(command) > 1 else None
            if scale is None:
                try:
                    scale = int(input("Enter new scale (positive integer): "))
                    if scale <= 0:
                        scale = 1  # Reset to 1 if invalid scale
                except ValueError:
                    scale = 1
        elif command.startswith('x'):
            offset_x = int(command[1:]) if len(command) > 1 else None
            if offset_x is None:
                try:
                    camera_x = int(input("Enter new camera X position (integer): "))
                except ValueError:
                    camera_x = 0
            else:
                camera_x += offset_x
        elif command == 'y':
            try:
                camera_y = int(input("Enter new camera Y position (integer): "))
            except ValueError:
                camera_y = 0
        elif command == 'z':
            try:
                camera_z = int(input("Enter new camera Z position (integer): "))
            except ValueError:
                camera_z = 0
        elif command == 'b':
            selected = (selected + 1) % len(vertices)  # Cycle through vertices
        elif command == 'q' or command == 'exit' or command == 'quit':
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
