
----------Huffman Compression and Decompression----------

--Program Description--
This Implementation of the Huffman algorithm is designed to compress and decompress text files.
For an average text file a compression of 50-60% of the original size can be expected.

--Program Requirements--
This Program requires the following 3rd party python Modules;
 - json
 - bitstring

This implementation was written in Python 3.9.2(64bit) on Windows 10
The program should work on other Operating systems and lower python3 versions
Although Errors may occur if attempts are made to do so

--Running the Program--
When run, the program will present the user with a menu
This will consist of the option to encode or decode a document
To proceed from this menu the string input of 'encode' or'e', 'decode' or 'd'
The Program will then ask for the user to input a filepath, this should be to the folder containing the file that is to be compressed
The last input request will be to input the filename, this should include the '.txt' postfix (Only when compressing a document)

Once Compressed, The original file will still remain,
to ensure a successful decompression it should be deleted
although it should still work if this is not complete

NOTE: Before Compressing a file, ensure there is no folder possesing the same name within the parent folder
      as this will interfere with the compression

