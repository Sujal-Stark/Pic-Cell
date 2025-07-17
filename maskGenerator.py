from PIL import Image, ImageDraw

class Masks:
    frameOptions = ["Rectangle Layer", "Rombous", "Ellipse", "Circle", "Double Circle", "Left Diagonal", "Right Diagonal", "Five Section Rectangle", "Dead pool", "Star", "Left Frame", "Right Frame", "Step Size"] # editing options available
    subEditingTree = {
        "Rectangle Layer" : {
            "Border" : {"minVal" : 10, "maxVal" : 200, "currentPosition" : 0, "change" : 25}
        },
        "Rombous" : {},
        "Ellipse" : {
            "Border" : {"minVal" : 0, "maxVal" : 200, "currentPosition" : 2, "change" : 25}
        },
        "Circle" : {
            "Border" : {"minVal" : 0, "maxVal" : 200, "currentPosition" : 10, "change" : 25}
        },
        "Double Circle" : {},
        "Left Diagonal" : {
            "Border" : {"minVal" : 0, "maxVal" : 200, "currentPosition" : 10, "change" : 25}
        },
        "Right Diagonal" : {
            "Border" : {"minVal" : 0, "maxVal" : 200, "currentPosition" : 10, "change" : 25}
        },
        "Left Frame" : {
            "Border" : {"minVal" : 0, "maxVal" : 300, "currentPosition" : 10, "change" : 25}
        },
        "Right Frame" : {
            "Border" : {"minVal" : 0, "maxVal" : 300, "currentPosition" : 10, "change" : 25}
        },
        "Star" : {},
        "Dead pool" : {},
        "Five Section Rectangle" : {},
        "Step Size" : {}
    }
    
    def getImageObject(self, img : Image.Image) -> None:
        self.image = img
        self.width, self.height = img.size
        return
    
    # self.buffer objects
    custom_color = (255, 255, 255, 255) # color of the frames
    bufferGroundLayer = Image.new(mode = "RGBA", size = (0, 0), color = (255,255,255,255))

    # constants
    layerRectangleModifier = 0
    elipticalMaskModifier = 10
    circularMaskModifier = 10
    leftDiagonalModifier = 10
    rightDiagonalModifier = 10
    leftLayoutModifier = 10
    rightLayoutModifier = 10

    # rectangle layer
    def layeredRectangle(self, modifier : int = 0, chosenColor : tuple = None) -> Image.Image:
        # stores and reuse the modifier value
        if modifier == 0:
            modifier = self.layerRectangleModifier
        else:
            self.layerRectangleModifier = modifier
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
              
        drawObject = ImageDraw.Draw(self.groundLayer)
        modifier1 = modifier + 10
        modifier2 = modifier + 20
        modifier3 = modifier + 30
        if self.width >= 2 * modifier3 and self.height >= 2 * modifier3:
            drawObject.rectangle((modifier1,modifier1 ,self.width-modifier1,self.height-modifier1),fill=(0,0,0,0))
            drawObject.rectangle((modifier2,modifier2,self.width-modifier2,self.height-modifier2),self.custom_color)
            drawObject.rectangle((modifier3,modifier3,self.width-modifier3,self.height-modifier3),fill=(0,0,0,0))
        return self.groundLayer
    
    # creating roumbous mask
    def rombousMask(self, chosenColor : tuple = None) -> Image.Image:
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        ImageDraw.Draw(self.groundLayer).polygon((0,self.height/2, self.width/2,self.height, self.width,self.height/2, self.width/2,0),fill=(0,0,0,0))
        return self.groundLayer
    
    # Elliptical mask
    def ellipticalMask(self, modifier : int =10, chosenColor : tuple = None) -> Image.Image:
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        # stores and releases the previous value
        if modifier == 10:
            modifier = self.elipticalMaskModifier
        else:
            self.elipticalMaskModifier = modifier

        if (modifier <= self.width-modifier) and (modifier <= self.height-modifier):
            ImageDraw.Draw(self.groundLayer).ellipse((modifier,modifier,self.width-modifier,self.height-modifier),fill=(0,0,0,0))
        return self.groundLayer
    
    # Circular mask
    def circularMask(self, modifier : int = 10, chosenColor : tuple = None) -> Image.Image:
        if modifier == 10:
            modifier = self.circularMaskModifier
        else:
            self.circularMaskModifier = modifier
        
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)

        pad = abs(self.width-self.height)/2
        if self.width > self.height:
            if (2*(pad + modifier) <= self.width) and (2 * pad <= self.height):
                ImageDraw.Draw(self.groundLayer).ellipse((pad + modifier, modifier, self.width - pad - modifier, self.height - modifier), fill= (0,0,0,0))
        elif self.height > self.width:
            if (2*(pad + modifier) <= self.height) and (2 * pad <= self.width):
                ImageDraw.Draw(self.groundLayer).ellipse((modifier, pad + modifier, self.width - modifier, self.height-pad - modifier), fill=(0,0,0,0))
        else:
            return self.ellipticalMask(modifier = modifier)
        return self.groundLayer
    
    # Double circle mask
    def doubleCircleMask(self, chosenColor : tuple = None) -> Image.Image:
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
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
    def style_one_mask(self, modifier : int = 10, chosenColor : tuple = None) -> Image.Image:
        if modifier == 10:
            modifier = self.leftDiagonalModifier
        else:
            self.leftDiagonalModifier = modifier
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        width3, height3 = self.width/3, self.height/3
        drawObject = ImageDraw.Draw(self.groundLayer)
        if modifier <= width3 and modifier <= height3:
            qWidth, qHeight = 2*(self.width/3), 2*(self.height/3)
            drawObject.polygon(((modifier,modifier), (modifier,self.height/3), (self.width/3,modifier), (modifier,modifier)),fill=(0,0,0,0))
            drawObject.polygon(((modifier,self.height/3), (qWidth,self.height-modifier), (self.width-modifier,qHeight), (self.width/3,modifier)),fill=(0,0,0,0))
            drawObject.polygon(((qWidth,self.height-modifier), (self.width-modifier,self.height-modifier), (self.width-modifier, qHeight), (qWidth,self.height-modifier)), fill=(0,0,0,0))
            self.bufferGroundLayer = self.groundLayer
            return self.groundLayer
        else:
            return self.bufferGroundLayer
    
    # style 2 : five section rectangle
    def style_two_mask(self, chosenColor : tuple = None) -> Image.Image:
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)

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
        self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color= (0,0,0,20))
        width, height = self.width, self.height
        if self.width < self.height:
            return self.groundLayer
        else:
            pad = abs(width-height)/2
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
    def starShape(self, chosenColor : tuple = None) -> Image.Image:
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
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
    def style_five_mask(self, modifier : int = 10, chosenColor : tuple = None) -> Image.Image:
        if modifier == 10:
            modifier = self.rightDiagonalModifier
        else:
            self.rightDiagonalModifier = modifier
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        width3, height3 = self.width/3, self.height/3 # 1/3 of the width, height
        if modifier <= width3 and modifier <= height3:
            quarterWidth, quarterHeight =  2 * self.width/3, 2 * self.height/3 # 2/3 of the width and height
            drawObject.polygon(xy = ((quarterWidth,modifier), (self.width-modifier, height3), (width3, self.height-modifier), (modifier, quarterHeight)), fill = (0,0,0,0))
            drawObject.polygon(xy = ((modifier, self.height-modifier), (modifier, quarterHeight), (width3, self.height - modifier), (modifier, self.height - modifier)), fill = (0, 0, 0, 0 ))
            drawObject.polygon(xy = ((self.width -modifier, modifier), (self.width - modifier, height3), (quarterWidth, modifier), (self.width-modifier, modifier)), fill = (0, 0, 0, 0))
            self.bufferGroundLayer = self.groundLayer
            return self.groundLayer
        else:
            return self.bufferGroundLayer
    
    # style 6 : left layOut
    def style_six_mask(self, modifier : int = 10, chosenColor : tuple = None) -> Image.Image:
        if modifier == 10:
            modifier = self.leftLayoutModifier
        else:
            self.leftLayoutModifier = modifier
        
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        quarterWidth =  2 * self.width/3 # 2/3 of the width
        if (modifier <= quarterWidth) and (quarterWidth - modifier >= self.width/3):
            drawObject.polygon(xy= ((10, 10), (10, self.height - 10), (quarterWidth-modifier, self.height - 10), (quarterWidth-modifier, 10)), fill= (0, 0, 0, 0))
            self.bufferGroundLayer = self.groundLayer
        else:
            self.groundLayer = self.bufferGroundLayer
        return self.groundLayer
    
    # style 7 : right layOut
    def style_seven_mask(self, modifier : int = 10, chosenColor : tuple = None) -> Image.Image:
        if modifier == 10:
            modifier = self.rightLayoutModifier
        else:
            self.rightLayoutModifier = modifier
        
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        width3 =  self.width/3 # 1/3 of the width
        if (modifier + width3 <= 2*width3):
            drawObject.polygon(xy= ((width3 + modifier, 10), (width3 + modifier, self.height - 10), (self.width - 10, self.height - 10,), (self.width - 10, 10)), fill= (0, 0, 0, 0))
            self.bufferGroundLayer = self.groundLayer
        else:
            self.groundLayer = self.bufferGroundLayer
        return self.groundLayer
    
    # style 8
    def style_eight_mask(self, chosenColor : tuple = None) -> Image.Image:
        # stores the previous color of frames
        if chosenColor:
            self.custom_color = chosenColor # when new color is available
            self.groundLayer = Image.new(mode="RGBA", size=(self.width, self.height), color=self.custom_color)
        else: # if new color is not available
            self.groundLayer = Image.new(mode="RGBA", size=self.image.size, color = self.custom_color)
        
        drawObject = ImageDraw.Draw(im = self.groundLayer)
        widthFraction, heightFraction = self.width/6, self.height/6 # divides the width and height in smaller units
        for i in range(6):
            drawObject.polygon(xy = ((i * widthFraction+10, 10), (i * widthFraction + 10, (6 - i) * heightFraction - 10), ((i + 1) * widthFraction + 10, (6 - i) * heightFraction - 10), ((i + 1) * widthFraction + 10, 10)), fill = (0, 0, 0 ,0))
        drawObject.polygon(xy = ((self.width - 10,0), (self.width - 10, heightFraction), (self.width, heightFraction), (self.width, 0)), fill = self.custom_color)
        for i in range(6):
            drawObject.line(xy = ((i * widthFraction + 10, 0), (i * widthFraction + 10, (6-i) * heightFraction)), fill= self.custom_color ,width = 2)
            drawObject.line(xy=((0,i*heightFraction-10),((6-i)*widthFraction+10,i*heightFraction-10)),fill=self.custom_color,width=2)
        return self.groundLayer
    pass