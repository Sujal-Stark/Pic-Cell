# important libraries
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from fileWindow import FileWindow
from viewerGrid import ViewerGrid

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
        self.imageToShow = None
        self.labelList = []
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
        self.galleryImageViewFrame.setFixedSize(1055,615)

        self.imageGridFrame = QFrame()
        self.imageGridFrame.setFrameShape(QFrame.Shape.Panel)
        # self.imageGridFrame.setFixedSize(250,400)

        self.imageInformationFrame = QFrame()
        self.imageInformationFrame.setFrameShape(QFrame.Shape.Panel)
        # self.imageInformationFrame.setFixedSize(250,200)
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
        return

    def createGalleryLabels(self):
        self.galleryImageLabel = QLabel("Your Image will show up here")
        self.galleryImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.galleryImageLabel.setFixedSize(1000,600)

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
        self.galleryImageView.addWidget(self.galleryImageViewFrame)
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
        if self.imageToShow != None:
            qImageObject = QPixmap(self.imageToShow)
            qImageObject = qImageObject.scaled(self.galleryImageLabel.width(), self.galleryImageLabel.height(), aspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio)
            self.galleryImageLabel.hide()
            self.galleryImageLabel.setPixmap(qImageObject)
            self.galleryImageLabel.show()
        else:
            return
    
    def openImageFromGrid(self):
        self.imageToShow = self.imageGrid.sender().objectName()
        self.openImageInGallery()
        return

    def closeImageFromGallery(self):
        if self.imageToShow != None:
            self.galleryImageLabel.hide()
            self.imageInformationLabel.hide()
            self.emptyImageGrid()

            self.galleryImageLabel.setText("Your Image will show up here")
            self.imageInformationLabel.setText("Image Information")

            self.galleryImageLabel.show()
            self.imageInformationLabel.show()
        return
    
    def emptyImageGrid(self):
        if len(self.labelList) != 0:
            try:
                for labels in self.labelList:
                    self.imageGrid.removeWidget(labels)
                self.labelList.clear()
            except RuntimeError as runTimeError:
                return f"{runTimeError} -> Unable to empty the Image View"

    def loadImageGrid(self, imageFileList:list):
        if len(imageFileList) == 0:
            return
        else:
            self.emptyImageGrid()
            try:
                for row in range((len(imageFileList) // 4)+1):
                    for col in range(4):
                        index = row * 3 + col
                        if index < len(imageFileList):
                            label = QLabel()
                            label.setObjectName(imageFileList[index])
                            self.labelList.append(label)
                            label.setFixedSize(50,50)
                            pixmap = QPixmap(imageFileList[index])
                            pixmap = pixmap.scaled(50,50)
                            label.setPixmap(pixmap)
                            self.imageGrid.addWidget(label, row, col)
                            self.imageGrid.setSpacing(1)
            except IndexError:
                print("Out off index")
            return
    pass

if __name__ == '__main__':
    app = QApplication([])
    galleryWindow = GalleryWindow()
    galleryWindow.show()
    app.exec_()