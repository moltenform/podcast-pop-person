# podcast-pop-person
Take a podcast episode and remove one of the speakers!

https://github.com/moltenform/podcast-pop-person
Ben Fisher, 2024
GPLv2

Prerequisites for doing the entire process:
    Python 3
    An Azure account
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
        and so on, running each script step.
        
            

