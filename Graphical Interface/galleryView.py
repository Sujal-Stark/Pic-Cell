# important libraries
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from fileWindow import FileWindow
import os

class GalleryWindow(QWidget):
    def __init__(self)-> None:
        super().__init__()
        self.setGeometry(0,0,600,400)
        self.galleryMasterLayout = QHBoxLayout(self)
        self.galleryWindowProperty()
        self.loadGalleryUI()
        return
    
    def galleryWindowProperty(self):
        self.windowView = FileWindow()
        self.imageToShow = ""
        self.labelList = []
        self.imagePaths = []
        self.currentImageObjectIndex = -1 # helps to shoe all the image in the directory one by one
        self.currentDirectory = ""
        self.bufferDirectory = ""
        self.isGridEmpty = True
        self.signalGenerator = AccessCommunication()
        self.imageLabelList = []
        self.imageNormalSize = (1050,600)
        self.originalSize = (1050, 600)
        return

    def loadGalleryUI(self):
        self.createGalleryLayout()
        self.createGalleryFrames()
        self.createScrollAreaWidgets()
        self.createGalleryLabels()
        self.constructGalleryInterface()
        return

    def createGalleryLayout(self):
        # layouts to show the Selected image
        self.galleryImageView = QVBoxLayout()
        self.galleryInnerImageView = QVBoxLayout()
        # control panel righ side
        self.galleryControlpanel = QVBoxLayout()
        # layout to list other images
        self.gridView = QVBoxLayout()
        # self.innerGridView = QVBoxLayout()
        self.imageGrid = QGridLayout()
        # shows the information about the image
        self.imageInformation = QVBoxLayout()
        self.imageInnerInformation = QVBoxLayout()
        return

    def createGalleryFrames(self):
        self.galleryImageViewFrame = QFrame()
        self.galleryImageViewFrame.setFrameShape(QFrame.Shape.Panel)

        self.imageGridFrame = QFrame()
        self.imageGridFrame.setFrameShape(QFrame.Shape.Panel)

        self.imageInformationFrame = QFrame()
        self.imageInformationFrame.setFrameShape(QFrame.Shape.Panel)
        return
    
    def createScrollAreaWidgets(self):
        self.imageInformationScrollArea = QScrollArea()
        self.imageInformationScrollArea.setWidgetResizable(True)
        self.imageInformationScrollArea.setFixedSize(250, 200)
        self.imageInformationScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageGridScrollArea = QScrollArea()
        self.imageGridScrollArea.setWidgetResizable(True)
        self.imageGridScrollArea.setFixedSize(250, 400)
        self.imageGridScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageViewScrollArea = QScrollArea()
        self.imageViewScrollArea.setWidgetResizable(True)
        self.imageViewScrollArea.setFixedSize(1050,600)
        return

    def createGalleryLabels(self):
        self.galleryImageLabel = QLabel("Your Image will show up here")
        self.galleryImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridViewLabel = QLabel("Other Images")
        self.labelList.append(self.gridViewLabel)
        self.gridViewLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.imageInformationLabel = QLabel("Picture Information")
        self.imageInformationLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        return
    
    def constructGalleryInterface(self):
        # adding in master layout
        self.galleryMasterLayout.addLayout(self.galleryImageView,80)
        self.galleryMasterLayout.addLayout(self.galleryControlpanel,20)
        
        # adding in gallery imageview layout
        self.galleryImageView.addWidget(self.imageViewScrollArea)
        self.imageViewScrollArea.setWidget(self.galleryImageViewFrame)
        self.galleryImageViewFrame.setLayout(self.galleryInnerImageView)

        # adding in gallery control pannel layout
        self.galleryControlpanel.addLayout(self.gridView, 60)
        self.galleryControlpanel.addLayout(self.imageInformation, 40)

        self.gridView.addWidget(self.imageGridScrollArea)
        self.imageGridScrollArea.setWidget(self.imageGridFrame)
        self.imageGridFrame.setLayout(self.imageGrid)
        # self.imageGridFrame.setLayout()

        self.imageInformation.addWidget(self.imageInformationScrollArea)
        self.imageInformationScrollArea.setWidget(self.imageInformationFrame)
        self.imageInformationFrame.setLayout(self.imageInnerInformation)

        self.galleryInnerImageView.addWidget(self.galleryImageLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.imageGrid.addWidget(self.gridViewLabel, 0, 0, alignment = Qt.AlignmentFlag.AlignCenter)
        self.imageInnerInformation.addWidget(self.imageInformationLabel, alignment= Qt.AlignmentFlag.AlignCenter)
        return
    
    def openImageInGallery(self):
        if self.imageToShow != "":
            qImageObject = QPixmap(self.imageToShow)
            qImageObject = qImageObject.scaled(self.imageNormalSize[0], self.imageNormalSize[1], aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio)
            self.galleryImageLabel.hide()
            self.galleryImageLabel.setPixmap(qImageObject)
            self.galleryImageLabel.show()
        else:
            return
    
    def openImageFromGrid(self, imagePathFromGrid:str):
        self.imageToShow = os.path.join(self.currentDirectory,imagePathFromGrid)
        self.imageNormalSize = self.originalSize
        self.openImageInGallery()
        return
    
    def emptyImageGrid(self) -> str:
        if len(self.imageLabelList) != 0:
            try:
                for i in range(self.imageGrid.count()):
                    currentItem = self.imageGrid.takeAt(0)
                    widgetInItem = currentItem.widget()
                    if widgetInItem:
                        widgetInItem.deleteLater()
                self.imageGrid.update()
                otherImagesLabel = QLabel("Other Images")
                otherImagesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.imageGrid.addWidget(otherImagesLabel, 0, 0)
                return "Succeed"
            except RuntimeError as runTimeError:
                return f"{runTimeError} -> Unable to empty the Image View"
        else:
            return "Grid is already Empty"
    
    def createImageLabel(self):
        if len(self.imagePaths) == 0:
            return
        else:
            try:
                self.imageLabelList.clear()
                for imagePath in self.imagePaths:
                    label = ClickableLabel(imagePath)
                    pixmap = QPixmap(imagePath)
                    pixmap = pixmap.scaled(50,50)
                    label.setPixmap(pixmap)
                    label.signalGenerator.mouseCLickSignal.connect(self.openImageFromGrid)
                    self.imageLabelList.append(label)
                return
            except IndexError:
                return 
    
    def loadImageToGrid(self):
        if self.isGridEmpty:
            self.createImageLabel()
            if len(self.imageLabelList) == 0:
                return "No Image to show"
            else:
                self.isGridEmpty = False
                self.signalGenerator.imageReadySignal.emit()
            return "Succeed"
        else:
            self.isGridEmpty = True
            return self.emptyImageGrid()

    def addImagesToGrid(self):
        if self.isGridEmpty:
            self.createImageLabel()
        else:
            self.emptyImageGrid()
        i, j = 0, 0
        for image in self.imageLabelList:
            if j == 6:
                j = 0
                i += 1
            self.imageGrid.addWidget(image, i, j)
            j += 1
        return
    
    def closeImageFromGallery(self):
        if self.imageToShow != None:
            self.galleryImageLabel.hide()
            self.imageInformationLabel.hide()

            self.galleryImageLabel.setText("Your Image will show up here")
            self.imageInformationLabel.setText("Image Information")

            self.galleryImageLabel.show()
            self.imageInformationLabel.show()
            return "Closed Successfully"
    
    # shows the next image Object to the screeen
    def showNextImage(self, imageFileList:list):
        if len(imageFileList) == 0 :
            return "No Image in directory"
        elif self.currentImageObjectIndex == (len(imageFileList)-1):
            return "Last image"
        else:
            try:
                self.currentImageObjectIndex = imageFileList.index(self.imageToShow.split("\\")[-1])
                self.currentImageObjectIndex += 1
                self.imageToShow = imageFileList[self.currentImageObjectIndex]
                self.openImageInGallery()
                return "Succeed"
            except ValueError:
                return "Unable to open This Image"

    # shows the previous image Object to the screeen
    def showPreviousImage(self, imageFileList:list):
        if self.currentImageObjectIndex == 0:
            return "First Image"
        elif len(imageFileList) == 0:
            return "No Image in directory"
        else:
            try:
                self.currentImageObjectIndex = imageFileList.index(self.imageToShow.split("\\")[-1])
                self.currentImageObjectIndex -= 1
                self.imageToShow = imageFileList[self.currentImageObjectIndex]
                self.openImageInGallery()
                return "Succeed"
            except ValueError:
                return "Unable to open This Image"
    
    pass

class ClickableLabel(QLabel):
    def __init__(self, text = ""):
        super().__init__()
        self.signalGenerator = AccessCommunication()
        self.text = text
        return
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.signalGenerator.mouseCLickSignal.emit(self.text)
        return
    pass

class AccessCommunication(QObject):
    imageReadySignal = pyqtSignal()
    mouseCLickSignal = pyqtSignal(str)
    pass

if __name__ == '__main__':
    app = QApplication([])
    galleryWindow = GalleryWindow()
    galleryWindow.show()
    app.exec_()