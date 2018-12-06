import time
import csv

playerScore = 0
playerMoves = 0
playerTime = 0
agentScore = 0
agentMoves = 0
agentTime = 0
agentMoveList = []

references = {}
allMetrics = {}
allResults = []

# searches = ['breadth', 'depth', 'flounder', 'greedy score', 'greedy move', 'greedy tiles']
# gameSearches = ['full alpha beta', 'depth limited alpha beta']
searches = ['depth', 'flounder', 'greedy score']
gameSearches = ['full depth maximizing', 'depth limited maximizing']

#pass in a reference so that it can save the specific time to a dicitonary, and then compare it to the end time once
# the reference is passed in again
def startTime(reference):
    references[str(reference)] = time.time()

# will return a float of the time passed
# parameters: a string of the object reference that is passed in, its a unique way to identify the specific
# clocks being used
def getTime(reference):
    elapsed = 0
    if str(reference) in references:
        elapsed = time.time() - references[str(reference)]
    return elapsed

# saves information when doing the metric testing
def setMetrics(reference, moves, score, depth, nodes, time):
    allMetrics[str(reference)] = [moves, score, depth, nodes, time]

# stores the metrics within a dictionary of lists with keys of each search that return a list of results
def saveResults(date, name, search, reference, score, depth, nodes, time, colors, size, depthLimit):
    allResults.append([date, name, search, reference, score, depth, nodes, time, colors, size, depthLimit])

def getResults(search):
    return allResults[search]

def getMetrics(reference):
    return allMetrics[str(reference)]

# saves the metrics file when the game is completed
def writeCSVFile():
    with open('logs/metrics.csv', 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(allResults)

# testing when metrics.py is run
if __name__ == '__main__':
    startTime("key")
    time.sleep(1.3445)
    getTime("key")