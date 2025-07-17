# this module is responsible for doing variaus kind of text editing it takes an image as input to use it's dimentions
from PIL import Image, ImageDraw, ImageFont
from icecream import ic
class TextEditor:
    DEFAULT_FONT_STYLE = r"D:\Programming Library\PythonProgramming\Learning\assets\times new roman.ttf"
    # value holders
    prev_text : str = None
    prev_font : ImageFont.ImageFont = None
    prev_position : tuple[int, int] = None
    prev_size : int = None
    prev_color : list = None
    prev_textWidth : int = None
    prev_anchorPoint : int = None
    prev_textOpacity : int = None

    prev_incrementFactor : int = None
    prev_outlineColor  : tuple = None
    prev_fillColor : tuple = None
    prev_opacity : int = None
    prev_lineWidth : int = None
    
    anchorList : list = {
        "Top Left" : "lt", # top left,
        "Top Center" : "mt", # top middle
        "Top Right" : "rt", # top right
        "Center Left" : "lm",# mid left
        "Center" : "mm", # centre
        "Center Right" : "rm", # mid right
        "Bottom Left" : "lb", # left bottom
        "Bottom Center" : "mb", # mid bottom
        "Bottom Right" : "rb", #right bottom
    }
    
    # consturctor
    def __init__(self, image : Image.Image)->None:
        '''Takes the Current working Image as parameter to create one RGBA Transparent layer of it'''
        self.baseLayer = Image.new(mode = "RGBA", size=image.size, color = (0, 0, 0, 0)) # holds text editing
        self.backgroundlayer = Image.new(mode = "RGBA", size=image.size, color = (0, 0, 0, 0)) # holds background editing
        self.image = image # holds the original image
        self.newLayer = None # holds the temporary text edit to show in window
        self.boxLayer = None # holds the text box edit to show in window
        self.imWidth, self.imHeight = self.image.size # holds the image dimentions
        self.meta = {
            "text" : None,
            "font" : None,
            "position" : None,
            "text size" : None,
            "text color" : None,
            "text width" : None,
            "anchor" : None,
            "text opacity" : None,
            "increment" : None,
            "outline color" : None,
            "box color" : None,
            "lineWidth" : None,
            "box opacity" : None
        }
        return

    def setMetaInformation(self, information : dict):
        self.prev_text = information["text"]
        self.prev_size = information["text size"]
        self.prev_position = information["position"]
        self.prev_anchorPoint = information["anchor"]
        self.prev_textWidth = information["text width"]
        self.prev_textOpacity = information["text opacity"]
        self.prev_textColor = information["text color"]
        self.prev_incrementFactor = information["increment"]
        self.prev_textBoxOpacity = information["box opacity"]
        self.prev_textBoxColor = information["box color"]
        self.prev_outlineColor = information["outline color"]
        # self.textEditor.prev_lineWidth = information["lineWidth"]
        return

    def generateFinalEdit(self) -> Image.Image:
        '''This method is responsible for generating the final image after text and text box editing'''
        self.newLayer.show()
        if self.boxLayer and self.newLayer: # if both layer are present
            return Image.alpha_composite(im1 = self.boxLayer, im2 = self.newLayer)
        elif self.newLayer: #only text layer can be rendered if no background layer is present
            return self.newLayer
    
    def editText(
            self, text : str = None, position : tuple = None, size : int = None, color : list = None, textWidth : int = None, anchor_tag : str = "Center",
            textOpacity : int = None
    ) -> None:
        self.newLayer = self.baseLayer.copy() # creates a new layer based upon the base layer
        drawObject = ImageDraw.Draw(self.newLayer) # draw object to perform drawing operatation
        
        if (self.prev_text == None and text): # text filter
            self.prev_text = text
        elif(self.prev_text and text == None):
            text = self.prev_text
        elif self.prev_text and text:
            self.prev_text = text

        if(position == None and self.prev_position == None): # position filter
            position = (self.baseLayer.width/2, self.baseLayer.height/2)
            self.prev_position = position
        elif(position and self.prev_position == None):
            self.prev_position = position
        elif(position == None and self.prev_position):
            position = self.prev_position
        else:
            self.prev_position = position
        
        if(size == None and self.prev_size == None): # size filter
            size = 50
            self.prev_size = size
        elif(size and self.prev_size == None):
            size = (1 if size <= 0 else size)
            self.prev_size = size
        elif(size == None and self.prev_size):
            size = self.prev_size
        else:
            size = (1 if size <= 0 else size)
            self.prev_size = size
        
        if(textOpacity == None and self.prev_textOpacity == None): # text opacity filter
            self.prev_textOpacity, textOpacity = 255, 255
        elif(textOpacity and self.prev_textOpacity == None):
            self.prev_textOpacity = textOpacity
        elif(textOpacity == None and self.prev_textOpacity):
            textOpacity = self.prev_textOpacity
        else:
            self.prev_textOpacity = textOpacity

        if(color == None and self.prev_color == None): # color filter
            color = [255, 255, 255, textOpacity]
            self.prev_color = color
        elif(color and self.prev_color == None):
            color = color + [textOpacity]
            self.prev_color = color
        elif(color == None and self.prev_color):
            self.prev_color[3] = textOpacity
            color = self.prev_color
        else:
            color = color + [textOpacity]
            self.prev_color = color
        
        if(textWidth == None and self.prev_textWidth == None): # textwidth filter
            textWidth = 0
            self.prev_textWidth = textWidth
        elif(textWidth and self.prev_textWidth == None):
            self.prev_textWidth = textWidth
        elif(textWidth == None and self.prev_textWidth):
            textWidth = self.prev_textWidth
        else:
            self.prev_textWidth = textWidth
        
        if(anchor_tag == None and self.prev_anchorPoint == None): # anchor point
            anchor_tag, self.prev_anchorPoint = 4, 4
        elif(anchor_tag and self.prev_anchorPoint == None):
            self.prev_anchorPoint = anchor_tag
        elif(anchor_tag == None and self.prev_anchorPoint):
            anchor_tag = self.prev_anchorPoint
        else:
            self.prev_anchorPoint = anchor_tag
        print(text)
        try:
            font = ImageFont.truetype(font=self.DEFAULT_FONT_STYLE, size = size)
            self.prev_text = text
            self.prev_font = font
            drawObject.text(
                xy = position, text = text, font = font, fill = tuple(color), stroke_width=textWidth, anchor = self.anchorList[anchor_tag]
            )
            self.meta["text"] = text
            self.meta["position"] = position
            self.meta["text size"] = size
            self.meta["text color"] = color
            self.meta["text width"] = textWidth
            self.meta["anchor"] = anchor_tag
            self.meta["text opacity"] = textOpacity
        except KeyError:
            print("Invalid anchor Tag")
        except TypeError:
            print("Got some typing Problem")
        except OSError:
            print("got some problem to find files")

    def editTextBox(
            self, increment_Factor : int = None, outlineColor : list = None,fillColor : list = None, opacity : int = None, lineWidth : int = None
    ):
        self.boxLayer : Image.Image = self.backgroundlayer.copy()
        tokenDrawObject : ImageDraw.ImageDraw = ImageDraw.Draw(self.boxLayer)
        
        if(increment_Factor == None and self.prev_incrementFactor == None): # increment factor
            increment_Factor, self.prev_incrementFactor = 0, 0
        elif(increment_Factor != None and self.prev_incrementFactor == None):
            self.prev_incrementFactor = increment_Factor
        elif(increment_Factor == None and self.prev_incrementFactor != None):
            increment_Factor = self.prev_incrementFactor
        else:
            self.prev_incrementFactor = increment_Factor
        
        if(opacity == None and self.prev_opacity == None): # opacity
            opacity, self.prev_opacity = 255, 255
        elif(opacity and self.prev_opacity == None):
            self.prev_opacity = opacity
        elif(opacity == None and self.prev_opacity):
            opacity = self.prev_opacity
        else:
            self.prev_opacity = opacity
        
        if(outlineColor == None and self.prev_outlineColor == None): # outline color
            outlineColor = [255,255,255,opacity]
            self.prev_outlineColor = outlineColor
        elif(outlineColor and self.prev_outlineColor == None):
            outlineColor = outlineColor + [opacity]
            self.prev_outlineColor = outlineColor
        elif(outlineColor == None and self.prev_outlineColor):
            self.prev_outlineColor[3] = opacity
            outlineColor = self.prev_outlineColor
        else:
            outlineColor = outlineColor + [opacity]
            self.prev_outlineColor = outlineColor

        
        if(fillColor == None and self.prev_fillColor == None): # fillcolor
            fillColor = [0,0,0,opacity]
            self.prev_fillColor = fillColor
        elif(fillColor and self.prev_fillColor == None):
            fillColor = fillColor+[opacity]
            self.prev_fillColor = fillColor
        elif(fillColor == None and self.prev_fillColor):
            self.prev_fillColor[3] = opacity
            fillColor = self.prev_fillColor
        else:
            fillColor = fillColor+[opacity]
            self.prev_fillColor = fillColor
        
        if(lineWidth == None and self.prev_lineWidth == None): # line width
            lineWidth, self.prev_lineWidth = 1, 1
        elif(lineWidth and self.prev_lineWidth == None):
            self.prev_lineWidth = lineWidth
        elif(lineWidth == None and self.prev_lineWidth):
            lineWidth = self.prev_lineWidth
        else:
            self.prev_lineWidth = lineWidth
        
        try:
            bbox = tokenDrawObject.textbbox(
                xy = self.prev_position, text = self.prev_text, font = self.prev_font, anchor = self.anchorList[self.prev_anchorPoint]
            )
            bbox = (bbox[0] - increment_Factor, bbox[1] - increment_Factor, bbox[2] + increment_Factor, bbox[3] + increment_Factor)
            tokenDrawObject.rectangle(xy = tuple(bbox), fill = tuple(fillColor), outline = tuple( outlineColor), width = lineWidth)
            self.meta["increment"] = increment_Factor,
            self.meta["outline color"] = outlineColor
            self.meta["box color"] = fillColor
            self.meta["lineWidth"] = lineWidth
            self.meta["box opacity"] = opacity
        except KeyError:
            print("Invalid key")
        except MemoryError:
            print("System Run out of memory")
        except TypeError:
            print("Got mismatched typing")
        except OSError:
            print("unable to fetch the file")
    pass

if __name__ == '__main__':
    textEditor = TextEditor(Image.open(
        r"D:\Gallery\PhotoSpace\downloaded pic\Phone WallPaper\e7dc3878-ed3a-4bd4-8bfa-3b5dc874ebec.jfif"
        )
    )
    textEditor.editText(text = "Sujal Khan", position = None ,size = 100, color = [255,0,255], textWidth=None, textOpacity = 120)
    textEditor.editTextBox(increment_Factor = 50, outlineColor = [255,255,0,255], fillColor = [0, 255, 255], opacity = 120, lineWidth = 2)
    image = textEditor.generateFinalEdit()
    image.show()
    pass