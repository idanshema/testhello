
import os
import requests
import hashlib
from colorama import init, Fore, Style
import sys
import time

init()

def type(text, delay=0.0001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as e:
        type(Fore.RED + f"Error reading file {file_path}: {e}")
        return None
    return hash_md5.hexdigest()

def check_file_with_virustotal(api_key, file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {
        "x-apikey": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        type(Fore.RED + f"Error querying VirusTotal: {response.status_code}")
        return None

def scan_folder(api_key, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            type(Style.BRIGHT + Fore.YELLOW + f"Scanning file: {file_path}")
            file_hash = get_file_hash(file_path)
            if file_hash:
                result = check_file_with_virustotal(api_key, file_hash)
                if result:
                    data = result.get("data", {}).get("attributes", {})
                    if data.get("last_analysis_stats", {}).get("malicious", 0) > 0:
                        type(Fore.RED + f"File {file_path} is malicious!")
                    else:
                        type(Fore.GREEN + f"File {file_path} is clean.")
            print(Style.RESET_ALL)

def main():
    type(Fore.CYAN + "Enter your VirusTotal API key: ", delay=0.02)
    api_key = input()
    type(Fore.CYAN + "Enter the path to the folder you want to scan: ", delay=0.02)
    folder_path = input()
    
    if not os.path.exists(folder_path):
        type(Fore.RED + "The folder path does not exist. Please enter a valid path.")
        return
    
    scan_folder(api_key, folder_path)
    type(Fore.CYAN + "Scanning completed.")
    print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
