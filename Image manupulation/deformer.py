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
    pass