from libs import *

f=open("options.txt")
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
    global x,y,grid,onupdate,running,oninteract,showat,setat,atpos,setvar,getvar,map_,onkeypress,oninteract,onkeypress,onupdate,debug,onload
    x=1
    y=6
    # wall: "#"
    # empty: " "
    grid=[
        [" "," ","#","#","#"],
        [" "," ","#","W","#"],
        ["#","#","#","#","#","#","#"],
        ["#"," "," "," "," "," ","#"],
        ["#"," "," ","/"," "," ","#"],
        ["#","#","#"," "," "," ","#"],
        ["#","?","!"," "," "," ","#"],
        ["#","#","#","#","#","#","#"],
        ["#","h","b","#"],
        ["#","#","#","#"],
    ]
    def onload():
        global x,y,grid,running,oninteract,onkeypress,setvar,getvar,showat,setat,atpos,map_,onkeypress,oninteract,onkeypress,onupdate,debug
        # initial msg vars
        setvar("t1",True)
        setvar("t2",True)

    def onupdate():
        global x,y,grid,running,oninteract,onkeypress,setvar,getvar,showat,setat,atpos,map_,onkeypress,oninteract,onkeypress,onupdate,debug
        if showat(3,4) == "\\":
            setat(3,2," ")
        else:
            setat(3,2,"#")
        
        def onkeypress(key):
            global x,y,grid,running,oninteract,onkeypress,setvar,getvar,showat,setat,atpos,map_,onkeypress,oninteract,onkeypress,onupdate,debug
            if key == b'h' and atpos(2,6) and getvar("t1"):
                goto(1,8)
        
        messageat(1,6,"Press arrow keys to move.", getvar("t1"))
        messageat(2,6,"Press 'h' for help.\n$1This will disappear after you go.$r",getvar("t1"))
        messageat(1,8,"Go to the slash '/'.\nGo right to go back.")
        messageat(3,4,"Press [space] to interact.",showat(3,4)=="/"and getvar("t2"))
        messageat(3,4,"Go to the 'W'",showat(3,4)=="\\",lambda:setvar("t2",False))
        
        if atpos(2,8):
            goto(3,6)
        
        if atpos(3,6):
            setat(1,6," ")
            setat(2,6," ")
            setat(1,5," ")
            setat(2,5," ")
            setat(0,8," ")
            setat(1,8," ")
            setat(2,8," ")
            setat(3,8," ")
            setat(0,9," ")
            setat(1,9," ")
            setat(2,9," ")
            setat(3,9," ")
            setvar("t1",False)

        messageat(3,1,"The tutorial is over.",after=stop)
        if atpos(3,1):
            sl(1)
            print("Press any key to continue.")




def main():
    global x,y,grid,onupdate,running,showat,setat,atpos,map_,oninteract,onload,onkeypress,oninteract,onkeypress,onupdate,debug
    onload()
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
        if char == b'\x00' or char == b'\xe0':
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
            exec(open("main.py",encoding="utf8").read())


if __name__ == "__main__":
    def reset():
        global running,viewdistx,viewdisty,v
        _viewdist = 7
        viewdistx = _viewdist
        viewdisty = _viewdist
        v = {}
        running = True

        map_()

    v:dict[Any]
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
        
        if showat(x+dx,y)[0] != "#":
            x += dx
        if showat(x,y+dy)[0] != "#":
            y += dy
    
    def goto(x_,y_):
        global x,y
        x = x_
        y = y_
    
    def messageat(x_,y_,msg,cond=True,before=lambda:None,after=lambda:None):
        if atpos(x_,y_) and cond:
            before()
            # formatting
            # black
            msg=msg.replace("$0","\033[30m")
            # red
            msg=msg.replace("$1","\033[31m")
            # green
            msg=msg.replace("$2","\033[32m")
            # yellow
            msg=msg.replace("$3","\033[33m")
            # blue
            msg=msg.replace("$4","\033[34m")
            # magenta
            msg=msg.replace("$5","\033[35m")
            # reset
            msg=msg.replace("$r","\033[0m")
            print(msg)
            after()

    def stop():
        global running
        running = False

    def setvar(var:str,val):
        global v
        v[var] = val
    def getvar(var:str):
        global v
        return v[var]
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
