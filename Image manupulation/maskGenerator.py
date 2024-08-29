from PIL import Image, ImageDraw

class Masks:
    #constructor
    def __init__(self, width : int, height : int) -> None:
        self.width, self.height = width, height
        self._metaData = {
            1 : "RGBA", # mode
            2 : (self.width, self.height), # size
            3 : (255,255,255,255) # color
        }# meta data helps to change the property of the masks
        self.groundLayer = Image.new(mode=self._metaData[1], size=self._metaData[2], color= self._metaData[3])
        return
    
    # rectangle layer
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
    
    # style 1 : Left diagonal
    def style_one_mask(self) -> Image.Image:
        qWidth = 2*(self.width/3)
        qHeight = 2*(self.height/3)
        drawObject = ImageDraw.Draw(self.groundLayer)
        drawObject.polygon(((10,10), (10,self.height/3), (self.width/3,10), (10,10)),fill=(0,0,0,0))
        drawObject.polygon(((10,self.height/3), (qWidth,self.height-10), (self.width-10,qHeight), (self.width/3,10)),fill=(0,0,0,0))
        drawObject.polygon(((qWidth,self.height-10), (self.width-10,self.height-10), (self.width-10, qHeight), (qWidth,self.height-10)), fill=(0,0,0,0))
        return self.groundLayer
    
    # style 2 : five section rectangle
    def style_two_mask(self) -> Image.Image:
        qwidth = 2*(self.width/3)
        lwidth, lheight = (self.width/3), (self.height/2)
        drawObject = ImageDraw.Draw(self.groundLayer)
        drawObject.polygon(((lwidth+10,10), (lwidth+10,self.height-10), (qwidth-10,self.height-10), (qwidth-10, 10)),fill=(0,0,0,0))
        drawObject.polygon(((10,10), (10,lheight-10), (lwidth-10, lheight-10), (lwidth-10, 10)), fill=(0,0,0,0))
        drawObject.polygon(((10,lheight+10), (10,self.height-10), (lwidth-10, self.height-10), (lwidth-10, lheight+10)), fill=(0,0,0,0))
        drawObject.polygon(((qwidth+10,lheight+10), (qwidth+10,self.height-10), (self.width-10,self.height-10), (self.width-10,lheight+10)), fill=(0,0,0,0))
        drawObject.polygon(((qwidth+10,10), (qwidth+10,lheight-10), (self.width-10,lheight-10), (self.width -10,10)), fill=(0,0,0,0))
        return self.groundLayer
    
    # style 3 : deadpool mask
    def style_three_mask(self) -> Image.Image:
        return self.groundLayer