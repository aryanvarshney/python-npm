import re
import requests

'''
Adds packages from the npm registry to the package.json file. If version is not included, add the latest release of the package

@param: package_and_version: String that is formatted either '{package name}' or '{package name}@{version}' depending on if a package version is included
'''
API = "https://registry.npmjs.org/"

def add(package_and_version: str):
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

    
    
'''
Helper method for making get request to npm registry
'''
def npm_registry_request(package_name: str, package_version: str ="latest"):
    request_url = API + package_name + "/" + package_version
    response = requests.get(request_url)
    try:
        response = requests.get(request_url)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise SystemExit("Something went wrong and the request timed out")
    except requests.exceptions.TooManyRedirects:
        raise SystemExit("Something went wrong and the request caused too many redirects")
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response.json()


npm_registry_request("tiny-tarball")