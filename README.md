# podcast-pop-person

Take a podcast episode and remove one of the speakers!

Uses AI to differentiate between the different speakers, and then replaces one of the speakers with a soft transition sound effect. You can provide an intro sound and an outro sound. To see it in action, run `step4_build_audio.py` and provide `../sample/podcast-pop-person-demo.flac` and `../sample/sample-transcribed.json` as inputs.


```
https://github.com/moltenform/podcast-pop-person
Ben Fisher, 2024
GPLv2

Prerequisites for doing the entire process:
    Python 3
    An Azure account
        (The script is also compatible with Whisper which is open source,
        but the Azure platform had much better diarization results).
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
        and so on, running each script step from 1 to 4.
        
The script is only recommended for conversations between 2 people talking, with no music or long sound effects, 
If there are more people speaking the parameters in `step2_get_transcription.py` can be increased,
and if there is music in the input a preprocessing step may be needed to remove it first.
```

