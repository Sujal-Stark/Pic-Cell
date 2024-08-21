#important libraries
from PIL import Image, ImageOps, ImageColor, ImageChops, ImageDraw

#colors
class ColorImage:
     #constructor
    def __init__(self,fileName : str) -> None:
        self.image = Image.open(fileName)
        self.copyImage = self.image
        self.user_message = None

        #sends user message
    def getMessage(self)->None:
        print(self.user_message)
        self.user_message=None # sets user message to null for next message
        return

    #interchanges the image with different classes
    def getImageObject(self,image:Image.Image):
        try:
            #the instance variable is set to given image
            self.image = image
        except OSError as osError:
            return f"Cant Open the image -> {osError}"
        except MemoryError as memoryError:
            return f"Can't load the image -> {memoryError}"
        finally:
            return "Succeed"
    
    #transmits an image
    def provideImageObject(self) -> Image.Image:
        return self.image
    
    #takes user choice
    def _makeChoice(self,choiceList:list)->int:
        try:
            user_choice = int(input("Enter choice:\t"))
        except ValueError:
            user_choice = 0
        if  user_choice not in choiceList:
            return 0
        else:
            return user_choice
    
    #total colors available for user
    def _colorList(self, index : int) -> list:
        colors = [[255,0,0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255], [255, 255, 0], [255, 165, 0], [128, 0, 128], [255, 192, 203], [165, 42, 42], [128, 128, 0], [0, 0, 128], [0, 128, 128], [230, 230, 250], [255, 215, 0], [192, 192, 192]]
        return colors[index]
    
    #total RGBA colors available for user
    def _RGBAcolorList(self, index : int) -> list:
        color_list = [
        (255, 0, 0, 0),  # Red
        (0, 255, 0, 128),  # Green
        (0, 0, 255, 128),  # Blue
        (0, 255, 255, 128),  # Cyan
        (255, 0, 255, 128),  # Magenta
        (255, 255, 0, 128),  # Yellow
        (255, 165, 0, 128),  # Orange
        (128, 0, 128, 128),  # Purple
        (255, 192, 203, 128),  # Pink
        (165, 42, 42, 128),  # Brown
        (128, 128, 0, 128),  # Olive
        (0, 0, 128, 128),  # Navy Blue
        (0, 128, 128, 128),  # Teal
        (230, 230, 250, 128),  # Lavender
        (255, 215, 0, 128),  # Gold
        (192, 192, 192, 128)  # Silver
        ]
        return color_list[index]
    
    # changes the color
    def changeColor(self,modeChoice : int,colorChoice : int) -> str:
        # creating user message
        self.user_message = "Modes:\n-1 -> Background, -2 -> Foreground\nChoice:\n0->None, 1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow, 7 -> Orange, 8 -> Purple, 9 -> Pink, 10 -> Brown, 11 -> Olive, 12 -> Navy Blue, 13 -> Teal, 14 -> Lavender, 15 -> Gold, 16 -> Silver"
        self.getMessage()
        #copying current image
        image = self.image
        try: # operaion
            if modeChoice == -1:
                image = ImageOps.colorize(image.convert('L'),black=tuple(self._colorList(colorChoice)), white='White')
            elif modeChoice == -2:
                image = ImageOps.colorize(image.convert('L'),black= 'black', white= tuple(self._colorList(colorChoice)))
            else:
                return "Invalid Input"
            return "Operation Completed"
        except MemoryError as memoryError:
            return f"Memory Error Occurred-> {memoryError}"
        except ValueError as valueError:
            return f"Value is unclear -> {valueError}"
        except IndexError as indexError:
            return f"{indexError}"
        finally:
            self.image = image
    
    # color Filter
    def addColorLayer(self, choice : int) -> str:
        #copying current image
        image = self.image
        #creating user message
        self.user_message = "1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow, 7 -> Orange, 8 -> Purple, 9 -> Pink, 10 -> Brown, 11 -> Olive, 12 -> Navy Blue, 13 -> Teal, 14 -> Lavender, 15 -> Gold, 16 -> Silver"
        self.getMessage()
        #procedure
        try:
            if choice == 0:
                return "Operation Complete"
            else:
                layer = Image.new(mode='RGBA',size=image.size,color=tuple(255-i for i in self._RGBAcolorList (choice)))#color is inverted as it will merge with image
                image = ImageChops.blend(layer,image.convert('RGBA'),alpha=2)
                return "Operation compelte"
        except MemoryError as memoryError:
            return f"Insufficient Memory -> {memoryError}"
        except ValueError as valueError:
            return f"Undefined Value -> {valueError}"
        except IndexError as indexError:
            return f"Invalid Index -> {indexError}"
        except TypeError as typeError:
            return f"Wrong Type -> {typeError}"
        finally:
            self.image = image
    pass