
# Ben Fisher, 2024
# https://github.com/moltenform/podcast-pop-person

# fade-in and fade-out
fadeLength = 1.0

# we'll support incoming audio in either 44.1k or 48k,
# and we'll adjust the sound effects without needing to resample the large input audio file.
defaultSampleRate = 48000

def main():
    pathIntro = input('Please enter path to an intro sound (default=intro.flac):')
    pathIntro = pathIntro or '../intro.flac'
    pathOutro = input('Please enter path to an outro sound (default=outro.flac):')
    pathOutro = pathOutro or '../outro.flac'
    pathGuitar = input('Please enter path to a marker sound played during transitions (default=sound.flac):')
    pathGuitar = pathGuitar or '../sound.flac'
    
    

def apply_fade_in_out(audio, fade_duration, sr):
   fade_in_samples = int(fade_duration * sr)
   fade_out_samples = int(fade_duration * sr)
   fade_in = np.arange(fade_in_samples)
   fade_in = fade_in / fade_in_samples
   fade_out = np.arange(fade_out_samples, 0, -1)
   fade_out = fade_out / fade_out_samples

   audio[:fade_in_samples] *= fade_in
   audio[-fade_out_samples:] *= fade_out
   return audio

def loadInputAudio(path, currentSampleRate, convertTo41):
    isMono = helper_diagnose_transcription_issue.isItMono(path)
    if isMono == 'stereo':
        print('Note, this is stereo, so it will not be as efficient.')
    
    if convertTo41:
        utils.assertEq(44100, currentSampleRate)
        audio, sr = librosa.load(path, sr=44100)
        utils.assertEq(currentSampleRate, sr, 'sample rate conversion failed for file ' + path)
    else:
        audio, sr = librosa.load(path, sr=None)
        utils.assertEq(currentSampleRate, sr, 'unexpected sample rate for file ' + path)
        
    return audio