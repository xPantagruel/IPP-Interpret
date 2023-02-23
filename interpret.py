from xmlParser import xmlparse
from argParser import ArgParse
import sys

def main():
    xmlparse()
    parser = ArgParse()
    parser.run()
if __name__ == '__main__':
    main()