# builtin libraries
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFrame, QLabel
from PyQt5.QtCore import Qt
from PIL import Image
import os

class FileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("File Explorer")
        self.setGeometry(0,0,400,300)
        self.masterLayout = QVBoxLayout(self)
        self.loadFileWindowUi()
        self.setProperties()
        self.fileListWidget.currentRowChanged.connect(self.fileAccess)
        self.forwardButton.clicked.connect(self.nextDirectory)
        self.previousButton.clicked.connect(self.previousDirectory)
        return
    
    def setProperties(self):
        self.currentPathName = ""
        self.iteratedDirectoryList = []
        self.iamgeObjectPath = None
        self.iamgeObjectListPath = []
        self.currentImageInformation = None
        return
    
    def loadFileWindowUi(self):
        self.windowButtonLayout = QHBoxLayout()
        self.windowInnerButtonLayout = QHBoxLayout()

        self.windowButtonFrame = QFrame()
        self.windowButtonFrame.setFrameShape(QFrame.Shape.Panel)
        self.windowButtonLayout.addWidget(self.windowButtonFrame)
        self.windowButtonFrame.setLayout(self.windowInnerButtonLayout)

        self.forwardButton = QPushButton("Forward")
        self.exploreFiles = QLabel("Explore Files")
        self.previousButton = QPushButton("Back")

        self.masterLayout.addLayout(self.windowButtonLayout)
        self.windowInnerButtonLayout.addWidget(self.forwardButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.windowInnerButtonLayout.addWidget(self.exploreFiles, alignment = Qt.AlignmentFlag.AlignCenter)
        self.windowInnerButtonLayout.addWidget(self.previousButton, alignment = Qt.AlignmentFlag.AlignRight)

        self.fileListWidget = QListWidget()
        self.masterLayout.addWidget(self.fileListWidget)
        self.fileListWidget.addItems(["Files",R"C:\\", R"D:\\", R"F:\\"])
        return
    
    def storeCurrentPath(self, directory:str):
        if directory not in self.iteratedDirectoryList and directory.endswith("\\"):
            self.iteratedDirectoryList.append(self.currentPathName)
            return
        
    def refillFileListWidget(self):
        '''
            This funnction is responsible for adding all the folders and the image file names in the file list. This adds the Folders first then it add all the images in the respective directory.
        '''
        self.storeCurrentPath(self.currentPathName)

        self.fileListWidget.clear() # clears file list
        self.fileListWidget.addItem("Files")

        if os.path.exists(self.currentPathName):# and os.path.isdir(self.currentPathName):
            os.chdir(self.currentPathName)
            allPaths = os.listdir()

            for path in allPaths:# stores the Folders 
                if os.path.isdir(path):
                    self.fileListWidget.addItem(path)

            self.iamgeObjectListPath.clear() # creates the previous directory Image object list

            for path in allPaths: # stores the image Files
                for extension in [".png", ".jpeg", ".jfif", ".jpg"]:
                    if path.endswith(extension):
                        self.fileListWidget.addItem(path)
                        self.iamgeObjectListPath.append(path)
        return
    
    def fileAccess(self):
        '''
            Use as PyQt slot. File access helps the file window to open the chosen directory if it is a Folder
        '''
        currentText = QListWidgetItem(self.fileListWidget.currentItem()).text()
        if currentText != "Files":
            if "." not in currentText:
                self.currentPathName = os.path.join(self.currentPathName,currentText)
                self.refillFileListWidget()
            else:
                if currentText.split(".")[-1] in ["png", "jpeg", "jfif", "jpg"]:
                    self.iamgeObjectPath = os.path.join(self.currentPathName, currentText)
                    self.currentImageInformation = self.createImageInformation()
                    self.close()
                    return
        
    def nextDirectory(self):
        try:
            currentIndex = self.iteratedDirectoryList.index(self.currentPathName)
            if currentIndex < len(self.iteratedDirectoryList)-1:
                self.currentPathName = self.iteratedDirectoryList[currentIndex + 1]
                self.refillFileListWidget()
                return "Succeed"
            elif currentIndex == len(self.iteratedDirectoryList)-1:
                return "Final folder is reached"
            else:
                return "Unable to proceed"
        except ValueError:
            return
        
    def previousDirectory(self):
        try:
            currentIndex = self.iteratedDirectoryList.index(self.currentPathName)
            if currentIndex == 0:
                self.fileListWidget.clear()
                self.fileListWidget.addItems(["Files",R"C:\\", R"D:\\", R"F:\\"])
                return "Reached to the primary directory"
            elif currentIndex > 0:
                self.currentPathName = self.iteratedDirectoryList[currentIndex-1]
                self.refillFileListWidget()
                return "Succeed"
            else:
                return "no previous directory"
        except ValueError:
            return "Value is not present"
        
    def createImageInformation(self) -> str:
        bandInformation = ""
        if self.iamgeObjectPath != None:
            with Image.open(self.iamgeObjectPath) as imageObject:
                bands = imageObject.getbands()
                if list(bands) == ['R', 'G', 'B']:
                    red_band = imageObject.getchannel("R")
                    green_band = imageObject.getchannel("G")
                    blue_band = imageObject.getchannel("B")
                    bandInformation = f"\n{red_band}\n{green_band}\n{blue_band}"
                extremeValue = imageObject.getextrema()
            return f"""
                Path: {self.iamgeObjectPath}
                Bands: {bands}
                Band Information: {bandInformation}
                Extrema: {extremeValue}
            """
        else:
            return
    pass
    
if __name__ == '__main__':
    app = QApplication([])
    fileWindow = FileWindow()
    fileWindow.show()
    app.exec_()