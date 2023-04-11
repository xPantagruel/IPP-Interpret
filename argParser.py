######
# File name: argParser.py
# Description: Projekt 2 do predmetu IPP 2023, FIT VUT
# Athor: Matěj Macek (xmacek27)
# Date: 10.04.2023
######

import argparse
import sys
import os

class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Popis programu.')
        self.parser.add_argument('--source',  help='Vstupní soubor s XML reprezentací zdrojového kódu.')
        self.parser.add_argument('--input', help='Soubor se vstupy pro interpretaci zadaného zdrojového kódu.')
        self.args = self.parser.parse_args()
        self.input = None
        self.inputFile = None
        self.source = None

    def run(self):
        if self.args.source is None and self.args.input is None:
            exit(10)
            
        if self.args.source is not None:
            try:
                self.source = open(self.args.source, 'r')
            except:
                exit(11)
        else:
            self.source = sys.stdin
            
        if self.args.input is not None:
            try:
                self.inputFile = open(self.args.input, 'r')
                self.input = [line.rstrip('\n') for line in self.inputFile]
                # self.input = open(self.args.input, 'r')
                
            except:
                exit(11)
        else:
            self.input = "stdin"           

    def GetSourceFile(self):
        return self.source

    def GetInputFile(self):
        return self.input

    def CloseF(self):
        try:
            self.source.close()
            if self.inputFile is not None:
                self.inputFile.close()
        except:
            pass 