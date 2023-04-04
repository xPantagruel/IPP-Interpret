from xmlParser import InstructionParser
from argParser import ArgParse
from Core import Interpret
def main():
    # create an instance of the ArgParse class and parse the command-line arguments
    argparser = ArgParse()
    argparser.run()

    # create an instance of the InstructionParser class and parse the source XML file
    xml_parser = InstructionParser(argparser.GetSource())
    xml_parser.parse()
    # get the instructions from the InstructionParser instance
    instructionsList = xml_parser.get_instructions()
    InterpretInstance = Interpret(instructionsList,argparser.GetInput())
    InterpretInstance.Interpretation()

if __name__ == '__main__':
    main()