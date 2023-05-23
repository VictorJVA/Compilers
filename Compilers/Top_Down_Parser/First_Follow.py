import re

start_sym=""
productions={}
first_table={}
follow_table={}
terminals_table=[]

grammar = open("Top_Down_Parser/Example_Grammars/Grammar7.txt")

def Create_productions(grammar):
    global start_sym
    for production in grammar:
        lhs, rhs = re.split("->", production)
        rhs = re.split("\||\n", rhs)
        productions[lhs] = set(rhs) - {''}
        if not start_sym:
            start_sym = lhs

def isNonterminal(sym):

    if sym.isupper():
        return True
    else:
        if sym not in terminals_table and sym != "@":
            terminals_table.append(sym)
        return False
    
def firstFunc(sym):

    if sym in first_table:
        return first_table[sym]
    
    if isNonterminal(sym):
        
        first = set()

        for x in productions[sym]:

            if x == "&":
                first = first.union('&')

            else:

                for i in range(len(x)+1):

                    fst = firstFunc(x[i])                        

                    if i < len(x)-1:

                        first = first.union(fst - {'&'})

                        if "@" in fst and isNonterminal(x[i+1]) and isNonterminal(x[i]):
                            first = first.union(firstFunc(x[i+1]))

                        else:

                            break

                    else:
                        first = first.union(fst)

                    if '&' not in fst:
                        break                    

        return first
    else:
        return set(sym)



        
def followFunc(sym):
    
    if sym not in follow_table:
        follow_table[sym] = set()
    for nt in productions.keys():
        for rule in productions[nt]:
            pos = rule.find(sym)
            if pos != -1:
                if pos == (len(rule) - 1):
                    if nt != sym:
                        follow_table[sym] = follow_table[sym].union(followFunc(nt))
                else:
                    first_next = set()
                    is_epsilon = True
                    cont=0

                    for next in rule[pos + 1:]:
                        first_next = firstFunc(next)
                        if "@" not in first_next:
                            is_epsilon = False
                        cont+=1
            
                        
                        if '@' in first_next:
                            
                            if nt != sym:

                                follow_table[sym] = follow_table[sym].union(first_next) - {'@'}

                                if (rule.find(sym)+2)<len(rule):
                                
                                    follow_table[sym] = follow_table[sym].union(firstFunc(rule[rule.find(sym)+2]))
                        

                    if is_epsilon==True:
                        follow_table[sym] = follow_table[sym].union(followFunc(nt))
                        
                    else:
                        follow_table[sym] = follow_table[sym].union(first_next - {'@'})

    return follow_table[sym]                                    


def Create_tables():
    for nonterminal in productions:
        first_table[nonterminal] = firstFunc(nonterminal)
    follow_table[start_sym] = set('$')
    terminals_table.append("$")
    for nt in productions:
        follow_table[nt] = followFunc(nt)

def print_tables():
    print('First')
    for nonterminal in productions:
        print(nonterminal + ':' + str(first_table[nonterminal]))
    print('\n')
    print("Follow")
    for nonterminal in productions:
        print(nonterminal + ':' + str(follow_table[nonterminal]))    
    print("\n")

def Top_Down_Parser():
    Create_productions(grammar)
    Create_tables()

                        
