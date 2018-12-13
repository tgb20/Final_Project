from py2neo import Graph

# Connect to database
graph = Graph("http://neo4j:*password*@localhost:7474")

# Purge all data in the database
graph.delete_all()