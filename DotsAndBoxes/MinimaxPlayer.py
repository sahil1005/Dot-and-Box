try:
    import BasicPlayers
except ModuleNotFoundError:
    import DotsAndBoxes.BasicPlayers as BasicPlayers
import time

class MinimaxPlayer(BasicPlayers.RandomPlayer):
    """
    Player that implements minimax. Inherits random player for random moves.
    Minimax algorithm with alpha-beta pruning for speed and iterative deepening
    for a time limit.
    """
    def __init__(self, playerIndex, colour="red", timeLimit=0.5, maxDepth=20):
        """
        Override for Minimax player to include time limit & max depth.
        This is the time limit given to the player to choose a move, in seconds.
        Args:
            playerIndex(int): player index in game
            colour(str): Colour for the UI to render. Defaults to Red
            timeLimit(int/float): Time limit in seconds for moves
            maxDepth(int): Max depth the computer player can reach.
        """
        self.index = playerIndex
        self.colour = colour
        self.timeLimit = timeLimit
        self.maxDepth = maxDepth

    def chooseMove(self, game):
        """
        Choose move for minimax player. This is the start of the search and looks
        at all moves that can be made by the player right now. Implements
        iterative deepening.
        When the time limit is reached, the move with the best score so far is
        chosen.
        Args:
            game(Game): Game that the player is making a move in
        Returns:
            3-Tuple[int]: move to be made.
        """
        moves = game.get_all_legal_moves()
        bestMove = (0, 0, 0)
        bestScore = -10000
        currentMaxDepth = 1
        startTime = time.time()
        # Search at max depth = 1 initially, and then increment the depth.
        # Keep incrementing until the time limit has been reached, then return
        # the best move found so far. This is iterative deepening.
        while time.time() - startTime <= self.timeLimit and currentMaxDepth <= self.maxDepth:
            for move in moves:
                # simulate the move and find the score
                copyGame = self.makeMove(game, move)
                score = self.getScore(copyGame, currentMaxDepth, -10000, 10000)
                # The move that returns the greatest score gets chosen.
                if score >= bestScore:
                    bestScore = score
                    bestMove = move
                # Break if we have reached the end of the time limit.
                if time.time() - startTime >= self.timeLimit:
                    break
            # Increment the current max depth for iterative deepening.
            currentMaxDepth += 1

        # Just in case we picked a bad move. Or no move at all.
        if game.is_legal_move(bestMove):
            return bestMove
        else:
            return self.randomMove(game)

    def getScore(self, game, depth, alpha, beta):
        """
        The recursive part of the minimax algorithm. Implements alpha-beta pruning.
        This will recursively search the tree to find the scores available at the bottom.
        Args:
            game(Game): game state to branch from.
            depth(int): current depth of search.
            alpha(int): alpha value
            beta(int): beta value
        Returns:
            int
        """
        # When we're at the bottom of the tree, return static evaluation
        if depth <= 0 or game.is_finished():
            return self.evaluate(game)

        moves = game.get_all_legal_moves()
        # Store the current player
        currentPlayer = game.currentPlayer
        # set bestScore to either high or low value depending on whose turn it is
        # also set maximise to True or False
        if currentPlayer == self.index:
            bestScore = -10000
            maximise = True
        else:
            bestScore = 10000
            maximise = False
        for move in moves:
            # Make the move and get the next state of the game.
            copyGame = self.makeMove(game, move)
            # recursive call
            score = self.getScore(copyGame, depth-1, alpha, beta)
            # Different actions depending on wether this is a min node or max node
            if maximise:
                bestScore = max(score, bestScore)
                alpha = max(alpha, bestScore)
            else:
                bestScore = min(score, bestScore)
                beta = min(beta, bestScore)
            # Alpha - beta pruning.
            if beta <= alpha:
                break
        return bestScore

    def evaluate(self, game):
        """
        Evaluate a particular game state. Get a static score.
        Args:
            game(Game): Game state to evaluate
        Returns:
            int: score calculated from game state.
        """
        # Find our own index and the other players'
        if self.index == 1:
            otherIndex = 2
        else:
            otherIndex = 1
        score = 0
        scores = game.get_scores()
        # Add 10 points for every box player has
        score += 10*scores[self.index]
        # Remove 10 for every box opponent has
        score -= 10*scores[otherIndex]
        # Evaluation needs to be different depending on whose turn it is.
        # If it's our turn next then we want boxes to complete
        if game.currentPlayer == self.index:
            for i in range(game.height-1):
                for j in range(game.width-1):
                    no_sides = game.boxes[i][j].sides_completed()
                    # 0 or 1. Don't care
                    if no_sides == 0 or no_sides == 1:
                        pass
                    # Only two, we don't want to make the third.
                    elif no_sides == 2:
                        score -= 1
                    # Three sides means we can complete the fourth and get points
                    elif no_sides == 3:
                        score += 5

        # If it's their turn next we don't want them to complete boxes
        elif game.currentPlayer == otherIndex:
            for i in range(game.height-1):
                for j in range(game.width-1):
                    no_sides = game.boxes[i][j].sides_completed()
                    # 0 or 1. Don't care
                    if no_sides == 0 or no_sides == 1:
                        pass
                    # Only two, we want them to make the third.
                    elif no_sides == 2:
                        score += 1
                    # Three sides means they can complete the fourth and get points
                    elif no_sides == 3:
                        score -= 5
        return score

    def makeMove(self, game, move):
        """
        Takes a game and a move, copies the game and makes the move in it.
        Args:
            game(Game): Game to be played in.
            move(Tuple[int]): Move to make
        Returns:
            Game: Deep copy of Game with move made
        """
        copyGame = game.get_copy()
        copyGame.take_turn(move)
        return copyGame

    def __str__(self):
        """
        String representation for minimax player. Used for writing results filenames.
        """
        return "{}_minimax".format(self.index)
