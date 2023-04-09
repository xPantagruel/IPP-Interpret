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
class Interpret():
    def __init__(self, Instructions, InputType=sys.stdin):
        self.Instructions = Instructions
        self.LabelList = []
        self.InputT = InputType
    
    def InitializateLists(self): 
        # initialize label list and check if label is defined
        for i in range(len(self.Instructions)):
            if self.Instructions[i].opcode == "LABEL":
                for j in range(len(self.LabelList)):
                    if self.LabelList[j].name == self.Instructions[i].args[0].value:
                        exit(52)
                
                self.LabelList.append(Label(self.Instructions[i].args[0].value, self.Instructions[i].args[0].value, i-1))
        
    def Interpretation(self):
        self.InitializateLists()
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
            elif Instr == "SUB":
                self.NumOfArgCheck(3)
                self.SUB()
            elif Instr == "MUL":
                self.NumOfArgCheck(3)
                self.MUL()
            elif Instr == "IDIV":
                self.NumOfArgCheck(3)
                self.IDIV()
            elif Instr == "LT":
                self.NumOfArgCheck(3)
                self.LT()
            elif Instr == "GT":
                self.NumOfArgCheck(3)
                self.GT()
            elif Instr == "EQ":
                self.NumOfArgCheck(3)
                self.EQ()
            elif Instr == "AND":
                self.NumOfArgCheck(3)
                self.AND()
            elif Instr == "OR":
                self.NumOfArgCheck(3)
                self.OR()
            elif Instr == "NOT":
                self.NumOfArgCheck(2)
                self.NOT()
            elif Instr == "INT2CHAR":
                self.NumOfArgCheck(2)
                self.INT2CHAR()
            elif Instr == "STRI2INT":
                self.NumOfArgCheck(3)
                self.STRI2INT()
            elif Instr == "READ":
                self.NumOfArgCheck(2)
                self.READ()
            elif Instr == "WRITE":
                self.NumOfArgCheck(1)
                self.WRITE()
            elif Instr == "CONCAT":
                self.NumOfArgCheck(3)
                self.CONCAT()
            elif Instr == "STRLEN":
                self.NumOfArgCheck(2)
                self.STRLEN()
            elif Instr == "GETCHAR":
                self.NumOfArgCheck(3)
                self.GETCHAR()
            elif Instr == "SETCHAR":
                self.NumOfArgCheck(3)
                self.SETCHAR()
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
            elif Instr == "JUMPIFNEQ":
                self.NumOfArgCheck(3)
                self.JUMPIFNEQ()
            elif Instr == "DPRINT":
                self.NumOfArgCheck(1)
                self.DPRINT()
            elif Instr == "EXIT":
                self.NumOfArgCheck(1)
                self.EXIT()
            elif Instr == "BREAK":
                self.NumOfArgCheck(0)
                self.BREAK()
            else:
                exit(32)#todo check if exit code is correct            

            self.NumOfInstr += 1
            
    # def PositionOfVar(self, var):
    #     for i in range(len(self.GlobalFrameList)):
    #         if self.GlobalFrameList[i].name == var:
    #             return i
    #     exit(54)
    
    def NumOfArgCheck(self, numOfArgs):
        if(len(self.Instructions[self.NumOfInstr].args) != numOfArgs):
            exit(32) 
            
    def GetVariable(self, varName, IsInicialized=True ):
        # print("---GetVariable-" + varName)
        if(varName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == varName):
                    if(IsInicialized):
                        if(self.GlobalFrameList[i].isInicialized == False):# check if variable is defined
                            exit(56)
                    return self.GlobalFrameList[i]
                
        elif(varName[0:3] == "LF@"):
            # print(self.FrameType)
            if(self.LocalFramesStack.IsEmpty()):
                exit(55)
            
            # Get the top list
            # print(self.LocalFramesStack.IsEmpty())
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
            for i in range(len(TopList)):     
                if(TopList[i].name == varName):
                    if(IsInicialized):
                        if(TopList[i].isInicialized == False):# check if variable is defined
                            exit(56)
                    return TopList[i]
                
        elif(varName[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == varName):
                    if(IsInicialized):
                        if(self.TemporaryFrames[i].isInicialized == False):# check if variable is defined
                            exit(56)
                    return self.TemporaryFrames[i]
                
        exit(54)
    
    # todo i have to add new type of variable to the frame
    def SetVariable(self,varName, newVarType, newVarValue):
        if(varName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == varName):
                    self.GlobalFrameList[i].type = newVarType
                    self.GlobalFrameList[i].value = self.ChangeVarType(newVarType, newVarValue)
                    if(self.GlobalFrameList[i].isInicialized == False): # nastaveni inicializace
                        self.GlobalFrameList[i].isInicialized = True
                    return
            exit(54)
            
            #todo fix this same as getvariable
        elif(varName[0:3] == "LF@"):
            if(self.LocalFramesStack == None or self.LocalFramesStack.IsEmpty()):
                exit(55)
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
            for i in range(len(TopList)):     
                if(TopList[i].name == varName):
                    TopList[i].type = newVarType
                    TopList[i].value = self.ChangeVarType(newVarType, newVarValue)#TODO FIX THIS IN README NOTE THAT I SHOULD POP BACK THE WHOLE LIST
                    if(TopList[i].isInicialized == False):
                        TopList[i].isInicialized = True
                    self.LocalFramesStack.pop()
                    self.LocalFramesStack.push(TopList)
                    return

            exit(54)    
        elif(varName[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == varName):
                    self.TemporaryFrames[i].value = self.ChangeVarType(newVarType, newVarValue)
                    self.TemporaryFrames[i].type = newVarType
                    if(self.TemporaryFrames[i].isInicialized == False):
                        self.TemporaryFrames[i].isInicialized = True
                    return
            exit(54)
        else:
            exit(54)
            
    def VarExists(self, VarName):
        if(VarName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == VarName):
                    return
        elif(VarName[0:3] == "LF@"):
            if(self.LocalFramesStack.IsEmpty()):
                exit(55)
                
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
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
            except ValueError:
                exit(53)
        elif(newVarType == "string"):
            if(newVarValue == None):
                return newVarValue
            try:
                newVarValue = str(newVarValue)
            except ValueError:
                exit(53)
        elif(newVarType == "nil"):
            return newVarValue
        else:
            exit(53)
        return newVarValue
    
    def GetSymbVars(self, symbType1, symbType2):
        
        # var var
        if symbType1 == "var" and symbType2 == "var":
            symb1 = self.GetVariable(self.GetVarName(1))
            symb2 = self.GetVariable(self.GetVarName(2))

        # symb var
        elif symbType1 != "var" and symbType2 == "var":
            symb1 = self.GetSymb(1)
            symb2 = self.GetVariable(self.GetVarName(2))

        # var symb
        elif symbType1 == "var" and symbType2 != "var":
            symb1 = self.GetVariable(self.GetVarName(1))
            symb2 = self.GetSymb(2)

        # symb symb
        elif symbType1 != "var" and symbType2 != "var":
            symb1 = self.GetSymb(1)
            symb2 = self.GetSymb(2)
        else:
            exit(53)
            
        return symb1, symb2
    
    # def CheckType(var, expectedType):
    #     if expectedType == "int" and isinstance(var, int):
    #         return True
    #     elif expectedType == "float" and isinstance(var, float):
    #         return True
    #     elif expectedType == "bool" and isinstance(var, bool):
    #         return True
    #     elif expectedType == "str" and isinstance(var, str):
    #         return True
    #     else:
    #         exit(53)

    def GetType(self, numOfArg):
        i = self.NumOfInstr
        return self.Instructions[i].args[numOfArg].type
    
    def GetValue(self, numOfArg):
        i = self.NumOfInstr
        return self.Instructions[i].args[numOfArg].value
    
    def GetVarName(self,numOfArg):
        i = self.NumOfInstr
        return self.Instructions[i].args[numOfArg].value
    
    def GetSymb(self, numOfArg):
        i = self.NumOfInstr
        symbVal = self.Instructions[i].args[numOfArg].value
        
        if(symbVal == None):# empty symb
            return Variable("Symb", self.Instructions[i].args[numOfArg].type)
        
        # string
        if(self.Instructions[i].args[numOfArg].type == "string"):
            symbVal = self.ConvertStringLiterals(str(symbVal))
        symbVal = self.ChangeVarType(self.Instructions[i].args[numOfArg].type, symbVal)
        var = Variable("Symb", self.Instructions[i].args[numOfArg].type, symbVal)
        return var
#-------------------------------------- INSTRUCTIONS --------------------------------------
#MOVE ⟨var⟩ ⟨symb⟩ 
# Zkopíruje hodnotu ⟨symb⟩ do ⟨var⟩. Např. MOVE LF@par GF@var provede zkopírování hodnoty
# proměnné var v globálním rámci do proměnné par v lokálním rámci.
    def MOVE(self):
        # move var symb
        if(self.GetType(0) == "var" and self.GetType(1) != "var"):
            # Check if variable is in frame
            self.VarExists(self.GetValue(0))

            # copy to var symb value and type
            self.SetVariable(self.GetValue(0), self.GetType(1), self.GetValue(1))

        elif(self.GetType(0) == "var" and self.GetType(1) == "var"):
            # Check if variable is in frame
            self.VarExists(self.GetValue(0))
            self.VarExists(self.GetValue(1))

            # copy to var value and type
            var = self.GetVariable(self.GetValue(1))
            self.SetVariable(self.GetValue(0), var.type, var.value)      
        
    def CREATEFRAME(self):
        # zahodí případný obsah původního dočasného rámce vytvoří nový dočasný rámec
        self.TemporaryFrames = []
        self.FrameType = "TF"

# todo TF bude po provedení instrukce nedefinován a je třeba jej před dalším
# todo použitím vytvořit pomocí CREATEFRAME. Pokus o přístup k nedefinovanému rámci vede na
# todo chybu 55.
    def PUSHFRAME(self):
        if(self.FrameType != "TF"):
            exit(55)
        # I need to change TF@ to LF@ and then push it to the stack
        for i in range(len(self.TemporaryFrames)):
            self.TemporaryFrames[i].name = self.TemporaryFrames[i].name.replace("TF@", "LF@")            

        self.LocalFramesStack.push(self.TemporaryFrames)
        self.FrameType = "LF"
        
        # todo priklad jak vstoupit do LF
        # # Get the top list
        # top_list = self.LocalFramesStack.peek()
        # print(top_list[0].name)

            
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
            exit(55)# todo check this if its neccesary
            
    def DEFVAR(self):
        # I have 3 cases - var@GF, var@LF, var@TF
        # first thing I have to check which frame is active and check symbols before '@' then check if it suits the frame the frame type, then I have to create variable in the frame
        # second thing of I have to check if the variable is already defined and if yes then I have to exit with error code 52
        # VarName = self.Instructions[self.NumOfInstr].args[0].value
        VarName = self.GetVarName(0)
        #check var type 
        # case 1 - var@GF
        if(VarName[0:3] == "GF@"):
            # check if var is already defined
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == VarName):
                    exit(52)
            
            self.GlobalFrameList.append(Variable(VarName))
                
        # case 2 - var@LF
        elif(VarName[0:3] == "LF@"):
            # todo check if i have to check if LF is defined and if not then exit with error code 55
            if(self.LocalFramesStack == None or self.LocalFramesStack.IsEmpty()):
                exit(55)
                    
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
            for i in range(len(TopList)):     
                if(TopList[i].name == VarName):
                    exit(52)
            
            # if var is not defined then I have to create it
            TopList.append(Variable(VarName))
            self.LocalFramesStack.pop()
            self.LocalFramesStack.push(TopList)


        # case 3 - var@TF
        elif(VarName[0:3] == "TF@" and self.FrameType == "TF"):
            # todo check if i have to check if LF is defined and if not then exit with error code 55
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
    
    # update NumberOfInstruction to the row of the labelv
#     CALL ⟨label⟩ Skok na návěští s podporou návratu
# Uloží inkrementovanou aktuální pozici z interního čítače instrukcí do zásobníku volání a provede
# skok na zadané návěští (případnou přípravu rámce musí zajistit jiné instrukce).
    def CALL(self):
        # save the current position of the instruction into stack
        self.CallStack.push(self.NumOfInstr)
        
        # find the row of the label
        for i in range(len(self.LabelList)):
            if(self.LabelList[i].name == self.Instructions[self.NumOfInstr].args[0].value):
                self.NumOfInstr = self.LabelList[i].row
                return
        exit(52)
        
            
# RETURN Návrat na pozici uloženou instrukcí CALL
# Vyjme pozici ze zásobníku volání a skočí na tuto pozici nastavením interního čítače instrukcí
# (úklid lokálních rámců musí zajistit jiné instrukce). Provedení instrukce při prázdném zásobníku
# volání vede na chybu 56.
    def RETURN(self):
        if(self.CallStack.IsEmpty()):
            exit(56)
        else:
            self.NumOfInstr = self.CallStack.pop()    
              
#Uloží hodnotu ⟨symb⟩ na datový zásobník.
# todo check if i should push it like this => only the value to the Datastack
    def PUSHS(self):
        instr = self.Instructions[self.NumOfInstr]
        # check if its variable(call function to get variable) or symbol
        if(instr.args[0].type == "var"):
            var = self.GetVariable(self.GetVarName(0))
            self.DataStack.push(var.value)
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
    def ADD(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        else: # set new value to the variable
            value = int(symb1.value) + int(symb2.value)
            self.SetVariable(self.GetVarName(0), "int", value)

    
    def SUB(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        else:
            #todo check if i should not put here try except
            value = int(symb1.value) - int(symb2.value)
            self.SetVariable(self.GetVarName(0), "int", value)

            
                    
    def MUL(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        else:
            #todo check if i should not put here try except
            value = int(symb1.value) * int(symb2.value)
            self.SetVariable(self.GetVarName(0), "int", value)
            
    def IDIV(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        elif(int(symb2.value) == 0):
            exit(57)
        else:
            #todo check if i should not put here try except
            value = int(symb1.value) // int(symb2.value)
            self.SetVariable(self.GetVarName(0), "int", value)
#     LT/GT/EQ ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Relační operátory menší, větší, rovno
# Instrukce vyhodnotí relační operátor mezi ⟨symb1⟩ a ⟨symb2⟩ (stejného typu; int, bool nebo
# string) a do ⟨var⟩ zapíše výsledek typu bool (false při neplatnosti nebo true v případě platnosti
# odpovídající relace). Řetězce jsou porovnávány lexikograficky a false je menší než true. Pro
# výpočet neostrých nerovností lze použít AND/OR/NOT. S operandem typu nil (další zdrojový
# operand je libovolného typu) lze porovnávat pouze instrukcí EQ, jinak chyba 53.

    def LT(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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
            else:
                exit(53)
                
            self.SetVariable(self.GetVarName(0), "bool", value)
    
    def GT(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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
            else:
                exit(53)
                
            self.SetVariable(self.GetVarName(0), "bool", value)

    def EQ(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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
            else:
                exit(53)
        else:
            exit(53)
            
        self.SetVariable(self.GetVarName(0), "bool", value)
            
#     AND/OR/NOT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Základní booleovské operátory
# Aplikuje konjunkci (logické A)/disjunkci (logické NEBO) na operandy typu bool ⟨symb1⟩ a
# ⟨symb2⟩ nebo negaci na ⟨symb1⟩ (NOT má pouze 2 operandy) a výsledek typu bool zapíše do
# ⟨var⟩.

    def AND(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true" and symb2.value == "true"):
                value = "true"
            else:
                value = "false"
                
            self.SetVariable(self.GetVarName(0), "bool", value)
            
    def OR(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true" or symb2.value == "true"):
                value = "true"
            else:
                value = "false"
                
            self.SetVariable(self.GetVarName(0), "bool", value)

    def NOT(self):
        symbType1 = self.GetType(1)
        
        # var
        if(symbType1 == "var"):
            symb1 = self.GetVariable(self.GetVarName(1))
            
        # symb
        elif(symbType1 != "var"):
            symb1 = self.GetSymb(1)
            
        else:
            exit(53)
            
        # check if symb1 is bool type
        if(symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true"):
                value = "false"
            else:
                value = "true"
                
            self.SetVariable(self.GetVarName(0), "bool", value)
    
#     INT2CHAR ⟨var⟩ ⟨symb⟩ Převod celého čísla na znak
# Číselná hodnota ⟨symb⟩ je dle Unicode převedena na znak, který tvoří jednoznakový řetězec
# přiřazený do ⟨var⟩. Není-li ⟨symb⟩ validní ordinální hodnota znaku v Unicode (viz funkce chr
# v Python 3), dojde k chybě 58.
    def INT2CHAR(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        
        # var
        if(symbType1 == "var"):
            symb1 = self.GetVariable(self.GetVarName(1))
            
        # symb
        elif(symbType1 != "var"):
            symb1 = self.GetSymb(1)
            
        else:
            exit(53)
        
        if(symb1.type != "int"):# todo is it neccecary?
            exit(53)

        try:
            value = chr(int(symb1.value))
            self.SetVariable(self.GetVarName(0), "string", value)
        except ValueError:
            exit(58)  
    
#     STRI2INT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Ordinální hodnota znaku
# Do ⟨var⟩ uloží ordinální hodnotu znaku (dle Unicode) v řetězci ⟨symb1⟩ na pozici ⟨symb2⟩
# (indexováno od nuly). Indexace mimo daný řetězec vede na chybu 58. Viz funkce ord v Python 3.
    def STRI2INT(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "string" or symb2.type != "int"):
            exit(53)
        
        # string outrange
        if(int(symb2.value) >= len(symb1.value) or int(symb2.value) < 0):
            exit(58)        

        try:
            value = ord(symb1.value[int(symb2.value)])
            self.SetVariable(self.GetVarName(0), "int", value)
        except ValueError:
            exit(58)
    
#     READ ⟨var⟩ ⟨type⟩ Načtení hodnoty ze standardního vstupu
# Načte jednu hodnotu dle zadaného typu ⟨type⟩ ∈ {int, string, bool} a uloží tuto hodnotu do
# proměnné ⟨var⟩. Načtení proveďte vestavěnou funkcí input() (či analogickou) jazyka Python 3,
# pak proveďte konverzi na specifikovaný typ ⟨type⟩. Při převodu vstupu na typ bool nezáleží na
# velikosti písmen a řetězec ”
# true“ se převádí na bool@true, vše ostatní na bool@false. V případě
# chybného nebo chybějícího vstupu bude do proměnné ⟨var⟩ uložena hodnota nil@nil
    def READ(self): # todo i have to decide if the input is from file or console
        type = self.GetValue(1)
        if(type == "int"):
            try:
                value = self.Input.readline().rstrip()
                self.SetVariable(self.GetVarName(0), "int", int(value))
            except ValueError:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
                
        elif(type == "string"):
            try:
                value = self.Input.readline().rstrip()
                self.SetVariable(self.GetVarName(0), "string", str(value))
            except ValueError:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
                
        elif(type == "bool"):# todo figure out if the input is not true shoudl i put in false or nil? 
            try:
                value = self.Input.readline().rstrip()
                if(value.lower() == "true"):
                    value = "true"
                else:
                    value = "false"
                self.SetVariable(self.GetVarName(0), "bool", value)
            except ValueError:
                self.SetVariable(self.GetVarName(0), "bool", "false")
        else:
            exit(53)
        
#     WRITE ⟨symb⟩ Výpis hodnoty na standardní výstup
# Vypíše hodnotu ⟨symb⟩ na standardní výstup. Až na typ bool a hodnotu nil@nil je formát
# výpisu kompatibilní s příkazem print jazyka Python 3 s doplňujícím parametrem end='' (zamezí dodatečnému odřádkování). Pravdivostní hodnota se vypíše jako true a nepravda jako
# false. Hodnota nil@nil se vypíše jako prázdný řetězec.
    def ConvertStringLiterals(self,string):
        # inicializace proměnných
        result = ""
        EscapeMode = False
        EscapeCode = ""
        
        # projdeme každý znak řetězce
        for char in string:
            # escape sekvence
            if EscapeMode:
                EscapeCode += char
                if len(EscapeCode) == 3:
                    result += chr(int(EscapeCode))
                    EscapeMode = False
                    EscapeCode = ""
            # běžný tisknutelný znak
            elif char not in [' ', '#', '\\']:
                result += char
            # začátek escape sekvence
            elif char == '\\':
                EscapeMode = True
            # zakázána mřížka a zpětné lomítko
            elif char in ['#', '\\']:
                pass
            # zakódování bílého znaku
            else:
                result += chr(ord(char) + 128)
        
        return result

    def WRITE(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(0)
        
        # var
        if(symbType1 == "var"):
            symb1 = self.GetVariable(self.GetVarName(0))
            
        # symb
        elif(symbType1 != "var"):
            symb1 = self.GetSymb(0)
            
        else:
            exit(53)
        
        if(symb1.value == "true"):
            print("true", end="")
        elif(symb1.value == "false"):
            print("false", end="")
        elif(symb1.type == "nil"):
            print("", end="")
        else:
            print(symb1.value, end="")
    
#     CONCAT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Konkatenace dvou řetězců
# Do proměnné ⟨var⟩ uloží řetězec vzniklý konkatenací dvou řetězcových operandů ⟨symb1⟩ a
# ⟨symb2⟩ (jiné typy nejsou povoleny).
    def CONCAT(self):
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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
            
        self.SetVariable(self.GetVarName(0), "string", value)
# STRLEN ⟨var⟩ ⟨symb⟩ Zjisti délku řetězce
# Zjistí počet znaků (délku) řetězce v ⟨symb⟩ a tato délka je uložena jako celé číslo do ⟨var⟩.
    def STRLEN(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        
        # var
        if(symbType1 == "var"):
            symb1 = self.GetVariable(self.GetVarName(1))
            
        # symb
        elif(symbType1 != "var"):
            symb1 = self.GetSymb(1)
            
        else:
            exit(53)
        
        # check if symb1 is string
        if(symb1.type != "string"):
            exit(53)
            
        if(symb1.value == None):
            value = 0
        else:
            value = len(symb1.value)  
        
        self.SetVariable(self.GetVarName(0), "int", value)
#     GETCHAR ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Vrať znak řetězce
# Do ⟨var⟩ uloží řetězec z jednoho znaku v řetězci ⟨symb1⟩ na pozici ⟨symb2⟩ (indexováno celým
# číslem od nuly). Indexace mimo daný řetězec vede na chybu 58.
    def GETCHAR(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        var = self.GetVarName(0)
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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

        self.SetVariable(self.GetVarName(0), "string", value)

# SETCHAR ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Změň znak řetězce
# Zmodifikuje znak řetězce uloženého v proměnné ⟨var⟩ na pozici ⟨symb1⟩ (indexováno celočíselně
# od nuly) na znak v řetězci ⟨symb2⟩ (první znak, pokud obsahuje ⟨symb2⟩ více znaků). Výsledný
# řetězec je opět uložen do ⟨var⟩. Při indexaci mimo řetězec ⟨var⟩ nebo v případě prázdného
# řetězce v ⟨symb2⟩ dojde k chybě 58.    
    def SETCHAR(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        var = self.GetVariable(self.GetVarName(0))
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)

        # check if var, symb2 is string type
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
        
        # case if symb2 is in format \ddd
        symb2Val = self.ConvertStringLiterals(symb2.value)
        
        value = var.value[:int(symb1.value)] + symb2Val[0] + var.value[int(symb1.value)+1:]

        self.SetVariable(self.GetVarName(0), "string", value)
# TYPE ⟨var⟩ ⟨symb⟩ Zjisti typ daného symbolu
# Dynamicky zjistí typ symbolu ⟨symb⟩ a do ⟨var⟩ zapíše řetězec značící tento typ (int, bool,
# string nebo nil). Je-li ⟨symb⟩ neinicializovaná proměnná, označí její typ prázdným řetězcem
    def TYPE(self):
        i = self.NumOfInstr
        symbType = self.GetType(1)
        
        # var
        if(symbType == "var"):
            symb = self.GetVariable(self.GetVarName(1),False)
            
        # symb
        else:
            symb = self.GetSymb(1)
            
        if(symb.type != None):
            value = symb.type
        else:
            value = ""
            
        self.SetVariable(self.GetVarName(0), "string", value)
# LABEL ⟨label⟩ Definice návěští
# Speciální instrukce označující pomocí návěští ⟨label⟩ důležitou pozici v kódu jako potenciální cíl
# libovolné skokové instrukce. Pokus o vytvoření dvou stejně pojmenovaných návěští na různých
# místech programu je chybou 52.
    def LABEL(self):
        pass
# JUMP ⟨label⟩ Nepodmíněný skok na návěští
# Provede nepodmíněný skok na zadané návěští ⟨label⟩.
    def JUMP(self):
        Label = self.GetValue(0)
        
        for j in range(len(self.LabelList)):
            if(self.LabelList[j].name == Label):
                self.NumOfInstr = self.LabelList[j].row  
                return
            
        exit(52)
# JUMPIFEQ ⟨label⟩ ⟨symb1⟩ ⟨symb2⟩ Podmíněný skok na návěští při rovnosti
# Pokud jsou ⟨symb1⟩ a ⟨symb2⟩ stejného typu nebo je některý operand nil (jinak chyba 53) a
# zároveň se jejich hodnoty rovnají, tak provede skok na návěští ⟨label⟩.    
    def JUMPIFEQ(self):
        Label = self.GetValue(0)
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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
                
    def JUMPIFNEQ(self):
        Label = self.GetValue(0)
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
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

# DPRINT ⟨symb⟩ Výpis hodnoty na stderr
# Předpokládá se, že vypíše zadanou hodnotu ⟨symb⟩ na standardní chybový výstup (stderr).
    def DPRINT(self) :
        symbType1 = self.GetType(0)
        
        if(symbType1 == "var"):
            symb = self.GetVariable(self.GetVarName(0))
        elif(symbType1 != "var"):
            symb = self.GetSymb(0)
        else:
            exit(52)
            
        print(symb.value, file=sys.stderr)
    
# Ukončí vykonávání programu, případně vypíše statistiky a ukončí interpret s návratovým kódem
# ⟨symb⟩, kde ⟨symb⟩ je celé číslo v intervalu 0 až 49 (včetně). Nevalidní celočíselná hodnota
# ⟨symb⟩ vede na chybu 57.
    def EXIT(self):
        symbType1 = self.GetType(0)
        
        if(symbType1 == "var"):
            symb = self.GetVariable(self.GetVarName(0))
        elif(symbType1 != "var"):
            symb = self.GetSymb(0)
        else:
            exit(52)
        
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
# BREAK Výpis stavu interpretu na stderr
# Předpokládá se, že na standardní chybový výstup (stderr) vypíše stav interpretu (např. pozice
# v kódu, obsah rámců, počet vykonaných instrukcí) v danou chvíli (tj. během vykonávání této
# instrukce).
    def BREAK(self):
        print("NumOfInstr: ", self.NumOfInstr, file=sys.stderr)
        print("GlobalFrameList: ", self.GlobalFrameList, file=sys.stderr)
        for var in self.LocalFramesStack:
            print("LocalFrameList: ", var, file=sys.stderr)
        print("TempFrameList: ", self.TempFrameList[0], file=sys.stderr)
        print("CallStack: ", self.CallStack, file=sys.stderr)
        print("DataStack: ", self.DataStack, file=sys.stderr)
        print("LabelList: ", self.LabelList, file=sys.stderr)