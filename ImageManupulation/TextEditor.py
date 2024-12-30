# this module is responsible for doing variaus kind of text editing it takes an image as input to use it's dimentions
from PIL import Image, ImageDraw, ImageFont

class TextEditor:
    DEFAULT_FONT_STYLE = r"D:\Programming Library\PythonProgramming\Learning\assets\times new roman.ttf"
    # value holders
    prev_position : tuple[int, int] = None
    prev_size : int = None
    prev_color : list = None
    prev_textWidth : int = None
    # consturctor
    def __init__(self, image : Image.Image)->None:
        '''Takes the Current working Image as parameter to create one RGBA Transparent layer of it'''
        self.baseLayer = Image.new(mode = "RGBA", size=image.size, color = (0, 0, 0, 0))
        self.drawObject = ImageDraw.Draw(self.baseLayer)
        return
    
    def editText(
            self, text : str = None, position : tuple = None, size : int = None, color : list = None,
            textWidth : int = None
    ) -> Image.Image:
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
            size = 20
            self.prev_size = 20
        elif(size and self.prev_size == None):
            self.prev_size = size
        elif(size == None and self.prev_size):
            size = self.prev_size
        else:
            self.prev_size = size
        
        if(color == None and self.prev_color == None): # color filter
            color = [255, 255, 255, 255]
            self.prev_color = color
        elif(color and self.prev_color == None):
            self.prev_color = color
        elif(color == None and self.prev_color):
            color = self.prev_color
        else:
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
        try:
            font = ImageFont.truetype(font=self.DEFAULT_FONT_STYLE, size = size)
            self.drawObject.text(
                xy = position, text = text, font = font, fill = tuple(color), stroke_width=textWidth, anchor = "mm"
            )
        except TypeError:
            print("Got some typing Problem")
        except OSError:
            print("got some problem to find files")
        return self.baseLayer
    pass

if __name__ == '__main__':
    textEditor = TextEditor(Image.open(
        r"D:\Gallery\PhotoSpace\downloaded pic\Phone WallPaper\e7dc3878-ed3a-4bd4-8bfa-3b5dc874ebec.jfif"
        )
    )
    layer = textEditor.editText(text = "Sujal Khan", position = (100,100) ,size = None, color = [255,0,0,255], textWidth=None)
    # layer.show()
    layer = textEditor.editText(text = "Sujal Khan", position = (300,300) ,size = None, color = [255,0,0,255], textWidth=None)
    # layer.show()
    layer = textEditor.editText(text = "Sujal Khan", position = (100,300) ,size = None, color = [255,0,0,255], textWidth=None)
    # layer.show()
    layer = textEditor.editText(text = "Sujal Khan", position = (300,100) ,size = None, color = [255,0,0,255], textWidth=None)
    layer.show()