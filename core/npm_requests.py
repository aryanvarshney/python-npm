import requests
import shutil

API = "https://registry.npmjs.org/"

'''
Get request to npm registry for getting package metadata
@param package_name
@param package_version: defaults to latest version returned by npm registry
'''
def npm_registry_request(package_name: str, package_version: str ="latest"):
    request_url = API + package_name + "/" + package_version
    response = get_request(request_url)
    return response.json()

'''
Download tarball into dependency folder
@param git_url: Git url where the repo is stored
@param path: Directory where the repo should be downloaded to
'''
def download_tar(tarball: str, path: str):
    response = get_request(tarball)
    temp_tar_path = path + "/tmp/" + tarball
    with open(temp_tar_path, 'wb') as f:
        f.write(response.raw.read())
    shutil.unpack_archive(temp_tar_path, path)

'''
Helper method for get request with error handling
'''
def get_request(request_url: str):
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
    return response