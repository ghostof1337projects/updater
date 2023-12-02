import os
import requests
import ctypes

# GitHub repository information
repo_owner = 'ghostof1337projects'
repo_name = 'updater'
repo_branch = 'main'  # or specify your branch

# Local directory to store the executable file
local_dir = 'python'
local_exe_path = os.path.join(local_dir, 'Updater.py')  # Replace with your executable file name

def download_latest_release():
    # Fetch the latest release information from GitHub
    releases_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
    
    try:
        response = requests.get(releases_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        if response.status_code == 200:
            release_info = response.json()
            asset_name = 'Updater.py'  # Replace with your executable file name
            download_asset(asset_name, release_info)
        else:
            print(f"Failed to fetch latest release information. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest release information: {e}")

def download_asset(asset_name, release_info):
    asset_url = None
    for asset in release_info['assets']:
        if asset['name'] == asset_name:
            asset_url = asset['browser_download_url']
            break
    
    if asset_url:
        try:
            response = requests.get(asset_url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            
            local_asset_size = 0
            if os.path.exists(local_exe_path):
                local_asset_size = os.path.getsize(local_exe_path)
            
            with open(local_exe_path, 'wb') as file:
                file.write(response.content)
            
            new_asset_size = os.path.getsize(local_exe_path)
            
            if local_asset_size != new_asset_size:
                print("New version downloaded! Updating...")
                remove_old_version()
            else:
                print("No new updates available.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {asset_name}: {e}")
    else:
        print(f"No asset named {asset_name} found in the release.")

def remove_old_version():
    if os.path.exists(local_exe_path):
        try:
            os.remove(local_exe_path)
            print("Old version removed.")
        except OSError as e:
            print(f"Error removing old version: {e}")

def check_for_updates():
    # Check if there are newer versions available on GitHub
    latest_release_url = f'https://github.com/{repo_owner}/{repo_name}/releases/latest'
    
    try:
        response = requests.head(latest_release_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        if response.status_code == 200:
            print("Checking for updates...")
            download_latest_release()
        elif response.status_code == 302:
            print("New update available! Downloading...")
            download_latest_release()
        else:
            print(f"Failed to check for updates. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking for updates: {e}")
check_for_updates()

message = "OLD VERSION"
ctypes.windll.user32.MessageBoxW(0, message, "V1", 0x30)
