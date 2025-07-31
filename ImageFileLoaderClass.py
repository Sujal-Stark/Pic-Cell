"""
QThread Subclass sends imageFilepath to the GalleryView File with some time delay
for QWidget to respond
"""

from PyQt5.QtCore import QThread, pyqtSignal

class ImageFileLoader(QThread):
    # class Attributes
    imageFilepaths : list[str] = [] # will hold imagePaths

    # Pyqt Signals
    imageObjectReady = pyqtSignal(str) # sends image path to GalleryView
    operationDone = pyqtSignal() # conveys that operation is done

    def __init__(self, imagePaths: list[str]):
        super().__init__()
        self.imageFilepaths = imagePaths
        return

    def run(self):
        if len(self.imageFilepaths) > 0: # works if there is any image
            try:
                for path in self.imageFilepaths:
                    self.imageObjectReady.emit(path)
                    self.msleep(50)
                else:
                    self.operationDone.emit() # to make sure thread Busy Statement is active
            except (MemoryError, OSError):
                print("Error occurred")
            return
        else: return
    pass