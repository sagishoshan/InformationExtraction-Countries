import requests
import lxml.html
import rdflib
from rdflib import Graph, Literal, RDF, URIRef
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF, XSD

wiki_prefix = "http://en.wikipedia.org"


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def createOntology():
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
            presidentBirthDate = rdflib.URIRef('http://example.org/' + "_".join(presidentBirthDate[:1]).replace(" ", "_"))
            g.add((president, presidentOf, country))
            g.add((president, bornAt, presidentBirthDate))
        if (len(primeMinister) > 0):
            primeMinister = rdflib.URIRef('http://example.org/' + primeMinister[0].replace(" ", "_"))
            pmBirthDate = rdflib.URIRef('http://example.org/' + "_".join(pmBirthDate[:1]).replace(" ", "_"))
            g.add((primeMinister, primeMinisterOf, country))
            g.add((primeMinister, bornAt, pmBirthDate))
        if (len(area) > 0):
            area = area[0].replace('\xa0', "_")
            area = area.replace(" ", "")
            if (area[-2:] == "km"):
                area = area + "2"
            else:
                area = area + "_km2"
            area = rdflib.URIRef('http://example.org/' + area)
            g.add((area, areaOf, country))
        if (len(population) > 0):
            population = rdflib.URIRef('http://example.org/' + population[0].replace(" ", ""))
            g.add((population, populationOf, country))
        if (len(government) > 0):
            government = rdflib.URIRef('http://example.org/' + "_".join(government).replace(" ", "_"))
            g.add((government, governmentOf, country))
        if (len(capital) > 0):
            capital = rdflib.URIRef('http://example.org/' + capital[0].replace(" ", "_"))
            g.add((capital, capitalOf, country))
    g.serialize("ontology.nt", format="nt")

