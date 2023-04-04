import argparse
import sys
import os

class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Popis programu.')
        self.parser.add_argument('--source', metavar='file',type = str, help='Vstupní soubor s XML reprezentací zdrojového kódu.')
        self.parser.add_argument('--input', metavar='file',type = str, help='Soubor se vstupy pro interpretaci zadaného zdrojového kódu.')
        self.args = self.parser.parse_args()
        self.input_data = None
        self.source_data = None
        
    def run(self):
        # missing arguments with files
        if self.args.source is None and self.args.input is None:
            exit(10)

        if self.args.source:
            with open(self.args.source, 'r') as f:
                self.source_data = f.read()
        else:
            self.source_data = sys.stdin.read()

        if self.args.input:
            with open(self.args.input, 'r') as f:
                self.input_data = f.read()
        else:
            self.input_data = sys.stdin.read()

        #kontrola zda jsou spravne nazvy souboru
        if self.args.source:
            if not os.path.exists(self.args.source):
                exit(11)
        if self.args.input:
            if not os.path.exists(self.args.input):
                exit(11)
                
    def GetSource(self):
        return self.args.source
    
    def GetInput(self):
        return self.args.input
        # #kontrola zda jsou spravne pripony
        # if self.args.source:
        #     if self.args.source[-3:] != 'xml':
        #         exit(31)
        # if self.args.input:
        #     if self.args.input[-3:] != 'src':
        #         exit(31)