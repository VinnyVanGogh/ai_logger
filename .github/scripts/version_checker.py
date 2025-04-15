import os
import sys
import configparser
import toml
import requests
from pathlib import Path

PACKAGE_NAME = "my_package"

def find_package_name():
    cwd = Path.cwd()
    setup_cfg = cwd / 'setup.cfg'
    pyproject_toml = cwd / 'pyproject.toml'
    if os.path.exists(setup_cfg):
        config = configparser.ConfigParser()
        config.read(setup_cfg)
        if 'metadata' in config and 'name' in config['metadata']:
            package_name = config['metadata']['name']

    if os.path.exists(pyproject_toml):
        try:
            with open(pyproject_toml, 'r') as file:
                pyproject_data = toml.load(file)
                package_name = pyproject_data.get('project', {}).get('name')
        except (FileNotFoundError, toml.TomlDecodeError):
            pass

    if not os.path.exists(pyproject_toml) and not os.path.exists(setup_cfg):
        package_name = PACKAGE_NAME

    return package_name

def get_pypi_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    print(f"Fetching version from PyPI: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching version from PyPI: {e}")
        return None

def get_setup_cfg_version():
    config = configparser.ConfigParser()
    config.read('setup.cfg')

    if 'metadata' in config and 'version' in config['metadata']:
        return config['metadata']['version']
    return None

def get_pyproject_toml_version():
    try:
        with open('pyproject.toml', 'r') as file:
            pyproject_data = toml.load(file)
            return pyproject_data.get('project', {}).get('version')
    except (FileNotFoundError, toml.TomlDecodeError):
        return None

def main():
    package_name = find_package_name()

    pypi_version = get_pypi_version(package_name)

    try:
        setup_cfg_version = get_setup_cfg_version()
        if setup_cfg_version and setup_cfg_version != pypi_version:
            print(f"Version changed in setup.cfg: {pypi_version} -> {setup_cfg_version}")
            sys.exit(0)
    except Exception as e:
        print(f"Error fetching version from setup.cfg: {e}")
        try:
            pyproject_toml_version = get_pyproject_toml_version()

            if pyproject_toml_version and pyproject_toml_version != pypi_version:
                print(f"Version changed in pyproject.toml: {pypi_version} -> {pyproject_toml_version}")
                sys.exit(0)
        except Exception as e:
            print(f"Error fetching version from pyproject.toml and setup.cfg: {e}")
            sys.exit(1)

    print("No version changes detected.")
    sys.exit(1)

if __name__ == "__main__":
    main()
