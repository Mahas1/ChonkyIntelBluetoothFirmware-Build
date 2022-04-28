import json
import os
import sys
from pathlib import Path

import assets

# Change the current directory to the project's root - Useful when the script is run from another working directory
project_root = Path(__file__).parent.absolute()
os.chdir(project_root)

if not assets.check_os():
    print("This script can only be run on macOS. Exiting...")
    sys.exit()

# Check for git and xcode installation
if not assets.check_xcode():
    print("Xcode is not installed. Please install Xcode to use this script.")
    sys.exit()

git_installed = assets.check_git()
if not git_installed:
    print("Git is not installed. Please install git to use the full potential of this script.")


if git_installed and not assets.check_dir("IntelBluetoothFirmware"):
    assets.download_src(ask_for_confirm=True)


os.chdir("IntelBluetoothFirmware")
# Change directory to the IntelBluetoothFirmware project root


try:
    os.remove('IntelBluetoothFirmware/FwBinary.cpp')
except FileNotFoundError:
    pass

firmwares = [fw[:-4] for fw in os.listdir('IntelBluetoothFirmware/fw') if not fw.endswith('.ddc')]
with open("firmwares.json", "w") as f:
    json.dump(firmwares, f)

try:
    os.mkdir('../Kexts')
except FileExistsError:
    pass

for firmware in firmwares:
    os.system(f'find IntelBluetoothFirmware/fw -type f -not -name "{firmware}.*" -delete')
    os.system('xcodebuild -project IntelBluetoothFirmware.xcodeproj -target fw_gen -configuration Release -sdk macosx')
    os.system(
        'xcodebuild -project IntelBluetoothFirmware.xcodeproj -target IntelBluetoothFirmware -configuration Release -sdk macosx')
    os.system(f'zip -r build/Release/{firmware}.zip build/Release/*.kext')
    os.system(f'mv build/Release/{firmware}.zip ../Kexts')
    os.system('git reset --hard HEAD')
    os.system('rm -rf build')
