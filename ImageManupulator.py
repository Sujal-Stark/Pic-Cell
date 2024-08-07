#this file is built to manupulate the different aspects of an image. The core idea is to make differnt image processing customise for user

#used librarries
from PIL import Image
from threading import Thread

#classes
class FrameAdjustment:
    #creates a image object and makes it a class attribute
    def __init__(self,image_file) -> None:
        self.image = Image.open(image_file)
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

        #inbuilt sizes
        _size16isto9 = self.__get16isto9()
        _size9isto16 = self.__get9isto16()
        _size1isto1 = self.__get1isto1()
        _size4isto3 = self.__get4isto3()
        _size3isto4 = self.__get3isto4()

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
                width_reduction,height_reduction = _size1isto1
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))

            #for 4 : 3 convention
            elif choice == 3:
                width_reduction,height_reduction = _size4isto3
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))
            
            # for 3 : 4 convention
            elif choice == 4:
                width_reduction,height_reduction = _size3isto4
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))

            #for 16:9 convension
            elif choice == 5:
                width_reduction, height_reduction = _size16isto9
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))
            
            #for 9 : 16 convention
            elif choice == 6:
                width_reduction, height_reduction = _size9isto16
                image = self.image.crop((width_reduction,height_reduction,width-width_reduction,height - height_reduction))
            
            #if no choice works
            else:
                choice = int(input("Enter choice:\t"))
            #choice for next resizement
            choice = int(input("Enter choice:\t"))

        # after all adjustments final iamge is stored as class variable
        self.image = image
        return
    pass

if __name__ == '__main__':
    frameAdjuster = FrameAdjustment(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    print("Command List:\n1--->Open an Image\n2--->Close Image\n3--->Crop Image\n-1To stop programme")
    command = int(input("Enter command:\t"))
    while(command != -1):
        #Open an image
        if command == 1:
            if(frameAdjuster.showImage()):
                print("Image Opened SuccessFully")
            else:
                print("Error Occurred")
        
        #close an image
        elif command == 2:
            if frameAdjuster.close():
                print("The file is closed")
            else:
                print("The file is in process")
        
        #crop an image
        elif command == 3:
            frameAdjuster.imageCrop()
            # frameAdjuster.showImage()
            print(frameAdjuster.image.size)

        #command for next operation
        command = int(input("Enter Command:\t"))
        pass