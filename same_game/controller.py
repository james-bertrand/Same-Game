# This module will intake commands and call the appropriate functions
# Utilizes the game_state object and agent object

from same_game import agent, game_state, searches, metrics, games, gui
from copy import deepcopy
import time
import datetime


# pass in the reference (typically the board being searched on) and it will retrieve the metric data from that
# specific board memory location
# prints out all the data from the specified test
def displayMetrics(reference):
    metric = metrics.getMetrics(reference.__repr__())
    moves = metric[0]
    score = metric[1]
    depth = metric[2]
    nodes = metric[3]
    time = metric[4]
    print('Moves:')
    count = 1
    for move in moves:
        print(count, ': ', move)
        count += 1
    print("-----------------------------------------")
    print('Total score:', score)
    print('Depth of solution:', depth)
    print('Number of nodes explored:', nodes)
    print('Seconds taken:', time)


def displayAvg(search):
    print(search.upper(), "AVERAGES:")
    results = metrics.allResults[search]
    avgscore = 0
    avgdepth = 0
    avgnodes = 0
    avgtime = 0
    for i in range(len(results)):
        if i == 0:
            avgscore = results[i][2]
            avgdepth = results[i][3]
            avgnodes = results[i][4]
            avgtime = results[i][5]
        else:
            avgscore = (results[i][2]+avgscore)/2
            avgdepth = (results[i][3]+avgscore)/2
            avgnodes = (results[i][4]+avgscore)/2
            avgtime = (results[i][5]+avgscore)/2
    print('Average score:', avgscore)
    print('Average depth of solution:', avgdepth)
    print('Average number of nodes explored:', avgnodes)
    print('Average seconds taken:', avgtime)


# will run the search and store metrics based on the memory location of the board
# parameters: search - a string that represents the search type ex: depth or breadth
#             board - the board to be searched
# it also prints the beginning and end board
def runSearch(search, board):
    ag = agent.Agent(board)
    print()
    print(search.upper(), "===========================")
    print('Starting board (', search, '):\n', board.data)
    metrics.startTime(board.__repr__())
    if search == "depth":
        result = searches.depth_first_tree_search(ag)
    elif search == "breadth":
        result = searches.breadth_first_tree_search(ag)
    elif search == "flounder":
        result = searches.flounder(ag)
    elif search == "greedy":
        result = searches.greedy_tree_search_score(ag)
    elif search == "greedy score":
        result = searches.greedy_tree_search_score(ag)
    elif search == "greedy move":
        result = searches.greedy_tree_search_move(ag)
    elif search == "greedy tiles":
        result = searches.greedy_tree_search_score_plus_tilesRemaining(ag)
    t = metrics.getTime(board.__repr__())
    path = result.path()
    moves = []
    for node in path:
        if node.action:
            moves.append(node.action)
    metrics.setMetrics(board.__repr__(), moves, result.state.score, result.depth, ag.nodesExplored, t)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    metrics.saveResults(st, board.name, search, board.__repr__(), result.state.score, result.depth, ag.nodesExplored, t, board.colors, board.size, 1)
    metrics.agentScore = result.state.score
    print('Final board (', search, '):\n', result.state.data)


def runGame(search, board, depthLimit):
    # print()
    # print(search.upper(), "============================ DEPTH LIMIT:", depthLimit)
    # print('Starting board (', search, '):\n', board.data)
    ag = agent.GameAgent(board)
    movesList = []
    metrics.startTime(board.__repr__())
    if search == "full depth maximizing":
        while board.movesLeft():
            move = games.maximizing_singleplayer(agent.GameAgent(board), board)
            movesList.append(move)
            board.remove(move)
    elif search == "depth limited maximizing":
        while board.movesLeft():
            gui.updateAgentBoard(board)
            metrics.agentMoves += 1
            move = games.maximizing_singleplayer_depthlimit(agent.GameAgent(board), board, depthLimit)
            movesList.append(move)
            board.remove(move)
            metrics.agentScore = board.score
    elif search == "depth limited minimizing":
        while board.movesLeft():
            gui.updateAgentBoard(board)
            metrics.agentMoves += 1
            move = games.minimizing_singleplayer_depthlimit(agent.GameAgent(board), board, depthLimit)
            movesList.append(move)
            board.remove(move)
            metrics.agentScore = board.score
    elif search == "full alpha beta":
        while board.movesLeft():
            move = games.alphabeta_singleplayer(agent.GameAgent(board), board, depthLimit)
            movesList.append(move)
            board.remove(move)
    elif search == "depth limited alpha beta":
        while board.movesLeft():
            move = games.alphabeta_singleplayer_depthlimit(ag, board, depthLimit)
            movesList.append(move)
            board.remove(move)
    t = metrics.getTime(board.__repr__())
    # metrics.setMetrics(board.__repr__(), movesList, board.score, None, None, time)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    metrics.saveResults(st, board.name, search, board.__repr__(), board.score, None, None, t,
                        board.colors, board.size, depthLimit)
    metrics.agentScore = board.score
    metrics.agentMoveList = movesList
    gui.finalAgentBoard(board)
    gui.compare()
    # print('Final board (', search, '):\n', board.data)
    # print('\nMoves taken:')
    # count = 1
    # for move in movesList:
    #     print(count, ')', move)
    #     count += 1
    # print('Score achieved:', board.score)


# runs the block of code where the player searches the board
# parameters: board - the board for the player to search in
def playerInput(board):
    while board.movesLeft():
        x = gui.updateBoard(board)
        metrics.playerMoves += 1
        # print("Move", metrics.playerMoves)
        # print(board.data)
        # print('Current Score:', board.score)
        # print("Choose a move #:")
        # for i in range(len(board.moves())):
        #     print(i, ")", board.moves()[i])
        # x = int(input("Your move: "))
        board.remove(board.moves()[x])
        metrics.playerScore = board.score
    metrics.playerTime = metrics.getTime("player")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    metrics.saveResults(st, board.name, "player", board.__repr__(), metrics.playerScore, None, None, metrics.playerTime,
                        board.colors, board.size, 0)
    # print("Final Board:")
    # print(board.data)
    # print("Final Score:", board.score)
    gui.finalBoard(board)


# the mode where the player can play against a search algorithm of choice
def agentVSPlayer():
    # print("Welcome to the Same Game!")
    # print("The goal of this game is to remove as many color groupings of 2 or more tiles as possible.")
    # print("The bigger the group you remove, the more points you score! Try to score as high as you can.")
    # print()
    # name = input("What is your name? ")
    while True:
        metrics.playerMoves = 1
        metrics.playerScore = 0
        metrics.agentMoveList = []
        metrics.agentMoves = 1
        metrics.agentScore = 0
        gui.intro()
        name = gui.getName()
        # size = int(input("What size board would you like to play on? (enter a single number. i.e. 5 = a 5x5 board) "))
        size = gui.getSize()
        # colors = int(input("How many different colors would you like? (Recommended 2 or more) "))
        if size == 3 or size == 4:
            colors = 2
        if size == 5 or size == 6:
            colors = 3
        board = game_state.State(name, size, colors)
        boardCopy = deepcopy(board)
        metrics.startTime("player")
        playerInput(board)

        # print("You took", metrics.playerTime, "seconds!")
        # print()
        # search = ""
        # while search != "breadth" and search != "depth" and search != "greedy" and search != "flounder":
        #     search = input("What search would you like? (breadth, depth, flounder, or greedy) ")
        # print("Now lets see how the agent did...")
        depthLimit = gui.difficulty()
        if depthLimit == 1:  # player chose easy difficulty
            search = "depth limited minimizing"
        else:
            search = "depth limited maximizing"
        runGame(search, boardCopy, depthLimit)
        # displayMetrics(boardCopy)
        # print()
        # print("You scored:", metrics.playerScore)
        # print("Agent scored:", metrics.agentScore)
        # if metrics.playerScore > metrics.agentScore:
        #     print("You win!")
        # elif metrics.playerScore == metrics.agentScore:
        #     print("You tied!")
        # else:
        #     print("You lost!")
        gui.results()
        # if(input("Play again? (y/n) ") == 'n'):
        #     break


# runs search algorithms on a list of boards, reporting the metrics for each
def agentOnlyMetrics(boards):
    print('Agent metrics on set of input same-game boards:')
    print('-----------------------------------------------')
    for board in boards: # for every board passed in
        for s in metrics.searches: # for every search defined in the metrics.py file
            boardCopy = deepcopy(board)
            runSearch(s, boardCopy)
            displayMetrics(boardCopy)
    # for s in metrics.searches:
    #     displayAvg(s)


# runs alphabeta search on a list of boards
def gameAgentOnly(boards, depthLimit):
    print('Agent test for a game search:')
    print('-----------------------------')
    for board in boards:
        for s in metrics.gameSearches:
            boardCopy = deepcopy(board)
            runGame(s, boardCopy, depthLimit)
            # displayMetrics(boardCopy)


if __name__ == '__main__':
    agentVSPlayer()

# # THIS IS OLD ONE THAT ISNT EFFICIENT
# def agentOnlyMetrics(boards):
#     print('Agent metrics on set of input same-game boards:')
#     print('-----------------------------------------------')
#     for board in boards:
#         boardCopy = deepcopy(board)
#         ag = agent.Agent(board)
#         ag2 = agent.Agent(boardCopy)
#
#         print('Starting board:\n', board.data, '\n')
#         metrics.startTime(board.__repr__())
#         breadth_result = searches.breadth_first_tree_search(ag)
#         metrics.getTime(board.__repr__())
#         print('Final board (breadth first):\n', breadth_result.state.data, '\n')
#         breadth_path = breadth_result.path()
#         breadth_moves = []
#         for node in breadth_path:
#             if node.action:
#                 breadth_moves.append(node.action)
#         print('Moves:')
#         count = 1
#         for move in breadth_moves:
#             print(count, ': ', move)
#             count += 1
#         print('\nTotal score:', breadth_result.state.score, '\n')
#         print('Depth of solution:', breadth_result.depth, '\n')
#         print('Number of nodes explored:', ag.nodesExplored, '\n')
#
#         print('Starting board:\n', boardCopy.data, '\n')
#         metrics.startTime(boardCopy.__repr__())
#         depth_result = searches.depth_first_tree_search(ag2)
#         metrics.getTime(boardCopy.__repr__())
#         print('Final board (depth first):\n', depth_result.state.data, '\n')
#         depth_path = depth_result.path()
#         depth_moves = []
#         for node in depth_path:
#             if node.action:
#                 depth_moves.append(node.action)
#         print('Moves:')
#         count = 1
#         for move in depth_moves:
#             print(count, ': ', move)
#             count += 1
#         print('\nTotal score:', depth_result.state.score, '\n')
#         print('Depth of solution:', depth_result.depth, '\n')
#         print('Number of nodes explored:', ag2.nodesExplored, '\n')

# THIS IS OLD ONE WITH THE WEIRD CHECK FOR COMPLETENESS
# def agentOnlyMetrics(boards):
#     print('Agent metrics on set of input same-game boards:')
#     print('-----------------------------------------------')
#     for board in boards:
#         board2 = deepcopy(board) #makes a placeholder for when it is only adding values within, where it needs to restart from where it left off instead of letting the agent change the board
#         go = True
#         add = True #wether it knows to continue with the adding
#         addLimit = board.size #how many times it will change tiles before generating an entirely new board
#         aL = deepcopy(addLimit) #a placeholder to keep track of how many times it has added
#         boardCount = 0
#         while go:
#             if not add: #this is to generate new random board every "addLimit" times
#                 board.data = board.setup()
#                 #print(board.data)
#                 add = True
#             else:
#                 board.data = deepcopy(board2.data) #these next three lines are when it is fixing the placeholder so the agent doesnt modify what is being passed in
#                 board.changeATile(1)
#                 board2.data = deepcopy(board.data)
#                 #print(board.data)
#                 aL = aL-1
#                 if aL == 0: #if the add counter hits 0, just restart and tell it to regenerate the board
#                     add = False
#                     aL = deepcopy(addLimit)
#             pre = deepcopy(board.data)
#             ag = agent.Agent(board)
#             searches.depth_first_tree_search(ag)
#             post = deepcopy(board.data)
#             if board.isEmpty() == True:
#                 go = False
#                 print('Starting board:\n', pre, '\n')
#                 print('Final board:\n', post, '\n')
#             boardCount = boardCount + 1
#
#         print("Boards generated before correct: ", boardCount, '\n')
#
#
