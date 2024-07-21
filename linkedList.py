# Defination of Node
class Node:
    def __init__(self,directory="",prev=None,new=None):
        self.directory=directory
        self.previousNode=prev
        self.nextNode=new
    def __delattr__(self,node):
        self.directory = self.nextNode = self.previousNode = None
    pass

# class LinkedList
class LinkedList:
    #defination of the head of L list
    def __init__(self,headNode:Node):
        self.head=headNode

    #adds directory when ever new directory is searched
    def addDirectory(self,directoryPath):
        if self.head == None:
            self.head=Node(directoryPath)
        temp=self.head
        if temp.directory == "":
            temp.directory=directoryPath
        else:
            while temp.nextNode!=None:
                temp=temp.nextNode
            newNode=Node(directoryPath)
            temp.nextNode=newNode
            newNode.previousNode=temp
        return self.head
    
    #Iterates Through all the directories
    def iterate(self,head:Node):
        temp=head
        while temp!=None:
            print(temp.directory)
            temp=temp.nextNode
    
    #adds a directory after currently used directory
    def addAfter(self,currentDir,newDir):
        temp=self.head
        while temp!=None:
            if temp.directory == currentDir:
                newNode = Node(newDir)
                newNode.nextNode=temp.nextNode
                if temp.nextNode != None:
                    Node(newNode.nextNode).previousNode= newNode
                temp.nextNode = newNode
                newNode.previousNode=temp
                break
            temp=temp.nextNode
        return self.head
    
    #returns a list containing all the directories visited
    def directoryList(self):
        dList = []
        bufferNode = self.head
        if bufferNode == None :
            return
        while bufferNode!=None:
            dList.append(bufferNode.directory)
            bufferNode = bufferNode.nextNode
        return dList
    
    #removes a directory
    def removeDirectory(self,head:Node,directory:str):
        if head.directory == directory:
            if head.nextNode != None:
                head = head.nextNode
                head.previousNode = None
            else:
                head = head.nextNode
            return head
        else:
            temp = head
            while temp != None:
                if temp.directory == directory:
                    if temp.nextNode != None:
                        temp.previousNode.nextNode = temp.nextNode
                        temp.nextNode.previousNode = temp.previousNode
                    else:
                        temp.previousNode.nextNode = temp.nextNode
                    return head
                temp = temp.nextNode
    
    #terminates the list
    def terminateList(self):
        if self.head == None:
            return False
        self.head=None
        return True
    
    #switch 2 directory
    def switchDirectory(self,currentDirectory1:str,currentDirectory2:str):
        currentDirectory1_node = self.getDirectoryNode(self.head,currentDirectory1)
        currentDirectory2_node = self.getDirectoryNode(self.head,currentDirectory2)
        if currentDirectory1_node != None and currentDirectory2_node != None:
            bufferDirectoryName=currentDirectory1_node.directory
            currentDirectory1_node.directory=currentDirectory2_node.directory
            currentDirectory2_node.directory=bufferDirectoryName
            return self.head
        else:
            None

    #returns a directory node of desire
    def getDirectoryNode(self,head:Node,curentDirectory:str):
        bufferHead = head
        while bufferHead != None:
            if bufferHead.directory == curentDirectory:
                return bufferHead
            else:
                bufferHead = bufferHead.nextNode
            if bufferHead == None :
                return None
    def getFirstNode(self,directoryNode:Node):
        while directoryNode.previousNode!=None:
            directoryNode=directoryNode.previousNode
        return directoryNode

#handles int input error
def intValueError(Query:str):
    try:
        return int(input(f"Enter {Query}\t"))
    except ValueError:
        print("Invalid Input...")
        intValueError(Query)

if __name__ == '__main__':
    print("Command List:\n-1 to Exit\n1--->add a directory\n2--->add a directory after some directory\n3--->Iterate\n4--->Directory List\n5--->Removes a Directory\n6--->Switch 2 Directory\n7--->get Desired DirectoryNode\n8--->Terminate List")
    linkedList=LinkedList(Node(""))
    command = intValueError("command")
    while command != -1:
        if command == 1:
            linkedList.addDirectory(input("Enter Directory\t"))
        elif command == 2:
            linkedList.addAfter(input("Current Directory:\t"),input("New Directory:\t"))
        elif command == 3:
            #can iterate through sublists
            linkedList.iterate(linkedList.head)
        elif command == 4:
            #always gives the list off all directories
            print(linkedList.directoryList())
        elif command == 5:
            linkedList.head = linkedList.removeDirectory(linkedList.head,input("Enter Directory Name:\t"))
            linkedList.iterate(linkedList.head)
        elif command == 6:
            linkedList.iterate(linkedList.switchDirectory(input("Enter Directory1 Name:\t"),input("Enter Directory2 Name:\t")))
        elif command == 7:
            directoryNode = linkedList.getDirectoryNode(linkedList.head,input("Enter Directory:\t"))
            print(directoryNode.directory) if directoryNode != None else print("Directory Not found")
        elif command == 8:
            print("List is terminated") if linkedList.terminateList() else print("Empty List was given")
        else:
            print("wrong Command")
        command = intValueError("Command")
    print("Programme Finished")