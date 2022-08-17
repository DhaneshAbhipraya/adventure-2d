from libs import *

f=open("options.txt","r")
options=f.read().splitlines()
f.close()
# field: debug
for i in options:
    field=i.split('=')[0]
    value=i.split('=')[1]
    if field == "debug":
        try: debug = bool(int(value))
        except: raise ValueError(f"{field} must be 1 or 0")
        break

def map_():
    global x,y,grid,onupdate,running,oninteract
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
        ["#"," "," "," "," "," ","#"],
        ["#","#","#","#","#","#","#"]
    ]
    def onupdate():
        global x,y,grid,running,oninteract,onkeypress
        if showat(3,4) == "\\":
            setat(3,2," ")
        else:
            setat(3,2,"#")
        
        def onkeypress(key):
            global x,y,grid,running,oninteract,onkeypress
            if key == b'c':
                goto(3,4)
        
        if atpos(3,1):
            print("Congratulations! You escaped the maze!\nPress any key to exit.")
            running = False




def main():
    global x,y,grid,onupdate,running,showat,setat,atpos,map_,oninteract
    while running:
        print("\033[H\033[J",end="")
        try: onupdate()
        except NameError: pass
        print(x,y) if debug else None

        
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
        try: onkeypress(char)
        except NameError: pass
        print(char) if debug else None
        if char == b'\x00':
            char2 = getch()
            print(char2) if debug else None
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
            try: oninteract()
            except NameError: pass
            # if on '/'
            if showat(x,y) == '/':
                # set to '\'
                setat(x,y,'\\')
            # if on '\'
            elif showat(x,y) == '\\':
                # set to '/'
                setat(x,y,'/')
        # r
        elif char == b'r' and debug:
            # restart the program
            reset()
            exec(open("main.py").read())


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
        if debug: print(showat(x+dx,y+dy))
        
        if showat(x+dx,y) != "#":
            x += dx
        if showat(x,y+dy) != "#":
            y += dy
    
    def goto(x_,y_):
        global x,y
        x = x_
        y = y_
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
