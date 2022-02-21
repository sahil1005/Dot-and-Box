from .Game import Game
import random

class GameHandler:
    def __init__(self, width=4, height=4):
        self.game = Game(width, height)
        self.no_players = 2


    def play_game(self):
        """
        Can play the game. Simply loops inputting moves with a catch so invalid
        moves are asked for again.
        """
        player = 0
        print("When playing the game, enter moves in the format \"0 0 0\".")
        while not self.game.is_finished():
            self.game.print_grid()
            self.game.print_scores()
            player = self.game.currentPlayer
            moveRaw = input("\nPlayer {} enter your move: ".format(player))
            if "r" in moveRaw:
                move = self.random_move()
            else:
                move = [int(x) for x in moveRaw.split()]
            while not self.game.is_legal_move(move):
                moveRaw = input("\nPlayer {} enter your move: ".format(player))
                if "r" in moveRaw:
                    move = self.random_move()
                else:
                    move = [int(x) for x in moveRaw.split()]
            self.game.take_turn(move)

        self.game.print_grid()
        print("Player {} wins!".format(self.game.winner()))

    def random_move(self):
        """
        Returns a random legal move.
        Returns:
            3-tuple(int)
        """
        move = random.choice(self.game.get_all_legal_moves())
        print("Making random move ({}, {}, {})".format(move[0], move[1], move[2]))
        return move

w = int(input("Enter Width: "))
h = int(input("Enter Height: "))
newGame = GameHandler(w,h)
newGame.play_game()
