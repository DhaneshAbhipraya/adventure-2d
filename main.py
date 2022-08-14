from msvcrt import *
from random import randint as r
from threading import Thread
from time import sleep as sl

def map_():
    global x,y,grid,onupdate,running
    x=1
    y=6
    # wall: "#"
    # empty: " "
    grid = [
        [" "," ","#","#","#"," "," "],
        [" "," ","#"," ","#"," "," "],
        ["#","#","#","#","#","#","#"],
        ["#"," "," "," "," "," ","#"],
        ["#"," "," ","/"," "," ","#"],
        ["#"," "," "," "," "," ","#"],
        ["#","o"," "," "," "," ","#"],
        ["#","#","#","#","#","#","#"]
    ]
    def onupdate():
        global x,y,grid,running
        if showat(3,4) == "\\":
            setat(3,2," ")
        else:
            setat(3,2,"#")
        
        if atpos(3,1):
            print("Congratulations! You escaped the maze!\nPress any key to exit.")
            running = False




def main():
    global x,y,grid,onupdate,running,showat,setat,atpos,setTimeout,map_
    while running:
        print("\033[H\033[J",end="")
        onupdate()
        print(x,y)

        
        print("┌"+"─"*viewdistx+"┐")
        for i in range(viewdistx):
            for j in range(viewdisty):
                # check if on the center of the screen
                if j == viewdisty//2 and i == viewdistx//2:
                    print("∙",end="")
                else:
                    if j == 0:
                        print("│",end="")
                    print(showat(j+x-(viewdistx//2),i+y-(viewdisty//2)),end="")
                    if j == viewdistx-1:
                        print("│",end="")
            print()
        print("└"+"─"*viewdistx+"┘")

        # input a single character
        char = getch()
        if char == b'\x00':
            char2 = getch()
            # up arrow
            if char2 == b'H':
                move(0,-1)
            # down arrow
            elif char2 == b'P':
                move(0,1)
            # left arrow
            elif char2 == b'K':
                move(-1,0)
            # right arrow
            elif char2 == b'M':
                move(1,0)
        # escape
        elif char == b'\x1b':
            print("\033[H\033[J",end="")
            break
        # space
        elif char == b' ':
            # if on '/'
            if showat(x,y) == '/':
                # set to '\'
                setat(x,y,'\\')
            # if on '\'
            elif showat(x,y) == '\\':
                # set to '/'
                setat(x,y,'/')


if __name__ == "__main__":
    def reset():
        global running,viewdistx,viewdisty
        _viewdist = 7
        viewdistx = _viewdist
        viewdisty = _viewdist
        running = True

        map_()

    reset()

    def atpos(x_,y_):
        return x_==x and y_==y

    def showat(x,y):
        try:
            return grid[y][x] if x>=0 and y>=0 else " "
        except IndexError:
            return " "
    
    def setat(x,y,char):
        try:
            grid[y][x] = char
        except IndexError:
            pass

    def move(dx,dy):
        global x,y
        
        if showat(x+dx,y+dy) != "#":
            x += dx
            y += dy
    # hide cursor
    print("\033[?25l")

    while True:
        main()
        print("\033[H\033[JIt looks like the game's main loop has ended.\nWould you like to play again? (y/n)")
        prompt=getch()
        if prompt == b'y':
            reset()
        elif prompt == b'n':
            break
    # show cursor
    print("\033[?25h")
