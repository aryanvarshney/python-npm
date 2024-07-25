import argparse
from add import add
from install import install

'''
Controller for parsing CLI commands. Ideally this will be a class and be much more robust in argument handling.
'''
parser = argparse.ArgumentParser(usage="Current commands supported: add, install")
parser.add_argument("command", type=str,help="node package manager action (add, install)")
parser.add_argument("path", type=str, help="The path to the directory where the package.json file is located")
parser.add_argument("--package", type=str, help="Provide package in either format package_name or package_name@package_version", )

args = parser.parse_args()
if args.command == "add":
    if args.path is not None and args.package is not None:
        add(args.package, args.path)
    else:
        raise SystemExit("Please provide a path and package argument")
elif args.command == "install":
    if args.path is not None:
        install(args.path)
    else:
        raise SystemExit("Please provide a path argument")
else:
    raise SystemExit("Currently only add and install commands are supported")
    