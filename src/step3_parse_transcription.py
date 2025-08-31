# Ben Fisher, 2024
# https://github.com/moltenform/podcast-pop-person

import utils
import os
import step4_build_audio

# currently supports Whisper(open source) and Azure speech recognition
# performs some needed debouncing.

# add a threshold. this helps reduce false-positives where the system mistakenly thinks
# the current speaker is changing rapidly.
# this does mean if speaker 1 is talking and speaker 2 interjects a few short words,
# the words will be left in, for better or for worse.
minLengthInSeconds = 7
iterationsToRemoveSmallPieces = 10
markEndOfAudio = 99999

# the algorithm can run left-to-right or right-to-left,
# if prioritizeIncomingSpeaker = True it runs right-to-left, we transition to the next speaker more quickly
prioritizeIncomingSpeaker = True

# if the fade length is longer than one segment of audio that might sound odd
assert step4_build_audio.fadeLength * 2 < minLengthInSeconds


def mainAskForInput():
    audioFile = input('Path to audio file:')
    jsonFile = input('Path to json file (results of transcription):')
    results = main(audioFile, jsonFile)
    outTextFile = audioFile + '.labels.txt'
    saveToLabels(results, outTextFile)

    print('Labels saved to ' + outTextFile)
    print('You can use Audacity (version<=3.0.2) to import this label.txt')
    print('and visually confirm that the audio is being split as expected.')


def main(audioFile, jsonPath):
    _prefs = utils.getPrefs()
    items = _goThroughJson(jsonPath)
    items = combineAdjacentWithSameSpeaker(items)
    _addLengths(items)
    for _ in range(iterationsToRemoveSmallPieces):
        items = removeWithLengthsUnderThreshold(items)
        items = combineAdjacentWithSameSpeaker(items)
        _addLengths(items) # refresh the lengths, since they need to be updated

    return items


class Item:
    speaker = None
    offset = None

    def __repr__(self):
        if 'length' in dir(self):
            return f'<Item speaker={self.speaker} offset={self.offset:.2f} length={self.length:.2f}>'
        else:
            return f'<Item speaker={self.speaker} offset={self.offset:.2f}>'


# write to a .labels.txt file that can be imported in Audacity
def saveToLabels(results, outTextFile):
    with open(outTextFile, 'w', encoding='utf-8') as fOut:
        for item in results:
            fOut.write(f'{item.offset}\t{item.offset}\tsp{item.speaker}\n')


def _goThroughJson(path):
    content = open(path, encoding='utf-8').read()
    if '"speaker": "SPEAKER_00' in content:
        print('whisper-detected')
        parts = content.split('"speaker": "SPEAKER_')
        parts.pop(0)
        items = []
        for part in parts:
            item = Item()
            item.speaker = int(part.split('"')[0])
            if item.speaker == 0:
                item.speaker = 2

            assert item.speaker == 1 or item.speaker == 2
            item.offset = part.split('"timestamp": [')[1].split(',')[0]
            assert len(item.offset) > 1

            item.offset = float(item.offset)
            items.append(item)
    else:
        print('azure-detected')
        parts = content.split(', "speaker": ')
        parts.pop(0)
        items = []
        for part in parts:
            item = Item()
            item.speaker = int(part.split(',')[0])
            assert item.speaker == 1 or item.speaker == 2
            item.offset = part.split(', "offset": "')[1].split('"')[0]
            assert len(item.offset) > 1

            item.offset = parseOffset(item.offset)
            items.append(item)

    # just in case, make sure it is all sorted in order
    items.sort(key=lambda item: item.offset)
    return items


def _addLengths(items):
    for i, item in enumerate(items):
        if i == len(items) - 1:
            item.length = markEndOfAudio
        else:
            item.length = items[i + 1].offset - items[i].offset


def removeWithLengthsUnderThreshold(items):
    # can be either a false-positive, or a short interjection by the other speaker, in both cases it's good to remove it
    itemsOut = []
    skipped = 0

    if prioritizeIncomingSpeaker:
        i = len(items) - 1
        while i >= 0:
            if i != len(items) - 1 and items[i].length < minLengthInSeconds:
                skipped += 1
                itemsOut[-1].offset = items[i].offset # remember to fix-up the location
            else:
                itemsOut.append(items[i])
            i -= 1
        itemsOut.reverse()
    else:
        for i, item in enumerate(items):
            if i != 0 and i != len(items) - 1 and item.length < minLengthInSeconds:
                skipped += 1
            else:
                itemsOut.append(item)

    print('Skipped this many segments for being too short:', skipped)
    return itemsOut


def combineAdjacentWithSameSpeaker(items):
    # coalesce repeated items with the same speaker down into one.
    # the lengths will get fixed-up by a later call to addLengths.
    currentSpeaker = None
    itemsOut = []
    for item in items:
        if item.speaker != currentSpeaker:
            itemsOut.append(item)
            currentSpeaker = item.speaker

    return itemsOut


def parseOffset(s):
    s = s.strip()
    utils.assertTrue(s.startswith('PT'))
    s = s.replace('PT', '')
    alltime = 0
    if 'H' in s:
        num, s = s.split('H')
        alltime += 60 * 60 * float(num.strip())
    if 'M' in s:
        num, s = s.split('M')
        alltime += 60 * float(num.strip())
    if 'S' in s:
        num, s = s.split('S')
        alltime += float(num.strip())

    utils.assertTrue(not s)
    return alltime


if __name__ == '__main__':
    mainAskForInput()
