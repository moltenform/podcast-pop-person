# Ben Fisher, 2024
# https://github.com/moltenform/podcast-pop-person

import subprocess
import pprint
import os
import sys
import json
from shinerainsevenlib.standard import *


def getPrefs():
    if not os.path.exists('.prefs.json'):
        assertTrue(
            False, 'no .prefs.json found. wrong current directory, or run step1_configure.py'
        )

    # read prefs file from disk
    with open('.prefs.json', encoding='utf-8') as f:
        s = f.read()
        prefsDict = json.loads(s)

    # convert to bucket format, so that we can say
    # prefs.curl_path instead of prefs['curl_path']
    prefsBucket = Bucket()
    for k in prefsDict:
        setattr(prefsBucket, k, prefsDict[k])

    return prefsBucket


def run(
    listArgs,
    shell=False,
    createNoWindow=True,
    throwOnFailure=RuntimeError,
    stripText=True,
    captureOutput=True,
    silenceOutput=False
):
    kwargs = {}

    if sys.platform.startswith('win') and createNoWindow:
        kwargs['creationflags'] = 0x08000000

    retcode = -1
    stdout = None
    stderr = None

    if captureOutput:
        sp = subprocess.Popen(
            listArgs, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
        )

        comm = sp.communicate()
        stdout = comm[0]
        stderr = comm[1]
        retcode = sp.returncode
        if stripText:
            stdout = stdout.rstrip()
            stderr = stderr.rstrip()
    else:
        assertTrue(False, 'not supported, see the full ben_python_common.')

    if throwOnFailure and retcode != 0:
        if throwOnFailure is True:
            throwOnFailure = RuntimeError

        exceptionText = 'retcode is not 0 for process ' + \
            str(listArgs) + '\nretcode was ' + str(retcode) + \
            '\nstdout was ' + str(stdout) + \
            '\nstderr was ' + str(stderr)
        raise throwOnFailure(srss.getPrintable(exceptionText))

    return retcode, stdout, stderr


def helpInterpretPath(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]

    return s
