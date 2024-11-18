# import libraries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QComboBox, QLineEdit, QPushButton
from PIL import Image

class CustomResizeWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Resize")
        self.setFixedSize(400,240)
        self.resizeWindowMasterLayout = QVBoxLayout(self)
        self.imageWidth = 0
        self.imageHeight = 0
        self.image = None
        self.createUI()
        self.createResponse()
        self.addStyleSheet()
        return
    
    def setWidthHeightOptions(self):
        
        return
        
    def createUI(self):
        self.createLayouts()
        self.createFrames()
        self.createlabels()
        self.createInputBox()
        self.createComBoBox()
        self.createButtons()
        self.construct()
        self.addWidgetConstraints()

    def createResponse(self):
        self.widthComboBox.currentTextChanged.connect(self.getInput)
        self.heightComboBox.currentTextChanged.connect(self.getInput)
        self.cancelButton.clicked.connect(self.cancelSelection)

    def createFrames(self):
        self.widthFrame = QFrame()
        self.widthFrame.setFrameShape(QFrame.Shape.Box)
        self.widthFrame.setFixedSize(self.width() - 20, self.height()//3 -10)

        self.heightFrame = QFrame()
        self.heightFrame.setFrameShape(QFrame.Shape.Box)
        self.heightFrame.setFixedSize(self.width() - 20, self.height()//3 -10)

        self.controlFrame = QFrame()
        self.controlFrame.setFrameShape(QFrame.Shape.Box)
        self. controlFrame.setFixedSize(self.width() - 20, self.height()//3 -10)
        return
    def createLayouts(self):
        self.widthValueReceiverLayout = QHBoxLayout()
        self.widthValueInnerLayout = QHBoxLayout()

        self.heightValueReceiverLayout = QHBoxLayout()
        self.heightValueInnerLayout = QHBoxLayout()

        self.actionControlLayout = QHBoxLayout()
        self.actionControlInnerLayout = QHBoxLayout()
        return
    
    def createlabels(self):
        self.widthLabel = QLabel("Width value:")
        self.heighLabel = QLabel("Height value:")
        self.widthPixLabel = QLabel("pixels")
        self.heightPixLabel = QLabel("pixels")
        return

    def createInputBox(self):
        self.widthInputBox = QLineEdit()
        self.heightInputBox = QLineEdit()
        return

    def createComBoBox(self):
        self.widthComboBox = QComboBox()
        self.widthComboBox.setObjectName("widthComboBox")

        self.heightComboBox = QComboBox()
        self.heightComboBox.setObjectName("heightComboBox")
        return
    
    def createButtons(self):
        self.continueButton = QPushButton("Continue")
        self.cancelButton = QPushButton("Cancel")
        return
    
    def construct(self):
        self.resizeWindowMasterLayout.addLayout(self.widthValueReceiverLayout)
        self.widthValueReceiverLayout.addWidget(self.widthFrame, alignment = Qt.AlignmentFlag.AlignCenter)
        self.widthFrame.setLayout(self.widthValueInnerLayout)

        self.resizeWindowMasterLayout.addLayout(self.heightValueReceiverLayout)
        self.heightValueReceiverLayout.addWidget(self.heightFrame, alignment = Qt.AlignmentFlag.AlignCenter)
        self.heightFrame.setLayout(self.heightValueInnerLayout)

        self.resizeWindowMasterLayout.addLayout(self.actionControlLayout)
        self.actionControlLayout.addWidget(self.controlFrame, alignment = Qt.AlignmentFlag.AlignCenter)
        self.controlFrame.setLayout(self.actionControlInnerLayout)
        return

    def addWidgetConstraints(self):
        self.widthValueInnerLayout.addWidget(self.widthLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.widthValueInnerLayout.addWidget(self.widthInputBox, alignment = Qt.AlignmentFlag.AlignCenter)
        self.widthValueInnerLayout.addWidget(self.widthComboBox, alignment = Qt.AlignmentFlag.AlignCenter)
        self.widthValueInnerLayout.addWidget(self.widthPixLabel, alignment = Qt.AlignmentFlag.AlignCenter)

        self.heightValueInnerLayout.addWidget(self.heighLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.heightValueInnerLayout.addWidget(self.heightInputBox, alignment = Qt.AlignmentFlag.AlignCenter)
        self.heightValueInnerLayout.addWidget(self.heightComboBox, alignment = Qt.AlignmentFlag.AlignCenter)
        self.heightValueInnerLayout.addWidget(self.heightPixLabel, alignment = Qt.AlignmentFlag.AlignCenter)

        self.actionControlInnerLayout.addWidget(self.cancelButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.actionControlInnerLayout.addWidget(self.continueButton, alignment = Qt.AlignmentFlag.AlignRight)
        return
    
    def getImageObject(self, image : Image.Image):
        self.image = image
        self.imageWidth, self.imageHeight = self.image.size
        self.widthComboBox.addItems(f"{i}" for i in range(0, self.imageWidth + 1, 10))
        self.heightComboBox.addItems(f"{i}" for i in range(0, self.imageHeight + 1, 10))
        return

    def getInput(self):
        sender = self.sender()
        if sender:
            if sender.objectName() == "widthComboBox":
                self.widthInputBox.setText(self.widthComboBox.currentText())
            elif sender.objectName() == "heightComboBox":
                self.heightInputBox.setText(self.heightComboBox.currentText())
            return
        
    def setOutput(self):
        self.close()
        if self.widthInputBox.text() and self.heightInputBox.text():
            return (int(self.widthInputBox.text()), int(self.heightInputBox.text()))
        else:
            return (self.imageWidth, self.imageHeight)
        
    def cancelSelection(self):
        if self.widthInputBox.text() and self.heightInputBox.text():
            self.widthComboBox.setCurrentText("0")
            self.heightComboBox.setCurrentText("0")
            self.widthInputBox.setText("")
            self.heightInputBox.setText("")
            self.close()
            return
        
    def getResizedImage(self, size : tuple):
        image = self.image
        try:
            image = image.resize(size=size)
        except ValueError:
            return "Undefined Image"

        self.image = image
        return self.image
    
    def continueAction(self):
        return self.getResizedImage(self.setOutput())
    
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
            QLineEdit{
                background-color : #ffffff;
                color : 000000;
                font : 12px;
            }
            QComboBox{
                background-color : #ffffff;
                color : #000000;
                font : 12px;
            }
            QComboBox : QAbstractItemView {
                background-color : #ffffff;
                color : #000000;
                font : 12px;
            }
            """
        )
    
if __name__ == '__main__':
    app = QApplication([])
    resizeWindow = CustomResizeWindow(None, Image.open(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png"))
    resizeWindow.show()
    app.exec_()