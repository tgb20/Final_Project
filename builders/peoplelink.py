import csv
from py2neo import Graph, Node, Relationship, NodeMatcher

# Create empty lists to hold all variables.
rtNodes = {}
aoNodes = {}
tpNodes = {}
rtRelationships = {}
aoRelationships = {}
tpRelationships = {}

# Connect to the database
graph = Graph("http://neo4j:*password*@localhost:7474")

matcher = NodeMatcher(graph)

# Read RT File
with open('data/rtpodcast.csv') as rtFile:
    reader = csv.DictReader(rtFile)

    for row in reader:
        # Get Node Values
        for key in row:
            if(row[key] == '1'):
                if(key in rtNodes):
                    rtNodes[key] += 1
                else:
                    rtNodes[key] = 1
        # Find Relationships
        for mainKey in row:
            for subKey in row:
                if(mainKey != subKey):
                    if(row[mainKey] == '1' and row[subKey] == '1'):
                        if(mainKey + subKey in rtRelationships and subKey + mainKey not in rtRelationships):
                            rtRelationships[mainKey + subKey]["strength"] += 1
                        elif(subKey + mainKey not in rtRelationships):
                            rtRelationships[mainKey + subKey] = {"mainKey": mainKey, "subKey": subKey, "strength": 1}
    rtFile.close()

# Read Always Open File
with open ('data/alwaysopen.csv') as aoFile:
    reader = csv.DictReader(aoFile)

    for row in reader:
        # Get Node Values
        for key in row:
            if(row[key] == '1'):
                if(key in aoNodes):
                    aoNodes[key] += 1
                else:
                    aoNodes[key] = 1
        # Find Relationships
        for mainKey in row:
            for subKey in row:
                if(mainKey != subKey):
                    if(row[mainKey] == '1' and row[subKey] == '1'):
                        if(mainKey + subKey in aoRelationships and subKey + mainKey not in aoRelationships):
                            aoRelationships[mainKey + subKey]["strength"] += 1
                        elif(subKey + mainKey not in aoRelationships):
                            aoRelationships[mainKey + subKey] = {"mainKey": mainKey, "subKey": subKey, "strength": 1}
    aoFile.close()

# Read The Patch file
with open ('data/thepatch.csv') as tpFile:
    reader = csv.DictReader(tpFile)
    for row in reader:
        # Get Node Values
        for key in row:
            if(row[key] == '1'):
                if(key in tpNodes):
                    tpNodes[key] += 1
                else:
                    tpNodes[key] = 1
        # Find Relationships
        for mainKey in row:
            for subKey in row:
                if(mainKey != subKey):
                    if(row[mainKey] == '1' and row[subKey] == '1'):
                        if(mainKey + subKey in tpRelationships and subKey + mainKey not in tpRelationships):
                            tpRelationships[mainKey + subKey]["strength"] += 1
                        elif(subKey + mainKey not in tpRelationships):
                            tpRelationships[mainKey + subKey] = {"mainKey": mainKey, "subKey": subKey, "strength": 1}
    tpFile.close()


# Create RT Nodes
for key in rtNodes:
    cast = Node("COSTAR", name = key, rta = rtNodes[key])
    graph.create(cast)  


# Create AO Nodes
for key in aoNodes:
    if key in rtNodes:
        ePerson = matcher.match("COSTAR", name = key).first()
        ePerson["ao"] = aoNodes[key]
        graph.push(ePerson)
    else:
        cast = Node("COSTAR", name = key, ao = aoNodes[key])
        graph.create(cast)

# Create TP Nodes
for key in tpNodes:
    if key in rtNodes or key in aoNodes:
        ePerson = matcher.match("COSTAR", name = key).first()
        ePerson["tp"] = tpNodes[key]
        graph.push(ePerson)
    else:
        cast = Node("COSTAR", name = key, tp = tpNodes[key])
        graph.create(cast)

# RT Relationships
for key, value in rtRelationships.viewitems():

    n1 = matcher.match("COSTAR", name = value["mainKey"]).first()
    n2 = matcher.match("COSTAR", name = value["subKey"]).first()

    ship = Relationship(n1, "RTPODCAST", n2, strength=value["strength"])
    graph.create(ship)

# Always Open Relationships
for key, value in aoRelationships.viewitems():

    n1 = matcher.match("COSTAR", name = value["mainKey"]).first()
    n2 = matcher.match("COSTAR", name = value["subKey"]).first()

    ship = Relationship(n1, "ALWAYSOPEN", n2, strength=value["strength"])
    graph.create(ship)

# The Patch Relationships
for key, value in tpRelationships.viewitems():

    n1 = matcher.match("COSTAR", name = value["mainKey"]).first()
    n2 = matcher.match("COSTAR", name = value["subKey"]).first()

    ship = Relationship(n1, "THEPATCH", n2, strength=value["strength"])
    graph.create(ship)