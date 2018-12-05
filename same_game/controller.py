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

# after metrics are ran, this will average all of the results together and print them based on a specific search
# parameter: search - string representation of the search used
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

# the active method that will use while loops to complete a board depending on the search inputted, as well as save
# metrics as well
# Parameters: search - string representation of the search,
#             board - the board object to be manipulated,
#             depth limit - int representing the depth limit of applicable searches
def runGame(search, board, depthLimit):
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

# runs the block of code that loops through the player searching the board
# parameters: board - the board for the player to search in
def playerInput(board):
    while board.movesLeft():
        x = gui.updateBoard(board)
        metrics.playerMoves += 1
        board.remove(board.moves()[x])
        metrics.playerScore = board.score
    metrics.playerTime = metrics.getTime("player")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    metrics.saveResults(st, board.name, "player", board.__repr__(), metrics.playerScore, None, None, metrics.playerTime,
                        board.colors, board.size, 0)
    gui.finalBoard(board)

# runs the mode where the player can play against a search algorithm of choice
def agentVSPlayer():
    while True:
        metrics.playerMoves = 1
        metrics.playerScore = 0
        metrics.agentMoveList = []
        metrics.agentMoves = 1
        metrics.agentScore = 0
        gui.intro()
        name = gui.getName()
        size = gui.getSize()
        if size == 3 or size == 4:
            colors = 2
        if size == 5 or size == 6:
            colors = 3
        board = game_state.State(name, size, colors)
        boardCopy = deepcopy(board)
        metrics.startTime("player")
        playerInput(board)
        search = "depth limited maximizing"
        depthLimit = gui.difficulty()
        runGame(search, boardCopy, depthLimit)
        gui.results()

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

# will run the game if controller.py is run
if __name__ == '__main__':
    agentVSPlayer()