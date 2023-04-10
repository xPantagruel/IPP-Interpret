- test frames (local frame)
- prepsat int kontrolu jako regex -> bude stacit CheckType(var, expected type) -> kluci maji try catch
- podivat se pokud xml bude na stdin zda to bude fungovat
- test read pokud bude input file nebo stdin
- otestovat BREAK
- kouknout jestli by nemelo byt try: except Exception:
- test #TODO FIX THIS IN README NOTE THAT I SHOULD POP BACK THE WHOLE LIST

TEST FAILURES:
    both/functionCalls
                        /functions10
                        /functions12    - problem in parser
                        /functions4     
                        /functions5
                        /functions9
    both/read       
                        /read_badval    - i think the Expected output is bad 

    interpret-only/arithmetic
                                /incorrectInt   - i can fix this by checking it in xml parser
    /interpret-only/32
                                /write_test     - I exit with 32 and before that i write out 0 and it takes as a failed test 
