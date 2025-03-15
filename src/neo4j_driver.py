# src/neo4j_driver.py
from neo4j import GraphDatabase
import config
import time

class Neo4jDriver:
    def __init__(self, max_retries=5, retry_delay=2):
        self.driver = None
        for attempt in range(max_retries):
            try:
                self.driver = GraphDatabase.driver(
                    config.NEO4J_URI,
                    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
                )
                self.driver.verify_connectivity()  # Ensure connection works
                print("Connected to Neo4j successfully.")
                break
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise Exception("Failed to connect to Neo4j after retries.")

    def close(self):
        if self.driver:
            self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared.")

    def create_node(self, label, properties):
        with self.driver.session() as session:
            query = f"CREATE (n:{label} $props) RETURN n"
            result = session.run(query, props=properties)
            return result.single()["n"]

    def create_relationship(self, from_id, to_id, rel_type):
        with self.driver.session() as session:
            query = """
            MATCH (a), (b)
            WHERE id(a) = $from_id AND id(b) = $to_id
            CREATE (a)-[:%s]->(b)
            """ % rel_type
            session.run(query, from_id=from_id, to_id=to_id)

if __name__ == "__main__":
    db = Neo4jDriver()
    db.clear_database()
    db.close()