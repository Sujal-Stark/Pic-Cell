# important libraries
from PIL import Image, ImageChops

# important custom modules
import sys, os

sys.path.append(os.getcwd())
from maskGenerator import Masks

# class
class SpecialFrames:
    frameOptions = ["Rectangle Layer", "Rombous", "Ellipse", "Circle", "Double Circle", "Left Diagonal", "Right Diagonal", "Five Section Rectangle", "Embrald", "Dead pool", "Star", "Left Frame", "Right Frame", "Step Size"] # editing options available
    
    # constructor
    def __init__(self, imageFile : str) -> None:
        self.image = Image.open(imageFile) # opens the real image
        self.imageConst = self.image # copying the actual image for modification
        self.user_message = None # accepts user message from methods
        self.saveStatus = False # the process will go continuously until save status become true
        self.user_request = None # recored the user taken choice 
        self._metaData = {
            "mode" : 'RGBA'
        } # stores the meta data
        return
    
    # sending user message
    def getMessage(self) -> str:
        return self.user_message
    
    # getting image object 
    def getImageObject(self, image : Image.Image) -> None:
        self.image = image
        return
    
    # setting image object
    def provideImageObject(self) -> Image.Image:
        return self.image
    
    # # layered rectangle mask
    def addFrame(self, maskChoice : int) -> str:
        #copying image object
        image = self.image
        #creating user message
        self.user_message = "1 -> Rectangle Layer, 2 -> Rombous, 3 -> Ellipse, 4 -> Circle, 5 -> Double Circle, 6 -> Left Diagonal, 7 -> Five Section Rectangle, 8 -> Embrald"
        self.getMessage()
        #operation
        try:
            self.user_request = maskChoice # recording user choice
            image = image.convert(self._metaData["mode"])
            width,height = image.size
            if maskChoice == 1:
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
        finally:
            self.image = image
            return "operation successful"