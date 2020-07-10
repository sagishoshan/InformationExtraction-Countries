import rdflib

Q1 = "SELECT (count(?s) as ?c) \
        WHERE {\
            ?s <http://example.org/pm_of> ?country.\
        }"

Q2 = "SELECT (count(?country) as ?c) \
        WHERE {\
            ?country <http://example.org/population_of> ?p.\
        }"

Q3 = 'SELECT (count(?country) as ?c) \
        WHERE {\
            ?country <http://example.org/government_of> ?g .\
            FILTER(contains(?g, "republic"))\
        }'

Q4 = 'SELECT (count(?country) as ?c) \
        WHERE {\
            ?country <http://example.org/government_of> ?g .\
            FILTER(contains(?g, "monarchy"))\
        }'


AllQueries = [Q1,Q2,Q3,Q4]


def getData():
    g = rdflib.Graph()
    g.parse("ontology.nt", format="nt")
    for i in range(len(AllQueries)):
        print("Query " + str(i + 1) + ": ")
        x = g.query(AllQueries[i])
        for q in x:
            print(q)
        print("\n\n")

getData()
