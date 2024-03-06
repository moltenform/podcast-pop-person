
import os
import utils
import json
import step2_get_transcription
import step3_parse_transcription
from step3_parse_transcription import parseOffset

def testParseOffset():
    def assertClose(expected, got):
        if abs(expected - got) > 0.0001:
            assert False, f'test failed, expected {expected} but got {got}'
    
    assertClose(2*60*60 + 45*60+11.48, parseOffset("PT2H45M11.48S"))
    assertClose(45*60+11.48, parseOffset("PT45M11.48S"))
    assertClose(11.48, parseOffset("PT11.48S"))
    print('testParseOffset complete')

testRemoveShortFragmentsData = [[
    '''[<Item speaker=1 offset=10.00 length=60.00>, <Item speaker=2 offset=70.00 length=30.00>, <Item speaker=1 offset=100.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT10S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT40S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT70S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT90S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT100S", "other": 123},
],
[
    '''[<Item speaker=1 offset=0.00 length=30.00>, <Item speaker=2 offset=30.00 length=30.00>, <Item speaker=1 offset=60.00 length=30.00>, <Item speaker=2 offset=90.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT0S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT30S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT60S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT90S", "other": 123},
],
[
    '''[<Item speaker=1 offset=0.00 length=30.00>, <Item speaker=2 offset=30.00 length=30.00>, <Item speaker=1 offset=60.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT0S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT30S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT60S", "other": 123},
],
[
    '''[<Item speaker=1 offset=0.00 length=60.00>, <Item speaker=2 offset=60.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT0S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT30S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT31S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT60S", "other": 123},
],
[
    '''[<Item speaker=1 offset=0.00 length=30.00>, <Item speaker=2 offset=30.00 length=30.00>, <Item speaker=1 offset=60.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT0S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT30S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT31S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT32S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT60S", "other": 123},
],
[
    '''[<Item speaker=1 offset=0.00 length=60.00>, <Item speaker=2 offset=60.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT0S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT30S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT31S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT32S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT33S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT60S", "other": 123},
],
[
    '''[<Item speaker=1 offset=0.00 length=30.00>, <Item speaker=2 offset=30.00 length=30.00>, <Item speaker=1 offset=60.00 length=99999.00>]''',
    {"other1": "ab", "speaker": 1, "offset": "PT0S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT30S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT31S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT32S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT33S", "other": 123},
    {"other1": "ab", "speaker": 2, "offset": "PT34S", "other": 123},
    {"other1": "ab", "speaker": 1, "offset": "PT60S", "other": 123},
],
]

def testRemoveShortFragments():
    tmpResults = r'temp.json'
    try:
        for test in testRemoveShortFragmentsData:
            expected = test.pop(0)
            with open(tmpResults, 'w') as fOut:
                fOut.write('aa' + json.dumps(test) + 'aa')
            results = step3_parse_transcription.main(None, tmpResults)
            utils.assertEq(str(expected), str(results))
    finally:
        if os.path.exists(tmpResults):
            os.unlink(tmpResults)


def testAll():
    testParseOffset()
    testRemoveShortFragments()


if __name__ == '__main__':
    testAll()
    