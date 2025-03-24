from qt_ui import SeparatorUI
from PyQt6.QtWidgets import QApplication

from page import ScorePages
import sys


# TODO: argument parser

if __name__ == "__main__":
    score_pager = ScorePages("./samples/imgs", "./sample_config.json")

    app = QApplication(sys.argv)
    window = SeparatorUI(score_pager)
    window.show()
    sys.exit(app.exec())