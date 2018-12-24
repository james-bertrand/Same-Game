## Same Game
###### by James Bertrand, James Brock, and Robert Coomber
###### v1.0

Released 12-6-18

##### VENV Library Requirements:
* numpy
* graphics.py ("graphics.py" NOT "graphics")

##### Bonuses:
- **_Writing quality_**
- **_Pretty, intuitive UI_** -> the game is playable with a GUI by running [\_\_main\_\_.py](__main__.py).
- **_Robust on many problem instances_** -> all boards are randomly generated, the agent successfully reaches its goal state on every iteration
- **_Smarter than the casual user_** -> the hardest difficulty almost always won (some CS students were able to win after several attempts, not on the first try, however)

### Instructions:

Clone this repository. Navigate to the **Same-Game** directory on your machine.

Make sure _virtualenv_ is installed on your machine with `pip install virtualenv`

Create a **python 3.6** virtual environment with `virtualenv --python=python3.6 venv`

Activate the virtual environment with `source venv/bin/activate`

Install requirements with `pip install -r requirements.txt`

-------------------------------

Run [\_\_main\_\_.py](__main__.py) to begin the game.

Read the instructions and compare your score to the agent.

metrics.csv will be created within the [logs](logs/) folder to store all values of each iteration of the game, so check [info.txt](logs/info.txt) to interpret the history of your results!
