from Parsing_Table import*
from First_Follow import*

stack = []

def invertir_cadena(cadena):
    for i in range(len(cadena) - 1, -1, -1):
        stack.append(cadena[i])

def buffer_reading(input_to_read):
    #start symbol to stack
    initial_symbol=list(productions.keys())
    input_to_read=input_to_read+"$"
    stack.append("$")
    stack.append(initial_symbol[0])
    print(stack)
    
    while(len(stack)>1):
        if(str(stack[-1])!="$" and str(stack[-1]).isupper()):
            reading_symbol=str(stack.pop())
            rules=parsing_table[reading_symbol][input_to_read[0]]
            if rules=="0":
                return False
            invertir_cadena(rules)
            print(stack)
            print(rules)
            print("Input:"+input_to_read)
            print("-------------------------------")

        else:
            if stack[-1]!="$" and stack[-1]==input_to_read[0]:
                if len(input_to_read)>1:
                    input_to_read=input_to_read[1:]
                    stack.pop()
                    print(stack)
                    print("Input:"+input_to_read)
                    print("-------------------------------")
            else:
                if stack[-1]=="@":
                    stack.pop()
                    print("Input:"+input_to_read)  
                    print("-------------------------------")
                else:
                    break    

    print(stack, input_to_read)
    if len(stack)==1 and str(stack[0])==input_to_read:
        return True
    else:
        return False                   


def Buffer_input():
    input_to_read=input("Put your input here: ")
    if buffer_reading(input_to_read):
        print("It's valid")
    else:
        print("It's NOT valid")