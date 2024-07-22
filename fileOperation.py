#inbuild Modules
import os
from PIL import Image
from linkedList import LinkedList
import shutil

#custom class for os management
class OperatingSystem:
    def __init__(self,name) -> None:
        self.name = name
        self.current_directory = "C:\\" #current directory can be accessed by methods and instance
    
    @classmethod # can open an image
    def openImage(cls,fileName : str):
        try:
             with Image.open(fileName) as image:
                image.show()
        except OSError as o:
            print(f"The file {fileName} can't be opened\n{o}")
    
    @classmethod #can open a text file
    def openTextFile(fileName : str):
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
            self.current_directory = os.getcwd()
        except OSError:
            print("Unexpected error occurred")
        finally:
            return
    
    #delete a directory
    def deleteDirectory(self,fileName):
        print(fileName)
        print(os.path.exists(fileName))
        print(os.path.isdir(fileName))
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
    def dirlist(self):
        self.directoryList =  os.listdir(os.getcwd())
        if len(self.directoryList) >0:
            return {i+1:self.directoryList[i] for i in range(len(self.directoryList))}
        else:
            return None
    
    #iterates and shows the directories in a given directory
    def iterateDir(self):

        while len(os.listdir(os.getcwd())) != 0:

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
            
            #sets the current directory to be the desired directory
            currentDir += f"\\{directoryDict[iter]}"
            self.current_directory = currentDir
            
            #tries to open the selected file
            if os.path.isdir(self.current_directory):
                self.openDirectory(self.current_directory)
            elif os.path.isfile(self.current_directory):
                if os.path.splitext(self.current_directory)[1]=='.py':
                    self.openTextFile(self.current_directory)
                elif os.path.splitext(self.current_directory)[1] in ['.jfif','.jpeg','.png']:
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
    print("List of operation\n0---> Open current Directory\n1--->Open a directory\n2--->Ask all directory\n3--->iterate thorugh Directory\n4--->Create a directory\n5--->delete a directory\n6--->Copy a directory\n7--->move a directory")
    command = intValueError()
    while command != -1:
        
        #Opens the current directory:
        if command == 0:
            myoperatingSystem.openDirectory(myoperatingSystem.current_directory)
        #Opens a directory
        elif command == 1:
            myoperatingSystem.openDirectory(input("Enter Address:\t"))
        
        #gives a list of directories
        elif command == 2:
            directoryList = myoperatingSystem.dirlist()
            for i in directoryList.keys():
                print(f"{i}---->{directoryList[i]}")
        
        #iterates a through directories
        elif command == 3:
            myoperatingSystem.iterateDir()
        
        #create a directory
        elif command == 4:
            myoperatingSystem.createDirectory(myoperatingSystem.current_directory)
        
        #delete a directory:
        elif command == 5:
            current_directory_list = myoperatingSystem.dirlist()
            if current_directory_list != None:
                print(current_directory_list)
                myoperatingSystem.deleteDirectory(current_directory_list[int(input("Give directory number:\t"))])
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
        
        #if no command matches
        else:
            print("Invalid Input")
        #takes new command for the further operation..
        command = intValueError()
    pass