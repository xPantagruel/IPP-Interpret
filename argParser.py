import argparse
import sys
import os

class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Popis programu.')
        self.parser.add_argument('--source', metavar='file', type=str, help='Vstupní soubor s XML reprezentací zdrojového kódu.')
        self.parser.add_argument('--input', metavar='file', type=str, help='Soubor se vstupy pro interpretaci zadaného zdrojového kódu.')
        self.args = self.parser.parse_args()
        self.input = None
        self.source = None

    def run(self):
        if self.args.source is None and self.args.input is None:
            exit(10)

        if self.args.source:
            with open(self.args.source, 'r') as f:
                self.source = f
        else:
            self.source = sys.stdin
        if self.args.input:
            with open(self.args.input, 'r') as f:
                self.input = f
        else:
            self.input = sys.stdin

        #kontrola zda jsou spravne nazvy souboru
        if self.args.source:
            if not os.path.exists(self.args.source):
                exit(11)
        if self.args.input:
            if not os.path.exists(self.args.input):
                exit(11)

    def GetSourceFile(self):
        return self.source

    def GetInputFile(self):
        return self.input
