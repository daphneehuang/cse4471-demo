import sys
import requests

BASE_URL = 'https://api.github.com'

api_token = '3876589a061f3fd1739199b9577bec1a36994cac'
HEADERS = {'Authorization': f'token {api_token}'}

# Used so script ignores binary files
# We could do another way later if we don't want to list out all extensions we want
SCRAPABLE_EXTENSIONS = {'cpp', 'txt', 'py', 'config', 'c', 'js', 'html'}

def get_user_repos(username):
    """Gets list of public repositories owned by a particular user
    
        [:param `username`] the String representation of the user's username
        
        [:rtype] `list` of dictionaries
        
        [:returns] a list of the public repositories owned by the user
    """
    
    url = f'{BASE_URL}/users/{username}/repos'

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.HTTPError as e:
        sys.exit(e)

    all_repo_names = []
    for repo in response.json():
        all_repo_names.append(repo['name'])
    return all_repo_names


def get_repo_files(username, repo_name, path=''):
    """Gets list of all files for a specific user
    
        [:param `username`] the String representation of the user's username
        [:param `repo_name`] the String representation of the name of a repository
        [:param `path`] the String representation of the path of a directory within a repository. Used in recursive calls.
        
        [:rtype] `dictionary`
        
        [:returns] a dictionary of all the file paths and content from a given user's repository
    """


    '''    
    # Get the sha value for my call to recursively get the repo tree
    url = f'{BASE_URL}/repos/{username}/{repo_name}/branches/master'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as e:
        sys.exit(e)


    r = response.json()
    sha = r['commit']['sha']
    '''

    # Get the entire tree to get file paths and in turn create the download urls
    url = f'{BASE_URL}/repos/{username}/{repo_name}/git/trees/master?recursive=1'

    try:
        response = requests.get(url, headers=HEADERS)
        res = response.json()
    except requests.HTTPError as e:
        sys.exit(e)

    repo_files = {}
    tree = res['tree']
    for t in tree:
        if t['type'] == 'blob':
            file_path = t['path']
            file_ext = file_path.split(".")[-1]
            if file_ext in SCRAPABLE_EXTENSIONS:
                download_url = f'https://raw.githubusercontent.com/{username}/{repo_name}/master/{file_path}'
                content = requests.get(download_url, headers=HEADERS).text
                file_key = repo_name + '/' + file_path
                repo_files[file_key] = content

    return repo_files

def get_all_files_for_user(username):
    all_files = {}
    repo_names = get_user_repos(username)
    for name in repo_names:
        repo_files = get_repo_files(username, name)
        all_files.update(repo_files)
    return all_files

if __name__ == '__main__':
    username = 'ss5nathan'

    files = get_all_files_for_user(username)
    #repos = get_user_repos(username)
    print(files)
    '''
    repo_names = get_user_repos(username)
    print(repo_names)

    for name in repo_names:
        contents = get_repo_files(username, name)
        print(contents)
    '''


