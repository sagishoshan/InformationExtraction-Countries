import re
# input_string = "Who is the president of <country>?"
# input_string = "Who is the prime minister of <country>?"
# input_string = "What is the population of <country>?"
# input_string = "What is the area of <country>?"
# input_string = "What is the government of <country>?"
# input_string = "What is the capital of <country>?"
# input_string = "When was the president of <country> born?"
# input_string = "When was the prime minister of <country> born?"
input_string = "Who is <entity>?"


input_breakdown = re.findall(r'[a-zA-Z]+',input_string)
# print(input_breakdown)

if input_string.startswith("Who is"):
    print("case1")

    if len(input_breakdown) > 3:

        if input_breakdown[3] == "president":
            print("searching for the president of...")

        elif input_breakdown[3] == "prime" and input_breakdown[4] == "minister":
            print("searching for the prime minister of...")

        else:
            print("searching for the entity... PART1")


    else:
        print("searching for the entity... PART2")

if input_string.startswith("What is the "):
    print("case2")

    if input_breakdown[3] == "population":
        print("searching for the population of...")

    elif input_breakdown[3] == "area":
        print("searching for the area of...")

    elif input_breakdown[3] == "government":
        print("searching for the goverment of...")

    elif input_breakdown[3] == "capital":
        print("searching for the capital of...")

if input_string.startswith("When was the "):
    print("case3")
    if input_breakdown[3] == "president":
        print("searching for the when president of... was born")

    elif input_breakdown[3] == "prime" and input_breakdown[4] == "minister":
        print("searching for the when president of... was born")

# relation =
# given_object =



