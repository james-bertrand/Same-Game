# The Same Game
# by James Bertrand, James Brock, Robert Coomber
# 12-6-18

from same_game import controller, metrics
import graphics

# will start the game and except an error from the termination of the game, which will then prompt it to save logs
try:
    controller.agentVSPlayer()
except graphics.GraphicsError:
    metrics.writeCSVFile()
    print("Game window was exited.")
except KeyboardInterrupt:
    metrics.writeCSVFile()
    print("Game was halted.")
