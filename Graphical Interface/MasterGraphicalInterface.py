# libraries
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
QPushButton, QLabel, QFrame, QMenuBar, QMenu, QAction, QShortcut)
from PyQt5.QtCore import Qt
from galleryView import GalleryWindow
from fileWindow import FileWindow
from threading import Thread
from editManager import EditingActionManager
from PyQt5.QtGui import QFont, QIcon
from icecream import ic
import os

class MasterWindow(QMainWindow):
    def __init__(self)-> None:
        super().__init__()
        
        self.setWindowTitle("Pic_Cell")
        self.setGeometry(0,0,800,600)
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.masterLayout = QVBoxLayout(self.mainWidget)
        self.setWindowIcon(QIcon("./static/Icon_Pic_Cell.png"))
        self.assignProperties()
        self.LoadUI()
        self.eventManager()
        self.addStyledSheet()
        self.show()
        return
    
    def LoadUI(self):
        self.createMenubar()
        self.createButtons()
        self.createLabels()
        self.createLayouts()
        self.createFrames()
        self.createTabs()
        self.construct()
        self.controlKeys()
        return
    
    def controlKeys(self):
        self.pressKeyToNextImage = QShortcut(Qt.Key.Key_Right, self)
        self.pressKeyToPreviousImage = QShortcut(Qt.Key.Key_Left, self)
        return
    
    def eventManager(self):
        self.newFileWindow.fileOpenButton.clicked.connect(self.openImageFromMainWindow)
        self.openFile.triggered.connect(self.createSeondWindow)
        self.closeFile.triggered.connect(self.closeImageObject)
        self.loadOtherImages.triggered.connect(self.connectImageGridWithFiles)
        self.saveImage.triggered.connect(self.tab2.saveImageInMachine)

        self.newFileWindow.fileListWidget.currentItemChanged.connect(self.newFileWindow.fileAccess)
        self.pressKeyToNextImage.activated.connect(self.openNextImageInGallery)
        self.pressKeyToPreviousImage.activated.connect(self.openPreviousImageInGallery)
        self.tab1.signalGenerator.imageReadySignal.connect(self.showGridObjects)
        self.zoomInOption.triggered.connect(self.scaleUPImage)
        self.zoomOutOption.triggered.connect(self.scaleDownImage)
        self.OriginalSize.triggered.connect(self.originalScale)
        self.toggleHideLeftBar.triggered.connect(self.tab2.toggleHideLeft)

        self.undoMethod.triggered.connect(self.tab2.undoOperation)
        self.redoMethod.triggered.connect(self.tab2.redoOperation)
        return
    
    def assignProperties(self):
        self.newFileWindow = FileWindow()
        self.outputInfo = ""
        self.comicSansFontLarger = QFont("Comic Sans MS", 16)
        self.comicSansFont = QFont("Comic Sans MS", 12)
        return
    
    
    def createMenubar(self):
        self.bar = QMenuBar(self)
        self.fileMenu = QMenu("File")
        self.fileMenu.setStyleSheet(
            """
                QMenu {
                    background-color : #2d0273;
                    font-size: 14px;
                    color: #ffffff;
                    padding : 2px;
                    border-radius : 10px;
                }
                QMenu::item:selected {
                    background-color: #4a90e2;
                    color: black
                }
                QMenu::separator {
                    height: 1px;
                    background: #5a5a5a;
                    margin: 5px;
                }
            """
        )
        self.fileMenu.setFont(self.comicSansFont)
        self.editMenu = QMenu("Edit")
        self.editMenu.setStyleSheet(
            """
                QMenu {
                    background-color : #2d0273;
                    font-size: 14px;
                    color: #ffffff;
                    padding : 2px;
                    border-radius : 10px;
                }
                QMenu::item:selected {
                    background-color: #4a90e2;
                    color: black
                }
                QMenu::separator {
                    height: 1px;
                    background: #5a5a5a;
                    margin: 5px;
                }
            """
        )
        self.editMenu.setFont(self.comicSansFont)
        self.viewMenu = QMenu("View")
        self.viewMenu.setStyleSheet(
            """
                QMenu {
                    background-color : #2d0273;
                    font-size: 14px;
                    color: #ffffff;
                    padding : 2px;
                    border-radius : 10px;
                }
                QMenu::item:selected {
                    background-color: #4a90e2;
                    color: black
                }
                QMenu::separator {
                    height: 1px;
                    background: #5a5a5a;
                    margin: 5px;
                }
            """
        )
        self.viewMenu.setFont(self.comicSansFont)
        self.bar.addMenu(self.fileMenu)
        self.bar.addMenu(self.editMenu)
        self.bar.addMenu(self.viewMenu)

        self.openFile = QAction("Open", self)
        self.openFile.setShortcut("ctrl+o")
        
        self.closeFile = QAction("Close", self)
        self.closeFile.setShortcut("ctrl+w")
        self.loadOtherImages = QAction("Load Other Images", self)
        self.loadOtherImages.setShortcut("ctrl+i")
        self.saveImage = QAction("Save", self)
        self.saveImage.setShortcut("ctrl+s")

        self.fileMenu.addActions([self.openFile, self.closeFile])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.loadOtherImages)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveImage)

        self.undoMethod = QAction("Undo", self)
        self.undoMethod.setShortcut("ctrl+z")
        self.redoMethod = QAction("Redo", self)
        self.redoMethod.setShortcut("ctrl+y")

        self.editMenu.addActions([self.undoMethod, self.redoMethod])

        self.zoomInOption = QAction("Zoom In", self)
        self.zoomInOption.setShortcut("ctrl+b")
        self.zoomOutOption = QAction("Zoom Out", self)
        self.zoomOutOption.setShortcut("ctrl+l")
        self.OriginalSize = QAction("original Size",self)
        self.OriginalSize.setShortcut("ctrl+.")
        self.theme = QAction("toggle Theme", self)
        self.theme.setCheckable(True)
        self.theme.setChecked(True)
        self.toggleHideLeftBar = QAction("Hide left bar(Toggle)", self)
        self.toggleHideLeftBar.setShortcut(Qt.Key.Key_F1)
        
        self.viewMenu.addActions([self.zoomInOption, self.zoomOutOption])
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.OriginalSize)
        self.viewMenu.addSeparator()
        self.viewMenu.addActions([self.theme, self.toggleHideLeftBar])
        self.setMenuBar(self.bar)
        return
    
    def createButtons(self):
        # self.fileButton = QPushButton("File Access")
        # self.editButton = QPushButton("Edit File")
        return
    
    def createLabels(self):
        self.methodInfo = QLabel("Any information about the any proecss will show up here")
        return
    
    def createFrames(self):
        self.midbodyFrame = QFrame()
        
        self.footerFrame = QFrame()
        self.footerFrame.setFrameShape(QFrame.Shape.Panel)
        self.footerFrame.setLineWidth(2)
        return
    
    def createLayouts(self):
        self.midbody = QHBoxLayout()

        self.outerFooter = QHBoxLayout()
        self.innerFooter = QHBoxLayout()
        return
    
    def createTabs(self):
        self.tabScreen = QTabWidget()

        self.tab1 = GalleryWindow()
        self.tab2 = EditingActionManager()

        self.tabScreen.addTab(self.tab1, "Gallery")
        self.tabScreen.addTab(self.tab2, "Edit Section")
        return
    
    def construct(self):
        self.masterLayout.addLayout(self.midbody,95)
        self.masterLayout.addLayout(self.outerFooter,5)

        self.midbody.addWidget(self.tabScreen)

        self.outerFooter.addWidget(self.footerFrame)
        self.footerFrame.setLayout(self.innerFooter)

        self.innerFooter.addWidget(self.methodInfo, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
    def createSeondWindow(self):
        if self.tabScreen.currentIndex() == 0:
            self.newFileWindow.setFixedSize(400,300)
            self.newFileWindow.removeImageHolderLayout()
            self.newFileWindow.show()
        elif self.tabScreen.currentIndex() == 1:
            self.newFileWindow.setFixedSize(600,300)
            self.newFileWindow.addImageHolderLayout()
            self.newFileWindow.show()
        return
    
    def openImageFromMainWindow(self):
        if self.tabScreen.currentIndex() == 0:
            self.openGalleryImage()
        elif self.tabScreen.currentIndex() == 1:
            self.openEditSectionImage()

    def closeImageObject(self):
        if self.tabScreen.currentIndex() == 0:
            self.outputInfo = self.tab1.closeImageFromGallery()
        elif self.tabScreen.currentIndex() == 1:
            self.outputInfo = self.tab2.closeImageInEditSection()
        self.methodInfo.setText(self.outputInfo)

    def connectImageGridWithFiles(self):
        self.tab1.imagePaths = self.newFileWindow.iamgeObjectListPath
        self.tab1.currentDirectory = self.newFileWindow.currentPathName
        self.tab1.loadImageToGrid()
        self.tab1.currentDirectory = self.newFileWindow.currentPathName
        return
    
    def showGridObjects(self):
            if self.tab1.gridBusy == False:
                self.methodInfo.setText("Loading... Please Wait")
                self.tab1.gridBusy = self.tab1.addImagesToGrid()
                self.methodInfo.setText("Loaded Successfully")
            else:
                self.methodInfo.setText("Grid is busy")
            return

    def openGalleryImage(self):
        self.tab1.imageToShow = self.newFileWindow.iamgeObjectPath
        if self.tab1.imageToShow != "":
            self.tab1.openImageInGallery()
            self.tab1.imageInformationLabel.setText(self.newFileWindow.createImageInformation(self.tab1.imageToShow))
            self.newFileWindow.close()
        return
    
    def openNextImageInGallery(self):
        if self.tabScreen.currentIndex() == 0:
            self.tab1.imageNormalSize = self.tab1.originalSize
            self.methodInfo.setText(self.tab1.showNextImage(self.newFileWindow.iamgeObjectListPath))
            self.tab1.imageInformationLabel.setText(self.newFileWindow.createImageInformation(self.tab1.imageToShow))
        elif self.tabScreen.currentIndex() == 1:
            self.methodInfo.setText("Can't Open next image in edit mode")
        return
    
    def openPreviousImageInGallery(self):
        if self.tabScreen.currentIndex() == 0:
            self.tab1.imageNormalSize = self.tab1.originalSize
            self.methodInfo.setText(self.tab1.showPreviousImage(self.newFileWindow.iamgeObjectListPath))
            self.tab1.imageInformationLabel.setText(self.newFileWindow.createImageInformation(self.tab1.imageToShow))
        elif self.tabScreen.currentIndex() == 1:
            self.methodInfo.setText("Can't open previous Image in edit mode")
        return
    
    def scaleUPImage(self):
        if self.tab1.imageNormalSize <= (10000, 10000):
            self.tab1.imageNormalSize=(self.tab1.imageNormalSize[0]*1.25,self.tab1.imageNormalSize[1]*1.25)
            self.tab1.openImageInGallery()
            return
        else:
            return
    
    def scaleDownImage(self):
        if self.tab1.imageNormalSize >= (100, 100):
            self.tab1.imageNormalSize = (self.tab1.imageNormalSize[0] / 1.25, self.tab1.imageNormalSize[1] / 1.25)
            self.tab1.openImageInGallery()
            return
        else:
            return
    
    def originalScale(self):
        self.tab1.imageNormalSize = self.tab1.originalSize
        self.tab1.openImageInGallery()
        return
    
    def openEditSectionImage(self):
        self.tab2.imageToEdit = self.newFileWindow.iamgeObjectPath
        self.newFileWindow.previewHolderLabel.hide()
        self.newFileWindow.previewHolderLabel.setText("Preview")
        self.newFileWindow.previewHolderLabel.show()
        self.methodInfo.setText(self.tab2.openImageInEditSection())
        self.newFileWindow.close()
        return
    
    def addStyledSheet(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #18122b;
                border-radius: 0px;
            }
            QFrame {
                border: 1px outset #4f4e4f;
                background-color: #020f17;
                padding : 2px;
            }
            QFrame:hover {
                border: 2px outset #4f4e50;
                background-color: #020f1c;
                padding : 2px;
            }
            QLabel {
                background-color : #190140;
                font-size: 12px;
                color: #ffffff;
                padding : 2px;
                border-radius : 10px;
            }
            QLabel:hover {
                background-color : #280180;
                font-size: 12px;
                color: #ffffff;
                padding : 2px;
                border-radius : 10px;
            }
            QMenuBar {
                background-color : #3f018f;
                color : #ffffff;
                font-size : 14px;
                border : 1px outset #4f4e4f;
            }
            QMenuBar::item {
                background-color: #3f018f;
                color: #ffffff;
            }
            QMenuBar::item:selected{
                background-color: #6004d6;
                color: #000000;
            }
            QTabBar::Tab {
                background-color: #5902c9;
                padding: 4px;
                color : #ffffff;
            }
            """
        )
    pass

if __name__ == '__main__':
    app = QApplication([])
    masterWindow = MasterWindow()
    app.exec_()