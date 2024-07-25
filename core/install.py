from crud_package import get_package_json_content
from npm_requests import npm_registry_request, download_tar
from pathlib import Path

'''
Install packages listed in the package.json file
@param path: Location of package.json file
'''
def install(path: str):
    data = get_package_json_content(path)
    os_path = Path(path)
    dependencies_folder = (os_path / 'dependencies').mkdir(parents=True, exist_ok=True)
    dependencies_path_str = path + "/dependencies"
    downloaded_map = {}
    download_queue = []
    tar_list = []

    if "dependencies" not in data:
        print("There are no dependencies installed")
        return
    dependencies = data[dependencies]

    for package, version in dependencies.items():
        download_queue.append((package, version))
    while len(download_queue) > 0:
        curr_package, curr_version = download_queue.pop()
        if curr_package in downloaded_map:
            if curr_version != downloaded_map[curr_package]:
                raise SystemExit("There is a discrepancy in " + curr_package + ". The 2 conflicting versions are " + curr_version + " and " + downloaded_map[curr_package])
        else:
            package_metadata = npm_registry_request(curr_package, curr_version)
            tarball = package_metadata["versions"][curr_version]["dist"]["tarball"]
            tar_list.append(tarball)
            if "dependencies" in package_metadata:
                for dep_package, dep_version in package_metadata["dependencies"].items():
                    download_queue.append((dep_package, dep_version))
            downloaded_map[curr_package] = curr_version

    for tarball in tar_list:
        download_tar(tarball, dependencies_path_str)
    
