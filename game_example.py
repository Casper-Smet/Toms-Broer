#!/usr/bin/python3

import pygame
from AStar import *
from tkinter import *
import os
import platform
import re

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (55, 29, 124)
HEIGHT = WIDTH = 25
MARGIN = 0
WINDOW_SIZE = [499, 550]
screen = pygame.display.set_mode(WINDOW_SIZE)

# List with all locations of interest
lista = ['Robot arm','Snake','3D Printer','Soldeerplek','Server','Whiteboard','Werkbank']
dictionary = {'Robot arm': (2, 19), 'Snake': (9, 19), '3D Printer': (20, 14), 'Soldeerplek': (2, 14), 'Server': (2, 9), 'Whiteboard': (21, 7), 'Werkbank': (2, 19)}


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Return>", self.enter)

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def enter(self, event):

        counter = 0

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
        else:
            for q in dictionary:
                if entry.get() == q:
                    grid = matrix_reader()
                    counter = 1
                    end = dictionary['{}'.format(q)]
                    print(end)
                    path = dmain((8, 19), end)
                    print(path)
                    grid[8][19] = 2
                    grid[end[0]][end[1]] = 3

                    for x in range(1, len(path) - 1):
                        column = path[x][1]
                        row = path[x][0]
                        grid[row][column] = 4
                    print(grid)
                    for row in range(len(grid)):
                        for column in range(len(grid[0])):
                            print(row,column)
                            color = WHITE
                            if grid[row][column] == 2:
                                color = GREEN
                            if grid[row][column] == 3:
                                color = PURPLE
                            if grid[row][column] == 4:
                                color = BLUE
                            print(screen)
                            if color != WHITE:
                                pygame.draw.rect(screen, color,
                                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN,
                                                  WIDTH, HEIGHT])

            if counter == 0 :
                print('This location does not exist, please choose another')

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]


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
            print(screen)
            if color != WHITE:
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])



def game_main():

    BackGround = Background("maps/background-blueprintv3.png", [0, 0])

    # This sets the WIDTH and HEIGHT of each grid location
    # WIDTH = 13
    # HEIGHT = 33
    HEIGHT = WIDTH = 25  # Needs adjusting

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
# GUI
root = Tk()
logo = PhotoImage(file = "pictures/tomsbroer.PNG")
icon = root.wm_iconbitmap('pictures/icon.ico')
lowbanner = PhotoImage(file = "pictures/Banner.PNG")
root.title("Tom's Broer")
w, h =root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.config(bg= "white")
banner1 = Label(root, image = logo, width = 1920, bg = "#303135")
banner1.pack(pady=1)
banner2 = Label(root, image = lowbanner, bg = 'white')
banner2.pack( pady = 40, side = BOTTOM)
embed = Frame(root, width=499, height=550)
embed.pack(pady=1, side = LEFT)
entry = AutocompleteEntry(lista, root, width=25, font = ("Arial", 20))
entry.pack(pady=20, padx= 25,)
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

# http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
