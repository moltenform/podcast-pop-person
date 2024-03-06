
# Ben Fisher, 2024
# https://github.com/moltenform/podcast-pop-person

import json
import os

def mainAskForInput():
    prefs = {}
    if os.path.exists('.prefs.json'):
        print('prefs file (.prefs.json) already exists.')
        return
        
    curl_path = input('Please enter a path for curl. If you are on a linux system, ' + 
        'just enter curl. If you are on a Windows system, we recommend you ' +
        'use curl from mingw64, Git for Windows, or chocolatey/msys2/scoop:')
    prefs['curl_path'] = curl_path
    
    sub_key = input('Go into Azure and create a Speech Service instance. ' +
        'You will need to be on the Standard pricing tier (but can still be in the $200 trial). ' +
        'On the first screen if you scroll down you will see Keys and Endpoint,'
        'Please copy one of the keys and paste it:')
    prefs['sub_key'] = sub_key
    
    region = input('Paste the Azure location/region, such as westus:')
    prefs['region'] = region
    
    with open('.prefs.json', 'w', encoding='utf-8') as fOut:
        fOut.write(json.dumps(prefs))
    
    print('Complete.')
    
if __name__=='__main__':
    mainAskForInput()

