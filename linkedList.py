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
        #if there is no head node
        if self.head == None:
            self.head=Node(directoryPath)
            self.head.previousNode = None
        temp=self.head

        #if head node exist
        if temp.directory == "":
            temp.directory=directoryPath
        else:
            while temp.nextNode!=None:#iterates to the last available node
                temp=temp.nextNode
            newNode=Node(directoryPath)
            temp.nextNode=newNode
            newNode.previousNode=temp
        return self.head #returning the modified head node
    
    #Iterates Through all the directories
    def iterate(self,head:Node):
        temp=head
        directory_list = []#stores all the direcotory
        while temp!=None:
            directory_list.append(temp.directory)
            temp=temp.nextNode
        return directory_list
    
    #adds a directory after currently used directory
    def addAfter(self,currentDir,newDir):
        temp=self.head

        # iterates to the directory after where new direcotory will be stored
        while temp!=None:
            if temp.directory == currentDir: # if head is current directory
                newNode = Node(newDir)
                newNode.nextNode=temp.nextNode
                #iterates to search and add new direcotory
                if temp.nextNode != None:
                    Node(newNode.nextNode).previousNode= newNode
                temp.nextNode = newNode
                newNode.previousNode=temp
                break
            temp=temp.nextNode

        return self.head
    
    #returns a list containing all the directories visited
    def directoryList(self):
        dList = [] #where the directories will be stored
        bufferNode = self.head 
        if bufferNode == None :#if head is empty
            return
        while bufferNode!=None: #if head is not empty
            dList.append(bufferNode.directory)
            bufferNode = bufferNode.nextNode
        return dList
    
    #removes a directory
    def removeDirectory(self,head:Node,directory:str):
        # if first directory is to be removed
        splittedhead = head.directory.split("\\",20)
        print(splittedhead)
        if splittedhead[len(splittedhead)-1] == directory:
            if head.nextNode != None:
                head = head.nextNode
                head.previousNode = None
            else:
                head = head.nextNode
            return head
        else:
            temp = head
            while temp != None:
                splittedrest = temp.directory.split("\\",20)
                print(splittedrest)
                if splittedrest[len(splittedrest)-1] == directory:
                    
                    if temp.nextNode != None: # if any node in the middle is to be deleted
                        temp.previousNode.nextNode = temp.nextNode
                        temp.nextNode.previousNode = temp.previousNode
                    
                    else: # if the last node is to be deleted
                        temp.previousNode.nextNode = temp.nextNode
                    return head
                temp = temp.nextNode
        return head 
    
    #delete after a specific directory:
    def deleteAfter(self, directoryName:str)->Node:
        temporary_head = self.head
        #iterates to the directory and removes every directory after that
        while temporary_head != None:
            if temporary_head.directory == directoryName:
                temporary_head = None
            temporary_head= temporary_head.nextNode
        
        return self.head
    ##cheaks if a directory exists in the list or not
    def direcoryExists(self,head:Node,directory:str):
       temporary_head = head

       while temporary_head != None:#while checks if the directory exists or not
            if temporary_head.directory == directory:
                return True
            else:
                temporary_head = temporary_head.nextNode
            return False

    #terminates the list
    def terminateList(self):
        if self.head == None: #checks if a list is empty or not
            return False
        self.head=None
        return True
    
    #switch 2 directory
    def switchDirectory(self,currentDirectory1:str,currentDirectory2:str):
        # get the directory in the nodes which to be swapped
        currentDirectory1_node = self.getDirectoryNode(self.head,currentDirectory1)
        currentDirectory2_node = self.getDirectoryNode(self.head,currentDirectory2)

        # checks if both directory node exists
        if currentDirectory1_node != None and currentDirectory2_node != None:

            # swapping algorithm
            bufferDirectoryName=currentDirectory1_node.directory
            currentDirectory1_node.directory=currentDirectory2_node.directory
            currentDirectory2_node.directory=bufferDirectoryName
            return self.head
        else:
            None

    #the last node of a list will be returned
    def get_lastNode(self,head:Node)->Node:
        copy_head = head   #copying head node
        while copy_head.nextNode != None: #iters upto the last node
            copy_head = copy_head.nextNode
        return copy_head #returns last node
    
    #returns a directory node of desire
    def getDirectoryNode(self,head:Node,curentDirectory:str):
        bufferHead = head

        #iters until the target node is found
        while bufferHead != None:
            if bufferHead.directory == curentDirectory: #if head is target
                return bufferHead
            
            #if any other node is the target node
            else:
                bufferHead = bufferHead.nextNode
            if bufferHead == None :
                return None
            
    #iters to the head node
    def getFirstNode(self,directoryNode:Node):
        while directoryNode.previousNode!=None:
            directoryNode=directoryNode.previousNode
        return directoryNode
    
    #gets the last node from a linked list and returns the linkedlist in reverse order
    def reverse_traversal(self,llist):
        directory_node = self.get_lastNode(llist) # retrieving the last node
        directoryList = []

        #iters to store the node directory name
        while directory_node!=None:
            directoryList.append(directory_node.directory)
            directory_node = directory_node.previousNode
        return directoryList
    
    #returns the length of a linked list
    def listLength(self)->int:
        temporary_head = self.head
        count = 0#measures the length
        while temporary_head != None:
            count += 1
            temporary_head = temporary_head.nextNode
        return count

#handles int input error
def intValueError(Query:str):
    try:
        return int(input(f"Enter {Query}\t"))
    except ValueError:
        print("Invalid Input...")
        intValueError(Query)

if __name__ == '__main__':
    print("Command List:\n-1 to Exit\n1--->add a directory\n2--->add a directory after some directory\n3--->Iterate\n4--->Directory List\n5--->Removes a Directory\n6--->Switch 2 Directory\n7--->get Desired DirectoryNode\n8--->Terminate List\n9--->get the last directory node\n10--->traverse in reverse way\n11--->Checks if a directory exists\n12->list length\n13--->delete after a directory")
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
        
        #getting the last directory node and printing the directory
        elif command == 9:
            print(linkedList.get_lastNode(linkedList).directory)

        #printing a linkedlist in reverse order
        elif command == 10:
            directorylist = linkedList.reverse_traversal(linkedList)
            for item in directorylist:
                print(f"Current directory is:\t {item}")
        
        #checks if a directory exists in the list
        elif command == 11:
            if linkedList.direcoryExists(linkedList.head,input("Enter directory name:\t")):
                print('The directory exists')
            else:
                print("The directory doesn't exists")

        #list length
        elif command == 12:
            print(linkedList.listLength())

        #delete after a directory
        elif command == 13:
            linkedList.head = linkedList.deleteAfter(input("Enter directory name:\t"))
            print(linkedList.directoryList())

        else:
            print("wrong Command")
        command = intValueError("Command")
    print("Programme Finished")