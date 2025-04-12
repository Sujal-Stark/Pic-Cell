from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QListWidget, QLabel, QPushButton, QLineEdit, QSlider, QShortcut, QColorDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage, QKeySequence, QColor
from PIL import Image
import sys, os
sys.path.append(os.getcwd())

# importing custom modules
from ImageManupulation.TextEditor import TextEditor

class TextEditorAssembly(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setFixedSize(980,500)
        self.textEditorMasterLayout = QVBoxLayout(self)
        self.addProperties()
        self.createUI()
        self.constructUI()
        self.addWidgetAttributes()
        self.createShortCuts()
        self.addStyleSheet()
        return
    
    def addProperties(self):
        self.comicSansFontLarger = QFont("Comic Sans MS", 16)
        self.comicSansFont = QFont("Comic Sans MS", 10)
        self.textEditFlag = False # raises flag when text text occur
        self.textBoxEditFlag = False # raises flag when box edit occur
        return
    
    def createUI(self):
        self.createframes()
        self.createLayouts()
        self.createScrollArea()
        self.createListWidgets()
        self.createLineEdits()
        self.createButtons()
        self.createLabels()
        self.createSliders()
        return
    
    def createLayouts(self):
        self.innerTExtEditorMasterLayout = QHBoxLayout()

        self.viewZone = QVBoxLayout()
        self.masterControlLayout = QVBoxLayout()
        self.masterControlInnerLayout = QVBoxLayout()
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

        self.finalizationActionHolderLayout = QHBoxLayout()
        self.innerFinalizationActionHolderLayout = QHBoxLayout()
        return

    def createScrollArea(self):
        self.viewPanelScrollArea = QScrollArea()
        self.viewPanelScrollArea.setFixedSize(300,400)
        self.viewPanelScrollArea.setWidgetResizable(True)

        self.textControlScrollArea = QScrollArea()
        self.textControlScrollArea.setFixedSize(295,350)
        self.textControlScrollArea.setWidgetResizable(True)

        self.textBoxControlScrollArea = QScrollArea()
        self.textBoxControlScrollArea.setFixedSize(295,350)
        self.textBoxControlScrollArea.setWidgetResizable(True)
        return

    def createframes(self):
        self.textEditorMasterFrame = QFrame()
        self.textEditorMasterFrame.setFixedSize(960,480)
        self.textEditorMasterFrame.setFrameShape(QFrame.Shape.Panel)

        self.viewPanelFrame = QFrame()
        self.viewPanelFrame.setFrameShape(QFrame.Shape.Panel)

        self.masterControlFrame = QFrame()
        self.masterControlFrame.setFrameShape(QFrame.Shape.Panel)

        self.controlFrame = QFrame()
        self.controlFrame.setFrameShape(QFrame.Shape.Panel)

        self.advanceControlFrame = QFrame()
        self.advanceControlFrame.setFrameShape(QFrame.Shape.Panel)

        self.finalizationActionHolderFrame = QFrame()
        self.finalizationActionHolderFrame.setFrameShape(QFrame.Shape.Panel)

        # lines
        self.textPanelEditingPanelLine1 = QFrame()
        self.textPanelEditingPanelLine1.setFrameShape(QFrame.Shape.HLine)
        self.textPanelEditingPanelLine1.setFrameShadow(QFrame.Shadow.Sunken)

        self.textBoxPanelLine = QFrame()
        self.textBoxPanelLine.setFrameShape(QFrame.Shape.HLine)
        self.textBoxPanelLine.setFrameShadow(QFrame.Shadow.Sunken)

        self.textBoxBorderLine = QFrame()
        self.textBoxBorderLine.setFrameShape(QFrame.Shape.HLine)
        self.textBoxBorderLine.setFrameShadow(QFrame.Shadow.Sunken)
        return
    
    def createLineEdits(self):
        self.textInput = QLineEdit()
        self.textInput.setFixedSize(200, 25)
        self.textInput.setFont(self.comicSansFont)
        return
    
    def createButtons(self):
        self.selectButton = QPushButton("Select") # input button
        self.selectButton.setFixedSize(100, 25)
        self.selectButton.setFont(self.comicSansFont)
        self.selectButton.clicked.connect(self.getTextFromInputLine)
        self.selectButton.setShortcut(QKeySequence("Return"))

        # buttons for advancement section
        self.backGroundButton = QPushButton("Add Text Box") # background
        self.backGroundButton.setFixedSize(250, 30)
        self.backGroundButton.setFont(self.comicSansFont)
        self.backGroundButton.setObjectName("textBoxAdderBackgroundButton")
        self.backGroundButton.clicked.connect(self.signalListener)

        self.backGroundColorButton = QPushButton("Backgound Color") # background color
        self.backGroundColorButton.setFixedSize(250, 30)
        self.backGroundColorButton.setFont(self.comicSansFont)
        self.backGroundColorButton.setObjectName("BackGroundColorButton")
        self.colorButton = QPushButton("Border color") # color 
        self.colorButton.setFixedSize(250, 30)
        self.colorButton.setFont(self.comicSansFont)
        self.colorButton.setObjectName("outlineColorButton")

        # buttons for text editing options
        self.colorPickerButton = QPushButton("Use Color pallet") # color picker
        self.colorPickerButton.setObjectName("ColorPickerButton")
        self.colorPickerButton.setFixedSize(250, 30)
        self.colorPickerButton.setFont(self.comicSansFont)
        self.colorPickerButton.clicked.connect(self.signalListener)

        # Finalization tools
        self.confirmButton = QPushButton("Confirm") # selects the edit to use in actual image
        self.confirmButton.setFixedSize(200, 30)
        self.confirmButton.setFont(self.comicSansFont)

        self.cancellationButton = QPushButton("Cancel") # Cancel the edited text
        self.cancellationButton.setFixedSize(200, 30)
        self.cancellationButton.setFont(self.comicSansFont)
        return
    
    def createListWidgets(self):
        self.anchorList = QListWidget() # stores all the anchor
        self.anchorList.setFixedSize(250, 25)
        self.anchorList.setFont(self.comicSansFont)
        self.anchorList.setObjectName("AnchorListWidget")
        self.anchorList.addItems(["Anchors", "Top Left", "Top Center", "Top Right", "Center Left", "Center", "Center Right", "Bottom Left", "Bottom Center", "Bottom Right"])
        self.anchorList.itemClicked.connect(self.signalListener)
        pass

    def createLabels(self):
        self.panelLabel = QLabel("View Window") # holder 1
        self.panelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.panelLabel.setFixedSize(300,25)
        self.panelLabel.setFont(self.comicSansFont)
        self.adjustmentLabel = QLabel("Adjustments") # holder 2
        self.adjustmentLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustmentLabel.setFixedSize(600, 25)
        self.adjustmentLabel.setFont(self.comicSansFont)
        self.textLabel = QLabel("Your TEXT will show up here") # text label
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.textLabel.setFont(self.comicSansFont)
        
        # labels for text editing options
        self.sizeLabel = QLabel("Set Size") # size
        self.sizeLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.sizeLabel.setFixedSize(100, 20)
        self.sizeLabel.setFont(self.comicSansFont)
        self.textOpacity = QLabel("Opacity") # opacity
        self.textOpacity.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.textOpacity.setFixedSize(100, 20)
        self.textOpacity.setFont(self.comicSansFont)
        self.textWidth = QLabel("Width") # text width
        self.textWidth.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.textWidth.setFixedSize(100, 20)
        self.textWidth.setFont(self.comicSansFont)

        # labels for textbox editing options
        self.boxSizeLabel = QLabel("Set Box Size") # box size
        self.boxSizeLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.boxSizeLabel.setFixedSize(100, 20)
        self.boxSizeLabel.setFont(self.comicSansFont)
        self.textBoxOpacityLabel = QLabel("Box Opacity") # box opacity
        self.textBoxOpacityLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.textBoxOpacityLabel.setFixedSize(100, 20)
        self.textBoxOpacityLabel.setFont(self.comicSansFont)
        self.textBoxBorderSizeLabel = QLabel("Border Size") # border size
        self.textBoxBorderSizeLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.textBoxBorderSizeLabel.setFixedSize(100, 20)
        self.textBoxBorderSizeLabel.setFont(self.comicSansFont)
        return
    
    def createSliders(self):
        self.sizeSlider = QSlider() # size slider
        self.sizeSlider.setRange(0, 1920)
        self.sizeSlider.setSliderPosition(0)
        self.sizeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.sizeSlider.setFixedWidth(250)
        self.sizeSlider.setObjectName("sizeSlider")
        self.sizeSlider.valueChanged.connect(self.signalListener)
        self.textOpacitySlider = QSlider() # opacity slider
        self.textOpacitySlider.setRange(0, 255)
        self.textOpacitySlider.setSliderPosition(255)
        self.textOpacitySlider.setOrientation(Qt.Orientation.Horizontal)
        self.textOpacitySlider.setFixedWidth(250)
        self.textOpacitySlider.setObjectName("textOpacitySlider")
        self.textOpacitySlider.valueChanged.connect(self.signalListener)
        self.textWidthSlider = QSlider() # text width slider
        self.textWidthSlider.setRange(0, 10)
        self.textWidthSlider.setSliderPosition(0)
        self.textWidthSlider.setOrientation(Qt.Orientation.Horizontal)
        self.textWidthSlider.setFixedWidth(250)
        self.textWidthSlider.setObjectName("textWidthSlider")
        self.textWidthSlider.valueChanged.connect(self.signalListener)

        # sliders for box editing options
        self.boxSizeSlider = QSlider() # box size slider
        self.boxSizeSlider.setRange(0, 1920) # will generate dynamically based upon image size
        self.boxSizeSlider.setSliderPosition(0)
        self.boxSizeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.boxSizeSlider.setFixedWidth(250)
        self.boxSizeSlider.setObjectName("boxSizeSlider")
        self.textBoxOpacitySlider = QSlider()# box opacity slider
        self.textBoxOpacitySlider.setRange(0,255)
        self.textBoxOpacitySlider.setSliderPosition(255)
        self.textBoxOpacitySlider.setOrientation(Qt.Orientation.Horizontal)
        self.textBoxOpacitySlider.setFixedWidth(250)
        self.textBoxOpacitySlider.setObjectName("textBoxOpacitySlider")
        self.textBoxBorderSize = QSlider() # border size slider
        self.textBoxOpacitySlider.setRange(0, 255) # will generate dynamically based upon image size
        self.textBoxBorderSize.setSliderPosition(0)
        self.textBoxBorderSize.setOrientation(Qt.Orientation.Horizontal)
        self.textBoxBorderSize.setFixedWidth(250)
        self.textBoxBorderSize.setObjectName("textBoxBorderSize")
        return

    def constructUI(self):
        self.textEditorMasterLayout.addWidget(self.textEditorMasterFrame)
        self.textEditorMasterFrame.setLayout(self.innerTExtEditorMasterLayout) # inner master

        self.innerTExtEditorMasterLayout.addLayout(self.viewZone) #zone1
        self.innerTExtEditorMasterLayout.addLayout(self.masterControlLayout)

        self.masterControlLayout.addWidget(self.masterControlFrame)
        self.masterControlFrame.setLayout(self.masterControlInnerLayout)
        self.masterControlInnerLayout.addLayout(self.labelHolder2) # holder 2
        self.masterControlInnerLayout.addLayout(self.controlZone) # zone2
        self.masterControlInnerLayout.addLayout(self.finalizationActionHolderLayout)

        self.viewZone.addLayout(self.viewPanel)

        self.viewPanel.addLayout(self.labelHolder1) # holder 1
        self.viewPanel.addLayout(self.inputLayout) # input layout
        self.viewPanel.addWidget(self.viewPanelScrollArea)
        self.viewPanelScrollArea.setWidget(self.viewPanelFrame)
        self.viewPanelFrame.setLayout(self.innerViewPanel) # editor

        self.controlZone.addLayout(self.controlLayout)
        self.controlZone.addLayout(self.advanceControlLayout)

        self.controlLayout.addWidget(self.textControlScrollArea)
        self.textControlScrollArea.setWidget(self.controlFrame)
        self.controlFrame.setLayout(self.innerControlLayout) # control layout

        self.advanceControlLayout.addWidget(self.textBoxControlScrollArea)
        self.textBoxControlScrollArea.setWidget(self.advanceControlFrame)
        self.advanceControlFrame.setLayout(self.innerAdvanceControlLayout) # advancement layout

        self.finalizationActionHolderLayout.addWidget(self.finalizationActionHolderFrame)
        self.finalizationActionHolderFrame.setLayout(self.innerFinalizationActionHolderLayout)
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
        self.innerControlLayout.addWidget(self.sizeLabel)
        self.innerControlLayout.addWidget(self.sizeSlider, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.textOpacity)
        self.innerControlLayout.addWidget(self.textOpacitySlider, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.textWidth)
        self.innerControlLayout.addWidget(self.textWidthSlider, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.textPanelEditingPanelLine1)
        self.innerControlLayout.addWidget(self.colorPickerButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerControlLayout.addWidget(self.anchorList, alignment = Qt.AlignmentFlag.AlignCenter)

        # advancement layout widgets
        self.innerAdvanceControlLayout.addWidget(self.backGroundButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.backGroundColorButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.boxSizeLabel)
        self.innerAdvanceControlLayout.addWidget(self.boxSizeSlider, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.textBoxPanelLine)

        self.innerAdvanceControlLayout.addWidget(self.textBoxBorderSizeLabel)
        self.innerAdvanceControlLayout.addWidget(self.textBoxBorderSize, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.colorButton, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerAdvanceControlLayout.addWidget(self.textBoxBorderLine)

        self.innerAdvanceControlLayout.addWidget(self.textBoxOpacityLabel)
        self.innerAdvanceControlLayout.addWidget(self.textBoxOpacitySlider, alignment = Qt.AlignmentFlag.AlignCenter)

        self.innerFinalizationActionHolderLayout.addWidget(self.cancellationButton, alignment = Qt.AlignmentFlag.AlignLeft)
        self.innerFinalizationActionHolderLayout.addWidget(self.confirmButton, alignment = Qt.AlignmentFlag.AlignRight)
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
                background-color : #190140;
                color : #ffffff;
            }
            QPushButton:hover{
                border : 2px outset #4f4e50;
                background-color : #6edefa;
                color : #000000;
            }
            QLabel{
                color : #ffffff;
            }
            QLabel:hover{
                color : #ffffff;
            }
            QListWidget{
                border : 1px outset #4f4e4f;
                background-color : #190140;
                color : #ffffff;
            }
            QScrollBar:vertical {
                border: 1px outset #4f4e4f;
                background-color: #190140;
                width: 12px;  /* Change width of vertical scrollbar */
                margin: 2px 2px 2px 2px;
            }
            QScrollBar::handle:vertical {
                background: #190140;
                min-height: 12px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background:  #4f4e4f;
            }
            QScrollBar:horizontal {
                border: none;
                background: #190140;
                height: 12px;  /* Change height of horizontal scrollbar */
                margin: 2px 2px 2px 2px;
            }
            QScrollBar::handle:horizontal {
                background: #190140;
                min-width: 12px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background:  #4f4e4f;
            }
            """
        )

    # interfacing
    def getOutput(self):
        return self.textEditor.generateFinalEdit()
    
    def getMetaInformation(self):
        return self.textEditor.meta
 
    def getPILImage(self, image : Image.Image):
        self.textEditor = TextEditor(image.convert(mode = "RGBA"))
        print("Woprking")
        self.inputImage = image
        return
    
    def createShortCuts(self) -> None:
        self.goToInputField = QShortcut(QKeySequence(Qt.Key.Key_T), self)
        self.goToInputField.activated.connect(lambda : self.textInput.setFocus())
        return

    @staticmethod
    def PILToPixmapConverter(pilImage : Image.Image):
        '''Converts a PIL Image object to a pixmap object'''
        try:
            if(pilImage):
                imageData = pilImage.convert("RGBA").tobytes("raw", "RGBA")
                qImage = QImage(imageData, pilImage.width, pilImage.height, QImage.Format.Format_RGBA8888)
                return QPixmap.fromImage(qImage)
        except Exception:
            pass

    def addImageToViewPanel(self, pilImage : Image.Image):
        try:
            if (exhibitionPixMap := self.PILToPixmapConverter(pilImage = pilImage)):
                self.textLabel.hide()
                self.textLabel.setFixedSize(exhibitionPixMap.size())
                self.textLabel.setPixmap(exhibitionPixMap)
                self.textLabel.show()
                QTimer.singleShot(
                    1, lambda : self.viewPanelScrollArea.horizontalScrollBar().setValue(self.viewPanelScrollArea.horizontalScrollBar().maximum()//2)
                )
                QTimer.singleShot(
                    1, lambda : self.viewPanelScrollArea.verticalScrollBar().setValue(self.viewPanelScrollArea.verticalScrollBar().maximum()//2)
                )
        except Exception as e:
            print(e)
        return

    def getTextFromInputLine(self):
        '''Takes the input text from inputLine and creates an imageLayer containing text'''
        if ((text := self.textInput.text()) != ""):
            self.textEditor.editText(text = text)
            pilImage = self.textEditor.generateFinalEdit()
            self.addImageToViewPanel(pilImage = pilImage)
            return
    
    def signalListener(self, signal):
        if(self.textInput.text() == ""): return
        objectName = self.sender().objectName()
        # slider action
        if (objectName == self.sizeSlider.objectName()):
            self.textEditor.editText(text = self.textInput.text(),size = signal)
            self.textEditFlag = True
        elif (objectName == self.textWidthSlider.objectName()):
            self.textEditor.editText(text= self.textInput.text(), textWidth = signal)
            self.textEditFlag = True
        elif (objectName == self.textOpacitySlider.objectName()):
            self.textEditor.editText(text = self.textInput.text(), textOpacity = signal)
            self.textEditFlag = True
        elif (objectName == self.boxSizeSlider.objectName()):
            self.textEditor.editTextBox(increment_Factor = signal)
        elif (objectName == self.textBoxOpacitySlider.objectName()):
            self.textEditor.editTextBox(opacity = signal)
        elif(objectName == self.textBoxBorderSize.objectName()):
            self.textEditor.editTextBox(lineWidth = signal)
        else:
            pass
        
        # list Widget Action
        if (objectName == self.anchorList.objectName()):
            if ((anchor := self.anchorList.currentItem().text()) != "Anchors"):
                self.textEditor.editText(text=self.textInput.text(), anchor_tag = anchor)
                self.textEditFlag = True
        
        # button Action
        if(objectName == self.colorPickerButton.objectName()):
            self.textEditor.editText(text = self.textInput.text(), color = list(QColorDialog.getColor().getRgb()[:3]))
        elif(objectName == self.colorButton.objectName()):
            self.textEditor.editTextBox(outlineColor = list(QColorDialog.getColor().getRgb()[:3]))
        elif(objectName == self.backGroundColorButton.objectName()):
            self.textEditor.editTextBox(fillColor = list(QColorDialog.getColor().getRgb()[:3]))
        elif(objectName == self.backGroundButton.objectName()):
            self.textEditor.editTextBox()
            self.boxSizeSlider.valueChanged.connect(self.signalListener)
            self.textBoxOpacitySlider.valueChanged.connect(self.signalListener)
            self.textBoxBorderSize.valueChanged.connect(self.signalListener)
            self.colorButton.clicked.connect(self.signalListener)
            self.backGroundColorButton.clicked.connect(self.signalListener)
            self.textBoxEditFlag = True

        self.addImageToViewPanel(self.textEditor.generateFinalEdit())
        self.textEditFlag = False
    pass

if __name__ == '__main__':
    app = QApplication([])
    textEditor = TextEditorAssembly()
    textEditor.getPILImage(Image.open(r"C:\Users\SUJAL KHAN\Downloads\85b4c2ae-9d5b-44f9-95d5-e96210695f98.jpg"))
    textEditor.show()
    app.exec_()
    