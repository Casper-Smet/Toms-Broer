"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
import csv as c
from AStar import *


def matrix_reader():
    with open(r"maps/mapmatrix02v3.txt", "r") as map:
        reader = c.reader(map)
        matrix = list()
        i = 0
        for row in reader:
            i += 1
            new_row = list()
            for x in row:
                new_row.append(int(x))
            #print(i)
            #addition = [e for e in row if e]
            #print(addition)
            matrix.append(list(new_row))
    better = [e for e in matrix if e]
    #print(better[15][80])
    return(better)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (55, 29, 124)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = matrix_reader()
"""for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell"""

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
#grid[1][5] = 1

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [630, 332]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#Initialize start and end_node
start = end = tuple()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            if not start:
                grid[row][column] = 2
                start = (row, column)
            elif not end:
                end = (row, column)
                grid[row][column] = 3
                path = dmain(start, end)
                for x in range(1,len(path)-1):
                    column = path[x][1]
                    row = path[x][0]
                    grid[row][column] = 4
            # Set that location to one
            print("Click ", pos, "Grid coordinates: ", row, column)
        #if start and end and event.type == pygame.MOUSEBUTTONDOWN:
         #   dmain(start,end)

            # break

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(13):
        for column in range(25):
            color = WHITE
            if grid[row][column] == 1:
                color = RED
            if grid[row][column] == 2:
                color = GREEN
            if grid[row][column] == 3:
                color = PURPLE
            if grid[row][column] == 4:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])


    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()