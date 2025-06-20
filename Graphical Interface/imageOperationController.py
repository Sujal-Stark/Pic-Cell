import sys, os
sys.path.append(os.getcwd())
from ImageManupulation.ImageframeAdjuster import FrameAdjustment
from ImageManupulation.imageFiltering import FilterImage
from ImageManupulation.imageColorEnhancer import ColorImage
from ImageManupulation.deformer import ImageDeformer
from ImageManupulation.maskGenerator import Masks
from textEditor import TextEditorAssembly
from icecream import ic

from PIL import Image
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QColor

class OperationFramework(QWidget):
    ORIGINALIMAGE : Image.Image = None # real image value to get set
    def __init__(self) -> None:
        super().__init__()
        self.treeChildItem : QTreeWidgetItem
        self.imageObject : Image.Image
        self.fileAdjustment = FrameAdjustment()
        self.imageFiltering = FilterImage()
        self.imageColoring = ColorImage()
        self.imageDeforming = ImageDeformer()
        self.imageFrames = Masks()
        self.textEditorAssembly =  TextEditorAssembly()
        return
    
    def signalManager(self, treeChild : QTreeWidgetItem, signalValue : object = None, multivalueOperaion : bool = False):
        self.treeChildItem = treeChild
        parentItem = self.treeChildItem.parent()
        subOperation = self.treeChildItem.text(0)
        if not multivalueOperaion:
            if signalValue is not None:
                return self.performAction(parentItem, subOperation, signalValue)
            elif signalValue is None:
                return self.singleOperations(parentItem, subOperation)
        elif multivalueOperaion:
            return self.multivalueOperation(parentWidget = parentItem, subOperation=subOperation, signalValue=signalValue)
        return None
    
    def editfromParsedData(self, valueHashList : dict = None):
        '''perform edits only on original image so that the resolution of the image may become intact'''
        image = self.ORIGINALIMAGE # copying the original image to image
        parent = valueHashList["parent"]
        subEdit = valueHashList["child"]
        signal = valueHashList["signalValue"]
        color = valueHashList["color"]
        if valueHashList["multivalue"]==False and color is None: # single value operations and no color access
            if signal != None: # signal value 1
                if isinstance(signal, dict):
                    self.textEditorAssembly.getPILImage(self.imageObject)
                    self.textEditorAssembly.textEditor.setMetaInformation(signal)
                    image = self.textEditorAssembly.textEditor.generateFinalEdit()
                    # image.show()
                else:
                    image = self.performAction(parentItem = parent, subOperation = subEdit, signalValue = signal)
            elif signal == None: # signal value 0
                if(parent.text(0) == "Frames"): # if frames are used then use overlay
                    overlayImage = self.singleOperations(parentItem = parent, subOperation = subEdit)
                    image = Image.alpha_composite(image.convert("RGBA"), overlayImage.resize(image.size).convert("RGBA"))
                else: # other non value operations
                    image = self.singleOperations(parentItem = parent, subOperation = subEdit)
        elif valueHashList["multivalue"]  and color is None: # multivalue operations and no color access
            if(parent.text(0) == "Frames"): # if frames are used then use loverlay
                overlay = self.multivalueOperation(parentWidget = parent, subOperation = subEdit, signalValue = signal)
                image = Image.alpha_composite(image.convert("RGBA"), overlay.resize(image.size).convert("RGBA"))
            else: # other multivalue operations
                image = self.multivalueOperation(parentWidget = parent, subOperation = subEdit, signalValue = signal)
        elif isinstance(color, QColor): # QColor objects are used
            if(parent.text(0)=="Frames"): # if frames are used then use overlay
                colorOverlay = self.provideColor(parent.text(0), subEdit, color)
                image = Image.alpha_composite(image.convert("RGBA"), colorOverlay.resize(image.size).convert("RGBA"))
            else: # other operations
                image = self.provideColor(parentMethod = parent.text(0), methodName = subEdit, givenColor = color)
        if(image):
            self.ORIGINALIMAGE = image
        return self.ORIGINALIMAGE
    
    def performAction(self, parentItem : QTreeWidgetItem, subOperation : str, signalValue:object) -> Image.Image:
        if parentItem:
            if parentItem.text(0) == "Adjust":
                self.fileAdjustment.getImageObject(self.imageObject)
                if subOperation == "Resize":
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
    
    def multivalueOperation(self, parentWidget : QTreeWidgetItem, subOperation : str, signalValue:object):
        if parentWidget:
            if parentWidget.text(0) == "Adjust":
                self.fileAdjustment.getImageObject(self.imageObject)
                if subOperation == "Rotate":
                    return self.fileAdjustment.imageRotate(rotationAngle=signalValue)
            elif parentWidget.text(0) == "Filters":
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
                    if signalValue != None:
                        keyList = list(signalValue.keys())
                        if "radius" == keyList[0]:
                            return self.imageFiltering.imageUnsharpMask(radius_choice=signalValue[keyList[0]])
                        elif "Threshold" == keyList[0]:
                            return self.imageFiltering.imageUnsharpMask(threshold_choice= signalValue[keyList[0]])
                    else:
                        return self.imageFiltering.imageUnsharpMask()
            if parentWidget.text(0) == "Deform Image":
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
                        keyList = list(signalValue.keys())
                        if keyList[0] == "Layer number":
                            return self.imageDeforming.layerize(repeaterValue = signalValue[keyList[0]])
                        elif keyList[0] == "Padding":
                            return self.imageDeforming.layerize(padding = signalValue[keyList[0]])
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
            if parentWidget.text(0) == "Frames":
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
    
    def provideColor(self, parentMethod: str, methodName : str, givenColor : QColor):
        if parentMethod == "Color Enhance":
            ic(givenColor)
            self.imageColoring.getImageObject(self.imageObject)
            keyMethods = list(self.imageColoring.subEditingTree.keys())
            if methodName == keyMethods[0]:
                self.imageColoring.custom_color = givenColor.getRgb()
                return self.imageColoring.changeColor()
            elif methodName == keyMethods[1]:
                self.imageColoring.custom_color = (givenColor.red(), givenColor.green(), givenColor.blue(), givenColor.alpha())
                return self.imageColoring.addColorLayer()
            return self.imageObject
        
        elif parentMethod == "Frames":
            ic(givenColor)
            customColor = (givenColor.red(), givenColor.green(), givenColor.blue(), givenColor.alpha())
            self.imageFrames.getImageObject(self.imageObject)
            keyMethods = list(self.imageFrames.subEditingTree.keys())
            if methodName == keyMethods[0]:
                return self.imageFrames.layeredRectangle(chosenColor = customColor)
            
            elif methodName == keyMethods[1]:
                return self.imageFrames.rombousMask(chosenColor = customColor)
            
            elif methodName == keyMethods[2]:
                return self.imageFrames.ellipticalMask(chosenColor = customColor)
            
            elif methodName == keyMethods[3]:
                return self.imageFrames.circularMask(chosenColor = customColor)
            
            elif methodName == keyMethods[4]:
                return self.imageFrames.doubleCircleMask(chosenColor = customColor)
            
            elif methodName == keyMethods[5]:
                return self.imageFrames.style_one_mask(chosenColor = customColor)
            
            elif methodName == keyMethods[6]:
                return self.imageFrames.style_five_mask(chosenColor = customColor)
            
            elif methodName == keyMethods[7]:
                return self.imageFrames.style_six_mask(chosenColor = customColor)
            
            elif methodName == keyMethods[8]:
                return self.imageFrames.style_seven_mask(chosenColor = customColor)
            
            elif methodName == keyMethods[9]:
                return self.imageFrames.starShape(chosenColor = customColor)
            
            elif methodName == keyMethods[10]:
                return self.imageFrames.style_three_mask()
            
            elif methodName == keyMethods[11]:
                return self.imageFrames.style_two_mask(chosenColor = customColor)
            
            elif methodName == keyMethods[12]:
                return self.imageFrames.style_eight_mask(chosenColor = customColor)
            return self.imageObject
        return None