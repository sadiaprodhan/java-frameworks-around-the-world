import os
import csv
import json
from geopy.geocoders import Nominatim
import pycountry_convert as pc
import json

frameworks= {'spring': 'org.springframework' , 'struts': 'org.apache.struts', 'jsf': 'javax.faces','play': 'org.playframework', 'jhipster': 'io.github.jhipster', 'vaadin':'com.vaadin',
             'vertx': 'io.vertx', 'dropwizard':'io.dropwizard', 'wicket': 'org.apache.wicket', 'tapestry': 'org.apache.tapestry5', 
             'spark': 'org.apache.spark','blade': 'com.bladejava', 'rapidoid': 'org.rapidoid','android': 'android', 'cordova':'org.apache.cordova', 'appgyver': 'appgyver','javafx': 'javafx', 
             'swingx': 'javax.swing', 'pivot': 'org.apache.pivot', 'awt': 'java.awt', 'jambi': 'com.trolltech.qt','swt': 'org.eclipse.swt',
             'jide':'com.jidesoft','junit': 'junit', 'testng': 'org.testng', 'selenium': 'org.openqa.selenium', 'cucumber':'io.cucumber.java',
             'spock': 'org.spockframework','testfx': 'org.testfx', 'dbunit': 'org.dbunit', 'arquillian':'org.jboss.arquillian',
             'citrus': 'com.consol.citrus','jbehave':'org.jbehave', 'mockito':'org.mockito','powermock':'org.powermock', 'gatling':'io.gatling'}

stackoverflow_questions_continent_count = []
continent_not_extracted = []
            
   
def stackoverflow_questions_location(directory_path):
    for filename in os.listdir(directory_path):
        if filename.startswith('android.csv'):

            file_path = os.path.join(directory_path, filename)
            key, ext = os.path.splitext(filename)
            with open(file_path, encoding='utf-8') as csvfile:
                    stackoverflow_framework_location=[]
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)  
            
            # Convert each row to a dictionary and append to the list
                    for row in csv_reader:
                        question,title, answer_count, location= row
                        dict = { 'location': location, 'framework': key}
                        stackoverflow_framework_location.append(dict)
            getContinentWithFrameworkforSO(stackoverflow_framework_location, key)
            print(f'proccesing {key} file now')
    #getContinentWithFrameworkforSO(stackoverflow_framework_location)        
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


        
def getContinentWithFrameworkforSO(stackoverflow_framework_location, framework):
    for so_fw_loc in stackoverflow_framework_location:

        continent = country_to_continent(so_fw_loc['location'])
    
        dict = {"continent": continent, "count": 1, "framework": so_fw_loc['framework']}
        
        if continent == None:
            continent_not_extracted.append({'location': so_fw_loc['location'], 'framework': so_fw_loc["framework"]})

        else :
            my_item = next((item for item in stackoverflow_questions_continent_count if item['continent'] == continent and item['framework'] == so_fw_loc['framework']), None)
            print(my_item)

            if my_item == None: 
                dict = {"continent": continent, "count": 1, "framework":so_fw_loc['framework']}
                stackoverflow_questions_continent_count.append(dict)
                
            else:
                stackoverflow_questions_continent_count.remove(my_item)
                count = my_item["count"] + 1
                my_item.update({"count": count})
                stackoverflow_questions_continent_count.append(my_item)
    directory = os.path.join(os.getcwd(),'so_continents')
    not_extracted_directory = os.path.join(os.getcwd(),'location_issues')
    
    os.makedirs(directory, exist_ok=True)
    os.makedirs(not_extracted_directory, exist_ok=True)
            

    with open(os.path.join(directory,f'so_with_continent_result_{framework}.json'), 'w', encoding='utf-8') as file:
            json.dump(stackoverflow_questions_continent_count,file)
    with open(os.path.join(not_extracted_directory,f'so_continent_not_extracted_{framework}.json'), 'w', encoding='utf-8') as file:
            json.dump(continent_not_extracted,file)
     
     
            
if __name__ == "__main__":
    stackoverflow_questions_location(os.path.join(os.getcwd(),"SO_files"))
  