from PyQt5.QtGui import QPixmap

class Node:
    def __init__(self) -> None:
        self.image : QPixmap
        self.nextNode = None
        self.previousNode = None
        return
    
class PixmapLinker:
    def __init__(self):
        self.head : Node = None
        return

    def createhead(self, img : QPixmap):
        if self.head == None:
            self.head = Node()
            self.head.image = img
            return
        
    def addPixmap(self, targetNode : Node, img : QPixmap) -> Node:
        if targetNode != None:
            newNode = Node()
            newNode.image = img
            newNode.nextNode = targetNode
            targetNode.previousNode = newNode
            targetNode = newNode
            return targetNode