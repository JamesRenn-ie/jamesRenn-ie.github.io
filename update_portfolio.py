import requests
import re

GITHUB_USERNAME = "JamesRenn-ie"
API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

response = requests.get(API_URL)
repos = response.json()

# Read existing index.html
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the start and end of the projects section
match = re.search(r"(<section id=\"projects\".*?>)(.*?)(</section>)", content, re.DOTALL)

if not match:
    print("Could not find projects section in index.html")
    exit(1)

start, existing_projects, end = match.groups()

# Generate new project cards
new_projects = ""
for repo in repos:
    repo_name = repo["name"]
    repo_url = repo["html_url"]
    repo_desc = repo.get("description", "No description available.")

    # Check if "no-portfolio" topic is in the repository topics
    topics_response = requests.get(repo["url"] + "/topics", headers={"Accept": "application/vnd.github.mercy-preview+json"})
    topics = topics_response.json().get("names", [])
    
    if "no-portfolio" in topics:
        continue  # Skip adding this repository

    # Avoid duplicate projects
    if repo_url in existing_projects:
        continue

    new_projects += f"""
    <a href="{repo_url}" class="project-card">
      <h3>{repo_name} <img src="github-logo.svg" alt="GitHub" class="github-icon"></h3>
      <p>{repo_desc}</p>
    </a>
    """

# Insert new projects while preserving existing ones
updated_content = content.replace(existing_projects, existing_projects + new_projects)

# Write back to index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(updated_content)
