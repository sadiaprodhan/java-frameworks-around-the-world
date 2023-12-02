import csv
import subprocess
import os
from git import Repo  
def clone_repo(url,location, target_directory):
    try:
        repo_path = os.path.join(target_directory, os.path.basename(url).split('.')[0]) 
        if not os.path.exists(repo_path):
            repo = Repo.clone_from(url, repo_path, depth=1)
            print("Repository cloned successfully.")
            text_file_path = os.path.join(repo_path, 'location.txt')
            file_name = 'location.txt'  
            text_content = f'{location}'  
            created_file_path = create_text_file(repo_path, file_name, text_content)
    
            if created_file_path:
                 print(f"Text file created at: {created_file_path}")
            else:
                print("Failed to create the text file.")

        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def create_text_file(repo_path, file_name, text):
    file_path = os.path.join(repo_path, file_name)
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(text)
    return file_path

def get_csv_file(csv_file_path, target_directory):
    try:
        with open(csv_file_path, 'r', encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  
            for row in csv_reader:
                url, location= row
                clone_repo(url,location, target_directory)
    except FileNotFoundError:
        print("CSV file not found or path is incorrect.")
    



if __name__ == "__main__":
    get_csv_file(os.path.join(os.getcwd(),'repo_info.csv'),os.path.join(os.getcwd(),'repositories') )
