
from collections import defaultdict
import json
from itertools import groupby
import os

continents = ["North America", "South America", "Asia", "Africa","Oceania","Europe","Antarctica"]
stackoverflow_proportion= []
github_proportion= []

def calculate_framework_proportion_github():
        with open('framework_count_with_country.json') as file:
            continent_framework_count_github = json.loads(file.read())   
            sorted_data_github = sorted(continent_framework_count_github, key=lambda x: (x['framework'], -x['count']))

            grouped_data_github = {framework: [{'co': cn['continent'], 'count': cn['count']} for cn in continents] 
                for framework, continents in groupby(sorted_data_github, key=lambda x: x['framework'])}

            
            
            with open('top_distinct_frameworks_of_github.json', 'r') as jsonfile:
                top_frameworks = json.loads(jsonfile.read())
                directory_path = os.path.join(os.getcwd(), 'so_continents')
                if not os.path.exists(directory_path):
                    print('directory does not exist')
                else:
                    for framework in top_frameworks:
                        so_proportion_dictionary_list = []
                        github_proportion_dictionary_list = []
                        filepath = os.path.join(directory_path, f'so_with_continent_result_{framework}.json')
                        if os.path.isfile(filepath):
                            with open(filepath, 'r') as so_file:
                                so_file = json.loads(so_file.read())
                                print(so_file)
                                total_count = sum(item['count'] for item in so_file)
                                for continent in continents:
                                    for data in so_file:
                                        if data['continent'] == continent:
                                            count = data['count']
                                            proportion = (count / total_count) * 100
                                            so_proportion_dictionary = {'continent': continent, 'proportion': proportion}
                                            so_proportion_dictionary_list.append(so_proportion_dictionary)
                        so_proportion_dictionary_list = sorted(so_proportion_dictionary_list, key=lambda x: x['proportion'], reverse=True)
                        stackoverflow_proportion.append({f'{framework}':so_proportion_dictionary_list })        
                        for key, value in grouped_data_github.items():
                            if key == framework:
                                github_continent_count_list = value
                                print(github_continent_count_list)
                                total_count_github = sum(item['count'] for item in github_continent_count_list)
                                for continent in continents:
                                    for github_data in github_continent_count_list:
                                        if github_data['co'] == continent:
                                            count = github_data['count']
                                            proportion = (count / total_count_github) * 100
                                            github_proportion_dictionary = {'continent': continent, 'proportion': proportion}
                                            github_proportion_dictionary_list.append(github_proportion_dictionary)
                        github_proportion_dictionary_list = sorted(github_proportion_dictionary_list, key=lambda x: x['proportion'], reverse=True)
                        github_proportion.append({f'{framework}':github_proportion_dictionary_list })
                    for github_lists in  github_proportion:
                        for so_lists in stackoverflow_proportion:
                            for key, value in github_lists.items():
                                for framework , data in so_lists.items():
                                    if key == framework:
                                        print(f'framework--{framework}')
                                        so_highest_data = data[0]
                                        so_highest_continent = so_highest_data['continent']
                                        so_highest_prop = so_highest_data['proportion']
                                        print(f'In stackoverflow {so_highest_continent} has the highest proportion -- {so_highest_prop} % ')
                                        github_highest_data = value[0]
                                        github_highest_continent = github_highest_data['continent']
                                        github_highest_prop = github_highest_data['proportion']
                                        print(f'In github {github_highest_continent} has the highest proportion -- {github_highest_prop} % ')
            
                                        for values in value:
                                            for datas in data:
                                                
                                                if values['continent'] == datas['continent']:
                                                    continent = values['continent']
                                                    so_value = datas['proportion']
                                                    github_value = values['proportion']
                                                    print(f'continent - {continent}')
                                                    print(f'SO percentage ----> {so_value}') 
                                                    print(f'Github percentage---> {github_value}')
              
if __name__ == "__main__":
    calculate_framework_proportion_github()

