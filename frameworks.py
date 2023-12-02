import time
from urllib.parse import quote
import requests;
from dateutil.parser import parse
import urllib
import json
from geopy.geocoders import Nominatim
import pycountry_convert as pc
import os
from git import Repo 

token = ''  # Replace with your GitHub personal access token
with open('token.txt', 'r')as token_file:
    token = token_file.read()


selected_repos = []
continents_with_framework_count= []
frameworks= {'spring': 'org.springframework' , 'struts': 'org.apache.struts', 'jsf': 'javax.faces','play': 'org.playframework', 'jhipster': 'io.github.jhipster', 'vaadin':'com.vaadin',
             'vertx': 'io.vertx', 'dropwizard':'io.dropwizard', 'wicket': 'org.apache.wicket', 'tapestry': 'org.apache.tapestry5', 
             'spark': 'org.apache.spark','blade': 'com.bladejava', 'rapidoid': 'org.rapidoid','android': 'android', 'cordova':'org.apache.cordova', 'appgyver': 'appgyver','javafx': 'javafx', 
             'swingx': 'javax.swing', 'pivot': 'org.apache.pivot', 'awt': 'java.awt', 'jambi': 'com.trolltech.qt','swt': 'org.eclipse.swt',
             'jide':'com.jidesoft','junit': 'junit', 'testng': 'org.testng', 'selenium': 'org.openqa.selenium', 'cucumber':'io.cucumber.java',
             'spock': 'org.spockframework','testfx': 'org.testfx', 'dbunit': 'org.dbunit', 'arquillian':'org.jboss.arquillian',
             'citrus': 'com.consol.citrus','jbehave':'org.jbehave', 'mockito':'org.mockito','powermock':'org.powermock', 'gatling':'io.gatling'}


frameworks_with_import = { "gatling": "io.gatling"}

    
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
        if existing_repo == None:
            repo_search_url = f'https://api.github.com/repos/{per_project_dict["repository"]["full_name"]}'
            repo_response = getResponse(repo_search_url)
            repo_dict= repo_response.json()
            repo_url = repo_dict['clone_url']
            print(repo_url)
            repo_folder = os.path.join(os.getcwd(),'repositories')
            clone_repository(repo_url, repo_folder,repo_dict)
            
          
           
    
        
def clone_repository(repo_url, repo_folder,repo):
    # Clone repository locally
    try:
        
        if not os.path.exists(repo_folder):
            os.makedirs(repo_folder)
        repo_name = repo_url.split('/')[-1]
        repo_path = os.path.join(repo_folder, repo_name)
        location = None
        if not os.path.exists(repo_path):
            if repo['private'] == False:
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
    except Exception as e: print(f'exception{e}')


def create_text_file(repo_path, file_name, text):
    file_path = os.path.join(repo_path, file_name)
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(text)
    return file_path
    
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
    #getContinentWithFramework()

