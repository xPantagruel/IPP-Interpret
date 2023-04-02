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

classes 
- zabalit kazdou instrukci jako class ktera bude mit execution
- vse se to bude volat z class interpret ktera bude mit v sobe instruction a ta v sobe bude mit instrukce jeste 