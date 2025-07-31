# important libraries
from operator import truediv

from PIL.ImageChops import constant
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QScrollArea,
                             QTableWidget, QTableWidgetItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtGui import QPixmap, QFont
from icecream import ic
import os

# custom Import
from fileWindow import FileWindow
from ImageFileLoaderClass import ImageFileLoader
import Constants

class GalleryWindow(QWidget):
    # Threads
    imageClassLoaderThread : ImageFileLoader =  None # populate the image grid

    def __init__(self)-> None:
        super().__init__()
        self.galleryMasterLayout = QHBoxLayout(self)
        self.galleryWindowProperty()
        qss = self.readQssFile(Constants.GALLERY_UI_STYLE_FILE)
        if qss != "": self.setStyleSheet(qss)
        self.loadGalleryUI()
        return
    
    def galleryWindowProperty(self):
        self.windowView = FileWindow()
        self.dimention = [self.height(), self.height()]
        self.imageToShow : str = ""
        self.imagePaths = []
        self.currentImageObjectIndex = -1 # helps to shoe all the image in the directory one by one
        self.currentDirectory = ""
        self.bufferDirectory = ""
        self.signalGenerator = AccessCommunication() # contains all pyqtSignal
        self.imageNormalSize = (1050,600)
        self.originalSize = (1050, 600)
        self.comicSansFontLarger = QFont(Constants.FONT_COMIC_SANS_MS, 16)
        self.comicSansFont = QFont(Constants.FONT_COMIC_SANS_MS, 12)
        self.gridBusy = False # stops multiple times over loading of grid 
        return

    def loadGalleryUI(self):
        self.createGalleryLabels()
        self.createGalleryLayout()
        self.createGalleryFrames()
        self.createTableWidget()
        self.createScrollAreaWidgets()
        self.constructGalleryInterface()
        return

    def createGalleryLayout(self):
        # layouts to show the Selected image
        self.galleryImageView = QVBoxLayout()
        self.galleryInnerImageView = QVBoxLayout()

        # control panel right side
        self.galleryControlpanel = QVBoxLayout()

        # layout to list other images
        self.gridView = QVBoxLayout()
        self.innerGridView = QVBoxLayout()
        self.gridScrollHolder = QVBoxLayout()
        self.imageTableGridHolder = QGridLayout()

        # shows the information about the image
        self.imageInformation = QVBoxLayout()
        self.imageInnerInformation = QVBoxLayout()
        return

    def createGalleryFrames(self):
        self.galleryImageViewFrame = QFrame()
        self.galleryImageViewFrame.setFrameShape(QFrame.NoFrame)
        self.galleryImageViewFrame.setStyleSheet("border: none;")

        self.grid_label_frame = QFrame()
        self.grid_label_frame.setFrameShape(QFrame.Shape.Panel)

        self.imageGridFrame = QFrame()
        self.imageGridFrame.setFrameShape(QFrame.Shape.Panel)

        self.imageGridInnerFrame = QFrame()
        self.imageGridInnerFrame.setFrameShape(QFrame.NoFrame)
        self.imageGridInnerFrame.setStyleSheet("border: none;")

        self.imageInformationFrame = QFrame()
        self.imageInformationFrame.setFrameShape(QFrame.NoFrame)
        self.imageInformationFrame.setStyleSheet("border: none;")
        return
    
    def createScrollAreaWidgets(self):
        self.imageInformationScrollArea = QScrollArea()
        self.imageInformationScrollArea.setWidgetResizable(True)
        self.imageInformationScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageGridScrollArea = QScrollArea()
        self.imageGridScrollArea.setWidgetResizable(True)
        self.imageGridScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageViewScrollArea = QScrollArea()
        self.imageViewScrollArea.setWidgetResizable(True)
        return

    def createGalleryLabels(self):
        self.galleryImageLabel = QLabel("Your Image will show up here")
        self.galleryImageLabel.setFixedSize(200, 40)
        self.galleryImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.galleryImageLabel.setFont(self.comicSansFont)

        self.gridViewLabel = QLabel("Other Images")
        self.gridViewLabel.setFixedSize(
            int(self.dimention[0]  * Constants.GRID_PANEL_WIDTH_PERCENTAGE),
            Constants.GRID_VIEW_LABEL_HEIGHT
        )
        self.gridViewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridViewLabel.setFont(self.comicSansFont)

        self.imageInformationLabel = QLabel("Picture Information")
        self.imageInformationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageInformationLabel.setFont(self.comicSansFont)
        return

    def createTableWidget(self) -> None:
        self.imageGrid = QTableWidget()
        self.imageGrid.setRowCount(0)
        self.imageGrid.setColumnCount(4)
        self.imageGrid.verticalHeader().setVisible(False)
        self.imageGrid.horizontalHeader().setVisible(False)
        for i in range(4):
            self.imageGrid.setColumnWidth(i, 80)
        return
    def constructGalleryInterface(self) -> None:
        # adding in master layout
        self.galleryMasterLayout.addLayout(self.galleryImageView,80)
        self.galleryMasterLayout.addLayout(self.galleryControlpanel,20)
        
        # adding in gallery imageview layout
        self.galleryImageView.addWidget(self.imageViewScrollArea)
        self.imageViewScrollArea.setWidget(self.galleryImageViewFrame)
        self.galleryImageViewFrame.setLayout(self.galleryInnerImageView)

        # adding in gallery control panel layout
        self.galleryControlpanel.addLayout(self.gridView, 60)
        self.galleryControlpanel.addLayout(self.imageInformation, 40)

        self.gridView.addWidget(self.grid_label_frame)
        self.grid_label_frame.setLayout(self.innerGridView)
        self.innerGridView.addWidget(self.gridViewLabel, 10, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerGridView.addLayout(self.gridScrollHolder, 90)
        self.gridScrollHolder.addWidget(self.imageGridScrollArea, alignment=Qt.AlignmentFlag.AlignCenter)
        self.imageGridScrollArea.setWidget(self.imageGridInnerFrame)
        self.imageGridInnerFrame.setLayout(self.imageTableGridHolder)
        self.imageTableGridHolder.addWidget(self.imageGrid)

        self.imageInformation.addWidget(self.imageInformationScrollArea)
        self.imageInformationScrollArea.setWidget(self.imageInformationFrame)
        self.imageInformationFrame.setLayout(self.imageInnerInformation)

        self.galleryInnerImageView.addWidget(self.galleryImageLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        self.imageInnerInformation.addWidget(self.imageInformationLabel, alignment= Qt.AlignmentFlag.AlignCenter)
        return

    def readQssFile(self, qssFile):
        try:
            with open(qssFile, 'r') as file:
                return file.read()
        except (PermissionError, FileNotFoundError, MemoryError, InterruptedError):
            return ""

    ############################################# INTERFACING ##########################################
    def resizeEvent(self, a0):
        currWidth, currHeight = self.width(), self.height()
        self.gridViewLabel.setFixedWidth(int(currWidth * Constants.GRID_PANEL_WIDTH_PERCENTAGE))

        self.imageGridScrollArea.setFixedSize(
            int(currWidth * Constants.GRID_PANEL_WIDTH_PERCENTAGE),
            int(currHeight * Constants.GRID_PANEL_HEIGHT_PERCENTAGE) - 60
        )

        self.imageGridInnerFrame.resize(
            int(currWidth * Constants.GRID_PANEL_WIDTH_PERCENTAGE),
            int(currHeight * Constants.GRID_PANEL_HEIGHT_PERCENTAGE)
        )
        super().resizeEvent(a0)
        return

    def setGridBusy(self) -> None:
        # when ImageFileLoader Thread completes it's action this method is called to set
        # gridBusy Status to be true
        self.gridBusy = True # so that no element can occupy the grid
        return

    def openImageInGallery(self) -> str | None:
        if self.imageToShow != "":
            qImageObject = QPixmap(self.imageToShow)
            qImageObject = qImageObject.scaled(
                int(self.imageNormalSize[0]), int(self.imageNormalSize[1]),
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio
            )
            self.galleryImageLabel.hide()
            self.galleryImageLabel.setFixedSize(qImageObject.width(), qImageObject.height())
            self.galleryImageLabel.setPixmap(qImageObject)
            self.galleryImageLabel.show()
            return Constants.IMAGE_OPENED_MESSAGE
        else: return None
    
    def openImageFromGrid(self, imagePathFromGrid:str) -> None:
        """
            :param imagePathFromGrid: take the absolute path of the image Given and call
            openImageGallery() method to open that image in Application
            :return: -> None
        """
        self.imageToShow = imagePathFromGrid
        self.imageNormalSize = self.originalSize
        self.openImageInGallery()
        return
    
    def emptyImageGrid(self) -> str:
        """
            Clear all the table item if there is any, and set the gridBusy Parameter to be True
            :return: String as operation output
        """
        if len(self.imagePaths) != 0:
            try:
                self.imageGrid.setRowCount(0) # grid become empty
                self.imageGrid.update() # update the change
                self.gridBusy = False # to Ensure next time images can load
                return "Succeed"
            except RuntimeError: return "Unable to empty the Image View"
        else: return "Grid is Empty"

    def createImageLabel(self) -> None:
        """
            Starts a Thread to load images in the Grid and set row cound
            :return: None
        """
        if len(self.imagePaths) > 0:
            try:
                self.imageGrid.setRowCount((len(self.imagePaths) // 4) + 1) # analyze required Rows
                self.imageClassLoaderThread = ImageFileLoader(imagePaths=self.imagePaths)

                # signal Connection
                self.imageClassLoaderThread.imageObjectReady.connect(self.addImagesToGrid)
                self.imageClassLoaderThread.operationDone.connect(self.setGridBusy)
                self.imageClassLoaderThread.start() # starting Thread
                return None
            except (OSError, RuntimeError, AttributeError): return None
        else: return None

    # call from MasterGraphicalInterface
    def loadImageToGrid(self) -> None:
        """
            Either populate the ImageGrid or Empty the ImageGrid
            :return: None
        """
        if self.gridBusy: self.emptyImageGrid() # empty
        else: self.createImageLabel() # populate
        return None


    def addImagesToGrid(self, row : int, col: int, path : str) -> None:
        """
            Takes parameter from Thread Signal and populate the Grid with image and Coordinates
            :param row: Position in Row
            :param col: Position in column
            :param path: The absolute Image path
            :return: None
        """
        try:
            label = ClickableLabel(path)
            label.setPixmap(
                QPixmap(path).scaled(Constants.GRID_IMAGE_WIDTH, Constants.GRID_IMAGE_WIDTH)
            )
            self.imageGrid.setRowHeight(row, Constants.GRID_IMAGE_WIDTH)
            self.imageGrid.setCellWidget(row, col, label)
            self.imageGrid.update()
            label.show()
            label.signalGenerator.mouseCLickSignal.connect(self.openImageFromGrid)
        except (OSError, TypeError, AttributeError, ValueError, FileNotFoundError): print("Error Occurred")
        return
    
    def closeImageFromGallery(self):
        if self.imageToShow is not None:
            self.emptyImageGrid() # if grid image is present, empty it
            self.galleryImageLabel.hide()
            self.imageInformationLabel.hide()

            self.galleryImageLabel.setFixedSize(200,40)
            self.galleryImageLabel.setText("Your Image will show up here")
            self.imageInformationLabel.setText("Image Information")

            self.galleryImageLabel.show()
            self.imageInformationLabel.show()
            return "Closed Successfully"
        return None

    # shows the next image Object to the screen
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

    # shows the previous image Object to the screen
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

class AccessCommunication(QObject):
    mouseCLickSignal = pyqtSignal(str)
    pass


class ClickableLabel(QLabel):
    def __init__(self, text=""):
        super().__init__()
        self.signalGenerator = AccessCommunication()
        self.setFixedSize(80, 80)
        self.text = text
        return

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.signalGenerator.mouseCLickSignal.emit(self.text)
        return

    pass

if __name__ == '__main__':
    app = QApplication([])
    galleryWindow = GalleryWindow()
    galleryWindow.show()
    app.exec_()