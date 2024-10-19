# important Libraries
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,QFrame, QAction, QShortcut, QTreeWidget, QTreeWidgetItem, QScrollArea, QLabel, QColorDialog
from PyQt5.QtCore import Qt
from threading import Thread
from PIL import Image
import sys, os

# adding current path to the system
sys.path.append(os.getcwd())

from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.deformer import ImageDeformer
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.imageFiltering import FilterImage
from ImageManupulation.maskGenerator import Masks
from imageOperationController import OperationFramework

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
        self.editingTreeBody.itemClicked.connect(self.addTreeItems)
        self.chooseColorLabel.clicked.connect(self.createColorPicker)
        self.editingTreeBody.itemClicked.connect(self.addSpecialMethodsToGrid)
        self.setEdit.clicked.connect(self.keepEdit)
        return
    
    def addProperties(self):
        self.currentColor = ""
        self.imageToEdit = ""
        self.imageSize = (850, 600)
        self.originalSize = (850, 600)
        self.valuePackage = {}
        self.imageObject : QPixmap = None
        self.newImageObject : QPixmap = None
        self.operationManager = OperationFramework()
        self.savingRequired = ["Rotate"]
        return
    
    def createLabels(self):
        self.imageForEditLabel = QLabel("Edit Your Image here")
        self.specialEditOptions = QLabel("Editing choice will show up here")
        return
    
    def createButtons(self):
        self.chooseColorLabel = QPushButton("Choose color")
        self.setEdit = QPushButton("Set")
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
        return
    
    def createListWidgets(self):
        return
    
    def creteScrollAreas(self):
        self.ScrollEditingBody = QScrollArea()
        self.ScrollEditingBody.setWidgetResizable(True)

        self.editableImageField = QScrollArea()
        self.editableImageField.setWidgetResizable(True)
        self.editableImageField.setFixedSize(850,600)

        self.editSpectrumScrollArea = QScrollArea()
        self.editSpectrumScrollArea.setWidgetResizable(True)
        self.editSpectrumScrollArea.setFixedSize(230,360)
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
        self.editSectionMasterLayout.addLayout(self.editingZoneLayout, 80)
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
        self.innerAdvancementLayout.addWidget(self.chooseColorLabel, alignment = Qt.AlignmentFlag.AlignBottom)
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
        else:
            pass
        for editOption in editOptions:
            item.addChild(QTreeWidgetItem([editOption]))
        editOptions.clear()
        return
    
    def clearEditSpectrum(self):
        for i in range(self.innerEditSpectrumLayout.count()):
            currentItem = self.innerEditSpectrumLayout.takeAt(0)
            internalWidget = currentItem.widget()
            if internalWidget:
                internalWidget.deleteLater()
            self.innerEditSpectrumLayout.update()
        return
    
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
                if treeItem.parent().text(0) == "Adjust":
                    self.valuePackage = FrameAdjustment.subEditingTree[treeItem.text(0)]
                elif treeItem.parent().text(0) == "Filters":
                    pass
                elif treeItem.parent().text(0) == "Color Enhance":
                    pass
                elif treeItem.parent().text(0) == "Deform Image":
                    pass
                elif treeItem.parent().text(0) == "Frames":
                    pass
                else:
                    pass
                self.fillEditSpectrum(self.valuePackage)
                return "Processes are loaded"
            except KeyError:
                return "Unavailable method access denied"
    
    def createColorPicker(self):
        self.currentColor = QColorDialog.getColor()
        return
    
    def showPixmap(self, imageObject : QPixmap):
        self.imageForEditLabel.hide()
        self.imageForEditLabel.setPixmap(imageObject)
        self.imageForEditLabel.show()
    
    def openImageInEditSection(self):
        if self.imageToEdit != "":
            self.imageSize = self.originalSize
            self.imageObject = QPixmap(self.imageToEdit)
            self.imageForEditLabel.hide()
            self.imageObject = self.imageObject.scaled(self.imageSize[0], self.imageSize[1], aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio)
            self.imageForEditLabel.setPixmap(self.imageObject)
            self.imageForEditLabel.show()
            return "Opened Successfully"
        else:
            return "Error occurred"
    
    def closeImageInEditSection(self):
        if self.imageToEdit != "":
            self.imageForEditLabel.hide()
            self.imageForEditLabel.setText("Edit Your Image here")
            self.imageForEditLabel.show()
            return "Closed Successfully"
    
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
    
    def performImageOperation(self):
        if self.editingTreeBody.currentItem() != None and self.imageObject != None:
            currentButton1 : QPushButton = self.innerEditSpectrumLayout.sender() # operaional button
            self.operationManager.imageObject = self.convertPixMaptoImage(self.imageObject) # passing ImageObject

            # invoking operation manager to perform editng
            if len(self.valuePackage.keys()) > 0:
                pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem(), self.valuePackage, self.valuePackage[currentButton1.text()])
            else:
                pilImageEdited = self.operationManager.signalManager(self.editingTreeBody.currentItem(), self.valuePackage, None)
            # conversion and showing image
            self.newImageObject = self.convertImagetoPixMap(pilImage = pilImageEdited)
            if (self.editingTreeBody.currentItem().text(0) in self.savingRequired)or(len(self.valuePackage.keys()) == 0):
                self.imageObject = self.newImageObject
            self.showPixmap(self.newImageObject)
        return "Operation Successful"

    def keepEdit(self):
        self.imageObject = self.newImageObject
    pass