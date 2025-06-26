# conda activate nlpfull
# pip install --no-deps --upgrade --requirement requirements.txt

# Explanation:
# --requirement or -r: Reads from requirements.txt.
# --no-deps: Prevents pip from reinstalling dependencies unnecessarily (optional).
# --upgrade: Installs if missing or outdated.
# ⚠️ Pip will still check the listed packages and install them if they're missing or outdated.


# Python script to install missing packages from requirements.txt using conda or pip

import pkg_resources # pkg_resources: Used to check if a package (and version) is installed. >conda install setuptools
import subprocess # subprocess: Runs pip install commands from within Python.

def is_package_installed(requirement_str):
    try:
        pkg_resources.require(requirement_str)
        print(f"{requirement_str} is already installed.")
        return True
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
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

for req in requirements:
    if is_package_installed(req):
        continue

    # Extract base package name (strip version constraints like ==, >=)
    base_pkg = req.split("==")[0].split(">=")[0].split("<=")[0].strip()

    # Try installing via conda
    if not install_with_conda(base_pkg):
        # Fall back to pip
        install_with_pip(req)
