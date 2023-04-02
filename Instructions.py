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


class Variable:
    def __init__(self, name, type="nil", value="nil"):
        self.name = name
        self.type = type
        self.value = value

class Label:
    def __init__(self, name, value,row):
        self.name = name
        self.value = value
        self.row = row

class Instructions:
    def __init__(self, Instructions):
        self.LabelList = []
        self.GlobalFrameList = [] 
        self.Instructions = Instructions
        self.FrameType = "none"
        self.DataStack = Stack()
        self.CallStack = Stack()
        self.TemporaryFrames = None
        self.LocalFramesStack = None
        self.NumberOfInstruction = 0

    def InitializateLists(self):
        
        # initialize label list and check if label is defined
        for i in range(len(self.Instructions)):
            if self.Instructions[i].opcode == "LABEL":
                if self.Instructions[i].args[0].value not in self.LabelList:
                    self.LabelList.append(Label(self.Instructions[i].args[0].value, self.Instructions[i].args[0].value, i))
                else:
                    exit(52)

        # # #todo check if label is defined
        # # for i in range(len(self.Instructions)):
        # #     if self.Instructions[i].opcode in ("JUMP", "JUMPIFEQ", "JUMPIFNEQ"):
        # #         if self.Instructions[i].args[0].value not in self.LabelList:
        # #             exit(52)
    
    # execute instructions from list of instructions
    def InstructionExecution(self):
        self.InitializateLists()
        while self.NumberOfInstruction < len(self.Instructions):
            print("self." + self.Instructions[self.NumberOfInstruction].opcode + "()")
            eval("self." + self.Instructions[self.NumberOfInstruction].opcode + "()")
            self.NumberOfInstruction += 1
            
#-------------------------------------- FUNCTIONS --------------------------------------
    def PositionOfVar(self, var):
        for i in range(len(self.GlobalFrameList)):
            if self.GlobalFrameList[i].name == var:
                return i
        exit(54)
    
    # todo create function that will check if variable is in specific frame and then it will return the variable from the frame    
    def GetVariable(self, var):
        if(var == "GF"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == var):
                    return self.GlobalFrameList[i]
        elif(var == "LF"):
            if(self.FrameType != "LF"):
                exit(55)
                
            for i in range(len(self.LocalFramesStack)):
                if(self.LocalFramesStack[0][i].name == var):
                    return self.LocalFramesStack[0][i]
        elif(var == "TF"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == var):
                    return self.TemporaryFrames[i]
        else:
            exit(54)
    
    # todo i have to add new type of variable to the frame
    def SetVariable(self,var,instruction = None):
        InstrName = instruction.value
        if(InstrName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):                
                if(self.GlobalFrameList[i].name == InstrName):
                    self.GlobalFrameList[i].type = var.type
                    self.GlobalFrameList[i].value = var.value
                    return
            exit(54)
        elif(InstrName[0:3] == "LF@"):
            if(self.FrameType != "LF"):
                exit(55)
                
            for i in range(len(self.LocalFramesStack)):
                if(self.LocalFramesStack[0][i].name == InstrName):
                    self.LocalFramesStack[0][i].type = var.type
                    self.LocalFramesStack[0][i].value = var.value
                    return
            exit(54)    
        elif(InstrName[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == InstrName):
                    self.TemporaryFrames[i].value = var.value
                    self.TemporaryFrames[i].type = var.type
                    return
            exit(54)
        else:
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
                  
            if(self.GlobalFrameList[NumOfVar1].type == "nil"):
                self.GlobalFrameList[NumOfVar1].type = self.GlobalFrameList[NumOfVar2].type
                self.GlobalFrameList[NumOfVar1].value = self.GlobalFrameList[NumOfVar2].value
                
            if(self.GlobalFrameList[NumOfVar1].type != self.GlobalFrameList[NumOfVar2].type):
                exit(53)
                
            if(self.Instructions[i].args[1].value == "nil"):
                exit(56)
        else: #move var symb
            var = self.Instructions[i].args[0]
            symb = self.Instructions[i].args[1]
            
            NumOfVar = self.PositionOfVar(var.value)
            
            if(self.GlobalFrameList[NumOfVar].type == "nil"):
                self.GlobalFrameList[NumOfVar].type = symb.type
                self.GlobalFrameList[NumOfVar].value = symb.value
                
            if(self.GlobalFrameList[NumOfVar].type != symb.type):
                exit(53)
                
            if(symb.value == "nil"):
                exit(56)
                            
        # if(self.Instructions[i].args[0].type == "var" and self.Instructions[i].args[1].type == "symb"):
            # todo - check if var is defined
            
        
    def CREATEFRAME(self):
        # zahodí případný obsah původního dočasného rámce vytvoří nový dočasný rámec
        self.TemporaryFrames = []
        self.FrameType = "TF"

# todo TF bude po provedení instrukce nedefinován a je třeba jej před dalším
# todo použitím vytvořit pomocí CREATEFRAME. Pokus o přístup k nedefinovanému rámci vede na
# todo chybu 55.
    def PUSHFRAME(self):
        # I need to change TF@ to LF@ and then push it to the stack
        for i in range(len(self.TemporaryFrames)):
            self.TemporaryFrames[i].name = self.TemporaryFrames[i].name.replace("TF@", "LF@")

        self.LocalFramesStack.push(self.TemporaryFrames)
        self.FrameType = "LF"
        
    def POPFRAME(self):
        if(self.LocalFramesStack.isEmpty() and self.FrameType != "TF"):
            exit(55)
        else:
            self.TemporaryFrames = self.LocalFramesStack.pop()
            self.FrameType = "TF"
            
            # replace LF@ to TF@
            for i in range(len(self.TemporaryFrames)):
                self.TemporaryFrames[i].name = self.TemporaryFrames[i].name.replace("LF@", "TF@")
            
    def DEFVAR(self):
        # I have 3 cases - var@GF, var@LF, var@TF
        # first thing I have to check which frame is active and check symbols before '@' then check if it suits the frame the frame type, then I have to create variable in the frame
        # second thing of I have to check if the variable is already defined and if yes then I have to exit with error code 52
        VarName = self.Instructions[self.NumberOfInstruction].args[0].value
        #check var type 
        # case 1 - var@GF
        if(VarName[0:3] == "GF@"):
            # check if var is already defined
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == VarName):
                    exit(52)
            
            self.GlobalFrameList.append(Variable(VarName))
                
        # case 2 - var@LF
        elif(VarName[0:3] == "LF@" and self.FrameType == "LF"):
            # todo check if i have to check if LF is defined and if not then exit with error code 55
            if(self.LocalFramesStack == None):
                exit(55)
            # check if var is already defined
            for i in range(len(self.LocalFramesStack)):
                if(self.LocalFramesStack[0][i].name == VarName):#todo check if it is correct 
                    exit(52)
            
            # if var is not defined then I have to create it
            self.LocalFramesStack[0].append(Variable(VarName))

        # case 3 - var@TF
        elif(VarName[0:3] == "TF@" and self.FrameType == "TF"):
            # todo check if i have to check if LF is defined and if not then exit with error code 55
            if(self.TempFrame == None):
                exit(55)
            # check if var is already defined
            for i in range(len(self.TempFrame)):
                if(self.TempFrame[i].name == VarName):
                    exit(52)
            else:
                self.TempFrame.append(Variable(VarName))
        else:
            exit(55)
    
    # update NumberOfInstruction to the row of the labelv
    def CALL(self):
        # save the current position of the instruction into stack
        self.CallStack.push(self.NumberOfInstruction)
        
        self.NumberOfInstruction = self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
    
    def RETURN(self):
        if(self.CallStack.isEmpty()):
            exit(56)
        else:
            self.NumberOfInstruction = self.CallStack.pop()    
              
#Uloží hodnotu ⟨symb⟩ na datový zásobník.
# todo check if i should push it like this => only the value to the Datastack
    def PUSHS(self):
        instr = self.Instructions[self.NumberOfInstruction]
        # check if its variable(call function to get variable) or symbol
        if(instr.args[0].type == "var"):
            var = self.GetVariable(instr.args[0].value)
            self.DataStack.push(var.value)
        else:
            symb = Variable("Symb",instr.args[0].type, instr.args[0].value )# the name is not crucial becouse it doesnt change anything "Symb"
            self.DataStack.push(symb) 
            
    def POPS(self):
        instr = self.Instructions[self.NumberOfInstruction]
        if(self.DataStack.IsEmpty()):
            exit(56)
        else:
            VarPop = self.DataStack.pop()
            self.SetVariable(VarPop,instr.args[0])
    
    # ADD ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ 
    # int check
    def ADD(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]

        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = int(symb1.value) + int(symb2.value)
        else: 
            exit(53)
        print("log:" + str(self.GlobalFrameList[self.PositionOfVar(var.value)].value))
                    
    def SUB(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = int(symb1.value) - int(symb2.value)
        else: 
            exit(53)
            
        print("log:" + str(self.GlobalFrameList[self.PositionOfVar(var.value)].value))
            
            
                    
    def MUL(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
                    
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = int(symb1.value) * int(symb2.value)
        else: 
            exit(53)
            
        print("log:" + str(self.GlobalFrameList[self.PositionOfVar(var.value)].value))

    def IDIV(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
            
        # division by zero
        if symb2.value == 0:
            exit(57)
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = int(symb1.value) // int(symb2.value)
        else: 
            exit(53)
            
        print("log:" + str(self.GlobalFrameList[self.PositionOfVar(var.value)].value))
#     LT/GT/EQ ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Relační operátory menší, větší, rovno
# Instrukce vyhodnotí relační operátor mezi ⟨symb1⟩ a ⟨symb2⟩ (stejného typu; int, bool nebo
# string) a do ⟨var⟩ zapíše výsledek typu bool (false při neplatnosti nebo true v případě platnosti
# odpovídající relace). Řetězce jsou porovnávány lexikograficky a false je menší než true. Pro
# výpočet neostrých nerovností lze použít AND/OR/NOT. S operandem typu nil (další zdrojový
# operand je libovolného typu) lze porovnávat pouze instrukcí EQ, jinak chyba 53.
    
    def LT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int" or symb2.type == "bool" and symb1.type == "bool" or symb2.type == "string" and symb1.type == "string" or symb2.type == "nil" or symb1.type == "nil":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value < symb2.value
        else: 
            exit(53)
    
    def GT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int" or symb2.type == "bool" and symb1.type == "bool" or symb2.type == "string" and symb1.type == "string" or symb2.type == "nil" or symb1.type == "nil":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value > symb2.value
        else: 
            exit(53)
    
    def EQ(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int" or symb2.type == "bool" and symb1.type == "bool" or symb2.type == "string" and symb1.type == "string" or symb2.type == "nil" or symb1.type == "nil":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value == symb2.value
        else: 
            exit(53)
    
#     AND/OR/NOT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Základní booleovské operátory
# Aplikuje konjunkci (logické A)/disjunkci (logické NEBO) na operandy typu bool ⟨symb1⟩ a
# ⟨symb2⟩ nebo negaci na ⟨symb1⟩ (NOT má pouze 2 operandy) a výsledek typu bool zapíše do
# ⟨var⟩.

    def AND(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "bool" and symb1.type == "bool":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value and symb2.value
        else: 
            exit(53)        
    
    def OR(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "bool" and symb1.type == "bool":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value or symb2.value
        else: 
            exit(53)
    
    def NOT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "bool" and symb1.type == "bool":
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = not symb1.value
        else: 
            exit(53)
    
#     INT2CHAR ⟨var⟩ ⟨symb⟩ Převod celého čísla na znak
# Číselná hodnota ⟨symb⟩ je dle Unicode převedena na znak, který tvoří jednoznakový řetězec
# přiřazený do ⟨var⟩. Není-li ⟨symb⟩ validní ordinální hodnota znaku v Unicode (viz funkce chr
# v Python 3), dojde k chybě 58.
    def INT2CHAR(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb = self.Instructions[i].args[1]
        
        # check if symb1 and symb2 are variables
        if symb.type == "var":
            symb = self.GlobalFrameList[self.PositionOfVar(symb.value)]
        
        if var.type == "var" and symb.type == "int":
            try:
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "string"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = chr(symb.value)
            except ValueError:
                exit(58)
        else: 
            exit(53)
    
#     STRI2INT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Ordinální hodnota znaku
# Do ⟨var⟩ uloží ordinální hodnotu znaku (dle Unicode) v řetězci ⟨symb1⟩ na pozici ⟨symb2⟩
# (indexováno od nuly). Indexace mimo daný řetězec vede na chybu 58. Viz funkce ord v Python 3.
    def STRI2INT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "string":
            try:
                self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
                self.GlobalFrameList[self.PositionOfVar(var.value)].value = ord(symb1.value[symb2.value])
            except ValueError:
                exit(58)
        else: 
            exit(53)
    
#     READ ⟨var⟩ ⟨type⟩ Načtení hodnoty ze standardního vstupu
# Načte jednu hodnotu dle zadaného typu ⟨type⟩ ∈ {int, string, bool} a uloží tuto hodnotu do
# proměnné ⟨var⟩. Načtení proveďte vestavěnou funkcí input() (či analogickou) jazyka Python 3,
# pak proveďte konverzi na specifikovaný typ ⟨type⟩. Při převodu vstupu na typ bool nezáleží na
# velikosti písmen a řetězec ”
# true“ se převádí na bool@true, vše ostatní na bool@false. V případě
# chybného nebo chybějícího vstupu bude do proměnné ⟨var⟩ uložena hodnota nil@nil
    def READ(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        type = self.Instructions[i].args[1]
        
        if var.type == "var" and type.type == "type":
            if type.value == "int":
                try:
                    self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
                    self.GlobalFrameList[self.PositionOfVar(var.value)].value = int(input())
                except ValueError:
                    self.GlobalFrameList[self.PositionOfVar(var.value)].type = "nil"
                    self.GlobalFrameList[self.PositionOfVar(var.value)].value = "nil"
            elif type.value == "string":
                try:
                    self.GlobalFrameList[self.PositionOfVar(var.value)].type = "string"
                    self.GlobalFrameList[self.PositionOfVar(var.value)].value = input()
                except ValueError:
                    self.GlobalFrameList[self.PositionOfVar(var.value)].type = "nil"
                    self.GlobalFrameList[self.PositionOfVar(var.value)].value = "nil"
            elif type.value == "bool":
                try:
                    self.GlobalFrameList[self.PositionOfVar(var.value)].type = "bool"
                    self.GlobalFrameList[self.PositionOfVar(var.value)].value = input()
                    if self.GlobalFrameList[self.PositionOfVar(var.value)].value.lower() == "true":
                        self.GlobalFrameList[self.PositionOfVar(var.value)].value = True
                    else:
                        self.GlobalFrameList[self.PositionOfVar(var.value)].value = False
                except ValueError:
                    self.GlobalFrameList[self.PositionOfVar(var.value)].type = "nil"
                    self.GlobalFrameList[self.PositionOfVar(var.value)].value = "nil"
        else: 
            exit(53)
    
#     WRITE ⟨symb⟩ Výpis hodnoty na standardní výstup
# Vypíše hodnotu ⟨symb⟩ na standardní výstup. Až na typ bool a hodnotu nil@nil je formát
# výpisu kompatibilní s příkazem print jazyka Python 3 s doplňujícím parametrem end='' (zamezí dodatečnému odřádkování). Pravdivostní hodnota se vypíše jako true a nepravda jako
# false. Hodnota nil@nil se vypíše jako prázdný řetězec.

    def WRITE(self):
        i = self.NumberOfInstruction
        symb = self.Instructions[i].args[0]
        
        # check if symb1 and symb2 are variables
        if symb.type == "var":
            symb = self.GlobalFrameList[self.PositionOfVar(symb.value)]
        
        if symb.type == "int" or symb.type == "string" or symb.type == "bool":
            print(symb.value, end='')
        elif symb.type == "nil":
            print('', end='')
        else: 
            exit(53)
    
#     CONCAT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Konkatenace dvou řetězců
# Do proměnné ⟨var⟩ uloží řetězec vzniklý konkatenací dvou řetězcových operandů ⟨symb1⟩ a
# ⟨symb2⟩ (jiné typy nejsou povoleny).
    def CONCAT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb1.type == "string" and symb2.type == "string":
            self.GlobalFrameList[self.PositionOfVar(var.value)].type = "string"
            self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value + symb2.value
        else: 
            exit(53)
# STRLEN ⟨var⟩ ⟨symb⟩ Zjisti délku řetězce
# Zjistí počet znaků (délku) řetězce v ⟨symb⟩ a tato délka je uložena jako celé číslo do ⟨var⟩.
    def STRLEN(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb = self.Instructions[i].args[1]
        
        # check if symb1 and symb2 are variables
        if symb.type == "var":
            symb = self.GlobalFrameList[self.PositionOfVar(symb.value)]
        
        if var.type == "var" and symb.type == "string":
            self.GlobalFrameList[self.PositionOfVar(var.value)].type = "int"
            self.GlobalFrameList[self.PositionOfVar(var.value)].value = len(symb.value)
        else: 
            exit(53)
#     GETCHAR ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Vrať znak řetězce
# Do ⟨var⟩ uloží řetězec z jednoho znaku v řetězci ⟨symb1⟩ na pozici ⟨symb2⟩ (indexováno celým
# číslem od nuly). Indexace mimo daný řetězec vede na chybu 58.
    def GETCHAR(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb1.type == "string" and symb2.type == "int":
            if int(symb2.value) < 0 or int(symb2.value) >= len(symb1.value):
                exit(58)
            self.GlobalFrameList[self.PositionOfVar(var.value)].type = "string"
            self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb1.value[int(symb2.value)]
        else: 
            exit(53)

# SETCHAR ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Změň znak řetězce
# Zmodifikuje znak řetězce uloženého v proměnné ⟨var⟩ na pozici ⟨symb1⟩ (indexováno celočíselně
# od nuly) na znak v řetězci ⟨symb2⟩ (první znak, pokud obsahuje ⟨symb2⟩ více znaků). Výsledný
# řetězec je opět uložen do ⟨var⟩. Při indexaci mimo řetězec ⟨var⟩ nebo v případě prázdného
# řetězce v ⟨symb2⟩ dojde k chybě 58.    
    def SETCHAR(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb1.type == "int" and symb2.type == "string":
            if symb2.value == "":
                exit(58)
            if int(symb1.value) < 0 or int(symb1.value) >= len(self.GlobalFrameList[self.PositionOfVar(var.value)].value):
                exit(58)
            self.GlobalFrameList[self.PositionOfVar(var.value)].value = self.GlobalFrameList[self.PositionOfVar(var.value)].value[:int(symb1.value)] + symb2.value[0] + self.GlobalFrameList[self.PositionOfVar(var.value)].value[int(symb1.value)+1:]
        else: 
            exit(53)

# TYPE ⟨var⟩ ⟨symb⟩ Zjisti typ daného symbolu
# Dynamicky zjistí typ symbolu ⟨symb⟩ a do ⟨var⟩ zapíše řetězec značící tento typ (int, bool,
# string nebo nil). Je-li ⟨symb⟩ neinicializovaná proměnná, označí její typ prázdným řetězcem
    def TYPE(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb = self.Instructions[i].args[1]
        
        # check if symb1 and symb2 are variables
        if symb.type == "var":
            symb = self.GlobalFrameList[self.PositionOfVar(symb.value)]
        
        if var.type == "var":
            self.GlobalFrameList[self.PositionOfVar(var.value)].type = "string"
            self.GlobalFrameList[self.PositionOfVar(var.value)].value = symb.type
        else: 
            exit(53)    
# LABEL ⟨label⟩ Definice návěští
# Speciální instrukce označující pomocí návěští ⟨label⟩ důležitou pozici v kódu jako potenciální cíl
# libovolné skokové instrukce. Pokus o vytvoření dvou stejně pojmenovaných návěští na různých
# místech programu je chybou 52.
    def LABEL(self):
        i = self.NumberOfInstruction
        LabelName = self.Instructions[i].args[0].value
        if LabelName not in self.LabelList:
            exit(52)
# JUMP ⟨label⟩ Nepodmíněný skok na návěští
# Provede nepodmíněný skok na zadané návěští ⟨label⟩.
    def JUMP(self):
        i = self.NumberOfInstruction
        Label = self.Instructions[i].args[0]
        if Label not in self.LabelList:
            exit(52)
        else : 
            self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1

# JUMPIFEQ ⟨label⟩ ⟨symb1⟩ ⟨symb2⟩ Podmíněný skok na návěští při rovnosti
# Pokud jsou ⟨symb1⟩ a ⟨symb2⟩ stejného typu nebo je některý operand nil (jinak chyba 53) a
# zároveň se jejich hodnoty rovnají, tak provede skok na návěští ⟨label⟩.    
    def JUMPIFEQ(self):
        i = self.NumberOfInstruction
        Label = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil":
            if symb1.type == "string":
                if symb1.value == symb2.value:
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
            elif symb1.type == "bool":
                if symb1.value == symb2.value:
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
            elif symb1.type == "int":
                if symb1.value == symb2.value:
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
            elif symb1.type == "nil":
                if symb2.type == "nil":
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
        else: 
            exit(53)
                
    def JUMPIFNEQ(self):
        i = self.NumberOfInstruction
        Label = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.GlobalFrameList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.GlobalFrameList[self.PositionOfVar(symb2.value)]
        
        if symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil":
            if symb1.type == "string":
                if symb1.value != symb2.value:
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
            elif symb1.type == "bool":
                if symb1.value != symb2.value:
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
            elif symb1.type == "int":
                if symb1.value != symb2.value:
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
            elif symb1.type == "nil":
                if symb2.type != "nil":
                    if Label not in self.LabelList:
                        exit(52)
                    else : 
                        self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
        else: 
            exit(53)
# DPRINT ⟨symb⟩ Výpis hodnoty na stderr
# Předpokládá se, že vypíše zadanou hodnotu ⟨symb⟩ na standardní chybový výstup (stderr).
    def DPRINT(self) :
        i = self.NumberOfInstruction
        symb = self.Instructions[i].args[0]
        
        # check if symb1 and symb2 are variables
        if symb.type == "var":
            symb = self.GlobalFrameList[self.PositionOfVar(symb.value)]
        
        print(symb.value, file=sys.stderr)
    
# BREAK Výpis stavu interpretu na stderr
# Předpokládá se, že na standardní chybový výstup (stderr) vypíše stav interpretu (např. pozice
# v kódu, obsah rámců, počet vykonaných instrukcí) v danou chvíli (tj. během vykonávání této
# instrukce).
    def BREAK(self):
        print("Pozice v kodu: ", self.NumberOfInstruction, file=sys.stderr)
        print("Obsah ramcu: ", self.GlobalFrameList, file=sys.stderr)
        print("Pocet vykonanych instrukci: ", self.NumberOfInstruction, file=sys.stderr)
        
        