
# Ben Fisher, 2024
# https://github.com/moltenform/podcast-pop-person

import utils
import json
import textwrap
import os

minSpeakersToDetect = 2
maxSpeakersToDetect = 2
pollingSleepTime = 120
locale = 'en-US'

def mainAskForInput():
    print('Note that the script is designed for speaking only (not music) and only 2 speakers,')
    print('The results may not work well otherwise.\n\n')
    print('For convenience, there is an example file online, ' + 
        'https://moltenform.com/pages/podcast-pop-person/podcast-pop-person-demo.flac ' +
        'to help demo the project.')
        
    print("\n\nNote also that very long (>3 hour) files sometimes run into failures. Most of the time,")
    print("issue was resolved just by starting the job again from scratch.")
    print("\n\nIf the audio file isn't already online, it needs to be uploaded first, at least to Azure.")
    audioUrl = input('Please enter an online url for an audio file (should be mono):')
    outName = input('Please enter an output name (default=transcribed.json):')
    outName = outName or 'transcribed.json'
    outName = utils.helpInterpretPath(outName)
    utils.assertTrue(not os.path.exists(outName), 'Already exists', outName)
    main(audioUrl, outName)

def main(audioUrl, outName):
    prefs = utils.getPrefs()
    transcId = launchJob(prefs, audioUrl, minSpeakersToDetect, maxSpeakersToDetect)
    print(audioUrl, 'Job sent to azure. Transcription job id=', transcId)
    _pollUntilCompleted(prefs, transcId, audioUrl, outName, pollingSleepTime)
    print('Complete')

# Tell azure to begin the job.
# audioUrl must be a url accessible to azure, such as a public mp3 url.
def launchJob(prefs, audioUrl, speakerMin, speakerMax):
    args = rf'-v|-X|POST|-H|Ocp-Apim-Subscription-Key: {prefs.sub_key}|-H|Content-Type: application/json|-d'.split('|')
    displayName = audioUrl.split('/')[-1]
    assert '"' not in displayName and '\n' not in displayName and '{' not in displayName and '}' not in displayName
    assert '"' not in audioUrl and '\n' not in audioUrl and '{' not in audioUrl and '}' not in audioUrl
    
    # intentionally add en-US, de-DE, es-ES, because it errors if only en-US is provided.
    jsonText = r'''{
  "contentUrls": [
    "%audioUrl"
  ],
  "locale": "%locale",
  "displayName": "%displayName",
  "model": null,
  "properties": {
    "wordLevelTimestampsEnabled": true,
    "diarizationEnabled": true,
    "minCount": %speakerMin,
    "maxCount": %speakerMax,
    "languageIdentification": {
      "candidateLocales": [
        %candidateLocales
      ],
    }
  },
}    
    '''
    
    # quirk with Azure's system: the call fails if only en-US is given, so give all three.
    candidateLocales = '"en-US", "de-DE", "es-ES"'
    
    # fill in the template
    jsonText = jsonText.replace('%displayName', displayName).replace('%audioUrl', audioUrl)
    jsonText = jsonText.replace('%speakerMin', str(speakerMin)).replace('%speakerMax', str(speakerMax))
    jsonText = jsonText.replace('%locale', locale).replace('%candidateLocales', candidateLocales)
    
    endpoint =  rf"https://{prefs.region}.api.cognitive.microsoft.com/speechtotext/v3.2-preview.1/transcriptions"
    args.append(jsonText)
    args.append(endpoint)
    args.insert(0, prefs.curl_path)
    print(args)
    
    print('Sending to azure:', endpoint)
    retcode, stdout, stderr = utils.run(args)
    jsonObj = json.loads(stdout.decode('utf-8'))
    if 'self' not in jsonObj:
        utils.assertTrue(False, 'self not present', stdout, stderr)
    
    lnk = jsonObj['self']
    utils.assertTrue('/transcriptions/' in lnk)
    transcId = lnk.split('/transcriptions/')[1].split('/')[0].split('"')[0]
    return transcId
    

# Perform get request against Azure
def _azureHttpGet(prefs, url):
    print('GET request from url: ', url)
    args = (rf'-v|-X|GET|{url}|-H|Ocp-Apim-Subscription-Key: {prefs.sub_key}').split('|')
    args.insert(0, prefs.curl_path)
    retcode, stdout, stderr = utils.run(args)
    jsonObj = json.loads(stdout.decode('utf-8'))
    return jsonObj

# Sleep until the status is complete.
def _pollUntilCompleted(prefs, transcriptionId, audioUrl, outPath, sleepTime):
    while True:
        urlCheck = f"https://{prefs.region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions/" + transcriptionId
        jsonObj = _azureHttpGet(prefs, urlCheck)
    
        if jsonObj['status'] == 'Running':
            print(f'Retrying in {sleepTime}s...')
            import time
            time.sleep(sleepTime)
        elif jsonObj['status'] == 'Succeeded':
            break
        else:
            if 'fail' in str(jsonObj['status']).lower():
                print('failed, fail status', outPath)
            else:
                print('failed, unknown status', outPath)
            
            with open(outPath + '.failed.json','w', encoding='utf-8') as fOut:
                fOut.write(json.dumps(jsonObj))
            return None
    
    filesUrl = jsonObj['links']['files']
    jsonObjFiles = _azureHttpGet(prefs, filesUrl)
    alreadyWrote = False
    for i, item in enumerate(jsonObjFiles['values']):
        if item['kind'] == 'Transcription':
            contentUrl = item['links']['contentUrl']
            theContent = _azureHttpGet(prefs, contentUrl)
            
            if alreadyWrote:
                utils.assertTrue(False, "We don't support results coming in more than one part.")
            alreadyWrote = True
            if os.path.exists(outPath):
                print('File already exists, skipping write to', outPath)
            else:
                print('Writing results json to', outPath)
                with open(outPath, 'w', encoding='utf-8') as fOut:
                    fOut.write(json.dumps(theContent))
    
    return outPath
    

# helper provided for your convenience.
# can also grab an id in case the process closes and you want to recover the results from an earlier run.
def showJobStatus(id='all'):
    prefs = utils.getPrefs()
    if id == 'all':
        endpoint =  rf"https://{prefs.region}.api.cognitive.microsoft.com/speechtotext/v3.2-preview.1/transcriptions"
    else:
        endpoint = rf'https://{prefs.region}.api.cognitive.microsoft.com/speechtotext/v3.2-preview.1/transcriptions/{id}'
        
    obj = _azureHttpGet(prefs, endpoint)
    lines = textwrap.wrap(json.dumps(obj), 80)
    for line in lines:
        print(line)

if __name__ == '__main__':
    mainAskForInput()

