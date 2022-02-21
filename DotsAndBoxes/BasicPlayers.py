import random
import time

class PlayerBase:
    """
    Basic class for player base. All players inherit from this model.
    """
    def __init__(self, playerIndex, colour="red"):
        self.index = playerIndex
        self.colour = colour

    def isHuman(self):
        pass

    def __str__(self):
        return "{}_player".format(self.index)

class HumanPlayer(PlayerBase):
    """
    Basic class for human player. Needs no implementation as the human player
    clicks using the UI.
    """
    def __init__(self, playerIndex, colour="blue"):
        """
        Override so human players are blue by default
        """
        super().__init__(playerIndex, colour)

    def isHuman(self):
        """
        Very important. Lets the UI know to give human player control.
        Returns:
            Bool
        """
        return True

    def __str__(self):
        """
        String representation for a random player. Used for writing results filenames.
        """
        return "{}_human".format(self.index)

class RandomPlayer(PlayerBase):
    """
    Most basic AI player. Chooses moves randomly from list of legal moves.
    """
    def chooseMove(self, game):
        """
        Chooses a move for the player by calling random move.
        """
        return self.randomMove(game)

    def randomMove(self, game):
        """
        Get list of legal moves and return any random one.
        """
        #time.sleep(0.25)
        return random.choice(game.get_all_legal_moves())

    def isHuman(self):
        """
        Very important. Lets the UI know NOT to give AI player UI control.
        Returns:
            Bool
        """
        return False

    def __str__(self):
        """
        String representation for a random player. Used for writing results filenames.
        """
        return "{}_random".format(self.index)

class MovesInOrder(PlayerBase):
    """
    Plays all of the legal moves in the order they are returned.
    """
    def chooseMove(self, game):
        moves = game.get_all_legal_moves()
        # Take a move from the middle of the list
        ind = int(len(moves)*0.5)
        return moves[ind]

    def __str__(self):
        return "{}_ordered".format(self.index)
