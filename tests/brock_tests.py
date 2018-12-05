from same_game import game_state as state
from same_game import controller, metrics

def test_game_state():
    testArray = state.State("testArray", 10, 4)
    print("The generated board:")
    print(testArray.data)
    print("All Sections:")
    print(testArray.sections())
    print("Valid Moves:")
    print(testArray.moves())
    print("The moves left and amount of blocks removed for every action:")
    for i in range(20):
        if testArray.isEmpty() == False and testArray.movesLeft():
            print(testArray.moves())
            print(testArray.count(testArray.moves()[0]))
            testArray.remove(testArray.moves()[0])
    print("Final:")
    print(testArray.data)
    print('Is the board empty?')
    print(testArray.isEmpty(),'\n')

def test_controller():
    for i in range(10):
        testBoards = [
            state.State("Test1."+str(i), 5, 2),
            # state.State("Test2."+str(i), 6, 2),
            # state.State("Test3."+str(i), 10, 2),
            state.State("Test4."+str(i), 5, 3),
            # state.State("Test5."+str(i), 6, 3),
            # state.State("Test6."+str(i), 10, 3),
            state.State("Test7."+str(i), 5, 4),
            # state.State("Test8."+str(i), 6, 4),
            state.State("Test9."+str(i), 5, 5),
        ]
        controller.agentOnlyMetrics(testBoards)

def test_game_search():
    for i in range(10):
        testBoards = [
            state.State("Game1."+str(i), 5, 2),
            # state.State("Game2."+str(i), 6, 2),
            # state.State("Game3."+str(i), 10, 2),
            state.State("Game4."+str(i), 5, 3),
            # state.State("Game5."+str(i), 6, 3),
            # state.State("Game6."+str(i), 10, 3),
            state.State("Game7."+str(i), 5, 4),
            # state.State("Game8."+str(i), 6, 4),
            state.State("Game9."+str(i), 5, 5),
        ]
        controller.gameAgentOnly(testBoards, 1)


# Call functions here to run specific tests
if __name__ == '__main__':
    # test_game_state()
    test_controller()
    test_game_search()
    metrics.writeCSVFile()
