import sys

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

class Label:
    def __init__(self, name, value,row):
        self.name = name
        self.value = value
        self.row = row

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
            eval("self." + self.Instructions[self.NumberOfInstruction].opcode + "()")
            self.NumberOfInstruction += 1
            
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
                
            if(self.Instructions[i].args[1].value == "nil"):
                exit(56)

        # if(self.Instructions[i].args[0].type == "var" and self.Instructions[i].args[1].type == "symb"):
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
        if name not in self.VariablesList:
             self.VariablesList.append(Variable(name))
        else:
            exit(52)
    
    # update NumberOfInstruction to the row of the labelv
    def CALL(self):
        self.NumberOfInstruction = self.LabelList[self.Instructions[self.NumberOfInstruction].order].row - 1
    
    def RETURN(self):
        pass
    
    def PUSHS(self):
        pass
    
    def POPS(self):
        pass
    
    # ADD ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩ 
    # int check
    def ADD(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.VariablesList[self.PositionOfVar(var.value)].type = "int"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value + symb2.value
        else: 
            exit(53)
                    
    def SUB(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.VariablesList[self.PositionOfVar(var.value)].type = "int"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value - symb2.value
        else: 
            exit(53)
                    
    def MUL(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.VariablesList[self.PositionOfVar(var.value)].type = "int"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value * symb2.value
        else: 
            exit(53)
    
    def IDIV(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
            
        # division by zero
        if symb2.value == 0:
            exit(57)
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int":
                self.VariablesList[self.PositionOfVar(var.value)].type = "int"
                self.VariablesList[self.PositionOfVar(var.value)].value = int(symb1.value * symb2.value)
        else: 
            exit(53)
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int" or symb2.type == "bool" and symb1.type == "bool" or symb2.type == "string" and symb1.type == "string" or symb2.type == "nil" or symb1.type == "nil":
                self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value < symb2.value
        else: 
            exit(53)
    
    def GT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int" or symb2.type == "bool" and symb1.type == "bool" or symb2.type == "string" and symb1.type == "string" or symb2.type == "nil" or symb1.type == "nil":
                self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value > symb2.value
        else: 
            exit(53)
    
    def EQ(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "int" or symb2.type == "bool" and symb1.type == "bool" or symb2.type == "string" and symb1.type == "string" or symb2.type == "nil" or symb1.type == "nil":
                self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value == symb2.value
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "bool" and symb1.type == "bool":
                self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value and symb2.value
        else: 
            exit(53)        
    
    def OR(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "bool" and symb1.type == "bool":
                self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value or symb2.value
        else: 
            exit(53)
    
    def NOT(self):
        i = self.NumberOfInstruction
        var = self.Instructions[i].args[0]
        symb1 = self.Instructions[i].args[1]
        symb2 = self.Instructions[i].args[2]
        
        # check if symb1 and symb2 are variables
        if symb1.type == "var":
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "bool" and symb1.type == "bool":
                self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                self.VariablesList[self.PositionOfVar(var.value)].value = not symb1.value
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
            symb = self.VariablesList[self.PositionOfVar(symb.value)]
        
        if var.type == "var" and symb.type == "int":
            try:
                self.VariablesList[self.PositionOfVar(var.value)].type = "string"
                self.VariablesList[self.PositionOfVar(var.value)].value = chr(symb.value)
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb2.type == "int" and symb1.type == "string":
            try:
                self.VariablesList[self.PositionOfVar(var.value)].type = "int"
                self.VariablesList[self.PositionOfVar(var.value)].value = ord(symb1.value[symb2.value])
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
                    self.VariablesList[self.PositionOfVar(var.value)].type = "int"
                    self.VariablesList[self.PositionOfVar(var.value)].value = int(input())
                except ValueError:
                    self.VariablesList[self.PositionOfVar(var.value)].type = "nil"
                    self.VariablesList[self.PositionOfVar(var.value)].value = "nil"
            elif type.value == "string":
                try:
                    self.VariablesList[self.PositionOfVar(var.value)].type = "string"
                    self.VariablesList[self.PositionOfVar(var.value)].value = input()
                except ValueError:
                    self.VariablesList[self.PositionOfVar(var.value)].type = "nil"
                    self.VariablesList[self.PositionOfVar(var.value)].value = "nil"
            elif type.value == "bool":
                try:
                    self.VariablesList[self.PositionOfVar(var.value)].type = "bool"
                    self.VariablesList[self.PositionOfVar(var.value)].value = input()
                    if self.VariablesList[self.PositionOfVar(var.value)].value.lower() == "true":
                        self.VariablesList[self.PositionOfVar(var.value)].value = True
                    else:
                        self.VariablesList[self.PositionOfVar(var.value)].value = False
                except ValueError:
                    self.VariablesList[self.PositionOfVar(var.value)].type = "nil"
                    self.VariablesList[self.PositionOfVar(var.value)].value = "nil"
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
            symb = self.VariablesList[self.PositionOfVar(symb.value)]
        
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb1.type == "string" and symb2.type == "string":
            self.VariablesList[self.PositionOfVar(var.value)].type = "string"
            self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value + symb2.value
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
            symb = self.VariablesList[self.PositionOfVar(symb.value)]
        
        if var.type == "var" and symb.type == "string":
            self.VariablesList[self.PositionOfVar(var.value)].type = "int"
            self.VariablesList[self.PositionOfVar(var.value)].value = len(symb.value)
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb1.type == "string" and symb2.type == "int":
            if int(symb2.value) < 0 or int(symb2.value) >= len(symb1.value):
                exit(58)
            self.VariablesList[self.PositionOfVar(var.value)].type = "string"
            self.VariablesList[self.PositionOfVar(var.value)].value = symb1.value[int(symb2.value)]
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
        if var.type == "var" and symb1.type == "int" and symb2.type == "string":
            if symb2.value == "":
                exit(58)
            if int(symb1.value) < 0 or int(symb1.value) >= len(self.VariablesList[self.PositionOfVar(var.value)].value):
                exit(58)
            self.VariablesList[self.PositionOfVar(var.value)].value = self.VariablesList[self.PositionOfVar(var.value)].value[:int(symb1.value)] + symb2.value[0] + self.VariablesList[self.PositionOfVar(var.value)].value[int(symb1.value)+1:]
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
            symb = self.VariablesList[self.PositionOfVar(symb.value)]
        
        if var.type == "var":
            self.VariablesList[self.PositionOfVar(var.value)].type = "string"
            self.VariablesList[self.PositionOfVar(var.value)].value = symb.type
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
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
            symb1 = self.VariablesList[self.PositionOfVar(symb1.value)]
        
        if symb2.type == "var":
            symb2 = self.VariablesList[self.PositionOfVar(symb2.value)]
        
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
            symb = self.VariablesList[self.PositionOfVar(symb.value)]
        
        print(symb.value, file=sys.stderr)
    
# BREAK Výpis stavu interpretu na stderr
# Předpokládá se, že na standardní chybový výstup (stderr) vypíše stav interpretu (např. pozice
# v kódu, obsah rámců, počet vykonaných instrukcí) v danou chvíli (tj. během vykonávání této
# instrukce).
    def BREAK(self):
        print("Pozice v kodu: ", self.NumberOfInstruction, file=sys.stderr)
        print("Obsah ramcu: ", self.VariablesList, file=sys.stderr)
        print("Pocet vykonanych instrukci: ", self.NumberOfInstruction, file=sys.stderr)
        
        