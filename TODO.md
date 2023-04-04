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

- prepsat if v add a ostatnich do jedne funkce ze ktere bude navratovy hodnoty dve instance classy
- test instructions 
- test frames (local frame)
- prepsat int kontrolu jako regex -> bude stacit CheckType(var, expected type)
- podivat se pokud xml bude na stdin zda to bude fungovat