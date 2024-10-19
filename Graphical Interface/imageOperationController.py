import sys, os
sys.path.append(os.getcwd())
from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.imageFiltering import FilterImage
from PIL import Image

from PyQt5.QtWidgets import QTreeWidgetItem

class OperationFramework:
    def __init__(self) -> None:
        self.treeChildItem : QTreeWidgetItem
        self.imageObject : Image.Image
        self.fileAdjustment = FrameAdjustment()
        return
    
    def signalManager(self, treeChild : QTreeWidgetItem, valuePackage : dict, signalValue : object):
        self.treeChildItem = treeChild
        parentItem = self.treeChildItem.parent()
        subOperation = self.treeChildItem.text(0)
        print(len(valuePackage.keys()))
        if signalValue != None:
            return self.performAction(parentItem, subOperation, signalValue)
        elif signalValue == None:
            return self.singleOperations(parentItem, subOperation)
        else:
            return
        
    def performAction(self, parentItem : QTreeWidgetItem, subOperation : str, signalValue:object) -> Image.Image:
        if parentItem:
            if parentItem.text(0) == "Adjust":
                self.fileAdjustment.getImageObject(self.imageObject)
                if subOperation == "Crop":
                    return self.fileAdjustment.imageCrop(choice = signalValue)
                elif subOperation == "Resize":
                    return self.fileAdjustment.resizeImage(resize_choice = signalValue)
                elif subOperation == "Resample":
                    return self.fileAdjustment.changeResampleType(resample_choice = signalValue)
                elif subOperation == "Rotate":
                    return self.fileAdjustment.imageRotate(rotationSignal = signalValue)
        return self.imageObject
    
    def singleOperations(self, parentItem : QTreeWidgetItem, subOperation : str) -> Image.Image:
        if parentItem:
            if parentItem.text(0) == "Adjust":
                self.fileAdjustment.getImageObject(self.imageObject)
                if subOperation == "Horizontal Flip":
                    return self.fileAdjustment.flip_horizontal()
                elif subOperation == "Vertical Flip":
                    return self.fileAdjustment.flip_vertical()
        return self.imageObject
