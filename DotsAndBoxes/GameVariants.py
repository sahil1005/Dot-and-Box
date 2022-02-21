try:
    from Game import Game
    from Box import Box
    from Line import Line
except ModuleNotFoundError:
    from DotsAndBoxes.Game import Game
    from DotsAndBoxes.Box import Box
    from DotsAndBoxes.Line import Line
import random

class SwedishGame(Game):
    """
    Subclass for the 'swedish' variant of the game board.
    All of the side pieces are filled in to begin with.
    """
    def __init__(self, width, height, maxPlayers=2, curPlayer=1, legalMoves=False, copy_grid=None, copy_boxes=None, movesMade=None):
        """
        Initialise the game with given width and height.
        If grid or boxes are passed, then create a copy of these objects.
        Args:
            width: int
            height: int
            maxPlayers: int (2)
            curPlayer: int (1)
            legalMoves: List(3-Tuple(int))
            copy_grid: List[][][Line]
            copy_boxes: List[][Box]
        """
        super().__init__(width, height, maxPlayers=2, curPlayer=1, legalMoves=False, copy_grid=None, copy_boxes=None, movesMade=None)
        if copy_grid is None and copy_boxes is None:
            self.make_board_swedish()

    def make_board_swedish(self):
        """
        Makes all of the outside edges inaccessible.
        """
        # first find all of the moves we want to block
        movesToMake = []
        # top and bottom edges
        for i in range(self.width-1):
            movesToMake.append((0,0,i))
            movesToMake.append((0,self.height-1,i))
        # left and right edges
        for i in range(self.height-1):
            movesToMake.append((1,0,i))
            movesToMake.append((1,self.width-1,i))
        # now make those moves, as if we are player 3.
        for move in movesToMake:
            self.grid[move[0]][move[1]][move[2]].draw(3)
            self.legalMoves.remove(move)


class RandomGame(Game):
    """
    Subclass for a 'random' variant of the game board.
    A random selection of lines are filled in automatically.
    """
    def __init__(self, width, height, maxPlayers=2, curPlayer=1, legalMoves=False, copy_grid=None, copy_boxes=None, movesMade=None):
        super().__init__(width, height, maxPlayers, curPlayer, legalMoves, copy_grid, copy_boxes, movesMade)
        if copy_grid is None and copy_boxes is None:
            self.make_board_random()

    def make_board_random(self):
        """
        Chooses some random lines and makes them inaccessible.
        Currently picks 25% of available lines
        """
        # first find all of the moves we want to block
        movesToMake = []
        # shuffle the list of legal moves
        legalMoves = self.get_all_legal_moves()
        random.shuffle(legalMoves)
        # then add 1 - 25% of all moves available to list
        for i in range(int(len(legalMoves)*0.25)):
            movesToMake.append(legalMoves[i])
        # now make those moves, as if we are player 3.
        for move in movesToMake:
            self.grid[move[0]][move[1]][move[2]].draw(3)
            self.legalMoves.remove(move)
