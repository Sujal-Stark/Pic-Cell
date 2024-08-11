#this file is built to manupulate the different aspects of an image. The core idea is to make differnt image processing customise for user

#used librarries
from PIL import Image, ImageOps, ImageEnhance

#classes
class FrameAdjustment:
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


class FilterImage:
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
            print("Came func")
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
    pass

if __name__ == '__main__':
    #setting a universal imageOject as Null
    universal_image = None

    #create an instance of classes
    frameAdjuster = FrameAdjustment(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    filterImage = FilterImage(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")

    #command List
    print("Command List:\n0--->Save the image\n1--->Open an Image\n2--->Close Image\n3--->Crop Image\n4--->Resize image\n5--->Resample Image\n6--->Rotate an image\n7--->Horizontal Flip\n8--->Vertical Flip\n9---> set Auto Contrast\n10--->GrayScale\n11--->Postarise\n-1--->To stop programme")

    command = int(input("Enter command:\t")) # takes user command

    while(command != -1):
        # save an image
        if command == 0:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)
            
            #image operation
            if frameAdjuster.saveImage():
                print("Saved Successfully!!")
            else:
                print("Error in saving")

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()
        
        #Open an image
        elif command == 1:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            if(frameAdjuster.showImage()):
                print("Image Opened SuccessFully")
            else:
                print("Error Occurred")

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        #close an image
        elif command == 2:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            if frameAdjuster.close():
                print("The file is closed")
            else:
                print("The file is in process")

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        #crop an image
        elif command == 3:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            frameAdjuster.imageCrop()

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        #resize an image
        elif command == 4:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            frameAdjuster.resizeImage()

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        #resample an image
        elif command == 5:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            #store the result declaration
            result = frameAdjuster.changeResampleType()
            if type(result) == str:#print if operaion fail or not initiated
                print(print)
            else:#print if the process is successful
                print("Operation successsful")

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        #rotate an image
        elif command == 6:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            frameAdjuster.imageRotate()

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        # Horizontal Flip
        elif command == 7:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            frameAdjuster.flip_horizontal()

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        # vertical Flip
        elif command == 8:
            # setting the instance variable
            if universal_image != None:
                frameAdjuster.getImageObject(universal_image)

            frameAdjuster.flip_vertical()

            #reassign the universal image object
            universal_image = frameAdjuster.provideImageObject()

        #Set Auto Contrast
        elif command == 9:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)

            if (filterImage.imageAutoContrast()):
                print("Operation completed")
            else:
                print("Operation Failure")

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()

        #colorise image
        elif command == 10:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)

            print(filterImage.grayScaleimage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        #postarise Image
        elif command ==  11:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.postarizeimage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        #no command found
        else:
            print("No command found")

        #command for next operation
        command = int(input("Enter Command:\t"))
        pass