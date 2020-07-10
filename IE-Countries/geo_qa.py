import sys
from .ontology import *
from .parser import *



command = sys.argv[1]
given_input = sys.argv[2]
print("command is", command)
print("input is", given_input)

if command == "create":
    createOntology()



if command == "question":
    print("case2")
    parsed_input = parse_question(given_input)
    print(parsed_input)
    #todo - query according to the parsed_input, print to screen and end run

