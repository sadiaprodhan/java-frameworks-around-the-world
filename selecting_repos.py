import requests
import xml.etree.ElementTree as ET
import os
from dateutil.parser import parse
import urllib
from git import Repo  # Assuming gitpython library is installed
from collections import defaultdict
from lxml import etree



# GitHub API variables
github_api = 'https://api.github.com'
github_token = ''  # Replace with your GitHub personal access token
with open('token.txt', 'r')as token_file:
    github_token = token_file.read()
headers = {'Authorization': f'token {github_token}'}

# Search query to find Java repositories on GitHub
query = 'language:java'

def call_github_api(url):
    # Function to fetch repositories based on search query
    response = requests.get(url, headers=headers)
    print(response)
    return response
    
def commit_count(project):
    url = f'{github_api}/repos/{project}/commits'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + github_token
    }
    params = {
        
        'per_page': 1,
    }
    resp = requests.request('GET', url, params=params,headers=headers)
    if (resp.status_code // 100) != 2:
        raise Exception(f'invalid github response: {resp.content}')
    # check the resp count, just in case there are 0 commits
    commit_count = len(resp.json())
    last_page = resp.links.get('last')
    # if there are no more pages, the count must be 0 or 1
    if last_page:
        # extract the query string from the last page url
        qs = urllib.parse.urlparse(last_page['url']).query
        # extract the page number from the query string
        commit_count = int(dict(urllib.parse.parse_qsl(qs))['page'])
    return commit_count


def findLocation(user):
    url = f'{github_api}/users/{user}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + github_token
    }
    
    resp = requests.request('GET', url, headers=headers)
    user_info = resp.json()
    return user_info["location"]



def clone_repository(repo_url, repo_folder,repo):
    # Clone repository locally
    try:
        
        if not os.path.exists(repo_folder):
            os.makedirs(repo_folder)
        repo_name = repo_url.split('/')[-1]
        repo_path = os.path.join(repo_folder, repo_name)
        location = None
        if not os.path.exists(repo_path):
            if repo["private"] == False:
                creation_Date = parse(repo["created_at"])
                pushed_Date = parse(repo["pushed_at"])
                if((pushed_Date - creation_Date).days > 180):
                    commits = commit_count(repo["full_name"])
                    if(commits) > 5 :
                        location = findLocation(repo["owner"]["login"])
                        if(location != None):
                            print(location)
                            try:
                                Repo.clone_from(repo_url, repo_path, depth =1)
                                if repo_path != None:
                                    print(f"Repository cloned at: {repo_path}")
    # Create a text file with a string inside the cloned repository
                                    file_name = 'location.txt'  # Replace with your desired file name
                                    text_content = f'{location}'  # Replace with your desired text content
                                    created_file_path = create_text_file(repo_path, file_name, text_content)
    
                                    if created_file_path:
                                        print(f"Text file created at: {created_file_path}")
                                    else:
                                        print("Failed to create the text file.")
                                else:
                                    print("Failed to clone the repository")
            
                            except:
                                 print("Failed to clone the repository.")
        else:
            print("requirement not fulfilled")
    except Exception as e: print(e)


def create_text_file(repo_path, file_name, text):
    file_path = os.path.join(repo_path, file_name)
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(text)
    return file_path
    
def getMappingsNode(node, nodeName):
    if node.findall('*'):
        for n in node.findall('*'):
            if nodeName in n.tag:
                return n
        else:
            return getMappingsNode(n, nodeName)


def find_repos(repositories):
    for repo in repositories:
            repo_url = repo['clone_url']
            repo_folder = os.path.join(os.getcwd(),'repositories')
            clone_repository(repo_url,repo_folder, repo)
            
            

# Fetch repositories
def find_appropriate_repositories():
    url = f'{github_api}/search/repositories?q={query}'
    response = call_github_api(url)
    if response.status_code == 200:
        find_repos(response.json()['items'])
        

        
        url = response.links.get("next")
        while(url != None):
            url = url["url"]
            response = call_github_api(url)
            if response.status_code == 200:
                find_repos(response.json()['items'])
                url = response.links.get("next")
            else:
                print('failed')
                break

        
            
if __name__ == "__main__":
    find_appropriate_repositories()
    