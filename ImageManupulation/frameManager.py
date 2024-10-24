# #important Libraries
from PIL import Image , ImageOps

class FrameGenerator:
    #constructor
    boderOptions = ["Add border"] # Editing options available
    
    def __init__(self) -> None:
        self.image : Image.Image
        self._metaData = {
                "mode" : 'RGB',
                "border" : 10,
                "color" : (255,255,255)
            } # store the initial changes made in image to replicate later
        return
    
    #total colors available for user
    def _colorList(self, index : int) -> tuple:
        colors = [
            (255,0,0), # red
            (0, 255, 0), # green
            (0, 0, 255), # blue
            (0, 255, 255), # cyan
            (255, 0, 255), # magenta
            (255, 255, 0), # yellow
            (255, 165, 0), # orange
            (128, 0, 128), # purble
            (255, 192, 203), # pink
            (165, 42, 42), # brown 
            (128, 128, 0), # olive
            (0, 0, 128), # navy blue
            (0, 128, 128), # teal
            (230, 230, 250), # lavender
            (255, 215, 0), # gold
            (192, 192, 192) # silver
        ]
        return colors[index]
    
    # accepting image instance/
    def getImageObject(self, image:Image.Image)->None:
        self.image = image
        return
    
    # creates a border arround the image
    def addBorder(self, borderWidth : int = 10):
        # copying image instance
        image = self.image
        # process
        try:
            image = ImageOps.expand(image.convert(self._metaData["mode"]), border = borderWidth, fill=self._metaData["color"])            
        except ValueError as valueError:
            return f"Invalid value -> {valueError}"
        except MemoryError as memoryError:
            return f"Insufficient Memory -> {memoryError}"
        except TypeError as typeError:
            return f"Incompitant Type of image -> {typeError}"
        except KeyError as keyError:
            return f"Invalid Key -> {keyError}"
        self.image = image
        return self.image
    
    # changes the border color
    def changeColor(self, userColorIndex : int) -> str:
        # changing meta data
        self._metaData["color"] = self._colorList(userColorIndex)
        #process
        return self.addBorder()
    pass