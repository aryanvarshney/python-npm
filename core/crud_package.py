from pathlib import Path
import json

'''
Get content of current package.json file
@param path: Directory where package.json exists
'''
def get_package_json_content(path: str):
    os_path = Path(path)
    package_json = os_path / 'package.json'
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