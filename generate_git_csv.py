import subprocess
import os
import csv
from git import Repo 
import shutil


repo_list = []
def prepare_csv(directory):
    i=0
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            git_repo_path = os.path.join(root, '.git')
            path = os.path.dirname(git_repo_path)
            print(path)
   
            try:
                repo = Repo(path)
                 
        
        # Get remote repository URLs
                remote_urls = [remote.url for remote in repo.remotes]
                repo_url = remote_urls[0]
        # Change directory to the repository path
                print(repo_url)

        # Get the commit hash of HEAD
                result_commit = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
                location_file = os.path.join(path, 'location.txt')
                if not os.path.exists(location_file):
                    shutil.rmtree(git_repo_path)
        
                else:
                    print(location_file)
                    with open(location_file, 'r', encoding="utf-8") as file:
                        location = file.read()
                        repo_list.append({'repo_url': repo_url,  'location': location})
                    
    

            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
            
    output_file = 'repo_info.csv'
    with open(output_file, 'w', encoding="utf-8", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Repository URL' 'Location'])
        for repo in repo_list:
            csv_writer.writerow([repo['repo_url'],  repo['location']])           

        
if __name__ == "__main__":
    prepare_csv(os.path.join(os.getcwd(),'repositories'))
    