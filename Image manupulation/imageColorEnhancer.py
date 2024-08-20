#important libraries
from PIL import Image, ImageOps, ImageColor

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
    def _colorList(self, index : int) -> int:
        colors = [(255,0,0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0)]
        return colors[index]

    # changes the color
    def changeColor(self,modeChoice : int,colorChoice : int) -> str:
        # creating user message
        self.user_message = "Modes:\n-1 -> Background, -2 -> Foreground\nChoice:\n0->None, 1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow"
        self.getMessage()
        #copying current image
        image = self.image
        try: # operaion
            if modeChoice == -1:
                image = ImageOps.colorize(image.convert('L'),black=self._colorList(colorChoice), white='White')
            elif modeChoice == -2:
                image = ImageOps.colorize(image.convert('L'),black= 'black', white= self._colorList(colorChoice))
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
    
    pass