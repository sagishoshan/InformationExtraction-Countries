import sys
import requests
import lxml.html
import rdflib
import re
from rdflib import Graph, Literal, RDF, URIRef


### possible inputs ###
# input_string = "Who is the president of <country>?"
# input_string = "Who is the prime minister of <country>?"
# input_string = "What is the population of <country>?"
# input_string = "What is the area of <country>?"
# input_string = "What is the government of <country>?"
# input_string = "What is the capital of <country>?"
# input_string = "When was the president of <country> born?"
# input_string = "When was the prime minister of <country> born?"
# input_string = "Who is <entity entity>?"
# input_string = "Who is <entity>?"


def parse_question(question_to_parse):
    relation = None
    entity = None
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
        print(breakdown)
        return breakdown

    else:
        # print("not a valid sentence")
        return 1


wiki_prefix = "http://en.wikipedia.org"


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def createOntology(name):
    # initialize ontology graph
    g = rdflib.Graph()
    presidentOf = rdflib.URIRef('http://example.org/president_of')
    primeMinisterOf = rdflib.URIRef('http://example.org/pm_of')
    bornAt = rdflib.URIRef('http://example.org/born_at')
    populationOf = rdflib.URIRef('http://example.org/population_of')
    areaOf = rdflib.URIRef('http://example.org/area_of')
    governmentOf = rdflib.URIRef('http://example.org/government_of')
    capitalOf = rdflib.URIRef('http://example.org/capital_of')

    # Get countries list
    res = requests.get(wiki_prefix + "/wiki/List_of_countries_by_population_(United_Nations)")
    doc = lxml.html.fromstring(res.content)
    countryLinks = doc.xpath("//table[2]//tr/td[2]//tr/td[1]//span/a/@href")
    countries = doc.xpath("//table[2]//tr/td[2]//tr/td[1]//span/a/text()")
    countryLinks.append("/wiki/Channel_Islands")
    # get info for each country
    for countryLink in countryLinks:
        res = requests.get(wiki_prefix + countryLink)
        doc = lxml.html.fromstring(res.content)
        president = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/div/a[text() = 'President']/ancestor::tr/td//a/text()")
        primeMinister = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/div/a[text() = 'Prime Minister']/ancestor::tr/td//a/text()")
        if countryLink == "/wiki/Russia":
            population = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Population']/ancestor::tr/following-sibling::tr[1]/td//text()[1]")
            population = population[1:]
        else:
            population = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Population']/ancestor::tr/following-sibling::tr[1]/td/text()")
        if len(population) == 0:
            population = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Population']/ancestor::tr/following-sibling::tr[1]/td/text()")
        area = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Area ']/ancestor::tr/following-sibling::tr[1]/td/text()")
        government = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Government']/ancestor::tr/td//a/text()")
        if len(government) == 0:
            government = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Government']/ancestor::tr/td//a/text()")
        for item in government:
            if hasNumbers(item):
                government.remove(item)
        capital = doc.xpath("//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Capital']/ancestor::tr/td//a/text()")
        presidentLink = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/div/a[text() = 'President']/ancestor::tr/td//a/@href")
        if (len(presidentLink) > 0):
            res = requests.get(wiki_prefix + presidentLink[0])
            doc = lxml.html.fromstring(res.content)
            presidentBirthDate = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Born']/ancestor::tr/td/text()[position()<4]")
        res = requests.get(wiki_prefix + countryLink)
        doc = lxml.html.fromstring(res.content)
        pmLink = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/div/a[text() = 'Prime Minister']/ancestor::tr/td//a/@href")
        if (len(pmLink) > 0):
            res = requests.get(wiki_prefix + pmLink[0])
            doc = lxml.html.fromstring(res.content)
            pmBirthDate = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Born']/ancestor::tr/td/text()[position()<4]")
        countryName = countryLink[6:].replace(" ", "_")
        country = rdflib.URIRef('http://example.org/' + countryName)
        if (len(president) > 0):
            president = rdflib.URIRef('http://example.org/' + president[0].replace(" ", "_"))
            presidentBirthDate = "_".join(presidentBirthDate[:1]).replace(" ", "_")
            g.add((president, presidentOf, country))
            g.add((president, bornAt, Literal(presidentBirthDate)))
        if (len(primeMinister) > 0):
            primeMinister = rdflib.URIRef('http://example.org/' + primeMinister[0].replace(" ", "_"))
            pmBirthDate = "_".join(pmBirthDate[:1]).replace(" ", "_")
            g.add((primeMinister, primeMinisterOf, country))
            g.add((primeMinister, bornAt, Literal(pmBirthDate)))
        if (len(area) > 0):
            area = area[0].replace('\xa0', "_")
            area = area.replace(" ", "")
            if (area[-2:] == "km"):
                area = area + "2"
            else:
                area = area + "_km2"
            g.add((country, areaOf, Literal(area)))
        if (len(population) > 0):
            population = population[0].replace(" ", "").replace("\t","").replace("\n","")
            g.add((country, populationOf, Literal(population)))
        if (len(government) > 0):
            government = "_".join(government).replace(" ", "_")
            g.add((country, governmentOf, Literal(government)))
        if (len(capital) > 0):
            capital = rdflib.URIRef('http://example.org/' + capital[0].replace(" ", "_"))
            g.add((capital, capitalOf, country))
    g.serialize(name, format="nt")


#interface
command = sys.argv[1]
given_input = sys.argv[2]

if command == "create":
    createOntology(given_input)

if command == "question":
    parsed_input = parse_question(given_input)
    print(parsed_input)

