from neo4j import GraphDatabase
from config import settings

driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

def test_graph():
    with driver.session() as session:
        session.run("MERGE (c:Case {id:'demo', text:'Test Case'})")
        session.run("MERGE (a:Action {name:'File FIR'})")
        session.run("MATCH (c),(a) WHERE c.id='demo' AND a.name='File FIR' MERGE (c)-[:SUGGESTS]->(a)")

if __name__ == "__main__":
    test_graph()
