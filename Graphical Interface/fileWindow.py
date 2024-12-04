# builtin libraries
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFrame, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PIL import Image
from icecream import ic
import os
import psutil

class FileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("File Explorer")
        self.setGeometry(0,0,400,300)
        self.masterLayout = QVBoxLayout(self)
        self.preViewLayout = None
        # ic.disable()
        self.setProperties()
        self.createWidgets()
        self.loadFileWindowUi()
        self.createResponse()
        qss = self.readQssFile(r"Graphical Interface\fileWindow.qss")
        if qss != "":
            self.setStyleSheet(qss)
        return
    
    def createResponse(self):
        self.fileListWidget.currentItemChanged.connect(self.fileAccess)
        self.forwardButton.clicked.connect(self.nextDirectory)
        self.previousButton.clicked.connect(self.previousDirectory)
        return
    
    def createWidgets(self):
        self.forwardButton = QPushButton("Forward") # forward
        self.forwardButton.setFixedSize(100,30)
        self.forwardButton.setFont(self.comicSansFont)
        self.exploreFiles = QLabel("Explore Files") # title
        self.exploreFiles.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exploreFiles.setFixedSize(100, 25)
        self.exploreFiles.setFont(self.comicSansFont)
        self.previousButton = QPushButton("Back") # backword
        self.previousButton.setFixedSize(100,30)
        self.previousButton.setFont(self.comicSansFont)
        self.fileListWidget = QListWidget() # file list
        self.fileListWidget.setFont(self.comicSansFont)
        self.ImageFileNameEditor = QLineEdit() # input
        self.ImageFileNameEditor.setFixedSize(240, 25)
        self.ImageFileNameEditor.setFont(self.comicSansFont)
        self.fileOpenButton = QPushButton("Open") # open
        self.fileOpenButton.setFixedSize(100,30)
        self.fileOpenButton.setFont(self.comicSansFont)
        self.fileSaveButton = QPushButton("Save") # save
        self.fileSaveButton.setFixedSize(100,30)
        self.fileSaveButton.setFont(self.comicSansFont)
        self.fileExtensionListWidget = QComboBox() # extension box
        self.fileExtensionListWidget.setFixedHeight(25)
        self.fileExtensionListWidget.setFont(self.comicSansFont)
        self.fileExtensionListWidget.view().setStyleSheet(
            """
            QAbstractItemView{
                border: 2px outset #4f4e50;
                background-color : #190140;
                color : #ffffff;
                font : 12px;
            }
            """
        )
        return
    def setProperties(self):
        self.currentPathName = ""
        self.iteratedDirectoryList = []
        self.iamgeObjectPath = None
        self.iamgeObjectListPath = []
        self.currentImageInformation = None
        self.comicSansFontLarger = QFont("Comic Sans MS", 16)
        self.comicSansFont = QFont("Comic Sans MS", 12)
        return
    
    def loadFileWindowUi(self):
        self.universalHolderLayout = QHBoxLayout()
        self.motherLayout = QVBoxLayout()
        self.windowButtonLayout = QHBoxLayout()
        self.windowInnerButtonLayout = QHBoxLayout()
        self.fileOpenerLayout = QVBoxLayout()
        self.fileOpenerInnerLayout = QHBoxLayout()
        self.fileSaveAndOpenLayout = QVBoxLayout()
        self.fileExtenstionsetterLayout = QVBoxLayout()

        self.masterLayout.addLayout(self.universalHolderLayout)
        self.universalHolderLayout.addLayout(self.motherLayout)

        self.windowButtonFrame = QFrame()
        self.windowButtonFrame.setFrameShape(QFrame.Shape.Panel)
        self.windowButtonLayout.addWidget(self.windowButtonFrame)
        self.windowButtonFrame.setLayout(self.windowInnerButtonLayout)

        self.motherLayout.addLayout(self.windowButtonLayout)
        self.windowInnerButtonLayout.addWidget(self.forwardButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.windowInnerButtonLayout.addWidget(self.exploreFiles, alignment = Qt.AlignmentFlag.AlignCenter)
        self.windowInnerButtonLayout.addWidget(self.previousButton, alignment = Qt.AlignmentFlag.AlignRight)

        self.motherLayout.addWidget(self.fileListWidget)
        self.fileListWidget.addItems(["Files"] + self.getDiskList())

        self.fileOpenerFrame = QFrame()
        self.fileOpenerFrame.setFrameShape(QFrame.Shape.Panel)
        self.fileOpenerLayout.addWidget(self.fileOpenerFrame)
        self.fileOpenerFrame.setLayout(self.fileSaveAndOpenLayout)

        self.fileOpenerInnerLayout.addWidget(self.ImageFileNameEditor, alignment = Qt.AlignmentFlag.AlignCenter)
        self.fileOpenerInnerLayout.addWidget(self.fileOpenButton, alignment = Qt.AlignmentFlag.AlignRight)

        self.fileSaveAndOpenLayout.addLayout(self.fileOpenerInnerLayout)
        self.motherLayout.addLayout(self.fileOpenerLayout)
        return
    
    def storeCurrentPath(self, directory:str):
        if directory not in self.iteratedDirectoryList and directory.endswith("\\"):
            self.iteratedDirectoryList.append(self.currentPathName)
            return

    # finds out the disks in the machine
    def getDiskList(self) -> list:
        '''
        Lists out the available disks in the machine percentage of usage
        '''
        disks = psutil.disk_partitions()
        diskList = []
        for disk in disks:
            diskList.append(disk[0])
        ic(diskList)
        return diskList
      
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
                for extension in [".png", ".jpeg", ".jfif", ".jpg", ".bmp"]:
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
                if currentText.split(".")[-1] in ["png", "jpeg", "jfif", "jpg", "bmp"]:
                    self.iamgeObjectPath = os.path.join(self.currentPathName, currentText)
                    self.ImageFileNameEditor.setText(currentText)
                    self.showPreviewPixmap()
                    self.currentImageInformation = self.createImageInformation(currentText)
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
                self.fileListWidget.addItems(["Files"] + self.getDiskList())
                return "Reached to the primary directory"
            elif currentIndex > 0:
                self.currentPathName = self.iteratedDirectoryList[currentIndex-1]
                self.refillFileListWidget()
                return "Succeed"
            else:
                return "no previous directory"
        except ValueError:
            return "Value is not present"
        
    def createImageInformation(self, imagePath : str) -> str:
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
                band Infomation:\n{bandInformation}\n
                Extrema: {extremeValue}
            """
        else:
            return
    
    def saveFileByNmae(self):
        if self.fileOpenButton:
            self.fileOpenerInnerLayout.removeWidget(self.fileOpenButton)
            self.fileOpenerInnerLayout.addWidget(self.fileSaveButton, alignment = Qt.AlignmentFlag.AlignCenter)
            self.fileOpenButton.deleteLater()
            self.fileOpenButton = None
            self.fileExtensionListWidget.setFixedWidth(self.ImageFileNameEditor.width())
            self.fileExtensionListWidget.addItems([".png", ".jpeg", ".jfif", ".jpg",  ".gif", ".bmp", ".ppm", ".tiff"])
            self.fileExtenstionsetterLayout.addWidget(self.fileExtensionListWidget, alignment = Qt.AlignmentFlag.AlignCenter)
            self.fileSaveAndOpenLayout.addLayout(self.fileExtenstionsetterLayout)
            self.setWindowTitle("Save image in machine")
        self.ImageFileNameEditor.setText("")
        self.show()
        return
    
    def addImageHolderLayout(self):
        if self.preViewLayout == None:
            self.preViewLayout = QVBoxLayout() # opens the Image in this layout
            self.universalHolderLayout.addLayout(self.preViewLayout)
            self.preViewHolderFrame = QFrame()
            self.preViewLayout.addWidget(self.preViewHolderFrame)
            self.preViewHolderFrame.setFixedSize(200,280)
            self.previewHolderLabel = QLabel("Preview")
            self.previewHolderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.previewHolderLabel.setFixedSize(180,260)
            self.previewHolderInnerLayout = QVBoxLayout()
            self.preViewHolderFrame.setLayout(self.previewHolderInnerLayout)
            self.previewHolderInnerLayout.addWidget(self.previewHolderLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
    def removeImageHolderLayout(self):
        if self.preViewLayout:
            self.universalHolderLayout.removeItem(self.preViewLayout)
            self.preViewHolderFrame.deleteLater()
            self.preViewLayout.deleteLater()
            self.previewHolderInnerLayout.deleteLater()
            self.previewHolderLabel.deleteLater()
            self.preViewLayout = None

    def showPreviewPixmap(self):
        if self.iamgeObjectPath and self.preViewLayout:
            self.previewHolderLabel.hide()
            previewPixmap = QPixmap(self.iamgeObjectPath)
            previewPixmap = previewPixmap.scaled(self.preViewHolderFrame.width(), self.preViewHolderFrame.height(), aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio)
            self.previewHolderLabel.setPixmap(previewPixmap)
            self.previewHolderLabel.show()
        return
    
    def readQssFile(self, qssFile):
        try:
            with open(qssFile, 'r') as file:
                return file.read()
        except Exception:
            return ""
    pass
    
if __name__ == '__main__':
    app = QApplication([])
    fileWindow = FileWindow()
    fileWindow.show()
    app.exec_()