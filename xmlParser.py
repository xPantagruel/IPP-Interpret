##########
# File name: xmlParser.py
# Description: Project 2 IPP 2023, FIT VUT
# Author: Matěj Macek (xmacek27)
# Date: 10.04.2023
##########

import xml.etree.ElementTree as ET

class Instr:
    def __init__(self, order, opcode, args):
        self.order = order
        self.opcode = opcode
        self.args = args

class Argument:
    def __init__(self, argType, argValue):
        self.type = argType
        self.value = argValue
        
##
# @brief Class for parsing XML file and creating list of instructions
class InstructionParser:
    def __init__(self, source):
        self.source = source
        self.instructions = []

    def parse(self):
        try:
            tree = ET.parse(self.source)
            root = tree.getroot()
        except:
            exit(31)
        

        self.instructions = []
        if(root.attrib['language'].upper() != 'IPPcode23'.upper()):
            exit(32)
            
        for instrElement in root:
            arg1=arg2=arg3 = 0
            if instrElement.tag != 'instruction' or root.tag != 'program' :
                exit(32)
            
            try:    
                instr_order = int(instrElement.get('order'))
                instr_opcode = str(instrElement.get('opcode'))
            except:
                exit(32)
            
            instrArgs = []
            for argElement in instrElement:
                # check if the arg name is valid
                if argElement.tag != 'arg1' and argElement.tag != 'arg2' and argElement.tag != 'arg3' :
                    exit(32)
                    
                if argElement.tag == 'arg1':
                    arg1 += 1 
                elif argElement.tag == 'arg2':
                    arg2 += 1 
                elif argElement.tag == 'arg3':
                    arg3 += 1 
                else:
                    exit(32)
                    
                argType = argElement.get('type')
                argValue = argElement.text
                argNumber = int(argElement.tag[3:])
                instrArgs.append((argNumber, Argument(argType, argValue)))

            # check arg numbers
            if(arg3 > 1 or arg2 > 1 or arg1 > 1):
                exit(32)
            if(arg3 == 1 and arg2 == 0 and arg1 == 0):
                exit(32)
            elif(arg3 == 1 and arg2 == 1 and arg1 == 0):
                exit(32)
            elif(arg3 == 1 and arg2 == 0 and arg1 == 1):
                exit(32)
            elif(arg3 == 0 and arg2 == 1 and arg1 == 0):
                exit(32)
                
            # sort the arguments by their number
            instrArgs.sort(key=lambda x: x[0])
            instrArgs = [arg[1] for arg in instrArgs]
            
            instr = Instr(instr_order, instr_opcode.upper(), instrArgs)
            self.instructions.append(instr)
        
    def GetInstructions(self):
        self.instructions.sort(key=lambda x: x.order)
        
        # check if there are no duplicate orders or no negative, 0 orders
        orders = []
        for instr in self.instructions:
            if instr.order in orders or instr.order <= 0:                
                exit(32)
            orders.append(instr.order)
        
        return self.instructions