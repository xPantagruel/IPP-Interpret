import xml.etree.ElementTree as ET

class Instr:
    def __init__(self, order, opcode, args):
        self.order = order
        self.opcode = opcode
        self.args = args

class Argument:
    def __init__(self, arg_type, arg_value):
        self.type = arg_type
        self.value = arg_value
        
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
        for instr_element in root:
            if instr_element.tag != 'instruction' or root.tag != 'program' :
                exit(32)
            
            try:    
                instr_order = int(instr_element.get('order'))
                instr_opcode = str(instr_element.get('opcode'))
            except:
                exit(32)
            
            instr_args = []
            for arg_element in instr_element:
                # check if the arg name is valid
                if arg_element.tag != 'arg1' and arg_element.tag != 'arg2' and arg_element.tag != 'arg3' :
                    exit(32)
                    
                arg_type = arg_element.get('type')
                arg_value = arg_element.text
                arg_number = int(arg_element.tag[3:])
                instr_args.append((arg_number, Argument(arg_type, arg_value)))

            # sort the arguments by their number
            instr_args.sort(key=lambda x: x[0])
            instr_args = [arg[1] for arg in instr_args]
            
            instr = Instr(instr_order, instr_opcode.upper(), instr_args)
            self.instructions.append(instr)
        
    def get_instructions(self):
        self.instructions.sort(key=lambda x: x.order)
        
        # check if there are no duplicate orders or no negative, 0 orders
        orders = []
        for instr in self.instructions:
            if instr.order in orders or instr.order <= 0:                
                exit(32)
            orders.append(instr.order)
        
            
        return self.instructions