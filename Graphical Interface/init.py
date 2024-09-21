# libraries
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QFrame, QMenuBar, QMenu, QAction, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from galleryView import GalleryWindow
from fileWindow import FileWindow
class MasterWindow(QMainWindow):
    def __init__(self)-> None:
        super().__init__()
        
        self.setWindowTitle("Pic_Cell")
        self.setGeometry(0,0,800,600)
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.masterLayout = QVBoxLayout(self.mainWidget)
        self.LoadUI()
        self.assignProperties()
        self.newFileWindow.fileOpenButton.clicked.connect(self.openGalleryImage)
        self.closeFile.triggered.connect(self.tab1.closeImageFromGallery)
        self.newFileWindow.fileListWidget.currentRowChanged.connect(self.connectImageGridWithFiles)
        self.show()
        return
    
    def assignProperties(self):
        self.newFileWindow = FileWindow()
        return
    
    def LoadUI(self):
        self.createMenubar()
        self.createButtons()
        self.createLabels()
        self.createLayouts()
        self.createFrames()
        self.createTabs()
        self.construct()
        return
    
    def createMenubar(self):
        self.bar = QMenuBar(self)
        self.fileMenu = QMenu("File")
        self.editMenu = QMenu("Edit")
        self.viewMenu = QMenu("View")
        self.bar.addMenu(self.fileMenu)
        self.bar.addMenu(self.editMenu)
        self.bar.addMenu(self.viewMenu)

        self.openFile = QAction("Open", self)
        self.openFile.setShortcut("ctrl+o")
        self.openFile.triggered.connect(self.createSeondWindow)
        self.closeFile = QAction("Close", self)
        self.closeFile.setShortcut("ctrl+w")

        self.fileMenu.addActions([self.openFile, self.closeFile])
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
        self.tab2 = QWidget()

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
        self.newFileWindow.show()
        return
    
    def connectImageGridWithFiles(self):
        self.tab1.loadImageGrid(self.newFileWindow.iamgeObjectListPath)
        # self.tab1.viewBar.acceptData(self.newFileWindow.iamgeObjectListPath)
        # self.tab1.viewBar.addShowableImages()
        return

    def openGalleryImage(self):
        self.tab1.imageToShow = self.newFileWindow.iamgeObjectPath
        if self.tab1.imageToShow != None:
            self.tab1.openImageInGallery()
            self.tab1.imageInformationLabel.setText(self.newFileWindow.currentImageInformation)
            self.newFileWindow.close()
        return
    
    pass

if __name__ == '__main__':
    app = QApplication([])
    masterWindow = MasterWindow()
    app.exec_()