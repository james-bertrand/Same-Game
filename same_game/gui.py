from graphics import *
from same_game import metrics

win = GraphWin("Same Game", 500, 500, autoflush=False)
name = ''

# will wait till there is a click within a square created by two points
def waitTillClick(p1, p2):
    click = Point(501,501)
    while (click.getX() < p1.getX() or click.getX() > p2.getX()) and (click.getY() < p1.getY() or click.getY() > p2.getY()):
        click = win.getMouse()

# will wait till a clikc is within a certain square and will then return which box it used
# parameters: boxes - array of boxes (two points) that represent the different places to click
# returns: the index of the box (two points) where the mouse was clicked
def waitTillClickSections(boxes):
    click = win.getMouse()
    out = False
    while True:
        index = 0
        for b in boxes:
            if click.getX() >= b.getP1().getX() and click.getX() <= b.getP2().getX() and click.getY() >= b.getP1().getY() and click.getY() <= b.getP2().getY():
                return index
            index += 1
        click = win.getMouse()

# will wait till a click is placed anywhere
def waitTillAnyClick():
    win.getMouse()
    return

# begins the screen that asks for the name of the plyaer
def getName():
    prompt = Text(Point(250, 220),
                "Please enter your name:")
    prompt.setSize(20)
    inputBox = Entry(Point(250, 250), 50)
    inputBox.draw(win)
    prompt.draw(win)
    go1 = Point(230, 270)
    go2 = Point(270, 290)
    go = Rectangle(go1, go2)
    goTxt = Text(Point(250, 280),
                  "Enter")
    goTxt.setStyle("bold")
    go.draw(win)
    goTxt.draw(win)
    update()
    waitTillClick(go1, go2)
    name = inputBox.getText()
    go.undraw()
    goTxt.undraw()
    inputBox.undraw()
    prompt.undraw()
    return name

# starts the screen that requests the size of the board
def getSize():
    prompt = Text(Point(250, 220),
                "What size board would you like to play on?")
    prompt.setSize(20)
    prompt.setStyle("italic")
    prompt.draw(win)
    go0 = Rectangle(Point(240,250), Point(260,270))
    go0Txt = Text(Point(250, 260),"3")
    go0Txt.setStyle("bold")
    go0.draw(win)
    go0Txt.draw(win)
    go1 = Rectangle(Point(240, 275), Point(260, 295))
    go1Txt = Text(Point(250, 285), "4")
    go1Txt.setStyle("bold")
    go1.draw(win)
    go1Txt.draw(win)
    go2 = Rectangle(Point(240, 300), Point(260, 320))
    go2Txt = Text(Point(250, 310), "5")
    go2Txt.setStyle("bold")
    go2.draw(win)
    go2Txt.draw(win)
    go3 = Rectangle(Point(240, 325), Point(260, 345))
    go3Txt = Text(Point(250, 335), "6")
    go3Txt.setStyle("bold")
    go3.draw(win)
    go3Txt.draw(win)
    update()
    index = waitTillClickSections([go0, go1, go2, go3])
    go0.undraw()
    go0Txt.undraw()
    go1.undraw()
    go1Txt.undraw()
    go2.undraw()
    go2Txt.undraw()
    go3.undraw()
    go3Txt.undraw()
    prompt.undraw()
    if index == 0:
        return 3
    elif index == 1:
        return 4
    elif index == 2:
        return 5
    elif index == 3:
        return 6

# will draw out the board that is passed in
# parameters: board - the board to be drawn out
def updateBoard(board):
    s = board.size
    r = []
    for i in range(s):
        for ii in range(s):
            r.append( Rectangle( Point(50+((400/s)*ii),50+((400/s)*i)), Point(50+((400/s)*(ii+1)),50+((400/s)*(i+1))) ) )
    index = 0
    score = Text(Point(250, 475),"Score: " + str(metrics.playerScore))
    score.setStyle("bold")
    score.draw(win)
    move = Text(Point(250, 25),"Move #" + str(metrics.playerMoves))
    move.setStyle("bold")
    move.draw(win)
    update()
    for i in r:
        i.setOutline("black")
        i.setWidth(2)
        i.setFill(squareColor(board, index))
        i.draw(win)
        index += 1
    toReturn = []
    go = True
    while go:
        x = waitTillClickSections(r)
        index = 0
        for i in board.moves():
            if [int(x/board.size),x%board.size] in i:
                go = False
                index -= 1
            index += 1
            if go == False:
                break
    for i in r:
        i.undraw()
    move.undraw()
    score.undraw()
    return index

# class to return the color of a square within a board based on its index
# parameters: board - the board to be looked into
#             index - the specific index of the move
# returns: a string representation of the color
def squareColor(board, index):
    x = board.data[int(index/board.size)][index%board.size]
    if x == 0:
        return "white"
    elif x == 1:
        return "red"
    elif x == 2:
        return "green"
    elif x == 3:
        return "blue"
    elif x == 4:
        return "yellow"

# updates the board every time a new agent move is made
def updateAgentBoard(board):
    s = board.size
    r = []
    for i in range(s):
        for ii in range(s):
            r.append(Rectangle(Point(50 + ((400 / s) * ii), 50 + ((400 / s) * i)),
                               Point(50 + ((400 / s) * (ii + 1)), 50 + ((400 / s) * (i + 1)))))
    index = 0
    score = Text(Point(250, 34), "Agent Score: " + str(metrics.agentScore))
    score.setStyle("bold")
    score.draw(win)
    move = Text(Point(250, 17), "Agent Move #" + str(metrics.agentMoves))
    move.setStyle("bold")
    move.draw(win)
    prompt = Text(Point(250, 475), "Click anywhere to continue to the next move...")
    prompt.setStyle("italic")
    prompt.setSize(18)
    prompt.draw(win)
    update()
    for i in r:
        i.setOutline("black")
        i.setWidth(2)
        i.setFill(squareColor(board, index))
        i.draw(win)
        index += 1
    win.getMouse()
    for i in r:
        i.undraw()
    move.undraw()
    score.undraw()
    prompt.undraw()

# displays the results and scores of the player
def finalBoard(board):
    s = board.size
    r = []
    for i in range(s):
        for ii in range(s):
            r.append(Rectangle(Point(50 + ((400 / s) * ii), 50 + ((400 / s) * i)),
                               Point(50 + ((400 / s) * (ii + 1)), 50 + ((400 / s) * (i + 1)))))
    index = 0
    prompt = Text(Point(250, 475), "Click anywhere to continue...")
    prompt.setSize(20)
    prompt.setStyle("italic")
    prompt.draw(win)
    move = Text(Point(250, 25), "You scored " + str(metrics.playerScore) + " in " + str(metrics.playerMoves-1) + " moves!")
    move.setStyle("bold")
    move.setSize(20)
    move.draw(win)
    for i in r:
        i.setOutline("black")
        i.setWidth(2)
        i.setFill(squareColor(board, index))
        i.draw(win)
        index += 1
    prompt2 = Text(Point(250, 250), "END")
    prompt2.setStyle("bold")
    prompt2.setTextColor("grey")
    prompt2.setSize(36)
    prompt2.draw(win)
    update()
    win.getMouse()
    for i in r:
        i.undraw()
    prompt.undraw()
    prompt2.undraw()
    move.undraw()

# displays the results and scores of the agent
def finalAgentBoard(board):
    s = board.size
    r = []
    for i in range(s):
        for ii in range(s):
            r.append(Rectangle(Point(50 + ((400 / s) * ii), 50 + ((400 / s) * i)),
                               Point(50 + ((400 / s) * (ii + 1)), 50 + ((400 / s) * (i + 1)))))
    index = 0
    prompt = Text(Point(250, 475), "Click anywhere to continue...")
    prompt.setSize(20)
    prompt.setStyle("italic")
    prompt.draw(win)
    move = Text(Point(250, 25),
                "Agent scored " + str(metrics.agentScore) + " in " + str(metrics.agentMoves-1) + " moves.")
    move.setStyle("bold")
    move.setSize(20)
    move.draw(win)
    for i in r:
        i.setOutline("black")
        i.setWidth(2)
        i.setFill(squareColor(board, index))
        i.draw(win)
        index += 1
    prompt2 = Text(Point(250, 250), "END")
    prompt2.setStyle("bold")
    prompt2.setTextColor("grey")
    prompt2.setSize(36)
    prompt2.draw(win)
    update()
    win.getMouse()
    for i in r:
        i.undraw()
    prompt.undraw()
    prompt2.undraw()
    move.undraw()

# begins the page that asks for the difficulty of the agent
def difficulty():
    prompt = Text(Point(250, 220),
                  "Now it is time to see how the artificial intelligence scores...")
    prompt.setSize(16)
    prompt.setStyle("italic")
    prompt.draw(win)
    prompt2 = Text(Point(250, 250),
                  "Please select the diffculty of the agent:")
    prompt2.setStyle("bold")
    prompt2.draw(win)
    go1 = Rectangle(Point(225, 275), Point(275, 295))
    go1Txt = Text(Point(250, 285), "Easy")
    go1Txt.setStyle("bold")
    go1.draw(win)
    go1Txt.draw(win)
    go2 = Rectangle(Point(225, 300), Point(275, 320))
    go2Txt = Text(Point(250, 310), "Medium")
    go2Txt.setStyle("bold")
    go2.draw(win)
    go2Txt.draw(win)
    go3 = Rectangle(Point(225, 325), Point(275, 345))
    go3Txt = Text(Point(250, 335), "Hard")
    go3Txt.setStyle("bold")
    go3.draw(win)
    go3Txt.draw(win)
    update()
    index = waitTillClickSections([go1, go2, go3])
    go1.undraw()
    go1Txt.undraw()
    go2.undraw()
    go2Txt.undraw()
    go3.undraw()
    go3Txt.undraw()
    prompt.undraw()
    prompt2.undraw()
    if index == 0:
        return 1
    elif index == 1:
        return 2
    elif index == 2:
        return 3

# the final screen that compares the scores of the player and agent
def compare():
    if metrics.playerScore > metrics.agentScore:
        result = Text(Point(250, 200), "You beat the agent by " + str(metrics.playerScore) + ":" + str(metrics.agentScore) + "!")
        result.setStyle("bold")
        result.setSize(20)
    elif metrics.playerScore < metrics.agentScore:
        result = Text(Point(250, 200), "You lost to the agent by " + str(metrics.playerScore) + ":" + str(metrics.agentScore) + "!")
        result.setStyle("bold")
        result.setSize(20)
    elif metrics.playerScore == metrics.agentScore:
        result = Text(Point(250, 200), "You tied with the agent by " + str(metrics.playerScore) + ":" + str(metrics.agentScore) + "!")
        result.setStyle("bold")
        result.setSize(20)
    n = Text(Point(250, 320), "Click anywhere to restart...")
    n.setSize(20)
    n.setStyle("italic")
    result.draw(win)
    n.draw(win)
    update()
    win.getMouse()
    result.undraw()
    n.undraw()

def results():
    return 0

# begins the first screen with the instructions of the game
def intro():
    hello = Text(Point(250,200), "Welcome to the Same Game!")
    hello.setStyle("bold")
    hello.setSize(20)
    goal = Text(Point(250, 230), "The goal of this game is to remove as many color groupings of 2 or more tiles as possible.")
    points = Text(Point(250, 260), "The bigger the group you remove, the more points you score! Try to score as high as you can.")
    points2 = Text(Point(250, 290),
                  "You cannot remove groups of less than 2 tiles, and you will only score for groups greater than 2.")
    n = Text(Point(250, 320),"Click anywhere to continue...")
    n.setSize(20)
    n.setStyle("italic")
    hello.draw(win)
    goal.draw(win)
    points.draw(win)
    points2.draw(win)
    n.draw(win)
    update()
    win.getMouse()
    hello.undraw()
    goal.undraw()
    points.undraw()
    points2.undraw()
    n.undraw()
    return

# a test if the gui.py file is run
if __name__ == '__main__':
    intro()
    getName()
    print(getSize())
    waitTillAnyClick()