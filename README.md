# JAVA Framework Analysis of Different Continents
We conducted an analysis of GitHub repositories to identify popular frameworks across seven continents. Subsequently, our objective was to establish a relationship between the proportions of the top distinct frameworks found within these continents and the respective proportions of StackOverflow questions associated with those frameworks

## System requirements
* Linux or macOS or Windows
* Python 3.11.5
* All the dependencies are listed in requirements.txt file

## Instructions

### 1. Repository Selection and Cloning
In the 'selecting_repos.py' file, we utilized the GitHub API to identify public Java project repositories meeting specific criteria: having more than 5 commits, a minimum gap of 180 days between the last pushed date and creation date of the repository, and having the user's location publicly available. Upon meeting these criteria, we cloned the repository into a designated directory (repositories directort) and created a 'location.txt' file within the cloned repository, containing the user's location information.

To execute this process, it requires a 'token.txt' file in the project folder, which should contain your GitHub token. The procedure took approximately 5-6 days to gather data from 2348 repositories due to limitations within the GitHub API. Each API call fetches a maximum of 100 repositories per page, and our specific criteria significantly filtered the repositories. Occasionally, encountering duplicate repositories in subsequent pages and experiencing system freezes necessitated re-running the 'python selecting_repos.py' command.

To make things easier we compiled all repository information into the 'repo_info.csv' file. To clone all repositories and obtain their associated location information in the 'repositories' directory, you can simply execute the command and this may consume approximately 64 GB:
```
python clone_repos.py
or 
python3 clone_repos.py
```

### 2. Answers to Research Question 1:  What are the popular Java frameworks in open-source software projects across different geographic regions?
To identify dependencies in Maven projects, we analyzed the 'pom.xml' files, while for Gradle projects, we analyzed the 'build.gradle' files. For other project types or instances with invalid 'build.gradle' files, we examined the import statements within the code. From these analyses, we mapped all dependencies and filtered for the specific frameworks of interest. The count of each framework for every continent was recorded and stored in the 'framework_count_with_country.json' file.

Utilizing these counts, we clustered the data according to continents, generating tables in the 'result' directory that list all frameworks alongside their respective counts within each continent. Notably, our investigation revealed that the minimum count of diverse frameworks across continents was only 3. Consequently, we extracted and compiled the top 3 frameworks for each continent, storing this information in the 'result' directory.

To reproduce the results of RQ1 (Research Question 1), after cloning all repositories, execute the command:
```
python finding_frameworks_github.py
or 
python3 finding_frameworks_github.py

```

### 3. Stack Overflow Question Analysis
After obtaining the top 3 frameworks from each continent based on the results of Research Question 1 (RQ1), we identified a total of 5 distinct frameworks. Using these frameworks as tags, we queried the Stack Exchange Data Explorer to retrieve the top 5000 questions with the most answers, provided that the user's location was public. It's important to note that some frameworks had fewer than 5000 questions available in the Stack Exchange database, and the retrieval of questions was last performed on 23/11/2023.
The query used is:

```
select TOP 20000 Posts.Body, Posts.Title, Posts.AnswerCount, Users.Location from Posts
INNER JOIN Users ON Posts.OwnerUserId = Users.Id
where Posts.Tags LIKE '%##Tag1##%' AND Users.Location IS NOT NULL AND Users.Location <> '' 
Order By Posts.AnswerCount desc
```

For access to the questions along with user locations, please download the entire folder from the following link 
'https://drive.google.com/drive/folders/1KoLDLys8iB05RHsvI83ERK_7sykmTaU3?usp=sharing'
and place it in the root directory of the project. Ensure that the directory name is 'SO_files'.

In the 'stackoverflow_analysis.py' script, we extracted the continent information from user locations and computed the count of questions for each continent. This process consumed more than 36 hours on average for all 5 frameworks, occasionally leading to system freezes, and needed to restart. To reproduce these findings, execute the command

```
 python stackoverflow_analysis.py
 or
 python3 stackoverflow_analysis.py
 ```

To make reproducibility easier for Research Question 2 (RQ2), all results have been stored in the 'so_continents' folder.
Please make sure 'so_continents' directory is there with 5 files to reproduce RQ2.

### 4. Answers to Research Question 2:  What is the relationship between the popular Java frameworks and the corresponding activity on StackOverflow within different geographic regions?

To find the proportion of github repositories and stackoverflow questions of each continent for each framework and the highest contributing continent of each platform
Please execute the command

```
python proportion_analysis.py 
or 
python3 stackoverflow_analysis.py
```
