#important libraries
from PIL import Image, ImageOps, ImageColor

#colors
class ColorImage:
     #constructor
    def __init__(self,fileName : str) -> None:
        self.image = Image.open(fileName)
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
    pass
