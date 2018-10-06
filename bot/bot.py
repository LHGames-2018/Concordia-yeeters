from helper import *


class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        # return create_move_action(Point(0, 1))

        try:
            StorageHelper.read("firstRunDone")
        except Exception as e:
            StorageHelper.write("firstRunDone", "false")

        if StorageHelper.read("firstRunDone") != "done":
            StorageHelper.write("firstRunDone", "done")
            StorageHelper.write("counterL", 4)
            StorageHelper.write("counterD", 1)

        if StorageHelper.read("counterL") != 0:
            return create_move_action(Point(-1, 0))
            StorageHelper.write("counterL", StorageHelper.read("counterL") - 1)
        elif StorageHelper.read("counterL") == 0 and StorageHelper.read("counterD") != 0:
            return create_move_action(Point(0, 1))
            StorageHelper.write("counterD", StorageHelper.read("counterD") - 1)
        else:
            return create_collect_action(0, 1)

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
