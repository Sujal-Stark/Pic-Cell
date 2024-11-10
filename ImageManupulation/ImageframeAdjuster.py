#this file is built to manupulate the different aspects of an image. The core idea is to make differnt image processing customise for user

#used librarries
from PIL import Image, ImageOps, ImageFilter

#classes
class FrameAdjustment:
    adjustmentSubEditOption = ["Crop", "Resize", "Resample", "Rotate", "Horizontal Flip", "Vertical Flip"] # editing options available
    subEditingTree = {
        "Crop" : {
            "Custom" : 1, "1:1" : 2, "4:3" : 3, "3:4" : 4, "9:16" : 5, "16:9" : 6
        },
        "Resize" : {
            "Custom" : 1, "1:1" : 2, "4:3" : 3, "3:4" : 4, "16:9" : 5, "9:16" : 6
        },
        "Resample" : {
            "NEAREST" : 1, "BILINEAR" : 2, "BICUBIC" : 3, "LANCZOS" : 4
        },
        "Rotate" : {
            "Custom" : 1, "Left" : 2, "right" : 3
        }, 
        "Horizontal Flip" : {},
        "Vertical Flip" : {}
    }
    
    width = 0
    height = 0
    #interchanges the image with different classes
    def getImageObject(self,image:Image.Image):
        try:
            #the instance variable is set to given image
            self.image = image
            self.width, self.height = self.image.size
        except OSError as osError:
            return f"Cant Open the image -> {osError}"
        except MemoryError as memoryError:
            return f"Can't load the image -> {memoryError}"
        finally:
            return "Succeed"

    #predefined reductions
    #16:9 convention
    def __get16isto9(self)->tuple:
        if self.width != 0 and self.height != 0:
            actualWidth , actualHeight = self.width, self.height
        if (actualWidth/16)>(actualHeight/9):
            reducedWidth,reducedHeight=((actualWidth-(16*(actualHeight/9)))/2),0
        elif (actualWidth/16)<(actualHeight/9):
            reducedWidth,reducedHeight=0,((actualHeight-(9*(actualWidth/16)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #16:9 convention
    def __get9isto16(self)->tuple:
        if self.width != 0 and self.height != 0:
            actualWidth , actualHeight = self.width, self.height
        if (actualWidth/9)>(actualHeight/16):
            reducedWidth,reducedHeight=((actualWidth-(9*(actualHeight/16)))/2),0
        elif (actualWidth/9)<(actualHeight/16):
            reducedWidth,reducedHeight=0,((actualHeight-(16*(actualWidth/9)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #1:1 convention
    def __get1isto1(self)->tuple:
        if self.width != 0 and self.height != 0:
            actualWidth , actualHeight = self.width, self.height
        if (actualWidth>actualHeight):
            reducedWidth,reducedHeight = ((actualWidth-actualHeight)/2),0
        elif actualWidth<actualHeight:
            reducedWidth,reducedHeight = 0,((actualHeight-actualWidth)/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #4:3 convention
    def __get4isto3(self)->tuple:
        if self.width != 0 and self.height != 0:
            actualWidth , actualHeight = self.width, self.height
        if (actualWidth/4)>(actualHeight/3):
            reducedWidth,reducedHeight = ((actualWidth-(4*(actualHeight/3)))/2),0
        elif (actualWidth/4)<(actualHeight/3):
            reducedWidth,reducedHeight = 0,((actualHeight-(3*(actualWidth/4)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #3:4  convention
    def __get3isto4(self)->tuple:
        if self.width != 0 and self.height != 0:
            actualWidth , actualHeight = self.width, self.height
        if ((actualWidth/3)>(actualHeight/4)):
            reducedWidth,reducedHeight = ((actualWidth-(3*(actualHeight/4)))/2),0
        elif (actualWidth/3)<(actualHeight/4):
            reducedWidth,reducedHeight = 0,((actualHeight-(4*(actualWidth/3)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    # resize the image
    def sendCropDimention(self, choice : int)->None:
        if self.width != 0 and self.height != 0:
            width , height = self.width, self.height
        #for 1 : 1 convention
        if choice == 2:
            _size1isto1 = self.__get1isto1()
            width_reduction,height_reduction = _size1isto1
            return (width_reduction,height_reduction,width-width_reduction,height - height_reduction)

        #for 4 : 3 convention
        elif choice == 3:
            _size4isto3 = self.__get4isto3()
            width_reduction,height_reduction = _size4isto3
            return (width_reduction,height_reduction,width-width_reduction,height - height_reduction)
            
        # for 3 : 4 convention
        elif choice == 4:
            _size3isto4 = self.__get3isto4()
            width_reduction,height_reduction = _size3isto4
            return (width_reduction,height_reduction,width-width_reduction,height - height_reduction)

        #for 16:9 convension
        elif choice == 5:
            _size16isto9 = self.__get16isto9()
            width_reduction, height_reduction = _size16isto9
            return (width_reduction,height_reduction,width-width_reduction,height - height_reduction)

            
        #for 9 : 16 convention
        elif choice == 6:
            _size9isto16 = self.__get9isto16()
            width_reduction, height_reduction = _size9isto16
            return (width_reduction,height_reduction,width-width_reduction,height - height_reduction)
    
    def cropImage(self, cropParameter:list):
        if cropParameter[2] <= self.width and cropParameter[3] <= self.height:
            image = self.image
            image = image.crop(cropParameter)
            self.image = image
            return self.image
        else:
            return self.image
    
    #resize the image
    def resizeImage(self, resize_choice :int)->Image.Image:
        image = self.image #local image variable
        width,height = self.image.size
        #1:1 convention
        if resize_choice == 2:
            _resize1isto1 = self.__get1isto1()
            reduced_width,reduced_height  = 2*(int(_resize1isto1[0])),2*(int(_resize1isto1[1]))
            image = self.image.resize((width-reduced_width,height-reduced_height))
            
        # 4:3 convention
        elif resize_choice == 3:
            _resize4isto3 = self.__get4isto3()
            reduced_width,reduced_height = 2*(int(_resize4isto3[0])),2*(int(_resize4isto3[1]))
            image = self.image.resize((width-reduced_width,height-reduced_height))

        # 3:4 convention
        elif resize_choice == 4:
            _resize3isto4 = self.__get3isto4()
            reduced_width,reduced_height = 2*(int(_resize3isto4[0])),2*(int(_resize3isto4[1]))
            image = self.image.resize((width-reduced_width,height-reduced_height))

        # 16:9 convention
        elif resize_choice == 5:
            _resize16isto9 = self.__get16isto9()
            reduced_width,reduced_height = 2*(int(_resize16isto9[0])),2*(int(_resize16isto9[1]))
            image = self.image.resize((width-reduced_width,height-reduced_height))

        # 9:16 convention
        elif resize_choice == 6:
            _resize9isto16 = self.__get9isto16()
            reduced_width,reduced_height = 2*(int(_resize9isto16[0])),2*(int(_resize9isto16[1]))
            image = self.image.resize((width-reduced_width,height-reduced_height))
        
        self.image = image
        return self.image
    
    # change resampling technique
    def changeResampleType(self, resample_choice : int) -> Image.Image:
        image = self.image # copying the original image

        #all possible resampling type is stored here
        resampler = [Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.LANCZOS]

        # user wants to resample
        image=self.image.resize((self.image.size[0],self.image.size[1]),resample= resampler[ resample_choice-1])
        self.image = image
        return self.image

    #rotate an image
    def imageRotate(self, rotationSignal : int = None, rotationAngle : int = None) -> None:
        image = self.image
        angleVal = 0
        if rotationSignal:
            if rotationSignal == 2:
                angleVal = 90
            elif rotationSignal == 3:
                angleVal = -90
        elif rotationAngle:
            angleVal = rotationAngle
        try:
            image = self.image.rotate(angle = angleVal,expand= True)
        except ValueError:
            return "Un matched value"
        except MemoryError:
            return "Unavailable space"

        self.image = image #rotation is finalized
        return self.image

    #flip an image horizontally
    def flip_horizontal(self) -> None:
        try:
            image = ImageOps.mirror(self.image)
        except MemoryError:
            return "Unsufficient Memory"
        except ValueError:
            return "Invalid Type"
        
        self.image = image
        return self.image

    #flips an image vertically
    def flip_vertical(self) -> None:
        try:
            image = ImageOps.flip(self.image)
        except MemoryError:
            return "Unsufficient Memory"
        except ValueError:
            return "Invalid Type"
        
        self.image = image
        return self.image
    
    pass