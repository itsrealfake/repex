# src/git_processor.py
from git import Repo
import config
from neo4j_driver import Neo4jDriver

def process_git_data():
    repo = Repo(config.LOCAL_REPO_PATH)
    db = Neo4jDriver()

    db.clear_database()

    commits = list(repo.iter_commits())
    commit_nodes = {}
    
    for commit in commits:
        commit_props = {
            "hash": commit.hexsha,
            "message": commit.message.strip(),
            "author": str(commit.author),
            "timestamp": commit.authored_datetime.isoformat()
        }
        commit_node = db.create_node("Commit", commit_props)
        commit_nodes[commit.hexsha] = commit_node.id

        for parent in commit.parents:
            if parent.hexsha in commit_nodes:
                db.create_relationship(
                    commit_nodes[commit.hexsha],
                    commit_nodes[parent.hexsha],
                    "PARENT"
                )

    db.close()
    print(f"Processed {len(commits)} commits into Neo4j.")

if __name__ == "__main__":
    process_git_data()