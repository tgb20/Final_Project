import csv
from py2neo import Graph, Node, Relationship, NodeMatcher

rtNodes = {}
aoNodes = {}
tpNodes = {}

# Connect to the database
graph = Graph("http://neo4j:*password*@localhost:7474")

matcher = NodeMatcher(graph)

# Read Rooster Teeth Podcast File
with open('data/rtpodcast.csv') as rtfile:
    reader = csv.DictReader(rtfile)

    # Get Node Values
    for row in reader:
        for key in row:
            if(row[key] == '1'):
                if(key in rtNodes):
                    rtNodes[key] += 1
                else:
                    rtNodes[key] = 1
    rtfile.close()

# Read Always Open Podcast File
with open('data/alwaysopen.csv') as aofile:
    reader = csv.DictReader(aofile)

    # Get Node Values
    for row in reader:
        for key in row:
            if(row[key] == '1'):
                if(key in aoNodes):
                    aoNodes[key] += 1
                else:
                    aoNodes[key] = 1
    aofile.close()

# Read The Patch Podcast File
with open('data/thepatch.csv') as tpFile:
    reader = csv.DictReader(tpFile)

    # Get Node Values
    for row in reader:
        for key in row:
            if(row[key] == '1'):
                if(key in tpNodes):
                    tpNodes[key] += 1
                else:
                    tpNodes[key] = 1
    tpFile.close()


# Create RT Nodes
for key in rtNodes:
    cast = Node("CAST", name = key, rta = rtNodes[key])
    graph.create(cast)

# Create AO Nodes
for key in aoNodes:
    if key in rtNodes:
        ePerson = matcher.match("CAST", name = key).first()
        ePerson["ao"] = aoNodes[key]
        graph.push(ePerson)
    else:
        cast = Node("CAST", name = key, ao = aoNodes[key])
        graph.create(cast)

# Create TP Nodes
for key in tpNodes:
    if key in rtNodes or key in aoNodes:
        ePerson = matcher.match("CAST", name = key).first()
        ePerson["tp"] = tpNodes[key]
        graph.push(ePerson)
    else:
        cast = Node("CAST", name = key, tp = tpNodes[key])
        graph.create(cast)

# Create RT Node
rtpodcast = Node("PODCAST", name = "Rooster Teeth Podcast", rta = 521)
graph.create(rtpodcast)

# Create AO Node
aopodcast = Node("PODCAST", name = "Always Open", ao = 84)
graph.create(aopodcast)

# Create TP Node
aopodcast = Node("PODCAST", name = "The Patch", tp = 122)
graph.create(aopodcast)

# Attach to RT Podcast
for key in rtNodes:
     n1 = matcher.match("CAST", name = key).first()
     n2 = matcher.match("PODCAST", name = "Rooster Teeth Podcast").first()
     ship = Relationship(n1, "APPEARED_ON", n2)
     graph.create(ship)

# Attach to Always Open Podcast
for key in aoNodes:
     n1 = matcher.match("CAST", name = key).first()
     n2 = matcher.match("PODCAST", name = "Always Open").first()
     ship = Relationship(n1, "APPEARED_ON", n2)
     graph.create(ship)

# Attach to The Patch Podcast
for key in tpNodes:
     n1 = matcher.match("CAST", name = key).first()
     n2 = matcher.match("PODCAST", name = "The Patch").first()
     ship = Relationship(n1, "APPEARED_ON", n2)
     graph.create(ship)