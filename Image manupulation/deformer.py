# important inbuilt libraries
from PIL import Image, ImageOps

# class
class ImageDeformer:
    def __init__(self, fileName : str) -> None:
        self.image = Image.open(fileName) # creating image object
        self.userMessage = None # stores message generated by any method
        return
    
    # provides user messege
    def getMessage(self):
        return self.userMessage
    
    # get image object
    def getImageObject(self, image : Image.Image) -> None:
        self.image = image
        return
    
    # set image obejct
    def provideImageObject(self) -> Image.Image:
        return self.image
    
    # looks like iamge is fast forwarded
    def middleTwist(self) -> str:
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
        return "Succeed"
    
    # twist at both quarter half
    def doubleTwisted(self) -> str:
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
        return "Succeed"
    
    # horizontally devides and deviates the image dimentions
    def horizontalSplit(self, repeaterValue = 4) -> str:
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
        return "Succeed"
    pass

    # vertical split
    def verticalSplit(self, repeaterValue = 4) -> str:
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
        return "Succeed"
    
    def multiply(self, repitaionNumber = 0) -> str:
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
        return "Succeed"

    # infiinite layer
    def layerize(self, repeaterValue = 1) -> str:
        image = self.image # copying actual image object
        widthRepeater, heightRepeater = image.size[0]//90, image.size[1]//90
        maxRepeater = widthRepeater if widthRepeater <= heightRepeater else heightRepeater
        # sending user message
        self.userMessage = f"Maximum repitation possible : {maxRepeater}"
        self.getMessage()
        try:
            class DeformImplicator:
                def getmesh(self, img : Image.Image):
                    width, height = img.size # image width, height 
                    meshes = [] # holds co ordinates
                    for i in range(repeaterValue):
                        pad = 45 * i
                        if i > maxRepeater-1:
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
        return "Succeed"
    
    # chekcer box pattern
    def chess(self, boxGap = 20) -> str:
        image = self.image # copying actual image instance
        # creating user message
        self.userMessage = "Box Gap should be greater than 0 and less than 80"
        self.getMessage()
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
        return "Succeed"
    
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
        return "Succeed"
    
    # mirrorification of the first quardant in 4 parts
    def mirrorQuad(self) -> str:
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
        # except ZeroDivisionError as zeroDivisionError:
            # return f"Cant break into more segments {zeroDivisionError}"
        self.image = image
        return "Succeed"
    pass
imd = ImageDeformer(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
print(imd.mirrorQuad())
imd.image.show()