# important Libraries
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QFrame, QAction, QShortcut, QTreeWidget, QTreeWidgetItem, QScrollArea, QLabel, QColorDialog
from PyQt5.QtCore import Qt
from threading import Thread
import sys, os
# adding current path to the system
sys.path.append(os.getcwd())

from  ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.deformer import ImageDeformer
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.imageFiltering import FilterImage
# from ImageManupulation.specialFrameGenerator import SpecialFrames
from ImageManupulation.maskGenerator import Masks

class EditingActionManager(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.editSectionMasterLayout = QHBoxLayout(self)
        self.loadUi()
        self.addResponse()
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
        return
    
    def addProperties(self):
        self.currentColor = ""
        self.imageToEdit = ""
        self.imageSize = (850, 600)
        self.originalSize = (850, 600)
        return
    
    def createLabels(self):
        self.imageForEditLabel = QLabel("Edit Your Image here")
        self.specialEditOptions = QLabel("Special editing choice will show up here")
        return
    
    def createButtons(self):
        self.chooseColorLabel = QPushButton("Choose color")
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
        self.innerEditSpectrumLayout = QVBoxLayout()
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
        return
    
    def editingTree(self):
        self.editingTreeBody = QTreeWidget()
        self.editingTreeBody.setColumnCount(1)
        self.editingTreeBody.setHeaderLabel("Editing Body")
        # editSections = self.addTreeItems()
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

        self.editControlLayout.addLayout(self.editSpectrumLayout, 60)
        self.editSpectrumLayout.addWidget(self.editSpectrumFrame)
        self.editSpectrumFrame.setLayout(self.innerEditSpectrumLayout)

        self.editControlLayout.addLayout(self.advancementLayout, 40)
        self.advancementLayout.addWidget(self.advancementframe)
        self.advancementframe.setLayout(self.innerAdvancementLayout)
        return
    
    def addWidgetAttributes(self):
        self.innerEditOptionPanel.addWidget(self.editingTreeBody)
        self.innerImageViewingPanel.addWidget(self.imageForEditLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerEditSpectrumLayout.addWidget(self.specialEditOptions, alignment = Qt.AlignmentFlag.AlignCenter)
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
    
    def createColorPicker(self):
        self.currentColor = QColorDialog.getColor()
        return
    
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
    pass

