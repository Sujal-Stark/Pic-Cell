from PyQt5.QtGui import QPixmap
from PIL import Image
class Node:
    def __init__(self) -> None:
        self.image : QPixmap # stores teh image in Pixmap Format
        self.PILImage : Image.Image # stores the image in PIL format
        self.nextNode = None  # store the next node address
        self.previousNode = None  # store the previous node address
        return
    
class PixmapLinker:
    def __init__(self):
        self.pixmapHead : Node = None # stores pixmap object
        return

    def createPixmappixmapHead(self, img : QPixmap, PILImage : Image.Image):
        if self.pixmapHead == None:
            self.pixmapHead = Node()
            self.pixmapHead.image = img
            self.pixmapHead.PILImage = PILImage
            return
    
    # adds other pixmap nodes
    def addPixmap(self, targetNode : Node, img : QPixmap, PILImage : Image.Image = None) -> Node:
        if (targetNode):
            newNode = Node() # create nodes
            newNode.image = img
            newNode.PILImage = PILImage
            newNode.nextNode = targetNode # newnode -> targetnode
            targetNode.previousNode = newNode # newnode <- targetnode
            targetNode = newNode # newnode = targetnode
            return targetNode
    pass