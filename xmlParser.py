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
        tree = ET.parse(self.source)
        root = tree.getroot()

        self.instructions = []
        for instr_element in root.findall('instruction'):
            instr_order = int(instr_element.get('order'))
            instr_opcode = instr_element.get('opcode')
            instr_args = []
            for arg_element in instr_element:
                arg_type = arg_element.get('type')
                arg_value = arg_element.text
                instr_args.append(Argument(arg_type, arg_value))

            instr = Instr(instr_order, instr_opcode, instr_args)
            self.instructions.append(instr)
        
    def get_instructions(self):
        self.instructions.sort(key=lambda x: x.order)
        return self.instructions