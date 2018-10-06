import json
from flask import Flask, request
from helper import GameMap, Player, Point
from bot import Bot
import numpy as np

app = Flask(__name__)

bot = Bot()

def deserialize(data):
    if "x" in data and "y" in data:
        return Point(data["x"], data["y"])
    elif "Name" in data:
        return Player(data["Health"], data["MaxHealth"], data["CarriedResources"],
                      data["CarryingCapacity"], data["CollectingSpeed"], data["TotalResources"],
                      data["AttackPower"], data["Defence"], data["Position"],
                      data["HouseLocation"], data["CarriedItems"], data["Score"], data["Name"],
                      data["UpgradeLevels"])
    elif "CustomSerializedMap" in data:
        data["GameMap"] = GameMap(
            data["CustomSerializedMap"], data["xMin"], data["yMin"], data["WallsAreBreakable"])
    return data


actions = {0:'left', 1:'right', 2:'up', 3:'down', 4:'mine'}

items = [[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{1},{1},{},{},{},{},{},{},{},{2},{},{},{},{},{},{},{},{1},{1},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{4,500,2.5},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{4,500,1},{},{},{1},{},{}],[{},{},{1},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{1},{},{}],[{},{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{},{}],[{},{},{},{},{1},{},{4,500,1},{},{},{},{},{},{},{},{},{},{1},{},{},{},{}],[{},{},{},{},{},{1},{1},{},{},{},{6},{},{},{},{1},{1},{},{},{},{},{}],[{},{},{},{},{},{},{1},{1},{1},{1},{1},{1},{1},{1},{1},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{1},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{4,500,2.5},{},{}],[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{1},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{1},{1},{1},{1},{1},{1},{1},{1},{1},{},{},{},{},{},{}],[{},{},{},{},{},{1},{1},{},{},{},{},{},{},{},{1},{1},{},{},{},{},{}],[{},{},{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{1},{},{},{},{}],[{},{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{},{}]]

def fixArrB(badArr):
    fixed = []
    for ri, rv in enumerate(badArr):
        fixed.append([])
        for ci, cv in enumerate(rv):
            if cv == {}:
                fixed[ri].append([0,0,0])
            elif cv == {1}:
                fixed[ri].append([1,0,0])
            elif len(cv) == 3:
                fixed[ri].append([list(cv)[0], list(cv)[1], list(cv)[2]])
            else:
                fixed[ri].append([list(cv)[0],0,0])
    return(fixed)

class Game():
    
    def __init__(self, grid_size=21):
        self.grid_size = grid_size
        self.reset()
        self.state_changed = True
        self.score = 0
        self.stateNow = np.array(deserialize(fixArrB([[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{1},{1},{},{},{},{},{},{},{},{2},{},{},{},{},{},{},{},{1},{1},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{}],[{4,500,2.5},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{4,500,1},{},{},{1},{},{}],[{},{},{1},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{1},{},{}],[{},{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{},{}],[{},{},{},{},{1},{},{4,500,1},{},{},{},{},{},{},{},{},{},{1},{},{},{},{}],[{},{},{},{},{},{1},{1},{},{},{},{6},{},{},{},{1},{1},{},{},{},{},{}],[{},{},{},{},{},{},{1},{1},{1},{1},{1},{1},{1},{1},{1},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{1},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{4,500,2.5},{},{}],[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{},{},{},{},{1},{},{},{},{},{},{},{},{},{},{}],[{},{},{},{},{},{},{1},{1},{1},{1},{1},{1},{1},{1},{1},{},{},{},{},{},{}],[{},{},{},{},{},{1},{1},{},{},{},{},{},{},{},{1},{1},{},{},{},{},{}],[{},{},{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{1},{},{},{},{}],[{},{},{},{1},{},{},{},{},{},{},{},{},{},{},{},{},{},{1},{},{},{}]])))

    def set_state(self, state):
        self.stateNow = state

    @property
    def name(self):
        return "LH"
    
    @property
    def nb_actions(self):
        return 5
    
    def reset(self):
        pass

    def play(self, action):
        assert action in range(5), "Invalid action."
        return action

    def get_state(self):
        return self.stateNow

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def is_over(self):
        return False

    def is_won(self):
        return False

    def get_frame(self):
        return self.get_state()

    def draw(self):
        return self.get_state()

    def get_possible_actions(self):
        return range(self.nb_actions)

game = Game()



















@app.route("/", methods=["GET"])
def ping():
    return "I am alive!"


@app.route("/", methods=["POST"])
def response():
    """
    Point d'entree appelle par le GameServer
    """
    gameInfo = json.loads(request.form["data"], object_hook=deserialize)
    player = gameInfo["Player"]

    Game.set_score(Game, np.array(gameInfo["Player"].CarriedResources))
    Game.set_state(Game, np.array(fixArrB(gameInfo['CustomSerializedMap'])))

    bot.before_turn(player)

    action = bot.execute_turn(gameInfo['GameMap'], gameInfo['OtherPlayers'])

    bot.after_turn()
    print(action)
    return action


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)























