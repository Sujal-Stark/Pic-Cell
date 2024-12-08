from PyQt5.QtGui import QPixmap
from PIL import Image
class Node:
    def __init__(self) -> None:
        self.image : QPixmap # stores teh image in Pixmap Format
        self.nextNode = None  # store the next node address
        self.previousNode = None  # store the previous node address
        return

# PIL image Node CLass
class PILNode:
    def __init__(self) -> None:
        self.PILimage : Image.Image = None # stores the PIL image
        self.nextNode : PILNode = None # store the next node address
        self.previousNode : PILNode = None # store the previous node address
        return
    
class PixmapLinker:
    # varibale heads to store objects 
    pixmapHead : Node = None # stores pixmap object
    PILHead  = None # stores PIL object

    def __init__(self):
        # self.pixmapHead : Node = None
        return

    def createPixmappixmapHead(self, img : QPixmap):
        if self.pixmapHead == None:
            self.pixmapHead = Node()
            self.pixmapHead.image = img
            return
    
    # create a head for PIL image
    def createPILHead(self, image : Image.Image) -> None:
        if self.PILHead == None:
            self.PILHead = PILNode()
            self.PILHead.PILimage = image
        return
    
    # adds other pixmap nodes
    def addPixmap(self, targetNode : Node, img : QPixmap) -> Node:
        if (targetNode):
            newNode = Node() # create nodes
            newNode.image = img
            newNode.nextNode = targetNode # newnode -> targetnode
            targetNode.previousNode = newNode # newnode <- targetnode
            targetNode = newNode # newnode = targetnode
            return targetNode
    
    # adds other pil nodes
    def addPILObject(self, targetNode : PILNode, image : Image.Image) -> PILNode:
        if(targetNode):
            newNode = PILNode()
            newNode.PILimage = image
            newNode.nextNode = targetNode # newnode -> targetnode
            targetNode.previousNode = newNode # newnode <- targetnode
            targetNode = newNode # newnode = targetnode
            return targetNode
    pass