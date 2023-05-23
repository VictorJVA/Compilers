import re
from collections import defaultdict

grammar = open("Top_Down_Parser/Example_Grammars/Grammar10.txt")

productions={}
start_sym=""
terminals_table=[]
nonterminals_table=[]
terminals_and_nonterminals = []
state0 = {}
states = []

def augmented_grammar(productions):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for letter in letters:
        if letter not in productions.keys():
            for i in productions.keys():
                productions[letter] = {"."+i}
                break
            break

    return productions, productions[letter]
    
def Create_productions(grammar):
    global start_sym
    for production in grammar:
        lhs, rhs = re.split("->", production)
        rhs = re.split("\||\n", rhs)
        productions[lhs] = set(rhs) - {''}
        if not start_sym:
            start_sym = lhs

def isNonterminal(sym):
    if sym.isupper() and sym not in nonterminals_table:
        nonterminals_table.append(sym)
    else:
        if sym not in terminals_table and sym != "@" and sym.isupper()==False:
            terminals_table.append(sym)
            

def remove_duplicates(arr):
    unique_arr = []
    for sub_arr in arr:
        if sub_arr not in unique_arr:
            unique_arr.append(sub_arr)
    return unique_arr

def get_values_with_dot_at_start(dictionary, key):
    words=[]
    for value in dictionary[key]:
            words.append("."+value)
            if value[0] not in terminals_and_nonterminals:
                terminals_and_nonterminals.append(value[0])
    return words


def closure(state, productions):

    
    closure_items = []
    dot_index = state.find(".")

    if dot_index != -1 and dot_index < len(state) - 1 and state[dot_index + 1].isupper():
        next_symbol = state[dot_index + 1]

        if next_symbol not in nonterminals_table:
            return closure_items

        temporal_closure = get_values_with_dot_at_start(productions, next_symbol)
        closure_items.extend(temporal_closure)  # Agregar los elementos del cierre temporal a closure_items

        # Calcular el cierre de cada elemento agregado
        for item in temporal_closure:
            if item[1]!=state[1]:
                closure_items.extend(closure(item, productions))

    return remove_duplicates(closure_items)


def get_goto_symbols(state):

    goto_symbols = []

    for item in state:

        dot_index = item.find('.')


        if  dot_index!=-1 and dot_index < len(item)-1:
            next_symbol = item[dot_index + 1]
            goto_symbols.append(next_symbol)

    return remove_duplicates(goto_symbols)
   

def goto(state, symbol):

    goto = {}

    goto[symbol] = []
    if len(state) > 0:
        for item in state:
                if len(item)>1:
                    dot_index = item.index('.')
                    if dot_index < len(item) - 1 and item[dot_index + 1] == symbol:
                        new_item = item[:dot_index] + symbol + '.' + item[dot_index + 2:]
                        goto[symbol].append(new_item)

    if len(goto[symbol]) != 0:
        for i in goto.values():
            goto[symbol].extend(closure(str(i),productions ))

    return goto


# Ejemplo de gramática representada como diccionario
Create_productions(grammar)

for i in productions:
    isNonterminal(i)
    for j in productions[i]:
        for k in j:
            isNonterminal(k)
         
productions, state_0 = augmented_grammar(productions)
closure_items = closure(str(state_0), productions)
closure_items = closure_items.append(state_0)


"""print("Items:")
for nonterminal, item_set in items.items():
    print(nonterminal, item_set) """

print("\nClosure Items:")
for item in closure_items:
    print(item)


class Item:
    def __init__(self):
        self.back = []

class State:
    def __init__(self):
        self.diccionario = {}

class LR0CANONICAL:
    def __init__(self):
        self.estados = []

def agregar_estado(lr_canonical, estado):
    lr_canonical.estados.append(estado) 

def imprimir_estados_canonical_lr(lr_canonical):
    for estado in lr_canonical.estados:
        print(estado.diccionario)

def validar_estado(lr_canonical, item):

    falses = []
    all_items = []

    for estados in lr_canonical.estados:
            for items in estados.diccionario.values():
                all_items.extend(items)

    for items0 in item:
        if items0 not in all_items:
                falses.append(items0)

    print(all_items)            

    if len(falses)==0:
        return True, falses
    else:
        return False, falses   

def agregar_estados():

    for estado in object_LR0.estados:

        for value in estado.diccionario.values():

                if len(value)>0:

                    state_result = LR0(value)
                    object_state = State()
                    object_state.diccionario = state_result
                    ##agregar_estado(object_LR0, object_state)


                else:
                    continue


object_LR0 = LR0CANONICAL()
cont=0


print("\nGoTo Items0:")
for symbol in terminals_and_nonterminals:
    goto_items= goto(closure_items, symbol)
    object_state = State()
    object_state.diccionario = goto_items
    agregar_estado(object_LR0, object_state)

imprimir_estados_canonical_lr(object_LR0)      

items_goto = []

def LR0(state_items):
    
    goto_symbols = get_goto_symbols(state_items)
    print(state_items)
    print(str(goto_symbols)+"chejej")

    if len(goto_symbols)==0:
        return state_items

    if len(goto_symbols)>0:

        for l in goto_symbols:

            goto_items = goto(state_items,l)[l]
            items_goto.append(goto_items)
            ##print(str(goto_items)+"estos son los items goto")

            valido, item = validar_estado(object_LR0, goto_items)

            if valido==False:

                print(validar_estado(object_LR0, item))
                ##print("se va con este ya que no esta aun" + str(item))
                LR0(item)

            else:

                break

agregar_estados()
print("siuuuuuuuuuuuuu")
imprimir_estados_canonical_lr(object_LR0)
##print(items_goto)