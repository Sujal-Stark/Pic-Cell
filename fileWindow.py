# builtin libraries
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QFrame, QLabel, QFileDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PIL import Image
import os

import Constants

class FileWindow(QDialog):
    # Signals
    fileSelectedSignal = pyqtSignal()

    # Attributes
    currentPathName : str = ""
    currentSavingPathName : str = ""
    imageSavePath : str = ""
    iteratedDirectoryList : list = []
    imageObjectPath : str = None
    imageObjectListPath = []
    currentImageInformation = None
    comicSansFontLarger = QFont(Constants.FONT_COMIC_SANS_MS, 16)
    comicSansFont = QFont(Constants.FONT_COMIC_SANS_MS, 12)

    ############################################ INTERFACE ####################################################
    def firstAction(self):
        self.imageObjectPath, _ = QFileDialog.getOpenFileName(
            None, Constants.FILE_WINDOW_TITLE, "", Constants.EXTENSION_LIST
        )
        self.currentPathName = os.path.dirname(self.imageObjectPath)
        if self.currentPathName:
            self.imageObjectListPath = list(map(lambda path: os.path.join(self.currentPathName, path), os.listdir(
                self.currentPathName)))
        self.fileSelectedSignal.emit()
        return

    @staticmethod
    def createImageInformation(imagePath : str) -> str:
        bandInformation = ""
        if imagePath != "":
            with Image.open(imagePath) as imageObject:
                bands = imageObject.getbands()
                if list(bands) == ['R', 'G', 'B']:
                    redBand, greenBand = imageObject.getchannel("R"), imageObject.getchannel("G")
                    blueBand = imageObject.getchannel("B")
                    bandInformation = f"Red Band: {redBand}\nGreen Band: {greenBand}\nBlue Band: {blueBand}"
                elif list(bands) == ['C', 'M', 'Y']:
                    cBand, mBand = imageObject.getchannel("C"), imageObject.getchannel("M")
                    yBand = imageObject.getchannel("Y")
                    bandInformation = f"Cyan Band: {cBand}\nMagenta Band: {mBand}\nYellow Band: {yBand}"
                extremeValue = imageObject.getextrema()
            return f"""
                Path: {imagePath}\n
                Bands: {bands}\n
                band Information:\n{bandInformation}\n
                Extrema: {extremeValue}
            """
        else:
            return
    
    def saveFileByName(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "All Files (*)")
        if file_path:
            self.imageSavePath = file_path
            self.currentSavingPathName = os.path.dirname(self.imageSavePath)
        return
    
    def addImageHolderLayout(self):
        # will be done
        return
    
    def removeImageHolderLayout(self):
        # will be done
        return

    def showPreviewPixmap(self):
        # will be done
        return


    pass
    
if __name__ == '__main__':
    app = QApplication([])
    fileWindow = FileWindow()
    fileWindow.show()
    app.exec_()