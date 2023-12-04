import xml.etree.ElementTree as ET
import os
import re
from geopy.geocoders import Nominatim
import pycountry_convert as pc
import json
from itertools import groupby
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


framework_locations = []
continents_with_framework_count= []


frameworks= {'spring': 'org.springframework' , 'struts': 'org.apache.struts', 'jsf': 'javax.faces','play': 'org.playframework', 'jhipster': 'io.github.jhipster', 'vaadin':'com.vaadin',
             'vertx': 'io.vertx', 'dropwizard':'io.dropwizard', 'wicket': 'org.apache.wicket', 'tapestry': 'org.apache.tapestry5', 
             'spark': 'org.apache.spark','blade': 'com.bladejava', 'rapidoid': 'org.rapidoid','android': 'android', 'cordova':'org.apache.cordova', 'appgyver': 'appgyver','javafx': 'javafx', 
             'swingx': 'javax.swing', 'pivot': 'org.apache.pivot', 'awt': 'java.awt', 'jambi': 'com.trolltech.qt','swt': 'org.eclipse.swt',
             'jide':'com.jidesoft','junit': 'junit', 'testng': 'org.testng', 'selenium': 'org.openqa.selenium', 'cucumber':'io.cucumber.java',
             'spock': 'org.spockframework','testfx': 'org.testfx', 'dbunit': 'org.dbunit', 'arquillian':'org.jboss.arquillian',
             'citrus': 'com.consol.citrus','jbehave':'org.jbehave', 'mockito':'org.mockito','powermock':'org.powermock', 'gatling':'io.gatling'}

def find_frameworks_count(all_dependencies, location):
    frameworks_found = set()

    for key, value in frameworks.items():
        regex = re.compile(value)

        for item in all_dependencies:
            
            if regex.search(item):
                frameworks_found.add(key)

    if len(frameworks_found) > 0:
        for value in frameworks_found:
            framework_locations.append({'framework': value, 'location':location})
   
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
    try:
        return continent_dict[continent_code]
    except:
        return None
               
def country_to_continent(country_name):
    try:
        geolocator = Nominatim(user_agent="frameworks")
        location = geolocator.geocode(country_name)  
        location = geolocator.reverse(f'{location.raw["lat"]} ,{location.raw["lon"]}', language="en")
        address = location.raw["address"]
        country_code = address["country_code"].upper()
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = get_continent_name(continent_code)
        return continent_name
    except:
        return None


        
def getContinentWithFramework():
    continent_not_extracted = []
    for framework_location in framework_locations:

        continent = country_to_continent(framework_location['location'])
    
        dict = {"continent": continent, "count": 1, "framework": framework_location['framework']}
        
        if continent == None:
            continent_not_extracted.append({'location': framework_location['location'], 'framework': framework_location["framework"]})

        else :
            my_item = next((item for item in continents_with_framework_count if item['continent'] == continent and item['framework'] == framework_location['framework']), None)
            print(my_item)

            if my_item == None: 
                dict = {"continent": continent, "count": 1, "framework":framework_location['framework']}
                continents_with_framework_count.append(dict)
                
            else:
                continents_with_framework_count.remove(my_item)
                count = my_item["count"] + 1
                my_item.update({"count": count})
                continents_with_framework_count.append(my_item)
                
    print(continent_not_extracted)

    #with open('framework_count_with_country.json', 'w') as file:
            #json.dump(continents_with_framework_count,file)
     with open('location_not_extracted.json', 'w') as file:
            json.dump(continent_not_extracted,file)



def plot_three_popular_fw_graph(data):
    df = pd.DataFrame(data)
    grouped = df.groupby(['continent', 'framework']).sum().reset_index()
    directory = os.path.join(os.getcwd(),'results')
    
    os.makedirs(directory, exist_ok=True)

    top_frameworks = grouped.groupby('continent').apply(lambda x: x.nlargest(3, 'count')).reset_index(drop=True)
    print(top_frameworks)
    distinct_framework = set()
    
    top_frameworks_dict = {}
    for _, row in top_frameworks.iterrows():
        continent = row['continent']
        framework = row['framework']
        count = row['count']
        distinct_framework.add(framework)
        print(distinct_framework)
    
    
        if continent not in top_frameworks_dict:
            top_frameworks_dict[continent] = []
    
        top_frameworks_dict[continent].append({'framework': framework, 'count': count})
        columns = ['Continent', 'Framework', 'Count']
        rows = []
        for continent, frameworks in top_frameworks_dict.items():
            for framework_data in frameworks:
                rows.append([continent, framework_data['framework'], framework_data['count']])

    fig, ax = plt.subplots(figsize=(10, 6))
    table = ax.table(cellText=rows, colLabels=columns, loc='center', cellLoc='center', colColours=['#f3f3f3']*3)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    ax.axis('off')  

    plt.title('Top 3 Frameworks of All Continents')
    plt.savefig(os.path.join(directory,'top_three_frameworks.png'), bbox_inches='tight')
    distinct_framework_list = list(distinct_framework)

    with open('top_distinct_frameworks_of_github.json', 'w') as file:
            json.dump(distinct_framework_list,file)
    

def create_table(grouped_data, merged_data):
    font_size = 12
    font = ImageFont.truetype("arial.ttf", font_size)
    cell_width = 250
    cell_height = 30
    padding = 10  
    directory = os.path.join(os.getcwd(),'results')
    
    os.makedirs(directory, exist_ok=True)

    for continent, continent_data in grouped_data.items():
    
        merged_data = pd.DataFrame(continent_data)
                
        table_width = 2 * cell_width
        table_height = min((len(merged_data) + 3) * cell_height, 5000) 

        img = Image.new('RGB', (table_width, table_height), color='white')
        draw = ImageDraw.Draw(img)

        header_text = f"{continent} Table"
        draw.rectangle([0, 0, table_width, cell_height], outline='black')
        draw.text((padding, padding), header_text, fill='black', font=font)

        header = merged_data.columns.tolist()
        for i, header_text in enumerate(header):
            draw.rectangle([i * cell_width, cell_height, (i + 1) * cell_width, (2 * cell_height)], outline='black')
            draw.text((i * cell_width + padding, cell_height + padding), header_text, fill='black', font=font)

        for index, row in merged_data.iterrows():
            row_data = row.tolist()
            for i, cell_text in enumerate(row_data):
                draw.rectangle([i * cell_width, (index + 2) * cell_height, (i + 1) * cell_width, (index + 3) * cell_height],
                           outline='black')
                draw.text((i * cell_width + padding, (index + 2) * cell_height + padding), str(cell_text),
                      fill='black', font=font)
            
       
        img.save(os.path.join(directory, f'{continent}_table.png'))

    
def cluster_into_continents():
    with open('framework_count_with_country.json') as file:
            file_contents = json.loads(file.read())   
            sorted_data = sorted(file_contents, key=lambda x: (x['continent'], -x['count']))

            grouped_data = {continent: [{'framework': fw['framework'], 'count': fw['count']} for fw in frameworks] 
                for continent, frameworks in groupby(sorted_data, key=lambda x: x['continent'])}

            
            merged_data = pd.DataFrame([(key, fw['framework'], fw['count']) for key, value in grouped_data.items() for fw in value],
                            columns=['Continent', 'Framework', 'Count'])
            print(merged_data)
            
            create_table(grouped_data,merged_data)

            plot_three_popular_fw_graph(sorted_data)
            
def extract_dependencies_pom_xml(repo_path, location):
    pom_xml_path = os.path.join(repo_path, 'pom.xml')
    if os.path.exists(pom_xml_path):
        tree = ET.parse(pom_xml_path)
        root = tree.getroot()
        namespace = root.tag.split('}')[0][1:]
        if namespace == None:
            namespace = 'http://maven.apache.org/POM/4.0.0'
        print(namespace)
        group_ids = []
        try:
            for dependency in root.findall('.//{' + namespace+ '}dependency'):
                group_id = dependency.find('{'+namespace +'}groupId').text
                group_ids.append(group_id)
            
                artifact_id = dependency.find('{'+namespace +'}artifactId').text

            find_frameworks_count(group_ids,location)
        except:
            search_import_statements(repo_path, location)                       
            
            
        else:
            print('no pom file')
            extract_dependencies_gradle(repo_path, location)

def search_import_statements(directory, location):
    import_statements = set()

    import_pattern = re.compile(r"import\s+([\w.]+(?:\.\w+)*\.\*?[\w*]*);")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r' , errors="ignore") as java_file:
                    content = java_file.read()
                    matches = import_pattern.findall(content)
                    import_statements.update(matches)

    find_frameworks_count(import_statements, location)        
                
    
def extract_dependencies_gradle(repo_path, location):
    gradle_files = [f for f in os.listdir(repo_path) if f.endswith('build.gradle')]
    print(gradle_files)
    if len(gradle_files) > 0:
        gradle_file = gradle_files[0]
        dependencies = []
        gradle_file_path = os.path.join(repo_path, gradle_file)
        print(gradle_file_path)
        
        with open(gradle_file_path, 'r',  encoding="utf-8") as file:
            content = file.read()
            pattern = re.compile(r"(\bcompile\b|\bimplementation\b|\bapi\b|\btestImplementation\b|\bandroidTestImplementation\b)\s+['\"]([^'\"]+):([^'\"]+):([^'\"]+)['\"]")
            matches = pattern.findall(content)
            print(matches)
            if(len(matches)> 0):
                for match in matches:
                    configuration, group, name, version = match
                    dependencies.append(group)
                print(len(matches))
                print(dependencies)
                find_frameworks_count(dependencies, location)

               
            else:
                search_import_statements(repo_path, location)
            
    if gradle_files == None:
        print('not gradle')
        search_import_statements(repo_path, location)
    
def list_folders(directory):
    folder_paths = []
    location = ''
    i=0
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            git_repo_path = os.path.join(root, '.git')
            path = os.path.dirname(git_repo_path)
            
            try:
                location_file = os.path.join(path, 'location.txt')
                print(location_file)
                with open(location_file, 'r',  encoding="utf-8") as file:
                    location = file.read()
                    extract_dependencies_pom_xml(path, location)
          
            
            except FileNotFoundError:
                location = None
                    
        


if __name__ == "__main__":
    #list_folders(os.path.join(os.getcwd(),'repositories'))
    #getContinentWithFramework()
    #cluster_into_continents()


