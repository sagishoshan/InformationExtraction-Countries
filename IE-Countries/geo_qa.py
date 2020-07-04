import sys
import parser

command = sys.argv[1]
given_input = sys.argv[2]
print("command is", command)
print("input is", given_input)

if command == "create":
    print("case1")
    #todo - create an ontology "ontology.nt" (given_input)



if command == "question":
    print("case2")
    parsed_input = parser.parse_question(given_input)
    print(parsed_input)
    #todo - query according to the parsed_input, print to screen and end run

