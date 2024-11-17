# builtin libraries
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QPushButton, QFrame, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
import os

class FileWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("File Explorer")
        self.setGeometry(0,0,400,300)
        self.masterLayout = QVBoxLayout(self)
        self.preViewLayout = None
        self.loadFileWindowUi()
        self.setProperties()
        self.createResponse()
        self.addStyleSheet()
        return
    
    def createResponse(self):
        self.fileListWidget.currentItemChanged.connect(self.fileAccess)
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

        self.forwardButton = QPushButton("Forward")
        self.exploreFiles = QLabel("Explore Files")
        self.previousButton = QPushButton("Back")

        self.motherLayout.addLayout(self.windowButtonLayout)
        self.windowInnerButtonLayout.addWidget(self.forwardButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.windowInnerButtonLayout.addWidget(self.exploreFiles, alignment = Qt.AlignmentFlag.AlignCenter)
        self.windowInnerButtonLayout.addWidget(self.previousButton, alignment = Qt.AlignmentFlag.AlignRight)

        self.fileListWidget = QListWidget()
        self.motherLayout.addWidget(self.fileListWidget)
        self.fileListWidget.addItems(["Files",R"C:\\", R"D:\\", R"F:\\"])

        self.fileOpenerFrame = QFrame()
        self.fileOpenerFrame.setFrameShape(QFrame.Shape.Panel)
        self.fileOpenerLayout.addWidget(self.fileOpenerFrame)
        self.fileOpenerFrame.setLayout(self.fileSaveAndOpenLayout)

        self.ImageFileNameEditor = QLineEdit()
        self.ImageFileNameEditor.setFixedWidth(260)
        self.fileOpenButton = QPushButton("Open")
        self.fileSaveButton = QPushButton("Save")

        self.fileOpenerInnerLayout.addWidget(self.ImageFileNameEditor, alignment = Qt.AlignmentFlag.AlignCenter)
        self.fileOpenerInnerLayout.addWidget(self.fileOpenButton, alignment = Qt.AlignmentFlag.AlignRight)

        self.fileSaveAndOpenLayout.addLayout(self.fileOpenerInnerLayout)
        self.motherLayout.addLayout(self.fileOpenerLayout)
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
            self.fileExtensionListWidget = QComboBox()
            self.fileExtensionListWidget.setFixedWidth(self.ImageFileNameEditor.width())
            self.fileExtensionListWidget.addItems([".png", ".jpeg", ".jfif", ".jpg"])
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
            self.preViewHolderFrame.setFixedSize(200,200)
            self.previewHolderLabel = QLabel("Preview")
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
    
    def addStyleSheet(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #18122b;
                border-radius: 0px;
            }
            QPushButton {
                border: 1px outset #4f4e4f;
                background-color: #190140;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                border: 1px outset #4f4e4f;
                background-color: #280180;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QFrame {
                border: 2px outset #4f4e4f;
                background-color: #020f17;
                border-radius: 10px;
                padding : 1px;
            }
            QFrame:hover {
                border: 2px outset #4f4e4f;
                background-color: #020f1c;
                border-radius: 10px;
                padding : 1px;
            }
            QLabel {
                background-color : #190140;
                font-size: 12px;
                color: #ffffff;
                padding : 2px;
                border-radius : 5px;
            }
            QLabel:hover {
                background-color : #280180;
                font-size: 12px;
                color: #ffffff;
                padding : 2px;
                border-radius : 5px;
            }
            QListWidget{
                border: 2px outset #4f4e4f;
                color : #ffffff;
                font : 14px;
                background-color: #020f1c;
                border-radius: 10px;
                padding : 1px;
            }
            """
        )
    pass
    
if __name__ == '__main__':
    app = QApplication([])
    fileWindow = FileWindow()
    fileWindow.show()
    app.exec_()