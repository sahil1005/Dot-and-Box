import unittest
import random
from DotsAndBoxes import Game, PlayerFactory
import DotsAndBoxes.MonteCarloPlayer
import DotsAndBoxes.MinimaxPlayer

class TestGameMethods(unittest.TestCase):
    def test_create_game(self):
        """
        Test creating different sizes of game.
        Assert that the grid and the boxes arrays have been created with the right dimensions.
        """
        for width in range(2, 10):
            for height in range(2, 10):
                g = Game.Game(width, height)
                self.assertEqual(len(g.grid), 2)
                self.assertEqual(len(g.grid[0]), height)
                self.assertEqual(len(g.grid[1]), width)
                self.assertEqual(len(g.grid[0][0]), width-1)
                self.assertEqual(len(g.grid[1][0]), height-1)
                self.assertEqual(len(g.boxes), height-1)
                self.assertEqual(len(g.boxes[0]), width-1)

    def test_create_game_bad_input(self):
        """
        Test creating the game with various bad inputs.
        """
        with self.assertRaises(TypeError):
            g = Game.Game(2.0, 4.0)
        with self.assertRaises(TypeError):
            g = Game.Game("string", "another")

    def test_copy(self):
        """
        Test copying a Game and make sure the copy behaves as intended.
        """
        # Make a game and make some moves but not all of them
        gOriginal = Game.Game(4, 4)
        for l in gOriginal.get_all_legal_moves()[0:12]:
            gOriginal.take_turn(l)
        # Then copy the game
        gCopy = gOriginal.get_copy()
        # Check that all lines have the same owner.
        for o in [0,1]:
            for i in range(3):
                for j in range(3):
                    self.assertEqual(gOriginal.grid[o][i][j].owner, gCopy.grid[o][i][j].owner)
        # Check all boxes have the same owner
        for i in range(3):
            for j in range(3):
                self.assertEqual(gOriginal.boxes[i][j].owner, gCopy.boxes[i][j].owner)
        # Check some other attributes
        self.assertEqual(gOriginal.currentPlayer, gCopy.currentPlayer)
        self.assertEqual(gOriginal.legalMoves, gCopy.legalMoves)
        self.assertEqual(gOriginal.get_scores(), gCopy.get_scores())

        # now check that making moves in one does not effect the other.
        gOriginal.take_turn((1, 2, 2))
        self.assertEqual(gOriginal.grid[1][2][2].owner, 1)
        self.assertEqual(gCopy.grid[1][2][2].owner, 0)
        self.assertEqual(gOriginal.currentPlayer, 2)
        self.assertEqual(gCopy.currentPlayer, 1)

    def test_play_game(self):
        """
        Test creating and playing a game.
        Assert that the game knows it's finished, and that the final score and
        winner are the same as expected.
        This test is only meaningful if test_legal_move_generation and test_game_finished
        pass.
        """
        # Make a game and get the list of all moves
        g = Game.Game(4, 4)
        legalMoves = g.get_all_legal_moves()
        # make all of the moves
        for move in legalMoves:
            g.take_turn(move)

        # Assert that the game thinks its finished
        self.assertTrue(g.is_finished())

        expectedScores = {0:0, 1:0, 2:9}
        scores = g.get_scores()
        # Assert all of the scores are as expected.
        self.assertEqual(scores, expectedScores)
        self.assertEqual(g.winner(), 2)

    def test_legal_move_generation_start(self):
        """
        Test new game legal move generation.
        Tests that generating a list of legal moves from the start of the game
        creates the expected list of moves.
        """
        g = Game.Game(4, 5)
        legalMoves = g.get_all_legal_moves()
        expectedMoves = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 3, 0), (0, 3, 1), (0, 3, 2), (0, 4, 0), (0, 4, 1), (0, 4, 2), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 1, 0), (1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 3, 0), (1, 3, 1), (1, 3, 2), (1, 3, 3)]
        self.assertEqual(legalMoves, expectedMoves)

    def test_legal_move_generation_middle(self):
        """
        Test mid game legal move generation.
        Tests that generating a list of legal moves once moves have already been
        made in the game creates the expected list of moves.
        """
        g = Game.Game(4, 5)
        # List of all moves that should be legal
        expectedMoves = [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 3, 0), (0, 3, 1), (0, 3, 2), (0, 4, 0), (0, 4, 1), (0, 4, 2), (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 1, 0), (1, 1, 1), (1, 1, 2), (1, 1, 3), (1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 3, 0), (1, 3, 1), (1, 3, 2), (1, 3, 3)]
        for i in range(10):
            # pop 10 random moves from this list of expected moves
            move = expectedMoves.pop(random.randrange(len(expectedMoves)))
            # and make those moves in the game
            g.take_turn(move)
        # Pass True to force the game to generate a new list.
        legalMoves = g.get_all_legal_moves(True)
        # Then assert that the lists are still identical
        self.assertEqual(legalMoves, expectedMoves)

    def test_move_making(self):
        """
        Test that making moves claims lines as expected.
        """
        g = Game.Game(3, 5)
        moves = g.get_all_legal_moves()
        for m in moves:
            # Check that every line is False before it is picked and True after
            self.assertFalse(g.grid[m[0]][m[1]][m[2]])
            g.take_turn(m)
            self.assertTrue(g.grid[m[0]][m[1]][m[2]])

    def test_bad_moves(self):
        """
        Ensure program behaves correctly when bad inputs are given.
        As long as it doesn't crash it passes the test.
        """
        g = Game.Game(4, 4)
        l1 = g.get_all_legal_moves()
        g.take_turn((5, 5, 5))
        g.take_turn((0, 5, 5))
        g.take_turn(0)
        g.take_turn("string")
        g.take_turn(False)
        g.take_turn(None)
        g.take_turn(0.7)
        l2 = g.get_all_legal_moves()
        self.assertEqual(l1, l2)

    def test_game_rules(self):
        """
        Test that the rules of the game are followed.
        There are specific rules that the game has that need to be tested to
        ensure they are working. These are:
            players take moves in turn
            player score increases after claiming a box
            players get an extra move after claiming a box
            game ends when all boxes/lines are claimed (see other tests)
        """
        g = Game.Game(3, 3)
        moves = [(1, 1, 0), (0, 1, 1), (1, 1, 1), (0, 1, 0), (1, 0, 0), (1, 2, 0), (1, 0, 1), (1, 2, 1)]
        # Claim lines and assert the players are alternating
        self.assertEqual(g.currentPlayer, 1)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 2)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 1)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 2)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 1)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 2)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 1)
        g.take_turn(moves.pop(0))
        self.assertEqual(g.currentPlayer, 2)
        g.take_turn(moves.pop(0))

        # now make the final 4 moves that claim the boxes and assert player stays the same
        moves = [(0, 0, 0), (0, 0, 1), (0, 2, 0), (0, 2, 1)]
        for i in range(len(moves)):
            # Check the players score goes up each turn
            self.assertEqual(g.check_score(1), i)
            self.assertEqual(g.currentPlayer, 1)
            g.take_turn(moves[i])
            self.assertEqual(g.check_score(1), i+1)
        # and check game is finished
        self.assertTrue(g.is_finished())

    def test_box_checking(self):
        """
        Test that the correct boxes are checked when move is made.
        When certain moves are made, certain boxes need to be checked.
        This test will look at the edge cases and ensure the correct boxes are
        checked & claimed.
        """
        g = Game.Game(3, 4)
        # None of these moves should claim a box
        moves = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, 2, 0), (0, 1, 0), (0, 1, 1), (1, 1, 1), (0, 2, 0), (0, 2, 1), (0, 3, 0), (0, 3, 1)]
        for m in moves:
            g.take_turn(m)
        # Check all of the boxes in the game have not been claimed
        for i in range(3):
            for j in range(2):
                if g.boxes[i][j].owner != 0:
                    self.fail("No boxes should be owned")

        # This move should claim these two boxes
        g.take_turn((1, 1, 0))
        self.assertEqual(g.boxes[0][0].owner, 2)
        self.assertEqual(g.boxes[0][1].owner, 2)

        # These moves should claim only one box each
        g.take_turn((1, 0, 1))
        self.assertEqual(g.boxes[1][0].owner, 2)
        self.assertEqual(g.boxes[1][1].owner, 0)
        g.take_turn((1, 2, 1))
        self.assertEqual(g.boxes[1][0].owner, 2)
        self.assertEqual(g.boxes[1][1].owner, 2)

        # This move shouldn't claim a box
        g.take_turn((1, 0, 2))
        self.assertEqual(g.boxes[2][0].owner, 0)
        self.assertEqual(g.boxes[2][1].owner, 0)
        # These two should
        g.take_turn((1, 1, 2))
        self.assertEqual(g.boxes[2][0].owner, 1)
        self.assertEqual(g.boxes[2][1].owner, 0)
        g.take_turn((1, 2, 2))
        self.assertEqual(g.boxes[2][0].owner, 1)
        self.assertEqual(g.boxes[2][1].owner, 1)

        self.assertTrue(g.is_finished())

    def test_game_finished(self):
        """
        Test that a finished game is reliably finished.
        """
        # Make a game and make every move so the game is finished.
        g = Game.Game(4, 4)
        legalMoves = g.get_all_legal_moves()
        for move in legalMoves:
            g.take_turn(move)

        # Check all of the boxes in the game have been claimed
        for i in range(3):
            for j in range(3):
                if g.boxes[i][j].owner == 0:
                    self.fail("All boxes should be owned")

        # Check all of the lines in the game have been claimed
        o = 0
        for o in [0,1]:
            for i in range(4):
                for j in range(3):
                    if g.grid[o][i][j].owner == 0:
                        self.fail("All lines should be owned")

        # Check there are no legal moves left to be made
        self.assertEqual(len(g.legalMoves), 0)

    def test_game_not_finished(self):
        """
        Test that a game in progress does not display as finished.
        """
        # Make a game and make some moves but not all of them.
        g = Game.Game(4, 4)
        legalMoves = g.get_all_legal_moves()
        for move in legalMoves[0:len(legalMoves):2]:
            g.take_turn(move)

        self.assertFalse(g.is_finished())

    def test_scores_correct(self):
        """
        Test that scores are awarded as expected when moves are made.
        """
        g = Game.Game(3, 3)
        # Make these 6 specific moves
        moves = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 2, 0)]
        for m in moves:
            g.take_turn(m)

        # Both players should still have 0 score at this point
        self.assertEqual(g.check_score(1), 0)
        self.assertEqual(g.check_score(2), 0)
        self.assertEqual(g.get_scores(), {0:4, 1:0, 2:0})

        # This move should give player 1 2 boxes in one turn.
        g.take_turn((1,1,0))
        self.assertEqual(g.check_score(1), 2)
        self.assertEqual(g.check_score(2), 0)
        self.assertEqual(g.get_scores(), {0:2, 1:2, 2:0})

        # Scores should not change after these 3 moves
        for m in [(0, 2, 0), (0, 2, 1), (1, 0, 1)]:
            g.take_turn(m)
        self.assertEqual(g.check_score(1), 2)
        self.assertEqual(g.check_score(2), 0)
        self.assertEqual(g.get_scores(), {0:2, 1:2, 2:0})

        # This move should give player 2 1 box.
        g.take_turn((1,1,1))
        self.assertEqual(g.check_score(1), 2)
        self.assertEqual(g.check_score(2), 1)
        self.assertEqual(g.get_scores(), {0:1, 1:2, 2:1})

        # This move should give player 2 another box.
        g.take_turn((1,2,1))
        self.assertEqual(g.check_score(1), 2)
        self.assertEqual(g.check_score(2), 2)
        self.assertEqual(g.get_scores(), {0:0, 1:2, 2:2})
        # check game is finished now.
        self.assertTrue(g.is_finished())

    def test_winner(self):
        """
        Ensure the game declares the correct winner.
        """
        g = Game.Game(4, 4)
        moves = g.get_all_legal_moves()
        for m in moves:
            g.take_turn(m)

        self.assertEqual(g.get_scores(), {0: 0, 1: 0, 2: 9})
        self.assertEqual(g.winner(), 2)

    def test_saving_scores(self):
        """
        Test that scores sent to save files are correctly saved.
        """
        filename = "test.txt"
        g = Game.Game(4, 4)
        l = g.get_all_legal_moves()
        for m in l:
            g.take_turn(m)
        g.save_statistics(filename, "w+")
        with open(filename, "r") as infile:
            lines = infile.readlines()

        self.assertEqual(lines[0], "4x4\n")
        self.assertEqual(lines[16], "(1, 1, 0)\n")
        self.assertEqual(lines[19], "(1, 2, 0)\n")
        self.assertEqual(lines[25], "0, 9\n")
        # Swapping these specific moves makes player 1 win
        l[15], l[18] = l[18], l[15]
        g = Game.Game(4, 4)
        for m in l:
            g.take_turn(m)
        g.save_statistics(filename, "a+")
        with open(filename, "r") as infile:
            lines = infile.readlines()

        self.assertEqual(lines[0], "4x4\n")
        self.assertEqual(lines[16], "(1, 1, 0)\n")
        self.assertEqual(lines[19], "(1, 2, 0)\n")
        self.assertEqual(lines[25], "0, 9\n")
        self.assertEqual(lines[26], "4x4\n")
        self.assertEqual(lines[42], "(1, 2, 0)\n")
        self.assertEqual(lines[45], "(1, 1, 0)\n")
        self.assertEqual(lines[51], "9, 0\n")

    def test_game_equality(self):
        """
        Test that game objects' eqality method works correctly.
        """
        g1 = Game.Game(3,5)
        g2 = Game.Game(3,5)
        g3 = Game.Game(3,5)
        g4 = Game.Game(5,3)
        self.assertTrue(g1 == g2)
        self.assertFalse(g1 == g4)
        move1 = (1,1,1)
        move2 = (0,0,0)
        move3 = (1,0,0)
        move4 = (0,1,1)
        #g1 and g2 always have the same moves made so should always be equal
        g1.take_turn(move1)
        g2.take_turn(move1)
        g3.take_turn(move3)
        # g3 has the same moves made but in a different order, so is not equal yet
        g1.take_turn(move2)
        g2.take_turn(move2)
        g3.take_turn(move4)

        self.assertTrue(g1 == g2)
        self.assertFalse(g1 == g3)

        g1.take_turn(move3)
        g2.take_turn(move3)
        g3.take_turn(move1)

        g1.take_turn(move4)
        g2.take_turn(move4)
        g3.take_turn(move2)
        # at this point the same moves have been made but in different orders.
        self.assertTrue(g1 == g2)
        self.assertTrue(g1 == g3)

class TestPlayerMethods(unittest.TestCase):
    def test_playerfactory(self):
        """
        Test that players returned from the player factory are correct.
        """
        factory = PlayerFactory.PlayerFactory()

        humanPlayer = factory.makePlayer("Human Player", 1)
        randomPlayer = factory.makePlayer("Random Player", 1)
        orderedPlayer = factory.makePlayer("Ordered Player", 1)
        minmaxPlayer = factory.makePlayer("Minimax Player", 1)
        monteCarloPlayer = factory.makePlayer("Monte Carlo Player", 1)
        alsoHumanPlayer = factory.makePlayer("bad input", 1)

        self.assertTrue(humanPlayer.isHuman())
        self.assertEqual(humanPlayer.__str__(), "1_human")

        self.assertTrue(alsoHumanPlayer.isHuman())
        self.assertEqual(alsoHumanPlayer.__str__(), "1_human")

        self.assertFalse(randomPlayer.isHuman())
        self.assertEqual(randomPlayer.__str__(), "1_random")

        self.assertFalse(orderedPlayer.isHuman())
        self.assertEqual(orderedPlayer.__str__(), "1_ordered")

        self.assertFalse(minmaxPlayer.isHuman())
        self.assertEqual(minmaxPlayer.__str__(), "1_minimax")

        self.assertFalse(monteCarloPlayer.isHuman())
        self.assertEqual(monteCarloPlayer.__str__(), "1_monty")

    def test_game_with_players(self):
        """
        Test that playing a game with two players works as intended.
        Simulates playing a real game with two players taking alternate turns.
        This logic is used in the same way to control game flow in the GUI.
        """
        # Make an instance of factory and game
        factory = PlayerFactory.PlayerFactory()
        game = Game.Game(4, 4)
        # Then make two players to play the game
        player1 = factory.makePlayer("Ordered Player", 1)
        player2 = factory.makePlayer("Ordered Player", 2)
        players = [player1, player2]
        # Then play the game
        while not game.is_finished():
            # Read the current player from the game object
            currentPlayer = players[game.currentPlayer-1]
            # ask the current player for their move
            move = currentPlayer.chooseMove(game.get_copy())
            # send that move to the game object.
            game.take_turn(move)
            self.assertEqual(game.movesMade[-1], move)
        # as the players are ordered we know the result.
        self.assertTrue(game.is_finished())
        self.assertEqual(game.winner(), 2)

class TestMonteCarloMethods(unittest.TestCase):
    def test_monte_carlo_tree(self):
        """
        Test the functionality of the Monte Carlo Tree class.
        """
        mct = DotsAndBoxes.MonteCarloPlayer.MonteCarloTree(1, 0.2)
        g1 = Game.Game(4,4)
        g2 = g1.get_copy()

        self.assertIsNone(mct.root)
        mct.update(g1.get_copy())
        self.assertIsInstance(mct.root, DotsAndBoxes.MonteCarloPlayer.MonteCarloNode)
        self.assertTrue(g1 == g2)
        self.assertTrue(mct.root.game == g1)
        self.assertTrue(mct.root.game == g2)
        # get two distinct moves and make them in both games
        move1 = mct.nextMove()
        if move1 == (1,1,1):
            move2 = (0,0,0)
        else:
            move2 = (1,1,1)
        g1.take_turn(move1)
        g1.take_turn(move2)
        g2.take_turn(move1)
        g2.take_turn(move2)

        # test the update and newRoot methods
        mct.update(g1.get_copy())
        self.assertEqual(g1, g2)
        self.assertEqual(mct.root.game, g1)
        self.assertEqual(mct.root.game, g2)
        self.assertFalse(mct.root.name == "Root")

    def test_monte_carlo_node(self):
        """
        Test the functionality of the Monte Carlo Node class.
        """
        g1 = Game.Game(4,4)

        n1 = DotsAndBoxes.MonteCarloPlayer.MonteCarloNode(1, g1, (0,0,0), "Root")
        self.assertEqual(n1.t, 0.0)
        self.assertEqual(n1.n, 0.0)
        self.assertEqual(n1.children, [])

        n2 = n1.chooseChild()

        self.assertIsInstance(n2, DotsAndBoxes.MonteCarloPlayer.MonteCarloNode)
        self.assertEqual(n2.t, 0.0)
        self.assertEqual(n2.n, 0.0)
        self.assertEqual(n2.children, [])

        n3 = n2.chooseChild()

        self.assertIsInstance(n3, DotsAndBoxes.MonteCarloPlayer.MonteCarloNode)
        self.assertEqual(n3.t, 0.0)
        self.assertEqual(n3.n, 0.0)
        self.assertEqual(n3.children, [])

        n3.backpropagate(True)

        self.assertEqual(n1.t, 1.0)
        self.assertEqual(n2.t, 1.0)
        self.assertEqual(n3.t, 1.0)
        self.assertEqual(n1.n, 1.0)
        self.assertEqual(n2.n, 1.0)
        self.assertEqual(n3.n, 1.0)

class TestMinimaxMethods(unittest.TestCase):
    def test_minimax_selection(self):
        """
        Test the correct operation of the Minimax algorithm.
        Minimax is deterministic. That means in a 3x3 game when Minimax goes first,
        it should always pick the same move (1,1,1). If it doesn't then something is up.
        This is with a time limit of one second and a max depth of 2.
        """
        g = Game.Game(3,3)
        minimax = DotsAndBoxes.MinimaxPlayer.MinimaxPlayer(1, colour="red", timeLimit=1, maxDepth=2)
        move = minimax.chooseMove(g.get_copy())
        self.assertEqual(move, (1,1,1))

    def test_minimax_evaluation(self):
        """
        Test that the Minimax evaluation function is consistent for both players.
        """
        # make a game and create a minimax for player 1 and player 2
        g = Game.Game(3,3)
        minimax1 = DotsAndBoxes.MinimaxPlayer.MinimaxPlayer(1)
        minimax2 = DotsAndBoxes.MinimaxPlayer.MinimaxPlayer(2)
        # make some moves to put the game in a known state
        moves = [(1,0,0),(0,0,0),(0,0,1),(1,0,1),(0,2,0),(1,1,1)]
        for m in moves:
            g.take_turn(m)
        # assert that the evaluations come out to the same but negative.
        eval1 = minimax1.evaluate(g.get_copy())
        eval2 = minimax2.evaluate(g.get_copy())
        self.assertEqual(eval1, 4)
        self.assertEqual(eval2, -4)
        # take another turn - this is a capturing move
        g.take_turn((0,1,0))
        # assert that the evaluations come out to the same but negative.
        eval1 = minimax1.evaluate(g.get_copy())
        eval2 = minimax2.evaluate(g.get_copy())
        self.assertEqual(eval1, 15)
        self.assertEqual(eval2, -15)

    # def test_(self):
    #     """
    #     Test template
    #     """
    #     pass
