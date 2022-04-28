import os
import platform
import subprocess
import sys

intel_bluetooth_url = r"https://github.com/OpenIntelWireless/IntelBluetoothFirmware"


def check_xcode():
    command = subprocess.run("xcodebuild -usage", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    if command.returncode == 0:
        return True
    else:
        return False


def check_git():
    command = subprocess.run("git --help", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    if command.returncode == 0:
        return True
    else:
        return False


def change_title(title):
    sys.stdout.write("\033]0;{}\007").__format__(title)


def check_os():
    if platform.system() == "Darwin":
        return True
    else:
        return False


def clone_repo(repo_link, print_output=True, print_errors=True):
    kwargs = {}
    if not print_output:
        kwargs["stdout"] = subprocess.DEVNULL
    if not print_errors:
        kwargs["stderr"] = subprocess.DEVNULL
    subprocess.run(["git", "clone", repo_link], **kwargs)


def check_dir(dir):
    if not os.path.isdir(dir):
        return False
    else:
        return True
