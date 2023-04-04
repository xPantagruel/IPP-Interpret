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
#------------------------------- Class Interpret --------------------------------
class Interpret():
    def __init__(self, Instructions, InputType="stdin"):
        self.Instructions = Instructions
        self.LabelList = []
        self.InputT = InputType
    
    def InitializateLists(self): 
        # initialize label list and check if label is defined
        for i in range(len(self.Instructions)):
            if self.Instructions[i].opcode == "LABEL":
                if self.Instructions[i].args[0].value not in self.LabelList:
                    self.LabelList.append(Label(self.Instructions[i].args[0].value, self.Instructions[i].args[0].value, i-1))
                else:
                    exit(52)
        
    def Interpretation(self):
        self.InitializateLists()
        # create instance of class Instructions
        Instr = Instructions(self.Instructions, self.LabelList, self.InputT)
        Instr.Execution()

#------------------------------- Class Instructions --------------------------------
class Instructions:
    def __init__(self, Instructions, LabelList, InputType="stdin"):
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
            # print("Instr: " + Instr)
            # create switch case
            if Instr == "MOVE":
                self.MOVE()
            elif Instr == "CREATEFRAME":
                self.CREATEFRAME()
            elif Instr == "PUSHFRAME":
                self.PUSHFRAME()
            elif Instr == "POPFRAME":
                self.POPFRAME()
            elif Instr == "DEFVAR":
                self.DEFVAR()
            elif Instr == "CALL":
                self.CALL()
            elif Instr == "RETURN":
                self.RETURN()
            elif Instr == "PUSHS":
                self.PUSHS()
            elif Instr == "POPS":
                self.POPS()
            elif Instr == "ADD":
                self.ADD()
            elif Instr == "SUB":
                self.SUB()
            elif Instr == "MUL":
                self.MUL()
            elif Instr == "IDIV":
                self.IDIV()
            elif Instr == "LT":
                self.LT()
            elif Instr == "GT":
                self.GT()
            elif Instr == "EQ":
                self.EQ()
            elif Instr == "AND":
                self.AND()
            elif Instr == "OR":
                self.OR()
            elif Instr == "NOT":
                self.NOT()
            elif Instr == "INT2CHAR":
                self.INT2CHAR()
            elif Instr == "STRI2INT":
                self.STRI2INT()
            elif Instr == "READ":
                self.READ()
            elif Instr == "WRITE":
                self.WRITE()
            elif Instr == "CONCAT":
                self.CONCAT()
            elif Instr == "STRLEN":
                self.STRLEN()
            elif Instr == "GETCHAR":
                self.GETCHAR()
            elif Instr == "SETCHAR":
                self.SETCHAR()
            elif Instr == "TYPE":
                self.TYPE()
            elif Instr == "LABEL":
                self.LABEL()
            elif Instr == "JUMP":
                self.JUMP()
            elif Instr == "JUMPIFEQ":
                self.JUMPIFEQ()
            elif Instr == "JUMPIFNEQ":
                self.JUMPIFNEQ()
            elif Instr == "DPRINT":
                self.DPRINT()
            elif Instr == "EXIT":
                self.EXIT()
            elif Instr == "BREAK":
                self.BREAK()
            else:
                exit(32)#todo check if exit code is correct            

            self.NumOfInstr += 1
            
    def PositionOfVar(self, var):
        for i in range(len(self.GlobalFrameList)):
            if self.GlobalFrameList[i].name == var:
                return i
        exit(54)
    
    def GetVariable(self, varName):
        # print("---GetVariable-" + varName)
        if(varName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == varName):
                    return self.GlobalFrameList[i]
                
        elif(varName[0:3] == "LF@"):
            # print(self.FrameType)
            # if(self.FrameType != "LF"):
            #     exit(55)
            
            # Get the top list
            # print(self.LocalFramesStack.IsEmpty())
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
            for i in range(len(TopList)):     
                if(TopList[i].name == varName):
                    return TopList[i]
                
        elif(varName[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == varName):
                    return self.TemporaryFrames[i]
        else:
            exit(54)
    
    # todo i have to add new type of variable to the frame
    def SetVariable(self,varName, newVarType, newVarValue):
        if(varName[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == varName):
                    self.GlobalFrameList[i].type = newVarType
                    self.GlobalFrameList[i].value = newVarValue
                    return
            exit(54)
            
            #todo fix this same as getvariable
        elif(varName[0:3] == "LF@"):
            # if(self.FrameType != "LF"):
            #     exit(55)
            TopList = self.LocalFramesStack.peek()
            # print(TopList[0].name)
            for i in range(len(TopList)):     
                if(TopList[i].name == varName):
                    TopList[i].type = newVarType
                    TopList[i].value = newVarValue
                    return

            exit(54)    
        elif(varName[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == varName):
                    self.TemporaryFrames[i].value = newVarValue
                    self.TemporaryFrames[i].type = newVarValue
                    return
            exit(54)
        else:
            exit(54)
            
    def VarExists(self, var):
        if(var[0:3] == "GF@"):
            for i in range(len(self.GlobalFrameList)):
                if(self.GlobalFrameList[i].name == var):
                    return
        elif(var[0:3] == "LF@"):
            if(self.FrameType != "LF"):
                exit(55)
                
            for i in range(len(self.LocalFramesStack)):
                if(self.LocalFramesStack[0][i].name == var):
                    return
        elif(var[0:3] == "TF@"):
            if(self.FrameType != "TF"):
                exit(55)
                
            for i in range(len(self.TemporaryFrames)):
                if(self.TemporaryFrames[i].name == var):
                    return
        else:
            exit(54)
        
        exit(54)
    
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
    
    def CheckType(var, expectedType):
        if expectedType == "int" and isinstance(var, int):
            return True
        elif expectedType == "float" and isinstance(var, float):
            return True
        elif expectedType == "bool" and isinstance(var, bool):
            return True
        elif expectedType == "str" and isinstance(var, str):
            return True
        else:
            return False

                
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
        var = Variable("Symb", self.Instructions[i].args[numOfArg].type, self.Instructions[i].args[numOfArg].value)
        return var
#-------------------------------------- INSTRUCTIONS --------------------------------------
#MOVE ⟨var⟩ ⟨symb⟩ 
# Zkopíruje hodnotu ⟨symb⟩ do ⟨var⟩. Např. MOVE LF@par GF@var provede zkopírování hodnoty
# proměnné var v globálním rámci do proměnné par v lokálním rámci.
    def MOVE(self):
        i = self.NumOfInstr
        
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

            # copy to var var value and type
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
            for i in range(len(self.TemporaryFrames)):
                self.TemporaryFrames[i].name = self.TemporaryFrames[i].name.replace("LF@", "TF@")
            
    def DEFVAR(self):
        # I have 3 cases - var@GF, var@LF, var@TF
        # first thing I have to check which frame is active and check symbols before '@' then check if it suits the frame the frame type, then I have to create variable in the frame
        # second thing of I have to check if the variable is already defined and if yes then I have to exit with error code 52
        VarName = self.Instructions[self.NumOfInstr].args[0].value
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
    def CALL(self):
        # save the current position of the instruction into stack
        self.CallStack.push(self.NumOfInstr)
        
        self.NumOfInstr = self.LabelList[self.Instructions[self.NumOfInstr].order].row
    
    def RETURN(self):
        if(self.CallStack.isEmpty()):
            exit(56)
        else:
            self.NumOfInstr = self.CallStack.pop()    
              
#Uloží hodnotu ⟨symb⟩ na datový zásobník.
# todo check if i should push it like this => only the value to the Datastack
    def PUSHS(self):
        instr = self.Instructions[self.NumOfInstr]
        # check if its variable(call function to get variable) or symbol
        if(instr.args[0].type == "var"):
            var = self.GetVariable(instr.args[0].value)
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
            self.SetVariable(VarPop,instr.args[0])
    
    # ADD ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ 
    # int check
    def ADD(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        else: # set new value to the variable
            try:
                value = int(symb1.value) + int(symb2.value)
                self.SetVariable(self.GetVarName(0), "int", value)
            except:
                exit(53)
    
    def SUB(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        else:
            try:
                value = int(symb1.value) - int(symb2.value)
                self.SetVariable(self.GetVarName(0), "int", value)
            except:
                exit(53)
            
                    
    def MUL(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        else:
            try:
                value = int(symb1.value) * int(symb2.value)
                self.SetVariable(self.GetVarName(0), "int", value)
            except:
                exit(53)
            
    def IDIV(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != "int" or symb2.type != "int"):
            exit(53)
        elif(int(symb2.value) == 0):
            exit(57)
        else:
            try:
                value = int(symb1.value) // int(symb2.value)
                self.SetVariable(self.GetVarName(0), "int", value)
            except:
                exit(53)
#     LT/GT/EQ ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Relační operátory menší, větší, rovno
# Instrukce vyhodnotí relační operátor mezi ⟨symb1⟩ a ⟨symb2⟩ (stejného typu; int, bool nebo
# string) a do ⟨var⟩ zapíše výsledek typu bool (false při neplatnosti nebo true v případě platnosti
# odpovídající relace). Řetězce jsou porovnávány lexikograficky a false je menší než true. Pro
# výpočet neostrých nerovností lze použít AND/OR/NOT. S operandem typu nil (další zdrojový
# operand je libovolného typu) lze porovnávat pouze instrukcí EQ, jinak chyba 53.
    
    def LT(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type):
            exit(53)
        else:
            if(symb1.type == "int"):
                if(int(symb1.value) < int(symb2.value)):
                    value = True
                else:
                    value = False
            elif(symb1.type == "bool"):
                if(symb1.value == "false" and symb2.value == "true"):
                    value = True
                else:
                    value = False
            elif(symb1.type == "string"):
                if(symb1.value < symb2.value):
                    value = True
                else:
                    value = False
            else:
                exit(53)
                
            self.SetVariable(self.GetVarName(0), "bool", value)
    
    def GT(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type):
            exit(53)
        else:
            if(symb1.type == "int"):
                if(int(symb1.value) > int(symb2.value)):
                    value = True
                else:
                    value = False
            elif(symb1.type == "bool"):
                if(symb1.value == "true" and symb2.value == "false"):
                    value = True
                else:
                    value = False
            elif(symb1.type == "string"):
                if(symb1.value > symb2.value):
                    value = True
                else:
                    value = False
            else:
                exit(53)
                
            self.SetVariable(self.GetVarName(0), "bool", value)

    def EQ(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)

        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type):
            exit(53)
        else:
            if(symb1.type == "int"):
                if(int(symb1.value) == int(symb2.value)):
                    value = True
                else:
                    value = False
            elif(symb1.type == "bool"):
                if(symb1.value == symb2.value):
                    value = True
                else:
                    value = False
            elif(symb1.type == "string"):
                if(symb1.value == symb2.value):
                    value = True
                else:
                    value = False
            else:
                exit(53)
                
            self.SetVariable(self.GetVarName(0), "bool", value)
            
#     AND/OR/NOT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Základní booleovské operátory
# Aplikuje konjunkci (logické A)/disjunkci (logické NEBO) na operandy typu bool ⟨symb1⟩ a
# ⟨symb2⟩ nebo negaci na ⟨symb1⟩ (NOT má pouze 2 operandy) a výsledek typu bool zapíše do
# ⟨var⟩.

    def AND(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true" and symb2.value == "true"):
                value = True
            else:
                value = False
                
            self.SetVariable(self.GetVarName(0), "bool", value)
            
    def OR(self):
        i = self.NumOfInstr
        
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true" or symb2.value == "true"):
                value = True
            else:
                value = False
                
            self.SetVariable(self.GetVarName(0), "bool", value)

    def NOT(self):
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
            
        # check if symb1 is bool type
        if(symb1.type != "bool"):
            exit(53)
        else:
            if(symb1.value == "true"):
                value = False
            else:
                value = True
                
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
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both int types
        if(symb1.type != symb2.type or symb1.type != "int"):
            exit(53)
        
        if(symb1.value < 0 or symb2.value < 0):
            exit(58)
        
        try:
            value = ord(self.GetVariable(self.GetVarName(1)).value[symb2.value])
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
        i = self.NumOfInstr
        type = self.GetValue(1)
        
        if(type == "int"):
            try:
                value = int(self.Input)
                self.SetVariable(self.GetVarName(0), "int", value)
            except ValueError:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
                
        elif(type == "string"):
            value = self.Input
            self.SetVariable(self.GetVarName(0), "string", value)
            
        elif(type == "bool"):
            try:
                value = self.Input
                if(value.lower() == "true"):
                    value = "true"
                else:
                    value = "false"
                self.SetVariable(self.GetVarName(0), "bool", value)
            except ValueError:
                self.SetVariable(self.GetVarName(0), "nil", "nil")
        else:
            exit(53)
        
#     WRITE ⟨symb⟩ Výpis hodnoty na standardní výstup
# Vypíše hodnotu ⟨symb⟩ na standardní výstup. Až na typ bool a hodnotu nil@nil je formát
# výpisu kompatibilní s příkazem print jazyka Python 3 s doplňujícím parametrem end='' (zamezí dodatečnému odřádkování). Pravdivostní hodnota se vypíše jako true a nepravda jako
# false. Hodnota nil@nil se vypíše jako prázdný řetězec.

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
        
        if(symb1.value == True):
            print("true", end="")
        elif(symb1.value == False):
            print("false", end="")
        elif(symb1.value == "nil@nil"):
            print("", end="")
        else:
            print(symb1.value, end="")
    
#     CONCAT ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Konkatenace dvou řetězců
# Do proměnné ⟨var⟩ uloží řetězec vzniklý konkatenací dvou řetězcových operandů ⟨symb1⟩ a
# ⟨symb2⟩ (jiné typy nejsou povoleny).
    def CONCAT(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both string types
        if(symb1.type != symb2.type or symb1.type != "string"):
            exit(53)
        
        value = symb1.value + symb2.value
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
        
        value = len(symb1.value)
        self.SetVariable(self.GetVarName(0), "int", value)
#     GETCHAR ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ Vrať znak řetězce
# Do ⟨var⟩ uloží řetězec z jednoho znaku v řetězci ⟨symb1⟩ na pozici ⟨symb2⟩ (indexováno celým
# číslem od nuly). Indexace mimo daný řetězec vede na chybu 58.
    def GETCHAR(self):
        i = self.NumOfInstr
        symbType1 = self.GetType(1)
        symbType2 = self.GetType(2)
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both string types
        if(symb1.type != symb2.type or symb1.type != "string"):
            exit(53)
        
        # check if symb2 is in range
        if(symb2.value < 0 or symb2.value >= len(symb1.value)):
            exit(58)
        
        value = symb1.value[symb2.value]
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
        
        symb1 , symb2 = self.GetSymbVars(symbType1, symbType2)
        
        # check if symb1 and symb2 are both string types
        if(symb1.type != symb2.type or symb1.type != "string"):
            exit(53)
        
        # check if symb2 is in range
        if(symb1.value < 0 or symb1.value >= len(symb1.value)):
            exit(58)
        
        # check if symb2 is not empty
        if(symb2.value == ""):
            exit(58)
        
        value = symb1.value
        value[symb1.value] = symb2.value[0]
        self.SetVariable(self.GetVarName(0), "string", value)

# TYPE ⟨var⟩ ⟨symb⟩ Zjisti typ daného symbolu
# Dynamicky zjistí typ symbolu ⟨symb⟩ a do ⟨var⟩ zapíše řetězec značící tento typ (int, bool,
# string nebo nil). Je-li ⟨symb⟩ neinicializovaná proměnná, označí její typ prázdným řetězcem
    def TYPE(self):
        i = self.NumOfInstr
        symbType = self.GetType(1)
        
        # var
        if(symbType == "var"):
            symb = self.GetVariable(self.GetVarName(1))
            
        # symb
        else:
            symb = self.GetSymb(1)
            
        # check if symb is not nil
        if(symb.type == "nil"):
            value = ""
        else:
            value = symb.type
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
        
        # check if symb1 and symb2 are both string types
        if(symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil"):
            if(symb1.value == symb2.value):
                for j in range(len(self.LabelList)):
                    if(self.LabelList[j].name == Label):
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
        
        # check if symb1 and symb2 are both string types
        if(symb1.type == symb2.type or symb1.type == "nil" or symb2.type == "nil"):
            if(symb1.value != symb2.value):
                for j in range(len(self.LabelList)):
                    if(self.LabelList[j].name == Label):
                        self.NumOfInstr = self.LabelList[j].row  
                        return
                exit(52)
        else:
            exit(53)
# DPRINT ⟨symb⟩ Výpis hodnoty na stderr
# Předpokládá se, že vypíše zadanou hodnotu ⟨symb⟩ na standardní chybový výstup (stderr).
    def DPRINT(self) :
        symb = self.GetSymb(0)
        print(symb.value, file=sys.stderr)
    
    def EXIT():
        pass
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