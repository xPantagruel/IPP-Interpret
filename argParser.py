import argparse
import sys

class ArgParse:
    if len(sys.argv) != 2:
        exit(10)#todo check if this is correct
    elif sys.argv[1] == "--help":
        print("Help description of your program")
    elif sys.argv[1] == "--source":
        
    elif sys.argv[1] == "--input":
                
                
    
        
    
    
    # parser = argparse.ArgumentParser(description='Description of your program')

    # # --help option
    # parser.add_argument('--help', action='store_true', help='Help description of your program')

    # # --source option
    # parser.add_argument('--source', type=str, metavar='file', help='Input file with XML representation of source code according to section 3.1 and additional definition in section 4')

    # # --input option
    # parser.add_argument('--input', type=str, metavar='file', help='Input file with inputs for the interpretation of the source code')

    # args = parser.parse_args()