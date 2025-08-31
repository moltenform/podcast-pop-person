# Ben Fisher, 2024
# https://github.com/moltenform/podcast-pop-person

import utils
import os
import itertools
import librosa
import soundfile
import numpy as np

# fade-in and fade-out
fadeLength = 1.0

# we'll support incoming audio in either 44.1k or 48k,
# and we'll optimize so that we never resample the large input audio coming in.
defaultSampleRate = 48000


def mainAskForInput():
    print('The script works best with mono files in flac or mp3 format.\n\n')
    pathMainAudio = input('Please enter path to the podcast episode audio:')
    pathJson = input('Please enter path to the transcription json file:')

    pathIntro = input('Please enter path to an intro sound (default=intro.flac):')
    pathIntro = pathIntro or '../sample/intro.flac'
    pathOutro = input('Please enter path to an outro sound (default=outro.flac):')
    pathOutro = pathOutro or '../sample/outro.flac'
    pathSoundDuringTransition = input(
        'Please enter path to a marker sound played during transitions (default=sound.flac):'
    )
    pathSoundDuringTransition = pathSoundDuringTransition or '../sample/sound.flac'

    pathMainAudio = utils.helpInterpretPath(pathMainAudio)
    pathJson = utils.helpInterpretPath(pathJson)
    pathIntro = utils.helpInterpretPath(pathIntro)
    pathOutro = utils.helpInterpretPath(pathOutro)
    pathSoundDuringTransition = utils.helpInterpretPath(pathSoundDuringTransition)

    main(pathMainAudio, pathJson, pathIntro, pathOutro, pathSoundDuringTransition)


def main(pathMainAudio, pathJson, pathIntro, pathOutro, pathSoundDuringTransition):
    buildAudioWithoutThisSpeaker(
        pathMainAudio, pathJson, pathIntro, pathOutro, pathSoundDuringTransition, 1,
        pathMainAudio + '.out.1.flac'
    )
    buildAudioWithoutThisSpeaker(
        pathMainAudio, pathJson, pathIntro, pathOutro, pathSoundDuringTransition, 2,
        pathMainAudio + '.out.2.flac'
    )


def buildAudioWithoutThisSpeaker(
    pathMainAudio, pathJson, pathIntro, pathOutro, pathSoundDuringTransition, whichToRemove,
    pathOutput
):
    import step3_parse_transcription
    itemsAll = step3_parse_transcription.main(pathMainAudio, pathJson)
    items = [item for item in itemsAll if item.speaker != whichToRemove]
    utils.assertTrue(len(items) > 0)

    origAudio, sr = librosa.load(pathMainAudio, sr=None)
    if sr == 48000:
        currentSampleRate = 48000
        convertTo44100 = False
    elif sr == 44100:
        currentSampleRate = 44100
        convertTo44100 = True
    else:
        utils.assertTrue(False, 'unsupported sample rate', sr)
        return

    soundDuringTransition = loadInputAudio(
        pathSoundDuringTransition, currentSampleRate, convertTo44100
    )
    intro = loadInputAudio(pathIntro, currentSampleRate, convertTo44100)
    outro = loadInputAudio(pathOutro, currentSampleRate, convertTo44100)

    result = intro.copy()
    for i, item in enumerate(items):
        isLast = i == len(items) - 1
        piece = getPieceOfAudio(
            origAudio, currentSampleRate, item.offset, item.offset + item.length
        )
        applyFadeInAndFadeOut(piece, fadeLength, currentSampleRate)

        result = np.append(result, piece)
        if not isLast:
            result = np.append(result, soundDuringTransition)

    result = np.append(result, outro)
    soundfile.write(pathOutput, result, currentSampleRate)


def getPieceOfAudio(origAud, currentSampleRate, startTimeRaw, endTimeRaw):
    # i chose to use librosa and soundfile for this project,
    # even though they need a few dependencies to install.
    # sox could also be used to put pieces of audio together.
    start = int(startTimeRaw * currentSampleRate)
    end = int(endTimeRaw * currentSampleRate)
    return origAud[start:end]


def applyFadeInAndFadeOut(audio, fadeDuration, currentSampleRate):
    fadeInSamples = int(fadeDuration * currentSampleRate)
    fadeOutSamples = int(fadeDuration * currentSampleRate)
    fadeIn = np.arange(fadeInSamples)
    fadeIn = fadeIn / fadeInSamples
    fadeOut = np.arange(fadeOutSamples, 0, -1)
    fadeOut = fadeOut / fadeOutSamples

    audio[:fadeInSamples] *= fadeIn
    audio[-fadeOutSamples:] *= fadeOut
    return audio


def loadInputAudio(path, currentSampleRate, convertTo44100):
    if convertTo44100:
        utils.assertEq(44100, currentSampleRate)
        audio, sr = librosa.load(path, sr=44100)
        utils.assertEq(currentSampleRate, sr, 'sample rate conversion failed for file ' + path)
    else:
        audio, sr = librosa.load(path, sr=None)
        utils.assertEq(currentSampleRate, sr, 'unsupported sample rate for file ' + path)

    return audio


if __name__ == '__main__':
    mainAskForInput()
