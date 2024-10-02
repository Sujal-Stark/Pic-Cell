# important Libraries
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QFrame, QAction, QShortcut, QTreeWidget, QTreeWidgetItem, QScrollArea
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
    def addProperties(self):
        return
    
    def createButtons(self):
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
        self.imageViewingPanel.addWidget(self.imageViewingFrame)
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
    pass

