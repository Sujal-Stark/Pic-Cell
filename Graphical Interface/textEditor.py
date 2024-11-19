from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QLabel, QPushButton, QLineEdit, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

class TextEditorAssembly(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setFixedSize(640,540)
        self.textEditorMasterLayout = QVBoxLayout(self)
        self.addProperties()
        self.createUI()
        self.constructUI()
        self.addWidgetAttributes()
        self.addStyleSheet()
        return
    
    def addProperties(self):
        self.comicSansFontLarger = QFont("Comic Sans MS", 16)
        self.comicSansFont = QFont("Comic Sans MS", 12)
        return
    
    def createUI(self):
        self.createframes()
        self.createLayouts()
        self.createScrollArea()
        self.createLineEdits()
        self.createButtons()
        self.createLabels()
        self.createSliders()
        return
    
    def createLayouts(self):
        self.innerTExtEditorMasterLayout = QVBoxLayout()

        self.viewZone = QVBoxLayout()
        self.controlZone = QHBoxLayout()

        self.viewPanel = QVBoxLayout()
        self.labelHolder1 = QVBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.innerViewPanel = QVBoxLayout()

        self.labelHolder2 = QVBoxLayout()

        self.controlLayout = QVBoxLayout()
        self.innerControlLayout = QVBoxLayout()

        self.advanceControlLayout = QVBoxLayout()
        self.innerAdvanceControlLayout = QVBoxLayout()
        return

    def createScrollArea(self):
        self.viewPanelScrollArea = QScrollArea()
        self.viewPanelScrollArea.setFixedSize(600,220)
        self.viewPanelScrollArea.setWidgetResizable(True)

        self.controlScrollArea = QScrollArea()
        self.controlScrollArea.setFixedSize(295,180)
        self.controlScrollArea.setWidgetResizable(True)

        self.advanceControlScrollArea = QScrollArea()
        self.advanceControlScrollArea.setFixedSize(295,180)
        self.advanceControlScrollArea.setWidgetResizable(True)
        return

    def createframes(self):
        self.textEditorMasterFrame = QFrame()
        self.textEditorMasterFrame.setFixedSize(620,520)
        self.textEditorMasterFrame.setFrameShape(QFrame.Shape.Panel)

        self.viewPanelFrame = QFrame()
        self.viewPanelFrame.setFrameShape(QFrame.Shape.Panel)

        self.controlFrame = QFrame()
        self.controlFrame.setFrameShape(QFrame.Shape.Panel)

        self.advanceControlFrame = QFrame()
        self.advanceControlFrame.setFrameShape(QFrame.Shape.Panel)
        return
    
    def createLineEdits(self):
        self.textInput = QLineEdit()
        self.textInput.setFixedSize(350, 25)
        self.textInput.setFont(self.comicSansFont)
        return
    
    def createButtons(self):
        self.selectButton = QPushButton("Select") # input button
        self.selectButton.setFixedSize(240, 25)
        self.selectButton.setFont(self.comicSansFont)

        # buttons for advancement section
        self.backGroundButton = QPushButton("Set Back Ground") # background
        self.backGroundButton.setFixedSize(250, 40)
        self.backGroundButton.setFont(self.comicSansFontLarger)
        self.borderButton = QPushButton("Set Border") # border
        self.borderButton.setFixedSize(250, 40)
        self.borderButton.setFont(self.comicSansFontLarger)
        self.colorButton = QPushButton("Choose color") # color 
        self.colorButton.setFixedSize(250, 40)
        self.colorButton.setFont(self.comicSansFontLarger)
        self.useButton = QPushButton("Use") # use
        self.useButton.setFixedSize(250, 40)
        self.useButton.setFont(self.comicSansFontLarger)

        return
    
    def createLabels(self):
        self.panelLabel = QLabel("View Window") # holder 1
        self.panelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.panelLabel.setFixedSize(600,25)
        self.panelLabel.setFont(self.comicSansFont)
        self.adjustmentLabel = QLabel("Adjustments") # holder 2
        self.adjustmentLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustmentLabel.setFixedSize(600,25)
        self.adjustmentLabel.setFont(self.comicSansFont)
        self.textLabel = QLabel("Your TEXT will show up here") # text label
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel.setFixedSize(300,40)
        self.textLabel.setFont(self.comicSansFontLarger)
        self.sizeLabel = QLabel("Set Size") # size
        self.sizeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sizeLabel.setFixedSize(200, 25)
        self.sizeLabel.setFont(self.comicSansFontLarger)
        self.rotateLabel = QLabel("Set Angle") # angle
        self.rotateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotateLabel.setFixedSize(200, 25)
        self.rotateLabel.setFont(self.comicSansFontLarger)
        return
    
    def createSliders(self):
        self.sizeSlider = QSlider() # size slider
        self.sizeSlider.setRange(0, 1920)
        self.sizeSlider.setSliderPosition(0)
        self.sizeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.sizeSlider.setFixedWidth(260)
        self.sizeSlider.setObjectName("sizeSlider")

        self.rotationSlider = QSlider() # rotate slider
        self.rotationSlider.setRange(0, 360)
        self.rotationSlider.setSliderPosition(0)
        self.rotationSlider.setOrientation(Qt.Orientation.Horizontal)
        self.rotationSlider.setFixedWidth(260)
        self.rotationSlider.setObjectName("rotationSlider")
        return

    def constructUI(self):
        self.textEditorMasterLayout.addWidget(self.textEditorMasterFrame)
        self.textEditorMasterFrame.setLayout(self.innerTExtEditorMasterLayout) # inner master

        self.innerTExtEditorMasterLayout.addLayout(self.viewZone) #zone1
        self.innerTExtEditorMasterLayout.addLayout(self.labelHolder2) # holder 2
        self.innerTExtEditorMasterLayout.addLayout(self.controlZone) # zone2

        self.viewZone.addLayout(self.viewPanel)

        self.viewPanel.addLayout(self.labelHolder1) # holder 1
        self.viewPanel.addLayout(self.inputLayout) # input layout
        self.viewPanel.addWidget(self.viewPanelScrollArea)
        self.viewPanelScrollArea.setWidget(self.viewPanelFrame)
        self.viewPanelFrame.setLayout(self.innerViewPanel) # editor

        self.controlZone.addLayout(self.controlLayout)
        self.controlZone.addLayout(self.advanceControlLayout)

        self.controlLayout.addWidget(self.controlScrollArea)
        self.controlScrollArea.setWidget(self.controlFrame)
        self.controlFrame.setLayout(self.innerControlLayout) # control layout

        self.advanceControlLayout.addWidget(self.advanceControlScrollArea)
        self.advanceControlScrollArea.setWidget(self.advanceControlFrame)
        self.advanceControlFrame.setLayout(self.innerAdvanceControlLayout) # advancement layout
        return
    
    def addWidgetAttributes(self):
        #View panel widgets
        self.labelHolder1.addWidget(self.panelLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.inputLayout.addWidget(self.textInput, alignment = Qt.AlignmentFlag.AlignCenter)

        # editor widgets
        self.innerViewPanel.addWidget(self.textLabel, alignment = Qt.AlignmentFlag.AlignCenter)

        #holder 2 panel widgets
        self.labelHolder2.addWidget(self.adjustmentLabel, alignment = Qt.AlignmentFlag.AlignCenter)

        #control panel widgets
        self.inputLayout.addWidget(self.selectButton, alignment = Qt.AlignmentFlag.AlignCenter)

        # control layout widgets
        self.innerControlLayout.addWidget(self.sizeLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.sizeSlider, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.rotateLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.rotationSlider, alignment = Qt.AlignmentFlag.AlignCenter)

        # advancement layout widgets
        self.innerAdvanceControlLayout.addWidget(self.backGroundButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.borderButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.colorButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.useButton, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
    def addStyleSheet(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #18122b;
                border-radius: 10px;
            }
            QFrame {
                border: 1px outset #4f4e4f;
                background-color: #01031c;
            }
            QFrame:hover{
                border : 2px outset #4f4e50;
            }
            QLineEdit{
                border : 1px outset #4f4e4f;
                background-color : #ffffff;
                color : #000000;
            }
            QLineEdit{
                border : 2px outset #4f4e50;
            }
            QPushButton{
                border : 1px outset #4f4e4f;
                font-style : Comic-Sans-Ms;
                background-color : #190140;
                color : #ffffff;
            }
            QPushButton:hover{
                border : 2px outset #4f4e50;
                background-color : #6edefa;
                color : #000000;
            }
            QLabel{
                border : 1px outset #4f4e4f;
                font-style : Comic-Sans-Ms;
                background-color : #190140;
                color : #ffffff;
            }
            QLabel:hover{
                border : 2px outset #4f4e50;
                background-color : #191049;
                color : #ffffff;
            }
            """
        )

if __name__ == '__main__':
    app = QApplication([])
    textEditor = TextEditorAssembly()
    textEditor.show()
    app.exec_()
    