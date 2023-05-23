from First_Follow import*
from Buffer_input import*

parsing_table = {}

# Initialize parsing table with error entries
def Initialize_table():
    for non_terminal in productions.keys():
        parsing_table[non_terminal] = {}
        for terminal in terminals_table:
            parsing_table[non_terminal][terminal] = "0"


def Create_parsing_table():
        for non_terminal, production_rules in productions.items():
            for rule in production_rules:

                if rule!="@":
                    rule_first = first_table[non_terminal]
                    for terminal in rule_first:
                        if terminal != "@":
                            if rule[0] in terminals_table and terminal==rule[0]:
                                if parsing_table[non_terminal][terminal] != "0":
                                    return False
                                else:
                                    parsing_table[non_terminal][terminal] = rule
                            elif rule[0].isupper() and terminal in first_table[rule[0]]:
                                if parsing_table[non_terminal][terminal] != "0":
                                    return False
                                else:
                                    parsing_table[non_terminal][terminal] = rule     
                        else:
                            continue
                        
            if rule!="@":
                if '@' in rule_first:
                    rule_follow = follow_table[non_terminal]
                    for terminal in rule_follow:
                        if parsing_table[non_terminal][terminal] != "0":
                            return False
                        else:
                            parsing_table[non_terminal][terminal] = '@' 
        return True 

            
def print_parsing_table():
    print("LL(1) Parsing Table:")
    terminals = sorted(terminals_table)
    header = " ".join(terminals_table)
    print("{:<5} {}".format("", header))
    for non_terminal, row in parsing_table.items():
        values = [row[terminal] for terminal in terminals_table]
        print("{:<5} {}".format(non_terminal, " ".join(values)))
                       

def Parsing_Table():
    Initialize_table()
    print_tables()
    if Create_parsing_table():
        print_parsing_table()
        return True
    else:
        print("OOPS, ERORR!!, It's not a LL(1) Grammar")

# Print the LL(1) parsing table


  