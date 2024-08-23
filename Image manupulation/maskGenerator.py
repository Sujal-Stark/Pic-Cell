from PIL import Image, ImageDraw

class Masks:
    #constructor
    def __init__(self, width : int, height : int) -> None:
        self.width, self.height = width, height
        self.groundLayer = Image.new(mode='RGBA', size=(self.width,self.height), color=(255,255,255,255))
        return
    
    # rectangular space mask
    def layeredRectangle(self) -> Image.Image:
        drawObject = ImageDraw.Draw(self.groundLayer)
        drawObject.rectangle((10,10,self.width-10,self.height-10),fill=(0,0,0,0))
        drawObject.rectangle((20,20,self.width-20,self.height-20),fill=(255,255,255,255))
        drawObject.rectangle((30,30,self.width-30,self.height-30),fill=(0,0,0,0))
        return self.groundLayer
    
    # creating roumbous mask
    def rombousMask(self) -> Image.Image:
        ImageDraw.Draw(self.groundLayer).polygon((0,self.height/2, self.width/2,self.height, self.width,self.height/2, self.width/2,0),fill=(0,0,0,0))
        return self.groundLayer
    
    # Elliptical mask
    def ellipticalMask(self) -> Image.Image:
        ImageDraw.Draw(self.groundLayer).ellipse((1.5, 1.5, self.width - 1.5, self.height - 1.5),fill=(0,0,0,0))
        return self.groundLayer
    
    # Circular mask
    def circularMask(self) -> Image.Image:
        if self.width > self.height:
            pad = (self.width-self.height)/2
            ImageDraw.Draw(self.groundLayer).ellipse((pad, 0, self.width - pad, self.height), fill= (0,0,0,0))
        elif self.height > self.width:
            pad = (self.height-self.width)/2
            ImageDraw.Draw(self.groundLayer).ellipse((0, pad, self.width, self.height-pad), fill=(0,0,0,0))
        else:
            return self.ellipticalMask(self.width,self.height)
        return self.groundLayer
    
    # Double circle mask
    def doubleCircleMask(self) -> Image.Image:
        drawObject = ImageDraw.Draw(self.groundLayer)
        if self.width>self.height:
            pad = self.width-self.height
            drawObject.ellipse((0,0,self.height,self.height),fill=(0,0,0,0))
            drawObject.ellipse((pad,0,self.width,self.height),fill=(0,0,0,0))
        elif self.height>self.width:
            pad = self.height-self.width
            drawObject.ellipse((0,0,self.width,self.width),fill=(0,0,0,0))
            drawObject.ellipse((0,pad,self.width,self.height),fill=(0,0,0,0))
        else:
            return self.ellipticalMask(self.width,self.height)
        return self.groundLayer
    
    # transverse image
    def style_one_mask(self) -> Image.Image:
        qWidth = 2*(self.width/3)
        qHeight = 2*(self.height/3)
        drawObject = ImageDraw.Draw(self.groundLayer)
        drawObject.polygon(((10,10), (10,self.height/3), (self.width/3,10), (10,10)),fill=(0,0,0,0))
        drawObject.polygon(((10,self.height/3), (qWidth,self.height-10), (self.width-10,qHeight), (self.width/3,10)),fill=(0,0,0,0))
        drawObject.polygon(((qWidth,self.height-10), (self.width-10,self.height-10), (self.width-10, qHeight), (qWidth,self.height-10)), fill=(0,0,0,0))
        return self.groundLayer
    
    pass
mask_one = Masks.style_one_mask(Masks(1920,1080))
mask_one.show()