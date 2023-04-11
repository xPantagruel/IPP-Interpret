- vytvorit soubor pro rozsireni 

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
