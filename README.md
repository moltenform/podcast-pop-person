# podcast-pop-person

Take a podcast episode and remove one of the speakers!

Uses AI to differentiate between the different speakers, and then replaces one of the speakers with a soft transition sound effect. You can provide an intro sound and an outro sound. To see it in action, run `step4_build_audio.py` and provide `../sample/podcast-pop-person-demo.flac` and `../sample/sample-transcribed.json` as inputs.


```
https://github.com/moltenform/podcast-pop-person
Ben Fisher, 2024
GPLv2

Since AI is still in its developments, the setup process to run the scripts takes several steps.
To see how to use the scripts, view the videos,

https://github.com/moltenform/podcast-pop-person/raw/main/docs/vid1.mp4
https://github.com/moltenform/podcast-pop-person/raw/main/docs/vid2.mp4
https://github.com/moltenform/podcast-pop-person/raw/main/docs/vid3.mp4

Alternately to watching the videos, do this:
    Get Python 3
    Get An Azure account
        (The script is also compatible with Whisper which is open source,
        but the Azure platform had much better diarization results).
        Start an instance of a Speech service
        Copy one of the keys to be later used by step1_configure.py.
    Python libraries librosa, numpy, and soundfile
        Best way to set this up:
        Install anaconda
        In an anaconda prompt,
            conda create -n my_conda_env_with_py310 python=3.10
            conda activate my_conda_env_with_py310
            python --version (should show 3.10)
            python -m pip install librosa
            python -m pip install numpy
            python -m pip install soundfile
        
    Then to run the scripts,
        conda activate my_conda_env_with_py310
        cd podcast-pop-person/src
        python ./step1_configure.py
        and so on, running each script step from step1 to step4.
        
The script is only recommended for conversations between 2 people talking,
with no music or long sound effects. If there are more people speaking,
the parameters in `step2_get_transcription.py` can be increased,
but if there is music in the input, you may need to remove it first.

Potential troubleshooting,
If there are errors regarding the endpoint,
Currently the system uses the endpoint
https://{region}.api.cognitive.microsoft.com/speechtotext/v3.2-preview.1/transcriptions
because the v3.1-preview is much cheaper. If this endpoint isn't working,
Edit step2_get_transcription.py and replace all of the references to 
api.cognitive.microsoft.com/speechtotext/v3.2-preview.1/transcriptions
with the endpoint that is seen on the same Azure page that shows the keys.

```

