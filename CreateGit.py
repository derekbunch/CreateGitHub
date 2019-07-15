import sys, os
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

# def setup(installLocation):
#     with open(installLocation + '/bin/config.json', 'r+') as config:
#         data = json.load(config)
#         install = data['folders']
#         install['install'] = installLocation
#         config.seek(0, 0)
#         json.dump(config, data)
#         config.truncate()

def newLanguage (language):
    print('This is a new language!')
    new = input('Would you like to create a new directory for this language? (y/n): ')
    while (new != 'y' and new != 'n'):
        new = input("Please choose (y) or (n): ")
    if (new == 'y'):
        os.mkdir('./{}'.format(language))
        print('Directory {} created!'.format(language))
    elif (new == 'n'):
        print('Nowhere to put files. Cancelling')
        sys.exit(1)

def create():
    bin = os.path.dirname(sys.argv[0]) + '/bin/'

    with open(bin + 'config.json') as config:
        data = json.load(config)
        #setup(os.path.dirname(sys.argv[0]))
        username = data['credentials']['username']
        password = data['credentials']['password']
        projectsFolder = data['folders']['projects']

    # Set variables for passed argument for reuse
    projectName = sys.argv[1]
    
    if (sys.argv[2] in data['languages']):
        language = data['languages'][sys.argv[2]]
    else:
        language = sys.argv[2]

    os.chdir(projectsFolder)
    dirs = os.listdir('.')
    # If there is not currently a folder for the language, create one and navigate to it
    if(language not in dirs):
        newLanguage(language)

    os.chdir('./{}'.format(language))
    try:
        os.mkdir('./{}'.format(projectName))
    except:
        new = input('This project already exists. What would you like to do? (o)verwrite/(n)ew name: ')
        while (new != 'o' and new != 'n'):
            new = input("Please choose (o) or (n): ")
        if (new == 'o'):
            confirm = input('Are you sure? (y/n) ')
            if (confirm == 'y'):
                os.rmdir('./{}'.format(projectName))
                os.mkdir('./{}'.format(projectName))
        elif (new == 'n'):
            projectName = input('What would you like the new name to be? ')
    
    options = Options()
    options.headless = True
    browser = webdriver.Firefox()#options=options)#,firefox_binary=bin)
    browser.get('http://github.com/login')

    pyButton = browser.find_element_by_xpath('//*[@id="login_field"]')
    pyButton.send_keys(username)
    pyButton = browser.find_element_by_xpath('//*[@id="password"]')
    pyButton.send_keys(password)
    pyButton = browser.find_element_by_xpath('/html/body/div[3]/main/div/form/div[3]/input[4]')
    pyButton.click()
    pyButton = browser.find_element_by_xpath('/html/body/div[4]/div/aside[1]/div[2]/div/div/h2/a')
    pyButton.click()
    pyButton = browser.find_element_by_xpath('//*[@id="repository_name"]')
    pyButton.send_keys(projectName)
    pyButton = browser.find_element_by_xpath('//*[@id="repository_visibility_private"]')
    pyButton.click()
    time.sleep(1)
    pyButton = browser.find_element_by_xpath('/html/body/div[4]/main/div/form/div[3]/button')
    pyButton.click()
    browser.close()

    os.chdir(projectName)
    os.system('git init')
    os.system('git remote add origin git@github.com:derekbunch/{}.git'.format(projectName))
    os.system('touch README.md')
    os.system('git add .')
    os.system('git commit -m "Initial Commit"')
    os.system('git push -u origin master')
    #os.system('code .')

if __name__ == '__main__':
    create()