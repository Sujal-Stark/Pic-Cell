import sys, os
sys.path.append(os.getcwd())
from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.imageFiltering import FilterImage
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.deformer import ImageDeformer
from ImageManupulation.maskGenerator import Masks
# from cropFrameWidget import CropWidget

from PIL import Image
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
# from PyQt5.QtCore import QPoint, Qt
# from PyQt5.QtGui import QMouseEvent

class OperationFramework(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.treeChildItem : QTreeWidgetItem
        self.imageObject : Image.Image
        self.fileAdjustment = FrameAdjustment()
        self.imageFiltering = FilterImage()
        self.imageColoring = ColorImage()
        self.imageDeforming = ImageDeformer()
        self.imageFrames = Masks()
        # self.editRubberWidget  : CropWidget
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
                    # w,h = self.fileAdjustment.imageCrop(choice = signalValue)
                    # self.editRubberWidget.setFixedSize(w,h)
                    # self.editRubberWidget
                    # self.editRubberWidget.show()
                    # return self.imageObject
                    pass
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
                    if signalValue != None:
                        return self.imageFiltering.imageAutoContrast(cutoffValue = signalValue)
                    else:
                        return self.imageFiltering.imageAutoContrast()
                elif subOperation == "Gaussian Blur":
                    if signalValue != None:
                        return self.imageFiltering.gaussianBlurImage(blurStrength = signalValue)
                    else:
                        return self.imageFiltering.gaussianBlurImage()
                elif subOperation == "Sharpen":
                    if signalValue != None:
                        return self.imageFiltering.sharpenImage(sharpValue = signalValue)
                    else:
                        return self.imageFiltering.sharpenImage()
                elif subOperation == "Detail":
                    if signalValue != None:
                        return self.imageFiltering.addDetail(strenghtChoice = signalValue)
                    else:
                        return self.imageFiltering.addDetail()
                elif subOperation == "Smoothen":
                    if signalValue != None:
                        return self.imageFiltering.smoothenImage(smoothingChoice = signalValue)
                    else:
                        return self.imageFiltering.smoothenImage()
                elif subOperation == "Box Blur":
                    if signalValue != None:
                        return self.imageFiltering.boxBlurImage(blurStrength = signalValue)
                    else:
                        return self.imageFiltering.boxBlurImage()
                elif subOperation == "Unsharp":
                    keyList = list(signalValue.keys())
                    if signalValue != None:
                        if "radius" == keyList[0]:
                            return self.imageFiltering.imageUnsharpMask(radius_choice=signalValue["radius"])
                        elif "Threshold" == keyList[0]:
                            return self.imageFiltering.imageUnsharpMask(threshold_choice= signalValue["Threshold"])
                    else:
                        return self.imageFiltering.imageUnsharpMask()
            if parentItem.text(0) == "Deform Image":
                self.imageDeforming.getImageObject(self.imageObject)
                if subOperation == "Horizontal Split":
                    if signalValue != None:
                        return self.imageDeforming.horizontalSplit(repeaterValue = signalValue)
                    else:
                        return self.imageDeforming.horizontalSplit()
                elif subOperation == "Vertical Split":
                    if signalValue != None:
                        return self.imageDeforming.verticalSplit(repeaterValue = signalValue)
                    else:
                        return self.imageDeforming.verticalSplit()
                elif subOperation == "Multiply":
                    if signalValue != None:
                        return self.imageDeforming.multiply(repitaionNumber = signalValue)
                    else:
                        return self.imageDeforming.multiply()
                elif subOperation == "Add Layer":
                    if signalValue != None:
                        return self.imageDeforming.layerize(repeaterValue = signalValue)
                    else:
                        return self.imageDeforming.layerize()
                elif subOperation == "Chess Like":
                    if signalValue != None:
                        return self.imageDeforming.chess(boxGap = signalValue)
                    else:
                        return self.imageDeforming.chess()
                elif subOperation == "Sine Curve":
                    if signalValue != None:
                        return self.imageDeforming.sinCurve(cycle = signalValue)
                    else:
                        return self.imageDeforming.sinCurve()
            if parentItem.text(0) == "Frames":
                self.imageFrames.getImageObject(self.imageObject)
                if subOperation == "Rectangle Layer":
                    if signalValue != None:
                        return self.imageFrames.layeredRectangle(modifier = signalValue)
                    else:
                        return self.imageFrames.layeredRectangle()
                elif subOperation == "Ellipse":
                    if signalValue != None:
                        return self.imageFrames.ellipticalMask(modifier = signalValue)
                    else:
                        return self.imageFrames.ellipticalMask()
                elif subOperation == "Circle":
                    if signalValue != None:
                        return self.imageFrames.circularMask(modifier = signalValue)
                    else:
                        return self.imageFrames.circularMask()
                elif subOperation == "Left Diagonal":
                    if signalValue != None:
                        return self.imageFrames.style_one_mask(modifier = signalValue)
                    else:
                        return self.imageFrames.style_one_mask()
                elif subOperation == "Right Diagonal":
                    if signalValue != None:
                        return self.imageFrames.style_five_mask(modifier = signalValue)
                    else:
                        return self.imageFrames.style_five_mask()
                elif subOperation == "Left Frame":
                    if signalValue != None:
                        return self.imageFrames.style_six_mask(modifier = signalValue)
                    else:
                        return self.imageFrames.style_six_mask()
                elif subOperation == "Right Frame":
                    if signalValue != None:
                        return self.imageFrames.style_seven_mask(modifier = signalValue)
                    else:
                        return self.imageFrames.style_seven_mask()
        return self.imageObject