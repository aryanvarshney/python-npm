import requests
from git import Repo

API = "https://registry.npmjs.org/"

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
    return response.json()

def download_repo(git_url: str):
    return