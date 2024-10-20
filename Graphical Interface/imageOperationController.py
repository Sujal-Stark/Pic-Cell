import sys, os
sys.path.append(os.getcwd())
from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.imageFiltering import FilterImage
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.deformer import ImageDeformer
from PIL import Image

from PyQt5.QtWidgets import QTreeWidgetItem

class OperationFramework:
    def __init__(self) -> None:
        self.treeChildItem : QTreeWidgetItem
        self.imageObject : Image.Image
        self.fileAdjustment = FrameAdjustment()
        self.imageFiltering = FilterImage()
        self.imageColoring = ColorImage()
        self.imageDeforming = ImageDeformer()
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
            elif parentItem.text(0) == "Filters":
                self.imageFiltering.getImageObject(self.imageObject)
                if subOperation == "Edge Enhance":
                    return self.imageFiltering.ImageEdgeEnhance(editChoice = signalValue)
            elif parentItem.text(0) == "Color Enhance":
                self.imageColoring.getImageObject(self.imageObject)
                if subOperation == "Change Color":
                    return self.imageColoring.changeColor(colorChoice = signalValue)
                elif subOperation == "Add color layer":
                    return self.imageColoring.addColorLayer(choice = signalValue)
        return self.imageObject
    
    def singleOperations(self, parentItem : QTreeWidgetItem, subOperation : str) -> Image.Image:
        if parentItem:
            if parentItem.text(0) == "Adjust":
                self.fileAdjustment.getImageObject(self.imageObject)
                if subOperation == "Horizontal Flip":
                    return self.fileAdjustment.flip_horizontal()
                elif subOperation == "Vertical Flip":
                    return self.fileAdjustment.flip_vertical()
            elif parentItem.text(0) == "Filters":
                self.imageFiltering.getImageObject(self.imageObject)
                if subOperation == "Grey Scale":
                    return self.imageFiltering.grayScaleimage()
                elif subOperation == "Posterize":
                    print("hey i am here")
                    return self.imageFiltering.postarizeimage()
                elif subOperation == "Contour":
                    return self.imageFiltering.contourImage()
                elif subOperation == "Emboss":
                    return self.imageFiltering.addEmboss()
            elif parentItem.text(0) == "Deform Image":
                self.imageDeforming.getImageObject(self.imageObject)
                if subOperation == "Twist":
                    return self.imageDeforming.middleTwist()
                elif subOperation == "Double Twist":
                    return self.imageDeforming.doubleTwisted()
                elif subOperation == "Half Mirror":
                    return self.imageDeforming.mirrorHalf()
                elif subOperation == "Four Mirror":
                    return self.imageDeforming.mirrorQuad()
        return self.imageObject
    
    def multivalueOperation(self, subOperation : str, signalValue:object):
        parentItem = self.treeChildItem.parent()
        if parentItem:
            if parentItem.text(0) == "Filters":
                self.imageFiltering.getImageObject(self.imageObject)
                if subOperation == "Auto contrast":
                    return self.imageFiltering.imageAutoContrast(cutoffValue = signalValue)
                elif subOperation == "Gaussian Blur":
                    return self.imageFiltering.gaussianBlurImage(blurStrength = signalValue)
                elif subOperation == "Sharpen":
                    return self.imageFiltering.sharpenImage(sharpValue = signalValue)
                elif subOperation == "Detail":
                    return self.imageFiltering.addDetail(strenghtChoice = signalValue)
                elif subOperation == "Smoothen":
                    return self.imageFiltering.smoothenImage(smoothingChoice = signalValue)
                elif subOperation == "Box Blur":
                    return self.imageFiltering.boxBlurImage(blurStrength = signalValue)
                elif subOperation == "Unsharp":
                    keyList = list(signalValue.keys())
                    if "radius" == keyList[0]:
                        return self.imageFiltering.imageUnsharpMask(radius_choice = signalValue["radius"])
                    elif "Threshold" == keyList[0]:
                        return self.imageFiltering.imageUnsharpMask(threshold_choice = signalValue["Threshold"])
            if parentItem.text(0) == "Deform Image":
                self.imageDeforming.getImageObject(self.imageObject)
                if subOperation == "Horizontal Split":
                    return self.imageDeforming.horizontalSplit(repeaterValue = signalValue)
                elif subOperation == "Vertical Split":
                    return self.imageDeforming.verticalSplit(repeaterValue = signalValue)
                elif subOperation == "Multiply":
                    return self.imageDeforming.multiply(repitaionNumber = signalValue)
                elif subOperation == "Add Layer":
                    return self.imageDeforming.layerize(repeaterValue = signalValue)
                elif subOperation == "Chess Like":
                    return self.imageDeforming.chess(boxGap = signalValue)
                elif subOperation == "Sine Curve":
                    print(signalValue)
                    return self.imageDeforming.sinCurve(cycle = signalValue)
        return self.imageObject
