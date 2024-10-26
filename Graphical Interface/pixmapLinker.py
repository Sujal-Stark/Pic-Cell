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
        
    def addPixmap(self, img : QPixmap):
        if self.head != None:
            newNode = Node()
            newNode.image = img
            newNode.nextNode = self.head
            self.head.previousNode = newNode
            self.head = newNode
            return
    
    def getlastPixmap(self) -> Node:
        newHead = self.head
        while newHead.nextNode:
            newHead = newHead.nextNode
        return newHead