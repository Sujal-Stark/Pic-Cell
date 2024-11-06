#important libraries
from PIL import Image, ImageOps, ImageColor, ImageChops, ImageDraw

#colors
class ColorImage:
    colorEnhanceOptions = ["Change Color", "Add color layer"] # editing options available
    
    subEditingTree = {
        "Change Color" : {
            "Custom" : 0, "Red" : 1, "Green" : 2, "Blue" : 3, "Cyan" : 4, "Magenta" : 5, "Yellow" : 6,
            "Orange" : 7, "Purple" : 8, "Pink" : 9, "Brown" : 10, "Olive" : 11, "Navy Blue" : 12, "Teal" : 13,
            "Lavender" : 14, "Gold" : 15, "Silver" : 16
        },
        "Add color layer" : {
            "Custom" : 0, "Red" : 1, "Green" : 2, "Blue" : 3, "Cyan" : 4, "Magenta" : 5, "Yellow" : 6,
            "Orange" : 7, "Purple" : 8, "Pink" : 9, "Brown" : 10, "Olive" : 11, "Navy Blue" : 12, "Teal" : 13,
            "Lavender" : 14, "Gold" : 15, "Silver" : 16
        }
    }

    # constants
    custom_color = (255,255,255) # custom color which can be used to colorise manually

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
    
    #total colors available for user
    def _colorList(self, index : int) -> tuple:
        colors = [
            (255,0,0), (0, 255, 0), (0, 0, 255), (0, 255, 255), 
            (255, 0, 255), (255, 255, 0),(255, 165, 0), (128, 0, 128),
            (255, 192, 203), (165, 42, 42), (128, 128, 0), (0, 0, 128),
            (0, 128, 128), (230, 230, 250), (255, 215, 0), (192, 192, 192)
        ]
        return colors[index]
    
    #total RGBA colors available for user
    def _RGBAcolorList(self, index : int) -> tuple:
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
    def changeColor(self, colorChoice : int = 0):
        #copying current image
        image = self.image
        try: # operaion
            if colorChoice != 0:
                image = ImageOps.colorize(image.convert('L'), black = 'black',white=self._colorList(colorChoice-1))
            else:
                if self.custom_color:
                    image = ImageOps.colorize(image.convert('L'), black = 'black', white = self.custom_color)
        except MemoryError as memoryError:
            return f"Memory Error Occurred-> {memoryError}"
        except ValueError as valueError:
            return f"Value is unclear -> {valueError}"
        except IndexError as indexError:
            return f"{indexError}"
        
        self.image = image
        return self.image
    
    # color Filter
    def addColorLayer(self, choice : int = 0):
        #copying current image
        image = self.image

        #procedure
        try:
            if choice != 0:
                # color layer creation
                layer = Image.new(mode='RGBA',size=image.size,color = self._RGBAcolorList(index = choice-1))
            else:
                if self.custom_color:
                    layer = Image.new(mode='RGBA', size=image.size, color=self.custom_color)
            image = ImageChops.blend(layer,image.convert('RGBA'),alpha=2) # blending
        except MemoryError as memoryError:
            return f"Insufficient Memory -> {memoryError}"
        except ValueError as valueError:
            return f"Undefined Value -> {valueError}"
        except IndexError as indexError:
            return f"Invalid Index -> {indexError}"
        except TypeError as typeError:
            return f"Wrong Type -> {typeError}"
        
        self.image = image
        return self.image
    pass