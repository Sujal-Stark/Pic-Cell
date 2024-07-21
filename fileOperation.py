#inbuild Modules
import os
from PIL import Image
from linkedList import LinkedList
import shutil

#custom class for os management
class OperatingSystem:
    def __init__(self,name) -> None:
        self.name = name
    
    #openDirectory
    def openDirectory(self,address:str):
        try:
            os.chdir(address)
        except OSError:
            print("Unexpected error occurred")
        finally:
            return
    
    #delete a directory
    def deleteDirectory(self,fileName):
        try:
            if os.path.exists(fileName):
                shutil.rmtree(fileName)
            else:
                print("Directory not found🙄")
                self.deleteDirectory()
        except FileNotFoundError as o:
            print(o)
            self.deleteDirectory()
        except PermissionError: print("Permission is denied by the authority")
        finally: return True
    #create a directory
    def createDirectory(self,current_directory):
        self.openDirectory(current_directory)
        try:
            os.mkdir(input("Enter File Name:\t"))
        except FileExistsError as o:
            print(o)
            self.createDirectory()
        finally: return True

    #current directory contents
    def dirlist(self):
        self.directoryList =  os.listdir(os.getcwd())
        return {i+1:self.directoryList[i] for i in range(len(self.directoryList))}
    
    #iterates and shows the directories in a given directory
    def iterateDir(self):
        while len(os.listdir(os.getcwd())) != 0:
            currentDir = os.getcwd()
            directoryDict = self.dirlist()
            for i in directoryDict.keys():
                print(f"{i}--->{directoryDict[i]}")
            iter = int(input("Enter Directory NUmber: "))#takes the user input
            if iter == 0:
                if os.path.isdir(currentDir):
                    self.current_directory = currentDir
                break
            elif iter == -1:
                break
            targetDirectory = directoryDict[iter]
            currentDir += f"\\{targetDirectory}"
            if os.path.isdir(currentDir):
                self.openDirectory(currentDir)
                self.current_directory = os.getcwd()
            elif os.path.isfile(currentDir):
                if os.path.splitext(currentDir)[1]=='.py':
                    self.openTextFile(currentDir)
                elif os.path.splitext(currentDir)[1] in ['.jfif','.jpeg','.png']:
                    self.openImage(currentDir)
                break
        return
    @classmethod
    def openImage(cls,fileName : str):
        iamge = Image.open(fileName)
        iamge.show()
    
    @classmethod
    def openTextFile(fileName : str):
        print("\nOpening your file....\n")
        try:
            with open(fileName,'r') as file:
                print(file.read())
        except FileNotFoundError as o:
            print(o)
    
    def copy(self,directory:str):
        self.openDirectory(input("Open a directory:\t"))
        self.iterateDir() #by this method the desired directory can be reached

         #handles if the path is a file
        if os.path.isfile(directory):
            try:
                shutil.copy(directory,self.current_directory)
            except FileNotFoundError:
                return f"File {directory} is not found.."
            except PermissionError:
                return f"Permission Denied.."
            except OSError as o:
                return f"Os Error: {o}"

        #hanles if the path is a directory
        elif os.path.isdir(directory):
            try:
                shutil.copytree(directory,input("target_directory"))
            except PermissionError as o:
                return f"Permission Denied {o}"
            except OSError as o:
                return f"Os Error: {o}"
        else:
            print("d")
            return "unexpected error occurred"
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
    print("List of operation\n1--->Open a directory\n2--->Ask all directory\n3--->iterate thorugh Directory\n4--->Create a directory\n5--->delete a directory\n6--->Copy a directory")
    command = intValueError()
    while command != -1:
        
        #Opens a directory
        if command == 1:
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
            print(current_directory_list)
            myoperatingSystem.deleteDirectory(current_directory_list[int(input("Give directory number:\t"))])
        
        #copy a file/ folder from current directory to another
        elif command == 6:
            print(myoperatingSystem.copy(myoperatingSystem.current_directory))

        #if no command matches
        else:
            print("Invalid Input")
        #takes new command for the further operation..
        command = intValueError()
    pass