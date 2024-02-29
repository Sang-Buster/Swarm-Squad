import subprocess
import sys
from importlib.metadata import distribution, PackageNotFoundError
from packaging import version

REQUIRED_PACKAGES = [
    'dash>=2.15.0',
    'plotly>=5.19.0',
    'pandas>=2.2.1',
    'flask>=3.0.2',
    'flask-cors>=4.0.0',
]

for package in REQUIRED_PACKAGES:
    try:
        if '==' in package:
            package_name, package_version = package.split('==')
            operator = '=='
        elif '>=' in package:
            package_name, package_version = package.split('>=')
            operator = '>='

        dist = distribution(package_name)
        if operator == '==':
            condition = dist.version != package_version
        elif operator == '>=':
            condition = version.parse(dist.version) < version.parse(package_version)

        if condition:
            print('{} ({}) is installed, but {} is required'.format(dist.metadata['Name'], dist.version, package_version))
            subprocess.call([sys.executable, "-m", "pip", "install", package])
        else:
            print('{} ({}) is installed'.format(dist.metadata['Name'], dist.version))
    except PackageNotFoundError:
        print('{} is NOT installed'.format(package))
        subprocess.call([sys.executable, "-m", "pip", "install", package])