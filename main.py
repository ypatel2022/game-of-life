# imports
import pygame
from random import *

# Initialize pygame
pygame.init()

# Define some colors
DARK = (39, 51, 63)
LIGHT = (88, 183, 165)

# WIDTH and HEIGHT of each cell
WIDTH = 15
HEIGHT = 15

# Frames Per second
FPS = 60
GAME_FPS = 1.5

# store if game has started or not
started = False

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [495, 495]
screen = pygame.display.set_mode(WINDOW_SIZE)

# cols and rows
ROWS = int(WINDOW_SIZE[0] / HEIGHT)
COLS = int(WINDOW_SIZE[1] / WIDTH)


# current generation
current_gen = 0


def make_grid(randomized=False):
    # make and return array

    temp_grid = []

    for row in range(ROWS):
        # Add an empty array that will hold each cell in this row
        temp_grid.append([])
        for col in range(COLS):

            if not randomized:
                # 0 is dead, every cell is dead by default
                temp_grid[row].append(0)

            else:
                # randomized cell
                # 0 = dead, 1 = alive
                state = randint(0, 1)
                temp_grid[row].append(state)

    return temp_grid


# Create starting grid
grid = make_grid()


# Loop until the user clicks the exit button on window options
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def print_grid():
    # print grid on terminal
    for row in range(ROWS):
        for col in range(COLS):

            if (col < COLS - 1):
                print(grid[row][col], end=" ")

            else:
                print(grid[row][col])

    print("\n---------------------------------\n")


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):

            # if cell is dead, then set to black
            if grid[row][col] == 0:
                color = DARK

            # if cell is alive, then set to white
            else:
                color = LIGHT

            # make and draw rect on screen
            pygame.draw.rect(
                screen, color, [WIDTH * col, HEIGHT * row, WIDTH, HEIGHT])

    # print_grid()


# -------- Main Program Loop --------
while not done:

    # User events
    for event in pygame.event.get():

        # If user clicked X on window options
        if event.type == pygame.QUIT:
            # We are done so we exit this loop
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN and not started:

            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()

            # Change the x/y screen coordinates to grid coordinates
            col = pos[0] // WIDTH
            row = pos[1] // HEIGHT

            # Change state of cell
            # grid[row][col] = not grid[row][col]
            if grid[row][col] == 1:
                grid[row][col] = 0
            else:
                grid[row][col] = 1

            # print which cell is clicked
            # print("Grid coordinates: ", row, col)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not started:
                # change window title
                pygame.display.set_caption(
                    "Conway's Game Of Life")
                # game started to true
                started = True

            # to restart game
            if event.key == pygame.K_r:
                grid = make_grid()
                started = False
                current_gen = 0

    # Set the screen background
    screen.fill(DARK)

    # default window title
    pygame.display.set_caption("Conway's Game Of Life | Press Enter To Start")

    # next generation
    # only start game if start key is pressed
    if started:

        temp_grid = make_grid()

        # Set title of window when game is on
        pygame.display.set_caption("Generation " + str(current_gen))

        for row in range(ROWS):
            for col in range(COLS):
                # store num of neighbours
                n = 0

                # to prevent index out of range errors
                top = row > 0
                bottom = row < (ROWS - 1)
                left = col > 0
                right = col < (COLS - 1)

                # top left
                if top and left and grid[row - 1][col - 1] == 1:
                    n += 1

                # top
                if top and grid[row - 1][col] == 1:
                    n += 1

                # top right
                if top and right and grid[row - 1][col + 1] == 1:
                    n += 1

                # left
                if left and grid[row][col - 1] == 1:
                    n += 1

                # right
                if right and grid[row][col + 1] == 1:
                    n += 1

                # bottom left
                if bottom and left and grid[row + 1][col - 1] == 1:
                    n += 1

                # bottom
                if bottom and grid[row + 1][col] == 1:
                    n += 1

                # bottom right
                if bottom and right and grid[row + 1][col + 1] == 1:
                    n += 1

                # --- RULE CHECKING ---

                # Rule 1
                # Any live cell with two or three live neighbours survives.
                if (grid[row][col] == 1 and (n == 2 or n == 3)):

                    # stay alive
                    # print("stay alive")
                    temp_grid[row][col] = 1

                # Rule 2
                # Any dead cell with three live neighbours becomes a live cell.
                elif (grid[row][col] == 0 and n == 3):

                    # become alive
                    # print("become alive")
                    temp_grid[row][col] = 1

                # Rule 3
                # All other live cells die in the next generation. Similarly, all other dead cells stay dead.
                # elif (grid[row][col] == 1):
                else:

                    # die
                    # print("die")
                    temp_grid[row][col] = 0

        # set original grid to new grid
        grid = temp_grid
        current_gen += 1

    # Draw the grid
    draw_grid()

    # Limit to FPS frames per second
    if not started:
        clock.tick(FPS)
    else:
        clock.tick(GAME_FPS)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()


# IDLE editor friendly
pygame.quit()
