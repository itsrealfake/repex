# src/download.py
import git
import os
import config

def download_repository():
    if os.path.exists(config.LOCAL_REPO_PATH):
        print(f"Repository already exists at {config.LOCAL_REPO_PATH}")
        return
    print(f"Cloning repository from {config.REPO_URL}...")
    git.Repo.clone_from(config.REPO_URL, config.LOCAL_REPO_PATH)
    print("Repository cloned successfully.")

if __name__ == "__main__":
    download_repository()