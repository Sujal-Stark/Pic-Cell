import sys, os
sys.path.append(os.getcwd())
from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.imageFiltering import FilterImage
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.deformer import ImageDeformer
from ImageManupulation.frameManager import FrameGenerator
from ImageManupulation.specialFrameGenerator import SpecialFrames
from ImageManupulation.maskGenerator import Masks
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
        self.imageFrames = Masks()
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
            elif parentItem.text(0) == "Frames":
                self.imageFrames.getImageObject(self.imageObject)
                if subOperation == "Rombous":
                    return self.imageFrames.rombousMask()
                elif subOperation == "Double Circle":
                    return self.imageFrames.doubleCircleMask()
                elif subOperation == "Star":
                    return self.imageFrames.starShape()
                elif subOperation == "Dead pool":
                    return self.imageFrames.style_three_mask()
                elif subOperation == "Five Section Rectangle":
                    return self.imageFrames.style_two_mask()
                elif subOperation == "Step Size":
                    return self.imageFrames.style_eight_mask()
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
                    return self.imageDeforming.sinCurve(cycle = signalValue)
            if parentItem.text(0) == "Frames":
                self.imageFrames.getImageObject(self.imageObject)
                if subOperation == "Rectangle Layer":
                    return self.imageFrames.layeredRectangle(modifier = signalValue)
                elif subOperation == "Ellipse":
                    return self.imageFrames.ellipticalMask(modifier = signalValue)
                elif subOperation == "Circle":
                    return self.imageFrames.circularMask(modifier = signalValue)
                elif subOperation == "Left Diagonal":
                    return self.imageFrames.style_one_mask(modifier = signalValue)
                elif subOperation == "Right Diagonal":
                    return self.imageFrames.style_five_mask(modifier = signalValue)
                elif subOperation == "Left Frame":
                    return self.imageFrames.style_six_mask(modifier = signalValue)
                elif subOperation == "Right Frame":
                    return self.imageFrames.style_seven_mask(modifier = signalValue)
        return self.imageObject
