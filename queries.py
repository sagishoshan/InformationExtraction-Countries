import rdflib

Q1 = "SELECT COUNT(DISTINCT ?country) \
        WHERE { \
            ?city <http://example.org/capital_of> ?country . \
        }"

# Q2 = "select ?player ?team \
#         where { \
#             ?player <http://example.org/playsFor> ?team . \
#             ?player <http://example.org/birthDate> ?date . \
#             FILTER ( ?date >= '1994-12-31'^^xsd:date) \
#         }"
#
# Q3 = "select ?player \
#         where { \
#             ?player <http://example.org/birthPlace> ?city . \
#             ?player <http://example.org/playsFor> ?team . \
#             ?team <http://example.org/homeCity> ?city . \
#         }"
#
# Q4 = "select ?team1 ?team2 \
#         where { \
#             ?team1 <http://example.org/homeCity> ?city . \
#             ?team2 <http://example.org/homeCity> ?city . \
#             FILTER(STR(?team1) < STR(?team2)) \
#         }"

AllQueries = [Q1, Q2, Q3, Q4]


def getData():
    g = rdflib.Graph()
    g.parse("ontology.nt", format="nt")
    for i in range(4):
        print("Query " + str(i + 1) + ": ")
        x = g.query(AllQueries[i])
        for q in x:
            print(q)
        print("\n\n")


getData()

