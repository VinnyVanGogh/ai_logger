import os
import sys
import configparser
import toml
import requests
from pathlib import Path

DEFAULT_PACKAGE_NAME = "my_package"

def find_package_name():
    """Find package name from setup.cfg, pyproject.toml (standard or Poetry), or setup.py files."""
    cwd = Path.cwd()
    setup_cfg = cwd / 'setup.cfg'
    pyproject_toml = cwd / 'pyproject.toml'
    package_name = None

    # Try to get name from setup.cfg
    if os.path.exists(setup_cfg):
        config = configparser.ConfigParser()
        config.read(setup_cfg)
        if 'metadata' in config and 'name' in config['metadata']:
            package_name = config['metadata']['name']
            print(f"Found package name in setup.cfg: {package_name}")
            return package_name

    # Try to get name from pyproject.toml (checking both standard and Poetry formats)
    if os.path.exists(pyproject_toml):
        try:
            with open(pyproject_toml, 'r') as file:
                pyproject_data = toml.load(file)
                
                # Check standard format
                if 'project' in pyproject_data and 'name' in pyproject_data['project']:
                    package_name = pyproject_data['project']['name']
                    print(f"Found package name in pyproject.toml (standard format): {package_name}")
                    return package_name
                
                # Check Poetry format
                if 'tool' in pyproject_data and 'poetry' in pyproject_data['tool'] and 'name' in pyproject_data['tool']['poetry']:
                    package_name = pyproject_data['tool']['poetry']['name']
                    print(f"Found package name in pyproject.toml (Poetry format): {package_name}")
                    return package_name
                
                # Look for the package under src directory
                if os.path.exists('src'):
                    subdirs = [d for d in os.listdir('src') if os.path.isdir(os.path.join('src', d))]
                    if len(subdirs) == 1 and not subdirs[0].startswith('__'):
                        package_name = subdirs[0]
                        print(f"Inferred package name from src directory structure: {package_name}")
                        return package_name
                
        except (FileNotFoundError, toml.TomlDecodeError) as e:
            print(f"Error reading pyproject.toml: {e}")

    # Use default if nothing was found
    print(f"No package name found, using default: {DEFAULT_PACKAGE_NAME}")
    return DEFAULT_PACKAGE_NAME

def get_pypi_version(package_name):
    """Get the latest version of a package from PyPI."""
    if not package_name:
        return None
        
    url = f"https://pypi.org/pypi/{package_name}/json"
    print(f"Fetching version from PyPI: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        version = data['info']['version']
        print(f"Found version {version} on PyPI")
        return version
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
            print(f"Package {package_name} not found on PyPI. This might be a new package.")
            return None
        else:
            print(f"Error fetching version from PyPI: {e}")
            return None

def get_setup_cfg_version():
    """Get version from setup.cfg file."""
    if not os.path.exists('setup.cfg'):
        return None
        
    config = configparser.ConfigParser()
    config.read('setup.cfg')

    if 'metadata' in config and 'version' in config['metadata']:
        version = config['metadata']['version']
        print(f"Found version {version} in setup.cfg")
        return version
    return None

def get_pyproject_toml_version():
    """Get version from pyproject.toml file (checking both standard and Poetry formats)."""
    if not os.path.exists('pyproject.toml'):
        return None
        
    try:
        with open('pyproject.toml', 'r') as file:
            pyproject_data = toml.load(file)
            
            # Check standard format
            if 'project' in pyproject_data and 'version' in pyproject_data['project']:
                version = pyproject_data['project']['version']
                print(f"Found version {version} in pyproject.toml (standard format)")
                return version
            
            # Check Poetry format
            if 'tool' in pyproject_data and 'poetry' in pyproject_data['tool'] and 'version' in pyproject_data['tool']['poetry']:
                version = pyproject_data['tool']['poetry']['version']
                print(f"Found version {version} in pyproject.toml (Poetry format)")
                return version
                
    except (FileNotFoundError, toml.TomlDecodeError) as e:
        print(f"Error reading pyproject.toml: {e}")
    
    return None

def main():
    # Get package name
    package_name = find_package_name()
    
    # Get local version from either setup.cfg or pyproject.toml
    local_version = get_setup_cfg_version() or get_pyproject_toml_version()
    
    if not local_version:
        print("No local version found in setup.cfg or pyproject.toml.")
        sys.exit(1)
    
    # Get PyPI version (might be None if package doesn't exist)
    pypi_version = get_pypi_version(package_name)
    
    # If package doesn't exist on PyPI, this is a new package
    if pypi_version is None:
        print(f"Package {package_name} not found on PyPI. This appears to be a new package with version {local_version}.")
        sys.exit(0)  # Success for new packages
    
    # Compare versions
    if local_version != pypi_version:
        print(f"Version changed: {pypi_version} -> {local_version}")
        sys.exit(0)  # Success for version changes
    else:
        print(f"No version change detected. Local and PyPI versions are both {local_version}.")
        sys.exit(1)  # No change detected

if __name__ == "__main__":
    main()