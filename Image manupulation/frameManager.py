# #important Libraries
from PIL import Image , ImageOps

class FrameGenerator:
    #constructor
    def __init__(self, fileName : str) -> None:
        self.image = Image.open(fileName)#creating an image Instance
        self.imageConst = self.image # a copy of the original image to do different color change
        self.user_message = None #user will get info about the process
        self._metaData = {
                "mode" : 'RGB',
                "border" : 10,
                "color" : (255,255,255)
            } # store the initial changes made in image to replicate later
        return
    
    #get message method to let user know system message
    def get_Message(self):
        return self.user_message
    
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
    
    # shows the available color choice
    def _showColor(self) ->str:
        return "1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow, 7 -> Orange, 8 -> Purple, 9 -> Pink, 10 -> Brown, 11 -> Olive, 12 -> Navy Blue, 13 -> Teal, 14 -> Lavender, 15 -> Gold, 16 -> Silver"
    
    # accepting image instance/
    def getImageObject(self, image:Image.Image)->None:
        self.image = image
        return
    
    # provide edited image
    def provideImageObject(self)-> Image.Image:
        return self.image
    
    # creates a border arround the image
    def addBorder(self) -> str:
        # copying image instance
        image = self.image
        # creating user message
        self.user_message = "Adding an white 10 by 10 border on the image"
        self.get_Message()
        # process
        try:
            image = ImageOps.expand(image.convert(self._metaData["mode"]), border = self._metaData["border"], fill=self._metaData["color"])            
        except ValueError as valueError:
            return f"Invalid value -> {valueError}"
        except MemoryError as memoryError:
            return f"Insufficient Memory -> {memoryError}"
        except TypeError as typeError:
            return f"Incompitant Type of image -> {typeError}"
        except KeyError as keyError:
            return f"Invalid Key -> {keyError}"
        finally:
            self.image = image
            return "Operation successful"
        
    # change border width
    def  changeWidth(self, userdefinedWidth:int) -> str:
        # copying image instance
        image = self.imageConst
        # creating user message
        self.user_message = "Enter Pixel value to change border width"
        self.get_Message()
        #changing meta data
        self._metaData["border"] = userdefinedWidth
        #process
        return self.addBorder()
    
    # changes the border color
    def changeColor(self, userColorIndex : int) -> str:
        # copying image instance
        self.image = self.imageConst
        # creating user message
        self.user_message = self._showColor()
        self.get_Message()
        # changing meta data
        self._metaData["color"] = self._colorList(userColorIndex)
        #process
        return self.addBorder()
    pass
# print(dir(ImageOps))
# print(ImageOps.expand.__doc__)