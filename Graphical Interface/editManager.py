# important Libraries
from PyQt5.QtGui import QPixmap, QImage, QPainter, QKeySequence
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,QFrame, QAction, QShortcut, QTreeWidget, QTreeWidgetItem, QScrollArea, QLabel, QColorDialog, QSlider, QApplication
from PyQt5.QtCore import Qt
from threading import Thread
from PIL import Image
import sys, os

# adding current path to the system
sys.path.append(os.getcwd())
from fileWindow import FileWindow
from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.deformer import ImageDeformer
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.imageFiltering import FilterImage
from ImageManupulation.maskGenerator import Masks
from imageOperationController import OperationFramework
from pixmapLinker import PixmapLinker, Node

class EditingActionManager(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.editSectionMasterLayout = QHBoxLayout(self)
        self.loadUi()
        self.addResponse()
        self.performImageOperation()
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
        self.editingTreeBody.itemChanged.connect(self.clearAdvancementLayer)
        self.chooseColorLabel.clicked.connect(self.createColorPicker)
        self.setEdit.clicked.connect(self.keepEdit)
        self.filewinowForSave.fileSaveButton.clicked.connect(self.saveImage)
        return
    
    def addProperties(self):
        self.filewinowForSave = FileWindow() # file window is used to open or save image
        self.currentColor = ""
        self.imageToEdit = "" # the name of the image which is about to get edit
        self.imageSize = (850, 600) # the size of the panel where the image must be shown
        self.ORIGINALSIZE = (850, 600) # this value is same but its like a constant
        self.valuePackage = {}
        self.imageObject : QPixmap = None
        self.newImageObject : QPixmap = None
        self.operationManager = OperationFramework()
        self.savingRequired = ["Rotate", "Horizontal Flip", "Vertical Flip"]
        self.removeableWidgets = []
        self.pixmapConnector = PixmapLinker()
        self.linker = None
        self.firstCallFlag : bool
        return
    
    def createLabels(self):
        self.imageForEditLabel = QLabel("Edit Your Image here")
        self.specialEditOptions = QLabel("Editing choice will show up here")
        return
    
    def createButtons(self):
        self.chooseColorLabel = QPushButton("Choose color")
        self.setEdit = QPushButton("Set")
        return
    
    def createColorPicker(self):
        self.currentColor = QColorDialog.getColor()
        return
    
    def createFrames(self):
        self.imageViewingFrame = QFrame()
        self.imageViewingFrame.setFrameShape(QFrame.Shape.Box)

        self.editOptionFrame = QFrame()
        self.editOptionFrame.setFrameShape(QFrame.Shape.Box)

        self.editSpectrumFrame = QFrame()
        self.editSpectrumFrame.setFrameShape(QFrame.Shape.Box)

        self.advancementframe = QFrame()
        self.advancementframe.setFrameShape(QFrame.Shape.Box)
        return
    
    def createLayouts(self):
        self.editingZoneLayout = QHBoxLayout()

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
        self.ScrollEditingBody = QScrollArea()
        self.ScrollEditingBody.setWidgetResizable(True)

        self.editableImageField = QScrollArea()
        self.editableImageField.setWidgetResizable(True)
        self.editableImageField.setFixedSize(860,610)

        self.editSpectrumScrollArea = QScrollArea()
        self.editSpectrumScrollArea.setWidgetResizable(True)
        self.editSpectrumScrollArea.setFixedSize(230,360)

        self.innerAdvancementScrollArea = QScrollArea()
        self.innerAdvancementScrollArea.setWidgetResizable(True)
        self.innerAdvancementScrollArea.setFixedSize(210, 160)
        return
    
    def editingTree(self):
        self.editingTreeBody = QTreeWidget()
        self.editingTreeBody.setColumnCount(1)
        self.editingTreeBody.setHeaderLabel("Editing Body")
        editSections = ["Adjust", "Filters", "Color Enhance", "Deform Image", "Frames", "Collage"]
        for editSection in editSections:
            self.editingTreeBody.addTopLevelItem(QTreeWidgetItem([editSection]))
        return
    
    def constructInterface(self):
        self.editSectionMasterLayout.addLayout(self.editingZoneLayout, 95)
        self.editSectionMasterLayout.addLayout(self.editControlLayout, 20)

        self.editingZoneLayout.addLayout(self.editOptionPanel, 15)
        self.editOptionPanel.addWidget(self.editOptionFrame)
        self.editOptionFrame.setLayout(self.innerEditOptionPanel)

        self.editingZoneLayout.addLayout(self.imageViewingPanel, 85)
        self.imageViewingPanel.addWidget(self.editableImageField)
        self.editableImageField.setWidget(self.imageViewingFrame)
        self.imageViewingFrame.setLayout(self.innerImageViewingPanel)

        self.editControlLayout.addLayout(self.editSpectrumLayout, 55)
        self.editSpectrumLayout.addWidget(self.editSpectrumScrollArea)
        self.editSpectrumScrollArea.setWidget(self.editSpectrumFrame)
        self.editSpectrumFrame.setLayout(self.innerEditSpectrumLayout)

        self.editControlLayout.addLayout(self.advancementLayout, 45)
        self.advancementLayout.addWidget(self.advancementframe)
        self.advancementframe.setLayout(self.innerAdvancementLayout)
        return
    
    def addWidgetAttributes(self):
        self.innerEditOptionPanel.addWidget(self.editingTreeBody)
        self.innerImageViewingPanel.addWidget(self.imageForEditLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.editSpectrumLayout.addWidget(self.setEdit, alignment = Qt.AlignmentFlag.AlignTop)
        self.innerEditSpectrumLayout.addWidget(self.specialEditOptions, 0, 0, alignment= Qt.AlignmentFlag.AlignCenter)
        self.innerAdvancementLayout.addWidget(self.innerAdvancementScrollArea, alignment = Qt.AlignmentFlag.AlignTop)
        self.innerAdvancementLayout.addWidget(self.chooseColorLabel, alignment = Qt.AlignmentFlag.AlignBottom)
        self.innerAdvancementScrollArea.setLayout(self.sliderHolderLayout)

    def addTreeItems(self, item : QTreeWidgetItem):
        parsedClass = item.text(0)
        editOptions = []
        if parsedClass == "Adjust":
            editOptions = FrameAdjustment.adjustmentSubEditOption
        elif parsedClass == "Filters":
            editOptions = FilterImage.filteringOption
        elif parsedClass == "Color Enhance":
            editOptions = ColorImage.colorEnhanceOptions
        elif parsedClass == "Deform Image":
            editOptions = ImageDeformer.deformOptions
        elif parsedClass == "Frames":
            editOptions = Masks.frameOptions
        elif parsedClass == "Collage":
            pass
        for editOption in editOptions:
            item.addChild(QTreeWidgetItem([editOption]))
        editOptions.clear()
        return
    
    def treeBodyItemclicked(self, treeItem : QTreeWidgetItem):
        self.clearAdvancementLayer()
        self.addTreeItems(item = treeItem)
        self.addSpecialMethodsToGrid(treeItem = treeItem)
        return

    def clearEditSpectrum(self):
        for i in range(self.innerEditSpectrumLayout.count()):
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
        self.innerEditSpectrumLayout.addWidget(QLabel("Editing choice will show up here"), 0, 0, alignment = Qt.AlignmentFlag.AlignCenter)
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
                limit = 1 if len(methodDict.keys())%2 == 0 else 0
                if j > limit:
                    i += 1
                    j = 0
                currentButton = QPushButton(key)
                currentButton.clicked.connect(self.performImageOperation)
                self.innerEditSpectrumLayout.addWidget(currentButton, i, j)
                j += 1
            self.innerEditSpectrumLayout.setVerticalSpacing(1)
            return
    
    def addSpecialMethodsToGrid(self, treeItem : QTreeWidgetItem):
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
    
    def showPixmap(self, imageObject : QPixmap):
        self.imageForEditLabel.hide()
        self.imageForEditLabel.setPixmap(imageObject)
        self.imageForEditLabel.show()
    
    def openImageInEditSection(self):
        if self.imageToEdit != "":
            self.imageSize = self.ORIGINALSIZE
            self.imageObject = QPixmap(self.imageToEdit)
            self.imageForEditLabel.hide()
            self.imageObject = self.imageObject.scaled(self.imageSize[0], self.imageSize[1], aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio)
            self.pixmapConnector.createhead(self.imageObject)
            self.firstCallFlag = True
            self.imageForEditLabel.setPixmap(self.imageObject)
            self.imageForEditLabel.show()
            return "Opened Successfully"
        else:
            return "Error occurred"
    
    def closeImageInEditSection(self):
        if self.imageToEdit != "":
            self.imageObject = None
            self.newImageObject = None
            self.imageForEditLabel.hide()
            self.imageForEditLabel.setText("Edit Your Image here")
            self.imageForEditLabel.show()
            return "Closed Successfully"
    
    def saveImageInMachine(self):
        self.filewinowForSave.saveFileByNmae()
        return
    
    def saveImage(self):
        fileName = self.filewinowForSave.ImageFileNameEditor.text()
        extension = self.filewinowForSave.fileExtensionListWidget.currentText()
        directory = self.filewinowForSave.currentPathName
        if directory:
            fullPath = os.path.join(directory, (fileName+extension))
            if self.imageObject:
                img = self.convertPixMaptoImage(self.imageObject)
                img = img.convert('RGB')
                img.save(fullPath)
                self.filewinowForSave.close()
        return
    def convertPixMaptoImage(self, imageObjectEditable : QPixmap) -> Image.Image:
        if self.imageObject:
            qImage = imageObjectEditable.toImage()
            qImage = qImage.convertToFormat(QImage.Format.Format_RGBA8888)
            width, height = qImage.width(), qImage.height()
            imageData = qImage.constBits().asstring(width * height * 4)
            return Image.frombytes("RGBA", (width, height), imageData, "raw", "RGBA", 0, 1)
        return
    
    def convertImagetoPixMap(self, pilImage : Image.Image) -> str:
        try:
            data = pilImage.convert("RGBA").tobytes("raw", "RGBA")
            width, height = pilImage.size
            qImage = QImage(data, width, height, QImage.Format.Format_RGBA8888)
            self.newImageObject = QPixmap.fromImage(qImage)
        except MemoryError:
            return "Huge size of image"
        return self.newImageObject
    
    def overLayPixmapObjects(self, basePixmap : QPixmap, overLayPixmap : QPixmap) -> QPixmap:
        resultPixmap = QPixmap(basePixmap.size())
        backGround = QPainter(resultPixmap)
        backGround.drawPixmap(0, 0, basePixmap)
        backGround.drawPixmap(0, 0, overLayPixmap)
        return resultPixmap
    
    def performImageOperation(self, signalValue : object = None):
        if self.editingTreeBody.currentItem() != None and self.imageObject != None:
            currentButton1 : QPushButton = self.innerEditSpectrumLayout.sender() # operaional button
            self.operationManager.imageObject = self.convertPixMaptoImage(self.imageObject) # passing ImageObject

            # handles if edit occur while itering
            if self.linker != None:
                self.linker.previousNode = None

            sender = self.sender()
            if isinstance(sender, QPushButton):
                # invoking operation manager to perform editng
                if len(self.valuePackage.keys()) > 0:
                    pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem(), self.valuePackage, self.valuePackage[currentButton1.text()])

            elif signalValue == None:
                    pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem(), self.valuePackage, None)

            elif isinstance(sender, QSlider):
                print(QSlider(sender).sliderPosition())
                self.operationManager.treeChildItem = self.editingTreeBody.currentItem()
                subOperation = self.editingTreeBody.currentItem().text(0)
                signalValue = self.modifySignalValueForMultipleSignal(key = sender.objectName(), signal =signalValue)
                pilImageEdited = self.operationManager.multivalueOperation(subOperation, signalValue)
            
            # Initial edit for slider value operations
            elif isinstance(sender, QTreeWidget):
                self.operationManager.treeChildItem = self.editingTreeBody.currentItem()
                subOperation = self.editingTreeBody.currentItem().text(0)
                pilImageEdited = self.operationManager.multivalueOperation(subOperation, None)

            # conversion and showing image
            self.newImageObject = self.convertImagetoPixMap(pilImage = pilImageEdited)

            if self.editingTreeBody.currentItem().parent().text(0) == "Frames":
                self.newImageObject = self.overLayPixmapObjects(self.imageObject, self.newImageObject)
            elif (self.editingTreeBody.currentItem().text(0) in self.savingRequired):
                self.imageObject = self.newImageObject
            self.showPixmap(self.newImageObject)
        return "Succeed"
    
    def undoOperation(self):
        if self.linker == None:
            # copies the real pixmap connectors head with the linker
            if self.pixmapConnector.head != None and self.firstCallFlag:
                self.linker = self.pixmapConnector.head
                self.linker = self.linker.nextNode
                self.imageObject = self.linker.image
                self.showPixmap(self.linker.image)
                self.firstCallFlag = False
        else:
            if self.linker.nextNode:
                self.linker = self.linker.nextNode
                self.imageObject = self.linker.image
                self.showPixmap(self.linker.image)
        return

    def redoOperation(self):
        if self.linker.previousNode:
            self.linker : Node = self.linker.previousNode
            self.imageObject = self.linker.image
            self.showPixmap(self.linker.image)
        return
    
    def keepEdit(self):
        if self.newImageObject != None:
            self.imageObject = self.newImageObject
            if self.linker:
                self.linker = self.pixmapConnector.addPixmap(self.linker, self.imageObject)
            else:
                self.pixmapConnector.head = self.pixmapConnector.addPixmap(self.pixmapConnector.head, self.imageObject)
    pass