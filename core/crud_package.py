from pathlib import Path
import json
import git

'''
Get content of current package.json file
@param path: Directory where package.json exists
'''
def get_package_json_content(path: str):
    os_path = Path(path)
    if not os_path.is_dir():
        SystemExit("Please provide a valid file path to a directory")
    package_json = os_path / 'package.json'
    if not package_json.is_file():
        SystemExit("There is no package.json file in the specified directory: " + str(os_path))
    content = package_json.read_text()
    data = json.load(content)
    return data

'''
Update content of current package.json file
@param path: Directory where package.json exists
'''
def update_package_json_content(path: str, package_json_data):
    os_path = Path(path)
    package_json = os_path / 'package.json'
    content = json.dumps(package_json_data)
    package_json.write_text(content)

'''
Download git repo into dependency folder
@param git_url: Git url where the repo is stored
@param path: Directory where the repo should be downloaded to
'''
def download_repo(git_url: str, path: str):
    os_path = Path(path)
    dependencies_folder = (os_path / 'dependencies').mkdir(parents=True, exist_ok=True)
    try:
        git.Repo.clone_from(git_url, dependencies_folder)
    except git.exc.GitError as err:
        SystemExit(err)
    return
