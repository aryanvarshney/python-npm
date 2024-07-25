import re
from pathlib import Path
from crud_package import *
from npm_requests import *

'''
Adds packages from the npm registry to the package.json file. If version is not included, add the latest release of the package

@param: package_and_version: String that is formatted either '{package name}' or '{package name}@{version}' depending on if a package version is included
@param: path: Path to the package.json file to update
'''
def add(package_and_version: str, path: str):
    # Parse string and check if it is valid format
    at_index = package_and_version.find('@')
    has_version_included = False
    if at_index == -1:
        package_name = package_and_version
        package_version = "latest"
    else:
        has_version_included = True
        package_name = package_and_version[:at_index]
        package_version = package_and_version[at_index+1:]
    if has_version_included:
        version_pattern = re.compile("^([0-9]{1,3}\.){2}[0-9]{1,3}(-(.*))$") 
        if not version_pattern.match(package_version):
            raise ValueError("Invalid input: the version number you have provided does not follow the correct pattern. Note: You must provide all major, minor, and patch numbers when including version")
    package_metadata = npm_registry_request(package_name, package_version)
    curr_package_json = get_package_json_content(path)
    if "dependencies" in curr_package_json:
        curr_package_json["dependencies"][package_metadata["name"]] = package_metadata["version"]
    else:
        curr_package_json["dependencies"] = {package_metadata["name"]: package_metadata["version"]}
    update_package_json_content(path, curr_package_json)
