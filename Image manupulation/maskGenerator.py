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
        self.groundLayer = Image.new(mode=self._metaData[1], size=self._metaData[2], color= (0,0,0,20))
        width, height = self.width, self.height
        if width > height:
            pad = (width-height)/2
            drawObject = ImageDraw.Draw(self.groundLayer)
            fillColor = [(255,0,0,150), (0,0,0,0), (255,0,0,150)]
            coordinates = [(pad, 0, width - pad, height),
                (pad + 20, 20, width - pad - 20, height - 20),
                (pad + 40, 40, width-pad-40, height-40)
            ]
            # outer layer(red), # middle layer(black), # inner layer(red)
            for i in range(len(fillColor)):
                drawObject.ellipse(coordinates[i], fill= fillColor[i])
        border_black = 50
        heightReducer = 30
        drawObject.polygon(((width/2 - border_black,heightReducer), (width/2 - border_black, height - heightReducer), (width/2 + border_black, height - heightReducer),(width/2 + border_black, heightReducer), ), fill = (0,0,0,0))
        # left eyes
        eyeLeft = (width/2-70,height/2)
        leftEyeCoordinates = [(width/4 + 40, height/4 + 40),
            (5*width/16 ,height/2),
            (5.4*width/16, 9*height/16),
            (6.1*width/16, 9.5*height/16),
            (6.8*width/16, 9*height/16),
        ]
        for i in range(len(leftEyeCoordinates)-1):
            drawObject.polygon((eyeLeft, leftEyeCoordinates[i], leftEyeCoordinates[i+1], eyeLeft), fill=(0,0,0,0))
        
        # right eye
        eyeRight = (width/2+70, height/2)
        rightEyeCoordinate = [(3*width/4 - 40, height/4+40),
            (11*width/16, height/2),
            (10.6*width/16, 9*height/16),
            (9.9*width/16, 9.5*height/16),
            (9.2*width/16, 9*height/16)
        ]
        for i in range(len(rightEyeCoordinate)-1):
            drawObject.polygon((eyeRight, rightEyeCoordinate[i], rightEyeCoordinate[i+1], eyeRight), fill=(0,0,0,0))
        return self.groundLayer
    
    # style 4 : star
    def starShape(self) -> Image.Image:
        width10, height10 = self.width/10, self.height/10 # smallest units of widtyh and height req here
        drawObject = ImageDraw.Draw(self.groundLayer)
        centre = (5*width10, 5*height10)
        coordinates = [
            (5*width10, 0.5*height10),
            (5.78*width10, 4*height10),
            (8*width10, 4*height10),
            (6*width10, 6*height10),
            (7*width10, 9.5*height10),
            (5*width10, 7*height10),
            (3*width10, 9.5*height10),
            (4*width10, 6*height10),
            (2*width10, 4*height10),
            (4.3*width10, 4*height10),
            (5*width10, 0.5*height10)
        ]
        for i in range(len(coordinates)-1):
            drawObject.polygon((centre, coordinates[i], coordinates[i+1], centre), fill=(0,0,0,0))
        return self.groundLayer
    
    # style 5 : right diagonal
    def style_five_mask(self) -> Image.Image:
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        quarterWidth, quarterHeight =  2 * self.width/3, 2 * self.height/3 # 2/3 of the width and height
        width3, height3 = self.width/3, self.height/3 # 1/3 of the width, height
        drawObject.polygon(xy = ((quarterWidth,10), (self.width-10, height3), (width3, self.height-10), (10, quarterHeight)), fill = (0,0,0,0))
        drawObject.polygon(xy = ((10, self.height-10), (10, quarterHeight), (width3, self.height - 10), (10, self.height - 10)), fill = (0, 0, 0, 0 ))
        drawObject.polygon(xy = ((self.width -10, 10), (self.width - 10, height3), (quarterWidth, 10), (self.width-10, 10)), fill = (0, 0, 0, 0))
        return self.groundLayer
    
    # style 6 : left layOut
    def style_six_mask(self) -> Image.Image:
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        quarterWidth, quarterHeight =  2 * self.width/3, 2 * self.height/3 # 2/3 of the width and height
        drawObject.polygon(xy= ((10, 10), (10, self.height - 10), (quarterWidth, self.height - 10), (quarterWidth, 10)), fill= (0, 0, 0, 0))
        return self.groundLayer
    
    # style 7 : right layOut
    def style_seven_mask(self) -> Image.Image:
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        width3, height3 =  self.width/3, self.height/3 # 1/3 of the width and height
        drawObject.polygon(xy= ((width3, 10), (width3, self.height - 10), (self.width - 10, self.height - 10,), (self.width - 10, 10)), fill= (0, 0, 0, 0))
        return self.groundLayer
Masks.style_seven_mask(Masks(1920, 1080)).show()