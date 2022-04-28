import os
import platform
import subprocess
import sys

intel_bluetooth_url = r"https://github.com/OpenIntelWireless/IntelBluetoothFirmware"
mac_kernel_sdk_url = r"https://github.com/acidanthera/MacKernelSDK"


def check_xcode():
    command = subprocess.run("which xcodebuild", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    if command.returncode == 0:
        return True
    else:
        return False


def check_git():
    command = subprocess.run("which git", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
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


def clone_repo(repo_link, silent=False):
    kwargs = {}
    if silent:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL
    subprocess.run(["git", "clone", repo_link], **kwargs)


def check_dir(dir):
    if not os.path.isdir(dir):
        return False
    else:
        return True


def download_src(ask_for_confirm=True):
    if not os.path.exists("IntelBluetoothFirmware"):
        if ask_for_confirm:
            confirm = True if input("Download IntelBluetoothFirmware? (y/n): ").lower().strip() == "y" else False
        else:
            confirm = True
        if confirm:
            clone_repo(intel_bluetooth_url)
    os.chdir("IntelBluetoothFirmware")
    if not os.path.exists("MacKernelSdk") and confirm:
        clone_repo(mac_kernel_sdk_url)
    os.chdir("..")
