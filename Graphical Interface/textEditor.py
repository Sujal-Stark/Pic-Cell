from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QLabel, QPushButton
from PyQt5.QtCore import Qt
import sys

class TextEditorAssembly(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setFixedSize(640,460)
        self.textEditorMasterLayout = QVBoxLayout(self)
        self.createUI()
        self.constructUI()
        self.addStyleSheet()
        return
    
    def createUI(self):
        self.createframes()
        self.createLayouts()
        self.createScrollArea()
        return
    
    def createLayouts(self):
        self.innerTExtEditorMasterLayout = QVBoxLayout()

        self.viewZone = QVBoxLayout()
        self.controlZone = QHBoxLayout()

        self.viewPanel = QVBoxLayout()
        self.innerViewPanel = QVBoxLayout()

        self.controlLayout = QVBoxLayout()
        self.innerControlLayout = QVBoxLayout()

        self.advanceControlLayout = QVBoxLayout()
        self.innerAdvanceControlLayout = QVBoxLayout()
        return

    def createScrollArea(self):
        self.viewPanelScrollArea = QScrollArea()
        self.viewPanelScrollArea.setFixedSize(600,220)

        self.controlScrollArea = QScrollArea()
        self.controlScrollArea.setFixedSize(295,180)

        self.advanceControlScrollArea = QScrollArea()
        self.advanceControlScrollArea.setFixedSize(295,180)
        return

    def createframes(self):
        self.textEditorMasterFrame = QFrame()
        self.textEditorMasterFrame.setFixedSize(620,440)
        self.textEditorMasterFrame.setFrameShape(QFrame.Shape.Box)

        self.viewPanelFrame = QFrame()
        # self.viewPanelFrame.setFixedSize(600,220)
        self.viewPanelFrame.setFrameShape(QFrame.Shape.Box)

        self.controlFrame = QFrame()
        # self.controlFrame.setFixedSize(295,180)
        self.controlFrame.setFrameShape(QFrame.Shape.Box)

        self.advanceControlFrame = QFrame()
        # self.advanceControlFrame.setFixedSize(295,180)
        self.advanceControlFrame.setFrameShape(QFrame.Shape.Box)
        return
    
    def constructUI(self):
        self.textEditorMasterLayout.addWidget(self.textEditorMasterFrame)
        self.textEditorMasterFrame.setLayout(self.innerTExtEditorMasterLayout)

        self.innerTExtEditorMasterLayout.addLayout(self.viewZone)
        self.innerTExtEditorMasterLayout.addLayout(self.controlZone)

        self.viewZone.addLayout(self.viewPanel)

        self.viewPanel.addWidget(self.viewPanelScrollArea)
        self.viewPanelScrollArea.setWidget(self.viewPanelFrame)
        self.viewPanelFrame.setLayout(self.innerViewPanel)

        self.controlZone.addLayout(self.controlLayout)
        self.controlZone.addLayout(self.advanceControlLayout)

        self.controlLayout.addWidget(self.controlScrollArea)
        self.controlScrollArea.setWidget(self.controlFrame)
        self.controlFrame.setLayout(self.innerControlLayout)

        self.advanceControlLayout.addWidget(self.advanceControlScrollArea)
        self.advanceControlScrollArea.setWidget(self.advanceControlFrame)
        self.advanceControlFrame.setLayout(self.innerAdvanceControlLayout)
        return
    
    def addStyleSheet(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #18122b;
                border-radius: 0px;
            }
            QFrame {
                border: 1px outset #4f4e4f;
                background-color: #01031c;
            }
            """
        )

if __name__ == '__main__':
    app = QApplication([])
    textEditor = TextEditorAssembly()
    textEditor.show()
    app.exec_()
    