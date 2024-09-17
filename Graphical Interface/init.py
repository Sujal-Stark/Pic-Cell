# libraries
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class MasterWindow(QWidget):
    def __init__(self)-> None:
        super().__init__()
        
        self.setWindowTitle("Pic_Cell")
        self.setGeometry(0,0,800,600)
        self.masterLayout = QVBoxLayout(self)
        self.LoadUI()
        self.show()
        return
    
    def LoadUI(self):
        self.createButtons()
        self.createLabels()
        self.createLayouts()
        self.createFrames()
        self.createTabs()
        self.construct()
    
    def createButtons(self):
        self.fileButton = QPushButton("File Access")
        self.editButton = QPushButton("Edit File")
        return
    
    def createLabels(self):
        self.imageLoader = QLabel("Your Image will show up here")
        self.methodInfo = QLabel("Any information about the image will show up here")
        return
    
    def createFrames(self):
        self.headerFrame = QFrame()
        self.headerFrame.Shape(QFrame.Shape.Box)
        self.footerFrame = QFrame()
        self.footerFrame.Shape(QFrame.Shape.Box)
        return
    
    def createLayouts(self):
        self.outerHeader = QHBoxLayout()
        self.innerHeader = QHBoxLayout()
        
        self.midbody = QHBoxLayout()

        
        self.outerFooter = QHBoxLayout()
        self.innerFooter = QHBoxLayout()
        return
    
    def createTabs(self):
        self.tabScreen = QTabWidget()

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabScreen.addTab(self.tab1, "Gallery")
        self.tabScreen.addTab(self.tab2, "Edit Section")
        return
    
    def construct(self):
        self.masterLayout.addLayout(self.outerHeader,10)
        self.masterLayout.addLayout(self.midbody,90)
        self.masterLayout.addLayout(self.outerFooter,10)

        self.outerHeader.addWidget(self.headerFrame)
        self.headerFrame.setLayout(self.innerHeader)
        self.outerFooter.addWidget(self.footerFrame)
        self.footerFrame.setLayout(self.innerFooter)

        self.innerHeader.addWidget(self.fileButton)
        self.innerHeader.addWidget(self.editButton)

        self.midbody.addWidget(self.tabScreen)

        self.innerFooter.addWidget(self.methodInfo, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
if __name__ == '__main__':
    app = QApplication([])
    masterWindow = MasterWindow()
    app.exec_()

