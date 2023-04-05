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

- prepsat if v add a ostatnich do jedne funkce ze ktere bude navratovy hodnoty dve instance classy
- test instructions 
- test frames (local frame)
- prepsat int kontrolu jako regex -> bude stacit CheckType(var, expected type) -> kluci maji try catch
- podivat se pokud xml bude na stdin zda to bude fungovat
- JUMPIFEQ nefunguje 
- sekvence /032 nefunguje 
- zalezi na velikosti pismene instrukce MOVE/move?
- nastavit setVariable aby zmenila typ podle noveho typu promene -> int(), str(),...
- WRITE STILL THERE ARE \032 ... 