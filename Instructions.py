class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


class Variable:
    def __init__(self, name, type="nil", value="nil"):
        self.name = name
        self.type = type
        self.value = value


class Instructions:
    def __init__(self, Instructions):
        self.LabelList = []
        self.VariablesList = []
        self.Instructions = Instructions
        self.FrameFlag = "none"
        self.stack = Stack()
        self.TemporaryStack = Stack()
        self.LocalStack = Stack()
        self.NumberOfInstruction = 0

    def InitializateLists(self):
        # todo - add to label num of instruction
        # storing labels names in list
        for i in range(len(self.Instructions)):
            if self.Instructions[i].opcode == "LABEL":
                if self.Instructions[i].args[0].value not in self.LabelList:
                    self.LabelList.append(self.Instructions[i].args[0].value)
                else:
                    exit(52)

        # #storing variables names with atributes in list
        # for i in range(len(self.Instructions)):
        #     if self.Instructions[i].opcode == "DEFVAR":
        #         name = self.Instructions[i].args[0].value
        #         if name is not self.LabelList:
        #             self.VariablesList.append(Variable(name))
        #         else:
        #             exit(52)

        # print(self.VariablesList[0].name)

        # check if label is defined
        for i in range(len(self.Instructions)):
            if self.Instructions[i].opcode in ("JUMP", "JUMPIFEQ", "JUMPIFNEQ"):
                if self.Instructions[i].args[0].value not in self.LabelList:
                    exit(52)

    def InstructionExecution(self):
        self.InitializateLists()

        for i in range(len(self.Instructions)):
            eval("self." + self.Instructions[i].opcode + "()")
            
#-------------------------------------- SEMANTIC CHECK FUNCTIONS --------------------------------------
    def PositionOfVar(self, var):
        for i in range(len(self.VariablesList)):
            if self.VariablesList[i].name == var:
                return i
        exit(54)
#-------------------------------------- INSTRUCTIONS --------------------------------------

    # options: move var symb | move var var
    def MOVE(self):
        i = self.NumberOfInstruction
        if(self.Instructions[i].args[0].type == "var" and self.Instructions[i].args[1].type == "var"):#move var var
            var1 = self.Instructions[i].args[0]
            var2 = self.Instructions[i].args[1]
            
            NumOfVar1 = self.PositionOfVar(var1.value)
            NumOfVar2 = self.PositionOfVar(var2.value)
                  
            if(self.VariablesList[NumOfVar1].type == "nil"):
                self.VariablesList[NumOfVar1].type = self.VariablesList[NumOfVar2].type
                
            if(self.VariablesList[NumOfVar1].type != self.VariablesList[NumOfVar2].type):
                exit(53)
                
            if()
                        
            if(self.Instructions[i].args[1].value == "nil"):
                exit(56)
                
            
            

        if(self.Instructions[i].args[0].type == "var" and self.Instructions[i].args[1].type == "symb"):
            # todo - check if var is defined
            
        
    def CREATEFRAME(self):
        pass

    def PUSHFRAME(self):
        pass

    def POPFRAME(self):
        pass

    # pridam do listu variable a zkontroluju zda uz jsem ji nepridal => tim pak vyresim v prubehu kodu zda je promenna definovana
    def DEFVAR(self):
        name = self.Instructions[self.NumberOfInstruction].args[0].value
        if name is not self.LabelList:
             self.VariablesList.append(Variable(name))
        else:
            exit(52)
    
    def CALL(self):
        pass
    
    def RETURN(self):
        pass
    
    def PUSHS(self):
        pass
    
    def POPS(self):
        pass
    
    def ADD(self):
        pass
    
    def SUB(self):
        pass
    
    def MUL(self):
        pass
    
    def IDIV(self):
        pass
    
    def LT(self):
        pass
    
    def GT(self):
        pass
    
    def EQ(self):
        pass
    
    def AND(self):
        pass
    
    def OR(self):
        pass
    
    def NOT(self):
        pass
    
    def INT2CHAR(self):
        pass
    
    def STRI2INT(self):
        pass
    
    def READ(self):
        pass
    
    def WRITE(self):
        pass
    
    def CONCAT(self):
        pass
    
    def STRLEN(self):
        pass
    
    def GETCHAR(self):
        pass
    
    def SETCHAR(self):
        pass
    
    def TYPE(self):
        pass
    
    def LABEL(self):
        pass
    
    def JUMP(self):
        pass
    
    def JUMPIFEQ(self):
        pass
    
    def JUMPIFNEQ(self):
        pass
    
    
    
        
    