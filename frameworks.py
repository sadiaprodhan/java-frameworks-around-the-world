import time
from urllib.parse import quote
import requests;
from dateutil.parser import parse
import urllib
import json

selected_repos = []
    
def commit_count(project):
    url = f'https://api.github.com/repos/{project}/commits'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + token
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
    
    url = f'https://api.github.com/users/{user}'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + token
    }
    
    resp = requests.request('GET', url, headers=headers)
    user_info = resp.json()
    return user_info["location"]

    
def parseResultsOfSearch(response):

    print("Status code: ", response.status_code)
    response_dict = response.json()
    repos_dicts_raw = response_dict['items']
    for i in range(len(repos_dicts_raw)):
        each_repo = repos_dicts_raw[i]
        creation_Date = parse(each_repo["created_at"])
        updated_date = parse(each_repo["pushed_at"])
        if((updated_date - creation_Date).days > 180):
            commits = commit_count(each_repo["full_name"])
            if(commits) > 5 :
                location = findLocation(each_repo["owner"]["login"])
                if(location != None):
                    each_repo["commit_count"] = commits
                    each_repo["location"] = location        
                    selected_repos.append(each_repo)
                    
    
    
        
    
def getResponse(url):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + token
    }
  
    response = requests.get(url, headers=headers)
    return response
   


def findRepo():
    url = 'https://api.github.com/search/repositories?sort=help-wanted-issues&direction=desc&q=is:public+language:java+created:%3C2023-11-01'
    response = getResponse(url)
    parseResultsOfSearch(response)
    print(len(selected_repos))
    while len(selected_repos) <= 400:
        url = response.links.get("next")
        url = url["url"]
        print(url)
    
        response = getResponse(url)
        parseResultsOfSearch(response)
        print(len(selected_repos))
    
        
    with open('file.txt', 'w') as file:
        json.dump(selected_repos,file)
   
    




            


if __name__ == "__main__":
    findRepo()

