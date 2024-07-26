#inbuild Modules
import os
from PIL import Image
from linkedList import LinkedList,Node
import shutil

#custom class for os management
class OperatingSystem:
    def __init__(self,name) -> None:
        self.name = name
        self.current_directory = "C:\\" #current directory can be accessed by methods and instance
        linkedList = LinkedList(Node(self.current_directory)) #default linkedlist by management system
        self.dir_linked_list = linkedList #self.dir_linked_list is system varaible which can accessed by other linked list and have same features
    
    @classmethod # can open an image
    def openImage(cls,fileName : str):
        try:
             with Image.open(fileName) as image:
                image.show()
        except OSError as o:
            print(f"The file {fileName} can't be opened\n{o}")
    
    @classmethod #can open a text file
    def openTextFile(cls,fileName : str):
        print("\nOpening your file....\n")
        try:
            with open(fileName,'r') as file:
                print(file.read())
        except FileNotFoundError as o:
            print(o)
    
    #openDirectory
    def openDirectory(self,address:str):
        try:
            os.chdir(address)
            self.dir_linked_list.addDirectory(address)#stored the newly Opened directory
            self.current_directory = os.getcwd()
        except OSError:
            print("Unexpected error occurred")
        finally:
            return
    
    #delete a directory
    def deleteDirectory(self,fileName):

        #removes the file / directory from the linkedlist if exist in it
        self.dir_linked_list.head = self.dir_linked_list.removeDirectory(self.dir_linked_list.head,fileName)
        try:
            if os.path.exists(fileName):
                shutil.rmtree(fileName)
                return True
            else:
                print("Directory not found🙄")
                return False
        except OSError as o:
            print(o)
            return False
    
    #create a directory
    def createDirectory(self,current_directory):
        self.openDirectory(current_directory)
        try:
            os.mkdir(input("Enter File Name:\t"))
            return True
        except FileExistsError as o:
            print(o)
            self.createDirectory(current_directory)
            return False
        except OSError as o:
            print(o)
            return True

    #current directory contents
    def dirlist(self) -> dict:
        self.directoryList =  os.listdir(os.getcwd())
        if len(self.directoryList) >0:
            return {i+1:self.directoryList[i] for i in range(len(self.directoryList))}
        else:
            return {}
    
    #iterates and shows the directories in a given directory
    def iterateDir(self):
        #if the directory is a folder
        while os.path.isdir(os.getcwd()):
            #cheaks if a directory is empty
            if len(os.listdir(os.getcwd())) == 0:
                return None
            
            #if a directory is not empty
            currentDir = self.current_directory #to be in the current directory if gives problem switch to os.getcwd()
            directoryDict = self.dirlist() #retrun a dictionary of the directories

            for i in directoryDict.keys(): #prints the name of all directory with index
                print(f"{i}--->{directoryDict[i]}")

            iter = int(input("Enter Directory NUmber: "))#takes the user input

            if iter == 0: # set the the current directory to be the desired directory
                if os.path.isdir(currentDir):
                    self.current_directory = currentDir
                break
            elif iter == -1: # breaks the while loop
                break
            
            #sets thse current directory to be the desired directory
            currentDir += f"\\{directoryDict[iter]}"
            self.current_directory = currentDir
            
            #tries to open the selected directory
            if os.path.isdir(self.current_directory):
                self.openDirectory(self.current_directory)
            
            #if it is a file
            elif os.path.isfile(self.current_directory):
                print(currentDir)
                print(os.path.splitext(currentDir))
                if os.path.splitext(currentDir)[1] in ['.py','.txt']:#if it is a text file
                    print("Done")
                    self.openTextFile(self.current_directory)
                
                # if it is a image
                elif os.path.splitext(currentDir)[1] in ['.jfif','.jpeg','.png']:
                    self.openImage(self.current_directory)
                break
        return
    
    #moves a directory
    def move(self,directory:str):
        self.copy(directory)
        self.deleteDirectory(directory)
        return
    
    #copy a file or directory
    def copy(self,directory:str):
         #handles if the path is a file
        if os.path.isfile(directory):
            self.copyFile(directory)

        #hanles if the path is a directory
        elif os.path.isdir(directory):
            self.copyDirectory(directory)
        
        #if not a directory nor a file
        else:
            print("d")
            return "unexpected error occurred"
        return
    
    #copy a directory to a different location
    def copyDirectory(self,targetDiretory):
        self.openDirectory(input("Open a directory:\t"))
        self.iterateDir() #by this method the desired directory can be reached
        nameList = targetDiretory.split("\\")
        self.current_directory += f"\\{nameList[len(nameList)-1]}"#creates the new destination
        try:
            shutil.copytree(targetDiretory,self.current_directory)
        except PermissionError as o:
            return f"Permission Denied {o}"
        except OSError as o:
            return f"Os Error: {o}"
    
    #copy a file to a different location
    def copyFile(self,targetFile):
        self.openDirectory(input("Open a directory:\t"))
        self.iterateDir() #by this method the desired directory can be reached
        nameList = targetFile.split("\\")
        self.current_directory += f"\\{nameList[len(nameList)-1]}"#creates the new destination
        try:
            shutil.copy(targetFile,self.current_directory)
        except FileNotFoundError:
            return f"File {targetFile} is not found.."
        except PermissionError:
            return f"Permission Denied.."
        except OSError as o:
            return f"Os Error: {o}"
    
    #back to previous Directory
    def previousDirectory(self):
        lastDirectoryNode = self.dir_linked_list.get_lastNode(self.dir_linked_list.head)
        self.current_directory = lastDirectoryNode.previousNode.directory
        os.chdir(self.current_directory)
    
    def goToDirectory(self):
        iterated_length = self.dir_linked_list.listLength() #length of the linkedlist
        temporary_head = self.dir_linked_list.head
        iterated_dictionary = {} #dictionary to store previously iterated directory
        for i in range(iterated_length):
            iterated_dictionary[i] = temporary_head.directory
            temporary_head = temporary_head.nextNode
        
        #viewing previous directories
        print(iterated_dictionary)
        
        iter = int(input("Enter directory number:\t"))
        #removinng everything from desired directory
        self.dir_linked_list.head = self.dir_linked_list.deleteAfter(iterated_dictionary[iter])

        #open the directory desired
        self.openDirectory(iterated_dictionary[iter])
        return

    pass


#useful functions
def intValueError():
    try:
        value = int(input("Enter command:\t"))
        return value
    except ValueError as v:
        print(f"***Invalid Input***")
        intValueError()
    
def invalidInputError(list):
    value = input("Input:\t")
    if value in list:
        print("Invalid Input")
    else:
        return True

#main loop
if __name__=='__main__':
    myoperatingSystem = OperatingSystem("File Operator")
    print("Done")
    print("List of operation\n0---> Open current Directory\n1--->Open a directory\n2--->Ask all directory\n3--->iterate thorugh Directory\n4--->Create a directory\n5--->delete a directory\n6--->Copy a directory\n7--->move a directory\n8--->go to previous Directory \n9--->go to directory")
    command = intValueError()
    while command != -1:
        
        #Opens the current directory:
        if command == 0:
            myoperatingSystem.openDirectory(myoperatingSystem.current_directory)
        
        #Opens a directory
        elif command == 1:
            myoperatingSystem.openDirectory(input("Enter Address:\t"))
            print(myoperatingSystem.dir_linked_list.directoryList())
        
        #gives a list of directories
        elif command == 2:
            directoryList = myoperatingSystem.dirlist()
            for i in directoryList.keys():
                print(f"{i}---->{directoryList[i]}")
        
        #iterates a through directories
        elif command == 3:
            myoperatingSystem.iterateDir()
            print(myoperatingSystem.dir_linked_list.directoryList())
        
        #create a directory
        elif command == 4:
            myoperatingSystem.createDirectory(myoperatingSystem.current_directory)
        
        #delete a directory:
        elif command == 5:
            current_directory_list = myoperatingSystem.dirlist()
            if current_directory_list != None:
                print(current_directory_list)
                myoperatingSystem.deleteDirectory(current_directory_list[int(input("Give directory number:\t"))])
                print(myoperatingSystem.dir_linked_list.directoryList())
            else:
                print("Can't delete a file being inside it😂")
        
        #copy a file/ folder from current directory to another
        elif command == 6:
            print(myoperatingSystem.copy(myoperatingSystem.current_directory))

        elif command == 7:
            current_directory_list = myoperatingSystem.dirlist()
            if current_directory_list != None:#if the directory is not empty
                print(current_directory_list)
                myoperatingSystem.move(current_directory_list[int(input("Give directory number:\t"))])
            else:#if the directory is empty
                myoperatingSystem.move(myoperatingSystem.current_directory)
        
        elif command == 8:
            myoperatingSystem.previousDirectory()

        # go to directory
        elif command == 9:
            myoperatingSystem.goToDirectory()
        
        #if no command matches
        else:
            print("Invalid Input") 
        #takes new command for the further operation..
        command = intValueError()
    pass