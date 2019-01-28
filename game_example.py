#!/usr/bin/python3

import pygame, os, platform, re, time
from AStar import *
from tkinter import *
from triangulation import *

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
lista = ['Robotarm','Snake','3D Printer','Soldeerplek','Server','Whiteboard','Werkbank']
dictionary = {'Robotarm': (2, 19), 'Snake': (9, 19), '3D Printer': (20, 14), 'Soldeerplek': (2, 14), 'Server': (2, 9), 'Whiteboard': (21, 7), 'Werkbank': (2, 19)}

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self['textvariable']
        if self.var == '':
            self.var = self['textvariable'] = StringVar()

        self.var.trace('w', self.changed)
        self.bind('<Right>', self.selection)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)
        self.bind('<Return>', self.enter)

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
                    self.lb.bind('<Double-Button-1>', self.selection)
                    self.lb.bind('<Right>', self.selection)
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
        grid = matrix_reader()
        current_location = location_convert()
        counter = 0
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

        elif type(current_location) == list:
            #grid = matrix_reader()
            start = location_convert()
            """for x in range(1, len(grid) -1):
                for i in (1, len(grid[0])-1):
                    if grid[x][i] == 4:
                        grid[x][i] = 0"""
            for q in dictionary:
                if entry.get() == q:
                    counter = 1
                    end = dictionary['{}'.format(q)]
                    print(end)
                    path = dmain(start, end)
                    print(path)
                    grid[end[0]][end[1]] = 3

                    for x in range(1, len(path) - 1):
                        column = path[x][1]
                        row = path[x][0]
                        grid[row][column] = 4
                        print(grid[row][column])
                    print('Regel 147:    ', grid)
                    grid_draw(grid)
            if counter == 0:
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

def grid_draw(grid):
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [499, 550]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    BackGround = Background('maps/background-blueprintv3.png', [0, 0])

    # This sets the WIDTH and HEIGHT of each grid location
    # WIDTH = 13
    # HEIGHT = 33
    HEIGHT = WIDTH = 25  # Needs adjusting

    current_location = location_convert()
    start = current_location
    grid[start[0]][start[1]] = 2

    # This sets the margin between each cell
    MARGIN = 0

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
                print(row,column)
            #print(screen)
            if color != WHITE:
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

def location_convert():
    try:
        current_location = menu()
    except:
        time.sleep(0.2)
        current_location = menu()

    if current_location[0] > (len(grid[0]) - 1) or current_location[1] > (len(grid) - 1) or current_location[0] < 0 or current_location[1] < 0:
        current_location = menu()

    if len(locationlist) <= 3:
        locationlist.append(current_location)
    else:
        del locationlist[0]
        locationlist.append(current_location)

    xTemp = []
    yTemp = []

    for i in range(len(locationlist)):
        xTemp.append(locationlist[i][1])
        yTemp.append(locationlist[i][0])

    current_location[0] = int(sum(yTemp) / len(yTemp))
    current_location[1] = int(sum(xTemp) / len(xTemp))

    return current_location

def game_main():

    # Create a 2 dimensional array based on binary map.
    global grid
    grid = matrix_reader()

    global locationlist
    locationlist = []

    current_location = location_convert()
    start = current_location
    grid[start[0]][start[1]] = 2

    # Draw the grid.
    grid_draw(grid)
    # Initialize pygame
    pygame.init()

    # Set title of screen
    pygame.display.set_caption('Array Backed Grid')

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Initialize start and end_node
    start = end = tuple()



    # -------- Main Program Loop -----------
    while not done:
        current_location = location_convert()
        start = current_location
        grid[start[0]][start[1]] = 2
        #updates TKinter GUI
        root.update()
        if current_location:
            grid[current_location[0]][current_location[1]] = 2
        """for event in pygame.event.get():  # User did something
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
                        print('Regel 278:     ', grid)
                    # Print clicked coördinates (debug)
                    print('Click ', pos, 'Grid coordinates: ', row, column)
        """

        grid[current_location[0]][current_location[1]] = 0
        # Limit to 60 frames per second
        clock.tick(30)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.

# GUI
root = Tk()
logo = PhotoImage(file = 'pictures/tomsbroer.png')
# try:
#     icon = root.wm_iconbitmap(bitmap = 'pictures/icon.ico')
# except:
#     icon = root.wm_iconbitmap(bitmap = 'pictures/icon.bmp')
lowbanner = PhotoImage(file = 'pictures/Banner.png')
root.title('Tom\'s Broer')
root.geometry("1280x720")
root.config(bg= 'white')
banner1 = Label(root, image = logo, width = 1920, bg = '#303135')
banner1.pack(pady=1)
banner2 = Label(root, image = lowbanner, bg = 'white')
banner2.pack( pady = 0, side = BOTTOM)
embed = Frame(root, width=499, height=550)
embed.pack(pady=1, side = LEFT)
entry = AutocompleteEntry(lista, root, width=25, font = ('Arial', 20))
entry.pack(pady=20, padx= 25,)
root.update()

# def pushed():
#     lbl = Label(root, text = 'Hello')
#     lbl.pack()
#     lbl.configure(text='Searched!')

if platform.system == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

pygame.quit()
game_main()

# http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/