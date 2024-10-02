from PIL import Image, ImageFilter, ImageOps
class FilterImage:
    filteringOption = ["Auto contrast", "Grey Scale", "Posterize", "Sharpen", "Smoothen", "Contour", "Detail", "Emboss", "Edge Enhance", "Gaussian Blur", "Box Blur", "Unsharp"] # editing options available
    
    #constructor
    def __init__(self,filepath) -> None:
        self.image = Image.open(filepath) # returns the image as iamge_object
        self.image.load()#loads the image in memory
        self.user_message = None # collects generated message for user
        return
    
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
    
    #transmits an image
    def provideImageObject(self) -> Image.Image:
        return self.image
    
    #takes user choice
    def _makeChoice(self,choiceList:list)->int:
        try:
            user_choice = int(input("Enter choice:\t"))
        except ValueError:
            user_choice = 0
        if  user_choice not in choiceList:
            return 0
        else:
            return user_choice

    #manupulates the contrast of the image    
    def imageAutoContrast(self)->bool:
        #creating user message
        self.user_message = "0--->Stop\n1--->Continue\nMore cutOff is more contrast. Auto contrast grayscales your image"
        self.getMessage()

        #creating a copy image
        image = self.image

        #user choice
        user_choice = int(input("Enter Choice:\t"))

        if user_choice not in [0,1]:
            # creates user message
            self.user_message = "Invalid Choice"
            self.getMessage()
            user_choice = int(input("Enter Choice:\t"))

        while user_choice != 0 :
            try:
                image = ImageOps.autocontrast(image.convert('L') ,cutoff= float(input("Enter Cutoff:\t")))
            #handles different exception
            except IOError:
                print("Can't write this image File")
            except ValueError:
                print("Unsupported Cut off")
            except MemoryError:
                print("Memory is insufficient")
            except NotImplementedError:
                print("Operation Not applied")
            finally:
                user_choice = int(input("Enter Choice:\t"))
                if user_choice not in [0,1]:
                    # creates user message
                    self.user_message = "Invalid Choice"
                    self.getMessage()
                    user_choice = int(input("Enter Choice:\t"))

        else: # making the changes permanent
            self.image = image

            return True

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
        else:
            return "Succeed"
    
    #postarize filter
    def postarizeimage(self):
        #copying the image
        image = self.image

        #creates the filter 
        try:
            image = ImageOps.posterize(image=image.convert('RGB'),bits=2)
            #sets the image variable
            self.image = image

        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"
    
    # Gaussian Blur
    def gaussianBlurImage(self):
        #copying instance image
        image = self.image

        #create user message
        self.user_message = "Take value from 0-100"
        self.getMessage()

        #user choice
        blurStrength = (self._makeChoice(list(range(0,101)))/10)

        #preocedure
        try:
            image = image.convert('RGB').filter(ImageFilter.GaussianBlur( radius= blurStrength)) #reduced by the factor 10
            self.image = image
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"    

    def sharpenImage(self):
        # copying instance image 
        image = self.image

        # creating user message
        self.user_message = "Input range from 0 to 10"
        self.getMessage()

        #user choice
        userChoice = self._makeChoice(list(range(0,11)))

        #process
        try:
            for _ in range(userChoice+1):
                image = image.convert('RGB').filter(ImageFilter.SHARPEN())
            
            self.image = image
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"    

    #contour an image
    def contourImage(self):
        #copying the image
        image = self.image

        #process
        try:
            image = image.convert('RGB').filter(ImageFilter.CONTOUR())
            self.image = image
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"
    
    # add detail (constrast + Sharpness)
    def addDetail(self):
        # copying the instance image
        image = self.image
        
        #creating user message
        self.user_message = "Add contrast + sharpness\nInput from 0 to 10"
        self.getMessage()

        #user input
        strenghtChoice = self._makeChoice(list(range(0,11)))

        #process
        try:
            for _ in range(strenghtChoice+1):
                image = image.convert('RGB').filter(ImageFilter.DETAIL())
            self.image = image
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"
    
    #add Smoothness
    def smoothenImage(self):
        # copying the image instance
        image = self.image

        #creating user message
        self.user_message = "Input from 0 to 11"
        self.getMessage()

        #user input
        smoothingChoice = self._makeChoice(list(range(0,11)))

        #process
        try:
            for _ in range(smoothingChoice+1):
                image = image.convert('RGB').filter(ImageFilter.SMOOTH())
            self.image = image
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"
    
    #edge enhance and forced edge enhance
    def ImageEdgeEnhance(self):
        #copying the image
        image = self.image
        
        # creating user message
        self.user_message = "0: Stop.1:Normal Edge Enhance. 2:Maximum Edge Enhance."
        self.getMessage()

        # user choice
        editChoice = self._makeChoice([0,1,2])

        try:
            if editChoice == 1:
                image = image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE())
            elif editChoice == 2:
                image = image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE_MORE())
            
            #reassigning the edited image
            self.image = image

        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"

    # add emboss
    def addEmboss(self):
        # copying the image instance
        image = self.image

        #creating user message
        self.user_message = "Apply specially for lighter images"
        self.getMessage()
        
        #process
        try:
            image = image.convert('RGB').filter(ImageFilter.EMBOSS())
            self.image = image
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"
    
    #box blur effect
    def boxBlurImage(self):
        #creating copy of image
        image = self.image

        # creating user message
        self.user_message = "Each Pixel has the avarage value of it's neighbouring pixel.\nInputs from 0 to 100"
        self.getMessage()

        #user choice
        blurStrength = self._makeChoice(list(range(0,101)))/5

        #process
        try:
            image =image.convert('RGB').filter(ImageFilter.BoxBlur(radius = blurStrength))
            self.image = image
        # excetion handleing
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"

    # unsharp mask
    def imageUnsharpMask(self):
        # copying the image
        image = self.image

        # create user mask
        self.user_message = "Enhance details and increase contrast in photos by making objects more identifiable\nRadius Range:(0-10), Threshold Range:(0-10)"
        self.getMessage()

        # user Choice 
        print("Radius Range:")
        radius_choice = self._makeChoice(list(range(0,11)))

        print("Threshold Range:")
        threshold_choice = self._makeChoice(list(range(0,11)))

        #process
        try:
            image =image.convert('RGB').filter(ImageFilter.UnsharpMask(radius=radius_choice, threshold = threshold_choice))
            self.image = image
        # excetion handleing
        except IOError as ioError:
            return f"Can't write the image file -> {ioError}"
        except MemoryError as memoryError:
            return f"Can't load image file in memory -> {memoryError}"
        except NotImplementedError as notImplementedError:
            return f"Can't Implement the effect -> {notImplementedError}"
        except ValueError as valueError:
            return f"Undefined value -> {valueError}"
        else:
            return "Succeed"
    
    pass
