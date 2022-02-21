import sys
import os
from PyQt5.QtWidgets import QApplication
import GameGUI
import Experiment
import ReadStatistics

def main():
    if len(sys.argv) > 1:
        # This means the program can be used to read results files from command line
        # >python DotsAndBoxes Results\\1_minimax_2_monty_3x3.txt
        if os.path.isfile(sys.argv[1]):
            ReadStatistics.get_scores(sys.argv[1])
        # this is to run specific experiment in Experiment.
        elif int(sys.argv[1]) == 2:
            Experiment.tournament()
        # Launching with an extra argument will launch into expriment mode, where multiple games are played
        # >python DotsAndBoxes 1
        else:
            app = QApplication(sys.argv)
            ex = Experiment.ExperimentFrame()
            sys.exit(app.exec_())
    # This will simply launch the game
    else:
        app = QApplication(sys.argv)
        ex = GameGUI.StartFrame()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
