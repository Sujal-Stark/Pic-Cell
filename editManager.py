# important Libraries
from PyQt5.QtGui import QMouseEvent, QPixmap, QImage, QPainter
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,QFrame, QTreeWidget,
QTreeWidgetItem, QScrollArea, QLabel, QColorDialog, QSlider, QRubberBand)
from PyQt5.QtCore import Qt, QTimer, QPoint, QRect, QSize
from PyQt5.QtGui import QColor, QFont
from icecream import ic
from PIL import Image
import sys, os

# Custom import
import Constants
from fileWindow import FileWindow
from ImageframeAdjuster import FrameAdjustment
from deformer import ImageDeformer
from imageColorEnhancer import ColorImage
from imageFiltering import FilterImage
from maskGenerator import Masks
from imageOperationController import OperationFramework
from pixmapLinker import PixmapLinker, Node
from customCropWindow import CustomResizeWindow
from textEditorUI import TextEditorAssembly

class EditingActionManager(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.editSectionMasterLayout = QHBoxLayout(self)
        self.setObjectName("EditPanel")
        self.loadUi()
        self.addResponse()
        self.performImageOperation()
        qss = self.filewinowForSave.readQssFile(Constants.EDIT_MANAGER_UI_STYLE_FILE)
        if qss != "":
            self.setStyleSheet(qss)
        return
    
    def loadUi(self):
        self.addProperties()
        self.createLabels()
        self.createButtons()
        self.createFrames()
        self.createListWidgets()
        self.creteScrollAreas()
        self.createLayouts()
        self.editingTree()
        self.constructInterface()
        self.addWidgetAttributes()
        return
    
    def addResponse(self):
        self.editingTreeBody.itemClicked.connect(self.treeBodyItemclicked)
        self.chooseColorButton.clicked.connect(self.createColorPicker)
        self.setEdit.clicked.connect(self.keepEdit)
        self.filewinowForSave.fileSaveButton.clicked.connect(self.saveImage)
        self.timeHolder.timeout.connect(self.showOriginal)
        self.viewOriginal.pressed.connect(self.buttonPressedAction)
        self.viewOriginal.released.connect(self.buttonRealeaseAction)
        self.customResizeWindow.continueButton.clicked.connect(self.showPixmapFromResizeWindow)
        self.textEditHandler.confirmButton.clicked.connect(self.handleConfirmActionForTextEditHandler)
        return
    
    def addProperties(self):
        self.comicSansFontLarger = QFont("Comic Sans MS", 16)
        self.comicSansFont = QFont("Comic Sans MS", 10)
        self.filewinowForSave = FileWindow() # file window is used to open or save image
        self.currentColor = QColor(255,255,255,255)
        self.imageToEdit = "" # the name of the image which is about to get edit
        self.imageSize = (850, 600) # the size of the panel where the image must be shown
        self.ORIGINALSIZE = (850, 600) # this value is same but its like a constant
        self.valuePackage = {} # stores the edit option in edit spectrum and advancement Layout
        self.imageObject : QPixmap = None # Qpixmap object that is used everywhere
        self.ORIGINALIMAGEOBJECT = None # Qpixmap object that holds the original image
        self.IMAGETOSAVE = None # does real time edit on final image
        self.newImageObject : QPixmap = None # shows unsaved edits
        self.operationManager = OperationFramework() # framework that connects edit option with GUI
        self.savingRequired = ["Rotate", "Horizontal Flip", "Vertical Flip"] # edit which needs to save automatically
        self.signalValue = None # stores the current signal value
        self.removeableWidgets = [] # widgets in spectrum and advancement that is needed to be removed
        self.pixmapConnector = PixmapLinker() # pixmap linkedlist variable
        self.customResizeWindow = CustomResizeWindow()
        self.linker = None # undo and redo operator
        self.firstCallFlag : bool # first undo initiation flag
        self.timeHolder = QTimer() # helps to show original Image for the time
        self.timeHolder.setInterval(100)
        self.cropRubberBand = QRubberBand(QRubberBand.Shape.Rectangle) # helps to crop the image efficiently
        self.cropRubberBand.close() # initially the image is closed
        self.isDragging = False # helps to check is mouse is moving or not
        self.currentPosition = QPoint() # position differnce between top left cropRubberBand and mouse position
        self.reResizable = False # flag for resizing the rubberband widget
        self.cornerThreshold = 50 # distance in pixels to detect corner proximity
        self.aspectRatio = 0
        self.toggleHideLeftFlag = True
        self.manualCropSignal = False
        self.finalEditMeta = {
            "parent" : None,
            "child" : "",
            "signalValue" : "",
            "color" : (),
            "multivalue" : False
        }# stores data for final Edit
        self.colorVal : QColor = None
        self.multivalueOperation = False
        self.textEditHandler = TextEditorAssembly()
        return
    
    def createLabels(self):
        self.imageForEditLabel = QLabel("Edit Your Image here")
        self.imageForEditLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageForEditLabel.setFixedSize(300,40)
        self.imageForEditLabel.setStyleSheet(
            """QLabel{
                background-color : #190140;
                font-size: 12px;
                color: #ffffff;
                padding : 2px;
                border-radius : 5px;
            }
            QLabel:hover{
                background-color : #280180;
                font-size: 12px;
                color: #ffffff;
                padding : 2px;
                border-radius : 5px;
            }
            """
        )
        self.imageForEditLabel.setFont(self.comicSansFontLarger)
        self.cropRubberBand.setParent(self.imageForEditLabel)
        self.specialEditOptions = QLabel("Editing choice will show up here")
        self.specialEditOptions.setStyleSheet(
            self.imageForEditLabel.styleSheet()
        )
        self.specialEditOptions.setFont(self.comicSansFont)
        return
    
    def createButtons(self):
        self.chooseColorButton = QPushButton("Choose color")
        self.chooseColorButton.setFont(self.comicSansFont)
        self.setEdit = QPushButton("Set")
        self.setEdit.setFont(self.comicSansFont)
        self.viewOriginal = QPushButton("View Original")
        self.viewOriginal.setFont(self.comicSansFont)
        return
    
    def createColorPicker(self):
        self.colorDialog = QColorDialog() # initialising the color dialog
        self.colorDialog.setOption(QColorDialog.ShowAlphaChannel, True) # initialising alpha chanel
        self.currentColor = self.colorDialog.getColor() # getting the current color
        if self.editingTreeBody.currentItem():
            if self.editingTreeBody.currentItem().text(0) in Masks.subEditingTree.keys():
                self.colorAddresser(self.currentColor)
        return self.currentColor
    
    def createFrames(self):
        self.imageViewingFrame = QFrame()
        self.imageViewingFrame.setFrameShape(QFrame.NoFrame)
        self.imageViewingFrame.setStyleSheet("border: none;")

        self.editOptionFrame = QFrame()
        self.editOptionFrame.setFrameShape(QFrame.Shape.Box)

        self.editSpectrumFrame = QFrame()
        self.editSpectrumFrame.setFrameShape(QFrame.NoFrame)
        self.editSpectrumFrame.setStyleSheet("border: none;")

        self.advancementframe = QFrame()
        self.advancementframe.setFrameShape(QFrame.Shape.Box)
        return
    
    def createLayouts(self):
        self.editingZoneLayout = QGridLayout()

        self.editOptionPanel = QVBoxLayout()
        self.innerEditOptionPanel = QVBoxLayout()
        self.imageViewingPanel = QHBoxLayout()
        self.innerImageViewingPanel = QHBoxLayout()

        self.editControlLayout = QVBoxLayout()

        self.editSpectrumLayout = QVBoxLayout()
        self.innerEditSpectrumLayout = QGridLayout()
        self.advancementLayout = QVBoxLayout()
        self.innerAdvancementLayout = QVBoxLayout()
        self.sliderHolderLayout = QVBoxLayout()
        return
    
    def createListWidgets(self):
        return

    def creteScrollAreas(self):
        self.editableImageField = QScrollArea()
        self.editableImageField.setWidgetResizable(True)

        self.editSpectrumScrollArea = QScrollArea()
        self.editSpectrumScrollArea.setWidgetResizable(True)

        self.innerAdvancementScrollArea = QScrollArea()
        self.innerAdvancementScrollArea.setWidgetResizable(True)
        return
    
    def editingTree(self):
        self.editingTreeBody = QTreeWidget()
        self.editingTreeBody.setFont(self.comicSansFont)
        # self.editingTreeBody.setFixedSize(190,580)
        self.clearEditSpectrum()
        self.editingTreeBody.setHeaderLabel("Edit Options")
        editSections = [
            Constants.EDIT_OPTION_ADJUST, Constants.EDIT_OPTION_FILTERS,
            Constants.EDIT_OPTION_COLOR_ENHANCE, Constants.EDIT_OPTION_DEFORM_IMAGE,
            Constants.EDIT_OPTION_FRAMES, Constants.EDIT_OPTION_TEXT_EDITOR
        ]
        for editSection in editSections:
            self.editingTreeBody.addTopLevelItem(QTreeWidgetItem([editSection]))
        return
    
    def constructInterface(self):
        self.editSectionMasterLayout.addLayout(self.editingZoneLayout)
        self.editSectionMasterLayout.addLayout(self.editControlLayout)

        self.editingZoneLayout.addLayout(self.editOptionPanel, 0, 0)
        self.editOptionPanel.addWidget(self.editOptionFrame)
        self.editOptionFrame.setLayout(self.innerEditOptionPanel)

        self.editingZoneLayout.addLayout(self.imageViewingPanel, 0, 1)
        self.imageViewingPanel.addWidget(self.editableImageField)
        self.editableImageField.setWidget(self.imageViewingFrame)
        self.imageViewingFrame.setLayout(self.innerImageViewingPanel)

        self.editControlLayout.addLayout(self.editSpectrumLayout, 50)
        self.editSpectrumLayout.addWidget(self.editSpectrumScrollArea)
        self.editSpectrumScrollArea.setWidget(self.editSpectrumFrame)
        self.editSpectrumFrame.setLayout(self.innerEditSpectrumLayout)

        self.editControlLayout.addLayout(self.advancementLayout, 30)
        self.advancementLayout.addWidget(self.advancementframe)
        self.advancementframe.setLayout(self.innerAdvancementLayout)
        return
    
    def addWidgetAttributes(self):
        self.innerEditOptionPanel.addWidget(self.editingTreeBody)
        self.innerImageViewingPanel.addWidget(self.imageForEditLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.editSpectrumLayout.addWidget(self.setEdit, alignment = Qt.AlignmentFlag.AlignTop)
        self.editSpectrumLayout.addWidget(self.viewOriginal, alignment = Qt.AlignmentFlag.AlignTop)
        self.innerEditSpectrumLayout.addWidget(self.specialEditOptions, 0, 0, alignment= Qt.AlignmentFlag.AlignCenter)
        self.innerAdvancementLayout.addWidget(self.innerAdvancementScrollArea, alignment = Qt.AlignmentFlag.AlignTop)
        self.innerAdvancementLayout.addWidget(self.chooseColorButton, alignment = Qt.AlignmentFlag.AlignBottom)
        self.innerAdvancementScrollArea.setLayout(self.sliderHolderLayout)
        AdvancementOptionLabel = QLabel("Advancement Options")
        AdvancementOptionLabel.setFont(self.comicSansFont)
        AdvancementOptionLabel.setStyleSheet(self.imageForEditLabel.styleSheet())
        self.sliderHolderLayout.addWidget(AdvancementOptionLabel,alignment=Qt.AlignmentFlag.AlignCenter)
        return

    ########################################### INTERFACING #############################################
    def resizeEvent(self, a0):
        currWidth, currHeight = self.width(), self.height()
        self.editableImageField.setFixedWidth(
            int(currWidth * Constants.EDIT_SECTION_VIEW_PANEL_WIDTH_PERCENTAGE) - 10
        )
        self.editOptionFrame.setFixedWidth(
            int(currWidth * Constants.EDIT_BODY_WIDTH_PERCENTAGE) - 10,
        )
        self.editSpectrumScrollArea.setFixedWidth(
            int(currWidth * Constants.EDIT_SPECTRUM_WIDTH_PERCENTAGE) - 10
        )
        self.advancementframe.setFixedWidth(
            int(currWidth * Constants.EDIT_SPECTRUM_WIDTH_PERCENTAGE) - 10
        )
        self.innerAdvancementScrollArea.setFixedHeight(
            int(currHeight * Constants.ADVANCEMENT_PANEL_HEIGHT_PERCENTAGE - 10)
        )
        super().resizeEvent(a0)
        return

    def toggleHideLeft(self):
        if self.toggleHideLeftFlag:
            self.editOptionPanel.setParent(None)
            self.imageViewingPanel.setParent(None)
            self.editableImageField.setFixedSize(self.editableImageField.width() + 200, 610)
            self.editingZoneLayout.addLayout(self.imageViewingPanel, 0, 0)
            self.toggleHideLeftFlag = False
        else:
            self.imageViewingPanel.setParent(None)
            self.editableImageField.setFixedSize(self.editableImageField.width() - 200,610)
            self.editingZoneLayout.addLayout(self.editOptionPanel, 0, 0)
            self.editingZoneLayout.addLayout(self.imageViewingPanel, 0, 1)
            self.toggleHideLeftFlag = True
        return
    
    def addTreeItems(self, item : QTreeWidgetItem):
        parsedClass = item.text(0)
        editOptions = []
        if parsedClass == Constants.EDIT_OPTION_ADJUST:
            editOptions = FrameAdjustment.adjustmentSubEditOption
        elif parsedClass == "Filters":
            editOptions = FilterImage.filteringOption
        elif parsedClass == "Color Enhance":
            editOptions = ColorImage.colorEnhanceOptions
        elif parsedClass == "Deform Image":
            editOptions = ImageDeformer.deformOptions
        elif parsedClass == "Frames":
            editOptions = Masks.frameOptions
        for editOption in editOptions:
            item.addChild(QTreeWidgetItem([editOption]))
        editOptions.clear()
        return
    
    # stores all the meta data 
    def storeMeta(self):
        if self.editingTreeBody.currentItem().parent():
            self.finalEditMeta["parent"] = self.editingTreeBody.currentItem().parent()
            self.finalEditMeta["child"] = self.editingTreeBody.currentItem().text(0)
        else:
            self.finalEditMeta["parent"] = None
            self.finalEditMeta["child"] = self.editingTreeBody.currentItem().text(0)
        self.finalEditMeta["signalValue"] = self.signalValue if self.editingTreeBody.currentItem().text(0) != "Text Editor" else self.textEditHandler.getMetaInformation()
        self.finalEditMeta["color"] = self.colorVal
        self.finalEditMeta["multivalue"] = self.multivalueOperation
        return


    def treeBodyItemclicked(self, treeItem : QTreeWidgetItem):
        self.clearAdvancementLayer()
        if treeItem.text(0) == "Text Editor":
            try:
                if self.newImageObject == None:
                    self.newImageObject = self.imageObject
                im = self.convertPixMaptoImage(self.newImageObject)
                self.operationManager.imageObject = im
                self.textEditHandler.getPILImage(im)
                del im
                self.textEditHandler.show()
            except Exception as e:
                return "Unable to Load Text Editor"
        else:
            self.addTreeItems(item = treeItem)
            self.addSpecialMethodsToGrid(treeItem = treeItem)
            self.cropRubberBand.close()

    def clearEditSpectrum(self):
        for _ in range(self.innerEditSpectrumLayout.count()):
            currentItem = self.innerEditSpectrumLayout.takeAt(0)
            internalWidget = currentItem.widget()
            if internalWidget:
                internalWidget.deleteLater()
            self.innerEditSpectrumLayout.update()
        return
    
    def clearAdvancementLayer(self):
        if len(self.removeableWidgets) > 0:
            for widget in self.removeableWidgets:
                widget : QWidget
                self.sliderHolderLayout.removeWidget(widget)
                widget.deleteLater()
                self.sliderHolderLayout.update()
            self.removeableWidgets = []
            return

    def fillInnerAdvanceMentlayout(self, valueparserList : dict):
        self.innerEditSpectrumLayout.addWidget(
            QLabel("Editing choice will show up here"), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        if len(valueparserList) == 0:
            self.performImageOperation()
        else:
            self.clearAdvancementLayer()
            for valueDictKey in valueparserList.keys():
                # creating slider
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setFixedWidth(180)

                # setting parameters
                sliderParameter = valueparserList[valueDictKey]
                slider.setRange(sliderParameter["minVal"], sliderParameter["maxVal"])
                slider.setSliderPosition(sliderParameter["currentPosition"])
                slider.setTickInterval(sliderParameter["change"])
                slider.setObjectName(valueDictKey)
                slider.setTickPosition(QSlider.TicksBelow)
                slider.valueChanged.connect(self.performImageOperation)

                # invoking initial edit
                self.performImageOperation(signalValue = slider.sliderPosition())

                # labels and sliders are merged into GUI
                newLabel = QLabel(valueDictKey)
                self.sliderHolderLayout.addWidget(newLabel,alignment = Qt.AlignmentFlag.AlignTop)
                self.sliderHolderLayout.addWidget(slider, alignment = Qt.AlignmentFlag.AlignTop)

                # storing widgets in delete bin
                self.removeableWidgets.append(newLabel)
                self.removeableWidgets.append(slider)
            return

    # handles multiple parameters in advancement layout by generating meta signal for operation controller
    def modifySignalValueForMultipleSignal(self, key :str, signal : object):
        try:
            if isinstance(self.valuePackage[key],dict):
                return {key : signal} if len(self.valuePackage) > 1 else signal
        except KeyError:
            return signal

    def fillEditSpectrum(self, methodDict : dict):
        if len(methodDict.keys()) == 0:
            self.innerEditSpectrumLayout.addWidget(QLabel("Editing choice will show up here"), 0, 0, alignment = Qt.AlignmentFlag.AlignCenter)
            self.performImageOperation()
            return
        else:
            i, j = 0, 0
            for key in methodDict.keys():
                limit = 0
                if j > limit:
                    i += 1
                    j = 0
                currentButton = QPushButton(key)
                currentButton.setFixedHeight(40)
                currentButton.setFont(self.comicSansFontLarger)
                if key == "Custom" and self.editingTreeBody.currentItem().text(0) in ColorImage.subEditingTree.keys():
                    currentButton.clicked.connect(self.performColorOperaion)
                elif key == "Custom" and self.editingTreeBody.currentItem().text(0) == "Resize":
                    currentButton.clicked.connect(self.getCustomResized)
                elif key == "Custom" and self.editingTreeBody.currentItem().text(0) == "Rotate":
                    currentButton.clicked.connect(self.getCustomRotation)
                else:
                    currentButton.clicked.connect(self.performImageOperation)
                self.innerEditSpectrumLayout.addWidget(currentButton, i, j)
                j += 1
            self.innerEditSpectrumLayout.setVerticalSpacing(1)
            return
    
    def addSpecialMethodsToGrid(self, treeItem : QTreeWidgetItem):
        # Adds special methods to grid
        if treeItem.parent():
            self.clearEditSpectrum()
            try:
                self.valuePackage = {}
                # image adjustments
                if treeItem.parent().text(0) == "Adjust":
                    self.valuePackage = FrameAdjustment.subEditingTree[treeItem.text(0)]
                    self.fillEditSpectrum(self.valuePackage)
                
                # Image Filering
                elif treeItem.parent().text(0) == "Filters":
                    self.valuePackage = FilterImage.subEditingTree[treeItem.text(0)]
                    if treeItem.text(0) != "Edge Enhance":
                        self.fillInnerAdvanceMentlayout(self.valuePackage)
                    else:
                        self.fillEditSpectrum(self.valuePackage)

                # Image Color Enhance
                elif treeItem.parent().text(0) == "Color Enhance":
                    self.valuePackage = ColorImage.subEditingTree[treeItem.text(0)]
                    self.fillEditSpectrum(self.valuePackage)

                # Image Deforming
                elif treeItem.parent().text(0) == "Deform Image":
                    self.valuePackage = ImageDeformer.subEditingTree[treeItem.text(0)]
                    if treeItem.text(0) in ["Twist", "Double Twist", "Half Mirror", "Four Mirror"]:
                        self.fillEditSpectrum(self.valuePackage)
                    else:
                        self.fillInnerAdvanceMentlayout(self.valuePackage)

                # image Frames
                elif treeItem.parent().text(0) == "Frames":
                    self.valuePackage = Masks.subEditingTree[treeItem.text(0)]
                    self.fillInnerAdvanceMentlayout(self.valuePackage)
                return "Loading"
            except KeyError:
                return "Method access denied"
        return None

    def showPixmap(self, imageObject : QPixmap):
        self.imageForEditLabel.hide()
        self.imageForEditLabel.setFixedSize(imageObject.width(), imageObject.height())
        self.imageForEditLabel.setPixmap(imageObject)
        self.imageForEditLabel.show()
    
    def openImageInEditSection(self):
        if self.imageToEdit != "":
            self.imageSize = self.ORIGINALSIZE
            self.imageObject = QPixmap(self.imageToEdit)
            self.IMAGETOSAVE = Image.open(self.imageToEdit)
            self.operationManager.ORIGINALIMAGE = self.IMAGETOSAVE
            self.imageForEditLabel.hide()
            self.imageObject = self.imageObject.scaled(self.imageSize[0], self.imageSize[1], aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio)
            self.ORIGINALIMAGEOBJECT = self.imageObject
            self.pixmapConnector.createPixmapHead(self.imageObject, self.IMAGETOSAVE)
            self.firstCallFlag = True
            self.imageForEditLabel.setFixedSize(self.imageObject.width(), self.imageObject.height())
            self.imageForEditLabel.setPixmap(self.imageObject)
            self.imageForEditLabel.show()
            return "Opened Successfully"
        else:
            return "Error occurred"
    
    def closeImageInEditSection(self):
        if self.imageToEdit != "":
            self.imageObject = None
            self.newImageObject = None
            self.ORIGINALIMAGEOBJECT = None
            self.imageForEditLabel.hide()
            self.imageForEditLabel.setFixedSize(300,40)
            self.imageForEditLabel.setText("Edit Your Image here")
            self.clearAdvancementLayer()
            self.clearEditSpectrum()
            self.linker = None
            self.pixmapConnector.pixmapHead = None
            self.editingTreeBody.collapseAll()
            self.imageForEditLabel.show()
            self.cropRubberBand.close()
            self.innerEditSpectrumLayout.addWidget(
                QLabel("Editing choice will show up here"), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
            )
            return "Closed Successfully"
        return None

    def handleConfirmActionForTextEditHandler(self):
        self.showPixmap(
            self.overLayPixmapObjects(basePixmap = self.imageObject, overLayPixmap = self.convertImagetoPixMap(self.textEditHandler.getOutput()))
        )
        self.textEditHandler.close()
        return

    def saveImageInMachine(self):
        self.filewinowForSave.saveFileByNmae()
        return
    
    def saveImage(self):
        '''takes input like user selected name and extension and saves it in the machine in the chosen directory'''
        fileName = self.filewinowForSave.ImageFileNameEditor.text() # new file name set by user
        extension = self.filewinowForSave.fileExtensionListWidget.currentText() # user chosen extension
        directory = self.filewinowForSave.currentPathName # routed path to store the image
        if directory:
            if fileName+extension in os.listdir(directory): # if the name name and extension exist before
                fullPath = os.path.join(directory, (fileName + "_EDITED_" + extension))
            else:
                fullPath = os.path.join(directory, (fileName+extension))
            if self.IMAGETOSAVE: # fina check if the image is not null
                self.IMAGETOSAVE.convert('RGB').save(fullPath) # image is stores as RGB
                self.IMAGETOSAVE = None
                self.filewinowForSave.close() # closing the window
        return
    
    def convertPixMaptoImage(self, imageObjectEditable : QPixmap) -> Image.Image:
        '''convert's a QPixMap Image object into PIL image object'''
        if self.imageObject:
            try:
                qImage = imageObjectEditable.toImage()
                qImage = qImage.convertToFormat(QImage.Format.Format_RGBA8888)
                width, height = qImage.width(), qImage.height()
                imageData = qImage.constBits().asstring(width * height * 4)
                return Image.frombytes("RGBA", (width, height), imageData, "raw", "RGBA", 0, 1)
            except Exception:
                return None
        return None
    
    def convertImagetoPixMap(self, pilImage : Image.Image) -> str:
        try:
            if pilImage:
                data = pilImage.convert("RGBA").tobytes("raw", "RGBA")
                width, height = pilImage.size
                qImage = QImage(data, width, height, QImage.Format.Format_RGBA8888)
                self.newImageObject = QPixmap.fromImage(qImage)
        except Exception:
            return self.imageObject
        return self.newImageObject
    
    def overLayPixmapObjects(self, basePixmap : QPixmap, overLayPixmap : QPixmap) -> QPixmap:
        resultPixmap = QPixmap(basePixmap.size())
        backGround = QPainter(resultPixmap)
        backGround.drawPixmap(0, 0, basePixmap)
        backGround.drawPixmap(0, 0, overLayPixmap)
        return resultPixmap
    
    # fucntion to create reisizeImage with custom inputs
    def getCustomResized(self):
        if self.imageObject:
            self.customResizeWindow.getImageObject(self.convertPixMaptoImage(self.imageObject))
            self.customResizeWindow.show()
            return

    # shows the pixmap through showPixmap method after getting resized from rezise window    
    def showPixmapFromResizeWindow(self) -> None:
        '''Get's a pil image from customResizeWindow and shows after converting it into Pixmap'''
        if self.imageObject:
            editedPILImage = self.customResizeWindow.continueAction()
            if isinstance(editedPILImage, Image.Image):
                self.newImageObject = self.convertImagetoPixMap(editedPILImage)
                self.showPixmap(self.newImageObject)
        return

    # get's an signal value process it and perform multiple image operations
    def performImageOperation(self, signalValue : object = None):
        if self.editingTreeBody.currentItem() is not None and self.imageObject is not None:
            currentButton1 : QPushButton = self.innerEditSpectrumLayout.sender() # operational button
            self.operationManager.imageObject = self.convertPixMaptoImage(self.imageObject) # passing ImageObject

            # handles if edit occur while iterating
            if self.linker is not None:
                self.linker.previousNode = None

            sender = self.sender() # QButton or QTeeWidgetItem or QSlider
            if isinstance(sender, QPushButton):
                # invoking operation manager to perform editing
                if len(self.valuePackage.keys()) > 0:
                    if self.editingTreeBody.currentItem().text(0) == "Crop":
                        self.getCropDimention(self.valuePackage[currentButton1.text()], sender.text())
                        pilImageEdited = self.convertPixMaptoImage(self.imageObject)
                    else:
                        self.signalValue = self.valuePackage[currentButton1.text()]
                        pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem(), self.valuePackage[currentButton1.text()])

            elif signalValue == None:
                    pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem())

            elif isinstance(sender, QSlider):
                subOperation = self.editingTreeBody.currentItem().text(0)
                signalValue = self.modifySignalValueForMultipleSignal(key = sender.objectName(), signal =signalValue)
                self.signalValue = signalValue
                self.multivalueOperation = True
                self.finalEditMeta["multivalue"] = self.multivalueOperation
                pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem(), self.signalValue, self.multivalueOperation)
            
            # Initial edit for slider value operations
            elif isinstance(sender, QTreeWidget):
                self.multivalueOperation = True
                subOperation = self.editingTreeBody.currentItem()
                self.finalEditMeta["multivalue"] = self.multivalueOperation
                pilImageEdited = self.operationManager.signalManager(subOperation, None, self.multivalueOperation)

            # conversion and showing image
            self.newImageObject = self.convertImagetoPixMap(pilImage = pilImageEdited)

            if self.editingTreeBody.currentItem().parent().text(0) == "Frames":
                self.newImageObject = self.overLayPixmapObjects(self.imageObject, self.newImageObject)
            elif (self.editingTreeBody.currentItem().text(0) in self.savingRequired):
                if self.editingTreeBody.currentItem().text(0) != "Rotate" or sender.objectName() != "Custom_Rotation":
                    self.imageObject = self.newImageObject
            self.showPixmap(self.newImageObject)
        return "Succeed"
    
    def performColorOperaion(self):
        sender = self.sender() # identifies which object sent signal
        if self.imageObject: # if imageobject exits
            if sender: # if the signal is valid
                if isinstance(sender, QPushButton):
                    if sender.text() == "Custom":
                        self.colorVal = self.createColorPicker() # color choosing
                        # for color image operation
                        if self.editingTreeBody.currentItem().text(0) in ColorImage.subEditingTree.keys():
                            targetMethod = self.editingTreeBody.currentItem().text(0)
                            parentMethod = self.editingTreeBody.currentItem().parent().text(0)
                            self.operationManager.imageObject = self.convertPixMaptoImage(self.imageObject)
                            editedPILImage = self.operationManager.provideColor(parentMethod, targetMethod, self.colorVal)
            # conversion and showing image
            self.newImageObject = self.convertImagetoPixMap(pilImage = editedPILImage)
            self.showPixmap(self.newImageObject) # showing the edited picture
            return

    # operates for the direct color access  
    def colorAddresser(self, colorObject : QColor):
        # provide color to operation manager for masks class
        if self.editingTreeBody.currentItem().text(0) in Masks.subEditingTree.keys():
            targetMethod = self.editingTreeBody.currentItem().text(0) # sub method
            targetParent = self.editingTreeBody.currentItem().parent().text(0) # method
            self.colorVal = colorObject
            self.operationManager.imageObject = self.convertPixMaptoImage(self.imageObject)
            editedImage = self.operationManager.provideColor(parentMethod = targetParent, methodName = targetMethod, givenColor = colorObject)
            self.newImageObject = self.convertImagetoPixMap(editedImage)
            self.newImageObject = self.overLayPixmapObjects(self.imageObject, self.newImageObject)
        self.showPixmap(self.newImageObject)
        return
    
    def undoOperation(self):
        if self.imageObject == None:
            '''Perform Undo Operation and iterate through previously edited version'''
            return # rundo operation can't be done if no image is selected in edit
        if self.linker == None: # no Image is set by keepEdit method
            # copies the real pixmap connectors pixmapHead with the linker
            if self.pixmapConnector.pixmapHead and self.firstCallFlag: # works if pixMapHead Exists and operating undo
                if self.pixmapConnector.pixmapHead:
                    self.linker = self.pixmapConnector.pixmapHead # copying current image object for iterating through LL
                    if self.linker.nextNode and self.linker.nextNode.image:
                        self.linker = self.linker.nextNode
                        self.imageObject = self.linker.image
                        self.newImageObject = self.linker.image
                        self.IMAGETOSAVE = self.linker.PILImage
                        if self.IMAGETOSAVE:
                            self.IMAGETOSAVE.show()
                        else:
                            ic(self.IMAGETOSAVE)
                    self.showPixmap(self.linker.image)
                    self.firstCallFlag = False
        else:
            if self.linker.nextNode:
                if self.linker.image:
                    ic("Nextnode")
                    self.linker = self.linker.nextNode
                    self.imageObject = self.linker.image
                    self.newImageObject = self.linker.image
                    self.IMAGETOSAVE = self.linker.PILImage
                    # if self.IMAGETOSAVE:
                    #         self.IMAGETOSAVE.show()
                    # else:
                    #     ic(self.IMAGETOSAVE)
                    self.showPixmap(self.linker.image)
        return

    # shows the latest Image
    def redoOperation(self):
        '''Perform Redo Operation and iterate through after the current edited version'''
        if self.imageObject == None:
            return
        if self.linker: # works if Connector exists
            if self.linker.previousNode: # works till the last node at oposite direction
                self.linker : Node = self.linker.previousNode
                self.imageObject = self.linker.image
                self.IMAGETOSAVE = self.linker.PILImage
                # if(self.IMAGETOSAVE):
                #     self.IMAGETOSAVE.show()
                # else:
                #     ic(self.IMAGETOSAVE)
                self.showPixmap(self.linker.image)
        return
    
    def keepEdit(self):
        if self.newImageObject:
            if self.editingTreeBody.currentItem().text(0) == "Crop":
                topLeftBand = self.imageForEditLabel.mapTo(self.imageForEditLabel, self.cropRubberBand.geometry().topLeft())
                rectBand = QRect(topLeftBand, self.cropRubberBand.size())
                self.signalValue = list(rectBand.getCoords())
                self.newImageObject = self.convertImagetoPixMap(self.frameAdjustment.cropImage(self.signalValue))
                self.cropRubberBand.close()
                self.showPixmap(self.newImageObject)
            self.storeMeta()
            ic(self.finalEditMeta)
            self.IMAGETOSAVE = self.operationManager.editfromParsedData(self.finalEditMeta)
            # self.IMAGETOSAVE.show()
            self.imageObject = self.newImageObject
            if self.linker: # saves the copy of current edit in linkedlist
                self.linker = self.pixmapConnector.addPixmap(self.linker, self.imageObject)
            else:
                self.pixmapConnector.pixmapHead = self.pixmapConnector.addPixmap(self.pixmapConnector.pixmapHead, self.imageObject, self.IMAGETOSAVE)
            self.signalValue = None
            self.multivalueOperation = False
            self.colorVal = None
            return


    def showOriginal(self):
        if self.ORIGINALIMAGEOBJECT:
            self.showPixmap(self.ORIGINALIMAGEOBJECT)
            return
    
    def buttonPressedAction(self):
        self.timeHolder.start()
        return
    
    def buttonRealeaseAction(self):
        if self.timeHolder.isActive() and self.ORIGINALIMAGEOBJECT:
            self.timeHolder.stop()
            self.showPixmap(self.imageObject)
            return
        
    def getCropDimention(self, signal, text : str):
        self.frameAdjustment = FrameAdjustment()
        self.frameAdjustment.getImageObject(self.convertPixMaptoImage(self.imageObject))
        if text != "Custom":
            a,b,c,d = self.frameAdjustment.sendCropDimension(signal)
            self.cropRubberBand.setFixedSize(int(c-a), int(d-b))
            self.cropRubberBand.move(int(a),int(b))
            self.cropRubberBand.show()
        else:
            self.cropRubberBand.close()
            self.manualCropSignal = True
        return

    # helps to find the edges of CropRubberband
    def isCornerReached(self, pos : QPoint):
        """Check if the given position is near any corner of the rubber band."""
        self.aspectRatio = self.cropRubberBand.width()/self.cropRubberBand.height()
        rect = self.cropRubberBand.geometry()
        corner_rect = QRect(rect.right() - 50, rect.bottom() - 50, 100, 100)
        return corner_rect.contains(QWidget(self.cropRubberBand.parent()).mapFromGlobal(pos))

    def mousePressEvent(self, event : QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            localPosition = self.cropRubberBand.parent().mapFromGlobal(event.globalPos())
            if self.manualCropSignal == False:
                if self.cropRubberBand.geometry().contains(localPosition):
                    if self.isCornerReached(event.globalPos()):
                        self.setCursor(Qt.CursorShape.ClosedHandCursor)
                        self.reResizable = True
                        self.currentPosition = event.globalPos()
                    else:
                        if not self.cropRubberBand.isVisible():
                            self.setCursor(Qt.CursorShape.ArrowCursor)
                            self.isDragging = True
                            self.currentPosition = event.pos() - self.cropRubberBand.pos()
                        else:
                            self.cropRubberBand.close()
                            self.setCursor(Qt.CursorShape.ArrowCursor)
                            self.isDragging = True
                            self.currentPosition = event.pos() - self.cropRubberBand.pos()
                            self.cropRubberBand.show()
            else:
                self.setCursor(Qt.CursorShape.CrossCursor)
                self.currentPosition = self.imageForEditLabel.mapFromGlobal(event.globalPos())

    def mouseMoveEvent(self, event : QMouseEvent):
        if self.manualCropSignal:
            self.cropRubberBand.show()
            mousePos = self.imageForEditLabel.mapFromGlobal(event.globalPos())
            diff = mousePos - self.currentPosition
            self.cropRubberBand.setGeometry(QRect(self.currentPosition, QSize(diff.x(), diff.y())))
            self.cropRubberBand.show()
        elif self.isDragging:
            new_pos = event.pos() - self.currentPosition
            self.cropRubberBand.move(new_pos)
        elif self.reResizable:
            newPosition = self.cropRubberBand.mapFromGlobal(event.globalPos())
            if newPosition.x() >= newPosition.y() * self.aspectRatio:
                new_width = newPosition.x()
                new_height = new_width//self.aspectRatio
            else:
                new_height = newPosition.y()
                new_width = int(new_height * self.aspectRatio)
            self.cropRubberBand.setFixedSize(int(new_width), int(new_height))
            # Update the start position to the current position for continuous resizing
            self.currentPosition = event.globalPos()

    def mouseReleaseEvent(self, event : QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isDragging = False
            self.reResizable = False
            self.currentPosition = None
            self.manualCropSignal = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def getCustomRotation(self):
        self.clearAdvancementLayer()
        newSlider = QSlider()
        newSlider.setFixedWidth(180)
        newSlider.setRange(0, 360)
        newSlider.setOrientation(Qt.Orientation.Horizontal)
        newSlider.setSliderPosition(0)
        newSlider.setTickInterval(30)
        newSlider.setObjectName("Custom_Rotation")
        newSlider.setTickPosition(QSlider.TicksBelow)
        newSlider.valueChanged.connect(self.performImageOperation)
        newLabel = QLabel("Angle")
        self.sliderHolderLayout.addWidget(newLabel, alignment = Qt.AlignmentFlag.AlignLeft)
        self.sliderHolderLayout.addWidget(newSlider, alignment = Qt.AlignmentFlag.AlignCenter)
        self.removeableWidgets.append(newLabel)
        self.removeableWidgets.append(newSlider)
        return
    pass