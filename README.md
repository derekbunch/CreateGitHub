Inspired by [KalleHallden](https://github.com/KalleHallden)'s [project](https://github.com/KalleHallden/ProjectInitializationAutomation) to automate the creation and deletion of a new github repo.

This project creates/deletes a folder on your local machine (organized by language) and initializes/removes it as a GitHub repo.

### Install: 
```bash
git clone https://github.com/derekbunch/CreateGitHub.git
cd CreateGitHub/bin
pip install -r requirements.txt
Update filepath in github file to the path where you installed CreateGitHub
./github
```
If you would like to run this from anywhere, add _<path_to_file>/CreateGitHub/bin_ to the $PATH in your shell

### Usage:
```bash
To run the script type in 'github <name of your project> <language> <Option>'

Options:
-c: Create
-d: Delete
```
If you face any issues with GitHub login, just delete the config.json file and you can go through the setup process again

Things I learned in this project:
* Read/Write JSON in Python
* Github API
* Webscraping with Selenium
