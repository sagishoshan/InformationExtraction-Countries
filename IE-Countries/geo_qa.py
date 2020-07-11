import sys
import requests
import lxml.html
import rdflib
import re
from rdflib import Graph, Literal, RDF, URIRef
import datetime


def parse_question(question_to_parse):
    relation = None
    entity = None
    input_length = len(question_to_parse)
    input_breakdown = re.findall(r'[a-zA-Z]+', question_to_parse)
    # initialize ontology graph
    g = rdflib.Graph()
    g.parse("ontology.nt", format="nt")
    if question_to_parse.startswith("Who is"):
        if len(input_breakdown) > 3:
            if input_breakdown[3] == "president":
                prefix_length = len("Who is the president of ")
                suffix_length = len("?")
                relation = "president"
                entity = question_to_parse[prefix_length:input_length - suffix_length]
                Q1 = "SELECT ?s \
                        WHERE {\
                            ?s <http://example.org/president_of>" + "<http://example.org/" + entity.replace(" ", "_") + "> . \
                        }"
                x = g.query(Q1)
                if len(x) == 0:
                    print("We didn't find an answer for this question in the ontology.")
                    return
                for q in x:
                    print(q[0][19:].replace("_"," "))
            elif input_breakdown[3] == "prime" and input_breakdown[4] == "minister":
                prefix_length = len("Who is the prime minister of ")
                suffix_length = len("?")
                relation = "prime minister"
                entity = question_to_parse[prefix_length:input_length - suffix_length]
                Q1 = "SELECT ?s \
                        WHERE {\
                            ?s <http://example.org/pm_of>" + "<http://example.org/" + entity.replace(" ", "_") + "> . \
                        }"
                x = g.query(Q1)
                if len(x) == 0:
                    print("We didn't find an answer for this question in the ontology.")
                    return
                for q in x:
                    print(q[0][19:].replace("_"," "))
            else:
                prefix_length = len("Who is ")
                suffix_length = len("?")
                relation = "entity"
                entity = question_to_parse[prefix_length:input_length - suffix_length]
                Q1 = "SELECT ?c ?r \
                        WHERE {\
                            <http://example.org/" + entity.replace(" ","_") + "> ?r ?c . \
                        }"
                x = g.query(Q1)
                if len(x) == 0:
                    print("We didn't find an answer for this question in the ontology.")
                    return
                for q in x:
                    if q[1][19:] == "president_of":
                        print("President of " + q[0][19:].replace("_", " "))
                    elif q[1][19:] == "pm_of":
                        print("Prime minister of " + q[0][19:].replace("_", " "))
        else:
            prefix_length = len("Who is ")
            sufix_length = len("?")

            relation = "entity"
            entity = question_to_parse[prefix_length:input_length - sufix_length]
    if question_to_parse.startswith("What is the "):
        if input_breakdown[3] == "population":
            prefix_length = len("What is the population of ")
            suffix_length = len("?")
            relation = "population"
            entity = question_to_parse[prefix_length:input_length - suffix_length]
            Q1 = "SELECT ?s \
                    WHERE {\
                      <http://example.org/" + entity.replace(" ", "_") + ">   <http://example.org/population_of> ?s . \
                    }"
            x = g.query(Q1)
            if len(x) == 0:
                print("We didn't find an answer for this question in the ontology.")
                return
            for q in x:
                try:
                    print(q[0][:q[0].index("(")])
                except ValueError:
                    print(q[0])

        elif input_breakdown[3] == "area":
            prefix_length = len("What is the area of ")
            suffix_length = len("?")
            relation = "area"
            entity = question_to_parse[prefix_length:input_length - suffix_length]
            Q1 = "SELECT ?s \
                    WHERE {\
                      <http://example.org/" + entity.replace(" ", "_") + ">   <http://example.org/area_of> ?s . \
                    }"
            x = g.query(Q1)
            if len(x) == 0:
                print("We didn't find an answer for this question in the ontology.")
                return
            for q in x:
                print(q[0].replace("\u2013","-").replace("_"," "))

        elif input_breakdown[3] == "government":
            prefix_length = len("What is the government of ")
            suffix_length = len("?")
            relation = "government"
            entity = question_to_parse[prefix_length:input_length - suffix_length]
            Q1 = "SELECT ?s \
                    WHERE {\
                      <http://example.org/" + entity.replace(" ", "_") + ">   <http://example.org/government_of> ?s . \
                    }"
            x = g.query(Q1)
            if len(x) == 0:
                print("We didn't find an answer for this question in the ontology.")
                return
            for q in x:
                if q[0][len(q[0])-1] == "]":
                    print(q[0].replace("\u2013", "-").replace("_", " ")[:-3])
                else:
                    print(q[0].replace("\u2013", "-").replace("_", " "))

        elif input_breakdown[3] == "capital":
            prefix_length = len("What is the capital of ")
            suffix_length = len("?")
            relation = "capital"
            entity = question_to_parse[prefix_length:input_length - suffix_length]
            Q1 = "SELECT ?s \
                    WHERE {\
                        ?s <http://example.org/capital_of>" + "<http://example.org/" + entity.replace(" ", "_") + "> . \
                    }"
            x = g.query(Q1)
            if len(x) == 0:
                print("We didn't find an answer for this question in the ontology.")
                return
            for q in x:
                print(q[0][19:].replace("_", " "))

    if question_to_parse.startswith("When was the "):
        if input_breakdown[3] == "president":
            prefix_length = len("When was the president of ")
            suffix_length = len(" born?")
            relation = "president born"
            entity = question_to_parse[prefix_length:input_length - suffix_length]
            Q1 = "SELECT ?d \
                    WHERE {\
                        ?s <http://example.org/president_of>" + "<http://example.org/" + entity.replace(" ", "_") + "> .\
                        ?s <http://example.org/born_at> ?d . \
                     } "
            x = g.query(Q1)
            if len(x) == 0:
                print("We didn't find an answer for this question in the ontology.")
                return
            for q in x:
                for fmt in ('%d %B %Y', '%B %d, %Y'):
                    try:
                        print(datetime.datetime.strptime(q[0].replace("_", " "), fmt).date())
                    except ValueError:
                        pass

        elif input_breakdown[3] == "prime" and input_breakdown[4] == "minister":
            prefix_length = len("When was the prime minister of ")
            suffix_length = len(" born?")
            relation = "prime minister born"
            entity = question_to_parse[prefix_length:input_length - suffix_length]
            Q1 = "SELECT ?d \
                    WHERE {\
                        ?s <http://example.org/pm_of>" + "<http://example.org/" + entity.replace(" ", "_") + "> .\
                        ?s <http://example.org/born_at> ?d . \
                     } "
            x = g.query(Q1)
            if len(x) == 0:
                print("We didn't find an answer for this question in the ontology.")
                return
            for q in x:
                for fmt in ('%d %B %Y', '%B %d, %Y'):
                    try:
                        print(datetime.datetime.strptime(q[0].replace("_", " "), fmt).date())
                    except ValueError:
                        pass

    if relation is not None and entity is not None:
        breakdown = [relation, entity]
        return breakdown

    else:
        print("The question is not a valid one")
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
        if len(population) == 0:
            population = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Population']/ancestor::tr/following-sibling::tr[1]/td/span/text()")
        if countryLink == "/wiki/Dominican_Republic" or countryLink == "/wiki/Vanuatu":
            population = doc.xpath("//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Population']/ancestor::tr/following-sibling::tr[1]/td/span/text()")
        if countryLink == "/wiki/Channel_Islands":
            population = doc.xpath("//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Population']/ancestor::tr/td/text()")
        area = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Area ']/ancestor::tr/following-sibling::tr["
            "1]/td/text()")
        if len(area) == 0:
            area = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Area']/ancestor::tr/following-sibling::tr["
                "1]/td/text()")
        if len(area) == 0:
            area = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Area']/ancestor::tr/following-sibling::tr[1]/td/text()")
        government = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/a[text() = 'Government']/ancestor::tr/td//a/text()")
        if len(government) == 0:
            government = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Government']/ancestor::tr/td//a/text()")
        for item in government:
            if hasNumbers(item):
                government.remove(item)
        capital = doc.xpath("//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Capital']/ancestor::tr/td//a/text()")
        if countryLink == "/wiki/Vatican_City":
            capital = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Capital']/ancestor::tr/td/span/b/text()")
        presidentLink = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/div/a[text() = 'President']/ancestor::tr/td//a/@href")
        presidentBirthDate = ""
        if len(presidentLink) > 0:
            res = requests.get(wiki_prefix + presidentLink[0])
            doc = lxml.html.fromstring(res.content)
            presidentBirthDate = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Born']/ancestor::tr/td/text()[position()<4]")
        res = requests.get(wiki_prefix + countryLink)
        doc = lxml.html.fromstring(res.content)
        pmLink = doc.xpath(
            "//table[contains(@class,'infobox')]/tbody/tr/th/div/a[text() = 'Prime Minister']/ancestor::tr/td//a/@href")
        pmBirthDate = ""
        if len(pmLink) > 0:
            res = requests.get(wiki_prefix + pmLink[0])
            doc = lxml.html.fromstring(res.content)
            pmBirthDate = doc.xpath(
                "//table[contains(@class,'infobox')]/tbody/tr/th[text() = 'Born']/ancestor::tr/td/text()[position()<4]")
        countryName = countryLink[6:].replace(" ", "_")
        country = rdflib.URIRef('http://example.org/' + countryName)
        if len(president) > 0:
            president = rdflib.URIRef('http://example.org/' + president[0].replace(" ", "_"))
            presidentBirthDate = "_".join(presidentBirthDate[:1]).replace(" ", "_")
            g.add((president, presidentOf, country))
            g.add((president, bornAt, Literal(presidentBirthDate)))
        if len(primeMinister) > 0:
            primeMinister = rdflib.URIRef('http://example.org/' + primeMinister[0].replace(" ", "_"))
            pmBirthDate = "_".join(pmBirthDate[:1]).replace(" ", "_")
            g.add((primeMinister, primeMinisterOf, country))
            g.add((primeMinister, bornAt, Literal(pmBirthDate)))
        if len(area) > 0:
            area = area[0].replace('\xa0', "_")
            area = area.replace(" ", "")
            if area[-2:] == "km":
                area = area + "2"
            else:
                area = area + "_km2"
            g.add((country, areaOf, Literal(area)))
        if len(population) > 0:
            population = population[0].replace(" ", "").replace("\t","").replace("\n","")
            g.add((country, populationOf, Literal(population)))
        if len(government) > 0:
            government = "_".join(government).replace(" ", "_")
            g.add((country, governmentOf, Literal(government)))
        if len(capital) > 0:
            capital = rdflib.URIRef('http://example.org/' + capital[0].replace(" ", "_"))
            g.add((capital, capitalOf, country))
    g.serialize(name, format="nt")


# CLI
command = sys.argv[1]
given_input = sys.argv[2]

if command == "create":
    createOntology(given_input)

if command == "question":
    parse_question(given_input)

