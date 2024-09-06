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
    pass
imd = ImageDeformer(R"C:\Users\SUJAL KHAN\Downloads\uwp4257296.jpeg")
print(imd.multiply(int(input("Enter how many times you want to repeat:\t"))))
imd.image.show()