# important inbuilt libraries
from PIL import Image, ImageOps

# class
class ImageDeformer:
    deformOptions = ["Twist", "Double Twist", "Horizontal Split", "Vertical Split", "Multiply", "Add Layer", "Chess Like", "Half Mirror", "Four Mirror", "Sine Curve"] # editing options

    subEditingTree = {
        "Twist" : {},
        "Double Twist" : {},
        "Horizontal Split" : {
            "Repetaion" : {"minVal" : 2, "maxVal" : 64, "currentPosition" : 4, "change" : 2}
        },
        "Vertical Split" : {
            "Repetaion" : {"minVal" : 2, "maxVal" : 64, "currentPosition" : 4, "change" : 2}
        },
        "Multiply" : {
            "Multiply factor" : {"minVal" : 0, "maxVal" : 6, "currentPosition" : 0, "change" : 1}
        },
        "Add Layer" : {
            "Layer number" : {"minVal" : 1, "maxVal" : 10, "currentPosition" : 5, "change" : 1},
            "Padding" : {"minVal" : 10, "maxVal" : 100, "currentPosition" : 10, "change" : 10}
        },
        "Chess Like" : {
            "Box Length" : {"minVal" : 1, "maxVal" : 80, "currentPosition" : 20, "change" : 5}
        },
        "Half Mirror" : {},
        "Four Mirror" : {},
        "Sine Curve" : {
            "Cycle value" : {"minVal" : 4, "maxVal" : 64, "currentPosition" : 32, "change" : 4}
        }
    }

    # constants
    layerValue = 5
    paddingValue = 10

    # provides user messege
    def getMessage(self):
        return self.userMessage
    
    # get image object
    def getImageObject(self, image : Image.Image) -> None:
        self.image = image
        return

    
    # looks like iamge is fast forwarded
    def middleTwist(self):
        image = self.image # copying original image object
        try:
            # mesh class will parse to deform method
            class DeformMesh:
                def getmesh(self, image):
                    width , height = image.size
                    desiredMesh1 = (0,0, 0,height, width, 0, width, height)
                    targetMesh1 = (0, 0, width, height)
                    return [(targetMesh1, desiredMesh1)]
            image = ImageOps.deform(image, DeformMesh())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        self.image = image
        return self.image
    
    # twist at both quarter half
    def doubleTwisted(self):
        image = self.image # copying image object
        try:
            class DeformMesh:
                def getmesh(self, image : Image.Image):
                    width , height = image.size
                    desiredMesh1 = (0, 0, 0, height, width/2,0, width/2, height)
                    targetMesh1 = (0, 0, width//2, height)
                    desiredMesh2 = (width/2, height, width/2, 0, width, height, width, 0)
                    targetMesh2 = (width//2, 0, width, height)
                    return [(targetMesh1, desiredMesh1), (targetMesh2, desiredMesh2)]
            image = ImageOps.deform(image=image, deformer= DeformMesh())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        self.image = image
        return self.image
    
    # horizontally devides and deviates the image dimentions
    def horizontalSplit(self, repeaterValue = 4):
        # copying actual image instance
        image = self.image
        try:
            class DefromElmlecator:
                def getmesh(self, image : Image.Image):
                    repeater = repeaterValue
                    width, height = image.size # original size of the image
                    width4, height8 = width//4, height//repeater # breaking the width and hight into quarters
                    width34 = width4*3 # 3rd quarter of the width
                    meshes = [] # stores the mesh co ordinates
                    for i in range(repeater):
                        firstQuarter= (0 if i%2 == 0 else width4)
                        thirdQuarter = (width34 if i%2 == 0 else width)
                        meshes.append(((0, i*height8,
                            width, (i+1) * height8),
                            (firstQuarter, i*height8,
                            firstQuarter, (i+1)*height8,
                            thirdQuarter, (i+1)*height8,
                            thirdQuarter, i* height8)))
                    return meshes
            image = ImageOps.deform(image=image, deformer=DefromElmlecator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    pass

    # vertical split
    def verticalSplit(self, repeaterValue = 4):
        image = self.image # copyin the actual image obejct
        try:
            class DeformImplicator:
                def getmesh(self, image : Image.Image):
                    width, height = image.size # copying actual image size
                    widthVar, height4 = width//repeaterValue, height//4
                    height34 = 3*height4
                    meshes = [] # stores the co ordiantes
                    for i in range(repeaterValue):
                        firstQuarter = (0 if i%2 == 0 else height4)
                        thirdQuarter = (height34 if i%2 ==0 else height)
                        meshes.append(
                            (
                                (
                                    i*widthVar, 0,
                                    (i+1)*widthVar, height
                                ), # target rect
                                (
                                    i*widthVar, firstQuarter,
                                    i*widthVar, thirdQuarter,
                                    (i+1)*widthVar, thirdQuarter,
                                    (i+1)*widthVar, firstQuarter
                                ) # source rect
                            )
                        )
                    return meshes
            image = ImageOps.deform(image=image, deformer=DeformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    
    def multiply(self, repitaionNumber = 2):
        image = self.image # coping actual image
        try:
            # deformed class
            class DeformImplicator:
                def getmesh(self, img : Image.Image):
                    widthHalf, heightHalf = img.size[0]//2, img.size[1]//2
                    meshes = []
                    for i in range(2):
                        for j in range(2):
                            meshes.append(
                                (
                                    (
                                        i * widthHalf, j * heightHalf,
                                        (i + 1) * widthHalf, (j + 1) * heightHalf
                                    ), # target rectangle
                                    (
                                        0, 0,
                                        0, heightHalf * 2,
                                        widthHalf * 2, heightHalf * 2,
                                        widthHalf * 2, 0
                                    ) # source rectangle
                                )
                            )
                    return meshes
            # main process
            for _ in range(repitaionNumber):
                image = ImageOps.deform(image=image, deformer= DeformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image

    # infiinite layer
    def layerize(self, repeaterValue = 0, padding = 0):
        image = self.image # copying actual image object
        # holding and releasing the repeater value
        if repeaterValue != 0:
            self.layerValue = repeaterValue
        else:
            repeaterValue = self.layerValue
        
        #holding and releasing padding value
        if padding != 0:
            self.paddingValue = padding
        else:
            padding = self.paddingValue

        try:
            class DeformImplicator:
                def getmesh(self, img : Image.Image):
                    width, height = img.size # image width, height 
                    meshes = [] # holds co ordinates
                    for i in range(repeaterValue):
                        pad = padding * i
                        # if i > repeater-1:
                        #     break
                        if width < 2 * pad or height < 2 * pad:
                            break
                        meshes.append(
                            (
                                (
                                    pad, pad,
                                    width - pad, height - pad
                                ), # target rectangle
                                (
                                    0, 0,
                                    0, height,
                                    width, height,
                                    width, 0
                                ) # source rectangle
                            )
                        )
                    return meshes
            image = ImageOps.deform(image=image, deformer=DeformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    
    # chekcer box pattern
    def chess(self, boxGap = 20):
        image = self.image # copying actual image instance
        # procedure
        try:
            columns, rows = image.size[0]//boxGap, image.size[1]//boxGap # row and column
            class DeformImplicator:
                def getmesh(self, img : Image.Image):
                    meshes = []
                    for i in range(columns):
                        for j in range(rows):
                            if i % 2 != 0 or j % 2 != 0:
                                continue
                            meshes.append(
                                (
                                    (
                                        i * boxGap, j * boxGap,
                                        (i+1) * boxGap, (j+1) * boxGap
                                    ), # target rectangle
                                    (
                                        i * boxGap, j * boxGap,
                                        i * boxGap, (j + 1) * boxGap,
                                        (i + 1) * boxGap, (j + 1) * boxGap,
                                         (i+ 1) * boxGap, j * boxGap
                                    ) # source rectangle
                                )
                            )
                    return meshes
            image = ImageOps.deform(image=image, deformer= DeformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    
    # mirror pattern
    def mirrorHalf(self)-> str:
        image = self.image # coping actual image instance
        try:
            class DeformImplicator:
                def getmesh(self, img : Image.Image):
                    width , height = img.size # weight and height
                    widthHalf , heightHalf = width//2, height//2 # half of width and height
                    meshes = [
                        (
                            (
                                0,0,
                                widthHalf, height
                            ), # target rectangle
                            (
                                0, 0,
                                0, height,
                                widthHalf, height,
                                widthHalf, 0  
                            )
                        ),
                        (
                            (
                                widthHalf, 0,
                                width, height
                            ), # target rectangle
                            (
                                widthHalf, 0,
                                widthHalf, height,
                                0, height,
                                0, 0
                            ) # source rectangle
                        )
                    ]
                    return meshes
            image = ImageOps.deform(image=image, deformer=DeformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    
    # mirrorification of the first quardant in 4 parts
    def mirrorQuad(self):
        image = self.image # coping actual image instance
        try:
            class DeformImplicator:
                def getmesh(self, img : Image.Image):
                    width, height = img.size
                    quarterWidth, quarerHeight = width//2, height//2 # quarter half of the width, height
                    meshes = [
                        (
                            (
                                0, 0,
                                quarterWidth, quarerHeight
                            ), # target rectangle
                            (
                                0, 0,
                                0, quarerHeight,
                                quarterWidth, quarerHeight,
                                quarterWidth, 0
                            ) # source rectangle
                        ), # first quardant
                        (
                            (
                                quarterWidth, 0,
                                width, quarerHeight
                            ), # target rectangle
                            (
                                quarterWidth, 0,
                                quarterWidth, quarerHeight,
                                0, quarerHeight,
                                0, 0
                            ) # source rectangle
                        ), # second quarter
                        (
                            (
                                0, quarerHeight,
                                quarterWidth, height
                            ), # target rectangle
                            (
                                0, quarerHeight,
                                0, 0,
                                quarterWidth, 0,
                                quarterWidth, quarerHeight
                            ) # source rectangle
                        ), # third quarter
                        (
                            (
                                quarterWidth, quarerHeight,
                                width, height
                            ), # target rectangle
                            (
                                quarterWidth, quarerHeight,
                                quarterWidth, 0,
                                0, 0,
                                0, quarerHeight
                            ) # source rectangle
                        ) # fourth quarter
                    ]
                    return meshes
            image = ImageOps.deform(image = image, deformer = DeformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    
    # a sinosoidal curve is generated
    def sinCurve(self, cycle = 32):
        image = self.image # copying image object
        halfCycle, quarterHalfCycle = cycle//2, cycle //4
        # procedure
        try:
            image = self.image
            class deformImplicator:
                def getmesh(self, img : Image.Image):
                    width, height = img.size # width and height of the image
                    # width part creates column and heightPart increase the unit height in iteration
                    widthPart , increamentFactor = width//cycle, height//halfCycle
                    # in height = initial height and end height = final height
                    inheight, endHeight = (quarterHalfCycle-1) * increamentFactor, (halfCycle-1) * increamentFactor
                    meshes = [] # holds the co ordinates
                    for i in range(cycle + 1):
                        inheight = inheight + increamentFactor # updates initial height value
                        endHeight = endHeight + increamentFactor # updates final height value
                        meshes.append(
                            (
                                (
                                    i * widthPart, inheight,
                                    (i + 1)* widthPart, endHeight
                                ), # targetRectangle
                                (
                                    i * widthPart, inheight,
                                    i * widthPart, endHeight,
                                    (i + 1) * widthPart, endHeight,
                                    (i + 1) * widthPart, inheight
                                ) # rource rectangle
                            )
                        )
                        if (i % quarterHalfCycle) == 0 :
                            increamentFactor = - increamentFactor
                    return meshes
            image = ImageOps.deform(image= image, deformer= deformImplicator())
        except IOError as ioError:
            return f"{ioError}"
        except MemoryError as memoryError:
            return f"Insufficient Error {memoryError}"
        except ValueError as valueError:
            return f"invalid value {valueError}"
        except ZeroDivisionError as zeroDivisionError:
            return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return self.image
    pass

if __name__ == '__main__':
    imd = ImageDeformer(R"D:\Gallery\PhotoSpace\downloaded pic\wp13349909-aquaman-and-the-lost-kingdom-wallpapers.jpg")
    print(imd.sinCurve())
    imd.image.show()