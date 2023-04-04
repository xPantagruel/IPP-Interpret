import argparse
import sys
import os

class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Popis programu.')
        self.parser.add_argument('--source', metavar='file', type=str, help='Vstupní soubor s XML reprezentací zdrojového kódu.')
        self.parser.add_argument('--input', metavar='file', type=str, help='Soubor se vstupy pro interpretaci zadaného zdrojového kódu.')
        self.args = self.parser.parse_args()

    def run(self):
        if self.args.source is None and self.args.input is None:
            exit(10)

        if self.args.source:
            with open(self.args.source, 'r') as f:
                source_data = f.read()
        else:
            source_data = sys.stdin.read()

        if self.args.input:
            with open(self.args.input, 'r') as f:
                input_data = f.read()
        else:
            input_data = sys.stdin.read()

        #kontrola zda jsou spravne nazvy souboru
        if self.args.source:
            if not os.path.exists(self.args.source):
                exit(11)
        if self.args.input:
            if not os.path.exists(self.args.input):
                exit(11)

    def GetSourceFile(self):
        if self.args.source:
            return open(self.args.source, 'r')
        else:
            return sys.stdin

    def GetInputFile(self):
        if self.args.input:
            return open(self.args.input, 'r')
        else:
            return sys.stdin
