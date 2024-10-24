# important libraries
from PIL import Image, ImageChops

# important custom modules
import sys, os

sys.path.append(os.getcwd())
from ImageManupulation.maskGenerator import Masks
from ImageManupulation.frameManager import FrameGenerator

# class
class SpecialFrames:
    frameOptions = ["Rectangle Layer", "Rombous", "Ellipse", "Circle", "Double Circle", "Left Diagonal", "Right Diagonal", "Five Section Rectangle", "Embrald", "Dead pool", "Star", "Left Frame", "Right Frame", "Step Size"] # editing options available
    subEditingTree = {
        "Rectangle Layer" : {
            "Border" : {"minVal" : 10, "maxVal" : 200, "currentPosition" : 10, "change" : 10}
        },
        "Rombous" : {
            "Border" : {"minVal" : 10, "maxVal" : 200, "currentPosition" : 10, "change" : 10}
        }
    }

    # constructor
    def __init__(self) -> None:
        self._metaData = {
            "mode" : 'RGBA'
        } # stores the meta data
        return

    
    # getting image object 
    def getImageObject(self, image : Image.Image) -> None:
        self.image = image
        return
    
    # # layered rectangle mask
    def addFrame(self, maskChoice : int) -> str:
        #copying image object
        image = self.image
        #operation
        try:
            self.user_request = maskChoice # recording user choice
            image = image.convert(self._metaData["mode"])
            width,height = image.size
            if maskChoice == 0:
                image = FrameGenerator.addBorder()
            elif maskChoice == 1:
                image = ImageChops.add(image, Masks.layeredRectangle(Masks(width,height)))
            elif maskChoice == 2:
                image = ImageChops.add(image, Masks.rombousMask(Masks(width,height)))
            elif maskChoice == 3:
                image = ImageChops.add(image, Masks.ellipticalMask(Masks(width,height)))
            elif maskChoice == 4:
                image = ImageChops.add(image, Masks.circularMask(Masks(width,height)))
            elif maskChoice == 5:
                image = ImageChops.add(image, Masks.doubleCircleMask(Masks(width,height)))
            elif maskChoice == 6:
                image = ImageChops.add(image, Masks.style_one_mask(Masks(width,height)))
            elif maskChoice == 7:
                image = ImageChops.add(image, Masks.style_two_mask(Masks(width,height)))
            elif maskChoice == 8:
                image = ImageChops.add(ImageChops.add(image, Masks.rombousMask(Masks(width,height))), Masks.circularMask (Masks(width,height)))
            elif maskChoice == 9:
                image = ImageChops.add(image, Masks.style_three_mask(Masks(width,height)))
            elif maskChoice == 10:
                image = ImageChops.add(image, Masks.starShape(Masks(width,height)))
            else:
                image = self.image # redeemed actual image
        except MemoryError as memoryError:
            return f"Insufficient memory -> {memoryError}"
        except TypeError as typeError:
            return f"Incompatible type -> {typeError}"
        self.image = image
        return self.image