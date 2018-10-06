from helper import *


class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        self.PlayerInfo = playerInfo
        

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        return create_move_action(Point(0, 1))

        # print(gameMap)
    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
