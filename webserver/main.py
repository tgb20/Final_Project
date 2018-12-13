from flask import Flask, render_template, request
from py2neo import Graph, Node, NodeMatcher, Relationship, RelationshipMatcher, Path
from json import dumps


app = Flask(__name__)

webserverstatic = '/path/to/webserver/static/'

# Returns the Homepage of the Website
@app.route('/')
def homePage():
    return render_template('homepage.html')


# Returns a graph of nearest nodes to the selected person
@app.route('/nearestnodes')
def returnDoF():
    person = request.args.get('person')

    # Connect to database
    graph = Graph("http://neo4j:*password*@localhost:7474")
    nodematcher = NodeMatcher(graph)
    relamatcher = RelationshipMatcher(graph)

    nodes = []
    edges = []

    # Find the node for the person selected
    personNode = nodematcher.match("COSTAR", name = person).first()

    # Convert node to GraphJSON
    nodes.append({"id": personNode.identity, "name": personNode["name"], "rta": personNode["rta"], "tp": personNode["tp"], "ao": personNode["ao"]})

    # Find all relationships for the selected person
    ships1 = relamatcher.match((personNode, None))
    ships2 = relamatcher.match((None, personNode))

    # Convert the relationships and nodes to GraphJSON
    for ship in ships1:
        nodes.append({"id": ship.end_node.identity, "name": ship.end_node["name"], "rta": ship.end_node["rta"], "tp": ship.end_node["tp"], "ao": ship.end_node["ao"]})
        edges.append({"source": ship.start_node.identity, "target": ship.end_node.identity, "role": "appeared_with"})
    for ship in ships2:
        nodes.append({"id": ship.start_node.identity, "name": ship.start_node["name"], "rta": ship.start_node["rta"], "tp": ship.start_node["tp"], "ao": ship.start_node["ao"]})
        edges.append({"source": ship.start_node.identity, "target": ship.end_node.identity, "role": "appeared_with"})

    jsonNodes = dumps(nodes)
    jsonEdges = dumps(edges)

    # Create a final json file with all GraphJSON
    finalJson = '{"nodes": ' + jsonNodes + ', "edges": ' + jsonEdges + '}'

    # Save file to server cache
    fileLocation = (webserverstatic + person + '.json').encode("utf-8")

    with open(fileLocation, "w+") as test:
        test.write(finalJson)

    # Send file to template to display generated graph
    return render_template('showdata.html', message = person)

# Returns a graph with all nodes in the podcast database
@app.route('/returnallpodcast')
def returnPodcasts():

    # Connect to database
    graph = Graph("http://neo4j:*password*@localhost:7474")
    nodematcher = NodeMatcher(graph)
    relamatcher = RelationshipMatcher(graph)

    # Find the nodes for the cast members and the podcast.
    castNodes = nodematcher.match("CAST")
    podcastNodes = nodematcher.match("PODCAST")
    nodes = []

    # Convert the nodes to GraphJSON format for Alchemy.js
    for node in castNodes:
        nodes.append({"id": node.identity, "name": node["name"], "rta": node["rta"], "tp": node["tp"], "ao": node["ao"]})
    for node in podcastNodes:
        nodes.append({"id": node.identity, "name": node["name"], "rta": node["rta"], "tp": node["tp"], "ao": node["ao"]})

    jsonNodes = dumps(nodes)

    # Find the Relationships within the database
    relationships = relamatcher.match(None, "APPEARED_ON")
    edges = []

    # Convert the relationships to GraphJSON
    for rel in relationships:
        edges.append({"source": rel.start_node.identity, "target": rel.end_node.identity, "role": "appeared_on"})

    jsonEdges = dumps(edges)

    # Create a json string with all GraphJSON
    finalJson = '{"nodes": ' + jsonNodes + ', "edges": ' + jsonEdges + '}'
    
    # Save file to server cache
    with open(webserverstatic + 'main.json', "w+") as jsonFile:
        jsonFile.write(finalJson)
        jsonFile.close()

    # Send file to template to display generated graph
    return render_template('showdata.html', message = "main")