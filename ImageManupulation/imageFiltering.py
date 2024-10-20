from PIL import Image, ImageFilter, ImageOps
class FilterImage:
    filteringOption = ["Auto contrast", "Grey Scale", "Posterize", "Sharpen", "Smoothen", "Contour", "Detail", "Emboss", "Edge Enhance", "Gaussian Blur", "Box Blur", "Unsharp"] # editing options available
    
    subEditingTree = {
        "Auto contrast" : {
            "Intensity" : {"minVal" : 0, "maxVal" : 50, "currentPosition" : 0, "change" : 1}
        },
        "Grey Scale" : {},
        "Posterize" : {},
        "Gaussian Blur" : {
            "Blur Strength" : {"minVal" : 0, "maxVal" : 100, "currentPosition" : 0, "change" : 1}
        },
        "Edge Enhance" : {"Edge Enhance" : 1 , "Maximum Edge Enhance" : 2},
        "Sharpen" : {
            "Sharp Value" : {"minVal" : 0, "maxVal" : 10, "currentPosition" : 0, "change" : 1}
        }, 
        "Contour" : {},
        "Detail" : {
            "Intensity" : {"minVal" : 0, "maxVal" : 10, "currentPosition" : 0, "change" : 1}
        },
        "Smoothen" : {
            "Intensity" : {"minVal" : 0, "maxVal" : 10, "currentPosition" : 0, "change" : 1}
        },
        "Emboss" : {},
        "Box Blur" : {
            "Blur Strength" : {"minVal" : 0, "maxVal" : 100, "currentPosition" : 0, "change" : 1}
        },
        "Unsharp" : {
            "radius" : {"minVal" : 0, "maxVal" : 10, "currentPosition" : 0, "change" : 1},
            "Threshold" : {"minVal" : 0, "maxVal" : 10, "currentPosition" : 0, "change" : 1}
        }
    }    
    #sends user message
    def getMessage(self)->None:
        print(self.user_message)
        self.user_message=None # sets user message to null for next message
        return

    #interchanges the image with different classes
    def getImageObject(self,image:Image.Image):
        try:
            #the instance variable is set to given image
            self.image = image
        except OSError as osError:
            return f"Cant Open the image -> {osError}"
        except MemoryError as memoryError:
            return f"Can't load the image -> {memoryError}"
        finally:
            return "Succeed"

    #manupulates the contrast of the image    
    def imageAutoContrast(self, cutoffValue : float)->bool:
        #creating a copy image
        image = self.image

        try:
            image = ImageOps.autocontrast(image.convert('L') ,cutoff= cutoffValue)
        #handles different exception
        except IOError:
            print("Can't write this image File")
        except ValueError:
            print("Unsupported Cut off")
        except MemoryError:
            print("Memory is insufficient")
        except NotImplementedError:
            print("Operation Not applied")
        else:
            self.image = image
            return self.image

    #gray scale image
    def grayScaleimage(self):
        # copying the image
        image = self.image

        #creates the grayscale image
        try:
            image = ImageOps.grayscale(image=image)
            # resets the image
            self.image = image
        except IOError as ioError:
            return f"Unable to Write the file -> {ioError}"
        except NotImplementedError as notImplementedError:
            return f"Unable to perform the action because -> {notImplementedError}"
        
        return self.image
    
    #postarize filter
    def postarizeimage(self):
        #copying the image
        image = self.image

        #creates the filter 
        try:
            image = ImageOps.posterize(image=image.convert('RGB'),bits=2)
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        
        self.image = image
        return self.image
    
    # Gaussian Blur
    def gaussianBlurImage(self, blurStrength):
        #copying instance image
        image = self.image

        #preocedure
        try:
            image = image.convert('RGB').filter(ImageFilter.GaussianBlur(radius= blurStrength/10)) #reduced by the factor 10
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        
        self.image = image
        return self.image

    def sharpenImage(self, sharpValue : int):
        # copying instance image 
        image = self.image

        #process
        try:
            for _ in range(sharpValue+1):
                image = image.convert('RGB').filter(ImageFilter.SHARPEN())
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"

        self.image = image
        return self.image

    #contour an image
    def contourImage(self):
        #copying the image
        image = self.image

        #process
        try:
            image = image.convert('RGB').filter(ImageFilter.CONTOUR())
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        self.image = image
        return self.image
    
    # add detail (constrast + Sharpness)
    def addDetail(self, strenghtChoice : int):
        # copying the instance image
        image = self.image

        #process
        try:
            for _ in range(strenghtChoice+1):
                image = image.convert('RGB').filter(ImageFilter.DETAIL())
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        self.image = image
        return self.image
    
    #add Smoothness
    def smoothenImage(self, smoothingChoice : int):
        # copying the image instance
        image = self.image

        #process
        try:
            for _ in range(smoothingChoice+1):
                image = image.convert('RGB').filter(ImageFilter.SMOOTH())
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        self.image = image
        return self.image
    
    #edge enhance and forced edge enhance
    def ImageEdgeEnhance(self, editChoice : int):
        #copying the image
        image = self.image
        try:
            if editChoice == 1:
                image = image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE())
            elif editChoice == 2:
                image = image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE_MORE())
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        #reassigning the edited image
        self.image = image
        return self.image

    # add emboss
    def addEmboss(self):
        # copying the image instance
        image = self.image

        #process
        try:
            image = image.convert('RGB').filter(ImageFilter.EMBOSS())
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        self.image = image
        return self.image
    
    #box blur effect
    def boxBlurImage(self , blurStrength : int):
        #creating copy of image
        image = self.image

        #process
        try:
            image =image.convert('RGB').filter(ImageFilter.BoxBlur(radius = blurStrength/5))
        # excetion handleing
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        self.image = image
        return self.image

    # unsharp mask
    def imageUnsharpMask(self, radius_choice : int = 0, threshold_choice : int = 0):
        # copying the image
        image = self.image

        #process
        try:
            image =image.convert('RGB').filter(ImageFilter.UnsharpMask(radius=radius_choice, threshold = threshold_choice))
        # excetion handleing
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        self.image = image
        return self.image
    
    pass