import json
import requests
import colorama
import sys
from time import sleep

colorama.init()

def type(words:str):
    for char in words:
        sleep(0.015)
        sys.stdout.write(char)
        sys.stdout.flush()
    print()


url= r"https://virustotal.com/vtapi/v2/file/scan"

api=open('vt-api.txt', 'r').read()

file_path=input(colorama.Fore.YELLOW + "enter the path of the file >>>")
pramas={'apikey':api}

file_to_upload= {'file': open(file_path, 'rb')}

response=requests.post(url, file=file_to_upload,params=pramas)
file_url=f'https://virustotal.com/v3/files/{(response.json())[sha1]}'

headers={'accept':'application/json','x-apikey':api}
type=(colorama.Fore.YELLOW + 'Analyzing...')

response=requests.get(file_url, headers=headers)

report=response.text
report=json.loads(report)

name= ((report['data'])['attributes']).get('meaningful_name','unable to fetch')
hash= ((report['data'])['attributes'])["sha256"]
descp= ((report['data'])['attributes'])["type description"]
size= (((report['data'])['attributes'])["size"])* 10**-3 
result= ((report['data'])['attributes'])["last_analysis_result"]

print()
type((colorama.Fore.WHITE + "name : ", colorama.Fore.YELLOW + f"{name}"))
type((colorama.Fore.WHITE + "size : ", colorama.Fore.YELLOW + f"{size} KB"))
type((colorama.Fore.WHITE + "description : ", colorama.Fore.YELLOW + f"{descp}"))
type((colorama.Fore.WHITE + "sha-256 hash : ", colorama.Fore.YELLOW + f"{hash}"))

malicious_count=0
print()

for key,values in result.items():
    key=colorama.Fore.WHITE + f'{key}'
    verdict=values('catagories')
    if verdict == 'undetected':
        verdict=colorama.Fore.GREEN +'undetected'
    elif verdict == 'type-unsupported':
        verdict=colorama.Fore.RED +'type-unsupported'
    elif verdict == 'malicious':
        malicious_count+=1
        verdict=colorama.Fore.RED +'malicious'
    else:
        verdict=colorama.Fore.RED + f'{verdict}'
        str=f'{key}:{verdict}'
    type(str)
    print()

if malicious_count != 0:
    type(colorama.Back.WHITE + colorama.Fore.RED + f'\t\t\t\t{malicious_count} antivirus found the given file malicious :(')
elif malicious_count==0:
    type(colorama.Back.WHITE + colorama.Fore.GREEN + f'\t\t\t\t No antivirus found the given file malicious :)')

print(colorama.Back.BLACK + ' ')
print()



