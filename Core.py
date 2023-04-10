######
# File name: core.py
# Description: Projekt 2 do predmetu IPP 2023, FIT VUT
# Athor: Matěj Macek (xmacek27)
# Date: 10.04.2023
######

import sys

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.IsEmpty():
            return self.items.pop()

    def peek(self):
        if not self.IsEmpty():
            return self.items[-1]

    def IsEmpty(self):
        return len(self.items) == 0
    
    def Clears(self):
        self.items = []

class Variable:
    def __init__(self, name, type=None, value=None, isInicialized=False):
        self.name = name
        self.type = type
        self.value = value
        self.isInicialized = isInicialized

class Label:
    def __init__(self, name, value,row):
        self.name = name
        self.value = value
        self.row = row
#------------------------------- Class Interpret --------------------------------
class Interpret():# todo jestli tohle nezrusit a nezavolat jen instanci Insstructions v mainu
    def __init__(self, Instructions, InputType=sys.stdin):
        self.Instructions = Instructions
        self.LabelList = []
        self.InputT = InputType
    
    def InitializateLabelList(self): 
        # initialize label list and check if label is defined
        for i in range(len(self.Instructions)):
            if self.Instructions[i].opcode == "LABEL":
                for j in range(len(self.LabelList)):
                    if self.LabelList[j].name == self.Instructions[i].args[0].value:
                        exit(52)
                
                self.LabelList.append(Label(self.Instructions[i].args[0].value, self.Instructions[i].args[0].value, i-1))
        
    def Interpretation(self):
        self.InitializateLabelList()
        # create instance of class Instructions
        Instr = Instructions(self.Instructions, self.LabelList, self.InputT)
        Instr.Execution()

#------------------------------- Class Instructions --------------------------------
class Instructions:
    def __init__(self, Instructions, LabelList, InputType=sys.stdin):
        self.LabelList = LabelList
        self.GlobalFrameList = [] 
        self.Instructions = Instructions
        self.FrameType = "none"
        self.DataStack = Stack()
        self.CallStack = Stack()
        self.TemporaryFrames = None
        self.LocalFramesStack = Stack()
        self.NumOfInstr = 0
        self.Input = InputType
    
    # execute instructions from list of instructions
    def Execution(self):
        while self.NumOfInstr < len(self.Instructions):
            # print("self." + self.Instructions[self.NumOfInstr].opcode + "()")
            Instr=self.Instructions[self.NumOfInstr].opcode
            
            # create switch case
            if Instr == "MOVE":
                self.NumOfArgCheck(2)
                self.MOVE()
            elif Instr == "CREATEFRAME":
                self.NumOfArgCheck(0)
                self.CREATEFRAME()
            elif Instr == "PUSHFRAME":
                self.NumOfArgCheck(0)
                self.PUSHFRAME()
            elif Instr == "POPFRAME":
                self.NumOfArgCheck(0)
                self.POPFRAME()
            elif Instr == "DEFVAR":
                self.NumOfArgCheck(1)
                self.DEFVAR()
            elif Instr == "CALL":
                self.NumOfArgCheck(1)
                self.CALL()
            elif Instr == "RETURN":
                self.NumOfArgCheck(0)
                self.RETURN()
            elif Instr == "PUSHS":
                self.NumOfArgCheck(1)
                self.PUSHS()
            elif Instr == "POPS":
                self.NumOfArgCheck(1)
                self.POPS()
            elif Instr == "ADD":
                self.NumOfArgCheck(3)
                self.ADD()
            elif Instr == "ADDS":
                self.ADD(StackOption=True)
            elif Instr == "SUB":
                self.NumOfArgCheck(3)
                self.SUB()
            elif Instr == "SUBS":
                self.SUB(StackOption=True)
            elif Instr == "MUL":
                self.NumOfArgCheck(3)
                self.MUL()
            elif Instr == "MULS":
                self.MUL(StackOption=True)
            elif Instr == "IDIV":
                self.NumOfArgCheck(3)
                self.IDIV()
            elif Instr == "IDIVS":
                self.IDIV(StackOption=True)
            elif Instr == "DIV":
                self.DIV()
            elif Instr == "LT":
                self.NumOfArgCheck(3)
                self.LT()
            elif Instr == "LTS":
                self.LT(StackOption=True)
            elif Instr == "GT":
                self.NumOfArgCheck(3)
                self.GT()
            elif Instr == "GTS":
                self.GT(StackOption=True)
            elif Instr == "EQ":
                self.NumOfArgCheck(3)
                self.EQ()
            elif Instr == "EQS":
                self.EQ(StackOption=True)
            elif Instr == "AND":
                self.NumOfArgCheck(3)
                self.AND()
            elif Instr == "ANDS":
                self.AND(StackOption=True)
            elif Instr == "OR":
                self.NumOfArgCheck(3)
                self.OR()
            elif Instr == "ORS":
                self.OR(StackOption=True)
            elif Instr == "NOT":
                self.NumOfArgCheck(2)
                self.NOT()
            elif Instr == "NOTS":
                self.NOT(StackOption=True)
            elif Instr == "INT2CHAR":
                self.NumOfArgCheck(2)
                self.INT2CHAR()
            elif Instr == "INT2CHARS":
                self.INT2CHAR(StackOption=True)
            elif Instr == "STRI2INT":
                self.NumOfArgCheck(3)
                self.STRI2INT()
            elif Instr == "STRI2INTS":
                self.STRI2INT(StackOption=True)
            elif Instr == "READ":
                self.NumOfArgCheck(2)
                self.READ()
            elif Instr == "WRITE":
                self.NumOfArgCheck(1)
                self.WRITE()
            elif Instr == "CONCAT":
                self.NumOfArgCheck(3)
                self.CONCAT()
            elif Instr == "CONCATS":
                self.CONCAT(StackOption=True)
            elif Instr == "STRLEN":
                self.NumOfArgCheck(2)
                self.STRLEN()
            elif Instr == "STRLENS":
                self.STRLEN(StackOption=True)
            elif Instr == "GETCHAR":
                self.NumOfArgCheck(3)
                self.GETCHAR()
            elif Instr == "GETCHARS":
                self.GETCHAR(StackOption=True)
            elif Instr == "SETCHAR":
                self.NumOfArgCheck(3)
                self.SETCHAR()
            elif Instr == "SETCHARS":
                self.SETCHAR(StackOption=True)
            elif Instr == "TYPE":
                self.NumOfArgCheck(2)
                self.TYPE()
            elif Instr == "LABEL":
                self.NumOfArgCheck(1)
                self.LABEL()
            elif Instr == "JUMP":
                self.NumOfArgCheck(1)
                self.JUMP()
            elif Instr == "JUMPIFEQ":
                self.NumOfArgCheck(3)
                self.JUMPIFEQ()
            elif Instr == "JUMPIFEQS":
                self.JUMPIFEQ(StackOption=True)
            elif Instr == "JUMPIFNEQ":
                self.NumOfArgCheck(3)
                self.JUMPIFNEQ()
            elif Instr == "JUMPIFNEQS":
                self.JUMPIFNEQ(StackOption=True)
            elif Instr == "DPRINT":
                self.NumOfArgCheck(1)
                self.DPRINT()
            elif Instr == "EXIT":
                self.NumOfArgCheck(1)
                self.EXIT()
            elif Instr == "BREAK":
                self.NumOfArgCheck(0)
                self.BREAK()
            elif Instr == "CLEARS":
                self.CLEARS()
            elif Instr == "FLOAT2INT":
                self.FLOAT2INT()
            elif Instr == "FLOAT2INTS":
                self.FLOAT2INT(StackOption=True)
            elif Instr == "INT2FLOAT":
                self.INT2FLOAT()
            elif Instr == "INT2FLOATS":
                self.INT2FLOAT(StackOption=True)
            else:
                exit(32)         

            self.NumOfInstr += 1
#----------------------------------------------------------------------------------------------------------
    def NumOfArgCheck(self, numOfArgs):
        if(len(self.Instructions[self.NumOfInstr].args) != numOfArgs):
            exit(32) 
            
    def GetVariable(self, varName, IsInicialized=True ):
        if(varName[0:3] == "GF@"):# check if variable is global
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == varName):
                    if(IsInicialized):
                        if(self.GlobalFrameList[i].isInicialized == False):# check if variable is defined
                            exit(56)
                    return self.GlobalFrameList[i]
                
        elif(varName[0:3] == "LF@"):# check if variable is local
            if(self.LocalFramesStack.IsEmpty()):
                exit(55)

            TopList = self.LocalFramesStack.peek()
            for i in range(len(TopList)):     
                if(TopList[i].name == varName):
                    if(IsInicialized):
                        if(TopList[i].isInicialized == False):# check if variable is defined
                            exit(56)
                    return TopList[i]
                
        elif(varName[0:3] == "TF@"):# check if variable is temporary
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == varName):
                    if(IsInicialized):
                        if(self.TemporaryFrames[i].isInicialized == False):# check if variable is defined
                            exit(56)
                    return self.TemporaryFrames[i]
                
        exit(54)
    
    def SetVariable(self,varName, newVarType, newVarValue ):
        if(varName[0:3] == "GF@"):# check if variable is global
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == varName):
                    self.GlobalFrameList[i].type = newVarType
                    self.GlobalFrameList[i].value = self.ChangeVarType(newVarType, newVarValue)
                    if(self.GlobalFrameList[i].isInicialized == False): # nastaveni inicializace
                        self.GlobalFrameList[i].isInicialized = True
                    return  
                          
        elif(varName[0:3] == "LF@"):# check if variable is local
            if(self.LocalFramesStack == None or self.LocalFramesStack.IsEmpty()):
                exit(55)
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
            for i in range(len(TopList)):     
                if(TopList[i].name == varName):
                    TopList[i].type = newVarType
                    TopList[i].value = self.ChangeVarType(newVarType, newVarValue)
                    if(TopList[i].isInicialized == False):
                        TopList[i].isInicialized = True
                    self.LocalFramesStack.pop()
                    self.LocalFramesStack.push(TopList)
                    return
                
        elif(varName[0:3] == "TF@"):# check if variable is temporary
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == varName):
                    self.TemporaryFrames[i].value = self.ChangeVarType(newVarType, newVarValue)
                    self.TemporaryFrames[i].type = newVarType
                    if(self.TemporaryFrames[i].isInicialized == False):
                        self.TemporaryFrames[i].isInicialized = True
                    return
        else:
            exit(54)
            
        exit(54)
            
    def VarExistsCheck(self, VarName):
        if(VarName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == VarName):
                    return
        elif(VarName[0:3] == "LF@"):
            if(self.LocalFramesStack.IsEmpty()):
                exit(55)
                
            TopList = self.LocalFramesStack.peek()
            for i in range(len(TopList)):     
                if(TopList[i].name == VarName):
                    return

        elif(VarName[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == VarName):
                    return
        else:
            exit(54)
            
        exit(54)
        
    def ChangeVarType(self, newVarType, newVarValue):
        if(newVarType == "bool"):
            if(newVarValue == "true"):
                newVarValue = "true"
            elif(newVarValue == "false"):
                newVarValue = "false"
            else:
                exit(53)
        elif(newVarType == "int"):
            try:
                newVarValue = int(newVarValue)
            except :
                exit(53)
        elif(newVarType == "string"):
            if(newVarValue == None):
                return newVarValue
            try:
                newVarValue = str(newVarValue)
            except :
                exit(53)
        elif(newVarType == "nil"):
            return newVarValue
        elif(newVarType == "float"):
            try:
                newVarValue = float.fromhex(str(newVarValue))
            except :
                exit(53)
        else:
            exit(53)
        return newVarValue
    
    def GetSymbOrVar(self, numOfSymb, StacOption = False):
        if(StacOption):
            symb = self.DataStack.pop()
        else:            
            symbType = self.GetType(numOfSymb)
            
            if(symbType == "var"):
                symb = self.GetVariable(self.GetVarName(numOfSymb))
            elif symbType != "var":
                symb = self.GetSymb(numOfSymb)
            else:
                exit(53)    
        return symb

    def GetType(self, numOfArg):
        i = self.NumOfInstr
        return self.Instructions[i].args[numOfArg].type
    
    def GetValue(self, numOfArg):
        i = self.NumOfInstr
        return self.Instructions[i].args[numOfArg].value
    
    def GetVarName(self,numOfArg, StackOption = False):
        if(StackOption):
            return None
        i = self.NumOfInstr
        return self.Instructions[i].args[numOfArg].value
    
    def GetSymb(self, numOfArg):
        i = self.NumOfInstr
        symbVal = self.Instructions[i].args[numOfArg].value
        
        if(symbVal == None):# empty symb
            return Variable("Symb", self.Instructions[i].args[numOfArg].type)
        
        if(self.Instructions[i].args[numOfArg].type == "string"):
            symbVal = self.ConvertStringLiterals(str(symbVal))
            
        if(self.Instructions[i].args[numOfArg].type == "float"):
            try:
                symbVal = float.fromhex(str(symbVal))
            except :
                exit(53)
        symbVal = self.ChangeVarType(self.Instructions[i].args[numOfArg].type, symbVal)
        Symb = Variable("Symb", self.Instructions[i].args[numOfArg].type, symbVal)
        return Symb
    
    def SetHandler(self, VarName = None, Type = None, Value = None, StackOption = False):
        if(StackOption == True):
            self.DataStack.push(Variable(VarName, Type, Value))
        else:
            self.SetVariable(VarName, Type, Value)
#-------------------------------------- INSTRUCTIONS --------------------------------------
    def MOVE(self):
        # move var symb
        if(self.GetType(0) == "var" and self.GetType(1) != "var"):
            # Check if variable is in frame
            self.VarExistsCheck(self.GetValue(0))

            if(self.GetType(1) == "string"):
                value = self.ConvertStringLiterals(str(self.GetValue(1)))
            else:
                value = self.GetValue(1)
            # copy to var symb value and type
            self.SetVariable(self.GetValue(0), self.GetType(1), value)

        elif(self.GetType(0) == "var" and self.GetType(1) == "var"):
            # Check if variable is in frame
            self.VarExistsCheck(self.GetValue(0))
            self.VarExistsCheck(self.GetValue(1))

            # copy to var value and type
            var = self.GetVariable(self.GetValue(1))
            self.SetVariable(self.GetValue(0), var.type, var.value)      
        
    def CREATEFRAME(self):
        # zahodí případný obsah původního dočasného rámce vytvoří nový dočasný rámec
        self.TemporaryFrames = []
        self.FrameType = "TF"

    def PUSHFRAME(self):
        if(self.FrameType != "TF"):
            exit(55)
        # I need to change TF@ to LF@ and then push it to the stack
        for i in range(len(self.TemporaryFrames)):
            self.TemporaryFrames[i].name = self.TemporaryFrames[i].name.replace("TF@", "LF@")            

        self.LocalFramesStack.push(self.TemporaryFrames)
        self.FrameType = "LF"
            
    def POPFRAME(self):
        if(self.LocalFramesStack.IsEmpty() and self.FrameType != "TF"):
            exit(55)
        else:
            self.TemporaryFrames = self.LocalFramesStack.pop()
            self.FrameType = "TF"
            
        # replace LF@ to TF@
        if(self.TemporaryFrames != None):
            for i in range(len(self.TemporaryFrames)):
                self.TemporaryFrames[i].name = self.TemporaryFrames[i].name.replace("LF@", "TF@")
        else:
            exit(55)
            
    def DEFVAR(self):
        VarName = self.GetVarName(0)
        
        # case 1 - var@GF
        if(VarName[0:3] == "GF@"):
            # check if var is already defined
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == VarName):
                    exit(52)
            
            self.GlobalFrameList.append(Variable(VarName))
                
        # case 2 - var@LF
        elif(VarName[0:3] == "LF@"):
            if(self.LocalFramesStack == None or self.LocalFramesStack.IsEmpty()):
                exit(55)
                    
            TopList = self.LocalFramesStack.peek()
            for i in range(len(TopList)):     
                if(TopList[i].name == VarName):
                    exit(52)
            
            # if var is not defined then I have to create it
            TopList.append(Variable(VarName))
            self.LocalFramesStack.pop()
            self.LocalFramesStack.push(TopList)


        # case 3 - var@TF
        elif(VarName[0:3] == "TF@" and self.FrameType == "TF"):
            if(self.TemporaryFrames == None):
                exit(55)
            # check if var is already defined
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == VarName):
                    exit(52)
            else:
                self.TemporaryFrames.append(Variable(VarName))
        else:
            exit(55)

    def CALL(self):
        # save the current position of the instruction into stack
        self.CallStack.push(self.NumOfInstr)
        
        # find the row of the label
        for i in range(len(self.LabelList)):
            if(self.LabelList[i].name == self.Instructions[self.NumOfInstr].args[0].value):
                self.NumOfInstr = self.LabelList[i].row
                return
        exit(52)
        
    def RETURN(self):
        if(self.CallStack.IsEmpty()):
            exit(56)
        else:
            self.NumOfInstr = self.CallStack.pop()    
              
    def PUSHS(self):
        instr = self.Instructions[self.NumOfInstr]
        # check if its variable(call function to get variable) or symbol
        if(instr.args[0].type == "var"):
            var = self.GetVariable(self.GetVarName(0))
            self.DataStack.push(var)
        else:
            symb = Variable("Symb",instr.args[0].type, instr.args[0].value )# the name is not crucial becouse it doesnt change anything "Symb"
            self.DataStack.push(symb) 
            
    def POPS(self):
        instr = self.Instructions[self.NumOfInstr]
        if(self.DataStack.IsEmpty()):
            exit(56)
        else:
            VarPop = self.DataStack.pop()
            self.SetVariable(instr.args[0].value, VarPop.type, VarPop.value)
            
    # ADD ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ 
    # int check
    def ADD(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1
        
        # check if symb1 and symb2 are both int types
        if(symb1.type == "int" and symb2.type == "int"):
            value = int(symb1.value) + int(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)
        elif(symb1.type == "float" and symb2.type == "float"):
            value = float(symb1.value) + float(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "float", float.hex(value), StackOption)
        else: # set new value to the variable
            exit(53)

    
    def SUB(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1

        # check if symb1 and symb2 are both int types
        if(symb1.type == "int" and symb2.type == "int"):
            #todo check if i should not put here try except
            value = int(symb1.value) - int(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)
        elif(symb1.type == "float" and symb2.type == "float"):
            value = float(symb1.value) - float(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "float", float.hex(value), StackOption)
        else:
            exit(53)
            
              
    def MUL(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        # check if symb1 and symb2 are both int types
        if(symb1.type == "int" and symb2.type == "int"):
            #todo check if i should not put here try except
            value = int(symb1.value) * int(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)
        elif(symb1.type == "float" and symb2.type == "float"):
            value = float(symb1.value) * float(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "float", float.hex(value), StackOption)
        else:
            exit(53)
            
    def IDIV(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        elif(int(symb2.value) == 0):
            exit(57)
        else:
            #todo check if i should not put here try except
            value = int(symb1.value) // int(symb2.value)# todo shouldnt be there only / ?
            self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)
            
    def DIV(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both int types
        if(symb1.type != "float" or symb2.type != "float"):
            exit(53)
        elif(float(symb2.value) == 0):
            exit(57)
        else:
            #todo check if i should not put here try except
            value = float(symb1.value) / float(symb2.value)
            self.SetHandler(self.GetVarName(0, StackOption), "float", value, StackOption)

    def LT(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type):
            exit(53)
        else:
            if(symb1.type == "int" and symb2.type == "int"):
                if(int(symb1.value) < int(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "bool" and symb2.type == "bool"):
                if(symb1.value == "false" and symb2.value == "true"):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "string" and symb2.type == "string"):
                if(str(symb1.value) < str(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "float" and symb2.type == "float"):
                if(float(symb1.value) < float(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            else:
                exit(53)
                
            self.SetHandler(self.GetVarName(0, StackOption), "bool", value, StackOption)
    
    def GT(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type):
            exit(53)
        else:
            if(symb1.type == "int" and symb2.type == "int"):
                if(int(symb1.value) > int(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "bool" and symb2.type == "bool"):
                if(symb1.value == "true" and symb2.value == "false"):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "string" and symb2.type == "string"):
                if(str(symb1.value) > str(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "float" and symb2.type == "float"):
                if(float(symb1.value) > float(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            else:
                exit(53)
                
            self.SetHandler(self.GetVarName(0, StackOption), "bool", value, StackOption)

    def EQ(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        # check if symb1 and symb2 are both int types
        if(symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil"):
            if(symb1.type == "int" and symb2.type == "int"):
                if(int(symb1.value) == int(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "bool" and symb2.type == "bool"):
                if(symb1.value == symb2.value):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "string" and symb2.type == "string"):
                if(str(symb1.value) == str(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "nil" or symb2.type == "nil"):
                if(symb1.type == symb2.type):
                    value = "true"
                else:
                    value = "false"
            elif(symb1.type == "float" and symb2.type == "float"):
                if(float(symb1.value) == float(symb2.value)):
                    value = "true"
                else:
                    value = "false"
            else:
                exit(53)
        else:
            exit(53)
            
        self.SetHandler(self.GetVarName(0, StackOption), "bool", value, StackOption)
            
    def AND(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true" and symb2.value == "true"):
                value = "true"
            else:
                value = "false"
                
            self.SetHandler(self.GetVarName(0, StackOption), "bool", value, StackOption)
            
    def OR(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true" or symb2.value == "true"):
                value = "true"
            else:
                value = "false"
                
            self.SetHandler(self.GetVarName(0, StackOption), "bool", value, StackOption)

    def NOT(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
            
        # check if symb1 is bool type
        if(symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true"):
                value = "false"
            else:
                value = "true"
                
            self.SetHandler(self.GetVarName(0, StackOption), "bool", value, StackOption)

    def INT2CHAR(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
                
        if(symb1.type != "int"):
            exit(53)

        # string outrange
        if(int(symb1.value) > 1114111 or int(symb1.value) < 0):
            exit(58)

        value = chr(int(symb1.value))
        self.SetHandler(self.GetVarName(0, StackOption), "string", value, StackOption)

    
    def STRI2INT(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both int types
        if(symb1.type != "string" or symb2.type != "int"):
            exit(53)
        
        # string outrange
        if(int(symb2.value) >= len(symb1.value) or int(symb2.value) < 0):
            exit(58)        

        value = ord(symb1.value[int(symb2.value)])
        self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)
    
    def READ(self): # todo i have to decide if the input is from file or console
        type = self.GetValue(1)
        if(type == "int"):
            try:
                value = input()
                self.SetVariable(self.GetVarName(0), "int", int(value))
            except Exception:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
                
        elif(type == "string"):
            try:
                value = input()
                self.SetVariable(self.GetVarName(0), "string", str(value))
            except Exception:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
                
        elif(type == "bool"):# todo figure out if the input is not true shoudl i put in false or nil? 
            try:
                value = input()
                if(value.lower() == "true"):
                    value = "true"
                else:
                    value = "false"
                self.SetVariable(self.GetVarName(0), "bool", value)
            except Exception:
                self.SetVariable(self.GetVarName(0), "bool", "false")
        elif(type == "float"):
            try:
                value = input()
                self.SetVariable(self.GetVarName(0), "float", value)
            except Exception:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
        else:
            exit(53)
        
    def ConvertStringLiterals(self,string):
        # var inicialization
        result = ""
        EscapeMode = False
        EscapeCode = ""
        
        # go through every char in string
        for char in string:
            # escape sequence
            if EscapeMode:
                EscapeCode += char
                if len(EscapeCode) == 3:
                    result += chr(int(EscapeCode))
                    EscapeMode = False
                    EscapeCode = ""
            # printable char
            elif char not in [' ', '#', '\\']:
                result += char
            # start of escape sequence
            elif char == '\\':
                EscapeMode = True
            # forbidden # and \
            elif char in ['#', '\\']:
                pass
            else:
                result += chr(ord(char) + 128)
        
        return result

    def WRITE(self):
        symb1 = self.GetSymbOrVar(0)
        
        if(symb1.value == "true"):
            print("true", end="")
        elif(symb1.value == "false"):
            print("false", end="")
        elif(symb1.type == "nil"):
            print("", end="")
        elif(symb1.type == "float"):
            print(float.hex(symb1.value), end="")
        else:
            print(symb1.value, end="")
    
    def CONCAT(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        # check if symb1 and symb2 are both string types
        if(symb1.type != symb2.type or symb1.type != "string"):
            exit(53)
        
        if(symb1.value == None and symb2.value == None):
            value = ""
        elif(symb1.value == None):
            value = symb2.value
        elif(symb2.value == None):
            value = symb1.value
        else:
            value = str(symb1.value) + str(symb2.value)
            
        self.SetHandler(self.GetVarName(0, StackOption), "string", value, StackOption)

    def STRLEN(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        
        # check if symb1 is string
        if(symb1.type != "string"):
            exit(53)
            
        if(symb1.value == None):
            value = 0
        else:
            value = len(symb1.value)  
        
        self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)

    def GETCHAR(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        
        if(StackOption):
            symb1, symb2 = symb2, symb1
        # check if symb1 and symb2 are both string types
        if(symb1.type != "string" or symb2.type != "int"):
            exit(53)
        
        # check if symb2 is in range of symb1
        if(int(symb2.value) < 0 or int(symb2.value) >= len(symb1.value)):
            exit(58)
                
        try:
            value = symb1.value[int(symb2.value)]
        except IndexError:
            exit(58)

        self.SetHandler(self.GetVarName(0, StackOption), "string", value, StackOption)

    def SETCHAR(self, StackOption = False):
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)
        if(StackOption == False):
            var = self.GetVariable(self.GetVarName(0))

        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        if(var.type != symb2.type or var.type != "string" or symb1.type != "int"):
            exit(53)
           
        # check if symb2 is in range
        if(int(symb1.value) < 0 or int(symb1.value) >= len(var.value)):

            exit(58)
        
        # check if symb2 is empty
        if(symb2.value == None):
            exit(58)
            
        # check if len of var is less then symb1 value
        if(len(var.value) < int(symb1.value)):
            exit(58)
        
        value = var.value[:int(symb1.value)] + symb2.value[0] + var.value[int(symb1.value)+1:]

        self.SetHandler(self.GetVarName(0, StackOption), "string", value, StackOption)

    def TYPE(self):
        symbType = self.GetType(1)
        
        # var
        if(symbType == "var"):
            symb = self.GetVariable(self.GetVarName(1),False)
        # symb
        elif symbType != "var": 
            symb = self.GetSymb(1)
        else:
            exit(53)        
            
        if(symb.type != None):
            value = symb.type
        else:
            value = ""
        
        self.SetHandler(self.GetVarName(0), "string", value)
        
    # label is already handled in the beginning of the program
    def LABEL(self):
        pass

    def JUMP(self):
        Label = self.GetValue(0)
        
        for j in range(len(self.LabelList)):
            if(self.LabelList[j].name == Label):
                self.NumOfInstr = self.LabelList[j].row  
                return
            
        exit(52)
  
    def JUMPIFEQ(self, StackOption = False):
        Label = self.GetValue(0)
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        if(symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil"):
            
            if(symb1.type == "string" and symb2.type == "string"):
                Equal = symb1.value == symb2.value
            elif(symb1.type == "int" and symb2.type == "int"):
                try:
                    Equal = int(symb1.value) == int(symb2.value)
                except:
                    exit(53)
            elif(symb1.type == "bool" and symb2.type == "bool"):
                try:
                    Equal = symb1.value == symb2.value
                except:
                    exit(53)
            elif(symb1.type == "nil" or symb2.type == "nil"):
                if(symb1.value == symb2.value):
                    Equal = True 
                else:
                    Equal = False
            else:
                exit(52)
            
            for j in range(len(self.LabelList)):
                if(self.LabelList[j].name == Label):
                    if(Equal == True):
                        self.NumOfInstr = self.LabelList[j].row  
                    return
            exit(52)
        else:
            exit(53)
                
    def JUMPIFNEQ(self, StackOption = False):
        Label = self.GetValue(0)
        symb1 = self.GetSymbOrVar(1, StackOption)
        symb2 = self.GetSymbOrVar(2, StackOption)

        if(StackOption):
            symb1, symb2 = symb2, symb1
            
        if(symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil"):
            
            if(symb1.type == "string" and symb2.type == "string"):
                Equal = symb1.value != symb2.value
            elif(symb1.type == "int" and symb2.type == "int"):
                try:
                    Equal = int(symb1.value) != int(symb2.value)
                except:
                    exit(53)
            elif(symb1.type == "bool" and symb2.type == "bool"):
                try:
                    Equal = symb1.value != symb2.value
                except:
                    exit(53)
            elif(symb1.type == "nil" or symb2.type == "nil"):
                if(symb1.value != symb2.value):
                    Equal = True 
                else:
                    Equal = False
            else:
                exit(52)
            
            for j in range(len(self.LabelList)):
                if(self.LabelList[j].name == Label):
                    if(Equal == True):
                        self.NumOfInstr = self.LabelList[j].row  
                    return
            exit(52)
        else:
            exit(53)
    
    def EXIT(self):
        symb = self.GetSymbOrVar(0)
        
        if(symb.type != "int"):
            exit(53)
        
        try:
            code = int(symb.value)
        except:
            exit(57)
            
        if(code >= 0 and code <= 49):
            exit(code)
        else:
            exit(57)        

    def BREAK(self):# todo test it
        print("NumOfInstr: ", self.NumOfInstr, file=sys.stderr)
        print("GlobalFrameList: ", self.GlobalFrameList, file=sys.stderr)
        print("TempFrameList: ", self.TemporaryFrames, file=sys.stderr)
        print("CallStack: ", self.CallStack, file=sys.stderr)
        print("DataStack: ", self.DataStack, file=sys.stderr)
        print("LabelList: ", self.LabelList, file=sys.stderr)

    def DPRINT(self) :
        symb = self.GetSymbOrVar(0)
            
        print(symb.value, file=sys.stderr)
              
    def CLEARS(self):
        self.DataStack.Clears()
    
    def FLOAT2INT(self, StackOption = False):
        symb = self.GetSymbOrVar(1, StackOption)
        
        if(symb.type != "float"):
            exit(53)
        
        try:
            value = int(symb.value)
        except:
            exit(57)
        
        self.SetHandler(self.GetVarName(0, StackOption), "int", value, StackOption)

    def INT2FLOAT(self, StackOption = False):
        symb = self.GetSymbOrVar(1,StackOption)
        
        if(symb.type != "int"):
            exit(53)
        
        try:
            value = float.hex(float(symb.value))
        except:
            exit(57)
        
        self.SetHandler(self.GetVarName(0, StackOption), "float", value, StackOption)