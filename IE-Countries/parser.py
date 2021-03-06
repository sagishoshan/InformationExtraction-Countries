import re

### possible inputs ###
input_string = "Who is the president of <country>?"
# input_string = "Who is the prime minister of <country>?"
# input_string = "What is the population of <country>?"
# input_string = "What is the area of <country>?"
# input_string = "What is the government of <country>?"
# input_string = "What is the capital of <country>?"
# input_string = "When was the president of <country> born?"
# input_string = "When was the prime minister of <country> born?"
# input_string = "Who is <entity entity>?"
# input_string = "Who is <entity>?"


def parse_question(question_to_parse_with_frame):
    relation = None
    entity = None

    question_to_parse = question_to_parse_with_frame[1:-1]  # remove <> from the question

    input_length = len(question_to_parse)
    input_breakdown = re.findall(r'[a-zA-Z]+', question_to_parse)

    if question_to_parse.startswith("Who is"):

        if len(input_breakdown) > 3:

            if input_breakdown[3] == "president":
                prefix_length = len("Who is the president of ")
                sufix_length = len("?")

                relation = "president"
                entity = question_to_parse[prefix_length:input_length - sufix_length]

            elif input_breakdown[3] == "prime" and input_breakdown[4] == "minister":
                prefix_length = len("Who is the prime minister of ")
                sufix_length = len("?")

                relation = "prime minister"
                entity = question_to_parse[prefix_length:input_length - sufix_length]

            else:
                prefix_length = len("Who is ")
                sufix_length = len("?")

                relation = "entity"
                entity = question_to_parse[prefix_length:input_length - sufix_length]

        else:
            prefix_length = len("Who is ")
            sufix_length = len("?")

            relation = "entity"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

    if question_to_parse.startswith("What is the "):

        if input_breakdown[3] == "population":
            prefix_length = len("What is the population of ")
            sufix_length = len("?")

            relation = "population"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

        elif input_breakdown[3] == "area":
            prefix_length = len("What is the area of ")
            sufix_length = len("?")

            relation = "area"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

        elif input_breakdown[3] == "government":
            prefix_length = len("What is the government of ")
            sufix_length = len("?")

            relation = "government"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

        elif input_breakdown[3] == "capital":
            prefix_length = len("What is the capital of ")
            sufix_length = len("?")

            relation = "capital"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

    if question_to_parse.startswith("When was the "):

        if input_breakdown[3] == "president":
            prefix_length = len("When was the president of ")
            sufix_length = len(" born?")

            relation = "president born"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

        elif input_breakdown[3] == "prime" and input_breakdown[4] == "minister":
            prefix_length = len("When was the prime minister of ")
            sufix_length = len(" born?")

            relation = "prime minister born"
            entity = question_to_parse[prefix_length:input_length - sufix_length]

    if relation is not None and entity is not None:
        breakdown = [relation, entity]
        # print(breakdown)
        return breakdown

    else:
        # print("not a valid sentence")
        return 1

# parse_question(input_string)
