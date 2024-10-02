#this file is built to manupulate the different aspects of an image. The core idea is to make differnt image processing customise for user

#used librarries
from PIL import Image, ImageOps, ImageFilter

#classes
class FrameAdjustment:
    adjustmentSubEditOption = ["Crop", "Resize", "Resample", "Rotate", "Horizontal Flip", "Vertical Flip"] # editing options available

    #creates a image object and makes it a class attribute
    def __init__(self,image_file) -> None:
        self.image = Image.open(image_file)
        self.image.load() #loads the image in the memory
        self.user_message = None #any info regarding operation will send to main
        return
    
    # shows the image
    def showImage(self)-> bool:
        self.image.show()
        return True
    
    #close the image object
    def close(self)->bool:
        self.image.close()
        return True
    
    #sends user message
    def getMessage(self)->None:
        print(self.user_message)
        self.user_message=None

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

    # save the image with desired extension
    def saveImage(self) -> bool:
        #sending user message
        self.user_message = {0:"Stop",1:'.png',2:'.jpeg',3:'.jpg',4:'.jfif'}
        extensionList = ['.png','.jpeg','.jpg','.jfif']
        self.getMessage()

        #user choice
        extension_choice = int(input("Choose extension:\t"))-1
        new_name = input("Provide name:\t")
        self.image.save(Rf"C:\Users\SUJAL KHAN\Downloads\{new_name}{extensionList[extension_choice]}")
        return True

    #predefined reductions
    #16:9 convention
    def __get16isto9(self)->tuple:
        actualWidth , actualHeight = self.image.size
        if (actualWidth/16)>(actualHeight/9):
            reducedWidth,reducedHeight=((actualWidth-(16*(actualHeight/9)))/2),0
        elif (actualWidth/16)<(actualHeight/9):
            reducedWidth,reducedHeight=0,((actualHeight-(9*(actualWidth/16)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #16:9 convention
    def __get9isto16(self)->tuple:
        actualWidth , actualHeight = self.image.size
        if (actualWidth/9)>(actualHeight/16):
            reducedWidth,reducedHeight=((actualWidth-(9*(actualHeight/16)))/2),0
        elif (actualWidth/9)<(actualHeight/16):
            reducedWidth,reducedHeight=0,((actualHeight-(16*(actualWidth/9)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #1:1 convention
    def __get1isto1(self)->tuple:
        actualWidth , actualHeight = self.image.size
        if (actualWidth>actualHeight):
            reducedWidth,reducedHeight = ((actualWidth-actualHeight)/2),0
        elif actualWidth<actualHeight:
            reducedWidth,reducedHeight = 0,((actualHeight-actualWidth)/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #4:3 convention
    def __get4isto3(self)->tuple:
        actualWidth , actualHeight = self.image.size
        if (actualWidth/4)>(actualHeight/3):
            reducedWidth,reducedHeight = ((actualWidth-(4*(actualHeight/3)))/2),0
        elif (actualWidth/4)<(actualHeight/3):
            reducedWidth,reducedHeight = 0,((actualHeight-(3*(actualWidth/4)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    #3:4  convention
    def __get3isto4(self)->tuple:
        actualWidth , actualHeight = self.image.size
        if ((actualWidth/3)>(actualHeight/4)):
            reducedWidth,reducedHeight = ((actualWidth-(3*(actualHeight/4)))/2),0
        elif (actualWidth/3)<(actualHeight/4):
            reducedWidth,reducedHeight = 0,((actualHeight-(4*(actualWidth/3)))/2)
        else:
            reducedWidth,reducedHeight = 0,0
        return (reducedWidth,reducedHeight)
    
    # resize the image 
    def imageCrop(self)->None:
        # actual image size
        width,height = self.image.size

        #create message
        self.user_message = {0:"Stop",1:"Custom size", 2:"1:1",3:"4:3",4:"3:4",5:"16:9",6:"9:16"}
        self.getMessage()

        #user choice
        choice = int(input("Enter choice:\t"))
        while choice != 0:
            #for custom input
            if choice == 1:
                horizontal_shift = int(input("Horizontal shift:\t"))
                vertical_shift = int(input("Vertical shift:\t"))
                
                if horizontal_shift >width or vertical_shift > height:
                    horizontal_shift,vertical_shift = width,height
                
                image = self.image.crop((horizontal_shift,vertical_shift,width-horizontal_shift, height-vertical_shift))
            
            #for 1 : 1 convention
            elif choice == 2:
                _size1isto1 = self.__get1isto1()
                width_reduction,height_reduction = _size1isto1
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))

            #for 4 : 3 convention
            elif choice == 3:
                _size4isto3 = self.__get4isto3()
                width_reduction,height_reduction = _size4isto3
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))
            
            # for 3 : 4 convention
            elif choice == 4:
                _size3isto4 = self.__get3isto4()
                width_reduction,height_reduction = _size3isto4
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))

            #for 16:9 convension
            elif choice == 5:
                _size16isto9 = self.__get16isto9()
                width_reduction, height_reduction = _size16isto9
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height -height_reduction))
            
            #for 9 : 16 convention
            elif choice == 6:
                _size9isto16 = self.__get9isto16()
                width_reduction, height_reduction = _size9isto16
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))
            
            #if no choice works
            else:
                print("Incorrect Choice")

            #choice for next resizement
            choice = int(input("Enter choice:\t"))

        # after all adjustments final iamge is stored as class variable
        self.image = image
        return
    
    #resize the image
    def resizeImage(self)->None:
        image = None #local image variable
        width,height = self.image.size
        #creating user message
        self.user_message = {0:"Stop",1:"Custom size",2:"1:1",3:"4:3",4:"3:4",5:"16:9",6:"9:16"}
        self.getMessage()
        
        #user choice
        resize_choice = int(input("Enter Choice:\t"))

        while resize_choice != 0:
            #custom resize
            if resize_choice == 1:
                image = self.image.resize((int(input("Enter Width:\t")),int(input("Enter height:\t"))))
            
            #1:1 convention
            elif resize_choice == 2:
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

            #for uncorrect choice
            else:
                print("Incorrect choice")
            
            #choice for next resize
            resize_choice = int(input("Enter Choice:\t"))

        #finalizing cahnges
        self.image = image
        return
    
    # change resampling technique
    def changeResampleType(self):
        #create message
        self.user_message = {0:"none",1:"nearest",2:"BILINEAR",3:"BICUBIC",4:"LANCZOS"}
        self.getMessage()

        #all possible resampling type is stored here
        resampler = [Image.NEAREST, Image.BILINEAR, Image.BICUBIC, Image.LANCZOS]

        #user choice
        resample_choice = int(input("Enter choice:\t"))

        #if user dont want change the resample type
        if resample_choice == 0:
            return "No change is made"
        # user wants to resample
        elif resample_choice <= 4 and resample_choice > 0:
            self.image=self.image.resize((self.image.size[0],self.image.size[1]),resample= resampler[ resample_choice-1])
        #if no choice matches
        else:
            return "No similer option"

    #rotate an image
    def imageRotate(self) -> None:
        flag = 1 # helps to re rotate everytime
        image = self.image

        #create message
        self.user_message = {1:"continue",0:"Stop"}
        self.getMessage()

        while flag != 0:
            #rotation process
            image = self.image.rotate(float(input("Enter rotation angle:\t")),expand= True)
            flag = int(input("Rotation flag status:\t"))
        
        self.image = image #rotation is finalized
        return

    #flip an image horizontally
    def flip_horizontal(self) -> None:
        flag = 1 #helps to flip multiple time
        image = self.image

        #create message
        self.user_message = {1:"continue",0:"Stop"}
        self.getMessage()

        while flag != 0:
            #flip process
            image = ImageOps.mirror(self.image)
            print("Flip Successful.....") #message to user
            flag = int(input("Rotation flag status:\t")) #re assign user action request

        self.image = image
        return

    #flips an image vertically
    def flip_vertical(self) -> None:
        flag = 1 #helps to flip multiple time
        image = self.image

        #create message
        self.user_message = {1:"continue",0:"Stop"}
        self.getMessage()

        while flag != 0 :
            image = ImageOps.flip(self.image)
            print("Flip Successful.....") #message to user
            flag = int(input("Rotation flag status:\t")) #re assign user action request
        
        self.image = image
        return
    
    pass