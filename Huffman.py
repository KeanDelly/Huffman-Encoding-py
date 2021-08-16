
#---------Huffman Algorithm---------#

#Importing All Required Modules
import os
import json
import time
from bitstring import BitArray

'''
A Class denoting a Node in the Huffman Tree
'''
class Node():
    #Defining variables within a Node
    left = None
    right = None
    code = None
    parent = None
    item = None
    frequency = 0

    #Defining the constructor methods
    def __init__(self, i, f, leftNode, RightNode):
        self.item = i
        self.frequency = f
        self.left = leftNode
        self.right = RightNode

    # Defining Set methods
    def setChildren(self, leftNode, rightNode): 
        self.left = leftNode
        self.right = rightNode

    def setCode(self, code):
        self.code = code
        #print('{} has code{}'.format(self.item, (self.code)))
    
    def setParent(self, parentNode):
        self.parent =parentNode

    #Defining method to increment node frequency
    def incrementFrequency(self):
        self.frequency +=1

    # Defining get methods
    def getItem(self):
        return self.item

    def hasParent(self):
        if (self.parent == None):
            return False
        else:
            return True

    def getFrequency(self):
        return self.frequency

    def printNode(self):
        return (self.item, self.frequency)

    def getNode(self):
        return (self.item, self.frequency, self.left, self.right, self.parent)

'''
Function to sort the Huffman Node tree
The sort will maintain a fromat of lowest frequency to highest frequency
'''
def bubbleSort(nodeTree):
    tempvalue = None #Set a Temporary Object Variable = None
    while True: #Loop as long as swaps are being made
        swap = False 
        for i in range(len(nodeTree)-1): #loop through every node in the huffman tree
            if (nodeTree[i].getFrequency()>nodeTree[i+1].getFrequency()): #check If the frequency of one node is greater than the next node
                tempvalue = nodeTree[i] #Set temporary object as current node
                nodeTree[i] = nodeTree[i+1] #let current node  be replaced by the next node
                nodeTree[i+1] = tempvalue #let next node be replaced by the temporary node
                swap = True #Set swap as being true

        if swap == False:
            break
    return(nodeTree) #returns the huffman tree

'''
Function to generate the Huffman Tree
By using the bubblesort to maintain a list of least frequent to most frequent
The function can iterate through the list to create the tree
'''
def generateHuffman(nodeTree):
    pointer1 = 0 #Defining two pointers to keep track of Nodes in the array
    pointer2 = 1
    while True: #Loop until huffman tree is created
        nodeTree = bubbleSort(nodeTree) #Sort the tree from least frequent to most frequent
        if (pointer1 != len(nodeTree)-1): #If the pointers have not reached the end of the list, then get Node data for the 2 pointers
            node1 = nodeTree[pointer1].getNode()
            node2 = nodeTree[pointer2].getNode()
        else:#If the end of the list has been reaches, only get the end node
            node1 = nodeTree[pointer1].getNode()
        if (nodeTree[pointer1] == nodeTree[len(nodeTree)-1]): #Check to see if tree has been completed by checking if the node is the root node
            print("Huffman Generated")
            break
        elif (node1[4] == None and node2[4] == None): #Check if both pointer nodes have a parent, if not then create a new node
            newNodeFrequency = node1[1] + node2[1]#Creating parenty node
            nodeTree.append(Node(None, newNodeFrequency, nodeTree[pointer1], nodeTree[pointer2])) #Add node to list
            nodeTree[pointer1].setParent(nodeTree[len(nodeTree)-1]) #Set parents for both child nodes
            nodeTree[pointer2].setParent(nodeTree[len(nodeTree)-1])

        else:#increment pointers by 1
            pointer1 +=1
            pointer2 +=1
    return(nodeTree)

'''
Function to create the variable length character codes
Uses a Tree traversal to determine a characters code
'''
def createCharacterCodes(node, code = ''):
    if (node.left == None and node.right == None):#Check if node is a leaf node, if yes then set code for the node
        node.setCode(code)
    if (node.left != None ): #If theres a left child node, add a 0 to code and traverse to it
        createCharacterCodes(node.left, code+'0')
    if (node.right !=None):#If theres a right child node, add a 1 to code and traverse to it
        createCharacterCodes(node.right, code+'1')

'''
Function to Collect the character codes from a Node and store it in a hashmap for encoding
'''
def fetchCharacterCodes(nodeTree):
    characterCodes = {} #create a dictionary to map characters to codes
    for node in nodeTree: # for all nodes in the huffman tree
        if (node.code !=""): #if the node is a leaf node
            characterCodes[node.item] = node.code #add the code and character to the dictionary
    return characterCodes #return the dictionary

'''
Function to Collect the character codes from a Node and store it in a hashmap for decoding
'''
def fetchDecodeCode(nodeTree):
    characterCodes = {} #create a dictionary to map characters to codes
    for node in nodeTree: # for all nodes in the huffman tree
        if (node.code !=""): #if the node is a leaf node
            characterCodes[node.code] = node.item #add the code and character to the dictionary
    return characterCodes #return the dictionary

    

'''
function to export the Huffman frequency hashmap to a json file
This is to allow for future decompression
'''
def exportTree(textPath,frequencies,filename):
    brokenfilename = filename.split(".") #splits the filename inputted in order to get the main string
    foldername = brokenfilename[0] #set the name for the folder

    try:
        os.mkdir(foldername) #Create a folder for the compressed file
        os.chdir(os.path.join(textPath, foldername)) #Change the working directory to the created folder
    except OSError:
        print ("Creation of the directory %s failed" % foldername)

    with open(foldername+".json","w") as f: #Create a Json file to store the Huffman Tree
        json.dump(frequencies, f) #Store the huffman Tree in a file
    
    f.close()
        
'''
Function to compress a text file to a bitfile
This uses a pre-created character code system to translate charactersin standard encoding to a variable length encoding
'''
def compressDocument(filepath, filename, characterCodes):
    with open(filename+" Compressed.bin", "wb") as writeFile: #Create the binary file to store the compressed version of text
        with open(os.path.join(filepath, filename+".txt"),'r',encoding='utf-8') as readFile: #Open the original file to read the characters from
            encodedDocument = [] #Create an empty list to store the Bit array
            while True: #Loop until the end of the file
                c = readFile.read(1) #read the next character in he file
                if not c: #If the end of the file is reached then break the loop
                    break
                else:
                    encodedDocument.append(characterCodes[c]) #append the corresponding character code to the array
                    
            CodedDocument = ''.join(encodedDocument) #Concatenate the array into an output for the file
            Document = BitArray(bin=CodedDocument)
            Document.tofile(writeFile) #Write the concatenated array to the file
                            
''' 
Function to decompress a compressed file back to its original state
This uses a pre-created character code system to translate from a bitfile to a text file
'''                            
def decompressFile(filename, characterCodes):
    nextbit = ''
    with open ("../"+filename+".txt","w",encoding='utf-8') as writeFile: #create the new textfile to be written to 
        with open(filename+" Compressed.bin", "rb") as readFile: #Open the binary file to be read from
            compressedText = BitArray(readFile.read()) #Read the binary file into a bitarray
            DataCode =[]#create an empty array for the binary code reading
            text = [] #Create an empty array for the text to be output to the file
            for each in compressedText: #loop through every bit in the bitarray
                if each == True: #Conversion of Binary to string format
                    nextbit = '1'
                else:
                    nextbit ='0'
                DataCode.append(nextbit) #append the next bit to the current code
                for code in characterCodes: # loop through each of the charactercodes
                    #print("Datacode{} code{}".format(DataCode, code))
                    checkCode = ''.join(DataCode)
                    if code == checkCode: #check whether the currently read bits are the same as any of teh character codes
                        text.append(characterCodes[code])

                        #print(code[0])
                        DataCode = []
                        break
            output_text = ''.join(text) #Concatenate the array for output
            writeFile.write(output_text) # write the text to file
                
                
            
'''
Function that imports the Huffman Frequencies in preparation for generating the huffman binary tree
'''
def importTree(filename, nodeTree):
    frequencies = {} #creates a character:frequency dictionary
    with open(filename+".json") as f: #Open the json file and import the frequencies
        frequencies = json.load(f)
    #print(frequencies)
    for key in frequencies: #for each entry in the frequency dictionary, create a huffman tree leaf node
        nodeTree.append(Node(key,frequencies[key], None, None))
    f.close()
    return nodeTree

'''
function to manage the compression of a file
his includes, requesting an input for the filepath of the file to be compressed,
The counting of the huffman frequencies, generation of tree, collection of corresponding codes and 
use of the codes to compress the file
'''
def encodeDocument():
    nodeTree = [] # create an empty huffman tree list
    frequencies = {} # create a character:frequency dictionary
    print("Please enter the path to the directory containing the file you wish to compress")
    print("no quotation marks are needed around the input")
    textPath = input("Input:") #Request input from user
    assert os.path.exists(textPath), "The file was not found at: "+str(textPath) #Ensure the file inputted exists
    os.chdir(textPath)                                                           #Change the working directory to the inputted file
    filename = input("please input the name of the file including postfix(i.e filename.txt)")
    startTime = time.time() # Start a timer
    f = open(filename, "r",encoding='utf-8') #Open the file to be read from
    print("The Size of the file before compression is {} bytes".format(os.path.getsize(textPath)))
    with f: #Using the open file
        while True: #While statement to read through whole file (the base nodes are generated)
            c = f.read(1) #read the character
            if not c: #if there isnt a character then the end of the file has been reached
                print ("End of file")
                break
            if c in frequencies: # if the character is in the frequency dictionary, add 1 to the frequency count
                frequencies[c]+=1
            else: #add the character to the frequencies list
                 frequencies[c]=1
        for key in frequencies: # for each entry in the dictionary, add a leaf node to the huffman tree
            nodeTree.append(Node(key,frequencies[key], None, None))
        print("Base nodes generated")
        nodeTree = bubbleSort(nodeTree) #Sort the huffman tree from lowest frequency to largest frequency
                        
        print("Exporting Tree")
        exportTree(textPath, frequencies,filename) #calls function exporttree
        print("Tree Exported")

        print("Beginning generation of Huffman")    
        generateHuffman(nodeTree) #complete the huffman tree
        print("Huffman generated")

        createCharacterCodes(nodeTree[len(nodeTree)-1]) #calls a function to create codes for all the nodes
        characterCodes = fetchCharacterCodes(nodeTree) #calls a function to obtain the variable length encoding
        print("Character Codes Generated")
            
        brokenfilename = filename.split(".")
        foldername = brokenfilename[0]
        print("Converting Document")
        compressDocument(textPath, foldername, characterCodes) #Calls the compress document function
        endTime = time.time()
        print("Document Compressed")
            
        print("The New Size is: {}")
        print("This achieved a compression rate of {}")
        print("The Program took {}s to perform this task".format(endTime-startTime))
                
    modeSelect()   

'''
function to manage the decompression of a file
This includes, requesting an input for the filepath of the file to be decompressed,
The Import of the huffman frequencies, generation of tree, collection of corresponding codes and 
use of the codes to decompress the file
'''
def decodeDocument():
    nodeTree = [] #Creates an empty Huffman Tree
    textPath = input("Please enter the path to the directory containing the compressed file, no quotation marks are needed around the input")
    assert os.path.exists(textPath), "The file was not found at: "+str(textPath) #ensure that the directory exists
    
    filename = input("please input the name of the folder excluding postfix(i.e FolderName)") 
    os.chdir(os.path.join(textPath, filename)) #set working directory to folder selected
    startTime = time.time() #start timer

    print("Importing Tree")
    nodeTree = importTree(filename, nodeTree) #calls import tree function
    print("Tree Exported")
    
    print("Beginning generation of Huffman")    
    nodeTree = generateHuffman(nodeTree) #calls function to create a huffman tree
    print("Huffman generated")

    createCharacterCodes(nodeTree[len(nodeTree)-1],'') #calls a function to create codes for all the nodes
    characterCodes = fetchDecodeCode(nodeTree) #calls a function to obtain the variable length encoding
    print("Character Codes Generated")
   
    print("Decompressing File")
    decompressFile(filename, characterCodes) # calls the decompress file function
    endTime = time.time() #end the timer
    print("File Decompressed")
    
    print("The file is back to its original size of: {}")
    print("The Program took {}s to perform this task".format(endTime-startTime))
    modeSelect()

'''
function to allow the user to wither encode or decode a document
'''
def modeSelect():
    print("To encode a function input the word 'encode'")
    print("To decode a function input the word 'decode'")
    print("--------------------------------------------")
    mode = input("")
    if (mode == ("encode") or mode == ("e")):
        encodeDocument()
    elif (mode == ("decode")or mode == ("d")):
        decodeDocument()
    else:
        modeSelect()

'''
function to introduce the user to the program
'''
def menu():
    '''Method to output a basic UI to the User'''
    print("----------------------------------")
    print("   Huffman File Size Management   ")
    print("----------------------------------")
    print("This Program is designed to compress and decompress a document")
    print("On compressing a document, a folder is created containing the compressed document and the key required to uncompress it")
    print("--------------------------------------------")
    modeSelect()


menu()