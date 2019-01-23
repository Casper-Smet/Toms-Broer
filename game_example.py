#!/usr/bin/python3

import pygame
from AStar import *
from tkinter import *
import os
import platform

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def grid_draw(grid, screen, MARGIN, HEIGHT, WIDTH, BackGround):
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    PURPLE = (55, 29, 124)

    # Set the screen background
    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)

    # Draw the grid
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            color = WHITE
            #if grid[row][column] == 1:
                #color = RED
            if grid[row][column] == 2:
                color = GREEN
            if grid[row][column] == 3:
                color = PURPLE
            if grid[row][column] == 4:
                color = BLUE

            if color != WHITE:
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])



def game_main():

    BackGround = Background("maps/background-blueprintv3.png", [0, 0])

    # This sets the WIDTH and HEIGHT of each grid location
    #WIDTH = 13
    #HEIGHT = 33
    HEIGHT = WIDTH = 25 #Needs adjusting


    # This sets the margin between each cell
    MARGIN = 0

    # Create a 2 dimensional array based on binary map.
    grid = matrix_reader()

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [499, 550]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Initialize start and end_node
    start = end = tuple()

    # -------- Main Program Loop -----------
    while not done:
        #updates TKinter GUI
        root.update()
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                # Check if clicked space is first click.
                if grid[row][column] != 1:
                    if not start:
                       # assign colour to space
                        grid[row][column] = 2

                      # Assign coördinates of click to start variable.
                        start = (row, column)

                    # Check if clicked space is second click.
                    elif not end:

                        # Assign colour to space.
                        grid[row][column] = 3

                        # Assign coördinates of click to end variable.
                        end = (row, column)

                        # Start A* pathfinding with given coördinates. Return results to path variable.
                        path = dmain(start, end)

                        # Sets all coördinates in path to colour.
                        for x in range(1, len(path) - 1):
                            column = path[x][1]
                            row = path[x][0]
                            grid[row][column] = 4
                    # Print clicked coördinates (debug)
                    print("Click ", pos, "Grid coordinates: ", row, column)


        # Draw the grid.
        grid_draw(grid,screen, MARGIN, HEIGHT, WIDTH, BackGround)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
root = Tk()
root.title("Tom's Broer")
root.geometry('1280x720')
embed = Frame(root, width=499, height=550)
embed.grid(row=0, column=0, sticky=S)
txt = Entry(root, width=75)
txt.grid(row = 0, column = 200)
root.update()

# def pushed():
#     lbl = Label(root, text = 'Hello')
#     lbl.pack()
#     lbl.configure(text="Searched!")

if platform.system == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

pygame.quit()
game_main()