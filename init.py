from PyQt5.QtWidgets import (QApplication, QSplashScreen)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import sys

# custom Import
from MasterGraphicalInterface import MasterWindow
import Constants

def startApplication(splashScreenObject : QSplashScreen, window : MasterWindow) -> None:
    splashScreenObject.finish(window)
    window.show()
    return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splashImage = QPixmap(Constants.SPLASH_SCREEN_PATH)
    splashScreen = QSplashScreen(splashImage)
    splashScreen.show()
    pic_cell = MasterWindow()
    QTimer.singleShot(Constants.SPLASH_SCREEN_TIME, lambda : startApplication(splashScreen, pic_cell))
    app.exec_()
