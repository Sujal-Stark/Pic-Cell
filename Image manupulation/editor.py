# custom made libraries
from ImageframeAdjuster import FrameAdjustment
from imageColorEnhancer import ColorImage
from imageFiltering import FilterImage
from frameManager import FrameGenerator
from specialFrameGenerator import SpecialFrames
from deformer import ImageDeformer

if __name__ == '__main__':
    #setting a universal imageOject as Null
    universal_image = None

    #create an instance of classes
    frameAdjuster = FrameAdjustment(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    filterImage = FilterImage(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    coloringImage = ColorImage(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    frameGenerator = FrameGenerator(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    specialFrames = SpecialFrames(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")
    imageDeformer = ImageDeformer(R"C:\Users\SUJAL KHAN\Downloads\Avengers.png")

    #command List
    print("Command List:\n0--->Save the image\n1--->Open an Image\n2--->Close Image\n3--->Crop Image\n4--->Resize image\n5--->Resample Image\n6--->Rotate an image\n7--->Horizontal Flip\n8--->Vertical Flip\n9---> set Auto Contrast\n10--->GrayScale\n11--->Postarise\n12--->Gaussian BLur\n13--->Sharp image\n14--->Contour\n15---> Add detail\n16--->Smooth out\n17--->Emboss image\n18--->Edge Enhance\n19--->Box Blur\n20--->Unsharp Mask\n21--->Colorise\n22--->Color Layer\n23---> Add Border\n24 ---> Change Border width\n25 ---> Change border color\n26--->layersREctangle frame\n27---> change color bg,\n28 ---> Deform : Middle Twist, \n29 ---> Deform : double twist\n-1--->To stop programme")

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
        
        #Gaussian Blur
        elif command ==  12:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.gaussianBlurImage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()

        # Sharp Image
        elif command ==  13:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.sharpenImage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        # contour Image
        elif command ==  14:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.contourImage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()

        # Add detail
        elif command ==  15:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.addDetail())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        # Add detail
        elif command ==  16:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.smoothenImage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        # Add Emboss
        elif command ==  17:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.addEmboss())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        # Edge enhancing
        elif command ==  18:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.ImageEdgeEnhance())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()
        
        # Box Blur
        elif command ==  19:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.boxBlurImage())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()

        # Unsharp  Mask
        elif command ==  20:
            # setting the instance variable
            if universal_image != None:
                filterImage.getImageObject(universal_image)
            
            # main effect
            print(filterImage.imageUnsharpMask())

            #reassign the universal image object
            universal_image = filterImage.provideImageObject()

        # coloring an image
        elif command == 21:
            # setting the instance variable
            if universal_image != None:
                coloringImage.getImageObject(universal_image)
            
            # main effect
            print("Modes:\n-1 -> Background, -2 -> Foreground\nChoice:\n0->None, 1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow, 7 -> Orange, 8 -> Purple, 9 -> Pink, 10 -> Brown, 11 -> Olive, 12 -> Navy Blue, 13 -> Teal, 14 -> Lavender, 15 -> Gold, 16 -> Silver")
            print(coloringImage.changeColor(modeChoice=coloringImage._makeChoice([-1,-2]),colorChoice=coloringImage._makeChoice (range(1, 17))-1))

            #reassign the universal image object
            universal_image = coloringImage.provideImageObject()
        
        #color layer
        elif command == 22:
            # setting the instance variable
            if universal_image != None:
                coloringImage.getImageObject(universal_image)
            
            # main effect
            print("1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow, 7 -> Orange, 8 -> Purple, 9 -> Pink, 10 -> Brown, 11 -> Olive, 12 -> Navy Blue, 13 -> Teal, 14 -> Lavender, 15 -> Gold, 16 -> Silver")
            print(coloringImage.addColorLayer(choice=coloringImage._makeChoice(range(1, 17))-1))

            #reassign the universal image object
            universal_image = coloringImage.provideImageObject()
        
        # add border
        elif command == 23:
            # setting the instance variable
            if universal_image != None:
                frameGenerator.getImageObject(universal_image)
            
            # main effect
            print(frameGenerator.addBorder())

            #reassign the universal image object
            universal_image = frameGenerator.provideImageObject()        
        
        # Change border width
        elif command == 24:
            # setting the instance variable
            if universal_image != None:
                frameGenerator.getImageObject(universal_image)
            
            # main effect
            print(frameGenerator.changeWidth(int(input("Enter width:\t"))))

            #reassign the universal image object
            universal_image = frameGenerator.provideImageObject()
        
        # Change border width
        elif command == 25:
            # setting the instance variable
            if universal_image != None:
                frameGenerator.getImageObject(universal_image)
            
            # main effect
            print(frameGenerator.changeColor(int(input("Enter color:\t"))))

            #reassign the universal image object
            universal_image = frameGenerator.provideImageObject()

        # special mask layered rectangle
        elif command == 26:
            # getting most recent edited iamge
            if universal_image != None:
                specialFrames.getImageObject(universal_image)
            
            # main effect
            print("1 -> Rectangle Layer, 2 -> Rombous, 3 -> Ellipse, 4 -> Circle, 5 -> Double Circle, 6 -> Left Diagonal, 7 -> Five Section Rectangle, 8 -> embrald, 9 -> Dead Pool Mask, 10 -> Star mask")
            print(specialFrames.addFrame(int(input("Enter choice:\t"))))

            #reassign the universal image object
            universal_image = specialFrames.provideImageObject()

        # special mask background color change
        elif command == 27:
            # setting the instance variable
            if universal_image != None:
                specialFrames.getImageObject(universal_image)
            
            # main effect
            print("1-> Red,2 -> Green, 3 -> Blue, 4 -> Cyan, 5 -> Magenta, 6 -> Yellow, 7 -> Orange, 8 -> Purple, 9 -> Pink, 10 -> Brown, 11 -> Olive, 12 -> Navy Blue, 13 -> Teal, 14 -> Lavender, 15 -> Gold, 16 -> Silver")
            print(specialFrames.changeAttribute(int(input("Enter choice:\t"))))
            
            #reassign the universal image object
            universal_image = specialFrames.provideImageObject()
        
        # deform fast forward
        elif command == 28:
            # getting most recent edited iamge
            if universal_image != None:
                imageDeformer.getImageObject(universal_image)
            
            # main effect
            print(imageDeformer.middleTwist())

            #reassign the universal image object
            universal_image = imageDeformer.provideImageObject()

        # deform fast forward
        elif command == 29:
            # getting most recent edited iamge
            if universal_image != None:
                imageDeformer.getImageObject(universal_image)
            
            # main effect
            print(imageDeformer.doubleTwisted())

            #reassign the universal image object
            universal_image = imageDeformer.provideImageObject()

        #no command found
        else:
            print("No command found")

        #command for next operation
        command = int(input("Enter Command:\t"))
        pass