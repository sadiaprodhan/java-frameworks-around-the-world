import time
from urllib.parse import quote
import requests;
from dateutil.parser import parse
import urllib
import json
from geopy.geocoders import Nominatim
import pycountry_convert as pc


selected_repos = []
continents_with_framework_count= []

frameworks_with_import = {"spring": "import org.springframework", "JSF": "import javax.faces"}

    
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
    projects_response = response.json()
    projects_list = projects_response['items']
    for i in range(len(projects_list)):
        per_project_dict = projects_list[i]
        existing_repo = next((item for item in selected_repos if item['full_name'] ==  f'{per_project_dict["repository"]["full_name"]}'), None)
        print(existing_repo)
        if existing_repo == None:
            repo_search_url = f'https://api.github.com/repos/{per_project_dict["repository"]["full_name"]}'
            repo_response = getResponse(repo_search_url)
            print(repo_response)
            repo_dict= repo_response.json()
          
            if repo_dict["private"] == False:
                creation_Date = parse(repo_dict["created_at"])
                pushed_Date = parse(repo_dict["pushed_at"])
                if((pushed_Date - creation_Date).days > 180):
                    commits = commit_count(repo_dict["full_name"])
                    if(commits) > 5 :
                        location = findLocation(repo_dict["owner"]["login"])
                        if(location != None):
                            repo_dict["commit_count"] = commits
                            repo_dict["location"] = location        
                            selected_repos.append(repo_dict)
                    
    
    
        
    
def getResponse(url):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + token
    }
  
    response = requests.get(url, headers=headers)
    return response
   


def findRepo():
    for key, value in frameworks_with_import.items():
        url = f'https://api.github.com/search/code?q={value}+in:file +language:java&sort=stars&direction=desc'
        response = getResponse(url)
        parseResultsOfSearch(response)
        print(len(selected_repos))
        while len(selected_repos) <= 20:
            url = response.links.get("next")
            if url != None:
                url = url["url"]
                print(url)
    
                response = getResponse(url)
                parseResultsOfSearch(response)
                print(len(selected_repos))
            else:
                break
    
        with open(f'{key}.json', 'w') as file:
            json.dump(selected_repos,file)
        selected_repos.clear()

def getContinentWithFramework():
    for key, value in frameworks_with_import.items():
        with open(f'{key}.json') as projects_file:
            file_contents = json.loads(projects_file.read())   
            for i in range(len(file_contents)):
                project = file_contents[i]
                continent = country_to_continent(project["location"])
                dict = {"continent": continent, "count": 1, "framework":key}
                print(continent)
                my_item = next((item for item in continents_with_framework_count if item['continent'] == continent and item['framework'] == key), None)
                print(my_item)

                if my_item == None: 
                    dict = {"continent": continent, "count": 1, "framework":key}
                    continents_with_framework_count.append(dict)
                
                else:
                    continents_with_framework_count.remove(my_item)
                    count = my_item["count"] + 1
                    my_item.update({"count": count})
                    continents_with_framework_count.append(my_item)
                    print(continents_with_framework_count)

    with open('framework_count_with_country.json', 'w') as file:
            json.dump(continents_with_framework_count,file)
        


def get_continent_name(continent_code: str) -> str:
    continent_dict = {
        "NA": "North America",
        "SA": "South America",
        "AS": "Asia",
        "AF": "Africa",
        "OC": "Oceania",
        "EU": "Europe",
        "AQ" : "Antarctica"
    }
    return continent_dict[continent_code]
               
def country_to_continent(country_name):
    geolocator = Nominatim(user_agent="frameworks")
    location = geolocator.geocode(country_name)  
    location = geolocator.reverse(f'{location.raw["lat"]} ,{location.raw["lon"]}', language="en")
    address = location.raw["address"]
    country_code = address["country_code"].upper()
    continent_code = pc.country_alpha2_to_continent_code(country_code)
    continent_name = get_continent_name(continent_code)
    return continent_name
    
            


if __name__ == "__main__":
    findRepo()
    getContinentWithFramework()

