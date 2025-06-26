# conda activate nlpfull
# pip install --no-deps --upgrade --requirement requirements.txt

# Explanation:
# --requirement or -r: Reads from requirements.txt.
# --no-deps: Prevents pip from reinstalling dependencies unnecessarily (optional).
# --upgrade: Installs if missing or outdated.
# ⚠️ Pip will still check the listed packages and install them if they're missing or outdated.


# Python script to install missing packages from requirements.txt using conda or pip

import subprocess
from importlib.metadata import version, PackageNotFoundError
from packaging.requirements import Requirement
from packaging.version import Version, InvalidVersion

def is_requirement_satisfied(req_str):
    try:
        req = Requirement(req_str)  # parses things like "openai>=1.3.3"
        installed_version = Version(version(req.name))
        if installed_version in req.specifier:
            print(f"{req} already satisfied (version {installed_version})")
            return True
        else:
            print(f"{req} found but version mismatch: {installed_version} not in {req.specifier}")
            return False
    except PackageNotFoundError:
        print(f"{req_str} not installed.")
        return False
    except InvalidVersion as e:
        print(f"Invalid version string in {req_str}: {e}")
        return False

def install_with_conda(package_name):
    try:
        subprocess.check_call(["conda", "install", "--yes", package_name])
        print(f"✔ Installed {package_name} via conda.")
        return True
    except subprocess.CalledProcessError:
        print(f"⚠ {package_name} not available via conda.")
        return False

def install_with_pip(requirement_str):
    try:
        subprocess.check_call(["pip", "install", requirement_str])
        print(f"✔ Installed {requirement_str} via pip.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {requirement_str} via pip. Error: {e}")

# Read from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

for req_str in requirements:
    if is_requirement_satisfied(req_str):
        continue

    base_pkg_name = Requirement(req_str).name

    # Try conda install (without version constraint)
    if not install_with_conda(base_pkg_name):
        install_with_pip(req_str)

