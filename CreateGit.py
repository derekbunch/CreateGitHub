import sys, os
import json
from github import Github
import time

def setup():
    print('---------------')
    print(' Initial Setup ')
    print('---------------')
    installFolder = sys.argv[0].replace('CreateGit.py','')
    projectsFolder = input('Where would you like projects to be saved?\n')
    authMethod = input('Would you like to use an access token (instead of Username and Password)? (y/n)\n')
    username, password, token = '', '', ''
    while (authMethod != 'y' and authMethod != 'n'):
        authMethod = input("Please choose (y) or (n): ")
    if (authMethod == 'y'):
        token = input('Access Token: ')
    elif (authMethod == 'n'):
        username = input('Username: ')
        password = input('Password: ')
    
    data = {}
    data['credentials'] = {
        'username': username,
        'password' : password,
        'accesstoken' : token
    }
    data['languages'] = {}
    data['folders'] = {
        'install' : installFolder,
        'projects' : projectsFolder
    }

    with open(bin + 'config.json', 'w') as config:
        json.dump(data, config, sort_keys=True, indent=4)


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
    with open(bin + 'config.json') as config:
        data = json.load(config)
        username = data['credentials']['username']
        password = data['credentials']['password']
        token = data['credentials']['accesstoken']
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
    
    if (token is None):
        g = Github(username, password)
    else:
        g = Github(token)
    user = g.get_user()
    user.create_repo(projectName)

    # git actions
    os.chdir(projectName)
    os.system('git init')
    os.system('git remote add origin git@github.com:derekbunch/{}.git'.format(projectName))
    os.system('touch README.md')
    os.system('git add .')
    os.system('git commit -m "Initial Commit"')
    os.system('git push -u origin master')
    #os.system('code-insiders .')
    print('\n{} repo created!\n'.format(projectName))

def delete():
    bin = os.path.dirname(sys.argv[0]) + '/bin/'

    with open(bin + 'config.json') as config:
        data = json.load(config)
        username = data['credentials']['username']
        password = data['credentials']['password']
        token = data['credentials']['accesstoken']
    projectName = sys.argv[1]

    if (token is None):
        g = Github(username, password)
    else:
        g = Github(token)
    repo = g.get_repo(username + '/' + projectName)
    repo.delete()
    print('\n{} repo deleted!\n'.format(projectName))


if __name__ == '__main__':
    data = []
    bin = os.path.dirname(sys.argv[0]) + '/bin/'

    if (not os.path.isfile(bin + 'config.json')):
        setup()

    if(sys.argv[3] == '-c'):
        create()
    elif (sys.argv[3] == '-d'):
        delete()