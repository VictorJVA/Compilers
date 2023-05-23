import re
#from Top_Down_Parser.First_Follow import *

class ItemCollection:
    def __init__(self):
        self.item = []

    def add_item(self, item):
        self.item.extend(item)

    def remove_item(self, item):
        self.item.remove(item)

    def show_items(self):
        for item in self.items:
            print(item.item)

    def validate_item(self, item):
        if item in self.item:
            return True
        else:
            return False        

class States:

    def __init__(self):
        self.items = []
        self.shift = {}
        self.reduce = {}

    def add_items(self, item):
        self.items.append(item)

    def remove_items(self, item):
        self.items.remove(item)

    def show_items(self):
        for item in self.items:
            print(item.item)

    def add_shift(self, symbol, state):
        self.shift[symbol] = state

    def add_reduce(self, symbol, production):
        self.reduce[symbol] = production       


class StateCollection:
    def __init__(self):
        self.states = set()

    def add_state(self, state):
        if state not in self.states:
            self.states.add(state)

    def remove_state(self, state):
        self.states.remove(state)

    def show_states(self):
        
        print("States:")
        for state in self.states:
            #print("State", state_id)
            print("Items:", state.items)
            print("Shifts:", state.shift)
            print("Reduces:", state.reduce)
            print()

grammar = open("Top_Down_Parser/Example_Grammars/Grammar0.txt")

start_sym=""
terminals_table=[]
nonterminals_table=[]
terminals_and_nonterminals = []
All_gotoes = []

def Create_productions(grammar, productions):

    global start_sym
    for production in grammar:
        lhs, rhs = re.split("->", production)
        rhs = re.split("\||\n", rhs)
        productions[lhs] = set(rhs) - {''}
        if not start_sym:
            start_sym = lhs

    return productions        

def augmented_grammar(productions):
    
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for letter in letters:
        if letter not in productions.keys():
            for i in productions.keys():
                productions[letter] = {"."+i}
                break
            break

    return productions, productions[letter]

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


def get_goto_symbols(state):

    goto_symbols = []

    for item in state:

        dot_index = item.find('.')


        if  dot_index!=-1 and dot_index < len(item)-1:
            next_symbol = item[dot_index + 1]
            goto_symbols.append(next_symbol)

    return remove_duplicates(goto_symbols)


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

    return goto

def validate_goto(state_items):

    goto_symbols = get_goto_symbols(state_items)
    goto_items = []
    vacio = []

    for symbol in goto_symbols:
        goto_items = goto(state_items,symbol)[symbol]
        if goto_items not in All_gotoes:
            return goto_items in All_gotoes, goto_items
        else:
            continue

    return True, vacio


def LR0(state_items, productions, Object_state, Object_StateCollection, Object_Items):

    
    goto_symbols = get_goto_symbols(state_items)
    print(state_items)


    if len(goto_symbols)==0:
        return state_items

    if len(goto_symbols)>0:

        for l in goto_symbols:

            goto_items = goto(state_items,l)[l]
            state_closure_items = []
            state_closure_items.extend(goto_items)

            for i in goto_items:
                state_closure_items.extend(closure(str(i), productions))
            
            print(str(state_closure_items)+"Este es el estado")

            ##valido, result = validate_goto (state_items)

            if goto_items not in All_gotoes:

                All_gotoes.append(goto_items)
                Object_Items.add_item(state_closure_items)
                Current_state = States()
                Current_state.add_items(state_closure_items)
                #Current_state.add_shift(l)
                #Current_state.add_reduce()
                Object_StateCollection.add_state(Current_state)
                LR0(state_closure_items, productions, Object_state, Object_StateCollection, Object_Items)

            else:

                break


def Main():

    productions = {}
    productions = Create_productions(grammar, productions) #Fist, create productions

    #Then put terminals and nonterminals in a list

    for i in productions:
        isNonterminal(i)
        for j in productions[i]:
            for k in j:
                isNonterminal(k)

    #Then create augmented grammar

    productions, state_0 = augmented_grammar(productions)

    #Later, we create the Zero state

    closure_items = closure(str(state_0), productions)
    print(closure_items)    

    #Agrego el item inicial

    closure_items.extend(str(item) for item in state_0)
    
    Object_Items = ItemCollection()
    Object_Items.add_item(closure_items)

    Object_state = States()
    Object_state.add_items(Object_Items)

    Object_StateCollection = StateCollection()
    Object_StateCollection.add_state(Object_state)

    #Ahora vamos a crear los demás estados por profundidad a partir de este

    ##All_gotoes.extend(closure_items)
    LR0(closure_items, productions, Object_state, Object_StateCollection, Object_Items)

    #Imprimir los estados
    Object_StateCollection.show_states()

    #obtener los shifts y reduces


Main()    




