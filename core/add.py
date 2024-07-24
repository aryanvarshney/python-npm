import re
import requests

'''
Adds packages from the npm registry to the package.json file. If version is not included, add the latest stable release of the package

@param: package_version: String that is formatted either '{package name}' or '{package name}@{version}' depending on if a package version is included
'''
def add(package_and_version: str):
    # Parse string and check if it is valid format
    at_index = package_and_version.find('@')
    has_version_included = False
    if at_index == -1:
        package_name = package_and_version
    else:
        has_version_included = True
        package_name = package_and_version[:at_index]
        package_version = package_and_version[at_index+1:]
    if has_version_included:
        version_pattern = re.compile("^([0-9]{1,3}\.){2}[0-9]{1,3}(-(.*))$") 
        if not version_pattern.match(package_version):
            raise ValueError("Invalid input: the version number you have provided does not follow the correct pattern")
    

def npm_registry_request(package_name: str, package_version: str):
    return