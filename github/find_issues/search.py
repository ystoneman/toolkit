import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Set up headers for GitHub API authentication
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Step 1: Search for issues
query = 'is:issue cohere'
issues_url = f'https://api.github.com/search/issues?q={query}'
issues_response = requests.get(issues_url, headers=headers)

# Check if the response was successful
if issues_response.status_code != 200:
    print(f"Failed to fetch issues: {issues_response.status_code}")
    print(issues_response.json())
    exit()

# Parse the response JSON
issues_data = issues_response.json()

# Check if 'items' key is in the response
if 'items' not in issues_data:
    print("No issues found or API response format has changed.")
    print(issues_data)
    exit()

issues = issues_data['items']

# Step 2: Extract repository names
repo_names = {issue['repository_url'] for issue in issues}

# Step 3: Fetch repository details and star counts
repos = []
for repo_url in repo_names:
    repo_response = requests.get(repo_url, headers=headers)
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        repos.append({
            'full_name': repo_data['full_name'],
            'stars': repo_data['stargazers_count']
        })
    else:
        print(f"Failed to fetch repo details for {repo_url}: {repo_response.status_code}")
        print(repo_response.json())

# Step 4: Map issues to their star counts
issues_with_stars = []
for issue in issues:
    repo_url = issue['repository_url']
    repo = next((repo for repo in repos if repo['full_name'] in repo_url), None)
    if repo:
        issue['repo_stars'] = repo['stars']
        issues_with_stars.append(issue)
    else:
        print(f"Repository details not found for issue: {issue['title']}")

# Step 5: Sort issues by repository star count
sorted_issues = sorted(issues_with_stars, key=lambda i: i['repo_stars'], reverse=True)

# Print sorted issues with URLs
for issue in sorted_issues:
    print(f"Issue: {issue['title']} | Stars: {issue['repo_stars']} | Repo: {issue['repository_url']} | URL: {issue['html_url']}")
