import requests
import shutil
from pathlib import Path

API = "https://registry.npmjs.org/"

'''
Get request to npm registry for getting package metadata
@param package_name
@param package_version: defaults to latest version returned by npm registry
'''
def npm_registry_request(package_name: str, package_version: str ="latest"):
    if package_version[0] == '^':
        package_version = package_version[1:]
    request_url = API + package_name + "/" + package_version
    response = get_request(request_url)
    return response.json()

'''
Download tarball into dependency folder
@param package: name of package
@param tarball: Url where the tar file is stored
@param path: Directory where the repo should be downloaded to
'''
def download_tar(package: str, tarball: str, path: str):
    response = get_request(tarball)
    temp_path = Path("tmp/")
    temp_path.mkdir(parents=True, exist_ok=True)
    file_name = package + ".tgz"
    temp_tar_path = temp_path / file_name
    with open(temp_tar_path, 'wb') as f:
        f.write(response.raw.read())
    dependencies_path = Path(path) / package
    dependencies_path.mkdir(parents=True, exist_ok=True)
    shutil.unpack_archive(temp_tar_path, dependencies_path)
    shutil.rmtree(temp_path)

'''
Helper method for get request with error handling
'''
def get_request(request_url: str):
    try:
        response = requests.get(request_url, stream=True)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise SystemExit("Something went wrong and the request timed out")
    except requests.exceptions.TooManyRedirects:
        raise SystemExit("Something went wrong and the request caused too many redirects")
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    return response