from Buffer_input import*
from Parsing_Table import*
from First_Follow import*


def Main():
    Top_Down_Parser()
    valid=Parsing_Table()
    if valid:
        Buffer_input()

Main()
    