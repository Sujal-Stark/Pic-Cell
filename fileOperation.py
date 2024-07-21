#inbuild Modules
import os
from PIL import Image
from linkedList import LinkedList

#custom class for os management
class OperatingSystem:
    def __init__(self,name) -> None:
        self.name = name
    
    #openDirectory
    def openDirectory(self,address:str):
        LinkedList.addDirectory(address)
        os.chdir(address)
        return True
    
    #delete a directory
    def deleteDirectory(self):
        try:
            fileName = input("Enter File Name:\t")
            if os.path.exists(fileName):
                os.remove(fileName)
            else:
                print("Directory not found🙄")
                self.deleteDirectory()
        except FileNotFoundError as o:
            print(o)
            self.deleteDirectory()
        except PermissionError: print("Permission is denied by the authority")
        finally: return True
    #create a directory
    def createDirectory(self):
        try:
            os.mkdir(input("Enter File Name:\t"))
        except FileExistsError as o:
            print(o)
            self.createDirectory()
        finally: return True

    #current directory contents
    def dirlist(self):
        dirList =  os.listdir(os.getcwd())
        return {i+1:dirList[i] for i in range(len(dirList))}
    
    #iterates and shows the directories in a given directory
    def iterateDir(self):
        while len(os.listdir(os.getcwd())) != 0:
            currentDir = os.getcwd()
            directoryDict = self.dirlist()
            for i in directoryDict.keys():
                print(f"{i}--->{directoryDict[i]}")
            iter = int(input("Enter Directory NUmber: "))#takes the user input
            if iter == 0: break
            targetDirectory = directoryDict[iter]
            currentDir += f"\\{targetDirectory}"
            try:
                self.openDirectory(currentDir)
            except NotADirectoryError:
                #open a directory if its file
                if os.path.isfile(currentDir):
                    if os.path.splitext(currentDir)[1]=='.py':
                        self.openTextFile(currentDir)
                    elif os.path.splitext(currentDir)[1] in ['.jfif','.jpeg']:
                        self.openImage(currentDir)
                    break
        return
    @classmethod
    def openImage(fileName : str):
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
    print("List of operation\n1--->Open a directory\n2--->Ask all directory\n3--->iterate thorugh Directory\n4--->Create a directory\n5--->delete a directory")
    command = intValueError()
    while command != -1:
        
        #Opens a directory
        if command == 1:
            print("Succedd!!")if myoperatingSystem.openDirectory(input("Enter Address:\t"))else print("Unexpected Error Occured")
            command = intValueError()
        
        #gives a list of directories
        elif command == 2:
            directoryList = myoperatingSystem.dirlist()
            for i in directoryList.keys():
                print(f"{i}---->{directoryList[i]}")
            command = intValueError()
        
        #iterates a through directories
        elif command == 3:
            myoperatingSystem.iterateDir()
            command = intValueError()
        
        #creat a directory
        elif command == 4:
            myoperatingSystem.createDirectory()
            command = intValueError()
        
        #delete a directory:
        elif command == 5:
            myoperatingSystem.deleteDirectory()
            command = intValueError()

        #if no command matches
        else:
            print("Invalid Input")
            command = intValueError()
    pass
