- Handle frames 

- findout:
what does this mean (odkazuje na vrcholový/aktuální rámec na zásobníku rámců)
lokální, značíme LF (Local Frame), který je na začátku nedefinován a odkazuje na vrcholový/aktuální rámec na zásobníku rámců; slouží pro ukládání lokálních proměnných funkcí (zásobník
rámců lze s výhodou využít při zanořeném či rekurzivním volání funkcí);

- fix move 
I should look at changing type of variable


- I tested 
    WORKING:
        PUSHS
        POPS
        DEFVAR
        MOVE
        WRITE
        ADD
        SUB
        LABEL
        JUMP
        SETCHAR
-definite test
    SETCHAR
    GETCHAR
    STRLEN
    CONCAT
    WRITE
    DEFVAR
    MOVE
    CREATEFRAME
    PUSHFRAME
    POPFRAME
    CALL
    RETURN
    PUSHS
    POPS
    ADD
    SUB
    MUL
    IDIV

- prepsat if v add a ostatnich do jedne funkce ze ktere bude navratovy hodnoty dve instance classy
- test instructions 
- test frames (local frame)
- prepsat int kontrolu jako regex -> bude stacit CheckType(var, expected type) -> kluci maji try catch
- podivat se pokud xml bude na stdin zda to bude fungovat
- nastavit setVariable aby zmenila typ podle noveho typu promene -> int(), str(),...
- zkontrolovat WRITE hodne essential 
- test defvar add multiple times same var in each frame and check if it returns 52
- prepsat aby zavolala pouze insance interpretu a vse uz se postaral
- podivat se na to kdyz pristupuju do lokalniho ramce co vse musi byt splneno 
- TODO FIX BUG KDYZ PRISTUPUJU DO FRAME LOCAL MEL BYCH PRI EDITU VARIABLE SI VYTAHNOUT ZMENIT A VRATIT ZPET DO STACKU 
- test read pokud bude input file nebo stdin
- otestovat BREAK A DPRINT

TEST FAILURES:
    both/functionCalls
                        /functions10
                        /functions12    - problem in xmlParser in getting root
                        /functions4     
                        /functions5
                        /functions9
    both/eq  
                        /eq2
    both/read       
                        /read_badval    - i think the Expected output is bad 

    interpret-only/arithmetic
                                /incorrectInt   - i think the return type should be 53 not 32
    /interpret-only/32
                                /missing_argument
                                /write_test     - I exit with 32 and before that i write out 0 and it takes as a failed test 