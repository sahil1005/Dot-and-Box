import sys
import os
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication, QLabel, QSpinBox,
    QComboBox, QColorDialog)
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from Game import Game
import ReadStatistics
import GameGUI
import PlayerFactory
import math
from MonteCarloPlayer import MonteCarloPlayer

class ExperimentFrame(QWidget):
    """
    Start frame class includes game options, and can launch the game with these options
    """
    def __init__(self):
        super().__init__()
        self.playerFactory = PlayerFactory.PlayerFactory()
        self.p1Col = "Red"
        self.p2Col = "Blue"
        self.initUI()

    def initUI(self):
        """
        Simple start window that asks for game options.
        Has a button that launches the game window.
        """
        # set up list of all elements for easy access later
        self.elements = []
        # set up window
        self.setWindowTitle("Dots and Boxes")
        self.setGeometry(200, 200, 600, 450)
        # Title label
        titleLabel = QLabel("Dots & Boxes", self)
        titleLabel.resize(titleLabel.sizeHint())
        titleLabel.move(100, 50)
        self.elements.append(titleLabel)
        # Welcome label
        instLabel = QLabel("Choose board size and players, then click 'Start Game'!", self)
        instLabel.resize(instLabel.sizeHint())
        instLabel.move(100, 65)
        self.elements.append(instLabel)
        # Input for size
        # Two number input boxes
        widthLabel = QLabel("Width:", self)
        widthLabel.resize(widthLabel.sizeHint())
        widthLabel.move(100, 103)
        self.elements.append(widthLabel)
        self.widthInput = QSpinBox(self)
        self.widthInput.resize(self.widthInput.sizeHint())
        self.widthInput.move(150, 100)
        self.widthInput.setRange(3, 10)
        self.elements.append(self.widthInput)

        heightLabel = QLabel("Height:", self)
        heightLabel.resize(heightLabel.sizeHint())
        heightLabel.move(100, 123)
        self.elements.append(heightLabel)
        self.heightInput = QSpinBox(self)
        self.heightInput.resize(self.heightInput.sizeHint())
        self.heightInput.move(150, 120)
        self.heightInput.setRange(3, 10)
        self.elements.append(self.heightInput)

        # Input for players. Dropdowns filled with values from factory
        # Create label first
        playerOneLabel = QLabel("Player One:", self)
        playerOneLabel.resize(playerOneLabel.sizeHint())
        playerOneLabel.move(100, 183)
        self.elements.append(playerOneLabel)
        # Then create the dropdown and size it
        self.playerOneDropdown = QComboBox(self)
        self.playerOneDropdown.resize(100, 20)
        self.playerOneDropdown.move(170, 180)
        self.elements.append(self.playerOneDropdown)
        # Create the colour picker button for player colour
        self.playerOneColour = QPushButton("Colour", self)
        self.playerOneColour.resize(self.playerOneColour.sizeHint())
        self.playerOneColour.move(280, 180)
        self.playerOneColour.setStyleSheet("background-color: {}".format(self.p1Col))
        self.playerOneColour.clicked.connect(self.playerOneColourPicker)
        self.elements.append(self.playerOneColour)

        playerTwoLabel = QLabel("Player Two:", self)
        playerTwoLabel.resize(playerTwoLabel.sizeHint())
        playerTwoLabel.move(100, 203)
        self.elements.append(playerTwoLabel)
        self.playerTwoDropdown = QComboBox(self)
        self.playerTwoDropdown.resize(100, 20)
        self.playerTwoDropdown.move(170, 200)
        self.elements.append(self.playerTwoDropdown)
        self.playerTwoColour = QPushButton("Colour", self)
        self.playerTwoColour.resize(self.playerTwoColour.sizeHint())
        self.playerTwoColour.move(280, 200)
        self.playerTwoColour.setStyleSheet("background-color: {}".format(self.p2Col))
        self.playerTwoColour.clicked.connect(self.playerTwoColourPicker)
        self.elements.append(self.playerTwoColour)
        # Populate both dropdowns with the player types in Player Factory.
        for player in self.playerFactory.playerTypes:
            self.playerOneDropdown.addItem(player)
            self.playerTwoDropdown.addItem(player)

        # Number of iterations picker.
        iterPickerLabel = QLabel("Number of Trials:", self)
        iterPickerLabel.resize(iterPickerLabel.sizeHint())
        iterPickerLabel.move(100, 250)
        self.elements.append(iterPickerLabel)
        self.numTrials = QSpinBox(self)
        self.numTrials.resize(self.numTrials.sizeHint())
        self.numTrials.move(190, 250)
        self.numTrials.setRange(10, 1000)
        self.numTrials.setValue(10)
        self.elements.append(self.numTrials)

        # Button to start game
        startButton = QPushButton('Start Experiment', self)
        startButton.resize(startButton.sizeHint())
        startButton.move(100, 280)
        startButton.clicked.connect(self.startExperiment)
        self.elements.append(startButton)

        self.show()

    def hideAllElements(self):
        """
        Hides all elements at the start of an experiment run.
        """
        [x.resize(0,0) for x in self.elements]

    def updateFrame(self, i, filename):
        """
        Updates frame with current experiment run.
        """
        iterLabel = QLabel("Running trial {} of {}...".format(i, self.numTrials.value()), self)
        iterLabel.resize(iterLabel.sizeHint())
        iterLabel.move(100, 100)
        fileLabel = QLabel("Results saved to {}".format(filename), self)
        fileLabel.resize(fileLabel.sizeHint())
        fileLabel.move(100, 130)
        QApplication.processEvents()

    def playerOneColourPicker(self):
        """
        Callback for p1 colour picker button
        """
        self.p1Col = QColorDialog.getColor().name()
        self.playerOneColour.setStyleSheet("background-color: {}".format(self.p1Col))

    def playerTwoColourPicker(self):
        """
        Callback for p2 colour picker button
        """
        self.p2Col = QColorDialog.getColor().name()
        self.playerTwoColour.setStyleSheet("background-color: {}".format(self.p2Col))

    def startExperiment(self):
        """
        Starts game. Creates two players with values from inputs using the Player Factory class.
        Then creates game and sends it options and players. Finally closes itself.
        """
        playerOne = self.playerFactory.makePlayer(self.playerOneDropdown.currentText(), 1, self.p1Col)
        playerTwo = self.playerFactory.makePlayer(self.playerTwoDropdown.currentText(), 2, self.p2Col)
        players = [playerOne, playerTwo]
        width = self.widthInput.value()
        height = self.heightInput.value()
        # Create a file at the results location
        resultsFilename = "Results\\{}_{}_{}x{}.txt".format(playerOne, playerTwo, width, height)
        if not os.path.exists("Results"):
            os.makedirs("Results")
        f = open(resultsFilename,"w+")
        f.close()
        #self.hideAllElements()
        for i in range(self.numTrials.value()):
            playerOne = self.playerFactory.makePlayer(self.playerOneDropdown.currentText(), 1, self.p1Col)
            playerTwo = self.playerFactory.makePlayer(self.playerTwoDropdown.currentText(), 2, self.p2Col)
            players = [playerOne, playerTwo]
            self.updateFrame(i, resultsFilename)
            game = Game(width, height)
            self.gf = GameGUI.GameFrame(game, players, resultsFilename)
            print("Current Scores:")
            ReadStatistics.get_scores(resultsFilename)
        print("Trials finished!")
        ReadStatistics.get_scores(resultsFilename)
        #self.close()

def main(trials=100,height=3,width=3):
    app = QApplication(sys.argv)
    ex = ExperimentFrame()
    sys.exit(app.exec_())

def c_experiment(no_trials=100, timeLimit=5):
    """
    Runs an experiment with MonteCarloPlayer, altering the value for c each time.
    """
    experiment_filenames = []
    setName = "random-v-monty2-29-03"
    filename_base = "Results\\"+setName+"\\1_random_2_monty_3x3_c-{}.txt"
    playerFactory = PlayerFactory.PlayerFactory()
    try:
        os.mkdir("Results\\"+setName)
    except FileExistsError:
        pass
    # values from 1.0 to 5.0 in increments of 0.2
    c_values = [x/10 for x in range(10,51,2)]
    # also try root 2 just for kicks.
    c_values.append(math.sqrt(2))
    for c in c_values:
        # create results file
        experiment_filename = filename_base.format(c)
        experiment_filenames.append(experiment_filename)
        f = open(experiment_filename,"w+")
        f.close()
        # create players
        randomPlayer = playerFactory.makePlayer("Random Player", 1, "red")
        print("\nStarting trail with c={}".format(c))
        # run game no_trials amount of times
        for i in range(no_trials):
            game = Game(3,3)
            monteCarloPlayer = playerFactory.makePlayer("Monte Carlo Player", 2, "red", timeLimit=timeLimit, c=c)
            players = [randomPlayer, monteCarloPlayer]
            while not game.is_finished():
                player = players[game.currentPlayer-1]
                move = player.chooseMove(game.get_copy())
                game.take_turn(move)
            game.save_statistics(experiment_filename, "a+")
            print("\nCompleted trial {} with c={}.".format(i, c))
            game.print_grid()
            ReadStatistics.get_scores(experiment_filename)
    print("\n\nAll trials completed.")
    ReadStatistics.compare(experiment_filenames)

def tournament():
    playerFactory = PlayerFactory.PlayerFactory()
    # get all player types except human
    playerTypes = playerFactory.playerTypes.copy()[1:]
    filenameBase = "Results\\rand-ord-19-05\\{}"
    # set up experiment parameters
    boardSizes = [(3, 3), (4, 4), (5, 5), (6, 6)]
    noTrials = 10000
    # go through all sizes
    for size in boardSizes:
        height, width = size[0], size[1]
        gameLength = ((width-1)*height) + ((height-1)*width)
        # go through all the player types for player 1 and player 2
        for p1type in ["Random Player", "Ordered Player"]:
            for p2type in ["Random Player", "Ordered Player"]:
                if p1type == "Ordered Player" and p2type == "Ordered Player":
                    break
                # set up the results file
                p1name = p1type.split()[0]
                p2name = p2type.split()[0]
                filenameExp = "1_{}_2_{}_{}x{}.txt".format(p1name, p2name, height, width)
                experimentFilename = filenameBase.format(filenameExp)
                f = open(experimentFilename,"w+")
                f.close()
                print("Starting trials: {} vs {}".format(p1type, p2type))
                # start game trials
                for i in range(noTrials):
                    game = Game(height, width)
                    player1 = playerFactory.makePlayer(p1type, 1, timeLimit=5)
                    player2 = playerFactory.makePlayer(p2type, 2, timeLimit=5)
                    players = [player1, player2]
                    print("Starting Trial {}...".format(i+1))
                    while not game.is_finished():
                        player = players[game.currentPlayer-1]
                        move = player.chooseMove(game.get_copy())
                        game.take_turn(move)
                        progressMade = int((len(game.movesMade)/gameLength)*100)
                        progressLeft = 100 - progressMade
                        progress = "\r"+("-"*progressMade)+("|"*progressLeft)
                        print(progress, end="", flush=True)
                    game.save_statistics(experimentFilename, "a+")
                    print("\rCompleted Trial {}.".format(i+1)+" "*90, flush=True)
                print("Completed trials: {} vs {}".format(p1type, p2type))
    print("\n\nAll trials completed.")


if __name__ == '__main__':
    main()
